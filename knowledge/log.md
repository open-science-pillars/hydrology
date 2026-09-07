# hydrology bundle: change log

Newest first. One line per change: date, concept path, what changed, who.

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
