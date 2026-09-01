---
type: connector
title: "PO.DAAC Hydrocron SWOT river series (observations server)"
description: "SWOT water surface elevation and width per river reach or node through hydrocron_timeseries; elevations sit on the EGM2008 geoid, fill values are large negatives, and reach and node identifiers come from SWORD."
tags: [connector, hydrocron, swot, rivers, podaac, mcp, observations]
status: draft
generated: { by: claude-code/fable-5, at: 2026-09-01T16:30:00Z }
stale_after: 2026-12-31
sources:
  - id: hydrocron
    resource: https://podaac.github.io/hydrocron/
    title: "Hydrocron documentation (features, fields, SWORD identifiers)"
  - id: live-probe
    resource: "hydrocron_timeseries probe, 2026-09-01: reach 63470800171, five passes of wse and width in 674 ms, anonymous"
    title: "Live verification of the timeseries path"
  - id: server
    resource: https://github.com/open-science-pillars/core/blob/main/connectors/observations_mcp.py
    title: "The observations server carrying the hydrocron tool"
---

# PO.DAAC Hydrocron SWOT river series

`hydrocron_timeseries` fetches SWOT river time series (water surface
elevation, width, and companion fields) per reach or node from
PO.DAAC's Hydrocron API, anonymous over HTTPS.[^hydrocron] Verified
live 2026-09-01: five passes for a Reach in under a second.[^live-probe]

**Three facts before science.** Elevations are on the EGM2008 geoid,
not the ellipsoid; mixing vertical references corrupts every
comparison. Fill values are large negatives and must be filtered, not
averaged. Reach and node identifiers come from the SWORD database;
a reach series and a node series answer different questions about
the same river.[^hydrocron]

**Provenance note.** This wraps PO.DAAC's public API, not their code;
the tool group is deliberately separable so the archive can take the
surface upstream if they choose to own it.[^server]

**Composition.** The satellite river series beside the USGS gauge of
record and GRACE storage: three agencies, one question about a
river's water.

[^hydrocron]: Hydrocron documentation
[^live-probe]: live probe 2026-09-01
[^server]: the observations server source
