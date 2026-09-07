# /// script
# requires-python = ">=3.11"
# dependencies = ["earthaccess>=0.14", "netCDF4", "numpy", "requests"]
# ///
"""Pull a basin window of MOD16 evapotranspiration from LP DAAC into a
window file the loader and the goldens read.

The product is MOD16A2GF (gap-filled, `--product mod16a2gf`, the
default) or its near-real-time companion MOD16A2 (`--product mod16a2`),
both version 061: `ET_500m`, an 8-day total in kg per m2 (numerically
mm) at 500 m on the MODIS sinusoidal grid, with `ET_QC_500m` beside it.
Values are stored RAW, as int16, because the fill codes are the point:
the file header carries one `_FillValue` but the product uses seven
codes, one per land cover class where evapotranspiration was not
computed, and a loader that rescales them into millimetres before the
loader sees them would hide exactly what the basin mean has to
declare.

The route: each granule's Cloud OPeNDAP URL (the CMR RelatedUrls entry
of subtype OPENDAP DATA) with a DAP4 constraint expression naming the
window by grid row and column, so a composite costs tens of kilobytes
instead of a 20 to 33 MB tile. When a subset request does not come
back as netCDF the granule is downloaded whole from the archive and
the same window is cut locally; the route taken is recorded per
composite. Both need an Earthdata Login that earthaccess reads (netrc,
environment or prompt) AND the one-time authorization of the LP DAAC
application on the user's Earthdata profile.

The window is the bounding box of a basin polygon fixture (a GeoJSON
with a `provenance` member, as the delineate-basin skill writes) or an
explicit `--bbox`, widened by one cell on each side; the loader clips
to the polygon. A window that spans more than one sinusoidal tile is
refused: the tiles do not share a row and column origin, and a
silently mosaicked window would put cells in the wrong place.

Usage:
  uv run verification/fixtures/fetch_et_fixtures.py \
      --basin verification/fixtures/basins/usgs_09085000_nldi.geojson \
      --start 2023-01-01 --end 2023-12-31 \
      --out verification/fixtures/et/mod16a2gf_roaring_fork_2023.nc
  uv run verification/fixtures/fetch_et_fixtures.py \
      --bbox -111.5,36.9,-110.9,37.5 --name lake_powell \
      --start 2023-01-01 --end 2023-12-31 \
      --out verification/fixtures/et/mod16a2gf_lake_powell_2023.nc
"""
import argparse
import datetime as dt
import hashlib
import json
import math
import re
import sys
import tempfile
import time
import warnings
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import earthaccess
import netCDF4
import numpy as np

EPOCH = dt.date(1970, 1, 1)

PRODUCTS = {  # name -> (ShortName, CMR version)
    "mod16a2gf": ("MOD16A2GF", "061"),
    "mod16a2": ("MOD16A2", "061"),
}

# The MODIS sinusoidal grid, as the product's own metadata defines it.
R = 6371007.181                     # sphere radius, metres
TILE = 1111950.5196666666           # tile side, metres
PIX = TILE / 2400                   # 500 m grid: 463.31271652777775 m
X0 = -20015109.354                  # west edge of tile column 0
Y0 = 10007554.677                   # north edge of tile row 0

GROUP = "/MOD_Grid_MOD16A2/Data_Fields"


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def sinu(lon, lat):
    """Longitude and latitude in degrees to sinusoidal metres."""
    return R * math.radians(lon) * math.cos(math.radians(lat)), R * math.radians(lat)


def inv_sinu(x, y):
    """Sinusoidal metres back to longitude and latitude in degrees."""
    lat = math.degrees(y / R)
    c = math.cos(math.radians(lat))
    return math.degrees(x / (R * c)) if c else 0.0, lat


def tile_of(lon, lat):
    x, y = sinu(lon, lat)
    return int((x - X0) // TILE), int((Y0 - y) // TILE)


def cell_of(lon, lat, h, v):
    x, y = sinu(lon, lat)
    xt, yt = X0 + h * TILE, Y0 - v * TILE
    return int((yt - y) // PIX), int((x - xt) // PIX)


def basin_bbox(path: Path):
    doc = json.loads(path.read_text())
    geom = doc["features"][0]["geometry"]
    coords = []

    def walk(c):
        if isinstance(c[0], (int, float)):
            coords.append(c)
        else:
            for x in c:
                walk(x)
    walk(geom["coordinates"])
    xs = [c[0] for c in coords]
    ys = [c[1] for c in coords]
    sha = hashlib.sha256(json.dumps(geom, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return (min(xs), min(ys), max(xs), max(ys)), sha, doc.get("provenance", {})


def lattice(bbox, step):
    lons = [bbox[0] + i * step for i in range(int((bbox[2] - bbox[0]) / step) + 1)] + [bbox[2]]
    lats = [bbox[1] + i * step for i in range(int((bbox[3] - bbox[1]) / step) + 1)] + [bbox[3]]
    return lons, lats


def tiles_for(bbox, step=0.05):
    """Every sinusoidal tile the bounding box touches. The corners are
    not enough: the grid converges toward the poles, so a box can cross
    a tile boundary between two corners."""
    lons, lats = lattice(bbox, step)
    return sorted({tile_of(lon, lat) for lon in lons for lat in lats})


def window_indices(bbox, h, v, margin=1, step=0.02):
    """Rows and columns of ONE tile holding the part of the bbox that
    falls inside it. Clipped to the tile: what reaches past its edge is
    covered by the neighbouring tile's own window, and the two are
    never mosaicked by index because they share no origin."""
    lons, lats = lattice(bbox, step)
    rc = [cell_of(lon, lat, h, v) for lon in lons for lat in lats if tile_of(lon, lat) == (h, v)]
    if not rc:
        raise SystemExit(f"REFUSED: no part of the bounding box falls in tile h{h:02d}v{v:02d}")
    r0 = max(0, min(r for r, _ in rc) - margin)
    r1 = min(2399, max(r for r, _ in rc) + margin)
    c0 = max(0, min(c for _, c in rc) - margin)
    c1 = min(2399, max(c for _, c in rc) + margin)
    return r0, r1, c0, c1


def cell_centres(h, v, r0, r1, c0, c1):
    """Longitude and latitude of every cell centre in the window, as
    2-D arrays: in a sinusoidal grid a column is not a meridian."""
    rows = np.arange(r0, r1 + 1)
    cols = np.arange(c0, c1 + 1)
    y = (Y0 - v * TILE) - (rows + 0.5) * PIX
    x = (X0 + h * TILE) + (cols + 0.5) * PIX
    xx, yy = np.meshgrid(x, y)
    lat = np.degrees(yy / R)
    lon = np.degrees(xx / (R * np.cos(np.radians(lat))))
    return lon.astype("f8"), lat.astype("f8")


def opendap_url(granule):
    for u in granule["umm"].get("RelatedUrls", []):
        if u.get("Subtype") == "OPENDAP DATA":
            return u["URL"]
    return None


def is_netcdf(content: bytes) -> bool:
    return content[:4] == b"\x89HDF" or content[:3] == b"CDF"


def composite_start(ur: str) -> dt.date:
    m = re.search(r"\.A(\d{4})(\d{3})\.", ur)
    return dt.date(int(m.group(1)), 1, 1) + dt.timedelta(int(m.group(2)) - 1)


def granule_days(granule) -> int:
    """The composite's length in days from the granule's own temporal
    extent: 8 for every period but the last of the year, which is 5 or
    6 (the user guide says so and the metadata confirms it)."""
    t = granule["umm"]["TemporalExtent"]["RangeDateTime"]
    b = dt.date.fromisoformat(t["BeginningDateTime"][:10])
    e = dt.date.fromisoformat(t["EndingDateTime"][:10])
    return (e - b).days + 1


def pull_window(session, granule, ce, workdir):
    url = opendap_url(granule)
    if url:
        try:
            r = session.get(url + ".dap.nc4", params={"dap4.ce": ce}, timeout=180)
            if r.status_code == 200 and is_netcdf(r.content):
                return r.content, "cloud-opendap-dap4", len(r.content)
            log(f"  subset failed ({r.status_code}, {len(r.content)} bytes, netcdf={is_netcdf(r.content)}) "
                f"for {granule['umm']['GranuleUR']}; archive fallback")
        except Exception as e:  # noqa: BLE001
            log(f"  subset raised {type(e).__name__}: {e}; archive fallback")
    files = earthaccess.download([granule], local_path=str(workdir), threads=1)
    full = Path(files[0])
    return full, "archive", full.stat().st_size


def read_window(content_or_path, r0, r1, c0, c1, subset: bool, workdir):
    """ET and QC over the window, raw. A subset comes back as bytes
    holding just the window; a fallback is a whole tile on disk, cut
    here to the same rows and columns."""
    if isinstance(content_or_path, (bytes, bytearray)):
        tmp = Path(tempfile.mkstemp(suffix=".nc4", dir=workdir)[1])
        tmp.write_bytes(content_or_path)
        ds = netCDF4.Dataset(tmp, mode="r")
    else:
        tmp = None
        ds = netCDF4.Dataset(str(content_or_path), mode="r")
    with ds:
        g = ds["MOD_Grid_MOD16A2"]["Data_Fields"] if "MOD_Grid_MOD16A2" in ds.groups else ds
        et = g["ET_500m"]
        qc = g["ET_QC_500m"]
        et.set_auto_maskandscale(False)
        qc.set_auto_maskandscale(False)
        if subset:
            et = np.asarray(et[:, :])
            qc = np.asarray(qc[:, :])
        else:
            et = np.asarray(et[r0:r1 + 1, c0:c1 + 1])
            qc = np.asarray(qc[r0:r1 + 1, c0:c1 + 1])
    if tmp:
        tmp.unlink()
    return et.astype("i2"), qc.astype("u1")


def write_window(out: Path, product, short, ver, starts, days, lon, lat, et, qc,
                 labels, routes, urs, attrs):
    out.parent.mkdir(parents=True, exist_ok=True)
    warnings.filterwarnings("ignore", message=".*Setting the shape.*")
    with netCDF4.Dataset(out, "w", format="NETCDF4") as ds:
        ds.createDimension("time", len(starts))
        ds.createDimension("row", lat.shape[0])
        ds.createDimension("col", lat.shape[1])
        t = ds.createVariable("time", "i4", ("time",))
        t.units = "days since 1970-01-01"
        t.calendar = "standard"
        t.long_name = "first day of the 8-day composite period"
        t[:] = [(d - EPOCH).days for d in starts]
        d = ds.createVariable("composite_days", "i1", ("time",))
        d.long_name = ("length of the composite period in days, from the granule's temporal extent: "
                       "8 for every period but the last of the year, which is 5 or 6")
        d[:] = days
        v = ds.createVariable("lat", "f8", ("row", "col"), zlib=True, complevel=9, shuffle=True)
        v.units = "degrees_north"
        v.long_name = "cell centre latitude (2-D: a sinusoidal column is not a meridian)"
        v[:] = lat
        v = ds.createVariable("lon", "f8", ("row", "col"), zlib=True, complevel=9, shuffle=True)
        v.units = "degrees_east"
        v.long_name = "cell centre longitude (2-D: a sinusoidal column is not a meridian)"
        v[:] = lon
        e = ds.createVariable("ET_500m", "i2", ("time", "row", "col"), zlib=True, complevel=9, shuffle=True)
        e.units = "kg/m^2/8day"
        e.scale_factor_note = ("stored raw: multiply valid values by 0.1 for kg per m2 (numerically mm) "
                               "over the composite period. Values above 32700 are not measurements: "
                               "32767 fill, 32766 water, 32765 barren or sparse vegetation, 32764 snow "
                               "and ice, 32763 wetland, 32762 urban, 32761 unclassified")
        e.valid_range = np.array([-32767, 32700], "i2")
        e[:] = et
        q = ds.createVariable("ET_QC_500m", "u1", ("time", "row", "col"), zlib=True, complevel=9, shuffle=True)
        q.long_name = ("quality control, inherited from MOD15A2: bit 0 MODLAND_QC, bit 1 sensor, "
                       "bit 2 dead detector, bits 3-4 cloud state, bits 5-7 SCF_QC")
        q[:] = qc
        s = ds.createVariable("label", str, ("time",))
        s.long_name = "the granule's version label"
        for k, r in enumerate(labels):
            s[k] = r
        s = ds.createVariable("route", str, ("time",))
        s.long_name = "how the composite's window was obtained: cloud-opendap-dap4 or archive"
        for k, r in enumerate(routes):
            s[k] = r
        s = ds.createVariable("granule", str, ("time",))
        s.long_name = "the granule the composite came from"
        for k, r in enumerate(urs):
            s[k] = r
        for k, val in attrs.items():
            ds.setncattr(k, json.dumps(val) if isinstance(val, (dict, list)) else val)


def fetch_tile(a, short, ver, session, bbox, sha, bprov, wname, start, end, h, v, out):
    """One tile's window, written to its own file: a basin larger than
    a tile is one file per tile, and the loader combines them by summing
    their cells."""
    tile = f"h{h:02d}v{v:02d}"
    r0, r1, c0, c1 = window_indices(bbox, h, v)
    log(f"window of {short} over {tile}: rows {r0}..{r1}, cols {c0}..{c1} "
        f"({r1 - r0 + 1} by {c1 - c0 + 1})")


    granules = earthaccess.search_data(short_name=short, version=ver, granule_name=f"*.{tile}.*",
                                       temporal=(f"{start}T00:00:00", f"{end}T23:59:59"), count=-1)
    granules = sorted(granules, key=lambda g: g["umm"]["GranuleUR"])
    keep = [g for g in granules if start <= composite_start(g["umm"]["GranuleUR"]) <= end]
    log(f"{len(keep)} {short} composites over {tile} between {start} and {end}")
    if not keep:
        raise SystemExit("no granules for that window and period")
    concept_ids = sorted({g["meta"]["collection-concept-id"] for g in keep})

    ce = (f"{GROUP}/ET_500m[{r0}:{r1}][{c0}:{c1}];"
          f"{GROUP}/ET_QC_500m[{r0}:{r1}][{c0}:{c1}]")
    nrow, ncol = r1 - r0 + 1, c1 - c0 + 1
    et = np.full((len(keep), nrow, ncol), 32767, "i2")
    qc = np.full((len(keep), nrow, ncol), 255, "u1")
    starts, days, labels, routes, urs = [], [], [], [], []
    nbytes = 0
    workdir = Path(tempfile.mkdtemp(prefix="et_fetch_"))
    t0 = time.time()

    def do(k_g):
        k, g = k_g
        content, route, n = pull_window(session, g, ce, workdir)
        return k, content, route, n, g

    # Threads do the HTTP only; every netCDF read happens in the main
    # thread (the HDF5 library underneath netCDF4 is not thread-safe).
    with ThreadPoolExecutor(a.threads) as ex:
        for k, content, route, n, g in ex.map(do, list(enumerate(keep))):
            ur = g["umm"]["GranuleUR"]
            e, q = read_window(content, r0, r1, c0, c1, route != "archive", workdir)
            et[k] = e
            qc[k] = q
            nbytes += n
            starts.append(composite_start(ur))
            days.append(granule_days(g))
            labels.append(ur.split(".")[3])
            routes.append(route)
            urs.append(ur)
            if (k + 1) % 10 == 0:
                log(f"  {k + 1}/{len(keep)} composites, {nbytes / 1e6:.2f} MB, {time.time() - t0:.0f} s")

    order = np.argsort([(d - EPOCH).days for d in starts])
    starts = [starts[i] for i in order]
    days = [days[i] for i in order]
    labels = [labels[i] for i in order]
    routes = [routes[i] for i in order]
    urs = [urs[i] for i in order]
    et = et[order]
    qc = qc[order]
    lon, lat = cell_centres(h, v, r0, r1, c0, c1)

    attrs = {
        "source": "mod16",
        "product": a.product,
        "short_name": short,
        "version": ver,
        "collection_concept_ids": concept_ids,
        "doi": f"10.5067/MODIS/{short}.061",
        "archive": "NASA LP DAAC (LPCLOUD)",
        "tile": tile,
        "window_indices": json.dumps({"row": [r0, r1], "col": [c0, c1]}),
        "grid": ("MODIS sinusoidal, 500 m: sphere radius 6371007.181 m, tile side 1111950.5196666666 m, "
                 "2400 by 2400 cells, cell 463.31271652777775 m"),
        "basin_fixture": a.basin.name if a.basin else "",
        "basin_geometry_sha256": sha,
        "basin_site": bprov.get("site", ""),
        "window_name": wname,
        "bbox": json.dumps([round(x, 6) for x in bbox]),
        "bbox_note": "bounding box of the basin polygon (or --bbox), widened by one cell on each side",
        "composites": len(keep),
        "first_composite": str(starts[0]),
        "last_composite": str(starts[-1]),
        "route": ("Cloud OPeNDAP DAP4 constraint expression per granule; archive download with a local cut "
                  "when a subset request is not netCDF (see the route variable)"),
        "dap4_constraint": ce,
        "bytes_transferred": nbytes,
        "wall_seconds": round(time.time() - t0, 1),
        "retrieved": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "fetch_script": "verification/fixtures/fetch_et_fixtures.py",
        "credential_note": ("Earthdata Login through earthaccess (netrc, environment or prompt) with the "
                            "LP DAAC application authorized; no credential is stored in this file"),
    }
    write_window(out, a.product, short, ver, starts, days, lon, lat, et, qc, labels, routes, urs, attrs)
    sz = out.stat().st_size
    log(f"{out}: {len(keep)} composites, {nbytes / 1e6:.2f} MB transferred in "
        f"{time.time() - t0:.0f} s, file {sz / 1e6:.2f} MB, routes {sorted(set(routes))}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--product", default="mod16a2gf", choices=list(PRODUCTS))
    ap.add_argument("--basin", type=Path, help="basin polygon fixture (GeoJSON with a provenance member)")
    ap.add_argument("--bbox", help="west,south,east,north in degrees, when there is no basin polygon")
    ap.add_argument("--name", default="", help="a name for the window when --bbox is used")
    ap.add_argument("--start", required=True, help="first day, YYYY-MM-DD")
    ap.add_argument("--end", required=True, help="last day, YYYY-MM-DD (inclusive)")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--threads", type=int, default=6)
    a = ap.parse_args()

    if not a.basin and not a.bbox:
        ap.error("one of --basin or --bbox is required")
    short, ver = PRODUCTS[a.product]
    start = dt.date.fromisoformat(a.start)
    end = dt.date.fromisoformat(a.end)

    if a.basin:
        bbox, sha, bprov = basin_bbox(a.basin)
        wname = a.name or a.basin.stem
    else:
        bbox = tuple(float(x) for x in a.bbox.split(","))
        sha, bprov, wname = "", {}, a.name or "bbox"
    tiles = tiles_for(bbox)
    log(f"the bounding box {bbox} touches {len(tiles)} sinusoidal tile(s): "
        + ", ".join(f"h{h:02d}v{v:02d}" for h, v in tiles))
    if len(tiles) > 1 and "{tile}" not in a.out.name:
        raise SystemExit(f"REFUSED: this bounding box spans {len(tiles)} tiles, so it is {len(tiles)} window "
                         f"files, one per tile: put {{tile}} in --out (for example "
                         f"{a.out.parent / (a.out.stem + '_{tile}' + a.out.suffix)}). Tiles share no row and "
                         f"column origin, so they are never mosaicked by index; the loader takes one --window "
                         f"per tile and combines them by summing their cells")

    auth = earthaccess.login(strategy="netrc")
    if not getattr(auth, "authenticated", False):
        auth = earthaccess.login()
    session = auth.get_session()

    written = []
    for h, v in tiles:
        out = Path(str(a.out).replace("{tile}", f"h{h:02d}v{v:02d}"))
        fetch_tile(a, short, ver, session, bbox, sha, bprov, wname, start, end, h, v, out)
        written.append(out)
    if len(written) > 1:
        log(f"{len(written)} window files, one per tile; the loader takes one --window per file")


if __name__ == "__main__":
    main()
