---
type: dataset-gotcha
title: "IMERG cold-season underestimation over snow and mountains: values present, quality reduced, and NLDAS-2 forcing as the check"
description: "IMERG V07 includes passive-microwave retrievals over frozen surfaces for the first time (V06 screened them out), with the quality index reduced there, and the release notes say snowfall rates over land are low and should be examined critically. Over the Colorado River basin above Lees Ferry the IMERG Final water-year 2023 total is 320 mm against 375 mm from the NLDAS-2 gauge-based forcing, a ratio of 0.86 for the year and 0.68 for November through March. The check is the NLDAS-2 series beside the IMERG one; the gap is not missing values."
tags: [imerg, gpm, precipitation, snow, orographic, cold-season, nldas, gauge, underestimation]
generated: { by: claude-code/fable-5, at: 2026-09-06T22:10:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-06T22:57:54Z }
severity: high
dataset: ../datasets/imerg-v07.md
eval_case: imerg-cold-season-orographic-underestimation
status: stable
stale_after: 2026-12-01
sources:
  - id: relnotes
    resource: https://gpm.nasa.gov/sites/default/files/2024-11/IMERG_V07_ReleaseNotes_241126.pdf
    title: "IMERG V07 Release Notes, 20 November 2024 (PMW estimates over frozen surfaces included with reduced quality index; the snowfall caution; GPROF skill over frozen surfaces, orographic areas and coastal zones)"
  - id: nldas
    resource: ../datasets/nldas2-forcing.md
    title: "This bundle's NLDAS-2 forcing concept (the precipitation field is the CPC gauge analysis with the PRISM terrain adjustment, disaggregated hourly)"
  - id: dataset
    resource: ../datasets/imerg-v07.md
    title: "This bundle's IMERG V07 dataset concept (the calibration per run, the daily variables)"
  - id: record
    resource: https://github.com/open-science-pillars/marketplace/issues/68
    title: "The precipitation record: the water-year 2023 IMERG Final and NLDAS-2 basin means over the Lees Ferry polygon, month by month"
---

# IMERG cold-season underestimation over snow and mountains

**Mechanism.** IMERG's precipitation is passive-microwave
retrievals (GPROF, over every constellation sensor) calibrated to
the GPM combined radar-radiometer product (CORRA) and filled with
infrared estimates between overpasses. Frozen surfaces are the
retrieval's hard case (the release notes list them with orographic
areas and coastal zones as the surface types "that tend to yield
lesser quality results"); before V07 IMERG screened those retrievals
out entirely for grid boxes of snow-covered or ice-covered land. V07
"included PMW estimates over frozen surfaces" for the first time,
with the half-hourly quality index reduced there to mark the lower
confidence, so the daily grid now carries a value everywhere. The
release notes are direct about what those values are worth: "IMERG
estimates for snowfall should be examined critically ... Recent
analysis shows low precipitation rates for snowfall over land due to
deficiencies in the detection and rate retrieval by CORRA, which is
used to intercalibrate the PMW estimates", and GPROF's skill over
"frozen surfaces, orographic areas, and coastal zones" is listed as
still to be demonstrated, with users asked to "seek confirmation of
the values". The Final run's gauge adjustment is a monthly ratio at
GPCC's gauge density, which over the mountain West is a handful of
valley stations per grid box of the analysis: it lifts the level, it
does not put the snow back where the terrain put it.[^relnotes]

The result is an underestimate, not a gap. The daily file for a
January over the Rockies is complete (`precipitation_cnt` 48, every
cell valid), and nothing in the daily product distinguishes a cell
where the retrieval saw the storm from one where it saw the
snowpack. A tool that checks for missing values finds none. This is
the corrected form of an older belief that IMERG has "no data over
snow": that was V06; the V07 failure is quieter.[^relnotes]

**Measured (2026-09-06).** Over the Colorado River basin above Lees
Ferry (276,444 km2; 2,869 IMERG cells and 1,851 NLDAS-2 cells
inside the frozen polygon), water year 2023, IMERG Final beside
NLDAS-2 primary forcing (the CPC gauge analysis with the PRISM
terrain adjustment, summed to days over the same
polygon):[^record][^nldas]

| Month | IMERG Final (mm) | NLDAS-2 forcing (mm) | IMERG over NLDAS-2 |
|---|---|---|---|
| 2022-10 | 29.13 | 36.53 | 0.80 |
| 2022-11 | 16.42 | 23.33 | 0.70 |
| 2022-12 | 30.73 | 43.92 | 0.70 |
| 2023-01 | 27.28 | 49.11 | 0.56 |
| 2023-02 | 16.43 | 27.04 | 0.61 |
| 2023-03 | 44.19 | 56.31 | 0.78 |
| 2023-04 | 24.14 | 19.91 | 1.21 |
| 2023-05 | 20.04 | 21.91 | 0.91 |
| 2023-06 | 26.35 | 23.80 | 1.11 |
| 2023-07 | 15.63 | 10.64 | 1.47 |
| 2023-08 | 47.58 | 41.59 | 1.14 |
| 2023-09 | 22.54 | 20.44 | 1.10 |
| Water year | 320.44 (88.585 km3) | 374.53 (103.535 km3) | 0.86 |

For the water year IMERG is 0.86 of the gauge-based total; for
November through March it is 0.68; from April through September it
is 1.06. The deficit is a cold-season one and not a uniform bias:
the November through March shortfall (64.7 mm) is larger than the
water-year shortfall (54.1 mm), so the annual ratio hides most of
it. The largest monthly gap is January 2023, 27.28 mm against 49.11
mm.

**Wrong-result mode.** A basin water balance takes the IMERG Final
water-year total as its P term, closes P minus Q minus ET against
GRACE storage change, and attributes the residual to
evapotranspiration or groundwater; a snow-drought index built on
IMERG reads the cold season as drier than the gauges do every year
and the anomaly as smaller than it is; a comparison of two basins
at different elevations carries a bias that scales with terrain.
The number is complete, has no fill, and cites a DOI.[^relnotes]

**Correct approach.** An IMERG total over snow-covered or
mountainous terrain for any window touching November through March
is stated with this bias named, and the gauge-based series is run
beside it: the load-precipitation skill loads the same polygon and
window through `--source nldas2` and reports the two basin means
and their ratio before the IMERG value goes into a budget. Where the
basin lies outside the NLDAS-2 domain (the conterminous United
States and its margins), the check is the national gauge analysis
that covers it, and its absence is stated. The IMERG number is not
corrected by the ratio silently; the two are reported as two
estimates, and the budget carries the difference as its
precipitation uncertainty.[^nldas][^dataset]

**Verification.** Load the fixture water year through both sources
(`verification/fixtures/precipitation/imerg_final_lees_ferry_wy2023.nc`
and `nldas2_lees_ferry_wy2023.nc` over
`verification/fixtures/basins/usgs_09380000_nldi.geojson`) and
reproduce the table; the golden notebook beside the fixtures asserts
the ratios.[^record]

[^relnotes]: IMERG V07 Release Notes, 20 November 2024
[^nldas]: this bundle's NLDAS-2 forcing concept
[^dataset]: this bundle's IMERG V07 dataset concept
[^record]: the precipitation record on open-science-pillars/marketplace issue 68
