---
type: connector
title: "USGS stream gauges: the Water Data API (observations server and dataretrieval)"
description: "The gauge of record through usgs_instantaneous and usgs_daily and through dataretrieval's waterdata module, both on api.waterdata.usgs.gov: cursor paging with no server-side total, an optional key as X-Api-Key, a continuous collection one rolling year deep, no retry on 429; the units are the trap (cubic feet per second and feet, never SI) and site identifiers are strings with an agency prefix and leading zeros. The legacy Water Services host closes in a window from 2026-11 to 2027-02."
tags: [connector, usgs, nwis, streamflow, gauge, mcp, observations, waterdata]
verified:
  - { by: human:PaulMRamirez, at: 2026-09-01T16:55:00Z }
  - { by: human:PaulMRamirez, at: 2026-09-05T00:17:00Z }
status: stable
citation:
  access_date_required: true
  authority: https://waterdata.usgs.gov/
  data: "U.S. Geological Survey, USGS Water Data for the Nation: U.S. Geological Survey National Water Information System database, accessed {access_date}"
  doi: "10.5066/F7P55KJN"
  note: "the access date is integral because much recent data is provisional and subject to revision"
generated: { by: claude-code/fable-5, at: 2026-09-01T16:30:00Z }
stale_after: 2026-11-01
sources:
  - id: waterdata-api
    resource: https://api.waterdata.usgs.gov/ogcapi/v0/
    title: "USGS Water Data API (OGC API Features), api-version 0.72.0, probed live 2026-09-05 and 2026-09-06"
  - id: waterdata-docs
    resource: https://api.waterdata.usgs.gov/docs/
    title: "USGS Water Data API documentation (collections, the key, rate limits)"
  - id: legacy-nwis
    resource: https://waterservices.usgs.gov/
    title: "USGS Water Services, the legacy host, decommission window 2026-11 through 2027-02"
  - id: dataretrieval
    resource: https://github.com/DOI-USGS/dataretrieval-python
    title: "dataretrieval 1.3.0 waterdata module (source read 2026-09-06: key handling, paging, retries)"
  - id: parity
    resource: https://github.com/open-science-pillars/marketplace/issues/65
    title: "The migration record: field map, paging and depth probes, rate-limit headers, six-window value parity (3167 of 3167 identical)"
  - id: server
    resource: https://github.com/open-science-pillars/core/blob/673ee1fc51ec44863e3ddd1d4a6aa5580829cbd0/connectors/observations_mcp.py
    title: "The observations server carrying the usgs tools (contract 0.3.0)"
---

# USGS stream gauges: the Water Data API

`usgs_instantaneous` and `usgs_daily` fetch from the USGS Water Data
API, the agency of record for United States streamflow, at
`https://api.waterdata.usgs.gov/ogcapi/v0` (an OGC API Features
service; `api-version` 0.72.0 on 2026-09-06).[^waterdata-api] The
hydrology skills reach the same API through dataretrieval's
`waterdata` module (`get_daily`, `get_continuous`,
`get_monitoring_locations`, `get_peaks`).[^dataretrieval] The
collections that matter: `daily` (statistics per day, `statistic_id`
`00003` for the mean), `continuous` (instantaneous values,
`statistic_id` `00011`), `monitoring-locations` (site names, HUCs,
datums, drainage areas: the observation rows carry none of these),
`peaks` (annual peaks with explicit partial-date fields) and
`time-series-metadata` (what a `time_series_id` means).[^waterdata-api]
Value parity with the legacy service was measured on six frozen
windows on 2026-09-06: 3167 of 3167 values identical.[^parity]

**Paging has no total.** `numberMatched` is always null and there is
no server-side count; a total is whatever the client counted. The
`limit` maximum is 50000 (larger is a 400). `sortby` is honored on
the first page only: with it, every following page is a 400, so a
client that needs a tail requests unsorted at the maximum, sorts
locally, and walks the `cursor` next links under a request budget
(the server's budget is four pages; dataretrieval walks until
`max_rows`). An unknown site is a 200 with zero
features, not an error.[^waterdata-api][^parity]

**The key is optional and named.** Requests work without a key. With
one, it travels as the `X-Api-Key` header to this host only, never in
a query string; dataretrieval reads it from the environment variable
`API_USGS_PAT`, and the observations server from the same
variable.[^dataretrieval][^server] The key appears in no request URL,
capture, receipt or response.

**Rate limit and 429 (probed 2026-09-06).** With the key every
response carries `x-ratelimit-limit: 1000` and an
`x-ratelimit-remaining` that counts down one per request, with no
reset header on a successful response; without the key no rate-limit
header is returned at all, so the two buckets are told apart by the
presence of `x-ratelimit-limit`. Neither bucket was exhausted in the
probe (151 keyed requests, more than 80 unkeyed, no 429), so the 429
body and the reset window are unrecorded; the API documentation is
the authority for the unkeyed limit.[^parity][^waterdata-docs] The
observations server does not retry a 429 (a retry spends the same
bucket); it reports the rate-limit headers it received and stops.
dataretrieval retries four times by default on 429 and 5xx, honoring
`Retry-After`; a session that must not spend the bucket turns that
off inside `dataretrieval.configure(WaterdataConfiguration(retries=0))`.[^dataretrieval][^server]

**Depth differs by collection.** `daily` reaches back to the start of
the record (site 09380000 to 1921-10-01). `continuous` is a rolling
one-year window, not an archive: on 2026-09-06 the earliest
instantaneous value served for 09380000 and 09085000 was
2025-09-06T03:45:00+00:00. Fifteen-minute data older than a year is
reachable as daily values, from a legacy capture taken before the
decommission, or from the legacy instantaneous service while it
answers.[^parity]

**Units are the trap.** Parameter 00060 is discharge in CUBIC FEET
per second (`unit_of_measure` `ft^3/s`) and 00065 is gage height in
FEET; nothing here is SI, and a silent unit assumption is how a
discharge comparison goes wrong by a factor of 35. Convert explicitly
and state units beside every number. Site identifiers arrive as
`USGS-09380000`: an agency prefix, then the site number as a string
with its leading zeros; the bare number is the suffix after the first
hyphen, and it is an identifier, never an integer. Continuous times
are ISO 8601 UTC; daily times are dates.[^waterdata-api][^parity]

**The legacy host, dated.** `waterservices.usgs.gov` (the `nwis/dv`
and `nwis/iv` services this connector used until 2026-09-06) is being
decommissioned in a window from 2026-11 through 2027-02; the
observations server and the hydrology skills no longer call it, and
dataretrieval removes its `nwis` module on or after 2027-05-06. A
capture taken from the legacy host keeps its own content hash and is
legacy evidence, comparable only with other legacy
captures.[^legacy-nwis][^dataretrieval] This concept's `stale_after`
sits at the opening of that window so the fact is re-checked when
the host actually closes.

**Composition.** Satellite discharge estimates confronted against the
gauge of record: SWOT reach series beside the station the river is
actually measured at, in one conversation.[^server]

[^waterdata-api]: the USGS Water Data API, probed live 2026-09-05 and 2026-09-06
[^waterdata-docs]: the USGS Water Data API documentation
[^legacy-nwis]: USGS Water Services, the legacy host
[^dataretrieval]: dataretrieval 1.3.0 source, read 2026-09-06
[^parity]: the migration record on open-science-pillars/marketplace issue 65
[^server]: the observations server source
