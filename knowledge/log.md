# hydrology bundle: change log

Newest first. One line per change: date, concept path, what changed, who.

_Historical note: older entries use build-era shorthand (a "close lint" is a knowledge-linter pass; red/yellow marks are nonconformant/advisory findings; check numbers refer to the linter checks documented in core/agents/knowledge-linter). The decision chains, not the labels, are what teach the standards._

- 2026-09-16 · STEWARD RE-SIGNING of
  knowledge/computations/basin-water-balance.md,
  knowledge/recipes/basin-water-balance.md,
  knowledge/recipes/nwm-gauge-confrontation.md: Maintainer review of the
  groundwater partition of the basin water balance (the edited attested
  computation concept and its recipe, re-signed after the edit) and of
  the NWM gauge confrontation recipe, merged in PR #70 after the
  coordinator's review of the chain and a fix round (the site range, the
  newly attested receipt fields, the parameter guard, the selection
  script, connected-component clustering, the sigma at spread and the
  term without the largest site). The NWM recipe is promoted to stable.
  The verified events are written on the steward's word. The new
  verified event is appended on the steward's word, the earlier events
  kept as history. (steward)

- 2026-09-15 · knowledge/computations/basin-water-balance.md and
  knowledge/recipes/basin-water-balance.md (both stable, edited and
  owing a new review; status left stable),
  knowledge/references/computations/basin_water_balance.py (0.2.0),
  knowledge/references/attesters/basin_water_balance_check.py,
  knowledge/recipes/nwm-gauge-confrontation.md (draft, no verified
  event) with its eval case evals/nwm-gauge-confrontation.yaml,
  verification/basin_water_balance.py and
  verification/fixtures/water-balance/ohio-olmsted-groundwater/ with
  its freezing script: the basin water balance extended with the
  groundwater part of the storage term by the water-table fluctuation
  method from USGS daily depth-to-water series at a well set
  (parameter 72019, unconfined wells inside the polygon with a stated
  constructed depth, 30-day end windows, wells within 2 km as one
  site, a stated specific yield with its sigma and source), reported
  as a partition of dS that leaves the residual unchanged, with every
  term carrying the stamp it came from and the receipt carrying its
  bookkeeping statements; the attester recomputes the term from the
  frozen well set, applies bar three (plausibility: the specific
  yield's bound and source, the site count, the level-change bound,
  the partition arithmetic, the part no larger than the whole), prints
  PASS or FAIL per check and carries a selftest over synthetic trees;
  the golden runs the fourth tree and the selftest, and the stored
  receipts were regenerated against the new executor hash. And a
  recipe confronting a gauge's daily flow with the National Water
  Model version 3.0 retrospective at the reach carrying the gauge,
  volume and timing scored apart, worked on the Roaring Fork at
  Glenwood Springs for calendar 2021 from a live call of the
  observations server's nwm_retrospective_streamflow (feature id
  1324997, fourteen chunks, 21 s) against the frozen 2021 gauge
  record. Sources read live the same day: the Water Data API
  collection list and the field-measurements, time-series-metadata
  and monitoring-locations collections (the well selection and site
  files); the retrospective bucket's listing (domains, the CONUS zarr
  and netcdf trees, the hourly CHRTOUT file sizes) and the chunks
  546.3 to 559.3 of the CONUS chrtout store; the Crossref records and
  abstracts of Gehman and others 2009 (10.1029/2007WR006096), Pool and
  Eychaner 1995 (10.1111/j.1745-6584.1995.tb00299.x), Crosbie and
  others 2019 (10.1029/2019WR025285) and Cosgrove and others 2024
  (10.1111/1752-1688.13184), and the Crossref record of Johnson 1967
  (10.3133/wsp1662D), whose landing page on pubs.usgs.gov the session
  could not reach, so it is cited on its registry record and no value
  is taken from it; the journal pages were not read. The groundwater
  and retrospective connector concepts, the GRACE partitioning recipe
  and the SWOT gauge confrontation recipe are linked, not repeated.
  knowledge/index.md updated. Coordinator fix round the same day: the
  concept's site range corrected (-1.5 to +2.6 m); the attester
  recomputes every reported groundwater field (millimetres, the
  specific yield bracket, the standard error, the median, minimum and
  maximum), the sigma at the spread and the term without its largest
  site, refuses an elevation parameter as the executor does, and
  prints the parameter under bar three; sites are connected components
  in both scripts; the freezing script performs the selection and
  records its counts; the receipt carries sigma_km3_at_spread, the
  sigma's components and without_largest_site; the concept names the
  standard-error assumption, the aquifer breakdown of the well set
  and the one riverbank well field that carries the term.
  (process:claude-code)
- 2026-09-15 · STEWARD SIGNING of
  knowledge/connectors/nwis-groundwater.md,
  knowledge/connectors/hydrocron-lakes.md,
  knowledge/connectors/nwm-retrospective.md: Maintainer review of the
  three connector concepts for the observations server's round three
  tools, merged in PR #67 after the coordinator's lint and fix round;
  promoted to stable. The verified event is written on the steward's
  word. (steward)

- 2026-09-15 · STEWARD SIGNING of knowledge/datasets/swot-lakes.md,
  knowledge/gotchas/swot-lake-identity-across-passes.md,
  knowledge/gotchas/swot-lake-elevation-datum.md,
  knowledge/recipes/precipitation-product-by-terrain.md: Maintainer
  review of the SWOT lake concepts and the precipitation product recipe
  seeded in PR #66 after the coordinator's lint and fix round; the
  dataset, the medium gotcha and the recipe promoted to stable, the
  high-severity lake identity gotcha keeps draft until a second review.
  The verified event is written on the steward's word. (steward)

- 2026-09-15 · knowledge/datasets/swot-lakes.md,
  knowledge/gotchas/swot-lake-identity-across-passes.md (severity
  high, eval case evals/swot-lake-identity-across-passes.yaml),
  knowledge/gotchas/swot-lake-elevation-datum.md (medium) and
  knowledge/recipes/precipitation-product-by-terrain.md authored as
  drafts, no verified event: the SWOT lake products (the Prior Lake
  Database as the prior file's p_ attributes, LakeSP obs, prior and
  unassigned, LakeAvg) as a water surface elevation and area series
  per prior lake, the two traps in keying and referencing that
  series, and a recipe for choosing among IMERG, Daymet, MERRA-2 and
  NLDAS-2 by terrain, latitude, season, scale and record length that
  cites this bundle's IMERG, NLDAS-2 and orographic concepts and the
  provider bundle's Daymet and MERRA-2 concepts by path at a pinned
  commit. Sources read live the same day: the PO.DAAC collection
  pages for SWOT_L2_HR_LakeSP_D, its obs, prior and unassigned
  sub-collections and SWOT_L2_HR_LakeAvg_D; the CMR collection
  records and granule probes for the C and D lake families
  (C3233944983, C3233942286, C3233942291, C3233942295, C3233944980,
  C2799438230, C2799438239, C2799438247, C2799438254, C2799438221 at
  POCLOUD, with the DOIs
  10.5067/SWOT-LAKESP-D, SWOT-LAKEAVG-D, SWOT-LAKESP-2.0 and
  SWOT-LAKEAVG-2.0) and the searches that found no Prior Lake
  Database collection at POCLOUD; the LakeSP and LakeAvg Product
  Description Documents (Revision C, 2025-03-07) and the Version D
  KaRIn release note (2025-04-23), all three linked from the CMR
  records; this plugin's frozen Tulare Lake bed LakeSP series; and
  the Crossref records and abstracts of Beck and others 2019 and
  2017, Derin and others 2016, Sun and others 2018, Gehne and others
  2016, Lundquist and others 2019, Daly and others 2008, Xia and
  others 2012, Reichle and others 2017, Thornton and others 2021,
  Newman and others 2015, Herold and others 2016 and Tan and others
  2019, with Henn and others 2018, Tang and others 2020 and
  Timmermans and others 2019 cited on their registry records only
  (no abstract on Crossref, publisher pages not reachable). The
  journal pages sit behind bot checks or outside the reachable
  domains and are cited on their registry records. The IMERG,
  NLDAS-2, SWOT river and Hydrocron concepts are linked, not
  repeated. knowledge/index.md updated. Severity rationale: the
  identity gotcha is high because an equality filter on the obs
  file returns a series with the right units and silent gaps, and a
  substring match returns a merged water body's average as the
  lake's, with nothing raised; the datum gotcha is medium because
  the geoid, the tide system and the Version C geoid error are
  documented behaviour whose step bites only across a family seam or
  against the catalogue reference, at a size of order the stated
  total uncertainty. Registration of the eval case in the evals
  repository's manifest is the coordinator's follow-up.
  (knowledge-seeder)
- 2026-09-15 · knowledge/connectors/nwis-groundwater.md,
  knowledge/connectors/hydrocron-lakes.md,
  knowledge/connectors/nwm-retrospective.md drafted for the three
  hydrology tools of the observations server's round three
  (nwis_groundwater_levels, hydrocron_lake_timeseries,
  nwm_retrospective_streamflow; core issue 43): the Water Data API
  probed live (no groundwater collection; field-measurements holds the
  readings; the parameter codes and their datums), the Hydrocron lake
  path probed live field by field (the documentation host unreachable
  from the session, stated in the concept), the retrospective's zarr
  store read and decoded at the Lees Ferry reach against the USGS
  daily record; status draft pending steward review (drafting
  session, connector seed)

- 2026-09-14 · STEWARD RE-SIGNING of
  knowledge/gotchas/grace-basin-below-resolution-floor.md,
  knowledge/gotchas/snow-cover-ndsi-is-not-fraction.md: second
  maintainer review recorded on the maintainer's explicit instruction in
  the coordinator session, the maintainer having reviewed the concept;
  promoted to stable under the two-review rule for high severity, with
  the playbook's preference for a different second reviewer noted, and a
  provider confirmation still invited The new verified event is appended
  on the steward's word, the earlier events kept as history. (steward)

- 2026-09-14 · STEWARD SIGNING of
  knowledge/datasets/modis-viirs-snow-cover.md,
  knowledge/gotchas/snow-cover-cloud-persistence-and-gap-filling.md,
  knowledge/gotchas/snow-cover-is-not-swe.md,
  knowledge/gotchas/snow-cover-overpass-time-and-compositing.md,
  knowledge/gotchas/snow-cover-snow-cloud-confusion.md,
  knowledge/gotchas/snow-cover-ndsi-is-not-fraction.md: maintainer's
  review of PR 61 recorded on the maintainer's standing instruction for
  round two of seeding; the dataset concept and the four non-high
  gotchas promoted to stable; snow-cover-ndsi-is-not-fraction (high
  severity) keeps draft with this first review until a second human
  review, per the two-review rule. The verified event is written on the
  steward's word. The verified event is written on the steward's word.
  (steward)

- 2026-09-14 · knowledge/datasets/modis-viirs-snow-cover.md,
  knowledge/gotchas/snow-cover-ndsi-is-not-fraction.md (severity
  high, eval case evals/snow-cover-ndsi-is-not-fraction.yaml),
  knowledge/gotchas/snow-cover-cloud-persistence-and-gap-filling.md
  (medium), knowledge/gotchas/snow-cover-snow-cloud-confusion.md
  (medium), knowledge/gotchas/snow-cover-overpass-time-and-compositing.md
  (medium) and knowledge/gotchas/snow-cover-is-not-swe.md (low)
  authored as drafts, no verified event: the daily NDSI snow cover
  products MOD10A1 version 61, MOD10A1F version 61 and VNP10A1
  version 2 at NSIDC DAAC, and the traps in reading them. Sources read
  live the same day: the three NSIDC product pages and their user
  guides (MOD10A1 v61 of December 2021, MOD10A1F v61 of December
  2021, VNP10A1 v2 of January 2026), the MODIS Snow Products
  Collection 6.1 User Guide and the SNPP/JPSS1 VIIRS Snow Cover
  Products Collection 2 User Guide, the NSIDC help articles on NDSI
  snow cover against FSC, on VIIRS against MODIS and on merging
  collections, the NSIDC SNODAS page, the CMR collection records for
  the family (C2565093311, C3028765772, C3173441659 and the Aqua,
  JPSS and gap-filled siblings at NSIDC_CPRD) with the newest granule
  of each daily collection, and the Crossref records and abstracts of
  Hall and Riggs 2007, Riggs and Hall 2020, Hall and others 2010 and
  2019, Riggs, Hall and Roman 2017, Salomonson and Appel 2004, Hall,
  Riggs and Salomonson 1995 and Hall and others 2002. The three
  product DOIs resolve through doi.org to the product pages and are
  not Crossref records; the Elsevier journal pages sit behind a bot
  check and are cited on their Crossref records. The SNODAS connector
  and gotcha are linked, not repeated. knowledge/index.md updated.
  Severity rationale: the NDSI gotcha is high because value over 100
  times area runs silently on the 8-bit field and returns a number
  with the right units and the wrong meaning; the three medium
  gotchas are documented product behaviour whose trap bites through
  a reading the file itself contradicts (an age field, a flag bit, a
  pointer field); the SWE gotcha is low because the index has no
  length unit and a units check catches the category error.
  (knowledge-seeder)
- 2026-09-13 · STEWARD SIGNING of knowledge/recipes/grace-basin-tws.md,
  knowledge/gotchas/grace-tws-is-total-storage.md,
  knowledge/gotchas/grace-scale-factors-once-and-for-hydrology.md,
  knowledge/gotchas/grace-basin-below-resolution-floor.md: maintainer's
  review of PR 57 recorded on the maintainer's instruction; the recipe
  and the two medium gotchas promoted to stable;
  grace-basin-below-resolution-floor (high severity) keeps draft with
  this first review until a second human review, per the two-review rule
  The verified event is written on the steward's word. (steward)

- 2026-09-13 · knowledge/recipes/grace-basin-tws.md,
  knowledge/gotchas/grace-basin-below-resolution-floor.md (severity
  high, eval case evals/grace-basin-below-resolution-floor.yaml),
  knowledge/gotchas/grace-tws-is-total-storage.md (medium) and
  knowledge/gotchas/grace-scale-factors-once-and-for-hydrology.md
  (medium) authored as drafts, no verified event: the hydrology side of
  GRACE terrestrial water storage, built on the PO.DAAC provider
  bundle's mascon dataset concept and its four GRACE gotchas, which are
  cited by path and not copied. Sources read live the same day: the
  PO.DAAC collection page for
  TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4, the CMR collection and
  granule records (C3195527175-POCLOUD, one granule through July
  2026), the collection's virtual dataset reference file in the public
  bucket (the variable names lwe_thickness, uncertainty, land_mask,
  mascon_ID, scale_factor and GAD with their attributes, the 2004 to
  2009 baseline and the 33 missing months), the JPL mascon release
  note, the RL06 month list, and the Crossref records and abstracts of
  Watkins and others 2015, Wiese and others 2016, Landerer and Swenson
  2012, Scanlon and others 2016 and Joodaki and others 2014. The
  mascon area the floor gotcha quotes is the one the basin water
  balance computation owns. The GRACE Tellus data pages returned 404;
  the Wiley journal pages sit behind a bot check. knowledge/index.md
  updated. Severity rationale: the total-storage gotcha is medium
  because the total-storage nature of the measurement is documented
  product behaviour and the trap bites through an understated
  uncertainty on a residual built with a second product, not through a
  silently wrong single-product number; the gain-factor gotcha is
  medium because the factors are an optional documented field and the
  trap bites through a misapplied option (twice, the wrong set, the
  wrong surface), the unscaled series being what the product delivers.
  FOR THE MAINTAINER: two stable concepts disagree on the storage
  term's formal error, knowledge/computations/basin-water-balance.md
  divides the area-weighted per-mascon sigma by the square root of the
  mascon count while the provider dataset concept says mascon errors
  are correlated and basin averages quote the product's guidance, not
  sqrt(N); the recipe states the provider's rule and neither stable
  concept was edited. (knowledge-seeder)
- 2026-09-12 · every dataset, gotcha, recipe and computation: `spheres`
  added to the frontmatter: hydrosphere throughout; hydrosphere with
  atmosphere on the IMERG and NLDAS-2 concepts, with cryosphere on the
  SNODAS gotcha and the drought anatomy recipe, with geosphere on the
  GRACE groundwater partitioning. The key classifies the claim by
  Earth science sphere (ADR A in the marketplace repository) and sits
  outside the signed text, so nothing owes a re-sign. No claim
  changed. (claude-code)
- 2026-09-08 · STEWARD RE-SIGNING of
  knowledge/datasets/swot-river-lake.md,
  knowledge/gotchas/hydrocron-collection-default.md,
  knowledge/recipes/swot-gauge-confrontation.md: signed on the steward's
  word: the SWOT concept re-signed for the SWORD prior dependence and
  the collection default, and the two drafts from the confrontation work
  The new verified event is appended on the steward's word, the earlier
  events kept as history. (steward)

- 2026-09-08 · knowledge/gotchas/hydrocron-collection-default.md and
  knowledge/recipes/swot-gauge-confrontation.md authored as drafts, no
  verified event, with the confrontation fetch and scoring scripts, the
  frozen Baton Rouge pair and the golden
  verification/swot_gauge_confrontation.py.
  knowledge/datasets/swot-river-lake.md gained two dated facts and OWES
  A RE-SIGN: the discharge variants rest on gauge-informed SWORD priors,
  so discharge against a gauge is a consistency check while elevation is
  a confrontation; and Hydrocron picks a collection when the caller does
  not. Measured and recorded on open-science-pillars/marketplace issue
  76. At reach 74210000331 the two product versions share no timestamp
  and differ by up to 7.4 m, and the older one puts the Mississippi
  three metres below the geoid at Baton Rouge, which the gauge says is
  not where the river is. The confrontation over calendar 2024, 50 of 52
  passes paired within 15 minutes: on changes, mean error +0.0019 m
  [-0.1062, +0.1101], RMSD 0.3823 m, correlation +0.9567 against a gauge
  change spread of 1.1959 m; the level difference is -0.2429 m and is
  published as a level difference containing an uncited datum offset
  rather than as a bias. The effective sample size is capped at the
  count, because differencing induces negative lag-1 correlation and an
  uncapped formula claimed 130 from 49 changes.

- 2026-09-08 · knowledge/datasets/reclamation-area-capacity.md,
  knowledge/gotchas/swot-gauge-datum-mismatch.md and
  knowledge/recipes/reservoir-ledger.md authored as drafts, no verified
  event, with the reservoir-ledger skill, the freeze and ledger scripts
  under verification/fixtures/, the six frozen captures and the 2018
  survey table, and the golden verification/reservoir_ledger.py.
  Measured and recorded on open-science-pillars/marketplace issue 75.
  Lake Powell, water year 2023, on NAVD88 against the 2018 table: pool
  3532.00 to 3576.10 ft, storage 7,534,061 to 10,527,321 acre-feet, a
  change of +2,993,260 (+3.692 km3); gauged inflow 11,935,172 and
  outflow 8,730,367, so the residual is -211,545 acre-feet, 1.8 per
  cent of inflow, and it is reported rather than closed. The inflow
  gauges span 82.2 per cent of the drainage above the outlet. The datum
  is sourced twice over: the gauge publishes both national datums and
  their difference over 365 days is 2.9148 ft, matching the table's own
  two columns. Read correctly on either datum the opening level agrees
  to 589 acre-feet; crossed, it is wrong by 170,580, while the change
  is wrong by only 51,020, which is why the mistake hides in a ledger
  that reports changes. The satellite comparison is refused: SWOT is
  geoid referenced and the geoid to NAVD88 offset was not sourced, so
  the same pass gives -1.497 m or -0.582 m depending on which gauge
  series it is subtracted from and neither is stated as a measurement.

- 2026-09-08 · STEWARD SIGNING of knowledge/connectors/snodas-nsidc.md,
  knowledge/gotchas/snodas-not-a-budget-term.md,
  knowledge/recipes/drought-anatomy.md,
  knowledge/datasets/usgs-peaks.md,
  knowledge/gotchas/peaks-two-series-one-response.md,
  knowledge/gotchas/screening-fit-is-not-bulletin-17c.md,
  knowledge/recipes/event-reconstruction.md: signed on the steward's
  word after the drought anatomy panels were shown: the three drought
  concepts, the three flood frequency concepts merged in pull 44, and
  the event reconstruction recipe merged in pull 43 The verified event
  is written on the steward's word. (steward)

- 2026-09-08 · knowledge/connectors/snodas-nsidc.md,
  knowledge/gotchas/snodas-not-a-budget-term.md and
  knowledge/recipes/drought-anatomy.md authored as drafts, no verified
  event, with the drought-anatomy skill, the panel assembler and two
  fetchers under verification/fixtures/, the five frozen panels of the
  Colorado above Lees Ferry for water years 2021 and 2023, and the
  golden verification/drought_anatomy.py. Measured and recorded on
  open-science-pillars/marketplace issue 74. SNODAS is registered in
  the catalog with a DOI and an ends-at-present flag and has zero
  granules for any window including none at all, so the route is a
  dated directory path over plain HTTPS with no credential and an
  agent that searches concludes the data is missing. Its eight layers
  are named by codes that do not describe them (11038 is a temperature
  and 11044 is melt) and the scale differs between layers by three
  orders of magnitude, so the header packed beside each layer is the
  authority. The distributor's line is narrower than a ban: not
  recommended for quantitative water budget analysis, while summing
  over an area to compare periods is reasonable, so the panel is
  comparative and the budget term is refused. The worked comparison:
  precipitation 257.2 against 320.4 mm, peak basin-mean snow water
  equivalent 64.8 against 163.1 mm, mean discharge 11,435 against
  12,059 ft3/s at an outlet below Glen Canyon Dam, and storage moving
  -0.50 cm across the drought year against +4.78 cm across the wet
  one. The panels disagree about the drought's size by more than an
  order of magnitude and the regulated one barely shows it, which is
  why the recipe refuses a single index.

- 2026-09-07 · knowledge/datasets/usgs-peaks.md and
  knowledge/gotchas/{peaks-two-series-one-response,
  screening-fit-is-not-bulletin-17c}.md authored as drafts, no verified
  event, with the load-peaks skill, the WATSTORE export and screening
  fit in verification/fixtures/load_peaks.py, three frozen peak records
  under verification/fixtures/peaks/ and the golden
  verification/peaks_export.py. Measured and recorded on
  open-science-pillars/marketplace issue 73. The qualifier vocabulary
  was enumerated over 134,722 rows in seven regions (34 codes, none of
  them documented in the API schema, which declares the field a string
  while the server returns an array), and its mapping to the WATSTORE
  qualification codes was derived by aligning the collection against
  the file the agency's own writer produces for 42 gauges rather than
  recalled: 15 codes map, 19 have no peak-file equivalent, and Bd, Bm,
  F and R are emitted by that writer without appearing in the manual's
  table. Over 3,525 aligned rows no value disagreed by more than
  0.5 ft3/s; the qualifiers disagreed on 7 rows at one gauge, where the
  retiring file carries a regulation code the collection does not. One
  response holds two series: at the worked gauge 130 discharge peaks
  from 1896 and 140 stage peaks from 1796, so an unfiltered row count
  nearly doubles the record. A peak whose month or day is unknown still
  comes back with a `time`, and the 1884 Lees Ferry peak, the largest
  in that record, is dated 1884-01-01 while its own qualifiers say the
  month and day are unknown. The mapping is worth deriving because the
  frequency program acts on codes 3, 4, 6, 7, 8 and C: it excludes
  regulated and urbanized peaks unless asked, and ignores historic
  peaks without a historic period. The export matches the agency's file
  byte for byte over the columns that program reads.

- 2026-09-07 · knowledge/recipes/event-reconstruction.md authored as a
  draft, no verified event, with the reconstruct-event skill, three
  fetch scripts, the five frozen panels of the Tulare Lake reflood of
  2023 under verification/fixtures/ and the golden
  verification/event_reconstruction.py beside them. The DSWx concepts
  the recipe cites are in the provider bundle
  (open-science-pillars/nasa-daac-knowledge pull 111). Measured and
  recorded on open-science-pillars/marketplace issue 72: surface water
  peaks at 500.0 km2 on 2023-06-17, 5.1 per cent of the bed, and is
  still 407.7 km2 on 2023-08-29; the radar product has zero granules
  for the whole event; IMERG Late overstated January, the wettest
  month, by 51 per cent against Final; the four gauges with a 2023
  record see between 23 and 92 per cent of their rivers and none of
  the inflow that filled the lake; the Central Valley storage rose
  46.9 cm between October 2022 and March 2023 at 1.40 mascons, while
  the bed at 0.09 of a mascon has no storage number; and SWOT observed
  the lake complex 17 times from 2023-07-30, after the peak. Five
  defects were found and fixed while building it, four of them in this
  plugin's own fetch scripts: an outside-polygon marker sharing the
  product's fill value, overlapping tiles inflating every area by a
  factor of 2.4, a granule cap that truncated the record two days
  after the peak, and a lake panel that tracked the hydrologic unit
  rather than the lake and so mixed a 53 m valley floor with 615 m
  reservoirs. (claude-code/fable-5)

- 2026-09-07 · STEWARD SIGNING of
  knowledge/computations/basin-water-balance.md,
  knowledge/recipes/basin-water-balance.md: the steward's first verified
  event on the basin water balance and its recipe, on the steward's
  explicit word, with status promoted from draft to stable and the index
  rows updated to match The verified event is written on the steward's
  word. (steward)

- 2026-09-07 · knowledge/recipes/basin-water-balance.md authored as a
  draft, no verified event, with the basin-water-balance skill, the
  golden verification/basin_water_balance.py and three eval cases in
  evals/. The refusal language in the computation concept, the recipe
  and the skill was strengthened after a measured trial refused the
  storage term correctly and then produced a closure by another route:
  below the footprint floor no residual follows by any route,
  including a hand calculation of P minus ET minus Q that leaves the
  storage term out. The three loading skills now say that a
  plugin-relative path resolves under the plugin's own root, which
  cut a whole class of wasted work in the measurement and is true for
  an installed plugin as well. All three cases measure 5 of 5 at
  N=5 under enforced trial isolation, and evals/RESULTS.md keeps the
  four earlier runs beside them because each one's failure is the
  evidence for a fix that followed it: a judge that discarded a
  verdict it had been handed, an eval runner that let a trial read
  outside its workspace, skills that did not say where their fixtures
  live, and a turn budget set for one kind of tooling.
  (claude-code/fable-5)

- 2026-09-07 · knowledge/computations/basin-water-balance.md authored as
  a draft, no verified event, with its sanctioned executor
  (knowledge/references/computations/basin_water_balance.py) and
  attester (knowledge/references/attesters/basin_water_balance_check.py),
  the frozen input trees for three basins over water year 2023 under
  verification/fixtures/water-balance/, and the three receipts beside
  them. The first attested computation in this bundle. The footprint
  floor is derived from the mascon product's own geometry rather than
  remembered: 111,266 km2, the median mostly-land mascon, a 334 km
  square. Measured for water year 2023: the Ohio at Olmsted closes at
  +70.174 km3 against a combined sigma of 96.874 (+0.72 sigma), the
  Colorado above Lees Ferry at -19.117 against 19.165 (-1.00 sigma, the
  outlet flagged regulated and the transmountain exports missing for
  want of a sourced number), and the Roaring Fork is refused on the
  storage term at 3.4 per cent of one mascon. The loader for
  evapotranspiration gained a coverage guard and a multi-tile route in
  the same change, after it was found returning a basin mean for the
  Lees Ferry polygon from a window covering three per cent of it.
  (claude-code/fable-5)

- 2026-09-07 · STEWARD SIGNING of knowledge/datasets/mod16a2gf.md,
  knowledge/connectors/openet-api.md,
  knowledge/gotchas/mod16-fill-over-water-barren-urban.md,
  knowledge/gotchas/mod16-composite-to-month.md,
  knowledge/gotchas/openet-area-cap.md,
  knowledge/gotchas/openet-provisional-window.md,
  knowledge/gotchas/openet-monthly-not-the-daily-sum.md: the steward's
  first verified event on the seven evapotranspiration concepts, on the
  steward's explicit word, with status promoted from draft to stable and
  the index rows updated to match. The verified event is written on the
  steward's word. The dataset and connector concepts keep upstream:
  pending, since no provider bundle for LP DAAC exists and OpenET is not
  a DAAC product. (steward)

- 2026-09-06 · knowledge/datasets/mod16a2gf.md,
  knowledge/connectors/openet-api.md,
  knowledge/gotchas/mod16-fill-over-water-barren-urban.md (high, eval
  case mod16-fill-over-water-barren-urban),
  knowledge/gotchas/openet-area-cap.md (high, eval case
  openet-area-cap), knowledge/gotchas/mod16-composite-to-month.md,
  knowledge/gotchas/openet-provisional-window.md and
  knowledge/gotchas/openet-monthly-not-the-daily-sum.md authored as
  drafts, no verified event, with the load-et skill, its loader and
  fetch script, two MOD16 basin-window fixtures (the Roaring Fork and
  a Lake Powell box, calendar 2023), two recorded OpenET ensemble
  responses over a HUC12 inside the Roaring Fork, and the golden
  beside them. Facts checked against the MOD16 user guide, the LP DAAC
  catalog, the CMR records, the granule metadata and the OpenET
  documentation on 2026-09-06 and recorded on
  open-science-pillars/marketplace issue 69: the product writes seven
  fill codes where the header lists one and the catalog page a third
  value; the last composite of each year is 5 or 6 days; the
  gap-filled record only advances at year end (last composite
  A2025361) while the MOD16A2 companion reaches within three weeks of
  the present; the OpenET per-request cap refuses every fixture basin;
  the ensemble is a MAD-filtered mean, not a median. Measured over the
  fixtures: 494.60 mm for the Roaring Fork in 2023, 521.12 mm for the
  Capitol Creek unit against the OpenET ensemble's 724.60 mm, and
  168.72 mm over a unit half covered by Lake Powell, where reading the
  fill codes as zero would give 80.39 mm instead. The
  monthly-against-daily concept records a disagreement found while
  making that comparison: over two units the monthly ensemble repeats
  one value for January through March 2023 while the daily ensemble
  varies and sums to a third less. The dataset concept carries
  upstream: pending, since no provider bundle for LP DAAC exists yet.
  (claude-code/fable-5)

- 2026-09-06 · STEWARD SIGNING of knowledge/datasets/imerg-v07.md,
  knowledge/datasets/nldas2-forcing.md,
  knowledge/connectors/gesdisc-earthaccess.md,
  knowledge/gotchas/imerg-run-mixing.md,
  knowledge/gotchas/imerg-cold-season-orographic-underestimation.md: the
  steward's first verified event on the five precipitation concepts, on
  the steward's explicit word, with status promoted from draft to stable
  and the index rows updated to match. The two dataset concepts keep
  upstream: pending, since no provider bundle for GES DISC exists yet.
  (steward)

- 2026-09-06 · knowledge/datasets/imerg-v07.md,
  knowledge/datasets/nldas2-forcing.md,
  knowledge/connectors/gesdisc-earthaccess.md,
  knowledge/gotchas/imerg-run-mixing.md (high, eval case
  imerg-run-mixing beside it) and
  knowledge/gotchas/imerg-cold-season-orographic-underestimation.md
  (high, eval case imerg-cold-season-orographic-underestimation)
  authored as drafts, no verified event, with the load-precipitation
  skill, its loader and fetch script, four basin-window fixtures over
  the Lees Ferry polygon (IMERG Final water year 2023, IMERG Late
  October 2022 and October 2023, NLDAS-2 forcing water year 2023) and
  the golden beside them. Facts checked against the catalog, the
  granule metadata, the V07 release notes and the GPM V08 transition
  notices on 2026-09-06 and recorded on
  open-science-pillars/marketplace issue 68: the Final record ends
  2025-09-30 and the near-real-time calibration changed 2026-03-01
  (both carried as dated seams with a stale_after of 2026-12-01);
  Late exceeds Final by 53 per cent over the basin for October 2022;
  IMERG Final is 0.86 of the NLDAS-2 gauge-based total for the water
  year and 0.68 for November through March (1.06 from April through
  September); V07 includes microwave retrievals over frozen surfaces with a
  reduced quality index rather than screening them, so the
  cold-season failure is an underestimate with values present, and
  NLDAS-2 forcing is the check. The two datasets carry upstream:
  pending, since no provider bundle for GES DISC exists yet.
  (claude-code/fable-5)

- 2026-09-06 · STEWARD SIGNING of knowledge/connectors/nldi-basin.md,
  knowledge/datasets/usgs-wbd.md, knowledge/gotchas/nldi-unsnapped-point.md
  and knowledge/gotchas/usgs-terminal-basin-no-outlet.md on the
  steward's explicit word: first verified event on each, status
  promoted from draft to stable. In the same change nldi-basin.md and
  nldi-unsnapped-point.md record the splitCatchment retry of 19:08 to
  19:14 UTC (the route still 502 on all three gauges; the process
  behind it reachable directly but timing out on its own upstream
  call) and the direct split-process result at the raw gauge
  coordinate (0.006 km2, no basin); the split effect on the fixture
  basins is still owed. (steward)

- 2026-09-06 · knowledge/connectors/nldi-basin.md,
  knowledge/datasets/usgs-wbd.md, knowledge/gotchas/nldi-unsnapped-point.md
  (high, eval case nldi-unsnapped-point beside it) and
  knowledge/gotchas/usgs-terminal-basin-no-outlet.md (medium) authored
  as DRAFTS from live probes of the NLDI, the Water Data API
  monitoring-locations collection and the Watershed Boundary Dataset
  service (three gauge traces against published drainage areas, the
  1 km offset table around 09085000, the Tulare Lake Bed union); the
  NLDI hydrolocation and splitCatchment routes were in an outage for
  the whole probe window, recorded as dated fact in the connector
  concept with the split effect owed. The delineate-basin skill, its
  script, four basin fixtures and a golden landed beside them.
  (claude-code/fable-5; unsigned)

- 2026-09-06 · STEWARD RE-SIGNING of knowledge/recipes/drought-index.md:
  drought-index recipe re-signed after its rewrite in the Water Data API
  vocabulary (approval as the gate, qualifier as disclosure; expected
  values re-measured identical on the migrated fixtures) The new
  verified event is appended on the steward's word, the earlier events
  kept as history. (steward)

- 2026-09-06 · STEWARD RE-SIGNING of knowledge/connectors/usgs-water.md,
  knowledge/datasets/nwis-streamflow.md, knowledge/gotchas/nwis-
  provisional-data.md: Steward signature on the three USGS concepts as
  merged for the Water Data API: the connector's endpoints, paging, key,
  depth, rate-limit and legacy-host facts; the dataset's approval_status
  and qualifier vocabulary; the gotcha's approval-beside-qualifier
  mechanism. Signed at the steward's instruction after the merge. The
  new verified event is appended on the steward's word, the earlier
  events kept as history. (steward)

- 2026-09-06 · THE USGS CONCEPTS MOVE TO THE WATER DATA API.
  connectors/usgs-water.md rewritten on the probed facts of
  api.waterdata.usgs.gov (collections, cursor paging with no
  server-side total, the optional key as X-Api-Key from API_USGS_PAT,
  keyed rate-limit headers vs none unkeyed, no retry on 429, the
  continuous collection one rolling year deep, daily to 1921) with
  the legacy waterservices.usgs.gov host kept as a dated deprecation
  fact (decommission window 2026-11 through 2027-02) and stale_after
  moved to 2026-11-01, the opening of that window; the server source
  pinned to the core commit that carries the migrated tools.
  datasets/nwis-streamflow.md: structure paragraph restated in the
  new API's vocabulary (approval_status Approved/Provisional beside a
  separate qualifier list; ESTIMATED days are still Approved), resource
  and version moved to the new API via dataretrieval 1.3.0, the
  legacy one-column layout kept as a dated note. gotchas/
  nwis-provisional-data.md: the qualifier vocabulary as the new API
  returns it, the 2026-07-05 legacy observation kept beside the
  2026-09-06 one; the trap is unchanged. All three edited after their
  signatures and owe one under the merge-then-sign rule; the steward
  signs after the merge. The five parquet fixtures were refetched from
  the new API in a documented schema (verification/fixtures/README.md;
  the calendar-2023 Lees Ferry fixture matched the legacy capture
  value for value) and every golden anchor re-measured identical.
  (claude-code, for the steward)
- 2026-09-05 · STEWARD RE-SIGNING of
  recipes/grace-groundwater-partitioning.md at 20:22:37Z, entered on
  the steward's explicit instruction. The wording pass that replaced
  specification section numbers with the rules' names edited the body
  after the 2026-09-05T04:54:00Z signature, so the recipe owed a
  signature under the merge-then-sign rule; the canonical repository's
  tools/signature_check.py found the debt by the signing commit. The
  steward read the diff and signed again, the earlier events kept as
  history. (steward)
- 2026-09-04 · STEWARD RE-SIGNING of
  recipes/grace-groundwater-partitioning.md. The retirement of the
  pinned copies (row below) replaced the recipe's four relative links
  into the copy with the provider concepts' bundle paths in text, an
  edit after the 2026-07-06 signature, so the recipe owed a signature
  under the merge-then-sign rule (SPEC 5.4); the canonical
  repository's tools/signature_check.py found the debt by the signing
  commit. The steward read the diff and signed again at
  2026-09-05T04:54:00Z, the earlier event kept as history. (steward)
- 2026-09-04 · THE PINNED PO.DAAC COPIES ARE RETIRED: snapshot-podaac/
  (three GRACE concepts at pin 24b27927c387) and snapshot.yaml deleted.
  The provider bundle reaches an install only as the
  nasa-daac-knowledge dependency (declared 2026-09-04, floor
  >=2026.9.1); the grace-groundwater skill, hydro-scout and the README
  cite the concepts by bundle path (knowledge/podaac/...), which
  consult-knowledge resolves through the installer's record; this
  index loses its snapshot section. POST-SIGNATURE EDIT, flagged under
  the merge-then-sign rule (SPEC 5.4):
  recipes/grace-groundwater-partitioning.md (stable, signed
  2026-07-06) had four relative links into the copy; each becomes the
  provider concept's bundle path in text, no other change. It owes a
  fresh signature once merged. (build assistant, steward review at
  merge)
- 2026-09-04 · STEWARD RE-SIGNING of the two connector concepts
  (connectors/hydrocron-swot.md, usgs-water.md). Each had gained its
  citation block on 2026-09-01 after the steward's signature of that
  day (hydrocron-swot's provenance note also changed then), so each
  owed a signature under the merge-then-sign rule (SPEC 5.4); the
  canonical repository's new tools/signature_check.py found the debt
  by the signing commit, the steward read both diffs and signed again
  at 2026-09-05T00:17:00Z, the earlier event kept as history. (steward)
- 2026-09-04 · STEWARD SIGNING and a Variants section.
  datasets/swot-river-lake.md gains a Variants section from the CMR
  collection sweep and granule probe of 2026-09-04: the 28 HR Level 2
  collections and the Level 4 discharge product with their concept
  ids, the C and D family holdings and bounds (C stops at cycle 032,
  2025-05-03; D carries the cal/val phase and forward processing), and
  the granule naming; the version field and the cal/val bullet under
  Known issues now say what the probe showed, and a cmr-sweep source
  carries the query. The inventory the deleted swot-hydro skill
  reference used to hold lives here now, so the scout resolves
  ShortNames from the concept. Re-signed at 22:36:00Z on the steward's
  instruction, covering the re-sourcing in the row below as well.
  gotchas/swot-reach-node-scope.md re-signed at 22:36:00Z on the same
  instruction after that re-sourcing; no text changed. stale_after
  untouched on both. (human:PaulMRamirez, recorded by the build
  assistant)
- 2026-09-04 · the three PO.DAAC copies under snapshot-podaac/ are
  declared in snapshot.yaml (SPEC 5.7, include form) and re-pinned
  from 1b8dd064d68d to the steward's signing commit 24b27927c387;
  the files were byte-identical at both pins, so no text changed.
  datasets/swot-river-lake.md and gotchas/swot-reach-node-scope.md
  carry `upstream: pending` (PO.DAAC product facts with no canonical
  counterpart yet); the gotcha's attribute-scope claim is re-sourced
  to the dataset concept's Structure section in place of the swot-hydro
  skill reference, which is deleted (it mirrored the concept). Both
  edits touch signed text: a re-sign is owed on each. evals/SCHEMA.md
  is now the pointer to the eval authoring guide; build labels left
  the verification headers, the eval note and this log. Checked by
  tools/sync_check.py in the canonical repository: OK at the pin.
  (build assistant; the steward's merge is the review)
- 2026-09-01 · both connector concepts gain citation blocks (USGS's
  suggested NWIS citation with its mandatory access date and DOI
  10.5066/F7P55KJN; the SWOT river product Version D DOI beside the
  Hydrocron software DOI), each verified against the authority this
  day; the Hydrocron provenance note now points at the demonstrated
  liftable file rather than a promise. Added after the concepts'
  verification events; the steward's merge is the review. (drafted by
  build assistant)
- 2026-09-01 · steward review passed: both connector concepts
  (usgs-water, hydrocron-swot) verified (verified_by
  human:PaulMRamirez) and promoted draft to stable
- 2026-09-01 · two connector concepts land with the observations MCP
  server (core repo): USGS NWIS gauges (units are the trap: cubic
  feet per second, feet, leading-zero site ids) and PO.DAAC Hydrocron
  SWOT river series (EGM2008 geoid, negative fill values, SWORD
  identifiers; wraps their public API, not their code, and the tool
  group is separable so the archive can take it upstream). Probed
  live 2026-09-01; CONNECTORS.md gains the disclosure section and
  .mcp.json runs the server from a commit-pinned URL. (drafted by
  build assistant; steward review pending)
- 2026-08-31 · OKF v0.2 MIGRATION of this bundle, which the original
  migration missed: all ten native concepts moved to the v0.2
  vocabulary (timestamp to generated events, status verified to stable,
  verified_by to a verified event, evidence to sources with footnote
  joins in the bodies, stale_after added). The steward signatures were
  CARRIED ACROSS on the steward's explicit direction, matching how the
  canonical bundle was migrated: each concept's existing
  `verified_by: OSP steward review` becomes
  `verified: { by: human:PaulMRamirez, at: <its original date> }`, so
  the review that already happened stays visible to a v0.2 consumer.
  No new signature was created. The three pinned podaac copies were
  re-synced byte-identical from canonical (a0c84fff959f, eight weeks
  stale and pre-migration, to 1b8dd064d68d), which brought them to
  v0.2 as a side effect. check_okf_v02: zero errors, and the bundle
  reads as thirteen human-reviewed concepts where it previously read
  as thirteen unverified ones.
- 2026-07-06 · steward addition: re-synced grace-fo-mascons snapshot from canonical (mascon-resolution/small-basin caveat); nwis-streamflow gains the rating-revision trigger (ratings remade after floods and channel shifts).

- 2026-07-06 · steward review PASSED: the 1 migration-draft recipe (grace-groundwater-partitioning) promoted draft to status: verified (verified_by OSP steward review); placeholder evidence replaced with resolving sources (NOAA CPC/NCEI/PSL for indices, published DOIs, TEOS-10, USGS, DataCite, pymannkendall, GRACE JPL, the ECCO variable catalog).

- 2026-07-05 · recipes/grace-groundwater-partitioning.md authored
  (status: draft) during the knowledge-coupling migration of
  skills/grace-groundwater; it single-sources the hydrology-side
  inference chain (partitioning residual, subtrahend products,
  uncertainty structure, basin-vs-effective-resolution and gap/GIA
  trend caveats) previously inlined in the skill; skill rewritten to
  defer (discover-by-glob consult step) and keep only the residual-not-a-
  measurement hard refusal; evidence is the internal relocation note,
  needs a steward evidence link before verified

- 2026-07-05 · snapshot-podaac/ provenance re-pinned to the canonical
  home per §5.7: open-science-pillars/nasa-daac-knowledge (podaac/),
  commit a0c84fff959f (previously ocean-science@1896335d083e);
  byte-identity verified by the canonical repo's sync_check, run
  green 2026-07-05; index.md provenance block updated
- 2026-07-05 · ERRATUM (steward-approved): the reservoir recipe's 2023
  minimum was labeled February; the daily data place it April 13-14
  (3,519.5 ft; February's low was 3,520.5). Discovered by the
  end-to-end run of the recipe, which reproduced all numeric anchors and contradicted
  only this label. Recipe, golden print label, and fixtures README
  corrected; numeric anchors unchanged
- 2026-07-05 · eval seed: 6/6 PASS (RESULTS-seed.md,
  claude-fable-5); the standing check-8 deferral on the high gotchas
  closes. Two independent trials surfaced the calendar-DOY vs
  month-day alignment step (3.3 points); steward-approved one-line
  clarification added to recipes/drought-index.md inputs (anchors
  unchanged)
- 2026-07-05 · gotchas/nwis-regulated-gauge.md ingested from
  the recipe-anchor measurement (Lees Ferry classified 2021 and 2023
  identically; Roaring Fork separated them by 20 median percentile
  points: the natural experiment is the evidence); recipes/{drought-index,
  reservoir-storage-change}.md authored with measured anchors only
  (Roaring Fork 2021/2023 contrast; Powell +44.20 ft 2023 refill);
  steward-verified the same day
- 2026-07-05 · close lint after the NWIS and SMAP seeds: zero 🔴, two 🟡. (1) The eval-seed
  deferral on the three authored high gotchas stands (closes with the
  hydrology eval seed). (2) Flat snapshot layout broke the pinned
  concepts' internal relative links; restructured to canonical shape
  (snapshot-podaac/{datasets,gotchas}/), files byte-identical, index
  paths updated. Steward ruling recorded: rule 9 eval coverage for
  PINNED copies is owned by the canonical bundle (ocean-science ships
  grace-leakage); pinned copies inherit review and eval coverage per
  §5.7 precedence
- 2026-07-05 · seeds: datasets/{nwis-streamflow, smap-l3}.md
  and gotchas/{nwis-provisional-data, smap-radar-loss}.md authored from
  live evidence (NWIS site 09380000 pull: trailing month 100% P vs 2023
  100% A; SMAP CMR audit incl. SPL3SMAP's bounded Apr-Jul 2015 span);
  snapshot-podaac/ pinned from ocean-science@1896335d083e per §5.7
  (3 GRACE concepts); load-grace-tws placeholder relabeled for the
  loader build that followed; dataretrieval deprecation of
  nwis.get_dv (removal on/after 2027-05-06) recorded in the nwis skill
  and dataset concept
- 2026-07-05 · close lint after the SWOT seed: zero 🔴, one 🟡 (dangling
  eval_case on swot-reach-node-scope), deferral to the eval seed
  accepted by the steward per SPEC v0.6 §10.3; scaffold frontmatter
  escaping bug in three placeholder skills caught at the close gate and
  fixed
- 2026-07-05 · datasets/swot-river-lake.md and
  gotchas/swot-reach-node-scope.md seeded from the CMR audit and
  live granule pulls (reach 731 features/127 attrs, node
  40,284/57, cycle 011 pass 424 AS PGD0); steward review passed the
  same day (verified_by OSP steward review)
