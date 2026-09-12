---
type: dataset-gotcha
spheres: [hydrosphere]
title: "RiverSP reach vs node: statistics quoted at the wrong aggregation level"
description: "Reach and node are separate collections at different aggregation levels; heights, widths, and especially discharge only mean something with the level named."
tags: [swot, riversp, reach, node, scope]
generated: { by: knowledge-seeder/claude, at: 2026-07-05T00:00:00Z }
severity: high
dataset: ../datasets/swot-river-lake.md
eval_case: swot-reach-node-scope
sources:
  - id: podaac-riversp-reach
    resource: https://podaac.jpl.nasa.gov/dataset/SWOT_L2_HR_RiverSP_reach_D
    title: "PO.DAAC collection page: SWOT_L2_HR_RiverSP_reach_D"
  - id: podaac-riversp-node
    resource: https://podaac.jpl.nasa.gov/dataset/SWOT_L2_HR_RiverSP_node_D
    title: "PO.DAAC collection page: SWOT_L2_HR_RiverSP_node_D"
  - id: swot-river-lake
    resource: ../datasets/swot-river-lake.md
    title: "This bundle's SWOT River and Lake dataset concept, Structure section (granule-verified attribute inventories, 2026-07-05)"
status: stable
upstream: pending
verified: { by: human:PaulMRamirez, at: 2026-09-04T22:36:00Z }
stale_after: 2027-01-04
---

# RiverSP reach vs node: statistics quoted at the wrong aggregation level

**Mechanism.** SWOT river observations ship at two aggregation levels
in SEPARATE collections: nodes (~200 m spacing along SWORD
centerlines; 40,284 features and 57 attributes in one observed
pass-continent granule) and reaches (~10 km aggregates; 731 features,
127 attributes, including all discharge variants, same granule pair,
granule-verified 2026-07-05).[^podaac-riversp-reach][^podaac-riversp-node]
The attribute sets differ: slope and discharge exist ONLY at reach
level; per-node position uncertainty and cross-track distance exist
only at node level.[^swot-river-lake]

**Wrong-result mode.** A "river water surface elevation" averaged
across nodes is not the reach wse (the reach value is the product's
own aggregation with its own uncertainty); node-level noise statistics
quoted as reach uncertainty overstate random error while missing
correlated systematics (the wse_u vs wse_r_u distinction); any
discharge or slope claim sourced from node data is fabricated, since
those attributes do not exist there. Nothing errors; the numbers are
simply at the wrong scale.

**Correct approach.** Every statistic names its level; questions map
to levels (reach for river-scale hydrology and discharge; node for
profiles and local structure); cross-level comparisons state the
product's own aggregation as authoritative; volumes are planned per
level (node data ~8x reach volume per pass-continent).

**Verification.** Reproducible from the granule pair recorded in the
dataset concept (cycle 011, pass 424, AS, PGD0): the attribute inventories
and feature counts above; discharge attributes absent from the node
shapefile schema.

[^podaac-riversp-reach]: PO.DAAC collection page, SWOT_L2_HR_RiverSP_reach_D
[^podaac-riversp-node]: PO.DAAC collection page, SWOT_L2_HR_RiverSP_node_D
[^swot-river-lake]: This bundle's SWOT River and Lake dataset concept, Structure section: the reach and node attribute inventories
