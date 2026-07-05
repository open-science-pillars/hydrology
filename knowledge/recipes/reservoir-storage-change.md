---
type: recipe
title: "Reservoir level change from gauge elevation: Lake Powell 2023"
description: "Annual reservoir elevation change from NWIS daily lake-surface elevation (62614); anchor is Lake Powell's documented 2023 refill, +44.2 ft."
tags: [reservoir, lake-powell, elevation, storage, water-resources]
timestamp: 2026-07-05
inputs: "NWIS daily lake/reservoir elevation (parameter 62614) at the reservoir gauge; approved values; a stated datum"
expected: "Site 09379900 (Lake Powell at Glen Canyon Dam), calendar 2023: start 3524.40 ft, minimum 3519.50 ft (April 13-14), maximum 3584.30 ft (July), end 3568.60 ft; annual (Dec 31 minus Jan 1) change +44.20 ft (measured 2026-07-05, all values qualifier A)"
expected_uncertainty: "Daily-mean elevation is reported to 0.01-0.1 ft and the measurement itself is sub-0.1 ft; the meaningful uncertainty is definitional: annual change varies by several feet depending on endpoint convention (calendar vs water year, single-day vs monthly-mean endpoints); the convention is stated with every number"
trainings:
  - https://appliedsciences.nasa.gov/join-mission/training/english/mapping-and-monitoring-lakes-and-reservoirs-satellite-observations
status: verified
verified: 2026-07-05
verified_by: OSP steward review
---

# Reservoir level change from gauge elevation: Lake Powell 2023

**Method.** Daily lake-surface elevation (NWIS parameter 62614) at
the reservoir's gauge; annual change is the difference between the
last and first daily values of the stated period, with minimum and
maximum reported alongside (a reservoir year is a trajectory, not two
endpoints). Storage-volume conversion requires the operator's
area-capacity table and is a separate, stated step; elevation is the
directly measured quantity.

**Anchor (measured 2026-07-05).** Lake Powell's 2023 refill, the
largest snowpack-driven recovery of the millennium drought era: the
expected values above. The mid-April minimum against the July maximum
(+64.8 ft within the year) is the sanity check that catches
endpoint-only implementations.

**Context that binds.** The gauge sits at Glen Canyon Dam: this is an
OPERATIONS quantity by nature (the regulated-gauge gotcha explains
why the same water's absence made downstream Lees Ferry percentiles
look identical in 2021 and 2023). The ARSET training linked above
covers the satellite complement (altimetry and SWOT lake products)
for reservoirs without gauges; the swot-river-lake concept records
those products.

**Provenance.** Cached fixture powell_62614_2023_dv.parquet in
verification/fixtures/ with the fetch script; the reservoir_storage
golden asserts these anchors.
