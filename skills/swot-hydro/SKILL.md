---
name: swot-hydro
description: "SWOT river and lake products: RiverSP reach vs node scope, LakeSP obs/prior, raster water masks, zipped-shapefile access, discharge products."
user-invocable: false
---

# swot-hydro

Background expertise for SWOT inland-water products. Product inventory and granule anatomy
live in `references/swot-hydro-products.md` (CMR- and
granule-verified 2026-07-05); baseline state lives in
`knowledge/datasets/swot-river-lake.md`.

## Knowledge first

Before any SWOT hydrology analysis, consult and restate:

1. `knowledge/datasets/swot-river-lake.md`: version families, current
   baselines, and the Uncertainty section (which `_u` attributes exist
   at each aggregation level and what they omit).
2. `knowledge/gotchas/swot-reach-node-scope.md`: EVERY river statistic
   names its aggregation level (reach or node) first; the levels are
   different collections with different attributes and an ~8x volume
   asymmetry.

## Working rules

- **Vector, not swath:** RiverSP/LakeSP granules are zipped shapefiles
  per pass per continent; read via geopandas from the zip; the
  continent code is part of the granule identity.
- **Scope before statistics:** reach aggregates and node observations
  answer different questions; a "river height" without its level is
  not a result. Discharge lives at reach level in multi-algorithm
  variants, each with its own `_u` and `_q`; quoting discharge means
  naming the algorithm variant.
- **Quality gates:** `reach_q`/`node_q` and `xovr_cal_q` gate
  features before statistics (core QC rules apply to attributes as
  much as pixels).
- **Uncertainty attributes travel:** `wse_u` (total) vs `wse_r_u`
  (random component) at both levels; the house rule quotes them with
  results, with the distinction stated.
- **Simulated-product check:** any ShortName containing SIMULATED is
  pre-launch synthetic data, never mixed with flight data.
- Loading is load-swot-hydro's job (gate, decode, scope-aware
  summary); this skill supplies what it restates.

## Must NOT

- Never quote a river or lake statistic without its aggregation level.
- Never mix reach and node values in one series or comparison without
  stating the level change.
- Never use SIMULATED collections as observations.
- Never quote a discharge without naming the algorithm variant and its
  quality flag.
- Never hardcode baselines; the dataset concept records them with
  verification dates.
