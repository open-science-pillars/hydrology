---
name: drought-anatomy
description: "Assemble a drought view as a set of receipted panels, each labelled with its product, its run or version and its own refusal: precipitation, soil moisture, streamflow and storage as the quantitative panels, snow as a qualitative one. Carries no number of its own and never reduces the panels to a single index."
---

# drought-anatomy

Build the picture of a drought from several products at once, without
letting any one of them borrow another's validity. Works by slash
command or conversationally ("show me the drought anatomy for this
basin, water year 2021 against 2023").

## Behavior, in order

1. **Parse and show back:** the basin, the two periods being compared,
   and which panels the request implies.
2. **Check the basin against the storage footprint floor first.** The
   storage panel comes from mascons whose native scale is about one
   mascon, and a basin below that floor has no storage signal of its
   own. Say so before drawing anything: a four-panel view with a
   stated refusal is the honest answer, and a four-panel view with an
   unexplained gap is not.
3. **Consult the bundle for each panel.** Consult installed knowledge
   concepts first, as the core `consult-knowledge` skill sets out. Each
   panel is governed by its own concepts and they do not transfer:
   the precipitation run rule, the evapotranspiration fill classes, the
   soil moisture retrieval's coverage and its short record, the
   regulated-gauge caution, the mascon footprint and lag, and the snow
   product's model-output status. Restate what applies per panel and
   cite each by path.
4. **Assemble panels, not an index.** Every panel carries its product,
   its run or version, its period, the count behind each number, and
   the one sentence that says what it cannot show. Panels are shown
   side by side and are never averaged, ranked together, or reduced to
   a single drought number: they measure different quantities with
   different validity and a composite index would hide exactly the
   disagreements that make the view worth having.
5. **Say what each panel cannot show, in the panel.** A regulated
   outlet is an operations record rather than a runoff signal. A soil
   moisture mean over a winter day rests on the cells that were
   retrieved, which in a snowy basin can be a small fraction of the
   basin. A storage panel stops where the record stops. A snow panel is
   a model output and a comparison, never a term.
6. **Summary as provenance:** basin with its area and its standing
   against the floor, the periods, each panel with its product and
   version, the fixtures or receipts behind it with their hashes, the
   concepts consulted, and every refusal that fired.

## Must NOT

- Never reduce the panels to a single index, score or ranking.
- Never draw a storage panel for a basin below the footprint floor,
  and never extend one past the record's last epoch.
- Never put a snow number into a water budget, or offer one as the
  explanation of a residual without labelling it a model output
  outside the identity.
- Never compare a precipitation panel's present against a climatology
  built from a different run.
- Never report a soil moisture mean without the count of cells behind
  it, and never read a fall in that mean across a freeze as drying.
- Never read a flat streamflow panel at a regulated gauge as evidence
  that a drought is absent or over.
- Never restate a product rule this skill could consult: every rule
  above lives in a concept and is read from it per run, which is what
  lets a corrected concept change this skill's behavior without an
  edit here.

## The shape of a good answer

The panels disagree about how large the drought is, because they
measure different things over different depths and times. That
disagreement is the finding, not a defect to be reconciled. A view
whose panels all agree is usually a view whose panels were drawn from
one product.
