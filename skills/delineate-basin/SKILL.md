---
name: delineate-basin
description: "Delineate a basin as a polygon with provenance: a gauge number, a point, or a list of hydrologic unit codes; the NLDI trace (a point snapped through hydrolocation first) or a Watershed Boundary Dataset union; area in an equal-area projection beside the gauge's drainage area; a terminal basin returned with the statement that it has no outlet."
---

# delineate-basin

Turn "the basin above this gauge", "the watershed of this point" or
"these hydrologic units" into a polygon on disk with a provenance
row, an area and an honest comparison. Works by slash command or
conversationally ("delineate the basin above 09085000", "what drains
to -107.33, 39.55", "the Tulare Lake Bed subbasin, 18030012").

This skill carries the pointer, not the facts: every endpoint,
parameter default, timing, outage shape, snapping rule, projection
choice, comparison rule and outlet rule lives in a knowledge concept
and is read from there per delineation, never restated here.

## Behavior, in order

1. **Parse and show back:** which of the three inputs was given (a
   site number as a string with its leading zeros; a point as
   longitude then latitude; one or more hydrologic unit codes of one
   length), and what the user means to do with the polygon.
2. **Consult the bundle for this delineation first.** Consult
   installed knowledge concepts first, as the core `consult-knowledge`
   skill sets out (search terms: nldi, basin, watershed, huc,
   hydrologic unit, wbd, delineation, snap, outlet, terminal). Read
   the NLDI connector concept (endpoints, the two point routes and
   which one snaps, the parameter defaults, timing, what a 502 with
   an upstream 400 means, what the trace measures and how it compares
   with the drainage area) and the Watershed Boundary Dataset concept
   (layers, fields, versioning, the unit types and the outlet field),
   and the gotchas the input triggers: the unsnapped-point trap for
   any point input, the terminal-basin trap for any region known or
   suspected to be closed. Restate what applies and cite each by
   path. The concepts this plugin resolves to today:
   - `knowledge/connectors/nldi-basin.md`
   - `knowledge/datasets/usgs-wbd.md`
   - `knowledge/gotchas/nldi-unsnapped-point.md`
   - `knowledge/gotchas/usgs-terminal-basin-no-outlet.md`
3. **Delineate through the script, not by hand.** Run
   `uv run ${CLAUDE_PLUGIN_ROOT}/verification/fixtures/delineate_basin.py`
   (the script ships with this plugin; the variable is this plugin's
   installed root) with `--gauge SITE`, `--point LON LAT` or `--huc
   CODE...`,
   `--compare SITE` where a gauge's published drainage area is the
   right comparison, `--name` and `--out` for where the polygon
   goes. The script sources the trace or the union, snaps a point
   through the route the connector concept names before tracing,
   stops with nothing written when it cannot snap, measures the
   polygon in the equal-area projection the concept names, and
   writes the GeoJSON with a `provenance` member (source, requests,
   date, version, geometry sha256, area and projection, snap or units,
   comparison, outlet). Report the summary line it prints. For a
   point, the snap line (distance moved, reach, its subbasin, measure)
   is checked against the river the user named, or the comparison
   gauge's hydrologic unit: a snap of hundreds of metres or a reach in
   another subbasin means the nearest flowline is probably not the
   river meant, and the polygon waits for the user's confirmation or
   a better position, as the gotcha concept sets out.
4. **Say what the number is.** The area is stated with its projection
   and beside the gauge's published total drainage area and
   contributing area where they exist, with the difference and, from
   the connector concept, why a trace and a drainage area differ by
   construction on a basin with closed ground; no published
   contributing area means say so, not a guess. A union of units
   states its member count and the per-unit version fields.
5. **Terminal basins.** When the provenance says the basin has no
   outlet, say so in the answer: no gauge measures its outflow, and a
   budget built on it closes on storage and evapotranspiration.
6. **Summary as provenance:** the input as parsed, the source and
   request URLs (no credential exists on these hosts), the retrieval
   date, the fixture path and its geometry hash, the area and its
   projection, the comparison, the snap or the units, the outlet
   statement, and the concepts consulted.

## Must NOT

- Never trace a basin from a raw point: a point goes through the
  snapping route first, and when that route cannot answer the
  delineation stops and says so. The gotcha concept records why the
  fallback carries no evidence. (Hard rule: fires on every point.)
- Never present a snapped point's polygon without its snap distance
  and reach, and never as the basin of a river the reach does not
  belong to.
- Never invent a contributing area, a drainage area or an outlet: a
  null field is reported as absent, a closed basin as closed.
- Never state an area without its projection, and never present the
  network trace as the gauge's drainage area.
- Never carry an endpoint, a default, a number or a rule in this
  file; read it from the concept that owns it and cite the path, so a
  corrected concept changes this skill's behavior without an edit
  here.
