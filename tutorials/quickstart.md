# hydrology quickstart

From installed to a defensible water number. Assumes core AND
hydrology are installed. USGS water data needs no credentials (an
optional key, read from `API_USGS_PAT`, raises the request rate limit
and is sent only to the USGS Water Data API); downloading
SWOT, GRACE or SMAP needs an Earthdata Login, which earthaccess takes
from the environment (`EARTHDATA_TOKEN`), from `~/.netrc`, or from a
prompt.

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

## 4b. Close a basin water balance, in one page

The Colorado above Lees Ferry, water year 2023, from the frozen inputs
this plugin ships. Ask: "close the water balance for the Lees Ferry
basin for water year 2023." The basin-water-balance skill checks three
things before it computes anything, and each can end the exercise: the
basin against the GRACE footprint floor (about 111,000 km2, one
mascon), the window against the mascon record's end (two to three
months behind the present), and a declared IMERG run for every month.

Then it runs the sanctioned computation and its attester:

```
uv run knowledge/references/computations/basin_water_balance.py \
    --inputs verification/fixtures/water-balance/lees-ferry \
    --regulated --receipt lees-ferry.json
uv run knowledge/references/attesters/basin_water_balance_check.py lees-ferry.json
```

which gives, in km3:

```
  P      88.585 +-  8.858     ET  83.719 +- 16.744
  Q      10.769 +-  0.538     REGULATED
  dS     13.214 +-  2.858     (+4.780 cm, 7 mascons, 2022-09-16 to 2023-09-16)
  residual -19.117 +- 19.165  (-1.00 sigma, -21.6% of P)
```

Four things in that output are the point, and none of them is the
residual on its own. The ratio to the combined sigma is what to quote:
19 km3 sounds small and is a full sigma. The regulated flag says the
discharge is Glen Canyon Dam's releases as well as the basin's
hydrology. The epochs are mid-month, so "water year 2023" is measured
between two mid-September epochs and the receipt says so in days. And
the exports term is missing rather than zero: transmountain diversions
out of the Upper Colorado are real, no sourced water-year total was
available to cite, so the receipt carries the assumption explicitly
and the residual is an upper bound on closure.

Run the same thing on the Roaring Fork and it refuses: 3,767 km2 is
3.4 per cent of one mascon, so there is no storage term, no residual,
and no gain factor to rescue it. The three terms that do exist are
still reported. A refusal that names the floor is the computation
working.

## 5. Report

The core report gate writes the provenance-complete summary: every
headline number with uncertainty, every concept cited.

The groundwater path (load-grace-tws + grace-groundwater's
partitioning chain) is the same shape, with the honesty rule that a
groundwater residual names every subtracted component.
