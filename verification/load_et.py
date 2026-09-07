# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "netCDF4",
#     "numpy",
# ]
# ///
# Golden notebook for the load-et workflow (the golden-notebook
# requirement: one fixture-backed asserting script per workflow skill):
# the frozen window files under fixtures/et/ (MOD16A2GF over the
# Roaring Fork and over a Lake Powell box for calendar 2023, and the
# OpenET ensemble over a HUC12 inside the Roaring Fork at both
# intervals) go through the loader beside them and reproduce the
# recorded basin means, the masked fractions and fill classes the fill
# gotcha requires, the short year-end composite the compositing gotcha
# requires, the area-cap refusal, the monthly against daily
# disagreement, and the MOD16 against OpenET comparison recorded in the
# dataset concept. Reference numbers measured at fixture creation and
# recorded in fixtures/README.md. Headless green via
# `uv run verification/load_et.py`; no network, no credential.

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
    loader = root / "load_et.py"
    basins = root / "basins"
    et = root / "et"
    tmp = Path(tempfile.mkdtemp(prefix="load_et_"))

    def run(basin, files=(), source="mod16", response=None, extra=(), name="r"):
        # The loader as the skill runs it: `uv run` on the script beside
        # the fixtures, refusals as exit 2 with a REFUSED line on stderr.
        cmd = ["uv", "run", str(loader), "--source", source,
               "--basin", str(basins / basin), "--out", str(tmp / f"{name}.json")]
        for f in files:
            cmd += ["--window", str(et / f)]
        if response:
            cmd += ["--response", str(et / response)]
        cmd += list(extra)
        p = subprocess.run(cmd, capture_output=True, text=True)
        receipt = json.loads((tmp / f"{name}.json").read_text()) if p.returncode == 0 else None
        return p.returncode, p.stdout, p.stderr, receipt

    def sha(f):
        return hashlib.sha256((et / f).read_bytes()).hexdigest()

    return et, run, sha


@app.cell
def _(run):
    # 1. MOD16A2GF over the Roaring Fork, calendar 2023: 46 composites,
    #    the monthly series apportioned by day, the annual total and
    #    volume, and a basin that is almost entirely measured (1.2 per
    #    cent masked), so the fill classes are present but marginal.
    _code, _out, _err, rf = run("usgs_09085000_nldi.geojson", ["mod16a2gf_roaring_fork_2023.nc"], name="rf")
    assert _code == 0, _err
    assert rf["product"] == "mod16a2gf" and rf["window"]["composites"] == 46
    assert rf["coverage"]["cells_inside"] == 17531
    assert abs(rf["coverage"]["masked_fraction_any_composite"] - 0.0119) < 0.002
    assert rf["window_files"][0]["doi"] == "10.5067/MODIS/MOD16A2GF.061"
    assert rf["window_files"][0]["tile"] == "h09v05"

    _expected = {"2023-01": 20.77, "2023-02": 29.88, "2023-03": 42.57, "2023-04": 54.38,
                 "2023-05": 61.76, "2023-06": 59.86, "2023-07": 65.12, "2023-08": 54.72,
                 "2023-09": 32.31, "2023-10": 23.66, "2023-11": 23.94, "2023-12": 25.65}
    assert [m["month"] for m in rf["monthly"]] == sorted(_expected)
    for _m in rf["monthly"]:
        assert abs(_m["mm"] - _expected[_m["month"]]) < 0.01, (_m, _expected[_m["month"]])
    assert abs(rf["total"]["mm"] - 494.60) < 0.01
    assert abs(rf["total"]["km3"] - 1.8391) < 0.001
    assert rf["total"]["days"] == 365
    return (rf,)


@app.cell
def _(run):
    # 2. The compositing rule: 46 periods, one of them short, and every
    #    calendar month covered by exactly its own days. The year-end
    #    composite is five days and is weighted as five, not eight.
    _code, _out, _err, r = run("usgs_09085000_nldi.geojson", ["mod16a2gf_roaring_fork_2023.nc"], name="comp")
    assert _code == 0, _err
    assert sorted(r["window"]["composite_days"]) == [5, 8]
    assert r["window"]["short_periods"] == [{"start": "2023-12-27", "days": 5}]
    assert "SHORT PERIOD" in _out and "2023-12-27 (5 days)" in _out
    _days = {m["month"]: m["days_covered"] for m in r["monthly"]}
    assert _days == {"2023-01": 31, "2023-02": 28, "2023-03": 31, "2023-04": 30, "2023-05": 31,
                     "2023-06": 30, "2023-07": 31, "2023-08": 31, "2023-09": 30, "2023-10": 31,
                     "2023-11": 30, "2023-12": 31}
    _last = [c for c in r["per_composite"] if c["days"] == 5][0]
    assert abs(_last["mm"] - 4.4461) < 0.001
    # Read as eight days, that period's rate would be five eighths of the
    # truth and three days of it would fall outside the year.
    assert abs(_last["mm"] / 5 - 0.8892) < 0.001 and abs(_last["mm"] / 8 - 0.5558) < 0.001
    return


@app.cell
def _(run):
    # 3. The fill gotcha, measured: over a unit half covered by Lake
    #    Powell the loader refuses rather than averaging the vegetated
    #    remnant, and names the masked fraction in the refusal.
    _code, _out, _err, _ = run("huc12_padre_creek_lake_powell.geojson",
                               ["mod16a2gf_lake_powell_2023.nc"], name="padre_refusal")
    assert _code == 2 and _err.startswith("REFUSED")
    assert "52.4%" in _err and "--max-masked" in _err
    assert "mod16-fill-over-water-barren-urban.md" in _err

    # Declared deliberately, the number comes with its masking: 242 water
    # cells and 14 barren of 489, and a volume over the 49.9 km2 that has
    # an estimate rather than the polygon's 104.6 km2.
    _code, _out, _err, lp = run("huc12_padre_creek_lake_powell.geojson",
                                ["mod16a2gf_lake_powell_2023.nc"],
                                extra=["--max-masked", "0.9"], name="padre")
    assert _code == 0, _err
    assert lp["coverage"]["cells_inside"] == 489
    assert abs(lp["coverage"]["masked_fraction_any_composite"] - 0.5235) < 0.002
    assert lp["coverage"]["fill_classes_max_cells"]["water"] == 242
    assert lp["coverage"]["fill_classes_max_cells"]["barren-or-sparse-vegetation"] == 14
    assert abs(lp["total"]["mm"] - 168.72) < 0.01
    assert abs(lp["coverage"]["mean_measured_area_km2"] - 50.0) < 0.5
    assert abs(lp["coverage"]["polygon_area_km2"] - 104.6) < 0.1
    assert abs(lp["total"]["km3"] - 0.0084) < 0.0005
    # The volume is over the measured area, so it is NOT the mean times
    # the polygon area: that product would be more than twice as large.
    assert abs(lp["total"]["km3"] / (168.72 * 1e-6 * lp["coverage"]["polygon_area_km2"]) - 0.478) < 0.01
    assert "no MOD16 cell" not in lp["open_water"] and "excluded from the mean" in lp["open_water"]
    return (lp,)


@app.cell
def _(lp):
    # 4. The zero reading, which is the failure the gotcha exists to
    #    catch, reproduced from the receipt: the same numerator over all
    #    489 cells instead of the measured ones is 80.4 mm, 48 per cent
    #    of the honest number, with no arithmetic error anywhere.
    _zero = sum(c["mm"] * c["cells_measured"] for c in lp["per_composite"]) / lp["coverage"]["cells_inside"]
    assert abs(_zero - 80.39) < 0.05, _zero
    assert abs(_zero / lp["total"]["mm"] - 0.476) < 0.005
    return


@app.cell
def _(run):
    # 5. The OpenET area cap: refused before any request leaves the
    #    machine, with the acreage, the cap and the multiple named, for
    #    the basin the fixtures hold.
    _code, _out, _err, _ = run("usgs_09085000_nldi.geojson", source="openet",
                               response="openet_ensemble_huc12_capitol_creek_2023.json", name="cap")
    assert _code == 2 and _err.startswith("REFUSED")
    assert "930,871 acres" in _err and "50,000 acres" in _err and "18.6 times" in _err
    assert "openet-area-cap.md" in _err

    # Under the cap, the recorded ensemble answers: twelve months, the
    # statistic named as a MAD-filtered mean rather than a median.
    _code, _out, _err, oe = run("huc12_capitol_creek.geojson", source="openet",
                                response="openet_ensemble_huc12_capitol_creek_2023.json", name="oe")
    assert _code == 0, _err
    assert oe["interval"] == "monthly" and len(oe["monthly"]) == 12
    assert "median absolute deviation" in oe["ensemble_statistic"] and "mean" in oe["ensemble_statistic"]
    assert oe["area"]["per_request_cap_acres"] == 50000
    assert abs(oe["area"]["polygon_acres"] - 23520) < 20
    assert abs(oe["total"]["mm"] - 724.60) < 0.01
    return (oe,)


@app.cell
def _(oe, run):
    # 6. The monthly series repeats January's value in February and March
    #    2023, the loader says so, and the daily ensemble over the same
    #    polygon and months disagrees with the monthly one by a third.
    _code, _out, _err, _ = run("huc12_capitol_creek.geojson", source="openet",
                               response="openet_ensemble_huc12_capitol_creek_2023.json", name="rep")
    assert "REPEATED VALUE" in _out and "2023-02, 2023-03" in _out
    assert "openet-monthly-not-the-daily-sum.md" in _out

    _code, _out, _err, day = run("huc12_capitol_creek.geojson", source="openet",
                                 response="openet_ensemble_huc12_capitol_creek_2023q1_daily.json", name="day")
    assert _code == 0, _err
    assert day["interval"] == "daily"
    _d = {m["month"]: m for m in day["monthly"]}
    assert [_d[k]["days_summed"] for k in ("2023-01", "2023-02", "2023-03")] == [31, 28, 31]
    for _k, _v in {"2023-01": 11.154, "2023-02": 20.853, "2023-03": 32.625}.items():
        assert abs(_d[_k]["mm"] - _v) < 0.01, (_k, _d[_k])
    _m = {m["month"]: m["mm"] for m in oe["monthly"]}
    assert _m["2023-01"] == _m["2023-02"] == _m["2023-03"] == 28.411
    _q1_monthly = sum(_m[k] for k in ("2023-01", "2023-02", "2023-03"))
    assert abs(_q1_monthly / day["total"]["mm"] - 1.319) < 0.005
    return


@app.cell
def _(oe, rf, run):
    # 7. The sub-cap consistency check the dataset concept records: MOD16
    #    against the OpenET ensemble over the one fixture unit small
    #    enough for the service, calendar 2023.
    _code, _out, _err, cc = run("huc12_capitol_creek.geojson",
                                ["mod16a2gf_roaring_fork_2023.nc"], name="cc")
    assert _code == 0, _err
    assert cc["coverage"]["cells_inside"] == 438
    assert abs(cc["total"]["mm"] - 521.12) < 0.01
    assert abs(cc["total"]["mm"] / oe["total"]["mm"] - 0.7192) < 0.001
    # Without the three suspect months the disagreement widens, so it is
    # not an artifact of them.
    _skip = ("2023-01", "2023-02", "2023-03")
    _m16 = sum(m["mm"] for m in cc["monthly"] if m["month"] not in _skip)
    _oet = sum(m["mm"] for m in oe["monthly"] if m["month"] not in _skip)
    assert abs(_m16 - 436.06) < 0.01 and abs(_oet - 639.37) < 0.01
    assert abs(_m16 / _oet - 0.682) < 0.001
    # And the sub-unit is not the basin: the Roaring Fork's own annual
    # mean differs from this unit's by more than five per cent.
    assert abs(cc["total"]["mm"] - rf["total"]["mm"]) > 0.05 * rf["total"]["mm"]
    return


@app.cell
def _(run):
    # 8. Refusals that keep a series honest: a window file that is not
    #    MOD16, and a basin that does not meet its window.
    _code, _out, _err, _ = run("huc12_capitol_creek.geojson",
                               ["mod16a2gf_lake_powell_2023.nc"], name="miss")
    assert _code == 2 and "no window cell centre falls inside the polygon" in _err

    _code, _out, _err, _ = run("usgs_09085000_nldi.geojson",
                               ["mod16a2gf_roaring_fork_2023.nc", "mod16a2gf_roaring_fork_2023.nc"], name="dup")
    assert _code == 2 and "appears in two window files" in _err
    return


@app.cell
def _(sha):
    # 9. The fixtures are the bytes their provenance rows record.
    _expected = {
        "mod16a2gf_roaring_fork_2023.nc": "56cf0d569db0e6b9b37c4e6943a834af41ea9eaa66e11e9c4bd5415caa6ff0c2",
        "mod16a2gf_lake_powell_2023.nc": "3c6cac209a1a5e01a91c29f416aff9cb2e0d1559495f48d0118595fe0f19b192",
        "openet_ensemble_huc12_capitol_creek_2023.json": "c1db46a65bd36d34ad9803eaf230666c0d985ebdeaa5d7a6750cdf965b6419e1",
        "openet_ensemble_huc12_capitol_creek_2023q1_daily.json": "956daee71ab4767569c435044a95f2f13c671f3ee1ee9d558a4a096ce3dbfe00",
    }
    for _f, _h in _expected.items():
        assert sha(_f) == _h, f"{_f}: sha256 {sha(_f)[:12]} differs from the recorded {_h[:12]}"
    return


@app.cell
def _(et):
    # 10. No credential and no key anywhere in the fixtures, including
    #     the OpenET responses, whose requests they record.
    import json as _json
    import re as _re

    for _p in sorted(et.glob("*.json")):
        _text = _p.read_text()
        # Nothing with the shape of an API key: the OpenET key is 32 hex
        # characters, and the fixtures record the request without it.
        assert not _re.search(r"\b[0-9a-f]{32}\b", _text), f"{_p.name} holds something key-shaped"
        assert "Authorization:" not in _text
        _doc = _json.loads(_text)
        _prov = _doc["provenance"]
        assert "OPENET_API_KEY" in _prov["credential_note"] and "not in this file" in _prov["credential_note"]
        assert _prov["per_request_cap_acres"] == 50000 and _prov["polygon_acres"] < 50000
    return


if __name__ == "__main__":
    app.run()
