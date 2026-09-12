---
type: dataset
spheres: [hydrosphere]
title: "Reservoir area-capacity tables: a survey, not a constant, and Lake Powell's is four per cent smaller than it was"
description: "The elevation-to-volume relationship a reservoir ledger depends on comes from a bathymetric survey, and a resurvey replaces it. Lake Powell's 2018 survey, the first since 1986, found full-pool capacity of 25,160,000 acre-feet at 3702.91 ft NAVD88: 4.00 per cent below the 1986 figure and 6.79 per cent below 1963. The table is published on NAVD88 with an NGVD29 column beside it, at a step of about a third of a foot, and a volume quoted without its revision is a volume from an unnamed year."
tags: [reservoir, area-capacity, lake-powell, bathymetry, sedimentation, navd88, storage, hydrology]
generated: { by: claude-code/opus-5, at: 2026-09-08T05:30:00Z }
resource: https://doi.org/10.5066/P9O3IPG3
version: "Elevation-area-capacity tables for Lake Powell, 2018; data release published 2022-03-21, read 2026-09-08"
status: draft
stale_after: 2027-03-08
citation:
  access_date_required: false
  authority: https://doi.org/10.5066/P9O3IPG3
  data: "U.S. Geological Survey, 2022, Elevation-area-capacity tables for Lake Powell, 2018: U.S. Geological Survey data release, https://doi.org/10.5066/P9O3IPG3"
  doi: "10.5066/P9O3IPG3"
  note: "the survey year is part of the citation: a later survey replaces this table rather than amending it, so a volume is quoted with the revision that produced it"
sources:
  - id: release
    resource: https://doi.org/10.5066/P9O3IPG3
    title: "The data release: Lake_Powell_2018_ElevAreaCap_calc.csv, 1,821 rows from 3120.08 to 3717.19 ft NAVD88, with both datum columns; read 2026-09-08"
  - id: report
    resource: https://pubs.usgs.gov/sir/2022/5017/sir20225017.pdf
    title: "USGS Scientific Investigations Report 2022-5017, Elevation-area-capacity relationships of Lake Powell in 2018 and estimated loss of storage capacity since 1963: the survey method and the capacity losses"
  - id: parameters
    resource: https://api.waterdata.usgs.gov/ogcapi/v0/collections/parameter-codes/items/62615
    title: "The USGS parameter code definitions, which fix the datum of a gauge's elevation series"
  - id: record
    resource: https://github.com/open-science-pillars/marketplace/issues/75
    title: "The measurement record: the conversion on this water year's endpoints and the cost of the datum mistake"
---

# A reservoir's area-capacity table is a survey result

**Identity.** For a given reservoir, a table of water surface
elevation against surface area and cumulative storage. The ledger
conversion from a gauge's elevation to a volume is a lookup in this
table, so the table is an input to every storage number and not a
property of the reservoir.

**It is measured, and it changes.** The relationship is the reservoir
basin's shape, and the basin fills with sediment. Lake Powell was
surveyed in 1963, 1986 and again in 2017 to 2018 by topobathymetric
survey.[^report] The 2018 result: **25,160,000 acre-feet at full pool,
3702.91 ft NAVD88**, which is **4.00 per cent below the 1986 figure**
(1,049,000 acre-feet) and 6.79 per cent below 1963 (1,833,000
acre-feet), an average loss near 33,270 acre-feet a year.[^report]

So a volume computed from the 1986 table is not the same quantity as a
volume computed from the 2018 one, and the difference is larger than
most of the terms in a reservoir ledger. **Name the revision.**

## Structure, as published

The 2018 data release carries the table as CSV.[^release] The file
used here, `Lake_Powell_2018_ElevAreaCap_calc.csv`, has 1,821 rows
from 3120.08 to 3717.19 ft NAVD88 at a step of about 0.33 ft, with
four columns:

| Column | Meaning |
|---|---|
| `Elevation_ft_NAVD88` | water surface elevation, North American Vertical Datum of 1988 |
| `Elevation_ft_NGVD29` | the same surface on the National Geodetic Vertical Datum of 1929 |
| `Area_acres` | surface area at that elevation |
| `Capacity_acrefeet` | cumulative storage below that elevation |

**Both datums are in the table**, and their difference here is 2.910
to 2.920 ft throughout. That column pair is not decoration: the
reservoir gauge's headline elevation parameter is on NGVD29 while the
table's primary column is NAVD88, so the pair is what lets a ledger
convert without assuming anything.[^record]

**Interpolation.** Between steps the relationship is smooth and linear
interpolation is adequate at this spacing; the step is a third of a
foot and the surface area changes by well under a per cent across one.
An elevation outside the table is not extrapolated: a reservoir below
the table's floor or above its top is outside the surveyed geometry.

## The datum, and what getting it wrong costs

The gauge's parameter code declares the datum: 62614 is above NGVD29,
62615 is above NAVD88.[^parameters] Reading a 62614 elevation into the
NAVD88 column is an available mistake, and at this reservoir in water
year 2023 it costs about **196,000 acre-feet in a stated volume**
while costing only **51,020 acre-feet in the change across the year**,
because a constant offset largely cancels in a difference.[^record]

That asymmetry is worth carrying. A ledger that only ever reports
changes can hold this mistake for years without anyone noticing, and
the day someone quotes a level from it, the level is wrong by more
than most reservoirs' annual evaporation.

## Uncertainty

The table carries no uncertainty field, and the survey report is the
place its accuracy is characterised. The practical uncertainties in a
storage number from it are, in rough order: which survey produced the
table, since revisions differ by per cent; the datum match between the
gauge and the table, which is an offset of feet; the gauge's own
elevation precision, which is 0.01 to 0.1 ft and negligible beside the
others; and the interpolation, which is smaller still. A storage
number should carry the table's revision for the first reason alone.

## Known issues

- A volume quoted without the survey revision cannot be reproduced or
  compared with another year's work.
- The two datum columns invite the wrong join; the parameter code on
  the gauge side is the authority for which one to use.
- Reclamation publishes its own report of the same survey, so two
  citations exist for one measurement; either is fine and the revision
  is what matters.
- Other reservoirs have their own tables on their own survey schedules,
  and nothing here transfers to them except the doctrine.

[^release]: the 2018 elevation-area-capacity data release
[^report]: USGS Scientific Investigations Report 2022-5017
[^parameters]: the USGS parameter code definitions
[^record]: the reservoir ledger measurement record
