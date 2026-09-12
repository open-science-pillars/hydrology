---
type: dataset-gotcha
spheres: [hydrosphere]
title: "The OpenET provisional window: the last 120 days will change, and a receipt without its access date cannot be reproduced"
description: "OpenET states that real-time data is provisional for the last 120 days and that those values can and will change, because gridMET is not final for 60 days and new Landsat imagery is still being processed; updates run monthly for the prior three to four months. A number pulled inside that window is a draft, so it carries its access date, it is not a baseline, and a comparison that mixes provisional months with settled ones measures the pipeline as well as the weather."
tags: [openet, evapotranspiration, et, provisional, reproducibility, access-date, api]
generated: { by: claude-code/fable-5, at: 2026-09-07T00:25:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-07T02:11:54Z }
severity: medium
connector: ../connectors/openet-api.md
status: stable
stale_after: 2027-03-06
sources:
  - id: faq
    resource: https://openet.gitbook.io/docs/additional-resources/faq
    title: "OpenET FAQ: 'Realtime OpenET data is considered provisional for the last 120 days. This data can and will change and is not considered stable/static/final', with the reasons (gridMET not finalized for 60 days; new Landsat imagery) and the monthly update of the prior three to four months, read 2026-09-06"
  - id: connector
    resource: ../connectors/openet-api.md
    title: "This bundle's OpenET connector concept (the endpoint, the tiers, the ensemble statistic and the provisional window)"
  - id: record
    resource: https://github.com/open-science-pillars/marketplace/issues/69
    title: "The evapotranspiration record: the requests made, their dates and the fixtures that hold their answers"
---

# The OpenET provisional window

**Mechanism.** OpenET publishes near the present, and the recent end
of the record is still moving: "Realtime OpenET data is considered
'provisional' for the last 120 days. This data can and will change
and is not considered stable/static/final."[^faq] The reasons are in
the same place: gridMET, the meteorological forcing, is not finalized
for 60 days, and Landsat scenes continue to arrive and be processed;
the service updates the prior three to four months every month.

Nothing in a response marks a value as provisional. A request for the
last twelve months returns twelve numbers of identical appearance, of
which the last four are drafts.

**Wrong-result mode.** A drought brief quotes this season's
evapotranspiration anomaly and the number moves under it before
anyone reads the brief twice. A month-by-month comparison against a
settled product reads the pipeline's revisions as physical change. A
baseline or a climatology is built with its most recent months still
in revision, so the anomalies computed against it drift as the
baseline settles. Two runs of the same analysis a month apart
disagree, and the disagreement is attributed to code.

**Correct approach.** Record the access date beside every OpenET
number, and state which months of the series were inside the 120-day
window on that date. Prefer months outside the window for anything
that has to be reproducible: a baseline, a published figure, a
comparison against another product. Where recent months are the
point, say in the same sentence that they are provisional and will be
revised, and keep the response itself, not just the derived number,
so the revision can be measured rather than guessed. A fixture that
holds an OpenET answer records the request, the polygon, the tier and
the retrieval time for exactly this reason.

**Measured (2026-09-06).** The fixtures in this bundle hold calendar
year 2023 over a HUC12 in the Roaring Fork, pulled on 2026-09-06:
every month is years outside the provisional window, so those numbers
are settled and can be compared against MOD16 without this caveat.
The same request for the months since May 2026 would not be.[^record]

**Verification.** Take the access date in an OpenET receipt, subtract
120 days, and confirm no month of the series begins after that date;
where one does, confirm the receipt says so.

[^faq]: OpenET FAQ, read 2026-09-06
[^connector]: this bundle's OpenET connector concept
[^record]: the evapotranspiration record, open-science-pillars/marketplace issue 69
