# /// script
# requires-python = ">=3.11"
# dependencies = ["earthaccess>=0.14", "numpy", "requests", "shapely>=2"]
# ///
"""Freeze a basin's SMAP L3 surface soil moisture for a window, one row
per day, through Cloud OPeNDAP subsets.

What is frozen and why it is a basin mean rather than the grid: a
granule is a global 406 by 964 EASE-Grid 2.0 field at 36 km, and a
water year of them is hundreds of megabytes for a basin that occupies a
few hundred cells. Each day is subset to the rows and columns covering
the basin, clipped to the polygon by cell centre, and reduced to the
mean, the spread and the counts behind them. The window indices, the
cell counts and each granule's identifier are recorded, so any row can
be recomputed from bytes that can be refetched.

Two things this keeps that a mean alone would hide. **Coverage moves.**
The retrieval is gappy: the swath does not cover every cell every day,
and cells that are frozen, snow-covered, densely vegetated or open
water are not retrieved at all. So a basin mean over a shrinking set of
cells is not the same quantity from day to day, and a winter mean in a
snowy basin can rest on a fraction of the basin. The count of retrieved
cells rides beside every mean, and the mean over a day whose coverage
is thin should be read as the mean of what was retrieved, not of the
basin. **The record is short.** SMAP begins 2015-03-31, which is not
long enough for a percentile against a climatology in the way a
century-long gauge record allows, and the concepts say so rather than
computing one.

The AM (descending) overpass is used, which is the one the retrieval is
validated for; the PM fields exist in the same file under the `_pm`
suffix and are not mixed in here.

Usage:
  uv run verification/fixtures/fetch_smap_fixtures.py \
      --basin verification/fixtures/basins/usgs_09380000_nldi.geojson \
      --start 2020-10-01 --end 2021-09-30 --label lees_ferry_wy2021 \
      --out verification/fixtures/smap
"""
import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

import earthaccess
import numpy as np
from shapely.geometry import Point, shape
from shapely.prepared import prep

COLLECTION = "C2938664585-NSIDC_CPRD"       # SPL3SMP v009
MAX_COORD_SCAN = 12                        # granules read to locate the grid
OPENDAP = "https://opendap.earthdata.nasa.gov/collections/{c}/granules/{g}"
GROUP = "Soil_Moisture_Retrieval_Data_AM"
FILL = -9999.0


def log(m):
    print(m, file=sys.stderr, flush=True)


def dap4(session, granule, expr):
    """One DAP4 constraint expression against one granule."""
    u = OPENDAP.format(c=COLLECTION, g=granule) + ".dap"
    r = session.get(u, params={"dap4.ce": expr}, timeout=300)
    r.raise_for_status()
    return r.content


def parse_dap4(body):
    """The values after the DMR. DAP4 frames the payload in chunks: a CRLF
    after the DMR, then per chunk one flags byte and a 24 bit big endian
    length, with bit 0 of the flags marking the last chunk and bit 2
    saying the payload is little endian."""
    i = body.find(b"</Dataset>")
    if i < 0:
        raise ValueError("no DMR in the DAP4 response")
    dmr = body[:i + len(b"</Dataset>")].decode("utf-8", "replace")
    rest = body[i + len(b"</Dataset>"):]
    p = 0
    while p < len(rest) and rest[p] in (0x0a, 0x0d):
        p += 1
    out = []
    while p + 4 <= len(rest):
        flags = rest[p]
        size = int.from_bytes(rest[p + 1:p + 4], "big")
        p += 4
        out.append(rest[p:p + size])
        p += size
        if flags & 0x01:
            break
    return dmr, b"".join(out)


DTYPES = {"Float32": "<f4", "Float64": "<f8", "Int16": "<i2", "UInt16": "<u2",
          "Int32": "<i4", "UInt32": "<u4", "Byte": "u1", "UInt8": "u1", "Int8": "i1"}


def unpack(dmr, raw, count):
    """Slice a DAP4 payload into its variables, by name.

    Two things make this less obvious than it looks. Each variable is
    followed by a four byte checksum, so a second variable read at the
    first one's length lands four bytes short. And the variables come
    back in the order the file declares them, not the order the
    constraint expression asked for: requesting latitude then longitude
    returns longitude first for this product, which silently swaps two
    arrays that are the same shape and dtype. So the order is read from
    the response's own DMR rather than assumed."""
    order = [(m.group(1), m.group(2))
             for m in re.finditer(r'<(' + "|".join(DTYPES) + r') name="([^"]+)">', dmr)]
    if not order:
        raise ValueError("no variables in the returned DMR")
    out, off = {}, 0
    for kind, name in order:
        a = np.frombuffer(raw, dtype=DTYPES[kind], count=count, offset=off)
        out[name] = a
        off += a.nbytes + 4
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--basin", required=True, type=Path)
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args()

    doc = json.loads(a.basin.read_text())
    geom = doc["features"][0]["geometry"]
    poly = shape(geom)
    prov = doc.get("provenance", {})
    gsha = hashlib.sha256(json.dumps(geom, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    auth = earthaccess.login(strategy="netrc")
    if not getattr(auth, "authenticated", False):
        auth = earthaccess.login()
    session = auth.get_session()

    granules = earthaccess.search_data(concept_id=COLLECTION, temporal=(a.start, a.end))
    log(f"{len(granules)} granules between {a.start} and {a.end}")
    if not granules:
        raise SystemExit("no granules in the window")

    # The grid is fixed but the coordinate arrays are not: latitude and
    # longitude are written only where that day retrieved something, so
    # one granule's coordinates describe one day's coverage rather than
    # the grid. Deriving a basin window from a single granule therefore
    # gives a window that depends on the weather of whichever day came
    # first, and two windows built from two different days are two
    # different cell sets whose means are not comparable. So the
    # coordinates are accumulated across granules until the mask stops
    # growing, which makes the window a property of the grid again.
    n = 406 * 964
    lat = np.full((406, 964), FILL)
    lon = np.full((406, 964), FILL)
    filled_before, scanned = -1, 0
    for g in granules[:MAX_COORD_SCAN]:
        dmr, raw = parse_dap4(dap4(session, g["umm"]["GranuleUR"],
                                   f"/{GROUP}/latitude;/{GROUP}/longitude"))
        c = unpack(dmr, raw, n)
        la = c["latitude"].reshape(406, 964).astype("float64")
        lo = c["longitude"].reshape(406, 964).astype("float64")
        take = (lat == FILL) & (la != FILL) & (lo != FILL)
        lat[take], lon[take] = la[take], lo[take]
        scanned += 1
        filled = int((lat != FILL).sum())
        if filled == filled_before:
            break
        filled_before = filled
    valid = (lat != FILL) & (lon != FILL)
    if valid.any() and not (-91 < lat[valid].min() < 91):
        raise SystemExit("the latitude array does not hold latitudes; the payload was misread")
    log(f"coordinates accumulated over {scanned} granules: {int(valid.sum())} cells located")
    w, s, e, nn = poly.bounds
    box = valid & (lon >= w) & (lon <= e) & (lat >= s) & (lat <= nn)
    if not box.any():
        raise SystemExit(
            f"REFUSED: no located cell falls in the basin's bounding box after scanning "
            f"{scanned} granules. The coordinate arrays are written only where a day "
            f"retrieved something, so this means the basin was not sampled at all in those "
            f"days rather than that the basin is outside the grid")
    r0, r1 = int(np.argwhere(box.any(1)).min()), int(np.argwhere(box.any(1)).max())
    c0, c1 = int(np.argwhere(box.any(0)).min()), int(np.argwhere(box.any(0)).max())
    pp = prep(poly)
    inside = np.zeros((r1 - r0 + 1, c1 - c0 + 1), bool)
    for i in range(r0, r1 + 1):
        for j in range(c0, c1 + 1):
            if valid[i, j] and pp.contains(Point(lon[i, j], lat[i, j])):
                inside[i - r0, j - c0] = True
    log(f"window rows {r0}:{r1} cols {c0}:{c1} ({inside.shape[0]} by {inside.shape[1]}), "
        f"{int(inside.sum())} cells inside the polygon")

    rows, nbytes = [], 0
    ce = (f"/{GROUP}/soil_moisture[{r0}:{r1}][{c0}:{c1}];"
          f"/{GROUP}/retrieval_qual_flag[{r0}:{r1}][{c0}:{c1}]")
    for k, g in enumerate(granules):
        ur = g["umm"]["GranuleUR"]
        day = g["umm"]["TemporalExtent"]["RangeDateTime"]["BeginningDateTime"][:10]
        try:
            body = dap4(session, ur, ce)
        except Exception as exc:
            rows.append({"date": day, "granule": ur, "error": str(exc)[:200]})
            log(f"  {day} ERROR {exc}")
            continue
        nbytes += len(body)
        dmr, raw = parse_dap4(body)
        m = inside.size
        got_vars = unpack(dmr, raw, m)
        sm = got_vars["soil_moisture"].reshape(inside.shape).astype("float64")
        qf = got_vars["retrieval_qual_flag"].reshape(inside.shape)
        got = inside & (sm != FILL)
        # bit 0 of the quality flag: the retrieval is recommended
        rec = got & ((qf & 1) == 0)
        v = sm[got]
        rows.append({
            "date": day, "granule": ur,
            "cells_inside": int(inside.sum()),
            "cells_retrieved": int(got.sum()),
            "cells_recommended": int(rec.sum()),
            "mean_m3m3": round(float(v.mean()), 5) if got.any() else None,
            "sd_m3m3": round(float(v.std(ddof=1)), 5) if got.sum() > 1 else None,
            "mean_recommended_m3m3": round(float(sm[rec].mean()), 5) if rec.any() else None,
        })
        if (k + 1) % 30 == 0:
            log(f"  {k+1}/{len(granules)} days, {nbytes/1e6:.1f} MB")

    a.out.mkdir(parents=True, exist_ok=True)
    out = {
        "product": "SMAP L3 radiometer global daily soil moisture (SPL3SMP) v009",
        "collection_concept_id": COLLECTION,
        "group": GROUP,
        "variable": "soil_moisture",
        "units": "cm3/cm3",
        "fill_value": FILL,
        "overpass": ("AM (descending), the overpass the retrieval is validated for; the PM "
                     "fields carry a _pm suffix in the same file and are not mixed in here"),
        "record_begins": "2015-03-31",
        "record_note": ("the record is too short for a percentile against a climatology of the "
                        "kind a long gauge record allows, so the panels compare years rather "
                        "than ranking one"),
        "coverage_note": ("the retrieval is gappy: frozen, snow covered, densely vegetated and "
                          "open water cells are not retrieved, so cells_retrieved moves through "
                          "the year and a mean is the mean of what was retrieved"),
        "window": {"rows": [r0, r1], "cols": [c0, c1],
                   "shape": [int(inside.shape[0]), int(inside.shape[1])],
                   "cells_inside_polygon": int(inside.sum()),
                   "coordinate_granules_scanned": scanned,
                   "note": ("the coordinate arrays are written only where a day retrieved "
                            "something, so they are accumulated across granules until the "
                            "located set stops growing; a window taken from one granule is "
                            "that day's coverage and two such windows are not comparable")},
        "basin": {"fixture": a.basin.name, "geometry_sha256": gsha,
                  "area_km2": prov.get("area_km2"), "site": prov.get("site", "")},
        "label": a.label,
        "start": a.start, "end": a.end, "days": len(rows),
        "bytes_transferred": nbytes,
        "retrieved": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "fetch_script": "verification/fixtures/fetch_smap_fixtures.py",
        "license": "NASA data, public (EOSDIS data use guidance)",
        "rows": rows,
    }
    p = a.out / f"smap_l3_{a.label}.json"
    p.write_text(json.dumps(out, indent=1))
    log(f"{p}: {len(rows)} days, {nbytes/1e6:.1f} MB read, {p.stat().st_size/1e3:.1f} kB")


if __name__ == "__main__":
    main()
