---
type: connector
title: "USGS groundwater levels: the Water Data API field-measurements collection (observations server)"
description: "Discrete groundwater levels through nwis_groundwater_levels on api.waterdata.usgs.gov. The API has no groundwater collection of its own: the readings taken on site visits live in field-measurements, parameter 72019 is depth to water below land surface in feet, and the elevation codes 62610, 62611, 72150 and 72229 each name the datum the elevation stands on. A continuously recorded well is a daily series through usgs_daily. The paging, the optional key and the no-retry rule on 429 are the streamflow connector's."
tags: [connector, usgs, nwis, groundwater, wells, water-level, mcp, observations, waterdata]
generated: { by: process:claude-code, at: 2026-09-15T14:00:00Z }
status: draft
citation:
  access_date_required: true
  authority: https://waterdata.usgs.gov/
  data: "U.S. Geological Survey, USGS Water Data for the Nation: U.S. Geological Survey National Water Information System database, accessed {access_date}"
  doi: "10.5066/F7P55KJN"
  note: "the access date is integral because recent readings are provisional and subject to revision; the DOI is the one the streamflow connector carries and is a USGS-registered dataset DOI that Crossref does not resolve"
stale_after: 2026-11-01
sources:
  - id: collections
    resource: https://api.waterdata.usgs.gov/ogcapi/v0/collections?f=json
    title: "The Water Data API collection list, read 2026-09-15: 37 collections and none named for groundwater; a request for a groundwater-levels collection answers 404 Collection not found"
  - id: field-measurements
    resource: https://api.waterdata.usgs.gov/ogcapi/v0/collections/field-measurements?f=json
    title: "The field-measurements collection description, queryables and schema, read 2026-09-15: readings of groundwater levels beside discharge and gage height measurements, collected at low frequency on site visits; the reading_type, vertical_datum, approval_status, qualifier, observing_procedure and field_measurements_series_id fields"
  - id: parameter-codes
    resource: https://api.waterdata.usgs.gov/ogcapi/v0/collections/parameter-codes/items/72019
    title: "The parameter code item records read 2026-09-15, five items under the parameter-codes collection, one per code: items/72019 water level depth below land surface (ft), items/62610 groundwater elevation above NGVD29 (ft), items/62611 above NAVD88 (ft), items/72150 above local mean sea level (ft), items/72229 above GUVD04 (ft); all five answer 200 with unit ft"
  - id: well-probe
    resource: "https://api.waterdata.usgs.gov/ogcapi/v0/collections/field-measurements/items?monitoring_location_id=USGS-255854080085601&parameter_code=72019&f=json"
    title: "Live probe 2026-09-15 of well USGS-255854080085601 (site name G-2074, a well in Florida, altitude 10 ft NAVD88, constructed depth 168 ft): 126 readings of 72019 from 1978-07-17 to 1994-05-04, 24 of them in 1988 and 1989, every one Approved on the Local Assumed Datum by the steel tape procedure with the Static qualifier; the same well carries 62610 and 62611 series over the same span; the daily collection answers parameter 72019 for continuously recorded wells with statistic codes 00003 and 00002"
  - id: openapi
    resource: https://api.waterdata.usgs.gov/ogcapi/v0/openapi?f=json
    title: "The API's OpenAPI description, read 2026-09-15: an API key gives higher rate limits and is obtained at the signup page; OVER_RATE_LIMIT is the 429 body"
  - id: streamflow-connector
    resource: usgs-water.md
    title: "This bundle's Water Data API streamflow connector: cursor paging with no server-side total, the key as X-Api-Key on this host only, the no-retry rule on 429 and the units trap, all of which hold here"
  - id: partitioning-recipe
    resource: ../recipes/grace-groundwater-partitioning.md
    title: "This bundle's GRACE groundwater partitioning recipe: the well of record is the confrontation term for the GRACE-derived groundwater residual"
  - id: server
    resource: https://github.com/open-science-pillars/core/blob/6d8de538894c59bbefef4c4fa7ea91fc654dd95c/connectors/observations_mcp.py
    title: "The observations server carrying nwis_groundwater_levels (contract 0.5.0); the recorded fixture is the 1988 to 1989 window of the probed well"
---

# USGS groundwater levels: the field-measurements collection

`nwis_groundwater_levels` fetches discrete groundwater levels from
the USGS Water Data API at `https://api.waterdata.usgs.gov/ogcapi/v0`,
the same OGC API Features service the streamflow tools read, from the
`field-measurements` collection.[^field-measurements] The API has no
collection named for groundwater: the collection list read on
2026-09-15 holds 37 collections and a request for `groundwater-levels`
answers 404.[^collections] The site-visit readings that the legacy
groundwater levels service used to serve are field measurements, and
the collection description says so: readings of groundwater levels
beside discharge and gage height measurements, collected at low
frequency and delivered after processing.[^field-measurements]

**One well, several numbers.** Parameter `72019` is depth to water
below land surface in FEET; `62610`, `62611`, `72150` and `72229` are
the water level as an elevation in feet above NGVD29, NAVD88, local
mean sea level and GUVD04 respectively.[^parameter-codes] A well can
carry all of them over the same span: USGS-255854080085601 serves a
`72019` series and `62610` and `62611` series from 1978-07-17 to
1994-05-04.[^well-probe] A depth and an elevation are different
numbers for one reading, and two elevations on two datums differ by
the datum offset, so every row the tool returns carries the
`vertical_datum` field the API attaches to it, the observing
procedure (steel tape on the probed well), the approval status and
the qualifier list (`Static` on the probed
well).[^field-measurements][^well-probe] Nothing here is SI.

**Continuous wells are daily values.** A well with a recorder is not
in `field-measurements`; its record is in the `daily` collection
under the same parameter code, with a statistic code (`00003` mean,
`00002` minimum seen on 2026-09-15), reachable through `usgs_daily`
with `parameter_cd` set to `72019` or an elevation code.[^well-probe]
The tool's empty-collection error says so, because an unknown well
and a continuously recorded well both answer the field-measurements
query with zero features and a 200.[^field-measurements][^server]

**Paging, key and rate limit.** Requests page by cursor with no
server-side total, the optional `API_USGS_PAT` key travels as the
`X-Api-Key` header to this host only, and a 429 is not retried; the
streamflow connector records those facts with their probe dates and
they hold for this collection, which the tool reads through the same
walker.[^streamflow-connector][^openapi][^server] Site numbers are
strings with an agency prefix (`USGS-255854080085601`, fifteen digits
for a well) and the bare number is the suffix after the first
hyphen.[^well-probe]

**Composition.** The well of record beside the GRACE-derived
groundwater residual and the streamflow gauge of record: the
groundwater partitioning recipe's confrontation term, in one
conversation.[^partitioning-recipe][^server]

[^collections]: the Water Data API collection list, read 2026-09-15
[^field-measurements]: the field-measurements collection description, queryables and schema, read 2026-09-15
[^parameter-codes]: the parameter code records, read 2026-09-15
[^well-probe]: live probe of well USGS-255854080085601, 2026-09-15
[^openapi]: the API's OpenAPI description, read 2026-09-15
[^streamflow-connector]: this bundle's Water Data API streamflow connector
[^partitioning-recipe]: this bundle's GRACE groundwater partitioning recipe
[^server]: the observations server source
