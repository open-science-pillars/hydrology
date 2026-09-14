---
type: dataset
spheres: [hydrosphere, cryosphere]
title: "MODIS and VIIRS daily snow cover (MOD10A1 v61, MOD10A1F v61, VNP10A1 v2): an NDSI index per cell, flag codes above 100, one overpass per day"
description: "Daily snow cover from Terra MODIS at 500 m (MOD10A1 version 61, with the cloud-gap-filled MOD10A1F beside it) and from Suomi NPP VIIRS at 375 m (VNP10A1 version 2), on the sinusoidal tile grid at NSIDC DAAC. The value in NDSI_Snow_Cover is the Normalized Difference Snow Index scaled to 0 to 100, an index of snow presence and not a fraction of the cell; everything above 100 is a code (200 missing, 201 no decision, 211 night, 237 inland water, 239 ocean, 250 cloud, 255 fill). Each cell holds one swath observation chosen by stated rules, cloud is the largest gap, and the gap-filled product carries the age of the observation it reuses."
tags: [modis, viirs, snow-cover, ndsi, mod10a1, mod10a1f, vnp10a1, cloud-gap-filled, nsidc, terra, suomi-npp, sinusoidal, cryosphere, hydrology]
generated: { by: knowledge-seeder/claude, at: 2026-09-14T05:30:00Z }
resource: https://nsidc.org/data/mod10a1/versions/61
version: "MOD10A1 version 61 (C2565093311-NSIDC_CPRD), MOD10A1F version 61 (C3028765772-NSIDC_CPRD) and VNP10A1 version 2 (C3173441659-NSIDC_CPRD), CMR-verified 2026-09-14: the MODIS records begin 2000-02-24 and the VIIRS record 2012-01-19, all flagged as ending at present; the latest granules on the read date were 2026-09-12 for the two MODIS products and 2026-09-08 for VNP10A1"
status: draft
stale_after: 2027-03-14
citation:
  access_date_required: true
  authority: https://nsidc.org/data/mod10a1/versions/61
  data: "Hall, D. K. and Riggs, G. A. (2021). MODIS/Terra Snow Cover Daily L3 Global 500m SIN Grid, Version 61. Boulder, Colorado USA. NASA National Snow and Ice Data Center Distributed Active Archive Center, accessed {access_date}, https://doi.org/10.5067/MODIS/MOD10A1.061"
  doi: "10.5067/MODIS/MOD10A1.061 (MOD10A1), 10.5067/MODIS/MOD10A1F.061 (MOD10A1F), 10.5067/45VDCKJBXWEE (VNP10A1)"
  note: "each product page carries its own citation with the subset used and the access date; the three DOIs resolve through doi.org to the NSIDC product pages and are not in Crossref"
sources:
  - id: mod10a1-page
    resource: https://nsidc.org/data/mod10a1/versions/61
    title: "The NSIDC product page for MOD10A1 version 61, read 2026-09-14: the citation, the version summary, the overview, coverage and format, the strengths and limitations, the access routes, and the operations banner on data loss from 7 July 2023"
  - id: mod10a1f-page
    resource: https://nsidc.org/data/mod10a1f/versions/61
    title: "The NSIDC product page for MOD10A1F version 61, read 2026-09-14: the citation, the overview, and the strengths and limitations of the cloud-gap-filled product"
  - id: vnp10a1-page
    resource: https://nsidc.org/data/vnp10a1/versions/2
    title: "The NSIDC product page for VNP10A1 version 2, read 2026-09-14: the citation, the overview, coverage and format, and the banner on the July 2026 Suomi NPP anomaly"
  - id: mod10a1-guide
    resource: https://nsidc.org/sites/default/files/mod10a1-v061-userguide_1.pdf
    title: "MOD10A1 version 61 user guide, NSIDC, published March 2021 and last updated December 2021, read 2026-09-14: Table 1 (the fields and their values), the algorithm flag bits, the grid, the selection criteria, the basic QA rules, the reported accuracy range and the Terra orbit note"
  - id: mod10a1f-guide
    resource: https://nsidc.org/sites/default/files/mod10a1f-v061-userguide_0.pdf
    title: "MOD10A1F version 61 user guide, NSIDC, published 25 October 2019 and last updated 10 December 2021, read 2026-09-14: the fields, the Cloud_Persistence semantics, the water-year series, the handling of missing tiles and fill"
  - id: vnp10a1-guide
    resource: https://nsidc.org/sites/default/files/documents/user-guide/multi_vnp10a1-v002-userguide.pdf
    title: "VNP10A1, VJ110A1 and VJ210A1 version 2 user guide, NSIDC, published June 2023 and last updated January 2026, read 2026-09-14: the fields and codes, the packed NDSI, the bit flags, the grid, the orbit times, the selection criteria, the accuracy statement and the version history"
  - id: c61-guide
    resource: https://nsidc.org/sites/default/files/c61_modis_snow_user_guide.pdf
    title: "MODIS Snow Products Collection 6.1 User Guide, Riggs, Hall and Roman, 2019, read 2026-09-14: the algorithm logic, the FSC statement, the cloud mask reading, the cloud and snow confusion section, the observation selection, the CMG binning and the CGF algorithm"
  - id: viirs-c2-guide
    resource: https://nsidc.org/sites/default/files/documents/technical-reference/snpp_jpss1_viirs_snow_cover_products_collection_2_user_guide.pdf
    title: "SNPP/JPSS1 VIIRS Snow Cover Products Collection 2 User Guide, Riggs and Hall, 2021, read 2026-09-14: the NDSI formula on bands I1 and I3, the scaling into NDSI_Snow_Cover, the cloud mask reading at 750 m, the cloud and snow confusion section and the selection algorithm"
  - id: cmr
    resource: https://cmr.earthdata.nasa.gov/search/collections.json?short_name[]=MOD10A1&short_name[]=MOD10A1F&short_name[]=VNP10A1&short_name[]=MYD10A1&short_name[]=VNP10A1F&short_name[]=MOD10A2&short_name[]=MYD10A1F&short_name[]=VJ110A1
    title: "The CMR collection records for the snow cover family at NSIDC_CPRD (concept ids, versions, DOIs, temporal extents, resolutions, platforms), and the newest granule of each daily collection by start date, searched 2026-09-14"
  - id: faq-ndsi
    resource: https://nsidc.org/data/user-resources/help-center/what-ndsi-snow-cover-and-how-does-it-compare-fsc
    title: "The NSIDC help article 'What is NDSI snow cover and how does it compare to FSC?', read 2026-09-14"
  - id: faq-viirs
    resource: https://nsidc.org/data/user-resources/help-center/how-does-viirs-snow-and-sea-ice-data-compare-modis
    title: "The NSIDC help article 'How does VIIRS snow and sea ice data compare to MODIS', last updated September 2023, read 2026-09-14"
  - id: faq-merge
    resource: https://nsidc.org/data/user-resources/help-center/can-i-merge-different-modis-collections
    title: "The NSIDC help article 'Can I merge different MODIS collections?', read 2026-09-14"
  - id: hall-riggs-2007
    resource: https://doi.org/10.1002/hyp.6715
    title: "Hall and Riggs, 2007, Accuracy assessment of the MODIS snow products, Hydrological Processes 21(12), 1534 to 1547; the Crossref record and abstract read 2026-09-14"
  - id: riggs-hall-2020
    resource: https://doi.org/10.3390/rs12223781
    title: "Riggs and Hall, 2020, Continuity of MODIS and VIIRS Snow Cover Extent Data Products for Development of an Earth Science Data Record, Remote Sensing 12(22), 3781; the Crossref record and abstract read 2026-09-14"
  - id: hall-2019
    resource: https://doi.org/10.5194/hess-23-5227-2019
    title: "Hall, Riggs, DiGirolamo and Roman, 2019, Evaluation of MODIS and VIIRS cloud-gap-filled snow-cover products for production of an Earth science data record, Hydrology and Earth System Sciences 23(12), 5227 to 5241; the Crossref record and abstract read 2026-09-14"
  - id: riggs-2017
    resource: https://doi.org/10.5194/essd-9-765-2017
    title: "Riggs, Hall and Roman, 2017, Overview of NASA's MODIS and VIIRS snow-cover Earth System Data Records, Earth System Science Data 9(2), 765 to 777; the Crossref record and abstract read 2026-09-14"
  - id: hall-1995
    resource: https://doi.org/10.1016/0034-4257(95)00137-P
    title: "Hall, Riggs and Salomonson, 1995, Development of methods for mapping global snow cover using moderate resolution imaging spectroradiometer data, Remote Sensing of Environment 54(2), 127 to 140; the Crossref record read 2026-09-14 (no abstract in the record; the journal page sits behind a bot check)"
  - id: hall-2002
    resource: https://doi.org/10.1016/S0034-4257(02)00095-0
    title: "Hall, Riggs, Salomonson, DiGirolamo and Bayr, 2002, MODIS snow-cover products, Remote Sensing of Environment 83(1 to 2), 181 to 194; the Crossref record read 2026-09-14 (no abstract in the record; the journal page sits behind a bot check)"
---

# MODIS and VIIRS daily snow cover

**Identity.** Three daily Level-3 snow cover products at NSIDC DAAC,
all on the MODIS sinusoidal tile grid of 10 by 10 degree tiles, all
produced by the same NDSI snow detection algorithm adjusted for the
sensor: MOD10A1 version 61 from Terra MODIS at 500 m (2400 by 2400
cells per tile, HDF-EOS2, 8-bit unsigned integers, from 2000-02-24),
its cloud-gap-filled companion MOD10A1F version 61 on the same grid
and span, and VNP10A1 version 2 from Suomi NPP VIIRS at 375 m (3000
by 3000 cells per tile, HDF-EOS5, from 2012-01-19). The Aqua line
(MYD10A1 and MYD10A1F, from 2002-07-04), the VIIRS gap-filled and
JPSS lines (VNP10A1F, VJ110A1 from 2018-01-05, VJ210A1) and the 8-day
MOD10A2 are separate collections in the same
family.[^cmr][^mod10a1-page][^vnp10a1-page][^vnp10a1-guide] On
2026-09-14 the newest granules were dated 2026-09-12 for MOD10A1 and
MOD10A1F and 2026-09-08 for VNP10A1; the VNP10A1 page carries a
banner that Suomi NPP science products were disabled at 01:30 UTC on
2026-07-11 after a spacecraft anomaly, that the spacecraft was nominal
again as of 2026-07-21, and that recoverable missing products would be
published after review. The MODIS pages carry a banner that version
6.1 products from 7 July 2023 onward may be subject to more frequent
non-recoverable data loss under the flight operations team's
lights-out operations.[^cmr][^vnp10a1-page][^mod10a1-page] The
MOD10A1 guide, last updated December 2021, expected the Terra mission
to end in December 2025; the archive carries daily granules past that
date.[^mod10a1-guide][^cmr]

**The value is an index.** Snow has high visible and low shortwave
infrared reflectance, and the Normalized Difference Snow Index is the
normalised difference of the two: MODIS band 4 against band 6, VIIRS
band I1 (0.64 micrometres) against I3 (1.61 micrometres). A pixel with
NDSI above 0.0 after the screens is "considered to have some snow
present"; a pixel at or below 0.0 is snow-free land. The
`NDSI_Snow_Cover` field holds that NDSI scaled to 0 to 100 for the
cells where snow was detected, and codes above 100 for everything
else. Fractional snow cover is not calculated in Collection 6.1: the
NDSI snow cover replaced the fractional cover of Collection 5, which
had been an empirical regression of Landsat-derived fractions on
NDSI.[^mod10a1-guide][^vnp10a1-guide][^c61-guide][^viirs-c2-guide][^faq-ndsi]
The gotcha [snow-cover-ndsi-is-not-fraction](../gotchas/snow-cover-ndsi-is-not-fraction.md)
carries the consequences.

## Fields and codes

MOD10A1 version 61, from its user guide's Table 1:[^mod10a1-guide]

| Field | Content |
|---|---|
| `NDSI_Snow_Cover` | 0 to 100 NDSI snow cover; 200 missing data; 201 no decision; 211 night; 237 inland water; 239 ocean; 250 cloud; 254 detector saturated; 255 fill |
| `NDSI_Snow_Cover_Basic_QA` | 0 best; 1 good; 2 ok; 3 poor (not used); 4 other (not used); 211 night; 239 ocean; 255 unusable input or no data |
| `NDSI_Snow_Cover_Algorithm_Flags_QA` | bit 0 inland water; bit 1 low visible screen, snow reversed to no snow; bit 2 low NDSI screen, snow reversed; bit 3 temperature and height screen; bit 4 high SWIR screen; bit 5 probably cloudy; bit 6 probably clear; bit 7 low illumination |
| `NDSI` | the raw index before screening, scaled by 10000, valid -10000 to 10000, fill -32768 |
| `Snow_Albedo_Daily_Tile` | 0 to 100 snow albedo; 101 no decision; 111 night; 125 land; 137 inland water; 139 ocean; 150 cloud; 151 cloud detected as snow; 250 missing; 251 self shadowing; 252 landmask mismatch; 253 BRDF failure; 254 non-production mask |
| `orbit_pnt`, `granule_pnt` | pointers into the file's orbit and granule arrays naming the swath each cell came from |

MOD10A1F version 61 carries `CGF_NDSI_Snow_Cover` with the same codes
as MOD10A1, `Cloud_Persistence` (0 to 254 days, 255 fill), the same
day's own `MOD10A1_NDSI_Snow_Cover` for comparison, and `Basic_QA` and
`Algorithm_Flags_QA` copied from the observation in use, which for a
filled cell is a previous day's.[^mod10a1f-guide]

VNP10A1 version 2 carries `NDSI_Snow_Cover` (0 to 100; 201 no
decision; 211 night; 237 lake or inland water; 239 ocean; 250 cloud;
251 missing L1B data; 252 L1B data failed calibration; 253 onboard
bowtie trim; 254 L1B fill; 255 L2 fill), `NDSI` packed with a
`scale_factor` of 0.001 (valid -1000 to 1000, with 21000 night, 29000
ocean, 24000 missing L1B, 25000 failed calibration, 31000 bowtie trim,
30000 L1B fill, 32767 fill), `Algorithm_bit_flags_QA`, `Basic_QA` (0
best, 1 good, 2 poor, 3 other; 211 night, 239 ocean, 250 cloud, 251 to
255 input and fill codes) and `granule_pnt`. The bit layout differs
from MODIS: on VIIRS the high SWIR screen is bit 5 and bits 4 and 6
are spare, while on MODIS the SWIR screen is bit 4 and bits 5 and 6
carry the cloud mask confidence. Code that decodes one product's
flags on the other reads the wrong screen.[^vnp10a1-guide][^mod10a1-guide]

## One observation per cell

Each daily tile holds one swath observation per cell, selected from
the one to several overpasses of the day by three criteria: nearest
local solar noon, nearest the orbit nadir track, and most coverage in
the cell. Terra crosses the equator southbound at about 10:30 local
time, with the crossing drifting earlier since the last inclination
manoeuvre in February 2020; Suomi NPP crosses northbound at about 1:30
in the afternoon, JPSS-1 fifty minutes later and JPSS-2 twenty minutes
earlier. The selection leaves a weave pattern along swath edges where
cloud changed between overpasses, and a geolocation wobble of one or
more cells from day to day blurs lake outlines in multi-day
composites.[^mod10a1-guide][^vnp10a1-guide][^c61-guide][^viirs-c2-guide]
The gotcha [snow-cover-overpass-time-and-compositing](../gotchas/snow-cover-overpass-time-and-compositing.md)
carries the consequences.

## Cloud, and the gap-filled product

Cloud is the product's largest limitation; a cell under "confident
cloudy" in the cloud mask is 250, and the three lower cloud
confidences are read as clear, with "probably cloudy" and "probably
clear" recorded in bits 5 and 6 so that cloud and snow confusion can
be examined. MOD10A1F replaces each cloudy cell with the most recent
clear view and counts the days since it in `Cloud_Persistence`; a
nearly cloud-free map typically takes five to seven days to build,
depending on season and place, and snow that fell and melted under
cloud is never
mapped.[^mod10a1-page][^mod10a1f-page][^mod10a1f-guide][^c61-guide]
The gotchas [snow-cover-cloud-persistence-and-gap-filling](../gotchas/snow-cover-cloud-persistence-and-gap-filling.md)
and [snow-cover-snow-cloud-confusion](../gotchas/snow-cover-snow-cloud-confusion.md)
carry the consequences.

## Access

A free Earthdata Login is required. The products are served over
HTTPS, through earthaccess, from the Earthdata Cloud in AWS us-west-2
with S3 credentials, and MOD10A1 and VNP10A1 also through AppEEARS
subsetting.[^mod10a1-page][^vnp10a1-page] Collections 6 and 6.1 of the
snow products may be used together, with minor calibration
differences; Collections 4 and 5 are archived and not recommended
beside newer collections.[^faq-merge] VIIRS products are built to be
similar to MODIS for continuity of the record, at 375 m rather than
500 m, and the two algorithms produce daily maps with 90 to 97 per
cent agreement in snow cover extent across landscapes, with 2 to 15
per cent differences attributed to viewing geometry, pixel spread and
time of observation.[^faq-viirs][^riggs-hall-2020]

## Uncertainty

- There is no per-cell uncertainty field. `Basic_QA` is a categorical
  gate set from the input radiance range and the solar zenith angle
  (ok for a solar zenith between 70 and 85 degrees), and the algorithm
  bit flags record which screens reversed or flagged a detection.
  Every quantitative statement of accuracy is a published range, not a
  field.[^mod10a1-guide][^vnp10a1-guide]
- The user guides state an accuracy range of 88 to 93 per cent reported
  by investigators under cloud-free conditions; Hall and Riggs 2007
  put the overall absolute accuracy of the 500 m swath and daily tile
  products at about 93 per cent, varying by land cover and snow
  condition, with the most frequent errors from snow and cloud
  discrimination and with very thin snow (under 1 cm) problematic.
  The VIIRS guide reports the Suomi NPP snow cover as 98 per cent
  consistent with MODIS.[^mod10a1-guide][^vnp10a1-guide][^hall-riggs-2007]
- Cloud cover is the largest source of missing snow, polar darkness
  removes the winter at high latitudes (night is a solar zenith of 85
  degrees or more), and ephemeral or very thin snow may not be
  mapped.[^mod10a1-page][^mod10a1-guide]
- The gap-filled product's uncertainty is the age of the reused
  observation: `Cloud_Persistence` is the instrument, and Hall and
  others 2019 introduce the cloud-persistence statistics as the
  quality data of the CGF products.[^mod10a1f-guide][^hall-2019]
- Snow albedo is estimated to be within 10 per cent of surface
  measurements under level, fully snow-covered conditions, with much
  larger errors in steep terrain, and the product reports no
  albedo-specific QA.[^mod10a1-guide]
- The Collection 6 revisions that put the NDSI itself and the
  algorithm flags into the product, and the methods lineage from the
  1995 and 2002 algorithm papers, are in the overview
  papers.[^riggs-2017][^hall-1995][^hall-2002]

## Known issues

- [snow-cover-ndsi-is-not-fraction](../gotchas/snow-cover-ndsi-is-not-fraction.md)
- [snow-cover-cloud-persistence-and-gap-filling](../gotchas/snow-cover-cloud-persistence-and-gap-filling.md)
- [snow-cover-snow-cloud-confusion](../gotchas/snow-cover-snow-cloud-confusion.md)
- [snow-cover-overpass-time-and-compositing](../gotchas/snow-cover-overpass-time-and-compositing.md)
- [snow-cover-is-not-swe](../gotchas/snow-cover-is-not-swe.md)

[^mod10a1-page]: the NSIDC product page for MOD10A1 version 61, read 2026-09-14
[^mod10a1f-page]: the NSIDC product page for MOD10A1F version 61, read 2026-09-14
[^vnp10a1-page]: the NSIDC product page for VNP10A1 version 2, read 2026-09-14
[^mod10a1-guide]: the MOD10A1 version 61 user guide, last updated December 2021
[^mod10a1f-guide]: the MOD10A1F version 61 user guide, last updated December 2021
[^vnp10a1-guide]: the VNP10A1, VJ110A1 and VJ210A1 version 2 user guide, last updated January 2026
[^c61-guide]: the MODIS Snow Products Collection 6.1 User Guide, 2019
[^viirs-c2-guide]: the SNPP/JPSS1 VIIRS Snow Cover Products Collection 2 User Guide, 2021
[^cmr]: the CMR collection and granule records, searched 2026-09-14
[^faq-ndsi]: the NSIDC help article on NDSI snow cover and FSC
[^faq-viirs]: the NSIDC help article on VIIRS against MODIS snow and sea ice data
[^faq-merge]: the NSIDC help article on merging MODIS collections
[^hall-riggs-2007]: Hall and Riggs 2007, Hydrological Processes, Crossref record and abstract
[^riggs-hall-2020]: Riggs and Hall 2020, Remote Sensing, Crossref record and abstract
[^hall-2019]: Hall and others 2019, Hydrology and Earth System Sciences, Crossref record and abstract
[^riggs-2017]: Riggs, Hall and Roman 2017, Earth System Science Data, Crossref record and abstract
[^hall-1995]: Hall, Riggs and Salomonson 1995, Remote Sensing of Environment, Crossref record
[^hall-2002]: Hall and others 2002, Remote Sensing of Environment, Crossref record
