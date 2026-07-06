---
name: drought-analysis
description: "Streamflow drought analysis: day-of-year percentile index at near-natural reference gauges per the drought recipe; regulated gauges refused for drought claims."
---

# drought-analysis

Drought characterization from streamflow, done at gauges that measure
hydrology.

## The regulated-gauge rule (hard refusal, non-negotiable)

A drought index requested at a REGULATED gauge is REFUSED for drought
claims: flow statistics there measure operations, not hydrology. The
refusal cites the gotcha (nwis-regulated-gauge) and offers a
near-natural reference gauge. This rule fires before any computation,
whatever the framing of the request; the gauge's regulation status and
the measured evidence behind the refusal are read from the gotcha, not
carried here.

## Behavior, in order

1. **Parse and show back:** basin/gauge, target period, climatology
   window (default the recipe's fixed climatology window, stated).
2. **Consult the bundle for THIS analysis first.** Discover and read the
   concepts that apply, do not restate them from memory: glob and grep
   `knowledge/gotchas/`, `knowledge/datasets/`, and `knowledge/recipes/`
   for every concept touching the gauge, the parameter, and the drought
   method (the regulated-gauge and provisional-data gotchas, the NWIS
   streamflow dataset, the drought-index recipe). Restate what each
   changes about the plan and cite it by path. A concept added or
   corrected since you last ran is found this way; the regulation
   evidence, the provisional-window rule, the fixed climatology window,
   and the drought class thresholds all live in concepts and are read
   from them, never from this skill.
3. **Load through load-nwis** (its gate and qualifier discipline).
4. **Compute per the recipe:** its day-of-year percentile method against
   the recipe's climatology, with the qualifier discipline the
   provisional-data gotcha requires; report the summaries the recipe
   defines (the median percentile and the below-threshold fractions),
   naming the recipe's class thresholds as read from it.
5. **Validate where the recipe anchors apply** (recipe sites/years
   reproduce within expected_uncertainty; anything else is a finding).
6. **Report with uncertainty framing:** the recipe's method-sensitivity
   band, the climatology window used, qualifier accounting, and the
   concepts consulted.

## Must NOT

- Never present a drought index from a regulated gauge as hydrology;
  refuse and offer a reference gauge. (Hard refusal: invariant,
  refusal-shaped, universal.)
- Never hardcode expected values; the recipe is the authority.
- Never compare indices computed against different climatology windows
  without saying so. (Method discipline: percentiles read against
  different baselines are not comparable, regardless of dataset.)

Dataset-specific rules (which gauges are regulated and the Lees Ferry
evidence, the provisional-versus-approved split, the fixed climatology
window, the USDM-style class thresholds, the recipe's expected values
and method-sensitivity band) are NOT restated here: they live in the
nwis-regulated-gauge and nwis-provisional-data gotchas, the
nwis-streamflow dataset, and the drought-index recipe, and are consulted
per step 2. That is what lets a corrected threshold, a new gotcha, or a
re-measured anchor change this skill's behavior without editing it.
