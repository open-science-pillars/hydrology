# /// script
# requires-python = ">=3.11"
# dependencies = ["dataretrieval>=1.3", "pandas", "requests"]
# ///
"""Freeze one reach-gauge pair for a confrontation: the satellite passes,
the gauge readings around each of them, and everything needed to say what
was compared with what.

Three things this keeps that a table of matched values would lose.

**The collection is named, not defaulted.** Hydrocron picks a collection
when the caller does not, and the default has moved between product
versions that differ by metres at this reach. Every request here names
one, and the fixture records which.

**The gauge readings around each pass, not only the nearest.** The
satellite sees an instant and the gauge reports every fifteen minutes, so
the pairing is a choice. Freezing a window either side of each pass keeps
the choice reproducible and lets a different tolerance be tried without
refetching.

**The approval status of every gauge value.** At this gauge the daily
record is approved only through 2022 while the satellite record begins in
2023, so a confrontation over the overlap is against provisional values.
That is a fact about the comparison, not a footnote, and it rides in the
fixture.

Usage:
  uv run verification/fixtures/fetch_confrontation_fixtures.py \
      --reach 74210000331 --gauge 07374000 \
      --start 2024-01-01 --end 2024-12-31 --label baton_rouge_2024 \
      --out verification/fixtures/confrontation
"""
import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

import pandas as pd
import requests
from dataretrieval import waterdata

HYDROCRON = "https://soto.podaac.earthdatacloud.nasa.gov/hydrocron/v1/timeseries"
UA = {"User-Agent": "open-science-pillars-hydrology/0.6 (confrontation fixture)"}
FT_M = 0.3048
COLLECTIONS = {"D": "SWOT_L2_HR_RiverSP_reach_D", "2.0": "SWOT_L2_HR_RiverSP_reach_2.0"}


def log(m):
    print(m, file=sys.stderr, flush=True)


def swot(reach, start, end, collection):
    p = {"feature": "Reach", "feature_id": reach,
         "start_time": f"{start}T00:00:00Z", "end_time": f"{end}T23:59:59Z",
         "fields": "reach_id,time_str,wse,wse_u,width,slope,reach_q,dark_frac,ice_clim_f",
         "collection_name": collection}
    r = requests.get(HYDROCRON, params=p, timeout=300, headers=UA)
    r.raise_for_status()
    body = r.json()
    rows = []
    for f in body["results"]["geojson"]["features"]:
        pr = f["properties"]
        t = pr.get("time_str")
        if not t or "no_data" in str(t):
            continue
        try:
            when = dt.datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            continue
        def num(k):
            try:
                v = float(pr.get(k))
                return None if v < -1e10 else v
            except (TypeError, ValueError):
                return None
        rows.append({"time": when.isoformat() + "Z", "wse_m": num("wse"),
                     "wse_u_m": num("wse_u"), "width_m": num("width"),
                     "slope": num("slope"), "reach_q": pr.get("reach_q"),
                     "dark_frac": num("dark_frac"), "ice_clim_f": pr.get("ice_clim_f")})
    return sorted(rows, key=lambda x: x["time"]), r.url


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--reach", required=True)
    ap.add_argument("--gauge", required=True)
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--window-minutes", type=int, default=60,
                    help="gauge readings kept either side of each pass")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)

    passes, url_d = swot(a.reach, a.start, a.end, COLLECTIONS["D"])
    other, url_c = swot(a.reach, a.start, a.end, COLLECTIONS["2.0"])
    log(f"  Version D: {len(passes)} passes with a time and an elevation")
    log(f"  Version 2.0: {len(other)} passes, kept for the version comparison")

    ml, _ = waterdata.get_monitoring_locations(monitoring_location_id=f"USGS-{a.gauge}",
                                               skip_geometry=True)
    m = ml.iloc[0]
    site = {k: (None if pd.isna(m[k]) else m[k]) for k in
            ("monitoring_location_name", "altitude", "altitude_accuracy",
             "altitude_method_name", "vertical_datum", "vertical_datum_name",
             "drainage_area", "time_zone_abbreviation") if k in ml.columns}

    iv, _ = waterdata.get_continuous(
        monitoring_location_id=f"USGS-{a.gauge}", parameter_code="00065",
        statistic_id="00011", time=f"{a.start}T00:00:00Z/{a.end}T23:59:59Z",
        skip_geometry=True)
    iv["t"] = pd.to_datetime(iv["time"], utc=True).dt.tz_convert(None)
    iv = iv.sort_values("t").reset_index(drop=True)
    log(f"  gauge: {len(iv)} instantaneous readings")

    win = dt.timedelta(minutes=a.window_minutes)
    kept = []
    for p in passes:
        t = dt.datetime.fromisoformat(p["time"].rstrip("Z"))
        sub = iv[(iv["t"] >= t - win) & (iv["t"] <= t + win)]
        kept.append([{"t": r["t"].isoformat() + "Z", "stage_ft": float(r["value"]),
                      "approval": r.get("approval_status"),
                      "qualifiers": sorted(r["qualifier"]) if isinstance(r.get("qualifier"), list) else None}
                     for _, r in sub.iterrows()])
    n_readings = sum(len(k) for k in kept)
    approvals = sorted({x["approval"] for k in kept for x in k})

    out = {
        "pair": {"reach_id": a.reach, "gauge": f"USGS-{a.gauge}", "site": site},
        "window": {"start": a.start, "end": a.end},
        "satellite": {
            "service": "PO.DAAC Hydrocron",
            "collection_named": COLLECTIONS["D"],
            "collection_note": ("the collection is named on every request; the service picks one "
                                "when the caller does not, and the default has moved between "
                                "versions that differ by metres at this reach"),
            "request_url": url_d.split("?")[0],
            "elevation_reference": ("water surface elevation against a geoid model, as the "
                                    "product documents it; this is not a national vertical datum"),
            "passes": len(passes),
            "rows": passes,
        },
        "satellite_other_version": {
            "collection_named": COLLECTIONS["2.0"], "passes": len(other), "rows": other,
            "why": "kept so the version step can be recomputed rather than quoted",
        },
        "gauge": {
            "parameter": "00065",
            "parameter_name": "Gage height, feet above the gauge datum",
            "statistic": "00011",
            "datum": site.get("vertical_datum"),
            "gauge_datum_altitude_ft": site.get("altitude"),
            "elevation_note": ("stage is height above the gauge datum, so an elevation is stage "
                               "plus the datum altitude; at this gauge the datum sits at 0.00 ft "
                               "so the two coincide, which is a property of this site and not a "
                               "general rule"),
            "approval_present": approvals,
            "approval_note": ("the daily record at this gauge is approved only through 2022 and "
                              "the satellite record begins in 2023, so the overlap is against "
                              "provisional values"),
            "window_minutes": a.window_minutes,
            "readings": n_readings,
            "readings_by_pass": kept,
        },
        "unit_note": f"stage is feet, satellite elevation is metres; 1 ft = {FT_M} m",
        "retrieved": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "fetch_script": "verification/fixtures/fetch_confrontation_fixtures.py",
        "license": {"satellite": "NASA data, public (EOSDIS data use guidance)",
                    "gauge": "US Government public domain"},
    }
    p = a.out / f"swot_gauge_{a.label}.json"
    p.write_text(json.dumps(out, indent=1))
    log(f"{p}: {len(passes)} passes, {n_readings} gauge readings, "
        f"approvals {approvals}, {p.stat().st_size/1e3:.1f} kB")


if __name__ == "__main__":
    main()
