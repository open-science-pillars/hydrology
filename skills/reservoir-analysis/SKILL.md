---
name: reservoir-analysis
description: "Reservoir level and storage-change analysis from gauge elevation per the reservoir recipe; endpoint conventions stated; ARSET satellite complement referenced."
---

# reservoir-analysis

Reservoir trajectories from gauge elevation, honestly framed as
operations quantities.

## Behavior, in order

1. **Parse and show back:** reservoir/gauge, parameter (the
   lake-surface elevation parameter, and any storage conversion, per
   the bundle), period, endpoint convention (calendar vs water year,
   stated ALWAYS).
2. **Consult the bundle for this analysis first.** Before computing,
   DISCOVER the applicable concepts and read them; do not carry their
   facts here. Glob and grep `knowledge/recipes/`, `knowledge/gotchas/`,
   and `knowledge/datasets/` for every concept touching reservoir and
   lake elevation, gauge regulation, provisional qualifiers, and the
   satellite complement for ungauged sites. Read the matches and
   restate what each changes about the plan (the elevation parameter,
   the endpoint-convention uncertainty and why the choice moves the
   answer, the area-capacity conversion, the validation anchors, the
   operations-plus-hydrology framing, the SWOT lake path, the ARSET
   training), citing each by path. A concept added since you last ran
   is found this way.
3. **Load through load-nwis.**
4. **Compute per the recipe:** trajectory statistics (start, end, min,
   max with dates) and the stated-convention annual change; a reservoir
   year is a trajectory, never two endpoints alone. (Invariant method.)
5. **Validate against the recipe's anchors** where they apply.
6. **Report:** trajectory plot per cartography, convention and datum
   stated, qualifier accounting, the operations-plus-hydrology framing
   the bundle sets, and the concepts consulted.

## Must NOT

- Never quote an annual change without its endpoint convention. (Hard
  refusal: universal reporting discipline; the convention's effect on
  the number lives in the recipe.)
- Never convert elevation to volume without naming the area-capacity
  source. (Hard refusal: a derived conversion without its cited source
  is wrong for any reservoir.)
- Never hardcode expected values; the recipe is the authority. (Hard
  refusal: numbers come from the bundle, cited.)

Dataset-specific facts (the elevation parameter code, the
endpoint-convention band and why it moves the answer, the
reservoir-is-operations framing, the provisional-window and
regulated-gauge cautions, the SWOT lake path for ungauged sites, the
validation anchors) are NOT restated here: they live in the recipe,
the gotcha concepts, and the SWOT dataset, and are consulted per step
2. That is what lets a corrected anchor or a new gotcha change this
skill's behavior without editing it.
