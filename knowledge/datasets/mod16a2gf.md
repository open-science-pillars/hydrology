---
type: dataset
spheres: [hydrosphere]
title: "MOD16A2GF v061 evapotranspiration: an 8-day total in millimetres, seven fill codes for the land it does not compute, and a record that only advances at year end"
description: "Terra MODIS evapotranspiration at 500 m on the sinusoidal grid, 8-day composites, from LP DAAC. ET_500m is an int16 total in kg per m2 (numerically mm) with scale factor 0.1 and a valid range of -32767 to 32700; everything above that range is one of seven fill codes naming the land cover where evapotranspiration was not computed, of which the file header advertises only one. The last composite of each year is 5 or 6 days, not 8. The gap-filled product is produced only at year end, so the current year exists only in the non-gap-filled MOD16A2 companion."
tags: [mod16, modis, evapotranspiration, et, lpdaac, terra, sinusoidal, hydrology, water-balance]
generated: { by: claude-code/fable-5, at: 2026-09-06T23:50:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-07T02:11:54Z }
resource: https://www.earthdata.nasa.gov/data/catalog/lpcloud-mod16a2gf-061
version: "061 (granule label 061); MOD16A2GF daily-composite record 2000-01-01 through the last composite of the most recently completed year (A2025361, 2025-12-27 to 2025-12-31, on 2026-09-06); MOD16A2 061 from 2021-01-01 to within about three weeks of the present"
status: stable
upstream: pending
stale_after: 2027-03-06
citation:
  access_date_required: true
  authority: https://lpdaac.usgs.gov/
  data: "Running, S., Mu, Q., Zhao, M., Moreno, A. (2021). MODIS/Terra Net Evapotranspiration Gap-Filled 8-Day L4 Global 500m SIN Grid V061 [Data set]. NASA EOSDIS Land Processes Distributed Active Archive Center, accessed {access_date}, 10.5067/MODIS/MOD16A2GF.061"
  doi: "10.5067/MODIS/MOD16A2GF.061 (gap-filled 8-day), 10.5067/MODIS/MOD16A2.061 (the near-real-time companion)"
  note: "the DOI landing page carries the authoritative citation; the access date matters because the gap-filled record's end moves once a year"
sources:
  - id: guide
    resource: https://lpdaac.usgs.gov/documents/931/MOD16_User_Guide_V61.pdf
    title: "MOD16 User's Guide, MODIS Land Team, version 1.0 of 2021-02-26: Table 6.1 (units, data types, valid ranges, scale factors), the seven fill values, the ET_QC_500m bit fields, the year-end composite length and the gap-filling method"
  - id: catalog
    resource: https://www.earthdata.nasa.gov/data/catalog/lpcloud-mod16a2gf-061
    title: "The LP DAAC catalog entry for MOD16A2GF v061 (layers, resolution, projection, temporal granularity), read 2026-09-06"
  - id: cmr
    resource: https://cmr.earthdata.nasa.gov/search/collections.umm_json?short_name=MOD16A2GF&version=061
    title: "CMR collection records for MOD16A2GF (C2565791021-LPCLOUD) and MOD16A2 (C2343113232-LPCLOUD), and the granule inventories that give each record's last composite, searched 2026-09-06"
  - id: granule
    resource: https://opendap.earthdata.nasa.gov/collections/C2565791021-LPCLOUD/granules/
    title: "Granule metadata read over Cloud OPeNDAP on 2026-09-06: the ET_500m attributes (units, scale factor, the single _FillValue), the grid dimensions and the temporal extents that give each composite its length"
  - id: record
    resource: https://github.com/open-science-pillars/marketplace/issues/69
    title: "The evapotranspiration record: the tile pulls with their sizes, the window route, the basin means measured over the fixtures and the comparison against the OpenET ensemble"
---

# MOD16A2GF v061 evapotranspiration

**Identity.** Terra MODIS evapotranspiration from the MOD16
algorithm, 500 m on the MODIS sinusoidal grid, as 8-day composites:
collection `MOD16A2GF` version 061 at LP DAAC (concept id
C2565791021-LPCLOUD, DOI 10.5067/MODIS/MOD16A2GF.061), cloud-hosted.
Each granule is one sinusoidal tile of 2400 by 2400 cells and carries
`ET_500m`, `LE_500m`, `PET_500m`, `PLE_500m` and `ET_QC_500m`. The
non-gap-filled companion `MOD16A2` version 061 (C2343113232-LPCLOUD,
DOI 10.5067/MODIS/MOD16A2.061) covers the same grid from 2021 to
within weeks of the present.[^cmr][^catalog]

## Variable, units and the scale factor

`ET_500m` is int16 in `kg/m^2/8day`, which is millimetres of water
over the composite period, with a scale factor of 0.1 and a valid
range of -32767 to 32700: a real value is the stored integer times
0.1.[^guide][^granule] `PET_500m` is the same in potential terms;
`LE_500m` and `PLE_500m` are latent heat in J per m2 per day with a
scale factor of 10000. Reading `ET_500m` without applying the scale
factor overstates evapotranspiration tenfold; reading it as a rate
per day rather than a total per period understates it eightfold.

## The seven fill codes, and why the header does not list them

The file attributes carry one `_FillValue`, 32767. The product uses
seven codes, and the user guide states them: "Though data attributes
list just one _FillValue: 32767 in the head file ... there are, in
fact, 7 fill values listed below for non-vegetated pixels, which we
didn't calculate ET".[^guide]

| Code | Meaning |
|---|---|
| 32767 | fill |
| 32766 | perennial salt or water bodies |
| 32765 | barren, sparse vegetation (rock, tundra, desert) |
| 32764 | perennial snow, ice |
| 32763 | permanent wetlands or inundated marshland |
| 32762 | urban or built-up |
| 32761 | unclassified, or not able to determine |

The LP DAAC catalog page adds a third account, listing the fill value
for `ET_500m` as 32761 rather than 32767.[^catalog] The safe reading,
and the one this bundle's loader implements, is that any value above
the valid range of 32700 is not a measurement; which code it is says
what kind of land it is. A basin mean that reads any of these as zero
evapotranspiration is wrong in the direction of the land cover it
crosses, which is why that failure has its own concept
([the fill gotcha](../gotchas/mod16-fill-over-water-barren-urban.md)).

## Quality

`ET_QC_500m` is uint8 and inherits the MOD15A2 layout: bit 0
MODLAND_QC (good quality, or other quality meaning a back-up
algorithm or fill), bit 1 sensor, bit 2 dead detector, bits 3 to 4
cloud state, bits 5 to 7 SCF_QC as a five-level confidence
score.[^guide] For the gap-filled product the guide says users "may
ignore QC data layer because cloud-contaminated LAI/FPAR gaps have
been temporally filled before calculating ET" and that QC then
denotes only whether filled inputs were used; for the non-gap-filled
MOD16A2 it says to exclude cloud-contaminated cells at least.

## Compositing: 46 periods a year, and the last one is short

There are 46 composites in a year, and the guide is explicit that
"the last 8-day (MOD16A2.A20??361.*.hdf) of each year is not 8-day
but either 5-day or 6-day depending on normal or leap year".[^guide]
The granule metadata says which: `MOD16A2GF.A2025361.h09v05` covers
2025-12-27 through 2025-12-31, five days.[^cmr] A month total that
divides every composite by eight is wrong at every year end, and a
sum of composites into a calendar month is wrong at every month
boundary; the apportioning rule has its own concept
([the compositing gotcha](../gotchas/mod16-composite-to-month.md)).

## The gap-filled record only advances once a year

MOD16A2GF cleans the poor-quality LAI and FPAR inputs before running
the algorithm, and the guide states the consequence: the gap-filled
products "will be generated at the end of each year when the entire
yearly 8-day M*D15A2 are available ... users cannot get
MOD16A2[3]GF in the near real-time manner".[^guide] Measured on
2026-09-06: the last MOD16A2GF composite is `A2025361` (produced
2026-02-05) and the last MOD16A2 composite is `A2026225`, covering
2026-08-13 to 2026-08-20 (produced 2026-08-31).[^cmr] So a series
that runs to the present is two products, gap-filled through the last
complete year and not gap-filled after it, and the QC layer that can
be ignored in the first half cannot be ignored in the second. The
`stale_after` on this concept is the date to re-read the record's
end.

The guide also warns that the first year of each mission (2000 for
Terra, 2002 for Aqua) is gap-filled across a long stretch before the
instrument's first data, so those years are weaker than the
rest.[^guide]

## Access

Cloud-hosted at LP DAAC behind Earthdata Login with the LP DAAC
application authorized. A whole tile is 20 to 33 MB per composite
(measured 2026-09-06 over nine tiles: 209.6 MB in about 32 s through
`earthaccess.download`), so a basin window is pulled instead, through
a Cloud OPeNDAP DAP4 constraint expression naming the rows and
columns of the one tile that holds it (`/MOD_Grid_MOD16A2/Data_Fields/ET_500m[r0:r1][c0:c1]`).
A year of the Roaring Fork window (144 by 352 cells, 46 composites)
moved 4.27 MB in 21 s.[^record] The tiles do not share a row and
column origin, so a window that spans two tiles is fetched tile by
tile and never mosaicked by index.

## Measured over the fixture basins (2026-09-06)

Calendar year 2023, MOD16A2GF, basin means over frozen polygons:

| Basin | ET mm | Volume km3 | Cells inside | Masked |
|---|---|---|---|---|
| Roaring Fork at Glenwood Springs | 494.60 | 1.8391 | 17,531 | 1.2 per cent |
| Capitol Creek (HUC12 140100040402) | 521.12 | 0.0490 | 438 | 0.0 per cent |
| Padre Creek-Lake Powell (HUC12 140700061004) | 168.72 | 0.0084 | 489 | 52.4 per cent |

The volumes are the basin mean over the area the measured cells
cover, not over the whole polygon: on the Roaring Fork that area is
3,718 km2 of 3,767, and on the Lake Powell unit it is 50.0 km2 of
104.6, so applying the land rate to the whole polygon there would
double the volume.[^record]

**Against the OpenET ensemble, where both can see the same ground.**
Over Capitol Creek, the one fixture unit small enough for the OpenET
per-request area cap, calendar year 2023: MOD16A2GF 521.12 mm against
the OpenET ensemble's 724.60 mm, a ratio of 0.72. The two products
disagree by a quarter of the annual total over a 95 km2 mountain unit,
which is the size of disagreement a basin water balance has to carry
as uncertainty rather than resolve by preference. The OpenET months
for January through March 2023 are themselves suspect over this unit
([the monthly-against-daily gotcha](../gotchas/openet-monthly-not-the-daily-sum.md));
excluding them, April through December is 436.06 mm from MOD16 against
639.37 mm from OpenET, a ratio of 0.68, so the disagreement is not an
artifact of those three months but widens without them. Month by month
the ratio runs from 0.47 in September to 2.86 in December: the two
products disagree about the shape of the year as well as its
total.[^record]

## Uncertainty

The algorithm was validated against 46 eddy covariance flux towers and
232 watersheds over 2000 to 2010; the guide reports the comparison and
its terms.[^guide] For a basin water balance the practical terms are
these: the product estimates land evapotranspiration only, over the
cells it did not mask, at 500 m, from 8-day composites of inputs that
were themselves gap-filled; open water, urban and barren surfaces
inside the basin carry no estimate at all; and the disagreement with
an independent ensemble over the same ground is of order a quarter of
the annual total.

## Known issues

- The fill codes are seven, the header says one and the catalog page
  says a third thing. Trust the valid range.
- The last composite of the year is 5 or 6 days.
- The gap-filled record ends at the last complete year; the current
  year is a different product with different quality handling.
- No open-water evaporation anywhere, so a basin holding a large
  reservoir needs that term from elsewhere.

[^guide]: MOD16 User's Guide version 1.0, 2021-02-26
[^catalog]: LP DAAC catalog entry for MOD16A2GF v061, read 2026-09-06
[^cmr]: CMR collection and granule records, searched 2026-09-06
[^granule]: granule metadata over Cloud OPeNDAP, read 2026-09-06
[^record]: the evapotranspiration record, open-science-pillars/marketplace issue 69
