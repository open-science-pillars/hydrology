# hydrology

Hydrology for Open Science Pillars: SWOT river and lake levels, GRACE-FO
groundwater, USGS NWIS streamflow, and SMAP soil moisture, with an applied
water-resources pack (drought and reservoir analysis).

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
from: `claude plugin update hydrology@open-science-pillars` moves it to
the current one, dependencies included, and `claude plugin list` shows
what you have. Cowork and Claude Science: add the marketplace and install
from it.

## What works today

- **SWOT rivers and lakes** and a loader that keeps reach-level and
  node-level data distinct (they answer different questions).
- **USGS streamflow** (NWIS), with the provisional-vs-approved data trap
  handled and a rule that steers drought analysis to near-natural reference
  gauges rather than dam-regulated ones.
- **GRACE-FO groundwater** and **SMAP soil moisture** skills; the GRACE
  concepts come from the PO.DAAC provider bundle, installed alongside as
  the nasa-daac-knowledge dependency. A pinned copy of them still travels
  under `knowledge/snapshot-podaac/` (declared in `knowledge/snapshot.yaml`,
  byte-checked against the canonical bundle) while the skills' paths move
  to the installed bundle; the copy retires when they have.
- **Applied workflows**: a streamflow drought index and a reservoir
  storage-change analysis, each validated against real gauge records.

New to the project's vocabulary? See the
[glossary](https://github.com/open-science-pillars/marketplace/blob/main/GLOSSARY.md).
USGS water data needs no login. Retrieving NASA data (SWOT, GRACE,
SMAP) needs an Earthdata Login, which earthaccess reads from the
environment (`EARTHDATA_TOKEN`, or username and password variables),
from `~/.netrc`, or from an interactive prompt; searching for data
needs no account at all.

License: Apache-2.0. Cite via CITATION.cff.
