# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "requests", "shapely>=2"]
# ///
"""Freeze a basin's SNODAS snow water equivalent for a set of dates, from
the directory the data actually lives in.

There is no catalog route. The collection is registered (G02158,
C1386246263-NSIDCV0, DOI 10.7265/N5TB14TC) with a temporal extent that
claims coverage to the present, and a granule search returns nothing for
any window, including no window at all. The files are served directly
by NSIDC over plain HTTPS with no credential, as a dated path under a
browsable directory. So this fetcher builds a URL from a date; it does
not search, and nothing here reaches for earthaccess.

What is frozen and why it is a basin mean rather than the grid: one
daily tar is 20 to 30 MB in the snow season and holds eight products on
a 6,935 by 3,351 grid at 1 km. A snow panel needs the basin's mean and
covered fraction per date, which is a handful of numbers. The tar is
read in memory, the snow water equivalent layer is clipped to the
polygon, and the tar is discarded; the fixture records the URL, the
file's own size and sha256, the layer's header description and scale,
and the counts behind the mean, so every number can be recomputed from
bytes that can be refetched while the directory stands.

The scale and the description are read from the header file packed
beside each layer rather than inferred from the file name, because the
name codes are not self-describing: 11038 is an average temperature and
11044 is melt, which their codes do not say.

This is a qualitative panel. The producer's guidance is that the
product is a model output and is not recommended for quantitative water
budget analysis, while comparing sums over an area between periods is
reasonable. Nothing here is a budget term, and the concepts say so.

Usage:
  uv run verification/fixtures/fetch_snodas_fixtures.py \
      --basin verification/fixtures/basins/usgs_09380000_nldi.geojson \
      --dates 2020-10-01:2021-09-01:MS --label lees_ferry_wy2021 \
      --out verification/fixtures/snodas
"""
import argparse
import datetime as dt
import gzip
import hashlib
import io
import json
import sys
import tarfile

import numpy as np
import requests
from shapely.geometry import Point, shape
from shapely.prepared import prep
from pathlib import Path

BASE = "https://noaadata.apps.nsidc.org/NOAA/G02158"
UA = {"User-Agent": "open-science-pillars-hydrology/0.6 (fixture fetch)"}
SWE_CODE = "11034"          # modeled snow water equivalent, total of snow layers
MONTHS = ["01_Jan", "02_Feb", "03_Mar", "04_Apr", "05_May", "06_Jun",
          "07_Jul", "08_Aug", "09_Sep", "10_Oct", "11_Nov", "12_Dec"]


def log(m):
    print(m, file=sys.stderr, flush=True)


def url_for(date: dt.date, tree="masked"):
    stem = "SNODAS" if tree == "masked" else "SNODAS_unmasked"
    return f"{BASE}/{tree}/{date.year}/{MONTHS[date.month - 1]}/{stem}_{date:%Y%m%d}.tar"


def parse_header(text):
    d = {}
    for line in text.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            d[k.strip()] = v.strip()
    return d


def read_layer(tar_bytes, code):
    """The named layer's array and its own header, from the tar in memory."""
    with tarfile.open(fileobj=io.BytesIO(tar_bytes)) as t:
        names = t.getnames()
        dat = next(n for n in names if code in n and n.endswith(".dat.gz"))
        txt = next(n for n in names if code in n and n.endswith(".txt.gz"))
        hdr = parse_header(gzip.decompress(t.extractfile(txt).read()).decode("latin-1"))
        raw = gzip.decompress(t.extractfile(dat).read())
    rows, cols = int(hdr["Number of rows"]), int(hdr["Number of columns"])
    a = np.frombuffer(raw, dtype=">i2").reshape(rows, cols)
    return a, hdr


def grid_axes(hdr):
    """Cell centres from the header's own corner and step."""
    rows, cols = int(hdr["Number of rows"]), int(hdr["Number of columns"])
    x0 = float(hdr["Minimum x-axis coordinate"])
    y1 = float(hdr["Maximum y-axis coordinate"])
    dx = float(hdr.get("X-axis resolution", 0.008333333333333)) or 0.008333333333333
    dy = float(hdr.get("Y-axis resolution", 0.008333333333333)) or 0.008333333333333
    lon = x0 + (np.arange(cols) + 0.5) * dx
    lat = y1 - (np.arange(rows) + 0.5) * dy
    return lat, lon


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--basin", required=True, type=Path)
    ap.add_argument("--dates", required=True,
                    help="START:END:MS for the first of each month, or a comma separated list")
    ap.add_argument("--label", required=True)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--tree", default="masked", choices=["masked", "unmasked"])
    a = ap.parse_args()

    doc = json.loads(a.basin.read_text())
    geom = doc["features"][0]["geometry"]
    poly = shape(geom)
    prov = doc.get("provenance", {})
    gsha = hashlib.sha256(json.dumps(geom, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    if ":MS" in a.dates:
        s, e, _ = a.dates.split(":")
        d0 = dt.date.fromisoformat(s)
        d1 = dt.date.fromisoformat(e)
        dates, cur = [], dt.date(d0.year, d0.month, 1)
        while cur <= d1:
            if cur >= d0:
                dates.append(cur)
            cur = dt.date(cur.year + (cur.month == 12), (cur.month % 12) + 1, 1)
    else:
        dates = [dt.date.fromisoformat(x) for x in a.dates.split(",")]

    a.out.mkdir(parents=True, exist_ok=True)
    inside = None
    rows, total_bytes = [], 0
    for d in dates:
        u = url_for(d, a.tree)
        r = requests.get(u, timeout=600, headers=UA)
        if r.status_code != 200:
            rows.append({"date": d.isoformat(), "url": u, "status": r.status_code,
                         "note": "no file at this path on this date"})
            log(f"  {d} {r.status_code}")
            continue
        total_bytes += len(r.content)
        arr, hdr = read_layer(r.content, SWE_CODE)
        if inside is None:
            lat, lon = grid_axes(hdr)
            mlon, mlat = np.meshgrid(lon, lat)
            w, s, e, n = poly.bounds
            box = (mlon >= w) & (mlon <= e) & (mlat >= s) & (mlat <= n)
            pp = prep(poly)
            inside = np.zeros(arr.shape, bool)
            idx = np.argwhere(box)
            for i, j in idx:
                if pp.contains(Point(mlon[i, j], mlat[i, j])):
                    inside[i, j] = True
            log(f"grid {arr.shape}, {int(box.sum())} cells in the bounding box, "
                f"{int(inside.sum())} inside the polygon")
        nodata = float(hdr["No data value"])
        scale = float(hdr["Data units"].split("/")[-1]) if "/" in hdr["Data units"] else 1.0
        vals = arr[inside].astype("float64")
        good = vals != nodata
        mm = vals[good] / scale * 1000.0 if "Meters" in hdr["Data units"] else vals[good] / scale
        rows.append({
            "date": d.isoformat(), "url": u, "status": 200,
            "bytes": len(r.content), "sha256": hashlib.sha256(r.content).hexdigest(),
            "cells_inside": int(inside.sum()), "cells_with_data": int(good.sum()),
            "swe_mean_mm": round(float(mm.mean()), 4) if good.any() else None,
            "swe_max_mm": round(float(mm.max()), 4) if good.any() else None,
            "cells_with_snow": int((mm > 0).sum()) if good.any() else 0,
        })
        log(f"  {d} {len(r.content)/1e6:.1f} MB  mean {rows[-1]['swe_mean_mm']} mm  "
            f"snow-covered {rows[-1]['cells_with_snow']}/{rows[-1]['cells_with_data']}")

    hdr_public = {k: hdr[k] for k in ("Description", "Data units", "Data type",
                                      "Number of columns", "Number of rows", "No data value")
                  if k in hdr}
    out = {
        "product": "SNODAS (NOAA NOHRSC), distributed by NSIDC as G02158",
        "collection_concept_id": "C1386246263-NSIDCV0",
        "doi": "10.7265/N5TB14TC",
        "route": {"kind": "direct HTTPS, no credential, no catalog search",
                  "base": BASE, "tree": a.tree,
                  "path_form": f"{BASE}/{a.tree}/YYYY/MM_Mon/SNODAS_YYYYMMDD.tar",
                  "note": ("a granule search on the collection returns zero results for any "
                           "window, so a catalog route does not exist and an agent that "
                           "searches concludes the data is missing")},
        "layer": {"code": SWE_CODE, "header": hdr_public,
                  "note": ("the description and the scale are read from the header packed "
                           "beside the layer, because the file name codes are not "
                           "self-describing")},
        "quantitative_use": ("the producer's guidance is that this is a model output and is "
                             "not recommended for quantitative water budget analysis, while "
                             "summing over an area between periods for comparison is "
                             "reasonable; nothing here is a budget term"),
        "basin": {"fixture": a.basin.name, "geometry_sha256": gsha,
                  "area_km2": prov.get("area_km2"), "site": prov.get("site", "")},
        "label": a.label,
        "dates": len(rows),
        "bytes_transferred": total_bytes,
        "retrieved": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "fetch_script": "verification/fixtures/fetch_snodas_fixtures.py",
        "license": "NSIDC distribution, US Government work",
        "rows": rows,
    }
    p = a.out / f"snodas_swe_{a.label}.json"
    p.write_text(json.dumps(out, indent=1))
    log(f"{p}: {len(rows)} dates, {total_bytes/1e6:.0f} MB read, {p.stat().st_size/1e3:.1f} kB")


if __name__ == "__main__":
    main()
