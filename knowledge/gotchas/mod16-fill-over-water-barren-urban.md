---
type: dataset-gotcha
spheres: [hydrosphere]
title: "MOD16 fill codes over water, barren and urban land: seven codes, one in the header, and none of them a zero"
description: "MOD16 writes seven codes above its valid range for cells where evapotranspiration was not computed (water, barren, snow and ice, wetland, urban, unclassified, fill), and the file header advertises only 32767 while the catalog page names a third value. Averaged as numbers they are nonsense; read as zero they understate the basin. Over a HUC12 half covered by Lake Powell, 52.4 per cent of cells carry a code and the zero reading halves the basin mean. The basin mean must exclude them, count them, and state the masked fraction."
tags: [mod16, modis, evapotranspiration, fill-value, water, urban, barren, basin-mean, lpdaac]
generated: { by: claude-code/fable-5, at: 2026-09-07T00:05:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-07T02:11:54Z }
severity: high
dataset: ../datasets/mod16a2gf.md
eval_case: mod16-fill-over-water-barren-urban
status: stable
stale_after: 2027-03-06
sources:
  - id: guide
    resource: https://lpdaac.usgs.gov/documents/931/MOD16_User_Guide_V61.pdf
    title: "MOD16 User's Guide version 1.0 of 2021-02-26: the seven fill values and the sentence that the header lists only one"
  - id: catalog
    resource: https://www.earthdata.nasa.gov/data/catalog/lpcloud-mod16a2gf-061
    title: "The LP DAAC catalog entry for MOD16A2GF v061, which reports the ET_500m fill value as 32761, read 2026-09-06"
  - id: dataset
    resource: ../datasets/mod16a2gf.md
    title: "This bundle's MOD16A2GF concept (units, scale factor, valid range, the fill table and the quality layer)"
  - id: record
    resource: https://github.com/open-science-pillars/marketplace/issues/69
    title: "The evapotranspiration record: the basin means measured over the fixtures, with the masked fraction and the fill classes per basin"
---

# MOD16 fill codes over water, barren and urban land

**Mechanism.** MOD16 computes evapotranspiration for vegetated land.
Where it does not compute it, it writes a code above the valid range
rather than leaving the cell empty, and the code says why: 32766
perennial salt or water bodies, 32765 barren or sparse vegetation,
32764 perennial snow and ice, 32763 permanent wetland, 32762 urban or
built-up, 32761 unclassified, 32767 fill.[^guide] The file header
carries one `_FillValue`, 32767, and the LP DAAC catalog page reports
the fill value as 32761,[^catalog] so a reader who trusts either one
alone leaves five or six codes in the array.

Those codes are large positive integers in the same int16 array as
the measurements. Three things then happen, in rising order of harm.
Averaged as numbers, with the scale factor applied, a single water
cell contributes 3276.6 mm for one 8-day period and the annual mean
comes out near 79,000 mm: absurd, and therefore caught. Masked only
on 32767, the other six codes stay and the mean is absurd in the same
way, which is again a mercy. Read as "no evapotranspiration here,
therefore zero", the arithmetic is quiet, the number looks entirely
reasonable, and the basin mean is diluted in exact proportion to how
much of the basin is water, rock, city or ice. Only the third one
survives review.

**Measured (2026-09-06).** Over HUC12 140700061004 (Padre Creek-Lake
Powell, 104.6 km2, 489 window cells inside the polygon), calendar
year 2023 of MOD16A2GF:[^record]

| Reading | Annual basin mean | What it is |
|---|---|---|
| Fill codes excluded, masked fraction stated | 168.72 mm over the measured cells (50.0 km2 of the unit's 104.6) | land evapotranspiration on the land that has an estimate |
| Fill codes read as zero | 80.39 mm over all 489 cells | the same land evapotranspiration diluted by the reservoir, 48 per cent of the first |
| Fill codes averaged as numbers | 78,987 mm | absurd, and therefore the harmless failure |

52.4 per cent of the unit's cells carry a code in at least one
composite: 242 water and 14 barren of 489. The zero reading loses
half the basin mean without any arithmetic error, and nothing in the
file objects.

By contrast the Roaring Fork at Glenwood Springs is 1.2 per cent
masked and Capitol Creek 0.0 per cent, so the same code path returns
494.60 mm and 521.12 mm for 2023 with the masked fraction reported as
what it is: negligible.[^record] The failure is not evenly
distributed; it is concentrated exactly where the water is.

**Wrong-result mode.** A basin water balance closes P minus Q minus
ET against storage change and takes the diluted ET, attributing the
residual to groundwater or to gauge error. A reservoir basin looks
like it evaporates half what it does, because MOD16 does not compute
open-water evaporation at all and the zero reading turns that silence
into a measurement. An irrigation study over a valley with a city in
it reads the urban cells as bare of evapotranspiration. A trend over
a shrinking reservoir moves as the water mask moves, and reads as
climate.

**Correct approach.** Treat every value above the valid range of
32700 as not-a-measurement, whatever the header says; exclude those
cells from the mean; count them by class; and put the masked fraction
in the receipt beside the mean, because a mean over 48 per cent of a
basin is a different quantity from a mean over 99 per cent of it.
Compute the volume over the area the measured cells actually cover,
not over the whole polygon, so a land rate is never applied to the
part of the basin that has no estimate. Refuse rather than average
when the masked fraction passes a stated threshold (this bundle's
loader refuses above 50 per cent and says so), and let the caller
raise the threshold deliberately, which puts the number and its
masked fraction in the same receipt. Where the masked part is open
water, say that the basin's reservoir evaporation is missing from the
total: no MOD16 cell carries any of it, so it has to come from a
reservoir water balance or an open-water evaporation product before
the basin's water loss is complete.

**Verification.** Load the Lake Powell fixture over the Padre Creek
polygon and confirm the refusal names the masked fraction; raise
`--max-masked` and confirm the receipt reports 52.4 per cent masked,
242 water cells and a volume computed over 49.9 km2 rather than
104.6 km2; load the Roaring Fork fixture and confirm the same code
path reports 1.2 per cent.[^record]

[^guide]: MOD16 User's Guide version 1.0, 2021-02-26
[^catalog]: LP DAAC catalog entry for MOD16A2GF v061, read 2026-09-06
[^dataset]: this bundle's MOD16A2GF concept
[^record]: the evapotranspiration record, open-science-pillars/marketplace issue 69
