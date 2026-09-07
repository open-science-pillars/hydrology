# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy",
# ]
# ///
# Golden notebook for the basin-water-balance workflow (the
# golden-notebook requirement: one fixture-backed asserting script per
# workflow skill): the three frozen input trees under
# fixtures/water-balance/ go through the sanctioned executor and its
# attester and reproduce the recorded terms, residuals and refusal, the
# footprint floor derived from the mascon product's own geometry, the
# two bars, and the failures the contract requires: a doctored term, a
# receipt missing an input's stamp, an unsourced transfer, and a tree
# edited after freezing. Reference numbers measured at fixture creation
# and recorded in fixtures/README.md. Headless green via
# `uv run verification/basin_water_balance.py`; no network, no
# credential.

import marimo

__generated_with = "0.23.13"
app = marimo.App()


@app.cell
def _():
    import hashlib
    import json
    import shutil
    import subprocess
    import tempfile
    from pathlib import Path

    root = Path(__file__).parent.parent
    trees = root / "verification" / "fixtures" / "water-balance"
    executor = root / "knowledge" / "references" / "computations" / "basin_water_balance.py"
    attester = root / "knowledge" / "references" / "attesters" / "basin_water_balance_check.py"
    tmp = Path(tempfile.mkdtemp(prefix="water_balance_"))

    def compute(basin, extra=(), name="r", inputs=None):
        # The executor as the skill runs it, from the repository root so
        # the receipt's tree path stays repo relative.
        out = tmp / f"{name}.json"
        cmd = ["uv", "run", str(executor), "--inputs", str(inputs or (trees / basin)),
               "--receipt", str(out), *extra]
        p = subprocess.run(cmd, capture_output=True, text=True, cwd=root)
        receipt = json.loads(out.read_text()) if out.is_file() and p.returncode == 0 else None
        return p.returncode, p.stdout, p.stderr, receipt, out

    def attest(receipt_path, extra=()):
        p = subprocess.run(["uv", "run", str(attester), str(receipt_path), *extra],
                           capture_output=True, text=True, cwd=root)
        return p.returncode, p.stdout, p.stderr

    def sha(p):
        return hashlib.sha256(Path(p).read_bytes()).hexdigest()

    return attest, compute, json, root, sha, shutil, tmp, trees


@app.cell
def _(json, trees):
    # 1. The footprint floor is derived from the mascon product, not
    #    remembered: every frozen tree carries the same derivation, and
    #    it is the median area of a mostly-land mascon.
    _floors = {}
    for _b in ("ohio-olmsted", "lees-ferry", "roaring-fork"):
        _s = json.loads((trees / _b / "storage.json").read_text())
        _f = _s["footprint_scale"]
        _floors[_b] = _f["median_land_mascon_km2"]
        assert _f["mascons_total"] == 4551 and _f["mascons_mostly_land"] == 1301
        assert abs(_f["median_equivalent_square_side_km"] - 333.6) < 1.0
        assert _f["p05_km2"] < _f["median_land_mascon_km2"] < _f["p95_km2"]
    assert len(set(_floors.values())) == 1, _floors
    assert abs(list(_floors.values())[0] - 111266.0) < 1.0
    return


@app.cell
def _(attest, compute):
    # 2. The Ohio at Olmsted: a large wet basin that closes, and passes
    #    both bars. Every term is checked against the recorded value.
    _code, _out, _err, ohio, ohio_path = compute("ohio-olmsted", name="ohio")
    assert _code == 0, _err
    _t = ohio["terms"]
    assert abs(_t["precipitation"]["km3"] - 647.384) < 0.01
    assert abs(_t["evapotranspiration"]["km3"] - 355.162) < 0.01
    assert abs(_t["discharge"]["km3"] - 220.865) < 0.01
    assert abs(_t["storage"]["km3"] - 1.183) < 0.01
    assert _t["storage"]["mascons"] == 10 and _t["storage"]["refused"] is False
    assert _t["imports"]["assumption"] == "none known, assumed zero"
    assert _t["exports"]["assumption"] == "none known, assumed zero"
    assert _t["discharge"]["regulated"] is False
    assert abs(ohio["residual"]["km3"] - 70.174) < 0.01
    assert abs(ohio["residual"]["sigma_km3"] - 96.874) < 0.01
    assert abs(ohio["residual"]["residual_over_sigma"] - 0.72) < 0.01

    _rc, _o, _e = attest(ohio_path)
    assert _rc == 0, _o + _e
    assert "bar one, consistency: |residual| / sigma = 0.72 against k = 2.0 -> within the bar" in _o
    assert "bar two, reproducibility" in _o
    return (ohio_path,)


@app.cell
def _(attest, compute):
    # 3. The Colorado above Lees Ferry: the marginal case, at exactly one
    #    sigma, with the regulated flag set and the epochs mid-month.
    _code, _out, _err, lf, lf_path = compute("lees-ferry", extra=["--regulated"], name="lf")
    assert _code == 0, _err
    _t = lf["terms"]
    assert abs(_t["precipitation"]["km3"] - 88.585) < 0.01
    assert abs(_t["evapotranspiration"]["km3"] - 83.719) < 0.01
    assert abs(_t["discharge"]["km3"] - 10.769) < 0.01
    assert abs(_t["storage"]["km3"] - 13.214) < 0.01
    assert _t["storage"]["mascons"] == 7
    assert _t["storage"]["first_epoch"] == "2022-09-16" and _t["storage"]["last_epoch"] == "2023-09-16"
    assert _t["storage"]["first_offset_days"] == -15 and _t["storage"]["last_offset_days"] == -14
    assert _t["storage"]["endpoint_open"] is False
    assert _t["discharge"]["regulated"] is True and "operations" in _t["discharge"]["regulated_note"]
    assert abs(lf["residual"]["km3"] + 19.117) < 0.01
    assert abs(lf["residual"]["sigma_km3"] - 19.165) < 0.01
    assert abs(lf["residual"]["residual_over_sigma"] + 1.00) < 0.01
    # The partial check travels beside the storage term and is never folded in.
    _pc = lf["partial_checks"][0]
    assert _pc["parameter"] == "62614" and _pc["folded_into_ds"] is False
    assert _pc["change_ft"] > 0, "Lake Powell rose over water year 2023, as the storage term says"

    _rc, _o, _e = attest(lf_path)
    assert _rc == 0, _o + _e
    assert "= 1.00 against k = 2.0 -> within the bar" in _o
    assert "the outlet gauge is regulated" in _o
    return (lf_path,)


@app.cell
def _(attest, compute):
    # 4. The Roaring Fork: below the footprint floor, so the storage term
    #    is refused, no residual is reported, and the attester agrees
    #    that the refusal follows the floor rather than passing it by.
    _code, _out, _err, rf, rf_path = compute("roaring-fork", name="rf")
    assert _code == 0, _err
    _st = rf["terms"]["storage"]
    assert _st["refused"] is True and _st["mascons"] == 1
    assert abs(_st["basin_km2"] - 3767.1) < 0.1 and abs(_st["floor_km2"] - 111266.0) < 1.0
    assert "gain factor is not applied" in _st["reason"]
    assert rf["residual"]["reported"] is False
    assert "km3" not in rf["residual"]
    # The other three terms are still there: a refusal is not a blank page.
    assert abs(rf["terms"]["precipitation"]["km3"] - 1.369) < 0.01
    assert abs(rf["terms"]["evapotranspiration"]["km3"] - 1.819) < 0.01
    assert abs(rf["terms"]["discharge"]["km3"] - 1.128) < 0.01
    assert "REFUSED" in _out

    _rc, _o, _e = attest(rf_path)
    assert _rc == 0, _o + _e
    assert "PASS (refusal)" in _o
    assert "bar one, consistency: not applicable, there is no residual to test" in _o
    return


@app.cell
def _(attest, json, ohio_path, tmp):
    # 5. A doctored term fails bar two: the attester recomputes from the
    #    frozen files and does not take the receipt's word for anything.
    _r = json.loads(ohio_path.read_text())
    _r["terms"]["evapotranspiration"]["km3"] = 425.34          # enough to zero the residual
    _r["residual"]["km3"] = 0.0
    _doctored = tmp / "doctored.json"
    _doctored.write_text(json.dumps(_r, indent=1))
    _rc, _o, _e = attest(_doctored)
    assert _rc == 1 and "FAIL: evapotranspiration" in _o

    # 6. A receipt that omits an input's stamp fails before any
    #    arithmetic: iterating the receipt's own list would let it hide
    #    a file by leaving it out.
    _r2 = json.loads(ohio_path.read_text())
    del _r2["inputs"]["files"]["storage.json"]
    _nostamp = tmp / "nostamp.json"
    _nostamp.write_text(json.dumps(_r2, indent=1))
    _rc, _o, _e = attest(_nostamp)
    assert _rc == 1 and "carries no stamp for storage.json" in _o
    return


@app.cell
def _(compute):
    # 7. An import or export without a source is refused: an unsourced
    #    transfer is the term that quietly closes a budget.
    _code, _out, _err, _, _ = compute("lees-ferry", extra=["--exports", "1.2"], name="nosource")
    assert _code == 2 and "VALUE_KM3:SOURCE" in _err
    # With a source it is a term, and it moves the residual.
    _code, _out, _err, withx, _ = compute("lees-ferry", extra=["--regulated", "--exports",
                                                               "1.2:a stated source for the demonstration"],
                                          name="withx")
    assert _code == 0, _err
    assert withx["terms"]["exports"]["entries"][0]["source"]
    assert abs(withx["residual"]["km3"] + 20.317) < 0.01, withx["residual"]["km3"]
    return


@app.cell
def _(compute, json, root, shutil, tmp, trees):
    # 8. A tree edited after freezing is refused by the executor before
    #    it computes anything: the receipt's whole claim is that these
    #    inputs produced these numbers.
    _edited = tmp / "edited-tree"
    shutil.copytree(trees / "roaring-fork", _edited, dirs_exist_ok=True)
    _p = json.loads((_edited / "precipitation.json").read_text())
    _p["total"]["km3"] = 99.0
    (_edited / "precipitation.json").write_text(json.dumps(_p, indent=1))
    _code, _out, _err, _, _ = compute(None, inputs=_edited, name="edited")
    assert _code == 2 and "does not match the manifest" in _err
    assert "edited after it was frozen" in _err
    _ = root
    return


@app.cell
def _(sha, trees):
    # 9. The frozen trees are the bytes their manifests record, and every
    #    manifest names every file in its tree.
    import json as _json

    for _b in ("ohio-olmsted", "lees-ferry", "roaring-fork"):
        _man = _json.loads((trees / _b / "manifest.json").read_text())
        _on_disk = {p.name for p in (trees / _b).glob("*") if p.name != "manifest.json"}
        assert set(_man["files"]) == _on_disk, (_b, set(_man["files"]) ^ _on_disk)
        for _name, _rec in _man["files"].items():
            assert sha(trees / _b / _name) == _rec["sha256"], f"{_b}/{_name}"
    return


@app.cell
def _(attest, trees):
    # 10. The receipts stored beside the trees still attest, so a reader
    #     who never runs the executor can check the numbers this bundle
    #     publishes.
    for _r in sorted((trees / "receipts").glob("*.json")):
        _rc, _o, _e = attest(_r)
        assert _rc == 0, f"{_r.name}: {_o}{_e}"
        assert "PASS" in _o
    return


if __name__ == "__main__":
    app.run()
