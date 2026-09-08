---
type: dataset-gotcha
title: "SNODAS is a model output: comparable between periods, not a term in a water budget"
description: "The distributor's own guidance draws the line: not recommended for quantitative water budget analysis, while summing over an area between periods to compare them is reasonable. So a snow panel that contrasts two years is sanctioned and a snow storage change carried into P + I - ET - Q - X = dS is not. The product arrives beside observational products, on the same grid, in water-equivalent units, which is what makes it read like a term."
tags: [snodas, snow, swe, water-balance, model-output, budget, hydrology]
generated: { by: claude-code/opus-5, at: 2026-09-08T05:40:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-08T04:19:42Z }
severity: high
dataset: ../connectors/snodas-nsidc.md
eval_case: snodas-not-a-budget-term
status: stable
stale_after: 2027-03-08
sources:
  - id: faq
    resource: https://nsidc.org/data/user-resources/help-center/can-i-sum-snodas-values-given-area
    title: "The NSIDC help article 'Can I sum SNODAS values for a given area?', read 2026-09-08: the sentence that draws the line and the caveat that follows it"
  - id: connector
    resource: ../connectors/snodas-nsidc.md
    title: "This bundle's SNODAS connector concept: the route, the layers and their scales"
  - id: balance
    resource: ../recipes/basin-water-balance.md
    title: "This bundle's water balance recipe: the identity a snow term would enter, and the terms it does accept"
---

# SNODAS is a model output

**Mechanism.** SNODAS is an assimilation: a snow model driven by
analysed forcing and nudged toward observations. Its output arrives in
the same shape as the observational products beside it, on a regular
grid, in water-equivalent millimetres, daily, from a distributor whose
other holdings are measurements. Nothing in the file marks it as
different, and snow water equivalent is exactly the quantity a basin
water balance is missing when a residual will not close in spring.

**What the distributor actually says.** The line is narrower than a
ban and more useful:[^faq]

> SNODAS is a model output, so it is not recommended for use for
> quantitative water budget analysis. However, it is reasonable to sum
> values over a given area for a period of time, if, for example, you
> wanted to compare annual totals of snow water equivalent (SWE) for a
> given area.

So two different uses, with a line between them:

- **Sanctioned:** summing or averaging over an area and comparing
  periods. A snow panel that puts one water year beside another, over
  the same basin, by the same method, is the example the distributor
  itself gives.
- **Not recommended:** the quantitative water budget. A snow storage
  change carried into the basin identity as a term, or a residual
  attributed to snow, is the use the guidance declines to support.

The same article adds a caveat that matters for anyone summing the
precipitation forcing: it is split into non-snow (L00) and snow (L01)
components, both as water equivalent, and liquid rain onto snow raises
the snow water equivalent in the short term and can leave the pack
later.[^faq]

**And the term would be counted twice.** This reason is independent of
the guidance and holds even for a perfect snow product. The storage
term in the basin identity is a mascon difference, and terrestrial
water storage already includes snow: the pack sits on the ground the
satellites weigh. A snow water equivalent change added beside dS
therefore counts the same water twice, once in the mascon field and
once in its own term. So the substitution is not merely unsupported by
the product's provider; it is wrong on the identity's own terms, and
it would still be wrong if the snow number were an observation.

**Wrong-result mode.** A spring residual in a snowy basin is usually
large and positive, and a snow water equivalent change of the right
sign is sitting right there in a product on the same grid. Adding it
closes the budget, and the closure is the problem: the term did not
come from an observation of that basin, so the residual it absorbed
was never explained, and the uncertainty of the closed budget is
unstated because the added term has no published one. The failure
survives review because the number is physically reasonable, the units
are right, and the closure looks like success.

**Correct approach.** Keep the snow panel and label it. A drought or
flood view shows snow because snow is the story, and shows it as a
comparison: this year against that one, this basin, this method,
stated. Where a budget needs snow water equivalent as a term, it needs
a product whose provider supports that use, and the honest move is to
say the term is unavailable rather than to substitute one that is not
recommended for it. A residual that is really snow is better reported
as an unexplained residual with snow named as its likely home.

**Where the residual can legitimately go.** A spring residual has
cheaper explanations to rule out first. The mascon epochs are
mid-month while a water year's ends are not, so the storage difference
is measured between snapshots that do not line up with the flux window,
and in a melt season that offset costs real volume; the receipt records
the offset in days for exactly this reason. An unsourced import or
export is another. Both are arithmetic about the window rather than a
missing physical term, and both are worth exhausting before anything
is added to the identity.

**Verification.** Take a snowy basin and a spring window, compute the
water balance residual, then compute the snow water equivalent change
over the same window and basin from this product. Confirm they are the
same order of magnitude, which is what makes the substitution
tempting, and confirm that the budget receipt refuses the term or
carries it labelled as a model output outside the identity.

[^faq]: the NSIDC help article on summing SNODAS values
[^connector]: this bundle's SNODAS connector concept
[^balance]: this bundle's basin water balance recipe
