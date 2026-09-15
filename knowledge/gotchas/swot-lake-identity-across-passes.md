---
type: dataset-gotcha
spheres: [hydrosphere]
title: "A SWOT lake series is keyed on the prior lake identifier in the prior file: the observed identifier is new every pass, a merged water body carries a semicolon list of prior identifiers, and an equality filter on the obs file silently drops the passes where lakes joined"
description: "In the LakeSP obs file obs_id names a detected water feature within one cycle and pass and never persists, and lake_id lists every Prior Lake Database lake the feature intersects, semicolon separated and ordered by overlap, so when neighbouring lakes coalesce the value is a list and the elevation is an average over the merged water. Measured over the Tulare Lake bed, July to November 2023, Version D: five of the seventeen observing passes carry merged identifiers, and on 2023-07-30 the single-lake record reads 53.331 m while the merged three-lake record twelve hours later reads 54.295 m. An equality filter on one identifier returns a series with silent gaps, a substring match returns another water body's average as this lake's level, and a join on lake_name pulls in neighbours; the prior file, one record per PLD lake per pass, is the key, and the PLD version differs between the C and D families."
tags: [swot, lakesp, lake_id, obs_id, prior-lake-database, pld, time-series, identity, merge, hydrology]
generated: { by: knowledge-seeder/claude, at: 2026-09-15T13:35:00Z }
severity: high
# high: nothing raises, the filtered series has the right units and a
# plausible shape, and the passes it lost or the neighbour it absorbed
# are invisible without the concept; the eval case tests avoidance.
dataset: ../datasets/swot-lakes.md
eval_case: swot-lake-identity-across-passes
status: draft
stale_after: 2027-03-15
sources:
  - id: pdd-lakesp
    resource: https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/pdd/SWOT-TN-CDM-0673-CNES_Product_Description_L2_HR_LakeSP_20250307_RevC_signed.pdf
    title: "SWOT L2_HR_LakeSP Product Description Document, Revision C, 2025-03-07, linked from the PO.DAAC collection record and read 2026-09-15: the identifiers section (obs_id unique within cycle and pass, lake_id as an overlap-ordered list, overlap and n_overlap), the observed-versus-PLD-lake note, the PLD-oriented file with one record per PLD lake and the polygon split, the PLD attributes populated from the largest-overlap lake, the partial and ice flags"
  - id: relnote-d
    resource: https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/SWOT_VersionD_KaRIn_Products_Release_Note_20250423b.pdf
    title: "Release Note, SWOT Version D KaRIn Science Data Products, 2025-04-23, read 2026-09-15: the Prior Lake Database from V1.06 in Version C to V2.01 in Version D, and the known issue on lakes missing from the obs and prior files"
  - id: fixture
    resource: ../../verification/fixtures/swot/lakesp_tulare_2023.json
    title: "This plugin's frozen LakeSP observation series over the Tulare Lake bed, Version D, July to November 2023, retrieved 2026-09-07: seventeen observing granules, the lake identifiers each row carries and the elevation statistics over them"
  - id: dataset
    resource: ../datasets/swot-lakes.md
    title: "This bundle's SWOT lake products concept: the three files, the identifiers, the series and the cycle average"
  - id: gauge-datum
    resource: ../gotchas/swot-gauge-datum-mismatch.md
    title: "This bundle's satellite-to-gauge datum gotcha, whose second trap records eleven features of two prior lakes around Lake Powell on one pass, with lake_name naming the reservoir in both"
---

# The prior lake identifier is the key of a lake series

**Mechanism.** The obs file of a LakeSP granule holds one record per
observed water body, and its two identifiers answer different
questions. `obs_id` is built from the pixel-cloud tile and a counter
within the tile and is unique to a detected feature within one cycle
and pass; the next pass over the same water assigns a new one.
`lake_id` is the link to the Prior Lake Database (PLD), and when the
observed water intersects more than one PLD lake it is a list of all
of them, semicolon separated and ordered by decreasing overlap area,
with `overlap` holding each one's percentage of the observed lake and
`n_overlap` the count. The document is explicit about why this
happens: the PLD was drawn from imagery of one season, and SWOT may
see a lake drier or more flooded than the catalogue shape, so two PLD
lakes can sit inside one observed water body.[^pdd-lakesp] The
elevation and area on such a record are the averages over the merged
water, and the PLD attributes on it (`lake_name`, `p_res_id`) come
from whichever PLD lake overlaps most.[^pdd-lakesp]

The prior file is organised the other way: one record per PLD lake
covered by the granule, `lake_id` a single value, the observed
polygon split between PLD lakes by distance to their catalogue
polygons, `obs_id` the list of observed features that touched the
lake, and unobserved PLD lakes present as records with fill values
and an empty shape.[^pdd-lakesp] Storage change is computed only
there, and not when the lake is partially observed.[^pdd-lakesp]

**Measured (fixture retrieved 2026-09-07).** Over the Tulare Lake
bed, Version D, July to November 2023, seventeen granules observed
the four prior lakes on the valley floor (7740005332, 7740005342,
7740005352, 7740005572). Five of the seventeen rows carry a merged
identifier, and the merges are not the same lakes each time: on
2023-07-30 at 13:05 UTC a single feature carries 7740005332 alone at
53.331 m, and at 23:46 UTC the same day one feature carries
7740005332;7740005352;7740005342 at 54.295 m; on 2023-08-09 the list
is 7740005332;7740005572;7740005352 at 53.070 m; on 2023-08-31 one
feature carries 7740005332;7740005572 beside a separate 7740005352;
on 2023-09-21 the list is 7740005572;7740005352. The same identifier
therefore appears alone, first in a list, and second in a list within
one season, and the merged records differ from the single-lake
records by up to about a metre on the same day.[^fixture] At Lake
Powell on one pass, eleven features inside a box around the
reservoir belong to two prior lakes, three carrying the reservoir's
identifier within 0.3 m and eight belonging to an arm complex ranging
over 43 m, while `lake_name` names Lake Powell in both.[^gauge-datum]

**Wrong-result mode.** A series assembled from the obs file by
`lake_id == "7740005332"` keeps the passes where the lake stood
alone and drops every pass where it had joined its neighbours: the
result is complete-looking, has the right units, and its gaps read as
passes that missed the lake, though the water was there and was
measured. A series assembled by substring match keeps those passes
but reports the merged water body's average as the lake's level, so
the record moves by the neighbour's elevation rather than the lake's.
A series keyed on `obs_id` has one point per identifier and no
continuity at all, and a series joined on `lake_name` collects every
feature the catalogue name touches. In the other direction, a reader
who takes the obs file's record count for the number of lakes seen
counts one where the catalogue has three. Nothing errors, and the
release note's own known issue, that a lake can be missing from the
obs and prior files when the PLD does not know it or misplaces it,
gives the gaps a ready explanation that is not the
cause.[^pdd-lakesp][^relnote-d]

**Correct approach.** The prior file is the series: one record per
PLD lake per pass, `lake_id` compared for equality, `partial_f` and
`quality_f` read beside `wse`, and the `obs_id` list kept as the
provenance of which observed features fed the record. A series from
the obs file is possible only with `n_overlap` read on every row and
the merged rows labelled as the merged water's average, never as the
lake's. The cycle average product is already keyed this way, one
record per PLD lake per basin per cycle.[^pdd-lakesp][^dataset] A
series that spans the C and D families names the PLD version of each
(V1.06 and V2.01), since the identifiers are defined against the
catalogue the family was processed with.[^relnote-d]

**Verification.** Over the Tulare fixture, count the rows whose
identifier field contains a semicolon (five of seventeen) and compare
the series filtered by equality on 7740005332 (three rows) with the
series of rows whose list contains it (seven rows); the difference is
the passes an equality filter loses, and the merged rows' elevations
are the ones a substring match would misattribute.[^fixture] On any
granule, open the prior file and confirm one record per `lake_id`
with `n_overlap` giving the number of observed features behind it.

[^pdd-lakesp]: SWOT L2_HR_LakeSP Product Description Document, Revision C, 2025-03-07
[^relnote-d]: Release Note, SWOT Version D KaRIn Science Data Products, 2025-04-23
[^fixture]: this plugin's frozen Tulare Lake bed LakeSP series, retrieved 2026-09-07
[^dataset]: this bundle's SWOT lake products concept
[^gauge-datum]: this bundle's satellite-to-gauge datum gotcha
