# Fixture provenance (hydrology)

Required by SPEC v0.6 §6. Current fixtures:

| Fixture | Kind | Source | License |
|---|---|---|---|
| synthetic reach/node pass (in-notebook) | synthesized deterministically inside load_swot_hydro.py (seed 20260705); attribute names mirrored from the live RiverSP D granule pair inspected 2026-07-05 (cycle 011, pass 424, AS, PGD0) | this repo | public domain (synthetic) |

Reference numbers the golden asserts (recorded 2026-07-05): reach wse
132.580 m vs gated node mean 132.564 m; naive sqrt(n) SE 0.015 m vs
total uncertainty 0.20 m (shared systematics dominate by more than
5x); 6 of 50 nodes quality-gated; slope and discharge exist only in
the reach table.
