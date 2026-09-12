# hydrology

Hydrology for Open Science Pillars: SWOT river and lake levels, GRACE-FO
groundwater, USGS NWIS streamflow, and SMAP soil moisture, with an applied
water-resources pack (drought and reservoir analysis).

A Hydrosphere capability, discipline Terrestrial Hydrology
(`.osp/repository.yaml`; ADR A in the marketplace repository). Its snow
concepts (SNODAS, the drought anatomy) also tag Cryosphere, so the
repository declares both spheres with Hydrosphere primary. Provider facts
are consulted from the PO.DAAC bundle and, for the producers that have no
bundle yet, held here with `upstream: pending`; the recipes and attested
computations that combine several providers' products are the methods
stewards' (CODEOWNERS). The Claude package files are the runtime
projection of `.osp/package.yaml`.

> **Status: in active development.** This plugin is being built openly and is
> not yet part of the general-availability set. The data-source skills and
> the drought/reservoir workflows work today; more is landing. Watch or star
> this repo to follow along. For a guided first experience with the project,
> start with the [tutorials](https://github.com/open-science-pillars/tutorials).

## Install

```bash
claude plugin marketplace add open-science-pillars/marketplace
claude plugin install hydrology@open-science-pillars
```

The plugin declares core (the foundation plugin) and the PO.DAAC provider
knowledge in nasa-daac-knowledge as dependencies, so the one install
brings both with it. An install stays at the release it was installed
from: `claude plugin update hydrology@open-science-pillars` moves this
plugin to the current one and only this plugin; a dependency moves by
its own update command (`claude plugin update core@open-science-pillars`,
`claude plugin update nasa-daac-knowledge@open-science-pillars`), and a
release that raises a floor says so in its notes. `claude plugin list`
shows what you have. Claude Code is the supported runtime; Claude Cowork installs from the
same marketplace and is tested; OpenAI Codex arrives through the Agent
Plugins projection, not built yet; Claude Science is a future runtime.
What each word asserts is in the marketplace repository's
docs/runtime-distribution.md.

## What works today

- **SWOT rivers and lakes** and a loader that keeps reach-level and
  node-level data distinct (they answer different questions).
- **USGS streamflow** (NWIS), with the provisional-vs-approved data trap
  handled and a rule that steers drought analysis to near-natural reference
  gauges rather than dam-regulated ones.
- **GRACE-FO groundwater** and **SMAP soil moisture** skills; the GRACE
  concepts come from the PO.DAAC provider bundle, installed alongside as
  the nasa-daac-knowledge dependency, and the skills cite them by bundle
  path (`knowledge/podaac/...`), which core's consult-knowledge convention
  resolves through the installer's record of installed plugins; nothing
  is copied into this repository.
- **Basin precipitation** from GPM IMERG V07 (the run declared, never
  chosen: Final, Late and Early share a variable name and differ in
  calibration; a change of run is a dated seam in the receipt, an
  undeclared mix is refused) and from NLDAS-2 forcing, the gauge-based
  series that checks IMERG over snow-covered mountains in the cold
  season; basin means over a frozen polygon with the fraction of cells
  inside, daily and monthly totals in mm and km3.
- **Basin evapotranspiration** from MOD16A2GF (8-day composites
  apportioned to calendar months by their true length, the seven fill
  codes over water, rock, city, ice and wetland excluded and counted
  rather than read as zero, the masked fraction and the open-water
  choice stated in the receipt) with the OpenET ensemble as an
  independent check wherever a polygon is under the service's
  per-request area cap, which no basin is: the cap is a refusal with
  the acreage named, not a smaller answer.
- **The basin water balance, attested**: P + I - ET - Q - X = dS over a
  frozen input tree, with a receipt carrying every term, its product
  and the source of its uncertainty, and an attester that recomputes
  the whole thing and applies two bars. The storage term is refused
  below the GRACE footprint floor (about 111,000 km2, one mascon,
  derived from the product's own geometry), a regulated outlet is
  flagged rather than refused, and an import or export without a
  source is refused outright. Measured for water year 2023 on three
  basins, one of which is the refusal.
- **Annual peaks and the flood frequency hand-off**: the peak record
  loaded whole, including the historic peaks whose month or day is
  unknown, with the parameter required because one response carries
  both the peak discharge and the peak stage in different units. The
  peak file the field's software reads is exported with each qualifier
  mapped to its qualification code, and the mapping was derived by
  aligning the record against the file the agency's own writer
  produces rather than recalled. No frequency estimate is computed
  here: a fit made in the session is labelled screening, refuses a
  regulated, historic or censored record until the analyst says which
  convention they want, and never reports a return period without an
  interval. The published number comes from the program the field
  uses, run by the analyst, and is read back with its own limits.
- **Applied workflows**: a streamflow drought index and a reservoir
  storage-change analysis, each validated against real gauge records.
- **Basin delineation**: the polygon above a gauge or a snapped point
  from the USGS NLDI, or a union of Watershed Boundary Dataset units,
  written with its provenance and measured in an equal-area
  projection beside the gauge's drainage area; a closed basin comes
  back as closed, with no invented outlet.

New to the project's vocabulary? See the
[glossary](https://github.com/open-science-pillars/marketplace/blob/main/GLOSSARY.md).
USGS water data needs no login (an optional key in `API_USGS_PAT`
raises the rate limit). Retrieving NASA data (SWOT, GRACE,
SMAP, IMERG, NLDAS-2) needs an Earthdata Login, which earthaccess reads
from the environment (`EARTHDATA_TOKEN`, or username and password
variables), from `~/.netrc`, or from an interactive prompt; searching
for data needs no account at all. IMERG and NLDAS-2 at GES DISC also
need the GES DISC application authorized on that account, a one-time
step only the account holder can take on the Earthdata Login site
(`knowledge/connectors/gesdisc-earthaccess.md` records the failure
shapes without it and the URL that fixes them).

License: Apache-2.0. Cite via CITATION.cff.
