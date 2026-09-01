# Connectors: hydrology

What this plugin talks to over the network, what leaves your machine
when it does, and what happens when it cannot. This file is the
disclosure; `.mcp.json` is the wire.

## NASA Earthdata MCP (`earthdata`)

**What it is.** `.mcp.json` registers NASA's Earthdata MCP server
(github.com/nasa/earthdata-mcp), a streamable-http server in front of
NASA's Common Metadata Repository.

**What leaves your machine.** Search terms only: collection names,
keywords, and the spatial or temporal bounds of a query, sent over
HTTPS to NASA's CMR. No credential is sent, because CMR search is a
public API and this connector needs none. No file, no local path, and
no data you hold ever passes through it.

**What does not go through it.** Downloads. Data retrieval happens
directly between your machine and the archive through earthaccess,
never through this connector, which is why an unreachable connector
cannot block a download.

**When it is unavailable.** Nothing breaks. discover-data falls back to
knowledge-based discovery with archive URLs (SPEC §3.4) and says which
path it used; loading proceeds from local files or direct library
access. USGS/NWIS work is unaffected either way, since it does not use
this connector at all.

**Where the facts about this service are maintained.** Endpoint,
transport, tool surface, auth boundary and deprecation status are
recorded as a dated concept with a staleness date in the PO.DAAC
knowledge bundle (`connectors/earthdata-mcp.md` in
github.com/open-science-pillars/nasa-daac-knowledge), re-verified on a
schedule. This file deliberately does not restate them, so there is
one place to correct when they change.

**Per-surface.** Claude Code and Cowork read `.mcp.json` from the
installed plugin. Claude Science configures connectors per session;
see marketplace/docs/surface-testing-guide.md.

## Credentials

An Earthdata Login is needed only to retrieve data, never to search.
It is read by earthaccess at download time and is never handled by
this plugin, never sent to the connector above, and never stored in
this repository in any form (SPEC §5.8). USGS water data needs no account of any kind.

## Observations MCP (`observations`)

**What it is.** `.mcp.json` runs the observations server (one thin
stdio server over five authoritative observation sources) via uv from
a COMMIT-PINNED URL in the core repository, so what runs is exactly
what was reviewed; the pin moves only by a reviewed edit to this
file. The groups this bundle uses: USGS NWIS stream gauges and
PO.DAAC Hydrocron SWOT river series.

**What leaves your machine.** Query parameters only (site and reach
identifiers, time ranges), over HTTPS to the agency endpoints. Every
source is anonymous; no credential exists in the process. Nothing
you hold is sent.

**When it is unavailable.** Nothing breaks; gates and attesters never
call it.

**Where the facts are maintained.** Dated concepts with staleness
dates in `knowledge/connectors/`: usgs-water.md, hydrocron-swot.md.
This file does not restate them.
