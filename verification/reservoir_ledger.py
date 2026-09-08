# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
# ]
# ///
# Golden notebook for the reservoir-ledger workflow (the golden-notebook
# requirement: one fixture-backed asserting script per workflow skill):
# Lake Powell for water year 2023 from six frozen captures and the 2018
# survey table, with the datum refusals asserted as behaviour and the
# residual reported rather than closed. Headless green via
# `uv run verification/reservoir_ledger.py`; no network, no credential.

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
    loader = root / "load_reservoir_ledger.py"
    inputs = root / "reservoir" / "ledger_powell_wy2023.json"
    tmp = Path(tempfile.mkdtemp(prefix="ledger_"))

    def run(datum="NAVD88", inputs_path=None, name="r"):
        out = tmp / f"{name}.json"
        p = subprocess.run(
            ["uv", "run", str(loader), "--inputs", str(inputs_path or inputs),
             "--datum", datum, "--out", str(out)], capture_output=True, text=True)
        r = json.loads(out.read_text()) if p.returncode == 0 else None
        return p.returncode, p.stderr, r

    return inputs, root, run, tmp, json, Path


@app.cell
def _(inputs, json):
    # 1. The inputs are six captures and one survey table, each carrying
    #    the identity a receipt cites. The elevation exists in two datums
    #    on purpose: that pair is what makes the conversion sourced.
    _d = json.loads(inputs.read_text())
    assert _d["reservoir"] == "Lake Powell"
    assert _d["window"]["convention"] == "water year 2023"
    _s = _d["series"]
    assert len(_s) == 6
    for _k, _v in _s.items():
        assert _v["days"] == 365, (_k, _v["days"])
        assert _v["approval"] == ["Approved"], (_k, _v["approval"])
        assert _v["capture_id"] and _v["content_sha256"]
    assert {_v["parameter"] for _v in _s.values()} == {"62614", "62615", "00060"}
    _t = _d["area_capacity_table"]
    assert _t["doi"] == "10.5066/P9O3IPG3"
    assert _t["rows"] == 1821
    assert "NAVD88" in _t["datum"] and "NGVD29" in _t["datum"]
    assert "1986" in _t["survey"], "the revision says which survey it replaced"
    return


@app.cell
def _(run):
    # 2. The ledger on the datum the table is primarily published on.
    _c, _e, led = run("NAVD88", name="navd88")
    assert _c == 0, _e
    _s = led["storage"]
    assert _s["elevation_series"]["parameter"] == "62615"
    assert _s["elevation_series"]["declares_datum"] == "NAVD88"
    assert _s["start"]["date"] == "2022-10-01" and _s["end"]["date"] == "2023-09-30"
    assert abs(_s["start"]["elevation_ft"] - 3532.00) < 0.005
    assert abs(_s["end"]["elevation_ft"] - 3576.10) < 0.005
    assert abs(_s["elevation_change_ft"] - 44.10) < 0.005
    assert abs(_s["start"]["capacity_acrefeet"] - 7534061) < 2
    assert abs(_s["end"]["capacity_acrefeet"] - 10527321) < 2
    assert abs(_s["change_acrefeet"] - 2993260) < 2
    assert abs(_s["change_km3"] - 3.692) < 0.001
    # The surface area grows by a third as the reservoir fills, which is
    # what makes the unmeasured evaporation term boundable by a reader.
    assert abs(_s["start"]["area_acres"] - 59286) < 2
    assert abs(_s["end"]["area_acres"] - 77259) < 2
    return (led,)


@app.cell
def _(led):
    # 3. The flows, and the residual reported rather than closed.
    _t = led["totals"]
    assert abs(_t["gauged_inflow_acrefeet"] - 11935172) < 2
    assert abs(_t["outflow_acrefeet"] - 8730367) < 2
    assert abs(_t["gauged_inflow_minus_outflow_acrefeet"] - 3204805) < 2
    assert abs(_t["residual_acrefeet"] - (-211545)) < 2
    assert abs(_t["residual_as_fraction_of_inflow"] - (-0.01772)) < 0.0001
    # The identity is not closed and the receipt says so, naming every
    # term it did not measure.
    assert "not closed" in led["not_closed"]
    _r = " ".join(led["residual_contains"]).lower()
    for _term in ("ungauged", "precipitation", "evaporation", "bank storage",
                  "travel time"):
        assert _term in _r, _term
    assert "not the dam release" in _r
    return


@app.cell
def _(led):
    # 4. The ungauged fraction is a stated term. Three inflow gauges span
    #    82.2 per cent of the area above the outlet, so a fifth of the
    #    basin arrives unmeasured and sits in the residual by name.
    _u = led["ungauged"]
    assert _u["gauged_drainage_mi2"] == 24100 + 44850 + 23000
    assert _u["outlet_drainage_mi2"] == 111800
    assert abs(_u["gauged_fraction"] - 0.82245) < 0.0001
    assert "contributing areas are not published" in _u["note"]
    return


@app.cell
def _(led):
    # 5. The datum, sourced rather than assumed: the agency publishes both
    #    series for this gauge, and their difference over the whole year
    #    is the conversion. The table's own two columns agree with it.
    _d = led["datum_check"]
    assert _d["other_datum"] == "NGVD29"
    assert _d["offset_ft"]["days"] == 365
    assert abs(_d["offset_ft"]["mean"] - 2.9148) < 0.001
    assert 2.89 < _d["offset_ft"]["min"] and _d["offset_ft"]["max"] < 3.01
    assert "not derived here" in _d["source"]

    # And what the confusion costs: large in a level, small in a change,
    # because a constant offset mostly cancels in a difference.
    _c = _d["cost_of_reading_the_other_datum_into_this_column"]
    assert abs(_c["start_acrefeet"] - 170580) < 2
    assert abs(_c["end_acrefeet"] - 221600) < 2
    assert abs(_c["change_acrefeet"] - 51020) < 2
    assert _c["change_acrefeet"] < _c["start_acrefeet"], \
        "the change is less wrong than either level, which is why this hides"
    return


@app.cell
def _(run):
    # 6. The same ledger on the other datum is internally consistent: the
    #    elevations differ by about three feet and the CHANGE agrees to
    #    within the rounding of the published values, because a constant
    #    offset cancels. This is the property that lets the mistake live.
    _c, _e, other = run("NGVD29", name="ngvd29")
    assert _c == 0, _e
    _s = other["storage"]
    assert _s["elevation_series"]["parameter"] == "62614"
    assert _s["elevation_series"]["declares_datum"] == "NGVD29"
    assert abs(_s["start"]["elevation_ft"] - 3529.10) < 0.005
    assert abs(_s["elevation_change_ft"] - 44.10) < 0.005
    return (other,)


@app.cell
def _(led, other):
    # 7. Read each elevation into its OWN column and the two datums
    #    describe the same water: the opening level agrees to about six
    #    hundred acre-feet in seven and a half million, which is the
    #    rounding of the published elevations to a tenth of a foot, and
    #    the change agrees as closely. The danger is not in either datum;
    #    it is entirely in crossing them, which cell 5 prices.
    _a = led["storage"]["change_acrefeet"]
    _b = other["storage"]["change_acrefeet"]
    _la = led["storage"]["start"]["capacity_acrefeet"]
    _lb = other["storage"]["start"]["capacity_acrefeet"]
    assert abs(_a - _b) < 1200, (_a, _b)
    assert abs(_la - _lb) < 1200, (_la, _lb)
    # The crossing error is two orders of magnitude larger than the
    # agreement, which is why the mistake is worth a concept.
    _crossed = led["datum_check"]["cost_of_reading_the_other_datum_into_this_column"]["start_acrefeet"]
    assert _crossed > 100 * abs(_la - _lb), (_crossed, abs(_la - _lb))
    print(f"read correctly, the two datums agree to {abs(_la - _lb):,.0f} acre-feet on the "
          f"opening level; crossed, they disagree by {_crossed:,.0f}")
    return


@app.cell
def _(Path, inputs, json, run, tmp):
    # 8. The refusals, asserted as behaviour. A table whose bytes moved is
    #    not the table that was published, and the loader will not read a
    #    volume out of it.
    _d = json.loads(inputs.read_text())
    _d["area_capacity_table"]["sha256"] = "0" * 64
    _bad = tmp / "tampered.json"
    _bad.write_text(json.dumps(_d))
    # the table itself lives beside the manifest, so copy it across
    import shutil as _shutil
    _shutil.copy(inputs.parent / _d["area_capacity_table"]["file"],
                tmp / _d["area_capacity_table"]["file"])
    _c, _err, _ = run("NAVD88", inputs_path=_bad, name="tampered")
    assert _c == 2, "a moved table must be refused"
    assert "not the bytes the manifest recorded" in _err, _err
    return


@app.cell
def _(inputs, json, run, tmp):
    # 9. And an elevation on a datum the input does not carry is refused
    #    rather than converted: this loader does not move an elevation
    #    between datums, it picks the series that declares the one asked
    #    for.
    _d = json.loads(inputs.read_text())
    _d["series"] = {k: v for k, v in _d["series"].items() if v["parameter"] != "62615"}
    _only29 = tmp / "only_ngvd29.json"
    _only29.write_text(json.dumps(_d))
    import shutil as _shutil
    _shutil.copy(inputs.parent / _d["area_capacity_table"]["file"],
                tmp / _d["area_capacity_table"]["file"])
    _c, _err, _ = run("NAVD88", inputs_path=_only29, name="only29")
    assert _c == 2, "with no NAVD88 series present the loader must refuse"
    assert "not converted between datums here" in _err, _err
    return


if __name__ == "__main__":
    app.run()
