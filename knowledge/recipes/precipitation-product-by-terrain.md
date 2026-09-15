---
type: recipe
spheres: [hydrosphere, atmosphere]
title: "Choosing a precipitation product by terrain and question: IMERG, Daymet, MERRA-2 and NLDAS-2 in complex terrain, at high latitude, in the cold season, for extremes and for long series, with a second product run beside the first as the check"
description: "How a precipitation product is chosen for a basin question from what each of four products is: IMERG a satellite merge on a global 0.1 degree grid with a monthly gauge adjustment in its Final run, Daymet a station interpolation on a 1 km North American grid, MERRA-2 a reanalysis whose land precipitation is corrected toward gauges outside the high latitudes, and NLDAS-2 the CPC gauge analysis with the PRISM terrain adjustment over the conterminous United States. The choice follows the terrain and the gauge network around it, the latitude band, the season, the scale the question needs and the homogeneity a trend needs, and the deliverable is never one product alone: the second product over the same polygon and window, with the ratio of the two totals, is the check, as the orographic gotcha measured over the Colorado headwaters."
tags: [precipitation, imerg, daymet, merra-2, nldas-2, terrain, orographic, high-latitude, cold-season, extremes, long-series, product-choice, hydrology]
generated: { by: knowledge-seeder/claude, at: 2026-09-15T13:35:00Z }
inputs: "The question (a budget term over a basin and a window, an event series, the tail of the daily distribution, a trend, or a cold-season total); the basin polygon and its location (inside or outside the conterminous United States and North America, its relief, its latitude); the window; and the four products as their concepts describe them: GPM IMERG V07 daily (GPM_3IMERGDF, GPM_3IMERGDL, GPM_3IMERGDE at GES DISC, this bundle's concept), NLDAS-2 File A hourly forcing (NLDAS_FORA0125_H 2.0 at GES DISC, this bundle's concept), Daymet Version 4 R1 daily prcp (Daymet_Daily_V4R1_2129 at ORNL DAAC, the provider bundle's concept) and MERRA-2 PRECTOTCORR and PRECTOT in M2T1NXFLX and M2TMNXFLX (GES DISC, the provider bundle's concept); the method a basin mean per product computed with each grid's own cell areas over the same polygon and window, and the ratio of the two totals reported beside the chosen product's value"
expected: "A choice stated with its reason, and two basin series over the same polygon and window with their totals and ratio. The one measured anchor this bundle owns is the orographic gotcha's: over the Colorado River basin above Lees Ferry for water year 2023, IMERG Final is 0.86 of the NLDAS-2 total for the year and 0.68 for November through March, and 1.06 for April through September, so a cold-season total from IMERG over snow-covered high terrain in the conterminous United States is expected to sit well below the gauge-based one and a warm-season total near it. No anchor is recorded yet for Daymet or MERRA-2 against either; the first one recorded here will be a receipt over a named basin"
expected_uncertainty: "The disagreement between the two products over the same polygon and window is the precipitation uncertainty carried into a budget, and it is reported as two estimates and a ratio, never as a correction applied to one. Its size is scope-dependent: the review of thirty global data sets found annual land precipitation deviating by as much as 300 mm per year among products, with the largest differences in complex mountain areas and some high-latitude regions, and the comparison of eleven global estimates (three high-resolution products, four climate data records and four reanalyses) found annual differences over continental regions around 0.8 mm per day. Each product's own error statement is a floor beneath that: IMERG carries no per-cell uncertainty in the daily file, NLDAS-2 inherits the gauge network's undercatch and sparsity with a climatological terrain ratio, Daymet's cross-validation error is a station-level statistic that is larger in station-sparse and high-relief regions than its domain average, and MERRA-2 ships no error field, with the analysis increment and the observing-system epochs standing in"
sources:
  - id: imerg
    resource: ../datasets/imerg-v07.md
    title: "This bundle's IMERG V07 dataset concept: the three runs and their calibrations (Final against GPCC with the Fuchs undercatch correction over Eurasia north of 45 N and Legates-Willmott elsewhere), the frozen-surface retrievals, the Final record ending 2025-09-30, the V08 seams, the daily variable and the absence of a per-cell uncertainty"
  - id: imerg-orographic
    resource: ../gotchas/imerg-cold-season-orographic-underestimation.md
    title: "This bundle's IMERG cold-season gotcha: the release-note caution on snowfall, and the measured water-year 2023 ratios of IMERG Final to NLDAS-2 over the Colorado River basin above Lees Ferry (0.86 for the year, 0.68 for November through March, 1.06 for April through September)"
  - id: imerg-runs
    resource: ../gotchas/imerg-run-mixing.md
    title: "This bundle's IMERG run-mixing gotcha: three calibrations under one variable name and the seams a series can cross"
  - id: nldas
    resource: ../datasets/nldas2-forcing.md
    title: "This bundle's NLDAS-2 forcing concept: the CPC gauge-only daily analysis with the PRISM orographic adjustment disaggregated to hours by radar, CMORPH or NARR weights that do not change the daily total, the conterminous domain (longitude -125 to -67, latitude 25 to 53), the record from 1979, the hour-ending stamp, and the gauge network's undercatch and sparsity as its error"
  - id: daymet
    resource: https://github.com/open-science-pillars/nasa-daac-knowledge/blob/2f04d4d6952c35e841a6f4088953cb0f5332de89/knowledge/ornldaac/datasets/daymet-v4.md
    title: "The provider bundle's Daymet Version 4 R1 dataset concept (knowledge/ornldaac/datasets/daymet-v4.md in nasa-daac-knowledge, cited at a pinned commit): daily surface weather interpolated from GHCN-daily stations on a 1 km Lambert conformal conic grid over continental North America (from 1980), Hawaii and Puerto Rico, updated at the close of each calendar year, with uncertainty as a separate station-level cross-validation dataset"
  - id: daymet-sparse
    resource: https://github.com/open-science-pillars/nasa-daac-knowledge/blob/2f04d4d6952c35e841a6f4088953cb0f5332de89/knowledge/ornldaac/gotchas/daymet-station-sparse-error.md
    title: "The provider bundle's Daymet station-sparse gotcha (knowledge/ornldaac/gotchas/daymet-station-sparse-error.md): the network is dense over most of the contiguous United States and very sparse over Arctic Alaska and Canada, northern Mexico and mountainous terrain, the cross-validation error is per station and larger there than the domain mean, and the derived variables have no cross-validation"
  - id: daymet-365
    resource: https://github.com/open-science-pillars/nasa-daac-knowledge/blob/2f04d4d6952c35e841a6f4088953cb0f5332de89/knowledge/ornldaac/gotchas/daymet-365-day-year.md
    title: "The provider bundle's Daymet calendar gotcha (knowledge/ornldaac/gotchas/daymet-365-day-year.md): every year has 365 days, a leap year keeps February 29 and drops December 31"
  - id: daymet-lcc
    resource: https://github.com/open-science-pillars/nasa-daac-knowledge/blob/2f04d4d6952c35e841a6f4088953cb0f5332de89/knowledge/ornldaac/gotchas/daymet-lcc-projection-and-cell-area.md
    title: "The provider bundle's Daymet projection gotcha (knowledge/ornldaac/gotchas/daymet-lcc-projection-and-cell-area.md): the cell is one square kilometer only on the standard parallels, and a total from a cell count is biased"
  - id: daymet-r1
    resource: https://github.com/open-science-pillars/nasa-daac-knowledge/blob/2f04d4d6952c35e841a6f4088953cb0f5332de89/knowledge/ornldaac/gotchas/daymet-v4-r1-correction.md
    title: "The provider bundle's Daymet R1 gotcha (knowledge/ornldaac/gotchas/daymet-v4-r1-correction.md): 2020 and 2021 were rerun with corrected Canadian station inputs under a new DOI, a difference concentrated in high-latitude January"
  - id: merra2
    resource: https://github.com/open-science-pillars/nasa-daac-knowledge/blob/2f04d4d6952c35e841a6f4088953cb0f5332de89/knowledge/gesdisc/datasets/merra-2.md
    title: "The provider bundle's MERRA-2 dataset concept (knowledge/gesdisc/datasets/merra-2.md): the reanalysis from 1980 on one 0.625 by 0.5 degree grid, the flux collections carrying PRECTOT and PRECTOTCORR, no error field, and the analysis increment and observing-system epochs standing in"
  - id: merra2-corr
    resource: https://github.com/open-science-pillars/nasa-daac-knowledge/blob/2f04d4d6952c35e841a6f4088953cb0f5332de89/knowledge/gesdisc/gotchas/merra2-prectotcorr-versus-prectot.md
    title: "The provider bundle's PRECTOTCORR gotcha (knowledge/gesdisc/gotchas/merra2-prectotcorr-versus-prectot.md): the land surface is forced with precipitation corrected toward gauge and satellite products outside the high latitudes, the correction blends to zero between 42.5 and 62.5 degrees of latitude and is absent poleward, and PRECTOT is the atmosphere's own"
  - id: merra2-streams
    resource: https://github.com/open-science-pillars/nasa-daac-knowledge/blob/2f04d4d6952c35e841a6f4088953cb0f5332de89/knowledge/gesdisc/gotchas/merra2-stream-boundaries-and-discontinuities.md
    title: "The provider bundle's stream-boundary gotcha (knowledge/gesdisc/gotchas/merra2-stream-boundaries-and-discontinuities.md): four production streams joined at 1992, 2001 and 2011, the reprocessed months, and the documented observing-system steps"
  - id: merra2-time
    resource: https://github.com/open-science-pillars/nasa-daac-knowledge/blob/2f04d4d6952c35e841a6f4088953cb0f5332de89/knowledge/gesdisc/gotchas/merra2-time-stamp-conventions.md
    title: "The provider bundle's time-stamp gotcha (knowledge/gesdisc/gotchas/merra2-time-stamp-conventions.md): the hourly time-averaged collections are stamped at the half hour and the instantaneous ones on the hour"
  - id: merra2-grid
    resource: https://github.com/open-science-pillars/nasa-daac-knowledge/blob/2f04d4d6952c35e841a6f4088953cb0f5332de89/knowledge/gesdisc/gotchas/merra2-grid-weights.md
    title: "The provider bundle's grid-weights gotcha (knowledge/gesdisc/gotchas/merra2-grid-weights.md): the regular latitude-longitude grid has no area variable and a plain mean over-represents high latitudes"
  - id: beck-2019
    resource: https://doi.org/10.5194/hess-23-207-2019
    title: "Beck, Pan, Roy, Weedon, Pappenberger, van Dijk and others, 2019, Daily evaluation of 26 precipitation datasets using Stage-IV gauge-radar data for the CONUS, Hydrology and Earth System Sciences 23 (record and abstract read on the Crossref registry 2026-09-15: the reanalyses performed better in winter and the satellite datasets in summer, IMERG outperformed ERA5 in convective regions and ERA5 outperformed IMERG in complex terrain, and a convection-permitting regional model gave considerably more accurate totals over the mountainous west)"
  - id: beck-2017
    resource: https://doi.org/10.5194/hess-21-6201-2017
    title: "Beck, Vergopolan, Pan, Levizzani, van Dijk, Weedon and others, 2017, Global-scale evaluation of 22 precipitation datasets using gauge observations and hydrological modeling, Hydrology and Earth System Sciences 21 (record and abstract read on the Crossref registry 2026-09-15: the good performance of the fully gauge-based CPC Unified analysis is unlikely to translate to sparsely or ungauged regions, and two reanalyses obtained lower trend errors than the satellite datasets)"
  - id: derin-2016
    resource: https://doi.org/10.1175/JHM-D-15-0197.1
    title: "Derin, Anagnostou, Berne, Borga, Boudevillain, Buytaert and others, 2016, Multiregional Satellite Precipitation Products Evaluation over Complex Terrain, Journal of Hydrometeorology 17 (record and abstract read on the Crossref registry 2026-09-15: nine satellite products over nine mountainous regions including the Rocky Mountains, most underestimating wet-season and overestimating dry-season precipitation, with the value of gauge adjustment depending on the representativeness of the gauge network; the journal page sits behind a bot check)"
  - id: sun-2018
    resource: https://doi.org/10.1002/2017RG000574
    title: "Sun, Miao, Duan, Ashouri, Sorooshian and Hsu, 2018, A Review of Global Precipitation Data Sets: Data Sources, Estimation, and Intercomparisons, Reviews of Geophysics 56 (record and abstract read on the Crossref registry 2026-09-15: thirty data sets, annual land precipitation deviating by as much as 300 mm per year among products, reanalyses the most variable, the largest annual and seasonal differences in tropical oceans, complex mountain areas, northern Africa and some high-latitude regions, and reliability limited by station coverage, satellite algorithms and assimilation models; the journal page sits behind a bot check)"
  - id: gehne-2016
    resource: https://doi.org/10.1175/JCLI-D-15-0618.1
    title: "Gehne, Hamill, Kiladis and Trenberth, 2016, Comparison of Global Precipitation Estimates across a Range of Temporal and Spatial Scales, Journal of Climate 29 (record and abstract read on the Crossref registry 2026-09-15: eleven estimates compared, three high-resolution products, four climate data records and four reanalyses; high-resolution products aim at the best local snapshot, climate data records at homogeneity, reanalysis precipitation is forecast rather than assimilated and compares poorly to gauges, and annual differences over continental regions are around 0.8 mm per day; the journal page sits behind a bot check)"
  - id: lundquist-2019
    resource: https://doi.org/10.1175/BAMS-D-19-0001.1
    title: "Lundquist, Hughes, Gutmann and Kapnick, 2019, Our Skill in Modeling Mountain Rain and Snow is Bypassing the Skill of Our Observational Networks, Bulletin of the American Meteorological Society 100 (record and abstract read on the Crossref registry 2026-09-15: in mountain terrain well-configured high-resolution atmospheric models simulate annual rain and snowfall better than spatial estimates from gauge networks and significantly better than radar or satellite estimates, judged against streamflow and snow in basins across the western United States and elsewhere; the journal page sits behind a bot check)"
  - id: daly-2008
    resource: https://doi.org/10.1002/joc.1688
    title: "Daly, Halbleib, Smith, Gibson, Doggett, Taylor and others, 2008, Physiographically sensitive mapping of climatological temperature and precipitation across the conterminous United States, International Journal of Climatology 28 (record and abstract read on the Crossref registry 2026-09-15: the PRISM climate-elevation regression per cell with stations weighted by physiographic similarity, and the greatest improvement over WorldClim and Daymet in the mountainous and coastal western United States with sparse data, large elevation gradients, rain shadows, inversions and cold air drainage; the journal page sits behind a bot check)"
  - id: xia-2012
    resource: https://doi.org/10.1029/2011JD016048
    title: "Xia, Mitchell, Ek, Sheffield, Cosgrove, Wood and others, 2012, Continental-scale water and energy flux analysis and validation for the North American Land Data Assimilation System project phase 2 (NLDAS-2): 1. Intercomparison and application of model products, Journal of Geophysical Research: Atmospheres 117 (record and abstract read on the Crossref registry 2026-09-15: the increased accuracy and consistency of the surface forcing over NLDAS-1, the 1979 to 2008 retrospective window, and the largest remaining inter-model differences in the northeast, Lake Superior and the western mountains, associated with cold-season processes; the journal page sits behind a bot check)"
  - id: reichle-2017
    resource: https://doi.org/10.1175/JCLI-D-16-0570.1
    title: "Reichle, Liu, Koster, Draper, Mahanama and Partyka, 2017, Land Surface Precipitation in MERRA-2, Journal of Climate 30 (record and abstract read on the Crossref registry 2026-09-15: observation-based products correct the precipitation falling on the land surface outside the high latitudes, the corrected field is better than the model's against monthly GPCP, its diurnal cycle against three-hourly TRMM has better amplitude but less realistic phasing than the model-generated precipitation, and at high latitudes the lack of reliable precipitation observations leaves land spin-up effects in the first published year of each stream, 1980, 1992, 2001 and 2011; the journal page sits behind a bot check)"
  - id: thornton-2021
    resource: https://doi.org/10.1038/s41597-021-00973-0
    title: "Thornton, Shrestha, Thornton, Kao, Wei and Wilson, 2021, Gridded daily weather data for North America with comprehensive uncertainty quantification, Scientific Data 8 (record and abstract read on the Crossref registry 2026-09-15: Daymet V4 as a 40-year daily 1 km dataset with cross-validation uncertainty for temperature and precipitation, and a new approach to high-elevation temperature measurement biases)"
  - id: newman-2015
    resource: https://doi.org/10.1175/JHM-D-15-0026.1
    title: "Newman, Clark, Craig, Nijssen, Wood, Gutmann and others, 2015, Gridded Ensemble Precipitation and Temperature Estimates for the Contiguous United States, Journal of Hydrometeorology 16 (record and abstract read on the Crossref registry 2026-09-15: gridded precipitation is inherently uncertain from interpolation over a sparse network, measurement representativeness and measurement error, and the uncertainty is generally not carried in gridded products; the journal page sits behind a bot check)"
  - id: herold-2016
    resource: https://doi.org/10.1002/2015GL066615
    title: "Herold, Alexander, Donat, Contractor and Becker, 2016, How much does it rain over land?, Geophysical Research Letters 43 (record and abstract read on the Crossref registry 2026-09-15: a large disparity in the land mean of daily precipitation intensity among gauge, satellite and reanalysis data sets, partly reconciled by the spatial scale each grid represents; the journal page sits behind a bot check)"
  - id: tan-2019
    resource: https://doi.org/10.1175/JTECH-D-19-0114.1
    title: "Tan, Huffman, Bolvin and Nelkin, 2019, IMERG V06: Changes to the Morphing Algorithm, Journal of Atmospheric and Oceanic Technology 36 (record and abstract read on the Crossref registry 2026-09-15: motion vectors from model total precipitable water vapor let IMERG extend from the 60 N to 60 S band to the entire globe from V06; the journal page sits behind a bot check)"
  - id: henn-2018
    resource: https://doi.org/10.1016/j.jhydrol.2017.03.008
    title: "Henn, Newman, Livneh, Daly and Lundquist, 2018, An assessment of differences in gridded precipitation datasets in complex terrain, Journal of Hydrology 556 (registry record only: the Crossref record carries no abstract and the publisher page is not reachable from this environment, so only the title, authors, journal and year are cited)"
  - id: tang-2020
    resource: https://doi.org/10.1016/j.rse.2020.111697
    title: "Tang, Clark, Papalexiou, Ma and Hong, 2020, Have satellite precipitation products improved over last two decades? A comprehensive comparison of GPM IMERG with nine satellite and reanalysis datasets, Remote Sensing of Environment 240 (registry record only: no abstract on Crossref and the publisher page is not reachable from this environment, so only the title, authors, journal and year are cited)"
  - id: timmermans-2019
    resource: https://doi.org/10.1007/s00382-018-4537-0
    title: "Timmermans, Wehner, Cooley, O'Brien and Krishnan, 2019, An evaluation of the consistency of extremes in gridded precipitation data sets, Climate Dynamics 52 (registry record only: no abstract on Crossref and the publisher page answered 403, so only the title, authors, journal and year are cited)"
status: draft
stale_after: 2026-12-01
---

# Choosing a precipitation product by terrain and question

**What is being chosen.** Four products answer "how much
precipitation fell on this basin" from four different kinds of
evidence, and the evidence, not the grid spacing, is what decides
where each is trustworthy. The table is the summary the choice turns
on; each product's concept owns the details and the current record
bounds: IMERG and NLDAS-2 in this bundle, Daymet and MERRA-2 in the
provider bundle at
`knowledge/ornldaac/datasets/daymet-v4.md` and
`knowledge/gesdisc/datasets/merra-2.md` in
nasa-daac-knowledge.[^imerg][^nldas][^daymet][^merra2]

| Product | Evidence | Grid and domain | Record | Where terrain enters |
|---|---|---|---|---|
| IMERG V07 | passive-microwave constellation calibrated to the GPM combined product, infrared fill between overpasses; Final adjusted monthly to the GPCC gauge analysis, Early and Late by a climatological ratio | 0.1 degree, global (the 60 N to 60 S band before V06) | from June 2000; the Final end date and the run seams are the IMERG concept's | not at all in the retrieval; the Final adjustment is a monthly ratio at GPCC gauge density[^imerg][^tan-2019] |
| NLDAS-2 File A | the CPC gauge-only daily analysis with the PRISM orographic adjustment, disaggregated to hours by radar, CMORPH or NARR weights | 0.125 degree, conterminous United States and margins | hourly from 1979; the NLDAS-2 concept's | through the PRISM climatological ratio, a climate-elevation regression per cell[^nldas][^daly-2008] |
| Daymet V4 R1 | interpolation and extrapolation of GHCN-daily station observations with distance and elevation weights | 1 km Lambert conformal conic, continental North America, Hawaii and Puerto Rico | daily from 1980; the Daymet concept's | through the elevation weighting, with error growing where stations are sparse and relief high[^daymet][^daymet-sparse][^thornton-2021] |
| MERRA-2 | the GEOS-5 reanalysis; PRECTOTCORR corrected toward gauge and satellite products outside the high latitudes, PRECTOT the model's own | 0.625 by 0.5 degree, global | hourly and monthly from 1980; the MERRA-2 concept's | through the model's resolved orography and the correction's gauge inputs, which fade to nothing poleward of 62.5 degrees[^merra2][^merra2-corr][^reichle-2017] |

**Method.**

1. **The question first.** A budget term is a total over a polygon
   and a window and needs the product whose level is right there. An
   event series needs the product whose timing is right at the hour
   or day. The tail of the daily distribution needs a product whose
   cell represents the scale the question means. A trend needs a
   record without seams. A cold-season total needs a product that
   sees snow. The products are not ranked; each is best at one of
   these somewhere and wrong at another.
2. **The domain and the network.** Outside the conterminous United
   States NLDAS-2 does not exist, outside North America Daymet does
   not, and the choice is between IMERG and MERRA-2, both of which
   lean on gauge products for their level. Inside, the question is
   what the gauge network around the basin looks like: the
   gauge-based analyses are only as good as their stations, dense
   over most of the contiguous United States and sparse in mountains,
   Arctic Alaska and Canada, and northern Mexico, and a gauge-based
   product's good performance where it is dense is unlikely to
   translate to sparsely or ungauged regions.[^daymet-sparse][^beck-2017]
   The latitude bands that matter are written into the products:
   IMERG's Final adjustment switches undercatch scheme at 45 N over
   Eurasia; MERRA-2's land correction blends to zero between 42.5 and
   62.5 degrees and is absent poleward, so above that PRECTOTCORR is
   the model's own precipitation under another name; IMERG covered
   only 60 N to 60 S before V06 extended it to the globe with model
   motion vectors.[^imerg][^merra2-corr][^tan-2019]
3. **Complex terrain.** Precipitation in mountains is decided by the
   terrain, and the products that carry a terrain relationship are
   the gauge analyses with one built in: NLDAS-2 through PRISM, whose
   physiographic regression brought its greatest improvement over
   plain interpolation exactly in the mountainous and coastal western
   United States with sparse stations, large elevation gradients,
   rain shadows and cold-air drainage, and Daymet through its
   elevation weighting, with the cross-validation files stating the
   error where relief is high.[^nldas][^daly-2008][^daymet-sparse]
   IMERG carries no terrain relationship and its monthly gauge
   adjustment is a ratio over a GPCC cell, so satellite products over
   mountainous regions underestimate the wet season, and the value of
   the gauge adjustment depends on how representative the gauges
   are.[^imerg-orographic][^derin-2016] In the CONUS daily
   evaluation against gauge-radar analysis, IMERG outperformed the
   ERA5 reanalysis in convective regions and ERA5 outperformed IMERG
   in complex terrain, and a convection-permitting model gave
   considerably more accurate totals over the mountainous west; the
   review of mountain precipitation concludes that well-configured
   high-resolution atmospheric models now beat spatial estimates from
   gauge networks there and beat radar and satellite estimates by
   more.[^beck-2019][^lundquist-2019] MERRA-2 is a coarser model than
   those, corrected toward gauge products, and its corrected field is
   better than its model field against monthly gauge analyses; it is
   a reanalysis and not a gauge product, and reanalysis precipitation
   is forecast, not assimilated.[^reichle-2017][^gehne-2016] Assessments
   of the differences among gridded products in complex terrain exist
   and are named in the sources by their records.[^henn-2018][^tang-2020]
4. **High latitude.** North of the dense network the gauge products
   thin out: Daymet's Arctic Alaska and Canada are its sparsest
   regions and its 2020 and 2021 files were rerun for missing
   Canadian January readings, MERRA-2's land correction is gone
   poleward of 62.5 degrees and the lack of reliable observations
   there leaves spin-up effects in the first published year of each
   stream, and IMERG's retrievals over frozen surfaces are the ones
   the release notes mark down.[^daymet-sparse][^daymet-r1][^merra2-corr][^reichle-2017][^imerg]
   The review of thirty data sets places some high-latitude regions
   among the areas of largest disagreement.[^sun-2018] The check there
   is between two products that both lack gauges, and the statement
   says so.
5. **Cold season.** Snow is where IMERG's level is lowest: the
   release notes call snowfall rates over land low and ask that they
   be examined critically, and the orographic gotcha's measured
   ratios of IMERG Final to NLDAS-2 over the Colorado headwaters,
   quoted in this recipe's expected values, put the November through
   March shortfall well below the water-year one.[^imerg][^imerg-orographic]
   The reanalyses performed better in winter and the satellite
   products in summer in the CONUS daily evaluation, and the land
   models NLDAS-2 drives, with forcing whose accuracy and consistency
   its second phase raised, still disagree most in the western
   mountains and the northeast, where cold-season processes
   rule.[^beck-2019][^xia-2012] The
   gauge analyses see snow through gauges that undercatch it in wind,
   which is what the Final run's undercatch correction and the NLDAS-2
   concept's error statement both name.[^imerg][^nldas] A cold-season
   total in the conterminous United States is NLDAS-2 with IMERG
   beside it; Daymet stands in only where its cross-validation files
   for the region are read, since no Daymet anchor against either is
   recorded here and the PRISM comparison found Daymet's grids the
   weaker in the mountainous west.[^daymet-sparse][^daly-2008] Outside
   the NLDAS-2 domain the orographic gotcha names the national gauge
   analysis that covers the basin as the check; where none is at
   hand, MERRA-2 PRECTOTCORR equatorward of 42.5 degrees is the CPC
   unified gauge analysis disaggregated by the model and serves as
   that check, and poleward of 62.5 degrees it is not a gauge product
   at all, so there the pair is two products that are both models of
   a sort.[^imerg-orographic][^merra2-corr]
6. **Extremes.** A cell value is an areal mean, and the spread in
   daily intensity among gauge, satellite and reanalysis data sets is
   large and only partly reconciled by the scale each grid
   represents.[^herold-2016] IMERG at 0.1 degree and half-hourly
   resolution is the finest of the four in time and outperformed the
   ERA5 reanalysis in convective regions in the CONUS daily
   evaluation; NLDAS-2's hourly shape comes from the radar
   weights while its daily total is the gauge analysis; Daymet is a
   daily station interpolation on a fine grid whose intensity is the
   stations' smoothed by the interpolation; MERRA-2's hourly
   precipitation is the model's diurnal cycle, with the corrected
   field's phasing less realistic than the model's own.[^beck-2019][^nldas][^daymet][^reichle-2017]
   Gridded products generally carry no uncertainty for this, and an
   evaluation of the consistency of extremes across gridded sets is
   named in the sources by its record.[^newman-2015][^timmermans-2019]
7. **Long series.** Homogeneity is a property of the record, not of
   the retrieval: climate data records emphasise it over instantaneous
   accuracy, high-resolution products the reverse.[^gehne-2016] The
   seams are documented per product: IMERG's Final record ends
   2025-09-30, the three runs are three calibrations, and the V08
   transition adds dated seams; MERRA-2 is four streams joined at
   1992, 2001 and 2011 with observing-system entries that leave steps;
   Daymet's 2020 and 2021 differ between Version 4 and R1 and every
   year has 365 days; NLDAS-2 runs from 1979 on one gauge analysis
   whose network changed with time.[^imerg][^imerg-runs][^merra2-streams][^daymet-r1][^daymet-365][^nldas]
   Two reanalyses obtained lower trend errors than the satellite
   datasets in the global evaluation.[^beck-2017] A trend names its
   seams and shows the series from the second product across them.
8. **Basin means with the grid's own areas.** Daymet's kilometre is
   a projected kilometre and its cells are not one square kilometre
   off the standard parallels; MERRA-2's cells shrink toward the
   poles and no area variable ships; NLDAS-2 and IMERG are regular
   latitude-longitude grids with the same cosine
   dependence.[^daymet-lcc][^merra2-grid][^nldas][^imerg] Each basin
   mean is area-weighted on its own grid, and the time conventions
   are each product's own: NLDAS-2 stamps the hour ending at the
   stamp, Daymet drops December 31 in leap years, and MERRA-2's
   averaged collections are stamped at the half hour.[^nldas][^daymet-365][^merra2-time]

**The check.** The deliverable is the chosen product's basin series
with a second product's series over the same polygon and window, both
totals and their ratio, with the seams each crosses named. The
orographic gotcha's water-year 2023 pair over the Colorado River
basin above Lees Ferry, IMERG Final beside NLDAS-2, is the measured
example of the size the disagreement takes over snow-covered high
terrain with a dense network beside it; its ratios are this recipe's
expected values, and the gotcha holds the month-by-month table and
the fixtures that reproduce it.[^imerg-orographic] Where the two products are both
without gauges, the ratio measures agreement between two models of
the same missing observation, and the statement says that rather
than reading the agreement as skill.

**Provenance.** Every basin value quoted from this recipe names the
product, collection and run or version, the polygon with its area,
the window, the second product and the ratio. Live checks on
2026-09-15: every journal DOI above was verified against the Crossref
registry (title, authors, journal, year), and the abstracts read there
are the source of every claim attributed to a paper; the AMS, Wiley
and Copernicus records carry abstracts, the three Elsevier and
Springer records do not and the publisher pages are not reachable
from this environment, so those three are cited for their titles
only. The product facts come from this bundle's IMERG and NLDAS-2
concepts and the provider bundle's Daymet and MERRA-2 concepts at the
commit cited, and nothing was re-derived from the product pages here.

[^imerg]: this bundle's IMERG V07 dataset concept
[^imerg-orographic]: this bundle's IMERG cold-season orographic gotcha
[^imerg-runs]: this bundle's IMERG run-mixing gotcha
[^nldas]: this bundle's NLDAS-2 forcing concept
[^daymet]: the provider bundle's Daymet Version 4 R1 dataset concept
[^daymet-sparse]: the provider bundle's Daymet station-sparse gotcha
[^daymet-365]: the provider bundle's Daymet 365-day calendar gotcha
[^daymet-lcc]: the provider bundle's Daymet projection and cell-area gotcha
[^daymet-r1]: the provider bundle's Daymet R1 correction gotcha
[^merra2]: the provider bundle's MERRA-2 dataset concept
[^merra2-corr]: the provider bundle's PRECTOTCORR versus PRECTOT gotcha
[^merra2-streams]: the provider bundle's MERRA-2 stream-boundary gotcha
[^merra2-grid]: the provider bundle's MERRA-2 grid-weights gotcha
[^merra2-time]: the provider bundle's MERRA-2 time-stamp gotcha
[^beck-2019]: Beck and others, 2019, Hydrology and Earth System Sciences, doi:10.5194/hess-23-207-2019
[^beck-2017]: Beck and others, 2017, Hydrology and Earth System Sciences, doi:10.5194/hess-21-6201-2017
[^derin-2016]: Derin and others, 2016, Journal of Hydrometeorology, doi:10.1175/JHM-D-15-0197.1
[^sun-2018]: Sun and others, 2018, Reviews of Geophysics, doi:10.1002/2017RG000574
[^gehne-2016]: Gehne and others, 2016, Journal of Climate, doi:10.1175/JCLI-D-15-0618.1
[^lundquist-2019]: Lundquist and others, 2019, Bulletin of the American Meteorological Society, doi:10.1175/BAMS-D-19-0001.1
[^daly-2008]: Daly and others, 2008, International Journal of Climatology, doi:10.1002/joc.1688
[^xia-2012]: Xia and others, 2012, Journal of Geophysical Research: Atmospheres, doi:10.1029/2011JD016048
[^reichle-2017]: Reichle and others, 2017, Journal of Climate, doi:10.1175/JCLI-D-16-0570.1
[^thornton-2021]: Thornton and others, 2021, Scientific Data, doi:10.1038/s41597-021-00973-0
[^newman-2015]: Newman and others, 2015, Journal of Hydrometeorology, doi:10.1175/JHM-D-15-0026.1
[^herold-2016]: Herold and others, 2016, Geophysical Research Letters, doi:10.1002/2015GL066615
[^tan-2019]: Tan and others, 2019, Journal of Atmospheric and Oceanic Technology, doi:10.1175/JTECH-D-19-0114.1
[^henn-2018]: Henn and others, 2018, Journal of Hydrology, doi:10.1016/j.jhydrol.2017.03.008 (registry record only)
[^tang-2020]: Tang and others, 2020, Remote Sensing of Environment, doi:10.1016/j.rse.2020.111697 (registry record only)
[^timmermans-2019]: Timmermans and others, 2019, Climate Dynamics, doi:10.1007/s00382-018-4537-0 (registry record only)
