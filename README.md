# hydrology

Terrestrial hydrology for Open Science Pillars: load USGS streamflow and
annual peaks, SWOT river and lake levels, GRACE-FO water storage, SMAP
soil moisture, IMERG and NLDAS-2 basin precipitation and MOD16 and
OpenET evapotranspiration through a size gate; delineate a basin;
close its water balance with an attested receipt; and run drought,
reservoir and event workflows, with an uncertainty on every headline
number and the knowledge concept behind every choice cited. It is a
Hydrosphere capability, discipline Terrestrial Hydrology, with
Cryosphere as a second sphere for its snow concepts (`kind: capability`,
`status: developing` in `.osp/repository.yaml`): it is built openly, the
workflows below work today, and more is landing. The words used on this
page (capability, plugin, sphere, knowledge bundle, runtime) are defined
in the
[glossary](https://github.com/open-science-pillars/marketplace/blob/main/GLOSSARY.md).

## Install

On Claude Code:

```bash
claude plugin marketplace add open-science-pillars/marketplace
claude plugin install hydrology@open-science-pillars
```

What comes with it: `core` (the foundation skills and the start,
discover-data and report workflows) and `nasa-daac-knowledge` (the
PO.DAAC provider bundle, where the GRACE concepts live), both declared as
dependencies, so the one install brings them with it. An install stays at
the release it was installed from:
`claude plugin update hydrology@open-science-pillars` moves this plugin
and only this plugin; a dependency moves by its own update command
(`claude plugin update core@open-science-pillars`,
`claude plugin update nasa-daac-knowledge@open-science-pillars`), and a
release that raises a floor says so in its notes. `claude plugin list`
shows what you have.

On Claude Cowork: add the marketplace by repository
(`open-science-pillars/marketplace`) under Customize > Plugins > Add
marketplace, then install the same capability from it; the shell commands
on this page are for Claude Code.

Local requirements: [uv](https://docs.astral.sh/uv/getting-started/installation/).
The observations connector and every script here (the verification
notebooks, the sanctioned computations and their attesters) declare
their dependencies in a PEP 723 header and run as `uv run <script>`; uv
builds the environment on first run, so nothing is installed by hand.
Never `python script.py`: it skips the header and fails at the first
import.

Credentials: USGS water data needs no login (an optional key in
`API_USGS_PAT` raises the rate limit). Retrieving NASA data (SWOT, GRACE,
SMAP, IMERG, NLDAS-2, MOD16) needs an Earthdata Login, which earthaccess
reads from the environment (`EARTHDATA_TOKEN`, or username and password
variables), from `~/.netrc`, or from an interactive prompt; searching for
data needs no account at all. IMERG and NLDAS-2 at GES DISC, and MOD16
at LP DAAC, also need that archive's application authorized on the
account, a one-time step only the account holder can take on the
Earthdata Login site (`knowledge/connectors/gesdisc-earthaccess.md`
records the failure shapes without it and the URL that fixes them).
OpenET is a separate service with its own key, read from
`OPENET_API_KEY` (`knowledge/connectors/openet-api.md`).

## Runtimes

Which runtimes this release is qualified on is the table below, rendered
from the qualification records; what each word asserts is in the
marketplace repository's
[docs/runtime-distribution.md](https://github.com/open-science-pillars/marketplace/blob/main/docs/runtime-distribution.md).

<!-- osp-runtimes:start -->
Runtime support for hydrology 0.8.0 (release lock `sha256:c22d480aa012`), rendered by build-kit's `osp.py advertise` from `.osp/surfaces.yaml` and the qualification records; edit those, not this block.

| Runtime | Role | Declared status | Qualification |
|---|---|---|---|
| Claude Code | development and runtime, required | planned | Not qualified, waived for this release (Claude Code is not qualified for this release, and the reason is structural rather than circumstantial. This package declares no attester in .osp/surfaces.yaml probes.prove, so the prove and receipt tests are blocked rather than failed: there is no command to run and no receipt to attest, and no re-run clears that. The shared attester is the open r4-shared-prove deliverable, and until it lands no release of this package can carry a Claude Code record. An honest run made for 0.8.0 confirmed it: install, dependency resolution, skill discovery, knowledge resolution, the connectors, the goldens on the installed tree and the release lock all pass; prove and receipt are blocked; and skill-invocation fails because the skill's output never names the capability, which is what the probe checks for. No record has ever existed for this surface at any version, so this waiver records a debt that predates this release rather than creating one. The surface is not advertised until the attester exists and a run passes.; human:PaulMRamirez, 2026-09-20) |
| Claude Cowork | runtime, required | tested | Not qualified, waived for this release (Claude Cowork is not qualified for this release. A Cowork record is a run by a person with Cowork in front of them, installing from the catalog, and no such run has been made for 0.8.0; the runtime cannot be driven headlessly, so the coordinator carrying this release on the maintainer's behalf cannot make one either. This repeats the decision recorded for land-ice 0.1.0 on 2026-09-19 for the same reason. Nothing about the capability is known to fail there: its projection renders and validates in the gate. The surface is not advertised until a run exists.; human:PaulMRamirez, 2026-09-20) |
| OpenAI Codex | runtime, required | planned | Not qualified, waived for this release (OpenAI Codex is not qualified for this release. No release in this organization has been qualified on Codex: the Agent Plugins projection renders and passes plugin-check in the gate, but the Codex leg has never been exercised, so there is no procedure to run and nothing to record. This repeats the decision recorded for land-ice 0.1.0 on 2026-09-19 for the same reason. The surface is not advertised, and the projection is published as conformant rather than as tested.; human:PaulMRamirez, 2026-09-20) |
| Claude Science | future runtime | limited-release | Outside the required matrix |

A runtime is advertised as supported only on a qualified record for this exact release; a release stays valid when a runtime is not qualified, and that runtime is simply not advertised.
<!-- osp-runtimes:end -->

## First result

[tutorials/quickstart.md](tutorials/quickstart.md) in this repository:
configure the project, plan the data, load a reference gauge through
the gate, compute a drought index against the recipe, then close the
water balance of the Colorado above Lees Ferry for water year 2023 from
the frozen inputs this plugin ships and attest the receipt, in one page.
It assumes core and hydrology are installed and, for the water balance
step, a terminal with `uv`; the gauge steps need no credentials. The
tutorials repository has no hydrology walkthrough yet:
[Tutorial 1, Getting Started](https://github.com/open-science-pillars/tutorials/blob/main/tutorial-1-getting-started.qmd)
(measured at 4.6 minutes on a fresh install) is the orientation, and the
quickstart here is the hydrology first result.

## What's inside

- **Skills** (`skills/`, one `SKILL.md` each): background on `nwis`,
  `swot-hydro` and `smap`; the gated loaders `load-nwis`, `load-peaks`,
  `load-swot-hydro`, `load-grace-tws`, `load-smap`, `load-precipitation`
  and `load-et`; `delineate-basin`; and the workflows
  `basin-water-balance`, `drought-analysis`, `drought-anatomy`,
  `reservoir-analysis`, `reservoir-ledger`, `grace-groundwater` and
  `reconstruct-event`. What each one refuses (a regulated gauge for
  drought work, an undeclared IMERG run, a basin below the GRACE
  footprint floor, a flood frequency estimate from a screening fit) is
  in its SKILL.md and the gotcha it cites. A script a skill runs at
  runtime (the basin delineation, the precipitation, evapotranspiration
  and peaks loaders, the drought panels, the reservoir ledger and the
  SWOT gauge confrontation) lives in that skill's `scripts/` directory,
  per the placement rule.
- **Agents** (`agents/`): `hydro-scout` returns a cited data plan,
  starting with which gauges measure hydrology and which measure dam
  operations; it never downloads on its own.
- **Knowledge** (`knowledge/`): datasets, gotchas, recipes, one attested
  computation (the basin water balance) and the connector concepts for
  USGS, Hydrocron, NLDI, GES DISC, OpenET and SNODAS. The GRACE concepts
  live at `knowledge/podaac/` in
  [nasa-daac-knowledge](https://github.com/open-science-pillars/nasa-daac-knowledge)
  and are installed as the dependency; skills cite them by bundle path
  and nothing is copied here. Producers with no provider bundle yet are
  held here with `upstream: pending`.
- **Verification** (`verification/`): one golden notebook per workflow
  (`load_nwis.py`, `load_swot_hydro.py`, `load_precipitation.py`,
  `load_et.py`, `delineate_basin.py`, `basin_water_balance.py`,
  `drought_analysis.py`, `drought_anatomy.py`, `reservoir_storage.py`,
  `reservoir_ledger.py`, `event_reconstruction.py`, `peaks_export.py`,
  `swot_gauge_confrontation.py`) on frozen fixtures, with the fixture
  builders and every frozen input under `verification/fixtures/`. The
  sanctioned computation and its attester sit in the scripts directory
  of the skill that runs them, `skills/basin-water-balance/scripts/`.
- **Evals** (`evals/`): one judgment case per high-severity gotcha and
  per refusal (the regulated flag, the declared run, the sub-floor
  refusal, the volume gate), with the seed and automated results.

## Configuration

Copy [`hydrology.local.md.template`](hydrology.local.md.template) into
your project as `hydrology.local.md`. Basins and their polygons,
reference and operational gauges (with regulation status), the cache
directory, the download gate (2 GB unless you change it) and the
climatology window live there, and the loaders and workflows read them.

## Connectors and credentials

The observations connector fetches USGS gauge and Hydrocron SWOT river
records from public agency endpoints; the NASA Earthdata connector
serves discovery when it is reachable, with knowledge-based discovery as
the fallback. What leaves your machine, which credential is read where
(the USGS key, the Earthdata Login, the OpenET key), and what happens
when a connector is unavailable is in [CONNECTORS.md](CONNECTORS.md).

## Contributing

Start with the marketplace repository's
[CONTRIBUTING.md](https://github.com/open-science-pillars/marketplace/blob/main/CONTRIBUTING.md)
and the guides under its `docs/` (contributing a skill, contributing
knowledge, testing, the package authoring guide).

## License and citation

Apache-2.0. Cite via [CITATION.cff](CITATION.cff).
