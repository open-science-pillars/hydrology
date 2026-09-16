---
type: Attested Computation
spheres: [hydrosphere]
title: "Basin water balance from observations: P + I - ET - Q - X = dS, with a footprint floor that refuses small basins and a groundwater partition of the storage term"
description: "The water balance closed over a basin polygon and a window from four independent observational products, each term carrying its source, its uncertainty source and the stamp it came from. The storage term is refused below a footprint floor derived here from the mascon product's own geometry (111,266 km2, one mostly-land mascon), because a basin smaller than one mascon has no signal of its own; a regulated outlet is flagged and never refused; imports and exports are receipt fields with a value and a source, or an explicit assumption of zero. When the frozen tree carries a well set, the groundwater part of dS is computed by the water-table fluctuation method from USGS daily depth-to-water series at a stated specific yield with its source, and dS is partitioned into groundwater and the rest; the residual does not move. Three bars for an observational budget: the residual within k sigma of the terms, an attester's recompute from the receipt, and plausibility bounds on the groundwater term."
tags: [water-balance, basin, attested, grace, imerg, mod16, discharge, groundwater, specific-yield, footprint, hydrology]
runtime: python
parameters:
  - { name: inputs, type: "path to a frozen input tree for one basin and window; a tree holding groundwater.json binds the groundwater term and its parameters", required: true }
  - { name: imports, type: "VALUE_KM3:SOURCE, repeatable", required: false }
  - { name: exports, type: "VALUE_KM3:SOURCE, repeatable", required: false }
  - { name: regulated, type: "flag: the outlet gauge is regulated", required: false }
  - { name: rating-uncertainty, type: "relative uncertainty of the discharge if the rating class is not good", required: false }
computation: references/computations/basin_water_balance.py
executor:
  resource: references/computations/basin_water_balance.py
  skill: hydrology/basin-water-balance
  receipt: [computation, code_sha256, tool_version, identity, basin, window, inputs, terms, partial_checks, residual, bookkeeping]
attester:
  resource: references/attesters/basin_water_balance_check.py
generated: { by: process:claude-code, at: 2026-09-15T18:30:00Z }
verified:
  - { by: human:PaulMRamirez, at: 2026-09-07T18:19:02Z }
  - { by: human:PaulMRamirez, at: 2026-09-16T03:04:07Z, role: maintainer, source: https://github.com/open-science-pillars/hydrology/pull/70 }
status: stable
stale_after: 2027-03-07
sources:
  - id: mascons
    resource: ../../../nasa-daac-knowledge/knowledge/podaac/datasets/grace-fo-mascons.md
    title: "The GRACE and GRACE-FO mascon concept: the native scale is the mascon and not the grid cell, the per-mascon uncertainty grids ship with the product, and the gain factors are documented for regions smaller than a mascon"
  - id: imerg
    resource: ../datasets/imerg-v07.md
    title: "This bundle's IMERG concept: the run is a declared input, the calibration differs between runs, and a change of run is a dated seam"
  - id: mod16
    resource: ../datasets/mod16a2gf.md
    title: "This bundle's MOD16A2GF concept: the units and scale factor, the seven fill codes, the compositing rule and the gap-filled record's year-end edge"
  - id: usgs
    resource: ../connectors/usgs-water.md
    title: "This bundle's USGS connector concept: the Water Data API, the approval and qualifier fields, and the capture route"
  - id: groundwater-connector
    resource: ../connectors/nwis-groundwater.md
    title: "This bundle's groundwater connector concept: parameter 72019 is depth to water below land surface in feet, the field-measurements collection holds the discrete readings, and a continuously recorded well is a daily series through usgs_daily with the same parameter code"
  - id: regulated
    resource: ../gotchas/nwis-regulated-gauge.md
    title: "The regulated-gauge gotcha: a regulated outlet measures operations as well as hydrology, which is a flag on the term and not a reason to refuse it"
  - id: fill
    resource: ../gotchas/mod16-fill-over-water-barren-urban.md
    title: "The fill gotcha: the evapotranspiration term is land evapotranspiration over the cells that carry an estimate, and open water is missing from it"
  - id: partitioning
    resource: ../recipes/grace-groundwater-partitioning.md
    title: "This bundle's GRACE groundwater partitioning recipe: groundwater as the total storage less the other stores, whose residual inherits the subtrahends' errors; the well set here is the confrontation term that recipe names"
  - id: gehman2009
    resource: https://doi.org/10.1029/2007WR006096
    title: "Gehman, Harry, Sanford, Stednick and Beckman 2009, Estimating specific yield and storage change in an unconfined aquifer using temporal gravity surveys, Water Resources Research 45(4): a specific yield of 0.21 plus or minus 0.03 from the gravimetric storage change divided by the measured water-level change at an unconfined alluvial aquifer in northeastern Colorado, within the range of the site's aquifer tests; the Crossref record and abstract read 2026-09-15, the journal page not read"
  - id: pool1995
    resource: https://doi.org/10.1111/j.1745-6584.1995.tb00299.x
    title: "Pool and Eychaner 1995, Measurements of aquifer-storage change and specific yield using gravity surveys, Groundwater 33(3) 425 to 432: average specific yield at wells of 0.16 to 0.21 in an alluvial aquifer in central Arizona, by the same method; the Crossref record and abstract read 2026-09-15, the journal page not read"
  - id: johnson1967
    resource: https://doi.org/10.3133/wsp1662D
    title: "Johnson 1967, Specific yield: compilation of specific yields for various materials, U.S. Geological Survey Water-Supply Paper 1662-D, the compilation of record for specific yield by material; the Crossref record (title, year, publisher, no author list on the record) read 2026-09-15, the landing page on pubs.usgs.gov not reachable from the drafting session, so no value is taken from it"
  - id: crosbie2019
    resource: https://doi.org/10.1029/2019WR025285
    title: "Crosbie, Doble, Turnadge and Taylor 2019, Constraining the magnitude and uncertainty of specific yield for use in the water table fluctuation method of estimating recharge, Water Resources Research 55(8) 7343 to 7361: the specific yield is the major source of uncertainty of the method and a conceptual parameter that cannot be measured for the purpose; the Crossref record and abstract read 2026-09-15"
  - id: field-measurements
    resource: https://api.waterdata.usgs.gov/ogcapi/v0/collections/field-measurements?f=json
    title: "The Water Data API field-measurements collection description, read 2026-09-15: readings of groundwater levels beside gage height and discharge measurements, collected at a low frequency on site visits and delivered after processing; the time-series-metadata collection beside it lists every daily series with its parameter, statistic, begin and end, which is how the well set was found"
  - id: capture-tool
    resource: https://github.com/open-science-pillars/core/blob/6d8de538894c59bbefef4c4fa7ea91fc654dd95c/connectors/obs_capture.py
    title: "core's capture tool: one observation query frozen into a record with a capture id, a raw hash and a content hash; the well series behind the groundwater term are usgs-dv captures of parameter 72019, the same route as the discharge term"
  - id: record
    resource: https://github.com/open-science-pillars/marketplace/issues/70
    title: "The basin water balance record: the frozen trees, the measured residuals, the refusal and the floor derivation"
---

# Basin water balance from observations

The identity, over a basin polygon and a window:

**P + I - ET - Q - X = dS**

precipitation plus imports, less evapotranspiration, discharge and
exports, equals the change in storage. Every term comes from a
different instrument and a different processing chain, so the residual
is not a rounding error: it is what four independent products fail to
agree on, and its size against their combined uncertainty is the only
honest statement the identity supports.

This is an OBSERVATIONAL budget. It does not close by construction the
way a model budget does, and its bars are not the numerical-closure
bars of a model: nothing here can be tightened by taking smaller time
steps.

## The terms, each with its source and its uncertainty source

| Term | Product | Uncertainty, and where the figure comes from |
|---|---|---|
| P | IMERG V07 daily, one declared run per month | 10 per cent, the documented land uncertainty at monthly to annual scales[^imerg] |
| ET | MOD16A2GF v061, composites apportioned by their true length | 20 per cent, the product's validation against flux towers and watersheds[^mod16] |
| Q | USGS daily mean discharge, from a frozen capture | 5 per cent for a good rating class, from the station description; a poorer class widens it and the receipt records which was used[^usgs] |
| dS | GRACE and GRACE-FO mascons, the difference between two epochs | the product's own per-mascon formal uncertainty grid, area weighted over the basin and divided by the square root of the mascons the basin spans[^mascons] |
| dS_gw | the groundwater part of dS: USGS daily depth to water at a well set, times a stated specific yield, times the basin area | quadrature of the specific yield's stated sigma and the standard error of the site mean; the spread over sites is reported beside it[^gehman2009][^crosbie2019] |
| I, X | receipt fields | no product: a value with a source, or the explicit assumption that none is known |

Every term in the receipt carries a stamp: the file of the frozen tree
it came from and that file's sha256, repeated on the term so a reader
of the term alone can find its bytes.

The run for P is declared per month and a change of run is a dated
seam in the receipt, because the three IMERG runs share a variable
name and differ in calibration.[^imerg] The ET term is land
evapotranspiration over the cells that carry an estimate: the fill
classes are excluded, the masked fraction is in the receipt, and open
water inside the basin has no MOD16 estimate at all, so a basin
holding a large reservoir is missing that water loss from its ET
term.[^fill]

**Imports and exports are terms, not corrections.** Each entry carries
a value in km3 and a source, and the executor refuses a value without
one: an unsourced transfer is the term that quietly closes a budget.
Where none is known the receipt says so in those words rather than
leaving the field empty.

**A regulated outlet is flagged, never refused.** A gauge below a dam
measures operations as well as hydrology; that is a fact about what
the residual contains, and the flag says it.[^regulated]

## The groundwater term: a partition of dS, not a sixth term

The mascons see total water storage: groundwater, soil moisture, snow,
surface water and canopy together.[^mascons] A well set sees one of
those stores. When the frozen tree carries `groundwater.json`, the
executor computes the groundwater part of dS by the water-table
fluctuation method and partitions the storage term:

**dS = dS_gw + dS_other**, and therefore
**P + I - ET - Q - X - dS_gw = dS_other + residual**.

The residual and its consistency bar do not move. Adding dS_gw to the
identity as a further term would count the groundwater twice, once
inside the mascon signal and once from the wells; the receipt states
this in its bookkeeping lines rather than leaving a reader to work out
which sum was taken. dS_other is what the mascons see that the wells
do not: soil moisture, snow, surface water, and groundwater outside
the well set's reach.[^partitioning]

**The well set and its rules.** The wells are continuously recorded
USGS wells whose daily mean depth to water (parameter 72019, feet
below land surface, statistic 00003) covers the window, found through
the Water Data API's time-series-metadata collection and read as
usgs-dv captures with the same capture tool as the discharge
term.[^groundwater-connector][^field-measurements][^capture-tool] A
well contributes when it is inside the basin polygon, its site file
says the aquifer is unconfined (a confined well's head change is a
pressure change, not a drained volume, and specific yield does not
apply to it), and its constructed depth is stated. The Water Data
API serves a well's constructed depth and hole depth and not its
screened interval, so the depth stated for every well is the
constructed depth, and the receipt says so.

**The level change.** At each well the level at an end of the window
is the mean of the daily depths over the first `end_window_days` days
and the last `end_window_days` days of the window (30 in the frozen
tree), and the rise is the first mean less the last: a shallower
water table is a rise. A well with fewer than `min_days_per_end` daily
values (20) in either end window is excluded by name with the counts.
Wells within `cluster_radius_km` of one another (2 km) are one site,
because a well field samples one water table and would otherwise be
counted once per well; sites are the connected components of the
wells joined by that distance, so a well within the radius of two
groups joins them into one and the result does not depend on the
order the wells are visited in. The mean over sites is the basin's level
change, and its spread over sites, its standard error and its median
travel beside the mean. Fewer than `min_sites` sites (3) is a refusal
of the term, not a smaller term.

**The specific yield is a stated parameter, not a measurement.** The
term is the specific yield times the mean rise times the basin area,
and it is linear in a number that cannot be measured for the purpose:
the apparent specific yield depends on the depth to the water table,
and it is the major source of uncertainty of the
method.[^crosbie2019] The frozen tree states the value with its sigma
and its source, and the receipt reports the term at the value and at
one sigma either side. The value the frozen Ohio tree carries is 0.21
plus or minus 0.03, the gravimetric measurement at an unconfined
alluvial aquifer by Gehman and others, which Pool and Eychaner's 0.16
to 0.21 at alluvial wells brackets from below.[^gehman2009][^pool1995]
A single value for a well set spanning glacial, alluvial and bedrock
aquifers is an assumption the tree states, not a property of the
basin; the compilation of record for specific yield by material is
Johnson's 1967 Water-Supply Paper, cited here on its registry record
because its landing page was not reachable when this was written, and
a basin-specific value from it would replace the stated one without
changing the arithmetic.[^johnson1967]

**Uncertainty.** The term's sigma is the quadrature of the specific
yield's sigma times the mean rise and the specific yield times the
standard error of the site mean. The standard error is the spread
over sites divided by the square root of the site count, which is the
sigma of the mean only if the sites are a random sample of the
basin's water table; the wells are the wells there are, not a
designed sample of the basin. On the Ohio the quoted sigma of 14.98
km3 is almost entirely the standard-error component (14.91 km3,
against 1.39 km3 from the specific yield's sigma), and with the
spread over sites in its place the sigma would be 93.2 km3, at which
bar three's "part no larger than the whole" is satisfied by any
groundwater change at all. The choice of the standard error is
therefore what gives bar three teeth, and it rests on the sampling
assumption named above. The receipt carries both figures,
`sigma_km3` and `sigma_km3_at_spread`, with the two components of the
first, and the attester recomputes all of them; a reader who does not
grant the assumption reads the second.

## The footprint floor, derived rather than remembered

The mascon concept states that the native resolution is the mascon and
of order 300 km, and carries no number.[^mascons] The number is owned
here, and derived from the product's own geometry: over the 4,551
mascons in the CRI grid, the 1,301 that are mostly land have a median
area of **111,266 km2** (p05 103,876, p95 123,457), which is a 334 km
square or a 376 km circle. That is the "order 300 km" made specific,
and it is recomputed by the freezing step from whatever release is in
hand rather than copied forward.

**Below one mascon there is no storage term, and therefore no
residual by any route.** A basin smaller than the floor spans one
mascon or part of one, so the mascon field over it carries the
neighbourhood's signal and not the basin's. The executor refuses the
term, does not report a residual, and does not apply a gain factor.
The other three terms are still reported, and their arithmetic
difference is not a residual in disguise: a budget with a term missing
is not a budget with a small imbalance. The product documents gain
factors for regions smaller than a mascon, which is precisely the case
being refused, and using one here would turn a missing measurement
into a number. A groundwater term on such a basin is reported as the
groundwater part of a dS the basin does not have, and it does not
stand in for the refused term.

The uncertainty side of the floor is the same fact stated as
statistics: cells inside one mascon are not independent samples, so
the effective sample size of a basin mean is the number of mascons the
basin spans. A basin on one mascon gets no averaging benefit at all,
which is why its storage uncertainty is the full per-mascon figure.

## The epoch rule and the endpoint latency

Mascon epochs are mid-month and a window's ends are not. The executor
uses the epoch nearest each end and records the offset in days, so a
water year beginning 1 October is measured between the 16 September
epochs at either end: a twelve-month span, offset by about half a
month, and the receipt says so rather than pretending the dates match.

The record ends about two to three months behind the present (last
epoch 2026-06-16 as of 2026-09-07). A window whose end falls past the
record's last epoch has an **open** closing endpoint: the receipt
reports it as open and the executor never fills it by extrapolation.

## The three bars

**Bar one, consistency.** The residual is within k times the
quadrature sum of the four term uncertainties. The default k is 2, and
2 is a choice with a reason: each figure is a documented one-sigma
uncertainty from its own product, the four chains are independent
enough for a quadrature sum to be the honest combination, and four
remote-sensing terms agreeing inside one sigma would be evidence of a
tuned term rather than of closure. A basin that passes at k=2 is
consistent with its terms. It is not thereby correct.

**Bar two, reproducibility.** The attester re-reads the frozen tree,
checks every file against the hash the receipt recorded, checks that
the receipt claims every file the tree declares (a receipt that omits
an input is not a record of what was computed) and that every term's
stamp is one of them, recomputes every term, the groundwater term from
the well set with its own arithmetic, the residual and the partition,
and requires agreement within 1e-6 km3.

**Bar three, plausibility of the groundwater term**, applied only when
a receipt carries one: the well set's parameter 72019 in feet below
land surface (an elevation parameter would reverse the sign of the
term, and the executor refuses one), the specific yield inside
(0, 0.5], the receipt's value equal to the tree's, a source beside it, the site
count at or above the parameters' minimum, every site's level change
within 30 m, the partition arithmetic exact, and the part no larger
than the whole: the groundwater change does not exceed the total
storage change by more than k times their combined sigma. A
groundwater change larger than the mascons' total is a specific yield
or a well set that does not describe the basin, and the attester says
so rather than passing the arithmetic.

The attester prints a PASS or FAIL line for every check and exits
nonzero on any FAIL; its `--selftest` runs the executor over synthetic
trees whose numbers can be checked by hand, with and without the
groundwater term, and the doctorings each bar must catch.

## What the executor may read

The frozen tree named by `--inputs`, and nothing else. No network. The
tree holds the basin polygon, the two loader receipts for P and ET,
the discharge capture's canonical body with its capture id, the
basin's mascon series extracted from the granule, and, when the term
is wanted, the well set with its captures, its site files, the
selection that produced it and the parameters with their sources,
each file with a sha256 in the tree's manifest; the executor checks
every hash before it computes and refuses a tree edited after
freezing.

The P and ET terms are frozen as their loaders' receipts rather than
as the grids behind them, because the grids do not fit the fixture
rule: a water year of MOD16 over the Ohio at Olmsted is five
sinusoidal tiles and 253 MB. The receipts carry the window files' own
hashes, the granule ids, the route and the coverage, so the
derivation stays traceable to bytes that can be refetched.

## Measured, water year 2023 (2022-10-01 to 2023-09-30)

| Basin | P km3 | ET km3 | Q km3 | dS km3 | Residual km3 | Residual / sigma |
|---|---|---|---|---|---|---|
| Ohio at Olmsted (524,136 km2) | 647.384 | 355.162 | 220.865 | +1.183 | +70.174 +- 96.874 | +0.72 |
| Colorado above Lees Ferry (276,444 km2) | 88.585 | 83.719 | 10.769 | +13.214 | -19.117 +- 19.165 | -1.00 |
| Roaring Fork (3,767 km2) | 1.369 | 1.819 | 1.128 | refused | not reported | not applicable |

Both reported basins pass bar one at k=2 and bar two exactly. Two
things the table does not say on its own:

- The Lees Ferry outlet is regulated and the flag is in its receipt:
  that discharge is Glen Canyon Dam's releases as much as the basin's
  hydrology. Its residual is negative, meaning storage rose by more
  than the other terms deliver, in a water year whose snowpack was
  exceptional. **The transmountain exports out of the Upper Colorado
  are a real term of this basin that is missing here**, and adding it
  would make the residual more negative, not less: the executor
  refuses an unsourced value and no water-year 2023 total from
  Reclamation or Colorado DWR records was available to cite when this
  was written. The receipt therefore carries the explicit assumption
  of zero, and the residual should be read as an upper bound on
  closure rather than as closure.
- The Roaring Fork is 3.4 per cent of one mascon. Its refusal is the
  computation working, not failing.

A partial check travels beside the Lees Ferry receipt: the Lake Powell
pool elevation at Glen Canyon Dam over the same window, in feet, as a
check on the sign and rough size of the storage term. It is a receipt
field and is never folded into dS.

**The groundwater partition on the Ohio at Olmsted** (the frozen tree
`ohio-olmsted-groundwater`, which copies the Ohio tree's four terms
byte for byte and adds the well set; measured 2026-09-15):

| Quantity | Value |
|---|---|
| Wells captured | 58 unconfined wells with a stated constructed depth inside the polygon, of 249 wells in the bounding box whose daily depth-to-water series covers the window |
| Wells used, sites | 50 (8 excluded for fewer than 20 daily values in an end window), 39 sites at 2 km (the Louisville well field of 12 wells is one site) |
| Mean rise over sites | +0.089 m, median -0.063 m, spread 0.846 m, standard error 0.136 m |
| Specific yield | 0.21 +- 0.03, stated with its source in the tree |
| dS_gw | +9.752 +- 14.982 km3 (18.6 mm); 8.359 at 0.18 and 11.145 at 0.24 |
| dS | +1.183 +- 5.103 km3 |
| dS_other | -8.569 +- 15.827 km3 |
| P + I - ET - Q - X - dS_gw | +61.605 km3, which is dS_other plus the residual of +70.174 |
| Bar three | |dS_gw| 9.752 against |dS| + k sigma of 32.836 km3, within |

The groundwater term is within one sigma of zero, and so is the
mascons' total; the median rise is negative while the mean is
positive, because one well field near the Ohio at Louisville rose
3.3 m and the other 38 sites sit between -1.5 and +2.6 m. Without
that one site the mean over the other 38 is +0.003 m and the term
is +0.339 km3: the whole positive term is one riverbank well field
beside the Ohio, whose water table follows the river's stage and the
field's pumping, and the receipt carries the term without its
largest site (`without_largest_site`, recomputed by the attester) so
that this is a number and not a remark. Four of the eight
completeness exclusions are Louisville wells as well. The receipt
does not report a groundwater fraction of dS, because a fraction of
a storage change indistinguishable from zero is not a number. What
the partition does say is that the terms less the groundwater change
still deliver about 62 km3 more than the other stores account for,
inside a combined sigma of 97 km3 that the evapotranspiration term
dominates: the groundwater term neither creates nor removes the
Ohio's residual.

**The well set is not an areal sample.** The 58 wells sit in 11
states, 18 in Kentucky, 13 in Indiana and 11 in Pennsylvania, and
the 39 sites are 11 in Pennsylvania, 8 in Indiana, 6 in Tennessee, 4
in Kentucky and 4 in North Carolina with one each in six other
states; the western and northern parts of the basin (Ohio, Illinois,
most of Indiana) are thinly sampled and the Appalachian edge is
dense. A site mean weights every site equally wherever it stands.
The next step, not taken here, is an areal weighting, by Thiessen
polygons over the basin or by the area of each state's share of it,
which the frozen tree already holds the coordinates for.

**The specific yield does not describe most of this set.** By the
receipt's national aquifer codes the 50 wells used are 13 in the
Pennsylvanian aquifers, 11 alluvial, 9 glacial, 5 Piedmont and Blue
Ridge crystalline, 5 Mississippian, 4 Valley and Ridge, 1
Ordovician, 1 Silurian-Devonian and 1 other: 30 of the 50 are in
bedrock aquifers, and their constructed depths run from 18 to 363
ft. The 0.21 plus or minus 0.03 is a gravimetric measurement at one
alluvial site, and the plus or minus 0.03 covers that measurement,
not its application to fractured sandstone, carbonate or crystalline
rock, for which an alluvial value is not a bracket. The replacement
that changes the number without changing the arithmetic is a value
per aquifer type from the compilation of record, Johnson 1967, or a
basin study, applied per well before the site mean; the tree's
parameter block is where it goes, and the receipt's sensitivity to
it is linear.[^johnson1967]

[^mascons]: the GRACE and GRACE-FO mascon concept in the provider bundle
[^imerg]: this bundle's IMERG V07 concept
[^mod16]: this bundle's MOD16A2GF concept
[^usgs]: this bundle's USGS Water Data API connector concept
[^groundwater-connector]: this bundle's USGS groundwater levels connector concept
[^regulated]: the regulated-gauge gotcha
[^fill]: the MOD16 fill-code gotcha
[^partitioning]: this bundle's GRACE groundwater partitioning recipe
[^gehman2009]: Gehman and others 2009, the Crossref record and abstract read 2026-09-15
[^pool1995]: Pool and Eychaner 1995, the Crossref record and abstract read 2026-09-15
[^johnson1967]: Johnson 1967, the Crossref record read 2026-09-15; the landing page not reachable
[^crosbie2019]: Crosbie and others 2019, the Crossref record and abstract read 2026-09-15
[^field-measurements]: the Water Data API field-measurements collection description, read 2026-09-15
[^capture-tool]: core's capture tool at the pinned commit
[^record]: the basin water balance record, open-science-pillars/marketplace issue 70
