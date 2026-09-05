---
type: connector
title: "USGS NWIS stream gauges (observations server)"
description: "The gauge of record through usgs_instantaneous and usgs_daily; the units are the trap: discharge arrives in cubic feet per second and gage height in feet, never SI, and site numbers are strings with leading zeros."
tags: [connector, usgs, nwis, streamflow, gauge, mcp, observations]
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
stale_after: 2026-12-31
sources:
  - id: nwis
    resource: https://waterservices.usgs.gov/
    title: "USGS Water Services documentation (parameter codes, services)"
  - id: ogc-api
    resource: https://api.waterdata.usgs.gov/ogcapi/v0/
    title: "The successor OGC API, verified live 2026-09-01 (collections listing)"
  - id: live-probe
    resource: "usgs_instantaneous probe, 2026-09-01: Potomac at Little Falls (01646500) discharge, live values"
    title: "Live verification of the instantaneous path"
  - id: server
    resource: https://github.com/open-science-pillars/core/blob/main/connectors/observations_mcp.py
    title: "The observations server carrying the usgs tools"
---

# USGS NWIS stream gauges

`usgs_instantaneous` and `usgs_daily` fetch from USGS Water
Services, the agency of record for United States streamflow,
anonymous over HTTPS.[^nwis] Verified live 2026-09-01: Potomac at
Little Falls discharge, minutes fresh.[^live-probe] USGS is migrating
toward an OGC API, also verified answering; the legacy services this
connector uses remain the stable, documented surface.[^ogc-api]

**Units are the trap.** Parameter 00060 is discharge in CUBIC FEET
per second and 00065 is gage height in FEET; nothing here is SI, and
a silent unit assumption is how a discharge comparison goes wrong by
a factor of 35. Convert explicitly and state units beside every
number. Site numbers are strings with leading zeros; treat them as
identifiers, never integers.[^nwis]

**Composition.** Satellite discharge estimates confronted against the
gauge of record: SWOT reach series beside the station the river is
actually measured at, in one conversation.[^server]

[^nwis]: USGS Water Services documentation
[^ogc-api]: the successor OGC API, probed live
[^live-probe]: live probe 2026-09-01
[^server]: the observations server source
