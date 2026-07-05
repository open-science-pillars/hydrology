# /// script
# requires-python = ">=3.11"
# dependencies = ["marimo", "pandas", "pyarrow"]
# ///
# Golden for reservoir-analysis (Session 17, SPEC v0.6 §10.3): asserts
# the reservoir-storage-change recipe's measured anchors on the cached
# Lake Powell 2023 fixture (09379900, 62614 daily elevation, pulled
# 2026-07-05). Calendar-year endpoint convention, as the recipe states.

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
    e = df["62614_Mean"]
    quals = df["62614_Mean_cd"].value_counts().to_dict()
    assert quals == {"A": 365}, f"expected fully approved year, got {quals}"

    # Recipe anchors (measured 2026-07-05), calendar convention.
    assert abs(e.iloc[0] - 3524.40) < 0.01
    assert abs(e.min() - 3519.50) < 0.01
    assert abs(e.max() - 3584.30) < 0.01
    assert abs(e.iloc[-1] - 3568.60) < 0.01
    change = e.iloc[-1] - e.iloc[0]
    assert abs(change - 44.20) < 0.01, f"annual change {change:+.2f} ft"

    # The trajectory check that catches endpoint-only implementations:
    # the within-year swing (Feb min to Jul max) far exceeds the
    # endpoint change.
    swing = e.max() - e.min()
    assert swing > change + 15, f"swing {swing:.1f} vs change {change:.1f}"

    # Datum sanity: Lake Powell full pool is 3700 ft; dead pool 3370.
    assert 3370 < e.min() and e.max() < 3700

    print("reservoir_storage golden: all assertions passed")
    print(f"  2023: {e.iloc[0]:.2f} -> {e.iloc[-1]:.2f} ft ({change:+.2f} ft), "
          f"min {e.min():.2f} (Feb), max {e.max():.2f} (Jul), swing {swing:.1f} ft")
    return


if __name__ == "__main__":
    app.run()
