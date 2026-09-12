---
type: dataset-gotcha
spheres: [hydrosphere]
title: "Terminal basins: a closed hydrologic unit has no outlet, and a tool that expects one names the wrong river"
description: "A closed basin such as Tulare Lake is a valid WBD unit with no downstream unit and no gauge at an outlet; delineate it as the union of its units, measure it, and state that there is no outlet rather than tracing from a river it does not reach."
tags: [wbd, huc, closed-basin, terminal, endorheic, tulare, nldi, hydrology]
generated: { by: claude-code/fable-5, at: 2026-09-06T18:20:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-06T19:12:06Z }
severity: medium
dataset: ../datasets/usgs-wbd.md
sources:
  - id: wbd-service
    resource: https://hydro.nationalmap.gov/arcgis/rest/services/wbd/MapServer
    title: "Watershed Boundary Dataset map service, Tulare-Buena Vista Lakes and Tulare Lake Bed queries, 2026-09-06"
  - id: tm11a3
    resource: https://pubs.usgs.gov/tm/11/a3/
    title: "Federal Standards and Procedures for the National Watershed Boundary Dataset (WBD), USGS Techniques and Methods 11-A3"
  - id: record
    resource: https://github.com/open-science-pillars/marketplace/issues/67
    title: "The basin-unit record: the Tulare Lake verification"
status: stable
stale_after: 2027-03-06
---

# Terminal basins: a closed hydrologic unit has no outlet

**Mechanism.** The WBD standard allows a unit to be a closed basin
(`hutype` C, `tohuc` `CLOSED BASIN` at the watershed and
subwatershed levels): water that enters it leaves by evaporation,
infiltration or diversion, not by a stream to a downstream unit.
Such a basin has no outlet gauge, no NLDI feature stands at its
mouth, and a flowline that appears to leave it on a map is a canal
or a flood-relief channel. A delineation built on "find the outlet,
trace upstream" has no outlet to find; asked for one anyway, it
finds the nearest through-flowing river and returns that river's
basin.[^tm11a3][^wbd-service]

**Measured (2026-09-06).** Tulare-Buena Vista Lakes (basin 180300)
is 42,497.47 km2 by the service's `areasqkm`; its Tulare Lake Bed
subbasin (18030012, loaddate 2024-08-16, tnmid
{86AD0A19-0A69-4AFB-80B8-A5CC488E750D}) is 9,808.23 km2, is made of
102 subwatersheds summing to 9,808.2 km2, and four of them (codes
180300122401 through 180300122404, about 600 km2, under the closed
watershed 1803001224) carry `hutype` C and `tohuc` `CLOSED BASIN`.
No subwatershed in the subbasin drains to a code outside it, so the
subbasin has no outlet; the equal-area measure of the union is
9,808.2 km2 against the published 9,808.23.[^wbd-service][^record]

**Wrong-result mode.** A user asks for "the Tulare Lake basin" and
the tool, given a point on the old lake bed or on the Kings River
fan, snaps to a flowline that in fact leaves the region through the
Kings or the San Joaquin and returns the San Joaquin's basin, or a
sliver of it, with the lake bed missing. The area, the water budget
and any GRACE mascon comparison then describe a different system.

**Avoidance.** Delineate a terminal basin as the union of its
hydrologic units (the dataset concept lists the layers and the
query form), measure it in an equal-area projection, and answer the
outlet question from the member subwatersheds: closed if any carries
`hutype` C or `tohuc` `CLOSED BASIN` and no member drains to a code
outside the set. State plainly that there is no outlet and that no
gauge measures outflow, so a water budget closes on storage change
and evapotranspiration, not on discharge. The delineation script
makes this determination and records it as `no_outlet` in the
polygon's provenance.[^wbd-service][^tm11a3]

**Evidence.** The service queries and the member listing are on the
basin-unit record; the union is held as a fixture with its
provenance.[^record]

[^wbd-service]: the WBD map service, probed 2026-09-06
[^tm11a3]: USGS Techniques and Methods 11-A3, the federal WBD standard
[^record]: the basin-unit record on open-science-pillars/marketplace issue 67
