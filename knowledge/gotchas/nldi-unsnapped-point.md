---
type: dataset-gotcha
spheres: [hydrosphere]
title: "NLDI unsnapped point: a coordinate answers for the nearest flowline, not the river you meant"
description: "A basin traced from a coordinate is the basin of whichever NHDPlus flowline is nearest (hydrolocation) or whichever catchment contains the point (comid/position); one kilometre from the Roaring Fork gauge both routes answer for the Colorado River, three times the area, and only the snapping route returns the distance, reach and measure that let the mismatch be seen."
tags: [nldi, hydrolocation, snap, basin, delineation, point, usgs]
generated: { by: claude-code/fable-5, at: 2026-09-06T18:20:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-06T19:12:06Z }
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
status: stable
stale_after: 2027-03-06
---

# NLDI unsnapped point: a coordinate answers for the nearest flowline

**Mechanism.** The NLDI offers two ways to turn a coordinate into a
network position, and neither knows which river the user meant.
`hydrolocation` returns "the nearest hydrologic location on the NHD
flowline network": the point snapped onto the nearest flowline, with
its `comid`, `reachcode` and `measure` and the snapped coordinates,
from which the snap distance follows. `comid/position` "locates the
catchment containing the point, then returns the corresponding NHD
flowline": no snap, no measure, no distance, just the catchment the
point is standing in. Near a confluence the tributary's and the main
stem's flowlines and catchments interleave at the scale of a few
hundred metres, so a coordinate a small way off the tributary is
nearer to, or inside the catchment of, the main stem, and the basin
traced from it is the main stem's. The snapping route is still the
one to use, because its answer carries the evidence: the distance
the point moved, the reach it landed on, and the reach's subbasin
(the first eight digits of the `reachcode`), which is what shows
that a point described as "on the Roaring Fork" (subbasin 14010004)
landed on the Colorado (14010001 above the confluence, 14010005
below).[^nldi-openapi][^nldi-probe]

**Measured (2026-09-06).** Around the Roaring Fork at Glenwood
Springs gauge (USGS-09085000, indexed to comid 1324997 on reach
14010004000002, basin 3,767 km2):

| Point | hydrolocation: comid, reach, snap distance | comid/position | Basin |
|---|---|---|---|
| the gauge coordinate | 1324997, 14010004000002, 41 m | 1324997 | 3,767 km2 |
| 1 km south | 1324997, 14010004000002, 9 m | 1324997 | 3,767 km2 |
| 1 km east | 1235819, 14010001002638, 385 m | 1235819 | 11,767 km2 (Colorado above the confluence) |
| 1 km north | 3175612, 14010005001940, 629 m | 3175612 | 15,539 km2 (Colorado below) |
| 1 km west | 3175612, 14010005001940, 831 m | 3175612 | 15,539 km2 (Colorado below) |

Three of the five nearby points answer for the wrong river by either
route, and the wrong answer is three to four times the right one;
the point traced from the gauge coordinate through the snapping
route reproduces the gauge's own fixture polygon byte for byte
(geometry sha256 9d02af22607d). At the Ohio at Metropolis gauge
(USGS-03611500) the containing catchment is comid 1840025 rather
than the indexed 1840007 and its basin is 16 km2 short of the
gauge's.[^nldi-probe][^record]

The split-catchment process behind `splitCatchment=true`, run
directly on the raw gauge coordinate (41 m off the flowline), is the
same lesson in a different route: it returned the local catchment
1324997 (14.13 km2) with a split portion of 0.006 km2 and no basin,
the few raster cells draining to that bank point rather than the
Roaring Fork above the gauge (19:09 UTC, 2026-09-06).

**Wrong-result mode.** The user gives a coordinate they read off a
map for a gauge, a bridge or a sampling site on a tributary; the
tool traces from the nearest flowline or the containing catchment;
the area, the yield per unit area and every downstream comparison
are those of the main stem. Nothing fails: the polygon is real, the
request succeeded, and the number is wrong by a factor that depends
on how far the point sits from the tributary's line. The
containing-catchment route gives no sign at all; the snapping route
gives a snap distance of hundreds of metres and a reach in another
subbasin, and the comparison with the gauge's published drainage
area reads +213% instead of a fraction of a per cent.

**Avoidance.** A point goes through `hydrolocation` first and the
trace starts from the snapped `comid`; the snap distance, the reach,
its subbasin and the measure are stated beside the polygon and
checked against the river the user named (or the gauge's
`hydrologic_unit_code` when a comparison gauge is given); a snap of
hundreds of metres, or a reach in a different subbasin from the one
the user described, is reported as a likely wrong river and the
polygon is not used until the user confirms or gives a better
position. When `hydrolocation` cannot answer (the connector concept
records the outage shape, a 502 whose `upstream_status` is 400), the
delineation stops and says so; it does not fall back to
`comid/position`, which carries none of the evidence. A gauge is
delineated by its site number, which the NLDI has already indexed,
never by its coordinate. Where a basin can be named as whole
hydrologic units, the union of those units needs no snap at
all.[^nldi-openapi][^nldi-probe]

**Evidence.** Offsets of 1 km in four directions from the Roaring
Fork gauge through both routes, and the nearest-catchment result at
Metropolis, run against the live service on 2026-09-06 and recorded
on the basin-unit record.[^record]

[^nldi-openapi]: the NLDI OpenAPI definition, version 3.0.4, read 2026-09-06
[^nldi-probe]: the NLDI linked-data service, probed 2026-09-06
[^record]: the basin-unit record on open-science-pillars/marketplace issue 67
