---
type: dataset-gotcha
title: "IMERG run mixing: three calibrations under one variable name, and a Final record that ends in September 2025"
description: "The Early, Late and Final daily products all carry precipitation in mm/day, and a series that concatenates them is not one series: Final is gauge-adjusted for its own month, Early and Late by a climatological ratio. Over the Lees Ferry basin Late exceeded Final by 53 per cent for October 2022. The Final record stops at 2025-09-30, so any series extended into 2026 changes run there and again at the 2026-03-01 calibration change."
tags: [imerg, gpm, precipitation, run, calibration, final, late, early, seam, gesdisc]
generated: { by: claude-code/fable-5, at: 2026-09-06T22:00:00Z }
severity: high
dataset: ../datasets/imerg-v07.md
eval_case: imerg-run-mixing
status: draft
stale_after: 2026-12-01
sources:
  - id: relnotes
    resource: https://gpm.nasa.gov/sites/default/files/2024-11/IMERG_V07_ReleaseNotes_241126.pdf
    title: "IMERG V07 Release Notes, 20 November 2024 (the calibration per run: GPCC with Fuchs-Legates undercatch for Final, a climatological adjustment to Final for Early and Late)"
  - id: v08-schedule
    resource: https://gpm.nasa.gov/data/news/imerg-v08-transition-schedule
    title: "IMERG V08 Transition Schedule, GPM data news of 2026-04-28 (the Final record ends September 2025; hybrid Late and Early; the CORRA calibration climatological from March 1)"
  - id: v08-update
    resource: https://gpm.nasa.gov/data/news/update-imerg-v08-transition-schedule-aug-2026
    title: "Update to the IMERG V08 Transition Schedule, GPM data news of 2026-08-06"
  - id: cmr
    resource: https://cmr.earthdata.nasa.gov/search/granules.json?collection_concept_id=C2723754864-GES_DISC&sort_key=-start_date&page_size=1
    title: "The Final daily collection's granule inventory (last granule 2025-09-30; the Late and Early label change to V07C on 2026-03-03 and 2026-03-04), searched 2026-09-06"
  - id: dataset
    resource: ../datasets/imerg-v07.md
    title: "This bundle's IMERG V07 dataset concept (the seam dates and the stale_after that governs them)"
  - id: record
    resource: https://github.com/open-science-pillars/marketplace/issues/68
    title: "The precipitation record: the Late against Final measurement over the Lees Ferry basin, October 2022"
---

# IMERG run mixing: three calibrations under one variable name

**Mechanism.** The three daily IMERG products at GES DISC are one
algorithm run at three latencies, and their files are
interchangeable to a reader: the same grid, the same variable
`precipitation` in `mm/day`, the same attributes, the same filename
pattern apart from `3IMERGDE`, `3IMERGDL` and `3IMERGDF`. They are
not the same quantity. Final is adjusted, month by month, to the
GPCC gauge analysis with an undercatch correction; Early and Late
never see their month's gauges and are scaled by "a climatological
adjustment ... based on the Final Run", a ratio from earlier years.
Where a month departs from its climatology, the near-real-time
value departs from Final by the same amount, and nothing in the
file says so. Concatenating files across runs, which xarray and
every "open all the files in the directory" pattern do silently,
yields a series whose level changes at an undocumented
date.[^relnotes]

The situation as of 2026-09-06 makes this the default failure
rather than a rare one: the V07 Final record ENDS at 2025-09-30
(the parent products moved to V08 and the V07 Final code was not
run on V08 inputs), while Late and Early continue in a "hybrid"
posture, with their calibration set to climatological CORRA values
from 2026-03-01 and the granule label changing V07B to V07C on
2026-03-03 (Late) and 2026-03-04 (Early). A request for "IMERG
through the present" cannot be satisfied by Final, and a script
that fills the gap with Late produces a series with a run seam at
2025-10-01 and a calibration seam at 2026-03-01. V08 Final,
expected fall 2026, will be a fresh retrospective record from 1998,
not a continuation.[^v08-schedule][^v08-update][^cmr]

**Measured (2026-09-06).** Over the Colorado River basin above Lees
Ferry (the frozen polygon in this plugin's fixtures, 276,444 km2,
2,869 IMERG cells), October 2022, all 31 days present in both runs
and every cell valid:

| Run | Basin mean, mm | Volume, km3 |
|---|---|---|
| Late (GPM_3IMERGDL) | 44.53 | 12.31 |
| Final (GPM_3IMERGDF) | 29.13 | 8.05 |

Late is 53 per cent above Final for the same month, the same cells
and the same variable name. A water year of Final over the basin
totals 320 mm; one month of run mixing at this size moves the
annual total by five per cent, and a seam inside a drought index
or a trend is read as a climate signal.[^record]

**Wrong-result mode.** A basin precipitation series is assembled
from whatever daily files exist for the window: Final up to
September 2025, Late after. The monthly totals look continuous;
the 2025 to 2026 change is reported as wetter or drier; a P minus
Q or a storage budget carries the calibration step as a physical
term. Nothing fails, no field flags it, and the receipt (if any)
names one product.[^relnotes][^v08-schedule]

**Correct approach.** The run is a declared input, never a
default: the loader takes one run for the whole window, or one run
per month, and refuses a month whose files carry a different run
from the declaration and a month whose files carry two runs. Every
receipt names the run per month. A change of run between months is
a declared seam, flagged by date in the receipt and in the answer,
and a series that crosses 2025-10-01 (the end of Final) or
2026-03-01 (the calibration change) carries those dates as seams
whatever the declaration. A Final series is not extended past
2025-09-30 unless the user declares the run for the later months,
and then the two segments are stated as two calibrations. The
load-precipitation skill in this plugin implements exactly this
contract and cites this concept for the reason.[^dataset]

**Verification.** Load one month through two runs and compare the
basin means (the table above is the fixture case: the Late October
2022 and Final water year 2023 files under
`verification/fixtures/precipitation/`); declare `final` for a
window that reaches past September 2025 and confirm the refusal
names the last Final granule; declare `2025-09:final,2025-10:late`
and confirm the receipt carries a run seam dated
2025-10-01.[^record]

[^relnotes]: IMERG V07 Release Notes, 20 November 2024
[^v08-schedule]: IMERG V08 Transition Schedule, GPM data news, 2026-04-28
[^v08-update]: Update to the IMERG V08 Transition Schedule, GPM data news, 2026-08-06
[^cmr]: CMR granule inventory of the Final daily collection, searched 2026-09-06
[^dataset]: this bundle's IMERG V07 dataset concept
[^record]: the precipitation record on open-science-pillars/marketplace issue 68
