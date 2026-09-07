---
type: dataset-gotcha
title: "MOD16 composites into calendar months: the periods straddle month ends and the last one of the year is five or six days"
description: "MOD16 delivers 46 composites a year, each an 8-day total, except the last of each year which covers 5 days (6 in a leap year). Composites straddle month boundaries, so a monthly total is an apportioning by day, not a sum of composites. Dividing every period by 8 spreads the year-end total over three days that do not exist: over the Roaring Fork in 2023 that moves 1.67 mm out of December and into January, and assigning composites to months by their start date moves millimetres across every month boundary while the annual total barely changes."
tags: [mod16, modis, evapotranspiration, compositing, monthly, aggregation, calendar]
generated: { by: claude-code/fable-5, at: 2026-09-07T00:20:00Z }
severity: medium
dataset: ../datasets/mod16a2gf.md
status: draft
stale_after: 2027-03-06
sources:
  - id: guide
    resource: https://lpdaac.usgs.gov/documents/931/MOD16_User_Guide_V61.pdf
    title: "MOD16 User's Guide version 1.0 of 2021-02-26: 'the last 8-day (MOD16A2.A20??361.*.hdf) of each year is not 8-day but either 5-day or 6-day depending on normal or leap year'"
  - id: cmr
    resource: https://cmr.earthdata.nasa.gov/search/granules.json?short_name=MOD16A2GF&version=061
    title: "Granule temporal extents that give each composite its true length (A2025361 covers 2025-12-27 to 2025-12-31, five days), searched 2026-09-06"
  - id: dataset
    resource: ../datasets/mod16a2gf.md
    title: "This bundle's MOD16A2GF concept (the compositing scheme and the units)"
  - id: record
    resource: https://github.com/open-science-pillars/marketplace/issues/69
    title: "The evapotranspiration record: the monthly series measured over the fixture basins"
---

# MOD16 composites into calendar months

**Mechanism.** A MOD16 composite is a total over its period, not a
rate: `ET_500m` is kg per m2 per 8 days. The periods begin on days of
year 1, 9, 17 and so on, which means they cross month boundaries
freely, and the last period of each year begins on day 361 and runs
to 31 December, so it is five days long in a normal year and six in a
leap year.[^guide] The granule metadata gives the true length:
`MOD16A2GF.A2025361.h09v05` covers 2025-12-27 to 2025-12-31.[^cmr]

Two habits break on this. Summing the composites whose start date
falls inside a month gives that month between three and four
composites at random and mixes in days from the neighbouring months.
Dividing every composite by eight to get a daily rate understates the
year-end period's rate by five eighths and, if the daily rates are
then re-accumulated, carries three days that do not exist into the
following January.

**Correct approach.** Read each composite's length from the granule's
own temporal extent, never from the number 8 and never from the day
of year alone. Turn each composite into a daily rate over its own
length, then accumulate the days into calendar months. A month's
total is then a sum of daily rates over exactly its days, the
year-end period contributes five days to December and nothing to
January, and a partial month at the edge of a series is visible as a
day count in the receipt rather than hidden in a total. This bundle's
loader carries the length per composite in the window file
(`composite_days`) and reports the short periods it used.

**Measured (2026-09-06).** Over the Roaring Fork for 2023, the
apportioned monthly series is 20.77, 29.88, 42.57, 54.38, 61.76,
59.86, 65.12, 54.72, 32.31, 23.66, 23.94 and 25.65 mm, 494.60 mm for
the year, with the composite beginning 2023-12-27 weighted by its
true five days.[^record] That composite holds 4.446 mm
over its five days, a rate of 0.889 mm a day; read as eight days the
rate becomes 0.556, and the five days that fall in December carry
2.78 mm instead of 4.45 while the three days that do not exist carry
1.67 mm into the following January. Assigning composites to months by
their start date instead of by their days moves several millimetres
between every pair of neighbouring months while leaving the annual
total nearly unchanged, which is what makes the error easy to miss in
an annual number and easy to see in a seasonal one.

**Wrong-result mode.** A seasonal water balance closes in the annual
total and fails month by month. A drought index built on monthly
anomalies inherits a systematic December deficit and a January
excess. A comparison against a monthly product from another source
(the OpenET ensemble, a gauge-based forcing) attributes the
apportioning error to the products.

**Verification.** Load the Roaring Fork fixture and confirm the
receipt names the short period `2023-12-27 (5 days)`, that every
month's `days_covered` matches the calendar, and that the monthly
totals sum to the annual total.[^record]

[^guide]: MOD16 User's Guide version 1.0, 2021-02-26
[^cmr]: CMR granule temporal extents, searched 2026-09-06
[^dataset]: this bundle's MOD16A2GF concept
[^record]: the evapotranspiration record, open-science-pillars/marketplace issue 69
