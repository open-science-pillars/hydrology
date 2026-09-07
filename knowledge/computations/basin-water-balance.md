---
type: Attested Computation
title: "Basin water balance from observations: P + I - ET - Q - X = dS, with a footprint floor that refuses small basins"
description: "The water balance closed over a basin polygon and a window from four independent observational products, each term carrying its source and its uncertainty source. The storage term is refused below a footprint floor derived here from the mascon product's own geometry (111,266 km2, one mostly-land mascon), because a basin smaller than one mascon has no signal of its own; a regulated outlet is flagged and never refused; imports and exports are receipt fields with a value and a source, or an explicit assumption of zero. Two bars for an observational budget: the residual within k sigma of the terms, and an attester's recompute from the receipt."
tags: [water-balance, basin, attested, grace, imerg, mod16, discharge, footprint, hydrology]
runtime: python
parameters:
  - { name: inputs, type: "path to a frozen input tree for one basin and window", required: true }
  - { name: imports, type: "VALUE_KM3:SOURCE, repeatable", required: false }
  - { name: exports, type: "VALUE_KM3:SOURCE, repeatable", required: false }
  - { name: regulated, type: "flag: the outlet gauge is regulated", required: false }
  - { name: rating-uncertainty, type: "relative uncertainty of the discharge if the rating class is not good", required: false }
computation: references/computations/basin_water_balance.py
executor:
  resource: references/computations/basin_water_balance.py
  receipt: [computation, code_sha256, tool_version, identity, basin, window, inputs, terms, partial_checks, residual]
attester:
  resource: references/attesters/basin_water_balance_check.py
generated: { by: claude-code/fable-5, at: 2026-09-07T04:00:00Z }
status: draft
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
  - id: regulated
    resource: ../gotchas/nwis-regulated-gauge.md
    title: "The regulated-gauge gotcha: a regulated outlet measures operations as well as hydrology, which is a flag on the term and not a reason to refuse it"
  - id: fill
    resource: ../gotchas/mod16-fill-over-water-barren-urban.md
    title: "The fill gotcha: the evapotranspiration term is land evapotranspiration over the cells that carry an estimate, and open water is missing from it"
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
| I, X | receipt fields | no product: a value with a source, or the explicit assumption that none is known |

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
is not a budget with a small imbalance. the product documents gain factors for regions smaller
than a mascon, which is precisely the case being refused, and using
one here would turn a missing measurement into a number.

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

## The two bars

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
an input is not a record of what was computed), recomputes every term
and the residual, and requires agreement within 1e-6 km3.

## What the executor may read

The frozen tree named by `--inputs`, and nothing else. No network. The
tree holds the basin polygon, the two loader receipts for P and ET,
the discharge capture's canonical body with its capture id, and the
basin's mascon series extracted from the granule, each with a sha256
in the tree's manifest; the executor checks every hash before it
computes and refuses a tree edited after freezing.

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

[^mascons]: the GRACE and GRACE-FO mascon concept in the provider bundle
[^imerg]: this bundle's IMERG V07 concept
[^mod16]: this bundle's MOD16A2GF concept
[^usgs]: this bundle's USGS Water Data API connector concept
[^regulated]: the regulated-gauge gotcha
[^fill]: the MOD16 fill-code gotcha
[^record]: the basin water balance record, open-science-pillars/marketplace issue 70
