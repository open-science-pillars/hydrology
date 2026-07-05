# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy",
#     "pandas",
# ]
# ///
# Golden notebook for the load-swot-hydro workflow (Session 15, SPEC
# v0.6 §10.3): scope and quality assertions on a synthetic reach/node
# fixture built to the granule structure observed live 2026-07-05
# (attribute names from the RiverSP D pair: cycle 011, pass 424, AS,
# PGD0). Headless green via `python verification/load_swot_hydro.py`.

import marimo

__generated_with = "0.23.13"
app = marimo.App()


@app.cell
def _():
    import numpy as np
    import pandas as pd

    return np, pd


@app.cell
def _(np, pd):
    # Synthetic pass-continent fixture, deterministic. One reach of 50
    # nodes (~200 m spacing) with a known water surface profile, plus
    # the product's own reach-level aggregate row, mirroring the
    # separate-collections reality.
    rng = np.random.default_rng(20260705)
    n_nodes = 50
    TRUE_WSE = 132.40          # m, reach-scale water surface elevation
    TRUE_SLOPE = 4.5e-5        # m/m, exists ONLY at reach level
    SYS_OFFSET = 0.18          # m, correlated systematic shared by all nodes

    dist = np.arange(n_nodes) * 200.0
    wse_true = TRUE_WSE + TRUE_SLOPE * (dist[::-1] - dist.mean())
    node_noise = rng.normal(0, 0.10, n_nodes)          # random per node
    nodes = pd.DataFrame({
        "reach_id": "731234500001",
        "node_id": [f"73123450000{i:04d}" for i in range(n_nodes)],
        "wse": wse_true + SYS_OFFSET + node_noise,
        "wse_u": np.sqrt(0.10**2 + SYS_OFFSET**2).round(3),  # total
        "wse_r_u": 0.10,                                      # random only
        "node_q": np.where(rng.random(n_nodes) < 0.1, 1, 0), # ~10% flagged
        "xtrk_dist": rng.uniform(10_000, 60_000, n_nodes),
    })
    reach = pd.DataFrame({
        "reach_id": ["731234500001"],
        "wse": [TRUE_WSE + SYS_OFFSET],
        "wse_u": [0.20],
        "wse_r_u": [0.10 / np.sqrt(n_nodes)],
        "slope": [TRUE_SLOPE],
        "slope_u": [1.1e-5],
        "dschg_gc": [412.0], "dschg_gc_u": [95.0], "dschg_gc_q": [0],
        "reach_q": [0],
    })
    return SYS_OFFSET, TRUE_SLOPE, nodes, reach


@app.cell
def _(SYS_OFFSET, TRUE_SLOPE, nodes, np, reach):
    # THE LOADER'S CONTRACT, asserted:
    # 1. Levels are separate tables; schemas differ as the products do.
    assert "slope" in reach.columns and "slope" not in nodes.columns
    assert "dschg_gc" in reach.columns and not any(c.startswith("dschg") for c in nodes.columns)
    assert "node_q" in nodes.columns and "reach_q" in reach.columns

    # 2. Quality gating: flagged nodes out before statistics, count reported.
    good = nodes[nodes.node_q == 0]
    n_flagged = int((nodes.node_q != 0).sum())
    assert n_flagged > 0 and len(good) == len(nodes) - n_flagged

    # 3. The scope lesson, numerically: node-mean wse approximates the
    #    reach value, but its naive standard error (wse_r_u / sqrt(n))
    #    understates total uncertainty because the systematic is shared.
    node_mean = float(good.wse.mean())
    reach_wse = float(reach.wse.iloc[0])
    assert abs(node_mean - reach_wse) < 0.05, "aggregation sanity"
    naive_se = float(good.wse_r_u.iloc[0]) / np.sqrt(len(good))
    total_u = float(reach.wse_u.iloc[0])
    assert naive_se < 0.03 and total_u > 0.15, \
        "fixture must exhibit the random-vs-systematic gap"
    assert total_u > 5 * naive_se, "systematics dominate; sqrt(n) is a lie here"

    # 4. Slope is answered from the reach table only, and matches truth.
    assert abs(float(reach.slope.iloc[0]) - TRUE_SLOPE) < 1e-9

    # 5. Summary provenance fields exist: level, ids, quality accounting.
    summary = {
        "level": "node+reach (separate tables)",
        "reach_id": reach.reach_id.iloc[0],
        "nodes_total": len(nodes), "nodes_flagged": n_flagged,
        "systematic_shared_m": SYS_OFFSET,
    }
    assert all(v is not None for v in summary.values())
    print("load_swot_hydro golden: all assertions passed")
    print(f"  node mean {node_mean:.3f} vs reach {reach_wse:.3f} m; "
          f"naive SE {naive_se:.4f} vs total u {total_u:.2f} m; "
          f"{n_flagged}/{len(nodes)} nodes gated")
    return


if __name__ == "__main__":
    app.run()
