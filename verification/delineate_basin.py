# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "shapely>=2",
#     "pyproj",
# ]
# ///
# Golden notebook for the delineate-basin workflow (the golden-notebook
# requirement: one fixture-backed asserting script per workflow skill):
# the frozen basin polygons under fixtures/basins/ (three NLDI traces
# upstream of USGS gauges and one Watershed Boundary Dataset union, the
# terminal case) re-hash to their provenance, re-measure to their
# recorded equal-area areas, compare with the published drainage areas
# the way the connector concept says they should, and place each basin
# against the GRACE mascon footprint. Reference numbers measured at
# fixture creation and recorded in fixtures/README.md.
# Headless green via `uv run verification/delineate_basin.py`.

import marimo

__generated_with = "0.23.13"
app = marimo.App()


@app.cell
def _():
    import hashlib
    import json
    from pathlib import Path

    from pyproj import Transformer
    from shapely.geometry import shape
    from shapely.ops import transform

    root = Path(__file__).parent / "fixtures" / "basins"
    tf = Transformer.from_crs("EPSG:4326", "ESRI:102008", always_xy=True)

    def load(name):
        doc = json.loads((root / f"{name}.geojson").read_text())
        geometry = doc["features"][0]["geometry"]
        return doc["provenance"], geometry, shape(geometry)

    def area_km2(geom):
        return transform(tf.transform, geom).area / 1e6

    def sha(geometry):
        return hashlib.sha256(json.dumps(geometry, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    return area_km2, load, sha


@app.cell
def _(area_km2, load, sha):
    # 1. The three gauge basins: each polygon is the bytes its provenance
    #    hashes, each re-measures to the recorded area in the recorded
    #    equal-area projection, and each gauge is indexed to the network
    #    (comid, reach code, measure), which is what makes a gauge trace
    #    safe where a raw point is not.
    expected = {
        # name: (site, recorded km2, geometry type, comid)
        "usgs_03611500_nldi": ("USGS-03611500", 522879.1, "MultiPolygon", 1840007),
        "usgs_09380000_nldi": ("USGS-09380000", 276443.7, "MultiPolygon", 20733845),
        "usgs_09085000_nldi": ("USGS-09085000", 3767.1, "Polygon", 1324997),
    }
    basins = {}
    for bname, (site, km2_ref, gtype, comid) in expected.items():
        bprov, bgeometry, bgeom = load(bname)
        assert bprov["site"] == site and bprov["source"].startswith("NLDI basin upstream of an indexed")
        assert bprov["splitCatchment"] is False, "the frozen traces are whole-catchment (splitCatchment=false)"
        assert sha(bgeometry) == bprov["geometry_sha256"], f"{bname}: geometry differs from its provenance hash"
        assert bgeometry["type"] == gtype
        assert bprov["index"]["comid"] == comid and bprov["index"]["reachcode"] and bprov["index"]["measure"] is not None
        assert bprov["area_projection"] == "ESRI:102008"
        bkm2 = area_km2(bgeom)
        assert abs(bkm2 - km2_ref) / km2_ref < 1e-4, f"{bname}: {bkm2:.1f} km2, recorded {km2_ref}"
        assert abs(bkm2 - bprov["area_km2"]) < 0.1
        basins[bname] = (bprov, bkm2)
    return basins


@app.cell
def _(basins):
    # 2. The comparison rule: an NLDI trace is the network-connected area,
    #    so it sits at or slightly below the published total drainage
    #    area; USGS publishes no contributing area for these three, and
    #    the fixture says so rather than inventing one. Lees Ferry is the
    #    marginal case on purpose: the 4.5% shortfall is the closed basins
    #    the total counts and the network cannot reach.
    KM2_PER_MI2 = 2.589988110336
    tolerance = {  # per basin, from the measured differences, not a universal number
        "usgs_03611500_nldi": (-1.0, 0.5),
        "usgs_09380000_nldi": (-5.0, -4.0),
        "usgs_09085000_nldi": (-0.5, 0.5),
    }
    for cname, (cprov, ckm2) in basins.items():
        c = cprov["comparison"]
        assert c["contributing_drainage_area_mi2"] is None, "USGS publishes no contributing area for these gauges"
        total_km2 = c["drainage_area_mi2"] * KM2_PER_MI2
        assert abs(total_km2 - c["drainage_area_km2"]) < 0.1
        pct = 100 * (ckm2 - total_km2) / total_km2
        lo, hi = tolerance[cname]
        assert lo <= pct <= hi, f"{cname}: polygon is {pct:+.2f}% of the published total, outside [{lo}, {hi}]"
    lees = basins["usgs_09380000_nldi"]
    assert lees[0]["comparison"]["drainage_area_mi2"] == 111800.0
    assert 13000 < 111800.0 * KM2_PER_MI2 - lees[1] < 13300, "the closed-basin shortfall at Lees Ferry is about 13,100 km2"
    return


@app.cell
def _(basins):
    # 3. The mascon footprint: 4,551 equal-area 3-degree caps over the
    #    Earth's surface (the product page for the JPL mascon solution)
    #    is 1.121e5 km2 per mascon. Ohio clears it with margin, Lees
    #    Ferry is marginal, the Roaring Fork is far below it: the three
    #    cases a footprint floor has to tell apart.
    mascon_km2 = 5.10072e8 / 4551
    assert abs(mascon_km2 - 1.121e5) / 1.121e5 < 1e-3
    multiples = {mname: mkm2 / mascon_km2 for mname, (_, mkm2) in basins.items()}
    assert 4.6 < multiples["usgs_03611500_nldi"] < 4.7
    assert 2.4 < multiples["usgs_09380000_nldi"] < 2.5
    assert multiples["usgs_09085000_nldi"] < 0.05
    return


@app.cell
def _(area_km2, load, sha):
    # 4. The terminal basin: the Tulare Lake Bed subbasin (HUC8 18030012)
    #    from the Watershed Boundary Dataset carries its version (the
    #    unit's loaddate and tnmid), re-hashes and re-measures, and its
    #    subwatersheds include closed-basin units with none draining
    #    outside the set: no outlet, so no outlet gauge, and the outflow
    #    term of a balance is zero by definition rather than missing.
    tprov, tgeometry, tgeom = load("tulare_lake_bed_wbd")
    assert tprov["source"].startswith("Watershed Boundary Dataset union")
    assert sha(tgeometry) == tprov["geometry_sha256"]
    assert tprov["units"][0]["code"] == "18030012" and tprov["units"][0]["name"] == "Tulare Lake Bed"
    assert tprov["version"]["loaddate_max"] == "2024-08-16" and tprov["version"]["tnmids"][0].startswith("{")
    tkm2 = area_km2(tgeom)
    assert abs(tkm2 - 9808.2) < 1.0, f"Tulare Lake Bed re-measures to {tkm2:.1f} km2"
    assert abs(tkm2 - tprov["units"][0]["areasqkm"]) / tkm2 < 1e-4, "the equal-area measure agrees with the WBD's own areasqkm"
    o = tprov["outlet"]
    assert o["no_outlet"] is True and o["drains_to"] == []
    assert o["member_huc12_count"] == 102 and len(o["closed_basin_units"]) == 4
    assert all(u.startswith("1803001224") for u in o["closed_basin_units"])
    return


if __name__ == "__main__":
    app.run()
