---
type: recipe
spheres: [hydrosphere]
title: "A basin's terrestrial water storage anomaly from the JPL mascon CRI grid: whole mascons, one pass of the gain factors, the formal error as a floor, and a trend fit around the holes"
description: "How a monthly terrestrial water storage anomaly for one basin is read from the JPL RL06.3M version 4 CRI-filtered mascon grid: the region as whole mascons chosen from the granule's own mascon_ID field, the area-weighted sum of lwe_thickness against the 2004 to 2009 baseline, the CLM gain factors applied once and only for land hydrology, the per-mascon uncertainty combined as a floor, the trend fit on the calendar epochs with the missing months left as holes, and what a TWS number contains (snow, surface water, soil moisture and groundwater together) so that subtracting modeled stores for groundwater is understood as inheriting the model."
tags: [grace, grace-fo, mascons, tws, terrestrial-water-storage, basin, hydrology, scale-factors, trend]
generated: { by: knowledge-seeder/claude, at: 2026-09-13T20:40:00Z }
inputs: "The CRI-filtered JPL mascon grid, TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4 (CMR concept C3195527175-POCLOUD, version RL06.3Mv04, DOI 10.5067/TEMSC-3JC634), one granule, GRCTellus.JPL.200204_202607.GLO.RL06.3M.MSCNv04CRI.nc at the verification date, carrying lwe_thickness, uncertainty, land_mask, mascon_ID, scale_factor and GAD on the 0.5-degree grid; the region as a set of whole mascons chosen from the granule's mascon_ID field, never a 0.5-degree cell mask, with the region's area the true area of those mascons; the method an area-weighted mean of lwe_thickness over the region's mascons per epoch against the product's 2004 to 2009 baseline, the gain factors applied once to the CRI grid for a land hydrology region with the scaled and unscaled series both kept, the formal error combined from the per-mascon uncertainty field per the product's guidance on correlated errors, and a trend fit with annual and semi-annual terms on the epochs read from the time axis with the missing months and the 2017 to 2018 gap as holes"
expected: "For each epoch, the sum over the region's mascons of anomaly (cm) times mascon area (km2), divided by the region's total area, is the basin mean in cm; the same sum times 1e-5 is the volume anomaly in km3, and at the product's water density of 1000 kg per cubic meter the same number is gigatonnes; both are anomalies against the 2004.000 to 2009.999 time mean the product removed. The trend in cm per year is the slope of a fit with linear, annual and semi-annual terms over the epochs read from the file's time axis, with the window's first and last epochs named and the holes inside it listed (the file's months_missing attribute lists 33 calendar months with no solution), and a window that crosses July 2017 through May 2018 states how the inter-mission continuity was handled. No numeric anchor is recorded yet: this recipe is a draft, and a first anchor for a named basin will be added from a basin water balance receipt, never from a remembered value"
expected_uncertainty: "The formal error comes from the granule's uncertainty field, a one-sigma value per 3-degree mascon and not per cell, area-weighted over the region's mascons and combined per the product's guidance on correlated mascon errors rather than as independent errors, since the provider bundle's dataset concept states that mascon errors are spatially correlated and that basin averages quote the product's guidance, not the square root of the mascon count; it is the floor of the statement, never the whole of it. Leakage and the constraint are their own term: a region of few mascons carries its neighbours' signal and the solution's a priori constraint, the CRI filter reduces coastal leakage by about half in the product team's synthetic tests, and combined with the CRI filter the gain factors reduce the leakage error in the mass balance of large basins (above 160,000 km2) by 11 to 30 per cent averaged globally; a basin near or below one mascon has no series of its own (the resolution-floor gotcha). The gain factors themselves come from a land model's simulated hydrology over 2002 to 2009, so the scaled series inherits that model's spatial pattern, and the unscaled series is reported beside it. The pre-applied corrections, the GIA model (ICE6G-D), the geocenter (the granule's attribute reads 'We use a version of TN-13 based on the JPL mascons') and the C20 and C30 substitutions from TN-14, are named as applied and never re-applied, and a trend across the 2017 to 2018 gap states its handling and cites the bridging evidence (the provider bundle's gotchas)"
sources:
  - id: product-page
    resource: https://podaac.jpl.nasa.gov/dataset/TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4
    title: "PO.DAAC collection page: TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4 (the product description: 4,551 equal-area 3-degree mascons, the CRI filter, the land mask, uncertainty values and gridded mascon-ID number, and the optional gain factors for sub-mascon hydrology)"
  - id: cmr
    resource: https://cmr.earthdata.nasa.gov/search/collections.umm_json?short_name=TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4
    title: "CMR collection record C3195527175-POCLOUD, version RL06.3Mv04, DOI 10.5067/TEMSC-3JC634, and its granule listing (one granule, 2002-04-16 through 2026-07-16)"
  - id: virtual-listing
    resource: https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-public/virtual_collections/TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4/TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4_virtual_https.json
    title: "The collection's virtual dataset reference file (public bucket): the granule's variables with their attributes and the file's global attributes, including time_mean_removed, months_missing, GIA_removed, the geocenter and C20/C30 substitutions and the water density"
  - id: release-note
    resource: https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/gracefo/open/docs/GRACE_GRACE-FO_ReleaseNotes_JPL_MASCON.txt
    title: "JPL GRACE mascon solution release notes (RL06.3M version 4): anomalies relative to 2004 to 2009, the land mask, mascon placement and scale factor files unchanged since RL05M, the GRACE-FO uncertainty calibration and the July 2025 GAD fix"
  - id: months-rl06
    resource: https://archive.podaac.earthdata.nasa.gov/podaac-ops-cumulus-docs/gracefo/open/docs/GRACE_GRACE-FO_Months_RL06.csv
    title: "GRACE and GRACE-FO RL06 month list (PO.DAAC): every calendar month since April 2002 with its solution index, the days used and the months with no coverage"
  - id: watkins-2015
    resource: https://doi.org/10.1002/2014JB011547
    title: "Watkins and others, 2015, Improved methods for observing Earth's time variable mass distribution with GRACE using spherical cap mascons, Journal of Geophysical Research: Solid Earth (the mascon solution, its a priori constraint from geophysical models, and the reduced dependence on scale factors)"
  - id: wiese-2016
    resource: https://doi.org/10.1002/2016WR019344
    title: "Wiese, Landerer and Watkins, 2016, Quantifying and reducing leakage errors in the JPL RL05M GRACE mascon solution, Water Resources Research (the CRI filter, and the gain factors for continental hydrology with their measured effect on large basins)"
  - id: landerer-2012
    resource: https://doi.org/10.1029/2011WR011453
    title: "Landerer and Swenson, 2012, Accuracy of scaled GRACE terrestrial water storage estimates, Water Resources Research (the effective resolution of GRACE TWS at a few hundred kilometers, and gain factors from land hydrology model simulations for the spherical harmonic grids)"
  - id: scanlon-2016
    resource: https://doi.org/10.1002/2016WR019494
    title: "Scanlon and others, 2016, Global evaluation of new GRACE mascon products for hydrologic applications, Water Resources Research (the JPL and CSR mascons against rescaled spherical harmonics in 176 basins: trends up to 20 mm per year against seasonal amplitudes up to 250 mm)"
  - id: joodaki-2014
    resource: https://doi.org/10.1002/2013WR014633
    title: "Joodaki, Wahr and Swenson, 2014, Estimating the human contribution to groundwater depletion in the Middle East, from GRACE data, land surface models, and well observations, Water Resources Research (a groundwater residual: lakes and the Caspian subtracted, then a land surface model's soil moisture, snow, canopy and river storage)"
  - id: dataset
    resource: https://github.com/open-science-pillars/nasa-daac-knowledge/blob/16152b3776cd1307a9a4e03bab3f5376e9b5e63b/knowledge/podaac/datasets/grace-fo-mascons.md
    title: "The provider bundle's mascon dataset concept (knowledge/podaac/datasets/grace-fo-mascons.md in nasa-daac-knowledge, cited at a pinned commit): the product's identity, structure, baseline and pre-applied corrections, the native scale, the uncertainty grids and the correlated errors"
  - id: leakage
    resource: https://github.com/open-science-pillars/nasa-daac-knowledge/blob/16152b3776cd1307a9a4e03bab3f5376e9b5e63b/knowledge/podaac/gotchas/grace-coastal-leakage.md
    title: "The provider bundle's coastal-leakage gotcha (knowledge/podaac/gotchas/grace-coastal-leakage.md)"
  - id: gia
    resource: https://github.com/open-science-pillars/nasa-daac-knowledge/blob/16152b3776cd1307a9a4e03bab3f5376e9b5e63b/knowledge/podaac/gotchas/grace-gia-correction.md
    title: "The provider bundle's GIA gotcha (knowledge/podaac/gotchas/grace-gia-correction.md)"
  - id: gap
    resource: https://github.com/open-science-pillars/nasa-daac-knowledge/blob/16152b3776cd1307a9a4e03bab3f5376e9b5e63b/knowledge/podaac/gotchas/grace-intermission-gap.md
    title: "The provider bundle's inter-mission gap gotcha (knowledge/podaac/gotchas/grace-intermission-gap.md)"
  - id: low-degree
    resource: https://github.com/open-science-pillars/nasa-daac-knowledge/blob/16152b3776cd1307a9a4e03bab3f5376e9b5e63b/knowledge/podaac/gotchas/grace-low-degree-replacements.md
    title: "The provider bundle's degree-1 and C20/C30 gotcha (knowledge/podaac/gotchas/grace-low-degree-replacements.md)"
  - id: floor
    resource: ../gotchas/grace-basin-below-resolution-floor.md
    title: "This bundle's resolution-floor gotcha: a basin near or below one mascon has no basin series"
  - id: total-storage
    resource: ../gotchas/grace-tws-is-total-storage.md
    title: "This bundle's total-storage gotcha: TWS is every store together, and a residual inherits the model"
  - id: scale-factors
    resource: ../gotchas/grace-scale-factors-once-and-for-hydrology.md
    title: "This bundle's gain-factor gotcha: applied once, for hydrology, and wrong over ice and ocean"
  - id: water-balance
    resource: ../computations/basin-water-balance.md
    title: "This bundle's basin water balance computation: the footprint floor derived from the product's geometry (111,266 km2, one mostly-land mascon), the storage term's uncertainty rule and the epoch rule"
  - id: partitioning
    resource: ./grace-groundwater-partitioning.md
    title: "This bundle's groundwater partitioning recipe: groundwater as the TWS-minus-other-stores residual"
status: draft
stale_after: 2027-03-13
---

# A basin's terrestrial water storage anomaly from the JPL mascon CRI grid

**What the file is.** The CRI-filtered JPL mascon product is one
netCDF granule on a 0.5-degree grid whose native resolution is the
3-degree mascon; its identity, structure, baseline and pre-applied
corrections are the provider bundle's dataset concept,
`knowledge/podaac/datasets/grace-fo-mascons.md` in nasa-daac-knowledge,
and are not repeated here.[^dataset] The granule carries
`lwe_thickness` (the anomaly in centimeters of equivalent water
thickness, CRI applied), `uncertainty` (centimeters, a one-sigma value
per 3-degree mascon written onto every cell of that mascon),
`land_mask` (binary, the mask the CRI filter used), `mascon_ID` (the
mascon identifier, 1 to 4,551, mapped to the grid), `scale_factor`
(dimensionless gain factors) and `GAD` (centimeters, the ocean and
atmosphere de-aliasing model, added back to ocean pixels only), with
`time` in days since 2002-01-01 and `time_bounds` the first and last
day of each monthly solution, and its `time_mean_removed` attribute
reads 2004.000 to 2009.999.[^virtual-listing]

**Method.**

1. **Region as whole mascons.** The basin polygon selects mascons from
   the granule's own `mascon_ID` field: a mascon is in the region by a
   stated rule (its center inside the polygon, or more than half its
   land area inside), and the region is those whole mascons. The
   information lives at the mascon, so a 0.5-degree cell mask clipped
   to the polygon reports the same mascon value many times over and
   invents a resolution the product does not have; the effective
   resolution of GRACE terrestrial water storage is a few hundred
   kilometers.[^virtual-listing][^dataset][^landerer-2012]
   The region's area is the true area of its mascons, computed from
   the cell bounds on the sphere, and the statement carries the number
   of mascons spanned beside the basin's own area. A basin near or
   below one mascon has no series of its own: what can be delivered
   is the containing mascon's series, labelled as that region's
   storage with the resolution and leakage caveats beside the formal
   error, and a water balance refuses the storage term
   there.[^floor][^water-balance]
   For a land hydrology region the cells are the land-mask cells of
   land mascons; a coastal mascon's ocean part carries ocean mass with
   GAD added back, a different quantity.[^virtual-listing][^leakage]
2. **Basin mean and volume.** For each epoch, the basin mean in
   centimeters is the sum over the region's mascons of anomaly times
   mascon area, divided by the region's total area. The volume anomaly
   in cubic kilometers is the same sum times 1e-5 (one centimeter over
   one square kilometer is 1e4 cubic meters), and at the product's
   water density of 1000 kilograms per cubic meter the same number is
   gigatonnes.[^virtual-listing] Both are anomalies against the
   product's 2004 to 2009 baseline, which the release note states as
   the reference of every released anomaly; a series re-baselined to
   another period says so.[^release-note]
3. **The gain factors, once and for hydrology.** For a land hydrology
   region the `scale_factor` field is multiplied into `lwe_thickness`
   cell by cell, once, before the area-weighted sum; the product
   describes the factors as optional and as the way to study mass
   change at sub-mascon resolution for continental hydrology, and the
   product team's paper derives them to reduce the leakage error that
   parameterizing the field in mascons introduces: combined with the
   CRI filter, the gain factors reduce the leakage error in the mass
   balance of large basins (above 160,000 km2) by 11 to 30 per cent
   (0.6 to 1.5 millimeters of equivalent water height) averaged
   globally.[^product-page][^wiese-2016] The mascon solution needs
   less of this than a spherical harmonic one (the global mean scale
   factor falls by 0.17), which is why the factors are an option and
   not a step.[^watkins-2015]
   The factors come from a land model's simulated hydrology over 2002
   to 2009, so they are for hydrology and not for ice or ocean mass,
   and they are never applied a second time or to a series that was
   scaled already; the scaled and unscaled series are both kept and
   the statement names which one it quotes.[^virtual-listing][^scale-factors][^dataset]
4. **Formal error.** The `uncertainty` field is one sigma per mascon,
   not per cell, so the region's formal error is the area-weighted
   combination over its mascons, never over its cells, combined per
   the product's guidance on correlated mascon errors rather than as
   independent errors: the provider bundle's dataset concept states
   that mascon errors are spatially correlated and that a basin
   average quotes the product's guidance, not the square root of the
   mascon count, and the result is the floor of the
   statement.[^virtual-listing][^dataset] The
   GRACE-FO months carry an uncertainty calibration updated in RL06.3M
   version 4 that mostly affects land mascons with low signal
   amplitude.[^release-note]
5. **Trend on the calendar epochs.** The epochs are read from the
   file's `time` and `time_bounds`, never counted from the number of
   solutions: the file's global attribute lists 33 calendar months
   with no solution, among them July 2017 through May 2018 and August
   and September 2018, and the month list distributed with the product
   marks the same months as no coverage.[^virtual-listing][^months-rl06]
   The fit carries linear, annual and semi-annual terms on the
   irregular epochs with the holes left as holes, never interpolated;
   its slope is the trend, and a window that crosses the inter-mission
   gap states how continuity was handled and cites the bridging
   evidence.[^gap] The GIA model and the low-degree series the product
   applied are named beside the trend and never re-applied.[^gia][^low-degree]

**What the number contains.** Terrestrial water storage from GRACE is
the total: snow and ice on land, surface water in rivers, lakes and
reservoirs, soil moisture, canopy water and groundwater, together and
inseparable in the measurement.[^dataset][^total-storage] The mascon
comparison across 176 basins found long-term trends up to about 20
millimeters per year riding on seasonal amplitudes up to 250
millimeters.[^scanlon-2016] A groundwater series is therefore a residual:
the total minus the other stores taken from a land surface model
(soil moisture, snow, canopy and river storage) and from observations
of lakes and reservoirs, which is what the published Middle East
analysis did with CLM4.5 and the Caspian and two lakes subtracted
before attributing the remainder to groundwater.[^joodaki-2014]
Subtracting a modeled store assumes the model's soil moisture and snow
are right in amplitude, phase and trend over the basin; whatever the
model gets wrong lands in the groundwater term, with the sign
reversed, and arrives without an error bar unless one is
constructed.[^total-storage][^partitioning]

**Cross-check.** The unscaled and scaled basin series differ by the
sub-mascon redistribution the factors impose; the factors were derived
to reduce the leakage error of the mascon parameterization, so their
effect on the region's series is one bound on that term, and the
coastal case carries the provider bundle's leakage gotcha beside
it.[^wiese-2016][^leakage] The formal error is the other floor. A basin water balance closed over the same basin and
window, with the storage change read from this series, tests the
series against precipitation, evapotranspiration and discharge; the
computation concept records how the residual is judged.[^water-balance]

**Provenance.** Every number quoted from this recipe names the
product version and granule, the baseline period, the region as a
list of mascon identifiers with its total area and mascon count,
whether the gain factors were applied, the window with its epochs and
holes, and the GIA model and low-degree series the product applied.
Live checks on 2026-09-13: the PO.DAAC collection page was read and
its description is the source for the product's structure and the
optional gain factors;[^product-page] the CMR collection record
(concept C3195527175-POCLOUD, version RL06.3Mv04, DOI
10.5067/TEMSC-3JC634, revised 2026-07-28) and its granule listing were
read, one granule, GRCTellus.JPL.200204_202607.GLO.RL06.3M.MSCNv04CRI.nc,
2002-04-16 through 2026-07-16, revised 2026-09-08;[^cmr] the
collection's virtual dataset reference file in the public bucket was
read and is the source for the variable names, their attributes and
the global attributes quoted above (it indexes the file ending June
2026, with 258 epochs and a date_created of 2026-08-19, one month
behind the granule CMR lists, so the variable set is confirmed on the
file in hand at analysis time);[^virtual-listing] the release note
was read (last modified 23 January 2020 in its footer, with entries
through July 2025);[^release-note] the month list was read: 290
calendar months from April 2002 through May 2026, the last solution
index 257, with July 2017 through May 2018 and August and September
2018 marked as no coverage;[^months-rl06] every DOI was verified
against the Crossref registry the same day (title, authors, journal,
year) and the abstracts read there, which is where the measured
leakage reductions, the 160,000 km2 basin size, the 176-basin
comparison and the CLM4.5 subtraction come from; the Wiley journal
pages themselves sit behind a bot check, and the GRACE Tellus data
pages returned 404 on the day, so the product's own attributes and
the release note stand in for them.

[^product-page]: PO.DAAC collection page: TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4
[^cmr]: CMR collection record C3195527175-POCLOUD and its granule listing
[^virtual-listing]: The collection's virtual dataset reference file (variables and global attributes)
[^release-note]: JPL GRACE mascon solution release notes, RL06.3M version 4
[^months-rl06]: GRACE and GRACE-FO RL06 month list, PO.DAAC
[^watkins-2015]: Watkins and others, 2015, Journal of Geophysical Research: Solid Earth, doi:10.1002/2014JB011547
[^wiese-2016]: Wiese, Landerer and Watkins, 2016, Water Resources Research, doi:10.1002/2016WR019344
[^landerer-2012]: Landerer and Swenson, 2012, Water Resources Research, doi:10.1029/2011WR011453
[^scanlon-2016]: Scanlon and others, 2016, Water Resources Research, doi:10.1002/2016WR019494
[^joodaki-2014]: Joodaki, Wahr and Swenson, 2014, Water Resources Research, doi:10.1002/2013WR014633
[^dataset]: The provider bundle's mascon dataset concept
[^leakage]: The provider bundle's coastal-leakage gotcha
[^gia]: The provider bundle's GIA gotcha
[^gap]: The provider bundle's inter-mission gap gotcha
[^low-degree]: The provider bundle's degree-1 and C20/C30 gotcha
[^floor]: This bundle's resolution-floor gotcha
[^total-storage]: This bundle's total-storage gotcha
[^scale-factors]: This bundle's gain-factor gotcha
[^water-balance]: This bundle's basin water balance computation
[^partitioning]: This bundle's groundwater partitioning recipe
