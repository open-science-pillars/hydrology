---
name: load-swot-hydro
description: Load SWOT river and lake vector products: parse region/continent, reach or node level, cycles; volume gate; quality decode; scope-aware summary.
---

# load-swot-hydro

Bring SWOT inland-water vectors into the session safely: level chosen
explicitly, gated on volume, quality-gated, scope preserved. Authored
in Session 15 per SPEC v0.6 §10; same gate contract as load-swot.

## Behavior, in order

1. **Parse and show back:** product (river reach, river node, lake
   obs/prior, raster), region AND continent code(s) (granules are
   per-continent; a region may span two), time range or cycles,
   version family per the dataset concept. The aggregation LEVEL is
   confirmed explicitly, never assumed: reach for reach-scale
   questions, node for profiles and local structure (~8x the volume).
2. **Knowledge first, restated:** the reach-node scope gotcha; the
   simulated-products check; version-family and crid notes from the
   dataset concept.
3. **Search before fetching:** granule count and estimated volume
   BEFORE any download (node granules ~41 MB, reach ~5 MB per
   pass-continent, observed 2026-07-05).
4. **The volume gate:** threshold from the project local config
   (template default 2 GB); above it, STOP with count, size,
   destination, and a smaller alternative (reach instead of node,
   fewer cycles, one continent); explicit confirmation required.
5. **Load with quality decoded:** geopandas from the zips;
   `reach_q`/`node_q`/`xovr_cal_q` gating applied and reported;
   features kept as vectors with SWORD ids intact (no premature
   rasterization).
6. **Scope-aware summary:** level, collections and crids loaded,
   cycles/passes/continents, feature counts before and after quality
   gating with dominant flag reasons, which `_u` attributes came
   along, and the concepts consulted: the provenance record.

## Must NOT

- Never download above the gate without explicit confirmation.
- Never deliver mixed reach and node features as one table.
- Never strip SWORD identifiers or quality attributes in loading.
- Never fetch a SIMULATED collection when flight data was requested.
- Never present ungated (quality-undecoded) feature statistics.
