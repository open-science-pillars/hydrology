# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas"]
# ///
"""Annual peaks out of the Water Data API and into the file the flood
frequency program reads, with nothing invented on the way.

What this does and does not do. It reads one gauge's peak record, writes
a WATSTORE peak file, and computes a screening fit. It does not compute a
Bulletin 17C estimate: that involves expected moments, a regional skew,
historic information and censored values, none of which are implemented
here. The screening fit is labelled screening in every field it writes,
carries an interval on every quantile, and refuses to speak at all where
the record breaks its own assumptions. The frequency answer comes from
PeakFQ, which the analyst runs; this reads its output back.

Three things about the record that the file format makes unavoidable:

**One response holds two series.** The peaks collection returns the
annual peak discharge (parameter 00060, cubic feet per second) and the
annual peak stage (00065, feet) for the same gauge, interleaved, with
the same column names. They are not the same event: the collection's own
description says the peak flow may not occur when the peak water level
does. So `--parameter` is required and this script refuses to run
without it.

**The date can be unknown, and the record still counts.** A historic
peak may carry a null month, a null day or both, and the qualifiers say
so. Those rows are the largest floods in most long records, they are
exactly what a frequency analysis carries as historic information, and a
loader that filters on a parsable date silently drops them. They are
carried here, and the file leaves the month and day columns blank, which
is what the format specifies.

**The qualifiers change the answer.** PeakFQ applies special handling to
codes 3, 4, 6, 7, 8 and C: peaks flagged regulated (6) or urbanized (C)
are excluded from the analysis unless the station option record asks for
them, and a historic peak (7) is only used when a historic period length
is supplied. A qualifier mapped wrongly does not raise an error anywhere;
it changes which peaks enter the fit.

Usage:
  uv run verification/fixtures/load_peaks.py --peaks verification/fixtures/peaks/peaks_03451500.json \
      --parameter 00060 --watstore out.pkf --out receipt.json
  uv run verification/fixtures/load_peaks.py --peaks ... --parameter 00060 --screening-fit
"""
import argparse
import datetime as dt
import hashlib
import json
import math
import random
import statistics
import sys
from pathlib import Path

# The qualification codes, derived rather than recalled: for 42 gauges the
# peaks collection's rows were aligned to the WATSTORE file the agency's
# own writer produced for the same gauge, and the mapping below is what
# rows carrying exactly one qualifier on each side showed, checked against
# every multiple-code row (see the peaks concept for the measurement).
# Codes 1 through 9, A, B, C, D and E are defined in the PeakFQ user's
# manual (Techniques and Methods 4-B4, table B.4). Bd, Bm, R and F are
# not in that table: the agency's writer emits them, so an export that
# means to be read the way the agency's file is read emits them too.
QUALIFIER_CODES = {
    "MAXDAILYMEAN": "1",       # discharge is a maximum daily average
    "ESTIMATED": "2",          # discharge is an estimate
    "DAMFAILURE": "3",         # discharge affected by dam failure
    "LESSTHAN": "4",           # discharge less than the indicated value
    "UNKNOWNREGULATION": "5",  # affected to an unknown degree by regulation
    "REGULATED": "6",          # affected by regulation or diversion
    "HISTORIC": "7",           # a historic peak, outside the systematic record
    "GREATERTHAN": "8",        # discharge actually greater than indicated
    "EVENT": "9",              # snowmelt, hurricane, ice jam or debris dam
    "YEARUNKNOWN": "A",        # year of occurrence unknown or not exact
    "DAYUNKNOWN": "Bd",        # the manual's B, narrowed by the agency writer
    "MONTHUNKNOWN": "Bm",      # the manual's B, narrowed by the agency writer
    "URBAN": "C",              # record affected by urbanization or mining
    "OTHERAGENCY": "F",        # not in the manual's table
    "REVISED": "R",            # not in the manual's table
}
# Measured on the same 42 gauges: qualifiers the collection uses that have
# no WATSTORE peak code at all. They come from the wider observation
# vocabulary rather than the peak-code table, and an export states them in
# its receipt rather than inventing a character for them.
NO_LEGACY_CODE = {
    "BACKWATER", "BLWMIN", "DATUMCHANGE", "DEBRIS", "DIFFDATUM", "DISCONTINUED",
    "DRY", "EQUIP", "FLOOD", "FORCEINTERPOLATION", "GHNOTASSCPKQ", "ICE",
    "NOTMAXGH", "OPPORTUNISTIC", "PARTIAL_RECORD", "RATINGDEV", "TEST",
    "UNAVAIL", "ZEROFLOW",
}
# PeakFQ acts on these rather than ignoring them (manual, table B.3 and the
# station-option K and H codes).
ACTED_ON = {"3", "4", "6", "7", "8", "C"}
EXCLUDED_WITHOUT_OPTION = {"6": "regulated", "C": "urbanized"}


def die(msg):
    print(f"REFUSED: {msg}", file=sys.stderr)
    raise SystemExit(2)


def codes_for(qualifiers):
    """Map a row's qualifier list to WATSTORE codes, in the order the
    agency's writer uses (ascending by code, so 2 before 7 before Bd)."""
    mapped, unmapped = [], []
    for q in qualifiers or []:
        if q in QUALIFIER_CODES:
            mapped.append(QUALIFIER_CODES[q])
        else:
            unmapped.append(q)
    return sorted(set(mapped)), sorted(set(unmapped))


def watstore_records(site, name, rows, meta):
    """The station header records and one type 3 record per peak, per the
    PeakFQ user's manual, table B.2 and table B.4."""
    def col(line, start, text):
        """Place text so it begins at column `start` (1-indexed)."""
        line = line.ljust(start - 1)
        return line + text

    sid = site.replace("USGS-", "")
    out = []
    z = col("Z", 33, "USGS")
    out.append(z)

    lat, lon = meta.get("latitude"), meta.get("longitude")
    loc = ""
    if lat is not None and lon is not None:
        def dms(v, deg_width):
            # Truncated, not rounded, which is what the agency's own
            # writer does: 36.8643333 is written 365151 and not 365152.
            v = abs(v)
            d = int(v); m = int((v - d) * 60); s = int((((v - d) * 60) - m) * 60)
            return f"{d:0{deg_width}d}{m:02d}{s:02d}"
        loc = dms(lat, 2) + dms(lon, 3) + "00"
    h = col("H", 2, sid.ljust(15))
    h = col(h, 17, loc.ljust(15))
    h = col(h, 39, "SW")
    if meta.get("huc"):
        h = col(h, 41, str(meta["huc"])[:8].ljust(8))
    if meta.get("drainage_area") is not None:
        h = col(h, 49, f"{meta['drainage_area']:g}".ljust(7))
    if meta.get("altitude") is not None:
        h = col(h, 63, f"{meta['altitude']:8.2f}")
    out.append(h.rstrip())
    out.append(col(col("N", 2, sid.ljust(15)), 17, (name or "")[:48]))

    for r in rows:
        line = col("3", 2, sid.ljust(15))
        # The manual: the calendar year where a month is given, the water
        # year where the month column is blank.
        _yr = r["year"] if r.get("month") else (r.get("water_year") or r["year"])
        line = col(line, 17, f"{int(_yr):4d}")
        line = col(line, 21, f"{int(r['month']):02d}" if r.get("month") else "  ")
        line = col(line, 23, f"{int(r['day']):02d}" if r.get("day") else "  ")
        line = col(line, 25, f"{r['value']:7.0f}" if r.get("value") is not None else " " * 7)
        line = col(line, 32, "".join(r["codes"]).ljust(12))
        # Columns 44 to 55 hold the gage height that went with this peak
        # discharge and its codes. They are left blank: the peak stage
        # series is a different series, on its own dates and its own datum
        # history, and some of its rows say outright that the height is not
        # the one associated with the peak discharge. The frequency program
        # ignores this range for a peak record.
        if r.get("gage_height") is not None:
            line = col(line, 44, f"{r['gage_height']:8.2f}")
        if r.get("peak_since"):
            line = col(line, 56, f"{int(r['peak_since']):4d}")
        out.append(line.rstrip())
    return out


def screening_fit(values, seed=20260907, trials=2000, aeps=(0.5, 0.1, 0.04, 0.02, 0.01, 0.002)):
    """A log-Pearson III fit by method of moments, with a bootstrap
    interval. This is a screening number and is labelled one everywhere it
    appears: no expected moments, no regional skew, no historic
    adjustment, no censored-value handling, so it is not a Bulletin 17C
    estimate and the difference is not cosmetic."""
    logs = [math.log10(v) for v in values]
    n = len(logs)
    if n < 10:
        die(f"a fit over {n} peaks is not a screening number, it is noise; "
            "the guidelines want a systematic record of at least 10 years")

    def moments(xs):
        m = statistics.fmean(xs)
        s = statistics.stdev(xs)
        k = len(xs)
        g = (k * sum((x - m) ** 3 for x in xs)) / ((k - 1) * (k - 2) * s ** 3) if k > 2 and s > 0 else 0.0
        return m, s, g

    def quantile(m, s, g, aep):
        z = statistics.NormalDist().inv_cdf(1 - aep)
        if abs(g) < 1e-6:
            k = z
        else:  # Wilson-Hilferty, the approximation the guidelines use
            k = (2 / g) * ((1 + g * z / 6 - g * g / 36) ** 3 - 1)
        return 10 ** (m + k * s)

    m, s, g = moments(logs)
    rng = random.Random(seed)
    boot = {a: [] for a in aeps}
    for _ in range(trials):
        sample = [logs[rng.randrange(n)] for _ in range(n)]
        try:
            bm, bs, bg = moments(sample)
            for a in aeps:
                boot[a].append(quantile(bm, bs, bg, a))
        except statistics.StatisticsError:
            continue
    rows = []
    for a in aeps:
        b = sorted(boot[a])
        if len(b) < trials // 2:
            die("the bootstrap did not converge, so no interval can be reported, "
                "so no quantile is reported either")
        rows.append({
            "annual_exceedance_probability": a,
            "return_period_years": round(1 / a),
            "screening_estimate_cfs": round(quantile(m, s, g, a), 1),
            "interval_90pct_cfs": [round(b[int(0.05 * len(b))], 1), round(b[int(0.95 * len(b))], 1)],
            "label": "screening",
        })
    return {"method": ("log-Pearson III, method of moments on log10 peaks, station skew, "
                       "Wilson-Hilferty frequency factors; interval from a nonparametric "
                       "bootstrap of the systematic peaks"),
            "is_bulletin_17c": False,
            "not_implemented": ["expected moments", "regional skew and its weighting",
                                "historic period adjustment", "censored (less-than) values",
                                "outlier tests", "confidence limits per the guidelines"],
            "n_systematic": n, "log_mean": round(m, 5), "log_sd": round(s, 5),
            "log_skew": round(g, 5), "bootstrap_trials": trials, "seed": seed,
            "quantiles": rows}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--peaks", required=True, type=Path, help="frozen peaks fixture JSON")
    ap.add_argument("--parameter", required=True, choices=["00060", "00065"],
                    help="00060 discharge or 00065 stage; required because one response holds both")
    ap.add_argument("--watstore", type=Path, help="write the WATSTORE peak file here")
    ap.add_argument("--screening-fit", action="store_true")
    ap.add_argument("--acknowledge-regulation", action="store_true",
                    help="fit anyway over a record carrying regulation or urbanization codes")
    ap.add_argument("--drop-historic", action="store_true",
                    help="drop historic and censored peaks from the screening fit and say so")
    ap.add_argument("--out", type=Path, help="receipt JSON path")
    a = ap.parse_args()

    doc = json.loads(a.peaks.read_text())
    site = doc["monitoring_location"]["monitoring_location_id"]
    name = doc["monitoring_location"].get("monitoring_location_name", "")
    all_rows = doc["rows"]
    rows_p = [r for r in all_rows if r.get("parameter_code") == a.parameter]
    other = [r for r in all_rows if r.get("parameter_code") != a.parameter]
    if not rows_p:
        die(f"the fixture holds no {a.parameter} rows for {site}")

    unit = {r.get("unit_of_measure") for r in rows_p}
    if len(unit) > 1:
        die(f"the {a.parameter} rows carry more than one unit ({sorted(unit)}), which no "
            "single series can be")

    prepared, unmapped_seen, partial, acted = [], {}, [], {}
    for r in sorted(rows_p, key=lambda x: (x.get("water_year") or 0)):
        codes, unmapped = codes_for(r.get("qualifier"))
        for u in unmapped:
            unmapped_seen[u] = unmapped_seen.get(u, 0) + 1
        for c in codes:
            if c in ACTED_ON:
                acted[c] = acted.get(c, 0) + 1
        if r.get("month") is None or r.get("day") is None:
            partial.append(r.get("water_year"))
        prepared.append({
            "water_year": r.get("water_year"), "year": r.get("year"),
            "month": r.get("month"), "day": r.get("day"),
            "value": float(r["value"]) if r.get("value") is not None else None,
            "codes": codes, "unmapped": unmapped,
            "peak_since": r.get("peak_since"), "gage_height": None,
        })

    meta = {}
    ml = doc["monitoring_location"]
    geom = ml.get("geometry")
    if isinstance(geom, (list, tuple)) and len(geom) == 2:
        meta["longitude"], meta["latitude"] = float(geom[0]), float(geom[1])
    for k, src in (("huc", "hydrologic_unit_code"), ("drainage_area", "drainage_area"),
                   ("altitude", "altitude")):
        if ml.get(src) is not None:
            meta[k] = ml[src]

    written = None
    if a.watstore:
        lines = watstore_records(site, name, prepared, meta)
        a.watstore.write_text("\n".join(lines) + "\n")
        written = {"path": str(a.watstore), "records": len(lines),
                   "type_3_records": sum(1 for l in lines if l.startswith("3")),
                   "sha256": hashlib.sha256(a.watstore.read_bytes()).hexdigest()}

    fit = None
    if a.screening_fit:
        if a.parameter != "00060":
            die("a flood frequency fit is a fit to discharge; a stage series has its own "
                "datum history and is not interchangeable with one")
        regulated = {c: n for c, n in acted.items() if c in EXCLUDED_WITHOUT_OPTION}
        if regulated and not a.acknowledge_regulation:
            names = ", ".join(f"{n} peaks {EXCLUDED_WITHOUT_OPTION[c]}" for c, n in sorted(regulated.items()))
            die(f"this record carries {names}. A frequency curve fitted through them describes "
                "the operating rule, not the flood hazard, and the frequency program excludes "
                "such peaks unless its station option record asks for them. Pass "
                "--acknowledge-regulation to fit anyway and have the receipt say so")
        censored = [p for p in prepared if {"4", "8"} & set(p["codes"])]
        historic = [p for p in prepared if "7" in p["codes"]]
        if (historic or censored) and not a.drop_historic:
            die(f"this record carries {len(historic)} historic and {len(censored)} censored "
                "peaks. Historic information enters a frequency analysis through a historic "
                "period length and a threshold, and censored values through an expected "
                "moments fit; neither is implemented here. Pass --drop-historic to fit the "
                "systematic record alone and have the receipt say what was dropped and which "
                "way it biases the answer")
        used = [p for p in prepared
                if p["value"] is not None and not ({"4", "7", "8"} & set(p["codes"]))]
        fit = screening_fit([p["value"] for p in used])
        fit["dropped"] = {
            "historic": [p["water_year"] for p in historic],
            "censored": [p["water_year"] for p in censored],
            "bias": ("dropping historic peaks removes the largest floods in the record, so a "
                     "screening curve fitted without them sits low at the rare end; the "
                     "direction is known and the size is not"),
        }
        if regulated:
            fit["regulation_acknowledged"] = {EXCLUDED_WITHOUT_OPTION[c]: n
                                              for c, n in sorted(regulated.items())}

    receipt = {
        "monitoring_location": ml,
        "parameter": a.parameter,
        "unit": sorted(unit)[0],
        "rows_used": len(prepared),
        "rows_in_fixture_other_parameters": {
            "count": len(other),
            "parameters": sorted({r.get("parameter_code") for r in other}),
            "note": ("the response holds more than one series; they are not the same event "
                     "and are never concatenated"),
        },
        "water_years": [min(p["water_year"] for p in prepared),
                        max(p["water_year"] for p in prepared)],
        "missing_water_years": sorted(
            set(range(min(p["water_year"] for p in prepared),
                      max(p["water_year"] for p in prepared) + 1))
            - {p["water_year"] for p in prepared}),
        "partial_date_water_years": partial,
        "qualifier_codes_acted_on_by_the_frequency_program": acted,
        "qualifiers_with_no_watstore_code": unmapped_seen,
        "watstore": written,
        "screening_fit": fit,
        "source_fixture": {"path": str(a.peaks),
                           "sha256": hashlib.sha256(a.peaks.read_bytes()).hexdigest(),
                           "retrieved": doc.get("retrieved")},
        "generated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    text = json.dumps(receipt, indent=1, default=str)
    if a.out:
        a.out.write_text(text)
        print(f"{a.out}: {len(prepared)} {a.parameter} rows, "
              f"{len(partial)} with a partial date", file=sys.stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
