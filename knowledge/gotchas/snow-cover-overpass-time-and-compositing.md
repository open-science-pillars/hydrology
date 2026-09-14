---
type: dataset-gotcha
spheres: [hydrosphere, cryosphere]
title: "A daily snow cover tile is one overpass per cell at the platform's local solar time, chosen by nearest solar noon, nearest nadir and most coverage, not a daily mean or a daily maximum"
description: "Each cell of MOD10A1 and VNP10A1 holds one swath observation of the day, selected from the one to several overpasses by three stated criteria: nearest local solar noon, nearest the orbit nadir track, most coverage in the cell. The time is the overpass: Terra descends across the equator at about 10:30 local time and has been drifting earlier since its last inclination manoeuvre in February 2020, Suomi NPP ascends at about 1:30 in the afternoon, JPSS-1 fifty minutes behind it and JPSS-2 twenty minutes ahead. Snow that comes and goes between overpasses is not in the record, adjacent swaths weave along their edges where cloud changed between them, and a Terra series compared with a VIIRS or Aqua series compares mornings with afternoons."
tags: [modis, viirs, snow-cover, overpass, local-solar-time, compositing, terra, suomi-npp, orbit-drift, granule-pointer, nsidc, cryosphere, hydrology]
generated: { by: knowledge-seeder/claude, at: 2026-09-14T05:30:00Z }
severity: medium
dataset: ../datasets/modis-viirs-snow-cover.md
status: draft
stale_after: 2027-03-14
sources:
  - id: mod10a1-guide
    resource: https://nsidc.org/sites/default/files/mod10a1-v061-userguide_1.pdf
    title: "MOD10A1 version 61 user guide, NSIDC, last updated December 2021, read 2026-09-14: the 10:30 descending node, the selection criteria, the orbit_pnt and granule_pnt pointers, the Terra orbit note (last inclination manoeuvre February 2020, 10:15 expected October 2022, 9:00 around December 2025, lower solar elevation and more shadow), the swath selection weave and the geolocation wobble"
  - id: vnp10a1-guide
    resource: https://nsidc.org/sites/default/files/documents/user-guide/multi_vnp10a1-v002-userguide.pdf
    title: "VNP10A1 version 2 user guide, NSIDC, last updated January 2026, read 2026-09-14: the 1:30 in the afternoon ascending node, JPSS-1 lagging by 50 minutes and JPSS-2 preceding by 20 minutes, the three selection criteria, the granule_pnt field and the swath selection weave"
  - id: c61-guide
    resource: https://nsidc.org/sites/default/files/c61_modis_snow_user_guide.pdf
    title: "MODIS Snow Products Collection 6.1 User Guide, Riggs, Hall and Roman, 2019, read 2026-09-14: the M*D10GA observation selection ('nearest local solar noon time, nearest the orbit nadir track and with most coverage in a grid cell') and the note that only a single observation of the one to several acquired in a day is stored"
  - id: viirs-c2-guide
    resource: https://nsidc.org/sites/default/files/documents/technical-reference/snpp_jpss1_viirs_snow_cover_products_collection_2_user_guide.pdf
    title: "SNPP/JPSS1 VIIRS Snow Cover Products Collection 2 User Guide, Riggs and Hall, 2021, read 2026-09-14: the L2G stacking, the selection on solar zenith, distance from nadir and coverage, and the weave along stitched swath edges"
  - id: riggs-hall-2020
    resource: https://doi.org/10.3390/rs12223781
    title: "Riggs and Hall, 2020, Continuity of MODIS and VIIRS Snow Cover Extent Data Products for Development of an Earth Science Data Record, Remote Sensing 12(22), 3781; the Crossref abstract read 2026-09-14: 90 to 97 per cent agreement, and differences of 2 to 15 per cent attributable to viewing geometry, pixel spread across a scan and time of observation"
  - id: mod10a1-page
    resource: https://nsidc.org/data/mod10a1/versions/61
    title: "The NSIDC product page for MOD10A1 version 61, read 2026-09-14: the limitation that areas of ephemeral and very thin snow cover may not be mapped"
---

# Overpass time and the daily composite

**Mechanism.** The Level-2 swaths of a day are gridded into an
intermediate product with every observation of a cell stacked, and a
selection algorithm keeps one: the observation "nearest local solar
noon time, nearest the orbit nadir track and with most coverage in a
grid cell", judged from the solar zenith angle, the distance from
nadir and the cell coverage, which the guides call the best sensor
view of the surface for snow detection. The daily tile is that one
observation per cell, and the `granule_pnt` (and on MODIS
`orbit_pnt`) field points into the file's granule arrays, from which
the swath and its beginning time can be
recovered.[^c61-guide][^viirs-c2-guide][^mod10a1-guide][^vnp10a1-guide]
The time of that observation is the platform's overpass. Terra's
sun-synchronous orbit crosses the equator southbound at about 10:30
local time; its last inclination manoeuvre was in February 2020, the
crossing was expected to reach 10:15 in October 2022 and about 9:00
around December 2025, and the guide notes that an earlier crossing
means lower solar elevation and more shadow. Suomi NPP crosses
northbound at about 1:30 in the afternoon, JPSS-1 on the same orbit
fifty minutes behind and JPSS-2 twenty minutes ahead. Near the poles
a cell is seen by several overpasses and the selection chooses among
them; at mid latitudes it is usually the one. Where cloud moved
between two overlapping swaths, the chosen observations alternate
along the swath edge and the map shows a weave or stitch pattern with
interwoven cloud and clear cells; the day-to-day gridding also shifts
a lake outline by one or more cells, so multi-day stacks blur
it.[^mod10a1-guide][^vnp10a1-guide][^viirs-c2-guide] Comparing MODIS
with VIIRS, Riggs and Hall 2020 find 90 to 97 per cent agreement in
extent and attribute the 2 to 15 per cent differences to viewing
geometry, pixel spread across the scan and the time of
observation.[^riggs-hall-2020]

**Wrong-result mode.** The date in the file name is read as a day and
the value as the day's state: a morning Terra map compared with an
afternoon station observation, a VIIRS map, a model's daily mean, or a
midday melt, as if simultaneous. Ephemeral snow that fell after the
overpass and was gone by the next is absent from the record, and its
absence is read as no snow. A difference between a Terra series and a
Suomi NPP series over the same basin is attributed to the sensor when
part of it is three hours of local time and the scan position. A
weave along a swath boundary is read as a snow line. And a multi-year
Terra series crosses the orbit drift, over which the illumination at
the observation changes and the low-illumination flag fires more, a
change in the observing conditions that a trend would carry as
snow.[^mod10a1-guide][^mod10a1-page][^riggs-hall-2020]

**Correct approach.** A snow cover series names its platform and
therefore its local solar time, and a receipt for a daily value
states the selection rule the product used. Where the hour matters,
`granule_pnt` and the granule beginning-time array give the actual
acquisition of each cell. A comparison across platforms is a
comparison across observation times and scan geometries, and is
stated that way, with the agreement figures of the continuity work as
the expectation rather than identity; Riggs and Hall 2020 found the
tile-to-tile differences shrink at a common 1 km grid. A series
spanning the Terra drift years states the drift, and a snow-line
position along a swath edge is checked against the weave pattern
before it is read as
terrain.[^mod10a1-guide][^vnp10a1-guide][^riggs-hall-2020][^c61-guide]

**Verification.** For one tile, decoding `granule_pnt` through the
granule pointer and beginning-time arrays gives one or two acquisition
times for the whole tile at mid latitudes and more near the poles, all
within the platform's local morning (Terra) or early afternoon (Suomi
NPP). Along an overlap between two swaths the pointer values
alternate across the weave. The same day's MOD10A1 and VNP10A1 over
the same basin differ in extent by an amount of the order the
continuity paper reports.[^mod10a1-guide][^vnp10a1-guide][^riggs-hall-2020]

[^mod10a1-guide]: the MOD10A1 version 61 user guide, last updated December 2021
[^vnp10a1-guide]: the VNP10A1 version 2 user guide, last updated January 2026
[^c61-guide]: the MODIS Snow Products Collection 6.1 User Guide, 2019
[^viirs-c2-guide]: the VIIRS Snow Cover Products Collection 2 User Guide, 2021
[^riggs-hall-2020]: Riggs and Hall 2020, Remote Sensing, Crossref record and abstract
[^mod10a1-page]: the NSIDC product page for MOD10A1 version 61, read 2026-09-14
