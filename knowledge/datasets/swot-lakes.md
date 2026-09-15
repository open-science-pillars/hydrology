---
type: dataset
spheres: [hydrosphere]
title: "SWOT lake products: the Prior Lake Database, the LakeSP single-pass files and the LakeAvg cycle average, as a water surface elevation and area series per prior lake"
description: "SWOT KaRIn lake products at PO.DAAC: LakeSP, three shapefiles per pass per continent (one record per observed water body, one record per Prior Lake Database lake including unobserved ones, and the unassigned features), each distributed as its own zipped granule in its own sub-collection, and LakeAvg, one shapefile per 21-day cycle per Pfafstetter level-2 basin with one record per prior lake. The series a reader builds is water surface elevation above the EGM2008 geoid, total water area and storage change per prior lake identifier; the Prior Lake Database itself is not a CMR collection at PO.DAAC and reaches the reader as the p_ prefixed attributes of the prior file. Version D is processed against PLD V2.01 and Version C against PLD V1.06."
tags: [swot, lakes, lakesp, lakeavg, prior-lake-database, pld, water-surface-elevation, storage-change, podaac, hydrology]
generated: { by: knowledge-seeder/claude, at: 2026-09-15T13:35:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-15T14:24:46Z, role: maintainer, source: https://github.com/open-science-pillars/hydrology/pull/66 }
resource: https://podaac.jpl.nasa.gov/dataset/SWOT_L2_HR_LakeSP_D
version: "Version D (CRID PGD0 reprocessing 2023-03-30 to 2025-04-27, PID0 forward processing from 2025-04-28; Prior Lake Database V2.01; DOI 10.5067/SWOT-LAKESP-D for LakeSP and its three sub-collections, 10.5067/SWOT-LAKEAVG-D for LakeAvg) and Version C (CRIDs PGC0, PIC0, PIC2; PLD V1.06; DOIs 10.5067/SWOT-LAKESP-2.0 and 10.5067/SWOT-LAKEAVG-2.0), CMR-verified 2026-09-15: the D LakeSP sub-collections each hold about 70,860 granules from cycle 474 pass 001 (2023-03-28) through cycle 056 pass 033 (2026-09-11), the C LakeSP family stops at cycle 032 pass 166 (2025-05-03), LakeAvg D holds 5,149 basin-cycle granules from cycle 001 (2023-07-21) through cycle 053 (2026-07-10) and LakeAvg C holds 51"
status: stable
upstream: pending
stale_after: 2027-03-15
citation:
  access_date_required: true
  authority: https://podaac.jpl.nasa.gov/
  data: "SWOT Level 2 KaRIn High Rate Lake Single Pass Vector Data Product, Version D (or Lake Cycle-Averaged Data Product, Version D), NASA PO.DAAC, accessed {access_date}, {doi}"
  doi: "10.5067/SWOT-LAKESP-D (LakeSP D and its obs, prior and unassigned sub-collections), 10.5067/SWOT-LAKEAVG-D (LakeAvg D), 10.5067/SWOT-LAKESP-2.0 and 10.5067/SWOT-LAKEAVG-2.0 (Version C)"
  note: "the family and the sub-collection (obs, prior or unassigned) are part of the citation, and the Prior Lake Database version the family was processed against is stated beside it"
sources:
  - id: podaac-lakesp
    resource: https://podaac.jpl.nasa.gov/dataset/SWOT_L2_HR_LakeSP_D
    title: "PO.DAAC collection page for SWOT_L2_HR_LakeSP_D, read 2026-09-15 with its obs, prior and unassigned sub-collection pages: the product description (three shapefiles per granule, the reference to the WGS84 ellipsoid corrected for geoid height, tides and path delays, the storage change in the PLD-oriented file), DOI 10.5067/SWOT-LAKESP-D, the page's swath width of 120 km, coverage 2022-12-16 to present"
  - id: podaac-lakeavg
    resource: https://podaac.jpl.nasa.gov/dataset/SWOT_L2_HR_LakeAvg_D
    title: "PO.DAAC collection page for SWOT_L2_HR_LakeAvg_D, read 2026-09-15: the one-sentence description (cycle average and aggregation of lake pass data within predefined hydrological basins), DOI 10.5067/SWOT-LAKEAVG-D"
  - id: cmr-lakesp
    resource: https://cmr.earthdata.nasa.gov/search/concepts/C3233944983-POCLOUD.umm_json
    title: "CMR collection records read 2026-09-15 for SWOT_L2_HR_LakeSP_D (C3233944983-POCLOUD) and its sub-collections obs (C3233942286), prior (C3233942291) and unassigned (C3233942295), and for the Version C family SWOT_L2_HR_LakeSP_2.0 (C2799438230, DOI 10.5067/SWOT-LAKESP-2.0) with obs (C2799438239), prior (C2799438247) and unassigned (C2799438254): abstracts, DOIs, the related-URL links to the PDD, ATBD and release note, and the granule counts and first and newest granules from start-date-sorted granule searches the same day, the umbrella's granule-name pattern counts per file kind, and one umbrella and one sub-collection granule record showing each granule as one .zip with sidecars"
  - id: cmr-lakeavg
    resource: https://cmr.earthdata.nasa.gov/search/concepts/C3233944980-POCLOUD.umm_json
    title: "CMR collection records read 2026-09-15 for SWOT_L2_HR_LakeAvg_D (C3233944980-POCLOUD, DOI 10.5067/SWOT-LAKEAVG-D) and SWOT_L2_HR_LakeAvg_2.0 (C2799438221-POCLOUD, DOI 10.5067/SWOT-LAKEAVG-2.0), with granule counts and first and newest granules from the granule search the same day; keyword and short-name pattern searches for a Prior Lake Database collection at POCLOUD the same day returned none"
  - id: pdd-lakesp
    resource: https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/pdd/SWOT-TN-CDM-0673-CNES_Product_Description_L2_HR_LakeSP_20250307_RevC_signed.pdf
    title: "SWOT Product Description Document, Level 2 KaRIn High Rate Lake Single Pass Vector Product (L2_HR_LakeSP), SWOT-TN-CDM-0673-CNES Revision C, 2025-03-07, linked from the PO.DAAC collection record and read in full 2026-09-15: the latency, the three shapefiles, the granule and swath geometry (approximately 128 km), the file naming, the identifiers obs_id and lake_id with their formats, the measured attributes and uncertainties, the quality indicators, the geoid and tide references, the PLD attributes and the storage change attributes"
  - id: pdd-lakeavg
    resource: https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/pdd/SWOT-TN-CDM-0676-CNES_Product_Description_L2_HR_LakeAvg_20250307_RevC_signed.pdf
    title: "SWOT Product Description Document, Level 2 KaRIn High Rate Lake Average Vector Product (L2_HR_LakeAvg), SWOT-TN-CDM-0676-CNES Revision C, 2025-03-07, linked from the PO.DAAC collection record and read 2026-09-15 in its product description, structure and qualitative description sections: the basin granule, the count of about 6 million currently referenced PLD lakes, the cycle-average rule for elevation, polygon and area, the minimum, median and maximum sets, the pass counts and the storage change"
  - id: relnote-d
    resource: https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/SWOT_VersionD_KaRIn_Products_Release_Note_20250423b.pdf
    title: "Release Note, SWOT Version D KaRIn Science Data Products, 2025-04-23, linked from the PO.DAAC collection record and read 2026-09-15: the CRIDs and their spans, the table of changes from Version C to D (the Prior Lake Database from V1.06 to V2.01, the geoid bug fix, the load tide model change, the lake processing enhancements), the hydroweb.next dataset table naming the Prior Lake Database, the height calibration refinement stated as O(5 mm) short-wavelength changes in the same table, and the lake known issues, among them the storage change issue that counts about 5.3 million lakes with storage change out of about 5.9 million PLD lakes in Version D"
  - id: river-lake
    resource: ./swot-river-lake.md
    title: "This bundle's SWOT River and Lake Single-Pass concept: the HR product inventory with ShortNames and concept ids, the version families, the granule naming and the zipped-shapefile access"
  - id: fixture
    resource: ../../verification/fixtures/swot/lakesp_tulare_2023.json
    title: "This plugin's frozen LakeSP observation series over the Tulare Lake bed, July to November 2023, Version D, retrieved 2026-09-07: seventeen granules that observed the four prior lakes on the valley floor, with the lake identifiers each row carries"
  - id: identity-gotcha
    resource: ../gotchas/swot-lake-identity-across-passes.md
    title: "This bundle's lake identity gotcha: the prior lake identifier in the prior file is the key of a series, and the observed file's identifier is a list when lakes merge"
  - id: datum-gotcha
    resource: ../gotchas/swot-lake-elevation-datum.md
    title: "This bundle's lake elevation datum gotcha: the geoid, the tide system, the Version C geoid error and the prior reference elevation"
  - id: gauge-datum
    resource: ../gotchas/swot-gauge-datum-mismatch.md
    title: "This bundle's satellite-to-gauge datum gotcha: a lake elevation against a gauge on a national datum"
---

# SWOT lake products

**Identity.** The Ka-band Radar Interferometer (KaRIn) high-rate
stream yields two lake products at PO.DAAC. `SWOT_L2_HR_LakeSP` is
the single-pass product: geolocated water surface elevation, total
water area and quality indicators for every observed lake and
unclassified water body in one continental pass, with polygons drawn
from the PIXCVec pixel cloud, distributed as three shapefile sets per
granule.[^podaac-lakesp][^cmr-lakesp] `SWOT_L2_HR_LakeAvg` is the
cycle average: one shapefile per 21-day science-orbit cycle per
Pfafstetter level-2 basin, one record per prior
lake.[^podaac-lakeavg][^pdd-lakeavg] Both rest on the Prior Lake
Database (PLD), the catalogue against which observed water is
identified, about 5.9 million lakes in the Version D products by the
release note's count and about 6 million currently referenced lakes
by the LakeAvg document's; the
PLD is not itself a CMR collection at PO.DAAC on the verification
date (keyword and short-name searches return none), CNES serves it
on hydroweb.next under the dataset id `SWOT_PRIOR_LAKE_DATABASE`,
and its content reaches a reader of these products as the `p_`
prefixed attributes of the prior file.[^cmr-lakeavg][^relnote-d][^pdd-lakesp]
The river and lake inventory concept beside this one records the
ShortNames, concept ids and version families of every HR product and
the zipped-shapefile reader; the facts here are the ones specific to
the lake series.[^river-lake]

## The three files of a LakeSP granule

A pass over one continent is one granule per file kind. The product
description document gives the full swath as approximately 128 km
across track, with performance requirements holding from 10 to 60 km
from nadir on each side and observations over the central 20 km
possibly missing, degraded or flagged; the PO.DAAC collection page
states the swath width as 120 km, the two documents differing on the
figure.[^pdd-lakesp][^podaac-lakesp] The three files are:

- **Obs**, the observation-oriented lake file: one record per
  observed water body above one hectare that intersects at least one
  PLD lake. One observed lake may correspond to several PLD lakes,
  because the imagery the PLD was built from saw a lake in one
  season and SWOT sees it drier or more flooded.[^pdd-lakesp]
- **Prior**, the PLD-oriented lake file: one record per PLD lake
  covered by the granule, including PLD lakes the pass did not
  observe, whose attributes are fill values and whose shape is empty.
  Where an observed lake spans several PLD lakes its polygon is split
  between them by distance to the PLD polygons. Storage change lives
  only in this file.[^pdd-lakesp]
- **Unassigned**, observation-oriented: detected water identified
  neither as a PLD lake nor as a river reach in the prior river
  database, which may be lakes absent from the PLD, river portions
  absent from the river database, wetlands or bright land such as
  layover, urban areas and roads. It carries no lake identifier, no
  ice flags and no PLD attributes.[^pdd-lakesp]

Lakes connected to the river topology (identifier type 3) appear in
both LakeSP and RiverSP; the obs and prior files are largely
redundant and exist to serve different reading patterns.[^pdd-lakesp]
Records in the obs and unassigned files are in processing order and
not geographically or time ordered; the prior file is ordered by
increasing lake identifier.[^pdd-lakesp] Polygons are the concave
hull of the height-constrained pixel cloud with posting of order 20 m
on average; each record's time is the average time tag of the pixels
contributing to it.[^pdd-lakesp] Latency is at most 45 days from
collection, and the document states that versions may be regenerated
with refined inputs such as an updated PLD.[^pdd-lakesp]

## Variants and holdings (CMR, 2026-09-15)

Every lake collection exists in the two version families the HR
products share, `*_2.0` (Version C) and `*_D` (Version D).[^river-lake][^cmr-lakesp]

| Product | Version C (concept id, granules) | Version D (concept id, granules) |
|---|---|---|
| LakeSP umbrella | `SWOT_L2_HR_LakeSP_2.0` (C2799438230) | `SWOT_L2_HR_LakeSP_D` (C3233944983) |
| LakeSP obs | `SWOT_L2_HR_LakeSP_obs_2.0` (C2799438239, 30,477) | `SWOT_L2_HR_LakeSP_obs_D` (C3233942286, 70,868) |
| LakeSP prior | `SWOT_L2_HR_LakeSP_prior_2.0` (C2799438247, 30,476) | `SWOT_L2_HR_LakeSP_prior_D` (C3233942291, 70,856) |
| LakeSP unassigned | `SWOT_L2_HR_LakeSP_unassigned_2.0` (C2799438254, 30,381) | `SWOT_L2_HR_LakeSP_unassigned_D` (C3233942295, 70,859) |
| LakeAvg | `SWOT_L2_HR_LakeAvg_2.0` (C2799438221, 51) | `SWOT_L2_HR_LakeAvg_D` (C3233944980, 5,149) |

Every granule is one zipped shapefile set (one .zip with its
metadata sidecars), and the umbrella collections list the obs, prior
and unassigned granules of a pass side by side, so a plan names the
sub-collection; the umbrella's granule count does not equal the sum
of its three sub-collections on the day, which is why the counts
above are the sub-collections' own.[^cmr-lakesp] The D
sub-collections run from cycle 474 pass 001 over Europe, whose first
granule CMR dates 2023-03-28 (CRID PGD0, the cal/val orbit) where the
release note places the PGD0 span from 2023-03-30, through cycle 056
pass 033 on 2026-09-11 (CRID PID0, forward processing); the C
sub-collections run from cycle 001 pass 148 (2023-07-26) to cycle 032
pass 166 (2025-05-03) and stop there.[^cmr-lakesp][^relnote-d] LakeAvg D holds basin-cycle
granules from cycle 001 (2023-07-21) through cycle 053 (2026-07-10),
and LakeAvg C holds 51 granules on the day, so the cycle-averaged
series is in practice a Version D product.[^cmr-lakesp][^cmr-lakeavg]
The release note places PGD0 over 2023-03-30 to 2025-04-27 and PID0
from 2025-04-28 onward, advises PGD0 where both exist for a date, and
lists the changes from C to D that touch lakes: the PLD from V1.06 to
V2.01 (adding lake catchment areas and reference heights), improved
pixel selection with a new bitwise quality flag, a geoid bug fix, and
the load tide model from FES2014 to FES2022b.[^relnote-d] A plan that
crosses 2025-05-03 or the cal/val phase resolves to the D family;
inside the shared span it names the family, since the PLD version and
the geoid differ between them.[^relnote-d][^datum-gotcha]

**Naming.** `SWOT_L2_HR_LakeSP_<Obs|Prior|Unassigned>_<cycle>_<pass>_<continent>_<start>_<end>_<crid>_<counter>`
for the single-pass files and
`SWOT_L2_HR_LakeAvg_<cycle>_<continent>_<basin>_<start>_<end>_<crid>_<counter>`
for the cycle average, where the basin is the continent code followed
by the top-level Pfafstetter basin number.[^pdd-lakesp][^pdd-lakeavg]
Shapefile attribute names are limited to ten characters, which is why
many are abbreviated and differ from the netCDF SWOT products.[^pdd-lakesp]

## Identifiers

Two identifiers carry the link between an observation and the
catalogue.[^pdd-lakesp]

- `obs_id`, thirteen characters `CBBTTTSNNNNNN`: continent code,
  basin code, PIXC tile number within the pass, swath side (L or R)
  and a lake counter within the tile. It is unique to a detected
  water feature within one cycle and pass, so it does not persist
  from pass to pass.
- `lake_id`, ten characters `CBBNNNNNNT`: continent code, basin
  code, lake counter within the basin and water body type, with type
  2 a disconnected lake and type 3 a lake connected to the river
  network. In the obs file it lists every PLD lake the observed lake
  intersects, semicolon separated and ordered by decreasing overlap
  area, with `overlap` giving each PLD lake's integer percentage of
  the observed lake and `n_overlap` the count. In the prior file it
  is the single key of the record, and there `obs_id` is the list of
  observed lakes intersecting the PLD lake, with `overlap` computed
  the other way round, as the fraction of the PLD lake.
- `reach_id` lists the connected-lake reaches of the river database
  where the lake is type 3.

Continent codes are 1 Africa (AF), 2 Europe and Middle East (EU), 3
Siberia (SI), 4 Central and South-East Asia (AS), 5 Australia and
Oceania (AU), 6 South America (SA), 7 North America and Caribbean
(NA), 8 North American Arctic (AR) and 9 Greenland (GR), the
HydroBASINS delineation.[^pdd-lakesp] The PLD attributes in the obs
file (`lake_name`, the name or names from OpenStreetMap, IGN
Carthage, GLWD or vMap0, and `p_res_id`, the GRanD reservoir
identifier) are populated, per the document's PLD information
section, from the PLD lake with the largest overlap when several are
listed; the attribute table and the string-attribute note in the same
document define `lake_name` as itself a semicolon-separated list of
the different names given to the lake, and this bundle's gauge datum
gotcha observed features of two prior lakes around Lake Powell whose
`lake_name` named the reservoir in both, so the field separates
neither prior lakes nor names.[^pdd-lakesp][^gauge-datum] The identity gotcha beside this concept holds
the measured consequence for a series.[^identity-gotcha]

## The series

**Elevation.** `wse` is the uncertainty-weighted average water
surface elevation of the feature relative to the EGM2008 geoid, after
media delays and the crossover calibration, and after the solid Earth,
load and pole tides are removed: wse = H minus geoid_hght minus
solid_tide minus load_tidef minus pole_tide, where H is the height
above the reference ellipsoid of the .prj file. `geoid_hght` is
carried as a basic attribute so the elevation can be converted to
another representation; the geoid includes the zero-frequency
permanent tide (the mean tide system). `wse_std` is the standard
deviation of the pixel elevations after the same
removals.[^pdd-lakesp] The datum gotcha beside this concept records
what follows for a series, and the gauge datum gotcha what follows
for a comparison with a gauge.[^datum-gotcha][^gauge-datum]

**Area.** `area_total` is the estimated water surface, the sum of
`area_detct` (the water SWOT detected, including water near land)
and dark water, the area not observed directly because of a weak
radar echo over smooth water or rain attenuation, filled in from a
prior water probability map; `area_wse` is the part over which the
height measurements contribute to `wse`, smaller than `area_total`
when pixels fail validity checks; `dark_frac` is one minus the
detected fraction. Areas are in square kilometers and volumes in
cubic kilometers.[^pdd-lakesp]

**Storage change (prior file only).** Four estimates and their
uncertainties: `ds1_l` and `ds1_q` by the direct approach against the
PLD reference elevation and area (`p_ref_wse`, `p_ref_area`) under a
linear (trapezoid) or quadratic (truncated pyramid) bathymetry, and
`ds2_l` and `ds2_q` by the incremental approach along a curve fitted
to observed elevation and area pairs held in the PLD; all four are
translated by `p_ds_t0` to read zero at `p_date_t0`, the first valid
measurement, which is not necessarily the date of the reference
state. Storage is not computed when the PLD lake is partially
observed, and a change between two passes is the difference of the
two passes' values.[^pdd-lakesp] `p_lon` and `p_lat` are the PLD
reference point, the point deepest inside the polygon, and
`p_storage` is a maximum storage value the document says is filled
after one year of mission.[^pdd-lakesp]

**Cycle average (LakeAvg).** For each PLD lake in a basin,
`wse_avg` is the plain average of every valid elevation in the cycle,
full and partial observations alike, with `t_avg` the average of
their times; the polygon and `area_avg` are those of the full
observation whose elevation is closest to `wse_avg` when the lake was
fully observed at least once, the overlap of the input polygons when
it was only partially observed, and empty or fill when it was not
observed. Three further sets carry the time, elevation, area and
storage change at the minimum, median and maximum elevation of the
cycle (`_hmin`, `_hmed`, `_hmax`), and `npass`, `npass_full`,
`pass_full`, `npass_part` and `pass_part` record which passes
contributed. The cycle-average storage change is computed from
`wse_avg` and `area_avg` and is not the average of the single-pass
values. Most lakes are observed no more than five times per cycle,
lakes above 70 degrees up to 35 times, and lakes in the nadir gap
never; a basin granule holds from about 200 (Australia basin 55) to
about 860,000 (North America basin 72) lakes. The product is
generated only for the science orbit, never for the one-day cal/val
orbit.[^pdd-lakeavg]

**Quality.** `quality_f` is 0 good, 1 suspect, 2 degraded and 3 bad
(bad values may be nonsensical); `qual_f_b`, added in the Revision C
document, is the bitflag behind it; `partial_f` is 1 when the observed
lake touches the near or far edge of a half swath; `ice_clim_f` is a
climatological ice flag and `ice_dyn_f` an optical-imagery ice flag
that may be entirely null filled in some processing versions;
`xovr_cal_q` grades the crossover calibration 0 good, 1 suspect, 2
bad or missing.[^pdd-lakesp] Flags are categorical gates, not
quantitative uncertainty.[^river-lake]

## Access

Zipped shapefiles per pass and continent at PO.DAAC behind Earthdata
Login, with the obs, prior and unassigned files as separate
sub-collections, and one basin-cycle shapefile per LakeAvg granule;
the reader and the bounding-box search behaviour are the ones the
river and lake concept records. Over the Tulare Lake bed this plugin's
fixture script found that a bounding-box search returns every granule
whose continental swath crosses the box, and that opening each
granule and filtering by geometry is what separates the passes that
observed the lakes from the ones that did not: seventeen granules
held the four valley-floor prior lakes between July and November
2023.[^river-lake][^fixture]

## Uncertainty

- `wse_u` is the total (random plus systematic) one-sigma
  uncertainty of the lake elevation, including the uncertainties of
  the corrections and references; `wse_r_u` is the random component
  independent between lakes, and the systematic part common to lakes
  within a granule is the square root of `wse_u` squared minus
  `wse_r_u` squared. `area_tot_u` and `area_det_u` are the area
  uncertainties, `layovr_val` an estimate of the elevation error from
  layover, and each storage change carries its own `_u`.[^pdd-lakesp]
- The storage change estimates and the PLD reference elevations
  under them are stated by the release note as not well validated;
  storage change exists for about 5.3 of the 5.9 million PLD lakes in
  Version D, the ones for which a reference elevation could be
  robustly estimated from the LakeSP series.[^relnote-d]
- Partial coverage and dark water degrade a record without emptying
  it: `partial_f` and `dark_frac` are the measures, and a partial
  observation still enters `wse_avg`.[^pdd-lakesp][^pdd-lakeavg]
- The Version C geoid carried an error of up to plus or minus 50 cm
  (typically within 10 cm) from a half-arcminute shift of the geoid
  file, largest where the geoid gradient is steep, fixed in Version
  D; the temporal height errors the release note lists for the LR
  products are of order millimetres.[^relnote-d]

## Known issues

- [swot-lake-identity-across-passes](../gotchas/swot-lake-identity-across-passes.md):
  the observed identifier does not persist and merged lakes carry a
  list.
- [swot-lake-elevation-datum](../gotchas/swot-lake-elevation-datum.md):
  the geoid, the tide system, the Version C geoid error and the
  prior reference elevation.
- [swot-gauge-datum-mismatch](../gotchas/swot-gauge-datum-mismatch.md):
  the comparison against a gauge on a national datum.
- Lakes can be missing from the obs and prior files when the PLD
  does not know them or has a wrong extent or location (they should
  then appear in the unassigned file) or when the pixel cloud did not
  detect the water (unobserved PLD lakes within the swath are present
  in the prior file as empty shapes and absent from the obs
  file).[^relnote-d]
- Water-water layover, two lakes at different altitudes overlapping
  in radar geometry, can produce a joint polygon in the prior file,
  overlapping polygons in the obs file and elevation errors; river
  portions absent from the river database can be absorbed into a
  lake polygon.[^relnote-d]
- Discharge is not the lake product's concern, but the same release
  note records that Version D discharge is absent from PGD0 and PID0
  until the reprocessing completes.[^relnote-d]

[^podaac-lakesp]: PO.DAAC collection page for SWOT_L2_HR_LakeSP_D and its sub-collections, read 2026-09-15
[^podaac-lakeavg]: PO.DAAC collection page for SWOT_L2_HR_LakeAvg_D, read 2026-09-15
[^cmr-lakesp]: CMR collection records and granule probes for the LakeSP families, 2026-09-15
[^cmr-lakeavg]: CMR collection records and granule probes for the LakeAvg families, and the PLD collection search, 2026-09-15
[^pdd-lakesp]: SWOT L2_HR_LakeSP Product Description Document, Revision C, 2025-03-07
[^pdd-lakeavg]: SWOT L2_HR_LakeAvg Product Description Document, Revision C, 2025-03-07
[^relnote-d]: Release Note, SWOT Version D KaRIn Science Data Products, 2025-04-23
[^river-lake]: this bundle's SWOT River and Lake Single-Pass concept
[^fixture]: this plugin's frozen Tulare Lake bed LakeSP series, retrieved 2026-09-07
[^identity-gotcha]: this bundle's lake identity gotcha
[^datum-gotcha]: this bundle's lake elevation datum gotcha
[^gauge-datum]: this bundle's satellite-to-gauge datum gotcha
