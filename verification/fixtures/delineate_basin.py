# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "shapely>=2", "pyproj"]
# ///
"""Delineate a basin and freeze it as a fixture with its provenance.

Three ways in, two sources out:

  --gauge SITE          NLDI trace upstream of a USGS gauge (the gauge is
                        indexed to the network: comid, reach, measure)
  --point LON LAT       NLDI trace upstream of a point, which is snapped
                        to the network through the hydrolocation service
                        FIRST; if that service does not answer, this
                        script stops rather than guessing a flowline
  --huc CODE [CODE ...] a union of Watershed Boundary Dataset units
                        (2 to 12 digits, one level per call) from the
                        National Map WBD service; a set that contains a
                        closed-basin unit is reported as having no outlet

The polygon is written as GeoJSON to the fixture tree (default
verification/fixtures/basins/ beside this script) with a `provenance`
member: source, every request URL, the UTC date, the source version
(the NLDI navigation service has none beyond its host; a WBD unit
carries its loaddate and tnmid), and the sha256 of the geometry as
written. Area is computed in an equal-area projection (ESRI:102008,
North America Albers Equal Area Conic) and, for a gauge, compared with
the monitoring-locations `drainage_area` (total) with
`contributing_drainage_area` beside it where USGS publishes one.

Every fact this script relies on (hosts, the snap-first rule, the
comparison rule, the closed-basin vocabulary) is recorded in the
knowledge concepts under knowledge/connectors/nldi-basin.md,
knowledge/datasets/usgs-wbd.md and the two basin gotchas; this file
implements them and cites nothing it does not use.

No credential is sent to any host this script calls.

Usage:
  uv run verification/fixtures/delineate_basin.py --gauge 09085000
  uv run verification/fixtures/delineate_basin.py --point -107.3308 39.5467 --name roaring_fork_point
  uv run verification/fixtures/delineate_basin.py --huc 18030012 --name tulare_lake_bed
  uv run verification/fixtures/delineate_basin.py --gauge 09380000 --split   # splitCatchment=true
  uv run verification/fixtures/delineate_basin.py --gauge 09085000 --full    # simplified=false
"""
import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

import requests
from pyproj import Geod, Transformer
from shapely.geometry import mapping, shape
from shapely.ops import transform, unary_union

NLDI = "https://api.water.usgs.gov/nldi/linked-data"
ML = "https://api.waterdata.usgs.gov/ogcapi/v0/collections/monitoring-locations/items"
WBD = "https://hydro.nationalmap.gov/arcgis/rest/services/wbd/MapServer"
WBD_LAYER = {2: 1, 4: 2, 6: 3, 8: 4, 10: 5, 12: 6}
KM2_PER_MI2 = 2.589988110336
EQUAL_AREA = "ESRI:102008"
TIMEOUT = 300

_tf = Transformer.from_crs("EPSG:4326", EQUAL_AREA, always_xy=True)


def area_km2(geom) -> float:
    return transform(_tf.transform, geom).area / 1e6


def get(url: str, params: dict | None = None) -> tuple[requests.Response, str]:
    r = requests.get(url, params=params, timeout=TIMEOUT, headers={"accept": "application/json"})
    return r, r.url


def fail(msg: str) -> None:
    print(f"delineate_basin: {msg}", file=sys.stderr)
    sys.exit(1)


def nldi_error(r: requests.Response, what: str) -> None:
    try:
        body = r.json()
        detail = f"{body.get('title')}: {body.get('detail')} (upstream_status {body.get('upstream_status')})"
    except ValueError:
        detail = r.text[:200]
    fail(f"{what} returned {r.status_code}; {detail}. Nothing was traced and nothing was written.")


def monitoring_location(site: str) -> dict:
    r, url = get(ML, {"id": f"USGS-{site}", "f": "json"})
    feats = r.json().get("features", []) if r.status_code == 200 else []
    if not feats:
        fail(f"monitoring-locations has no record for USGS-{site} (status {r.status_code})")
    p = feats[0]["properties"]
    return {"request": url, "name": p["monitoring_location_name"],
            "hydrologic_unit_code": p["hydrologic_unit_code"],
            "drainage_area_mi2": p["drainage_area"],
            "contributing_drainage_area_mi2": p["contributing_drainage_area"],
            "coordinates": feats[0]["geometry"]["coordinates"]}


def trace_gauge(site: str, split: bool, simplified: bool) -> tuple[object, dict]:
    r, url = get(f"{NLDI}/nwissite/USGS-{site}")
    if r.status_code != 200 or not r.json().get("features"):
        nldi_error(r, f"NLDI nwissite lookup for USGS-{site}")
    p = r.json()["features"][0]["properties"]
    index = {"comid": p["comid"], "reachcode": p["reachcode"], "measure": p["measure"], "request": url}
    r2, url2 = get(f"{NLDI}/nwissite/USGS-{site}/basin",
                   {"splitCatchment": str(split).lower(), "simplified": str(simplified).lower()})
    if r2.status_code != 200:
        nldi_error(r2, f"NLDI basin for USGS-{site} (splitCatchment={str(split).lower()})")
    geom = shape(r2.json()["features"][0]["geometry"])
    return geom, {"source": "NLDI basin upstream of an indexed USGS gauge",
                  "site": f"USGS-{site}", "index": index, "splitCatchment": split, "simplified": simplified,
                  "requests": [url, url2]}


def trace_point(lon: float, lat: float, split: bool, simplified: bool) -> tuple[object, dict]:
    r, url = get(f"{NLDI}/hydrolocation", {"coords": f"POINT({lon} {lat})"})
    if r.status_code != 200 or not r.json().get("features"):
        nldi_error(r, "NLDI hydrolocation (the snap of the point to the network)")
    hits = [f for f in r.json()["features"] if f["properties"].get("type") == "hydrolocation"]
    if not hits or not hits[0]["properties"].get("comid"):
        fail("hydrolocation answered without a snapped location; the point did not snap to a flowline")
    p = hits[0]["properties"]
    snapped = hits[0]["geometry"]["coordinates"]
    comid = p["comid"]
    # The snap is to the NEAREST flowline, which need not be the river the
    # user meant; the distance and the reach's subbasin (the first eight
    # digits of the reachcode) are what lets the caller check.
    snap_m = Geod(ellps="WGS84").inv(lon, lat, snapped[0], snapped[1])[2]
    snap = {"comid": comid, "reachcode": p.get("reachcode"), "measure": p.get("measure"),
            "snapped_coordinates": snapped, "snap_distance_m": round(snap_m, 1),
            "subbasin": (p.get("reachcode") or "")[:8], "request": url}
    r2, url2 = get(f"{NLDI}/comid/{comid}/basin",
                   {"splitCatchment": str(split).lower(), "simplified": str(simplified).lower()})
    if r2.status_code != 200:
        nldi_error(r2, f"NLDI basin for comid {comid}")
    geom = shape(r2.json()["features"][0]["geometry"])
    return geom, {"source": "NLDI basin upstream of a point snapped through hydrolocation",
                  "point": [lon, lat], "snap": snap, "splitCatchment": split, "simplified": simplified,
                  "requests": [url, url2]}


def wbd_union(codes: list[str]) -> tuple[object, dict]:
    lengths = {len(c) for c in codes}
    if len(lengths) != 1 or next(iter(lengths)) not in WBD_LAYER:
        fail(f"hydrologic unit codes must share one length in {sorted(WBD_LAYER)}; got {codes}")
    n = next(iter(lengths)); layer = WBD_LAYER[n]; field = f"huc{n}"
    where = f"{field} IN ({','.join(repr(c) for c in codes)})"
    fields = [field, "name", "areasqkm", "loaddate", "tnmid"] + (["tohuc", "hutype"] if n >= 10 else [])
    r, url = get(f"{WBD}/{layer}/query", {"where": where, "outFields": ",".join(fields),
                                           "returnGeometry": "true", "outSR": "4326", "f": "geojson"})
    if r.status_code != 200 or "features" not in r.json():
        fail(f"WBD service layer {layer} returned {r.status_code}: {r.text[:200]}")
    feats = r.json()["features"]
    found = {f["properties"][field] for f in feats}
    missing = sorted(set(codes) - found)
    if missing:
        fail(f"WBD layer {layer} has no unit for {missing}")
    geom = unary_union([shape(f["geometry"]) for f in feats])
    units = []
    for f in sorted(feats, key=lambda f: f["properties"][field]):
        p = f["properties"]
        u = {"code": p[field], "name": p["name"], "areasqkm": p["areasqkm"],
             "loaddate": dt.datetime.fromtimestamp(p["loaddate"] / 1000, dt.UTC).strftime("%Y-%m-%d"),
             "tnmid": p["tnmid"]}
        if n >= 10:
            u["tohuc"] = p.get("tohuc"); u["hutype"] = p.get("hutype")
        units.append(u)
    requests_made = [url]
    # The outlet question is answered at the 12-digit level, where each
    # unit names the unit it drains to (`tohuc`) or `CLOSED BASIN`; for a
    # coarser code the member subwatersheds are listed without geometry.
    if n >= 10:
        members = [{"huc12": u["code"], "tohuc": u.get("tohuc"), "hutype": u.get("hutype")} for u in units]
    else:
        like = " OR ".join(f"huc12 LIKE '{c}%'" for c in codes)
        r2, url2 = get(f"{WBD}/6/query", {"where": like, "outFields": "huc12,tohuc,hutype",
                                          "returnGeometry": "false", "f": "json"})
        if r2.status_code != 200 or "features" not in r2.json():
            fail(f"WBD service layer 6 returned {r2.status_code}: {r2.text[:200]}")
        members = [f["attributes"] for f in r2.json()["features"]]
        requests_made.append(url2)
    inside = {m["huc12"] for m in members}
    closed = sorted(m["huc12"] for m in members if m.get("hutype") == "C" or m.get("tohuc") == "CLOSED BASIN")
    downstream = sorted({m["tohuc"] for m in members if m.get("tohuc") and m["tohuc"] not in inside and m["tohuc"] != "CLOSED BASIN"})
    outlet = {"drains_to": downstream, "closed_basin_units": closed,
              "no_outlet": bool(closed) and not downstream, "member_huc12_count": len(members)}
    return geom, {"source": "Watershed Boundary Dataset union (National Map WBD service)",
                  "layer": layer, "field": field, "units": units,
                  "version": {"loaddate_max": max(u["loaddate"] for u in units),
                              "tnmids": [u["tnmid"] for u in units]},
                  "outlet": outlet, "requests": requests_made}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--gauge", metavar="SITE", help="USGS site number as a string, leading zeros kept")
    g.add_argument("--point", nargs=2, type=float, metavar=("LON", "LAT"))
    g.add_argument("--huc", nargs="+", metavar="CODE")
    ap.add_argument("--split", action="store_true", help="NLDI splitCatchment=true (split the local catchment at the feature)")
    ap.add_argument("--full", action="store_true", help="NLDI simplified=false (the service simplifies by default; the effect on area is recorded in the connector concept)")
    ap.add_argument("--compare", metavar="SITE", help="compare a point or WBD polygon with this gauge's drainage_area")
    ap.add_argument("--name", help="fixture name (default derived from the input)")
    ap.add_argument("--out", type=Path, default=Path(__file__).parent / "basins",
                    help="directory for <name>.geojson, or a file path ending in .geojson")
    a = ap.parse_args()

    if a.gauge:
        site = a.gauge
        geom, prov = trace_gauge(site, a.split, not a.full)
        name = a.name or f"usgs_{site}_nldi{'_split' if a.split else ''}"
    elif a.point:
        site = a.compare
        geom, prov = trace_point(a.point[0], a.point[1], a.split, not a.full)
        name = a.name or f"point_{a.point[0]:.4f}_{a.point[1]:.4f}_nldi"
    else:
        site = a.compare
        geom, prov = wbd_union(a.huc)
        name = a.name or f"wbd_{'_'.join(a.huc)}"

    geometry = mapping(geom)
    canonical = json.dumps(geometry, sort_keys=True, separators=(",", ":")).encode()
    sha = hashlib.sha256(canonical).hexdigest()
    km2 = area_km2(geom)
    prov.update({"date": dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
                 "geometry_sha256": sha, "geometry_type": geometry["type"],
                 "area_km2": round(km2, 1), "area_projection": EQUAL_AREA})

    comparison = None
    if site:
        ml = monitoring_location(site)
        da = ml["drainage_area_mi2"]; cda = ml["contributing_drainage_area_mi2"]
        comparison = {"site": f"USGS-{site}", "name": ml["name"], "request": ml["request"],
                      "drainage_area_mi2": da, "drainage_area_km2": round(da * KM2_PER_MI2, 1) if da else None,
                      "contributing_drainage_area_mi2": cda,
                      "contributing_drainage_area_km2": round(cda * KM2_PER_MI2, 1) if cda else None,
                      "polygon_vs_total_pct": round(100 * (km2 - da * KM2_PER_MI2) / (da * KM2_PER_MI2), 2) if da else None}
        prov["comparison"] = comparison

    if a.out.suffix == ".geojson":
        path = a.out
        name = a.name or path.stem
    else:
        path = a.out / f"{name}.geojson"
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = {"type": "FeatureCollection", "name": name, "provenance": prov,
           "features": [{"type": "Feature", "properties": {"name": name, "area_km2": round(km2, 1)}, "geometry": geometry}]}
    path.write_text(json.dumps(doc, separators=(",", ":")) + "\n")

    print(f"{name}: {geometry['type']}, {km2:,.1f} km2 in {EQUAL_AREA}, geometry sha256 {sha[:12]}, written {path}")
    if comparison and comparison["drainage_area_km2"]:
        c = comparison
        contrib = f"{c['contributing_drainage_area_km2']:,.1f} km2" if c["contributing_drainage_area_km2"] else "not published"
        print(f"  {c['site']} {c['name']}: drainage_area {c['drainage_area_mi2']:,} mi2 = {c['drainage_area_km2']:,.1f} km2 (total); "
              f"contributing {contrib}; polygon is {c['polygon_vs_total_pct']:+.2f}% of total")
    if prov.get("outlet") is not None:
        o = prov["outlet"]
        if o["no_outlet"]:
            print(f"  outlet: NONE; {len(o['closed_basin_units'])} of {o['member_huc12_count']} subwatersheds are closed-basin units "
                  f"({', '.join(o['closed_basin_units'])}) and none drains outside the set")
        else:
            print(f"  outlet: drains to {', '.join(o['drains_to'])}" + (f"; closed-basin units inside: {', '.join(o['closed_basin_units'])}" if o["closed_basin_units"] else ""))
    if prov.get("snap"):
        s = prov["snap"]
        print(f"  snapped {s['snap_distance_m']:,.0f} m to comid {s['comid']} reach {s['reachcode']} "
              f"(subbasin {s['subbasin']}) measure {s['measure']:.2f} at {s['snapped_coordinates']}; "
              f"confirm this is the river you meant before using the polygon")


if __name__ == "__main__":
    main()
