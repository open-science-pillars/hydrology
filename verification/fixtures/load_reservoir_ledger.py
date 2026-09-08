# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""A reservoir ledger in volume units, with every conversion's source named.

The identity, over one window:

    dS = I_gauged + I_ungauged + P - O - E - B

storage change, gauged inflow, ungauged inflow, precipitation on the
water surface, outflow, evaporation, bank storage. This tool measures
the first, the second and the fifth, and it does not measure the rest.
So it reports the residual, names what is in it, and does not close the
identity by inventing a term. A ledger that closes because something
was assumed is not a ledger.

Three rules it enforces rather than documents.

**The datum is not optional.** The storage change comes from a pool
elevation read into an area-capacity table, and the two carry datums
that differ by about three feet at this reservoir. The table here is
NAVD88 with an NGVD29 column beside it, and the gauge publishes both
series, so the conversion is the agency's own. The loader refuses an
elevation whose datum it cannot match to a column, because the mistake
costs about 196,000 acre-feet in a stated volume and is invisible in
the arithmetic.

**The table revision is part of the answer.** Reservoirs are
resurveyed and the survey replaces the table: Lake Powell lost four per
cent of its capacity between the 1986 and 2018 surveys. The receipt
names the table, its DOI and its hash.

**The ungauged fraction is a term, not a rounding.** The inflow gauges
here drain 82.2 per cent of the area above the dam, so a fifth of the
basin arrives unmeasured. The receipt states the fraction and puts the
ungauged inflow in the residual by name, rather than letting a ledger
that omits it close better than it should.

Usage:
  uv run verification/fixtures/load_reservoir_ledger.py \
      --inputs verification/fixtures/reservoir/ledger_powell_wy2023.json \
      --datum NAVD88 --out receipt.json
"""
import argparse
import csv
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

CFS_DAY_ACREFEET = 1.983471          # one cubic foot per second for one day
ACREFOOT_KM3 = 1.233481837548e-6
DATUM_COLUMN = {"NAVD88": "Elevation_ft_NAVD88", "NGVD29": "Elevation_ft_NGVD29"}
PARAMETER_DATUM = {"62614": "NGVD29", "62615": "NAVD88"}


def die(msg):
    print(f"REFUSED: {msg}", file=sys.stderr)
    raise SystemExit(2)


def read_table(path: Path, datum: str):
    col = DATUM_COLUMN[datum]
    rows = list(csv.DictReader(path.read_text().splitlines()))
    if col not in rows[0]:
        die(f"the area-capacity table has no {datum} column, so an elevation on that datum "
            f"cannot be read into it; the table carries {sorted(rows[0])}")
    elev = [float(r[col]) for r in rows]
    area = [float(r["Area_acres"]) for r in rows]
    cap = [float(r["Capacity_acrefeet"]) for r in rows]
    if elev != sorted(elev):
        die("the area-capacity table is not sorted by elevation")
    return elev, area, cap


def interp(xs, ys, x, what):
    if x < xs[0] or x > xs[-1]:
        die(f"{x:.2f} ft is outside the table, which runs {xs[0]:.2f} to {xs[-1]:.2f}; "
            f"no {what} is extrapolated from an area-capacity table")
    for i in range(1, len(xs)):
        if xs[i] >= x:
            f = (x - xs[i - 1]) / (xs[i] - xs[i - 1])
            return ys[i - 1] + f * (ys[i] - ys[i - 1])


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--inputs", required=True, type=Path)
    ap.add_argument("--datum", default="NAVD88", choices=sorted(DATUM_COLUMN))
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()

    doc = json.loads(a.inputs.read_text())
    series = doc["series"]
    tbl_meta = doc["area_capacity_table"]
    tbl = a.inputs.parent / tbl_meta["file"]
    if hashlib.sha256(tbl.read_bytes()).hexdigest() != tbl_meta["sha256"]:
        die(f"{tbl_meta['file']} is not the bytes the manifest recorded; a volume from a table "
            "that moved is not the volume that was published")

    # The elevation series whose parameter code declares the datum asked
    # for. The parameter code is the authority: 62614 is above NGVD29 and
    # 62615 above NAVD88, and the site file's own altitude datum is a
    # different fact about the gauge's benchmark.
    picked = [k for k, s in series.items()
              if PARAMETER_DATUM.get(s["parameter"]) == a.datum]
    if not picked:
        die(f"no series in this input carries an elevation on {a.datum}; the parameter codes "
            f"present are {sorted({s['parameter'] for s in series.values()})}, and an elevation "
            "is not converted between datums here")
    elev_key = picked[0]
    es = series[elev_key]
    days = sorted(es["values"])
    e0, e1 = float(es["values"][days[0]]), float(es["values"][days[-1]])

    elev, area, cap = read_table(tbl, a.datum)
    c0 = interp(elev, cap, e0, "capacity")
    c1 = interp(elev, cap, e1, "capacity")
    a0 = interp(elev, area, e0, "area")
    a1 = interp(elev, area, e1, "area")
    dS = c1 - c0

    # The other datum, reported beside it so the cost of the confusion is
    # visible rather than asserted.
    other = "NGVD29" if a.datum == "NAVD88" else "NAVD88"
    alt = [k for k, s in series.items() if PARAMETER_DATUM.get(s["parameter"]) == other]
    datum_note = None
    if alt:
        os_ = series[alt[0]]
        o0, o1 = float(os_["values"][days[0]]), float(os_["values"][days[-1]])
        offsets = [float(es["values"][d]) - float(os_["values"][d])
                   for d in days if d in os_["values"]]
        wrong0 = interp(elev, cap, o0, "capacity") if elev[0] <= o0 <= elev[-1] else None
        wrong1 = interp(elev, cap, o1, "capacity") if elev[0] <= o1 <= elev[-1] else None
        datum_note = {
            "other_datum": other,
            "other_series_capture": os_["capture_id"],
            "offset_ft": {"mean": round(sum(offsets) / len(offsets), 4),
                          "min": round(min(offsets), 3), "max": round(max(offsets), 3),
                          "days": len(offsets)},
            "source": ("the agency publishes both series for this gauge, so the offset is its "
                       "own conversion and is not derived here; the table carries both columns "
                       "and agrees"),
            "cost_of_reading_the_other_datum_into_this_column": {
                "start_acrefeet": round(c0 - wrong0, 0) if wrong0 else None,
                "end_acrefeet": round(c1 - wrong1, 0) if wrong1 else None,
                "change_acrefeet": round(dS - (wrong1 - wrong0), 0) if wrong0 and wrong1 else None,
                "note": ("the error is large in a level and small in a change, because it mostly "
                         "cancels in a difference; a ledger that only reports changes can carry "
                         "this mistake for years"),
            },
        }

    flows, gauged_area = {}, 0.0
    for k, s in series.items():
        if s["parameter"] != "00060":
            continue
        v = sum(float(x) for x in s["values"].values()) * CFS_DAY_ACREFEET
        role = "outflow" if k.startswith("outflow") else "inflow"
        flows[k] = {"site": s["site"], "site_name": s["site_name"], "role": role,
                    "days": s["days"], "acrefeet": round(v, 0),
                    "km3": round(v * ACREFOOT_KM3, 4),
                    "drainage_area_mi2": s["drainage_area_mi2"],
                    "capture_id": s["capture_id"], "approval": s["approval"]}
        if role == "inflow":
            gauged_area += s["drainage_area_mi2"] or 0

    inflow = sum(f["acrefeet"] for f in flows.values() if f["role"] == "inflow")
    outflow = sum(f["acrefeet"] for f in flows.values() if f["role"] == "outflow")
    outlet_area = next((f["drainage_area_mi2"] for f in flows.values()
                        if f["role"] == "outflow"), None)
    residual = dS - (inflow - outflow)

    receipt = {
        "reservoir": doc["reservoir"],
        "window": doc["window"],
        "datum": a.datum,
        "storage": {
            "elevation_series": {"key": elev_key, "site": es["site"],
                                 "parameter": es["parameter"],
                                 "declares_datum": PARAMETER_DATUM[es["parameter"]],
                                 "capture_id": es["capture_id"]},
            "start": {"date": days[0], "elevation_ft": e0,
                      "capacity_acrefeet": round(c0, 0), "area_acres": round(a0, 0)},
            "end": {"date": days[-1], "elevation_ft": e1,
                    "capacity_acrefeet": round(c1, 0), "area_acres": round(a1, 0)},
            "elevation_change_ft": round(e1 - e0, 2),
            "change_acrefeet": round(dS, 0),
            "change_km3": round(dS * ACREFOOT_KM3, 4),
            "table": {k: tbl_meta[k] for k in ("file", "sha256", "doi", "title", "published",
                                               "survey", "datum")},
            "interpolation": "linear between the table's steps, which are about 0.33 ft apart",
        },
        "datum_check": datum_note,
        "flows": flows,
        "totals": {
            "gauged_inflow_acrefeet": round(inflow, 0),
            "outflow_acrefeet": round(outflow, 0),
            "gauged_inflow_minus_outflow_acrefeet": round(inflow - outflow, 0),
            "measured_storage_change_acrefeet": round(dS, 0),
            "residual_acrefeet": round(residual, 0),
            "residual_as_fraction_of_inflow": round(residual / inflow, 5) if inflow else None,
        },
        "ungauged": {
            "gauged_drainage_mi2": gauged_area,
            "outlet_drainage_mi2": outlet_area,
            "gauged_fraction": round(gauged_area / outlet_area, 5) if outlet_area else None,
            "note": ("the inflow gauges do not span the basin above the dam, so ungauged inflow "
                     "is in the residual by name; these are total drainage areas, since "
                     "contributing areas are not published for these sites"),
        },
        "residual_contains": [
            "ungauged inflow from the fraction of the basin no gauge here measures",
            "precipitation on the water surface",
            "evaporation from the water surface, which no gauge in this ledger measures and "
            "which the satellite evapotranspiration product does not estimate over open water",
            "bank storage, which moves into the banks while the reservoir fills and back out "
            "when it falls",
            "the reach between the dam and the outflow gauge, which is not the dam release",
            "travel time, since the inflow gauges are hundreds of miles upstream",
        ],
        "not_closed": ("the identity is not closed here. The terms above are named and not "
                       "measured, so the residual is reported as a residual; a ledger that "
                       "closes by assuming one of them is not a measurement"),
        "generated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_manifest": {"path": a.inputs.name,
                            "sha256": hashlib.sha256(a.inputs.read_bytes()).hexdigest()},
    }
    text = json.dumps(receipt, indent=1)
    if a.out:
        a.out.write_text(text)
        print(f"{a.out}: {doc['reservoir']} {doc['window']['convention']} on {a.datum}",
              file=sys.stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
