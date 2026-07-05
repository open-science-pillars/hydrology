# hydrology quickstart

From installed to a defensible water number. Assumes core AND
hydrology are installed; NWIS needs no credentials, SWOT/GRACE/SMAP
need Earthdata Login in `~/.netrc`.

## 1. Configure

Copy `hydrology.local.md.template` into your project as
`hydrology.local.md`: basins, gauges (with regulation status), and
the download gate live there.

## 2. Plan

Ask: "How dry was the upper Colorado in 2021 compared to 2023? Plan
the data first." The hydro-scout agent (or the skills
conversationally) returns a cited plan, and the first thing it will
tell you is which gauges measure hydrology and which measure dam
operations (the regulated-gauge rule).

## 3. Load through the gate

load-nwis pulls the reference gauge's daily values with qualifier
accounting (provisional data segregated); load-swot-hydro,
load-grace-tws, and load-smap follow the same gate contract for the
satellite complement.

## 4. Compute against the recipe

drought-analysis reads `knowledge/recipes/drought-index.md`: DOY
percentiles against a fixed 30-year climatology, with measured
anchors (2021 vs 2023 separate by ~20 median percentile points at
the reference gauge). reservoir-analysis does the same for
`reservoir-storage-change.md` (Lake Powell's +44.2 ft 2023 refill is
the anchor).

## 5. Report

The core report gate writes the provenance-complete summary: every
headline number with uncertainty, every concept cited.

The groundwater path (load-grace-tws + grace-groundwater's
partitioning chain) is the same shape, with the honesty rule that a
groundwater residual names every subtracted component.
