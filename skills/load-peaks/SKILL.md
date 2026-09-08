---
name: load-peaks
description: "Load a gauge's annual peak record from the Water Data API, export the fixed-width peak file the flood frequency program reads, and read that program's output back. Computes a screening fit only, labelled as one, with an interval on every quantile."
---

# load-peaks

Bring an annual peak record into the session, hand it off in the form
the field's software reads, and read the answer back. Works by slash
command or conversationally ("get the annual peaks for the French
Broad at Asheville and write a peak file").

## Behavior, in order

1. **Parse and show back:** the site, the parameter, the water years.
   **The parameter is required.** One peaks response holds two series
   in two units, so a request that does not name one is answered with
   the question, not a default.
2. **Consult the bundle for this load first.** Consult installed
   knowledge concepts first, as the core `consult-knowledge` skill
   sets out. Read the connector concept (endpoints, paging, the
   optional key, the rate limits, the decommission window), the annual
   peaks concept (the two series, partial dates, the qualifier
   vocabulary and its mapping, what the frequency program does with
   each code) and the gotchas the request triggers: the two-series
   trap on any load, the screening-fit trap whenever a frequency
   number is wanted, and the regulated-gauge caution whenever the site
   sits below a dam. Restate what applies and cite each by path; do
   not carry these facts here.
3. **Load the record whole.** Every water year the collection holds
   for that parameter, with the qualifiers and with the rows whose
   month or day is null. Do not filter on a parsable date: those rows
   are the historic peaks, they are usually the largest floods in the
   record, and dropping them is silent.
4. **State the record before analysing it.** The count of peaks, the
   first and last water year, the water years missing from between
   them, the rows with a partial date, and the qualifier codes present
   that the frequency program acts on: regulated, urbanized, historic,
   censored above or below. Say plainly what each means for what can
   be computed here.
5. **Export, do not estimate.** Write the peak file through
   `verification/fixtures/load_peaks.py --watstore`, which maps each
   qualifier to its qualification code and leaves the month and day
   columns blank where the record says unknown. Report the mapping it
   used and any qualifier that has no code in that format.
6. **A frequency number comes from the frequency program.** The
   analyst runs it on the exported file and returns its output; this
   skill parses that output and reports its estimates with the
   program's own confidence limits and its version. A screening fit
   computed here is labelled screening in every line that carries it,
   states what it did not implement, and carries an interval on every
   quantile.
7. **Summary as provenance:** site with name and drainage area,
   parameter and unit, water years and gaps, qualifier counts, the
   exported file with its hash, the concepts consulted, and, when a
   fit was computed, its method line and what it dropped.

## Must NOT

- Never load peaks without a parameter, and never concatenate the
  discharge and stage series.
- Never drop a row because its date will not parse.
- Never report a return period without an interval, from any source.
- Never call a fit computed here a Bulletin 17C or published estimate,
  and never present one beside a program's output without the labels
  that separate them.
- Never fit through regulated, urbanized, historic or censored peaks
  without the analyst saying so first; the loader refuses, and the
  refusal is the skill's behavior rather than an obstacle to route
  around.
- Never restate a rule this skill could consult: the qualifier
  vocabulary, the code mapping and the cautions live in the concepts
  the hydrology skill lists and are read from them per load.

## Refusals worth stating out loud

The peak file is exported from the collection, but the writer that
produces the agency's own copy of that file lives on the host being
decommissioned. Where an export is checked against that copy, say when
it was checked, because the reference is going away.
