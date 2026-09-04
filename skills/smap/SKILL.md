---
name: smap
description: "SMAP soil moisture: L3 radiometer products (36 km and enhanced 9 km), retrieval quality flags, the 2015 radar loss and product lineage, L4 model-value-added."
user-invocable: false
---

# smap

Background expertise for SMAP soil moisture. This skill is deliberately
reference-light: the product facts (the L3 radiometer line and its
enhanced posting, the L4 model-assimilated family, the retrieval-quality
flags, the surface-layer depth semantics) and the radar-loss lineage
break live in the knowledge bundle's concepts, not in this file. Here we
keep only the discipline that discovers and reads them per analysis.

## Consult the bundle for this dataset

Before ANY statement about SMAP soil moisture, consult installed
knowledge concepts first, as the core `consult-knowledge` skill sets
out (the directories to glob, how to voice a concept's status, which
concept wins on conflict), by the products, quantities, and time span
in play (search by product name, and by SMAP, soil moisture, radar,
flags, depth). Read the matches, restate what each changes about the
plan, and cite it by path before answering. A concept added or
corrected since you last ran is found this way; consulting the bundle
is how a new or fixed concept changes this skill's behavior without
editing the skill. The concepts this plugin resolves to today:

- the L3 dataset: the radiometer line and its enhanced posting, the
  model-assimilated L4 family, the retrieval-quality flags, the
  surface-layer depth semantics, the accuracy figures:
  `knowledge/datasets/smap-l3.md`;
- the 2015 radar loss and the product-lineage break:
  `knowledge/gotchas/smap-radar-loss.md`.

Routing hints: any record touching 2015 consults the radar-loss
gotcha; any retrieval-quality or uncertainty claim consults the
dataset concept's flag and uncertainty notes. Both are read per
analysis, never from this list.

## Must NOT

- Never work from a remembered dataset rule where a concept exists: the
  radar-loss lineage break, the L3-retrieval-versus-L4-model epistemic
  class, the retrieval-quality flag gating, and the surface-versus-root-
  zone depth semantics all live in the bundle's concepts
  (datasets/smap-l3.md and gotchas/smap-radar-loss.md) and are read from
  them per analysis, never carried or restated in this skill.
- Never invent product facts, numbers, spans, or resolutions: the SMAP
  product line, its postings and dates, and the retrieval-accuracy
  figures come from the concepts, cited.
