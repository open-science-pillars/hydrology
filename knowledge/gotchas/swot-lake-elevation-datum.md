---
type: dataset-gotcha
spheres: [hydrosphere]
title: "A SWOT lake elevation is a height above the EGM2008 geoid in the mean-tide system with three tide models removed: the Version C geoid carried an error of up to half a metre that Version D fixed, and the prior reference elevation is a catalogue value, not an observation"
description: "LakeSP and LakeAvg report wse as the ellipsoid height minus geoid_hght, solid_tide, load_tidef and pole_tide, against EGM2008 including the permanent tide, with geoid_hght carried so the value can be re-referenced. The Version C products interpolated the geoid from a file shifted by half an arcminute, an error within plus or minus 50 cm and typically within 10 cm, largest on steep geoid gradients, corrected in Version D along with a change of load tide model, so a series that joins the two families carries a step that is neither water nor instrument. The p_ref_wse in the prior file is the Prior Lake Database's reference elevation for storage change, stated by the release note as not well validated, and a difference between wse and it is not a level change."
tags: [swot, lakesp, lakeavg, geoid, egm2008, datum, tide-system, p_ref_wse, version, hydrology]
generated: { by: knowledge-seeder/claude, at: 2026-09-15T13:35:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-15T14:24:46Z, role: maintainer, source: https://github.com/open-science-pillars/hydrology/pull/66 }
severity: medium
upstream: pending
# medium: the geoid, the tide system and the Version C error are
# documented product behaviour; the trap bites through a series that
# mixes families or a difference against the catalogue reference,
# and the step is of the order of the stated total uncertainty rather
# than of the signal, so a single-family series is unaffected.
dataset: ../datasets/swot-lakes.md
status: stable
stale_after: 2027-03-15
sources:
  - id: pdd-lakesp
    resource: https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/pdd/SWOT-TN-CDM-0673-CNES_Product_Description_L2_HR_LakeSP_20250307_RevC_signed.pdf
    title: "SWOT L2_HR_LakeSP Product Description Document, Revision C, 2025-03-07, linked from the PO.DAAC collection record and read 2026-09-15: the wse definition and formula, the geophysical references section (EGM2008 in the mean tide system, the solid, pole and load tide models, the alternative load tide), the PLD reference attributes and the storage change section"
  - id: pdd-lakeavg
    resource: https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/pdd/SWOT-TN-CDM-0676-CNES_Product_Description_L2_HR_LakeAvg_20250307_RevC_signed.pdf
    title: "SWOT L2_HR_LakeAvg Product Description Document, Revision C, 2025-03-07, read 2026-09-15: the measured hydrological parameters section stating the cycle elevations are relative to EGM2008 with the LakeSP corrections already applied"
  - id: relnote-d
    resource: https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/web-misc/swot_mission_docs/SWOT_VersionD_KaRIn_Products_Release_Note_20250423b.pdf
    title: "Release Note, SWOT Version D KaRIn Science Data Products, 2025-04-23, read 2026-09-15: the C to D change table (geoid bug fix, FES2014 to FES2022b load tide, the height calibration refinement stated as O(5 mm) short-wavelength changes in SSH and WSE, improved pixel selection for lakes), the Version C known issue describing the geoid error and its size, and the known issue that storage change and the PLD reference elevations are not well validated"
  - id: dataset
    resource: ../datasets/swot-lakes.md
    title: "This bundle's SWOT lake products concept: the families, the series and the storage change attributes"
  - id: gauge-datum
    resource: ../gotchas/swot-gauge-datum-mismatch.md
    title: "This bundle's satellite-to-gauge datum gotcha: the comparison of a geoid height with a gauge on a national datum"
  - id: hydrocron
    resource: ../connectors/hydrocron-swot.md
    title: "This bundle's Hydrocron connector, which records that the river series it serves sit on the EGM2008 geoid"
---

# A lake elevation is a geoid height, and the geoid has a version

**Mechanism.** The elevation in the LakeSP files is not a height
above the ellipsoid and not a height above a national datum. The
document defines it as wse = H minus geoid_hght minus solid_tide
minus load_tidef minus pole_tide, where H is the geocentric height of
the water surface above the reference ellipsoid of the .prj file
after the media delays and the crossover calibration, `geoid_hght`
is the EGM2008 geoid height above that ellipsoid including the
zero-frequency permanent tide (the mean tide system), `solid_tide` is
the solid Earth tide without the permanent tide, `pole_tide` the sum
of the body and load pole tides, and `load_tidef` the FES ocean load
tide, with `load_tideg` from GOT4.10c provided as a swap.[^pdd-lakesp]
The cycle-average elevations of LakeAvg are the same quantity, taken
from LakeSP with the corrections already applied.[^pdd-lakeavg] The
Hydrocron river series rests on the same geoid.[^hydrocron]

The geoid value itself has a history. The Version C products
(PGC0, PIC0, PIC2) interpolated the geoid from a one-arcminute file
that had been shifted by half an arcminute in longitude and latitude;
the release note bounds the resulting error at plus or minus 50 cm,
more typically within 10 cm, and largest where the geoid gradient is
steep. Version D fixed it, refined the height calibration at the
level of about 5 mm, and moved the load tide model from FES2014 to
FES2022b.[^relnote-d] Since wse subtracts `geoid_hght`, an error in
the geoid is an error in the elevation of the same size and opposite
sign.[^pdd-lakesp]

A third elevation sits in the prior file: `p_ref_wse`, the reference
water surface elevation from the Prior Lake Database against which
the storage change is computed, beside `p_ref_area`, `p_date_t0` (the
first valid measurement, which is not necessarily the date of the
reference state) and `p_ds_t0` (the shift that makes the storage
change read zero at that date).[^pdd-lakesp] The release note states
that the storage change estimates and the reference elevations under
them are not well validated.[^relnote-d]

**Wrong-result mode.** A lake series that joins Version C granules
to Version D granules across the shared span, or that extends a C
series past 2025-05-03 with D granules, carries a step at the seam
that is the geoid correction at that lake, of order 10 cm and up to
half a metre in steep-gradient terrain, with the tide model change
beside it; it reads as a level change and nothing in either file
announces it. A reader who subtracts `p_ref_wse` from `wse` to get
"the change since the reference" has differenced an observation
against a catalogue value the release note does not vouch for, and
has not computed the product's storage change, which is translated to
`p_date_t0` for that reason. A reader who adds an ellipsoid height
from another source to the comparison, or a geoid height in the
tide-free system, has mixed reference surfaces that differ by
decimetres.[^pdd-lakesp][^relnote-d]

**Correct approach.** One family per series, the family named, and
where the C and D families both cover a date the D family, as the
release note advises; a series that must cross families states the
seam and the geoid change as a term. Elevations are quoted as heights
above EGM2008 in the mean tide system with the three tides removed,
and `geoid_hght` is carried beside `wse` so a reader can recover the
ellipsoid height as their sum. A change against the reference state
is the product's `ds` attribute with its `_u` and its `p_date_t0`,
never `wse` minus `p_ref_wse`. A comparison against a gauge on a
national datum is the separate case the gauge datum gotcha
holds.[^pdd-lakesp][^relnote-d][^gauge-datum][^dataset]

**Verification.** For one lake observed on the same pass in a
Version C and a Version D granule, read `geoid_hght` from each; the difference is the geoid correction at that lake and is the step a
joined series would carry; `wse` plus `geoid_hght`, the ellipsoid
height, differs between the two by the other Version D changes the
release note lists for lakes (the height calibration refinement of
order 5 mm, the load tide model from FES2014 to FES2022b and the
improved pixel selection), so the geoid step is read from
`geoid_hght` alone and not from the elevations. Read the .prj
file for the ellipsoid and the .shp.xml metadata for the geoid and
tide model names.[^pdd-lakesp][^relnote-d]

[^pdd-lakesp]: SWOT L2_HR_LakeSP Product Description Document, Revision C, 2025-03-07
[^pdd-lakeavg]: SWOT L2_HR_LakeAvg Product Description Document, Revision C, 2025-03-07
[^relnote-d]: Release Note, SWOT Version D KaRIn Science Data Products, 2025-04-23
[^dataset]: this bundle's SWOT lake products concept
[^gauge-datum]: this bundle's satellite-to-gauge datum gotcha
[^hydrocron]: this bundle's Hydrocron connector
