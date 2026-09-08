---
type: recipe
title: "Confronting a satellite river elevation with a gauge: score the changes, publish the level difference, call neither a bias"
description: "How a SWOT reach is placed beside a gauge when the two are on different vertical references: name the collection, pair each pass with a gauge reading inside a stated tolerance, score the changes because a change is insensitive to a constant datum offset, and report the level difference separately in language that does not make it a bias. Worked on the Mississippi at Baton Rouge for 2024: 50 of 52 passes paired, change correlation +0.957, change RMSD 0.382 m against a gauge spread of 1.196 m, and a level difference of -0.243 m that is not a measurement of anything."
tags: [swot, confrontation, gauge, stage, datum, skill-scores, hydrology]
generated: { by: claude-code/opus-5, at: 2026-09-08T06:35:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-08T05:18:36Z }
inputs: "A steward-accepted reach-gauge pair; Hydrocron passes for the reach with the collection named; the gauge's instantaneous stage with its approval status and the gauge datum from the site file"
expected: "Reach 74210000331 against USGS-07374000, calendar 2024, collection SWOT_L2_HR_RiverSP_reach_D: 50 of 52 passes paired within 15 minutes; on 49 changes, mean error +0.0019 m with a 95 per cent sampling interval of [-0.1062, +0.1101], RMSD 0.3823 m, correlation +0.9567, against a gauge change spread of 1.1959 m; the level difference is -0.2429 m [-0.3442, -0.1416] with a spread of 0.301 m"
expected_uncertainty: "The intervals are sampling intervals under a lag-1 autocorrelation model with the effective sample size capped at the count, and they carry neither the satellite's published per-pass uncertainty (median 0.096 m here) nor the gauge's. The level difference additionally contains an uncited offset between the geoid model and the national datum, which is why it is not scored"
status: stable
stale_after: 2027-03-08
---

# Confronting a satellite river elevation with a gauge

**Method.** Pair each satellite pass with a gauge reading inside a
stated time tolerance, difference the paired series, and score the
changes. Report the level difference beside the scores, in language
that says what it contains.

**Why the changes are the confrontation.** The satellite reports
elevation against a geoid model and the gauge against a national
vertical datum. The offset between those two surfaces is not published
for an arbitrary pair, so a level difference is a real signal plus an
uncited constant: uninterpretable rather than merely uncertain. A
change over an interval is insensitive to any constant offset, so it
can be scored without the citation. Where the offset can be cited from
an authority, the level becomes scorable too and the citation goes in
the receipt.

## Before scoring

**Name the collection.** The service picks a product version when the
caller does not, and the versions differ by metres on the same reach.
The receipt records which collection answered.

**Read the gauge's datum and its parameter.** Stage is height above the
gauge datum, so an elevation is stage plus the datum's own altitude, on
the datum the site file names. A gauge whose datum sits at zero makes
stage and elevation coincide, which is a property of that site and not
a rule.

**Check the approval status of the window.** A gauge record is approved
in arrears, and a satellite record is recent by construction, so the
overlap between the two is often provisional on the gauge side. That is
a fact about the confrontation and belongs in the scores' caption.

**State the pairing tolerance.** The satellite sees an instant; the
gauge reports at an interval. A pass with no reading inside the
tolerance is dropped by name and counted, never matched to the nearest
reading at any distance.

## The scores

Four numbers, in the form the ocean confrontations use, each with a
sampling interval:

- **Mean error of the change**, which is the confrontation's bias term
  and the one a constant datum offset cannot touch.
- **Root mean square difference of the change**, the size of the
  disagreement including everything the mean does not capture.
- **Correlation of the changes**, which says whether the satellite sees
  the same rises and falls.
- **The gauge's own change spread**, so the RMSD can be read against
  the signal rather than in isolation. A RMSD of a third of the spread
  is a different statement from a RMSD equal to it.

**The intervals are sampling intervals** under a lag-1 autocorrelation
model, with the effective sample size **capped at the count**. The cap
matters: differencing a series induces negative lag-1 correlation, and
an uncapped formula then returns an effective sample larger than the
series, so a change series claims more information than it holds.

They carry neither instrument uncertainty. The satellite publishes a
per-pass uncertainty and the receipt reports it separately, so a reader
can see whether the disagreement is explained by the product's own
stated precision. Here it is not: the RMSD is about four times it.

## What the recipe refuses

- Scoring a level difference across two vertical references without a
  cited offset between them, or calling such a difference a bias.
- A pass matched to a gauge reading outside the stated tolerance.
- A confrontation on fewer than ten pairs.
- The word confrontation for a comparison against a product whose
  algorithm was constrained with gauge-informed priors. That is a
  consistency check, and the distinction is the convention this bundle
  keeps.
- An unnamed collection.

## The worked example

Mississippi River at Baton Rouge, reach 74210000331 against gauge
USGS-07374000, 0.44 km apart, calendar 2024, collection
`SWOT_L2_HR_RiverSP_reach_D`, 50 of 52 passes paired within 15 minutes.

| Score | Value |
|---|---|
| Mean error of the change | +0.0019 m, 95 per cent [-0.1062, +0.1101] |
| RMSD of the change | 0.3823 m |
| Correlation of the changes | +0.9567 |
| Gauge change spread | 1.1959 m |
| RMSD over spread | 0.320 |

| Reported separately | Value |
|---|---|
| Level difference | -0.2429 m, 95 per cent [-0.3442, -0.1416], spread 0.301 m |
| Satellite's own per-pass uncertainty | median 0.096 m |
| Gauge approval in this window | provisional throughout |

**How to read it.** The satellite follows this river's rises and falls
closely: the changes correlate at 0.957 and their mean error is
indistinguishable from zero, at about a third of the signal's own
spread. The level sits 0.24 m below the gauge, and that number is not a
bias, a calibration or a validation result. It is a level difference
containing an uncited datum offset, and the near-zero mean error in the
changes is what says the offset is close to constant rather than
drifting.

**What would make the level scorable** is a citation: an authoritative
relationship between the geoid model the product uses and the datum the
gauge is on, at this location. Until then the honest output is the
change scores and a labelled level difference.
