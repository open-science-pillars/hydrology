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

## 2026-09-07, N=5, claude-opus-5: the two event-reconstruction cases

The cases written beside the DSWx concepts that landed in
open-science-pillars/nasa-daac-knowledge pull 111. Workspace: the
hydrology checkout at the event-reconstruction merge, with the
provider bundle beside it; trials and rubric judge both on
claude-opus-5, so these rates are not comparable with the
claude-fable-5 entries below. Isolation enforced.

| Case | Passes | Valid trials | Rate | 95% CI | Errors | Verdict |
|---|---|---|---|---|---|---|
| swath-footprint-is-not-an-observation | 5 | 5 | 1.00 | [0.57, 1.00] | 0 | PASS |
| dswx-class-mismatch | 3 | 5 | 0.60 | [0.23, 0.88] | 0 | FAIL |

Every swath trial declined to confirm a first-observation date taken
from a bounding-box search, and said the check is opening the granules
and filtering by feature geometry.

The class-mismatch case fails at 3 of 5, and the failures are worth
more than the rate. One trial answered in 106 characters, treating the
request as something to file rather than to answer. The other got the
structure right (class 3, the mask collision, the artifact step at the
changeover) and then **invented a class**: it described DSWx-S1 class 2
as an existing "bright water" class and advised the user on whether to
fold it into the water mask. Class 2 does not exist in DSWx-S1. That is
precisely the failure the case exists to catch, asserting a class
meaning without reference to the product that defines it, and it
happened while the concept quoting both tables was readable in the
workspace.

**The rate stands as measured and the concepts are not being tuned to
it.** The obvious repair is to state in each dataset concept which
values are unused in that product rather than leaving it to the
reader's comparison of two tables. That is a real improvement and it
is owed, but making it and re-running until the number moved would be
fitting the artifact to its own test. The rate above describes the
artifacts as shipped.

**A runner defect this run found first.** These cases test concepts in
the provider bundle, and the isolation added in
open-science-pillars/evals pull 19 opened only the plugin under test,
so the first attempt would have measured the sandbox rather than the
knowledge and read as a knowledge failure. The runner now opens the
plugin's declared dependency bundles as well, which for hydrology is
core and nasa-daac-knowledge: what a real install has, and nothing
more.

## 2026-09-07, N=5, claude-opus-5: the three water-balance cases

The cases written beside the attested basin water balance
(open-science-pillars/hydrology pull 36 and 37), measured under
enforced trial isolation. Workspace: the hydrology checkout at that
merge, handed to each trial with `--plugin-dir` and the installed
plugin disabled by a `--settings` override; core 0.4.1 and
nasa-daac-knowledge 2026.9.2 as installed. Trials and rubric judge
both on claude-opus-5, so these rates are not comparable with the
claude-fable-5 entries below.

| Case | Passes | Valid trials | Rate | 95% CI | Errors | Verdict |
|---|---|---|---|---|---|---|
| water-balance-sub-floor-refusal | 5 | 5 | 1.00 | [0.57, 1.00] | 0 | PASS |
| water-balance-regulated-flag | 5 | 5 | 1.00 | [0.57, 1.00] | 0 | PASS |
| water-balance-run-declared | 5 | 5 | 1.00 | [0.57, 1.00] | 0 | PASS |

Every sub-floor trial refused the storage term on the footprint floor,
reported no residual and reached for no gain factor. Every
regulated-flag trial named the outlet as regulated and said the
discharge measures operations as well as hydrology. Every run-declared
trial named both dated limits: no Final run exists for water year 2026
(the V07 Final record ends 2025-09-30, and the run seam falls exactly
on the water-year boundary), and the storage endpoint for a window
ending this month is open because the mascon record runs months
behind.

**Isolation, and why these rates mean more than the ones that came
before them.** `--allowedTools` is a permission rule, and a rule loses
to the permission mode a parent session leaves in the settings: a
trial launched with `--allowedTools "Read,Skill"` was measured running
shell commands, querying CMR through MCP servers, and reading the
launching session's memory files and an earlier eval's transcripts.
Trials now run under `--restricted` with `--tools` from the case's own
allowed_tools, `--strict-mcp-config`, and `--add-dir` on the checkout
under test alone (open-science-pillars/evals pull 19). A probe case
asking for the launching session's memory and a shell command now gets
neither. No rate above could have been answered from this workspace's
memory, from an earlier transcript, or from a live catalogue.

### What it took to get here, and what each step measured

Four runs, because the first three were measuring the harness as much
as the plugin. The sequence is kept because each step's failure is the
evidence for the fix that followed it.

| Run | sub-floor | regulated | run-declared | What changed after it |
|---|---|---|---|---|
| 1, isolation not enforced | 3/4 recorded (truly 3/5) | 5/5 | 3/5 | the judge fix and the fixture-path pointer |
| 2, isolation not enforced | 5/5 | 5/5 | 0/5 | isolation enforced in the runner |
| 3, isolation enforced | 5/5 | 5/5 | 1/5 | the turn budget sized from measurement |
| 4, budget 35 | | | 3/5 | the consult made two-tier |
| 5, final | 5/5 | 5/5 | 5/5 | |

Four defects were found and fixed by these runs, three of them in the
measuring apparatus rather than in the plugin:

- **The judge discarded a verdict it had been given.** A reply
  truncated mid-reason still states its grade; the runner recorded an
  infrastructure error and dropped the trial from the denominator,
  reporting 3 of 4 rather than 3 of 5. A stated verdict is now
  salvaged, and ERROR is reserved for replies stating no grade at all
  (open-science-pillars/evals pull 17). What that judge caught was
  real: the trial refused the storage term correctly and then produced
  a closure by another route, so the computation concept, the recipe
  and the skill now say that below the floor no residual follows by
  any route, including a hand calculation that leaves the storage term
  out.
- **Trials could read anything.** Fixed as described above.
- **The skills did not say where their fixtures live.** Trials start in
  an empty directory while case prompts name fixtures by a
  plugin-relative path, so trials searched the filesystem and a
  recursive search of a home directory burns a full command timeout
  returning nothing. The three loading skills now say such a path
  resolves under `${CLAUDE_PLUGIN_ROOT}`, which is true for an
  installed plugin as well. The sub-floor case went from 3 of 5 to 5
  of 5 on that change alone.
- **A turn budget set for one kind of tooling.** The run-declared case
  allows `Read,Skill` only, and a tool that reads one file per call
  spends a call on every concept: a streamed probe finished the
  reasoning correctly in 26 turns against a budget of 20, so the case
  could not pass however well it reasoned. The budget was raised to 35
  from that measurement, which took it to 3 of 5, and the remaining
  failures were a consult that read seven concepts by habit. Listing
  the concepts in two tiers, one read always and the rest against the
  condition that makes each bind, took it to 5 of 5. Note that the
  first attempt at this was a soft hint ("read in order of what
  decides the question") sitting directly below the flat list of
  seven, and it changed nothing: an enumerated list outweighs a hint
  about how to use it.

The last of those is a fact about the skill's own economics, not about
the case: a flat list of seven concepts invites reading all seven, and
a reader who must pay a call per file pays for the habit. The two-tier
form is better guidance for a person as well.

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
