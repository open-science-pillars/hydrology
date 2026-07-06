# hydrology bundle

The hydrology knowledge bundle (SPEC v0.6 §10.2). The pinned podaac
snapshot fields land with Sessions 16-17 (§5.7):

- Snapshot source repository: github.com/open-science-pillars/nasa-daac-knowledge (podaac/, the CANONICAL home per §5.7)
- Snapshot source commit: a0c84fff959f (files byte-identical; sync_check run green 2026-07-05)
- Snapshot date: 2026-07-05 (refresh at every hydrology release per §5.7; canonical concept wins on conflict)

## snapshot-podaac (pinned copies, §5.7)

- [GRACE/GRACE-FO JPL mascon solutions](snapshot-podaac/datasets/grace-fo-mascons.md), snapshot
- [GRACE mascon coastal leakage](snapshot-podaac/gotchas/grace-coastal-leakage.md), snapshot
- [GRACE GIA correction](snapshot-podaac/gotchas/grace-gia-correction.md), snapshot

## datasets

- [SWOT River and Lake Single-Pass vector products (RiverSP, LakeSP)](datasets/swot-river-lake.md), status: verified
- [USGS NWIS streamflow (daily and instantaneous values)](datasets/nwis-streamflow.md), status: verified
- [SMAP L3 radiometer soil moisture (SPL3SMP, SPL3SMP_E)](datasets/smap-l3.md), status: verified

## gotchas

- [RiverSP reach vs node: statistics quoted at the wrong aggregation level](gotchas/swot-reach-node-scope.md), severity high, status: verified
- [Regulated gauges: flow statistics measure operations, not hydrology](gotchas/nwis-regulated-gauge.md), severity high, status: verified
- [NWIS provisional data: recent values are revisable and flagged P](gotchas/nwis-provisional-data.md), severity high, status: verified
- [SMAP radar loss (July 2015): the product lineage breaks](gotchas/smap-radar-loss.md), severity high, status: verified

## recipes

- [Streamflow drought index: day-of-year percentiles at a reference gauge](recipes/drought-index.md), status: verified
- [Reservoir level change from gauge elevation: Lake Powell 2023](recipes/reservoir-storage-change.md), status: verified
- [GRACE-FO groundwater from terrestrial water storage: the partitioning residual](recipes/grace-groundwater-partitioning.md), status: draft
