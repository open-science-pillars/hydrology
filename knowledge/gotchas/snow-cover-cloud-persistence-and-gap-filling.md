---
type: dataset-gotcha
spheres: [hydrosphere, cryosphere]
title: "Cloud hides snow on the days snow changes, and the gap-filled product reuses an older view whose age is a field the reader has to consult"
description: "In MOD10A1 and VNP10A1 a cell under confident cloud is 250, and the storms that deposit snow are the days the surface is not seen. MOD10A1F fills each cloudy cell with the most recent clear observation and counts the days since it in Cloud_Persistence: 0 means the cell was seen today, 1 that today was cloudy, larger values the run of cloudy days. A missing input tile advances the count for every cell, fill is treated like cloud, and the series restarts each water year from a copy of the day's MOD10A1. Snow that fell and melted under cloud is never mapped, a change under cloud appears on the day the cloud clears, and a nearly cloud-free map typically takes five to seven days to build."
tags: [modis, viirs, snow-cover, cloud, cloud-gap-filled, cgf, mod10a1f, cloud-persistence, vnp10a1f, nsidc, cryosphere, hydrology]
generated: { by: knowledge-seeder/claude, at: 2026-09-14T05:30:00Z }
severity: medium
dataset: ../datasets/modis-viirs-snow-cover.md
status: draft
stale_after: 2027-03-14
sources:
  - id: mod10a1f-guide
    resource: https://nsidc.org/sites/default/files/mod10a1f-v061-userguide_0.pdf
    title: "MOD10A1F version 61 user guide, NSIDC, last updated 10 December 2021, read 2026-09-14: the fields, the Cloud_Persistence semantics (0, 1, greater than 1), the five to seven days, the water-year series and its first-day attributes, missing tiles and fill"
  - id: mod10a1f-page
    resource: https://nsidc.org/data/mod10a1f/versions/61
    title: "The NSIDC product page for MOD10A1F version 61, read 2026-09-14: the overview and the limitation that snow which fell and melted before the clouds cleared may not be mapped"
  - id: mod10a1-page
    resource: https://nsidc.org/data/mod10a1/versions/61
    title: "The NSIDC product page for MOD10A1 version 61, read 2026-09-14: cloud cover as the biggest limitation of the products"
  - id: c61-guide
    resource: https://nsidc.org/sites/default/files/c61_modis_snow_user_guide.pdf
    title: "MODIS Snow Products Collection 6.1 User Guide, Riggs, Hall and Roman, 2019, read 2026-09-14: Section 12 on the CGF algorithm, the cloud persistence count, the first day of a series, missing days processed as cloudy, fill processed like cloud, and cloud and snow confusion carried through as persistent cloud"
  - id: hall-2019
    resource: https://doi.org/10.5194/hess-23-5227-2019
    title: "Hall, Riggs, DiGirolamo and Roman, 2019, Evaluation of MODIS and VIIRS cloud-gap-filled snow-cover products for production of an Earth science data record, Hydrology and Earth System Sciences 23(12), 5227 to 5241; the Crossref abstract read 2026-09-14: the CGF products include cloud-persistence statistics showing the age of the observation in each pixel"
  - id: hall-2010
    resource: https://doi.org/10.1016/j.rse.2009.10.007
    title: "Hall, Riggs, Foster and Kumar, 2010, Development and evaluation of a cloud-gap-filled MODIS daily snow-cover product, Remote Sensing of Environment 114(3), 496 to 503; the Crossref record read 2026-09-14 (no abstract in the record; the journal page sits behind a bot check); the method the product guides cite for retaining the previous clear view"
  - id: cmr
    resource: https://cmr.earthdata.nasa.gov/search/collections.json?short_name[]=MOD10A1F&short_name[]=VNP10A1F&short_name[]=MYD10A1F
    title: "The CMR collection records for MOD10A1F (C3028765772-NSIDC_CPRD), VNP10A1F (C3173405448-NSIDC_CPRD) and MYD10A1F (C3091257892-NSIDC_CPRD), searched 2026-09-14"
---

# Cloud persistence and the gap-filled product

**Mechanism.** The snow algorithm reads the cloud mask and writes 250
into every cell the mask calls confident cloudy. Cloud is "the biggest
limitation to the use of the MODIS snow-cover products", and it is not
a random gap: the days on which snow arrives are storm days, so the
observation is missing when the surface changes most.[^mod10a1-page]
The cloud-gap-filled product exists for this. MOD10A1F takes the
day's MOD10A1 and the previous day's MOD10A1F and replaces each cloudy
cell with the previous clear view, following Hall and others 2010;
`Cloud_Persistence` counts the days since the cell was last seen: 0
when the current day was clear, 1 when the current day was cloudy,
and above 1 the number of consecutive cloud-obscured days. A missing
MOD10A1 tile is processed as a fully cloudy day, so every cell's count
advances and the previous map is carried forward; fill from orbit gaps
is handled the same way. The series is produced per water year from
1 October to 30 September: on the first day the CGF map is a copy of
MOD10A1 with persistence 1 under cloud, and the global attributes
`First_Day_of_series`, `Time_Series_Day` and
`Missing_days_MODIS_10A1_tile_count` say where in the series a file
sits. Typically five to seven days pass before the map is nearly cloud
free, depending on season and location. The same day's own
observation travels in the file as `MOD10A1_NDSI_Snow_Cover`, and the
QA fields of a filled cell are the QA of the older observation. The
VIIRS and Aqua lines have the same companion (VNP10A1F, MYD10A1F), and
Hall and others 2019 introduce the cloud-persistence statistics as the
quality data that give "the age of the observation in each
pixel".[^mod10a1f-guide][^c61-guide][^hall-2010][^hall-2019][^cmr]

**Wrong-result mode.** Three readings go wrong in the same direction.
A daily snow extent from MOD10A1 that treats 250 as not snow collapses
during every storm and recovers when the sky clears, so the series
shows snow arriving on the first clear day and losing extent whenever
cloud comes; a series that drops the cloudy cells and normalises on
the visible ones reports the fraction of what was seen as the fraction
of the basin. A CGF map read as that day's observation dates a change
to the wrong day: snow that fell and melted under a week of cloud "may
not be mapped" at all, and melt-out under cloud is recorded on the day
the cloud lifted, so a snow-off date from the CGF series is late by
the persistence count wherever the count is high. And cloud and snow
confusion in the underlying product passes through the CGF as cloud
that persists for more days than cloud plausibly would, so the oldest
filled cells can be snow the cloud mask misread rather than
cloud.[^mod10a1f-page][^mod10a1f-guide][^c61-guide]

**Correct approach.** The daily observed product carries the cloud
share as a reported quantity beside the extent, not as a zero and not
as a denominator. The gap-filled product is read with its age: each
value comes with its `Cloud_Persistence`, and the analysis declares an
age it accepts, which the product does not set for the user; the
guide's five to seven days is how long a nearly cloud-free map takes
to build, not a validity limit. A date of change taken from the CGF
series is a date bounded by the persistence count on that day, and the
day's own `MOD10A1_NDSI_Snow_Cover` in the same file shows whether the
change was observed or inherited. The water-year restart is a seam:
the first days of October carry cloud again until the series has
rebuilt, and a series across 1 October shows it. Missing input tiles,
counted in the file's attribute, advance the age of every cell at
once.[^mod10a1f-guide][^c61-guide][^hall-2019]

**Verification.** For one tile and day, the count of cells whose
`Cloud_Persistence` is 0 equals the count of cells that are not 250 in
the same file's `MOD10A1_NDSI_Snow_Cover`, apart from the codes that
are neither, and the cells with persistence above 0 are 250 there
while `CGF_NDSI_Snow_Cover` holds a snow or land value for them. A file
dated 1 October reads `First_Day_of_series` as Y with persistence 1
under its cloud; a file after a missing tile shows the tile count in
its attribute and an age incremented across the whole
tile.[^mod10a1f-guide][^c61-guide]

[^mod10a1f-guide]: the MOD10A1F version 61 user guide, last updated December 2021
[^mod10a1f-page]: the NSIDC product page for MOD10A1F version 61, read 2026-09-14
[^mod10a1-page]: the NSIDC product page for MOD10A1 version 61, read 2026-09-14
[^c61-guide]: the MODIS Snow Products Collection 6.1 User Guide, 2019
[^hall-2019]: Hall and others 2019, Hydrology and Earth System Sciences, Crossref record and abstract
[^hall-2010]: Hall and others 2010, Remote Sensing of Environment, Crossref record
[^cmr]: the CMR collection records for the gap-filled lines, searched 2026-09-14
