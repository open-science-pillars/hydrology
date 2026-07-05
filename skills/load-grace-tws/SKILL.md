---
name: load-grace-tws
description: "Load GRACE/GRACE-FO mascon TWS with the volume gate; snapshot-concept caveats (leakage, GIA, the 2017-2018 gap) restated; basin-scale checks."
---

# load-grace-tws

Bring GRACE/GRACE-FO terrestrial water storage into the session
safely.

## Behavior, in order

1. **Parse and show back:** product (JPL mascons per the snapshot
   dataset concept), basin/region, period, and the intended use
   (TWS directly vs groundwater residual, which routes through
   grace-groundwater's partitioning chain).
2. **Knowledge first, restated:** coastal leakage for any basin
   touching a coastline; GIA handling for trends; the 2017-2018
   inter-mission gap for any spanning window; basin area vs effective
   mascon resolution (small basins get the leakage-dominated warning
   BEFORE loading).
3. **Search before fetching** with granule counts and volume; the
   local-config gate above threshold.
4. **Load with the error grids kept:** mascon uncertainty fields
   travel with the data; CRI-filtered vs unfiltered stated.
5. **Summary as provenance:** product and release, basin with area,
   period with the gap handling stated, which corrections are
   pre-applied (per the snapshot concept), concepts consulted.

## Must NOT

- Never fetch above the gate without explicit confirmation.
- Never deliver a small-basin TWS series without the resolution and
  leakage caveats stated.
- Never bridge the 2017-2018 gap silently.
- Never drop the mascon uncertainty fields in loading.
