---
type: dataset-gotcha
spheres: [hydrosphere]
title: "Hydrocron picks a product version when you do not, and the versions differ by metres"
description: "The timeseries service accepts a collection_name and chooses one when the caller omits it. The default is now Version D. Measured on one Mississippi reach for 2024: Version C spans -3.347 to 2.561 m and Version D spans -0.534 to 10.201 m, the two share no timestamps at all, and matched passes differ by up to 7.4 m. A series assembled across a change of default carries a step that is the product version, and it cannot be detected by joining on time because there is no overlap to join."
tags: [swot, hydrocron, riversp, lakesp, version, collection, podaac, hydrology]
generated: { by: claude-code/opus-5, at: 2026-09-08T06:20:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-08T05:18:36Z }
severity: high
dataset: ../datasets/swot-river-lake.md
eval_case: hydrocron-collection-default
status: stable
stale_after: 2027-03-08
sources:
  - id: service
    resource: https://soto.podaac.earthdatacloud.nasa.gov/hydrocron/v1/timeseries
    title: "The Hydrocron timeseries endpoint, probed live 2026-09-08: the collection_name parameter, the ten names its own 400 lists, and the default"
  - id: record
    resource: https://github.com/open-science-pillars/marketplace/issues/76
    title: "The measurement record: the version comparison at reach 74210000331 and at 63470800171, and the gauge that says which version is physical"
  - id: connector
    resource: ../connectors/hydrocron-swot.md
    title: "This bundle's Hydrocron connector concept: the endpoint, the fields and the citation"
---

# Hydrocron picks a version when you do not

**Mechanism.** `collection_name` is an optional parameter. Omit it and
the service answers from whichever collection it currently defaults to,
and that default has moved with the product: it is **Version D** as of
2026-09-08.[^service] Nothing in the response says which collection
answered, so a series carries no record of the version it came from,
and two series pulled either side of a change of default differ by the
version without differing in anything a reader can see.

The parameter is real and validated: a name the service does not know
returns 400 with all ten it accepts,
`SWOT_L2_HR_{RiverSP,RiverSP_reach,RiverSP_node,LakeSP,LakeSP_prior}_{2.0,D}`.[^service]

**But a misspelled parameter is ignored rather than refused.**
`collection`, `collection_id` and `version` are all accepted silently
and change nothing.[^record] So a caller who guesses the key gets the
default and a clean 200, and believes they pinned a version. That is
the worse half of this: an explicit attempt to be careful produces the
same result as no attempt at all.

**Measured (2026-09-08).** Reach 74210000331, the Mississippi at Baton
Rouge, calendar 2024:[^record]

| | Version C (2.0) | Version D |
|---|---|---|
| Passes with a time and an elevation | 47 | 52 |
| Water surface elevation range | -3.347 to 2.561 m | -0.534 to 10.201 m |
| Timestamps shared with the other version | **0** | **0** |

Matched passes are 2 to 3 seconds apart, so **the two versions cannot
be joined on time**, which is the first thing anyone would try in order
to see the step. Across the 17 passes that match within two minutes,
Version D minus Version C runs -3.095 to +7.431 m with a mean of
+4.011 m. On a second reach, 63470800171, the same comparison gives
+3.206 to +9.493 m with a mean of +5.375 m over 15 matched passes.

**A gauge settles which version is physical here.** The gauge at Baton
Rouge puts the 2024 water surface between 1.47 and 10.37 m above its
datum, which sits at zero. Version D brackets that range; Version C
does not, and a Mississippi surface three metres below the geoid 380 km
from the Gulf is not a river.[^record] So at this reach the collection
choice is not a calibration nuance. It decides whether the series can
be believed.

**Wrong-result mode.** A study that pulled a series before the default
changed and extended it afterwards has a step of metres in the middle
with nothing marking it, on a quantity whose real interannual signal is
of the same order. The step will be read as hydrology: a shift in stage,
a change in the rating, a flood. And the natural check fails silently,
because the timestamps do not line up, so an analyst comparing the two
pulls finds no common passes and concludes the records are simply
different periods.

**Correct approach.** Name the collection on every request, and record
the name in the receipt beside the retrieval date. Where a series must
span a version change, treat it as two series and say so, rather than
concatenating and hoping. Do not pin a version by adding a parameter
whose name you have not checked against the service's own error message:
confirm the key is honoured by asking for a collection you know differs
and seeing the answer change.

**Verification.** Pick a reach with a year of passes. Request it twice,
once naming the 2.0 collection and once naming the D collection, and
confirm the elevations differ and the timestamps do not match. Then
request it with a deliberately misspelled parameter name and confirm the
response is identical to the default rather than an error.

[^service]: the Hydrocron timeseries endpoint, probed live
[^record]: the scout and confrontation measurement record
[^connector]: this bundle's Hydrocron connector concept
