---
type: connector
title: "GES DISC through earthaccess: Earthdata Login plus a one-time application authorization, and the window pull over Cloud OPeNDAP"
description: "IMERG and NLDAS-2 at GES DISC need two things: an Earthdata Login and the GES DISC application authorized on that account, which nothing but the account holder can do. Without the authorization every data route fails in its own way (a 403 with an EULA body from the archive, a 403 DAP4 error from Cloud OPeNDAP, an HTML page where netCDF was expected from the on-premises host). What leaves the machine is the credential to urs.earthdata.nasa.gov, and the granule name and a constraint expression naming a window of grid indices to two GES DISC hosts."
tags: [connector, gesdisc, earthaccess, earthdata-login, opendap, dap4, imerg, nldas, hydrology]
generated: { by: claude-code/fable-5, at: 2026-09-06T21:50:00Z }
status: draft
citation:
  access_date_required: true
  authority: https://disc.gsfc.nasa.gov/
  data: "the dataset concept's citation, with the run (IMERG) and the retrieval date; GES DISC's guidance at https://disc.gsfc.nasa.gov/data-guidelines"
  note: "the connector is not the thing cited; the data set is, by its DOI, and the access date is integral because the near-real-time IMERG runs are revised"
stale_after: 2027-03-06
sources:
  - id: earthaccess
    resource: https://github.com/nsidc/earthaccess
    title: "earthaccess 0.14 (login strategies, get_requests_https_session, download), source read 2026-09-06"
  - id: urs-apps
    resource: https://urs.earthdata.nasa.gov/approve_app?client_id=e2WVk8Pw6weeLUKZYOxvTQ
    title: "The Earthdata Login application approval page for the GES DISC archive (client_id e2WVk8Pw6weeLUKZYOxvTQ), the resolution URL the archive's 403 body names"
  - id: opendap
    resource: https://opendap.earthdata.nasa.gov/
    title: "NASA Cloud OPeNDAP (Hyrax), the per-granule DAP4 endpoint CMR lists as the OPENDAP DATA related URL; probed 2026-09-06 before and after authorization"
  - id: cmr
    resource: https://cmr.earthdata.nasa.gov/search/
    title: "CMR search (collections and granules at provider GES_DISC; the RelatedUrls of a granule carry the archive and the OPeNDAP URLs), no credential"
  - id: record
    resource: https://github.com/open-science-pillars/marketplace/issues/68
    title: "The precipitation record: the three failure shapes before authorization, the pulls and their sizes after it, the fallback measurement"
---

# GES DISC through earthaccess

The load-precipitation skill's fetch script reaches GES DISC (the
Goddard Earth Sciences Data and Information Services Center, the
archive of IMERG and NLDAS-2) through earthaccess: `login` with the
`netrc` strategy, a CMR search for the granules of a collection and
window, and one HTTP request per granule to the Cloud OPeNDAP
endpoint CMR lists for it, falling back to the archive file when
the subset request does not answer with netCDF.[^earthaccess][^cmr]

**Two credentials, not one.** An Earthdata Login account is the
first. The second is an authorization, on that account, of the GES
DISC application: a one-time acceptance on the Earthdata Login
site, which only the account holder can give. An account without it
authenticates (earthaccess reports a successful login) and then
fails on every data request, in three shapes observed on 2026-09-06
before the steward authorized the application:[^record]

- the archive host `data.gesdisc.earthdata.nasa.gov` (what
  `earthaccess.download` uses): HTTP 403 with the JSON body
  `{"status_code":403,"error_description":"EULA Acceptance Failure","resolution_url":"https://urs.earthdata.nasa.gov/approve_app?client_id=e2WVk8Pw6weeLUKZYOxvTQ"}`;
  earthaccess raises `EulaNotAccepted`;
- Cloud OPeNDAP `opendap.earthdata.nasa.gov`: 403 as a DAP4 error
  document naming the same source URL;
- the on-premises host `gpm1.gesdisc.eosdis.nasa.gov` serves `.dmr`
  and `.das` metadata without login, and a data request redirects
  through Earthdata Login to an HTML page ("Pre authorization
  required"): a 200 where a client expected netCDF, the shape that
  produces "not a netCDF file" errors far from the cause. The
  sibling `hydro1.gesdisc.eosdis.nasa.gov` (NLDAS) answers 410
  "Service Permanently Retired" and points at Cloud OPeNDAP.

The fix is the resolution URL in the first body, opened by the
account holder. The tooling reports the URL and stops; it does not
open it, and a stored password is never used to click through
it.[^urs-apps][^record]

**What leaves the machine.** The Earthdata Login credential, read
by earthaccess from `~/.netrc` (machine `urs.earthdata.nasa.gov`)
or from the environment, is presented to `urs.earthdata.nasa.gov`
only; the data hosts see the session that login establishes. To
`opendap.earthdata.nasa.gov` and `data.gesdisc.earthdata.nasa.gov`
go the granule identifier and, for a subset request, the DAP4
constraint expression: variable names and index ranges
(`/precipitation[0:0][679:744][1254:1335];...`), which disclose the
bounding box of the window as grid indices and nothing about the
polygon inside it. To `cmr.earthdata.nasa.gov` go the collection
short name and version and the temporal bounds, with no credential.
No file, no local path and no data held locally goes to any of
them.[^earthaccess][^record]

**The window pull.** CMR's granule record carries the OPeNDAP URL
(related URL subtype "OPENDAP DATA"); appending `.dap.nc4?dap4.ce=`
and the constraint returns a netCDF4 file of the window: about 47
KB per IMERG day (66 by 82 cells plus the count variable) and 37 KB
per NLDAS hour (53 by 66 cells), against 31 MB and 1.7 MB for the
global files. Measured 2026-09-06: 31 IMERG days in 44 s, 1.25 MB
transferred; a water year of IMERG 15.5 MB in 67 s; an NLDAS day
0.9 MB in 4.7 s, a water year about 320 MB. A subset request that
returns anything but netCDF (an HTML page, an error document, a
timeout) is not retried as a subset: the script downloads the
archive file through earthaccess and cuts the same window locally
(the same 31-day IMERG window came back identical by that route,
32 MB per day instead of 47 KB), and the receipt names the route
per granule.[^opendap][^record]

**When it is unavailable.** A subset failure falls back to the
archive; an archive failure stops the fetch for that granule and
the loader reports the day absent and the month incomplete rather
than filling it. An authorization failure is reported with the
resolution URL and nothing is retried. Search through CMR needs no
credential and works throughout.[^record]

[^earthaccess]: earthaccess 0.14 source, read 2026-09-06
[^urs-apps]: the Earthdata Login application approval page for GES DISC
[^opendap]: NASA Cloud OPeNDAP, probed 2026-09-06
[^cmr]: CMR search at provider GES_DISC
[^record]: the precipitation record on open-science-pillars/marketplace issue 68
