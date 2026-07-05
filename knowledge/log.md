# hydrology bundle: change log

Newest first. One line per change: date, concept path, what changed, who.

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
