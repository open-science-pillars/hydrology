# Fixture provenance (hydrology)

Required by the fixture-provenance rule (every fixture's source,
version, and license recorded). Current fixtures:

| Fixture | Kind | Source | License |
|---|---|---|---|
| synthetic reach/node pass (in-notebook) | synthesized deterministically inside load_swot_hydro.py (seed 20260705); attribute names mirrored from the live RiverSP D granule pair inspected 2026-07-05 (cycle 011, pass 424, AS, PGD0) | this repo | public domain (synthetic) |
| lees_ferry_00060_2023_dv.parquet (9.6 KB) | cached real subset: USGS Water Data API daily collection, USGS-09380000 (Colorado River at Lees Ferry, AZ), parameter 00060, statistic 00003, calendar 2023; 365 rows, all Approved, no qualifier; pulled 2026-09-06 via dataretrieval 1.3.0 (waterdata module); row count and every value checked against the 2026-07-05 legacy-service capture of the same window (365 of 365 identical); regenerate with fetch_usgs_fixtures.py (no credentials needed) | USGS Water Data API | US Government public domain |
| powell_62614_2023_dv.parquet (9.7 KB) | cached real subset: USGS Water Data API daily collection, USGS-09379900 (Lake Powell at Glen Canyon Dam, AZ), parameter 62614 (lake elevation, ft), statistic 00003, calendar 2023; 365 rows, all Approved, no qualifier; pulled 2026-09-06 via dataretrieval 1.3.0; regenerate with fetch_usgs_fixtures.py | USGS Water Data API | US Government public domain |
| roaring_fork_00060_2021_dv.parquet (10.3 KB) | cached real subset: USGS Water Data API daily collection, USGS-09085000 (Roaring Fork River at Glenwood Springs, CO), parameter 00060, statistic 00003, calendar 2021; 365 rows, all Approved, 8 carrying the ESTIMATED qualifier; pulled 2026-09-06 via dataretrieval 1.3.0; regenerate with fetch_usgs_fixtures.py | USGS Water Data API | US Government public domain |
| roaring_fork_00060_2023_dv.parquet (10.4 KB) | cached real subset: same site and parameter, calendar 2023; 365 rows, all Approved, 20 ESTIMATED; pulled 2026-09-06 via dataretrieval 1.3.0; regenerate with fetch_usgs_fixtures.py | USGS Water Data API | US Government public domain |
| roaring_fork_00060_clim9120_dv.parquet (87.4 KB) | cached real subset: same site and parameter, 1991-01-01 through 2020-12-31 (the drought-index recipe's climatology window); 10958 rows, all Approved, 609 ESTIMATED; pulled 2026-09-06 via dataretrieval 1.3.0; regenerate with fetch_usgs_fixtures.py | USGS Water Data API | US Government public domain |

Fixture schema (the five USGS parquets): one row per day with the
columns `monitoring_location_id` (agency-prefixed string,
`USGS-09380000`), `parameter_code`, `statistic_id` (`00003`, daily
mean), `time_series_id`, `time` (the API's date string), `value`
(float64), `unit_of_measure` (`ft^3/s` or `ft`), `approval_status`
(`Approved` or `Provisional`), `qualifier` (a sorted list such as
`["ESTIMATED"]`, or null when the API reports none) and
`last_modified`. Approval and qualifier are separate columns on this
API: an ESTIMATED day is still Approved. The geometry and per-row id
the API also returns are dropped. Earlier fixtures (pulled 2026-07-05
from the legacy Water Services endpoint) carried the dataretrieval
nwis column layout (`00060_Mean`, `00060_Mean_cd`, `site_no`); the
2026-09-06 refetch replaced them, and every recorded anchor below was
re-measured identical on the new fixtures.

Reference numbers the goldens assert:

- load_swot_hydro (recorded 2026-07-05): reach wse 132.580 m vs gated
  node mean 132.564 m; naive sqrt(n) SE 0.015 m vs total uncertainty
  0.20 m (shared systematics dominate by more than 5x); 6 of 50 nodes
  quality-gated; slope and discharge exist only in the reach table.
- load_nwis (measured 2026-07-05 at fixture creation, re-measured
  2026-09-06 on the Water Data API fixture, identical): 365 days all
  Approved with no qualifier; mean 12113.6 cfs, min 6570, max 39600;
  with a 30-day synthetic Provisional tail at 8000 cfs, the blended
  mean differs from the approved-only mean by more than 200 cfs (the
  segregation detector; measured 312 cfs).
- drought_analysis (measured 2026-07-05, re-measured 2026-09-06,
  identical): daily percentile-of-climatology index, approved days
  only; 2021 median 13.3, fraction below the 30th percentile 0.92,
  below the 10th 0.28; 2023 median 33.3, 0.39, 0.05; separation 20.0
  points.
- reservoir_storage (measured 2026-07-05, re-measured 2026-09-06,
  identical): Lake Powell 2023 elevation 3524.40 ft on 1 January to
  3568.60 ft on 31 December (+44.20 ft); minimum 3519.50 (mid April),
  maximum 3584.30 (July); within-year swing 64.8 ft.
