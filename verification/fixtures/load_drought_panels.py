# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas", "pyarrow"]
# ///
"""Assemble one period's drought panels into a receipt, each panel
carrying its own product, its own counts and its own refusal.

This builds ONE period. A drought view is a comparison, and the
comparison is made by putting two of these receipts side by side, which
is the caller's job. The tool never sees two periods at once, so it
cannot average them, rank them, or reduce them to an index; that is a
property of the shape rather than a rule someone has to remember.

The five panels and what each one refuses:

- **Precipitation** comes from the precipitation loader's receipt, so
  the run is already declared there and any seam is already named. This
  reads the run back and refuses a receipt whose months are not all one
  run, because a deficit computed across a calibration change is a
  deficit in the calibration.
- **Soil moisture** carries the count of cells actually retrieved
  beside every mean. The retrieval skips frozen, snow covered, densely
  vegetated and open water cells, so in a snowy basin a winter mean can
  rest on a few per cent of the basin, and a fall in the mean across a
  freeze is the sampling changing rather than the soil drying. The
  panel reports the mean, the count, and the fraction of the basin it
  represents, and refuses to report a mean at all on a day with no
  retrieved cells.
- **Streamflow** is labelled with the regulation the record carries.
  Below a major dam the panel is an operations record: it will not fall
  in a drought the way an unregulated river does, and reading it as a
  runoff signal is the mistake this label exists to prevent.
- **Storage** stops at the record's last epoch rather than at the
  window's end, and is refused outright for a basin below the mascon
  footprint floor. The effective sample size is the mascon count, not
  the cell count.
- **Snow** is a model output. It is a comparison between periods, which
  is the use its distributor sanctions, and never a term in a budget.

Usage:
  uv run verification/fixtures/load_drought_panels.py --label lees_ferry_wy2021 \
      --basin verification/fixtures/basins/usgs_09380000_nldi.geojson \
      --precipitation-receipt p_wy2021.json \
      --soil-moisture verification/fixtures/smap/smap_l3_lees_ferry_wy2021.json \
      --streamflow verification/fixtures/lees_ferry_00060_wy2021_dv.parquet \
      --storage verification/fixtures/grace/mascon_lees_ferry_wy2021.json \
      --snow verification/fixtures/snodas/snodas_swe_lees_ferry_wy2021.json \
      --out receipt.json
"""
import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

import pandas as pd

FOOTPRINT_FLOOR_KM2 = 111266.4     # the median mostly-land mascon, derived in the storage fixture


def die(msg):
    print(f"REFUSED: {msg}", file=sys.stderr)
    raise SystemExit(2)


def sha(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def source(p: Path):
    return {"path": p.name, "sha256": sha(p)}


def precipitation_panel(p: Path):
    d = json.loads(p.read_text())
    runs = sorted(set(d["runs_by_month"].values()))
    if len(runs) != 1:
        die(f"the precipitation receipt mixes runs {runs}; a deficit computed across a "
            "calibration change is a deficit in the calibration, so declare one run")
    months = d["monthly"]
    return {
        "product": d.get("source", "precipitation"), "run": runs[0],
        "months": len(months),
        "total_mm": round(sum(m["mm"] for m in months), 2),
        "monthly_mm": {m["month"]: round(m["mm"], 2) for m in months},
        "cannot_show": ("a total, not a rank: a percentile needs a climatology from the same "
                        "run, and the run that covers the present is not the run that covers "
                        "the archive"),
        "source": source(p),
    }


def soil_moisture_panel(p: Path):
    d = json.loads(p.read_text())
    rows = [r for r in d["rows"] if r.get("cells_retrieved")]
    inside = d["window"]["cells_inside_polygon"]
    by_month = {}
    for r in rows:
        by_month.setdefault(r["date"][:7], []).append(r)
    monthly = {}
    for m, rs in sorted(by_month.items()):
        cells = sum(x["cells_retrieved"] for x in rs)
        if not cells:
            continue
        # Weighted by the cells behind each day, so a day that saw three
        # cells does not count as much as a day that saw two hundred.
        monthly[m] = {
            "mean_m3m3": round(sum(x["mean_m3m3"] * x["cells_retrieved"] for x in rs) / cells, 5),
            "days": len(rs),
            "mean_cells_retrieved": round(cells / len(rs), 1),
            "coverage": round(cells / len(rs) / inside, 4),
        }
    thin = sorted(m for m, v in monthly.items() if v["coverage"] < 0.25)
    return {
        "product": d["product"], "variable": d["variable"], "units": d["units"],
        "overpass": d["overpass"], "record_begins": d["record_begins"],
        "cells_inside_polygon": inside,
        "days_with_any_retrieval": len(rows), "days_in_window": len(d["rows"]),
        "monthly": monthly,
        "months_under_quarter_coverage": thin,
        "cannot_show": ("a mean is the mean of the cells retrieved that day, and the retrieval "
                        "skips frozen, snow covered and open water ground, so a change across "
                        "a freeze is the sampling moving and not the soil drying; the record "
                        f"begins {d['record_begins']}, which is too short for a percentile"),
        "source": source(p),
    }


def streamflow_panel(p: Path, regulated: bool, note: str):
    df = pd.read_parquet(p)
    v = df["value"].astype(float)
    return {
        "site": str(df["monitoring_location_id"].iloc[0]),
        "parameter": str(df["parameter_code"].iloc[0]),
        "unit": str(df["unit_of_measure"].iloc[0]),
        "days": int(len(df)),
        "mean": round(float(v.mean()), 1),
        "min": round(float(v.min()), 1), "max": round(float(v.max()), 1),
        "approval": df["approval_status"].value_counts().to_dict(),
        "regulated": regulated,
        "cannot_show": (note if regulated else
                        "the gauge's own record, with its approval status and qualifiers"),
        "source": source(p),
    }


def storage_panel(p: Path, basin_area_km2: float):
    d = json.loads(p.read_text())
    if basin_area_km2 < FOOTPRINT_FLOOR_KM2:
        die(f"the basin is {basin_area_km2:,.0f} km2 against a mascon footprint floor of "
            f"{FOOTPRINT_FLOOR_KM2:,.0f} km2, so it has no storage signal of its own and this "
            "panel is refused rather than drawn at a scale it cannot support")
    ep = d["epochs"]
    # The fixture pads the epoch list either side of the window so the
    # bounding months are available, so the first and last rows are not
    # the period's ends. The change across the period is measured between
    # the epochs nearest its own bounds, and both dates are reported so a
    # reader can see what "across the year" meant here.
    w0 = dt.date.fromisoformat(d["window"]["start"])
    w1 = dt.date.fromisoformat(d["window"]["end"])
    near = lambda t: min(ep, key=lambda e: abs(dt.date.fromisoformat(e["epoch"]) - t))
    a0, a1 = near(w0), near(w1)
    return {
        "product": d["product"], "mascons": d["mascons"], "mascon_ids": d["mascon_ids"],
        "epochs": len(ep),
        "window": d["window"],
        "at_period_start": {"epoch": a0["epoch"], "lwe_cm": a0["lwe_cm"]},
        "at_period_end": {"epoch": a1["epoch"], "lwe_cm": a1["lwe_cm"]},
        "first": {"epoch": ep[0]["epoch"], "lwe_cm": ep[0]["lwe_cm"]},
        "last": {"epoch": ep[-1]["epoch"], "lwe_cm": ep[-1]["lwe_cm"]},
        "min": min(e["lwe_cm"] for e in ep), "max": max(e["lwe_cm"] for e in ep),
        "change_cm": round(a1["lwe_cm"] - a0["lwe_cm"], 3),
        "typical_uncertainty_cm": round(sum(e["uncertainty_cm"] for e in ep) / len(ep), 3),
        "record_last_epoch": d["record_last_epoch"],
        "effective_sample_size": d["mascons"],
        "cannot_show": ("the basin at a finer scale than one mascon, and nothing past "
                        f"{d['record_last_epoch']}, where the record stops"),
        "source": source(p),
    }


def snow_panel(p: Path):
    d = json.loads(p.read_text())
    rows = [r for r in d["rows"] if r.get("status") == 200]
    peak = max(rows, key=lambda r: r["swe_mean_mm"])
    return {
        "product": d["product"], "layer": d["layer"]["header"].get("Description"),
        "is_model_output": True,
        "dates": len(rows),
        "peak": {"date": peak["date"], "basin_mean_swe_mm": peak["swe_mean_mm"],
                 "max_cell_swe_mm": peak["swe_max_mm"],
                 "cells_with_snow": peak["cells_with_snow"]},
        "series_mm": {r["date"]: r["swe_mean_mm"] for r in rows},
        "quantitative_use": d["quantitative_use"],
        "cannot_show": ("a budget term: the distributor states this is a model output and is "
                        "not recommended for quantitative water budget analysis, while a "
                        "comparison between periods over one area is the use it sanctions"),
        "source": source(p),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--label", required=True)
    ap.add_argument("--basin", required=True, type=Path)
    ap.add_argument("--precipitation-receipt", required=True, type=Path)
    ap.add_argument("--soil-moisture", required=True, type=Path)
    ap.add_argument("--streamflow", required=True, type=Path)
    ap.add_argument("--storage", required=True, type=Path)
    ap.add_argument("--snow", required=True, type=Path)
    ap.add_argument("--regulated", action="store_true",
                    help="the streamflow gauge is below a dam or diversion; the panel says so")
    ap.add_argument("--regulation-note", default=(
        "the outlet is regulated, so this panel is an operations record rather than a runoff "
        "signal and will not fall in a drought the way an unregulated river does"))
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()

    doc = json.loads(a.basin.read_text())
    prov = doc.get("provenance", {})
    area = float(prov.get("area_km2") or 0)

    receipt = {
        "label": a.label,
        "basin": {"fixture": a.basin.name, "area_km2": area,
                  "mascons": round(area / FOOTPRINT_FLOOR_KM2, 2),
                  "above_footprint_floor": area >= FOOTPRINT_FLOOR_KM2,
                  "site": prov.get("site", "")},
        "panels": {
            "precipitation": precipitation_panel(a.precipitation_receipt),
            "soil_moisture": soil_moisture_panel(a.soil_moisture),
            "streamflow": streamflow_panel(a.streamflow, a.regulated, a.regulation_note),
            "storage": storage_panel(a.storage, area),
            "snow": snow_panel(a.snow),
        },
        "no_index": ("these panels are not combined. They measure different quantities over "
                     "different depths and times, with different validity, and a single "
                     "number would hide the disagreements that make the view worth having"),
        "generated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    text = json.dumps(receipt, indent=1)
    if a.out:
        a.out.write_text(text)
        print(f"{a.out}: five panels for {a.label}", file=sys.stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
