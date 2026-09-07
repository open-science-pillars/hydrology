# /// script
# requires-python = ">=3.11"
# dependencies = ["netCDF4", "numpy", "requests", "shapely>=2"]
# ///
"""Basin-mean evapotranspiration from MOD16, and the OpenET ensemble
where the polygon is small enough for the service to answer.

Two sources, one receipt:

  mod16   MOD16A2GF (gap-filled) or MOD16A2 (the near-real-time
          companion) version 061, read from a window file written by
          fetch_et_fixtures.py: `ET_500m`, an 8-day total in kg per m2
          (numerically mm) at 500 m on the MODIS sinusoidal grid. The
          default source.
  openet  the OpenET ensemble through the API, or a recorded response
          on disk. Refused outright when the polygon is larger than
          the account's per-request area cap, which every basin in
          this plugin's fixtures is.

Three rules this script enforces, each because the wrong answer is
silent otherwise:

1. **Fill codes are not zero.** The product writes seven codes above
   the valid range for cells where evapotranspiration was not
   computed: 32767 fill, 32766 water, 32765 barren or sparsely
   vegetated, 32764 snow and ice, 32763 wetland, 32762 urban, 32761
   unclassified. The file header advertises only 32767. Every code is
   excluded from the mean, counted separately, and reported as a
   masked fraction; a basin whose masked fraction exceeds
   `--max-masked` (default 0.5) is refused rather than averaged.
2. **A composite is not always eight days.** The last period of each
   year is five or six days, from the granule's own temporal extent.
   Monthly totals apportion each composite by its daily rate over the
   days it actually covers, so the year-end period is weighted by its
   true length.
3. **Open water is a stated field, never a silent zero.** MOD16
   computes no evaporation over water, so the receipt says which
   choice was made (`exclude`, the default, or `zero`) and how much
   of the basin it concerns. A basin holding a large reservoir loses
   water the product never sees, and a zero would present that
   silence as a measurement.

Basin mean: the mean over cells whose centre falls inside the polygon
and whose value is in the valid range. A sinusoidal cell has a
constant area (463.31271652777775 m square, 0.214659 km2), so the mean
is unweighted and the area a mean represents is the count of measured
cells times that area. Volume is that mean over THAT area, not over
the whole polygon: applying a land evapotranspiration rate to the
masked part of a basin is the error the fill gotcha exists to catch,
so the receipt carries the polygon area, the measured area and their
ratio, and the volume states which one it used.

Usage:
  uv run verification/fixtures/load_et.py \
      --basin verification/fixtures/basins/usgs_09085000_nldi.geojson \
      --window verification/fixtures/et/mod16a2gf_roaring_fork_2023.nc \
      --out receipt.json
  uv run verification/fixtures/load_et.py --source openet \
      --basin <a polygon under the area cap> --response recorded.json --out receipt.json
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

import netCDF4
import numpy as np
from shapely.geometry import Point, shape
from shapely.prepared import prep

EPOCH = dt.date(1970, 1, 1)
ACRES_PER_KM2 = 247.10538146717

# The seven codes the product writes where it did not compute
# evapotranspiration, from the MOD16 user guide (the file header
# carries only the first). Anything above the valid range is one of
# these, and none of them is a zero.
FILL_CLASSES = {
    32767: "fill",
    32766: "water",
    32765: "barren-or-sparse-vegetation",
    32764: "snow-and-ice",
    32763: "wetland",
    32762: "urban",
    32761: "unclassified",
}
VALID_MAX = 32700
VALID_MIN = -32767
CELL_M = 1111950.5196666666 / 2400          # 463.31271652777775 m
CELL_KM2 = (CELL_M / 1000) ** 2             # 0.2146586 km2, constant on the sinusoidal grid

# The account tiers OpenET publishes, in acres per request. The cap is
# a property of the service, not a preference of this script.
OPENET_TIERS = {"tier1": 50000, "tier2": 200000}
OPENET_ENDPOINT = "https://openet-api.org/raster/timeseries/polygon"


def die(msg, code=2):
    print(f"REFUSED: {msg}", file=sys.stderr)
    sys.exit(code)


def load_basin(path: Path):
    doc = json.loads(path.read_text())
    geom = doc["features"][0]["geometry"]
    prov = doc.get("provenance", {})
    sha = hashlib.sha256(json.dumps(geom, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if "area_km2" not in prov:
        die(f"{path} carries no area_km2 in its provenance; the volume needs the polygon's equal-area area")
    return shape(geom), prov, sha


def inside_mask(poly, lat, lon):
    """Cells whose centre is inside the polygon. lat and lon are 2-D:
    a sinusoidal column is not a meridian."""
    pp = prep(poly)
    mask = np.zeros(lat.shape, bool)
    for j in range(lat.shape[0]):
        for i in range(lat.shape[1]):
            mask[j, i] = pp.contains(Point(float(lon[j, i]), float(lat[j, i])))
    return mask


def read_window(paths):
    comps, meta = {}, []
    lat = lon = None
    for p in paths:
        with netCDF4.Dataset(p) as ds:
            if ds.getncattr("source") != "mod16":
                die(f"{p} holds source {ds.getncattr('source')!r}, not 'mod16'")
            la = np.asarray(ds["lat"][:])
            lo = np.asarray(ds["lon"][:])
            if lat is None:
                lat, lon = la, lo
            elif la.shape != lat.shape or not (np.allclose(la, lat) and np.allclose(lo, lon)):
                die(f"{p} is on a different window than the first file; every window file in one load shares a grid")
            t = np.asarray(ds["time"][:])
            days = np.asarray(ds["composite_days"][:])
            et = np.asarray(ds["ET_500m"][:])
            qc = np.asarray(ds["ET_QC_500m"][:])
            product = ds.getncattr("product")
            labels = [str(x) for x in ds["label"][:]]
            grans = [str(x) for x in ds["granule"][:]]
            for k in range(len(t)):
                start = EPOCH + dt.timedelta(int(t[k]))
                if start in comps:
                    die(f"the composite starting {start} appears in two window files "
                        f"({comps[start]['file']} and {Path(p).name}); a composite has one source row")
                comps[start] = {"et": et[k], "qc": qc[k], "days": int(days[k]), "product": product,
                                "label": labels[k], "granule": grans[k], "file": Path(p).name}
            meta.append({"file": Path(p).name, "product": product,
                         "short_name": ds.getncattr("short_name"), "version": ds.getncattr("version"),
                         "doi": ds.getncattr("doi"), "tile": ds.getncattr("tile"),
                         "retrieved": ds.getncattr("retrieved"), "composites": int(ds.getncattr("composites")),
                         "route": ds.getncattr("route"), "dap4_constraint": ds.getncattr("dap4_constraint"),
                         "basin_fixture": ds.getncattr("basin_fixture"),
                         "basin_geometry_sha256": ds.getncattr("basin_geometry_sha256"),
                         "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()})
    return sorted(comps), comps, lat, lon, meta


def classify(values, inside):
    """Split the cells inside the polygon into measured and each fill
    class. Returns (valid mask, counts by class)."""
    v = values
    valid = inside & (v >= VALID_MIN) & (v <= VALID_MAX)
    counts = {}
    for code, name in FILL_CLASSES.items():
        n = int(np.count_nonzero(inside & (v == code)))
        if n:
            counts[name] = n
    other = int(np.count_nonzero(inside & ~valid & ~np.isin(v, list(FILL_CLASSES))))
    if other:
        counts["above-valid-range-unlisted"] = other
    return valid, counts


def polygon_acres(poly, area_km2):
    return area_km2 * ACRES_PER_KM2


def openet_from_response(doc):
    """Monthly totals from a response at either interval, and which
    interval it was. A daily response is summed into months here: the
    monthly and the daily ensembles are separate series, and comparing
    them is the only way to catch a month whose monthly value does not
    match its own days (see knowledge/gotchas/openet-monthly-not-the-daily-sum.md)."""
    rows = doc if isinstance(doc, list) else doc.get("timeseries", doc.get("data", []))
    times = [str(r["time"]) for r in rows]
    interval = "monthly" if all(t[8:10] == "01" for t in times) and len(times) <= 12 else "daily"
    months = defaultdict(float)
    days = defaultdict(int)
    for r in rows:
        months[str(r["time"])[:7]] += float(r["et"])
        days[str(r["time"])[:7]] += 1
    out = [{"month": m, "mm": round(v, 4), **({"days_summed": days[m]} if interval == "daily" else {})}
           for m, v in sorted(months.items())]
    return out, interval


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", default="mod16", choices=["mod16", "openet"])
    ap.add_argument("--basin", required=True, type=Path, help="basin polygon fixture (GeoJSON with a provenance member)")
    ap.add_argument("--window", action="append", type=Path, default=[], help="MOD16 window file, repeatable")
    ap.add_argument("--response", type=Path, help="a recorded OpenET response to read instead of calling the service")
    ap.add_argument("--interval", default="monthly", choices=["monthly", "daily"],
                    help="the interval of a live request; a recorded response is read at whatever interval it holds")
    ap.add_argument("--tier", default="tier1", choices=list(OPENET_TIERS), help="the OpenET account tier, which sets the area cap")
    ap.add_argument("--start", help="first day, YYYY-MM-DD (OpenET request window)")
    ap.add_argument("--end", help="last day, YYYY-MM-DD (OpenET request window)")
    ap.add_argument("--open-water", default="exclude", choices=["exclude", "zero"],
                    help="what to do with cells the product marks as water: exclude them from the mean (default) "
                         "or count them as zero evapotranspiration (never silently: the choice is in the receipt)")
    ap.add_argument("--max-masked", type=float, default=0.5,
                    help="refuse the basin mean when more than this fraction of the basin's cells carry a fill code")
    ap.add_argument("--out", type=Path, help="write the receipt here as JSON")
    a = ap.parse_args()

    poly, prov, sha = load_basin(a.basin)
    area_km2 = float(prov["area_km2"])
    acres = polygon_acres(poly, area_km2)

    if a.source == "openet":
        cap = OPENET_TIERS[a.tier]
        if acres > cap:
            die(f"the polygon is {acres:,.0f} acres and the OpenET {a.tier} per-request cap is {cap:,} acres "
                f"({acres / cap:.1f} times the cap): the service refuses this request with "
                f"'Single query area limit exceeded' and no basin mean exists to return. OpenET is a field and "
                f"sub-basin product; for a basin this size use --source mod16, and see "
                f"knowledge/gotchas/openet-area-cap.md")
        if a.response:
            months, interval = openet_from_response(json.loads(a.response.read_text()))
            route = f"recorded response {a.response.name}"
        else:
            import requests
            key = os.environ.get("OPENET_API_KEY")
            if not key:
                die("OPENET_API_KEY is not set; the OpenET key is read from the environment and never "
                    "written into a URL, a capture or a receipt")
            if not (a.start and a.end):
                die("--start and --end are required for a live OpenET request")
            ring = list(poly.exterior.coords) if poly.geom_type == "Polygon" else \
                list(max(poly.geoms, key=lambda q: q.area).exterior.coords)
            geom = [c for xy in ring for c in (round(xy[0], 6), round(xy[1], 6))]
            body = {"date_range": [a.start, a.end], "interval": a.interval, "geometry": geom,
                    "model": "Ensemble", "variable": "ET", "reference_et": "gridMET",
                    "reducer": "mean", "units": "mm", "file_format": "JSON"}
            r = requests.post(OPENET_ENDPOINT, json=body, headers={"Authorization": key}, timeout=600)
            if r.status_code != 200:
                die(f"OpenET answered {r.status_code}: {r.text[:300]}")
            months, interval = openet_from_response(r.json())
            route = "live request to " + OPENET_ENDPOINT
        total = sum(m["mm"] for m in months)
        receipt = {
            "source": "openet",
            "model": "Ensemble",
            "interval": interval,
            "ensemble_statistic": "mean of the six models after outlier filtering by median absolute deviation",
            "tier": a.tier,
            "area": {"polygon_km2": round(area_km2, 2), "polygon_acres": round(acres, 1),
                     "per_request_cap_acres": cap},
            "basin": {"fixture": a.basin.name, "geometry_sha256": sha, "site": prov.get("site", ""),
                      "area_km2": area_km2},
            "route": route,
            "provisional": ("OpenET calls the last 120 days provisional: those values can and will change, "
                            "so a receipt older than 120 days from its months is not a final number"),
            "monthly": months,
            "total": {"mm": round(total, 3), "km3": round(total * 1e-6 * area_km2, 6)},
            "attribution": "OpenET (CC-BY-4.0); cite Melton et al. 2021, doi:10.1111/1752-1688.12956",
        }
        print(f"OpenET ensemble ({interval}) over {a.basin.stem}: {len(months)} months, total {total:.2f} mm")
        for m in months:
            extra = f"  from {m['days_summed']} days" if "days_summed" in m else ""
            print(f"  {m['month']}  {m['mm']:8.3f} mm{extra}")
        same = [months[k]["month"] for k in range(1, len(months))
                if months[k]["mm"] == months[k - 1]["mm"]]
        if same:
            print(f"REPEATED VALUE: {', '.join(same)} repeat the month before to the last decimal; a monthly "
                  f"series that repeats is a signal, not a coincidence. Compare the daily series over the same "
                  f"polygon (--interval daily) before using these months "
                  f"(knowledge/gotchas/openet-monthly-not-the-daily-sum.md)")
        if a.out:
            a.out.write_text(json.dumps(receipt, indent=1))
        return

    if not a.window:
        die("--window names at least one MOD16 window file (fetch one with fetch_et_fixtures.py)")
    starts, comps, lat, lon, meta = read_window(a.window)
    inside = inside_mask(poly, lat, lon)
    n_inside = int(inside.sum())
    if not n_inside:
        die("no window cell centre falls inside the polygon; the window and the basin do not overlap")

    products = sorted({comps[s]["product"] for s in starts})
    if len(products) > 1:
        die(f"the window files hold more than one product ({', '.join(products)}); MOD16A2GF is gap-filled "
            f"and MOD16A2 is not, so a series that mixes them is not one series. Load them separately")

    daily = defaultdict(float)          # calendar day -> basin-mean mm for that day
    daily_km3 = defaultdict(float)      # calendar day -> volume over the area the mean represents
    per_composite = []
    masked_any = np.zeros(lat.shape, bool)
    for s in starts:
        c = comps[s]
        valid, counts = classify(c["et"], inside)
        n_valid = int(valid.sum())
        masked = n_inside - n_valid
        if a.open_water == "zero":
            water = inside & (c["et"] == 32766)
            n_water = int(water.sum())
        else:
            n_water = 0
        masked_any |= inside & ~valid
        n_mean = n_valid + n_water                                # zeros add to the denominator only
        if n_mean == 0:
            mm = float("nan")
            area = 0.0
        else:
            total = float(np.sum(c["et"][valid])) * 0.1          # scale factor 0.1
            mm = total / n_mean
            area = n_mean * CELL_KM2
        per_composite.append({
            "start": s.isoformat(), "days": c["days"], "mm": None if mm != mm else round(mm, 4),
            "cells_measured": n_valid, "cells_masked": masked,
            "masked_fraction": round(masked / n_inside, 4),
            "measured_area_km2": round(area, 3),
            "km3": None if mm != mm else round(mm * 1e-6 * area, 6),
            "fill_classes": counts, "label": c["label"], "granule": c["granule"],
        })
        if mm == mm:
            rate = mm / c["days"]
            vol = mm * 1e-6 * area / c["days"]
            for k in range(c["days"]):
                daily[s + dt.timedelta(k)] += rate
                daily_km3[s + dt.timedelta(k)] += vol

    masked_fraction_any = float(masked_any.sum()) / n_inside
    if masked_fraction_any > a.max_masked:
        die(f"{masked_fraction_any:.1%} of the basin's cells carry a fill code in at least one composite "
            f"(more than --max-masked {a.max_masked:.0%}): the basin mean would be an average over the "
            f"vegetated remnant of the basin, not over the basin. See knowledge/gotchas/"
            f"mod16-fill-over-water-barren-urban.md")

    months = defaultdict(float)
    months_km3 = defaultdict(float)
    month_days = defaultdict(int)
    for day, mm in sorted(daily.items()):
        months[day.strftime("%Y-%m")] += mm
        months_km3[day.strftime("%Y-%m")] += daily_km3[day]
        month_days[day.strftime("%Y-%m")] += 1
    monthly = [{"month": m, "mm": round(v, 4), "km3": round(months_km3[m], 6),
                "days_covered": month_days[m]} for m, v in sorted(months.items())]
    total_mm = sum(m["mm"] for m in monthly)
    total_km3 = sum(months_km3.values())
    mean_measured_area = float(np.mean([r["measured_area_km2"] for r in per_composite if r["mm"] is not None]))

    # The classes over the whole series, for the receipt's masked line.
    class_cells = defaultdict(int)
    for r in per_composite:
        for k, v in r["fill_classes"].items():
            class_cells[k] = max(class_cells[k], v)

    receipt = {
        "source": "mod16",
        "product": products[0],
        "basin": {"fixture": a.basin.name, "geometry_sha256": sha, "site": prov.get("site", ""),
                  "area_km2": area_km2},
        "window_files": meta,
        "window": {"first_composite": starts[0].isoformat(), "last_composite": starts[-1].isoformat(),
                   "composites": len(starts),
                   "composite_days": sorted({comps[s]["days"] for s in starts}),
                   "short_periods": [{"start": s.isoformat(), "days": comps[s]["days"]}
                                     for s in starts if comps[s]["days"] != 8]},
        "coverage": {"cells_in_window": int(lat.size), "cells_inside": n_inside,
                     "fraction_of_window_inside": round(n_inside / lat.size, 4),
                     "masked_fraction_any_composite": round(masked_fraction_any, 4),
                     "polygon_area_km2": round(area_km2, 3),
                     "mean_measured_area_km2": round(mean_measured_area, 3),
                     "measured_area_over_polygon_area": round(mean_measured_area / area_km2, 4),
                     "cell_area_km2": round(CELL_KM2, 6),
                     "fill_classes_max_cells": dict(sorted(class_cells.items())),
                     "mean": "mean over cells inside the polygon whose value is in the valid range",
                     "volume": ("basin-mean depth times the area those measured cells cover, NOT times the "
                                "polygon area: the masked part of the basin has no MOD16 estimate and its "
                                "water loss has to come from somewhere else")},
        "open_water": (
            "cells the product marks as water (32766) are excluded from the mean: MOD16 computes no open-water "
            "evaporation, so this basin mean is land evapotranspiration and any reservoir evaporation has to be "
            "added from another source" if a.open_water == "exclude" else
            "cells the product marks as water (32766) are counted as zero evapotranspiration on request "
            "(--open-water zero); MOD16 computes no open-water evaporation, so this understates the basin's "
            "true water loss by the reservoir evaporation it cannot see"),
        "monthly": monthly,
        "per_composite": per_composite,
        "total": {"mm": round(total_mm, 3), "km3": round(total_km3, 6),
                  "days": sum(month_days.values())},
    }
    print(f"{products[0]} over {a.basin.stem}: {len(starts)} composites, "
          f"{n_inside} cells inside, masked {masked_fraction_any:.1%}")
    print("month     mm       km3")
    for m in monthly:
        print(f"{m['month']}  {m['mm']:8.2f}  {m['km3']:8.4f}")
    print(f"total     {total_mm:8.2f}  {receipt['total']['km3']:8.4f}")
    print(f"the mean covers {mean_measured_area:.1f} km2 of the polygon's {area_km2:.1f} km2 "
          f"({mean_measured_area / area_km2:.1%})")
    if receipt["window"]["short_periods"]:
        sp = ", ".join(f"{p['start']} ({p['days']} days)" for p in receipt["window"]["short_periods"])
        print(f"SHORT PERIOD weighted by its true length: {sp}")
    if a.out:
        a.out.write_text(json.dumps(receipt, indent=1))


if __name__ == "__main__":
    main()
