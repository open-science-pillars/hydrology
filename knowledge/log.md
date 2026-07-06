# hydrology bundle: change log

Newest first. One line per change: date, concept path, what changed, who.

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
  commit a0c84fff959f (previously ocean-science@1896335d083e, Session
  16); byte-identity verified by the canonical repo's sync_check, run
  green 2026-07-05; index.md provenance block updated
- 2026-07-05 · ERRATUM (steward-approved): the reservoir recipe's 2023
  minimum was labeled February; the daily data place it April 13-14
  (3,519.5 ft; February's low was 3,520.5). Discovered by the Session
  17 e2e run, which reproduced all numeric anchors and contradicted
  only this label. Recipe, golden print label, and fixtures README
  corrected; numeric anchors unchanged
- 2026-07-05 · Session 17 eval seed: 6/6 PASS (RESULTS-seed.md,
  claude-fable-5); the standing check-8 deferral on the high gotchas
  closes. Two independent trials surfaced the calendar-DOY vs
  month-day alignment step (3.3 points); steward-approved one-line
  clarification added to recipes/drought-index.md inputs (anchors
  unchanged)
- 2026-07-05 · Session 17: gotchas/nwis-regulated-gauge.md ingested from
  the recipe-anchor measurement (Lees Ferry classified 2021 and 2023
  identically; Roaring Fork separated them by 20 median percentile
  points: the natural experiment is the evidence); recipes/{drought-index,
  reservoir-storage-change}.md authored with measured anchors only
  (Roaring Fork 2021/2023 contrast; Powell +44.20 ft 2023 refill);
  steward-verified same session
- 2026-07-05 · Session 16 close lint: zero 🔴, two 🟡. (1) The eval-seed
  deferral on the three authored high gotchas stands (closes with the
  hydrology eval seed). (2) Flat snapshot layout broke the pinned
  concepts' internal relative links; restructured to canonical shape
  (snapshot-podaac/{datasets,gotchas}/), files byte-identical, index
  paths updated. Steward ruling recorded: rule 9 eval coverage for
  PINNED copies is owned by the canonical bundle (ocean-science ships
  grace-leakage); pinned copies inherit review and eval coverage per
  §5.7 precedence
- 2026-07-05 · Session 16 seeds: datasets/{nwis-streamflow, smap-l3}.md
  and gotchas/{nwis-provisional-data, smap-radar-loss}.md authored from
  live evidence (NWIS site 09380000 pull: trailing month 100% P vs 2023
  100% A; SMAP CMR audit incl. SPL3SMAP's bounded Apr-Jul 2015 span);
  snapshot-podaac/ pinned from ocean-science@1896335d083e per §5.7
  (3 GRACE concepts); load-grace-tws placeholder relabeled to Session 17
  (guide block authors two loaders here); dataretrieval deprecation of
  nwis.get_dv (removal on/after 2027-05-06) recorded in the nwis skill
  and dataset concept
- 2026-07-05 · Session 15 close lint: zero 🔴, one 🟡 (dangling eval_case
  on swot-reach-node-scope), deferral to the Session 16 eval seed
  accepted by the steward per SPEC v0.6 §10.3; scaffold frontmatter
  escaping bug in three placeholder skills caught at the close gate and
  fixed
- 2026-07-05 · datasets/swot-river-lake.md and
  gotchas/swot-reach-node-scope.md seeded from the Session 15 CMR
  audit and live granule pulls (reach 731 features/127 attrs, node
  40,284/57, cycle 011 pass 424 AS PGD0); steward review passed same
  session (verified_by OSP steward review)
