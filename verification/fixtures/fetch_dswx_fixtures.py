# /// script
# requires-python = ">=3.11"
# dependencies = ["earthaccess>=0.14", "numpy", "pyproj", "rasterio", "shapely>=2"]
# ///
"""Freeze a DSWx water-class census over a basin polygon, one row per
granule, into a small JSON the timeline and its golden read.

What is frozen, and why it is a census rather than the rasters: a
single DSWx granule's water layer is a 3660 by 3660 COG, and a season
of them over a basin is hundreds of megabytes. What a timeline needs
from each granule is the count of pixels in each class inside the
basin, which is a few dozen integers. The census carries the granule
identifier (which holds both the acquisition and the production date),
the tile, the class counts, the basin's geometry hash and the class
table's own source, so every area in the timeline can be recomputed
from it and traced back to bytes that can be refetched.

One date is one mosaic, not a sum of tiles. The MGRS tiles overlap at
their edges, so adding per-tile class counts double-counts the overlap:
measured over the Tulare Lake bed, six tiles of one acquisition summed
to 186 per cent of the basin's area. Every granule of an acquisition
date is therefore reprojected into one grid (EPSG:5070 at 30 m, the
polygon's bounds) and the classes are counted once on that mosaic.

The class values are NOT interpreted here. They are counted as they
appear and named from the product's own table in the concept, because
the two DSWx products use the same integers for different things: 2 is
partial surface water in the optical product and unused in the radar
one, 3 is inundated vegetation in the radar product and unused in the
optical one, and above the data range 252 and 253 (snow, cloud) collide
with 250 and 251 (HAND, layover). A census that folded classes together
here would bake one product's vocabulary into a file that names neither.

Usage:
  uv run verification/fixtures/fetch_dswx_fixtures.py --product hls \
      --basin verification/fixtures/basins/tulare_lake_bed_wbd.geojson \
      --start 2023-01-01 --end 2023-08-31 \
      --out verification/fixtures/dswx/dswx_hls_tulare_2023.json
"""
import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import tempfile
import time
from pathlib import Path

import earthaccess
import numpy as np
import pyproj
import rasterio
from rasterio.features import geometry_mask
from rasterio.transform import from_origin
from rasterio.warp import Resampling, reproject
from shapely.geometry import mapping, shape
from shapely.ops import transform as shp_transform

PRODUCTS = {
    "hls": {"concept_id": "C2617126679-POCLOUD", "short_name": "OPERA_L3_DSWX-HLS_V1",
            "doi": "10.5067/OPDSW-PL3V1", "layer": "_B01_WTR.tif",
            "spec": "OPERA DSWx-HLS Product Specification v1.0.1, JPL D-107395 Rev B, 2024-07-10, Table 4-1"},
    "s1": {"concept_id": "C2949811996-POCLOUD", "short_name": "OPERA_L3_DSWX-S1_V1",
           "doi": "10.5067/OPDSWS1-L3V1", "layer": "_B01_WTR.tif",
           "spec": "OPERA DSWx-S1 Product Specification Rev A, JPL D-108761"},
}


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def granule_dates(ur: str):
    """Acquisition and production, both of which a receipt needs: the
    archive is reprocessed, so a 2023 acquisition can carry a 2026
    production date."""
    m = re.findall(r"(\d{8}T\d{6}Z)", ur)
    def parse(x):
        return dt.datetime.strptime(x, "%Y%m%dT%H%M%SZ").replace(tzinfo=dt.timezone.utc)
    return (parse(m[0]).isoformat() if m else None,
            parse(m[1]).isoformat() if len(m) > 1 else None)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--product", required=True, choices=list(PRODUCTS))
    ap.add_argument("--basin", required=True, type=Path)
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--max-granules", type=int, default=-1,
                    help="cap on the granule search; -1 means every granule in the window. A cap that "
                         "is reached truncates the timeline at a date the data does not end on, so "
                         "reaching it is an error rather than a note")
    a = ap.parse_args()

    spec = PRODUCTS[a.product]
    doc = json.loads(a.basin.read_text())
    geom = doc["features"][0]["geometry"]
    poly = shape(geom)
    prov = doc.get("provenance", {})
    gsha = hashlib.sha256(json.dumps(geom, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    auth = earthaccess.login(strategy="netrc")
    if not getattr(auth, "authenticated", False):
        auth = earthaccess.login()
    session = auth.get_session()

    bbox = poly.bounds
    granules = earthaccess.search_data(concept_id=spec["concept_id"], bounding_box=bbox,
                                       temporal=(a.start, a.end), count=a.max_granules)
    log(f"{len(granules)} {a.product} granules over {bbox} between {a.start} and {a.end}")
    if a.max_granules > 0 and len(granules) >= a.max_granules:
        raise SystemExit(f"REFUSED: the search returned {len(granules)} granules and the cap is "
                         f"{a.max_granules}, so the window is truncated at whatever date the cap fell on "
                         f"rather than at the end of the data. Raise --max-granules or drop it")

    # One grid for every date: the polygon's bounds in an equal-area
    # CONUS projection at the product's own 30 m posting.
    GRID_CRS = "EPSG:5070"
    to_grid = pyproj.Transformer.from_crs("EPSG:4326", GRID_CRS, always_xy=True).transform
    gpoly = shp_transform(to_grid, poly)
    x0, y0, x1, y1 = gpoly.bounds
    res = 30.0
    W = int(np.ceil((x1 - x0) / res))
    H = int(np.ceil((y1 - y0) / res))
    transform = from_origin(x0, y1, res, res)
    inside = ~geometry_mask([mapping(gpoly)], out_shape=(H, W), transform=transform, invert=False)
    log(f"grid {W} by {H} at {res} m in {GRID_CRS}; {int(inside.sum())} cells inside the polygon "
        f"({inside.sum() * res * res / 1e6:.1f} km2 against the polygon's {prov.get('area_km2')} km2)")

    by_date = {}
    for g in granules:
        ur = g["umm"]["GranuleUR"]
        acq, prod = granule_dates(ur)
        if not acq:
            continue
        by_date.setdefault(acq[:10], []).append((ur, prod, g))

    rows, nbytes = [], 0
    workdir = Path(tempfile.mkdtemp(prefix="dswx_"))
    t0 = time.time()
    for k, day in enumerate(sorted(by_date)):
        mosaic = np.full((H, W), 255, "uint8")
        seen = np.zeros((H, W), bool)
        used, prods, tiles = [], set(), set()
        for ur, prod, g in sorted(by_date[day]):
            urls = [r["URL"] for r in g["umm"].get("RelatedUrls", [])
                    if r.get("Type") == "GET DATA" and r["URL"].endswith(spec["layer"])]
            if not urls:
                continue
            r = session.get(urls[0], timeout=300)
            if r.status_code != 200:
                log(f"  {ur}: {r.status_code}, skipped")
                continue
            nbytes += len(r.content)
            p = workdir / "wtr.tif"
            p.write_bytes(r.content)
            with rasterio.open(p) as ds:
                dst = np.full((H, W), 255, "uint8")
                reproject(source=rasterio.band(ds, 1), destination=dst,
                          src_transform=ds.transform, src_crs=ds.crs,
                          dst_transform=transform, dst_crs=GRID_CRS,
                          resampling=Resampling.nearest, src_nodata=255, dst_nodata=255)
            # First granule of the date to reach a cell owns it; the
            # overlap between tiles is written once, never twice.
            fresh = (dst != 255) & ~seen
            mosaic[fresh] = dst[fresh]
            seen |= fresh
            used.append(ur)
            m = re.search(r"_(T\d{2}[A-Z]{3})_", ur)
            if m:
                tiles.add(m.group(1))
            if prod:
                prods.add(prod)
        cells = inside & seen
        if not cells.any():
            continue
        vals, counts = np.unique(mosaic[inside], return_counts=True)
        census = {int(v): int(c) for v, c in zip(vals, counts)}
        rows.append({"date": day, "granules": sorted(used), "tiles": sorted(tiles),
                     "produced": sorted(prods),
                     "cells_in_polygon": int(inside.sum()),
                     "cells_observed": int(cells.sum()),
                     "class_counts": census})
        if (k + 1) % 10 == 0:
            log(f"  {k + 1}/{len(by_date)} dates, {nbytes / 1e6:.1f} MB, {time.time() - t0:.0f} s")

    rows.sort(key=lambda r: r["date"])
    out = {
        "product": a.product,
        "short_name": spec["short_name"],
        "concept_id": spec["concept_id"],
        "doi": spec["doi"],
        "layer": spec["layer"].strip("_.tif"),
        "class_table_source": spec["spec"],
        "class_note": ("counts are raw class values over the cells whose centre is inside the polygon; "
                       "pixels_in_polygon is their total, so a valid fraction is computed from the classes "
                       "and never from the raster's padding. The two DSWx products use the same integers "
                       "for different classes, so the meaning comes from the product's own table and "
                       "never from the value"),
        "basin": {"fixture": a.basin.name, "geometry_sha256": gsha,
                  "area_km2": prov.get("area_km2"), "site": prov.get("site", "")},
        "window": {"start": a.start, "end": a.end},
        "granules_searched": len(granules),
        "dates": len(rows),
        "grid": {"crs": "EPSG:5070", "resolution_m": 30, "width": W, "height": H,
                 "cells_in_polygon": int(inside.sum()),
                 "note": "one mosaic per acquisition date; overlapping MGRS tiles are written once"},
        "bytes_transferred": nbytes,
        "retrieved": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "fetch_script": "verification/fixtures/fetch_dswx_fixtures.py",
        "rows": rows,
    }
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(out, indent=1))
    log(f"{a.out}: {len(rows)} dates from {len(granules)} granules, "
        f"{nbytes / 1e6:.1f} MB read in {time.time() - t0:.0f} s, file {a.out.stat().st_size / 1e3:.1f} kB")


if __name__ == "__main__":
    main()
