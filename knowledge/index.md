---
okf_version: "0.2"
---

# hydrology bundle

The hydrology knowledge bundle. OKF v0.2 conformant (okf_version:
"0.2"; the vendored spec text lives in marketplace docs/upstream).

The GRACE concepts this plugin's skills rely on (the mascon dataset
concept and its four gotchas: coastal leakage, the GIA correction, the
inter-mission gap and the degree-1 and C20/C30 replacements, and the
mass-to-sea-level recipe the gain-factor gotcha cites) live in the
PO.DAAC provider bundle, canonical home
github.com/open-science-pillars/nasa-daac-knowledge (knowledge/podaac/),
installed alongside this plugin as the nasa-daac-knowledge dependency
at a release the plugin names a floor for; nothing from it is copied
here: this bundle's GRACE recipe and gotchas cite those concepts at a
pinned commit and carry only the granule's own variable-level facts. The core skill consult-knowledge finds every installed bundle
through the installer's record of installed plugins and globs each
root the same way; this plugin cites provider concepts by bundle path,
`knowledge/podaac/<type>/<concept>.md`. The provider concept wins on
conflict.

## datasets

- [SWOT River and Lake Single-Pass vector products (RiverSP, LakeSP)](datasets/swot-river-lake.md), status: stable
- [USGS NWIS streamflow (daily and instantaneous values)](datasets/nwis-streamflow.md), status: stable
- [SMAP L3 radiometer soil moisture (SPL3SMP, SPL3SMP_E)](datasets/smap-l3.md), status: stable
- [USGS Watershed Boundary Dataset (WBD): hydrologic units from HUC2 to HUC12](datasets/usgs-wbd.md), status: stable
- [GPM IMERG V07 daily precipitation: three runs, one variable name, and a Final record that ends in September 2025](datasets/imerg-v07.md), status: stable
- [NLDAS-2 primary forcing precipitation: the gauge-based hourly field over the conterminous United States](datasets/nldas2-forcing.md), status: stable
- [MOD16A2GF v061 evapotranspiration: an 8-day total in millimetres, seven fill codes for the land it does not compute, and a record that only advances at year end](datasets/mod16a2gf.md), status: stable
- [USGS annual peak streamflow (the peaks collection)](datasets/usgs-peaks.md), status: stable
- [Reservoir area-capacity tables: a survey, not a constant, and Lake Powell's is four per cent smaller than it was](datasets/reclamation-area-capacity.md), status: draft
- [MODIS and VIIRS daily snow cover (MOD10A1 v61, MOD10A1F v61, VNP10A1 v2): an NDSI index per cell, flag codes above 100, one overpass per day](datasets/modis-viirs-snow-cover.md), status: stable
- [SWOT lake products: the Prior Lake Database, the LakeSP single-pass files and the LakeAvg cycle average, as a water surface elevation and area series per prior lake](datasets/swot-lakes.md), status: stable

## gotchas

- [RiverSP reach vs node: statistics quoted at the wrong aggregation level](gotchas/swot-reach-node-scope.md), severity high, status: stable
- [Regulated gauges: flow statistics measure operations, not hydrology](gotchas/nwis-regulated-gauge.md), severity high, status: stable
- [NWIS provisional data: recent values are revisable and flagged Provisional](gotchas/nwis-provisional-data.md), severity high, status: stable
- [SMAP radar loss (July 2015): the product lineage breaks](gotchas/smap-radar-loss.md), severity high, status: stable
- [NLDI unsnapped point: a coordinate answers for the nearest flowline, not the river you meant](gotchas/nldi-unsnapped-point.md), severity high, status: stable
- [Terminal basins: a closed hydrologic unit has no outlet, and a tool that expects one names the wrong river](gotchas/usgs-terminal-basin-no-outlet.md), severity medium, status: stable
- [IMERG run mixing: three calibrations under one variable name, and a Final record that ends in September 2025](gotchas/imerg-run-mixing.md), severity high, status: stable
- [IMERG cold-season underestimation over snow and mountains: values present, quality reduced, and NLDAS-2 forcing as the check](gotchas/imerg-cold-season-orographic-underestimation.md), severity high, status: stable
- [MOD16 fill codes over water, barren and urban land: seven codes, one in the header, and none of them a zero](gotchas/mod16-fill-over-water-barren-urban.md), severity high, status: stable
- [The OpenET area cap: a basin request is refused, not sampled, and no basin mean comes back](gotchas/openet-area-cap.md), severity high, status: stable
- [MOD16 composites into calendar months: the periods straddle month ends and the last one of the year is five or six days](gotchas/mod16-composite-to-month.md), severity medium, status: stable
- [The OpenET provisional window: the last 120 days will change, and a receipt without its access date cannot be reproduced](gotchas/openet-provisional-window.md), severity medium, status: stable
- [One peaks response holds two series, and they are not the same event](gotchas/peaks-two-series-one-response.md), severity high, status: stable
- [A log-Pearson III fit computed in a session is a screening number, not a flood frequency estimate](gotchas/screening-fit-is-not-bulletin-17c.md), severity high, status: stable
- [SNODAS is a model output: comparable between periods, not a term in a water budget](gotchas/snodas-not-a-budget-term.md), severity high, status: stable
- [A satellite lake elevation and a gauge elevation are on different datums, and the difference between them is mostly the datum](gotchas/swot-gauge-datum-mismatch.md), severity high, status: draft
- [Hydrocron picks a product version when you do not, and the versions differ by metres](gotchas/hydrocron-collection-default.md), severity high, status: stable
- [The OpenET monthly ensemble is not always the sum of its own days: three repeated months over Colorado headwater units in 2023](gotchas/openet-monthly-not-the-daily-sum.md), severity medium, status: stable
- [A basin near or below one mascon has no GRACE series of its own: the values are the neighbourhood's and the constraint's, and nothing errors](gotchas/grace-basin-below-resolution-floor.md), severity high, status: stable
- [GRACE terrestrial water storage is every store together: a groundwater trend from GRACE minus a land surface model inherits the model's soil moisture and snow errors as a term](gotchas/grace-tws-is-total-storage.md), severity medium, status: stable
- [The mascon gain factors: applied once, to the CRI grid, for land hydrology, and meaningless over ice and ocean](gotchas/grace-scale-factors-once-and-for-hydrology.md), severity medium, status: stable
- [NDSI snow cover is an index thresholded into snow, not a fraction of the cell: a value of 40 is not 40 per cent snow, and the codes above 100 are not values](gotchas/snow-cover-ndsi-is-not-fraction.md), severity high, status: stable
- [Cloud hides snow on the days snow changes, and the gap-filled product reuses an older view whose age is a field the reader has to consult](gotchas/snow-cover-cloud-persistence-and-gap-filling.md), severity medium, status: stable
- [Snow and cloud are confused in both directions, and the algorithm flags name the cases: a cloud fringe read as snow, thin plains snow masked as cloud, and neither reversed by a screen](gotchas/snow-cover-snow-cloud-confusion.md), severity medium, status: stable
- [A daily snow cover tile is one overpass per cell at the platform's local solar time, chosen by nearest solar noon, nearest nadir and most coverage, not a daily mean or a daily maximum](gotchas/snow-cover-overpass-time-and-compositing.md), severity medium, status: stable
- [Snow cover is where the snow is, not how much: an observed NDSI index and SNODAS's modelled snow water equivalent are different quantities that arrive as daily grids of the same shape](gotchas/snow-cover-is-not-swe.md), severity low, status: stable
- [A SWOT lake series is keyed on the prior lake identifier in the prior file: the observed identifier is new every pass, a merged water body carries a semicolon list of prior identifiers, and an equality filter on the obs file silently drops the passes where lakes joined](gotchas/swot-lake-identity-across-passes.md), severity high, status: draft
- [A SWOT lake elevation is a height above the EGM2008 geoid in the mean-tide system with three tide models removed: the Version C geoid carried an error of up to half a metre that Version D fixed, and the prior reference elevation is a catalogue value, not an observation](gotchas/swot-lake-elevation-datum.md), severity medium, status: stable

## computations

- [Basin water balance from observations: P + I - ET - Q - X = dS, with a footprint floor that refuses small basins](computations/basin-water-balance.md), status: stable

## recipes

- [Basin water balance: when the identity can be closed from observations, and what it refuses](recipes/basin-water-balance.md), status: stable
- [Event reconstruction: a receipted timeline for an event no budget can close](recipes/event-reconstruction.md), status: stable
- [Drought anatomy: five panels, five sets of facts, and no single number](recipes/drought-anatomy.md), status: stable
- [Reservoir ledger: a budget in volume units that reports its residual instead of closing](recipes/reservoir-ledger.md), status: draft
- [Confronting a satellite river elevation with a gauge: score the changes, publish the level difference, call neither a bias](recipes/swot-gauge-confrontation.md), status: stable
- [Streamflow drought index: day-of-year percentiles at a reference gauge](recipes/drought-index.md), status: stable
- [Reservoir level change from gauge elevation: Lake Powell 2023](recipes/reservoir-storage-change.md), status: stable
- [GRACE-FO groundwater from terrestrial water storage: the partitioning residual](recipes/grace-groundwater-partitioning.md), status: stable
- [A basin's terrestrial water storage anomaly from the JPL mascon CRI grid: whole mascons, one pass of the gain factors, the formal error as a floor, and a trend fit around the holes](recipes/grace-basin-tws.md), status: stable
- [Choosing a precipitation product by terrain and question: IMERG, Daymet, MERRA-2 and NLDAS-2 in complex terrain, at high latitude, in the cold season, for extremes and for long series, with a second product run beside the first as the check](recipes/precipitation-product-by-terrain.md), status: stable

## connectors

- [USGS stream gauges: the Water Data API (observations server and dataretrieval)](connectors/usgs-water.md), status: stable
- [USGS groundwater levels: the Water Data API field-measurements collection](connectors/nwis-groundwater.md), status: stable
- [PO.DAAC Hydrocron SWOT river series](connectors/hydrocron-swot.md), status: stable
- [PO.DAAC Hydrocron SWOT lake series](connectors/hydrocron-lakes.md), status: stable
- [USGS NLDI basin tracing: the polygon upstream of a gauge or a snapped point](connectors/nldi-basin.md), status: stable
- [GES DISC through earthaccess: Earthdata Login plus a one-time application authorization, and the window pull over Cloud OPeNDAP](connectors/gesdisc-earthaccess.md), status: stable
- [The OpenET API: a key in a header, a per-request area cap that no basin clears, and a 120-day window in which values change](connectors/openet-api.md), status: stable
- [SNODAS: a registered collection with no granules, served from a dated directory](connectors/snodas-nsidc.md), status: stable
- [The NOAA National Water Model retrospective, version 3.0, on AWS](connectors/nwm-retrospective.md), status: stable
