---
type: recipe
title: "Reservoir ledger: a budget in volume units that reports its residual instead of closing"
description: "Storage change from a gauge elevation through a named area-capacity revision, gauged inflow and outflow in acre-feet, and a residual that names what is in it: ungauged inflow, precipitation on the water, evaporation, bank storage, the reach below the dam and travel time. Worked on Lake Powell for water year 2023, where the inflow gauges span 82.2 per cent of the basin above the dam and the residual is -211,545 acre-feet, 1.8 per cent of inflow."
tags: [reservoir, ledger, lake-powell, storage, inflow, outflow, datum, hydrology]
generated: { by: claude-code/opus-5, at: 2026-09-08T05:40:00Z }
inputs: "A capture of the reservoir's daily pool elevation on a declared datum; captures of the inflow and outflow gauges; the reservoir's area-capacity table with its survey revision; the drainage areas of each gauge from the site files"
expected: "Lake Powell, water year 2023, on NAVD88 against the 2018 table: pool 3532.00 to 3576.10 ft, storage 7,534,061 to 10,527,321 acre-feet, change +2,993,260 (+3.692 km3); gauged inflow 11,935,172 and outflow 8,730,367, so gauged inflow minus outflow is +3,204,805 and the residual is -211,545 acre-feet"
expected_uncertainty: "The residual is 1.8 per cent of inflow and 7.1 per cent of the storage change, and it is not an error bar: it is the sum of terms this ledger does not measure, whose individual sizes are not established here. The storage change's own sensitivity is dominated by the table revision and the datum match, both of which are stated rather than estimated"
status: draft
stale_after: 2027-03-08
---

# Reservoir ledger: report the residual, do not close the identity

**Method.** Over one window, in one volume unit:

    dS = I_gauged + I_ungauged + P - O - E - B

storage change, gauged inflow, ungauged inflow, precipitation on the
water surface, outflow, evaporation and bank storage. A gauge network
measures the first, the second and the fifth. The rest are named and
left in the residual, and the residual is reported as a residual.

**The temptation is to close it.** Every unmeasured term has a
plausible magnitude, and choosing values that make the identity balance
produces a ledger that looks finished. It is not a measurement: the
residual it absorbed was never explained, and the closed budget's
uncertainty cannot be written down. A reservoir operator reading a
ledger wants to know what was measured and what was not.

## Before computing anything

**Fix the datum.** The storage change is an elevation read into an
area-capacity table, and the two carry vertical datums that need not
agree. On the gauge side the parameter code is the authority: 62614 is
above NGVD29, 62615 is above NAVD88, 00062 is above a datum the site
file names. On the table side the survey states it. Where the gauge
publishes both national datums, their difference is the agency's own
conversion and can be used; where it does not, the offset is cited from
an authority or the ledger uses the datum the table is on. Never derive
the offset from the data being reconciled.

**Name the table revision.** Reservoirs are resurveyed and a survey
replaces the table. The revision goes in the receipt beside the volume.

**Count the ungauged fraction before you need it.** Add the inflow
gauges' drainage areas and compare with the outlet's. That fraction is
a term in the ledger, and a ledger that omits it closes better than it
should.

## The terms

**Storage change.** Both endpoint elevations into the table, both
volumes reported, the change as their difference, with the
interpolation named. Report the surface areas too: they are what makes
the evaporation term's absence quantifiable by a reader who wants to
bound it.

**Gauged inflow and outflow.** Daily discharge summed over the window,
converted once, with the conversion factor stated. Each gauge carries
its approval status and its drainage area.

**The residual.** What is left, reported with its sign, its size
against inflow, and an explicit list of what it contains.

## What the residual contains, and why none of it is measured here

- **Ungauged inflow.** The fraction of the basin above the dam that no
  inflow gauge in the ledger measures.
- **Precipitation on the water surface**, which the surface areas make
  boundable but which this ledger does not compute.
- **Evaporation**, which no gauge in the ledger measures and which the
  satellite evapotranspiration product cannot supply, since that
  product carries no estimate at all over open water.
- **Bank storage**, which moves into the surrounding rock while the
  reservoir fills and back out as it falls, so its sign follows the
  direction of the year.
- **The reach between the dam and the outflow gauge.** An outflow gauge
  below the dam is not the dam release; it collects whatever enters
  between them.
- **Travel time**, since inflow gauges are often hundreds of miles
  upstream and a window's inflow is not the water that arrived in it.

## What the ledger refuses

- A volume from a table whose revision is not named.
- A volume from an elevation whose datum does not match the table's
  column.
- An elevation outside the surveyed table, by extrapolation.
- A closure produced by assigning a value to an unmeasured term.
- A satellite-to-gauge elevation difference without both datums and a
  cited offset between them.

## The worked example

Lake Powell, water year 2023, on NAVD88 against the 2018 survey.

| Term | Value |
|---|---|
| Pool elevation, 2022-10-01 | 3532.00 ft NAVD88 (7,534,061 acre-feet, 59,286 acres) |
| Pool elevation, 2023-09-30 | 3576.10 ft NAVD88 (10,527,321 acre-feet, 77,259 acres) |
| Storage change | **+2,993,260 acre-feet** (+3.692 km3), a rise of 44.10 ft |
| Gauged inflow, three gauges | 11,935,172 acre-feet |
| Outflow at the downstream gauge | 8,730,367 acre-feet |
| Gauged inflow minus outflow | +3,204,805 acre-feet |
| **Residual** | **-211,545 acre-feet**, 1.8 per cent of inflow |

The inflow gauges drain 91,950 of the 111,800 square miles above the
outflow gauge, so **82.2 per cent of the basin is gauged** and the
remaining fifth arrives unmeasured.

**How to read the residual's sign.** It is negative: the reservoir
gained less than the gauged flows alone would give. Ungauged inflow and
precipitation push it positive, evaporation and bank storage push it
negative, and a filling reservoir moves water into its banks. So the
sign is consistent with evaporation and bank storage together exceeding
the ungauged inflow, which is a statement about which terms dominate
and not a measurement of any of them.

**What would make this a closed budget** is not a better fit. It is an
evaporation estimate with a source, a bank storage model with a
citation, and an ungauged inflow estimate from a method that can be
named. Each is a separate piece of work, and until they exist the
residual is the honest output.
