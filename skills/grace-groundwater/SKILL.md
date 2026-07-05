---
name: grace-groundwater
description: "GRACE-FO terrestrial water storage to groundwater: TWS anomaly partitioning, what must be subtracted, and the mascon caveats via the pinned podaac snapshot."
user-invocable: false
---

# grace-groundwater

Background expertise for groundwater work from GRACE/GRACE-FO. Authored
in Session 16 per SPEC v0.6 §10. The mascon product facts live in the
PINNED SNAPSHOT concepts (`knowledge/snapshot-podaac/`, source and
commit in index.md per §5.7); this skill carries the hydrology-side
inference chain.

## Knowledge first

Consult and restate before analysis: the snapshot's grace-fo-mascons
concept (formal error grids, their limits), both snapshot gotchas
(coastal leakage; GIA pre-applied), and this plugin's basin conventions.
The snapshot is a copy: on conflict with the canonical bundle, the
canonical concept wins (§5.7 precedence).

## The partitioning chain, stated honestly

GRACE senses TOTAL water storage change. Groundwater is a residual:

GW anomaly = TWS anomaly - (soil moisture + snow + surface water + canopy)

Every subtracted term comes from ANOTHER product (SMAP or model soil
moisture, SNODAS/model snow, altimetry or gauge surface water), so the
groundwater estimate inherits every subtrahend's errors and biases,
usually without formal error propagation available. Consequences:

- The residual's uncertainty is BOUNDED BELOW by the mascon formal
  error and is typically dominated by the subtrahends; a groundwater
  trend quoted with only the GRACE formal error is understated.
- Basin size matters: below a few mascon footprints (order 300 km),
  the estimate is leakage-dominated (snapshot gotcha) and honest work
  states basin area against effective resolution.
- The 2017-2018 inter-mission gap and GIA-model sensitivity (snapshot
  concepts) bite trends directly; trend windows state their handling.
- Human signals (irrigation drawdown) and climate signals mix in the
  residual; attribution needs independent evidence, not the residual
  alone.

## Must NOT

- Never quote groundwater from TWS without naming every subtracted
  component and its source product.
- Never quote residual uncertainty as the GRACE formal error alone.
- Never analyze basins below the effective mascon resolution without
  the leakage caveat front and center.
- Never bridge the 2017-2018 gap with a fit that treats it as data.
