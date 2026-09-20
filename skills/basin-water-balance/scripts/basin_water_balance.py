# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy>=1.26,<3"]
# ///
"""Sanctioned executor: the basin water balance P + I - ET - Q - X = dS
over a frozen input tree, with a receipt, and the groundwater part of
dS from a well set when the tree carries one.

Contract, as knowledge/computations/basin-water-balance.md sets it out:

  * the executor reads ONLY the frozen tree named by --inputs, and
    never the network; every file it reads is hashed into the receipt
    and checked against the tree's own manifest first, so a tree edited
    after freezing is refused rather than computed;
  * every term carries its value, its unit, its source, the source of
    its uncertainty and the stamp (file and sha256) it came from;
    imports and exports are receipt fields with a value and a source,
    or the explicit assumption that none is known;
  * the storage term is refused below the footprint floor, and the
    floor is derived here from the mascon product's own geometry
    rather than remembered from a sentence;
  * a regulated gauge is flagged, never refused: the flag says the
    discharge measures operations as well as hydrology;
  * the groundwater term is optional: when the tree holds
    groundwater.json, the change in water level over the well set,
    times the specific yield the tree states with its source, times
    the basin area, is the groundwater part of dS. It partitions the
    storage term; it is not a sixth term of the identity, and the
    residual and its bar do not move when it is present;
  * the residual is reported with the quadrature sum of the term
    uncertainties beside it, and the consistency bar is applied by the
    attester, not here. This executor states, it does not judge.

Usage:
  uv run skills/basin-water-balance/scripts/basin_water_balance.py \
      --inputs verification/fixtures/water-balance/lees-ferry \
      --receipt receipt.json
  (--imports and --exports take VALUE_KM3:SOURCE, repeatable)
"""
import argparse
import datetime as dt
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

TOOL_VERSION = "0.2.0"
CFS_TO_KM3_PER_DAY = 0.0283168466 * 86400 / 1e9      # cubic feet per second to km3 per day
FT_TO_M = 0.3048
EARTH_R_KM = 6371.0088

# The uncertainty each term carries, and where the number comes from.
# None of these is invented here: each is the figure its own concept or
# its own product documentation states, and the receipt names the
# source beside the value so a reader can disagree with the number
# rather than with the arithmetic.
TERM_UNCERTAINTY = {
    "precipitation": {"relative": 0.10,
                      "source": "IMERG V07 documented uncertainty over land at monthly to annual scales, "
                                "as knowledge/datasets/imerg-v07.md records it"},
    "evapotranspiration": {"relative": 0.20,
                           "source": "MOD16 validation against flux towers and watersheds, as "
                                     "knowledge/datasets/mod16a2gf.md records it"},
    "discharge": {"relative": 0.05,
                  "source": "USGS rating class good, plus or minus 5 per cent of the daily value, from the "
                            "station description; a poorer class widens this and the receipt says which"},
    "storage": {"absolute_cm": None,
                "source": "the mascon product's own per-mascon formal uncertainty grid, area weighted over "
                          "the basin and divided by the square root of the number of mascons the basin spans"},
    "groundwater": {"source": "quadrature of the specific yield's stated uncertainty times the mean level change "
                              "and the specific yield times the standard error of the site mean (the spread "
                              "over sites divided by the square root of the site count); the spread itself is "
                              "reported beside it, because the wells are the wells there are and not a designed "
                              "sample of the basin"},
}


def die(msg, code=2):
    print(f"REFUSED: {msg}", file=sys.stderr)
    sys.exit(code)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tree(root: Path):
    """Every file of the frozen tree, checked against its own manifest.

    A tree whose bytes have moved since it was frozen is refused: the
    receipt's whole claim is that these inputs produced these numbers."""
    man_path = root / "manifest.json"
    if not man_path.is_file():
        die(f"{root} has no manifest.json; the executor reads only a frozen tree")
    man = json.loads(man_path.read_text())
    files = {}
    for name, rec in man["files"].items():
        p = root / name
        if not p.is_file():
            die(f"{name} is named in the manifest and missing from the tree")
        got = sha256(p)
        if got != rec["sha256"]:
            die(f"{name} does not match the manifest: sha256 {got[:12]} against the frozen {rec['sha256'][:12]}. "
                f"The tree was edited after it was frozen; refreeze it or restore the file")
        files[name] = json.loads(p.read_text()) if name.endswith(".json") or name.endswith(".geojson") else None
    return man, files


def stamp(man, name):
    """The stamp a term came from: the file and the sha256 the manifest
    records for it, repeated on the term so a reader of the term alone
    can find its bytes."""
    return {"file": name, "sha256": man["files"][name]["sha256"]}


def parse_flux(text, label):
    """VALUE_KM3:SOURCE, the only form an import or an export may take.

    A number with no source is refused: an unsourced transfer is the
    term that quietly closes a budget."""
    if ":" not in text:
        die(f"--{label} takes VALUE_KM3:SOURCE (a value with no source is not a term): got {text!r}")
    v, src = text.split(":", 1)
    src = src.strip()
    if not src:
        die(f"--{label} carries no source; say where the number comes from")
    try:
        return {"km3": float(v), "source": src}
    except ValueError:
        die(f"--{label} value {v!r} is not a number")


def discharge_km3(series, start, end):
    """The discharge volume over the window, from the capture's own
    rows, with the qualified days counted rather than dropped."""
    rows = None
    for s in series:
        if s.get("parameter") == "00060" and s.get("statistic") == "00003":
            rows = s["rows"]
            break
    if rows is None:
        die("the discharge capture holds no daily mean discharge (parameter 00060, statistic 00003)")
    total = 0.0
    days = qualified = provisional = 0
    for r in rows:
        d = dt.date.fromisoformat(r["t"])
        if not (start <= d <= end):
            continue
        if r["v"] in (None, "", "--"):
            continue
        total += float(r["v"]) * CFS_TO_KM3_PER_DAY
        days += 1
        if r.get("qualifiers"):
            qualified += 1
        if r.get("approval") != "Approved":
            provisional += 1
    return total, days, qualified, provisional


def storage_term(storage, start, end, area_km2, floor_km2):
    """dS between the epochs nearest the window's ends, or a refusal.

    The mascon epochs are mid-month and the window's ends are not, so
    the epochs used are the nearest to each end and the receipt states
    the offset in days. Below the footprint floor there is no storage
    term at all: a basin smaller than one mascon has no independent
    mascon signal, and the product's gain factors exist for regions
    smaller than a mascon, which is exactly the case being refused."""
    n_mascons = storage["mascons"]
    if area_km2 < floor_km2:
        return {"refused": True,
                "reason": (f"the basin is {area_km2:,.0f} km2, below the footprint floor of {floor_km2:,.0f} km2 "
                           f"(one mostly-land mascon, derived from the product's own geometry): it spans "
                           f"{n_mascons} mascon(s), so the mascon field carries no signal that is this basin's "
                           f"rather than its neighbourhood's. No storage term exists, the residual is not "
                           f"reported, and a gain factor is not applied to rescue it"),
                "basin_km2": round(area_km2, 1), "floor_km2": round(floor_km2, 1),
                "mascons": n_mascons, "mascon_ids": storage["mascon_ids"]}
    epochs = [(dt.date.fromisoformat(e["epoch"]), e) for e in storage["epochs"]]
    if not epochs:
        die("the frozen storage series holds no epoch near the window")
    first = min(epochs, key=lambda x: (abs((x[0] - start).days), x[0]))
    last = min(epochs, key=lambda x: (abs((x[0] - end).days), x[0]))
    if first[0] == last[0]:
        die("the window's two ends resolve to the same mascon epoch; a storage change needs two")
    record_end = dt.date.fromisoformat(storage["record_last_epoch"])
    open_end = end > record_end
    d_cm = last[1]["lwe_cm"] - first[1]["lwe_cm"]
    sigma_cm = float(np.hypot(first[1]["uncertainty_cm"], last[1]["uncertainty_cm"]) / np.sqrt(n_mascons))
    return {"refused": False,
            "first_epoch": first[0].isoformat(), "last_epoch": last[0].isoformat(),
            "first_offset_days": (first[0] - start).days, "last_offset_days": (last[0] - end).days,
            "lwe_first_cm": first[1]["lwe_cm"], "lwe_last_cm": last[1]["lwe_cm"],
            "d_lwe_cm": round(d_cm, 4),
            "km3": round(d_cm * 0.01 * 1e-3 * area_km2, 6),
            "sigma_cm": round(sigma_cm, 4),
            "sigma_km3": round(sigma_cm * 0.01 * 1e-3 * area_km2, 6),
            "mascons": n_mascons, "mascon_ids": storage["mascon_ids"],
            "basin_km2": round(area_km2, 1), "floor_km2": round(floor_km2, 1),
            "record_last_epoch": storage["record_last_epoch"],
            "endpoint_open": open_end,
            "endpoint_note": ("the window ends after the mascon record's last epoch, so the closing endpoint is "
                              "OPEN: it is reported as open and never filled by extrapolation"
                              if open_end else
                              "both endpoints fall inside the mascon record; the epochs are mid-month and the "
                              "offsets from the window's ends are stated in days")}


def haversine_km(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    c = math.sin(p1) * math.sin(p2) + math.cos(p1) * math.cos(p2) * math.cos(dl)
    return EARTH_R_KM * math.acos(max(-1.0, min(1.0, c)))


def groundwater_term(gw, start, end, area_km2):
    """The groundwater part of dS by the water-table fluctuation method,
    from the well set the tree froze and the parameters it states.

    For every unconfined well: the mean depth to water over the first
    end_window_days of the window and over the last, and their
    difference with the sign turned so that a shallower water table is
    a rise. Wells within cluster_radius_km of one another are one
    site, because a well field samples one water table and would
    otherwise be counted once per well. The term is the specific yield
    times the mean rise over sites times the basin area; its sigma is
    the quadrature of the specific yield's stated sigma and the
    standard error of the site mean, and the spread over sites is
    reported beside it. Fewer than min_sites sites is a refusal of the
    term, not a smaller term."""
    unit = str(gw.get("unit", ""))
    if gw.get("parameter") != "72019" or "below land surface" not in unit:
        die(f"the groundwater well set is parameter {gw.get('parameter')!r} in {unit!r}; the term is computed only "
            f"from parameter 72019, depth to water below land surface in feet, because the sign convention (a "
            f"shallower depth is a rise) is that parameter's, and an elevation parameter (62610, 62611, 72150, "
            f"72229) would compute the term with the sign reversed")
    prm = gw["parameters"]
    sy = float(prm["specific_yield"]["value"])
    sy_sigma = float(prm["specific_yield"]["sigma"])
    n_end = int(prm["end_window_days"])
    min_days = int(prm["min_days_per_end"])
    radius = float(prm["cluster_radius_km"])
    min_sites = int(prm["min_sites"])
    first_hi = start + dt.timedelta(days=n_end - 1)
    last_lo = end - dt.timedelta(days=n_end - 1)
    if first_hi >= last_lo:
        die(f"the groundwater end windows of {n_end} days overlap inside a window of {(end - start).days + 1} days")

    used, excluded = [], []
    for w in sorted(gw["wells"], key=lambda x: x["site"]):
        if w.get("aquifer_type_code") != "U":
            excluded.append({"site": w["site"], "reason": f"aquifer type {w.get('aquifer_type_code')!r} is not "
                                                          f"unconfined; a confined head change is not a storage "
                                                          f"change at specific yield"})
            continue
        first, last = [], []
        days = approved = qualified = 0
        for r in w["rows"]:
            if r["v"] in (None, "", "--"):
                continue
            d = dt.date.fromisoformat(r["t"])
            if not (start <= d <= end):
                continue
            days += 1
            approved += r.get("approval") == "Approved"
            qualified += bool(r.get("qualifiers"))
            if d <= first_hi:
                first.append(float(r["v"]))
            elif d >= last_lo:
                last.append(float(r["v"]))
        if len(first) < min_days or len(last) < min_days:
            excluded.append({"site": w["site"], "reason": f"{len(first)} and {len(last)} daily values in the two "
                                                          f"end windows against the {min_days} the rule requires"})
            continue
        rise_ft = float(np.mean(first)) - float(np.mean(last))
        used.append({"site": w["site"], "name": w.get("name"), "lat": w["lat"], "lon": w["lon"],
                     "state": w.get("state"), "aquifer_code": w.get("aquifer_code"),
                     "national_aquifer_code": w.get("national_aquifer_code"),
                     "aquifer_type_code": w.get("aquifer_type_code"),
                     "well_constructed_depth_ft": w.get("well_constructed_depth_ft"),
                     "altitude_ft": w.get("altitude_ft"), "altitude_datum": w.get("altitude_datum"),
                     "capture_id": w.get("capture_id"),
                     "days": days, "days_approved": approved, "days_qualified": qualified,
                     "first_days": len(first), "last_days": len(last),
                     "first_mean_ft": round(float(np.mean(first)), 4), "last_mean_ft": round(float(np.mean(last)), 4),
                     "rise_ft": round(rise_ft, 4), "rise_m": round(rise_ft * FT_TO_M, 4),
                     "_rise_m": rise_ft * FT_TO_M})

    # Sites are the connected components of the graph whose edges join
    # wells within the radius of one another, so the result does not
    # depend on the order the wells are visited in; the components are
    # listed by their first member in site order.
    parent = list(range(len(used)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i in range(len(used)):
        for j in range(i + 1, len(used)):
            if haversine_km(used[i]["lat"], used[i]["lon"], used[j]["lat"], used[j]["lon"]) <= radius:
                parent[find(i)] = find(j)
    groups = {}
    for i, w in enumerate(used):
        groups.setdefault(find(i), []).append(w)
    clusters = sorted(groups.values(), key=lambda c: c[0]["site"])
    site_rises = [float(np.mean([m["_rise_m"] for m in c])) for c in clusters]
    sites = [{"members": [m["site"] for m in c],
              "lat": round(float(np.mean([m["lat"] for m in c])), 5),
              "lon": round(float(np.mean([m["lon"] for m in c])), 5),
              "rise_m": round(rise, 4)} for c, rise in zip(clusters, site_rises)]
    for w in used:
        del w["_rise_m"]
    base = {"method": "water-table fluctuation: specific yield times the mean water-level change over the site "
                      "set times the basin area; a partition of dS, not a term of the identity",
            "clustering": "sites are the connected components of wells within cluster_radius_km of one another",
            "parameter": gw.get("parameter"), "statistic": gw.get("statistic"), "unit_of_levels": gw.get("unit"),
            "specific_yield": sy, "specific_yield_sigma": sy_sigma,
            "specific_yield_source": prm["specific_yield"]["source"],
            "specific_yield_applies_to": prm["specific_yield"].get("applies_to", ""),
            "end_window_days": n_end, "min_days_per_end": min_days, "cluster_radius_km": radius,
            "min_sites": min_sites,
            "first_window": {"start": start.isoformat(), "end": first_hi.isoformat()},
            "last_window": {"start": last_lo.isoformat(), "end": end.isoformat()},
            "wells_in_tree": len(gw["wells"]), "wells_used": len(used), "wells_excluded": excluded,
            "sites": len(sites), "site_list": sites, "wells": used,
            "screened_interval_note": gw.get("screened_interval_note", ""),
            "captures": [{"capture_id": c["capture_id"], "content_sha256": c.get("content_sha256"),
                          "sites": len(c.get("sites", []))} for c in gw.get("captures", [])],
            "selection": {k: v for k, v in gw.get("selection", {}).items() if k != "site_file_requests"}}
    if len(sites) < min_sites:
        return {**base, "refused": True,
                "reason": f"{len(sites)} site(s) after clustering against the {min_sites} the parameters require; "
                          f"a groundwater term on fewer sites is not computed"}
    rises = np.array(site_rises, float)
    mean_m = float(rises.mean())
    sd_m = float(rises.std(ddof=1)) if len(rises) > 1 else 0.0
    se_m = sd_m / math.sqrt(len(rises))
    km3 = sy * mean_m * area_km2 * 1e-3                       # m over km2 is 1e-3 km3
    sigma_km3 = area_km2 * 1e-3 * math.hypot(sy_sigma * mean_m, sy * se_m)
    # The term without its largest site (by the size of the level
    # change), because one well field can carry the whole mean.
    largest = max(range(len(sites)), key=lambda i: abs(site_rises[i]))
    rest = [x for i, x in enumerate(site_rises) if i != largest]
    mean_rest = float(np.mean(rest)) if rest else 0.0
    return {**base, "refused": False,
            "mean_rise_m": round(mean_m, 4), "median_rise_m": round(float(np.median(rises)), 4),
            "spread_sd_m": round(sd_m, 4), "standard_error_m": round(se_m, 4),
            "min_rise_m": round(float(rises.min()), 4), "max_rise_m": round(float(rises.max()), 4),
            "km3": round(km3, 6), "mm": round(sy * mean_m * 1000, 4),
            "sigma_km3": round(sigma_km3, 6),
            "sigma_components_km3": {"specific_yield": round(area_km2 * 1e-3 * sy_sigma * abs(mean_m), 6),
                                     "standard_error": round(area_km2 * 1e-3 * sy * se_m, 6)},
            "sigma_km3_at_spread": round(area_km2 * 1e-3 * math.hypot(sy_sigma * mean_m, sy * sd_m), 6),
            "sigma_note": "sigma_km3 uses the standard error of the site mean, which is the sigma of the mean "
                          "only if the sites are a random sample of the basin's water table; sigma_km3_at_spread "
                          "uses the spread over sites instead and is the figure for a reader who does not grant "
                          "that assumption",
            "without_largest_site": {"site": sites[largest]["members"], "rise_m": round(site_rises[largest], 4),
                                     "sites": len(rest), "mean_rise_m": round(mean_rest, 4),
                                     "km3": round(sy * mean_rest * area_km2 * 1e-3, 6)},
            "km3_at_specific_yield_low": round((sy - sy_sigma) * mean_m * area_km2 * 1e-3, 6),
            "km3_at_specific_yield_high": round((sy + sy_sigma) * mean_m * area_km2 * 1e-3, 6),
            "uncertainty_source": TERM_UNCERTAINTY["groundwater"]["source"]}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--inputs", required=True, type=Path, help="the frozen input tree for one basin")
    ap.add_argument("--imports", action="append", default=[], help="VALUE_KM3:SOURCE, repeatable")
    ap.add_argument("--exports", action="append", default=[], help="VALUE_KM3:SOURCE, repeatable")
    ap.add_argument("--regulated", action="store_true",
                    help="the outlet gauge is regulated: the flag goes in the receipt and the discharge term "
                         "is reported as operations as well as hydrology")
    ap.add_argument("--rating-uncertainty", type=float, default=None,
                    help="relative uncertainty of the discharge from the station's rating class, if it is not good")
    ap.add_argument("--receipt", type=Path, help="write the receipt here")
    a = ap.parse_args()

    man, files = read_tree(a.inputs)
    start = dt.date.fromisoformat(man["window"]["start"])
    end = dt.date.fromisoformat(man["window"]["end"])
    basin = files["basin.geojson"]
    prov = basin.get("provenance", {})
    area_km2 = float(prov["area_km2"])
    p = files["precipitation.json"]
    et = files["evapotranspiration.json"]
    q = files["discharge.json"]
    storage = files["storage.json"]

    if p["window"]["start"] != man["window"]["start"] or p["window"]["end"] != man["window"]["end"]:
        die(f"the precipitation receipt covers {p['window']['start']} to {p['window']['end']}, not the tree's "
            f"window {man['window']['start']} to {man['window']['end']}")

    floor_km2 = storage["footprint_scale"]["median_land_mascon_km2"]

    p_km3 = float(p["total"]["km3"])
    et_km3 = float(et["total"]["km3"])
    q_km3, q_days, q_qualified, q_provisional = discharge_km3(q["series"], start, end)
    expected_days = (end - start).days + 1
    if q_days != expected_days:
        die(f"the discharge capture covers {q_days} of the window's {expected_days} days; a water balance "
            f"needs the whole window or an explicit statement of what is missing")

    imports = [parse_flux(x, "imports") for x in a.imports]
    exports = [parse_flux(x, "exports") for x in a.exports]
    i_km3 = sum(x["km3"] for x in imports)
    x_km3 = sum(x["km3"] for x in exports)

    st = storage_term(storage, start, end, area_km2, floor_km2)
    st["stamp"] = stamp(man, "storage.json")

    gw = None
    if "groundwater.json" in files:
        g = files["groundwater.json"]
        if g["window"]["start"] != man["window"]["start"] or g["window"]["end"] != man["window"]["end"]:
            die(f"the groundwater well set covers {g['window']['start']} to {g['window']['end']}, not the tree's "
                f"window")
        gw = groundwater_term(g, start, end, area_km2)
        gw["stamp"] = stamp(man, "groundwater.json")

    sig_p = p_km3 * TERM_UNCERTAINTY["precipitation"]["relative"]
    sig_et = et_km3 * TERM_UNCERTAINTY["evapotranspiration"]["relative"]
    rel_q = a.rating_uncertainty if a.rating_uncertainty is not None else TERM_UNCERTAINTY["discharge"]["relative"]
    sig_q = q_km3 * rel_q

    receipt = {
        "computation": "basin-water-balance",
        "concept": "knowledge/computations/basin-water-balance.md",
        "tool_version": TOOL_VERSION,
        "code_sha256": sha256(Path(__file__)),
        "run_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "identity": "P + I - ET - Q - X = dS",
        "basin": {"name": man["basin"], "area_km2": area_km2, "site": prov.get("site", ""),
                  "geometry_sha256": prov.get("geometry_sha256", "")},
        "window": {"start": man["window"]["start"], "end": man["window"]["end"], "days": expected_days},
        "inputs": {"tree": str(a.inputs), "frozen_at": man["frozen_at"], "files": man["files"]},
        "terms": {
            "precipitation": {
                "km3": round(p_km3, 6), "mm": p["total"]["mm"], "sigma_km3": round(sig_p, 6),
                "source": f"{p['window_files'][0]['short_name']} run {p['window_files'][0]['run']}, "
                          f"DOI {p['window_files'][0]['doi']}",
                "run_by_month": p.get("runs_by_month", {}),
                "seams": p.get("seams", []),
                "uncertainty_source": TERM_UNCERTAINTY["precipitation"]["source"],
                "coverage": p["coverage"],
                "stamp": stamp(man, "precipitation.json"),
            },
            "evapotranspiration": {
                "km3": round(et_km3, 6), "mm": et["total"]["mm"], "sigma_km3": round(sig_et, 6),
                "source": f"{et['window_files'][0]['short_name']} {et['window_files'][0]['version']}, "
                          f"DOI {et['window_files'][0]['doi']}, tiles "
                          f"{', '.join(sorted({w['tile'] for w in et['window_files']}))}",
                "uncertainty_source": TERM_UNCERTAINTY["evapotranspiration"]["source"],
                "masked_fraction": et["coverage"]["masked_fraction_any_composite"],
                "covered_fraction": et["coverage"]["covered_area_over_polygon_area"],
                "open_water": et["open_water"],
                "stamp": stamp(man, "evapotranspiration.json"),
            },
            "discharge": {
                "km3": round(q_km3, 6), "sigma_km3": round(sig_q, 6),
                "source": f"USGS capture {q['capture_id']} ({q['params'].get('sites')}), content sha256 "
                          f"{q['content_sha256'][:12]}",
                "days": q_days, "days_qualified": q_qualified, "days_provisional": q_provisional,
                "uncertainty_source": TERM_UNCERTAINTY["discharge"]["source"],
                "relative_uncertainty": rel_q,
                "regulated": bool(a.regulated),
                "regulated_note": ("the outlet gauge is regulated: this discharge measures reservoir operations "
                                   "as well as hydrology, and the residual carries that. The term is flagged, "
                                   "never refused" if a.regulated else "not declared regulated"),
                "stamp": stamp(man, "discharge.json"),
            },
            "imports": {"km3": round(i_km3, 6), "entries": imports} if imports else
                       {"km3": 0.0, "entries": [], "assumption": "none known, assumed zero"},
            "exports": {"km3": round(x_km3, 6), "entries": exports} if exports else
                       {"km3": 0.0, "entries": [], "assumption": "none known, assumed zero"},
            "storage": st,
        },
        "partial_checks": [],
    }
    if gw is not None:
        receipt["terms"]["groundwater"] = gw

    if "partial_check.json" in files:
        pc = files["partial_check.json"]
        rows = [r for s in pc["series"] for r in s["rows"]
                if start <= dt.date.fromisoformat(r["t"]) <= end and r["v"] not in (None, "", "--")]
        if rows:
            receipt["partial_checks"].append({
                "name": "reservoir pool elevation",
                "capture_id": pc["capture_id"],
                "parameter": pc["params"].get("parameter_cd"),
                "first": {"date": rows[0]["t"], "value_ft": float(rows[0]["v"])},
                "last": {"date": rows[-1]["t"], "value_ft": float(rows[-1]["v"])},
                "change_ft": round(float(rows[-1]["v"]) - float(rows[0]["v"]), 2),
                "note": pc.get("note", ""),
                "folded_into_ds": False,
                "stamp": stamp(man, "partial_check.json"),
            })

    bookkeeping = []
    if st["refused"]:
        receipt["residual"] = {"reported": False, "reason": st["reason"]}
        bookkeeping.append("the storage term is refused below the footprint floor, so no residual is reported "
                           "and P + I - ET - Q - X is a difference of terms, not a residual")
        if gw is not None:
            bookkeeping.append("a groundwater term is present and is NOT a storage term: it is the groundwater "
                               "part of a dS that this basin does not have, and it does not stand in for the "
                               "refused term")
    else:
        resid = p_km3 + i_km3 - et_km3 - q_km3 - x_km3 - st["km3"]
        sig = float(np.sqrt(sig_p ** 2 + sig_et ** 2 + sig_q ** 2 + st["sigma_km3"] ** 2))
        receipt["residual"] = {
            "reported": True,
            "km3": round(resid, 6),
            "mm": round(resid * 1e6 / area_km2, 4),
            "sigma_km3": round(sig, 6),
            "residual_over_sigma": round(resid / sig, 4) if sig else None,
            "residual_over_precipitation": round(resid / p_km3, 4) if p_km3 else None,
            "definition": "P + I - ET - Q - X - dS, so a positive residual means the terms deliver more water "
                          "than the storage change accounts for",
            "sigma_definition": "quadrature sum of the four term uncertainties, each from the source named "
                                "beside its term",
        }
        bookkeeping.append(f"P + I - ET - Q - X - dS = residual: {p_km3:.3f} + {i_km3:.3f} - {et_km3:.3f} - "
                           f"{q_km3:.3f} - {x_km3:.3f} - {st['km3']:.3f} = {resid:+.3f} km3, against a combined "
                           f"sigma of {sig:.3f} km3")
        if gw is not None and not gw["refused"]:
            other = st["km3"] - gw["km3"]
            other_sigma = float(np.hypot(st["sigma_km3"], gw["sigma_km3"]))
            left = p_km3 + i_km3 - et_km3 - q_km3 - x_km3 - gw["km3"]
            receipt["residual"]["partition"] = {
                "groundwater_km3": gw["km3"], "groundwater_sigma_km3": gw["sigma_km3"],
                "other_storage_km3": round(other, 6), "other_storage_sigma_km3": round(other_sigma, 6),
                "groundwater_fraction_of_storage_change": (round(gw["km3"] / st["km3"], 4)
                                                           if abs(st["km3"]) > 2 * st["sigma_km3"] else None),
                "fraction_note": ("the fraction is reported only when dS is more than two sigma from zero; a "
                                  "fraction of a storage change indistinguishable from zero is not a number"),
                "terms_less_groundwater_km3": round(left, 6),
                "definition": "dS = dS_gw + dS_other, where dS_gw is the well set's water-table change at the "
                              "stated specific yield over the basin area and dS_other is everything else the "
                              "mascons see: soil moisture, snow, surface water and groundwater the wells do "
                              "not sample. P + I - ET - Q - X - dS_gw equals dS_other plus the residual. The "
                              "residual itself and its bar do not move: the groundwater term partitions dS, "
                              "it is not a sixth term",
            }
            bookkeeping.append(f"dS = dS_gw + dS_other: {st['km3']:.3f} = {gw['km3']:+.3f} + {other:+.3f} km3 "
                               f"(dS_gw at specific yield {gw['specific_yield']} over {gw['sites']} sites, "
                               f"mean rise {gw['mean_rise_m']:+.3f} m with a spread of {gw['spread_sd_m']:.3f} m)")
            bookkeeping.append(f"P + I - ET - Q - X - dS_gw = dS_other + residual: {left:+.3f} = {other:+.3f} + "
                               f"{resid:+.3f} km3")
            bookkeeping.append("the residual and its consistency bar are unchanged by the groundwater term, "
                               "which partitions the storage change and is not added to the identity")
        elif gw is not None:
            bookkeeping.append(f"the groundwater term is refused ({gw['reason']}); dS is not partitioned")
    receipt["bookkeeping"] = bookkeeping

    print(f"{man['basin']}  {man['window']['start']} to {man['window']['end']}  ({area_km2:,.0f} km2)")
    print(f"  P  {p_km3:10.3f} km3 +- {sig_p:7.3f}")
    print(f"  I  {i_km3:10.3f} km3" + ("" if imports else "   (none known, assumed zero)"))
    print(f"  ET {et_km3:10.3f} km3 +- {sig_et:7.3f}")
    print(f"  Q  {q_km3:10.3f} km3 +- {sig_q:7.3f}" + ("   REGULATED" if a.regulated else ""))
    print(f"  X  {x_km3:10.3f} km3" + ("" if exports else "   (none known, assumed zero)"))
    if st["refused"]:
        print(f"  dS      REFUSED: {st['reason']}")
        print("  residual not reported")
    else:
        print(f"  dS {st['km3']:10.3f} km3 +- {st['sigma_km3']:7.3f}   "
              f"({st['d_lwe_cm']:+.3f} cm, {st['mascons']} mascons, epochs {st['first_epoch']} to {st['last_epoch']})")
        r = receipt["residual"]
        print(f"  residual {r['km3']:+.3f} km3 +- {r['sigma_km3']:.3f}  "
              f"({r['residual_over_sigma']:+.2f} sigma, {r['residual_over_precipitation']:+.1%} of P)")
    if gw is not None:
        if gw["refused"]:
            print(f"  dS_gw   REFUSED: {gw['reason']}")
        else:
            print(f"  dS_gw {gw['km3']:8.3f} km3 +- {gw['sigma_km3']:7.3f}   "
                  f"(specific yield {gw['specific_yield']} +- {gw['specific_yield_sigma']}, {gw['sites']} sites from "
                  f"{gw['wells_used']} wells, mean rise {gw['mean_rise_m']:+.3f} m, spread {gw['spread_sd_m']:.3f} m)")
            if not st["refused"]:
                pt = receipt["residual"]["partition"]
                frac = pt["groundwater_fraction_of_storage_change"]
                print(f"  dS_other {pt['other_storage_km3']:+.3f} km3 +- {pt['other_storage_sigma_km3']:.3f}   "
                      f"(dS less dS_gw; " + (f"groundwater is {frac:.2f} of dS)" if frac is not None else
                                             "dS is within two sigma of zero, so no fraction of it is reported)"))
    if a.receipt:
        a.receipt.write_text(json.dumps(receipt, indent=1))
        print(f"  receipt {a.receipt}")


if __name__ == "__main__":
    main()
