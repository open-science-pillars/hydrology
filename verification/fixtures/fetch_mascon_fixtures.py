# /// script
# requires-python = ">=3.11"
# dependencies = ["earthaccess>=0.14", "netCDF4", "numpy", "shapely>=2"]
# ///
"""Freeze a basin's terrestrial water storage series for a window, from
the mascon file, with the footprint scale derived beside it.

The whole mission is one file of about 46 MB, and any basin concerns a
few hundred numbers of it, so the file is fetched, read and discarded
and the fixture keeps the series, the mascon identities behind it, the
file's own hash and the record's last epoch.

The last epoch is part of the panel, not a footnote. The record runs a
quarter or so behind the present, so a storage panel drawn to the same
date as the others would be extrapolating; it stops where the data
stops and says when that was.

The extraction is the same routine the water balance freezes its
storage term with, imported rather than reimplemented, so a basin's
storage series is one number wherever it appears in this plugin.

Usage:
  uv run verification/fixtures/fetch_mascon_fixtures.py \
      --basin verification/fixtures/basins/usgs_09380000_nldi.geojson \
      --start 2020-10-01 --end 2021-09-30 --label lees_ferry_wy2021 \
      --out verification/fixtures/grace
"""
import argparse
import datetime as dt
import hashlib
import json
import sys
import tempfile
from pathlib import Path

import earthaccess
from shapely.geometry import shape

sys.path.insert(0, str(Path(__file__).parent))
from freeze_water_balance_inputs import basin_mascon_series  # noqa: E402

COLLECTION = "C3195527175-POCLOUD"      # JPL GRACE and GRACE-FO mascon RL06.3Mv04 CRI


def log(m):
    print(m, file=sys.stderr, flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--basin", required=True, type=Path)
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--mascon", type=Path, help="an already downloaded mascon file")
    a = ap.parse_args()

    doc = json.loads(a.basin.read_text())
    geom = doc["features"][0]["geometry"]
    poly = shape(geom)
    prov = doc.get("provenance", {})
    gsha = hashlib.sha256(json.dumps(geom, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    path = a.mascon
    if path is None:
        auth = earthaccess.login(strategy="netrc")
        if not getattr(auth, "authenticated", False):
            auth = earthaccess.login()
        granules = earthaccess.search_data(concept_id=COLLECTION)
        if not granules:
            raise SystemExit("no mascon granule found")
        tmp = Path(tempfile.mkdtemp(prefix="mascon_"))
        log(f"downloading the mission file into {tmp}")
        files = earthaccess.download(granules[:1], str(tmp))
        path = Path(files[0])
    log(f"reading {path.name} ({path.stat().st_size/1e6:.1f} MB)")

    got = basin_mascon_series(path, poly, dt.date.fromisoformat(a.start),
                              dt.date.fromisoformat(a.end))

    a.out.mkdir(parents=True, exist_ok=True)
    out = {
        "product": got["title"],
        "collection_concept_id": COLLECTION,
        "file": got["file"],
        "sha256": got["sha256"],
        "record_first_epoch": got["record_first_epoch"],
        "record_last_epoch": got["record_last_epoch"],
        "time_coverage_end": got["time_coverage_end"],
        "lag_note": ("the record ends a quarter or so behind the present, so this panel stops "
                     "where the data stops rather than at the window's end"),
        "region": {"fixture": a.basin.name, "geometry_sha256": gsha,
                   "area_km2": prov.get("area_km2"), "site": prov.get("site", "")},
        "cells_inside": got["cells_inside"],
        "inside_area_km2": got["inside_area_km2"],
        "mascon_ids": got["mascon_ids"],
        "mascons": got["mascons"],
        "footprint_scale": got["footprint_scale"],
        "effective_sample_note": ("cells inside one mascon carry one number, so the effective "
                                  "sample size of a basin mean is the mascon count and not the "
                                  "cell count"),
        "window": {"start": a.start, "end": a.end},
        "label": a.label,
        "epochs": got["epochs"],
        "retrieved": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "fetch_script": "verification/fixtures/fetch_mascon_fixtures.py",
        "license": "NASA data, public (EOSDIS data use guidance)",
    }
    p = a.out / f"mascon_{a.label}.json"
    p.write_text(json.dumps(out, indent=1))
    log(f"{p}: {len(got['epochs'])} epochs over {got['mascons']} mascons, "
        f"{p.stat().st_size/1e3:.1f} kB")


if __name__ == "__main__":
    main()
