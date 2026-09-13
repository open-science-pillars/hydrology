---
type: dataset-gotcha
spheres: [hydrosphere]
title: "GRACE terrestrial water storage is every store together: a groundwater trend from GRACE minus a land surface model inherits the model's soil moisture and snow errors as a term"
description: "The mascon anomaly is the change in total mass on land: snow and ice, surface water, soil moisture, canopy water and groundwater, inseparable in the measurement. Groundwater from GRACE is the residual after the other stores are subtracted from a land surface model or from observations, so whatever the model gets wrong in its soil moisture and snow (amplitude, phase, trend) lands in the groundwater series with the sign reversed, and the residual arrives without an error bar unless the model's is stated as a term beside the formal error."
tags: [grace, grace-fo, tws, groundwater, soil-moisture, snow, land-surface-model, residual, partitioning]
generated: { by: knowledge-seeder/claude, at: 2026-09-13T20:40:00Z }
severity: medium
# medium, not high: the total-storage nature of the measurement is
# documented product behavior and the residual method is the published
# one; the trap bites through an understated uncertainty on the
# residual rather than through a silently wrong single-product series,
# and the recipe that owns the method already states it.
# The dataset concept for the product lives in the PO.DAAC provider
# bundle (knowledge/podaac/datasets/grace-fo-mascons.md in
# nasa-daac-knowledge, installed beside this plugin). This key carries
# the product page, the same resource the recipe's sources name, and
# the provider concepts are cited in sources by their repository URL
# at a pinned commit, so neither depends on where the bundle is
# installed.
dataset: https://podaac.jpl.nasa.gov/dataset/TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4
status: draft
stale_after: 2027-03-13
sources:
  - id: product-page
    resource: https://podaac.jpl.nasa.gov/dataset/TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4
    title: "PO.DAAC collection page: TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4 (gridded monthly global water storage anomalies, surface mass change in equivalent water thickness)"
  - id: virtual-listing
    resource: https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-public/virtual_collections/TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4/TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4_virtual_https.json
    title: "The collection's virtual dataset reference file: the lwe_thickness variable (Liquid_Water_Equivalent_Thickness, cm) and the file's summary, monthly gravity solutions with the CRI filter applied"
  - id: joodaki-2014
    resource: https://doi.org/10.1002/2013WR014633
    title: "Joodaki, Wahr and Swenson, 2014, Estimating the human contribution to groundwater depletion in the Middle East, from GRACE data, land surface models, and well observations, Water Resources Research (the residual method: lakes and the Caspian subtracted, then CLM4.5 soil moisture, snow, canopy and river storage; the groundwater loss quoted with its uncertainty; wells as the independent check)"
  - id: scanlon-2016
    resource: https://doi.org/10.1002/2016WR019494
    title: "Scanlon and others, 2016, Global evaluation of new GRACE mascon products for hydrologic applications, Water Resources Research (long-term trends up to 20 mm per year against seasonal amplitudes up to 250 mm across 176 basins)"
  - id: dataset
    resource: https://github.com/open-science-pillars/nasa-daac-knowledge/blob/16152b3776cd1307a9a4e03bab3f5376e9b5e63b/knowledge/podaac/datasets/grace-fo-mascons.md
    title: "The provider bundle's mascon dataset concept (knowledge/podaac/datasets/grace-fo-mascons.md in nasa-daac-knowledge, cited at a pinned commit): monthly mass anomaly as equivalent water thickness, with the formal errors as the floor"
  - id: partitioning
    resource: ../recipes/grace-groundwater-partitioning.md
    title: "This bundle's groundwater partitioning recipe: groundwater as the TWS-minus-other-stores residual, bounded below by the mascon formal error and dominated by the subtrahends"
  - id: recipe
    resource: ../recipes/grace-basin-tws.md
    title: "This bundle's basin TWS recipe: what a TWS number contains and what subtracting modeled stores assumes"
  - id: snodas
    resource: ./snodas-not-a-budget-term.md
    title: "This bundle's SNODAS gotcha: a modeled snow product is comparable between periods, not a measured budget term"
---

# GRACE terrestrial water storage is every store together

**Mechanism.** The mascon product is the change in surface mass,
expressed as a thickness of water: the collection describes it as
gridded monthly water storage anomalies, and the variable is the
liquid water equivalent thickness of whatever mass moved.[^product-page][^virtual-listing]
On land that is snow and ice, water in rivers, lakes and reservoirs,
soil moisture, canopy water and groundwater, added together by
gravity; the measurement does not separate them.[^dataset] Across 176
basins the mascon products show long-term trends of up to about 20
millimeters per year on seasonal amplitudes of up to 250 millimeters,
so a trend in one store is a small number under a large seasonal
cycle that every store shares in.[^scanlon-2016] Groundwater
from GRACE is therefore a residual. The published Middle East
analysis is the pattern: the Caspian Sea and two large lakes were
subtracted first, then a version of the CLM4.5 land surface model
supplied the soil moisture, snow, canopy and river storage to remove,
and the remainder was attributed to groundwater, checked against wells
and quoted with an uncertainty.[^joodaki-2014]

**Wrong-result mode.** A groundwater series is produced as the
mascon series minus a land surface model's soil moisture and snow,
and its trend is quoted with the GRACE formal error alone. The model's
snow water equivalent that melts a month early, a soil column too
shallow to hold a wet year, a spin-up drift or a forcing bias with a
trend of its own: each is subtracted from a total that did not contain
it, so it appears in the groundwater series with the opposite sign
and the same size. A modeled snow product used as a subtrahend brings
its own version of this (the SNODAS gotcha).[^snodas] Nothing errors,
and the residual's stated uncertainty is the smallest term in it.

**Correct approach.** A groundwater residual names each subtrahend
with its product and version, and carries the model's error as its
own term beside the GRACE formal error: the residual's uncertainty is
bounded below by the mascon formal error and is usually dominated by
the subtrahends, so a groundwater trend quoted with the GRACE error
alone is understated.[^partitioning][^recipe] Where the model has no
error statement, the spread between two land surface models or
between the model and an observed store (a snow product, soil moisture
from SMAP, reservoir records) stands in and is labelled as such. An
attribution of the groundwater trend to pumping or to climate needs
independent evidence, as the wells were in the published
case.[^joodaki-2014][^partitioning]

**Verification.** The product describes itself as total water storage
in equivalent water thickness, and the provider concept and this
bundle's partitioning recipe record the residual's error
structure.[^product-page][^dataset][^partitioning] Live checks on
2026-09-13: the collection page and the virtual dataset reference
file were read; the two papers' records were verified against the
Crossref registry the same day (title, authors, journal, year) and
their abstracts read there, which is where the subtracted stores and
the trend and seasonal magnitudes come from; the Wiley journal pages
sit behind a bot check.

[^product-page]: PO.DAAC collection page: TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4
[^virtual-listing]: The collection's virtual dataset reference file (the lwe_thickness variable and the file summary)
[^joodaki-2014]: Joodaki, Wahr and Swenson, 2014, Water Resources Research, doi:10.1002/2013WR014633
[^scanlon-2016]: Scanlon and others, 2016, Water Resources Research, doi:10.1002/2016WR019494
[^dataset]: The provider bundle's mascon dataset concept
[^partitioning]: This bundle's groundwater partitioning recipe
[^recipe]: This bundle's basin TWS recipe
[^snodas]: This bundle's SNODAS gotcha
