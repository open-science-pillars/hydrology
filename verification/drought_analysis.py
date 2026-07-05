# /// script
# requires-python = ">=3.11"
# dependencies = ["marimo", "numpy", "pandas", "pyarrow"]
# ///
# Golden for drought-analysis (Session 17, SPEC v0.6 §10.3): asserts
# the drought-index recipe's measured anchors on cached fixtures
# (Roaring Fork 09085000, 2021 drought vs 2023 wet, 1991-2020 daily
# climatology; pulled 2026-07-05). The recipe is the authority for
# every number here.

import marimo

__generated_with = "0.23.13"
app = marimo.App()


@app.cell
def _():
    from pathlib import Path

    import numpy as np
    import pandas as pd

    fx = Path(__file__).parent / "fixtures"
    clim = pd.read_parquet(fx / "roaring_fork_00060_clim9120_dv.parquet")
    clim["doy"] = pd.to_datetime(clim["datetime"]).dt.dayofyear
    groups = clim.groupby("doy")["00060_Mean"]

    def index_for(year_file):
        df = pd.read_parquet(fx / year_file)
        df["doy"] = pd.to_datetime(df["datetime"]).dt.dayofyear
        # approved values only, per the recipe ("A" and "A, e" both approved)
        df = df[df["00060_Mean_cd"].str.startswith("A")]
        pct = np.array([(groups.get_group(r.doy) < r["00060_Mean"]).mean() * 100
                        for _, r in df.iterrows() if r.doy in groups.groups])
        return pct

    return groups, index_for, np


@app.cell
def _(index_for, np):
    # Recipe anchors, measured 2026-07-05; tolerance well inside the
    # recipe's expected_uncertainty (+/- ~3 percentile points).
    p21 = index_for("roaring_fork_00060_2021_dv.parquet")
    p23 = index_for("roaring_fork_00060_2023_dv.parquet")

    assert abs(np.median(p21) - 13.3) < 1.0, f"2021 median {np.median(p21):.1f}"
    assert abs((p21 < 30).mean() - 0.92) < 0.03
    assert abs((p21 < 10).mean() - 0.28) < 0.03
    assert abs(np.median(p23) - 33.3) < 1.0, f"2023 median {np.median(p23):.1f}"
    assert abs((p23 < 30).mean() - 0.39) < 0.03
    assert abs((p23 < 10).mean() - 0.05) < 0.03

    # The physics check: the drought year and the wet year separate by
    # ~20 median percentile points; an index that cannot see this is
    # not measuring drought.
    sep = np.median(p23) - np.median(p21)
    assert sep > 15, f"2021/2023 separation only {sep:.1f} points"

    print("drought_analysis golden: all assertions passed")
    print(f"  2021 median pctile {np.median(p21):.1f} vs 2023 {np.median(p23):.1f} "
          f"(separation {sep:.1f} points); below-30th fractions "
          f"{(p21 < 30).mean():.2f} vs {(p23 < 30).mean():.2f}")
    return


if __name__ == "__main__":
    app.run()
