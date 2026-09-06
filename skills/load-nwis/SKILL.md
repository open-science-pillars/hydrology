---
name: load-nwis
description: "Load USGS streamflow from the Water Data API through dataretrieval's waterdata module with the volume gate: sites, parameters, windows parsed; approval status and qualifiers surfaced and segregated; provenance summary."
---

# load-nwis

Bring NWIS records into the session safely. Works by slash command or
conversationally ("load daily discharge for site 09380000, 2023").

## Behavior, in order

1. **Parse and show back:** sites, parameter codes, window, dv vs iv
   cadence.
2. **Consult the bundle for this load first.** Consult installed
   knowledge concepts first, as the core `consult-knowledge` skill
   sets out, by the sites, parameter, and window in play; the nwis
   skill lists the concepts this plugin resolves to. Read the
   connector concept (endpoints, paging, the optional key, depth per
   collection, the rate limit) and the streamflow dataset concept
   (site-identifier typing, the approval status and qualifier
   vocabulary and their meaning, the rating curve and its revisions,
   daily vs continuous structure, the deprecated client) and the gotchas the
   request or downstream intent triggers (the provisional-data caution
   whenever the window reaches the trailing period; the
   regulated-gauge caution for any drought, low-flow, or trend
   framing). Restate what applies and cite each by path; do not carry
   these facts in this skill.
3. **Volume sanity before fetching (hard gate).** Estimate rows (iv is
   far denser than dv; rows scale with sites times window length) and
   apply the project local-config threshold. At or below: state the
   estimate and destination, proceed. Above: STOP, present the estimate
   and a smaller alternative (shorter window, dv instead of iv, fewer
   sites), and wait for explicit confirmation.
4. **Load with flags kept:** fetch through dataretrieval's `waterdata`
   module (`get_daily` for daily statistics, `get_continuous` for
   instantaneous values), with the approval status and qualifier
   columns retained; the accounting reported per the vocabulary the
   dataset concept defines; nothing dropped silently.
5. **Summary as provenance:** sites with names, parameters and units,
   window, row counts by approval status and qualifier, cadence, the
   request URL the client reports (never the key), whether a key was
   in the environment, dataretrieval's version, cache location, and
   the concepts consulted.

## Must NOT

- Never fetch above the gate threshold without explicit confirmation, on
  any surface. (Hard gate: fires without consulting anything.)
- Never fetch through dataretrieval's `nwis` module or the legacy
  Water Services host; the connector concept records why and until
  when they answer.
- Never restate a dataset rule this skill could consult: the qualifier
  handling, the site-identifier typing, and the provisional and
  regulated-gauge cautions live in the NWIS concepts the nwis skill
  lists and are read from them per load, not carried here. That is what
  lets a revised gotcha change this skill's behavior without editing it.
