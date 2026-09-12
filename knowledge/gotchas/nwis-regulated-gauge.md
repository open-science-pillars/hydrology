---
type: dataset-gotcha
spheres: [hydrosphere]
title: "Regulated gauges: flow statistics measure operations, not hydrology"
description: "Downstream of dams, percentiles, droughts, and trends reflect release decisions; drought indices need near-natural reference gauges."
tags: [nwis, regulation, dams, drought, reference-gauges]
generated: { by: knowledge-seeder/claude, at: 2026-07-05T00:00:00Z }
severity: high
dataset: ../datasets/nwis-streamflow.md
eval_case: nwis-regulated-gauge
# eval id reserved for the hydrology eval seed (one case per high-severity gotcha).
sources:
  - id: usgs-09380000
    resource: https://waterdata.usgs.gov/monitoring-location/09380000/
    title: "USGS monitoring location 09380000 (Colorado River at Lees Ferry)"
  - id: usgs-09085000
    resource: https://waterdata.usgs.gov/monitoring-location/09085000/
    title: "USGS monitoring location 09085000 (Colorado River near Dotsero)"
status: stable
verified: { by: human:PaulMRamirez, at: 2026-07-05T00:00:00Z }
stale_after: 2027-01-04
---

# Regulated gauges: flow statistics measure operations, not hydrology

**Mechanism.** A gauge downstream of a dam records releases, not
runoff. Drought percentiles, low-flow statistics, and trends computed
there characterize reservoir operating decisions; the hydrologic
signal is absorbed by storage upstream. USGS maintains near-natural
reference networks (HCDN-2009) precisely because most long gauges are
regulated.

**Wrong-result mode, measured (2026-07-05).** Day-of-year flow
percentiles against a 1991-2020 climatology at Lees Ferry (09380000,
directly below Glen Canyon Dam) classify BOTH 2021 (severe basin
drought) and 2023 (a top-tier snowpack year) as equally dry (median
percentiles 23.3 and 20.0): the 2023 water was being held to refill
Lake Powell.[^usgs-09380000] The same method at the near-natural
Roaring Fork gauge (09085000) separates the years
cleanly:[^usgs-09085000] 2021 median percentile 13.3
with 92% of days below the 30th; 2023 median 33.3 with 5% below the
10th. Nothing errors; the regulated gauge simply answers a different
question.

**Correct approach.** Drought and climate analyses use near-natural
reference gauges (or naturalized flow products) and say so; regulated
gauges answer operations questions (storage, deliveries, compliance);
any flow statistic names the gauge's regulation status, checked
against the site page's upstream-dam context.

**Verification.** Reproducible from cached fixtures in
verification/fixtures/ (both gauges, 2021 and 2023 vs the 1991-2020
climatology); the drought-index recipe records the reference-gauge
numbers as its anchors.

[^usgs-09380000]: USGS monitoring location 09380000 (Colorado River at Lees Ferry, below Glen Canyon Dam)
[^usgs-09085000]: USGS monitoring location 09085000 (Roaring Fork, near-natural reference gauge)
