---
name: load-grace-tws
description: "Load GRACE/GRACE-FO mascon TWS with the volume gate; consults the bundle and restates the applicable gotchas; basin-scale checks."
---

# load-grace-tws

Bring GRACE/GRACE-FO terrestrial water storage into the session
safely: gated on volume, native uncertainty kept, the applicable
dataset caveats consulted and restated. Works by slash command or
conversationally ("load GRACE TWS for the Colorado basin").

## Behavior, in order

1. **Parse and show back:** product, basin/region, period, and the
   intended use (TWS directly vs a groundwater residual, which routes
   through grace-groundwater's partitioning chain). Resolve the product,
   release, and variant from the dataset concept, not from a remembered
   name.
2. **Consult the bundle for this load first.** Discover and read the
   GRACE concepts that apply (glob `knowledge/`, grep by product,
   basin, and topic): the dataset concept for the product, release, and
   variants, and the gotchas the request or downstream intent triggers
   (a coastline touched by the basin, a trend to be fit, a window that
   spans an inter-mission gap, a basin whose area approaches the native
   mascon scale). Restate what each changes about the plan and cite it
   by path; do not carry these facts in this skill. A concept added or
   corrected since the last run is found this way.
3. **Search before fetching:** granule count and estimated volume
   BEFORE any download.
4. **The volume gate.** Threshold from the project local config. At or
   below: state count, size, destination, proceed. Above: STOP, present
   count, total size, destination, and a smaller alternative (shorter
   window, fewer basins), and wait for explicit confirmation.
5. **Load with the native uncertainty kept:** the product's per-mascon
   uncertainty fields travel with the data (what the product ships is
   read from the dataset concept), and the loaded variant (CRI-filtered
   vs unfiltered) is stated. Corrections the product already carries are
   never re-applied.
6. **Summary as provenance:** product and release, basin with area,
   period with the gap handling stated, which corrections are
   pre-applied (per the dataset concept), the variant loaded, and the
   concepts consulted. State the compute scale for what comes next.

## Must NOT

- Never fetch above the gate threshold without explicit confirmation,
  on any surface. (Hard gate: fires without consulting anything.)
- Never drop the product's native uncertainty fields in loading. (Load
  procedure; that this product ships per-mascon uncertainty grids is
  read from the dataset concept.)
- Never deliver a basin TWS series at or below the product's native
  mascon resolution without stating the resolution and leakage caveats
  the bundle supplies. (Gate; the caveat content is read from the GRACE
  concepts per load, not carried here.)
- Never bridge a known inter-mission gap, or re-correct a pre-applied
  correction, silently. (Procedure; the gap's dates and the applied
  corrections are read from the GRACE concepts, not carried here.)
- Never restate a GRACE dataset rule this skill could consult: coastal
  leakage, the GIA correction, the inter-mission gap, the native mascon
  scale, and the variant catalog live in the bundle's concepts and are
  read from them per load. Consulting them is how a new or corrected
  concept changes this skill without editing it.
