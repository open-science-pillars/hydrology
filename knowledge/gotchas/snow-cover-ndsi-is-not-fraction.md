---
type: dataset-gotcha
spheres: [hydrosphere, cryosphere]
title: "NDSI snow cover is an index thresholded into snow, not a fraction of the cell: a value of 40 is not 40 per cent snow, and the codes above 100 are not values"
description: "NDSI_Snow_Cover in MOD10A1, MOD10A1F and VNP10A1 holds the Normalized Difference Snow Index scaled to 0 to 100 for cells where the algorithm detected snow, and any positive index after the screens means some snow is present. It is not a sub-pixel fraction: fractional snow cover is not calculated in Collection 6.1, and the climate modeling grid percentages are tallies of binary detections over 0.05 degree cells. Values from 200 up are codes (250 is cloud). A snow-covered area computed as value over 100 times cell area, or a basin mean that includes the codes, is a number with no physical meaning."
tags: [modis, viirs, snow-cover, ndsi, fractional-snow-cover, fsc, mod10a1, vnp10a1, flags, nsidc, cryosphere, hydrology]
generated: { by: knowledge-seeder/claude, at: 2026-09-14T05:30:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-14T12:13:16Z, role: maintainer, source: https://github.com/open-science-pillars/hydrology/pull/61 }
severity: high
dataset: ../datasets/modis-viirs-snow-cover.md
eval_case: snow-cover-ndsi-is-not-fraction
status: draft
stale_after: 2027-03-14
sources:
  - id: faq-ndsi
    resource: https://nsidc.org/data/user-resources/help-center/what-ndsi-snow-cover-and-how-does-it-compare-fsc
    title: "The NSIDC help article 'What is NDSI snow cover and how does it compare to FSC?', read 2026-09-14: NDSI snow cover as an index related to the presence of snow, the whole 0.0 to 1.0 range used from version 6, and the Collection 5 FSC as an empirical Landsat relationship it replaced"
  - id: mod10a1-guide
    resource: https://nsidc.org/sites/default/files/mod10a1-v061-userguide_1.pdf
    title: "MOD10A1 version 61 user guide, NSIDC, last updated December 2021, read 2026-09-14: Table 1 (0 to 100 NDSI snow cover and the codes 200 to 255), the low NDSI screen, the true cell size and the accuracy range"
  - id: vnp10a1-guide
    resource: https://nsidc.org/sites/default/files/documents/user-guide/multi_vnp10a1-v002-userguide.pdf
    title: "VNP10A1 version 2 user guide, NSIDC, last updated January 2026, read 2026-09-14: values greater than 0 typically indicating at least some snow, the NDSI_Snow_Cover codes, and the packed NDSI field"
  - id: c61-guide
    resource: https://nsidc.org/sites/default/files/c61_modis_snow_user_guide.pdf
    title: "MODIS Snow Products Collection 6.1 User Guide, Riggs, Hall and Roman, 2019, read 2026-09-14: the NDSI formula, 'a pixel with 0.0 < NDSI <= 1.0 is considered to have some snow present', 'FSC is not calculated in C6.1', the binary interpretation in the climate modeling grid binning, and the monthly fractional example"
  - id: viirs-c2-guide
    resource: https://nsidc.org/sites/default/files/documents/technical-reference/snpp_jpss1_viirs_snow_cover_products_collection_2_user_guide.pdf
    title: "SNPP/JPSS1 VIIRS Snow Cover Products Collection 2 User Guide, Riggs and Hall, 2021, read 2026-09-14: NDSI values scaled to 0 to 100 in the algorithm and written to NDSI_Snow_Cover, and also written packed to the NDSI variable"
  - id: salomonson-appel-2004
    resource: https://doi.org/10.1016/j.rse.2003.10.016
    title: "Salomonson and Appel, 2004, Estimating fractional snow cover from MODIS using the normalized difference snow index, Remote Sensing of Environment 89(3), 351 to 360; the Crossref record read 2026-09-14 (no abstract in the record; the journal page sits behind a bot check); the regression the NSIDC page names for converting NDSI to a fraction"
  - id: hall-riggs-2007
    resource: https://doi.org/10.1002/hyp.6715
    title: "Hall and Riggs, 2007, Accuracy assessment of the MODIS snow products, Hydrological Processes 21(12), 1534 to 1547; the Crossref abstract read 2026-09-14: the Collection 5 products carried an FSC layer, and the daily products' accuracy of about 93 per cent is a detection accuracy"
  - id: mod10a1-page
    resource: https://nsidc.org/data/mod10a1/versions/61
    title: "The NSIDC product page for MOD10A1 version 61, read 2026-09-14: 'users can use the NDSI as is or convert it to fractional or binary snow cover', citing Salomonson and Appel 2004 and Riggs and others 2019"
---

# NDSI snow cover is an index, not a fraction

**Mechanism.** The algorithm computes the Normalized Difference Snow
Index from a visible and a shortwave infrared band, MODIS band 4
against band 6 and VIIRS I1 against I3. Its logic is that snow always
has an NDSI above 0.0 while not every feature above 0.0 is snow, so a
pixel with 0.0 < NDSI <= 1.0 "is considered to have some snow present"
and the screens then reverse or flag the doubtful cases (a detection
below 0.1 is reversed to not snow). The index of each surviving
detection is scaled to 0 to 100 and written to `NDSI_Snow_Cover`; the
same index goes to the `NDSI` field unscreened. The number is a
spectral index that says snow is present and how strong the
visible-against-shortwave contrast was, and NSIDC's own gloss is that
it is "an index that is related to the presence of snow in a
pixel".[^c61-guide][^viirs-c2-guide][^faq-ndsi][^mod10a1-guide][^vnp10a1-guide]
Fractional snow cover is a different quantity with a history: the
Collection 5 products carried an FSC layer computed by an empirical
relationship between NDSI and the snow extent in Landsat 30 m pixels
inside a MODIS cell, from Salomonson and Appel 2004. Collection 6
replaced that layer with the NDSI snow cover and used the whole 0.0 to
1.0 range for detection, and the Collection 6.1 guide states it flat:
"FSC is not calculated in C6.1". The product page says a user "can use
the NDSI as is or convert it to fractional or binary snow cover", and
a conversion is the user's, with its regression and its
provenance.[^faq-ndsi][^hall-riggs-2007][^salomonson-appel-2004][^c61-guide][^mod10a1-page]
The percentages in the coarser climate modeling grid products are not
sub-pixel fractions either: the binning algorithm interprets the 0 to
100 value "as a binary snow flag" and reports the share of snow
observations among the 500 m observations in a 0.05 degree cell, and
the monthly product scales that share by the clear-view
index.[^c61-guide]

Everything above 100 is a code, stored in the same 8-bit field: 200
missing, 201 no decision, 211 night, 237 inland water, 239 ocean, 250
cloud, 254 detector saturated, 255 fill on MODIS, and on VIIRS 251 to
255 for missing or failed input, bowtie trim and fill. A winter tile is
dominated by 250.[^mod10a1-guide][^vnp10a1-guide]

**Wrong-result mode.** A snow-covered area computed as the sum over
cells of value divided by 100 times the cell area, or a basin snow
fraction computed as the mean of `NDSI_Snow_Cover` over the polygon.
The first understates extent wherever the index is below 100, which is
most snow, and the understatement moves with illumination, vegetation
and snow condition rather than with extent, so a series of such areas
carries a signal that is not snow extent. The second is worse: any
cloudy cell contributes 250 to the mean, so a half-clouded basin
returns a "fraction" above 100 and a lightly clouded one a fraction
inflated by a term that is cloud. A comparison against a fractional
product of another sensor, or against the Collection 5 FSC, then
compares an index with a fraction. Nothing fails: the field is
unsigned 8-bit, the arithmetic runs, and the units look like per cent.
The published accuracy of about 93 per cent is the accuracy of the
snow or no snow decision under clear sky and says nothing about a
fraction.[^mod10a1-guide][^hall-riggs-2007]

**Correct approach.** Extent is counted, not summed: a cell with a
value from 1 to 100 (or above a threshold the analysis declares) is a
snow-covered cell, a cell at 0 is snow-free, and every code above 100
is neither and is tallied by what it is, with cloud (250) reported
beside the extent as the share of the basin that was not observed.
The count times the cell area is the extent: the true MODIS cell is
463.31271653 m on a side, so a 500 m cell covers 0.2147 km2 (that
length squared) and a tile 2400 by 2400 of them. A fraction of a cell,
where one is needed, is a declared conversion: Salomonson and Appel's
regression with its citation, developed for the Collection 5 Terra
products, or a fractional product of another sensor, named as such.
The receipt records the threshold or the conversion, the cloud share,
and the product and version, so a later reader can tell an extent
from a fraction.[^mod10a1-guide][^mod10a1-page][^salomonson-appel-2004][^faq-ndsi]

**Verification.** A histogram of `NDSI_Snow_Cover` over a winter tile
shows the mass above 100 sitting on the code values, with 250
dominant, and nothing between 101 and 199. For the snow cells, the
`NDSI` field divided by 10000 (MODIS) or times 0.001 (VIIRS) reproduces
the `NDSI_Snow_Cover` value divided by 100 up to rounding, which shows
the field is the index and not a separate fraction. The local
attributes of the fields (`flag_values` and `flag_meanings` on VIIRS,
the coded integer keys on MODIS) list the codes; a file's own
`long_name` for the field reads "NDSI snow cover".[^c61-guide][^viirs-c2-guide][^vnp10a1-guide]

[^faq-ndsi]: the NSIDC help article on NDSI snow cover and FSC, read 2026-09-14
[^mod10a1-guide]: the MOD10A1 version 61 user guide, last updated December 2021
[^vnp10a1-guide]: the VNP10A1 version 2 user guide, last updated January 2026
[^c61-guide]: the MODIS Snow Products Collection 6.1 User Guide, 2019
[^viirs-c2-guide]: the VIIRS Snow Cover Products Collection 2 User Guide, 2021
[^salomonson-appel-2004]: Salomonson and Appel 2004, Remote Sensing of Environment, Crossref record
[^hall-riggs-2007]: Hall and Riggs 2007, Hydrological Processes, Crossref record and abstract
[^mod10a1-page]: the NSIDC product page for MOD10A1 version 61, read 2026-09-14
