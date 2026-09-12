---
type: dataset
spheres: [hydrosphere]
title: "USGS Watershed Boundary Dataset (WBD): hydrologic units from HUC2 to HUC12"
description: "The national hydrologic-unit polygons, versioned by publication date on the staged products and by loaddate and tnmid per unit on the map service; a unit is a drainage area with one outlet or a closed basin, and its areasqkm agrees with an equal-area measure of the polygon to five figures."
tags: [wbd, huc, hydrologic-unit, watershed, usgs, nhd, hydrology]
generated: { by: claude-code/fable-5, at: 2026-09-06T18:20:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-06T19:12:06Z }
resource: https://hydro.nationalmap.gov/arcgis/rest/services/wbd/MapServer
version: "map service document version 3.3.0 (queried 2026-09-06; per-unit loaddate and tnmid are the unit-level version); National GPKG published 2026-09-02; HU2 region GPKGs published 2025-01-08"
status: stable
stale_after: 2027-03-06
sources:
  - id: wbd-service
    resource: https://hydro.nationalmap.gov/arcgis/rest/services/wbd/MapServer
    title: "Watershed Boundary Dataset map service (document version 3.3.0), layer list, fields and queries probed 2026-09-06"
  - id: wbd-national
    resource: https://prd-tnm.s3.amazonaws.com/StagedProducts/Hydrography/WBD/National/GPKG/WBD_National_GPKG.zip
    title: "WBD National GeoPackage, staged product published 2026-09-02 (5.72 GB), metadata read 2026-09-06"
  - id: wbd-hu2
    resource: https://prd-tnm.s3.amazonaws.com/StagedProducts/Hydrography/WBD/HU2/GPKG/WBD_14_HU2_GPKG.zip
    title: "WBD region 14 GeoPackage, staged product published 2025-01-08 (regions 05, 14 and 18 checked, 106 to 182 MB each), metadata read 2026-09-06"
  - id: tm11a3
    resource: https://pubs.usgs.gov/tm/11/a3/
    title: "Federal Standards and Procedures for the National Watershed Boundary Dataset (WBD), USGS Techniques and Methods 11-A3"
  - id: record
    resource: https://github.com/open-science-pillars/marketplace/issues/67
    title: "The basin-unit record: the WBD product table and the Tulare Lake verification"
---

# USGS Watershed Boundary Dataset

**Identity.** The Watershed Boundary Dataset (WBD) is the national
set of hydrologic-unit polygons that USGS and its partners maintain
under the federal standard (Techniques and Methods 11-A3): six nested
levels from region (HUC2) through subregion (4), basin (6),
subbasin (8), watershed (10) and subwatershed (12), with 14 and 16
digit units where they have been delineated. Every unit carries a
code of that many digits (a string with a leading zero in the first
region; `05140206` is a subbasin of the Ohio), a name, an area in
square kilometres and, at the watershed and subwatershed levels, the
code of the unit it drains to and a type.[^tm11a3][^wbd-service]

**A unit is a drainage area, not always a basin.** The standard
defines the units so that a watershed or subwatershed drains to a
single outlet (`hutype` S, standard) or is a closed basin
(`hutype` C) or one of the other types the standard lists; `tohuc`
names the downstream unit and reads `CLOSED BASIN` where there is
none. Units at HUC8 and above carry no `tohuc`, so the outlet of an
aggregate is answered from its member subwatersheds, which is what
the terminal-basin gotcha (`../gotchas/usgs-terminal-basin-no-outlet.md`)
turns on. A basin delineated as a union of whole units therefore
states its outlet from its members, and the two sources this plugin
uses agree where the basin is one or more whole units: subbasin
14010004 (Roaring Fork) unions to 3,767.3 km2 against a 3,767.1 km2
NLDI trace (the connector concept `../connectors/nldi-basin.md`
holds the trace side).[^tm11a3][^wbd-service][^record]

**Versioning.** The staged products are versioned by their
publication date, which is in each product's metadata title and
nowhere in the file name: on 2026-09-06 the National GeoPackage was
published 2026-09-02 (5.72 GB; the National file geodatabase 2.78
GB) while the per-region (HU2) GeoPackages were published 2025-01-08
(106 to 182 MB for regions 05, 14 and 18), so a region file lags the
national one by months and a citation names which. Each staged
product has its metadata XML beside it. On the map service every
unit carries `loaddate` (epoch milliseconds; 2024-08-16 for the
Tulare Lake Bed subbasin) and `tnmid` (a GUID, the unit's identity
across releases), and the service document reports version 3.3.0;
loaddate and tnmid are the per-unit version a query result
records.[^wbd-national][^wbd-hu2][^wbd-service]

**Access (live 2026-09-06).** The map service at
`https://hydro.nationalmap.gov/arcgis/rest/services/wbd/MapServer`
takes no credential. Layers by level: 1 HUC2, 2 HUC4, 3 HUC6, 4 HUC8,
5 HUC10, 6 HUC12, 7 HUC14, 8 HUC16. Fields: `huc<n>` (the code at
that layer), `name`, `areasqkm`, `loaddate`, `tnmid`,
`metasourceid`, with `tohuc` and `hutype` at layers 5 and 6. A query
with `outSR=4326&f=geojson` returns WGS84 GeoJSON; a name search
must be written `upper(name) LIKE '%TULARE%'` (a bare `name LIKE`
is a 400); `returnGeometry=false` lists members cheaply. Whole-region
work downloads the staged GeoPackage instead of paging the
service.[^wbd-service][^wbd-national]

**Area agrees with an equal-area measure.** The service's `areasqkm`
for the Tulare Lake Bed subbasin (18030012) is 9,808.23 km2; the
polygon measured in ESRI:102008 (North America Albers Equal Area
Conic) is 9,808.2 km2 and its 102 member subwatersheds sum to
9,808.2, so `areasqkm` is a trustworthy area for a unit and the
equal-area projection reproduces it to about one part in ten
thousand. The delineation script uses the projection so that unions
across units and NLDI traces are measured the same way.[^wbd-service][^record]

**Citation.** "U.S. Geological Survey, Watershed Boundary Dataset,
published <date of the product used>, accessed <date>", naming the
staged product or the map service with its document version; the
data are US Government work in the public domain. Where a single
unit is quoted, its code, name, loaddate and tnmid identify it
exactly.[^wbd-national][^wbd-service]

## Known issues

- [usgs-terminal-basin-no-outlet](../gotchas/usgs-terminal-basin-no-outlet.md):
  a closed basin is a valid unit with no outlet, and a tool that
  expects one will name the wrong river.
- The HU2 region products lag the national product; a unit taken
  from a region file may predate a boundary revision the national
  file carries. Name the product date.

[^tm11a3]: USGS Techniques and Methods 11-A3, the federal WBD standard
[^wbd-service]: the WBD map service, probed 2026-09-06
[^wbd-national]: the WBD National GeoPackage staged product and its metadata, read 2026-09-06
[^wbd-hu2]: the WBD region 14 GeoPackage staged product and its metadata, read 2026-09-06
[^record]: the basin-unit record on open-science-pillars/marketplace issue 67
