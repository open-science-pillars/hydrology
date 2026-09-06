---
type: connector
title: "USGS NLDI basin tracing: the polygon upstream of a gauge or a snapped point"
description: "The Network Linked Data Index at api.water.usgs.gov/nldi returns the upstream basin of an indexed gauge or of an NHDPlus catchment; a point must pass through hydrolocation first, splitCatchment defaults to false and simplified to true, no credential is sent, and the trace is the network-connected area, which is not the monitoring-locations drainage area on a basin with closed sub-basins."
tags: [connector, nldi, nhdplus, basin, watershed, delineation, usgs, hydrology]
generated: { by: claude-code/fable-5, at: 2026-09-06T18:20:00Z }
status: draft
citation:
  access_date_required: true
  authority: https://api.water.usgs.gov/nldi/
  data: "U.S. Geological Survey, Network Linked Data Index (NLDI), api.water.usgs.gov/nldi, basin polygon derived from the NHDPlus network, accessed {access_date}"
  note: "no DOI is published for the NLDI service or for the polygons it derives; cite the request URL and the retrieval date beside the polygon, the API version, and the NHDPlus as the network the polygon was derived from; the date is the version"
stale_after: 2027-03-06
sources:
  - id: nldi-openapi
    resource: https://api.water.usgs.gov/nldi/docs/openapi.json
    title: "Network Linked Data Index API, OpenAPI definition version 3.0.4, read 2026-09-06 (endpoint descriptions and parameter defaults quoted from it)"
  - id: nldi-probe
    resource: https://api.water.usgs.gov/nldi/linked-data
    title: "NLDI linked-data root, probed live 2026-09-06 (three gauge traces, the comid/position probes, the hydrolocation and splitCatchment outage)"
  - id: monitoring-locations
    resource: https://api.waterdata.usgs.gov/ogcapi/v0/collections/monitoring-locations
    title: "USGS Water Data API monitoring-locations collection (drainage_area, contributing_drainage_area, hydrologic_unit_code), read 2026-09-06"
  - id: wbd
    resource: https://hydro.nationalmap.gov/arcgis/rest/services/wbd/MapServer
    title: "Watershed Boundary Dataset map service, the cross-check source (subbasin 14010004 union), queried 2026-09-06"
  - id: record
    resource: https://github.com/open-science-pillars/marketplace/issues/67
    title: "The basin-unit record: the three fixture basins, the unsnapped-point offsets, the outage as observed"
---

# USGS NLDI basin tracing

The Network Linked Data Index (NLDI) at
`https://api.water.usgs.gov/nldi` (API version 3.0.4 on 2026-09-06)
answers one question this plugin needs: what is the polygon upstream
of this place on the river network. It indexes USGS gauges and other
feature sources onto the NHDPlus flowline network, identifies a
network position by NHDPlus `comid` (an integer catchment and
flowline identifier), `reachcode` and `measure` (per cent along the
reach), and navigates the network from there.[^nldi-openapi] The
`delineate-basin` skill reaches it through
`verification/fixtures/delineate_basin.py`, which writes the polygon
and its provenance; this concept holds the facts that script depends
on.

**Endpoints (quoted from the OpenAPI definition).** A gauge is
`linked-data/nwissite/USGS-<site>`, one feature carrying its `comid`,
`reachcode`, `measure` and mainstem; the basin is
`linked-data/{source}/{identifier}/basin`, described as "Compute
upstream basin polygon for a feature... Optionally splits the local
catchment at the feature's position", with two query parameters:
`splitCatchment` (default `false`) and `simplified` (default `true`).
A point has two routes. `linked-data/hydrolocation?coords=POINT(lon lat)`
is described as "Return hydrologic location nearest to coordinates...
the nearest hydrologic location on the NHD flowline network, plus the
original provided point"; it returns the snapped point with its
`comid`, `reachcode` and `measure` (the response holds two features,
the `hydrolocation` and the `point` provided, told apart by their
`type`), and that `comid` then goes to
`linked-data/comid/{comid}/basin`; the gauge coordinate of 09085000
snapped 41 m onto its indexed reach and traced the gauge's own
fixture polygon byte for byte. The nearest flowline is not always
the river the user meant, which is the unsnapped-point gotcha. The other route,
`linked-data/comid/position?coords=`, "Locates the catchment
containing the point, then returns the corresponding NHD flowline";
it snaps nothing and returns no measure, and it is the route the
unsnapped-point gotcha is about
(`../gotchas/nldi-unsnapped-point.md`).[^nldi-openapi] Coordinates
are `POINT(lon lat)` in that order, longitude first, WGS84.

**No credential.** Nothing is sent: no key, no cookie, no header
beyond a user agent. The same holds for the monitoring-locations
comparison and the Watershed Boundary Dataset service the script
also calls.[^nldi-probe]

**Timing and the outage shape.** A plain gauge trace answered in 0.4
to 2.1 s on 2026-09-06 for basins from 3,767 km2 (Roaring Fork at
Glenwood Springs, 09085000) to 522,879 km2 (Ohio at Metropolis,
03611500). The service's own backend has a 5 s read timeout: a
request that the backend cannot answer in time comes back as HTTP
502 with a JSON body `{"title": "Bad Gateway", "status": 502,
"detail": "Error executing process: ... Read timed out. (read
timeout=5)", "upstream_status": 400}`. Between 17:38 and 18:12 UTC
on 2026-09-06 every `hydrolocation` request returned that 502, while
plain traces, `comid/position` and the gauge lookups answered
normally; by 18:39 `hydrolocation` answered again. A 502 with
`upstream_status` 400 is therefore the backend, not the request; the
client waits up to 300 s and does not retry, and a point delineation
that cannot snap stops with nothing traced and nothing written,
because the only fallback is the unsnapped route. The
`splitCatchment=true` route failed throughout the same day, before,
during and after the hydrolocation outage, with a different detail
(`'NoneType' object has no attribute 'lower'`), so it is a fault of
its own and not the same outage.[^nldi-probe]

**Two parameters change the polygon.** `simplified=true` is the
default and what the fixtures hold; on 09085000 the unsimplified
polygon has 1,798 vertices to the simplified 466 and its equal-area
measure differs by 0.001% (3,767.14 against 3,767.11 km2), so
simplification is a rendering choice, not an area
choice.[^nldi-probe] `splitCatchment=true` clips the gauge's own
NHDPlus catchment at the gauge's position instead of including it
whole; the effect is the fraction of one catchment, largest in
relative terms on a small basin. Its size on the three fixture basins
is UNMEASURED: the split route failed for the whole of 2026-09-06 as
recorded above. That measurement is owed to this concept and the
fixtures were traced with the default, recorded in each file's
provenance as `splitCatchment: false`.[^nldi-probe][^record]

**What the trace measures, and the comparison rule.** The polygon is
the network-connected upstream area: the union of NHDPlus catchments
that drain through the flowline network to the feature. The
monitoring-locations `drainage_area` (in square miles; multiply by
2.589988110336 for km2) is the total topographic area USGS records
for the site, and `contributing_drainage_area` is the part USGS
considers to contribute; for the three fixture gauges
`contributing_drainage_area` is null, so no published contributing
area exists to compare against and the script says so rather than
inventing one.[^monitoring-locations] Measured in ESRI:102008 (North
America Albers Equal Area Conic) on 2026-09-06: 03611500 traces
522,879.1 km2 against 203,000 mi2 = 525,768 km2 (-0.55%); 09085000
traces 3,767.1 against 1,453 mi2 = 3,763.3 (+0.10%); 09380000
(Colorado at Lees Ferry) traces 276,443.7 against 111,800 mi2 =
289,561 (-4.53%, a 13,117 km2 shortfall). The Lees Ferry gap is the
closed sub-basins of the upper Colorado, which the network does not
connect to the river (the Great Divide Basin alone is on the order of
10,000 km2), so a trace and a drainage area differ by construction
wherever a basin holds internally drained ground; agreement within a
per cent is the expected case only where there is none. State both
numbers and the difference; never quote the trace as "the drainage
area" of the gauge.[^nldi-probe][^record]

**Cross-check against the hydrologic units.** The Watershed Boundary
Dataset subbasin 14010004 (Roaring Fork) unions to 3,767.3 km2
against the 3,767.1 km2 trace, a 0.005% difference, and its outlet
unit drains to 140100050102; where a basin is one or more whole
hydrologic units the two sources agree to that order and either is a
fair delineation, with the dataset concept
(`../datasets/usgs-wbd.md`) carrying the unit-side facts.[^wbd]

**Three fixture basins.** Recorded on marketplace issue 67 and held
under `verification/fixtures/basins/`: 03611500 (comid 1840007,
reachcode 05140206000050, measure 30.975, MultiPolygon), 09380000
(20733845, 14070006009387, 21.0042, MultiPolygon) and 09085000
(1324997, 14010004000002, 8.925, Polygon), each with the request
URLs, the retrieval date, the geometry sha256 and the comparison in
the file's `provenance` member.[^record]

**Citation.** The NLDI is a USGS service over the NHDPlus network;
cite the service and the access date as the citation block above
sets out, and cite the NHDPlus as the network the polygon was
derived from. A polygon is reproducible only from its request URL,
its parameters and its date, which is why the fixture records all
three.[^nldi-openapi]

[^nldi-openapi]: the NLDI OpenAPI definition, version 3.0.4, read 2026-09-06
[^nldi-probe]: the NLDI linked-data service, probed live 2026-09-06
[^monitoring-locations]: the Water Data API monitoring-locations collection, read 2026-09-06
[^wbd]: the Watershed Boundary Dataset map service, queried 2026-09-06
[^record]: the basin-unit record on open-science-pillars/marketplace issue 67
