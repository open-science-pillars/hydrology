# /// script
# requires-python = ">=3.11"
# dependencies = ["earthaccess>=0.14", "netCDF4", "numpy", "requests"]
# ///
"""Pull a basin window of daily precipitation from GES DISC into a
window file the loader and the goldens read.

Two sources, one file schema:

  imerg   GPM IMERG V07 daily (GPM_3IMERGDF, GPM_3IMERGDL or
          GPM_3IMERGDE, chosen by --run final|late|early; the run is
          a declared input, never a default): `precipitation` in
          mm/day (the variable IMERG V07 renamed from precipitationCal)
          and `precipitation_cnt`, one granule per UTC day.
  nldas2  NLDAS-2 primary forcing (NLDAS_FORA0125_H version 2.0):
          hourly `Rainf` in kg m-2 (an hourly accumulation, numerically
          mm) summed over the 24 granules of each UTC day. A granule's
          time stamp is the END of its hour (the granule labelled
          D.0000 covers 23:00 to 00:00 of the day before), so day D is
          the granules labelled D.0100 through D+1.0000.

The route: each granule's Cloud OPeNDAP URL (the CMR RelatedUrls entry
of subtype OPENDAP DATA) with a DAP4 constraint expression that names
the window by grid index, so a day costs tens of kilobytes instead of
a global granule (about 30 MB for IMERG, 1.7 MB per NLDAS hour). When a
subset request does not come back as netCDF, the granule is downloaded
whole from the archive and the same window is cut locally; the route
taken is recorded per day. Both need an Earthdata Login that
earthaccess reads (netrc, environment or prompt) AND the one-time
authorization of the GES DISC application on the user's Earthdata
profile; without the authorization every request is a 403 and the
connector concept records the symptoms.

The window is the bounding box of a basin polygon fixture (a GeoJSON
with a `provenance` member, as the delineate-basin skill writes),
widened by one cell on each side; the loader clips to the polygon.
Values are stored to 0.001 mm (netCDF least_significant_digit=3, then
zlib), which keeps a water year of the Lees Ferry window under the
fixture size rule.

Usage:
  uv run verification/fixtures/fetch_precipitation_fixtures.py --source imerg --run final \
      --basin verification/fixtures/basins/usgs_09380000_nldi.geojson \
      --start 2022-10-01 --end 2023-09-30 \
      --out verification/fixtures/precipitation/imerg_final_lees_ferry_wy2023.nc
  uv run verification/fixtures/fetch_precipitation_fixtures.py --source nldas2 \
      --basin ... --start 2022-10-01 --end 2023-09-30 --out .../nldas2_lees_ferry_wy2023.nc
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
FILL = -9999.0

IMERG_RUNS = {  # run name -> (ShortName, CMR version)
    "final": ("GPM_3IMERGDF", "07"),
    "late": ("GPM_3IMERGDL", "07"),
    "early": ("GPM_3IMERGDE", "07"),
}
NLDAS = ("NLDAS_FORA0125_H", "2.0")

# Grid definitions: (lon0, lat0, step) where the first cell spans
# [lon0, lon0 + step); index = floor((x - x0) / step).
GRIDS = {
    "imerg": (-180.0, -90.0, 0.1),      # 3600 x 1800, dims (time, lon, lat)
    "nldas2": (-125.0, 25.0, 0.125),   # 464 x 224, dims (time, lat, lon)
}


def log(msg):
    print(msg, file=sys.stderr, flush=True)


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


def window_indices(source, bbox, margin=1):
    lon0, lat0, step = GRIDS[source]
    i0 = math.floor((bbox[0] - lon0) / step) - margin
    i1 = math.floor((bbox[2] - lon0) / step) + margin
    j0 = math.floor((bbox[1] - lat0) / step) - margin
    j1 = math.floor((bbox[3] - lat0) / step) + margin
    return i0, i1, j0, j1


def opendap_url(granule):
    for u in granule["umm"].get("RelatedUrls", []):
        if u.get("Subtype") == "OPENDAP DATA":
            return u["URL"]
    return None


def is_netcdf(content: bytes) -> bool:
    return content[:4] == b"\x89HDF" or content[:3] == b"CDF"


def imerg_day(ur: str) -> dt.date:
    m = re.search(r"\.(\d{8})-S", ur)
    return dt.datetime.strptime(m.group(1), "%Y%m%d").date()


def imerg_label(ur: str) -> str:
    return re.search(r"\.(V\d{2}[A-Z])\.", ur).group(1)


def nldas_stamp(ur: str) -> dt.datetime:
    m = re.search(r"\.A(\d{8})\.(\d{4})\.", ur)
    return dt.datetime.strptime(m.group(1) + m.group(2), "%Y%m%d%H%M")


def pull_window(session, granule, ce, cut, workdir):
    """One granule's window: (array dict, route, bytes). `cut` slices a
    full granule to the same window when the subset route fails."""
    url = opendap_url(granule)
    if url:
        try:
            r = session.get(url + ".dap.nc4", params={"dap4.ce": ce}, timeout=120)
            if r.status_code == 200 and is_netcdf(r.content):
                return r.content, "cloud-opendap-dap4", len(r.content)
            log(f"  subset failed ({r.status_code}, {len(r.content)} bytes, netcdf={is_netcdf(r.content)}) for {granule['umm']['GranuleUR']}; archive fallback")
        except Exception as e:  # noqa: BLE001
            log(f"  subset raised {type(e).__name__}: {e}; archive fallback")
    files = earthaccess.download([granule], local_path=str(workdir), threads=1)
    full = Path(files[0])
    nbytes = full.stat().st_size
    return cut(full), "archive", nbytes


def open_any(content_or_path, workdir):
    """A subset comes back as bytes; a fallback is a file on disk. Both
    are opened from disk (netCDF4's in-memory open is noisy on HDF5)."""
    if isinstance(content_or_path, (bytes, bytearray)):
        tmp = Path(tempfile.mkstemp(suffix=".nc4", dir=workdir)[1])
        tmp.write_bytes(content_or_path)
        return netCDF4.Dataset(tmp, mode="r"), tmp
    return netCDF4.Dataset(str(content_or_path), mode="r"), None


def read_imerg(content_or_path, i0, i1, j0, j1, subset: bool, workdir):
    ds, tmp = open_any(content_or_path, workdir)
    with ds:
        if subset:
            p = ds["precipitation"][0, :, :]
            c = ds["precipitation_cnt"][0, :, :]
            lon = ds["lon"][:]
            lat = ds["lat"][:]
        else:
            p = ds["precipitation"][0, i0:i1 + 1, j0:j1 + 1]
            c = ds["precipitation_cnt"][0, i0:i1 + 1, j0:j1 + 1]
            lon = ds["lon"][i0:i1 + 1]
            lat = ds["lat"][j0:j1 + 1]
    if tmp:
        tmp.unlink()
    # IMERG stores (lon, lat); the window file stores (lat, lon)
    p = np.ma.filled(p, FILL).astype("f4").T
    c = np.ma.filled(c, 0).astype("i1").T
    return p, c, np.asarray(lon, "f8"), np.asarray(lat, "f8")


def read_nldas(content_or_path, i0, i1, j0, j1, subset: bool, workdir):
    ds, tmp = open_any(content_or_path, workdir)
    with ds:
        if subset:
            r = ds["Rainf"][0, :, :]
            lon = ds["lon"][:]
            lat = ds["lat"][:]
        else:
            r = ds["Rainf"][0, j0:j1 + 1, i0:i1 + 1]
            lon = ds["lon"][i0:i1 + 1]
            lat = ds["lat"][j0:j1 + 1]
    if tmp:
        tmp.unlink()
    return np.ma.filled(r, FILL).astype("f4"), np.asarray(lon, "f8"), np.asarray(lat, "f8")


def write_window(out: Path, source, days, lat, lon, precip, cnt, runs, labels, ngran, routes, attrs):
    out.parent.mkdir(parents=True, exist_ok=True)
    warnings.filterwarnings("ignore", message=".*Setting the shape.*")  # netCDF4 internals under numpy 2.5, harmless
    with netCDF4.Dataset(out, "w", format="NETCDF4") as ds:
        ds.createDimension("time", len(days))
        ds.createDimension("lat", len(lat))
        ds.createDimension("lon", len(lon))
        t = ds.createVariable("time", "i4", ("time",))
        t.units = "days since 1970-01-01"
        t.calendar = "standard"
        t[:] = [(d - EPOCH).days for d in days]
        v = ds.createVariable("lat", "f8", ("lat",))
        v.units = "degrees_north"
        v.long_name = "cell centre latitude"
        v[:] = lat
        v = ds.createVariable("lon", "f8", ("lon",))
        v.units = "degrees_east"
        v.long_name = "cell centre longitude"
        v[:] = lon
        p = ds.createVariable("precipitation", "f4", ("time", "lat", "lon"), zlib=True,
                              complevel=6, least_significant_digit=3, fill_value=FILL)
        p.units = "mm/day"
        p.long_name = ("IMERG daily precipitation (the V07 `precipitation` variable, formerly precipitationCal)"
                       if source == "imerg" else
                       "NLDAS-2 Rainf (kg m-2 per hour, numerically mm) summed over the 24 hourly granules of the UTC day")
        p.precision_note = "stored to 0.001 mm (least_significant_digit=3) then zlib"
        p[:] = precip
        if cnt is not None:
            c = ds.createVariable("precipitation_cnt", "i1", ("time", "lat", "lon"), zlib=True, complevel=6)
            c.units = "count"
            c.long_name = "IMERG count of valid half-hourly retrievals in the day (48 is complete)"
            c[:] = cnt
        s = ds.createVariable("run", str, ("time",))
        s.long_name = "the run each day came from: final, late or early for IMERG; nldas2 for NLDAS-2"
        for k, r in enumerate(runs):
            s[k] = r
        s = ds.createVariable("label", str, ("time",))
        s.long_name = "the granule's version label (V07B, V07C, ... for IMERG; 2.0 for NLDAS-2)"
        for k, r in enumerate(labels):
            s[k] = r
        g = ds.createVariable("granules", "i2", ("time",))
        g.long_name = "granules composing the day (1 for IMERG; 24 expected for NLDAS-2); 0 means no data for the day"
        g[:] = ngran
        s = ds.createVariable("route", str, ("time",))
        s.long_name = "how the day's window was obtained: cloud-opendap-dap4 or archive"
        for k, r in enumerate(routes):
            s[k] = r
        for k, val in attrs.items():
            ds.setncattr(k, json.dumps(val) if isinstance(val, (dict, list)) else val)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", required=True, choices=["imerg", "nldas2"])
    ap.add_argument("--run", choices=list(IMERG_RUNS), help="IMERG run, required for --source imerg (a declared input, never a default)")
    ap.add_argument("--basin", required=True, type=Path, help="basin polygon fixture (GeoJSON with a provenance member)")
    ap.add_argument("--start", required=True, help="first UTC day, YYYY-MM-DD")
    ap.add_argument("--end", required=True, help="last UTC day, YYYY-MM-DD (inclusive)")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--threads", type=int, default=6)
    a = ap.parse_args()

    if a.source == "imerg" and not a.run:
        ap.error("--run is required for IMERG: the daily runs (final, late, early) differ in calibration, so the run is declared, never chosen here")
    start = dt.date.fromisoformat(a.start)
    end = dt.date.fromisoformat(a.end)
    days = [start + dt.timedelta(n) for n in range((end - start).days + 1)]

    bbox, sha, bprov = basin_bbox(a.basin)
    i0, i1, j0, j1 = window_indices(a.source, bbox)
    log(f"window of {a.source}: lon index {i0}..{i1}, lat index {j0}..{j1} for bbox {bbox}")

    auth = earthaccess.login(strategy="netrc")
    if not getattr(auth, "authenticated", False):
        auth = earthaccess.login()
    session = auth.get_session()

    t0 = time.time()
    if a.source == "imerg":
        short, ver = IMERG_RUNS[a.run]
        ce = (f"/precipitation[0:0][{i0}:{i1}][{j0}:{j1}];/precipitation_cnt[0:0][{i0}:{i1}][{j0}:{j1}];"
              f"/lon[{i0}:{i1}];/lat[{j0}:{j1}];/time")
        granules = earthaccess.search_data(short_name=short, version=ver,
                                           temporal=(f"{start}T00:00:00", f"{end}T23:59:59"), count=-1)
        by_day = {imerg_day(g["umm"]["GranuleUR"]): g for g in granules}
        log(f"{len(granules)} {short} granules for {len(days)} days")
    else:
        short, ver = NLDAS
        ce = f"/Rainf[0:0][{j0}:{j1}][{i0}:{i1}];/lon[{i0}:{i1}];/lat[{j0}:{j1}];/time"
        granules = earthaccess.search_data(short_name=short, version=ver,
                                           temporal=(f"{start}T00:30:00", f"{end + dt.timedelta(1)}T00:30:00"), count=-1)
        by_day = {}
        for g in granules:
            stamp = nldas_stamp(g["umm"]["GranuleUR"])
            day = (stamp - dt.timedelta(hours=1)).date()  # the hour ENDING at the stamp
            by_day.setdefault(day, []).append(g)
        log(f"{len(granules)} {short} granules for {len(days)} days")
    concept_ids = sorted({g["meta"]["collection-concept-id"] for g in granules})

    nlat, nlon = j1 - j0 + 1, i1 - i0 + 1
    precip = np.full((len(days), nlat, nlon), FILL, "f4")
    cnt = np.zeros((len(days), nlat, nlon), "i1") if a.source == "imerg" else None
    runs, labels, ngran, routes = [], [], [], []
    lat = lon = None
    nbytes = 0
    urs = []
    workdir = Path(tempfile.mkdtemp(prefix="precip_fetch_"))

    def imerg_cut(path):
        return path  # read_imerg handles a path with the indices

    # Threads do the HTTP only; every netCDF read happens in the main
    # thread (the HDF5 library underneath netCDF4 is not thread-safe).
    def do_imerg(k_day):
        k, day = k_day
        g = by_day.get(day)
        if g is None:
            return k, None
        content, route, n = pull_window(session, g, ce, imerg_cut, workdir)
        return k, (content, route, n, g["umm"]["GranuleUR"], imerg_label(g["umm"]["GranuleUR"]))

    def do_nldas_hour(g):
        content, route, n = pull_window(session, g, ce, lambda p: p, workdir)
        return content, route, n, g["umm"]["GranuleUR"]

    with ThreadPoolExecutor(a.threads) as ex:
        if a.source == "imerg":
            for k, res in ex.map(do_imerg, enumerate(days)):
                if res is None:
                    runs.append(""); labels.append(""); ngran.append(0); routes.append("")
                    log(f"  {days[k]}: no granule")
                    continue
                content, route, n, ur, label = res
                p, c, lo, la = read_imerg(content, i0, i1, j0, j1, route != "archive", workdir)
                precip[k] = p
                cnt[k] = c
                lat, lon = la, lo
                nbytes += n
                runs.append(a.run); labels.append(label); ngran.append(1); routes.append(route)
                urs.append(ur)
                if (k + 1) % 30 == 0:
                    log(f"  {k + 1}/{len(days)} days, {nbytes / 1e6:.2f} MB, {time.time() - t0:.0f} s")
        else:
            for k, day in enumerate(days):
                gs = sorted(by_day.get(day, []), key=lambda g: g["umm"]["GranuleUR"])
                if not gs:
                    runs.append(""); labels.append(""); ngran.append(0); routes.append("")
                    log(f"  {day}: no granules")
                    continue
                total = np.zeros((nlat, nlon), "f8")
                valid = np.ones((nlat, nlon), bool)
                rts = set()
                for content, route, n, ur in ex.map(do_nldas_hour, gs):
                    r, lo, la = read_nldas(content, i0, i1, j0, j1, route != "archive", workdir)
                    bad = r == FILL
                    valid &= ~bad
                    total += np.where(bad, 0.0, r)
                    lat, lon = la, lo
                    nbytes += n
                    rts.add(route)
                    urs.append(ur)
                precip[k] = np.where(valid, total, FILL).astype("f4")
                runs.append("nldas2"); labels.append(ver); ngran.append(len(gs))
                routes.append(",".join(sorted(rts)))
                if (k + 1) % 10 == 0:
                    log(f"  {k + 1}/{len(days)} days ({len(urs)} granules), {nbytes / 1e6:.2f} MB, {time.time() - t0:.0f} s")

    wall = time.time() - t0
    attrs = {
        "source": a.source,
        "short_name": short,
        "version": ver,
        "run": a.run or "nldas2",
        "collection_concept_ids": concept_ids,
        "doi": {"imerg": {"final": "10.5067/GPM/IMERGDF/DAY/07", "late": "10.5067/GPM/IMERGDL/DAY/07",
                          "early": "10.5067/GPM/IMERGDE/DAY/07"}, "nldas2": {"nldas2": "10.5067/THUF4J1RLSYG"}}[a.source][a.run or "nldas2"],
        "archive": "NASA GES DISC (data.gesdisc.earthdata.nasa.gov; Cloud OPeNDAP at opendap.earthdata.nasa.gov)",
        "route": "Cloud OPeNDAP DAP4 constraint expression per granule; archive download with a local cut when a subset request is not netCDF (see the route variable)",
        "dap4_constraint": ce,
        "window_indices": {"lon": [i0, i1], "lat": [j0, j1], "grid": GRIDS[a.source]},
        "basin_fixture": a.basin.name,
        "basin_geometry_sha256": sha,
        "basin_site": bprov.get("site", ""),
        "bbox": list(bbox),
        "bbox_note": "the basin polygon's bounding box widened by one cell each side; the loader clips to the polygon",
        "days_requested": len(days),
        "days_with_data": int(sum(1 for n in ngran if n > 0)),
        "granule_count": len(urs),
        "first_granule": urs[0] if urs else "",
        "last_granule": urs[-1] if urs else "",
        "hour_convention": ("a NLDAS_FORA0125_H granule's stamp is the end of its hour; UTC day D is the granules "
                            "labelled D.0100 through D+1.0000") if a.source == "nldas2" else "one granule per UTC day",
        "bytes_transferred": nbytes,
        "wall_seconds": round(wall, 1),
        "retrieved": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "fetch_script": "verification/fixtures/fetch_precipitation_fixtures.py",
        "credential_note": "Earthdata Login through earthaccess (netrc) plus the GES DISC application authorization; nothing about the credential is stored here",
    }
    write_window(a.out, a.source, days, lat, lon, precip, cnt, runs, labels, ngran, routes, attrs)
    size = a.out.stat().st_size
    print(f"{a.out}: {len(days)} days ({attrs['days_with_data']} with data), {len(urs)} granules, "
          f"{nbytes / 1e6:.2f} MB transferred in {wall:.0f} s, file {size / 1e6:.2f} MB, routes {sorted(set(routes))}")
    if size > 5_000_000:
        print("WARNING: over the 5 MB fixture rule", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
