---
type: dataset-gotcha
title: "One peaks response holds two series, and they are not the same event"
description: "A peaks query without a parameter returns the annual peak discharge and the annual peak stage together, interleaved, with identical column names and different units. Measured at French Broad River at Asheville: 270 rows, 130 of them discharge in cubic feet per second for 1896 through 2025 and 140 stage in feet for 1796 through 2025. A count of the response is not a count of the record, and a series built from it mixes feet with cubic feet per second."
tags: [usgs, peaks, flood-frequency, parameter, stage, discharge, hydrology]
generated: { by: claude-code/opus-5, at: 2026-09-07T23:45:00Z }
severity: high
dataset: ../datasets/usgs-peaks.md
eval_case: peaks-two-series-one-response
status: draft
stale_after: 2027-03-07
sources:
  - id: api
    resource: https://api.waterdata.usgs.gov/ogcapi/v0/collections/peaks
    title: "The peaks collection: the parameter_code and unit_of_measure fields, and the collection description's own warning that the peak flow and the maximum water level need not coincide; probed live 2026-09-07"
  - id: measurement
    resource: https://github.com/open-science-pillars/marketplace/issues/73
    title: "The row counts at French Broad River at Asheville and the qualifier vocabulary measurement"
---

# One peaks response holds two series

**Mechanism.** The peaks collection stores one row per monitoring
location, **parameter** and water year. A typical streamgage has two
peak series: discharge (parameter 00060, `ft^3/s`) and stage (00065,
`ft`). A query that names only the site returns both, sorted together,
in rows whose columns are identical apart from `parameter_code` and
`unit_of_measure`.[^api]

They are not two views of one event. The collection's own description
says the annual peak flow may not occur at the same time as the
maximum water level, because of backwater, tidal fluctuation and
similar conditions,[^api] and the stage series carries a qualifier
that says exactly that on individual rows: `GHNOTASSCPKQ`, the gage
height is not the one associated with the peak discharge. The stage
series also runs on its own datum history, with `DATUMCHANGE` and
`DIFFDATUM` rows marking where the reference moved.

**Measured (2026-09-07).** French Broad River at Asheville, North
Carolina (USGS-03451500):[^measurement]

| | Rows | Water years | Units |
|---|---|---|---|
| Discharge (00060) | 130 | 1896 to 2025 | ft^3/s |
| Stage (00065) | 140 | 1796 to 2025 | ft |
| Unfiltered response | 270 | 1796 to 2025 | both |

The stage record is the longer one and begins a century earlier,
because the nineteenth century high-water marks survive as heights
and were never converted to discharges.

**Wrong-result mode.** The failure is quiet at every step. A record
length taken from the response is 270 years of peaks for a gauge with
130 of them, which doubles the apparent sample and shrinks every
confidence interval. A maximum over the mixed column returns the
discharge, so nothing looks wrong. A minimum returns a stage, so the
range is meaningless. A frequency fit over the concatenation is fitted
to a bimodal mixture of two quantities in two units, and log-Pearson
III will fit it and return numbers. And a peak file written from the
mixed rows hands a flood frequency program a station whose record
appears to run from 1796 with 270 peaks.

**Correct approach.** Pass the parameter, always: `parameter_code`
in the query, or filter on it before anything else. Where a workflow
loads peaks, make the parameter a required argument rather than a
default, so the choice is stated at the call site. Report the series
with its unit attached. If both series are wanted, keep them as two
series with two units and two record lengths, and never join them on
water year as though the rows describe one event.

**Verification.** Query a long-record gauge for peaks without naming a
parameter, then group the rows by `parameter_code` and
`unit_of_measure`. Confirm two groups with different units and, at
most long-record gauges, different first years. Then check for at
least one water year in which the stage peak and the discharge peak
carry different dates.

[^api]: the peaks collection and its documentation, probed live
[^measurement]: the row-count and vocabulary measurement record
