---
type: recipe
title: "Basin water balance: when the identity can be closed from observations, and what it refuses"
description: "How to run P + I - ET - Q - X = dS over a basin and a window, what has to be true before it is worth running (a basin above the GRACE footprint floor, a window inside the mascon record, a declared precipitation run), how to read the receipt (the masked fraction, the regulated flag, the epochs and their offsets, the residual against its combined sigma), and the three cases it refuses rather than approximates."
tags: [water-balance, basin, grace, imerg, mod16, discharge, residual, hydrology]
generated: { by: claude-code/fable-5, at: 2026-09-07T05:00:00Z }
inputs: "A frozen input tree for one basin and window: the basin polygon with its equal-area area, the precipitation and evapotranspiration loader receipts, a discharge capture's canonical body, and the basin's mascon series; imports and exports as values with sources, or the explicit assumption of none"
expected: "Water year 2023 measured on the three fixture basins: Ohio at Olmsted residual +70.174 km3 against a combined sigma of 96.874 (+0.72 sigma, PASS); Colorado above Lees Ferry -19.117 against 19.165 (-1.00 sigma, PASS, outlet regulated, exports term missing); Roaring Fork refused on the storage term at 3.4 per cent of one mascon"
expected_uncertainty: "The combined sigma is the quadrature sum of four documented one-sigma figures (P 10 per cent, ET 20 per cent, Q 5 per cent at a good rating, dS the product's own per-mascon grid over the square root of the mascons the basin spans); it is dominated by ET on a wet basin and by dS on a dry one"
status: draft
stale_after: 2027-03-07
---

# Basin water balance: when the identity can be closed from observations

**Method.** Freeze the four terms for one basin and one window, run
the attested computation over the frozen tree, and read the residual
against the combined uncertainty of its terms. The computation concept
holds the contract, the floor derivation and the two bars:
[basin-water-balance](../computations/basin-water-balance.md).

## Before it is worth running

Three questions, in this order, because each can end the exercise:

1. **Is the basin above the footprint floor?** The storage term comes
   from GRACE mascons, whose native scale is the mascon: about
   111,000 km2, derived from the product's own geometry. A basin
   smaller than one mascon has no storage signal of its own and the
   computation refuses the term. There is no workaround, and the
   product's gain factors are not one.
2. **Does the window fall inside the mascon record?** The record runs
   two to three months behind the present. A window whose end is
   later has an open closing endpoint: the computation reports it as
   open and never fills it. Wait, or shorten the window.
3. **Is the precipitation run declared?** IMERG's three runs share a
   variable name and differ in calibration, and the Final record ends
   2025-09-30. A window reaching past that is a different run, named
   per month, with the seam in the receipt.

If all three pass, the terms are worth freezing. If the first fails,
the honest deliverable is P, ET and Q with the storage term named as
refused, which is still a useful description of a basin.

## How to read the receipt

- **The residual against its sigma, not on its own.** A residual of
  70 km3 sounds large and is 0.72 sigma on the Ohio; a residual of 19
  km3 sounds smaller and is a full sigma on the Colorado. The ratio is
  the number to quote, and the sign says which way the terms miss:
  positive means the terms deliver more water than the storage change
  accounts for.
- **The masked fraction of the evapotranspiration term.** MOD16 does
  not compute evapotranspiration over water, rock, city, ice or
  wetland, so the ET term is land evapotranspiration over the cells
  that carry an estimate. A basin holding a large reservoir is missing
  that reservoir's evaporation from the term entirely, and the
  receipt's masked fraction is how much of the basin that is.
- **The regulated flag.** A regulated outlet measures operations as
  well as hydrology. The flag does not change the bars and does not
  disqualify the basin; it changes what the residual is a statement
  about.
- **The epochs and their offsets.** Mascon epochs are mid-month, so a
  water year is measured between two mid-September epochs and the
  receipt says so in days. A budget quoted as "water year 2023" whose
  storage term spans 16 September to 16 September is not wrong, but
  the offset belongs in the methods.
- **Imports and exports.** Every entry has a source, or the receipt
  says none is known and assumes zero. An assumed zero is a claim: on
  the Colorado above Lees Ferry the transmountain exports are real,
  unsourced here, and their absence makes the residual an upper bound
  on closure rather than closure.

## What it refuses

- **A basin below the floor**, with the floor and the basin's size
  named. Not approximated, not rescaled, and not routed around: the
  three terms that do exist are worth reporting, but their arithmetic
  difference is not a residual. P minus ET minus Q with the storage
  term silently absent is the shape this refusal is most often
  defeated by, and it reads exactly like a closure to anyone who did
  not watch it being made.
- **A frozen tree whose bytes have moved** since it was frozen: the
  receipt's whole claim is that these inputs produced these numbers.
- **An import or export with a value and no source.** An unsourced
  transfer is the term that quietly closes a budget.

## What a pass means, and does not

Bar one asks whether the residual is within k sigma of the terms, with
k=2. A basin that passes is consistent with its four products. It is
not thereby correct: four products can be jointly wrong, an omitted
term can hide inside the uncertainty of a large one, and a wet basin's
sigma is dominated by evapotranspiration at 20 per cent, which is
generous enough to swallow a great deal. Bar two asks only that the
receipt reproduces, which is a statement about bookkeeping rather than
about hydrology. Quote both bars and the residual ratio, and treat a
pass as the beginning of an argument.

## Worked anchors (water year 2023)

| Basin | Residual km3 | Combined sigma | Ratio | What it shows |
|---|---|---|---|---|
| Ohio at Olmsted, 524,136 km2 | +70.174 | 96.874 | +0.72 | a large wet basin closing comfortably, its sigma dominated by the evapotranspiration term |
| Colorado above Lees Ferry, 276,444 km2 | -19.117 | 19.165 | -1.00 | a regulated outlet, a missing exports term, and a storage rise the other terms do not deliver |
| Roaring Fork, 3,767 km2 | not reported | not applicable | not applicable | the refusal: 3.4 per cent of one mascon |
