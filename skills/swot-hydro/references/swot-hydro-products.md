# SWOT hydrology products (river, lake, raster)

Reference for the swot-hydro skill, per SPEC v0.6 §10.1-§10.2.
**ShortNames verified against live CMR 2026-07-05**; granule anatomy
below is granule-verified from live pulls the same day. The current
baseline state lives in `knowledge/datasets/swot-river-lake.md`.

## The ocean/hydro split

One instrument, two product families: KaRIn Low Rate (LR) serves
oceanography (the ocean-science plugin); High Rate (HR) serves inland
water. HR products are VECTOR (zipped shapefiles) and RASTER, not
swath NetCDF; the mental model from the ocean side does not transfer.

## River products (RiverSP)

Both version families exist, same C/D pattern as the ocean side
(`*_2.0` = Version C, `*_D` = Version D):

| ShortName family | Contents |
|---|---|
| `SWOT_L2_HR_RiverSP_reach_{2.0,D}` | reach-level aggregates (~10 km SWORD reaches): one zipped shapefile per pass per continent |
| `SWOT_L2_HR_RiverSP_node_{2.0,D}` | node-level observations (~200 m spacing along SWORD centerlines) |
| `SWOT_L2_HR_RiverSP_{2.0,D}` | umbrella carrying both |
| `SWOT_L4_HR_DAWG_SOS_DISCHARGE_V3` | Level 4 community discharge products (SoS) |

**Granule anatomy (granule-verified 2026-07-05):**
`SWOT_L2_HR_RiverSP_Reach_011_424_AS_20240229T..._PGD0_01.zip`: cycle,
pass, CONTINENT code (AS, AU, NA, ...), time span, crid, counter. The
zip holds a shapefile set (.shp/.dbf/.prj/.shx/.xml); read via
`geopandas.read_file("zip://...")`.

- Reach files: ~731 features and 127 attributes per pass-continent
  (observed): `wse/wse_u/wse_r_u`, `slope/slope_u/slope_r_u`,
  `width/width_u`, areas, and the multi-algorithm discharge family
  (`dschg_{c,gc,m,gm,b,gb,h,gh,o,go,s,gs,i,gi}` each with `_u` and
  `_q`), plus `reach_q`, `xovr_cal_q`. About 5 MB per granule.
- Node files: ~40,000 features and 57 attributes per pass-continent
  (observed): `wse/wse_u/wse_r_u`, `wse_sm*` (smoothed), `width_u`,
  `node_q`, `xtrk_dist`, `lat_u/lon_u`. About 41 MB per granule:
  **node data is roughly 8x reach volume**; gates and plans respect
  that asymmetry.

## Lake products (LakeSP)

`SWOT_L2_HR_LakeSP_{obs,prior,unassigned}_{2.0,D}` plus the umbrella:
`prior` ties observations to the Prior Lake Database, `obs` carries
observation-defined features, `unassigned` holds water detected but
not matched. Same zip-of-shapefile packaging.

## Raster products

`SWOT_L2_HR_Raster_{100m,250m}_{2.0,D}` water-mask raster images
(plus umbrella): the gridded complement for inundation work.

## Traps recorded in the bundle

- **Reach vs node scope** (gotcha): statistics quoted at the wrong
  aggregation level; see `knowledge/gotchas/swot-reach-node-scope.md`.
- **Simulated products in the same catalog:**
  `SWOT_SIMULATED_NA_CONTINENT_L2_HR_{RIVERSP,LAKESP,RASTER}_V1` are
  PRE-LAUNCH simulations; a keyword search that lands on them yields
  plausible fake data. Check for `SIMULATED` in every ShortName.
- The C/D family and crid-drift behavior mirrors the ocean side
  (swot-karin concept); cal/val-era coverage caveats apply to HR
  products as well until verified per collection.
