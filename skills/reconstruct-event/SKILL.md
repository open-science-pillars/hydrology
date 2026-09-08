---
name: reconstruct-event
description: "Assemble a receipted timeline of one hydrologic event from several products when a water balance cannot close: every observation carries its product, version, acquisition and production dates and access date; every panel states what that sensor could not see; areas from an optical class product carry the valid fraction; a storage number for a basin below the GRACE footprint floor is refused, and a date is taken from a file rather than from a catalogue search."
---

# reconstruct-event

Turn "what happened during this flood" into a timeline a reader can
audit: which product saw what, when, and what each one could not see.
Works by slash command or conversationally ("reconstruct the Tulare
reflood", "when did SWOT first see this lake", "why is there no
storage number for this basin").

This skill carries the pointer, not the facts, and no number of its
own: the class tables, archive start dates, footprint floor and gauge
record all live in concepts and are read per run.

**Where the files are.** A path a user gives relative to the plugin
(`verification/fixtures/...`) resolves under `${CLAUDE_PLUGIN_ROOT}`,
not under the working directory: the fixtures ship with the plugin.
Resolve it there first rather than searching the filesystem.

## Behavior, in order

1. **Parse and show back:** the region (a polygon fixture with an
   equal-area area), the window, and which panels the user wants.
   Say what the timeline is for: a brief, a tutorial, or an input to
   something else.
2. **Consult the bundle for this event, in two tiers.** The recipe
   first, always:
   - `${CLAUDE_PLUGIN_ROOT}/knowledge/recipes/event-reconstruction.md`

   Then only what the event turns on:
   - an optical surface-water panel: the DSWx-HLS dataset concept and
     the class-mismatch gotcha in the provider bundle
   - a radar surface-water panel, or a question about why one is
     missing: the DSWx-S1 dataset concept and its archive start
   - a swath product's first or last observation: the
     swath-footprint gotcha
   - a storage panel: this plugin's water-balance computation concept
     for the footprint floor and its derivation
   - a precipitation panel: the IMERG concept and the run-mixing gotcha
   - a discharge panel: the USGS connector and the regulated-gauge
     gotcha

   Restate what applies and cite each by path.
3. **Check what the record can support before drawing anything.** For
   each requested panel: does the product's archive cover the window;
   is the region above the footprint floor where that matters; does a
   catalogue search's date survive opening the file. Report the panels
   that cannot be drawn and why, before the ones that can.
4. **Build each panel from the frozen census or capture**, never by
   reinterpreting raw granules by hand. Every area from a class
   product carries the valid fraction of the region on that date, and
   every class is named from its own product's table.
5. **Report the timeline as rows, not as a line.** Each row: date,
   product, version, what was observed, the qualifying number (valid
   fraction, gauge fraction of basin, mascon count), and the granule
   or capture identifier. Where a gap exists, the gap is a row with
   its reason.
6. **Close with what the record could not show**, in the recipe's
   terms. On an event where the observing system was weakest when the
   water was highest, that sentence is the finding.

## Must NOT

- Produce a storage number for a basin below the footprint floor, by
  any route, including a difference of other terms.
- Quote an area from an optical class product without the valid
  fraction of the region on that date.
- Take a first or last observation date from a catalogue search for a
  swath product without opening the granules.
- Join two products' class series into one panel without a written
  crosswalk naming the classes on both sides and showing the
  discontinuity.
- Interpolate across a gap, or draw a line where the rows are points.
- Present a gauge as measuring an inflow it does not measure: a
  headwater gauge is named with the fraction of the basin above it.
