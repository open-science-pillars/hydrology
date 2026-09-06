# /// script
# requires-python = ">=3.11"
# dependencies = ["marimo", "pandas", "pyarrow"]
# ///
# Golden for reservoir-analysis (the golden-notebook requirement: one
# fixture-backed asserting script per workflow skill): asserts
# the reservoir-storage-change recipe's measured anchors on the cached
# Lake Powell 2023 fixture (USGS-09379900, 62614 daily mean elevation,
# from the USGS Water Data API through dataretrieval; regenerate via
# fixtures/fetch_usgs_fixtures.py). Calendar-year endpoint convention,
# as the recipe states.

import marimo

__generated_with = "0.23.13"
app = marimo.App()


@app.cell
def _():
    from pathlib import Path

    import pandas as pd

    fx = Path(__file__).parent / "fixtures" / "powell_62614_2023_dv.parquet"
    df = pd.read_parquet(fx)
    return (df,)


@app.cell
def _(df):
    assert df["parameter_code"].iloc[0] == "62614" and df["unit_of_measure"].iloc[0] == "ft"
    e = df["value"]
    quals = df["approval_status"].value_counts().to_dict()
    assert quals == {"Approved": 365}, f"expected fully approved year, got {quals}"

    # Recipe anchors (measured 2026-07-05 on the legacy service,
    # re-measured 2026-09-06 on the Water Data API fixture, identical),
    # calendar convention.
    assert abs(e.iloc[0] - 3524.40) < 0.01
    assert abs(e.min() - 3519.50) < 0.01
    assert abs(e.max() - 3584.30) < 0.01
    assert abs(e.iloc[-1] - 3568.60) < 0.01
    change = e.iloc[-1] - e.iloc[0]
    assert abs(change - 44.20) < 0.01, f"annual change {change:+.2f} ft"

    # The trajectory check that catches endpoint-only implementations:
    # the within-year swing (mid-Apr min to Jul max) far exceeds the
    # endpoint change.
    swing = e.max() - e.min()
    assert swing > change + 15, f"swing {swing:.1f} vs change {change:.1f}"

    # Datum sanity: Lake Powell full pool is 3700 ft; dead pool 3370.
    assert 3370 < e.min() and e.max() < 3700

    print("reservoir_storage golden: all assertions passed")
    print(f"  2023: {e.iloc[0]:.2f} -> {e.iloc[-1]:.2f} ft ({change:+.2f} ft), "
          f"min {e.min():.2f} (mid-Apr), max {e.max():.2f} (Jul), swing {swing:.1f} ft")
    return


if __name__ == "__main__":
    app.run()
