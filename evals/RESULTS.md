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

swot-reach-node-scope fails: one trial returned an empty transcript
(counted as an infrastructure error, not a failure) and two of the
four valid trials failed the rubric. The runner does not keep
transcripts, so the failing trials are not diagnosable from this run.
The seed record notes that this case's first manual attempt hit a
turn cap with no output at 12 turns and graded only at 30; the
manifest allows 15, and the empty trial is consistent with the same
cap. A re-run of this case alone, with transcripts kept and the
turn allowance raised, is the next measurement; until then the case
is recorded as failing at N=5 with a wide interval.

An N=5 interval is wide by construction (a perfect 5 of 5 is
[0.57, 1.00]); the verdicts above say whether the observed rate
cleared the threshold, not that the true rate does. The full N=20
sweep is the runner's standard measurement.

Runner fixes made for this run, both merged in the evals repository:
the hydrology manifest allowed a conda invocation no workspace
carries and now allows `uv run`; the runner treated an inline rubric
as a file path and now takes a value with whitespace as the rubric
text.
