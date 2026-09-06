---
okf_version: "0.2"
---

# hydrology bundle

The hydrology knowledge bundle. OKF v0.2 conformant (okf_version:
"0.2"; the vendored spec text lives in marketplace docs/upstream).

The GRACE concepts this plugin's skills rely on (the mascon dataset,
the coastal leakage and GIA correction gotchas) live in the PO.DAAC
provider bundle, canonical home
github.com/open-science-pillars/nasa-daac-knowledge (knowledge/podaac/),
installed alongside this plugin as the nasa-daac-knowledge dependency
at a release the plugin names a floor for; nothing from it is copied
here. The core skill consult-knowledge finds every installed bundle
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

## gotchas

- [RiverSP reach vs node: statistics quoted at the wrong aggregation level](gotchas/swot-reach-node-scope.md), severity high, status: stable
- [Regulated gauges: flow statistics measure operations, not hydrology](gotchas/nwis-regulated-gauge.md), severity high, status: stable
- [NWIS provisional data: recent values are revisable and flagged Provisional](gotchas/nwis-provisional-data.md), severity high, status: stable
- [SMAP radar loss (July 2015): the product lineage breaks](gotchas/smap-radar-loss.md), severity high, status: stable
- [NLDI unsnapped point: a coordinate answers for the nearest flowline, not the river you meant](gotchas/nldi-unsnapped-point.md), severity high, status: stable
- [Terminal basins: a closed hydrologic unit has no outlet, and a tool that expects one names the wrong river](gotchas/usgs-terminal-basin-no-outlet.md), severity medium, status: stable
- [IMERG run mixing: three calibrations under one variable name, and a Final record that ends in September 2025](gotchas/imerg-run-mixing.md), severity high, status: stable
- [IMERG cold-season underestimation over snow and mountains: values present, quality reduced, and NLDAS-2 forcing as the check](gotchas/imerg-cold-season-orographic-underestimation.md), severity high, status: stable

## recipes

- [Streamflow drought index: day-of-year percentiles at a reference gauge](recipes/drought-index.md), status: stable
- [Reservoir level change from gauge elevation: Lake Powell 2023](recipes/reservoir-storage-change.md), status: stable
- [GRACE-FO groundwater from terrestrial water storage: the partitioning residual](recipes/grace-groundwater-partitioning.md), status: stable

## connectors

- [USGS stream gauges: the Water Data API (observations server and dataretrieval)](connectors/usgs-water.md), status: stable
- [PO.DAAC Hydrocron SWOT river series](connectors/hydrocron-swot.md), status: stable
- [USGS NLDI basin tracing: the polygon upstream of a gauge or a snapped point](connectors/nldi-basin.md), status: stable
- [GES DISC through earthaccess: Earthdata Login plus a one-time application authorization, and the window pull over Cloud OPeNDAP](connectors/gesdisc-earthaccess.md), status: stable
