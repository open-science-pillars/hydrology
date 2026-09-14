---
type: dataset-gotcha
spheres: [hydrosphere, cryosphere]
title: "Snow cover is where the snow is, not how much: an observed NDSI index and SNODAS's modelled snow water equivalent are different quantities that arrive as daily grids of the same shape"
description: "MOD10A1 and VNP10A1 report an index of snow presence per cell, 0 to 100, from visible and shortwave reflectance, with no depth and no mass in it; a cell at 100 says the contrast was strong, not that the pack is deep. SNODAS, the snow product beside it in this bundle, is a model output whose layers are snow water equivalent and depth in metres. Extent and amount are complementary and neither substitutes for the other: a full-extent basin with a thin pack and one with a deep pack read alike in the index, and a snow water equivalent field says nothing about the day's observed extent."
tags: [modis, viirs, snow-cover, ndsi, snodas, snow-water-equivalent, swe, extent, model-output, nsidc, cryosphere, hydrology]
generated: { by: knowledge-seeder/claude, at: 2026-09-14T05:30:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-14T12:13:16Z, role: maintainer, source: https://github.com/open-science-pillars/hydrology/pull/61 }
severity: low
dataset: ../datasets/modis-viirs-snow-cover.md
status: stable
stale_after: 2027-03-14
sources:
  - id: mod10a1-guide
    resource: https://nsidc.org/sites/default/files/mod10a1-v061-userguide_1.pdf
    title: "MOD10A1 version 61 user guide, NSIDC, last updated December 2021, read 2026-09-14: the NDSI as the magnitude of the visible against shortwave contrast, the 0 to 100 NDSI snow cover field, and the snow albedo field as the product's other quantity"
  - id: faq-ndsi
    resource: https://nsidc.org/data/user-resources/help-center/what-ndsi-snow-cover-and-how-does-it-compare-fsc
    title: "The NSIDC help article 'What is NDSI snow cover and how does it compare to FSC?', read 2026-09-14: the index is related to the presence of snow in a pixel"
  - id: g02158-page
    resource: https://nsidc.org/data/g02158
    title: "The NSIDC data set page for SNODAS (G02158), read 2026-09-14: snow pack properties such as depth and snow water equivalent from a modeling and data assimilation system, 1 km, daily from 30 September 2003"
  - id: snodas-connector
    resource: ../connectors/snodas-nsidc.md
    title: "This bundle's SNODAS connector concept: the eight layers read from the file headers, with snow water equivalent and depth in metres divided by 1000 and the model provenance"
  - id: snodas-gotcha
    resource: ../gotchas/snodas-not-a-budget-term.md
    title: "This bundle's SNODAS gotcha: a model output that compares between periods and is not a term in a water budget"
  - id: riggs-2017
    resource: https://doi.org/10.5194/essd-9-765-2017
    title: "Riggs, Hall and Roman, 2017, Overview of NASA's MODIS and VIIRS snow-cover Earth System Data Records, Earth System Science Data 9(2), 765 to 777; the Crossref abstract read 2026-09-14: the products map snow cover extent, an essential climate variable, and the algorithms optimise the accuracy of mapping that extent"
---

# Snow cover is not snow water equivalent

**Mechanism.** The MODIS and VIIRS snow products answer one question,
whether snow is present in a cell, and their objective is "to optimize
the accuracy of mapping snow-cover extent". The value they carry is
the Normalized Difference Snow Index, the magnitude of the difference
between a visible and a shortwave infrared reflectance, scaled to 0 to
100, "an index that is related to the presence of snow in a pixel".
No depth, density or mass enters the algorithm and none leaves it; the
product's other quantity is a snow albedo, also
dimensionless.[^riggs-2017][^mod10a1-guide][^faq-ndsi] The snow
amount product beside it in this bundle is SNODAS, whose layers are
modelled snow water equivalent and snow depth in metres (stored as
integers divided by 1000), melt, sublimation and pack temperature, at
1 km over the conterminous United States, daily, from a modelling and
data assimilation system rather than from an
observation.[^g02158-page][^snodas-connector] The two arrive in the
same shape, a daily grid with a snow word in its name from the same
archive, and that is the whole of the resemblance: one is an observed
index of presence on a sinusoidal 500 m or 375 m grid, the other a
modelled amount on a geographic 1 km grid.

**Wrong-result mode.** A basin whose cells all read 100 is described
as fully snow-packed, when the index says only that snow was seen and
its contrast was strong; a spring decline in the basin-mean index is
read as melt of the pack, when it is a mix of shrinking extent and
changing surface contrast; a snow water equivalent is assigned to a
cell because the index says snow, or a modelled snow water equivalent
is called observed because an observed extent agrees with where it is
non-zero. In the reverse direction, SNODAS's snow water equivalent is
used as the day's observed extent, which no model output is, and its
zeros are read as observed bare ground. The mistake is a category
error rather than a silent numerical one, which is why its severity is
low: the index has no length unit and the SNODAS header states
metres, so a units check catches it, and the SNODAS gotcha in this
bundle already keeps the model output out of a
budget.[^snodas-gotcha][^snodas-connector]

**Correct approach.** Extent comes from the observation and amount
from the model, each named for what it is. A snow panel that shows
where the snow is uses the index thresholded into a snow-covered area
with its cloud share, and a panel that shows how much uses SNODAS with
the distributor's limits stated, as the SNODAS gotcha sets out. A
statement that joins them says so: an observed extent of this many
square kilometres on this date, and a modelled water equivalent over
the same polygon, from two products with two provenances. Neither is
converted into the other.[^snodas-gotcha][^mod10a1-guide]

**Verification.** The `NDSI_Snow_Cover` field's attributes carry no
length unit and its `long_name` reads "NDSI snow cover"; the SNODAS
layer headers name "Modeled snow water equivalent" with a scale in
metres. A basin where the MODIS index is 100 across the pack and the
SNODAS water equivalent ranges over an order of magnitude across the
same cells shows the two are not the same
quantity.[^mod10a1-guide][^snodas-connector]

[^riggs-2017]: Riggs, Hall and Roman 2017, Earth System Science Data, Crossref record and abstract
[^mod10a1-guide]: the MOD10A1 version 61 user guide, last updated December 2021
[^faq-ndsi]: the NSIDC help article on NDSI snow cover and FSC, read 2026-09-14
[^g02158-page]: the NSIDC data set page for SNODAS, read 2026-09-14
[^snodas-connector]: this bundle's SNODAS connector concept
[^snodas-gotcha]: this bundle's SNODAS gotcha
