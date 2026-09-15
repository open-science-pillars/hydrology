# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=1.26,<3"]
# ///
"""Attester for the basin water balance: recompute from the receipt and
apply the bars.

The attester trusts nothing in the receipt but the inputs it names. It
re-reads the frozen tree, checks every file against the hash the
receipt recorded, recomputes each term from those files, and compares
its own numbers with the receipt's. Then it applies the bars, which
are the bars for an OBSERVATIONAL budget and not the numerical-closure
bars of a model budget:

  Bar one, consistency: the residual is within k times the quadrature
  sum of the four term uncertainties. k is 2 by default, and 2 is a
  choice with a reason: each term's uncertainty is a documented
  one-sigma figure from its own product, the four are independent
  enough for a quadrature sum to be the honest combination, and a
  budget of four remote-sensing terms that agreed inside one sigma
  would be evidence of a tuned term rather than of closure. A basin
  whose residual passes at k=2 is consistent with its terms; it is not
  thereby correct.

  Bar two, reproducibility: every recomputed value matches the
  receipt's within a stated numerical tolerance (1e-6 km3 absolute,
  which is a cubic metre per side and far below any term's precision).
  This bar fails on a doctored receipt, a moved input file, or a
  change in the executor that the receipt's code hash does not
  acknowledge.

  Bar three, plausibility of the groundwater term, applied only when
  the receipt carries one: the specific yield inside (0, 0.5], the
  site count at or above the parameters' minimum, every site's level
  change and the mean within 30 m, the partition arithmetic exact,
  and the part no larger than the whole: the groundwater change does
  not exceed the total storage change by more than k times their
  combined sigma. The term is recomputed here from the frozen well
  set with this file's own arithmetic, which shares no code with the
  executor.

A receipt whose storage term was refused below the footprint floor has
no residual, so bar one does not apply and the attester says so rather
than passing it silently.

The receipt's `code_sha256` is checked against the sanctioned
computation file, so a receipt produced by an edited executor fails
even when its arithmetic is right: that is what makes the ritual's
"old against new" step mean anything.

Every check prints a PASS or FAIL line and the process exits nonzero
on any FAIL.

Usage: basin_water_balance_check.py RECEIPT.json [--computation PATH] [-k 2]
       basin_water_balance_check.py --selftest
"""
import argparse
import datetime as dt
import hashlib
import json
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

TOL_KM3 = 1e-6
CFS_TO_KM3_PER_DAY = 0.0283168466 * 86400 / 1e9
FT_TO_M = 0.3048
EARTH_R_KM = 6371.0088
SPECIFIC_YIELD_BOUND = 0.5      # no aquifer material drains more than half its volume
LEVEL_CHANGE_BOUND_M = 30.0     # a water table moving more than this in a year is a data problem, not a term


class Fail(Exception):
    pass


def fail(msg):
    raise Fail(msg)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close(a, b, tol=TOL_KM3):
    return abs(float(a) - float(b)) <= tol


def haversine_km(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    c = (math.sin(p1) * math.sin(p2)
         + math.cos(p1) * math.cos(p2) * math.cos(math.radians(lon2 - lon1)))
    return EARTH_R_KM * math.acos(max(-1.0, min(1.0, c)))


def recompute_groundwater(gw: dict, start: dt.date, end: dt.date, area_km2: float) -> dict:
    """The groundwater term again, from the frozen well set and its
    parameters, in this file's own words: end-window means per
    unconfined well, the rise as first minus last depth, wells within
    the radius as one site, the mean rise over sites times the specific
    yield times the area."""
    prm = gw["parameters"]
    sy, sy_sigma = float(prm["specific_yield"]["value"]), float(prm["specific_yield"]["sigma"])
    n_end, min_days = int(prm["end_window_days"]), int(prm["min_days_per_end"])
    radius, min_sites = float(prm["cluster_radius_km"]), int(prm["min_sites"])
    first_hi = start + dt.timedelta(days=n_end - 1)
    last_lo = end - dt.timedelta(days=n_end - 1)
    used = []
    for w in sorted(gw["wells"], key=lambda x: x["site"]):
        if w.get("aquifer_type_code") != "U":
            continue
        first = [float(r["v"]) for r in w["rows"] if r["v"] not in (None, "", "--")
                 and start <= dt.date.fromisoformat(r["t"]) <= first_hi]
        last = [float(r["v"]) for r in w["rows"] if r["v"] not in (None, "", "--")
                and last_lo <= dt.date.fromisoformat(r["t"]) <= end]
        if len(first) < min_days or len(last) < min_days:
            continue
        used.append((w["site"], w["lat"], w["lon"], (sum(first) / len(first) - sum(last) / len(last)) * FT_TO_M))
    clusters = []
    for site, lat, lon, rise in used:
        for c in clusters:
            if any(haversine_km(lat, lon, m[1], m[2]) <= radius for m in c):
                c.append((site, lat, lon, rise))
                break
        else:
            clusters.append([(site, lat, lon, rise)])
    rises = [sum(m[3] for m in c) / len(c) for c in clusters]
    out = {"wells_used": len(used), "sites": len(clusters), "min_sites": min_sites,
           "specific_yield": sy, "specific_yield_sigma": sy_sigma, "site_rises_m": rises}
    if len(clusters) < min_sites:
        return {**out, "refused": True}
    mean_m = sum(rises) / len(rises)
    sd = math.sqrt(sum((r - mean_m) ** 2 for r in rises) / (len(rises) - 1)) if len(rises) > 1 else 0.0
    se = sd / math.sqrt(len(rises))
    return {**out, "refused": False, "mean_rise_m": mean_m, "spread_sd_m": sd,
            "km3": sy * mean_m * area_km2 * 1e-3,
            "sigma_km3": area_km2 * 1e-3 * math.hypot(sy_sigma * mean_m, sy * se)}


def attest(receipt_path: Path, computation: Path, k: float) -> list[str]:
    """Every check as a line; a Fail is raised on the first failure."""
    lines = []
    r = json.loads(receipt_path.read_text())

    # The receipt has to say what it is before anything else is worth checking.
    for field in ("computation", "concept", "code_sha256", "tool_version", "identity", "basin",
                  "window", "inputs", "terms", "residual", "bookkeeping"):
        if field not in r:
            fail(f"the receipt has no {field}: an attester cannot check a receipt that does not say what it is")
    if r["computation"] != "basin-water-balance":
        fail(f"this receipt is for {r['computation']!r}, not the basin water balance")
    if not computation.is_file():
        fail(f"no such computation to check the receipt against: {computation}")
    want = hashlib.sha256(computation.read_bytes()).hexdigest()
    if r["code_sha256"] != want:
        fail(f"code_sha256 does not match the sanctioned computation: the receipt says {r['code_sha256'][:12]} "
             f"and {computation.name} hashes to {want[:12]}. A receipt from an edited executor is not "
             f"attested by this attester")
    lines.append(f"PASS: the receipt names the computation and its code_sha256 {want[:12]} is the executor on disk")

    tree = Path(r["inputs"]["tree"])
    if not tree.is_dir():
        fail(f"the input tree {tree} named by the receipt is not there; the recompute cannot be done")

    # Every stamp the receipt claims, checked against the bytes on disk,
    # AND every file the tree declares, checked to be claimed: iterating
    # the receipt's own list alone would let a receipt hide a file by
    # leaving it out, which is the cheapest doctoring there is.
    declared = set(json.loads((tree / "manifest.json").read_text())["files"])
    claimed = set(r["inputs"]["files"])
    if declared - claimed:
        fail(f"the receipt carries no stamp for {', '.join(sorted(declared - claimed))}: the frozen tree "
             f"declares {len(declared)} files and the receipt claims {len(claimed)}. A receipt that omits an "
             f"input is not a record of what was computed")
    if claimed - declared:
        fail(f"the receipt claims {', '.join(sorted(claimed - declared))}, which the frozen tree does not declare")
    for name, rec in r["inputs"]["files"].items():
        p = tree / name
        if not p.is_file():
            fail(f"{name} is named in the receipt and missing from the tree")
        got = sha256(p)
        if got != rec["sha256"]:
            fail(f"{name} does not match the receipt: sha256 {got[:12]} against the receipt's {rec['sha256'][:12]}")
    # Every term's own stamp is one of those files, with the same hash.
    for name, term in r["terms"].items():
        if "stamp" in term:
            st_ = term["stamp"]
            if st_["file"] not in r["inputs"]["files"] or r["inputs"]["files"][st_["file"]]["sha256"] != st_["sha256"]:
                fail(f"the {name} term's stamp {st_['file']} {st_['sha256'][:12]} is not a stamp of the tree")
    lines.append(f"PASS: {len(r['inputs']['files'])} input files match the hashes the receipt recorded, and "
                 f"every term's stamp is one of them")

    man = json.loads((tree / "manifest.json").read_text())
    if man["window"]["start"] != r["window"]["start"] or man["window"]["end"] != r["window"]["end"]:
        fail("the receipt's window is not the frozen tree's window")

    start = dt.date.fromisoformat(r["window"]["start"])
    end = dt.date.fromisoformat(r["window"]["end"])
    p = json.loads((tree / "precipitation.json").read_text())
    et = json.loads((tree / "evapotranspiration.json").read_text())
    q = json.loads((tree / "discharge.json").read_text())
    st = json.loads((tree / "storage.json").read_text())
    basin = json.loads((tree / "basin.geojson").read_text())
    area = float(basin["provenance"]["area_km2"])

    if not close(area, r["basin"]["area_km2"], 1e-3):
        fail(f"the basin area in the receipt ({r['basin']['area_km2']}) is not the polygon's ({area})")

    # Term by term, recomputed from the frozen files.
    if not close(p["total"]["km3"], r["terms"]["precipitation"]["km3"]):
        fail(f"precipitation: receipt {r['terms']['precipitation']['km3']}, recomputed {p['total']['km3']}")
    if not close(et["total"]["km3"], r["terms"]["evapotranspiration"]["km3"]):
        fail(f"evapotranspiration: receipt {r['terms']['evapotranspiration']['km3']}, recomputed {et['total']['km3']}")

    rows = next(s["rows"] for s in q["series"] if s.get("parameter") == "00060" and s.get("statistic") == "00003")
    q_km3 = sum(float(x["v"]) * CFS_TO_KM3_PER_DAY for x in rows
                if start <= dt.date.fromisoformat(x["t"]) <= end and x["v"] not in (None, "", "--"))
    if not close(q_km3, r["terms"]["discharge"]["km3"], 1e-5):
        fail(f"discharge: receipt {r['terms']['discharge']['km3']}, recomputed {round(q_km3, 6)}")
    lines.append("PASS: precipitation, evapotranspiration and discharge recomputed from the frozen files")

    floor = st["footprint_scale"]["median_land_mascon_km2"]
    refused = r["terms"]["storage"].get("refused", False)
    if (area < floor) != refused:
        fail(f"the storage term's refusal does not follow the floor: basin {area:,.0f} km2, floor {floor:,.0f} km2, "
             f"receipt says refused={refused}")

    # The groundwater term, when the tree carries one: recomputed here
    # with this file's own arithmetic and held to bar three.
    gw_r = r["terms"].get("groundwater")
    gw = None
    if ("groundwater.json" in declared) != (gw_r is not None):
        fail("the tree carries groundwater.json and the receipt carries no groundwater term, or the reverse")
    if gw_r is not None:
        gw = recompute_groundwater(json.loads((tree / "groundwater.json").read_text()), start, end, area)
        if gw["wells_used"] != gw_r["wells_used"] or gw["sites"] != gw_r["sites"]:
            fail(f"groundwater well set: receipt {gw_r['wells_used']} wells over {gw_r['sites']} sites, recomputed "
                 f"{gw['wells_used']} over {gw['sites']}")
        if not close(gw["specific_yield"], gw_r["specific_yield"], 1e-12) or \
                not close(gw["specific_yield_sigma"], gw_r["specific_yield_sigma"], 1e-12):
            fail(f"groundwater: the receipt's specific yield {gw_r['specific_yield']} +- {gw_r['specific_yield_sigma']} "
                 f"is not the tree's {gw['specific_yield']} +- {gw['specific_yield_sigma']}")
        if not (0 < gw["specific_yield"] <= SPECIFIC_YIELD_BOUND):
            fail(f"bar three: specific yield {gw['specific_yield']} is outside (0, {SPECIFIC_YIELD_BOUND}]")
        if not gw["specific_yield_sigma"] >= 0:
            fail("bar three: the specific yield's sigma is negative")
        if not gw_r.get("specific_yield_source"):
            fail("bar three: the specific yield carries no source; a parameter without one is a guess")
        if gw["refused"] != gw_r["refused"]:
            fail(f"the groundwater term's refusal does not follow the site count: {gw['sites']} sites against "
                 f"{gw['min_sites']}, receipt says refused={gw_r['refused']}")
        if not gw["refused"]:
            if any(abs(x) > LEVEL_CHANGE_BOUND_M for x in gw["site_rises_m"]):
                fail(f"bar three: a site's water-level change exceeds {LEVEL_CHANGE_BOUND_M} m")
            if not close(gw["mean_rise_m"], gw_r["mean_rise_m"], 1e-3):
                fail(f"groundwater mean rise: receipt {gw_r['mean_rise_m']} m, recomputed {round(gw['mean_rise_m'], 4)}")
            if not close(gw["spread_sd_m"], gw_r["spread_sd_m"], 1e-3):
                fail(f"groundwater spread: receipt {gw_r['spread_sd_m']} m, recomputed {round(gw['spread_sd_m'], 4)}")
            if not close(gw["km3"], gw_r["km3"], 1e-5):
                fail(f"groundwater: receipt {gw_r['km3']}, recomputed {round(gw['km3'], 6)}")
            if not close(gw["sigma_km3"], gw_r["sigma_km3"], 1e-5):
                fail(f"groundwater sigma: receipt {gw_r['sigma_km3']}, recomputed {round(gw['sigma_km3'], 6)}")
            lines.append(f"PASS: groundwater term recomputed from the frozen well set: {gw['wells_used']} wells, "
                         f"{gw['sites']} sites, mean rise {gw['mean_rise_m']:+.4f} m, {gw['km3']:+.3f} km3 at "
                         f"specific yield {gw['specific_yield']}")
        else:
            lines.append(f"PASS: groundwater term refused on {gw['sites']} sites against {gw['min_sites']}, as the "
                         f"parameters require")

    if refused:
        if r["residual"].get("reported", False):
            fail("the storage term was refused and the receipt reports a residual anyway")
        lines.append(f"PASS (refusal): storage refused below the floor ({area:,.0f} km2 against {floor:,.0f} km2) "
                     f"and no residual is reported, as the concept requires")
        lines.append("bar one, consistency: not applicable, there is no residual to test")
        lines.append(f"bar two, reproducibility: every recomputed value matches the receipt within {TOL_KM3} km3")
        return lines

    epochs = {e["epoch"]: e for e in st["epochs"]}
    for label in ("first_epoch", "last_epoch"):
        if r["terms"]["storage"][label] not in epochs:
            fail(f"the receipt's {label} {r['terms']['storage'][label]} is not an epoch of the frozen series")
    d_cm = (epochs[r["terms"]["storage"]["last_epoch"]]["lwe_cm"]
            - epochs[r["terms"]["storage"]["first_epoch"]]["lwe_cm"])
    ds_km3 = d_cm * 0.01 * 1e-3 * area
    if not close(ds_km3, r["terms"]["storage"]["km3"], 1e-5):
        fail(f"storage: receipt {r['terms']['storage']['km3']}, recomputed {round(ds_km3, 6)}")
    lines.append(f"PASS: storage recomputed from the frozen mascon series over {r['terms']['storage']['mascons']} mascons")

    i_km3 = r["terms"]["imports"]["km3"]
    x_km3 = r["terms"]["exports"]["km3"]
    for label in ("imports", "exports"):
        for entry in r["terms"][label]["entries"]:
            if not entry.get("source"):
                fail(f"an {label} entry carries no source; an unsourced transfer is not a term")
        if not r["terms"][label]["entries"] and "assumption" not in r["terms"][label]:
            fail(f"{label} is empty and the receipt does not state the assumption")

    resid = (r["terms"]["precipitation"]["km3"] + i_km3 - r["terms"]["evapotranspiration"]["km3"]
             - r["terms"]["discharge"]["km3"] - x_km3 - r["terms"]["storage"]["km3"])
    if not close(resid, r["residual"]["km3"], 1e-5):
        fail(f"residual: receipt {r['residual']['km3']}, recomputed {round(resid, 6)}")
    sig = float(np.sqrt(r["terms"]["precipitation"]["sigma_km3"] ** 2
                        + r["terms"]["evapotranspiration"]["sigma_km3"] ** 2
                        + r["terms"]["discharge"]["sigma_km3"] ** 2
                        + r["terms"]["storage"]["sigma_km3"] ** 2))
    if not close(sig, r["residual"]["sigma_km3"], 1e-5):
        fail(f"combined sigma: receipt {r['residual']['sigma_km3']}, recomputed {round(sig, 6)}")
    lines.append("PASS: residual and combined sigma recomputed from the terms")

    if gw is not None and not gw["refused"]:
        pt = r["residual"].get("partition")
        if not pt:
            fail("a groundwater term is present and the residual carries no partition")
        other = r["terms"]["storage"]["km3"] - gw_r["km3"]
        left = (r["terms"]["precipitation"]["km3"] + i_km3 - r["terms"]["evapotranspiration"]["km3"]
                - r["terms"]["discharge"]["km3"] - x_km3 - gw_r["km3"])
        if not close(other, pt["other_storage_km3"], 1e-5) or not close(left, pt["terms_less_groundwater_km3"], 1e-5):
            fail("partition: dS_other or the terms less groundwater do not recompute from the terms")
        if not close(left, other + resid, 1e-5):
            fail("partition: P + I - ET - Q - X - dS_gw is not dS_other plus the residual")
        whole = abs(r["terms"]["storage"]["km3"]) + k * math.hypot(r["terms"]["storage"]["sigma_km3"],
                                                                   gw_r["sigma_km3"])
        if abs(gw_r["km3"]) > whole:
            fail(f"bar three: the groundwater change {gw_r['km3']:+.3f} km3 exceeds the total storage change "
                 f"{r['terms']['storage']['km3']:+.3f} km3 by more than k = {k:.1f} times their combined sigma; "
                 f"a part larger than the whole is a specific yield or a well set that does not describe this basin")
        if pt.get("groundwater_fraction_of_storage_change") is not None and \
                abs(r["terms"]["storage"]["km3"]) <= 2 * r["terms"]["storage"]["sigma_km3"]:
            fail("partition: a fraction of dS is reported while dS is within two sigma of zero")
        lines.append(f"PASS: partition dS = dS_gw + dS_other recomputed ({r['terms']['storage']['km3']:+.3f} = "
                     f"{gw_r['km3']:+.3f} + {other:+.3f} km3), and the part is no larger than the whole")
        lines.append(f"bar three, plausibility: specific yield {gw['specific_yield']} in (0, {SPECIFIC_YIELD_BOUND}], "
                     f"{gw['sites']} sites at or above {gw['min_sites']}, every site change within "
                     f"{LEVEL_CHANGE_BOUND_M:.0f} m, |dS_gw| {abs(gw_r['km3']):.3f} against |dS| + k sigma {whole:.3f} km3")

    ratio = abs(resid) / sig if sig else float("inf")
    bar_one = ratio <= k
    lines.append(f"bar one, consistency: |residual| / sigma = {ratio:.2f} against k = {k:.1f} -> "
                 f"{'within' if bar_one else 'outside'} the bar "
                 f"(residual {resid:+.3f} km3, sigma {sig:.3f} km3)")
    lines.append(f"bar two, reproducibility: every recomputed value matches the receipt within {TOL_KM3} km3")
    if r["terms"]["discharge"].get("regulated"):
        lines.append("note: the outlet gauge is regulated, so this residual carries reservoir operations as well as "
                     "hydrology; the flag is in the receipt and does not change the bars")
    if r["terms"]["storage"].get("endpoint_open"):
        lines.append("note: the closing endpoint is open, reported as open and not filled")
    if not bar_one:
        fail(f"bar one: |residual| / sigma = {ratio:.2f} is outside k = {k:.1f}")
    return lines


def run_attest(receipt_path: Path, computation: Path, k: float) -> int:
    try:
        lines = attest(receipt_path, computation, k)
    except Fail as e:
        print(f"FAIL: {e}")
        return 1
    print("\n".join(lines))
    return 0


# ------------------------------------------------------------- selftest
def _synthetic_tree(root: Path, with_groundwater: bool, sy: float = 0.2, n_wells: int = 6, rise_ft: float = 1.0):
    """A small frozen tree with round numbers, so the arithmetic of every
    term and of the groundwater partition can be checked by hand:
    P 100, ET 40, Q 30 km3 over a 200,000 km2 basin of 2 mascons,
    dS +6 cm of water (12 km3, six sigma from zero), and a well set
    whose water table rises rise_ft feet at every well."""
    start, end = dt.date(2022, 10, 1), dt.date(2023, 9, 30)
    days = (end - start).days + 1
    basin = {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {},
             "geometry": {"type": "Polygon", "coordinates": [[[-86, 38], [-84, 38], [-84, 40], [-86, 40], [-86, 38]]]}}],
             "provenance": {"area_km2": 200000.0, "site": "TEST-1", "geometry_sha256": "0" * 64}}
    q_cfs = 30 / (days * CFS_TO_KM3_PER_DAY)
    files = {
        "basin.geojson": basin,
        "precipitation.json": {"window": {"start": start.isoformat(), "end": end.isoformat()},
                               "total": {"km3": 100.0, "mm": 500.0}, "coverage": {},
                               "window_files": [{"short_name": "TEST_P", "run": "final", "doi": "none"}]},
        "evapotranspiration.json": {"total": {"km3": 40.0, "mm": 200.0},
                                    "window_files": [{"short_name": "TEST_ET", "version": "1", "doi": "none",
                                                      "tile": "h00v00"}],
                                    "coverage": {"masked_fraction_any_composite": 0.0,
                                                 "covered_area_over_polygon_area": 1.0},
                                    "open_water": {}},
        "discharge.json": {"capture_id": "selftest", "params": {"sites": "TEST"}, "content_sha256": "0" * 64,
                           "series": [{"parameter": "00060", "statistic": "00003",
                                       "rows": [{"t": (start + dt.timedelta(i)).isoformat(), "v": f"{q_cfs:.6f}",
                                                 "approval": "Approved", "qualifiers": []} for i in range(days)]}]},
        "storage.json": {"mascons": 2, "mascon_ids": [1, 2],
                         "footprint_scale": {"median_land_mascon_km2": 111266.4},
                         "epochs": [{"epoch": "2022-09-16", "lwe_cm": 0.0, "uncertainty_cm": 1.0},
                                    {"epoch": "2023-09-16", "lwe_cm": 6.0, "uncertainty_cm": 1.0}],
                         "record_last_epoch": "2026-06-16"},
    }
    if with_groundwater:
        wells = []
        for i in range(n_wells):
            depth0 = 20.0 + i
            rows = [{"t": (start + dt.timedelta(d)).isoformat(),
                     "v": f"{depth0 - rise_ft * d / (days - 1):.4f}", "approval": "Approved", "qualifiers": []}
                    for d in range(days)]
            wells.append({"site": f"TEST-{i:02d}", "name": f"well {i}", "lat": 38.5 + 0.2 * i, "lon": -85.0,
                          "aquifer_type_code": "U", "well_constructed_depth_ft": 50.0, "rows": rows})
        # A confined well and a well with a short record, both excluded by rule.
        wells.append({"site": "TEST-C", "lat": 39.9, "lon": -84.2, "aquifer_type_code": "C",
                      "well_constructed_depth_ft": 400.0, "rows": wells[0]["rows"]})
        wells.append({"site": "TEST-S", "lat": 39.8, "lon": -84.3, "aquifer_type_code": "U",
                      "well_constructed_depth_ft": 40.0, "rows": wells[0]["rows"][:10]})
        files["groundwater.json"] = {
            "parameter": "72019", "statistic": "00003", "unit": "ft below land surface",
            "window": {"start": start.isoformat(), "end": end.isoformat()},
            "parameters": {"specific_yield": {"value": sy, "sigma": 0.02, "source": "selftest: a stated value"},
                           "end_window_days": 30, "min_days_per_end": 20, "cluster_radius_km": 2.0,
                           "min_sites": 3},
            "captures": [], "selection": {}, "wells": wells}
    root.mkdir(parents=True, exist_ok=True)
    man_files = {}
    for name, body in files.items():
        (root / name).write_text(json.dumps(body))
        man_files[name] = {"sha256": sha256(root / name)}
    (root / "manifest.json").write_text(json.dumps({
        "basin": "selftest", "window": {"start": start.isoformat(), "end": end.isoformat()},
        "frozen_at": "2026-01-01T00:00:00Z", "frozen_by": "selftest", "files": man_files}))
    return root


def selftest(computation: Path) -> int:
    """The attester against receipts it can predict by hand: a tree with
    and without the groundwater term, then the doctorings each bar must
    catch. Prints PASS or FAIL per case and returns nonzero on any FAIL."""
    if not computation.is_file():
        print(f"FAIL: selftest needs the executor at {computation}")
        return 1
    tmp = Path(tempfile.mkdtemp(prefix="wb_selftest_"))
    failures = 0

    def case(name, ok, detail=""):
        nonlocal failures
        print(f"{'PASS' if ok else 'FAIL'}: selftest {name}" + (f" ({detail})" if detail else ""))
        failures += not ok

    def run(tree, receipt):
        p = subprocess.run([sys.executable, str(computation), "--inputs", str(tree), "--receipt", str(receipt)],
                           capture_output=True, text=True, cwd=tmp, env={**os.environ, "PYTHONPATH": ""})
        return p.returncode, p.stdout + p.stderr

    def attest_quiet(receipt, k=2.0):
        try:
            return 0, attest(receipt, computation, k)
        except Fail as e:
            return 1, [str(e)]

    # 1. Without the groundwater term: the four-term receipt attests and its
    #    arithmetic is the hand result, residual 100 - 40 - 30 - 12 = +18 km3.
    t0 = _synthetic_tree(tmp / "plain", with_groundwater=False)
    rc, out = run(t0, tmp / "plain.json")
    case("executor runs the plain tree", rc == 0, out.strip().splitlines()[-1] if out.strip() else "")
    if rc == 0:
        r0 = json.loads((tmp / "plain.json").read_text())
        case("plain residual is +18 km3 by hand", close(r0["residual"]["km3"], 18.0, 1e-3), str(r0["residual"]["km3"]))
        case("plain receipt carries no groundwater term and no partition",
             "groundwater" not in r0["terms"] and "partition" not in r0["residual"])
        rc2, lines = attest_quiet(tmp / "plain.json")
        case("plain receipt attests", rc2 == 0, lines[-1] if rc2 else "")

    # 2. With the groundwater term: six wells rising 1 ft, one confined and
    #    one short well excluded by rule; the term by hand is
    #    0.2 * 0.3048 m * 200,000 km2 * 1e-3 = 12.192 km3, but the end-window
    #    means sit 14.5 days inside each end, so the rise over the means is
    #    1 ft * (364 - 29) / 364 and the term 11.2208 km3.
    t1 = _synthetic_tree(tmp / "gw", with_groundwater=True)
    rc, out = run(t1, tmp / "gw.json")
    case("executor runs the groundwater tree", rc == 0, out.strip().splitlines()[-1] if out.strip() else "")
    if rc == 0:
        r1 = json.loads((tmp / "gw.json").read_text())
        g = r1["terms"]["groundwater"]
        expect = 0.2 * 0.3048 * (335 / 364) * 200000 * 1e-3
        case("groundwater term is the hand value", close(g["km3"], expect, 1e-3), f"{g['km3']} against {expect:.4f}")
        case("confined and short wells excluded by rule", g["wells_used"] == 6 and len(g["wells_excluded"]) == 2,
             f"{g['wells_used']} used, {len(g['wells_excluded'])} excluded")
        case("six wells 22 km apart are six sites", g["sites"] == 6, str(g["sites"]))
        case("spread over identical rises is zero", close(g["spread_sd_m"], 0.0, 1e-6))
        case("residual unchanged by the groundwater term", close(r1["residual"]["km3"], 18.0, 1e-3))
        pt = r1["residual"]["partition"]
        case("partition sums: dS = dS_gw + dS_other", close(pt["groundwater_km3"] + pt["other_storage_km3"], 12.0, 1e-4))
        case("terms less groundwater is dS_other plus the residual",
             close(pt["terms_less_groundwater_km3"], pt["other_storage_km3"] + r1["residual"]["km3"], 1e-4))
        case("fraction of dS reported when dS is six sigma from zero",
             pt["groundwater_fraction_of_storage_change"] is not None
             and close(pt["groundwater_fraction_of_storage_change"], expect / 12.0, 1e-3))
        case("bookkeeping statements present", len(r1["bookkeeping"]) == 4, str(len(r1["bookkeeping"])))
        rc2, lines = attest_quiet(tmp / "gw.json")
        case("groundwater receipt attests", rc2 == 0, lines[-1] if rc2 else "")
        case("attester prints bar three", rc2 == 0 and any(x.startswith("bar three") for x in lines))

        # 3. The doctorings bar two and bar three must catch.
        def doctored(mutate, label, expect_text):
            r = json.loads((tmp / "gw.json").read_text())
            mutate(r)
            p = tmp / f"doc_{label}.json"
            p.write_text(json.dumps(r))
            rc3, lines3 = attest_quiet(p)
            case(f"doctored {label} fails", rc3 == 1 and expect_text in lines3[0], lines3[0][:90])

        def d_gw(r):
            r["terms"]["groundwater"]["km3"] = 4.0
            r["residual"]["partition"]["groundwater_km3"] = 4.0
        doctored(d_gw, "groundwater volume", "groundwater: receipt")

        def d_sy(r):
            r["terms"]["groundwater"]["specific_yield"] = 0.9
        doctored(d_sy, "specific yield in the receipt (recompute reads the tree)", "is not the tree's")

        def d_src(r):
            r["terms"]["groundwater"]["specific_yield_source"] = ""
        doctored(d_src, "specific yield without a source", "bar three: the specific yield carries no source")

        def d_drop(r):
            del r["terms"]["groundwater"]
        doctored(d_drop, "groundwater term dropped from the receipt", "the tree carries groundwater.json")

        def d_part(r):
            r["residual"]["partition"]["other_storage_km3"] = 0.0
        doctored(d_part, "partition arithmetic", "partition: dS_other")

    # 4. A specific yield outside the bound, and a groundwater change larger
    #    than the whole, are refused by bar three even when the arithmetic
    #    reproduces.
    t2 = _synthetic_tree(tmp / "sy", with_groundwater=True, sy=0.8)
    rc, out = run(t2, tmp / "sy.json")
    if rc == 0:
        rc2, lines = attest_quiet(tmp / "sy.json")
        case("specific yield 0.8 fails bar three", rc2 == 1 and "outside (0, 0.5]" in lines[0], lines[0][:90])
    else:
        case("executor runs the out-of-bound tree", False, out[-200:])
    t3 = _synthetic_tree(tmp / "big", with_groundwater=True, sy=0.3, rise_ft=6.0)
    rc, out = run(t3, tmp / "big.json")
    if rc == 0:
        rc2, lines = attest_quiet(tmp / "big.json")
        case("groundwater change larger than the whole fails bar three",
             rc2 == 1 and "exceeds the total storage change" in lines[0], lines[0][:90])
    else:
        case("executor runs the part-larger-than-whole tree", False, out[-200:])

    # 5. Too few sites is a refusal of the term, and the partition is absent.
    t4 = _synthetic_tree(tmp / "few", with_groundwater=True, n_wells=2)
    rc, out = run(t4, tmp / "few.json")
    if rc == 0:
        r4 = json.loads((tmp / "few.json").read_text())
        case("two sites refuse the groundwater term", r4["terms"]["groundwater"]["refused"] is True
             and "partition" not in r4["residual"])
        rc2, lines = attest_quiet(tmp / "few.json")
        case("refused groundwater term attests", rc2 == 0 and any("groundwater term refused" in x for x in lines),
             lines[-1][:90] if lines else "")
    else:
        case("executor runs the few-sites tree", False, out[-200:])

    print(f"selftest: {failures} failure(s)")
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("receipt", type=Path, nargs="?")
    ap.add_argument("--computation", type=Path,
                    default=Path(__file__).resolve().parent.parent / "computations" / "basin_water_balance.py",
                    help="the sanctioned computation the receipt must have come from")
    ap.add_argument("-k", type=float, default=2.0, help="the consistency bar's multiple of the combined sigma")
    ap.add_argument("--selftest", action="store_true",
                    help="run the attester over synthetic receipts it can predict by hand, including the "
                         "groundwater term and the doctorings each bar must catch")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest(a.computation))
    if a.receipt is None:
        ap.error("a receipt is required unless --selftest is given")
    sys.exit(run_attest(a.receipt, a.computation, a.k))


if __name__ == "__main__":
    main()
