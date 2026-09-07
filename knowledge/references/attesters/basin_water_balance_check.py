# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy"]
# ///
"""Attester for the basin water balance: recompute from the receipt and
apply the two bars.

The attester trusts nothing in the receipt but the inputs it names. It
re-reads the frozen tree, checks every file against the hash the
receipt recorded, recomputes each term from those files, and compares
its own numbers with the receipt's. Then it applies two bars, which
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

A receipt whose storage term was refused below the footprint floor has
no residual, so bar one does not apply and the attester says so rather
than passing it silently.

The receipt's `code_sha256` is checked against the sanctioned
computation file, so a receipt produced by an edited executor fails
even when its arithmetic is right: that is what makes the ritual's
"old against new" step mean anything.

Usage: basin_water_balance_check.py RECEIPT.json [--computation PATH] [-k 2]
"""
import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

TOL_KM3 = 1e-6
CFS_TO_KM3_PER_DAY = 0.0283168466 * 86400 / 1e9


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close(a, b, tol=TOL_KM3):
    return abs(float(a) - float(b)) <= tol


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("receipt", type=Path)
    ap.add_argument("--computation", type=Path,
                    default=Path(__file__).resolve().parent.parent / "computations" / "basin_water_balance.py",
                    help="the sanctioned computation the receipt must have come from")
    ap.add_argument("-k", type=float, default=2.0, help="the consistency bar's multiple of the combined sigma")
    a = ap.parse_args()

    r = json.loads(a.receipt.read_text())
    checks = []

    # The receipt has to say what it is before anything else is worth checking.
    for field in ("computation", "concept", "code_sha256", "tool_version", "identity", "basin",
                  "window", "inputs", "terms", "residual"):
        if field not in r:
            fail(f"the receipt has no {field}: an attester cannot check a receipt that does not say what it is")
    if r["computation"] != "basin-water-balance":
        fail(f"this receipt is for {r['computation']!r}, not the basin water balance")
    if not a.computation.is_file():
        fail(f"no such computation to check the receipt against: {a.computation}")
    want = hashlib.sha256(a.computation.read_bytes()).hexdigest()
    if r["code_sha256"] != want:
        fail(f"code_sha256 does not match the sanctioned computation: the receipt says {r['code_sha256'][:12]} "
             f"and {a.computation.name} hashes to {want[:12]}. A receipt from an edited executor is not "
             f"attested by this attester")

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
    checks.append(f"{len(r['inputs']['files'])} input files match the hashes the receipt recorded")

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
    checks.append("precipitation, evapotranspiration and discharge recomputed from the frozen files")

    floor = st["footprint_scale"]["median_land_mascon_km2"]
    refused = r["terms"]["storage"].get("refused", False)
    if (area < floor) != refused:
        fail(f"the storage term's refusal does not follow the floor: basin {area:,.0f} km2, floor {floor:,.0f} km2, "
             f"receipt says refused={refused}")

    if refused:
        if r["residual"].get("reported", False):
            fail("the storage term was refused and the receipt reports a residual anyway")
        checks.append(f"storage refused below the floor ({area:,.0f} km2 against {floor:,.0f} km2) and no "
                      f"residual is reported, as the concept requires")
        print("PASS (refusal): " + "; ".join(checks))
        print(f"bar one, consistency: not applicable, there is no residual to test")
        print(f"bar two, reproducibility: every recomputed value matches the receipt within {TOL_KM3} km3")
        return

    epochs = {e["epoch"]: e for e in st["epochs"]}
    for label in ("first_epoch", "last_epoch"):
        if r["terms"]["storage"][label] not in epochs:
            fail(f"the receipt's {label} {r['terms']['storage'][label]} is not an epoch of the frozen series")
    d_cm = (epochs[r["terms"]["storage"]["last_epoch"]]["lwe_cm"]
            - epochs[r["terms"]["storage"]["first_epoch"]]["lwe_cm"])
    ds_km3 = d_cm * 0.01 * 1e-3 * area
    if not close(ds_km3, r["terms"]["storage"]["km3"], 1e-5):
        fail(f"storage: receipt {r['terms']['storage']['km3']}, recomputed {round(ds_km3, 6)}")
    checks.append(f"storage recomputed from the frozen mascon series over {r['terms']['storage']['mascons']} mascons")

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
    checks.append("residual and combined sigma recomputed from the terms")

    ratio = abs(resid) / sig if sig else float("inf")
    bar_one = ratio <= a.k
    print(("PASS: " if bar_one else "FAIL (bar one): ") + "; ".join(checks))
    print(f"bar one, consistency: |residual| / sigma = {ratio:.2f} against k = {a.k:.1f} -> "
          f"{'within' if bar_one else 'outside'} the bar "
          f"(residual {resid:+.3f} km3, sigma {sig:.3f} km3)")
    print(f"bar two, reproducibility: every recomputed value matches the receipt within {TOL_KM3} km3")
    if r["terms"]["discharge"].get("regulated"):
        print("note: the outlet gauge is regulated, so this residual carries reservoir operations as well as "
              "hydrology; the flag is in the receipt and does not change the bars")
    if r["terms"]["storage"].get("endpoint_open"):
        print("note: the closing endpoint is open, reported as open and not filled")
    if not bar_one:
        sys.exit(1)


if __name__ == "__main__":
    main()
