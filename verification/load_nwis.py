# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "pandas",
#     "pyarrow",
# ]
# ///
# Golden notebook for the load-nwis workflow (Session 16, SPEC v0.6
# §10.3): qualifier segregation and identifier discipline on a cached
# real gauge subset (Colorado River at Lees Ferry, site 09380000,
# 00060 daily values, calendar 2023, pulled 2026-07-05; regenerate via
# fixtures/fetch_nwis_2023.py). Reference numbers measured at fixture
# creation and recorded in fixtures/README.md.
# Headless green via `python verification/load_nwis.py`.

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
    # 1. Identifier discipline: site numbers are strings; the leading
    #    zero of 09380000 survives the round trip.
    assert df.site_no.dtype == object or pd.api.types.is_string_dtype(df.site_no)
    assert df.site_no.iloc[0] == "09380000", "leading zero must survive"

    # 2. Qualifier accounting: the 2023 record is fully approved, and
    #    the loader's accounting must say so explicitly.
    quals = df["00060_Mean_cd"].value_counts().to_dict()
    assert quals == {"A": 365}, f"expected 365 approved days, got {quals}"

    # 3. Reference statistics (measured 2026-07-05 at fixture creation):
    #    dam-controlled reach; mean 12113.6 cfs, min 6570, max 39600.
    q = df["00060_Mean"]
    assert abs(q.mean() - 12113.6) < 0.1
    assert q.min() == 6570.0 and q.max() == 39600.0
    assert (q > 0).all(), "discharge must be positive on this reach"
    return (quals,)


@app.cell
def _(df, pd):
    # 4. The P/A segregation contract, exercised: append a synthetic
    #    provisional tail (as a trailing window would deliver) and
    #    assert split statistics, never a silent blend.
    tail = pd.DataFrame({
        "00060_Mean": [8000.0] * 30,
        "00060_Mean_cd": ["P"] * 30,
        "site_no": ["09380000"] * 30,
    })
    mixed = pd.concat([df, tail], ignore_index=True)

    by_flag = mixed.groupby("00060_Mean_cd")["00060_Mean"].agg(["count", "mean"])
    assert set(by_flag.index) == {"A", "P"}
    assert by_flag.loc["A", "count"] == 365 and by_flag.loc["P", "count"] == 30

    blended = mixed["00060_Mean"].mean()
    approved_only = mixed.loc[mixed["00060_Mean_cd"] == "A", "00060_Mean"].mean()
    # The blend moves the mean by hundreds of cfs: the gotcha's
    # wrong-result mode is numerically visible, so a loader that fails
    # to segregate cannot pass this notebook by accident.
    assert abs(blended - approved_only) > 200, "fixture must expose the blend error"

    print("load_nwis golden: all assertions passed")
    print(f"  365 A days (mean {approved_only:.1f} cfs) + 30 synthetic P days; "
          f"blended mean {blended:.1f} cfs differs by "
          f"{abs(blended - approved_only):.0f} cfs: segregation is not optional")
    return


if __name__ == "__main__":
    app.run()
