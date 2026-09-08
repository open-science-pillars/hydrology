# /// script
# requires-python = ">=3.11"
# dependencies = ["requests"]
# ///
"""Freeze one reservoir's ledger inputs: the captures, the area-capacity
table, and the satellite elevations, each with the hash that identifies it.

The gauge series are already citable records: core's capture tool has
fetched and hashed them, and a capture is the thing a receipt cites. So
this does not refetch them; it reads the capture store, copies the
canonical rows it needs, and records each capture's id and content hash
beside them, which is what lets the ledger name its sources without
carrying a network.

The area-capacity table is fetched once and kept whole, because it is
small, because a resurvey replaces it, and because a volume computed
from an unnamed revision is not a measurement. Its DOI, its file name
and its sha256 go in the manifest.

The elevation series are kept in BOTH published datums. That is not
redundancy: the modern table is referenced to NAVD88 and the reservoir
gauge's headline parameter is NGVD29, so the pair is what proves the
offset the ledger applies rather than assumes.

Usage:
  uv run verification/fixtures/freeze_reservoir_inputs.py \
      --store ~/obs-captures --out verification/fixtures/reservoir
"""
import argparse
import datetime as dt
import glob
import hashlib
import json
import os
import sys
from pathlib import Path

import requests

TABLE_URL = ("https://www.sciencebase.gov/catalog/file/get/614ccd07d34e0df5fb9868e2"
             "?f=__disk__97%2F11%2F02%2F971102deb47629dff297d23ba2dadcb375fb6b8d")
TABLE_NAME = "Lake_Powell_2018_ElevAreaCap_calc.csv"
TABLE_DOI = "10.5066/P9O3IPG3"
WANT = [
    ("pool_elevation_ngvd29", "09379900", "62614", "Lake Powell at Glen Canyon Dam, AZ"),
    ("pool_elevation_navd88", "09379900", "62615", "Lake Powell at Glen Canyon Dam, AZ"),
    ("inflow_colorado_cisco", "09180500", "00060", "Colorado River near Cisco, UT"),
    ("inflow_green_river",    "09315000", "00060", "Green River at Green River, UT"),
    ("inflow_san_juan_bluff", "09379500", "00060", "San Juan River near Bluff, UT"),
    ("outflow_lees_ferry",    "09380000", "00060", "Colorado River at Lees Ferry, AZ"),
]
# Total drainage areas from the site files, in square miles. Contributing
# areas are not published for these sites, which the basin concepts record.
DRAINAGE_MI2 = {"09180500": 24100, "09315000": 44850, "09379500": 23000, "09380000": 111800}


def log(m):
    print(m, file=sys.stderr, flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--store", type=Path, default=Path.home() / "obs-captures")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--start", default="2022-10-01")
    ap.add_argument("--end", default="2023-09-30")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)

    # The capture store: newest capture per (site, parameter) whose rows
    # cover the window exactly.
    found = {}
    for p in sorted(glob.glob(str(a.store / "*.canonical.json"))):
        try:
            d = json.loads(Path(p).read_text())
        except Exception:
            continue
        if not (isinstance(d, list) and d and isinstance(d[0], dict) and "rows" in d[0]):
            continue
        s = d[0]
        rows = s["rows"]
        if not rows or rows[0]["t"] != a.start or rows[-1]["t"] != a.end:
            continue
        found[(s.get("site"), s.get("parameter"))] = (Path(p), s)

    series = {}
    for name, site, pcode, label in WANT:
        key = (site, pcode)
        if key not in found:
            raise SystemExit(
                f"REFUSED: no capture in {a.store} covers {site} parameter {pcode} for "
                f"{a.start} to {a.end}. Take it with core's capture tool first; this script "
                "reads the citable record and does not create one")
        path, s = found[key]
        cid = path.name.split(".")[0]
        series[name] = {
            "site": site, "site_name": label, "parameter": pcode,
            "statistic": s.get("statistic"),
            "capture_id": cid,
            "content_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "drainage_area_mi2": DRAINAGE_MI2.get(site),
            "days": len(s["rows"]),
            "values": {r["t"]: r["v"] for r in s["rows"]},
            "approval": sorted({r["approval"] for r in s["rows"]}),
            "qualifiers": sorted({q for r in s["rows"] for q in (r["qualifiers"] or [])}),
        }
        log(f"  {name}: capture {cid}, {len(s['rows'])} days, approval {series[name]['approval']}")

    tbl = a.out / TABLE_NAME
    if not tbl.exists():
        r = requests.get(TABLE_URL, timeout=300,
                         headers={"User-Agent": "open-science-pillars-hydrology/0.6"})
        r.raise_for_status()
        tbl.write_bytes(r.content)
        log(f"  fetched {TABLE_NAME}, {len(r.content)/1e3:.1f} kB")
    rows = tbl.read_text().splitlines()

    manifest = {
        "reservoir": "Lake Powell",
        "window": {"start": a.start, "end": a.end, "convention": "water year 2023"},
        "series": series,
        "area_capacity_table": {
            "file": TABLE_NAME,
            "sha256": hashlib.sha256(tbl.read_bytes()).hexdigest(),
            "bytes": tbl.stat().st_size,
            "rows": len(rows) - 1,
            "header": rows[0],
            "doi": TABLE_DOI,
            "title": "Elevation-area-capacity tables for Lake Powell, 2018",
            "publication": ("England, J.F., and others; the survey is reported in USGS "
                            "Scientific Investigations Report 2022-5017, Elevation-area-capacity "
                            "relationships of Lake Powell in 2018 and estimated loss of storage "
                            "capacity since 1963"),
            "published": "2022-03-21",
            "survey": "2017 to 2018 topobathymetric survey, the first update since 1986",
            "datum": "NAVD88, with an NGVD29 column beside it",
            "note": ("a resurvey replaces this table rather than amending it, so a volume is "
                     "quoted with the revision that produced it"),
        },
        "retrieved": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "fetch_script": "verification/fixtures/freeze_reservoir_inputs.py",
        "license": {"gauges": "US Government public domain",
                    "table": "US Government public domain"},
    }
    p = a.out / "ledger_powell_wy2023.json"
    p.write_text(json.dumps(manifest, indent=1))
    log(f"{p}: {len(series)} series, table {manifest['area_capacity_table']['rows']} rows, "
        f"{p.stat().st_size/1e3:.1f} kB")


if __name__ == "__main__":
    main()
