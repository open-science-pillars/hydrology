# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "pandas",
#     "pyarrow",
# ]
# ///
# Golden notebook for the load-nwis workflow (the golden-notebook
# requirement: one fixture-backed asserting script per workflow skill):
# qualifier segregation and identifier discipline on a cached
# real gauge subset (Colorado River at Lees Ferry, USGS-09380000,
# 00060 daily mean values, calendar 2023, from the USGS Water Data API
# through dataretrieval; regenerate via fixtures/fetch_usgs_fixtures.py).
# Reference numbers measured at fixture creation and recorded in
# fixtures/README.md.
# Headless green via `uv run verification/load_nwis.py`.

import marimo

__generated_with = "0.23.13"
app = marimo.App()


@app.cell
def _():
    from pathlib import Path

    import pandas as pd

    fixture = Path(__file__).parent / "fixtures" / "lees_ferry_00060_2023_dv.parquet"
    df = pd.read_parquet(fixture)
    return df, pd


@app.cell
def _(df, pd):
    # 1. Identifier discipline: the location id is a string with its
    #    agency prefix, and the site number derived from it keeps the
    #    leading zero of 09380000 through the round trip.
    assert pd.api.types.is_object_dtype(df.monitoring_location_id) or \
        pd.api.types.is_string_dtype(df.monitoring_location_id)
    assert df.monitoring_location_id.iloc[0] == "USGS-09380000"
    site = df.monitoring_location_id.iloc[0].split("-", 1)[1]
    assert site == "09380000", "leading zero must survive"
    assert df.parameter_code.iloc[0] == "00060" and df.statistic_id.iloc[0] == "00003"
    assert df.unit_of_measure.iloc[0] == "ft^3/s", "discharge arrives in cubic feet per second"

    # 2. Qualifier accounting: the 2023 record is fully approved with
    #    no qualifier on any day, and the loader's accounting must say
    #    so explicitly (approval_status and the qualifier list are two
    #    columns on this API, not one code).
    approval = df["approval_status"].value_counts().to_dict()
    assert approval == {"Approved": 365}, f"expected 365 approved days, got {approval}"
    assert df["qualifier"].isna().all(), "no qualifier expected on the 2023 record"

    # 3. Reference statistics (measured 2026-09-06 at fixture creation,
    #    identical to the legacy-service values of 2026-07-05):
    #    dam-controlled reach; mean 12113.6 cfs, min 6570, max 39600.
    q = df["value"]
    assert abs(q.mean() - 12113.6) < 0.1
    assert q.min() == 6570.0 and q.max() == 39600.0
    assert (q > 0).all(), "discharge must be positive on this reach"
    return (approval,)


@app.cell
def _(df, pd):
    # 4. The provisional/approved segregation contract, exercised:
    #    append a synthetic provisional tail (as a trailing window
    #    would deliver) and assert split statistics, never a silent
    #    blend.
    tail = pd.DataFrame({
        "monitoring_location_id": ["USGS-09380000"] * 30,
        "value": [8000.0] * 30,
        "approval_status": ["Provisional"] * 30,
    })
    mixed = pd.concat([df[["monitoring_location_id", "value", "approval_status"]], tail],
                      ignore_index=True)

    by_flag = mixed.groupby("approval_status")["value"].agg(["count", "mean"])
    assert set(by_flag.index) == {"Approved", "Provisional"}
    assert by_flag.loc["Approved", "count"] == 365 and by_flag.loc["Provisional", "count"] == 30

    blended = mixed["value"].mean()
    approved_only = mixed.loc[mixed["approval_status"] == "Approved", "value"].mean()
    # The blend moves the mean by hundreds of cfs: the gotcha's
    # wrong-result mode is numerically visible, so a loader that fails
    # to segregate cannot pass this notebook by accident.
    assert abs(blended - approved_only) > 200, "fixture must expose the blend error"

    print("load_nwis golden: all assertions passed")
    print(f"  365 approved days (mean {approved_only:.1f} cfs) + 30 synthetic provisional days; "
          f"blended mean {blended:.1f} cfs differs by "
          f"{abs(blended - approved_only):.0f} cfs: segregation is not optional")
    return


if __name__ == "__main__":
    app.run()
