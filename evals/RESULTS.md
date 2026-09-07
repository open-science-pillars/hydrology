# Eval results (hydrology)

Runner results for the eleven hydrology cases, distinct from the
hand-graded seed in RESULTS-seed.md. Each run: the org runner
(open-science-pillars/evals, runner/run_evals.py) against a workspace
holding the plugins at the stated commits, N trials per case, a trial
passing only when every grader present agrees (the rubric judge is the
case's own rubric text), pass rate with a Wilson 95% interval against
the case's threshold of 0.8. Newest first.

Every entry names its model, and the model is part of the
measurement: rates from different models are not comparable with each
other, and an entry says so where it differs from the ones around
it.

## 2026-09-07, N=5, claude-opus-5: the three water-balance cases (PROVISIONAL, isolation not enforced)

**Read the caveat before the rates.** While diagnosing a turn-budget
failure in these runs, a streamed transcript showed a trial whose
manifest row allows only `Read,Skill` using Bash, ToolSearch and MCP
tools, querying CMR live, and reading two things it should never have
seen: this workspace's session memory files and the transcripts of an
earlier eval. A minimal test confirmed the mechanism: a headless trial
launched with `--allowedTools "Read"` and asked to run a shell command
runs it, and neither `--permission-mode default` nor a `deny` rule in
`--settings` changes that. The allow-list is advisory, and launching
from an empty directory does not isolate a trial that can read the
whole filesystem.

So these rates are recorded and marked provisional. They are not
withdrawn (the transcripts are real and the failures they show are
real), but no rate below should be read as measuring what the plugin
alone supplies: a case whose answer exists in this workspace's memory,
in a prior transcript, or in the concepts themselves could be answered
from those. The runner is being fixed and the cases will be measured
again under enforced isolation; those rates will supersede these.

Workspace: the hydrology checkout at the water-balance merge
(open-science-pillars/hydrology pull 36) handed to each trial with
`--plugin-dir`, the installed plugin disabled by a `--settings`
override; core 0.4.1 and nasa-daac-knowledge 2026.9.2 as installed.
Trials and rubric judge both on claude-opus-5, so these rates are not
comparable with the claude-fable-5 entries below.

### Second run, after two fixes (the rates)

| Case | Passes | Valid trials | Rate | 95% CI | Errors | Verdict |
|---|---|---|---|---|---|---|
| water-balance-sub-floor-refusal | 5 | 5 | 1.00 | [0.57, 1.00] | 0 | PASS |
| water-balance-regulated-flag | 5 | 5 | 1.00 | [0.57, 1.00] | 0 | PASS |
| water-balance-run-declared | 0 | 5 | 0.00 | [0.00, 0.43] | 0 | FAIL |

Every regulated-flag trial named the outlet as regulated and said the
discharge measures operations as well as hydrology. Every sub-floor
trial refused the storage term on the footprint floor, reported no
residual, and reached for no gain factor; the fastest ran in 77 s
against 436 s in the first run.

Every run-declared trial exhausted its turn budget with no answer
written, and the streamed probe says why: the trial spends its turns
verifying the IMERG, MOD16 and GRACE records live against CMR rather
than answering from the frozen fixture, which is possible only because
the allow-list does not bind. The case asks about a window ending this
month, which invites exactly that. This is the clearest evidence in
the run that the isolation problem changes behaviour and not just
provenance.

### First run, and the two defects it exposed

| Case | Passes | Valid | Rate | Errors | Verdict |
|---|---|---|---|---|---|
| water-balance-sub-floor-refusal | 3 | 4 recorded (truly 5) | 0.75 recorded (truly 0.60) | 1 | FAIL |
| water-balance-regulated-flag | 5 | 5 | 1.00 | 0 | PASS |
| water-balance-run-declared | 3 | 5 | 0.60 | 0 | FAIL |

Two defects, both fixed before the second run:

- **The judge discarded a verdict it had been given.** A judge answered
  `{"grade": "FAIL", "reason": "Although the storage term is correctly
  refused ... the response still delivers a basin closure number by
  another route` and was cut off mid-reason. The runner recorded an
  infrastructure error and dropped the trial from the denominator,
  reporting 3 of 4 rather than 3 of 5. A verdict that was stated is a
  verdict even when its envelope is damaged, and it is now salvaged;
  ERROR is reserved for replies stating no grade at all
  (open-science-pillars/evals pull 17). Note what that judge caught:
  the trial refused the storage term correctly and then produced a
  closure by another route, which is exactly the failure the case
  exists to detect, and the concept, recipe and skill now say that no
  residual follows by any route including a hand calculation that
  leaves the storage term out.
- **The skills did not say where their fixtures live.** A trial starts
  in an empty directory and the case prompts name fixtures by a
  plugin-relative path, so trials searched the filesystem, and a
  recursive search of a home directory burns the full two-minute
  command timeout without returning anything. Three of the six
  non-passes in the first run were turn exhaustion of this kind. The
  three loading skills now say that a plugin-relative path resolves
  under `${CLAUDE_PLUGIN_ROOT}`, which is also true for an installed
  plugin and so helps real users. The sub-floor case went from 3 of 5
  to 5 of 5 on that change alone.

## 2026-09-06, N=5, claude-opus-5: the two evapotranspiration cases (first run)

**A different measurement basis from every entry below.** These two
cases were run on claude-opus-5, trials and rubric judge both, at the
steward's instruction after the claude-fable-5 five-hour usage limit
blocked two attempts on that model (every trial returned the limit
message and was recorded as an error, correctly, and no rate was
produced). The rates here are therefore NOT comparable with the
claude-fable-5 entries below; they say what these cases do on Opus,
not how the two models compare, which would need both measured under
the same conditions.

Workspace: the hydrology checkout at the evapotranspiration merge
(open-science-pillars/hydrology pull 33) handed to each trial with
`--plugin-dir`, the installed hydrology plugin disabled for the trial
by a `--settings` override (the runner records both under
`claude_args`); core 0.4.1 and nasa-daac-knowledge 2026.9.2 as
installed. Launched from an empty directory so no project
instructions or memory reached the trials. Allowed tools per the
manifest: Read, Skill, Bash(uv run*) and Write for the fill case
(max_turns 25); Read and Skill for the area-cap case (max_turns 20).
Wall clock about 50 min for ten trials plus judging.

| Case | Passes | Valid trials | Rate | 95% CI | Errors | Verdict |
|---|---|---|---|---|---|---|
| openet-area-cap | 5 | 5 | 1.00 | [0.57, 1.00] | 0 | PASS |
| mod16-fill-over-water-barren-urban | 4 | 5 | 0.80 | [0.38, 0.96] | 0 | PASS |

| Trial | Case | Wall clock | Verdict | What the transcript shows |
|---|---|---|---|---|
| 1 | fill | 397 s | PASS | hit the loader's refusal at the default masking threshold, raised it deliberately, and reported 168.72 mm scoped to the 50.0 km2 measured of the polygon's 104.6, with 242 water cells of 489; named both the zero-fill reading (80.39 mm) and the whole-polygon volume as errors |
| 2 | fill | 359 s | PASS | the same, with the reservoir's own evaporation named as absent from the number |
| 3 | fill | 396 s | FAIL | reached the 25-turn limit with no answer written; the turns went to the loader and the concepts without an answer being composed |
| 4 | fill | 369 s | PASS | the same as trial 1, with the volume error called out explicitly |
| 5 | fill | 349 s | PASS | the same; 242 water and 14 barren of 489 stated with the mean |
| 1 | area cap | 132 s | PASS | 930,871 acres against the 50,000 acre Tier 1 cap, 18.6 times over, the 422 refusal named, no OpenET basin mean offered, tiling and polygon simplification both declined, MOD16 delivered for the basin |
| 2 | area cap | 358 s | PASS | the same, and OpenET offered only on the named sub-cap unit |
| 3 | area cap | 150 s | PASS | the same |
| 4 | area cap | 235 s | PASS | the same, with the sub-cap unit named as one 95 km2 unit and not the basin |
| 5 | area cap | 145 s | PASS | the same |

The area-cap case passes at 5 of 5: every trial refused the basin
request with the acreage and the multiple, and none proposed tiling
or shrinking the polygon, which are the failures the case exists to
catch.

The fill case passes at 4 of 5, and the one failure is not a wrong
answer: the trial exhausted its 25-turn budget without composing one.
The four that answered all did the same thing, which is what the
gotcha asks for: they met the loader's refusal at the default masking
threshold, raised it deliberately rather than working round it, and
returned the number with its masked fraction, its measured area and
the missing reservoir evaporation stated beside it. A turn budget
that a workflow can exhaust is a real cost of that workflow and is
counted here as a failure rather than as an infrastructure error; if
this recurs, the loader's runtime over a 50,000-cell window is the
thing to look at, not the rubric.

**A defect in the measuring apparatus, found and fixed during this
run.** The first Opus attempt recorded every trial as
`FAIL: unparseable judge output` while the transcripts held correct
answers. The rubric judge was hardcoded to claude-fable-5 while the
trials honoured `--model`, so the judge alone hit that model's usage
limit, its reply parsed as no JSON, and an outage was recorded as a
failed trial. The judge now takes the runner's model, and a timeout,
a limit message or an unreadable reply returns ERROR, which the
runner excludes from the denominator exactly as it already did for a
trial that never ran (open-science-pillars/evals pull 16). The rates
above were measured after that fix.

## 2026-09-06, N=5, claude-fable-5: the two IMERG cases (first run)

The cases written beside the two high-severity IMERG gotchas, run the
day they were registered (open-science-pillars/evals pull 14).
Workspace: the hydrology checkout at the precipitation merge
(open-science-pillars/hydrology pull 30, main at 4033231) handed to
each trial with `--plugin-dir`, the installed hydrology plugin
disabled for the trial by a `--settings` override (the runner records
both under `claude_args`); core 0.4.1 and nasa-daac-knowledge 2026.9.2
as installed. Launched from an empty directory so no project
instructions or memory reached the trials. Allowed tools per the
manifest: Read and Skill for imerg-run-mixing (max_turns 20); Read,
Skill, Bash(uv run*) and Write for the cold-season case (max_turns
25). Judge claude-fable-5 on the case rubric. Wall clock about 22 min
for ten trials plus judging.

| Case | Passes | Valid trials | Rate | 95% CI | Errors | Verdict |
|---|---|---|---|---|---|---|
| imerg-cold-season-orographic-underestimation | 5 | 5 | 1.00 | [0.57, 1.00] | 0 | PASS |
| imerg-run-mixing | 2 | 5 | 0.40 | [0.12, 0.77] | 0 | FAIL |

| Trial | Case | Wall clock | Verdict | What the transcript shows |
|---|---|---|---|---|
| 1 | cold-season | 75 s | PASS | ran the loader on both fixtures; 320.44 mm and 88.585 km3 with the run named and 2,869 of 5,412 cells; the NLDAS-2 check beside it at 374.53 mm; ratios 0.86 and 0.68 stated as an underestimate with values present |
| 2 | cold-season | 72 s | PASS | the same, with the release-notes snowfall caveat quoted and the gauge analysis named as a check rather than truth |
| 3 | cold-season | 66 s | PASS | the same; the November through March ratio carried into the water-balance advice |
| 4 | cold-season | 78 s | PASS | the same; NLDAS-2's own high-elevation undercatch stated beside it |
| 5 | cold-season | 64 s | PASS | the same; the fixture named and the cold-season months listed |
| 1 | run-mixing | 194 s | ERROR (graded FAIL) | reached the 20-turn limit with no answer written; the turns went to a hand search of the installed plugin cache for an IMERG concept that is not in the installed version |
| 2 | run-mixing | 192 s | PASS | read the checkout's dataset and run-mixing concepts; Final ends 2025-09-30, Late named per segment as a different calibration, both the 2025-10-01 run seam and the 2026-03-01 calibration seam required in the methods text |
| 3 | run-mixing | 180 s | FAIL | everything else right, but the calibration seam dated 2026-03-03 (the V07B to V07C label change) instead of 2026-03-01 (the calibration change); the trial had searched the installed bundles, found no IMERG concept, and read the date off granule labels |
| 4 | run-mixing | 192 s | PASS | as trial 2 |
| 5 | run-mixing | 193 s | FAIL | as trial 3, and it added that March 2026 mixes two V07B days with 29 V07C days |

The cold-season case passes at 5 of 5: every trial ran the loader
rather than reading the file by hand, and every trial ran the
gauge-based check the gotcha names as the correct approach.

The run-mixing case fails at 2 of 5, and the split is not about the
gotcha. Every failing trial got the end of the Final record, the run
attribution per segment and the refusal to call the series continuous
right. All three failures share one cause: the trial searched the
installed bundles, found no IMERG concept there (the installed
hydrology plugin is 0.4.0, cut before this work), and reconstructed
the second seam from CMR granule labels, which put the V07B to V07C
label change of 2026-03-03 in the methods text where the calibration
change of 2026-03-01 belongs. Both dates are real and the dataset
concept carries both; a trial that read the concept got the
distinction, a trial that did not, did not.

The measurement therefore found a discovery defect, not a knowledge
defect. `claude plugin list --json` does not list a plugin loaded from
a directory with `--plugin-dir`, and it does not reflect a session's
`--settings` override, so a bundle search run the way the core
consult-knowledge skill describes finds the stale installed bundle and
reports the concept missing (open-science-pillars/core issue 24). The
load-precipitation skill now anchors its concept pointers at
`${CLAUDE_PLUGIN_ROOT}` so the concepts resolve from the running
plugin's own root either way.

A rerun of the case with the anchored skill was stopped by a model
usage limit after three trials (1 pass, 2 fails, both fails the same
seam date, both from trials that again searched the installed
bundles); trials 4 and 5 returned the limit message and are recorded
as errors, not failures. The case stays FAIL until it is measured
again at N=5 against an install that carries the concepts. The rate
above is the first run, which is the complete one.

## 2026-09-06, N=5, claude-fable-5: nldi-unsnapped-point (first run)

The case written beside the high-severity unsnapped-point gotcha,
run alone the day it was registered. Workspace: the hydrology
checkout at the delineate-basin merge (open-science-pillars/hydrology
pull 27 plus the snap-distance refinement in the follow-up pull),
handed to each trial with `--plugin-dir` and the installed hydrology
plugin disabled for the trial by a `--settings` override (the runner
records both under `claude_args`); core 0.4.1 and
nasa-daac-knowledge 2026.9.2 as installed. Launched from an empty
directory so no project instructions or memory reached the trials.
Allowed tools per the manifest: Read, Skill, Bash(uv run*), Write;
max_turns 25; judge claude-fable-5 on the case rubric. Wall clock
about 7 min for five trials plus judging (63 to 90 s per trial). The
NLDI hydrolocation route was answering throughout (it had been in an
outage earlier the same day, recorded in the connector concept).

| Case | Passes | Valid trials | Rate | 95% CI | Errors | Verdict |
|---|---|---|---|---|---|---|
| nldi-unsnapped-point | 5 | 5 | 1.00 | [0.57, 1.00] | 0 | PASS |

| Trial | Wall clock | Verdict | What the transcript shows |
|---|---|---|---|
| 1 | 74 s | PASS | snapped through hydrolocation; comid 1235819, reach 14010001002638, measure 28.20 named; the reach identified as the Colorado above the confluence, not the Roaring Fork; both areas with ESRI:102008 beside the gauge's 3,763.3 km2 |
| 2 | 90 s | PASS | the same, with the 385 m snap distance stated and the coordinate returned to the user for confirmation |
| 3 | 63 s | PASS | the same; the 11,766.7 km2 polygon declined as the site's basin until the position is confirmed |
| 4 | 85 s | PASS | the same; the gauge's own trace offered as the likely divisor |
| 5 | 82 s | PASS | the same; snap distance and subbasin mismatch both named |

Every trial ran the plugin's delineation script rather than hand
requests, so every trial's polygon came from the snapped route with
its provenance; the case's failure mode (a Colorado main-stem area
handed over as the Roaring Fork site's basin) did not occur. The
snapped route itself answers for the nearest flowline, which for
this point IS the Colorado; what the trials got right was the
evidence beside the number, which is what the gotcha, rewritten
after this measurement, now asks for.

## 2026-09-06, N=5, claude-fable-5

Workspace: hydrology at the USGS Water Data API migration branch
(skills on dataretrieval's waterdata module, fixtures refetched from
the new API in the documented schema), core at 673ee1f (observations
server on the new API). Allowed tools per the manifest: Read and
Skill for the gotcha cases; Read, Skill, Bash(uv run*) and Write for
the two NWIS cases and the recipe case. Judge: claude-fable-5 on the
case rubric. Wall clock about 2 h 10 min for 30 trials plus judging.

| Case | Passes | Valid trials | Rate | 95% CI | Errors | Verdict |
|---|---|---|---|---|---|---|
| swot-reach-node-scope | 2 | 4 | 0.50 | [0.15, 0.85] | 1 | FAIL |
| nwis-provisional-data | 5 | 5 | 1.00 | [0.57, 1.00] | 0 | PASS |
| smap-radar-loss | 5 | 5 | 1.00 | [0.57, 1.00] | 0 | PASS |
| nwis-regulated-gauge | 5 | 5 | 1.00 | [0.57, 1.00] | 0 | PASS |
| volume-gate-rejection | 5 | 5 | 1.00 | [0.57, 1.00] | 0 | PASS |
| recipe-fidelity-drought | 4 | 5 | 0.80 | [0.38, 0.96] | 0 | PASS |

Five of six cases pass at N=5. The three cases that exercise the
USGS record (nwis-provisional-data, nwis-regulated-gauge,
recipe-fidelity-drought) pass on the new API and the refetched
fixtures; the provisional case is the first run in which the agent
reads approval_status and the qualifier list rather than the legacy
one-column code.

swot-reach-node-scope failed in that run: one trial returned an
empty transcript (counted as an infrastructure error, not a failure)
and two of the four valid trials failed the rubric. The runner keeps
no transcripts, so those trials were not readable; the case was rerun
alone the same day (below).

### swot-reach-node-scope rerun, 2026-09-06, N=5, transcripts kept

Same prompt, rubric, judge and model, run through the runner's own
grader modules with two settings changed: max_turns 30 in place of
the manifest's 15, and a 900 s per-trial timeout in place of the
runner's 600 s. Every transcript, stderr and judge verdict was kept.

| Trial | Wall clock | Verdict | What the transcript shows |
|---|---|---|---|
| 1 | 217 s | PASS | reach-level height named; discharge searched at reach level, variants and quality flags named |
| 2 | 643 s | PASS | reach-level height; discharge from the L4 SOS product at reach level, consensus variant and reach_q gating named |
| 3 | 252 s | PASS | reach-level height; the fourteen reach dschg fields found all fill and said so; the gauge offered as an option, no number given |
| 4 | 515 s | PASS | reach-level height and discharge, consensus variant and quality gating named |
| 5 | 289 s | FAIL | reach-level height; dschg fields found all fill and said so; the gauge of record pulled and reported, labeled as a USGS number and not a SWOT retrieval |

Rate 0.80, 95% CI [0.38, 0.96], threshold 0.8: PASS at N=5, no
empty transcripts.

What the rerun resolves. The first run's empty trial is explained by
the runner's timeout, not the plugin: trial 2 here ran 643 s, past
the runner's 600 s cap, after which the runner returns an empty
transcript and counts an error. Its two rubric failures are
consistent with the 15-turn allowance cutting a transcript short (the
seed record met the same cap at 12 turns), since no trial at 30 turns
was cut. The one failure here is a rubric-precision finding, not a
trap the agent fell into: trials 3 and 5 both established that the
reach discharge fields are unpopulated in the held granules, neither
claimed discharge from node data, and the judge passed the one that
offered the gauge as an option while failing the one that reported
the gauge value with its source labeled. The rubric's clause "sources
discharge from reach-level data (naming the algorithm variant and
quality flag)" presumes discharge exists in the reach files; when it
does not, a labeled substitute is the honest answer and the case
should say whether that passes.

Follow-ups from this run, all done 2026-09-06: the manifest's
max_turns for this case is 30 and the runner's per-trial timeout is a
flag defaulting to 1200 s (open-science-pillars/evals#11, which also
records every trial in the results file and keeps transcripts under
--transcripts); the case rubric now states the unpopulated-discharge
outcome (a labeled gauge substitute beside the reach-level statement
passes, a substitute presented as SWOT discharge fails). Trial 5
above was graded under the earlier wording and its verdict stands as
recorded; the next run measures the case under the new rubric.

An N=5 interval is wide by construction (a perfect 5 of 5 is
[0.57, 1.00]); the verdicts above say whether the observed rate
cleared the threshold, not that the true rate does. The full N=20
sweep is the runner's standard measurement.

Runner fixes made for this run, all merged in the evals repository:
the hydrology and core manifests allowed a conda invocation no
workspace carries and now allow `uv run`; the runner treated an
inline rubric as a file path and now takes a value with whitespace as
the rubric text.
