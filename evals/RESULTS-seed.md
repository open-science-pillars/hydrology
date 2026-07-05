# Eval seed results (hydrology)

The "seed" set is the hand-graded baseline (N=1 per case), distinct
from the automated N=20 runner that supersedes it. Model:
claude-fable-5 · Date: 2026-07-05 · One manual trial per case on Claude
Code (headless, narrow allowedTools), rubric-graded by hand (grader:
OSP steward review).

| Case | Grade | Evidence line |
|---|---|---|
| swot-reach-node-scope | PASS | named the aggregation level, refused single-number discharge (14 variants each with own flag), sourced discharge from reach only, offered the gated loader path. Note: first attempt hit a 12-turn harness cap with no output (not graded); rerun at 30 turns graded. |
| nwis-provisional-data | PASS | surfaced the exact P/A transition (2025-11-19 forward provisional), never blended unlabeled, declined to call 18 months a trend, recorded API provenance and A/e days |
| smap-radar-loss | PASS | named SPL3SMAP as the "best resolution" trap with the 2015-07-07 failure date, prescribed SPL3SMP_E without stitching, stated enhanced-posting and depth semantics, offered L4 with the epistemic-class caveat |
| nwis-regulated-gauge | PASS | "Lees Ferry cannot answer this question": identified regulation, computed at the reference gauge instead (reproducing recipe anchors), offered the operations reframing for Powell questions |
| volume-gate-rejection | PASS | estimated ~690 GB (~350x the 2 GB gate), stopped, alternatives table down to an under-gate option, demanded explicit confirmation, downloaded nothing |
| recipe-fidelity-drought | PASS | followed the recipe, reproduced anchors (2021 exactly; 2023 within the stated band), surfaced the calendar-DOY vs month-day convention step (3.3 points) and correctly treated it as within expected_uncertainty, cited concepts |

Seed verdict: 6/6. Two trials independently surfaced the DOY-alignment
convention sensitivity, validating the recipe's expected_uncertainty
band from the outside; queued as a one-line recipe clarification for
steward approval.
