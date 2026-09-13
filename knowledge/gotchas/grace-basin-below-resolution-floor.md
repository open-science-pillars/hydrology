---
type: dataset-gotcha
spheres: [hydrosphere]
title: "A basin near or below one mascon has no GRACE series of its own: the values are the neighbourhood's and the constraint's, and nothing errors"
description: "The JPL mascon grid is written at 0.5 degrees but estimated on 3-degree equal-area mascons (one mostly-land mascon is about 111,000 km2, a square of about 330 km), and the effective resolution of GRACE terrestrial water storage is a few hundred kilometers. A basin whose area is near or below one mascon gets that mascon's value, which is the signal of everything inside the mascon and the leakage of its neighbours under the solution's a priori constraint, not the basin's storage; the extraction runs, returns monthly values with formal uncertainties, and nothing marks the series as not the basin's."
tags: [grace, grace-fo, mascons, tws, resolution, leakage, basin-size, small-basin, footprint]
generated: { by: knowledge-seeder/claude, at: 2026-09-13T20:40:00Z }
severity: high
# The dataset concept for the product lives in the PO.DAAC provider
# bundle (knowledge/podaac/datasets/grace-fo-mascons.md in
# nasa-daac-knowledge, installed beside this plugin); a relative path
# to it from this key is not stable across installations, so the key
# carries the product page, the same resource the recipe's sources name.
dataset: https://podaac.jpl.nasa.gov/dataset/TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4
eval_case: grace-basin-below-resolution-floor
status: draft
stale_after: 2027-03-13
sources:
  - id: product-page
    resource: https://podaac.jpl.nasa.gov/dataset/TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4
    title: "PO.DAAC collection page: TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4 (4,551 equal-area 3-degree mascons; the mascons act as an inherent smoother; the gain factors as the option for sub-mascon hydrology)"
  - id: virtual-listing
    resource: https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-public/virtual_collections/TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4/TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4_virtual_https.json
    title: "The collection's virtual dataset reference file: the grid resolution attributes ('0.5 degree grid; however the native resolution of the data is 3-degree equal-area mascons') and the uncertainty variable's comment ('not for each 0.5 degree grid cell, but for each 3-degree mascon estimate')"
  - id: landerer-2012
    resource: https://doi.org/10.1029/2011WR011453
    title: "Landerer and Swenson, 2012, Accuracy of scaled GRACE terrestrial water storage estimates, Water Resources Research (the effective spatial resolution of GRACE TWS at length scales of a few hundred kilometers; gain factors from land hydrology models as the extrapolation to about 100 km, and the cases where they reduce accuracy)"
  - id: wiese-2016
    resource: https://doi.org/10.1002/2016WR019344
    title: "Wiese, Landerer and Watkins, 2016, Quantifying and reducing leakage errors in the JPL RL05M GRACE mascon solution, Water Resources Research (leakage errors of 11 to 30 per cent remain, averaged globally, even for basins above 160,000 km2 before the gain factors are applied)"
  - id: scanlon-2016
    resource: https://doi.org/10.1002/2016WR019494
    title: "Scanlon and others, 2016, Global evaluation of new GRACE mascon products for hydrologic applications, Water Resources Research (the mascon intercomparison in 176 river basins covering about 60 per cent of the global land area, the basin scale at which the products were judged usable)"
  - id: watkins-2015
    resource: https://doi.org/10.1002/2014JB011547
    title: "Watkins and others, 2015, Improved methods for observing Earth's time variable mass distribution with GRACE using spherical cap mascons, Journal of Geophysical Research: Solid Earth (the a priori constraint from near-global geophysical models that the mascon solution carries)"
  - id: dataset
    resource: ../../../nasa-daac-knowledge/knowledge/podaac/datasets/grace-fo-mascons.md
    title: "The provider bundle's mascon dataset concept (knowledge/podaac/datasets/grace-fo-mascons.md in nasa-daac-knowledge): the native resolution is the mascon, of order 300 km, and a basin near or below it is resolution- and leakage-dominated"
  - id: leakage
    resource: ../../../nasa-daac-knowledge/knowledge/podaac/gotchas/grace-coastal-leakage.md
    title: "The provider bundle's coastal-leakage gotcha (knowledge/podaac/gotchas/grace-coastal-leakage.md): the same geometry at the coast"
  - id: water-balance
    resource: ../computations/basin-water-balance.md
    title: "This bundle's basin water balance computation: the footprint floor derived from the product's own geometry (the 1,301 mostly-land mascons have a median area of 111,266 km2, a 334 km square), the refusal of the storage term below it, and the measured refusal of a 3,767 km2 basin at 3.4 per cent of one mascon"
  - id: recipe
    resource: ../recipes/grace-basin-tws.md
    title: "This bundle's basin TWS recipe: the region as whole mascons from the granule's mascon_ID field"
---

# A basin near or below one mascon has no GRACE series of its own

**Mechanism.** The product is distributed on a 0.5-degree grid, and
its own attributes say the grid is not the resolution: "0.5 degree
grid; however the native resolution of the data is 3-degree equal-area
mascons", and the uncertainty variable is "not for each 0.5 degree
grid cell, but for each 3-degree mascon estimate".[^virtual-listing]
Every cell inside a mascon carries the mascon's one value, so a
polygon clipped onto the grid returns that value as many times as it
has cells and averages it back to itself.[^product-page][^dataset]
This bundle's basin water balance computation derives the size from
the product's geometry: the 1,301 mostly-land mascons have a median
area of 111,266 km2, a square of 334 km on a side, and a basin below
that spans one mascon or part of one.[^water-balance] The mascon
value itself is not the basin's storage even when the basin fills the
mascon: the solution is estimated with an a priori constraint from
geophysical models, the mascons act as an inherent smoother, and the
product team's own synthetic tests leave leakage errors of 11 to 30
per cent, averaged globally, in basins above 160,000 km2 before the
gain factors are applied.[^watkins-2015][^product-page][^wiese-2016]
The effective resolution of GRACE terrestrial water storage is a few
hundred kilometers, and the published gain factors extrapolate from
that scale toward about 100 kilometers using a land hydrology model,
with the paper that introduced them noting the cases where scaling
reduces accuracy.[^landerer-2012] The global evaluation of the mascon
products for hydrology was made across 176 river basins covering
about 60 per cent of the land area, which is the scale at which the
products were judged.[^scanlon-2016]

**Wrong-result mode.** A request for the storage series of a basin of
a few thousand square kilometers (a headwater catchment, a single
HUC8, a small aquifer) runs to completion: the cells inside the
polygon are found, a monthly series with formal uncertainties comes
back, its seasonal cycle looks like hydrology, and its trend is
quoted. The series is the mascon's: the storage of everything in a
111,000 km2 block, including the neighbouring basins, the reservoir
across the divide and the leakage from the blocks around it, shaped by
the constraint. A drought index, a groundwater residual or a water
balance built on it describes the region, not the basin, and nothing
in the output says so. The gain factors are not a way out: they
redistribute a mascon's signal by a land model's pattern, and using
them on a basin the product cannot resolve turns a missing measurement
into a number (the computation concept refuses the term rather than
scale it).[^landerer-2012][^water-balance]

**Correct approach.** A basin's area is stated against the mascon
count it spans before any series is extracted, with the region
defined as whole mascons from the granule's `mascon_ID` field, never
as clipped cells.[^recipe] Below one mascon there is no basin series
by any route, and the storage term is refused as the water balance
computation refuses it (the Roaring Fork, 3,767 km2, is 3.4 per cent
of one mascon and was refused in the measured run).[^water-balance]
At one to a few mascons the series exists with the leakage and
constraint caveats stated as its own uncertainty term beside the
formal error, and the coastal case carries the coastal-leakage gotcha
as well.[^dataset][^leakage] A small basin's storage question is
answered from the mascons that contain it, described as that region,
or from another observation (wells, snow products, reservoir records)
with GRACE as the regional context.

**Verification.** The product's own attributes state the native
resolution and the per-mascon uncertainty, and the collection page
describes the mascons as an inherent smoother with the gain factors as
the sub-mascon option.[^virtual-listing][^product-page] The floor
number is owned by the computation concept and recomputed there from
the release in hand.[^water-balance] Live checks on 2026-09-13: the
collection page was read; the virtual dataset reference file in the
public bucket was read for the attributes quoted above; the four
papers' records were verified against the Crossref registry the same
day (title, authors, journal, year) and their abstracts read there,
which is where the few-hundred-kilometer resolution, the 160,000 km2
basin size with its leakage percentages and the 176-basin evaluation
come from; the Wiley journal pages sit behind a bot check, so the
papers' full guidance on the smallest usable basin beyond their
abstracts is not quoted here; the GRACE Tellus data pages returned 404
on the day.

[^product-page]: PO.DAAC collection page: TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4
[^virtual-listing]: The collection's virtual dataset reference file (grid and uncertainty attributes)
[^landerer-2012]: Landerer and Swenson, 2012, Water Resources Research, doi:10.1029/2011WR011453
[^wiese-2016]: Wiese, Landerer and Watkins, 2016, Water Resources Research, doi:10.1002/2016WR019344
[^scanlon-2016]: Scanlon and others, 2016, Water Resources Research, doi:10.1002/2016WR019494
[^watkins-2015]: Watkins and others, 2015, Journal of Geophysical Research: Solid Earth, doi:10.1002/2014JB011547
[^dataset]: The provider bundle's mascon dataset concept
[^leakage]: The provider bundle's coastal-leakage gotcha
[^water-balance]: This bundle's basin water balance computation
[^recipe]: This bundle's basin TWS recipe
