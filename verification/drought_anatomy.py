# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "pandas",
#     "pyarrow",
# ]
# ///
# Golden notebook for the drought-anatomy workflow (the golden-notebook
# requirement: one fixture-backed asserting script per workflow skill):
# the five frozen panels of the Colorado above Lees Ferry for water year
# 2021 against water year 2023, the refusals asserted as behaviour, and
# the two years' panels checked for comparability before they are
# compared. Headless green via `uv run verification/drought_anatomy.py`;
# no network, no credential.

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
    loader = root / "load_drought_panels.py"
    precip_loader = root / "load_precipitation.py"
    basin = root / "basins" / "usgs_09380000_nldi.geojson"
    tmp = Path(tempfile.mkdtemp(prefix="drought_"))

    def precip_receipt(wy):
        out = tmp / f"p_{wy}.json"
        if not out.exists():
            p = subprocess.run(
                ["uv", "run", str(precip_loader), "--source", "imerg", "--run", "final",
                 "--basin", str(basin),
                 "--window", str(root / "precipitation" / f"imerg_final_lees_ferry_{wy}.nc"),
                 "--out", str(out)], capture_output=True, text=True)
            assert p.returncode == 0, p.stderr[-2000:]
        return out

    def run(wy, extra=(), basin_override=None, name=None):
        name = name or wy
        out = tmp / f"r_{name}.json"
        cmd = ["uv", "run", str(loader), "--label", f"lees_ferry_{wy}",
               "--basin", str(basin_override or basin),
               "--precipitation-receipt", str(precip_receipt(wy)),
               "--soil-moisture", str(root / "smap" / f"smap_l3_lees_ferry_{wy}.json"),
               "--streamflow", str(root / f"lees_ferry_00060_{wy}_dv.parquet"),
               "--storage", str(root / "grace" / f"mascon_lees_ferry_{wy}.json"),
               "--snow", str(root / "snodas" / f"snodas_swe_lees_ferry_{wy}.json"),
               "--out", str(out)]
        cmd += list(extra)
        p = subprocess.run(cmd, capture_output=True, text=True)
        r = json.loads(out.read_text()) if p.returncode == 0 else None
        return p.returncode, p.stderr, r

    REG = ["--regulated"]
    return REG, basin, root, run


@app.cell
def _(REG, run):
    # 1. Both years assemble, and the basin clears the storage footprint
    #    floor, which is the question that decides how many panels there
    #    can be.
    _c1, _e1, dry = run("wy2021", REG)
    _c2, _e2, wet = run("wy2023", REG)
    assert _c1 == 0, _e1
    assert _c2 == 0, _e2
    for _r in (dry, wet):
        assert _r["basin"]["above_footprint_floor"] is True
        assert abs(_r["basin"]["mascons"] - 2.48) < 0.01, _r["basin"]["mascons"]
        assert set(_r["panels"]) == {"precipitation", "soil_moisture", "streamflow",
                                     "storage", "snow"}
        assert "not combined" in _r["no_index"]
    return dry, wet


@app.cell
def _(dry, wet):
    # 2. Comparability before comparison. The soil moisture panels are
    #    means over a cell mask, and a mask derived from one day's
    #    coverage would differ between years and make the two means
    #    different quantities. Both years must stand on the same cells.
    _a, _b = dry["panels"]["soil_moisture"], wet["panels"]["soil_moisture"]
    assert _a["cells_inside_polygon"] == _b["cells_inside_polygon"] == 213
    # And the storage panels must span the same mascons, for the same
    # reason.
    assert dry["panels"]["storage"]["mascon_ids"] == wet["panels"]["storage"]["mascon_ids"]
    assert dry["panels"]["storage"]["mascons"] == 7
    return


@app.cell
def _(dry, wet):
    # 3. Precipitation: one run for the whole series in both years, and
    #    the wet year about a quarter wetter.
    _a, _b = dry["panels"]["precipitation"], wet["panels"]["precipitation"]
    assert _a["run"] == _b["run"] == "final"
    assert _a["months"] == _b["months"] == 12
    assert abs(_a["total_mm"] - 257.2) < 0.5, _a["total_mm"]
    assert abs(_b["total_mm"] - 320.4) < 0.5, _b["total_mm"]
    assert 1.2 < _b["total_mm"] / _a["total_mm"] < 1.3
    return


@app.cell
def _(dry, wet):
    # 4. Snow, the panel that shows the drought most sharply: the wet
    #    year peaks at about two and a half times the dry year, and both
    #    peaks are in early April.
    _a, _b = dry["panels"]["snow"], wet["panels"]["snow"]
    assert _a["is_model_output"] and _b["is_model_output"]
    assert _a["peak"]["date"] == "2021-04-01" and _b["peak"]["date"] == "2023-04-01"
    assert abs(_a["peak"]["basin_mean_swe_mm"] - 64.78) < 0.05
    assert abs(_b["peak"]["basin_mean_swe_mm"] - 163.14) < 0.05
    assert 2.4 < _b["peak"]["basin_mean_swe_mm"] / _a["peak"]["basin_mean_swe_mm"] < 2.6
    # Both years end their water year with no snow, which is what makes
    # the peak the comparable quantity.
    assert _a["series_mm"]["2021-08-01"] == 0.0 and _b["series_mm"]["2023-08-01"] == 0.0
    assert "not recommended" in _a["cannot_show"]
    return


@app.cell
def _(dry, wet):
    # 5. Streamflow: the panel that shows nothing. Five per cent apart
    #    across the driest and one of the wettest years, because the
    #    gauge is below a major dam, and the panel says so itself.
    _a, _b = dry["panels"]["streamflow"], wet["panels"]["streamflow"]
    assert _a["site"] == _b["site"] == "USGS-09380000"
    assert _a["days"] == _b["days"] == 365
    assert abs(_a["mean"] - 11435) < 5 and abs(_b["mean"] - 12059) < 5
    assert _b["mean"] / _a["mean"] < 1.06, "the release schedule, not the weather"
    assert _a["regulated"] and "operations record" in _a["cannot_show"]
    assert _a["approval"] == {"Approved": 365}
    return


@app.cell
def _(dry, wet):
    # 6. Storage: the only panel that speaks in water the basin kept.
    #    The drought year ends where it began; the wet year gains nearly
    #    5 cm, which is well outside the per-epoch uncertainty.
    _a, _b = dry["panels"]["storage"], wet["panels"]["storage"]
    assert abs(_a["change_cm"] - (-0.5)) < 0.1, _a["change_cm"]
    assert abs(_b["change_cm"] - 4.78) < 0.1, _b["change_cm"]
    assert _b["change_cm"] > 2 * _a["typical_uncertainty_cm"]
    assert abs(_a["change_cm"]) < _a["typical_uncertainty_cm"], \
        "the drought year's change is inside its own uncertainty, and is reported as such"
    assert _a["effective_sample_size"] == 7, "mascons, not cells"
    assert _a["record_last_epoch"] == _b["record_last_epoch"] == "2026-06-16"
    assert "where the record stops" in _a["cannot_show"]
    return


@app.cell
def _(dry, wet):
    # 7. Soil moisture: the panel whose honesty is the count beside it.
    #    Winter coverage collapses in a snowy basin, so a winter mean is
    #    the mean of a few per cent of the basin, and the panel names the
    #    months where that is true rather than letting them pass.
    _a, _b = dry["panels"]["soil_moisture"], wet["panels"]["soil_moisture"]
    for _p in (_a, _b):
        assert _p["record_begins"] == "2015-03-31"
        assert "too short for a percentile" in _p["cannot_show"]
        assert "AM" in _p["overpass"]
        _winter = [m for m in _p["monthly"] if m[-2:] in ("12", "01", "02")]
        assert _winter, "the window covers a winter"
        _thin = set(_p["months_under_quarter_coverage"])
        assert _thin & set(_winter), "winter months fall under quarter coverage"
        for _m, _v in _p["monthly"].items():
            assert 0 < _v["coverage"] <= 1.0
            assert 0.0 <= _v["mean_m3m3"] <= 0.6
    # Summer coverage is far better than winter coverage in both years,
    # which is the sampling and not the soil.
    for _p in (_a, _b):
        _win = [_p["monthly"][m]["coverage"] for m in _p["monthly"] if m[-2:] in ("01", "02")]
        _sum = [_p["monthly"][m]["coverage"] for m in _p["monthly"] if m[-2:] in ("07", "08")]
        assert min(_sum) > max(_win), (min(_sum), max(_win))
    return


@app.cell
def _(REG, root, run):
    # 8. The refusals, asserted as behaviour rather than described. A
    #    basin below the footprint floor gets no storage panel, and the
    #    refusal names the floor rather than leaving a gap.
    _c, _err, _ = run("wy2021", REG, basin_override=root / "basins" / "usgs_09085000_nldi.geojson",
                      name="below_floor")
    assert _c == 2, "a basin below the floor must not receive a storage panel"
    assert "footprint floor" in _err and "111,266" in _err, _err
    return


@app.cell
def _(dry, wet):
    # 9. The panels disagree about the size of the drought, and that is
    #    the finding rather than a defect. Ordered by how much the wet
    #    year exceeds the dry one: snow, then precipitation, then
    #    streamflow, with storage changing sign.
    _snow = (wet["panels"]["snow"]["peak"]["basin_mean_swe_mm"]
             / dry["panels"]["snow"]["peak"]["basin_mean_swe_mm"])
    _precip = wet["panels"]["precipitation"]["total_mm"] / dry["panels"]["precipitation"]["total_mm"]
    _flow = wet["panels"]["streamflow"]["mean"] / dry["panels"]["streamflow"]["mean"]
    assert _snow > _precip > _flow, (_snow, _precip, _flow)
    assert _snow > 2.4 and _flow < 1.06
    assert dry["panels"]["storage"]["change_cm"] < 0 < wet["panels"]["storage"]["change_cm"]
    print(f"wet over dry: snow {_snow:.2f}, precipitation {_precip:.2f}, "
          f"streamflow {_flow:.2f}; storage {dry['panels']['storage']['change_cm']:+.1f} "
          f"against {wet['panels']['storage']['change_cm']:+.1f} cm")
    return


if __name__ == "__main__":
    app.run()
