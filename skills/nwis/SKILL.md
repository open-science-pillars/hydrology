---
name: nwis
description: "USGS NWIS streamflow: gauges, daily values via dataretrieval, provisional vs approved flags, rating-curve caveats, the waterdata API migration."
user-invocable: false
---

# nwis

Background expertise for USGS streamflow data. Product facts live in
`knowledge/datasets/nwis-streamflow.md`; the provisional trap in
`knowledge/gotchas/nwis-provisional-data.md`.

## Knowledge first

Consult and restate: the provisional-data gotcha on ANY window
touching recent months (observed 2026-07-05: a June-July window came
back 100% P-flagged while 2023 was 100% A); the dataset concept's
rating-curve and revision notes.

## Working facts

- Daily values (dv) are the workhorse; instantaneous values (iv) are
  15-minute. Parameter codes select variables (00060 discharge cfs,
  00065 gage height ft); site numbers are the identity (8-15 digits,
  kept as STRINGS: leading zeros are significant, e.g. 09380000).
- Every value carries a qualifier: A approved, P provisional, plus
  qualifiers like e (estimated) and Ice. Statistics segregate by flag.
- Discharge is not measured; it is stage passed through a RATING
  CURVE that is remade after floods and channel shifts, so approved
  values can still be revised when ratings are, and extreme flows sit
  on the extrapolated end of the rating.
- Library note (observed 2026-07-05): dataretrieval's `nwis.get_dv`
  is deprecated for removal on/after 2027-05-06 in favor of
  `waterdata.get_daily()`; new code targets the waterdata API.
- Units are US customary (cfs, feet); conversions are stated.

## Must NOT

- Never mix P and A values in one statistic without stating the split.
- Never treat site numbers as integers.
- Never quote an extreme flow without the rating-extrapolation caveat.
- Never assume approved means final; ratings revise history.
