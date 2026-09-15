# /// script
# requires-python = ">=3.11"
# dependencies = ["shapely>=2,<3", "numpy>=1.26,<3"]
# ///
"""Freeze the groundwater term beside an existing water-balance tree:
a new tree that copies the frozen files byte for byte and adds
groundwater.json, the well set behind the water-table fluctuation
term, with its parameters and their sources.

What is frozen. The daily mean depth to water (USGS parameter 72019,
statistic 00003, feet below land surface) at every well the captures
hold, over the tree's window, read out of captures taken with core's
obs_capture.py (the same tool the discharge term comes through, so
every series carries a capture id and a content hash); the site file
of every well from the monitoring-locations collection (the aquifer,
its type, the constructed depth, the altitude and its datum); the
selection that produced the well set, re-run here so the counts are
recorded with the date; and the parameters the executor binds: the
specific yield with its uncertainty and its source, the averaging
window at each end of the window, the completeness rule, the
clustering radius that turns a well field into one site, and the
smallest site count the term is computed on.

What is not decided here. The executor computes the term from these
files; this script records inputs and parameters and computes
nothing that the receipt reports. The screened interval of a well is
not served by the Water Data API; the constructed depth is the depth
the site file states, and the receipt says so.

Usage:
  uv run verification/fixtures/water-balance/freeze_groundwater_term.py \
      --from-tree verification/fixtures/water-balance/ohio-olmsted \
      --name ohio-olmsted-groundwater --captures CAPTURE_STORE \
      --specific-yield 0.21 --specific-yield-sigma 0.03 \
      --specific-yield-source "..." --out verification/fixtures/water-balance
"""
import argparse
import datetime as dt
import hashlib
import json
import shutil
import urllib.parse
import urllib.request
from pathlib import Path

from shapely.geometry import Point, shape
from shapely.prepared import prep

USGS_API = "https://api.waterdata.usgs.gov/ogcapi/v0/collections"
PARAMETER = "72019"
STATISTIC = "00003"


def sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/json",
                                               "User-Agent": "osp-hydrology-freeze/0.1"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def site_records(ids: list[str]) -> dict[str, dict]:
    """The monitoring-locations record of every well, fetched in
    batches, with the request recorded beside the answer."""
    out = {}
    requests = []
    for i in range(0, len(ids), 40):
        url = (f"{USGS_API}/monitoring-locations/items?f=json&limit=100&id="
               + ",".join(ids[i:i + 40]))
        requests.append(url)
        for f in get_json(url)["features"]:
            p = f["properties"]
            x, y = f["geometry"]["coordinates"]
            out[p["id"]] = {**p, "lon": x, "lat": y}
    return out, requests


def selection_counts(poly, start: str, end: str):
    """The selection re-run for its counts: every daily 72019 mean
    series in the polygon's bounding box, those covering the window."""
    x0, y0, x1, y1 = poly.bounds
    url = (f"{USGS_API}/time-series-metadata/items?parameter_code={PARAMETER}&statistic_id={STATISTIC}"
           f"&bbox={x0:.2f},{y0:.2f},{x1:.2f},{y1:.2f}&limit=2000&skipGeometry=true&f=json")
    j = get_json(url)
    feats = j.get("features", [])
    covering = sorted({f["properties"]["monitoring_location_id"] for f in feats
                       if (f["properties"].get("begin") or "9") <= start
                       and (f["properties"].get("end") or "0") >= end})
    return {"request": url, "read_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "series_in_bbox": len(feats), "wells_covering_window": len(covering),
            "next_link": any(link.get("rel") == "next" for link in j.get("links", []))}, covering


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--from-tree", required=True, type=Path, help="the frozen tree the new one copies")
    ap.add_argument("--name", required=True, help="the new tree's name")
    ap.add_argument("--captures", required=True, type=Path, help="the capture store holding the well captures")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--specific-yield", required=True, type=float)
    ap.add_argument("--specific-yield-sigma", required=True, type=float)
    ap.add_argument("--specific-yield-source", required=True)
    ap.add_argument("--end-window-days", type=int, default=30,
                    help="the level at each end of the window is the mean over this many days inside it")
    ap.add_argument("--min-days-per-end", type=int, default=20,
                    help="a well with fewer daily values than this in either end window is excluded")
    ap.add_argument("--cluster-radius-km", type=float, default=2.0,
                    help="wells within this distance of one another are one site")
    ap.add_argument("--min-sites", type=int, default=3, help="the smallest site count the term is computed on")
    a = ap.parse_args()

    src_man = json.loads((a.from_tree / "manifest.json").read_text())
    start, end = src_man["window"]["start"], src_man["window"]["end"]
    basin = json.loads((a.from_tree / "basin.geojson").read_text())
    poly = shape(basin["features"][0]["geometry"])
    pp = prep(poly)

    # The captures: every usgs-dv capture of parameter 72019 in the store.
    captures = []
    series = {}
    for line in (a.captures / "manifest.jsonl").read_text().splitlines():
        row = json.loads(line)
        if row.get("source") != "usgs-dv" or row.get("params", {}).get("parameter_cd") != PARAMETER:
            continue
        if row["params"].get("start_date") != start or row["params"].get("end_date") != end:
            raise SystemExit(f"REFUSED: capture {row['capture_id']} is not over the tree's window {start} to {end}")
        body = json.loads((a.captures / f"{row['capture_id']}.canonical.json").read_text())
        sites = []
        for s in body:
            if s["parameter"] != PARAMETER or s["statistic"] != STATISTIC:
                continue
            series[s["site"]] = {"capture_id": row["capture_id"], "rows": s["rows"]}
            sites.append(s["site"])
        captures.append({"capture_id": row["capture_id"], "source": row["source"], "params": row["params"],
                         "captured_at": row.get("retrieved_at", row.get("captured_at")), "rows": row.get("rows"),
                         "pages": row.get("pages"), "tool_sha256": row.get("tool_sha256", ""),
                         "content_sha256": row.get("content_sha256"), "raw_sha256": row.get("raw_sha256"),
                         "tool": row.get("tool_version", row.get("tool", "")),
                         "request_url": row.get("request_url", ""), "sites": sorted(sites)})
    if not series:
        raise SystemExit("REFUSED: the capture store holds no daily 72019 series")

    ids = sorted(f"USGS-{s}" for s in series)
    records, site_requests = site_records(ids)
    selection, covering = selection_counts(poly, start, end)

    wells, excluded = [], []
    for sid in ids:
        rec = records.get(sid)
        if rec is None:
            excluded.append({"site": sid, "reason": "no monitoring-locations record"})
            continue
        reasons = []
        if not pp.contains(Point(rec["lon"], rec["lat"])):
            reasons.append("outside the basin polygon")
        if rec.get("aquifer_type_code") != "U":
            reasons.append(f"aquifer type {rec.get('aquifer_type_code')!r} is not unconfined")
        if not rec.get("well_constructed_depth"):
            reasons.append("no constructed depth in the site file")
        if reasons:
            excluded.append({"site": sid, "reason": "; ".join(reasons)})
            continue
        wells.append({
            "site": sid, "name": rec.get("monitoring_location_name"),
            "lat": rec["lat"], "lon": rec["lon"], "state": rec.get("state_name"), "county": rec.get("county_name"),
            "hydrologic_unit_code": rec.get("hydrologic_unit_code"),
            "site_type_code": rec.get("site_type_code"),
            "aquifer_code": rec.get("aquifer_code"), "national_aquifer_code": rec.get("national_aquifer_code"),
            "aquifer_type_code": rec.get("aquifer_type_code"),
            "well_constructed_depth_ft": rec.get("well_constructed_depth"),
            "hole_constructed_depth_ft": rec.get("hole_constructed_depth"),
            "altitude_ft": rec.get("altitude"), "altitude_datum": rec.get("vertical_datum"),
            "capture_id": series[sid.split("-", 1)[1]]["capture_id"],
            "rows": series[sid.split("-", 1)[1]]["rows"],
        })

    gw = {
        "term": "groundwater storage change by the water-table fluctuation method: specific yield times the "
                "mean change in water level over the well set, over the basin area",
        "parameter": PARAMETER, "statistic": STATISTIC, "unit": "ft below land surface",
        "window": {"start": start, "end": end},
        "route": "USGS Water Data API daily collection through core's obs_capture.py (the discharge term's "
                 "tool); the site file from the monitoring-locations collection; the candidate set from the "
                 "time-series-metadata collection. A continuously recorded well is a daily series through "
                 "usgs_daily rather than a field-measurements series, as the groundwater connector concept says",
        "selection": {
            **selection,
            "criteria": ["a daily mean series of parameter 72019 whose record begins on or before the window's "
                         "start and ends on or after its end",
                         "the well inside the basin polygon",
                         "aquifer type code U (unconfined) in the site file, because a confined well's head "
                         "change is not a storage change at specific yield",
                         "a constructed depth stated in the site file"],
            "wells_captured": len(ids), "wells_kept": len(wells), "wells_excluded": excluded,
            "site_file_requests": site_requests,
            "site_file_read_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
        "parameters": {
            "specific_yield": {"value": a.specific_yield, "sigma": a.specific_yield_sigma,
                               "source": a.specific_yield_source,
                               "applies_to": "unconfined wells only; the term is linear in this value and the "
                                             "receipt reports it at the value and at one sigma either side"},
            "end_window_days": a.end_window_days,
            "min_days_per_end": a.min_days_per_end,
            "cluster_radius_km": a.cluster_radius_km,
            "min_sites": a.min_sites,
            "sign": "depth to water decreasing is the water level rising: the level change is the first-window "
                    "mean depth minus the last-window mean depth, positive when storage rose",
        },
        "screened_interval_note": "the Water Data API serves the constructed depth and the hole depth of a well "
                                  "and not its screened interval; the depth stated for every well here is the "
                                  "constructed depth from the site file",
        "captures": captures,
        "wells": wells,
    }

    root = a.out / a.name
    root.mkdir(parents=True, exist_ok=True)
    files = {}
    for name, rec in src_man["files"].items():
        shutil.copyfile(a.from_tree / name, root / name)
        files[name] = {**rec, "copied_from": f"{a.from_tree}/{name}",
                       "copied_note": "byte for byte from the tree named, so the four terms are the same numbers"}
        assert sha256(root / name) == rec["sha256"], name
    (root / "groundwater.json").write_text(json.dumps(gw, separators=(",", ":"), sort_keys=False) + "\n")
    files["groundwater.json"] = {"sha256": sha256(root / "groundwater.json"),
                                 "kind": "well set for the groundwater term, from captures",
                                 "captures": [c["capture_id"] for c in captures],
                                 "content_sha256": [c["content_sha256"] for c in captures],
                                 "wells": len(wells)}
    manifest = {"basin": a.name, "window": {"start": start, "end": end},
                "frozen_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "frozen_by": "verification/fixtures/water-balance/freeze_groundwater_term.py",
                "from_tree": {"name": src_man["basin"], "frozen_at": src_man["frozen_at"],
                              "frozen_by": src_man["frozen_by"]},
                "files": files,
                "note": ("the executor reads this tree and nothing else; the four terms' files are the "
                         "originating tree's bytes, and groundwater.json adds the well set and the parameters "
                         "of the groundwater term with their sources")}
    (root / "manifest.json").write_text(json.dumps(manifest, indent=1))
    total = sum((root / f).stat().st_size for f in files)
    print(f"{root}: {len(files)} files, {total / 1e3:.1f} kB; {len(ids)} wells captured, {len(wells)} kept, "
          f"{len(excluded)} excluded; {selection['wells_covering_window']} candidates covered the window in the "
          f"bounding box")


if __name__ == "__main__":
    main()
