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
claude plugin install core@open-science-pillars
claude plugin install hydrology@open-science-pillars
```

**Install core first** (the foundation plugin), the same way ocean-science
builds on core. Cowork and Claude Science: add the marketplace and install
from it.

## What works today

- **SWOT rivers and lakes** and a loader that keeps reach-level and
  node-level data distinct (they answer different questions).
- **USGS streamflow** (NWIS), with the provisional-vs-approved data trap
  handled and a rule that steers drought analysis to near-natural reference
  gauges rather than dam-regulated ones.
- **GRACE-FO groundwater** and **SMAP soil moisture** skills, reusing the
  GRACE knowledge from the ocean side.
- **Applied workflows**: a streamflow drought index and a reservoir
  storage-change analysis, each validated against real gauge records.

New to the project's vocabulary? See the
[glossary](https://github.com/open-science-pillars/marketplace/blob/main/GLOSSARY.md).
USGS water data needs no login; NASA data (SWOT, GRACE, SMAP) needs an
Earthdata Login in `~/.netrc`.

License: Apache-2.0. Cite via CITATION.cff.
