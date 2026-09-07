# /// script
# requires-python = ">=3.11"
# dependencies = ["netCDF4", "numpy", "shapely>=2"]
# ///
"""Freeze one basin's water-balance inputs into a tree the executor can
read without a network, and stamp every file with its hash.

What is frozen, and why it is these files and not the grids: the
precipitation and evapotranspiration terms are the receipts the two
loaders write, because the grids behind them do not fit the fixture
rule. A water year of MOD16 over the Ohio at Olmsted is five
sinusoidal tiles and 253 MB, and over the Colorado above Lees Ferry
four tiles and 142 MB; the receipts that carry their basin means are
tens of kilobytes and carry the window files' own sha256, the granule
ids, the route and the coverage, so the derivation stays traceable to
bytes that can be refetched with the fetch script rather than stored.
The discharge term is the canonical body of a capture from core's
capture tool, which is already a frozen record with an id. The storage
term is extracted here from the mascon file: the basin's monthly
series and its formal uncertainty, with the file's sha256 and the
mascon ids beside them, because the file is one 45.8 MB record for the
whole mission and only a few hundred numbers of it concern any basin.

Every file written carries a sha256 in manifest.json, and the manifest
records what produced it. The executor reads this tree and nothing
else.

Usage:
  uv run verification/fixtures/freeze_water_balance_inputs.py \
      --basin verification/fixtures/basins/usgs_09380000_nldi.geojson \
      --name lees-ferry --start 2022-10-01 --end 2023-09-30 \
      --precipitation P_RECEIPT.json --evapotranspiration ET_RECEIPT.json \
      --capture CAPTURE_DIR/<id>.canonical.json --capture-manifest CAPTURE_DIR/manifest.jsonl \
      --mascon GRCTellus...nc --out verification/fixtures/water-balance
"""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path

import netCDF4
import numpy as np
from shapely.geometry import Point, shape
from shapely.prepared import prep

EARTH_R_KM = 6371.0088
MASCON_EPOCH = dt.date(2002, 1, 1)


def sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def basin_mascon_series(mascon: Path, poly, start: dt.date, end: dt.date):
    """The basin's mascon series: every monthly epoch, the area-weighted
    anomaly and formal uncertainty over the cells whose centre is inside
    the polygon, and the distinct mascon ids they belong to.

    The mascon count is not decoration: cells inside one mascon carry
    one number, so the effective sample size of a basin mean is the
    number of mascons it spans, not the number of cells."""
    with netCDF4.Dataset(mascon) as ds:
        lat = np.asarray(ds["lat"][:]).ravel()
        lon = np.asarray(ds["lon"][:]).ravel()
        lonw = np.where(lon > 180, lon - 360, lon)
        t = np.asarray(ds["time"][:])
        lwe = np.asarray(ds["lwe_thickness"][:])
        unc = np.asarray(ds["uncertainty"][:])
        mid = np.asarray(ds["mascon_ID"][:])
        land = np.asarray(ds["land_mask"][:])
        title = ds.getncattr("title")
        coverage_end = ds.getncattr("time_coverage_end")
    dates = [MASCON_EPOCH + dt.timedelta(float(x)) for x in t]

    pp = prep(poly)
    x0, y0, x1, y1 = poly.bounds
    inside = np.zeros((len(lat), len(lon)), bool)
    for j, y in enumerate(lat):
        if not (y0 - 1 <= y <= y1 + 1):
            continue
        for i, x in enumerate(lonw):
            if x0 - 1 <= x <= x1 + 1:
                inside[j, i] = pp.contains(Point(float(x), float(y)))
    if not inside.any():
        raise SystemExit("REFUSED: no mascon cell centre falls inside the polygon")

    dlat = abs(lat[1] - lat[0])
    dlon = abs(lon[1] - lon[0])
    band = (EARTH_R_KM ** 2) * np.radians(dlon) * (
        np.sin(np.radians(lat + dlat / 2)) - np.sin(np.radians(lat - dlat / 2)))
    area = np.repeat(band[:, None], len(lon), axis=1)
    w = area * inside
    wsum = float(w.sum())

    ids = sorted(int(x) for x in np.unique(mid[inside]))
    series = []
    for k, d in enumerate(dates):
        series.append({"epoch": d.isoformat(),
                       "lwe_cm": round(float((lwe[k] * w).sum() / wsum), 4),
                       "uncertainty_cm": round(float((unc[k] * w).sum() / wsum), 4)})

    # The footprint scale, derived here from the product rather than
    # remembered: the area of a mostly-land mascon.
    flat = mid.ravel()
    uids, inv = np.unique(flat, return_inverse=True)
    areas = np.bincount(inv, weights=area.ravel())
    landfrac = np.bincount(inv, weights=(land.ravel() * area.ravel())) / areas
    land_areas = areas[landfrac > 0.5]
    scale = {"mascons_total": int(len(uids)), "mascons_mostly_land": int(len(land_areas)),
             "median_land_mascon_km2": round(float(np.percentile(land_areas, 50)), 1),
             "p05_km2": round(float(np.percentile(land_areas, 5)), 1),
             "p95_km2": round(float(np.percentile(land_areas, 95)), 1),
             "median_equivalent_square_side_km": round(float(np.percentile(land_areas, 50) ** 0.5), 1),
             "median_equivalent_circle_diameter_km": round(
                 float(2 * (np.percentile(land_areas, 50) / np.pi) ** 0.5), 1)}
    return {"file": Path(mascon).name, "sha256": sha256(mascon), "title": title,
            "time_coverage_end": coverage_end,
            "cells_inside": int(inside.sum()), "mascon_ids": ids, "mascons": len(ids),
            "inside_area_km2": round(wsum, 1),
            "footprint_scale": scale,
            "epochs": [s for s in series
                       if start - dt.timedelta(45) <= dt.date.fromisoformat(s["epoch"]) <= end + dt.timedelta(45)],
            "record_first_epoch": dates[0].isoformat(), "record_last_epoch": dates[-1].isoformat()}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--basin", required=True, type=Path)
    ap.add_argument("--name", required=True, help="the basin's name in the frozen tree")
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--precipitation", required=True, type=Path, help="load_precipitation receipt")
    ap.add_argument("--evapotranspiration", required=True, type=Path, help="load_et receipt")
    ap.add_argument("--capture", required=True, type=Path, help="the discharge capture's canonical body")
    ap.add_argument("--capture-manifest", required=True, type=Path, help="the capture store's manifest.jsonl")
    ap.add_argument("--partial-check", type=Path, help="a second capture reported beside the storage term, not folded into it")
    ap.add_argument("--partial-check-note", default="", help="what the partial check is and why it is not a term")
    ap.add_argument("--mascon", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args()

    start = dt.date.fromisoformat(a.start)
    end = dt.date.fromisoformat(a.end)
    doc = json.loads(a.basin.read_text())
    poly = shape(doc["features"][0]["geometry"])
    prov = doc.get("provenance", {})

    root = a.out / a.name
    root.mkdir(parents=True, exist_ok=True)

    def capture_row(cid):
        for line in a.capture_manifest.read_text().splitlines():
            row = json.loads(line)
            if row.get("capture_id") == cid:
                return row
        raise SystemExit(f"REFUSED: capture {cid} is not in {a.capture_manifest}")

    files = {}
    (root / "basin.geojson").write_text(a.basin.read_text())
    files["basin.geojson"] = {"sha256": sha256(root / "basin.geojson"),
                              "from": str(a.basin), "area_km2": prov.get("area_km2"),
                              "geometry_sha256": prov.get("geometry_sha256", ""),
                              "site": prov.get("site", "")}
    for label, src in (("precipitation.json", a.precipitation), ("evapotranspiration.json", a.evapotranspiration)):
        (root / label).write_text(src.read_text())
        files[label] = {"sha256": sha256(root / label), "from": str(src),
                        "kind": "loader receipt (the grids behind it are refetchable, not stored)"}

    for label, cap in (("discharge.json", a.capture), ("partial_check.json", a.partial_check)):
        if cap is None:
            continue
        cid = cap.name.split(".")[0]
        row = capture_row(cid)
        body = json.loads(cap.read_text())
        payload = {"capture_id": cid, "source": row.get("source"), "params": row.get("params"),
                   "captured_at": row.get("captured_at"), "rows": row.get("rows"),
                   "content_sha256": row.get("content_sha256"), "raw_sha256": row.get("raw_sha256"),
                   "tool": row.get("tool_version", row.get("tool", "")), "series": body}
        if label == "partial_check.json":
            payload["note"] = a.partial_check_note
        (root / label).write_text(json.dumps(payload, indent=1))
        files[label] = {"sha256": sha256(root / label), "capture_id": cid,
                        "content_sha256": row.get("content_sha256")}

    storage = basin_mascon_series(a.mascon, poly, start, end)
    (root / "storage.json").write_text(json.dumps(storage, indent=1))
    files["storage.json"] = {"sha256": sha256(root / "storage.json"),
                             "from": str(a.mascon), "granule_sha256": storage["sha256"]}

    manifest = {"basin": a.name, "window": {"start": a.start, "end": a.end},
                "frozen_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "frozen_by": "verification/fixtures/freeze_water_balance_inputs.py",
                "files": files,
                "note": ("the executor reads this tree and nothing else; every file's sha256 is here and "
                         "the receipts carry the window files' own hashes, granule ids and routes")}
    (root / "manifest.json").write_text(json.dumps(manifest, indent=1))
    total = sum((root / f).stat().st_size for f in files)
    print(f"{root}: {len(files)} files, {total / 1e3:.1f} kB, storage {storage['mascons']} mascons "
          f"over {storage['cells_inside']} cells, footprint scale "
          f"{storage['footprint_scale']['median_land_mascon_km2']:,.0f} km2")


if __name__ == "__main__":
    main()
