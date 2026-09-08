# /// script
# requires-python = ">=3.11"
# dependencies = ["earthaccess>=0.14", "geopandas", "numpy", "shapely>=2"]
# ///
"""Freeze a SWOT LakeSP observation series over a basin polygon, one
row per pass that actually observed it.

The point of this script is the distinction a catalogue search cannot
make. A bounding-box search returns every granule whose swath
footprint crosses the box, and for SWOT a footprint spans a continent:
measured over the Tulare Lake bed, 22 of 66 granules returned for
July to November 2023 hold any lake feature inside the basin. So the
search result is a candidate list, every granule is opened, features
are filtered by geometry, and the frozen series carries both counts:
what the search offered and what was observed.

Each row is one granule that observed the basin: its date, the number
of prior-lake features inside the polygon, their identifiers, and the
water surface elevation statistics over them. Elevations are reported
as the product reports them, against its own datum, and never
differenced against a gauge here.

Usage:
  uv run verification/fixtures/fetch_swot_lake_fixtures.py \
      --basin verification/fixtures/basins/tulare_lake_bed_wbd.geojson \
      --start 2023-07-01 --end 2023-11-30 \
      --out verification/fixtures/swot/lakesp_tulare_2023.json
"""
import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import tempfile
import zipfile
from pathlib import Path

import earthaccess
import geopandas as gpd
import numpy as np
from shapely.geometry import shape

COLLECTIONS = {"D": "C3233944983-POCLOUD", "2.0": "C2799438230-POCLOUD"}


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--basin", required=True, type=Path)
    ap.add_argument("--family", default="D", choices=list(COLLECTIONS))
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args()

    doc = json.loads(a.basin.read_text())
    geom = doc["features"][0]["geometry"]
    poly = shape(geom)
    prov = doc.get("provenance", {})
    gsha = hashlib.sha256(json.dumps(geom, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    auth = earthaccess.login(strategy="netrc")
    if not getattr(auth, "authenticated", False):
        auth = earthaccess.login()

    granules = earthaccess.search_data(concept_id=COLLECTIONS[a.family], bounding_box=poly.bounds,
                                       temporal=(a.start, a.end), count=-1)
    obs = sorted({g["umm"]["GranuleUR"]: g for g in granules if "_Obs_" in g["umm"]["GranuleUR"]}.values(),
                 key=lambda g: g["umm"]["GranuleUR"])
    log(f"{len(obs)} observation granules matched by the search over {poly.bounds}")

    work = Path(tempfile.mkdtemp(prefix="lakesp_"))
    rows = []
    for k, g in enumerate(obs):
        ur = g["umm"]["GranuleUR"]
        try:
            f = Path(earthaccess.download(g, str(work))[0])
        except Exception as e:  # noqa: BLE001
            log(f"  {ur}: download failed ({type(e).__name__}), skipped")
            continue
        if f.suffix != ".zip":
            continue
        out = work / ("x_" + ur[:48])
        try:
            with zipfile.ZipFile(f) as z:
                z.extractall(out)
        except zipfile.BadZipFile:
            log(f"  {ur}: not a zip, skipped")
            continue
        shp = list(out.rglob("*.shp"))
        if not shp:
            continue
        df = gpd.read_file(shp[0])
        sub = df[df.geometry.intersects(poly)]
        if not len(sub):
            continue                    # matched the swath, observed elsewhere
        m = re.search(r"_(\d{8}T\d{6})_", ur)
        when = dt.datetime.strptime(m.group(1), "%Y%m%dT%H%M%S").replace(tzinfo=dt.timezone.utc) if m else None
        wse = np.asarray(sub["wse"], dtype="f8") if "wse" in sub.columns else np.array([])
        wse = wse[np.isfinite(wse)]
        wse = wse[np.abs(wse) < 1e5]    # the product uses a large sentinel for no value
        rows.append({
            "granule": ur,
            "observed_at": when.isoformat() if when else None,
            "features_in_granule": int(len(df)),
            "features_in_basin": int(len(sub)),
            "lake_ids": sorted({str(x) for x in sub["lake_id"].head(12)}) if "lake_id" in sub.columns else [],
            "wse_m": {"n": int(wse.size),
                      "median": round(float(np.median(wse)), 3) if wse.size else None,
                      "min": round(float(wse.min()), 3) if wse.size else None,
                      "max": round(float(wse.max()), 3) if wse.size else None},
        })
        log(f"  observed {ur[26:52]}  {len(sub)} of {len(df)} features in the basin")
        if (k + 1) % 20 == 0:
            log(f"  {k + 1}/{len(obs)} granules opened, {len(rows)} observing")

    rows.sort(key=lambda r: r["observed_at"] or "")
    out = {
        "product": "SWOT_L2_HR_LakeSP",
        "family": a.family,
        "concept_id": COLLECTIONS[a.family],
        "basin": {"fixture": a.basin.name, "geometry_sha256": gsha, "area_km2": prov.get("area_km2")},
        "window": {"start": a.start, "end": a.end},
        "granules_matched_by_search": len(obs),
        "granules_that_observed_the_basin": len(rows),
        "search_note": ("a bounding-box match is a swath footprint crossing the box, not an observation of "
                        "the basin; every granule is opened and filtered by feature geometry, and both counts "
                        "are kept because their difference is a fact about the product's sampling"),
        "datum_note": ("water surface elevations are as the product reports them, against its own reference; "
                       "they are never differenced against a gauge datum here"),
        "retrieved": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "fetch_script": "verification/fixtures/fetch_swot_lake_fixtures.py",
        "rows": rows,
    }
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(out, indent=1))
    log(f"{a.out}: {len(rows)} of {len(obs)} granules observed the basin, file {a.out.stat().st_size / 1e3:.1f} kB")


if __name__ == "__main__":
    main()
