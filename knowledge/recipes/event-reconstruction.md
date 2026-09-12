---
type: recipe
spheres: [hydrosphere]
title: "Event reconstruction: a receipted timeline for an event no budget can close"
description: "How to assemble a timeline of one flood from several products when the water balance refuses the basin: each observation carries its product, version, acquisition date, production date and access date, and the recipe states for each sensor what it could not see. Worked on the Tulare Lake reflood of 2023, where the radar product did not yet exist, the satellite altimeter arrived after the peak, the optical product was mostly cloud, the storage product cannot resolve the basin, and the rivers that filled the lake are barely gauged."
tags: [event, timeline, flood, dswx, swot, imerg, tulare, receipt, hydrology]
generated: { by: claude-code/fable-5, at: 2026-09-07T21:00:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-08T04:19:42Z }
inputs: "A basin polygon with its equal-area area; a DSWx class census over that polygon per granule; the discharge captures that exist for the window; the precipitation loader's runs; the mascon series at a scale above the footprint floor"
expected: "The Tulare Lake bed for 2023: DSWx-S1 contributes nothing (zero granules before 2023-12-01), SWOT's first observation is 2023-07-30 against a search that offers 2023-07-27, the optical scenes are dominated by cloud, GRACE is a Central Valley panel and never a Tulare number, and USGS gauges cover headwaters rather than the inflow that reached the lake"
expected_uncertainty: "Every area from the optical product carries the valid fraction of the basin on that date; a date with a low valid fraction carries an area that is a lower bound, not a measurement"
status: stable
stale_after: 2027-03-07
---

# Event reconstruction: a receipted timeline

**Method.** When a basin cannot be closed, describe it instead. A
timeline is a receipted set of observations rather than a series: each
row names its product, its version, the acquisition date, the
production date and the access date, and the recipe states beside each
panel what that sensor could not see. The reader is meant to be able
to tell, for any date, whether an absence is water that was not there
or an observation that did not happen.

## What goes in a row

- **The product and its version**, from the concept that owns it.
- **The acquisition date and the production date.** These differ, and
  for a reprocessed archive they can differ by years: a DSWx-HLS
  granule acquired 2023-03-20 was produced 2026-03-17. A timeline
  rebuilt later may not reproduce an earlier one unless both are
  pinned.
- **The access date**, because a catalogue's holdings move.
- **What the observation covers.** For a raster class product, the
  valid fraction of the basin on that date. For a swath vector
  product, whether the granule actually held a feature inside the
  region rather than merely matching the search.
- **The class or variable, named from the product's own table.** The
  two DSWx products use the same integers for different classes, so a
  number without its product is not interpretable.

## What each sensor could not see, on this event

This is the part a reader needs and a series will not give them.

- **The radar product did not exist.** OPERA DSWx-S1's archive begins
  2023-12-01, and a search over the Tulare bed for the whole reflood
  returns zero granules. The reasoning that leads to it during a
  cloudy flood is sound and the result is still empty.
- **The optical product was mostly cloud.** A March 2023 scene over
  the bed is 57 per cent cloud and adjacent-to-cloud, 41 per cent
  fill, with about one per cent classified. Every area from it is
  quoted with the valid fraction, and a date with a low valid fraction
  gives a lower bound rather than a measurement.
- **The altimeter arrived after the peak.** SWOT LakeSP's first
  observation over the bed is 2023-07-30, months after the lake filled,
  so it measures the recession and never the rise. Note that a
  bounding-box search offers 2023-07-27: three earlier granules match
  the box on their swath footprint and contain no feature in it.
- **The storage product cannot resolve the basin.** The Tulare Lake
  bed is 9,808 km2 against a footprint floor of 111,266 km2, under
  nine per cent of one mascon. A GRACE panel may be shown at Central
  Valley scale with its footprint stated; a Tulare storage number does
  not exist and is never produced.
- **The rivers are barely gauged.** Of 137 USGS gauges named for the
  Kings, Kaweah, Tule and Kern, 22 have any daily discharge in 2023
  and all are headwater or conduit gauges: the main-stem records ended
  in 1959, 1921 and 1990 respectively, and the Kern gauge at the
  valley edge begins after the peak. The flow that reached the lake
  bed passed through Corps reservoirs recorded elsewhere. The
  discharge panel is therefore what was measured, each gauge with the
  fraction of its river's basin it represents, and an explicit
  statement that the inflow itself was not gauged by this network.
- **Precipitation has two runs.** IMERG Final is what the record says
  now; Late is what an analyst saw at the time. Both are shown, named
  per month, and never concatenated.

## What the timeline refuses

- **A storage number for a basin below the footprint floor**, by any
  route.
- **An area from a scene whose valid fraction is not stated.**
- **A date taken from a catalogue search rather than from a file**,
  for a swath product.
- **A single series spanning two products with different class
  tables.** One product per panel, or a written crosswalk that names
  the classes on both sides and shows the discontinuity.

## How to read it

The shape of the record is itself the finding. On this event the
observing system was at its weakest exactly when the water was at its
highest: the cloud that made the flood also blinded the optical
product, the radar that would have seen through it was not yet
flying, the altimeter arrived for the recession, and the gauges that
would have measured the inflow were retired decades ago. A
reconstruction that hides those gaps behind an interpolated line is
not describing the event; it is describing the interpolation.
