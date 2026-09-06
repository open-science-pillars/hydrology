---
name: nwis
description: "USGS streamflow: gauges, daily and continuous values through dataretrieval's waterdata module (the USGS Water Data API), approval status and qualifiers, rating-curve caveats, the legacy Water Services deprecation."
user-invocable: false
---

# nwis

Background expertise for USGS streamflow (the NWIS record, served
today by the USGS Water Data API). This skill carries the pointer,
not the facts: every product number, qualifier meaning, rating-curve
caveat, provisional trap, endpoint, paging rule and deprecation date
lives in exactly one knowledge concept and is read from there per
analysis, never restated here. Single-sourcing is what lets a
corrected or newly added concept change this skill's behavior without
editing the skill.

## The client

Fetch through dataretrieval's `waterdata` module (`get_daily`,
`get_continuous`, `get_monitoring_locations`, `get_peaks`), never
through its `nwis` module and never by hand-built requests to the
legacy host. Every fact about the API that the fetch depends on (the
host and collections, the paging and count behavior, the optional key
and the environment variable it is read from, the depth of each
collection, the rate limit and what a 429 means, the legacy endpoint's
deprecation window) is read from the connector concept at fetch time
and cited by path; this file names the module and nothing more.

## Knowledge first (standing step)

Before ANY NWIS work, consult installed knowledge concepts first, as
the core `consult-knowledge` skill sets out (the directories to glob,
how to voice a concept's status, which concept wins on conflict), by
the sites, parameters, and window in play (search terms: nwis,
streamflow, discharge, gauge, provisional, regulated, rating). Read
each match, restate what it changes about the plan before computing,
and cite it by path. A concept added since you last ran is found this
way, not from this file. The concepts this plugin resolves to today:

- the streamflow dataset: parameter codes, the agency-prefixed string
  site identifiers with their leading zeros, the approval status and
  qualifier vocabulary as the API returns them, daily and continuous
  structure, the rating curve and its revisions, the extreme-flow
  extrapolation caveat, and the dataretrieval `nwis` module's removal
  date: `knowledge/datasets/nwis-streamflow.md`;
- the provisional-window trap: `knowledge/gotchas/nwis-provisional-data.md`;
- the regulated-gauge trap: `knowledge/gotchas/nwis-regulated-gauge.md`;
- the gauge-borne recipes with their anchors:
  `knowledge/recipes/drought-index.md` and
  `knowledge/recipes/reservoir-storage-change.md`;
- the API itself: endpoints, paging, the optional key, depth, the
  rate limit and 429 behavior, the units and identifier traps, and the
  legacy endpoint's deprecation: `knowledge/connectors/usgs-water.md`.

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
- Never put the API key anywhere but the environment variable the
  connector concept names, and never echo it into a summary, a cache
  path, a request URL or a receipt.
