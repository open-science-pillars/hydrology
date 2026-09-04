---
name: nwis
description: "USGS NWIS streamflow: gauges, daily values via dataretrieval, provisional vs approved flags, rating-curve caveats, the waterdata API migration."
user-invocable: false
---

# nwis

Background expertise for USGS NWIS streamflow. This skill carries the
pointer, not the facts: every product number, qualifier meaning,
rating-curve caveat, provisional trap, and API-migration note lives in
exactly one knowledge concept and is read from there per analysis, never
restated here. Single-sourcing is what lets a corrected or newly added
concept change this skill's behavior without editing the skill.

## Knowledge first (standing step)

Before ANY NWIS work, consult installed knowledge concepts first, as
the core `consult-knowledge` skill sets out (the directories to glob,
how to voice a concept's status, which concept wins on conflict), by
the sites, parameters, and window in play (search terms: nwis,
streamflow, discharge, gauge, provisional, regulated, rating). Read
each match, restate what it changes about the plan before computing,
and cite it by path. A concept added since you last ran is found this
way, not from this file. The concepts this plugin resolves to today:

- the streamflow dataset: parameter codes, the string site identifiers
  with their leading zeros, the qualifier meanings (A approved, P
  provisional, and modifiers), dv and iv structure, the rating curve
  and its revisions, the extreme-flow extrapolation caveat, and the
  dataretrieval-to-waterdata API migration:
  `knowledge/datasets/nwis-streamflow.md`;
- the provisional-window trap: `knowledge/gotchas/nwis-provisional-data.md`;
- the regulated-gauge trap: `knowledge/gotchas/nwis-regulated-gauge.md`;
- the gauge-borne recipes with their anchors:
  `knowledge/recipes/drought-index.md` and
  `knowledge/recipes/reservoir-storage-change.md`;
- the units and identifier traps of the interactive gauge endpoint:
  `knowledge/connectors/usgs-water.md`.

Every one of those facts is read from its concept per analysis, never
from this list, which only says where to look.

## Hard refusals

None fire unconditionally in this skill. Every NWIS rule (segregate P
from A in a statistic; keep site numbers as strings; caveat extreme
flows; treat approved values as still revisable) is DATASET-coupled: it
is correct because of how NWIS is built, not regardless of dataset, so
it is read from the concept that owns it rather than hardcoded here. The
generic principle behind the first one (do not blend different approval
qualities into one statistic without disclosing the split) is the core
quality-control rule, applied through that skill.

## Must NOT

- Never carry an NWIS fact, number, or gotcha rule in this file; read it
  from the bundle concept that owns it and cite the path. Consulting the
  concept is how a corrected fact or a new gotcha changes this skill's
  behavior without an edit here.
