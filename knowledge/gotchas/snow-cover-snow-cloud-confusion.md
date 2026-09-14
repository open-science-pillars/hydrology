---
type: dataset-gotcha
spheres: [hydrosphere, cryosphere]
title: "Snow and cloud are confused in both directions, and the algorithm flags name the cases: a cloud fringe read as snow, thin plains snow masked as cloud, and neither reversed by a screen"
description: "The snow algorithm calls a cell cloud only when the cloud mask says confident cloudy and reads the other three confidences as clear, recording probably cloudy and probably clear in bits 5 and 6 of the algorithm flags. Sub-pixel cloud, cloud fringes, popcorn cloud over vegetation and cloud in the shadow of cloud are spectrally indistinct from snow and pass as snow with no screen reversing them; thin or sparse snow on plains, and snow in Antarctica, is masked as confident cloudy when the cloud mask's snow background flag is wrong and appears as 250. Snow and cloud discrimination is the most frequent error in the product's accuracy assessment, and a misread cell passes through the gap-filled product as cloud that persists for days."
tags: [modis, viirs, snow-cover, cloud-mask, mod35, cloud-snow-confusion, algorithm-flags, commission-error, omission-error, nsidc, cryosphere, hydrology]
generated: { by: knowledge-seeder/claude, at: 2026-09-14T05:30:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-14T12:13:16Z, role: maintainer, source: https://github.com/open-science-pillars/hydrology/pull/61 }
severity: medium
dataset: ../datasets/modis-viirs-snow-cover.md
status: stable
stale_after: 2027-03-14
sources:
  - id: c61-guide
    resource: https://nsidc.org/sites/default/files/c61_modis_snow_user_guide.pdf
    title: "MODIS Snow Products Collection 6.1 User Guide, Riggs, Hall and Roman, 2019, read 2026-09-14: the Cloud and Snow Confusion section (the four confidences, the fringe and popcorn cases, the Nebraska plains case where thin snow became confident cloudy, Antarctica), the C6.1 overview stating significant cloud and snow confusion remains, and the CGF section on confusion persisting as cloud"
  - id: mod10a1-guide
    resource: https://nsidc.org/sites/default/files/mod10a1-v061-userguide_1.pdf
    title: "MOD10A1 version 61 user guide, NSIDC, last updated December 2021, read 2026-09-14: the cloud possible screens on bits 5 and 6 and their stated purpose, the Snow_Albedo_Daily_Tile code 151 (cloud detected as snow), and the basic QA rules"
  - id: viirs-c2-guide
    resource: https://nsidc.org/sites/default/files/documents/technical-reference/snpp_jpss1_viirs_snow_cover_products_collection_2_user_guide.pdf
    title: "SNPP/JPSS1 VIIRS Snow Cover Products Collection 2 User Guide, Riggs and Hall, 2021, read 2026-09-14: the cloud mask at 750 m mapped to four 375 m pixels, Section 3.4.5 on cloud and snow confusion, and the snow background processing path"
  - id: vnp10a1-guide
    resource: https://nsidc.org/sites/default/files/documents/user-guide/multi_vnp10a1-v002-userguide.pdf
    title: "VNP10A1 version 2 user guide, NSIDC, last updated January 2026, read 2026-09-14: the errors section naming cloud and snow confusion among the conditions that interfere with the screens, and the Antarctic Peninsula note"
  - id: hall-riggs-2007
    resource: https://doi.org/10.1002/hyp.6715
    title: "Hall and Riggs, 2007, Accuracy assessment of the MODIS snow products, Hydrological Processes 21(12), 1534 to 1547; the Crossref abstract read 2026-09-14: the most frequent errors are due to snow and cloud discrimination problems"
  - id: mod10a1-page
    resource: https://nsidc.org/data/mod10a1/versions/61
    title: "The NSIDC product page for MOD10A1 version 61, read 2026-09-14: the version summary adding the probably cloudy and probably clear flags to the algorithm flags QA"
---

# Snow and cloud confusion, and the flags that name it

**Mechanism.** The snow algorithm does not detect cloud. It reads the
cloud mask product's Unobstructed FOV Quality Flag, which has four
values, and it sets a cell to cloud (250) only for "confident cloudy";
"probably cloudy", "probably clear" and "confident clear" are all
interpreted as clear and the cell is processed for snow. Collection
6.1 records the two middle confidences in the algorithm flags, bit 5
for probably cloudy and bit 6 for probably clear, "so they can be used
to evaluate possible cloud/snow confusion situations"; on VIIRS the
cloud mask is at 750 m and one mask value is mapped onto four 375 m
cells.[^c61-guide][^mod10a1-guide][^viirs-c2-guide][^mod10a1-page]
The confusion runs both ways. Clouds the mask does not call confident
cloudy, and whose reflectance resembles snow, are detected as snow:
sub-pixel cloud at the periphery of cloud fields, scattered popcorn
cloud over vegetated landscapes, streaming formations, and cloud lying
in the shadow of other cloud are "spectrally indistinct from snow in
the algorithm", and none of the data screens reverses or flags that
commission error. In the other direction, the cloud mask chooses its
processing path from a snow or ice background flag, and where that
flag is wrong, thin or sparse snow on plains has been masked as
confident cloudy by a single visible cloud test, so real snow arrives
in the product as 250 with the brighter, deeper snow around it
detected. Over Antarctica the lack of thermal contrast between cloud
and snow leaves visible patches of "no snow" that are wrong either
way. The guide states that the C6.1 revisions improved clear-sky
detection rather than cloud discrimination, that "significant
cloud/snow confusion situations remain", and that a reinterpretation
of the cloud mask that fixed the plains case was inconsistent
elsewhere.[^c61-guide][^viirs-c2-guide][^vnp10a1-guide] Hall and
Riggs 2007 name snow and cloud discrimination as the most frequent
error in the product's accuracy assessment.[^hall-riggs-2007] The
snow albedo field carries its own trace of the first direction, code
151 "cloud detected as snow".[^mod10a1-guide]

**Wrong-result mode.** Snow extent over a forested or boreal basin on
a day of scattered cloud is inflated by cloud fringes counted as snow,
and the inflation is largest at low to moderate index values, exactly
where a threshold on the index would keep them. A snow-off date over
plains is early where thin late-season snow was masked as cloud and
the cloudy cells were dropped, or is missed altogether. In the
gap-filled product a misread cell becomes a cloud run of unreasonable
length, so the oldest filled cells in a CGF map can be the misread
rather than weather; in the 8-day maximum-extent composite a single
day's false snow survives for the period. None of this is marked in
`Basic_QA`, which is set from the input radiance range and the solar
zenith angle, not from the cloud decision.[^c61-guide][^mod10a1-guide]

**Correct approach.** The snow value is read with its algorithm
flags. A snow cell with bit 5 set (probably cloudy, processed as
clear) is a detection the cloud mask half-doubted, and the share of
such cells in an extent is reported; the same for bit 6 where the
concern is the other way. Where a run of 250 sits on plains or on a
known snowpack in season, or where snow appears on a day of broken
cloud over forest, the guide's own check applies: comparison with the
surface reflectance product (MOD09GA) or the true-colour imagery for
the same overpass, which is how the guide's own figures diagnose both
cases. A result over a landscape the guide names, boreal forest under
popcorn cloud, snow-fringed plains, Antarctica, states the case and its
direction beside the number. The accuracy of about 93 per cent is a
clear-sky figure.[^c61-guide][^hall-riggs-2007][^viirs-c2-guide]

**Verification.** In a tile with scattered cloud over forest, the
cells with snow values and bit 5 set cluster along cloud edges in the
true-colour image of the same day, and their index values sit low;
the `Snow_Albedo_Daily_Tile` field shows code 151 on some of them. In
the plains case, a block of 250 whose neighbours are snow at low
values, on a day the imagery shows clear sky, is the snow background
flag failing, and the same cells carry bit 6 (probably clear) or no
cloud bit at all in the CGF's inherited flags.[^c61-guide][^mod10a1-guide]

[^c61-guide]: the MODIS Snow Products Collection 6.1 User Guide, 2019
[^mod10a1-guide]: the MOD10A1 version 61 user guide, last updated December 2021
[^viirs-c2-guide]: the VIIRS Snow Cover Products Collection 2 User Guide, 2021
[^vnp10a1-guide]: the VNP10A1 version 2 user guide, last updated January 2026
[^hall-riggs-2007]: Hall and Riggs 2007, Hydrological Processes, Crossref record and abstract
[^mod10a1-page]: the NSIDC product page for MOD10A1 version 61, read 2026-09-14
