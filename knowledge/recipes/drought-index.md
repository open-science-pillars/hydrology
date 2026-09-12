---
type: recipe
spheres: [hydrosphere]
title: "Streamflow drought index: day-of-year percentiles at a reference gauge"
description: "USDM-style flow percentiles against a fixed 30-year daily climatology at a near-natural gauge; anchors measured at Roaring Fork 2021 (drought) and 2023 (wet)."
tags: [drought, streamflow, percentiles, usdm, reference-gauge]
generated: { by: knowledge-seeder/claude, at: 2026-07-05T00:00:00Z }
inputs: "NWIS daily discharge (00060) at a near-natural gauge; a fixed 30-year climatology window (1991-2020 here); calendar day-of-year alignment; approved values only (approval_status Approved in the USGS Water Data API; the legacy services coded the same as A)"
expected: "Site 09085000 vs 1991-2020 climatology: 2021 median DOY percentile 13.3, fraction of days below 30th percentile 0.92, below 10th 0.28; 2023 median 33.3, below 30th 0.39, below 10th 0.05 (measured 2026-07-05 on the legacy services, re-measured identical 2026-09-06 on the Water Data API fixtures)"
expected_uncertainty: "Percentile-method and window sensitivity of a few points (median +/- ~3 percentile points across interpolation choices and climatology end-year +/- 2); the 2021-vs-2023 separation (median gap ~20 points) is robust far beyond that"
trainings:
  - https://droughtmonitor.unl.edu/About/AbouttheData/DroughtClassification.aspx
status: stable
verified:
  - { by: human:PaulMRamirez, at: 2026-07-05T00:00:00Z }
  - { by: human:PaulMRamirez, at: 2026-09-06T17:46:51Z }
stale_after: 2027-01-04
---

# Streamflow drought index: day-of-year percentiles at a reference gauge

**Method.** At a NEAR-NATURAL gauge (the regulated-gauge gotcha is
binding: [nwis-regulated-gauge](../gotchas/nwis-regulated-gauge.md)):
build the day-of-year discharge climatology over a fixed 30-year
window (approved values only: rows whose `approval_status` is
`Approved`, the gate being approval, not the qualifier list); for each
day of the target year, the
index is the fraction of climatology days (same DOY) below that day's
flow, in percent. Summaries: the median percentile and the fraction
of days below the 30th and 10th percentiles (USDM-style class
thresholds, see trainings link).

**Anchors (measured 2026-07-05, site 09085000, Roaring Fork River at
Glenwood Springs, 1991-2020 climatology; re-measured 2026-09-06 on
fixtures refetched from the Water Data API, identical to the stated
precision).** The expected values above
capture the validation contrast: 2021, a documented severe drought
year in the upper Colorado basin, against 2023, a top-tier snowpack
year. A correct implementation reproduces both years within the
expected-uncertainty band; the ~20-point median separation is the
physics check.

**Provenance.** Cached fixtures (both years plus climatology) in
verification/fixtures/, refetched 2026-09-06 through dataretrieval's
waterdata module by the fetch script beside them; the
drought_analysis golden asserts these anchors. Qualifier note: the
fixture years are fully approved, with 8 days in 2021 and 20 in 2023 carrying
the `ESTIMATED` qualifier on an approved row (the legacy services
showed these as "A, e"); they are retained and counted, since
approval is the gate and the qualifier is disclosure
([nwis-provisional-data](../gotchas/nwis-provisional-data.md)).
