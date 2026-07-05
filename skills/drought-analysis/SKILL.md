---
name: drought-analysis
description: "Streamflow drought analysis: day-of-year percentile index at near-natural reference gauges per the drought recipe; regulated gauges refused for drought claims."
---

# drought-analysis

Drought characterization from streamflow, done at gauges that measure
hydrology.

## Behavior, in order

1. **Parse and show back:** basin/gauge, target period, climatology
   window (default the recipe's fixed 30-year window, stated).
2. **Knowledge first, restated:** the regulated-gauge gotcha is
   BINDING: a drought index requested at a regulated gauge is refused
   for drought claims, with the measured Lees Ferry natural experiment
   cited and a near-natural alternative offered; the provisional-data
   gotcha applies to any recent window.
3. **Load through load-nwis** (its gate and qualifier discipline).
4. **Compute per the recipe:** DOY percentiles against the fixed
   climatology, approved values only; report the median percentile and
   the below-30th/below-10th fractions with the class thresholds
   named.
5. **Validate where the recipe anchors apply** (recipe sites/years
   reproduce within expected_uncertainty; anything else is a finding).
6. **Report with uncertainty framing:** the recipe's method-sensitivity
   band, the climatology window, qualifier accounting, and concepts
   consulted.

## Must NOT

- Never present a drought index from a regulated gauge as hydrology;
  refuse and offer a reference gauge.
- Never mix provisional values into an index without the split stated.
- Never hardcode expected values; the recipe is the authority.
- Never compare indices computed against different climatology windows
  without saying so.
