---
type: recipe
spheres: [hydrosphere, geosphere]
title: "GRACE-FO groundwater from terrestrial water storage: the partitioning residual"
description: "Groundwater anomaly as the TWS-minus-other-stores residual: which product supplies each subtrahend, why the residual inherits their errors, and the basin-resolution and trend caveats."
tags: [grace, grace-fo, groundwater, tws, partitioning, mascons, hydrology]
generated: { by: knowledge-seeder/claude, at: 2026-07-05T00:00:00Z }
inputs: "GRACE/GRACE-FO mascon TWS anomaly (see the mascon dataset concept) plus one product per subtracted store: soil moisture (SMAP L3 or a land-surface model), snow water equivalent (SNODAS or a model), surface water (altimetry or gauges), and canopy water (a model); all anomalies on the same baseline period as the mascon product"
expected: "A groundwater storage anomaly time series on the mascon's native scale (not the 0.5-degree grid cell); qualitative here, no fixed numeric anchor is recorded yet (draft)"
expected_uncertainty: "Bounded BELOW by the mascon formal-error grids and typically DOMINATED by the subtrahends, which usually arrive without formal error propagation; a groundwater trend quoted with only the GRACE formal error is understated"
sources:
  - id: grace-tellus
    resource: https://grace.jpl.nasa.gov/
    title: "GRACE Tellus project site (grace.jpl.nasa.gov)"
status: stable
verified:
  - { by: human:PaulMRamirez, at: 2026-07-06T00:00:00Z }
  - { by: human:PaulMRamirez, at: 2026-09-05T04:54:00Z }
  - { by: human:PaulMRamirez, at: 2026-09-05T20:22:37Z }
stale_after: 2027-01-04
---

# GRACE-FO groundwater from terrestrial water storage: the partitioning residual

**Method.** GRACE and GRACE-FO sense TOTAL terrestrial water storage
change (every store together).[^grace-tellus] Groundwater is not measured; it is the
RESIDUAL left after every other store is subtracted:

GW anomaly = TWS anomaly - (soil moisture + snow + surface water + canopy)

Each anomaly is referenced to the same baseline period as the mascon
product, and the estimate lives on the mascon's native information scale
(not the 0.5-degree grid cell; see the provider bundle's mascon
dataset concept, `knowledge/podaac/datasets/grace-fo-mascons.md`,
installed with the nasa-daac-knowledge dependency).

**Every subtrahend is another product.** Soil moisture comes from SMAP
L3 ([smap-l3](../datasets/smap-l3.md)) or a land-surface model; snow
water equivalent from SNODAS or a model; surface water from altimetry
or gauges; canopy water from a model. The groundwater residual
therefore INHERITS every subtrahend's errors and biases, usually
without formal error propagation available.

**Uncertainty structure.** The residual's uncertainty is bounded below
by the mascon formal error and is typically dominated by the
subtrahends; a groundwater trend quoted with only the GRACE formal
error is understated. Basin size matters: below a few mascon footprints
(order 300 km, the 3-degree mascon scale) the estimate is
leakage-dominated (see the provider bundle's
`knowledge/podaac/gotchas/grace-coastal-leakage.md`),
and honest work states basin area against the effective resolution.

**Trends.** The 2017-2018 GRACE-to-GRACE-FO gap and GIA-model
sensitivity bite trends directly (see the provider bundle's
`knowledge/podaac/datasets/grace-fo-mascons.md` and
`knowledge/podaac/gotchas/grace-gia-correction.md`);
every trend window states how the gap is handled and names the applied
GIA model, and no fit treats the gap as data.

**Attribution.** Human signals (irrigation drawdown) and climate
signals mix in the same residual; attributing a trend to one needs
independent evidence, not the residual alone.

**Provenance.** Relocated from the grace-groundwater skill during the
knowledge-coupling migration (status: draft). Needs a steward evidence
link; if a measured numeric anchor is added, it also needs an eval case
(every high-severity numeric anchor carries a matching eval case).

[^grace-tellus]: GRACE Tellus project site, the total-storage measurement basis
