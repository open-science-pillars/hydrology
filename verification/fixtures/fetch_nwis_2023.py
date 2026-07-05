# /// script
# requires-python = ">=3.11"
# dependencies = ["dataretrieval", "pandas", "pyarrow"]
# ///
"""Regenerate the load_nwis golden fixture: Lees Ferry 00060 dv, 2023.

No credentials required (public USGS water services). Note the library
migration recorded in the nwis skill: nwis.get_dv is deprecated for
removal on/after 2027-05-06; switch to waterdata.get_daily() then.
"""
from pathlib import Path

import dataretrieval.nwis as nwis

df, _ = nwis.get_dv(sites="09380000", parameterCd="00060",
                    start="2023-01-01", end="2023-12-31")
df = df.reset_index()[["00060_Mean", "00060_Mean_cd", "site_no"]] \
    if "site_no" in df.reset_index().columns else df
out = Path(__file__).parent / "lees_ferry_00060_2023_dv.parquet"
df.to_parquet(out)
print(f"wrote {out} rows={len(df)}")
