---
name: load-swot-hydro
description: "Load SWOT river and lake vector products: parse region/continent, reach or node level, cycles; volume gate; quality decode; scope-aware summary."
---

# load-swot-hydro

Bring SWOT inland-water vectors into the session safely: level chosen
explicitly, gated on volume, quality-gated, scope preserved. Works by
slash command or conversationally ("load SWOT river reaches for the
Amazon, cycle 11").

## Behavior, in order

1. **Parse and show back:** product and aggregation LEVEL, region and
   the continent code(s) it resolves to, time range or cycles, and
   version family. The level (reach vs node) is a real fork, confirmed
   explicitly and never assumed; the product inventory, the per-continent
   granule packaging (so one region can resolve to more than one code),
   the version family, and what each level means and costs all come from
   the concepts read in the next step, not from memory.
2. **Consult the bundle for this load first.** Discover and read the
   SWOT inland-water concepts that apply (glob `knowledge/`): the dataset
   concept for the product and level inventory, per-continent packaging,
   version family and crid, the per-level quality attributes, the
   simulated-vs-flight collection trap, and the `_u` uncertainty fields;
   and the gotchas the request or downstream intent triggers (the
   reach-vs-node scope trap whenever a statistic will be quoted at a
   level). Restate what each changes about the plan and cite it by path;
   do not carry these facts in this skill. A concept added since you last
   ran is found this way.
3. **Search before fetching:** granule count and estimated volume BEFORE
   any download, using the per-granule sizes the dataset concept records
   (they differ sharply by level).
4. **The volume gate (hard gate).** Threshold from the project local
   config (template default 2 GB). At or below: state count, size,
   destination, proceed. Above: STOP and present count, total size,
   destination, and a smaller alternative (reach instead of node, fewer
   cycles, one continent), and wait for explicit confirmation. The gate
   lives here in the skill body so it fires on every surface.
5. **Load with quality decoded:** read features with geopandas from the
   zipped shapefiles; apply and report the product's quality gating (the
   dataset concept names the quality attributes per level); keep features
   as vectors with their feature identifiers intact, no premature
   rasterization (a loading contract, not analysis).
6. **Scope-aware summary:** level, collections and crids loaded,
   cycles/passes/continents, feature counts before and after quality
   gating with the dominant flag reasons, which uncertainty (`_u`)
   attributes came along (per the dataset concept's Uncertainty section),
   and the concepts consulted. This summary is the downstream provenance
   record.

## Must NOT

- Never download above the gate threshold without explicit confirmation,
  on any surface. (Hard gate: invariant, universal; fires without
  consulting anything.)
- Never present ungated (quality-undecoded) feature statistics. (Hard
  refusal: invariant, universal.)
- Never strip feature identifiers or quality attributes during a load;
  they are the provenance the summary and downstream steps need. (Loading
  contract; the specific identifier and quality attribute names live in
  the dataset concept, not here.)
- Never rasterize as a loading step; keep vectors and rasterize
  deliberately elsewhere if at all. (Loading contract, not a dataset
  fact.)
- Never work from a remembered SWOT inland-water rule where a concept
  exists: the product and level inventory, per-continent packaging,
  version family and crid, the reach-vs-node scope trap and its per-level
  volume asymmetry, the simulated-vs-flight collection trap, and the
  quality and uncertainty attribute sets all live in the swot concepts
  (datasets/swot-river-lake.md and gotchas/swot-reach-node-scope.md) and
  are read from them per load. Consulting them is how a new or corrected
  concept changes this skill's behavior without editing it.
