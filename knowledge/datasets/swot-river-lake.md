---
type: dataset
title: "SWOT River and Lake Single-Pass vector products (RiverSP, LakeSP)"
description: "Inland-water heights, widths, slopes, and discharge as zipped shapefiles per pass per continent; reach and node are separate collections with different attributes."
tags: [swot, rivers, lakes, riversp, lakesp, hydrology, podaac]
timestamp: 2026-07-05
resource: https://podaac.jpl.nasa.gov/dataset/SWOT_L2_HR_RiverSP_reach_D
version: "Version families C (*_2.0) and D (*_D) both live in CMR as of 2026-07-05, mirroring the LR SSH pattern; observed crid PGD0 on D granules the same day; crid varies within collections as on the ocean side"
status: verified
verified: 2026-07-05
verified_by: Paul Ramirez (steward pro tem)
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
  history); cal/val-era coverage per HR collection is unverified
  here and checked at first use.
