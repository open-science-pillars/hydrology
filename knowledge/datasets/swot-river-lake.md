---
type: dataset
title: "SWOT River and Lake Single-Pass vector products (RiverSP, LakeSP)"
description: "Inland-water heights, widths, slopes, and discharge as zipped shapefiles per pass per continent; reach and node are separate collections with different attributes."
tags: [swot, rivers, lakes, riversp, lakesp, hydrology, podaac]
generated: { by: knowledge-seeder/claude, at: 2026-07-05T00:00:00Z }
resource: https://podaac.jpl.nasa.gov/dataset/SWOT_L2_HR_RiverSP_reach_D
version: "Version families C (*_2.0) and D (*_D) both live in CMR (swept 2026-09-04), mirroring the LR SSH pattern; the C family stops at cycle 032 (2025-05-03) and the D family carries the cal/val phase and forward processing; crid varies within collections as on the ocean side"
status: stable
upstream: pending
verified: { by: human:PaulMRamirez, at: 2026-09-04T22:36:00Z }
stale_after: 2027-01-04
sources:
  - id: cmr-sweep
    resource: "https://cmr.earthdata.nasa.gov/search/collections.json?provider=POCLOUD&short_name=SWOT_L2_HR_*&options[short_name][pattern]=true"
    title: "CMR collection sweep, provider POCLOUD, ShortName patterns SWOT_L2_HR_* and SWOT_L4_HR_*, 2026-09-04; family holdings from CMR-Hits and start-date-sorted granule searches per collection the same day"
---

# SWOT River and Lake Single-Pass vector products

**Identity.** KaRIn High Rate inland-water products: RiverSP (reach
and node collections plus an umbrella), LakeSP (obs, prior,
unassigned), water-mask rasters (100 m, 250 m), and the Level 4
community discharge products (SWOT_L4_HR_DAWG_SOS_DISCHARGE_V3).
Archive PO.DAAC. Granules are ZIPPED SHAPEFILES, one per pass per
CONTINENT (code in the filename), readable via geopandas from the zip.

**Structure (granule-verified 2026-07-05, D family, cycle 011 pass
424, continent AS).** Reach granule: 731 features, 127 attributes,
~5 MB: `wse/wse_u/wse_r_u`, `slope/slope_u/slope_r_u`,
`width/width_u`, area fields, fourteen discharge variants
(`dschg_*` each with `_u` and `_q`), `reach_q`, `xovr_cal_q`, SWORD
`reach_id`. Node granule: 40,284 features, 57 attributes, ~41 MB:
`node_id/reach_id`, `wse/wse_u/wse_r_u`, smoothed `wse_sm*`,
`width/width_u`, `node_q`, `xtrk_dist`, `lat_u/lon_u`. Node volume
runs roughly 8x reach volume per pass-continent.

## Variants

All ShortNames below were found in CMR (provider POCLOUD) by the
public sweep of 2026-09-04, exactly once each, with the concept ids
CMR reports.[^cmr-sweep] Every HR product exists in two version
families, `*_2.0` (titled Version C) and `*_D` (Version D), the
pattern the LR SSH products follow. The umbrella collections
`SWOT_L2_HR_RiverSP_2.0` (C2799438299-POCLOUD) / `SWOT_L2_HR_RiverSP_D`
(C3233944997-POCLOUD) and `SWOT_L2_HR_LakeSP_2.0` (C2799438230-POCLOUD)
/ `SWOT_L2_HR_LakeSP_D` (C3233944983-POCLOUD) are the parents of the
per-level collections; a plan names the per-level collection, never
the umbrella.

| Product | Version C ShortName (concept id) | Version D ShortName (concept id) | Contents |
|---|---|---|---|
| RiverSP reach | `SWOT_L2_HR_RiverSP_reach_2.0` (C2799438303) | `SWOT_L2_HR_RiverSP_reach_D` (C3233942283) | reach-level aggregates over the roughly 10 km SWORD reaches |
| RiverSP node | `SWOT_L2_HR_RiverSP_node_2.0` (C2799438301) | `SWOT_L2_HR_RiverSP_node_D` (C3233942282) | node-level observations about 200 m apart along the SWORD centerlines |
| LakeSP obs | `SWOT_L2_HR_LakeSP_obs_2.0` (C2799438239) | `SWOT_L2_HR_LakeSP_obs_D` (C3233942286) | observation-defined lake features |
| LakeSP prior | `SWOT_L2_HR_LakeSP_prior_2.0` (C2799438247) | `SWOT_L2_HR_LakeSP_prior_D` (C3233942291) | features tied to the Prior Lake Database |
| LakeSP unassigned | `SWOT_L2_HR_LakeSP_unassigned_2.0` (C2799438254) | `SWOT_L2_HR_LakeSP_unassigned_D` (C3233942295) | water detected but matched to no prior lake |
| Raster 100 m | `SWOT_L2_HR_Raster_100m_2.0` (C2799438280) | `SWOT_L2_HR_Raster_100m_D` (C3233942298) | water-mask raster image on a 100 m UTM grid |
| Raster 250 m | `SWOT_L2_HR_Raster_250m_2.0` (C2799438288) | `SWOT_L2_HR_Raster_250m_D` (C3233942299) | water-mask raster image on a 250 m UTM grid |

Beside these sit the cycle-averaged lines `SWOT_L2_HR_RiverAvg_{2.0,D}`
and `SWOT_L2_HR_LakeAvg_{2.0,D}`, the pixel-cloud products
`SWOT_L2_HR_PIXC_{2.0,D}` and `SWOT_L2_HR_PIXCVec_{2.0,D}`, and the
raster umbrellas `SWOT_L2_HR_Raster_{2.0,D}`: 28 HR Level 2
collections in all. The Level 4 community discharge product is
`SWOT_L4_HR_DAWG_SOS_DISCHARGE_V3` (C3905028734-POCLOUD), one
collection with no C/D split.[^cmr-sweep]

**Family holdings (granule probe of 2026-09-04).**[^cmr-sweep] The
Version C reach and node collections each hold about 32,200 granules
from cycle 001 pass 148 (2023-07-26, CRID PGC0) to cycle 032 pass 166
(2025-05-03, CRID PIC2) and stop there. The Version D collections
each hold about 68,000, from cycle 474 pass 001 (2023-03-28, CRID
PGD0) through cycle 055 pass 253 (2026-08-29, CRID PID0, forward
processing): only the D family carries the cal/val phase (the cycles
numbered in the 400s and 500s that precede the science orbit's cycle
001 of 2023-07-26), and only the D family is still growing. LakeSP
obs and prior run to the same bounds with about 30,500 (C) and 69,900
(D) granules; the 100 m raster D line holds about 1.23 million
granules, tiled by UTM zone rather than by continent. A plan that
touches the cal/val phase or any date after 2025-05-03 resolves to
the D family; a plan inside the shared science-era span states which
family it read, since the same pass carries different CRIDs in the
two.

**Granule naming.** Vector granules are named
`SWOT_L2_HR_RiverSP_Reach_<cycle>_<pass>_<continent>_<start>_<end>_<crid>_<counter>.zip`
(for example `RiverSP_Reach_011_424_AS_20240229T..._PGD0_01`): cycle,
pass, the two-letter continent code (AS, AU, EU, NA, SI, and the
rest), the time span, the CRID, and a product counter; the Node files
and the LakeSP Obs, Prior, and Unassigned files follow the same
shape. The zip holds one shapefile set (.shp, .dbf, .prj, .shx, .xml)
that `geopandas.read_file("zip://...")` reads directly. Raster
granules carry the UTM zone in place of the continent
(`Raster_100m_UTM35S_N_x_x_x_474_001_107F_...`).

## Uncertainty

- Both levels carry `wse_u` (TOTAL height uncertainty) and `wse_r_u`
  (the RANDOM component); the difference is the correlated systematic
  part, so averaging nodes along a reach shrinks `wse_r_u`-style
  noise but not the shared systematics. Widths and areas carry their
  own `_u`; reach slopes carry `slope_u/slope_r_u`.
- Discharge variants each carry their own `_u` and `_q`; the variants
  are different algorithms, not repeated measurements, and their
  spread is algorithmic disagreement, not sampling error.
- Quality attributes (`reach_q`, `node_q`, `xovr_cal_q`,
  `wse_sm_q`) are categorical gates, not quantitative uncertainty
  (core QC rule).

## Known issues

- [swot-reach-node-scope](../gotchas/swot-reach-node-scope.md).
- Simulated pre-launch collections
  (`SWOT_SIMULATED_NA_CONTINENT_L2_HR_*_V1`) share the catalog;
  any ShortName containing SIMULATED is synthetic, never flight data.
- The C/D version-family split and crid drift mirror the LR SSH
  products (the ocean bundle's swot-karin concept records that
  history); the Variants section above records which family carries
  the cal/val era, from the 2026-09-04 granule probe.

[^cmr-sweep]: CMR collection sweep and granule probe, provider POCLOUD, 2026-09-04
