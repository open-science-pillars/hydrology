# /// script
# requires-python = ">=3.11"
# dependencies = ["dataretrieval>=1.3", "pandas", "requests"]
# ///
"""Freeze one gauge's annual peak record, and beside it the WATSTORE file
the agency's own writer produces for the same gauge.

Why both. The peaks collection on the Water Data API serves the record;
it does not serve the fixed-width peak file that flood-frequency software
reads. The legacy Water Services host still does, at
`nwis.waterdata.usgs.gov/nwis/peak?format=hn2`, and that host is being
decommissioned in a window from 2026-11 to 2027-02. So for as long as
both exist, the agency's own file is the reference an export can be
checked against, and freezing it now keeps that check available after the
writer is gone. Every fixture here carries both.

The whole record is kept, both parameters and every qualifier, because
the traps live in the rows a filter would drop: the historic peaks with
no month or day, the stage series that is not the discharge series, and
the qualifier codes that say the record is not what a frequency analysis
assumes. The site's time zone is kept beside them, because the two
services do not agree on what day a peak fell on and the difference
follows the clock.

Usage:
  uv run verification/fixtures/fetch_peaks_fixtures.py --site 03451500 \
      --out verification/fixtures/peaks
"""
import argparse
import datetime as dt
import hashlib
import json
import sys
import time
from pathlib import Path

import pandas as pd
import requests
from dataretrieval import waterdata

LEGACY = "https://nwis.waterdata.usgs.gov/nwis/peak"
UA = {"User-Agent": "open-science-pillars-hydrology/0.6 (peaks fixture)"}


def log(m):
    print(m, file=sys.stderr, flush=True)


def clean(v):
    if isinstance(v, float) and pd.isna(v):
        return None
    if isinstance(v, (pd.Timestamp, dt.datetime, dt.date)):
        return v.isoformat()
    if isinstance(v, (list, tuple)):
        return sorted(str(x) for x in v)
    if hasattr(v, "item"):
        return v.item()
    return v


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--site", required=True, help="site number without the agency prefix")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--note", default="", help="why this gauge is in the fixture set")
    a = ap.parse_args()
    sid = f"USGS-{a.site}"
    a.out.mkdir(parents=True, exist_ok=True)

    ml, _ = waterdata.get_monitoring_locations(monitoring_location_id=sid, skip_geometry=False)
    if ml.empty:
        raise SystemExit(f"no monitoring location for {sid}")
    site = {k: clean(ml.iloc[0][k]) for k in
            ("monitoring_location_id", "monitoring_location_name", "drainage_area",
             "contributing_drainage_area", "state_name", "county_name",
             "hydrologic_unit_code", "altitude", "vertical_datum_name",
             "time_zone_abbreviation", "uses_daylight_savings", "geometry")
            if k in ml.columns}

    df, _ = waterdata.get_peaks(monitoring_location_id=sid, skip_geometry=True)
    if df.empty:
        raise SystemExit(f"no peaks for {sid}")
    df = df.sort_values(["parameter_code", "water_year"])
    rows = [{k: clean(r[k]) for k in df.columns if k != "peak_id"} for _, r in df.iterrows()]

    r = requests.get(LEGACY, params={"site_no": a.site, "agency_cd": "USGS", "format": "hn2"},
                     timeout=180, headers=UA)
    r.raise_for_status()
    ref = a.out / f"watstore_{a.site}_reference.txt"
    ref.write_text(r.text)
    n3 = sum(1 for l in r.text.splitlines() if l.startswith("3"))

    by_param = df.groupby("parameter_code").size().to_dict()
    out = {
        "monitoring_location": site,
        "collection": "peaks",
        "endpoint": "https://api.waterdata.usgs.gov/ogcapi/v0/collections/peaks/items",
        "client": "dataretrieval waterdata.get_peaks",
        "note": a.note,
        "rows_by_parameter": {str(k): int(v) for k, v in by_param.items()},
        "reference_file": {
            "name": ref.name,
            "source": f"{LEGACY}?site_no={a.site}&agency_cd=USGS&format=hn2",
            "what": ("the WATSTORE peak file as the agency's own writer produces it; the "
                     "reference an export is diffed against, frozen because this host is "
                     "being decommissioned in a window from 2026-11 to 2027-02"),
            "type_3_records": n3,
            "sha256": hashlib.sha256(r.content).hexdigest(),
            "bytes": len(r.content),
        },
        "retrieved": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "fetch_script": "verification/fixtures/fetch_peaks_fixtures.py",
        "license": "US Government public domain",
        "rows": rows,
    }
    p = a.out / f"peaks_{a.site}.json"
    p.write_text(json.dumps(out, indent=1, default=str))
    log(f"{p}: {len(rows)} rows {by_param}, reference {n3} type 3 records, "
        f"{p.stat().st_size / 1e3:.1f} kB")
    time.sleep(1)


if __name__ == "__main__":
    main()
