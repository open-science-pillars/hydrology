---
type: dataset
title: "USGS NWIS streamflow (daily and instantaneous values)"
description: "Gauge discharge and stage from the National Water Information System; every value carries an approval qualifier, and discharge rides a revisable rating curve."
tags: [nwis, usgs, streamflow, discharge, gauges, hydrology]
timestamp: 2026-07-05
resource: https://waterservices.usgs.gov/
version: "NWIS daily/instantaneous services via dataretrieval 1.2.0 (access verified 2026-07-05); the legacy nwis functions are deprecated for removal on/after 2027-05-06 in favor of the waterdata API"
status: verified
verified: 2026-07-05
verified_by: Paul Ramirez (steward pro tem)
---

# USGS NWIS streamflow

**Identity.** The USGS National Water Information System: discharge
(parameter 00060, cfs), gage height (00065, ft), and hundreds of other
parameters at ~10,000+ active gauges; daily values (dv) and 15-minute
instantaneous values (iv). Site identifiers are 8-15 digit STRINGS
with significant leading zeros (site 09380000, Colorado River at Lees
Ferry, is the live-verified example).

**Structure (live-verified 2026-07-05 via dataretrieval).** dv frames
carry the value column (e.g. `00060_Mean`) and its qualifier column
(`00060_Mean_cd`): A approved, P provisional, with modifiers (e
estimated, Ice). A recent window (2026-06) returned 100% P; calendar
2023 returned 100% A on the same site.

## Uncertainty

- **Discharge is derived, not measured:** stage passes through a
  site-specific rating curve maintained from manual measurements.
  USGS characterizes good daily discharge records as typically within
  about 10% (site-and-regime dependent; no per-value error bars ship
  with dv data). Extremes sit on the extrapolated end of ratings and
  carry the largest, least-quantified uncertainty.
- **Approved does not mean frozen:** rating revisions re-compute
  historical discharge; analyses citing NWIS record the retrieval
  date.
- Qualifier flags are categorical gates, not quantitative uncertainty
  (core QC rule).

## Known issues

- [nwis-provisional-data](../gotchas/nwis-provisional-data.md).
- API migration: legacy `nwis.*` functions in dataretrieval are
  deprecated (removal on/after 2027-05-06); the waterdata API
  (`waterdata.get_daily()`) is the target (observed in library
  warnings 2026-07-05).
