---
type: connector
title: "SNODAS: a registered collection with no granules, served from a dated directory"
description: "The snow assimilation the United States runs daily, distributed by NSIDC over plain HTTPS with no credential, as a dated path under a browsable directory. The collection is in the catalog with a DOI and a temporal extent claiming coverage to the present, and a granule search returns nothing for any window, so an agent that searches concludes the data is missing. One daily tar holds eight products whose file-name codes are not self-describing; the header packed beside each layer is the authority for what it is and how it is scaled."
tags: [connector, snodas, nsidc, nohrsc, snow, swe, https, hydrology]
generated: { by: claude-code/opus-5, at: 2026-09-08T05:30:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-08T04:19:42Z }
resource: https://noaadata.apps.nsidc.org/NOAA/G02158/
version: "G02158 version 1, the NOAA at NSIDC HTTPS file system, probed live 2026-09-08"
status: stable
stale_after: 2027-03-08
citation:
  access_date_required: true
  authority: https://nsidc.org/data/g02158
  data: "National Operational Hydrologic Remote Sensing Center. 2004. Snow Data Assimilation System (SNODAS) Data Products at NSIDC, Version 1. Boulder, Colorado USA. NSIDC: National Snow and Ice Data Center, accessed {access_date}, https://doi.org/10.7265/N5TB14TC"
  doi: "10.7265/N5TB14TC"
  note: "the access date matters because the directory is the only index: there is no granule record to pin, and a file that moves leaves nothing behind"
sources:
  - id: dataset
    resource: https://nsidc.org/data/g02158
    title: "The NSIDC data set page for G02158, read 2026-09-08: the level of service, the two spatial domains, the resolution and the access route"
  - id: directory
    resource: https://noaadata.apps.nsidc.org/NOAA/G02158/
    title: "The distribution directory itself, probed live 2026-09-08: the masked and unmasked trees, the dated path form, six files fetched with no credential"
  - id: faq
    resource: https://nsidc.org/data/user-resources/help-center/can-i-sum-snodas-values-given-area
    title: "The NSIDC help article 'Can I sum SNODAS values for a given area?', which states what the product is and is not for"
  - id: record
    resource: https://github.com/open-science-pillars/marketplace/issues/74
    title: "The measurement record: the granule searches that returned nothing, the file sizes, and the layer headers as read from the files"
---

# SNODAS: registered, catalogued, and not in the catalog

**Identity.** The Snow Data Assimilation System, run daily by NOAA's
National Operational Hydrologic Remote Sensing Center, distributed by
NSIDC as G02158.[^dataset] A 1 km grid over the conterminous United
States, daily from 2003-09-30, with snow water equivalent, snow depth,
melt, sublimation, snowpack temperature and the precipitation forcing
that drove them.

**The trap is the route.** The collection is registered in the
catalog: concept id `C1386246263-NSIDCV0`, DOI 10.7265/N5TB14TC, a
temporal extent beginning 2003-09-30 with the ends-at-present flag
set. A granule search against it returns **zero results for a month
inside the record, zero for the last two weeks, and zero with no
temporal filter at all** (measured 2026-09-08).[^record] There are no
granule records to find. An agent that searches the catalog, as it
would for any other NASA-adjacent product, finds a collection that
claims daily coverage to the present and concludes the data is
missing or the service is down.

**The data is a directory.** Plain HTTPS, no credential, no token, no
account:[^directory]

```
https://noaadata.apps.nsidc.org/NOAA/G02158/masked/2021/03_Mar/SNODAS_20210315.tar
https://noaadata.apps.nsidc.org/NOAA/G02158/unmasked/2021/03_Mar/SNODAS_unmasked_20210315.tar
```

The month directory is `MM_Mon` (`03_Mar`), the file is
`SNODAS_YYYYMMDD.tar` in the masked tree and
`SNODAS_unmasked_YYYYMMDD.tar` in the unmasked one, and each directory
is browsable, which is the only index there is. Build the URL from the
date; do not search for it, and do not reach for a NASA data client
here.

**Two domains, and two grids.** Read from the files themselves on
2026-09-08 rather than from the catalogue page, whose stated extents do
not match either header exactly:[^record]

| | Grid | West to east | South to north |
|---|---|---|---|
| masked | 6,935 by 3,351 | -124.7333 | to 52.8750 north |
| unmasked | 8,192 by 4,096 | -130.5167 to -62.2500 | 24.1000 to 58.2333 |

Both are 1 km. The unmasked file is roughly twice the size and is a
different array shape, so a reader that hardcodes the masked grid and
then pulls from the unmasked tree gets a reshape error at best and a
misaligned basin at worst. The layer descriptions, scales and no-data
value are the same in both.

**Sizes, measured 2026-09-08.**[^record]

| Date | masked | unmasked |
|---|---|---|
| 2021-03-15 | 19.9 MB | 37.8 MB |
| 2023-03-15 | 27.6 MB | 47.7 MB |
| 2026-09-01 | 2.7 MB | 5.7 MB |

The size follows the snow: these are compressed integer grids, and a
bare late-summer domain compresses to a tenth of a deep March one.
Useful for budgeting a pull, and not a measurement of anything.

## What one file holds

A daily tar holds 16 members: eight products, each a `.dat.gz` beside
a `.txt.gz` header. Every layer is a big-endian 16-bit integer grid at
1 km with -9999 for no data, on whichever of the two grids above the
tree uses. The descriptions
below are quoted from those headers.[^record]

| Code in the file name | Description, from the file's own header | Units |
|---|---|---|
| 1025 SlL00 | Scaled Non-snow accumulation, 24-hour total | kg per m2 / 10 |
| 1025 SlL01 | Scaled Snow accumulation, 24-hour total | kg per m2 / 10 |
| 11034 tS__ | Modeled snow water equivalent, total of snow layers | metres / 1000 |
| 11036 tS__ | Modeled snow layer thickness, total of snow layers | metres / 1000 |
| 11038 wS__ | Modeled average temperature, SWE-weighted average of snow layers, 24-hour average | Kelvins |
| 11039 lL00 | Modeled blowing snow sublimation, 24-hour total | metres / 100000 |
| 11044 bS__ | Modeled melt, bottom of snow layers, 24-hour total | metres / 100000 |
| 11050 lL00 | Modeled snowpack sublimation, 24-hour total | metres / 100000 |

**Read the header, not the file name.** The codes do not say what they
hold: 11038 is a temperature and 11044 is melt, and neither is what
its position in the list suggests. The scale is in the header too, and
it differs between layers by three orders of magnitude. A reader that
maps codes to meanings from a remembered list will produce a snow
water equivalent that is a temperature, in the wrong units, without
raising anything.

## Level of service

NSIDC states a **Basic** level of service for this data set, and says
it "was recently changed to a 'Basic' Level of Service" because of
funding limitations. No date is published for that change; do not
supply one.[^dataset] In practice a Basic level means the files are
served and the support around them is not guaranteed, which is a
reason to freeze what a result depends on rather than to plan on
refetching it later.

## What leaves the machine

A GET for a dated path. No credential, no token, no query string, no
account. The request carries the URL and a user agent and nothing
else, so nothing identifying the user or the analysis leaves the
machine beyond the fact that a date was fetched.

## What this connector is not for

Not a water budget term. The product's own distributor states that it
is a model output and is not recommended for quantitative water budget
analysis, while comparing sums over an area between periods is
reasonable.[^faq] The gotcha beside this concept carries the rule and
the wording it rests on.

[^dataset]: the NSIDC data set page for G02158
[^directory]: the distribution directory, probed live
[^faq]: the NSIDC help article on summing SNODAS values
[^record]: the measurement record for this work
