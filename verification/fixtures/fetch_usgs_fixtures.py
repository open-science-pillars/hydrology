# /// script
# requires-python = ">=3.11"
# dependencies = ["dataretrieval>=1.3,<2", "pandas", "pyarrow"]
# ///
"""Regenerate the USGS daily-value fixtures the goldens read.

Source: the USGS Water Data API (api.waterdata.usgs.gov, the `daily`
collection) through dataretrieval's waterdata module. No credential
is required; a free key in API_USGS_PAT (https://api.waterdata.usgs.gov/signup/)
raises the rate limit and travels only as an X-Api-Key header, which
dataretrieval sends on its own. Retries on 429 are turned off here:
a retry spends a second request against an hourly bucket.

Schema, one row per day, ten columns as the API names them:
monitoring_location_id (with its USGS- prefix), parameter_code,
statistic_id, time_series_id, time (the API's date string), value
(float64), unit_of_measure, approval_status (Approved or Provisional),
qualifier (a list of strings such as ESTIMATED, or null), last_modified.
Geometry is dropped. Site numbers keep their leading zeros because the
identifier is a string with a prefix.

The Lees Ferry fixture carries a row-count check against the frozen
legacy capture of the same window (calendar 2023, 365 rows, content
sha256 51a6b2bdc514, taken 2026-09-06 from waterservices.usgs.gov
before that host's decommission); pass --legacy with the path to that
capture's canonical JSON to compare it value by value as well.

Usage:
  uv run verification/fixtures/fetch_usgs_fixtures.py            # all five
  uv run verification/fixtures/fetch_usgs_fixtures.py --only lees_ferry_00060_2023_dv
  uv run verification/fixtures/fetch_usgs_fixtures.py --legacy PATH/TO/51a6b2bd.canonical.json
"""
import argparse
import json
import sys
from pathlib import Path

import dataretrieval
import pandas as pd
from dataretrieval import waterdata
from dataretrieval.waterdata.configuration import WaterdataConfiguration

COLUMNS = ["monitoring_location_id", "parameter_code", "statistic_id",
           "time_series_id", "time", "value", "unit_of_measure",
           "approval_status", "qualifier", "last_modified"]

# name -> (location, parameter, window)
FIXTURES = {
    "lees_ferry_00060_2023_dv": ("USGS-09380000", "00060", "2023-01-01/2023-12-31"),
    "powell_62614_2023_dv": ("USGS-09379900", "62614", "2023-01-01/2023-12-31"),
    "roaring_fork_00060_2021_dv": ("USGS-09085000", "00060", "2021-01-01/2021-12-31"),
    "roaring_fork_00060_2023_dv": ("USGS-09085000", "00060", "2023-01-01/2023-12-31"),
    "roaring_fork_00060_clim9120_dv": ("USGS-09085000", "00060", "1991-01-01/2020-12-31"),
    # The drought view's streamflow panel, by water year rather than
    # calendar year, at a gauge below a major dam: the panel is an
    # operations record and is labelled as one.
    "lees_ferry_00060_wy2021_dv": ("USGS-09380000", "00060", "2020-10-01/2021-09-30"),
    "lees_ferry_00060_wy2023_dv": ("USGS-09380000", "00060", "2022-10-01/2023-09-30"),
}
LEGACY_ROWS = {"lees_ferry_00060_2023_dv": 365}


def fetch(location: str, parameter: str, window: str) -> tuple[pd.DataFrame, str]:
    df, md = waterdata.get_daily(
        monitoring_location_id=location, parameter_code=parameter,
        statistic_id="00003", time=window, skip_geometry=True,
        convert_type=False)
    if df.empty:
        sys.exit(f"no rows for {location} {parameter} {window}")
    df = df[COLUMNS].copy()
    df["value"] = df["value"].astype("float64")
    df["qualifier"] = df["qualifier"].apply(
        lambda q: None if q is None or (isinstance(q, float) and pd.isna(q)) else sorted(q))
    for c in COLUMNS:
        if c not in ("value", "qualifier"):
            df[c] = df[c].astype(object)
    df = df.sort_values("time").reset_index(drop=True)
    return df, md.url


def compare_legacy(df: pd.DataFrame, path: Path) -> None:
    rows = json.loads(path.read_text())[0]["rows"]
    legacy = {r["t"][:10]: r["v"] for r in rows}
    new = {t[:10]: v for t, v in zip(df["time"], df["value"])}
    missing = sorted(set(legacy) - set(new))
    diffs = [d for d in legacy if d in new and float(legacy[d]) != new[d]]
    print(f"  legacy {len(legacy)} rows, api {len(new)} rows, "
          f"missing {len(missing)}, value differences {len(diffs)}")
    if missing or diffs:
        sys.exit("legacy comparison failed")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", action="append", default=[], choices=sorted(FIXTURES))
    ap.add_argument("--legacy", type=Path, default=None,
                    help="canonical JSON of the legacy calendar-2023 Lees Ferry capture")
    args = ap.parse_args()
    here = Path(__file__).parent
    for name in (args.only or FIXTURES):
        location, parameter, window = FIXTURES[name]
        with dataretrieval.configure(WaterdataConfiguration(retries=0)):
            df, url = fetch(location, parameter, window)
        if name in LEGACY_ROWS and len(df) != LEGACY_ROWS[name]:
            sys.exit(f"{name}: {len(df)} rows, legacy capture had {LEGACY_ROWS[name]}")
        if name == "lees_ferry_00060_2023_dv" and args.legacy:
            compare_legacy(df, args.legacy)
        out = here / f"{name}.parquet"
        df.to_parquet(out, index=False)
        quals = df["approval_status"].value_counts().to_dict()
        est = int(df["qualifier"].apply(lambda q: bool(q) and "ESTIMATED" in q).sum())
        print(f"wrote {out.name}: {len(df)} rows {df['time'].iloc[0]}..{df['time'].iloc[-1]}, "
              f"{quals}, estimated {est}, {out.stat().st_size / 1024:.1f} KB, "
              f"dataretrieval {dataretrieval.__version__}\n  {url}")


if __name__ == "__main__":
    main()
