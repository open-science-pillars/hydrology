# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy",
# ]
# ///
# Golden notebook for the basin-water-balance workflow (the
# golden-notebook requirement: one fixture-backed asserting script per
# workflow skill): the four frozen input trees under
# fixtures/water-balance/ go through the sanctioned executor and its
# attester and reproduce the recorded terms, residuals and refusal, the
# footprint floor derived from the mascon product's own geometry, the
# groundwater term and the partition of the storage change it gives on
# the tree that carries a well set, the three bars, and the failures
# the contract requires: a doctored term, a doctored groundwater
# volume, a receipt missing an input's stamp, an unsourced transfer,
# and a tree edited after freezing; and the attester's own selftest.
# Reference numbers measured at fixture creation and recorded in
# fixtures/README.md. Headless green via
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
    scripts = root / "skills" / "basin-water-balance" / "scripts"
    executor = scripts / "basin_water_balance.py"
    attester = scripts / "basin_water_balance_check.py"
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
    for _b in ("ohio-olmsted", "lees-ferry", "roaring-fork", "ohio-olmsted-groundwater"):
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
    assert "bar three" not in _o, "no groundwater term, so no bar three"
    return ohio, ohio_path


@app.cell
def _(attest, compute, json, ohio, tmp):
    # 2b. The Ohio at Olmsted with the groundwater term: the same four
    #     terms byte for byte (the tree copies them), the water-table
    #     fluctuation term from the frozen well set, the partition of dS
    #     it gives, the bookkeeping statements, and bar three. The
    #     residual does not move: the term partitions dS, it is not a
    #     sixth term.
    _code, _out, _err, gw, gw_path = compute("ohio-olmsted-groundwater", name="ohiogw")
    assert _code == 0, _err
    for _t in ("precipitation", "evapotranspiration", "discharge", "storage"):
        assert gw["terms"][_t]["km3"] == ohio["terms"][_t]["km3"], _t
        assert gw["terms"][_t]["stamp"]["sha256"] == ohio["terms"][_t]["stamp"]["sha256"], _t
    assert gw["residual"]["km3"] == ohio["residual"]["km3"]
    assert gw["residual"]["sigma_km3"] == ohio["residual"]["sigma_km3"]
    _g = gw["terms"]["groundwater"]
    assert _g["refused"] is False
    assert _g["specific_yield"] == 0.21 and _g["specific_yield_sigma"] == 0.03
    assert "10.1029/2007WR006096" in _g["specific_yield_source"] and "10.3133/wsp1662D" in _g["specific_yield_source"]
    assert _g["parameter"] == "72019" and _g["statistic"] == "00003"
    assert _g["end_window_days"] == 30 and _g["min_days_per_end"] == 20 and _g["cluster_radius_km"] == 2.0
    assert _g["first_window"] == {"start": "2022-10-01", "end": "2022-10-30"}
    assert _g["last_window"] == {"start": "2023-09-01", "end": "2023-09-30"}
    assert _g["wells_in_tree"] == 58 and _g["wells_used"] == 50 and len(_g["wells_excluded"]) == 8
    assert all("end windows" in x["reason"] for x in _g["wells_excluded"])
    assert _g["sites"] == 39
    _biggest = max(_g["site_list"], key=lambda s: len(s["members"]))
    assert len(_biggest["members"]) == 12 and abs(_biggest["lat"] - 38.342) < 0.01, "the Louisville well field is one site"
    assert all(w["aquifer_type_code"] == "U" and w["well_constructed_depth_ft"] for w in _g["wells"])
    assert abs(_g["mean_rise_m"] - 0.0886) < 0.001 and abs(_g["median_rise_m"] + 0.0631) < 0.001
    assert abs(_g["spread_sd_m"] - 0.8463) < 0.001 and abs(_g["standard_error_m"] - 0.1355) < 0.001
    assert abs(_g["km3"] - 9.752) < 0.01 and abs(_g["sigma_km3"] - 14.982) < 0.01
    assert abs(_g["km3_at_specific_yield_low"] - 8.359) < 0.01 and abs(_g["km3_at_specific_yield_high"] - 11.145) < 0.01
    assert _g["stamp"]["file"] == "groundwater.json"
    assert "constructed depth" in _g["screened_interval_note"]
    _pt = gw["residual"]["partition"]
    assert abs(_pt["other_storage_km3"] + 8.569) < 0.01 and abs(_pt["other_storage_sigma_km3"] - 15.827) < 0.01
    assert abs(_pt["terms_less_groundwater_km3"] - 61.605) < 0.01
    assert abs(_pt["groundwater_km3"] + _pt["other_storage_km3"] - gw["terms"]["storage"]["km3"]) < 1e-5
    assert abs(_pt["terms_less_groundwater_km3"] - _pt["other_storage_km3"] - gw["residual"]["km3"]) < 1e-5
    assert _pt["groundwater_fraction_of_storage_change"] is None, "dS is within two sigma of zero"
    assert len(gw["bookkeeping"]) == 4 and ("not a sixth term" in gw["bookkeeping"][-1]
                                           or "not added to the identity" in gw["bookkeeping"][-1])
    # The sigma is almost entirely the standard-error component; at the
    # spread it would be 93 km3, and without the Louisville site the term
    # is a third of a cubic kilometre.
    assert abs(_g["sigma_components_km3"]["standard_error"] - 14.914) < 0.01
    assert abs(_g["sigma_components_km3"]["specific_yield"] - 1.393) < 0.01
    assert abs(_g["sigma_km3_at_spread"] - 93.161) < 0.01
    _wl = _g["without_largest_site"]
    assert _wl["sites"] == 38 and len(_wl["site"]) == 12 and abs(_wl["rise_m"] - 3.3384) < 0.001
    assert abs(_wl["mean_rise_m"] - 0.0031) < 0.001 and abs(_wl["km3"] - 0.339) < 0.01
    assert _g["parameter"] == "72019" and "connected components" in _g["clustering"]
    assert "dS_gw" in _out and "dS_other" in _out

    _rc, _o, _e = attest(gw_path)
    assert _rc == 0, _o + _e
    assert "PASS: groundwater term recomputed from the frozen well set: 50 wells, 39 sites" in _o
    assert "bar three, plausibility: parameter 72019 (depth to water below land surface), specific yield 0.21 in (0, 0.5], 39 sites at or above 3" in _o
    assert "= 0.72 against k = 2.0 -> within the bar" in _o

    # A doctored groundwater volume fails bar two on the recompute from
    # the frozen well set, and a receipt that drops the term while the
    # tree carries the well set fails before any arithmetic.
    _r = json.loads(gw_path.read_text())
    _r["terms"]["groundwater"]["km3"] = 1.183
    _r["residual"]["partition"]["groundwater_km3"] = 1.183
    _d = tmp / "doctored_gw.json"
    _d.write_text(json.dumps(_r, indent=1))
    _rc, _o, _e = attest(_d)
    assert _rc == 1 and "FAIL: groundwater: receipt 1.183" in _o, _o
    _r2 = json.loads(gw_path.read_text())
    del _r2["terms"]["groundwater"]
    _d2 = tmp / "dropped_gw.json"
    _d2.write_text(json.dumps(_r2, indent=1))
    _rc, _o, _e = attest(_d2)
    assert _rc == 1 and "the tree carries groundwater.json and the receipt carries no groundwater term" in _o, _o
    return


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

    for _b in ("ohio-olmsted", "lees-ferry", "roaring-fork", "ohio-olmsted-groundwater"):
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
    _names = set()
    for _r in sorted((trees / "receipts").glob("*.json")):
        _rc, _o, _e = attest(_r)
        assert _rc == 0, f"{_r.name}: {_o}{_e}"
        assert "PASS" in _o
        _names.add(_r.stem)
    assert _names == {"ohio-olmsted", "lees-ferry", "roaring-fork", "ohio-olmsted-groundwater"}, _names
    return


@app.cell
def _(root, tmp):
    # 11. The groundwater tree's well set carries its provenance and
    #     parameters with their sources, and the attester's own selftest
    #     (synthetic trees with hand-checkable numbers, the doctorings
    #     each bar must catch, the bounds of bar three) passes.
    import json as _json
    import subprocess as _sp

    _gw = _json.loads((root / "verification" / "fixtures" / "water-balance" / "ohio-olmsted-groundwater"
                       / "groundwater.json").read_text())
    assert _gw["parameters"]["specific_yield"]["source"]
    assert _gw["selection"]["wells_captured"] == 58 and _gw["selection"]["wells_kept"] == 58
    _sel = _gw["selection"]
    assert _sel["wells_covering_window"] == 249 and _sel["inside_polygon"] == 141
    assert _sel["inside_by_aquifer_type"] == {"U": 62, "C": 34, "M": 3, "X": 1, "none": 41}
    assert len(_sel["unconfined_without_constructed_depth"]) == 4 and len(_sel["inside_without_aquifer_type_code"]) == 41
    assert len(_sel["selected"]) == 58 and set(_sel["selected"]) == {w["site"] for w in _gw["wells"]}
    assert len(_gw["captures"]) == 6 and all(c["content_sha256"] and c["capture_id"] for c in _gw["captures"])
    assert all(w["aquifer_type_code"] == "U" and w["capture_id"] for w in _gw["wells"])
    _p = _sp.run(["uv", "run", str(root / "skills" / "basin-water-balance" / "scripts"
                       / "basin_water_balance_check.py"),
                  "--selftest"], capture_output=True, text=True, cwd=root)
    assert _p.returncode == 0, _p.stdout + _p.stderr
    assert "selftest: 0 failure(s)" in _p.stdout and "FAIL" not in _p.stdout
    _ = tmp
    return


if __name__ == "__main__":
    app.run()
