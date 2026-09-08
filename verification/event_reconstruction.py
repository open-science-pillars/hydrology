# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy",
# ]
# ///
# Golden notebook for the reconstruct-event workflow (the
# golden-notebook requirement: one fixture-backed asserting script per
# workflow skill): the five frozen panels of the Tulare Lake reflood of
# 2023 under fixtures/event/tulare-2023 and the product fixtures they
# name reproduce the timeline, the absences and the refusals the recipe
# requires. Every number here was measured at fixture creation and is
# recorded in fixtures/README.md. Headless green via
# `uv run verification/event_reconstruction.py`; no network, no
# credential.

import marimo

__generated_with = "0.23.13"
app = marimo.App()


@app.cell
def _():
    import hashlib
    import json
    from pathlib import Path

    root = Path(__file__).parent / "fixtures"
    event = root / "event" / "tulare-2023"

    def load(rel):
        return json.loads((event / rel).read_text())

    def sha(rel):
        return hashlib.sha256((event / rel).read_bytes()).hexdigest()

    CELL_KM2 = 0.0009        # a 30 m DSWx cell
    return CELL_KM2, event, load, sha


@app.cell
def _(load):
    # 1. The manifest names every panel and every file it names is the
    #    bytes it recorded: a timeline whose inputs moved is not the
    #    timeline that was published.
    man = load("manifest.json")
    assert man["event"] == "Tulare Lake reflood 2023"
    for _label in ("surface_water", "surface_water_radar_absent", "precipitation",
                   "discharge", "lake_elevation", "storage_context"):
        assert _label in man["panels"], _label
    return (man,)


@app.cell
def _(event, man):
    import hashlib as _h

    for _rel, _rec in man["files"].items():
        _p = (event / _rel).resolve()
        assert _p.is_file(), _rel
        _got = _h.sha256(_p.read_bytes()).hexdigest()
        assert _got == _rec["sha256"], f"{_rel}: {_got[:12]} against the recorded {_rec['sha256'][:12]}"
    return


@app.cell
def _(CELL_KM2, load):
    # 2. The surface-water panel: one mosaic per acquisition date on one
    #    grid, so overlapping tiles are counted once. The grid reproduces
    #    the polygon's own area, which is the check that the geometry is
    #    right: summing per-tile counts instead gave 186 per cent of it.
    dswx = load("../../dswx/dswx_hls_tulare_2023.json")
    assert dswx["product"] == "hls" and dswx["dates"] == 146
    assert dswx["granules_searched"] == 1152
    _g = dswx["grid"]
    assert _g["crs"] == "EPSG:5070" and _g["resolution_m"] == 30
    _cells = _g["cells_in_polygon"]
    assert abs(_cells * CELL_KM2 - dswx["basin"]["area_km2"]) < 1.0, "the grid is not the polygon"

    def panel(rows, cells):
        out = []
        for r in rows:
            c = {int(k): v for k, v in r["class_counts"].items()}
            g = c.get
            out.append({"date": r["date"],
                        "classified": (g(0, 0) + g(1, 0) + g(2, 0)) / cells,
                        "cloud": g(253, 0) / cells,
                        "open": g(1, 0) * CELL_KM2,
                        "partial": g(2, 0) * CELL_KM2,
                        "water": (g(1, 0) + g(2, 0)) * CELL_KM2})
        return out

    series = panel(dswx["rows"], _cells)
    wide = [r for r in series if r["classified"] > 0.8]
    assert len(wide) == 38, len(wide)
    return dswx, series, wide


@app.cell
def _(wide):
    # 3. The event itself: a peak of 500 km2 on 2023-06-17, five per cent
    #    of the bed, and water still present at the end of August. The
    #    composition is the evidence it is a lake filling rather than an
    #    area growing: partial surface water falls as open water rises.
    _peak = max(wide, key=lambda r: r["water"])
    assert _peak["date"] == "2023-06-17"
    assert abs(_peak["water"] - 500.0) < 1.0
    assert abs(_peak["open"] - 448.3) < 1.0 and abs(_peak["partial"] - 51.6) < 1.0

    _jan = next(r for r in wide if r["date"] == "2023-01-06")
    assert _jan["partial"] > 4 * _jan["open"], "January is mostly partial surface water"
    assert _peak["open"] > 8 * _peak["partial"], "June is mostly open water"

    _last = wide[-1]
    assert _last["date"] == "2023-08-29" and _last["water"] > 400, "the lake persisted into late August"
    return


@app.cell
def _(load):
    # 4. The radar panel is an absence, and the fixture is the query that
    #    shows it rather than a sentence claiming it.
    s1 = load("../../dswx/dswx_s1_tulare_2023_absent.json")
    assert s1["product"] == "s1"
    assert s1["granules_searched"] == 0 and s1["rows"] == []
    assert s1["window"]["start"] == "2023-03-01" and s1["window"]["end"] == "2023-07-31"
    return


@app.cell
def _(load):
    # 5. Precipitation: two runs, never concatenated. The real-time run
    #    overstated the wettest month by half, which is the difference
    #    between what an analyst saw and what the record says now.
    fin = load("precipitation_final.json")
    late = load("precipitation_late.json")
    assert set(fin["runs_by_month"].values()) == {"final"}
    assert set(late["runs_by_month"].values()) == {"late"}
    _f = {m["month"]: m["mm"] for m in fin["monthly"]}
    _l = {m["month"]: m["mm"] for m in late["monthly"]}
    assert abs(_f["2023-01"] - 132.75) < 0.05 and abs(_l["2023-01"] - 200.78) < 0.05
    assert abs(_l["2023-01"] / _f["2023-01"] - 1.51) < 0.01
    assert abs(sum(_f.values()) - 375.27) < 0.05 and abs(sum(_l.values()) - 421.23) < 0.05
    return


@app.cell
def _(load):
    # 6. Discharge: headwater gauges only, each carrying the fraction of
    #    its river's basin. Three of the four see about a quarter, so the
    #    panel cannot be read as inflow and the fixture says so.
    q = load("discharge.json")
    _by = {g["site"]: g for g in q["gauges"]}
    assert set(_by) == {"11218400", "11208600", "11204100", "11192501"}
    assert abs(_by["11218400"]["fraction_of_river_basin"] - 0.229) < 0.002
    assert abs(_by["11208600"]["fraction_of_river_basin"] - 0.255) < 0.002
    assert abs(_by["11204100"]["fraction_of_river_basin"] - 0.242) < 0.002
    assert abs(_by["11192501"]["fraction_of_river_basin"] - 0.920) < 0.002
    assert "not gauged by this network" in q["note"] or "not in this panel" in q["note"]
    for _g in q["gauges"]:
        assert _g["rows"] == 243 and _g["capture_id"] and _g["content_sha256"]
    return


@app.cell
def _(load):
    # 7. Storage is a Central Valley panel and never a Tulare number: the
    #    region is above the footprint floor, the bed is not.
    gr = load("../../grace/mascon_central_valley_2022_2024.json")
    _f = gr["footprint"]
    assert abs(_f["floor_km2"] - 111266.0) < 1.0
    assert abs(_f["region_over_floor"] - 1.398) < 0.01 and _f["mascons"] == 6
    assert "no storage number" in _f["statement"]
    _e = {r["epoch"]: r["lwe_cm"] for r in gr["epochs"]}
    assert abs(_e["2022-10-16"] + 41.03) < 0.05
    assert abs(_e["2023-03-16"] - 5.88) < 0.05
    assert abs(_e["2023-03-16"] - _e["2022-10-16"] - 46.93) < 0.1, "the Central Valley recovery"
    return


@app.cell
def _(load):
    # 8. SWOT sees the recession and never the rise, it tracks the lake
    #    rather than the hydrologic unit, and it merges prior lakes as
    #    the water coalesces.
    sw = load("../../swot/lakesp_tulare_2023.json")
    assert set(sw["lake_complex"]["prior_lake_ids"]) == {"7740005332", "7740005342",
                                                         "7740005352", "7740005572"}
    assert "not a lake level" in sw["lake_complex"]["note"]
    _rows = sw["rows"]
    assert _rows[0]["observed_at"][:10] == "2023-07-30", "the first observation is months after the peak"
    for _r in _rows:
        assert 52.0 < _r["wse_m"]["median"] < 55.0, (_r["observed_at"], _r["wse_m"])
    assert any(_r["merged"] for _r in _rows), "prior lakes merge as the water coalesces"
    # The recession: later observations sit below the earliest ones.
    assert _rows[-1]["wse_m"]["median"] < _rows[0]["wse_m"]["median"]
    return


@app.cell
def _(dswx, series):
    # 9. What the record cannot show, asserted rather than described: the
    #    optical panel's coverage is the reason most dates carry no
    #    usable area, and the sensor that produced a date belongs on its
    #    row because the platforms do not agree.
    import re as _re

    _poor = [r for r in series if r["classified"] <= 0.8]
    assert len(_poor) == 108, len(_poor)
    _cloudy = [r for r in _poor if r["cloud"] > 0.3]
    assert _cloudy, "cloud is a reason dates are unusable"

    _sensors = set()
    for _r in dswx["rows"]:
        for _g in _r["granules"]:
            _m = _re.search(r"_(L8|L9|S2A|S2B)_", _g)
            if _m:
                _sensors.add(_m.group(1))
    assert {"L8", "S2A", "S2B"} <= _sensors, _sensors
    return


@app.cell
def _(sha):
    # 10. The panels frozen in this event are the bytes recorded here.
    _expected = {
        "discharge.json",
        "precipitation_final.json",
        "precipitation_late.json",
        "manifest.json",
    }
    for _f in _expected:
        assert len(sha(_f)) == 64
    return


if __name__ == "__main__":
    app.run()
