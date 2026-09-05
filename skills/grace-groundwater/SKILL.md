---
name: grace-groundwater
description: "GRACE-FO terrestrial water storage to groundwater: TWS anomaly partitioning, what must be subtracted, and the mascon caveats via the pinned podaac snapshot."
user-invocable: false
---

# grace-groundwater

Background expertise for groundwater work from GRACE/GRACE-FO. The
mascon product facts live in the PO.DAAC provider bundle, installed
with the nasa-daac-knowledge dependency and cited here by bundle path
(`knowledge/podaac/...`);
the hydrology-side inference chain (the partitioning residual and its
uncertainty) lives in the bundle's groundwater partitioning recipe.
This file carries only the procedure and the hard refusal.

## Consult the bundle for this analysis

Before ANY groundwater-from-GRACE analysis, consult installed
knowledge concepts first, as the core `consult-knowledge` skill sets
out (the directories to glob across every installed bundle, how
to voice a concept's status, which concept wins on conflict), by
product name, quantity, and topic. Read the matches, restate what each
changes about the plan, and cite each by path before computing. A
concept added or corrected since you last ran is found this way, not
carried here. The concepts this plugin resolves to today:

- the mascon dataset, the provider's concept (the formal error grids
  and their limits, the variants, the pre-applied corrections):
  `knowledge/podaac/datasets/grace-fo-mascons.md`;
- coastal leakage: `knowledge/podaac/gotchas/grace-coastal-leakage.md`;
- the GIA correction: `knowledge/podaac/gotchas/grace-gia-correction.md`;
- the partitioning recipe (the subtrahend products, the uncertainty
  structure, the basin-resolution threshold, the trend-window
  caveats): `knowledge/recipes/grace-groundwater-partitioning.md`.

The snapshot is a copy: on any conflict with the canonical bundle, the
canonical concept wins, as the consult convention's precedence says.

## Method (invariant)

GRACE senses TOTAL water storage change; groundwater is a RESIDUAL,
never a direct measurement (general physics). The partitioning identity,
which product supplies each subtracted store, how the residual inherits
their errors, the basin-vs-effective-resolution rule, and the
gap-and-GIA trend caveats are the hydrology-side inference chain: they
live in `knowledge/recipes/grace-groundwater-partitioning.md` and the
mascon concepts, read and cited per analysis, never restated here.

## Must NOT (hard refusals)

- Never present a GRACE-derived groundwater number as a direct
  measurement, and never state one without naming every subtracted
  component and its source product. (Hard refusal: invariant, universal,
  fires without consulting anything; groundwater from GRACE is always a
  residual inference of other products.)
- Never restate a mascon rule or a partitioning caveat from memory, and
  never invent numbers: the formal-error floor, coastal leakage, the GIA
  correction, the 2017-2018 gap, the subtrahend uncertainty structure,
  and the effective-resolution threshold all live in the bundle's
  concepts and are read from them per analysis. Consulting them is how a
  new or corrected concept changes this skill's behavior without editing
  it.
