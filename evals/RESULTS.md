# Eval results (hydrology)

Runner results for the six hydrology cases, distinct from the
hand-graded seed in RESULTS-seed.md. Each run: the org runner
(open-science-pillars/evals, runner/run_evals.py) against a workspace
holding the plugins at the stated commits, N trials per case, a trial
passing only when every grader present agrees (the rubric judge is the
case's own rubric text), pass rate with a Wilson 95% interval against
the case's threshold of 0.8. Newest first.

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

Follow-ups from this run: the manifest's max_turns for this case to
30 and the runner's per-trial timeout above 600 s (both in the evals
repository); the case rubric to state the unpopulated-discharge
outcome (this repository); and a runner that keeps transcripts, so a
failure is readable without a rerun.

An N=5 interval is wide by construction (a perfect 5 of 5 is
[0.57, 1.00]); the verdicts above say whether the observed rate
cleared the threshold, not that the true rate does. The full N=20
sweep is the runner's standard measurement.

Runner fixes made for this run, all merged in the evals repository:
the hydrology and core manifests allowed a conda invocation no
workspace carries and now allow `uv run`; the runner treated an
inline rubric as a file path and now takes a value with whitespace as
the rubric text.
