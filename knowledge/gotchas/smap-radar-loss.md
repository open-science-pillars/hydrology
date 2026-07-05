---
type: dataset-gotcha
title: "SMAP radar loss (July 2015): the product lineage breaks"
description: "The radar failed 2015-07-07; the combined radar/radiometer 9 km line (SPL3SMAP) ends there, and records spanning 2015 mix product lineages."
tags: [smap, radar, lineage, 2015]
timestamp: 2026-07-05
severity: high
dataset: ../datasets/smap-l3.md
eval_case: smap-radar-loss
# eval id reserved for the hydrology eval seed (SPEC v0.6 §10.3).
evidence:
  - https://nsidc.org/data/spl3smap
  - https://nsidc.org/data/spl3smp
status: verified
verified: 2026-07-05
verified_by: Paul Ramirez (steward pro tem)
---

# SMAP radar loss (July 2015): the product lineage breaks

**Mechanism.** SMAP launched with a radar and a radiometer; the radar
failed on 2015-07-07, a few months into science operations. The
combined radar/radiometer soil moisture line (SPL3SMAP, 9 km) exists
ONLY for April to July 2015 (its collection page records the span;
CMR-verified as a live but bounded collection 2026-07-05). Everything
after mid-2015 is radiometer-only (SPL3SMP at 36 km; SPL3SMP_E's 9 km
is enhanced posting, not radar resolution).

**Wrong-result mode.** A "SMAP soil moisture record" assembled across
2015 mixes retrieval algorithms and effective resolutions at the
break; apparent mid-2015 shifts can be lineage artifacts; a user
finding SPL3SMAP and extrapolating its properties to the ongoing
mission builds on a product that ended within months.

**Correct approach.** Records name their product line explicitly;
anything spanning mid-2015 treats the break as a lineage boundary
(analyzed per line or with the discontinuity acknowledged);
resolution claims follow the radiometer footprint after the loss.

**Verification.** The SPL3SMAP collection's bounded temporal extent
(April to July 2015) against SPL3SMP's ongoing record, both on their
NSIDC pages (evidence links) and in CMR (audited 2026-07-05).
