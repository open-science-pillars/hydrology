---
name: reservoir-ledger
description: "Assemble a reservoir's budget in volume units from captured gauge records and a named area-capacity revision: storage change, gauged inflow and outflow, and a residual that names what is in it. Reports the residual rather than closing the identity, and refuses a volume whose datum or table revision is unstated."
---

# reservoir-ledger

Build the budget an operator would recognise, for one reservoir and one
window, and be honest about which terms were measured. Works by slash
command or conversationally ("build the water year 2023 ledger for Lake
Powell").

## Behavior, in order

1. **Parse and show back:** the reservoir, the window and its
   convention (water year or calendar year: the choice moves the answer
   by feet), and which gauges will play which role.
2. **Consult the bundle first.** Consult installed knowledge concepts
   first, as the core `consult-knowledge` skill sets out. Read the
   area-capacity concept (what a survey revision is and what a resurvey
   changes), the datum gotcha (which parameter code declares which
   datum, and why a satellite-to-gauge difference needs a cited
   offset), the elevation-change recipe this ledger extends, the
   streamflow concepts for approval and qualifiers, and the
   regulated-gauge caution. Restate what applies and cite each by path.
3. **Settle the datum before any volume.** Take the elevation series
   whose parameter code declares the datum the table is on. If the
   gauge publishes both national datums, say so and use the matching
   one; if it publishes only the other, use the agency's own conversion
   where one exists and refuse otherwise. Never derive a datum offset
   from the data being reconciled.
4. **Name the table revision** in the same breath as the volume. A
   volume without its survey year is not reproducible.
5. **Count the ungauged fraction** from the gauges' drainage areas
   against the outlet's, and state it before the totals, not after.
6. **Compute the terms and report the residual.** Storage change from
   both endpoints with both volumes and both surface areas; gauged
   inflow and outflow with the conversion factor stated; the residual
   with its sign, its size against inflow, and the list of what it
   contains. Do not assign a value to an unmeasured term to make the
   identity balance.
7. **Summary as provenance:** the reservoir and window, every capture
   id and content hash, the table file with its DOI and hash, the datum
   on both sides, the ungauged fraction, each term, and the residual
   with its contents named.

## Must NOT

- Never quote a volume without the table revision that produced it.
- Never read an elevation into a table column on a different datum, and
  never convert between datums by a number derived from the comparison.
- Never extrapolate beyond the surveyed table.
- Never close the identity by assigning a value to evaporation, bank
  storage or ungauged inflow. Name them and leave them in the residual.
- Never present an outflow gauge below a dam as the dam release.
- Never quote a satellite-to-gauge elevation difference without both
  datums and a cited offset; where the offset cannot be cited, report
  that rather than the difference.
- Never restate a rule this skill could consult: the datum authority,
  the survey revision doctrine and the gauge cautions live in concepts
  and are read from them per run.

## Where the honest answer is uncomfortable

A ledger whose residual is a few per cent of throughput will look worse
than one that closes, and the one that closes usually got there by
choosing a value for a term nobody measured. Report the residual, name
its contents, and let the reader judge. If a reader wants it closed,
what they need is an evaporation estimate with a source, not a better
fit.
