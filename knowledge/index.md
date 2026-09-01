---
okf_version: "0.2"
---

# hydrology bundle

The hydrology knowledge bundle. OKF v0.2 conformant (okf_version:
"0.2"; the vendored spec text lives in marketplace docs/upstream). The
pinned podaac copies below follow SPEC §5.7:

- Snapshot source repository: github.com/open-science-pillars/nasa-daac-knowledge (podaac/, the CANONICAL home per §5.7)
- Snapshot source commit: 1b8dd064d68d (files byte-identical; re-synced 2026-08-31)
- Snapshot date: 2026-08-31 (refresh at every hydrology release per §5.7; canonical concept wins on conflict)

## snapshot-podaac (pinned copies, §5.7)

- [GRACE/GRACE-FO JPL mascon solutions](snapshot-podaac/datasets/grace-fo-mascons.md), snapshot
- [GRACE mascon coastal leakage](snapshot-podaac/gotchas/grace-coastal-leakage.md), snapshot
- [GRACE GIA correction](snapshot-podaac/gotchas/grace-gia-correction.md), snapshot

## datasets

- [SWOT River and Lake Single-Pass vector products (RiverSP, LakeSP)](datasets/swot-river-lake.md), status: stable
- [USGS NWIS streamflow (daily and instantaneous values)](datasets/nwis-streamflow.md), status: stable
- [SMAP L3 radiometer soil moisture (SPL3SMP, SPL3SMP_E)](datasets/smap-l3.md), status: stable

## gotchas

- [RiverSP reach vs node: statistics quoted at the wrong aggregation level](gotchas/swot-reach-node-scope.md), severity high, status: stable
- [Regulated gauges: flow statistics measure operations, not hydrology](gotchas/nwis-regulated-gauge.md), severity high, status: stable
- [NWIS provisional data: recent values are revisable and flagged P](gotchas/nwis-provisional-data.md), severity high, status: stable
- [SMAP radar loss (July 2015): the product lineage breaks](gotchas/smap-radar-loss.md), severity high, status: stable

## recipes

- [Streamflow drought index: day-of-year percentiles at a reference gauge](recipes/drought-index.md), status: stable
- [Reservoir level change from gauge elevation: Lake Powell 2023](recipes/reservoir-storage-change.md), status: stable
- [GRACE-FO groundwater from terrestrial water storage: the partitioning residual](recipes/grace-groundwater-partitioning.md), status: stable

## connectors

- [USGS NWIS stream gauges](connectors/usgs-water.md), status: draft
- [PO.DAAC Hydrocron SWOT river series](connectors/hydrocron-swot.md), status: draft
