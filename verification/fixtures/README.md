# Fixture provenance (hydrology)

Required by SPEC v0.6 §6. Current fixtures:

| Fixture | Kind | Source | License |
|---|---|---|---|
| synthetic reach/node pass (in-notebook) | synthesized deterministically inside load_swot_hydro.py (seed 20260705); attribute names mirrored from the live RiverSP D granule pair inspected 2026-07-05 (cycle 011, pass 424, AS, PGD0) | this repo | public domain (synthetic) |
| lees_ferry_00060_2023_dv.parquet (7.4 KB) | cached real subset: USGS NWIS daily discharge, site 09380000 (Colorado River at Lees Ferry, AZ), parameter 00060, calendar 2023; pulled 2026-07-05 via dataretrieval 1.2.0; regenerate with fetch_nwis_2023.py (no credentials needed) | USGS NWIS | US Government public domain |

Reference numbers the goldens assert:

- load_swot_hydro (recorded 2026-07-05): reach wse 132.580 m vs gated
  node mean 132.564 m; naive sqrt(n) SE 0.015 m vs total uncertainty
  0.20 m (shared systematics dominate by more than 5x); 6 of 50 nodes
  quality-gated; slope and discharge exist only in the reach table.
- load_nwis (measured at fixture creation, 2026-07-05): 365 days all
  qualifier A; mean 12113.6 cfs, min 6570, max 39600; with a 30-day
  synthetic provisional tail at 8000 cfs, the blended mean differs
  from the approved-only mean by more than 200 cfs (the segregation
  detector).
