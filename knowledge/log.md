# hydrology bundle: change log

Newest first. One line per change: date, concept path, what changed, who.

- 2026-07-05 · Session 17: gotchas/nwis-regulated-gauge.md ingested from
  the recipe-anchor measurement (Lees Ferry classified 2021 and 2023
  identically; Roaring Fork separated them by 20 median percentile
  points: the natural experiment is the evidence); recipes/{drought-index,
  reservoir-storage-change}.md authored with measured anchors only
  (Roaring Fork 2021/2023 contrast; Powell +44.20 ft 2023 refill);
  steward-verified same session · Session 17
- 2026-07-05 · Session 16 close lint: zero 🔴, two 🟡. (1) The eval-seed
  deferral on the three authored high gotchas stands (closes with the
  hydrology eval seed). (2) Flat snapshot layout broke the pinned
  concepts' internal relative links; restructured to canonical shape
  (snapshot-podaac/{datasets,gotchas}/), files byte-identical, index
  paths updated. Steward ruling recorded: rule 9 eval coverage for
  PINNED copies is owned by the canonical bundle (ocean-science ships
  grace-leakage); pinned copies inherit review and eval coverage per
  §5.7 precedence · Session 16
- 2026-07-05 · Session 16 seeds: datasets/{nwis-streamflow, smap-l3}.md
  and gotchas/{nwis-provisional-data, smap-radar-loss}.md authored from
  live evidence (NWIS site 09380000 pull: trailing month 100% P vs 2023
  100% A; SMAP CMR audit incl. SPL3SMAP's bounded Apr-Jul 2015 span);
  snapshot-podaac/ pinned from ocean-science@1896335d083e per §5.7
  (3 GRACE concepts); load-grace-tws placeholder relabeled to Session 17
  (guide block authors two loaders here); dataretrieval deprecation of
  nwis.get_dv (removal on/after 2027-05-06) recorded in the nwis skill
  and dataset concept · Session 16
- 2026-07-05 · Session 15 close lint: zero 🔴, one 🟡 (dangling eval_case
  on swot-reach-node-scope), deferral to the Session 16 eval seed
  accepted by the steward per SPEC v0.6 §10.3; scaffold frontmatter
  escaping bug in three placeholder skills caught at the close gate and
  fixed · Session 15
- 2026-07-05 · datasets/swot-river-lake.md and
  gotchas/swot-reach-node-scope.md seeded from the Session 15 CMR
  audit and live granule pulls (reach 731 features/127 attrs, node
  40,284/57, cycle 011 pass 424 AS PGD0); steward review passed same
  session (verified_by Paul Ramirez) · Session 15
