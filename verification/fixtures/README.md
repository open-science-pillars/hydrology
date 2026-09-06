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
| basins/usgs_03611500_nldi.geojson (398 KB) | NLDI basin trace upstream of USGS-03611500 (Ohio River at Metropolis, IL), comid 1840007, splitCatchment=false, simplified=true; MultiPolygon, 522,879.1 km2 in ESRI:102008, geometry sha256 4d84f947...; monitoring-locations drainage_area 203,000 mi2, contributing_drainage_area null; traced 2026-09-06; regenerate with delineate_basin.py --gauge 03611500 (no credentials) | USGS NLDI (api.water.usgs.gov) | US Government public domain |
| basins/usgs_09380000_nldi.geojson (253 KB) | NLDI basin trace upstream of USGS-09380000 (Colorado River at Lees Ferry, AZ), comid 20733845, same parameters; MultiPolygon, 276,443.7 km2; drainage_area 111,800 mi2, contributing null; traced 2026-09-06; regenerate with delineate_basin.py --gauge 09380000 | USGS NLDI | US Government public domain |
| basins/usgs_09085000_nldi.geojson (15 KB) | NLDI basin trace upstream of USGS-09085000 (Roaring Fork River at Glenwood Springs, CO), comid 1324997, same parameters; Polygon, 3,767.1 km2; drainage_area 1,453 mi2, contributing null; traced 2026-09-06; regenerate with delineate_basin.py --gauge 09085000 | USGS NLDI | US Government public domain |
| precipitation/imerg_final_lees_ferry_wy2023.nc (1.99 MB) | cached real subset: GPM IMERG Final daily V07 (GPM_3IMERGDF 07, DOI 10.5067/GPM/IMERGDF/DAY/07), `precipitation` (mm/day) and `precipitation_cnt` over the Lees Ferry window (lon index 679 to 744, lat 1254 to 1335, 66 by 82 cells, one cell of margin round the polygon's bounding box), 2022-10-01 through 2023-09-30, 365 granules all V07B, every day complete; 2869 of 5412 window cells inside the polygon (99.5% of its area); pulled 2026-09-06 through Cloud OPeNDAP DAP4 constraint expressions (15.5 MB transferred, 67 s, every granule by the subset route); values stored to 0.001 mm; regenerate with fetch_precipitation_fixtures.py --source imerg --run final (Earthdata Login with the GES DISC application authorized) | NASA GES DISC (GPM IMERG) | NASA data, public (EOSDIS data use guidance) |
| precipitation/imerg_late_lees_ferry_2022-10.nc (151 KB) | cached real subset: GPM IMERG Late daily V07 (GPM_3IMERGDL 07, DOI 10.5067/GPM/IMERGDL/DAY/07), the same window, 2022-10-01 through 2022-10-31, 31 granules V07B, complete; the same month as the Final fixture, kept for the calibration difference; pulled 2026-09-06 (1.27 MB, 8 s, subset route); regenerate with --run late | NASA GES DISC (GPM IMERG) | NASA data, public (EOSDIS data use guidance) |
| precipitation/imerg_late_lees_ferry_2023-10.nc (135 KB) | cached real subset: GPM IMERG Late daily V07, the same window, 2023-10-01 through 2023-10-31, 31 granules V07B, complete; the month after the Final fixture ends, kept for the declared-seam case; pulled 2026-09-06 (subset route); regenerate with --run late | NASA GES DISC (GPM IMERG) | NASA data, public (EOSDIS data use guidance) |
| precipitation/nldas2_lees_ferry_wy2023.nc (1.28 MB) | cached real subset: NLDAS-2 primary forcing hourly V2.0 (NLDAS_FORA0125_H 2.0, DOI 10.5067/THUF4J1RLSYG), `Rainf` summed to UTC days (day D is the granules D 01:00 through D+1 00:00) over the Lees Ferry window at 0.125 degree (lon index 103 to 155, lat 83 to 148, 66 by 53 cells), 2022-10-01 through 2023-09-30, 8760 granules, every day complete; 1,851 of 3,498 window cells inside the polygon (100.36% of its area); pulled 2026-09-06 (361.9 MB transferred in 3,256 s, Cloud OPeNDAP DAP4 for most granules, archive download for the ones whose subset request timed out or returned 502); values stored to 0.001 mm; regenerate with fetch_precipitation_fixtures.py --source nldas2 | NASA GES DISC (NLDAS-2) | NASA data, public (EOSDIS data use guidance) |
| basins/tulare_lake_bed_wbd.geojson (722 KB) | Watershed Boundary Dataset union of subbasin 18030012 (Tulare Lake Bed, CA; loaddate 2024-08-16, tnmid {86AD0A19-0A69-4AFB-80B8-A5CC488E750D}), map service document version 3.3.0; 9,808.2 km2 in ESRI:102008 against areasqkm 9,808.23; 102 member subwatersheds, four closed, no outlet; queried 2026-09-06; regenerate with delineate_basin.py --huc 18030012 --name tulare_lake_bed_wbd | USGS WBD (hydro.nationalmap.gov) | US Government public domain |

Basin fixtures (the four GeoJSONs under basins/): a FeatureCollection
with one feature and a top-level `provenance` member recording the
source, the request URLs as sent (no credential exists on these
hosts), the retrieval date, the NLDI parameters or the WBD units with
their loaddate and tnmid, the geometry sha256 (over the compact
sorted-key JSON of the geometry), the area and its projection, the
drainage-area comparison, and for a unit union the outlet
determination. Every number the goldens assert is read from that
member or re-measured from the geometry.

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

Precipitation window fixtures (the four netCDF files under
precipitation/): dimensions time, lat, lon over the window; global
attributes recording the collection, the DOI, the run, the DAP4
constraint expression, the window indices, the basin fixture and its
geometry sha256, the hour convention (NLDAS), the bytes transferred,
the wall time and the retrieval date; per-day string variables `run`,
`label` (the granule version label) and `route` (subset or archive)
and a per-day granule count. The loader beside them reads the run
per day from the file and checks it against the declaration; it never
trusts a filename.

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
- delineate_basin (measured 2026-09-06 at fixture creation): traces
  522,879.1, 276,443.7 and 3,767.1 km2 for 03611500, 09380000 and
  09085000 against published totals of 525,768, 289,561 and 3,763.3
  km2 (-0.55%, -4.53% with a 13,117 km2 shortfall, +0.10%); no
  published contributing area at any of the three; 4.67, 2.47 and
  0.034 GRACE mascons of 1.121e5 km2; Tulare Lake Bed 9,808.2 km2
  against areasqkm 9,808.23, 102 members, four closed, no outlet.
- load_precipitation (measured 2026-09-06 at fixture creation): IMERG
  Final water year 2023 over the Lees Ferry polygon (276,443.7 km2,
  cosine-latitude weighted mean over the 2869 cells whose centre is
  inside, 99.55% of the polygon area by cell area): monthly mm
  29.13, 16.42, 30.73, 27.28, 16.43, 44.19, 24.14, 20.04, 26.35,
  15.63, 47.58, 22.54 (October 2022 through September 2023), total
  320.44 mm and 88.585 km3; Late October 2022 44.53 mm and 12.311
  km3 against Final 29.13 mm (ratio 1.529); Late October 2023 20.78
  mm; Final September 2023 plus Late October 2023 under a per-month
  declaration carries one run seam dated 2023-10-01; NLDAS-2 forcing
  water year 2023 over the same polygon (1,851 cells inside of
  3,498, 100.36% of the area): total 374.53 mm and
  103.535 km3, monthly mm 36.53, 23.33, 43.92, 49.11, 27.04, 56.31, 19.91, 21.91, 23.80, 10.64, 41.59, 20.44; IMERG Final over NLDAS-2
  0.856 for the water year and 0.676 for November through
  March.
