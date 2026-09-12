---
type: dataset-gotcha
spheres: [hydrosphere]
title: "The OpenET monthly ensemble is not always the sum of its own days: three repeated months over Colorado headwater units in 2023"
description: "The monthly and daily OpenET ensembles are separate series, and over two Roaring Fork HUC12s the monthly ensemble returned one identical value for January, February and March 2023 (28.411 mm three times on one unit, 23.225 on the other) while the daily ensemble over the same polygon and months varied normally and summed to 11.15, 20.85 and 32.63 mm. The same units in 2021, 2022 and 2024 show twelve distinct monthly values. A repeated monthly value is a signal to check against the daily series before the months are used."
tags: [openet, evapotranspiration, et, monthly, daily, ensemble, verification, anomaly]
generated: { by: claude-code/fable-5, at: 2026-09-07T00:30:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-07T02:11:54Z }
severity: medium
connector: ../connectors/openet-api.md
status: stable
stale_after: 2027-03-06
sources:
  - id: connector
    resource: ../connectors/openet-api.md
    title: "This bundle's OpenET connector concept (the endpoint, the intervals and the ensemble statistic)"
  - id: ee
    resource: https://developers.google.com/earth-engine/datasets/catalog/OpenET_ENSEMBLE_CONUS_GRIDMET_MONTHLY_v2_0
    title: "The Earth Engine catalog entry for the OpenET monthly ensemble: the ensemble statistic and the member models, read 2026-09-06"
  - id: faq
    resource: https://openet.gitbook.io/docs/additional-resources/faq
    title: "OpenET FAQ, read 2026-09-06: the documentation consulted for an explanation of the repeated months, which it does not give"
  - id: record
    resource: https://github.com/open-science-pillars/marketplace/issues/69
    title: "The evapotranspiration record: the monthly and daily requests over Capitol Creek and Outlet Castle Creek with their responses"
---

# The OpenET monthly ensemble is not always the sum of its own days

**Mechanism.** OpenET serves a monthly ensemble and a daily ensemble.
They are separate collections built by separate aggregations, so
neither is derived from the other at request time, and nothing in a
response says whether the two agree. Over two hydrologic units in the
Roaring Fork they do not agree for the first three months of 2023,
and the monthly series gives away that something is wrong only if the
values are looked at rather than summed: it repeats one number three
times.

**Measured (2026-09-06).** Monthly Ensemble ET, mm, model `Ensemble`,
`reducer` mean, `reference_et` gridMET:[^record]

| Unit | 2023-01 | 2023-02 | 2023-03 |
|---|---|---|---|
| HUC12 140100040402, Capitol Creek (95.2 km2) | 28.411 | 28.411 | 28.411 |
| HUC12 140100040203, Outlet Castle Creek (22.3 km2) | 23.225 | 23.225 | 23.225 |

Both units return ordinary varying values from April onward. The
daily ensemble over the Capitol Creek polygon for exactly those three
months has 87 distinct values across 90 days, between 0.064 and 1.77
mm a day, and sums to 11.154, 20.853 and 32.625 mm for January,
February and March: a rising late-winter series, which is what a
snowmelt basin should show. The monthly product's flat 28.411 is 2.5
times the daily January and 0.87 of the daily March, and the three
monthly values together (85.23 mm) exceed the daily total (64.63 mm)
by a third.

The same Capitol Creek unit in other years shows nothing of the kind:
2021, 2022 and 2024 each return twelve distinct monthly values, and
their Januaries are 9.693, 10.038 and 9.275 mm, in line with the
daily sum for January 2023 and not with the monthly 28.411.[^record]

No page of the OpenET documentation read on that date (quotas, FAQ,
data availability, terms of service, the Earth Engine ensemble
catalog entry) mentions repeated months, interpolation between
overpasses, or a winter fallback, so this concept records the
measurement and not a mechanism.[^faq][^ee] What can be said is
bounded: two units, one product, three consecutive months of one
year, reproducible on demand from the fixtures beside this concept.

**Wrong-result mode.** A monthly water balance for water year 2023
over these units carries 20 mm of evapotranspiration that the daily
product does not see, in the months when a snowmelt basin is storing
rather than evaporating. A cold-season drought index reads three
identical months as unremarkable rather than as a defect. A
comparison against MOD16 (which gives 19.88, 27.61 and 37.57 mm for
those months over Capitol Creek) attributes the difference to MOD16.

**Correct approach.** Look at a monthly OpenET series before using
it: a value that repeats its neighbour to the last decimal is not a
coincidence in a physical quantity, and this bundle's loader prints
that signal when it sees it. Where the months matter, pull the daily
ensemble for the same polygon and period and compare the sums; where
they disagree, use the daily series and say so, or drop the months.
Keep both responses as fixtures so the disagreement stays
recomputable, and report it to the provider rather than working
around it silently.

**Verification.** Load the monthly fixture over Capitol Creek and
confirm the loader names 2023-02 and 2023-03 as repeats of the month
before; load the daily fixture for the same quarter and confirm the
monthly sums 11.154, 20.853 and 32.625; confirm the two totals for
the quarter differ by about a third.[^record]

[^connector]: this bundle's OpenET connector concept
[^ee]: Earth Engine catalog, OpenET ensemble monthly v2.0, read 2026-09-06
[^faq]: OpenET FAQ, read 2026-09-06
[^record]: the evapotranspiration record, open-science-pillars/marketplace issue 69
