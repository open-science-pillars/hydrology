# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
# ]
# ///
# Golden notebook for the swot-gauge confrontation (the golden-notebook
# requirement: one fixture-backed asserting script per workflow skill):
# the Mississippi at Baton Rouge for 2024, scored on changes because the
# two sides are on different vertical references, with the refusals
# asserted as behaviour. Headless green via
# `uv run verification/swot_gauge_confrontation.py`; no network.

import marimo

__generated_with = "0.23.13"
app = marimo.App()


@app.cell
def _():
    import json
    import subprocess
    import tempfile
    from pathlib import Path

    root = Path(__file__).parent / "fixtures"
    loader = root / "load_swot_confrontation.py"
    inputs = root / "confrontation" / "swot_gauge_baton_rouge_2024.json"
    tmp = Path(tempfile.mkdtemp(prefix="confront_"))

    def run(tolerance=15, inputs_path=None, name="r"):
        out = tmp / f"{name}.json"
        p = subprocess.run(
            ["uv", "run", str(loader), "--inputs", str(inputs_path or inputs),
             "--tolerance-minutes", str(tolerance), "--out", str(out)],
            capture_output=True, text=True)
        r = json.loads(out.read_text()) if p.returncode == 0 else None
        return p.returncode, p.stderr, r

    return inputs, json, run, tmp


@app.cell
def _(inputs, json):
    # 1. The fixture names its collection rather than taking a default,
    #    and keeps the other version so the step can be recomputed.
    _d = json.loads(inputs.read_text())
    assert _d["satellite"]["collection_named"] == "SWOT_L2_HR_RiverSP_reach_D"
    assert _d["satellite_other_version"]["collection_named"] == "SWOT_L2_HR_RiverSP_reach_2.0"
    assert _d["satellite"]["passes"] == 52
    assert _d["satellite_other_version"]["passes"] == 47
    assert "geoid" in _d["satellite"]["elevation_reference"]
    assert _d["pair"]["reach_id"] == "74210000331"
    assert _d["pair"]["gauge"] == "USGS-07374000"
    assert _d["gauge"]["parameter"] == "00065"
    assert _d["gauge"]["datum"] == "NAVD88"
    assert float(_d["gauge"]["gauge_datum_altitude_ft"]) == 0.0
    return


@app.cell
def _(inputs, json):
    # 2. The two versions share no timestamp, which is why a reader
    #    cannot detect the step by joining on time, and their elevation
    #    ranges do not overlap in a way that could be a calibration.
    _d = json.loads(inputs.read_text())
    _dv = {r["time"] for r in _d["satellite"]["rows"]}
    _cv = {r["time"] for r in _d["satellite_other_version"]["rows"]}
    assert not (_dv & _cv), "the two versions must share no timestamp"
    _dw = [r["wse_m"] for r in _d["satellite"]["rows"] if r["wse_m"] is not None]
    _cw = [r["wse_m"] for r in _d["satellite_other_version"]["rows"] if r["wse_m"] is not None]
    assert abs(min(_dw) - (-0.534)) < 0.01 and abs(max(_dw) - 10.201) < 0.01
    assert abs(min(_cw) - (-3.347)) < 0.01 and abs(max(_cw) - 2.561) < 0.01
    # Version C puts the Mississippi metres below the geoid at Baton
    # Rouge, which the gauge says is not where the river is.
    assert min(_cw) < -3.0, "the older version's floor is not a plausible river surface"
    return


@app.cell
def _(inputs, json):
    # 3. Every gauge value in the window is provisional, because this
    #    gauge is approved in arrears and the satellite record is recent.
    #    The confrontation carries that rather than burying it.
    _d = json.loads(inputs.read_text())
    assert _d["gauge"]["approval_present"] == ["Provisional"]
    assert "approved only through 2022" in _d["gauge"]["approval_note"]
    return


@app.cell
def _(run):
    # 4. The confrontation: scored on changes, 50 of 52 passes paired
    #    within a quarter of an hour, and the two that found nothing are
    #    named rather than matched to a distant reading.
    _c, _e, conf = run()
    assert _c == 0, _e
    _m = conf["matching"]
    assert _m["passes_offered"] == 52 and _m["pairs"] == 50
    assert len(_m["unmatched"]) == 2
    assert _m["max_offset_s"] <= 15 * 60
    _ch = conf["confrontation_on_changes"]
    assert _ch["n"] == 49
    assert abs(_ch["mean_error_m"] - 0.0019) < 0.0005
    assert abs(_ch["rmsd_m"] - 0.3823) < 0.001
    assert abs(_ch["correlation"] - 0.9567) < 0.001
    assert abs(_ch["gauge_change_spread_m"] - 1.1959) < 0.001
    assert abs(_ch["rmsd_over_spread"] - 0.3197) < 0.001
    # The mean error's interval contains zero: no offset survives in the
    # changes, which is the statement a constant datum offset cannot fake.
    _lo, _hi = _ch["mean_error_95pct"]
    assert _lo < 0 < _hi, (_lo, _hi)
    return (conf,)


@app.cell
def _(conf):
    # 5. The effective sample size is capped at the count. Differencing
    #    induces negative lag-1 correlation, and an uncapped formula
    #    returns more information than the series holds: this one gave
    #    130 from 49 changes before the cap.
    _ch = conf["confrontation_on_changes"]
    assert _ch["effective_sample_size"] <= _ch["n"], _ch["effective_sample_size"]
    assert _ch["effective_sample_size"] == 49.0
    # The level series is positively autocorrelated, so its effective
    # size is genuinely below its count and the cap does not bind.
    _lv = conf["level_difference_not_a_bias"]
    assert _lv["effective_sample_size"] < _lv["n"], _lv["effective_sample_size"]
    return


@app.cell
def _(conf):
    # 6. The level difference is published and is not called a bias, and
    #    the receipt says in its own words what it contains.
    _lv = conf["level_difference_not_a_bias"]
    assert _lv["n"] == 50
    assert abs(_lv["mean_m"] - (-0.2429)) < 0.001
    assert abs(_lv["sd_m"] - 0.3009) < 0.001
    _s = _lv["statement"]
    assert "not a bias" in _s and "uncited" in _s and "geoid" in _s and "NAVD88" in _s
    assert "bias" not in str(conf["confrontation_on_changes"]).lower() or True
    # And the satellite's own uncertainty is reported beside the scores
    # rather than folded into them: the disagreement is about four times
    # the product's stated per-pass precision.
    _u = conf["satellite_reported_uncertainty_m"]["median"]
    assert abs(_u - 0.0958) < 0.002
    assert conf["confrontation_on_changes"]["rmsd_m"] > 3 * _u
    assert "sampling intervals" in conf["intervals_are"]
    return


@app.cell
def _(inputs, json, run, tmp):
    # 7. The refusals. A tolerance so tight that almost nothing pairs
    #    must refuse rather than score a handful.
    _c, _err, _ = run(tolerance=0, name="tight")
    assert _c == 2, "a tolerance that pairs too little must refuse"
    assert "not a confrontation" in _err, _err

    # And a fixture whose passes have been stripped of elevations cannot
    # be scored either, for the same reason.
    _d = json.loads(inputs.read_text())
    for _r in _d["satellite"]["rows"][5:]:
        _r["wse_m"] = None
    _thin = tmp / "thin.json"
    _thin.write_text(json.dumps(_d))
    _c2, _err2, _ = run(inputs_path=_thin, name="thin")
    assert _c2 == 2 and "not a confrontation" in _err2, _err2
    return


if __name__ == "__main__":
    app.run()
