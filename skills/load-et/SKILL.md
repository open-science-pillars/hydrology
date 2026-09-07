---
name: load-et
description: "Basin-mean evapotranspiration over a frozen polygon from MOD16A2GF or MOD16A2 (the basin term: 8-day composites apportioned to calendar months in mm and km3, the seven fill classes excluded and counted, the masked fraction and the open-water choice stated) and from the OpenET ensemble where a polygon is under the service's per-request area cap (the sub-basin check, refused above the cap), with a receipt."
---

# load-et

Turn "evapotranspiration over this basin for this window" into a
monthly series with a receipt: which product, which cells, how much
of the basin has an estimate at all, what was done with the water,
rock and city inside it, and how the answer compares with an
independent product where both can see the same ground. Works by
slash command or conversationally ("MOD16 over the Roaring Fork for
2023", "the ET term for my water balance", "check that against
OpenET").

This skill carries the pointer, not the facts: every collection
name, DOI, unit, scale factor, fill code, compositing rule, quota,
area cap, ensemble statistic and access requirement lives in a
knowledge concept and is read from there per load, never restated
here.

## Behavior, in order

1. **Parse and show back:** the source (`mod16`, the default, or
   `openet`), the basin polygon (a fixture written by the
   delineate-basin skill, or any GeoJSON whose `provenance` carries
   an area and its projection), the window as dates, and for MOD16
   the product (`mod16a2gf`, gap-filled, or `mod16a2` for a period
   the gap-filled record does not reach). Say what the user means to
   do with the series: a water balance, a drought index and a
   field-scale comparison need different things said about the same
   number.
2. **Consult the bundle for this load first.** Consult installed
   knowledge concepts first, as the core `consult-knowledge` skill
   sets out (search terms: mod16, modis, evapotranspiration, et,
   fill, water, urban, barren, composite, openet, ensemble, area
   cap, provisional). The concepts live under this plugin's own root,
   whatever the installer's record lists for the hydrology plugin (a
   checkout loaded from a directory is not in that record, and an
   older installed version may be): read them from there before
   searching anywhere else.
   - `${CLAUDE_PLUGIN_ROOT}/knowledge/datasets/mod16a2gf.md`
   - `${CLAUDE_PLUGIN_ROOT}/knowledge/connectors/openet-api.md`
   - `${CLAUDE_PLUGIN_ROOT}/knowledge/gotchas/mod16-fill-over-water-barren-urban.md`
   - `${CLAUDE_PLUGIN_ROOT}/knowledge/gotchas/mod16-composite-to-month.md`
   - `${CLAUDE_PLUGIN_ROOT}/knowledge/gotchas/openet-area-cap.md`
   - `${CLAUDE_PLUGIN_ROOT}/knowledge/gotchas/openet-provisional-window.md`
   - `${CLAUDE_PLUGIN_ROOT}/knowledge/gotchas/openet-monthly-not-the-daily-sum.md`
   Restate what applies and cite each by path. The fill gotcha
   applies to every MOD16 basin mean; the area-cap gotcha applies
   before any OpenET request over anything larger than a field or a
   small hydrologic unit.
3. **Check the polygon against the cap before asking OpenET for
   anything.** The per-request cap is a property of the service
   (50,000 acres at Tier 1, 200,000 at Tier 2), and every basin in
   this plugin's fixtures is one to three orders of magnitude above
   it. Say the acreage and the multiple, and offer MOD16 for the
   basin or OpenET on a named sub-cap unit; never tile a basin into
   sub-cap pieces and average them, and never shrink the polygon
   until the service answers.
4. **Load through the script, not by hand.** Run
   `uv run ${CLAUDE_PLUGIN_ROOT}/verification/fixtures/load_et.py`
   (the script ships with this plugin; the variable is this plugin's
   installed root) with `--source`, `--basin PATH`, `--window FILE`
   for each MOD16 window file on disk, or `--response FILE` for a
   recorded OpenET answer, and `--out` for the receipt. Pull a
   missing MOD16 window with
   `uv run ${CLAUDE_PLUGIN_ROOT}/verification/fixtures/fetch_et_fixtures.py`
   (an Earthdata Login with the LP DAAC application authorized, as
   the dataset concept sets out). The script excludes every fill
   code, counts them by class, apportions composites to calendar
   months by their true length, and refuses rather than averaging
   when more than half the basin is masked.
5. **Report the number with what qualifies it.** Monthly and annual
   totals in mm and km3; the cells inside the polygon and the area
   they cover against the polygon's own area; the masked fraction
   and which classes it is; the open-water choice in words; the
   short composite periods that were weighted by their true length;
   and, when the basin holds open water, the sentence that the
   reservoir's own evaporation is not in this number and has to come
   from elsewhere. For OpenET add the access date and whether any
   month falls inside the 120-day provisional window, and check the
   monthly series for repeated values before handing it over.
6. **Offer the check, where it is possible.** On a polygon under the
   cap, the OpenET ensemble beside MOD16 is an independent estimate,
   and the disagreement is a fact to carry rather than resolve: over
   the fixture unit it is about a quarter of the annual total. On a
   basin, say plainly that no second product is available at this
   scale in this bundle.

## Must NOT

- Present a MOD16 basin mean without the masked fraction, or read a
  fill code as zero evapotranspiration.
- Apply a land evapotranspiration rate to the part of a basin that
  carries no estimate, in a mean or in a volume.
- Divide every composite by eight, or assign composites to months by
  their start date.
- Mix MOD16A2GF and MOD16A2 in one series without saying where the
  product changes.
- Send an OpenET request for a polygon above the account's cap, tile
  a basin to get round the cap, or present a sub-cap unit's number as
  a basin's.
- Put the OpenET key anywhere but the `Authorization` header of a
  request to the service, and never in a URL, a log, a fixture or a
  receipt.
- Call the OpenET ensemble a median, or quote provisional months
  without saying they will change.
