---
type: dataset-gotcha
title: "NWIS provisional data: recent values are revisable and flagged P"
description: "Recent gauge data is provisional and can change or vanish on approval; statistics mixing P and A values are silently unstable."
tags: [nwis, provisional, qualifiers, streamflow]
generated: { by: knowledge-seeder/claude, at: 2026-07-05T00:00:00Z }
severity: high
dataset: ../datasets/nwis-streamflow.md
eval_case: nwis-provisional-data
# eval id reserved for the hydrology eval seed (SPEC v0.6 §10.3).
sources:
  - id: usgs-provisional-statement
    resource: https://waterdata.usgs.gov/provisional-data-statement/
    title: "USGS provisional data statement"
  - id: usgs-09380000
    resource: https://waterdata.usgs.gov/monitoring-location/09380000/
    title: "USGS monitoring location 09380000 (Colorado River at Lees Ferry)"
status: stable
verified: { by: human:PaulMRamirez, at: 2026-07-05T00:00:00Z }
stale_after: 2027-01-04
---

# NWIS provisional data: recent values are revisable and flagged P

**Mechanism.** New gauge data publishes immediately as PROVISIONAL
(qualifier P) and remains so until USGS review approves it (A), a
site-dependent process that commonly takes months. The USGS
provisional data statement says such data may be revised or
removed.[^usgs-provisional-statement] Observed 2026-07-05 at site
09380000: the trailing month was 100% P while calendar 2023 was 100% A
on the same parameter.[^usgs-09380000]

**Wrong-result mode.** A trend, flood statistic, or comparison
computed over a window mixing P and A values changes when the
provisional segment is revised; a rerun months later silently gives
different numbers with no error anywhere. Drought and flood
declarations built on trailing windows are the classic casualty.

**Correct approach.** Qualifier columns are kept and reported;
statistics either exclude provisional values or present the split
explicitly; any analysis touching the trailing ~year records its
retrieval date so revisions are detectable; published results based
on P values say so.

**Verification.** Reproducible: pull any active gauge's trailing month
and a past calendar year via dataretrieval; the qualifier columns show
the P/A transition (recorded pull: 09380000, 00060 dv,
2026-07-05).[^usgs-09380000]

[^usgs-provisional-statement]: USGS provisional data statement
[^usgs-09380000]: USGS monitoring location 09380000, the recorded pull
