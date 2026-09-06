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
knowledge-based discovery with archive URLs and says which path it
used; loading proceeds from local files or direct library
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
this repository in any form. USGS water data needs no account; an
optional key (`API_USGS_PAT`, from https://api.waterdata.usgs.gov/signup/)
raises the rate limit and is handled only as described below.

## GES DISC (the load-precipitation skill)

**What it is.** The `load-precipitation` skill's fetch script reaches
NASA's Goddard Earth Sciences Data and Information Services Center,
the archive of GPM IMERG and NLDAS-2, through earthaccess: a CMR
search for the granules of a window, then one request per granule to
NASA Cloud OPeNDAP for the basin window as a DAP4 constraint
expression, with the archive file as the fallback. No MCP server is
involved; the script runs on your machine.

**What leaves your machine.** Your Earthdata Login credential, to
`urs.earthdata.nasa.gov` only, presented by earthaccess (from
`~/.netrc` or the environment). To `opendap.earthdata.nasa.gov` and
`data.gesdisc.earthdata.nasa.gov`: the granule identifier and, for a
subset request, the constraint expression, which names variables and
grid index ranges (the bounding box of the window as cell indices; the
polygon itself never leaves). To `cmr.earthdata.nasa.gov`: the
collection short name and version and the window's dates, with no
credential. No file, no local path and no data you hold goes to any
of them.

**Two credentials.** The account, and the GES DISC application
authorized on it, a one-time acceptance only the account holder can
give on the Earthdata Login site. Without it the login succeeds and
every data request fails; the script reports the resolution URL and
stops, and never uses a stored password to click through it. The
connector concept `knowledge/connectors/gesdisc-earthaccess.md`
records the failure shapes and the pull sizes.

**When it is unavailable.** A subset request that returns anything but
netCDF falls back to the archive file, cut locally; an archive failure
leaves the day absent and the loader reports the month incomplete
rather than filling it. Search through CMR works throughout.

## USGS basin services (the delineate-basin skill)

**What it is.** The `delineate-basin` skill's script calls three
public USGS hosts directly over HTTPS: `api.water.usgs.gov` (the
Network Linked Data Index, for the basin upstream of a gauge or a
snapped point), `api.waterdata.usgs.gov` (the monitoring-locations
collection, for a gauge's published drainage area) and
`hydro.nationalmap.gov` (the Watershed Boundary Dataset map service,
for hydrologic-unit polygons).

**What leaves your machine.** A site number, a coordinate or a list
of hydrologic unit codes, as query parameters. No credential is sent
to any of the three: the script sets no key, reads no environment
variable, and the monitoring-locations lookup goes unkeyed even when
`API_USGS_PAT` is set. The request URLs are written into the
polygon's provenance as sent.

**When it is unavailable.** Nothing breaks; the polygon is simply not
written. A gauge trace or a unit union that fails reports the
service's error and stops. A point delineation whose snapping step
cannot answer stops with nothing traced, because the only fallback
is the unsnapped route the plugin's knowledge names as the wrong
answer; the connector concept records what the outage looks like.

## Observations MCP (`observations`)

**What it is.** `.mcp.json` runs the observations server (one thin
stdio server over five authoritative observation sources) via uv from
a COMMIT-PINNED URL in the core repository, so what runs is exactly
what was reviewed; the pin moves only by a reviewed edit to this
file. The groups this bundle uses: USGS NWIS stream gauges and
PO.DAAC Hydrocron SWOT river series.

**What leaves your machine.** Query parameters only (site and reach
identifiers, time ranges), over HTTPS to the agency endpoints. One
optional credential exists. If `API_USGS_PAT` is set in your
environment, the server sends its value as an `X-Api-Key` header to
api.waterdata.usgs.gov and to no other host; the request URL that
every response, capture manifest and receipt copies never carries
it, and the server's selftests assert a sentinel key appears in none
of them. The two USGS skills, which fetch through dataretrieval's
waterdata module rather than the server, read the same variable and
send it the same way. Unset, USGS requests share the per-address
bucket with everything else on your machine that calls that API, and
a 429 comes back as a structured error; the server never retries
against that host. Hydrocron takes no credential. Nothing else you
hold is sent.

**When it is unavailable.** Nothing breaks; gates and attesters never
call it.

**Where the facts are maintained.** Dated concepts with staleness
dates in `knowledge/connectors/`: usgs-water.md, hydrocron-swot.md.
This file does not restate them.
