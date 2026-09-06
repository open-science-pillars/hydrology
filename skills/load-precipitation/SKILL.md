---
name: load-precipitation
description: "Basin-mean precipitation over a frozen polygon from GPM IMERG V07 (a declared run: final, late or early, one for the window or one per month) or from NLDAS-2 forcing (the gauge-based check): daily and monthly totals in mm and km3, the fraction of grid cells inside the polygon, the run named per month, a change of run or of calibration flagged as a dated seam, an undeclared mix refused, and a receipt."
---

# load-precipitation

Turn "precipitation over this basin for this window" into a daily
and monthly series with a receipt: which product, which run for
which month, which cells, how much of the polygon they cover, and
where the series is not one series. Works by slash command or
conversationally ("IMERG Final over the Lees Ferry basin for water
year 2023", "the NLDAS precipitation over the same polygon",
"extend my Final series through this summer").

This skill carries the pointer, not the facts: every collection
name, DOI, calibration statement, seam date, grid convention, hour
convention, access requirement, failure shape and bias statement
lives in a knowledge concept and is read from there per load,
never restated here.

## Behavior, in order

1. **Parse and show back:** the source (`imerg` or `nldas2`), the
   basin polygon (a fixture written by the delineate-basin skill, or
   any GeoJSON whose `provenance` carries an area and its
   projection), the window as dates, and, for IMERG, the run the
   user declared: one run for the whole window or a run per month.
   If the user asked for IMERG and named no run, ask for one and
   explain, from the dataset concept, why the loader will not choose
   it. Say what the user means to do with the series.
2. **Consult the bundle for this load first.** Consult installed
   knowledge concepts first, as the core `consult-knowledge` skill
   sets out (search terms: imerg, gpm, precipitation, run, final,
   late, early, nldas, forcing, gesdisc, opendap, snow, orographic,
   seam). Read the IMERG dataset concept (runs, the variable, the
   calibration per run, the date the Final record ends, the seam
   dates and the stale_after that governs them), the NLDAS-2 forcing
   concept (what the precipitation field is, the hour convention),
   the GES DISC connector concept (the login, the application
   authorization the account holder alone can give, the failure
   shapes, what leaves the machine) and the two gotchas: run mixing
   for any IMERG window, and the cold-season underestimate for any
   IMERG window that touches November through March over snow or
   mountains. Restate what applies and cite each by path. The
   concepts live under this plugin's own root, whatever the
   installer's record lists for the hydrology plugin (a checkout
   loaded from a directory is not in that record, and an older
   installed version may be): read them from there before searching
   anywhere else.
   - `${CLAUDE_PLUGIN_ROOT}/knowledge/datasets/imerg-v07.md`
   - `${CLAUDE_PLUGIN_ROOT}/knowledge/datasets/nldas2-forcing.md`
   - `${CLAUDE_PLUGIN_ROOT}/knowledge/connectors/gesdisc-earthaccess.md`
   - `${CLAUDE_PLUGIN_ROOT}/knowledge/gotchas/imerg-run-mixing.md`
   - `${CLAUDE_PLUGIN_ROOT}/knowledge/gotchas/imerg-cold-season-orographic-underestimation.md`
3. **Load through the script, not by hand.** Run
   `uv run ${CLAUDE_PLUGIN_ROOT}/verification/fixtures/load_precipitation.py`
   (the script ships with this plugin; the variable is this plugin's
   installed root) with `--source`, `--basin PATH`, `--run RUN` or
   `--run YYYY-MM:RUN,...` for IMERG, `--window FILE` for each
   basin-window file already on disk or `--fetch --start --end` to
   pull the window through the fetch script beside it (an Earthdata
   Login with the GES DISC application authorized, as the connector
   concept sets out), and `--out` for the receipt. The script checks
   the run in every file against the declaration and refuses a
   mismatch, a month holding two runs, duplicate days and a mixed
   grid; computes the cosine-latitude weighted mean over the cells
   whose centre is inside the polygon and the fraction of the
   window's cells that are inside; converts to volume with the
   polygon's own area; names the run per month; and lists every
   seam: a change of run between months, a change of granule label
   inside a run, and the dated seams the dataset concept records
   when the window crosses them. Report the table it prints and
   every `SEAM` line with it.
4. **Say what the number is.** A monthly total is stated with its
   run, its completeness (days present over days in the month), the
   fraction of cells inside the polygon and the polygon area the
   volume used. A window that crosses a seam is two series, and the
   answer says so and names the date; it is never smoothed over. A
   Final window that reaches past the date the dataset concept
   records as the end of the Final record is reported as absent
   there, not filled.
5. **The cold-season check.** When the source is IMERG and the
   window touches the months the cold-season gotcha names over
   terrain it names, run the same window through `--source nldas2`
   (or name that check and its concept path if the NLDAS window is
   not on disk and cannot be fetched) and report the two basin means
   side by side with their ratio, before the IMERG number goes into
   any budget. The gotcha concept carries the reason and the size
   observed.
6. **Summary as provenance:** the source and run per month, the
   window files with their sha256 and DOIs, the route per granule
   from the file attributes, the basin fixture and its geometry
   hash, the coverage numbers, the seams, the receipt path, and the
   concepts consulted.

## Must NOT

- Never choose an IMERG run: the run is the user's declaration, and
  a window with none is a question back to the user, not a default.
  (Hard rule: fires on every IMERG load.)
- Never concatenate files of different runs, or a Final segment with
  a near-real-time one, without the run named per month and the
  seam date stated; the script refuses an undeclared mix and the
  answer does not work around it.
- Never hand over an IMERG total over snow-covered or mountainous
  terrain for a window touching the cold season without the
  gauge-based check named beside it, as the gotcha concept sets out.
- Never state a total without the run, the completeness, the
  fraction of cells inside and the polygon area.
- Never present a subset that fell back to the archive route as
  anything other than what the receipt says it is, and never retry
  an authorization failure with a stored password: the connector
  concept names the URL the account holder must open.
- Never carry a collection name, a DOI, a seam date, a grid or hour
  convention, a bias size or a rule in this file; read it from the
  concept that owns it and cite the path, so a corrected concept
  changes this skill's behavior without an edit here.
