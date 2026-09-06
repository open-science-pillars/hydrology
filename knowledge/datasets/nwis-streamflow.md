---
type: dataset
title: "USGS NWIS streamflow (daily and instantaneous values)"
description: "Gauge discharge and stage from the National Water Information System, served by the USGS Water Data API; every value carries an approval status and a qualifier list, and discharge rides a revisable rating curve."
tags: [nwis, usgs, streamflow, discharge, gauges, hydrology]
generated: { by: knowledge-seeder/claude, at: 2026-07-05T00:00:00Z }
resource: https://api.waterdata.usgs.gov/ogcapi/v0/
version: "USGS Water Data API daily and continuous collections (api-version 0.72.0) via dataretrieval 1.3.0 waterdata module (access verified 2026-09-06; first verified on the legacy services via dataretrieval 1.2.0 on 2026-07-05); dataretrieval's legacy nwis module is deprecated for removal on/after 2027-05-06"
status: stable
verified:
  - { by: human:PaulMRamirez, at: 2026-07-05T00:00:00Z }
  - { by: human:PaulMRamirez, at: 2026-09-06T17:01:38Z }
stale_after: 2027-01-04
---

# USGS NWIS streamflow

**Identity.** The USGS National Water Information System: discharge
(parameter 00060, cfs), gage height (00065, ft), and hundreds of other
parameters at ~10,000+ active gauges; daily values (the `daily`
collection, one row per day and statistic) and 15-minute
instantaneous values (the `continuous` collection). Site identifiers
are 8-15 digit STRINGS with significant leading zeros, served with
an agency prefix as `monitoring_location_id` (`USGS-09380000`,
Colorado River at Lees Ferry, is the live-verified example; the bare
number is the suffix after the first hyphen). The daily record
reaches the start of the station record (09380000 to 1921); the
continuous collection serves one rolling year, as the connector
concept records.

**Structure (live-verified 2026-09-06 via dataretrieval's waterdata
module).** One row per observation with `monitoring_location_id`,
`parameter_code` (`00060`), `statistic_id` (`00003` daily mean,
`00011` continuous), `time_series_id`, `time` (a date for daily, an
ISO 8601 UTC instant for continuous), `value` (served as a string,
cast to float by the client), `unit_of_measure` (`ft^3/s` for
discharge, `ft` for stage and elevation), `approval_status`
(`Approved` or `Provisional`), `qualifier` (a list, or none; the
values seen so far are `ESTIMATED` on approved daily rows of
09085000 and `REGULATED` on peaks) and `last_modified`. Approval and
qualifier are separate columns: an `ESTIMATED` day is still
`Approved`, and a statistic that gates on approval keeps it. The
legacy services returned the same information as one code column
(`00060_Mean_cd`: A approved, P provisional, with modifiers e
estimated and Ice); calendar 2023 at 09380000 was 100% A there
(2026-07-05) and 100% `Approved` here (2026-09-06), and a trailing
window is provisional under either vocabulary.

## Uncertainty

- **Discharge is derived, not measured:** stage passes through a
  site-specific rating curve maintained from manual measurements.
  USGS characterizes good daily discharge records as typically within
  about 10% (site-and-regime dependent; no per-value error bars ship
  with dv data). Extremes sit on the extrapolated end of ratings and
  carry the largest, least-quantified uncertainty.
- **Approved does not mean frozen:** rating curves are remade after
  floods and channel shifts, so rating revisions re-compute historical
  discharge; analyses citing NWIS record the retrieval date.
- Qualifier flags are categorical gates, not quantitative uncertainty
  (core QC rule).

## Known issues

- [nwis-provisional-data](../gotchas/nwis-provisional-data.md).
- [nwis-regulated-gauge](../gotchas/nwis-regulated-gauge.md).
- Client migration: dataretrieval's legacy `nwis.*` functions are
  deprecated (removal on/after 2027-05-06, observed in library
  warnings 2026-07-05); this plugin fetches through
  `waterdata.get_daily()` and `waterdata.get_continuous()` as of
  2026-09-06. The endpoints, paging, key, depth and rate-limit facts,
  and the legacy host's decommission window, live in the connector
  concept (`../connectors/usgs-water.md`).
