# /// script
# requires-python = ">=3.11"
# dependencies = ["netCDF4", "numpy", "shapely>=2"]
# ///
"""Basin-mean daily and monthly precipitation from a window file, with
the run declared and the seams named.

Reads one or more window files written by fetch_precipitation_fixtures.py
(the same schema for IMERG and NLDAS-2), clips them to a basin polygon
fixture by cell centre, and writes a receipt: daily basin means, monthly
totals in mm and km3, the run each month came from, every seam in the
series, and the coverage numbers a reader needs to judge the mean.

The rule this script enforces for IMERG: the run is a DECLARED input.
The three daily runs (Final, Late, Early) carry the same variable name
and differ in calibration, and a concatenation across them raises no
error anywhere else, so this loader refuses to proceed without
`--run`, refuses a month whose file holds a run other than the one
declared for it, refuses a month that holds two runs, and names every
run change between months as a seam with its date. A declaration is
one run for the whole series (`--run final`) or one per month
(`--run 2025-09:final,2025-10:late`). NLDAS-2 has one run.

Basin mean: cosine-latitude weighted mean over the cells whose centre
falls inside the polygon; the fraction of window cells inside and the
ratio of inside-cell area to the polygon's equal-area area are both in
the receipt. Volume: the basin-mean depth times the polygon's area as
its provenance records it (km3 = mm * 1e-6 * km2).

Usage:
  uv run verification/fixtures/load_precipitation.py --source imerg --run final \
      --basin verification/fixtures/basins/usgs_09380000_nldi.geojson \
      --window verification/fixtures/precipitation/imerg_final_lees_ferry_wy2023.nc \
      --out receipt.json
  uv run verification/fixtures/load_precipitation.py --source nldas2 --basin ... --window ...
  (--fetch pulls a missing window file first, through fetch_precipitation_fixtures.py,
   for a single-run declaration and a --start/--end window)
"""
import argparse
import datetime as dt
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import netCDF4
import numpy as np
from shapely.geometry import Point, shape
from shapely.prepared import prep

EPOCH = dt.date(1970, 1, 1)
FILL = -9999.0
EARTH_R_KM = 6371.0088
RUNS = ("final", "late", "early")

# Dated facts the granules cannot show, from the IMERG dataset concept
# (knowledge/datasets/imerg-v07.md, whose stale_after governs them):
# a series crossing one of these is flagged even when its run is
# homogeneous. The date the near-real-time runs began ingesting V08
# inputs is not published and is not listed.
KNOWN_SEAMS = [
    {"date": "2025-10-01", "runs": ["final"], "kind": "final-end",
     "note": "no V07 Final exists after 2025-09-30; a Final series cannot continue past this date"},
    {"date": "2026-03-01", "runs": ["late", "early"], "kind": "calibration",
     "note": "Late and Early calibration became climatological on 2026-03-01 (the hybrid period); values before and after are calibrated differently"},
]


def die(msg, code=2):
    print(f"REFUSED: {msg}", file=sys.stderr)
    sys.exit(code)


def parse_declaration(text, source):
    if source == "nldas2":
        if text and text != "nldas2":
            die(f"--run {text!r} names an IMERG run; the nldas2 source has one run (omit --run or say nldas2)")
        return {"*": "nldas2"}
    if not text:
        die("IMERG needs --run (final, late or early, or one per month as YYYY-MM:run,...): the three daily "
            "runs share a variable name and differ in calibration, so the run is declared, never chosen here")
    if text in RUNS:
        return {"*": text}
    decl = {}
    for part in text.split(","):
        m = re.fullmatch(r"(\d{4}-\d{2}):(final|late|early)", part.strip())
        if not m:
            die(f"cannot read the run declaration {part!r}; use final|late|early or YYYY-MM:run,...")
        decl[m.group(1)] = m.group(2)
    return decl


def load_basin(path: Path):
    doc = json.loads(path.read_text())
    geom = doc["features"][0]["geometry"]
    prov = doc.get("provenance", {})
    sha = hashlib.sha256(json.dumps(geom, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if "area_km2" not in prov:
        die(f"{path} carries no area_km2 in its provenance; the volume needs the polygon's equal-area area")
    return shape(geom), prov, sha


def read_windows(paths, source):
    days, rows = [], {}
    meta = []
    lat = lon = None
    for p in paths:
        with netCDF4.Dataset(p) as ds:
            if ds.getncattr("source") != source:
                die(f"{p} holds source {ds.getncattr('source')!r}, not {source!r}")
            la, lo = ds["lat"][:].filled(), ds["lon"][:].filled()
            if lat is None:
                lat, lon = la, lo
            elif la.shape != lat.shape or lo.shape != lon.shape or not (np.allclose(la, lat) and np.allclose(lo, lon)):
                die(f"{p} is on a different window than the first file; every window file in one load shares a grid")
            t = ds["time"][:].filled()
            pr = ds["precipitation"][:].filled(FILL)
            runs = [str(x) for x in ds["run"][:]]
            labels = [str(x) for x in ds["label"][:]]
            gran = ds["granules"][:].filled()
            routes = [str(x) for x in ds["route"][:]]
            for k in range(len(t)):
                day = EPOCH + dt.timedelta(int(t[k]))
                if day in rows:
                    die(f"{day} appears in two window files ({rows[day]['file']} and {p.name}); a day has one source row")
                rows[day] = {"p": pr[k], "run": runs[k], "label": labels[k], "granules": int(gran[k]),
                             "route": routes[k], "file": p.name}
            meta.append({"file": p.name, "short_name": ds.getncattr("short_name"), "run": ds.getncattr("run"),
                         "doi": ds.getncattr("doi"), "retrieved": ds.getncattr("retrieved"),
                         "granule_count": int(ds.getncattr("granule_count")),
                         "route": ds.getncattr("route"), "dap4_constraint": ds.getncattr("dap4_constraint"),
                         "basin_fixture": ds.getncattr("basin_fixture"),
                         "basin_geometry_sha256": ds.getncattr("basin_geometry_sha256"),
                         "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()})
    return sorted(rows), rows, lat, lon, meta


def inside_mask(poly, lat, lon):
    pp = prep(poly)
    mask = np.zeros((len(lat), len(lon)), bool)
    for j, y in enumerate(lat):
        for i, x in enumerate(lon):
            mask[j, i] = pp.contains(Point(float(x), float(y)))
    return mask


def cell_areas_km2(lat, lon):
    dlat = float(abs(lat[1] - lat[0]))
    dlon = float(abs(lon[1] - lon[0]))
    a = (EARTH_R_KM ** 2) * math.radians(dlon) * (np.sin(np.radians(lat + dlat / 2)) - np.sin(np.radians(lat - dlat / 2)))
    return np.repeat(a[:, None], len(lon), axis=1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", required=True, choices=["imerg", "nldas2"])
    ap.add_argument("--run", help="IMERG run declaration: final|late|early, or YYYY-MM:run,... per month")
    ap.add_argument("--basin", required=True, type=Path)
    ap.add_argument("--window", required=True, type=Path, action="append", help="window file(s); repeat to concatenate")
    ap.add_argument("--start", help="first day, YYYY-MM-DD (default: the files' first day)")
    ap.add_argument("--end", help="last day, YYYY-MM-DD (default: the files' last day)")
    ap.add_argument("--fetch", action="store_true", help="pull a missing window file first (single run, --start and --end required)")
    ap.add_argument("--out", type=Path, help="receipt JSON path")
    a = ap.parse_args()

    decl = parse_declaration(a.run, a.source)
    poly, bprov, bsha = load_basin(a.basin)

    missing = [w for w in a.window if not w.exists()]
    if missing:
        if not a.fetch:
            die(f"window file(s) not found: {', '.join(str(m) for m in missing)} (pass --fetch to pull, or run fetch_precipitation_fixtures.py)")
        if len(missing) > 1 or "*" not in decl or not (a.start and a.end):
            die("--fetch pulls one window file for a single-run declaration between --start and --end; fetch per-month segments separately")
        fetch = Path(__file__).with_name("fetch_precipitation_fixtures.py")
        cmd = [shutil.which("uv") or "uv", "run", str(fetch), "--source", a.source, "--basin", str(a.basin),
               "--start", a.start, "--end", a.end, "--out", str(missing[0])]
        if a.source == "imerg":
            cmd += ["--run", decl["*"]]
        print("fetching:", " ".join(cmd), file=sys.stderr)
        subprocess.run(cmd, check=True)

    days, rows, lat, lon, meta = read_windows(a.window, a.source)
    for m in meta:
        if m["basin_geometry_sha256"] != bsha:
            print(f"note: {m['file']} was windowed on basin geometry {m['basin_geometry_sha256'][:12]}, "
                  f"this polygon is {bsha[:12]}; the clip uses this polygon", file=sys.stderr)
    start = dt.date.fromisoformat(a.start) if a.start else days[0]
    end = dt.date.fromisoformat(a.end) if a.end else days[-1]
    wanted = [start + dt.timedelta(n) for n in range((end - start).days + 1)]
    have = [d for d in wanted if d in rows and rows[d]["granules"] > 0]
    absent = [d for d in wanted if d not in have]
    if a.source == "imerg":
        final_end = dt.date.fromisoformat(KNOWN_SEAMS[0]["date"]) - dt.timedelta(1)
        past = sorted({d.strftime("%Y-%m") for d in wanted
                       if d > final_end and decl.get("*", decl.get(d.strftime("%Y-%m"))) == "final"})
        if past:
            die(f"final is declared for {', '.join(past)}, but the V07 Final record ends at {final_end} "
                f"(the last Final daily granule; see knowledge/datasets/imerg-v07.md): no Final exists for those months. "
                f"Declare the run that does (late or early) per month, and the receipt will carry the run seam at {KNOWN_SEAMS[0]['date']}")
    if not have:
        die(f"no data between {start} and {end} in the window file(s)")

    # The declaration against the files, month by month.
    months = sorted({d.strftime("%Y-%m") for d in wanted})
    runs_by_month = defaultdict(set)
    labels_by_month = defaultdict(set)
    for d in have:
        runs_by_month[d.strftime("%Y-%m")].add(rows[d]["run"])
        labels_by_month[d.strftime("%Y-%m")].add(rows[d]["label"])
    declared = {}
    problems = []
    for mth in months:
        want = decl.get("*", decl.get(mth))
        if want is None:
            problems.append(f"{mth}: no run declared for this month")
            continue
        declared[mth] = want
        found = runs_by_month.get(mth, set())
        if len(found) > 1:
            problems.append(f"{mth}: the file holds {' and '.join(sorted(found))} in one month; a run is declared per month, split the request at the seam")
        elif found and found != {want}:
            problems.append(f"{mth}: declared {want}, the file holds {next(iter(found))}")
    if problems:
        die("the declared run does not match the data:\n  " + "\n  ".join(problems))

    # Seams: a run change between months, a label change inside a run,
    # and the dated facts the concept records.
    seams = []
    prev = None
    for mth in months:
        r = declared[mth]
        if prev and r != prev:
            seams.append({"date": f"{mth}-01", "kind": "run", "from": prev, "to": r,
                          "note": "the run changes here; the two sides are calibrated differently and the series is not homogeneous across this date"})
        prev = r
    prevd = None
    for d in have:
        if prevd and rows[d]["label"] != rows[prevd]["label"] and rows[d]["run"] == rows[prevd]["run"]:
            seams.append({"date": d.isoformat(), "kind": "label", "from": rows[prevd]["label"], "to": rows[d]["label"],
                          "note": "the granule version label changes inside one run"})
        prevd = d
    for ks in KNOWN_SEAMS:
        ksd = dt.date.fromisoformat(ks["date"])
        if start < ksd <= end and any(declared[m] in ks["runs"] for m in months):
            seams.append({"date": ks["date"], "kind": ks["kind"], "note": ks["note"]})
    # The clip.
    mask = inside_mask(poly, lat, lon)
    areas = cell_areas_km2(lat, lon)
    w = np.where(mask, np.cos(np.radians(lat))[:, None], 0.0)
    n_inside = int(mask.sum())
    if n_inside == 0:
        die("no cell centre falls inside the polygon; the window does not cover this basin")
    inside_area = float(areas[mask].sum())

    daily = []
    for d in have:
        p = rows[d]["p"]
        valid = mask & (p != FILL)
        ww = np.where(valid, w, 0.0)
        mean = float((p * ww).sum() / ww.sum()) if ww.sum() > 0 else None
        daily.append({"date": d.isoformat(), "mm": None if mean is None else round(mean, 4),
                      "valid_fraction": round(float(valid.sum() / n_inside), 4),
                      "run": rows[d]["run"], "label": rows[d]["label"], "granules": rows[d]["granules"]})

    area_km2 = float(bprov["area_km2"])
    monthly = []
    for mth in months:
        rows_m = [x for x in daily if x["date"].startswith(mth) and x["mm"] is not None]
        y, mo = int(mth[:4]), int(mth[5:])
        ndays = (dt.date(y + (mo == 12), mo % 12 + 1, 1) - dt.date(y, mo, 1)).days
        in_window = [d for d in wanted if d.strftime("%Y-%m") == mth]
        mm = sum(x["mm"] for x in rows_m)
        monthly.append({"month": mth, "run": declared[mth], "days": len(rows_m), "days_in_window": len(in_window),
                        "days_in_month": ndays, "complete": len(rows_m) == ndays,
                        "labels": sorted(labels_by_month.get(mth, [])),
                        "mm": round(mm, 3), "km3": round(mm * 1e-6 * area_km2, 4),
                        "all_cells_valid": all(x["valid_fraction"] == 1.0 for x in rows_m)})
    total_mm = sum(m["mm"] for m in monthly)
    receipt = {
        "source": a.source,
        "run_declaration": a.run or ("nldas2" if a.source == "nldas2" else None),
        "runs_by_month": {m["month"]: m["run"] for m in monthly},
        "seams": seams,
        "window": {"start": start.isoformat(), "end": end.isoformat(), "days_requested": len(wanted),
                   "days_with_data": len(have), "days_absent": [d.isoformat() for d in absent]},
        "basin": {"fixture": a.basin.name, "site": bprov.get("site"), "geometry_sha256": bsha,
                  "area_km2": area_km2, "area_projection": bprov.get("area_projection")},
        "coverage": {"cells_in_window": int(mask.size), "cells_inside": n_inside,
                     "fraction_of_window_inside": round(n_inside / mask.size, 4),
                     "inside_cell_area_km2": round(inside_area, 1),
                     "inside_area_over_polygon_area": round(inside_area / area_km2, 4),
                     "cell_size_deg": [float(abs(lat[1] - lat[0])), float(abs(lon[1] - lon[0]))],
                     "mean": "cosine-latitude weighted over cells whose centre is inside the polygon",
                     "volume": "basin-mean depth times the polygon's equal-area area from its provenance"},
        "monthly": monthly,
        "total": {"mm": round(total_mm, 3), "km3": round(total_mm * 1e-6 * area_km2, 4),
                  "complete": all(m["complete"] for m in monthly)},
        "daily": daily,
        "window_files": meta,
        "consulted": ["knowledge/datasets/imerg-v07.md", "knowledge/gotchas/imerg-run-mixing.md",
                      "knowledge/gotchas/imerg-cold-season-orographic-underestimation.md",
                      "knowledge/connectors/gesdisc-earthaccess.md"] if a.source == "imerg" else
                     ["knowledge/datasets/nldas2-forcing.md", "knowledge/connectors/gesdisc-earthaccess.md"],
        "produced": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "script": "verification/fixtures/load_precipitation.py",
    }
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(json.dumps(receipt, indent=1))

    print(f"{a.source} over {a.basin.name} ({bprov.get('site', '')}, {area_km2:,.1f} km2): {start} to {end}, "
          f"{len(have)} of {len(wanted)} days; {n_inside} of {mask.size} window cells inside "
          f"({100 * inside_area / area_km2:.1f}% of the polygon area by cell area)")
    print("month     run     days  mm       km3")
    for m in monthly:
        flag = "" if m["complete"] else "  (incomplete)"
        print(f"{m['month']}   {m['run']:<7} {m['days']:>3}  {m['mm']:>8.2f} {m['km3']:>8.3f}{flag}")
    print(f"total             {len(have):>3}  {total_mm:>8.2f} {total_mm * 1e-6 * area_km2:>8.3f}")
    for s in seams:
        print(f"SEAM {s['date']} ({s['kind']}): {s.get('note')}")
    if absent:
        print(f"{len(absent)} requested day(s) without data, first {absent[0]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
