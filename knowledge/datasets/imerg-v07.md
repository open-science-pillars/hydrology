---
type: dataset
title: "GPM IMERG V07 daily precipitation: three runs, one variable name, and a Final record that ends in September 2025"
description: "Global 0.1 degree precipitation from GES DISC in three daily runs (Early, Late, Final) that share the variable name precipitation in mm/day but are calibrated differently: Final against the GPCC gauge analysis with undercatch correction, Early and Late by a climatological adjustment to Final. The V07 Final record stops at 2025-09-30; Late and Early continue in a hybrid posture whose calibration changed on 2026-03-01."
tags: [imerg, gpm, precipitation, gesdisc, daily, final, late, early, hydrology]
generated: { by: claude-code/fable-5, at: 2026-09-06T21:30:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-06T22:57:54Z }
resource: https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGDF_07/summary
version: "V07 (granule labels V07B, and V07C for Late from 2026-03-03 and Early from 2026-03-04); Final daily 2000-06-01 through 2025-09-30, Late and Early through yesterday (2026-09-05 on 2026-09-06); the monthly GPM_3IMERGM is Final only"
status: stable
upstream: pending
stale_after: 2026-12-01
citation:
  access_date_required: true
  authority: https://disc.gsfc.nasa.gov/
  data: "Huffman, G.J., E.F. Stocker, D.T. Bolvin, E.J. Nelkin, Jackson Tan (2023), GPM IMERG {run} Precipitation L3 1 day 0.1 degree x 0.1 degree V07, Greenbelt, MD, Goddard Earth Sciences Data and Information Services Center (GES DISC), accessed {access_date}, {doi}"
  doi: "10.5067/GPM/IMERGDF/DAY/07 (Final), 10.5067/GPM/IMERGDL/DAY/07 (Late), 10.5067/GPM/IMERGDE/DAY/07 (Early), 10.5067/GPM/IMERG/3B-MONTH/07 (monthly Final)"
  note: "the run is part of the citation; a series that spans two runs cites both and states the seam date"
sources:
  - id: cmr
    resource: https://cmr.earthdata.nasa.gov/search/collections.json?provider=GES_DISC&short_name=GPM_3IMERGDF&version=07
    title: "CMR collections at provider GES_DISC for GPM_3IMERGDF, GPM_3IMERGDL, GPM_3IMERGDE and GPM_3IMERGM version 07 (concept ids C2723754864, C2723754859, C2723754850 and C2723754851), and the granule inventory of the Final daily collection (last granule 2025-09-30), searched 2026-09-06"
  - id: granule
    resource: https://opendap.earthdata.nasa.gov/collections/C2723754864-GES_DISC/granules/
    title: "File metadata of the daily granules read over Cloud OPeNDAP on 2026-09-06 (variable names, units, long names, the DOI attribute, the time origin)"
  - id: relnotes
    resource: https://gpm.nasa.gov/sites/default/files/2024-11/IMERG_V07_ReleaseNotes_241126.pdf
    title: "IMERG V07 Release Notes, 20 November 2024 (the calibration per run, the rename of precipitationCal, the frozen-surface retrievals, the snowfall caution)"
  - id: v08-schedule
    resource: https://gpm.nasa.gov/data/news/imerg-v08-transition-schedule
    title: "IMERG V08 Transition Schedule, GPM data news of 2026-04-28 (the Final record ends September 2025; hybrid Late and Early; CORRA calibration climatological from March 1)"
  - id: v08-update
    resource: https://gpm.nasa.gov/data/news/update-imerg-v08-transition-schedule-aug-2026
    title: "Update to the IMERG V08 Transition Schedule, GPM data news of 2026-08-06 (Final now expected fall 2026; the near-real-time switch no sooner than winter 2026)"
  - id: record
    resource: https://github.com/open-science-pillars/marketplace/issues/68
    title: "The precipitation record: catalog check, the granule inventory per run, the window pulls and their sizes, the Late against Final comparison over the Lees Ferry basin"
---

# GPM IMERG V07 daily precipitation

**Identity.** IMERG (Integrated Multi-satellitE Retrievals for GPM)
merges the passive-microwave constellation, calibrated to the GPM
Core Observatory's combined radar-radiometer product (CORRA), with
infrared estimates, on a 0.1 degree global grid. The daily products
at GES DISC are three collections that differ only in latency and
calibration: `GPM_3IMERGDE` (Early, about four hours), `GPM_3IMERGDL`
(Late, about fourteen hours) and `GPM_3IMERGDF` (Final, a few
months, gauge-adjusted). A fourth, `GPM_3IMERGM`, is the monthly
Final. All four are version 07, provider GES_DISC, cloud
hosted.[^cmr]

**Variable and units (granule-verified 2026-09-06).** Every daily
granule carries `precipitation`, float32, `mm/day`, long name "Daily
mean precipitation rate (combined microwave-IR) estimate. Formerly
precipitationCal.", fill -9999.9, dimensions (time, lon, lat) with
lon first; `precipitation_cnt` (int8, the count of half-hour
periods with data, 48 when complete); `lon` and `lat` at cell
centres; `time` in days since 1980-01-06. The grid index of a
coordinate is floor((lon + 180) / 0.1), floor((lat + 90) / 0.1).
The V06 name `precipitationCal` was renamed to `precipitation` in
V07 (the release notes list the rename); code written for V06
finds nothing under the old name. The monthly file's variable is a
mean rate in `mm/hr`, and a monthly total is that rate times the
hours in the month.[^granule][^relnotes]

## Calibration per run

The three runs carry the same variable name and the same units and
are NOT the same quantity.[^relnotes]

- **Final** is adjusted to the GPCC monthly gauge analysis with an
  undercatch correction: a joint scheme, climatological Fuchs over
  Eurasia north of 45 N and Legates-Wilmott elsewhere (V07 changed
  this because Legates-Wilmott overcorrected at high latitudes).
- **Early and Late** are near-real-time and see no gauge analysis
  for their own month; V07 applies "a climatological adjustment to
  the Early and Late Runs based on the Final Run", so their level is
  set by past years' Final-to-satellite ratios, not by the month's
  own gauges.

Measured over the Colorado River basin above Lees Ferry (276,444
km2, the frozen polygon in this plugin's fixtures) for October 2022:
Late 44.53 mm, Final 29.13 mm, the same variable name, a difference
of 53 per cent of the Final value, with all 31 days present in both
and every cell valid. That is the size the calibration difference
can take over a single month in a dry, mountainous interior basin;
it is not a data gap, and no field in either file announces
it.[^record]

## The Final record ends in September 2025 (dated fact)

The last V07 Final daily granule is 2025-09-30 (thirty granules in
September 2025, none after), and the last monthly is September
2025. The reason is published: CORRA and GPROF, the parent products,
moved to V08, and the V07 Final code expects V07 inputs, so Final
production stopped rather than take V08 inputs and risk a
discontinuity.[^cmr][^v08-schedule]

The Late and Early runs continued in a "hybrid" posture (the V07
algorithm ingesting GPROF V08). From 2026-03-01 the calibration of
GPROF V08 to CORRA was set to climatological values computed from
selected seasonal periods of previous years and updated seasonally,
and the daily granule label changed from V07B to V07C on 2026-03-03
(Late) and 2026-03-04 (Early). The date the near-real-time runs
began ingesting GPROF V08 is not published on the GPM news pages
and the granule metadata carries no input-product versions; the
documented dates are the ones above.[^v08-schedule][^cmr]

The V08 Final Run, a retrospective processing from January 1998,
was announced for summer 2026 and moved to fall 2026 on 2026-08-06;
the Late and Early switch to V08 follows "no sooner than winter of
2026", with their own retrospective records released between the two.
This concept's `stale_after` sits at 2026-12-01 so that the gap, the
V08 dates and the seam list are re-read when V08 Final is expected
to exist.[^v08-update]

**Seams a series can cross (as of 2026-09-06).** 2025-10-01: the
Final record ends, so a series extended past September 2025 changes
run. 2026-03-01: the Late and Early calibration changes to
climatological CORRA values (label V07B to V07C two or three days
later). A future seam at the Late and Early switch to V08 and the
V08 Final release, undated. The load-precipitation skill in this
plugin names the run per month in its receipt and flags each of
these dates when the window crosses it; it will not extend a Final
series past 2025-09-30 unless the run for those months is declared
by the user.[^v08-schedule][^v08-update]

## Access

Cloud-hosted at GES DISC behind Earthdata Login with the GES DISC
application authorized on the account (the connector concept
records the failure shapes and what leaves the machine). A basin
window is pulled per granule through a Cloud OPeNDAP DAP4
constraint expression on the OPeNDAP URL CMR lists for the granule
(about 47 KB per day for the Lees Ferry window, 1.3 MB per month,
15.5 MB for a water year, against 31 MB per global daily file), with
the archive download and a local cut as the fallback when a subset
request does not answer with netCDF.[^record]

## Uncertainty

IMERG carries no per-cell uncertainty in the daily product beyond
`precipitation_cnt` and the half-hourly quality index, which the
daily file does not carry. The Final run's gauge adjustment is
monthly and at GPCC's gauge density: over sparsely gauged high
terrain the adjustment is a large-scale ratio, not a local
correction. The release notes ask that snowfall estimates "be
examined critically" and note "low precipitation rates for snowfall
over land" from the CORRA retrieval that calibrates the
constellation; the cold-season gotcha beside this concept carries
the check.[^relnotes]

## Known issues

- Three runs, one variable name: a series that concatenates runs
  without declaring them mixes calibrations (the run-mixing gotcha).
- V07 includes passive-microwave retrievals over frozen surfaces
  for the first time (V06 screened them out), with the quality index
  reduced there; the estimates over snow-covered and orographic
  terrain remain low (the cold-season gotcha).
- The monthly mean of the daily product does not exactly equal the
  monthly product over regions of very light precipitation, a
  rounding difference the release notes record.
- January 1998 through May 2000 (the retrospective TRMM-era
  extension using GridSat-B1 infrared) is of lower quality than the
  record after June 2000; the daily Final collection at GES DISC
  begins 2000-06-01.

[^cmr]: CMR collections and granule inventory at provider GES_DISC, searched 2026-09-06
[^granule]: daily granule file metadata read over Cloud OPeNDAP, 2026-09-06
[^relnotes]: IMERG V07 Release Notes, 20 November 2024
[^v08-schedule]: IMERG V08 Transition Schedule, GPM data news, 2026-04-28
[^v08-update]: Update to the IMERG V08 Transition Schedule, GPM data news, 2026-08-06
[^record]: the precipitation record on open-science-pillars/marketplace issue 68
