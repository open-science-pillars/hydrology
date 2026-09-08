# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Confront a satellite river elevation with a gauge, on changes, and say
what the level difference is without calling it a bias.

Why changes are the confrontation and the level is not. The satellite
reports elevation against a geoid model and the gauge against a national
vertical datum, and the offset between those two surfaces is not
published for this pair. A level difference therefore contains a real
signal plus an uncited constant, which makes it uninterpretable rather
than merely uncertain. A change over an interval is insensitive to any
constant offset, so it means something without the citation. This tool
scores the changes and reports the level difference beside them, labelled.

The scores follow the form the ocean confrontations use: a bias, a root
mean square difference, a correlation, and each with a sampling interval
computed under a lag-1 autocorrelation model rather than from the raw
count, because consecutive passes are not independent. The intervals
carry sampling uncertainty only. They do not carry the satellite's own
uncertainty, which the product publishes per pass and which this receipt
reports separately, nor the gauge's.

What it refuses:

- **A pass with no gauge reading inside the tolerance.** The pairing is
  a choice and the tolerance is stated; a pass that finds nothing is
  dropped by name and counted, never matched to the nearest reading at
  any distance.
- **A confrontation over fewer than ten pairs**, which is not a score.
- **The word bias for the level difference.** It is reported as a level
  difference containing an uncited datum offset, in that language.

Usage:
  uv run verification/fixtures/load_swot_confrontation.py \
      --inputs verification/fixtures/confrontation/swot_gauge_baton_rouge_2024.json \
      --tolerance-minutes 15 --out receipt.json
"""
import argparse
import datetime as dt
import hashlib
import json
import math
import statistics
import sys
from pathlib import Path

FT_M = 0.3048
MIN_PAIRS = 10


def die(msg):
    print(f"REFUSED: {msg}", file=sys.stderr)
    raise SystemExit(2)


def t(s):
    return dt.datetime.fromisoformat(s.rstrip("Z"))


def lag1_neff(x):
    """Effective sample size under a lag-1 autocorrelation model, capped at
    the count.

    Passes a fortnight apart on a river are not independent draws, and a
    count of them overstates what the sample knows. But the formula runs
    the other way too: a NEGATIVELY autocorrelated series returns an
    effective size larger than its own length, and differencing a series
    induces exactly that, so a change series reliably reports more
    information than it contains. Capping at n keeps the interval
    conservative and stops a receipt claiming an effective sample of 130
    from 49 changes."""
    n = len(x)
    if n < 3:
        return float(n)
    m = statistics.fmean(x)
    num = sum((x[i] - m) * (x[i - 1] - m) for i in range(1, n))
    den = sum((v - m) ** 2 for v in x)
    if den <= 0:
        return float(n)
    r = max(-0.99, min(0.99, num / den))
    return max(2.0, min(float(n), n * (1 - r) / (1 + r)))


def interval(x):
    """A 95 per cent sampling interval on the mean, with the effective
    sample size in place of the count."""
    n_eff = lag1_neff(x)
    m = statistics.fmean(x)
    if len(x) < 2:
        return m, None, None, n_eff
    se = statistics.stdev(x) / math.sqrt(n_eff)
    return m, m - 1.96 * se, m + 1.96 * se, n_eff


def pearson(a, b):
    ma, mb = statistics.fmean(a), statistics.fmean(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    da = math.sqrt(sum((x - ma) ** 2 for x in a))
    db = math.sqrt(sum((y - mb) ** 2 for y in b))
    return num / (da * db) if da and db else None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--inputs", required=True, type=Path)
    ap.add_argument("--tolerance-minutes", type=int, default=15)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()

    doc = json.loads(a.inputs.read_text())
    sat = doc["satellite"]
    gauge = doc["gauge"]
    datum_alt_ft = gauge.get("gauge_datum_altitude_ft") or 0.0
    tol = dt.timedelta(minutes=a.tolerance_minutes)

    pairs, unmatched = [], []
    for p, readings in zip(sat["rows"], gauge["readings_by_pass"]):
        if p["wse_m"] is None:
            unmatched.append({"time": p["time"], "why": "the pass carries no elevation"})
            continue
        when = t(p["time"])
        near = [r for r in readings if abs(t(r["t"]) - when) <= tol]
        if not near:
            unmatched.append({"time": p["time"],
                              "why": f"no gauge reading within {a.tolerance_minutes} minutes"})
            continue
        best = min(near, key=lambda r: abs(t(r["t"]) - when))
        pairs.append({
            "time": p["time"],
            "gauge_time": best["t"],
            "offset_s": abs((t(best["t"]) - when).total_seconds()),
            "satellite_m": p["wse_m"],
            "satellite_u_m": p["wse_u_m"],
            "gauge_stage_ft": best["stage_ft"],
            "gauge_elevation_m": (best["stage_ft"] + datum_alt_ft) * FT_M,
            "approval": best["approval"],
        })
    if len(pairs) < MIN_PAIRS:
        die(f"{len(pairs)} matched pairs is not a confrontation; at least {MIN_PAIRS} are needed "
            "before a score means anything")

    pairs.sort(key=lambda x: x["time"])
    level = [p["satellite_m"] - p["gauge_elevation_m"] for p in pairs]
    lm, llo, lhi, lneff = interval(level)

    # Changes between consecutive matched passes. A pass pair whose gauge
    # barely moved carries no information about agreement and would inflate
    # a correlation, so the series is reported whole and the correlation is
    # computed over the changes as they are.
    ch_sat = [pairs[i]["satellite_m"] - pairs[i - 1]["satellite_m"] for i in range(1, len(pairs))]
    ch_gau = [pairs[i]["gauge_elevation_m"] - pairs[i - 1]["gauge_elevation_m"]
              for i in range(1, len(pairs))]
    err = [s - g for s, g in zip(ch_sat, ch_gau)]
    em, elo, ehi, eneff = interval(err)
    rmsd = math.sqrt(sum(e * e for e in err) / len(err))
    r = pearson(ch_sat, ch_gau)
    spread = statistics.stdev(ch_gau)

    receipt = {
        "pair": doc["pair"],
        "window": doc["window"],
        "collection_named": sat["collection_named"],
        "matching": {"tolerance_minutes": a.tolerance_minutes,
                     "passes_offered": len(sat["rows"]),
                     "pairs": len(pairs),
                     "unmatched": unmatched,
                     "max_offset_s": max(p["offset_s"] for p in pairs)},
        "approval": {"values_used": sorted({p["approval"] for p in pairs}),
                     "note": gauge["approval_note"]},
        "confrontation_on_changes": {
            "n": len(err),
            "mean_error_m": round(em, 4),
            "mean_error_95pct": [round(elo, 4), round(ehi, 4)] if elo is not None else None,
            "effective_sample_size": round(eneff, 1),
            "rmsd_m": round(rmsd, 4),
            "correlation": round(r, 4) if r is not None else None,
            "gauge_change_spread_m": round(spread, 4),
            "rmsd_over_spread": round(rmsd / spread, 4) if spread else None,
            "why_changes": ("a change over an interval is insensitive to a constant datum "
                            "offset, so it can be scored without citing one"),
        },
        "level_difference_not_a_bias": {
            "n": len(level),
            "mean_m": round(lm, 4),
            "mean_95pct": [round(llo, 4), round(lhi, 4)] if llo is not None else None,
            "effective_sample_size": round(lneff, 1),
            "sd_m": round(statistics.stdev(level), 4),
            "min_m": round(min(level), 4), "max_m": round(max(level), 4),
            "statement": ("this is a level difference containing an uncited datum offset, not a "
                          "bias: the satellite is referenced to a geoid model and the gauge to "
                          f"{gauge.get('datum')}, and the relationship between them is not "
                          "published for this pair"),
        },
        "satellite_reported_uncertainty_m": {
            "median": round(statistics.median([p["satellite_u_m"] for p in pairs
                                               if p["satellite_u_m"] is not None]), 4)
            if any(p["satellite_u_m"] is not None for p in pairs) else None,
            "note": ("the product's own per-pass uncertainty, reported here and NOT folded into "
                     "the intervals above, which are sampling intervals only"),
        },
        "intervals_are": ("sampling intervals under a lag-1 autocorrelation model, carrying "
                          "neither the satellite's published uncertainty nor the gauge's"),
        "pairs": pairs,
        "generated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_fixture": {"path": a.inputs.name,
                           "sha256": hashlib.sha256(a.inputs.read_bytes()).hexdigest()},
    }
    text = json.dumps(receipt, indent=1)
    if a.out:
        a.out.write_text(text)
        print(f"{a.out}: {len(pairs)} pairs, {len(err)} changes", file=sys.stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
