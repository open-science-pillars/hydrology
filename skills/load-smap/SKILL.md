---
name: load-smap
description: "Load SMAP L3 soil moisture with the volume gate: product line and version parsed, retrieval-quality flags decoded, applicable concepts consulted."
---

# load-smap

Bring SMAP L3 into the session safely: product line resolved, gated on
volume, quality flags decoded, applicable concepts consulted. Works by
slash command or conversationally ("load SMAP soil moisture for the
Southern Great Plains, 2016").

## Behavior, in order

1. **Parse and show back:** product line, version, region, window, and
   AM/PM overpass choice. The model-assimilated L4 family is offered
   only on explicit request and labeled as model output; which L3
   product lines exist and how they differ is read from the bundle
   (step 2), not listed here.
2. **Consult the bundle for this dataset first.** Discover and read the
   SMAP concepts that apply (glob and grep `knowledge/`): the dataset
   concept for the product lines, resolutions, ~5 cm depth semantics, and
   flag meanings; the gotchas the window or intent triggers (a window
   touching 2015 pulls in the radar-loss lineage break). Restate what
   each changes about the plan and cite it by path; do not carry these
   facts in this skill. A concept added since you last ran is found this
   way.
3. **Search before fetching:** granule count and estimated volume BEFORE
   any download.
4. **The volume gate.** Threshold from the project local config. At or
   below: state count, size, destination, proceed. Above: STOP, present
   count, total size, destination, and a smaller alternative (the
   coarser-posting product, a shorter window, fewer granules), and wait
   for explicit confirmation.
5. **Load with flags decoded:** apply the retrieval-quality gate the
   dataset concept defines and report it (gated fraction and the
   dominant flag reasons); keep AM and PM retrievals distinct.
6. **Summary as provenance:** product line and version, granule count,
   window, the quality accounting, the depth semantics stated (read from
   the concept), cache location, and the concepts consulted.

## Must NOT

- Never fetch above the gate threshold without explicit confirmation, on
  any surface. (Hard gate: fires without consulting anything.)
- Never merge the model-assimilated L4 family with observational L3
  retrievals, or present the one as the other. (Hard refusal: the
  observation-vs-model epistemic class is universal; which SMAP line is
  which is read from the dataset concept.)
- Never average AM and PM retrievals into one field silently. (Load
  procedure: they are distinct overpass populations.)
- Never present retrieval statistics without the quality gate applied
  and reported. (Load procedure; the flag semantics are the concept's.)
- Never restate a dataset rule this skill could consult: the L3 product
  lines and resolutions, the ~5 cm depth semantics, the flag meanings,
  and the 2015 radar-loss lineage break live in the SMAP concepts
  (datasets/smap-l3.md and gotchas/smap-radar-loss.md) and are read from
  them per load. Consulting them is how a corrected or new concept
  changes this skill without editing it.
