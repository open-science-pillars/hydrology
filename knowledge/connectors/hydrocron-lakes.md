---
type: connector
title: "PO.DAAC Hydrocron SWOT lake series (observations server)"
description: "SWOT lake water surface elevation and area per prior-database lake through hydrocron_lake_timeseries: the PriorLake feature, the lake_id of the prior lake database, a D-family prior-lake collection named by the tool rather than defaulted by the service, fifty accepted field names probed one by one, and units that travel with every row."
tags: [connector, hydrocron, swot, lakes, lakesp, podaac, mcp, observations]
generated: { by: process:claude-code, at: 2026-09-15T14:00:00Z }
status: draft
citation:
  access_date_required: true
  authority: https://podaac.jpl.nasa.gov/
  data: "SWOT Level 2 Lake Single-Pass Vector Data Product, prior lake collection SWOT_L2_HR_LakeSP_prior_D, NASA PO.DAAC, accessed {access_date} via Hydrocron"
  software: "podaac/hydrocron (software), https://doi.org/10.5281/zenodo.11176233"
  note: "cite the collection Hydrocron served at access (the tool returns the name it used) and the Hydrocron software DOI beside it; the product DOI is on the PO.DAAC landing page, which was not reachable from the drafting session and is to be added on review"
stale_after: 2027-03-15
sources:
  - id: service-probe
    resource: "https://soto.podaac.earthdatacloud.nasa.gov/hydrocron/v1/timeseries?feature=PriorLake&feature_id=6350036102&start_time=2024-01-01T00:00:00Z&end_time=2024-06-30T00:00:00Z&fields=lake_id,time_str,wse,area_total,quality_f&collection_name=SWOT_L2_HR_LakeSP_prior_D"
    title: "Live probe 2026-09-15 of the timeseries endpoint for PriorLake 6350036102 (lake_name LAGOA GUA CLARA, near 19.82S 42.59W): 15 passes between 2024-01-17 and 2024-06-30 in 63 ms, the first at 260.889 m with area 0.575579 km^2 and quality_f 0; wse_units m and area_total_units km^2 returned beside the values; anonymous"
  - id: fields-probe
    resource: https://soto.podaac.earthdatacloud.nasa.gov/hydrocron/v1/timeseries
    title: "Field acceptance probed one name at a time on 2026-09-15 against the prior-lake D collection: fifty names accepted (lake_id, reach_id, obs_id, overlap, n_overlap, time, time_tai, time_str, wse, wse_u, wse_r_u, wse_std, area_total, area_tot_u, area_detct, area_det_u, layovr_val, xtrk_dist, ds1_l, ds1_q, ds2_l, ds2_q, quality_f, dark_frac, ice_clim_f, ice_dyn_f, partial_f, xovr_cal_q, geoid_hght, solid_tide, load_tidef, load_tideg, pole_tide, dry_trop_c, wet_trop_c, iono_c, xovr_cal_c, lake_name, p_res_id, p_lon, p_lat, p_ref_wse, p_ref_area, p_date_t0, p_ds_t0, p_storage, cycle_id, pass_id, continent_id, crid, collection_shortname, collection_version, granuleUR, ingest_time); sword_version refused with the 400 'fields parameter should contain valid SWOT fields'; an unknown collection_name refused with the 400 that lists the ten collections the service serves"
  - id: dataset
    resource: ../datasets/swot-river-lake.md
    title: "This bundle's SWOT RiverSP and LakeSP dataset concept: the LakeSP obs, prior and unassigned collections, the C and D families, zipped shapefiles per pass per continent"
  - id: collection-default
    resource: ../gotchas/hydrocron-collection-default.md
    title: "This bundle's gotcha on the service's default collection: the default moved between product versions and the versions differ by metres, so the tool names the collection"
  - id: river-connector
    resource: hydrocron-swot.md
    title: "This bundle's Hydrocron river connector: the EGM2008 geoid reference of wse, the large negative fill values, and the standalone file"
  - id: server
    resource: https://github.com/open-science-pillars/core/blob/9fad9ab515e05aef5be73076ef24ca4a9ad83f5f/connectors/observations_mcp.py
    title: "The observations server carrying hydrocron_lake_timeseries (contract 0.5.0); the recorded fixture is the probed lake's 2024-01 to 2024-06 window"
---

# PO.DAAC Hydrocron SWOT lake series

`hydrocron_lake_timeseries` fetches SWOT lake time series (water
surface elevation, total area, their uncertainties and the quality,
partial-observation, dark-water and ice flags by default) for one lake
of the prior lake database from PO.DAAC's Hydrocron API, anonymous
over HTTPS, as the `PriorLake` feature.[^service-probe] Verified live
2026-09-15: fifteen passes over one Brazilian lake in the first half of
2024 in under a tenth of a second, each row carrying its units
(`wse_units` m, `area_total_units` km^2).[^service-probe]

**The collection is named, not defaulted.** The service accepts a
`collection_name` and picks one when the request omits it, and the
default has moved between product versions that differ by
metres.[^collection-default] The tool therefore sends
`SWOT_L2_HR_LakeSP_prior_D` when the caller names nothing, returns
the name it used, and refuses a name outside the ten the service
lists in its own 400 before sending it.[^fields-probe][^server] The
LakeSP family has obs, prior and unassigned collections; Hydrocron
serves the prior one, keyed by `lake_id`, the prior lake database
identifier.[^dataset][^service-probe]

**Fields the service accepts (probed 2026-09-15).** Fifty names
answered 200 against the prior-lake D collection, among them the
elevation and its uncertainties (`wse`, `wse_u`, `wse_r_u`,
`wse_std`), the areas (`area_total`, `area_tot_u`, `area_detct`,
`area_det_u`), the storage-change fields (`ds1_l`, `ds1_q`, `ds2_l`,
`ds2_q`), the flags (`quality_f`, `partial_f`, `dark_frac`,
`ice_clim_f`, `ice_dyn_f`, `xovr_cal_q`), the geophysical corrections
(`geoid_hght`, `solid_tide`, `load_tidef`, `load_tideg`, `pole_tide`,
the troposphere and ionosphere terms), the prior-database attributes
(`lake_name`, `p_lon`, `p_lat`, `p_ref_wse`, `p_ref_area`,
`p_storage`) and the granule provenance (`cycle_id`, `pass_id`,
`crid`, `collection_shortname`, `collection_version`, `granuleUR`).
`sword_version` is refused: lakes are not SWORD
features.[^fields-probe] An unknown field name is a 400 with the
service's message and no list, so the accepted names above are the
record.[^fields-probe]

**Three facts before science.** Elevations are on the EGM2008 geoid
(the `geoid_hght` field is the height the correction used), fill
values are large negatives that must be filtered rather than
averaged, and a lake observed in part (`partial_f`) or under a high
dark-water fraction carries an area the flags qualify.[^river-connector][^fields-probe]
The lake series and a reservoir gauge sit on different datums; the
datum gotcha in this bundle measures the size of that
difference.[^dataset]

**What was not read.** The Hydrocron documentation host was not
reachable from the drafting session (the JPL host answered 502 through
the session's proxy and the GitHub Pages mirror is outside the
session's policy), so the field list and the error shapes above come
from the live service, probed name by name, and not from the
documentation.[^fields-probe]

**Composition.** The satellite lake series beside the reservoir gauge
of record and the area-capacity table: the reservoir ledger's
elevation term, with its datum difference stated.[^server]

[^service-probe]: live probe of PriorLake 6350036102, 2026-09-15
[^fields-probe]: field acceptance probed name by name against the live service, 2026-09-15
[^dataset]: this bundle's SWOT RiverSP and LakeSP dataset concept
[^collection-default]: this bundle's gotcha on the Hydrocron default collection
[^river-connector]: this bundle's Hydrocron river connector
[^server]: the observations server source
