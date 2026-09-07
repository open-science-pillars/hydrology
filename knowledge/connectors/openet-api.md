---
type: connector
title: "The OpenET API: a key in a header, a per-request area cap that no basin clears, and a 120-day window in which values change"
description: "OpenET serves field and sub-basin evapotranspiration over the conterminous United States from a POST endpoint that takes one simple closed polygon and returns a timeseries. The key travels in the Authorization header from the environment. The account tier sets a per-request area cap of 50,000 or 200,000 acres, which every basin in this plugin's fixtures exceeds by one to three orders of magnitude, and the service refuses rather than truncates. The last 120 days are provisional and will change."
tags: [openet, evapotranspiration, et, api, connector, area-cap, provisional, conus, hydrology]
generated: { by: claude-code/fable-5, at: 2026-09-06T23:55:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-07T02:11:54Z }
resource: https://openet.gitbook.io/docs
status: stable
stale_after: 2027-03-06
citation:
  access_date_required: true
  authority: https://openet.gitbook.io/docs
  data: "OpenET ensemble evapotranspiration, accessed {access_date}; Melton, F., Huntington, J., Grimm, R., et al., 2021. OpenET: Filling a Critical Data Gap in Water Management for the Western United States. Journal of the American Water Resources Association, doi:10.1111/1752-1688.12956"
  doi: "10.1111/1752-1688.12956 (the OpenET paper; the API itself carries no dataset DOI)"
  note: "the data is CC-BY-4.0 and the terms of service require visible attribution of OpenET as the source whenever the data is redistributed or displayed; the ensemble's own models each carry a citation in the Earth Engine catalog"
sources:
  - id: quota
    resource: https://openet.gitbook.io/docs/additional-resources/quota
    title: "OpenET account tiers and quotas (monthly query limit, max area acres, max polygons, field ids per query) and the global rate limit, read 2026-09-06"
  - id: api
    resource: https://openet.gitbook.io/docs/reference/api-reference/raster.md
    title: "The raster timeseries polygon endpoint: URL, method, the Authorization header and the request body fields, read 2026-09-06"
  - id: faq
    resource: https://openet.gitbook.io/docs/additional-resources/faq
    title: "The OpenET FAQ: the 120-day provisional window and why it exists (gridMET not finalized for 60 days, new Landsat imagery), read 2026-09-06"
  - id: ee
    resource: https://developers.google.com/earth-engine/datasets/catalog/OpenET_ENSEMBLE_CONUS_GRIDMET_MONTHLY_v2_0
    title: "The Earth Engine catalog entry for the OpenET ensemble: the ensemble statistic, the six member models, the band names and the citation, read 2026-09-06"
  - id: tos
    resource: https://openet.gitbook.io/docs/terms-of-service
    title: "OpenET terms of service: the visible source attribution requirement, read 2026-09-06"
  - id: record
    resource: https://github.com/open-science-pillars/marketplace/issues/69
    title: "The evapotranspiration record: the measured refusal above the cap, the sub-cap request that answered, and the monthly against daily comparison"
---

# The OpenET API

**What it is.** OpenET publishes satellite-based evapotranspiration
over the conterminous United States, aimed at fields and small
management units. This bundle uses the Ensemble model as an
independent check on MOD16 where a polygon is small enough for the
service to answer, never as the basin term.

## The request

`POST https://openet-api.org/raster/timeseries/polygon`, JSON body,
with the key in the `Authorization` header.[^api] The body carries
`date_range` (two ISO dates), `interval` (`daily` or `monthly`),
`geometry` (a flat list of longitude and latitude for one simple
closed polygon), `model`, `variable`, `reference_et`, `reducer`,
`units` and `file_format`. Omitting `reducer` is answered `422` with
the missing field named, measured 2026-09-06.[^record] A polygon with
thousands of vertices is simplified before it is sent; the
simplification tolerance and the resulting vertex count belong in the
receipt, because they change the polygon whose mean is returned.

## The key

The key is read from `OPENET_API_KEY` in the environment and travels
only in the `Authorization` header of a request to `openet-api.org`.
It never appears in a URL, a log line, a capture, a fixture or a
receipt. Without it the service answers `403 {"detail":"Not
authenticated"}`.[^record]

## Tiers, quotas and the area cap

| Tier | Area per request | Polygons | Queries per month |
|---|---|---|---|
| Tier 1 | 50,000 acres | 100 | 100 |
| Tier 2 | 200,000 acres | 200 | 400 |

All users share a global rate limit of 20 queries per minute and 500
per hour.[^quota]

The area cap is the constraint that decides what OpenET can be used
for here. Every basin in this plugin's fixtures is far above it: the
Roaring Fork at Glenwood Springs is 930,871 acres (18.6 times the
Tier 1 cap), the Colorado above Lees Ferry 68,310,627 acres (1,366
times), the Ohio at Metropolis 129,206,044 acres (2,584 times). The
service refuses rather than truncating or sampling, and names the cap
when it does: `422 {"detail":"Single query area limit exceeded.
Region must not exceed 50000 acres."}`, measured over the whole
Roaring Fork polygon on 2026-09-06.[^record] The refusal is the
correct behaviour and the loader reproduces it before any request is
sent ([the area-cap gotcha](../gotchas/openet-area-cap.md)).

A sub-cap request over HUC12 140100040402 (Capitol Creek, 23,512
acres, inside the Roaring Fork) answered `200` in 2.6 seconds with 12
monthly values.[^record]

## The ensemble statistic

The ensemble value is not a median. The Earth Engine catalog states
it is "computed as the mean of the ensemble after filtering outliers
using the median absolute deviation (mad)", over ALEXI/DisALEXI,
eeMETRIC, geeSEBAL, PT-JPL, SIMS and SSEBop; the band is
`et_ensemble_mad`, and `et_ensemble_mad_min`, `_max` and `_count`
travel beside it.[^ee] A receipt that calls the value a median
describes a different statistic than the one it holds.

## The provisional window

"Realtime OpenET data is considered 'provisional' for the last 120
days. This data can and will change and is not considered
stable/static/final."[^faq] The FAQ gives the reasons: gridMET is not
finalized for 60 days, and new Landsat imagery has to be processed;
updates are made monthly for the prior three to four months. A number
pulled inside that window has to carry its access date, and a result
that depends on it is not reproducible until the window has passed
([the provisional-window gotcha](../gotchas/openet-provisional-window.md)).

## Coverage

Conterminous United States. The ensemble is monthly from 2000 and
daily from 2016.[^faq] Coverage is not what stops a basin request;
the area cap is.

## What leaves the machine

The key, to `openet-api.org` only, in the `Authorization` header. The
polygon (simplified), the date range, the interval, the model and the
units, in the request body. Nothing else: no file, no local path, no
Earthdata credential. The service's answer is a timeseries, which
this bundle stores as a fixture with its request beside it so the
number can be traced without repeating the request.

## Attribution

The data is CC-BY-4.0 and the terms of service require OpenET to be
visibly attributed as the source wherever the data is reproduced or
displayed.[^tos] Cite Melton et al. 2021 beside it.[^ee]

[^quota]: OpenET quota documentation, read 2026-09-06
[^api]: OpenET raster API reference, read 2026-09-06
[^faq]: OpenET FAQ, read 2026-09-06
[^ee]: Earth Engine catalog, OpenET ensemble monthly v2.0, read 2026-09-06
[^tos]: OpenET terms of service, read 2026-09-06
[^record]: the evapotranspiration record, open-science-pillars/marketplace issue 69
