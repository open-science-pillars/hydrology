---
type: dataset-gotcha
spheres: [hydrosphere]
title: "The OpenET area cap: a basin request is refused, not sampled, and no basin mean comes back"
description: "OpenET caps a single request at 50,000 acres on Tier 1 and 200,000 on Tier 2, and answers a larger polygon with 422 'Single query area limit exceeded'. Every basin in this bundle's fixtures is above the cap: the Roaring Fork by 18.6 times, the Colorado above Lees Ferry by 1,366, the Ohio at Metropolis by 2,584. The answer is not to tile the basin into sub-cap pieces and average them, nor to shrink the polygon until the service answers; it is to use a product that can see the basin and keep OpenET as a sub-cap check."
tags: [openet, evapotranspiration, et, area-cap, quota, api, basin-mean, refusal]
generated: { by: claude-code/fable-5, at: 2026-09-07T00:15:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-07T02:11:54Z }
severity: high
connector: ../connectors/openet-api.md
eval_case: openet-area-cap
status: stable
stale_after: 2027-03-06
sources:
  - id: quota
    resource: https://openet.gitbook.io/docs/additional-resources/quota
    title: "OpenET account tiers and quotas: 50,000 acres and 100 queries a month at Tier 1, 200,000 acres and 400 at Tier 2, 20 queries a minute and 500 an hour for all users, read 2026-09-06"
  - id: connector
    resource: ../connectors/openet-api.md
    title: "This bundle's OpenET connector concept (the endpoint, the key handling, the tiers and the measured refusal)"
  - id: dataset
    resource: ../datasets/mod16a2gf.md
    title: "This bundle's MOD16A2GF concept: the product that does cover a basin, and its own limits"
  - id: record
    resource: https://github.com/open-science-pillars/marketplace/issues/69
    title: "The evapotranspiration record: the refused whole-basin request and the sub-cap request that answered, both verbatim"
---

# The OpenET area cap

**Mechanism.** OpenET is built for fields and small management units,
and the service enforces that with a per-request area cap: 50,000
acres on Tier 1, 200,000 on Tier 2.[^quota] A request over a larger
polygon is refused outright. Measured on 2026-09-06 over the whole
Roaring Fork polygon, the answer was `422 {"detail":"Single query
area limit exceeded. Region must not exceed 50000 acres."}` in 1.3
seconds.[^record] Nothing is sampled, nothing is truncated, and no
partial series comes back.

The trap is not the refusal, which is loud. It is what a determined
caller does next.

**Measured (2026-09-06).** Every fixture basin in this bundle, in
acres, against the two caps:[^record]

| Basin | Acres | Times the Tier 1 cap | Times the Tier 2 cap |
|---|---|---|---|
| Roaring Fork at Glenwood Springs | 930,871 | 18.6 | 4.7 |
| Colorado above Lees Ferry | 68,310,627 | 1,366 | 342 |
| Ohio at Metropolis | 129,206,044 | 2,584 | 646 |

A HUC12 inside the Roaring Fork (Capitol Creek, 23,512 acres) is
under the cap and answers in 2.6 seconds.[^record] The gap between a
sub-basin unit and a basin is three orders of magnitude, not a
setting.

**Wrong-result mode.** Three ways round the refusal, each of which
produces a number:

- Tile the basin into sub-cap polygons and average the answers. At
  Tier 1 the Lees Ferry basin needs about 1,370 requests against a
  quota of 100 a month, so in practice a few tiles get requested and
  their mean is presented as the basin's. It is the mean of wherever
  the tiles happened to fall, and OpenET's models are calibrated for
  agricultural and managed land, so the tiles that answer are not a
  random sample of a basin that is mostly forest, rock and snow.
- Shrink or simplify the polygon until the service answers, and call
  the result the basin. The polygon that was measured is then not the
  polygon in the methods section.
- Take a nearby field or a single sub-unit as representative of the
  basin. Over the Capitol Creek unit the OpenET annual total for 2023
  is 724.60 mm; over the whole Roaring Fork, MOD16 gives 494.60 mm.
  A sub-unit is not a basin.

**Correct approach.** Refuse the basin request before it is sent,
name the cap, state how many times over it the polygon is, and say
what to use instead: a product whose grid covers the basin (MOD16 in
this bundle, and the basin term stays MOD16 for exactly this reason).
Use OpenET where it is designed to be used, on a sub-cap unit, and
use it as a check on the basin product rather than as a substitute
for it: the sub-cap comparison over Capitol Creek for 2023 is
MOD16 521.12 mm against OpenET 724.60 mm, a ratio of 0.72, and that
disagreement is a fact about the two products worth carrying into any
water balance.[^dataset] If a basin mean from OpenET is genuinely
needed, the honest route is a request for a higher tier or a bulk
export, declared as such, not a mosaic of whatever fitted under the
cap.

**Verification.** Ask this bundle's loader for OpenET over a fixture
basin and confirm it refuses with the acreage, the cap and the
multiple before any request leaves the machine; ask it over the
Capitol Creek polygon and confirm it returns the twelve months.[^record]

[^quota]: OpenET quota documentation, read 2026-09-06
[^connector]: this bundle's OpenET connector concept
[^dataset]: this bundle's MOD16A2GF concept
[^record]: the evapotranspiration record, open-science-pillars/marketplace issue 69
