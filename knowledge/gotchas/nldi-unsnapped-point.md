---
type: dataset-gotcha
title: "NLDI unsnapped point: a raw coordinate traces whichever catchment it falls in, not the river you meant"
description: "A basin traced from a point that was not snapped to the flowline network through hydrolocation is the basin of whatever NHDPlus catchment contains the point; one kilometre from the Roaring Fork gauge that is the Colorado River, three to four times the area."
tags: [nldi, hydrolocation, snap, basin, delineation, point, usgs]
generated: { by: claude-code/fable-5, at: 2026-09-06T18:20:00Z }
severity: high
dataset: ../connectors/nldi-basin.md
eval_case: nldi-unsnapped-point
sources:
  - id: nldi-openapi
    resource: https://api.water.usgs.gov/nldi/docs/openapi.json
    title: "Network Linked Data Index API, OpenAPI definition version 3.0.4, read 2026-09-06 (the hydrolocation and comid/position descriptions)"
  - id: nldi-probe
    resource: https://api.water.usgs.gov/nldi/linked-data
    title: "NLDI linked-data service, comid/position and basin probes around USGS-09085000 and USGS-03611500, 2026-09-06"
  - id: record
    resource: https://github.com/open-science-pillars/marketplace/issues/67
    title: "The basin-unit record: the unsnapped-point offset table"
status: draft
stale_after: 2027-03-06
---

# NLDI unsnapped point: a raw coordinate traces whichever catchment it falls in

**Mechanism.** The NLDI offers two ways to turn a coordinate into a
network position. `hydrolocation` returns "the nearest hydrologic
location on the NHD flowline network": the point snapped onto a
flowline, with its `comid`, `reachcode` and `measure`, so the basin
traced from it is the basin upstream of that place on that river.
`comid/position` "locates the catchment containing the point, then
returns the corresponding NHD flowline": no snap, no measure, just
the catchment the point is standing in. Every NHDPlus catchment
belongs to one flowline, and near a confluence the catchments of
the tributary and of the main stem interleave at the scale of a few
hundred metres, so a coordinate that is off the tributary's line by
a small amount falls into a main-stem catchment and traces the main
stem's basin.[^nldi-openapi][^nldi-probe]

**Measured (2026-09-06).** Around the Roaring Fork at Glenwood
Springs gauge (USGS-09085000, itself indexed to comid 1324997,
basin 3,767 km2), `comid/position` for the gauge coordinate and for
a point 1 km south gives comid 1324997 and 3,767 km2; 1 km east
gives comid 1235819, the Colorado above the confluence, 11,767 km2;
1 km north or west gives comid 3175612, the Colorado below the
confluence, 15,539 km2. The Roaring Fork drains into the Colorado at
Glenwood Springs, so three of the five nearby points answer for the
wrong river, and the wrong answer is three to four times the right
one with nothing in the response to say so. At the Ohio at
Metropolis gauge (USGS-03611500) the nearest catchment is comid
1840025 rather than the indexed 1840007 and its basin is 16 km2
short of the gauge's, a small error on 522,879 km2 but still not
the gauge's basin.[^nldi-probe][^record]

**Wrong-result mode.** The user gives a coordinate they read off a
map for a gauge, a bridge or a sampling site on a tributary; the
tool traces from the containing catchment; the area, the mean flow
per unit area and every downstream comparison are those of the main
stem. Nothing fails: the polygon is real, the request succeeded,
and the number is wrong by a factor that depends on how far the
point sits from the tributary's line.

**Avoidance.** A point goes through `hydrolocation` first and the
trace starts from the snapped `comid`; the response's `measure` and
the snapped coordinates are stated beside the polygon so the user
can see where the point landed and on which reach. When
`hydrolocation` cannot answer (the connector concept records the
outage shape, a 502 whose `upstream_status` is 400), the
delineation stops and says so; it does not fall back to
`comid/position`, because the fallback is exactly this error. A
gauge is delineated by its site number, which the NLDI has already
indexed, never by its coordinate. Where a basin can be named as
whole hydrologic units, the union of those units needs no snap at
all.[^nldi-openapi][^nldi-probe]

**Evidence.** Offsets of 1 km in four directions from the Roaring
Fork gauge, and the nearest-catchment result at Metropolis, run
against the live service on 2026-09-06 and recorded on the
basin-unit record.[^record]

[^nldi-openapi]: the NLDI OpenAPI definition, version 3.0.4, read 2026-09-06
[^nldi-probe]: the NLDI linked-data service, probed 2026-09-06
[^record]: the basin-unit record on open-science-pillars/marketplace issue 67
