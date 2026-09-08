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
| basins/huc12_capitol_creek.geojson (43 KB) | Watershed Boundary Dataset unit 140100040402 (Capitol Creek, CO), inside the Roaring Fork basin; Polygon, 95.2 km2 in ESRI:102008 against areasqkm 95.15, geometry sha256 7c3cce30...; drains to 140100040403; queried 2026-09-06; regenerate with delineate_basin.py --huc 140100040402 --name huc12_capitol_creek. Chosen because it is 23,512 acres, under the OpenET Tier 1 per-request cap of 50,000, so it is the one fixture unit both evapotranspiration products can see | USGS WBD (hydro.nationalmap.gov) | US Government public domain |
| basins/huc12_padre_creek_lake_powell.geojson (59 KB) | Watershed Boundary Dataset unit 140700061004 (Padre Creek-Lake Powell, UT/AZ); Polygon, 104.6 km2 in ESRI:102008, geometry sha256 68f891fa...; drains to 140700061007; queried 2026-09-06; regenerate with delineate_basin.py --huc 140700061004 --name huc12_padre_creek_lake_powell. Chosen because half of it is reservoir: 242 of the 489 MOD16 cells inside it carry the water fill code and 14 more carry barren | USGS WBD (hydro.nationalmap.gov) | US Government public domain |
| et/mod16a2gf_roaring_fork_2023.nc (2.51 MB) | cached real subset: MOD16A2GF v061 (DOI 10.5067/MODIS/MOD16A2GF.061), `ET_500m` and `ET_QC_500m` stored RAW as int16 and uint8 (the fill codes are the point), over the Roaring Fork window on sinusoidal tile h09v05 (rows 103 to 246, cols 1548 to 1899, 144 by 352 cells, one cell of margin round the polygon's bounding box), calendar 2023, 46 composites, the last of them 5 days; 17,531 window cells inside the polygon; pulled 2026-09-06 through Cloud OPeNDAP DAP4 constraint expressions (4.27 MB transferred, 21 s, every composite by the subset route); 2-D lat and lon are stored because a sinusoidal column is not a meridian; regenerate with fetch_et_fixtures.py --basin basins/usgs_09085000_nldi.geojson (Earthdata Login with the LP DAAC application authorized) | NASA LP DAAC (MODIS/Terra) | NASA data, public (EOSDIS data use guidance) |
| et/mod16a2gf_lake_powell_2023.nc (1.31 MB) | cached real subset: MOD16A2GF v061, the same variables and year, over a Lake Powell box (bbox -111.5, 36.9 to -110.9, 37.5; tile h09v05 rows 598 to 744, cols 199 to 485, 147 by 287 cells), 46 composites; pulled 2026-09-06 (3.10 MB transferred, 21 s, subset route); kept for the fill-class case, since it holds water, barren and urban cells; regenerate with fetch_et_fixtures.py --bbox="-111.5,36.9,-110.9,37.5" --name lake_powell | NASA LP DAAC (MODIS/Terra) | NASA data, public (EOSDIS data use guidance) |
| et/openet_ensemble_huc12_capitol_creek_2023.json (2.1 KB) | recorded real response: OpenET Ensemble monthly ET over the Capitol Creek HUC12 polygon simplified to 113 ring points (tolerance 0.0005 degrees), calendar 2023, `POST https://openet-api.org/raster/timeseries/polygon`, HTTP 200 in 2.6 s on 2026-09-06 from a Tier 1 account; the request is recorded beside the answer and the key is not in the file (it travelled in the Authorization header from OPENET_API_KEY); 12 monthly values, of which January, February and March are identical | OpenET | CC-BY-4.0, attribute OpenET; cite Melton et al. 2021 |
| et/openet_ensemble_huc12_capitol_creek_2023q1_daily.json (5.6 KB) | recorded real response: the same polygon and service at the daily interval for 2023-01-01 through 2023-03-31, HTTP 200 on 2026-09-06; 90 daily values with 87 distinct, kept so the disagreement with the monthly response beside it can be recomputed | OpenET | CC-BY-4.0, attribute OpenET; cite Melton et al. 2021 |
| basins/tulare_lake_bed_wbd.geojson (722 KB) | Watershed Boundary Dataset union of subbasin 18030012 (Tulare Lake Bed, CA; loaddate 2024-08-16, tnmid {86AD0A19-0A69-4AFB-80B8-A5CC488E750D}), map service document version 3.3.0; 9,808.2 km2 in ESRI:102008 against areasqkm 9,808.23; 102 member subwatersheds, four closed, no outlet; queried 2026-09-06; regenerate with delineate_basin.py --huc 18030012 --name tulare_lake_bed_wbd | USGS WBD (hydro.nationalmap.gov) | US Government public domain |
| peaks/peaks_03451500.json (115 KB) | cached real record: USGS Water Data API `peaks` collection, USGS-03451500 (French Broad River at Asheville, NC; 945 mi2, HUC 06010105, EST with daylight saving), every row of both parameters: 130 annual peak discharges for water years 1896 through 2025 with no missing year, and 140 annual peak stages for 1796 through 2025; the discharge series carries EVENT on 2 rows and no regulation qualifier, and its largest peak, 113,000 ft3/s on 2024-09-27, is in its most recent year; pulled 2026-09-08 via dataretrieval 1.3.0 (waterdata.get_peaks, no credentials needed); regenerate with fetch_peaks_fixtures.py --site 03451500 | USGS Water Data API | US Government public domain |
| peaks/watstore_03451500_reference.txt (10.7 KB) | the WATSTORE peak file for the same gauge as the agency's own writer produces it, 140 type 3 records, from `nwis.waterdata.usgs.gov/nwis/peak?format=hn2` on 2026-09-08; frozen because that host is being decommissioned in a window from 2026-11 to 2027-02 and the export is diffed against it over the columns the frequency program reads. The three reference files carry CRLF line endings as the service serves them and are marked `-text` in .gitattributes so git does not normalise them: their recorded hashes are hashes of the bytes that were fetched, not of a rewritten copy | USGS Water Services (legacy host) | US Government public domain |
| peaks/peaks_03451000.json (95 KB) | cached real record: the same collection, USGS-03451000 (Swannanoa River at Biltmore, NC; 130 mi2, same hydrologic unit and clock), 110 annual peak discharges reaching back to water year 1791 and 110 stages; 13 of the discharges are historic, 7 have no day (6 of them saying DAYUNKNOWN, the seventh being the row whose month is unknown) and 1 has no month; pulled 2026-09-08; regenerate with fetch_peaks_fixtures.py --site 03451000 | USGS Water Data API | US Government public domain |
| peaks/watstore_03451000_reference.txt (8.4 KB) | the agency's own WATSTORE file for that gauge, 110 type 3 records, same host and date and the same reason for freezing it | USGS Water Services (legacy host) | US Government public domain |
| peaks/peaks_09380000.json (92 KB) | cached real record: the same collection, USGS-09380000 (Colorado River at Lees Ferry, AZ; 111,800 mi2, hydrologic unit 140700061105, MST), 104 annual peak discharges for water years 1884 through 2023 and 105 stages; 61 of the discharges carry REGULATED, which makes this the counterexample rather than a subject, and the 1884 peak of 210,000 ft3/s has neither month nor day; kept also because its twelve-digit hydrologic unit code shifts the station header record's later fields, which the golden asserts; pulled 2026-09-08; regenerate with fetch_peaks_fixtures.py --site 09380000 | USGS Water Data API | US Government public domain |
| peaks/watstore_09380000_reference.txt (8.0 KB) | the agency's own WATSTORE file for that gauge, 104 type 3 records, same host and date and the same reason for freezing it | USGS Water Services (legacy host) | US Government public domain |
| precipitation/imerg_final_lees_ferry_wy2021.nc (1.85 MB) | cached real subset: GPM IMERG Final daily V07 over the Lees Ferry window, water year 2021 (2020-10-01 through 2021-09-30), 365 granules all V07B, every day complete; the drought year against the wy2023 file beside it; pulled 2026-09-08 through Cloud OPeNDAP DAP4 (15.3 MB transferred, 95 s); regenerate with fetch_precipitation_fixtures.py --source imerg --run final --start 2020-10-01 --end 2021-09-30 | NASA GES DISC (GPM IMERG) | NASA data, public (EOSDIS data use guidance) |
| lees_ferry_00060_wy2021_dv.parquet (9.1 KB), lees_ferry_00060_wy2023_dv.parquet (9.6 KB) | cached real subsets: USGS Water Data API daily collection, USGS-09380000, parameter 00060, statistic 00003, by WATER year (2020-10-01/2021-09-30 and 2022-10-01/2023-09-30); 365 rows each, all Approved, no qualifiers; the gauge is below Glen Canyon Dam, so these are an operations record and the panels label them as one; pulled 2026-09-08 via dataretrieval 1.3.0; regenerate with fetch_usgs_fixtures.py --only lees_ferry_00060_wy2021_dv | USGS Water Data API | US Government public domain |
| grace/mascon_lees_ferry_wy2021.json (2.7 KB), grace/mascon_lees_ferry_wy2023.json (2.7 KB) | the Colorado above Lees Ferry extracted from the mission mascon file GRCTellus.JPL.200204_202606.GLO.RL06.3M.MSCNv04CRI.nc (45.8 MB, sha256 d5a6737b...): 14 monthly epochs per water year with their formal uncertainties, the 7 mascon ids the basin spans (the effective sample size), 282,929.6 km2 inside, and the record's last epoch 2026-06-16; extracted 2026-09-08; regenerate with fetch_mascon_fixtures.py --start 2020-10-01 --end 2021-09-30 | NASA PO.DAAC (JPL mascon RL06.3Mv04 CRI) | NASA data, public (EOSDIS data use guidance) |
| snodas/snodas_swe_lees_ferry_wy2021.json (6.3 KB), snodas/snodas_swe_lees_ferry_wy2023.json (6.3 KB) | basin snow water equivalent from SNODAS (G02158) on the first of each month of each water year, 12 dates each: the basin mean and maximum in mm, the snow-covered cell count, and each source tar's URL, size and sha256. Read from the masked tree over plain HTTPS with no credential, 134 MB and 154 MB fetched and discarded; the layer's description and scale come from the header packed beside it. A model output, kept as a comparative panel and never as a budget term; pulled 2026-09-08; regenerate with fetch_snodas_fixtures.py --dates 2020-10-01:2021-09-01:MS | NOAA NOHRSC via NSIDC | NSIDC distribution, US Government work |
| reservoir/ledger_powell_wy2023.json (62 KB) | the six citable gauge records behind the Lake Powell ledger, read out of core's capture store rather than refetched: daily pool elevation on BOTH published datums (09379900 parameters 62614 NGVD29 and 62615 NAVD88) and daily discharge at three inflow gauges (09180500, 09315000, 09379500) and the outflow (09380000), water year 2023, 365 days each, all Approved with no qualifiers. Each series carries its capture id and content hash, so the receipt cites the capture and the fixture is a copy rather than a second source; the elevation pair is kept because it is what makes the datum conversion the agency's own. Frozen 2026-09-08; regenerate with freeze_reservoir_inputs.py after taking the captures with core's obs_capture.py | USGS Water Data API, through core's capture tool | US Government public domain |
| reservoir/Lake_Powell_2018_ElevAreaCap_calc.csv (65 KB) | the elevation-area-capacity table from the 2018 topobathymetric survey, the first since 1986: 1,821 rows from 3120.08 to 3717.19 ft at a 0.33 ft step, with columns for NAVD88 and NGVD29 elevation, surface area in acres and cumulative capacity in acre-feet. USGS data release DOI 10.5066/P9O3IPG3, published 2022-03-21, reported in USGS Scientific Investigations Report 2022-5017; kept whole because it is small and because a volume from an unnamed revision is not a measurement. Fetched 2026-09-08 | USGS (ScienceBase data release) | US Government public domain |
| confrontation/swot_gauge_baton_rouge_2024.json (73 KB) | the steward-accepted reach-gauge pair frozen for confrontation: SWOT reach 74210000331 from PO.DAAC Hydrocron with the collection NAMED (`SWOT_L2_HR_RiverSP_reach_D`, 52 passes) and the same reach under `SWOT_L2_HR_RiverSP_reach_2.0` beside it (47 passes) so the version step can be recomputed rather than quoted; and USGS-07374000 (Mississippi River at Baton Rouge) instantaneous stage, parameter 00065, kept as the 386 readings falling within an hour of a pass so the pairing tolerance can be changed without refetching. Every gauge value in the window is Provisional, which the fixture records because the daily record at this gauge is approved only through 2022 while the satellite record begins in 2023. The gauge datum is NAVD88 with the datum at 0.00 ft; the satellite elevation is against a geoid model, and the offset between them is not published, which is why the confrontation scores changes. Pulled 2026-09-08; regenerate with fetch_confrontation_fixtures.py --reach 74210000331 --gauge 07374000 | PO.DAAC Hydrocron, USGS Water Data API | NASA data public (EOSDIS guidance); US Government public domain |

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
- load_et (measured 2026-09-06 at fixture creation): MOD16A2GF
  calendar 2023, fill codes excluded and the volume taken over the
  area the measured cells cover. Roaring Fork (3,767.1 km2, 17,531
  window cells inside, 1.19% masked in at least one composite):
  monthly mm 20.77, 29.88, 42.57, 54.38, 61.76, 59.86, 65.12, 54.72,
  32.31, 23.66, 23.94, 25.65, total 494.60 mm and 1.8391 km3 over
  3,718.3 km2. Capitol Creek HUC12 (95.2 km2, 438 cells, 0.0%
  masked): 521.12 mm and 0.0490 km3. Padre Creek-Lake Powell HUC12
  (104.6 km2, 489 cells, 52.35% masked, 242 water and 14 barren):
  168.72 mm and 0.0084 km3 over 50.0 km2, and the same numerator over
  all 489 cells (fill read as zero) would be 80.39 mm, 47.6% of it.
  The composite beginning 2023-12-27 is 5 days and holds 4.446 mm,
  0.889 mm a day rather than the 0.556 an eight-day reading gives.
  OpenET Ensemble monthly over Capitol Creek 2023: 28.411, 28.411,
  28.411, 59.728, 98.032, 119.907, 126.824, 96.546, 74.378, 36.920,
  17.582, 9.454 mm, total 724.60 mm, so MOD16 over OpenET is 0.7192
  for the year and 0.682 for April through December; the daily
  ensemble over the same polygon gives 11.154, 20.853 and 32.625 mm
  for January, February and March, a third less than the monthly
  series over the same quarter (ratio 1.319).
