---
name: reservoir-analysis
description: "Reservoir level and storage-change analysis from gauge elevation per the reservoir recipe; endpoint conventions stated; ARSET satellite complement referenced."
---

# reservoir-analysis

Reservoir trajectories from gauge elevation, honestly framed as
operations quantities. Authored in Session 17 per SPEC v0.6 §10;
method and anchors live in
`knowledge/recipes/reservoir-storage-change.md`.

## Behavior, in order

1. **Parse and show back:** reservoir/gauge, parameter (62614
   elevation; storage conversion only with an operator area-capacity
   table, stated), period, endpoint convention (calendar vs water
   year, stated ALWAYS: the recipe records why it moves the answer by
   feet).
2. **Knowledge first, restated:** the recipe's definitional
   uncertainty; provisional-data gotcha on recent windows; for
   ungauged reservoirs, the satellite path (SWOT lake products per
   swot-river-lake, ARSET training linked in the recipe).
3. **Load through load-nwis.**
4. **Compute per the recipe:** trajectory statistics (start, end, min,
   max with dates), the stated-convention annual change; never
   endpoints alone.
5. **Validate where anchors apply** (Powell 2023 reproduces within
   the recipe band).
6. **Report:** trajectory plot per cartography, convention and datum
   stated, qualifier accounting, concepts consulted.

## Must NOT

- Never quote an annual change without its endpoint convention.
- Never convert elevation to volume without naming the area-capacity
  source.
- Never present reservoir level as a climate signal; it is operations
  plus hydrology, and the framing says so.
- Never hardcode expected values; the recipe is the authority.
