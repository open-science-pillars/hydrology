---
name: load-smap
description: "Load SMAP L3 soil moisture with the volume gate: product line and version parsed, retrieval-quality flags decoded, lineage notes restated."
---

# load-smap

Bring SMAP L3 into the session safely. Authored in Session 16 per
SPEC v0.6 §10; gate contract as the other loaders.

## Behavior, in order

1. **Parse and show back:** product (SPL3SMP vs SPL3SMP_E; L4 only on
   explicit request, stated as model output), version, region, window,
   AM/PM overpass choice.
2. **Knowledge first, restated:** the radar-loss gotcha when the
   window touches 2015; flag semantics from the dataset concept.
3. **Search before fetching** with granule counts and volume; the
   local-config gate above threshold with alternatives (36 km instead
   of 9 km, shorter window).
4. **Load with flags decoded:** retrieval-quality gating applied and
   reported (fraction and dominant reasons); AM/PM kept distinct.
5. **Summary as provenance:** product/version/granules, window,
   quality accounting, depth semantics stated, cache location,
   concepts consulted.

## Must NOT

- Never fetch above the gate without explicit confirmation.
- Never merge AM and PM retrievals or L3 and L4 silently.
- Never present ungated retrieval statistics.
- Never omit the 2015 lineage note on spanning windows.
