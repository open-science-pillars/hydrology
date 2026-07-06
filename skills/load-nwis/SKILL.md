---
name: load-nwis
description: "Load USGS NWIS streamflow with the volume gate: sites, parameters, windows parsed; provisional flags surfaced and segregated; provenance summary."
---

# load-nwis

Bring NWIS records into the session safely. Works by slash command or
conversationally ("load daily discharge for site 09380000, 2023").

## Behavior, in order

1. **Parse and show back:** sites, parameter codes, window, dv vs iv
   cadence.
2. **Consult the bundle for this load first.** Discover and read the
   concepts that apply (glob `knowledge/`), do not restate them from
   memory: the streamflow dataset concept (site-identifier typing, the
   qualifier codes and their meaning, the rating curve and its
   revisions, dv/iv structure, the current vs deprecated API) and the
   gotchas the request or downstream intent triggers (the provisional-
   data caution whenever the window reaches the trailing period; the
   regulated-gauge caution for any drought, low-flow, or trend framing).
   Restate what applies and cite each by path; do not carry these facts
   in this skill.
3. **Volume sanity before fetching (hard gate).** Estimate rows (iv is
   far denser than dv; rows scale with sites times window length) and
   apply the project local-config threshold. At or below: state the
   estimate and destination, proceed. Above: STOP, present the estimate
   and a smaller alternative (shorter window, dv instead of iv, fewer
   sites), and wait for explicit confirmation.
4. **Load with flags kept:** qualifier columns retained; the qualifier
   accounting reported per the codes the dataset concept defines;
   nothing dropped silently.
5. **Summary as provenance:** sites with names, parameters and units,
   window, row counts by qualifier, cadence, the API actually used
   (waterdata vs legacy nwis), cache location, and the concepts
   consulted.

## Must NOT

- Never fetch above the gate threshold without explicit confirmation, on
  any surface. (Hard gate: fires without consulting anything.)
- Never restate a dataset rule this skill could consult: the qualifier
  handling, the site-identifier typing, and the provisional and
  regulated-gauge cautions live in the NWIS concepts (glob `knowledge/`)
  and are read from them per load, not carried here. That is what lets a
  revised gotcha change this skill's behavior without editing it.
