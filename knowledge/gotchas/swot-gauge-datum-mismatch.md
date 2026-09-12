---
type: dataset-gotcha
spheres: [hydrosphere]
title: "A satellite lake elevation and a gauge elevation are on different datums, and the difference between them is mostly the datum"
description: "SWOT reports water surface elevation against a geoid model; a reservoir gauge reports against NGVD29 or NAVD88, and which one is fixed by the parameter code rather than by the site. Measured at Lake Powell on one pass: the same comparison gives -1.497 m against the gauge's NAVD88 series and -0.582 m against its NGVD29 series, so the choice of datum moves the answer by 0.914 m, which is most of it. Neither number is a measurement until the relationship between the geoid model and the gauge's datum is cited."
tags: [swot, lakesp, datum, navd88, ngvd29, geoid, reservoir, elevation, hydrology]
generated: { by: claude-code/opus-5, at: 2026-09-08T05:20:00Z }
severity: high
dataset: ../datasets/swot-river-lake.md
eval_case: swot-gauge-datum-mismatch
status: draft
stale_after: 2027-03-08
sources:
  - id: parameters
    resource: https://api.waterdata.usgs.gov/ogcapi/v0/collections/parameter-codes/items/62614
    title: "The USGS parameter code definitions read 2026-09-08: 62614 is lake or reservoir water surface elevation above NGVD 1929, 62615 above NAVD 1988, 00062 above an unspecified datum"
  - id: granule
    resource: https://podaac.jpl.nasa.gov/dataset/SWOT_L2_HR_LakeSP_D
    title: "SWOT LakeSP: the wse field and the geoid_hght field beside it, read from granule SWOT_L2_HR_LakeSP_Obs_001_162_NA_20230726T234646_20230726T235518_PGD0_01 on 2026-09-08"
  - id: record
    resource: https://github.com/open-science-pillars/marketplace/issues/75
    title: "The measurement record: the two gauge series, the two differences, and the offset that could not be sourced"
---

# The difference between a satellite and a gauge is mostly the datum

**Mechanism.** Both numbers are called an elevation and both are in
length units, so subtracting them looks like a comparison. They are
heights above different surfaces.

- **SWOT LakeSP** reports `wse` against a geoid model, and carries
  `geoid_hght` beside it, which is the geoid's height above the
  ellipsoid at that location and is **not** the offset to any national
  vertical datum.[^granule]
- **A USGS reservoir gauge** reports against a national datum, and
  **which one is declared by the parameter code, not by the site**:
  62614 is "above NGVD 1929", 62615 is "above NAVD 1988", and 00062 is
  "above datum" with the datum left to the site file.[^parameters] A
  gauge can publish more than one of these for the same water.

So a difference between the two carries the real signal plus an offset
that neither file states.

**Measured (2026-09-08).** Lake Powell, one SWOT pass on 2023-07-26,
against the dam gauge's own daily values for that day:[^record]

| Compared against | Difference |
|---|---|
| Gauge 3584.50 ft NAVD88 (parameter 62615) = 1092.556 m | **-1.497 m** |
| Gauge 3581.50 ft NGVD29 (parameter 62614) = 1091.641 m | **-0.582 m** |

The choice of gauge series moves the answer by 0.914 m and neither is
a measurement, because the geoid-to-NAVD88 relationship was not
sourced. A paper that reports either number as a satellite-to-gauge
agreement has reported a datum.

**A second trap in the same file.** The eleven features inside a box
around Lake Powell on that pass belong to two prior lakes: three carry
the reservoir's own identifier and cluster within 0.3 m, while eight
belong to an arm complex and range over 43 m. A median across all
eleven is 1101.258 m, ten metres above the reservoir. The `lake_name`
field does not separate them, because it is a semicolon-joined list
that names Lake Powell in both. **The identity is the lake id.**

**Wrong-result mode.** Nothing raises, the units agree, and the
magnitudes are plausible: a metre of disagreement between a satellite
and a gauge is exactly what a validation study expects to find and
report. The error survives review because the number looks like a
result. Worse, it is stable: the same offset appears in every pass, so
a time series of differences looks precise and consistent while being
displaced by a fixed unsourced amount, and a bias computed from it is
the datum.

**Correct approach.** State the datum of each side, from the parameter
code on the gauge side and from the product's own documentation on the
satellite side, and cite the offset between them from an authority
rather than deriving it from the data being compared. Where that
offset cannot be cited, say so and do not quote a difference: an
uncited datum makes a difference uninterpretable, not merely
uncertain. Where the two national datums are both published for the
same gauge, their difference is the agency's own conversion and can be
used freely; that is a different situation from an unsourced geoid
relationship.

Compare changes rather than levels where the question allows it. A
change over a window is insensitive to a constant datum offset, which
is why a rise of 44 ft is safe to state when a level of 3576 ft is not.

**Verification.** Take a reservoir with a SWOT record and a gauge that
publishes both national datums. Compute the satellite-minus-gauge
difference against each series. Confirm the two differ by the datum
offset and not by anything about the water, and confirm the offset
matches the agency's own conversion between its two published series.

[^parameters]: the USGS parameter code definitions
[^granule]: the SWOT LakeSP product and the granule read here
[^record]: the reservoir ledger measurement record
