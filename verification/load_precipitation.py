# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "netCDF4",
#     "numpy",
# ]
# ///
# Golden notebook for the load-precipitation workflow (the golden-notebook
# requirement: one fixture-backed asserting script per workflow skill):
# the frozen basin-window files under fixtures/precipitation/ (IMERG
# Final for water year 2023, IMERG Late for October 2022 and October
# 2023, NLDAS-2 forcing for water year 2023, all cut to the Colorado
# River basin above Lees Ferry) go through the loader beside them and
# reproduce the recorded basin means, the coverage numbers, the
# refusals the run-mixing gotcha requires, the seam a declared change
# of run produces, the Late against Final difference and the NLDAS-2
# against IMERG cold-season ratio. Reference numbers measured at
# fixture creation and recorded in fixtures/README.md. Headless green
# via `uv run verification/load_precipitation.py`; no network, no
# credential.

import marimo

__generated_with = "0.23.13"
app = marimo.App()


@app.cell
def _():
    import hashlib
    import json
    import subprocess
    import tempfile
    from pathlib import Path

    root = Path(__file__).parent / "fixtures"
    loader = root / "load_precipitation.py"
    basin = root / "basins" / "usgs_09380000_nldi.geojson"
    windows = root / "precipitation"
    tmp = Path(tempfile.mkdtemp(prefix="load_precipitation_"))

    def run(source, run_decl, files, start=None, end=None, name="r"):
        # The loader as the skill runs it: `uv run` on the script beside
        # the fixtures, refusals as exit 2 with a REFUSED line on stderr.
        cmd = ["uv", "run", str(loader), "--source", source, "--basin", str(basin),
               "--out", str(tmp / f"{name}.json")]
        if run_decl:
            cmd += ["--run", run_decl]
        for f in files:
            cmd += ["--window", str(windows / f)]
        if start:
            cmd += ["--start", start, "--end", end]
        p = subprocess.run(cmd, capture_output=True, text=True)
        receipt = json.loads((tmp / f"{name}.json").read_text()) if p.returncode == 0 else None
        return p.returncode, p.stdout, p.stderr, receipt

    def sha(f):
        return hashlib.sha256((windows / f).read_bytes()).hexdigest()

    return run, sha, windows


@app.cell
def _(run):
    # 1. IMERG Final, water year 2023, declared once for the window: every
    #    month is final and complete, no seam, and the basin mean and
    #    volume reproduce the recorded numbers. Coverage: 2869 of the
    #    5412 window cells have their centre inside the polygon and their
    #    area is 99.5 per cent of the polygon's equal-area area.
    _code, _out, _err, final = run("imerg", "final", ["imerg_final_lees_ferry_wy2023.nc"], name="final")
    assert _code == 0, _err
    assert final["run_declaration"] == "final" and final["seams"] == []
    assert set(final["runs_by_month"].values()) == {"final"} and len(final["monthly"]) == 12
    assert all(m["complete"] and m["run"] == "final" and m["labels"] == ["V07B"] for m in final["monthly"])
    assert final["window"]["days_with_data"] == 365 and final["window"]["days_absent"] == []
    cov = final["coverage"]
    assert cov["cells_in_window"] == 5412 and cov["cells_inside"] == 2869
    assert abs(cov["inside_area_over_polygon_area"] - 0.9955) < 5e-4
    assert abs(final["basin"]["area_km2"] - 276443.7) < 0.1 and final["basin"]["area_projection"] == "ESRI:102008"
    monthly = {m["month"]: m["mm"] for m in final["monthly"]}
    expected = {"2022-10": 29.13, "2022-11": 16.42, "2022-12": 30.73, "2023-01": 27.28, "2023-02": 16.43,
                "2023-03": 44.19, "2023-04": 24.14, "2023-05": 20.04, "2023-06": 26.35, "2023-07": 15.63,
                "2023-08": 47.58, "2023-09": 22.54}
    for mth, mm in expected.items():
        assert abs(monthly[mth] - mm) < 0.01, f"{mth}: {monthly[mth]} mm, recorded {mm}"
    assert abs(final["total"]["mm"] - 320.44) < 0.01 and abs(final["total"]["km3"] - 88.585) < 0.001
    assert final["window_files"][0]["doi"] == "10.5067/GPM/IMERGDF/DAY/07"
    assert "SEAM" not in _out
    return (final,)


@app.cell
def _(run):
    # 2. The refusals the run-mixing gotcha requires: no run declared; a
    #    run declared that the file does not hold (Final on a Late file,
    #    and the same file appended to a Final window as an undeclared
    #    mix); a day present in two files; and Final declared for months
    #    after the end of the V07 Final record, refused with the date.
    _code, _, _err, _ = run("imerg", None, ["imerg_final_lees_ferry_wy2023.nc"], name="norun")
    assert _code == 2 and _err.startswith("REFUSED") and "--run" in _err and "never chosen" in _err

    _code, _, _err, _ = run("imerg", "final", ["imerg_late_lees_ferry_2023-10.nc"], name="mismatch")
    assert _code == 2 and "declared final, the file holds late" in _err

    _code, _, _err, _ = run("imerg", "final", ["imerg_final_lees_ferry_wy2023.nc", "imerg_late_lees_ferry_2023-10.nc"],
                          "2023-09-01", "2023-10-31", name="mix")
    assert _code == 2 and "2023-10: declared final, the file holds late" in _err

    _code, _, _err, _ = run("imerg", "final", ["imerg_final_lees_ferry_wy2023.nc", "imerg_final_lees_ferry_wy2023.nc"], name="dup")
    assert _code == 2 and "appears in two window files" in _err

    _code, _, _err, _ = run("imerg", "final", ["imerg_final_lees_ferry_wy2023.nc"], "2025-09-01", "2025-10-31", name="past")
    assert _code == 2 and "ends at 2025-09-30" in _err and "2025-10" in _err and "imerg-v07.md" in _err
    return


@app.cell
def _(run):
    # 3. A declared change of run is a seam, dated and named per month:
    #    Final for September 2023 and Late for October 2023 load as two
    #    calibrations with the seam at 2023-10-01, and each month keeps
    #    its own run in the receipt.
    _code, _out, _err, seam = run("imerg", "2023-09:final,2023-10:late",
                               ["imerg_final_lees_ferry_wy2023.nc", "imerg_late_lees_ferry_2023-10.nc"],
                               "2023-09-01", "2023-10-31", name="seam")
    assert _code == 0, _err
    assert seam["runs_by_month"] == {"2023-09": "final", "2023-10": "late"}
    assert [s["kind"] for s in seam["seams"]] == ["run"]
    assert seam["seams"][0]["date"] == "2023-10-01" and seam["seams"][0]["from"] == "final" and seam["seams"][0]["to"] == "late"
    assert "SEAM 2023-10-01 (run)" in _out
    assert abs(seam["monthly"][0]["mm"] - 22.54) < 0.01 and abs(seam["monthly"][1]["mm"] - 20.78) < 0.01
    return


@app.cell
def _(final, run):
    # 4. The same month through two runs: Late October 2022 against Final
    #    October 2022, the same 2869 cells and the same variable name,
    #    differ by 53 per cent of the Final value. This is the size of
    #    the calibration difference the gotcha records; no field in
    #    either file announces it.
    _code, _, _err, late = run("imerg", "late", ["imerg_late_lees_ferry_2022-10.nc"], name="late")
    assert _code == 0, _err
    assert late["runs_by_month"] == {"2022-10": "late"} and late["monthly"][0]["complete"]
    assert late["coverage"]["cells_inside"] == final["coverage"]["cells_inside"]
    late_mm, final_mm = late["total"]["mm"], final["monthly"][0]["mm"]
    assert abs(late_mm - 44.53) < 0.01 and abs(final_mm - 29.13) < 0.01
    assert 1.52 < late_mm / final_mm < 1.54, f"Late over Final for October 2022: {late_mm / final_mm:.3f}"
    assert abs(late["total"]["km3"] - 12.311) < 0.001
    return


@app.cell
def _(final, run, windows):
    # 5. NLDAS-2 forcing over the same polygon and water year: the
    #    gauge-based series the cold-season gotcha names as the check.
    #    The file records the hour convention (day D is the granules D
    #    01:00 through D+1 00:00).
    import netCDF4

    _code, _, _err, nldas = run("nldas2", None, ["nldas2_lees_ferry_wy2023.nc"], name="nldas")
    assert _code == 0, _err
    assert nldas["source"] == "nldas2" and set(nldas["runs_by_month"].values()) == {"nldas2"}
    assert nldas["window"]["days_with_data"] == 365 and all(m["complete"] for m in nldas["monthly"])
    assert nldas["coverage"]["cells_inside"] == 1851 and nldas["coverage"]["cells_in_window"] == 3498
    assert abs(nldas["coverage"]["inside_area_over_polygon_area"] - 1.0036) < 5e-4
    assert abs(nldas["total"]["mm"] - 374.53) < 0.01 and abs(nldas["total"]["km3"] - 103.535) < 0.001
    assert nldas["window_files"][0]["doi"] == "10.5067/THUF4J1RLSYG"
    with netCDF4.Dataset(str(windows / "nldas2_lees_ferry_wy2023.nc")) as ds:
        assert "D.0100" in ds.hour_convention and "granule_count" in ds.ncattrs() and ds.granule_count == 365 * 24
    # The cold-season ratio: November through March, IMERG Final over
    # NLDAS-2, and the water-year ratio, both recorded in fixtures/README.md.
    imerg = {m["month"]: m["mm"] for m in final["monthly"]}
    gauge = {m["month"]: m["mm"] for m in nldas["monthly"]}
    cold = ["2022-11", "2022-12", "2023-01", "2023-02", "2023-03"]
    cold_ratio = sum(imerg[m] for m in cold) / sum(gauge[m] for m in cold)
    year_ratio = final["total"]["mm"] / nldas["total"]["mm"]
    assert abs(cold_ratio - 0.676) < 0.005, f"cold-season IMERG over NLDAS-2: {cold_ratio:.3f}"
    assert abs(year_ratio - 0.856) < 0.005, f"water-year IMERG over NLDAS-2: {year_ratio:.3f}"
    assert cold_ratio < year_ratio < 1.0, "IMERG reads low against the gauge analysis, and lower in the cold season"
    return


@app.cell
def _(sha):
    # 6. The fixtures are the bytes their provenance rows record.
    _expected = {
        "imerg_final_lees_ferry_wy2023.nc": "84d1051cf3aff32a60a6959eaaeb4c8f0e993fae5682f9a75a1aa833f98a2ea8",
        "imerg_late_lees_ferry_2022-10.nc": "115d1c746f3ffed610f3983ae89a0c9b60d620d92588663796ac9617bcc43de3",
        "imerg_late_lees_ferry_2023-10.nc": "c1f497ffbdfe59ccc441d20aa0cd701025c097fe6e3e3b7683e2341138347fbb",
        "nldas2_lees_ferry_wy2023.nc": "2c0d1d4aa17be9a5dab8d5338e8e5dffd2643a34e1144b8d337e2fb038f4c006",
    }
    for _f, _h in _expected.items():
        assert sha(_f) == _h, f"{_f}: sha256 {sha(_f)[:12]} differs from the recorded {_h[:12]}"
    return


if __name__ == "__main__":
    app.run()
