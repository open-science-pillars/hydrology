---
type: dataset-gotcha
spheres: [hydrosphere]
title: "The mascon gain factors: applied once, to the CRI grid, for land hydrology, and meaningless over ice and ocean"
description: "The scale_factor field shipped in the JPL mascon CRI granule is a set of gridded gain factors derived from a land model's simulated hydrology (CLM, 2002 to 2009) to restore the sub-mascon signal the mascon parameterization and its constraint smooth away, for continental hydrology. They multiply the CRI-filtered lwe_thickness once, cell by cell, before any basin sum; they are not the spherical-harmonic Tellus gain factors, which belong to a different product; a series scaled twice, or scaled with the wrong set, is amplified by a model pattern that was never meant for it; and over ice sheets, glaciers and the ocean the factors carry no information about the mass that is there, so a scaled ice or ocean series is wrong. The placement, land mask and scale factor files have not changed since RL05M."
tags: [grace, grace-fo, mascons, scale-factors, gain-factors, clm, hydrology, ice, ocean, cri]
generated: { by: knowledge-seeder/claude, at: 2026-09-13T20:40:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-13T21:08:45Z, role: maintainer, source: https://github.com/open-science-pillars/hydrology/pull/57 }
severity: medium
# medium, not high: the factors are optional and documented, and the
# trap bites through a misapplied option (twice, the wrong set, or the
# wrong surface) rather than through a silently wrong default series;
# the unscaled series is always the one the product delivers.
# The dataset concept for the product lives in the PO.DAAC provider
# bundle (knowledge/podaac/datasets/grace-fo-mascons.md in
# nasa-daac-knowledge, installed beside this plugin). This key carries
# the product page, the same resource the recipe's sources name, and
# the provider concepts are cited in sources by their repository URL
# at a pinned commit, so neither depends on where the bundle is
# installed.
dataset: https://podaac.jpl.nasa.gov/dataset/TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4
status: stable
stale_after: 2027-03-13
sources:
  - id: product-page
    resource: https://podaac.jpl.nasa.gov/dataset/TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4
    title: "PO.DAAC collection page: TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4 (the mascons act as an inherent smoother; a set of optional gain factors is provided within the netCDF for sub-mascon resolution, for example continental hydrology, with Wiese and others 2016 as the reference)"
  - id: virtual-listing
    resource: https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-public/virtual_collections/TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4/TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4_virtual_https.json
    title: "The collection's virtual dataset reference file: the scale_factor variable ('Gridded scale factors to be used with mascon solution that has the CRI filter applied; based on CLM data from 2002-2009', dimensionless, valid range about -2.9 to 24.1), the land_mask used with the CRI filter, and the GAD field added back to ocean pixels only"
  - id: release-note
    resource: https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/gracefo/open/docs/GRACE_GRACE-FO_ReleaseNotes_JPL_MASCON.txt
    title: "JPL GRACE mascon solution release notes (RL06.3M version 4): the land mask, mascon placement and scale factor files unchanged from RL05M to RL06M and from RL06M version 1 to version 2"
  - id: wiese-2016
    resource: https://doi.org/10.1002/2016WR019344
    title: "Wiese, Landerer and Watkins, 2016, Quantifying and reducing leakage errors in the JPL RL05M GRACE mascon solution, Water Resources Research (a set of gain factors derived to reduce leakage errors for continental hydrology applications; combined with the CRI filter they reduce the leakage error of basins above 160,000 km2 by 11 to 30 per cent averaged globally, locally 38 to 81 per cent)"
  - id: landerer-2012
    resource: https://doi.org/10.1029/2011WR011453
    title: "Landerer and Swenson, 2012, Accuracy of scaled GRACE terrestrial water storage estimates, Water Resources Research (the gain factors for the gridded spherical harmonic TWS product, a different set for a different product, derived from land hydrology model simulations independent of the GRACE data)"
  - id: watkins-2015
    resource: https://doi.org/10.1002/2014JB011547
    title: "Watkins and others, 2015, Improved methods for observing Earth's time variable mass distribution with GRACE using spherical cap mascons, Journal of Geophysical Research: Solid Earth (mascon solutions lower the dependence on scale factors: the global mean scale factor decreases by 0.17 against the spherical harmonic solution)"
  - id: dataset
    resource: https://github.com/open-science-pillars/nasa-daac-knowledge/blob/16152b3776cd1307a9a4e03bab3f5376e9b5e63b/knowledge/podaac/datasets/grace-fo-mascons.md
    title: "The provider bundle's mascon dataset concept (knowledge/podaac/datasets/grace-fo-mascons.md in nasa-daac-knowledge, cited at a pinned commit): the scale factors come from a land hydrology model and are not applied over ice"
  - id: sea-level-recipe
    resource: https://github.com/open-science-pillars/nasa-daac-knowledge/blob/16152b3776cd1307a9a4e03bab3f5376e9b5e63b/knowledge/podaac/recipes/grace-mass-to-sea-level.md
    title: "The provider bundle's mass-to-sea-level recipe (knowledge/podaac/recipes/grace-mass-to-sea-level.md): an ice-sheet region sums the unscaled mascons, the factors being for hydrology"
  - id: recipe
    resource: ../recipes/grace-basin-tws.md
    title: "This bundle's basin TWS recipe: the factors applied once, cell by cell, to the CRI grid of a land hydrology region, with the unscaled series kept beside the scaled one"
  - id: floor
    resource: ./grace-basin-below-resolution-floor.md
    title: "This bundle's resolution-floor gotcha: the factors are not a way to resolve a basin below one mascon"
---

# The mascon gain factors: applied once, to the CRI grid, for land hydrology

**Mechanism.** The mascon solution estimates one value per 3-degree
mascon under an a priori constraint, so the mascons act as an inherent
smoother on the field; the product ships an optional set of gain
factors within the netCDF so that mass change can be studied at
sub-mascon resolution, "e.g. for continental hydrology applications",
and names the paper that derived them.[^product-page] In the granule
the field is `scale_factor`, described as "Gridded scale factors to be
used with mascon solution that has the CRI filter applied; based on
CLM data from 2002-2009", dimensionless, with a valid range from about
-2.9 to 24.1.[^virtual-listing] The product team derived the factors
to reduce the leakage error that parameterizing the gravity field in
mascons introduces, for continental hydrology, and measured the
effect: combined with the CRI filter, the gain factors reduce the
leakage error in the mass balance of large basins (above 160,000 km2)
by 11 to 30 per cent averaged globally, with local improvements of 38
to 81 per cent.[^wiese-2016]
The factors are a model's spatial pattern: the granule states they
are based on the CLM land model over 2002 to 2009, the same kind of
construction as the earlier gain factors for the gridded spherical
harmonic product, which were inferred from land hydrology model
simulations at different spatial scales, independent of the GRACE
data, and are a different set for a different product.[^virtual-listing][^landerer-2012] The
mascon solution needs less of this than a spherical harmonic one (the
global mean scale factor falls by 0.17), which is why the factors are
an option and not a step.[^watkins-2015] The placement, land mask and
scale factor files have not changed since RL05M, so the factors in
hand are the ones every release since has shipped.[^release-note]

**Wrong-result mode.** Three misapplications, none of which errors.
Applied twice (once by a loader that scales on read, once by an
analysis that scales the series it was handed, or the spherical
harmonic Tellus factors laid over the mascon grid), the series is
amplified by the square of a model pattern whose valid range in the
granule reaches 24.[^virtual-listing][^landerer-2012]
Applied over an ice sheet or a glacier region, the factors carry a
land model's hydrology pattern where the mass change is ice, so a
scaled ice mass series is a hydrology model's opinion of the ice;
the provider bundle's ice and sea level work sums the unscaled
mascons for that reason, and its dataset concept states that the
factors are not applied over ice.[^sea-level-recipe][^dataset]
Applied over ocean cells, where the CRI grid carries ocean mass with
the de-aliasing model added back, the factors scale a quantity they
were never derived for.[^virtual-listing] And applied to a basin the
product cannot resolve, they turn a missing measurement into a
number.[^floor]

**Correct approach.** For a land hydrology region the factors
multiply the CRI-filtered `lwe_thickness` once, cell by cell, over the
land-mask cells of the region's mascons, before the area-weighted sum;
the unscaled series is kept beside the scaled one, the statement
names which it quotes, and their difference is one bound on the
leakage term.[^recipe] Nothing scales a series a second time, nothing
applies the spherical harmonic product's factors to the mascon grid,
and an ice, glacier or ocean region is summed unscaled.[^dataset][^sea-level-recipe]

**Verification.** The granule's own variable attributes state the
factors' basis and their pairing with the CRI filter; the collection
page states their purpose and their optional
status.[^virtual-listing][^product-page] Live checks on 2026-09-13:
the collection page, the virtual dataset reference file and the
release note were read; the three papers' records were verified
against the Crossref registry the same day (title, authors, journal,
year) and their abstracts read there, which is where the measured
leakage reductions and the 0.17 figure come from; the Wiley journal
pages sit behind a bot check, and the GRACE Tellus data pages returned
404 on the day.

[^product-page]: PO.DAAC collection page: TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4
[^virtual-listing]: The collection's virtual dataset reference file (the scale_factor, land_mask and GAD variables)
[^release-note]: JPL GRACE mascon solution release notes, RL06.3M version 4
[^wiese-2016]: Wiese, Landerer and Watkins, 2016, Water Resources Research, doi:10.1002/2016WR019344
[^landerer-2012]: Landerer and Swenson, 2012, Water Resources Research, doi:10.1029/2011WR011453
[^watkins-2015]: Watkins and others, 2015, Journal of Geophysical Research: Solid Earth, doi:10.1002/2014JB011547
[^dataset]: The provider bundle's mascon dataset concept
[^sea-level-recipe]: The provider bundle's mass-to-sea-level recipe
[^recipe]: This bundle's basin TWS recipe
[^floor]: This bundle's resolution-floor gotcha
