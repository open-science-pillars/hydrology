---
name: swot-hydro
description: "SWOT river and lake products: RiverSP reach vs node scope, LakeSP obs/prior, raster water masks, zipped-shapefile access, discharge products."
user-invocable: false
---

# swot-hydro

Background expertise for SWOT inland-water products. This skill carries
the method and the one hard refusal, not the dataset facts. The product
inventory and granule anatomy live in
`references/swot-hydro-products.md` (CMR- and granule-verified
2026-07-05); the baselines, attribute rules, and uncertainty framing
live in the knowledge bundle and are read from there per analysis.

## Knowledge first

Before ANY SWOT hydrology analysis, DISCOVER and consult the installed
knowledge bundle; do not work from a remembered list of rules. Search
`knowledge/datasets/`, `knowledge/gotchas/`, and `knowledge/recipes/`
(glob and grep by product name, attribute, and topic: RiverSP, LakeSP,
reach, node, discharge, wse, quality, simulated), read every concept
that touches the products and quantities in play, restate what each
changes about the plan before computing, and cite it by path. A concept
added or corrected since you last ran is found this way; that discovery,
not this file, is what changes behavior.

Everything dataset-specific is read from the bundle, never carried here:
version families and current baselines; which `_u` attributes exist at
each aggregation level and what they omit (`wse_u` total vs `wse_r_u`
random, and the rest); the reach-vs-node scope rule and its volume
asymmetry; the discharge algorithm variants and their per-variant `_u`
and `_q`; the quality attributes that gate features; and which
collections are simulated rather than flown.

## Method (invariant, not dataset facts)

- **Feature product, not a swath.** SWOT hydrology spans vector feature
  collections and raster water masks; which product is which is in the
  concept. Handle each in kind: for a vector feature collection you
  compute statistics over features and QC gates apply to attributes
  exactly as core QC gates apply them to pixels; do not read a feature
  product as a gridded swath. The granule mechanics (packaging,
  per-continent identity, reader) are the concept's to state.
- **Aggregation level is part of a result.** An aggregated statistic is
  meaningless without the level it was computed at; map each question to
  the level the product answers it at. The specific SWOT levels, their
  differing attributes, and the volume asymmetry are dataset facts:
  consult the scope gotcha, do not restate them here.
- **Loading is load-swot-hydro's job** (volume gate, decode, scope-aware
  summary); this skill supplies what it restates.

## Must NOT

- **Hard refusal (invariant, universal, fires without consulting
  anything):** never present simulated or synthetic collections as
  observations, and never blend them into an observational series.
  Passing synthetic data off as flown data is wrong regardless of
  dataset; WHICH collections are simulated is dataset knowledge,
  consulted from the concept.
- Never hardcode a baseline, an attribute rule, a discharge variant, or
  the reach/node scope rule, and never restate a gotcha here: read them
  from the dataset and gotcha concepts per the Knowledge-first step,
  cited. That single-sourcing is what lets a corrected concept change
  this skill's behavior without editing it.
