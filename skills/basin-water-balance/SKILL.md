---
name: basin-water-balance
description: "Close P + I - ET - Q - X = dS over a basin and a window from frozen observational inputs, through the attested computation and its attester: the storage term refused below the GRACE footprint floor, a regulated outlet flagged, imports and exports sourced or explicitly assumed zero, and the residual reported against the combined uncertainty of its terms with both bars stated."
---

# basin-water-balance

Turn "does this basin's water balance close" into a receipt: which
products, which window, which terms, what each term's uncertainty
rests on, and how far the residual is from zero in units of that
uncertainty. Works by slash command or conversationally ("close the
water balance for the upper Colorado in water year 2023", "why does
this basin refuse", "read me this receipt").

This skill carries the pointer, not the facts, and it carries no
number of its own: the footprint floor, the two bars, k, every term's
uncertainty figure and every measured residual live in the computation
concept and its recipe, and are read from there per run.

## Behavior, in order

1. **Parse and show back:** the basin (a polygon fixture with an
   equal-area area in its provenance), the window as dates, whether a
   frozen input tree already exists for that pair, and what the user
   means to do with the residual. A water balance quoted in a brief
   and a water balance used to size a groundwater term need different
   things said about the same number.
2. **Consult the bundle for this run first, in two tiers.** Consult
   installed knowledge concepts first, as the core `consult-knowledge`
   skill sets out (search terms: water balance, residual, mascon,
   footprint, floor, storage, regulated, run, fill, masked). The
   concepts live under this plugin's own root, whatever the
   installer's record lists for the hydrology plugin: read them from
   there before searching anywhere else.

   **Always, before answering anything:**
   - `${CLAUDE_PLUGIN_ROOT}/knowledge/computations/basin-water-balance.md`
     (the floor and its derivation, the epoch rule and the endpoint
     latency, the two bars, what each term's uncertainty rests on)

   **Then only what the request turns on:**
   - a window reaching past 2025-09 or into the current year:
     `knowledge/gotchas/imerg-run-mixing.md` for the run change and
     the seam
   - a residual to be interpreted, or a basin whose outlet is a dam:
     `knowledge/gotchas/nwis-regulated-gauge.md`
   - a basin holding open water, or an evapotranspiration term to be
     defended: `knowledge/gotchas/mod16-fill-over-water-barren-urban.md`
   - how to read a receipt, or what a bar-one pass does not mean:
     `knowledge/recipes/basin-water-balance.md`
   - the storage term's native scale or its uncertainty grids: the
     mascon dataset concept in the provider bundle

   The computation concept alone answers most questions about whether
   a basin and a window can be closed at all, and it names the others
   where they bind. A tool that reads one file per call spends a call
   on every concept, so reading all seven before answering a question
   about one of them can cost more than the answer is worth. Restate
   what applies and cite each by path.
3. **Check the three preconditions before computing anything**, in the
   order the recipe gives them: the basin against the footprint floor,
   the window against the mascon record's end, and the precipitation
   run declared for every month of the window. Say which of the three
   decides the answer. A basin below the floor is a refusal to state,
   not a problem to route around.
**Where the files are.** A path a user gives relative to the plugin
(`verification/fixtures/...`) resolves under `${CLAUDE_PLUGIN_ROOT}`,
not under the working directory: the fixtures ship with the plugin.
Resolve it there first rather than searching the filesystem, which is
slow and can find the wrong copy.

4. **Run the sanctioned computation, never a hand calculation.**
   `uv run ${CLAUDE_PLUGIN_ROOT}/knowledge/references/computations/basin_water_balance.py`
   with `--inputs` naming the frozen tree, `--imports` and `--exports`
   as VALUE_KM3:SOURCE where they are known, `--regulated` where the
   outlet is, and `--receipt` for the receipt. Then run the attester
   over that receipt:
   `uv run ${CLAUDE_PLUGIN_ROOT}/knowledge/references/attesters/basin_water_balance_check.py RECEIPT.json`.
   Report the attester's verdict, not your own reading of the numbers.
5. **Report the residual with what qualifies it:** the ratio to the
   combined sigma and its sign; the masked fraction and open-water
   handling of the evapotranspiration term; the regulated flag if set;
   the two epochs and their offsets from the window's ends; every
   import and export with its source, or the assumption in the words
   the receipt uses; and both bars with k. Where a term is missing and
   known to be real, say so and say which way it moves the residual.
6. **Where the storage term was refused,** give the three terms that
   do exist, name the floor and the basin's size against it, and say
   plainly that no residual follows. Offer the neighbouring larger
   basin if one is in hand.

## Must NOT

- Report a residual for a basin below the footprint floor, by ANY
  route: not from the mascon field, not from a gain or scale factor,
  and not from a hand calculation of P minus ET minus Q that simply
  leaves the storage term out. A budget missing a term is not a budget
  with a small residual; without dS there is no residual to report,
  and an arithmetic difference of the other three terms is a number
  with no meaning that a reader will take for closure.
- Fill an open storage endpoint by extrapolation, by substituting a
  nearby epoch silently, or by shortening the window without saying so.
- Add an import or export without a source, or leave the assumption
  unstated when none is known.
- Refuse a basin because its outlet is regulated: that is a flag on
  the discharge term.
- Present a residual as a hydrological finding without the combined
  sigma beside it, or a bar-one pass as evidence that the terms are
  correct.
- Compute any term by hand, edit the sanctioned computation, or read
  anything but the frozen tree at run time.
