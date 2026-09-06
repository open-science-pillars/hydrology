---
type: dataset-gotcha
title: "NWIS provisional data: recent values are revisable and flagged Provisional"
description: "Recent gauge data is provisional and can change or vanish on approval; statistics mixing Provisional and Approved values are silently unstable."
tags: [nwis, provisional, qualifiers, streamflow]
generated: { by: knowledge-seeder/claude, at: 2026-07-05T00:00:00Z }
severity: high
dataset: ../datasets/nwis-streamflow.md
eval_case: nwis-provisional-data
# eval id reserved for the hydrology eval seed (one case per high-severity gotcha).
sources:
  - id: usgs-provisional-statement
    resource: https://waterdata.usgs.gov/provisional-data-statement/
    title: "USGS provisional data statement"
  - id: usgs-09380000
    resource: https://waterdata.usgs.gov/monitoring-location/09380000/
    title: "USGS monitoring location 09380000 (Colorado River at Lees Ferry)"
status: stable
verified:
  - { by: human:PaulMRamirez, at: 2026-07-05T00:00:00Z }
  - { by: human:PaulMRamirez, at: 2026-09-06T17:01:38Z }
stale_after: 2027-01-04
---

# NWIS provisional data: recent values are revisable and flagged Provisional

**Mechanism.** New gauge data publishes immediately as PROVISIONAL
and remains so until USGS review approves it, a site-dependent
process that commonly takes months. The USGS provisional data
statement says such data may be revised or
removed.[^usgs-provisional-statement] The Water Data API returns the
state as `approval_status` (`Provisional` or `Approved`) beside a
separate `qualifier` list (`ESTIMATED` is the value observed so far); the
legacy services folded both into one code column (P or A with
modifiers), so the vocabulary changed on 2026-09-06 and the trap did
not. Observed 2026-07-05 at site 09380000 on the legacy services: the
trailing month was 100% P while calendar 2023 was 100% A on the same
parameter; on 2026-09-06 the same calendar year returned 100%
`Approved` from the new API, and a period-anchored recent window
captured on 2026-09-06 was uniformly provisional.[^usgs-09380000]

**Wrong-result mode.** A trend, flood statistic, or comparison
computed over a window mixing Provisional and Approved values changes when the
provisional segment is revised; a rerun months later silently gives
different numbers with no error anywhere. Drought and flood
declarations built on trailing windows are the classic casualty.

**Correct approach.** The approval status and qualifier columns are
kept and reported; statistics either exclude provisional values or
present the split explicitly; an `ESTIMATED` qualifier on an approved
day is not a reason to drop it (approval is the gate, the qualifier
is disclosure); any analysis touching the trailing ~year records its
retrieval date so revisions are detectable; published results based
on provisional values say so.

**Verification.** Reproducible: pull any active gauge's trailing month
and a past calendar year via dataretrieval's `waterdata.get_daily`;
`approval_status` shows the Provisional to Approved transition
(recorded pulls: 09380000, 00060 daily, 2026-07-05 on the legacy
services and 2026-09-06 on the Water Data API).[^usgs-09380000]

[^usgs-provisional-statement]: USGS provisional data statement
[^usgs-09380000]: USGS monitoring location 09380000, the recorded pull
