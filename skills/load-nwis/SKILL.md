---
name: load-nwis
description: "Load USGS NWIS streamflow with the volume gate: sites, parameters, windows parsed; provisional flags surfaced and segregated; provenance summary."
---

# load-nwis

Bring NWIS records into the session safely. Authored in Session 16 per
SPEC v0.6 §10; the gate contract follows load-swot.

## Behavior, in order

1. **Parse and show back:** sites (as strings), parameter codes,
   window, dv vs iv cadence.
2. **Knowledge first, restated:** the provisional gotcha whenever the
   window touches roughly the last year (the P-to-A transition is
   site-dependent and unannounced); rating-revision note for older
   extremes.
3. **Volume sanity before fetching:** dv pulls are small; iv pulls
   over years times many sites are not; estimate rows and apply the
   local-config gate above threshold with a smaller alternative.
4. **Load with flags kept:** qualifier columns retained; P/A/estimated
   accounting reported; nothing dropped silently.
5. **Summary as provenance:** sites with names, parameters and units,
   window, row counts by qualifier, cadence, the API actually used
   (waterdata vs legacy nwis), cache location, concepts consulted.

## Must NOT

- Never fetch above the gate without explicit confirmation.
- Never strip qualifier columns.
- Never deliver mixed provisional/approved statistics unsplit.
- Never round or re-type site identifiers.
