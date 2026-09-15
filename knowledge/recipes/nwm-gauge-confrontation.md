---
type: recipe
spheres: [hydrosphere]
title: "Confronting a gauge's daily flow with the National Water Model retrospective at the same reach: model output beside the record, the clocks named, the volume and the timing scored apart"
description: "How a USGS gauge's daily mean discharge is placed beside the National Water Model version 3.0 retrospective at the reach the store's gage_id axis assigns to it: the window kept inside the record and the chunk budget, the model's UTC days beside the gauge's local days, the approval and qualifiers of the gauge read first, and the confrontation scored as volume (bias, the annual ratio) and timing (correlation at lags, the peak dates) rather than one number. Worked on the Roaring Fork at Glenwood Springs for calendar 2021: correlation +0.952 on daily flows, the model's volume 1.355 times the gauge's, its June mean 100.6 against 57.3 m3/s, and its peak five days after the gauge's."
tags: [nwm, national-water-model, retrospective, confrontation, gauge, streamflow, hydrology]
generated: { by: process:claude-code, at: 2026-09-15T18:30:00Z }
inputs: "A USGS gauge with a daily mean discharge record over the window (parameter 00060, statistic 00003, with approval status and qualifiers), and the retrospective's daily means at the reach carrying that gauge through nwm_retrospective_streamflow on the observations server, the window inside the store's time axis and the fourteen-chunk budget"
expected: "Roaring Fork River at Glenwood Springs, USGS-09085000, against NHDPlus reach 1324997 (feature index 119426, the reach whose gage_id is 09085000), calendar 2021, 365 model days of 24 hours each from chunks 546 to 559: daily correlation +0.952, Nash-Sutcliffe efficiency -0.030 on flows and +0.625 on their logarithms, Kling-Gupta efficiency 0.122 with a variability ratio of 1.801 and a mean ratio of 1.355, percent bias +35.5 per cent; annual volume 0.586 km3 at the gauge and 0.794 km3 in the model; monthly means agreeing within 1 m3/s from January to April and the model's June mean 100.59 against the gauge's 57.29 m3/s; peaks 92.3 m3/s on 2021-06-06 at the gauge and 139.2 on 2021-06-11 in the model; the gauge's day t correlating best with the model's day t+1 (0.968, against 0.952 at the same day and 0.929 the other way)"
expected_uncertainty: "No sampling intervals are attached: the scores are descriptive statistics of one year at one reach, and the gauge record is Approved throughout with 8 ESTIMATED days, so the gauge side carries the rating's own uncertainty (about 5 per cent for a good rating) and the model side carries none that the store publishes. A change of the aggregation day (the model's UTC day against the gauge's Mountain Standard day) moves the daily correlation by about 0.015, which is the size of the one-day lag effect measured here"
status: draft
stale_after: 2027-03-15
sources:
  - id: nwm-connector
    resource: ../connectors/nwm-retrospective.md
    title: "This bundle's National Water Model retrospective connector concept: the store's layout, the hourly time axis from 1979-02-01 to 2023-02-01, the chunking, the gage_id axis, the daily aggregation in UTC with the hours counted, the fourteen-chunk budget, and the Lees Ferry decode that shows a reach below a dam holding the model's near-constant release"
  - id: streamflow-connector
    resource: ../connectors/usgs-water.md
    title: "This bundle's Water Data API streamflow connector: the daily collection, the approval and qualifier fields, and the units trap (cubic feet per second)"
  - id: regulated-gauge
    resource: ../gotchas/nwis-regulated-gauge.md
    title: "The regulated-gauge gotcha: a gauge below a dam records operations, and a model reach below a dam records the model's reservoir treatment; neither is the basin's hydrology"
  - id: swot-confrontation
    resource: swot-gauge-confrontation.md
    title: "This bundle's SWOT gauge confrontation recipe: the convention that a confrontation names its collection, states its pairing rule, scores what the reference is insensitive to, and reserves the word for a comparison against a product not constrained by the gauge"
  - id: bucket-layout
    resource: "https://noaa-nwm-retrospective-3-0-pds.s3.amazonaws.com/?list-type=2&delimiter=/"
    title: "The bucket listing read 2026-09-15: the domains Alaska, CONUS, Hawaii and PR; under CONUS/zarr/ the stores chrtout.zarr, forcing, gwout.zarr, lakeout.zarr, ldasout.zarr and rtout.zarr; under CONUS/netcdf/ the trees CHANOBS, CHRTOUT, FORCING, GWOUT, LAKEOUT, LDASOUT and RTOUT, the CHRTOUT files one per hour of about 48 MB (202101010000.CHRTOUT_DOMAIN1 is 48,018,574 bytes)"
  - id: roaring-fork-decode
    resource: https://noaa-nwm-retrospective-3-0-pds.s3.amazonaws.com/CONUS/zarr/chrtout.zarr/streamflow/546.3
    title: "The live call of 2026-09-15 behind the worked example: nwm_retrospective_streamflow with usgs_site 09085000 and the window 2021-01-01 to 2021-12-31 resolved the reach to feature_id 1324997 at feature index 119426, read the fourteen streamflow chunks 546.3 to 559.3 and their time chunks in 21 seconds, and returned 365 UTC days of 24 hours each in cubic metres per second from the store titled OUTPUT FROM WRF-Hydro v5.3.0-alpha1, code version v5.3.0-alpha1"
  - id: gauge-fixture
    resource: ../../verification/fixtures/README.md
    title: "This plugin's frozen gauge record for the worked example: roaring_fork_00060_2021_dv.parquet, USGS-09085000 daily mean discharge for calendar 2021 from the Water Data API, 365 rows all Approved, 8 carrying the ESTIMATED qualifier, pulled 2026-09-06"
  - id: cosgrove2024
    resource: https://doi.org/10.1111/1752-1688.13184
    title: "Cosgrove, Gochis, Flowers and others 2024, NOAA's National Water Model: advancing operational hydrology through continental-scale modeling, JAWRA Journal of the American Water Resources Association 60(2) 247 to 272: the model as an hourly cycling analysis and forecast system over millions of reaches, and the statement that version upgrades are measured against hourly streamflow correlation, Nash-Sutcliffe efficiency and bias; the Crossref record and abstract read 2026-09-15, the journal page not read. The retrospective itself carries no DOI on the bucket"
---

# Confronting a gauge's daily flow with the National Water Model retrospective

**Method.** Resolve the reach that carries the gauge, read the
retrospective's daily means over a window inside the record, read the
gauge's daily record with its approval and qualifiers, and score the
two series apart for volume and for timing. Name the retrospective
version, the store, the reach and the clocks in the caption. The
retrospective is model output beside a record; it is never the
record's replacement, and it is never the truth the gauge is checked
against.[^nwm-connector]

**Why volume and timing are scored apart.** A single efficiency
number folds a bias and a timing error into one figure and reads
worst when a model has the shape right and the size wrong. On the
Roaring Fork the daily correlation is +0.95 and the Nash-Sutcliffe
efficiency is below zero in the same year, because the model's
snowmelt volume is a third too large: a reader given the efficiency
alone would call the model useless, and a reader given the
correlation alone would call it good. Both are true of different
things.

## Before scoring

**Keep the window inside the record and the budget.** The CONUS
store's time axis is hours since 1979-02-01T01:00 and ends at
2023-02-01T00:00; a window past that is refused before any chunk is
read, and so is a window wider than fourteen 28-day chunks (about
392 days), because a reach's series lives one column deep in chunks
of 672 hours by 30,000 reaches and each chunk is 4 to 9
MB.[^nwm-connector] A calendar year touches fourteen chunks and is
the widest window one call answers. The hourly netCDF files beside
the store, one per hour of about 48 MB with every reach in each, are
the same output at a far higher cost for one reach, and the tool does
not read them.[^bucket-layout]

**Resolve the reach by the gauge, and record the feature id.** The
store's gage_id axis names the USGS gauge the model assigns to 8,660
of its reaches; the tool resolves a gauge number to that reach and
returns the feature id and index, which the caption
carries.[^nwm-connector] A gauge not on the axis needs the NHDPlus
feature id from elsewhere, and the pairing is then the caller's claim
rather than the model's.

**Read the gauge's approval and qualifiers first.** The gauge's daily
mean is Approved in arrears and may carry qualifiers (ESTIMATED on
ice-affected days); the retrospective is a finished simulation. On
the worked year the gauge is Approved throughout with 8 ESTIMATED
days, which the caption states.[^gauge-fixture][^streamflow-connector]

**Name the clocks.** The model's day is a UTC calendar day, the mean
of 24 hourly values with the fill excluded and the hours counted; the
gauge's day is the local day of its time zone, Mountain Standard at
Glenwood Springs, which begins seven hours after the UTC day. A daily
comparison therefore pairs days that overlap by seventeen hours, and
the lag correlations say how much that matters.[^nwm-connector]

**Convert the units once.** The gauge serves cubic feet per second
and the store cubic metres per second; the factor is 0.0283168466,
applied to the gauge and stated.[^streamflow-connector]

**A reach below a dam is a different confrontation.** The gauge
records operations and the model reach records the model's reservoir
treatment; the connector concept's Lees Ferry decode shows the model
holding a near-constant release where the gauge swings by a factor of
two. The recipe applies there too, but the caption says what each
side measures.[^regulated-gauge][^nwm-connector]

## The scores

For volume:

- **Percent bias** of the model against the gauge over the window,
  and the **ratio of annual volumes**, which is the same fact in km3.
- **Monthly means** side by side, because a bias concentrated in one
  season is a different statement from a uniform one.

For timing and shape:

- **Correlation of the daily flows**, at the same day and at a lag of
  one day either way, so the clock offset and any routing delay are
  visible as a number rather than absorbed.
- **The peak dates and sizes** on each side.
- **Nash-Sutcliffe efficiency** on flows and on their logarithms, and
  **Kling-Gupta efficiency** with its three components (correlation,
  the variability ratio, the mean ratio), reported because the
  literature quotes them and read with the caution above: they are
  summaries of the four numbers before them, not additional
  evidence.[^cosgrove2024]

No sampling intervals are attached to one year at one reach; the
scores are descriptive, and a second year or a second reach is a
second row, not a wider interval.

## What the recipe refuses

- Calling the retrospective an observation, or the gauge the truth:
  the one is model output and the other a rated record with its own
  approval and qualifiers.
- A window past the record's end or wider than the budget, which the
  tool refuses before reading; a recipe that pads the missing months
  from a forecast product has changed models mid-series.
- A comparison that does not name the retrospective version, the
  store, the feature id and the clocks.
- One efficiency number as the result.
- The word confrontation for a comparison at a reach whose model
  parameters were calibrated on this gauge, which is a consistency
  check; the retrospective's calibration record is not on the bucket,
  and the caption says whether it is known.[^swot-confrontation]

## The worked example

Roaring Fork River at Glenwood Springs, USGS-09085000, against the
CONUS retrospective at feature id 1324997 (index 119426, gage_id
09085000), calendar 2021, read live on 2026-09-15 in 21 seconds from
chunks 546 to 559; the gauge from this plugin's frozen 2021 record,
365 days Approved with 8 ESTIMATED.[^roaring-fork-decode][^gauge-fixture]

| Volume | Gauge | Model |
|---|---|---|
| Mean, m3/s | 18.59 | 25.19 |
| Annual volume, km3 | 0.586 | 0.794 |
| Percent bias | | +35.5 per cent |
| June mean, m3/s | 57.29 | 100.59 |
| January to April means, m3/s | 9.91, 9.43, 9.17, 12.61 | 9.14, 8.33, 8.11, 13.06 |
| Peak | 92.3 m3/s on 2021-06-06 | 139.2 m3/s on 2021-06-11 |

| Timing and shape | Value |
|---|---|
| Correlation, same day | +0.952 |
| Correlation, gauge day t against model day t+1 | +0.968 |
| Correlation, gauge day t against model day t-1 | +0.929 |
| Nash-Sutcliffe efficiency, flows | -0.030 |
| Nash-Sutcliffe efficiency, log flows | +0.625 |
| Kling-Gupta efficiency | 0.122 (correlation 0.952, variability ratio 1.801, mean ratio 1.355) |
| Seven-day means | correlation +0.962, percent bias +35.3 per cent |

**How to read it.** The model has the year's shape: the recession,
the low winter flows within 1 m3/s of the gauge, the rise in April
and the fall from July. It has the melt's size wrong by a third, all
of it in May to August, with a peak a third larger and five days
later than the gauge's, which is why the efficiency on flows is
negative while the efficiency on logarithms, which weights the low
flows, is positive. The gauge's day aligns best with the model's
following day, a one-day timing difference the clock offset alone
does not produce. What the confrontation cannot say is why the melt
volume is too large: the forcing, the snow model, the routing, and
any diversion above the gauge that the model does not carry are all
candidates, and a second year on the same reach is the next row.

**What this is not.** It is not a validation of the National Water
Model, which its authors measure over thousands of gauges and hourly
flows, and it is not a bias to be subtracted: a model 35 per cent
high in one drought year at one snowmelt reach is a fact about that
year and that reach.[^cosgrove2024]

[^nwm-connector]: this bundle's National Water Model retrospective connector concept
[^streamflow-connector]: this bundle's Water Data API streamflow connector concept
[^regulated-gauge]: this bundle's regulated gauge gotcha
[^swot-confrontation]: this bundle's SWOT gauge confrontation recipe
[^bucket-layout]: the bucket listing, read 2026-09-15
[^roaring-fork-decode]: the live call of 2026-09-15 at the Roaring Fork reach
[^gauge-fixture]: this plugin's frozen Roaring Fork 2021 gauge record and its provenance
[^cosgrove2024]: Cosgrove and others 2024, the Crossref record and abstract read 2026-09-15
