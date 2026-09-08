---
type: dataset-gotcha
title: "A log-Pearson III fit computed in a session is a screening number, not a flood frequency estimate"
description: "The published method involves expected moments, a regional skew weighted against the station skew, a historic period with a threshold, and censored values entering the fit as inequalities. A fit that reads the peaks and calls the quantile function implements none of that, and it produces a number in the same units with the same name. The record itself says why it matters: peaks flagged regulated or urbanized are excluded from the published analysis by default, and historic peaks are ignored unless a historic period is supplied."
tags: [flood-frequency, peakfq, bulletin-17c, log-pearson, statistics, hydrology, ownership]
generated: { by: claude-code/opus-5, at: 2026-09-07T23:50:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-08T04:19:42Z }
severity: high
dataset: ../datasets/usgs-peaks.md
eval_case: screening-fit-is-not-bulletin-17c
status: stable
stale_after: 2027-03-07
sources:
  - id: manual
    resource: https://pubs.usgs.gov/tm/2006/tm4b4/tm4b4.pdf
    title: "Flynn, Kirby and Hummel, 2006, User's Manual for Program PeakFQ, USGS Techniques and Methods 4-B4: the station option record (table B.3), the K and H options, the generalized skew and its standard error, and the qualification codes the program acts on (table B.4)"
  - id: b17c
    resource: https://pubs.usgs.gov/tm/04/b05/tm4b5.pdf
    title: "England, J.F., and others, 2018 (revised 2019), Guidelines for Determining Flood Flow Frequency, Bulletin 17C: USGS Techniques and Methods 4-B5: the expected moments algorithm, regional skew, historic information and low outlier treatment"
  - id: peaks
    resource: ../datasets/usgs-peaks.md
    title: "This bundle's peaks concept: the qualifier vocabulary and what the frequency program does with each code"
---

# A screening fit is not a flood frequency estimate

**Mechanism.** Fitting a log-Pearson III distribution to a column of
peaks takes three lines: log the values, take the moments, evaluate
the quantile. What comes back is a discharge in cubic feet per second
for a stated exceedance probability, which is the same shape of answer
the published method produces. It is not that answer.

The published method is the expected moments algorithm, with a
regional skew weighted against the station skew by their respective
standard errors, historic information entering through a historic
period length and a threshold, censored values entering as
inequalities rather than being dropped or treated as observed, and a
low-outlier test that changes which peaks are fitted.[^b17c] A
session-computed fit implements none of these. The gap is largest
exactly where flood estimates are used: at the rare end, on short
records, and at gauges whose largest floods are historic.

**Why the record makes this concrete.** The peak record's own
qualifiers control the published analysis.[^manual][^peaks] Peaks
flagged as affected by regulation or urbanization are **excluded** by
default and are only included if the station option record asks for
them; a historic peak is **ignored** unless a historic period length
is supplied, and any high outlier is then treated as an ordinary
systematic peak. So a fit that simply reads every row and takes
moments differs from the published one in which peaks it uses, before
any question of method.

**How large the station-skew term alone is.** The published method
weights the station skew against a regional skew because a single
station's skew is a noisy estimate, and the quantile is sensitive to
it. Thirty independent 130 year records drawn from one log-Pearson III
with a log skew of 0.3 (a synthetic demonstration, seeded and
reproducible in the peaks export golden, not a measurement of any
gauge) give station skews from -0.23 to +0.84 and 100 year estimates
from 31,100 to 63,400 cubic feet per second: **a factor of two, from
sampling noise alone, on records as long as any this collection
holds.** The population value is 43,300 and 13 of the 30 estimates
fall below it. That spread is one term of the several the published
method handles, and it is already wider than most people expect a
century of record to leave.

**Wrong-result mode.** Nothing raises. The screening number is
plausible, often within tens of per cent, and it is reported with a
return period, which is the form a permit, a design, or a floodplain
map consumes. Two specific directions: dropping historic peaks
removes the largest floods in a long record and leaves the curve low
at the rare end, while fitting through regulated peaks describes the
reservoir's operating rule and typically leaves it low as well. A
number quoted without an interval hides that the sampling uncertainty
on a hundred-year quantile from a hundred years of record is wide
enough to contain both answers.

**Correct approach.** Own what the tool can reproduce. A fit computed
in a session is labelled a screening fit in every field it writes, it
carries an interval on every quantile, and it states what it did not
implement. The frequency estimate comes from the program the field
uses, run by the analyst on the peak file the workflow exports, and
read back with its own confidence limits. Where a return period cannot
be given an interval, it is not reported at all. Where a record is
regulated, urbanized, historic-bearing or censored, the fit refuses
until the analyst says which convention they want and the receipt
records the choice.

**Verification.** Take a long unregulated record, compute a screening
fit, and compare its 1 per cent quantile against the published
estimate for the same gauge. Then drop the historic peaks and compute
it again: the difference between those two numbers, at one gauge, is
the size of one of the several effects the published method handles
and a screening fit does not.

[^manual]: the PeakFQ user's manual
[^b17c]: Bulletin 17C, the guidelines for determining flood flow frequency
[^peaks]: this bundle's annual peaks concept
