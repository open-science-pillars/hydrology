---
type: recipe
spheres: [hydrosphere, cryosphere]
title: "Drought anatomy: five panels, five sets of facts, and no single number"
description: "How to show a drought from several products at once without letting any of them borrow another's validity: precipitation, soil moisture, streamflow and terrestrial water storage as the quantitative panels, snow as a qualitative one, each labelled with its product, its run or version, the counts behind it and the one thing it cannot show. Worked on the Colorado above Lees Ferry, water year 2021 against water year 2023, where the panels disagree about the size of the drought by more than an order of magnitude and one of them does not show it at all."
tags: [drought, panels, imerg, smap, grace, snodas, streamflow, composite, hydrology]
generated: { by: claude-code/opus-5, at: 2026-09-08T06:10:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-08T04:19:42Z }
inputs: "A basin polygon with its equal-area area; a precipitation loader receipt with its run declared; a soil moisture series carrying the retrieved-cell count per day; a discharge capture with its regulation status; the basin's mascon series; a snow water equivalent series over the same basin"
expected: "The Colorado above Lees Ferry (276,444 km2, 2.48 mascons), water year 2021 against 2023: precipitation 257.2 against 320.4 mm, peak basin-mean snow water equivalent 64.8 against 163.1 mm, mean discharge 11,435 against 12,059 ft3/s at a regulated outlet, and storage moving -0.5 cm across the drought year against +4.8 cm across the wet one"
expected_uncertainty: "Each panel carries its own and they do not combine: the mascon series has a formal uncertainty near 1.9 cm per epoch against a seasonal range of 10 cm in the drought year and 17 in the wet one; the soil moisture mean has the count of retrieved cells behind it, which in winter is a small fraction of the basin; the snow panel is a model output with no published uncertainty and is comparative only"
status: stable
stale_after: 2027-03-08
---

# Drought anatomy: five panels, and what each one cannot show

**Method.** Draw each panel from its own product, label it with that
product's version and run, put the count behind every number beside
it, and state in the panel the one thing it cannot show. Then put the
periods side by side and read the disagreement, because the
disagreement is the finding.

**Do not build an index.** A single drought number from five products
hides the one thing a five-product view is for. The panels measure
different quantities, over different depths, at different times, with
different validity; averaging them produces a number whose uncertainty
cannot be written down and whose movement cannot be attributed.

## Before drawing anything

**Check the basin against the storage footprint floor.** The storage
panel comes from mascons, whose native scale is about one mascon, near
111,000 km2 as derived from the product's own geometry. A basin below
that has no storage signal of its own: the panel is refused, and the
view is four panels with a stated refusal rather than four panels and
an unexplained gap. This is the first question because it is the one
that changes what can be shown.

## The panels

**Precipitation.** One run for the whole series, declared, with any
seam named. The run matters more than it looks: the runs share a
variable name and differ in calibration, and the run that covers the
present is not the run that covers the archive, so a present ranked
against an archive climatology is ranking a calibration change. Where
a rank is wanted and the runs will not allow it, the panel reports
totals and compares periods instead, or uses the gauge-based forcing
series with the satellite product as context.

**Soil moisture.** The mean, and beside it the count of cells actually
retrieved and what fraction of the basin they are. The retrieval skips
frozen, snow covered, densely vegetated and open water ground, so
coverage moves through the year, and in a snowy basin a winter mean
can rest on a few per cent of the cells. A drop in the mean across a
freeze is the sampling moving, not the soil drying. The record is
about a decade long, which is too short for the kind of percentile a
century-long gauge record supports, so this panel compares periods
rather than ranking one.

**Streamflow.** The gauge's own record, with its approval status,
qualifiers and, above all, its regulation. Below a major dam the panel
is an operations record: it will not fall in a drought the way an
unregulated river does, because the release schedule is a decision
rather than a response. The panel is kept and labelled, never quietly
dropped, because a reader who sees four panels and no streamflow will
assume the river was not gauged.

**Storage.** The basin's mascon series, with the mascon count as the
effective sample size rather than the cell count, and the record's
last epoch stated. The record runs a quarter or so behind the present,
so this panel stops before the others and says where. Its formal
uncertainty is per epoch and is not small against a seasonal range.

**Snow, qualitative.** A model output, shown as a comparison between
periods over one basin by one method, which is the use its distributor
sanctions, and never a term in a water budget, which is the use it
declines to support. In a snowmelt basin this panel usually carries
the clearest signal of the five, which is exactly why the line matters.

## What the panels refuse

- A storage panel for a basin below the footprint floor, by any route.
- A storage panel drawn past the record's last epoch.
- A precipitation deficit computed across a change of run.
- A soil moisture mean without the count of cells behind it.
- A snow number inside a water balance identity.
- Any single index, score or ranking combining the panels.

## The worked example

Colorado River above Lees Ferry, 276,443.7 km2, which is 2.48 mascons,
so the storage panel is allowed. Water year 2021 against water year
2023, one of the driest years of the recent record against one of the
wettest snow years in two decades.

| Panel | Water year 2021 | Water year 2023 | Ratio |
|---|---|---|---|
| Precipitation (IMERG Final V07) | 257.2 mm | 320.4 mm | 1.25 |
| Snow, peak basin-mean SWE (SNODAS) | 64.8 mm on 2021-04-01 | 163.1 mm on 2023-04-01 | 2.52 |
| Streamflow, mean (USGS-09380000, regulated) | 11,435 ft3/s | 12,059 ft3/s | 1.05 |
| Storage, change across the year (mascon) | -0.5 cm | +4.8 cm | sign change |

**Read the disagreement.** Precipitation says the wet year had a
quarter more water. Snow says it had two and a half times as much at
the peak. Storage says the drought year ended where it began while the
wet year gained nearly 5 cm across the basin, which is the only panel
that speaks in a volume the basin actually kept. And streamflow, five
per cent apart, says almost nothing at all, because the gauge is below
Glen Canyon Dam and the release is a decision.

Each of those is correct about what it measures. The precipitation
figure is depth over the whole basin, most of which is dry most of the
year; the snow figure is the fraction of that depth that was stored as
snow at the peak, where the drought signal concentrates; the storage
figure integrates everything, including groundwater and reservoirs,
over the mascon footprint. The ratios differ because the quantities
differ, and a single index would have averaged that into silence.

**The panel that shows nothing is not a broken panel.** A reader who
takes the flat streamflow record as evidence that the drought was mild
has read an operating rule as hydrology. That is the failure this
recipe is shaped to prevent, and it is why the regulation label sits
in the panel rather than in a footnote.
