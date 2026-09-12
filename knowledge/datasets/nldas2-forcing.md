---
type: dataset
spheres: [hydrosphere, atmosphere]
title: "NLDAS-2 primary forcing precipitation: the gauge-based hourly field over the conterminous United States"
description: "Hourly 0.125 degree precipitation (Rainf, kg m-2 per hour, summed over the hour) from the NLDAS-2 File A forcing at GES DISC, 1979 to the present: a temporal disaggregation of the CPC gauge-only daily analysis with a PRISM orographic adjustment, so its daily total is the gauge analysis. The hourly granule stamped hour H covers H minus one to H, and the day D total is granules D 01:00 through D+1 00:00; there is no daily collection."
tags: [nldas, nldas2, precipitation, forcing, gauge, cpc, prism, gesdisc, conus, hydrology]
generated: { by: claude-code/fable-5, at: 2026-09-06T21:40:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-06T22:57:54Z }
resource: https://disc.gsfc.nasa.gov/datasets/NLDAS_FORA0125_H_2.0/summary
version: "2.0 (netCDF, converted from the GRIB files; release date 2021-04-11 per the collection citation); hourly from 1979-01-01 13:00 UTC, ends at present; monthly NLDAS_FORA0125_M 2.0 beside it"
status: stable
upstream: pending
stale_after: 2027-03-06
citation:
  access_date_required: true
  authority: https://disc.gsfc.nasa.gov/
  data: "NLDAS project (2021), NLDAS Primary Forcing Data L4 Hourly 0.125 x 0.125 degree V2.0, edited by David M. Mocko, NASA/GSFC/HSL, Greenbelt, Maryland, USA, Goddard Earth Sciences Data and Information Services Center (GES DISC), accessed {access_date}, 10.5067/THUF4J1RLSYG"
  doi: "10.5067/THUF4J1RLSYG (hourly), 10.5067/2DPKB5B5N14O (monthly)"
  note: "creator, editor, release date and publisher as the CMR collection citation records them; the generation of the forcing is described in Xia et al. (2012), which the abstract names"
sources:
  - id: cmr
    resource: https://cmr.earthdata.nasa.gov/search/collections.umm_json?concept_id=C2033151148-GES_DISC
    title: "CMR collection record for NLDAS_FORA0125_H 2.0 (concept id C2033151148-GES_DISC; abstract, extent, DOI, citation) and NLDAS_FORA0125_M 2.0 (C1887583680-GES_DISC), read 2026-09-06"
  - id: readme
    resource: https://docserver.gesdisc.eosdis.nasa.gov/public/project/hydrology/NLDAS2_README.pdf
    title: "NLDAS-2 README (GES DISC hydrology documentation), the variable list and the forcing description"
  - id: granule
    resource: https://opendap.earthdata.nasa.gov/collections/C2033151148-GES_DISC/granules/
    title: "File metadata and time bounds of the hourly granules read over Cloud OPeNDAP on 2026-09-06 (Rainf attributes, the time begin and end attributes, the grid)"
  - id: record
    resource: https://github.com/open-science-pillars/marketplace/issues/68
    title: "The precipitation record: the granule inspection, the hour convention, the window pulls and their sizes"
---

# NLDAS-2 primary forcing precipitation

**Identity.** The North American Land Data Assimilation System phase
2 (NLDAS-2) "File A" primary forcing: the hourly meteorological
fields that drive the NLDAS land models, on a 0.125 degree grid over
the conterminous United States and its margins (lon -125 to -67,
lat 25 to 53), hourly from 1979-01-01 13:00 UTC to the present,
netCDF converted from the original GRIB. Collection
`NLDAS_FORA0125_H` version 2.0 at GES DISC (DOI
10.5067/THUF4J1RLSYG); the monthly aggregate `NLDAS_FORA0125_M`
2.0 (DOI 10.5067/2DPKB5B5N14O) sits beside it. There is no daily
collection: a daily total is a sum of 24 hourly fields.[^cmr]

**What the precipitation is.** The abstract is explicit that the
precipitation field is not the NARR reanalysis precipitation the
other forcing fields come from: it is "a temporal disaggregation of
a gauge-only CPC analysis of daily precipitation, performed
directly on the NLDAS grid and including an orographic adjustment
based on the widely-applied PRISM climatology." The hourly weights
come from WSR-88D radar, CMORPH or NARR in that order of
availability, and "do not change the daily total precipitation". A
daily sum of `Rainf` is therefore the gauge analysis at 0.125
degree with the PRISM terrain adjustment, which is what makes it
the check for a satellite estimate over snow-covered high
terrain.[^cmr][^readme]

**Variable (granule-verified 2026-09-06).** `Rainf`, float32, units
`kg m-2` (one kg m-2 is one mm of water), `cell_methods` "time:
sum" (the hour's total, not a rate), fill -9999, dimensions (time,
lat, lon). Cell centres at -124.9375 + 0.125 i and 25.0625 + 0.125 j;
the index of a coordinate is floor((lon + 125) / 0.125),
floor((lat - 25) / 0.125). One hourly granule is about 1.7 MB (all
eleven forcing fields, the whole domain).[^granule]

**The hour convention.** The granule stamped `A<YYYYMMDD>.<HHMM>`
carries the total of the hour ENDING at that stamp: the time
variable's `begin_date` and `end_date` attributes on the granule
stamped 2022-10-01 00:00 read 2022-09-30 23:00:00 to 2022-10-01
00:00:00. The UTC day D is therefore the 24 granules D 01:00
through D+1 00:00, and a sum of the granules stamped D 00:00 through
D 23:00 puts the last hour of the day before into day D. A daily
series built the wrong way is shifted by one hour, which is
invisible in a monthly total and visible in a daily
comparison.[^granule][^record]

## Access

Cloud-hosted at GES DISC behind Earthdata Login with the GES DISC
application authorized (the connector concept). A basin window is
pulled per hourly granule through a Cloud OPeNDAP DAP4 constraint
expression (37 KB per hour for the Lees Ferry window, 0.9 MB per
day; the water-year 2023 pull moved 362 MB in 54 minutes at six
concurrent requests, most of the time spent waiting on subset
requests that timed out or answered 502), with the archive download
and a local cut as the fallback when a subset request does not
answer with netCDF.[^record]

## Uncertainty

The daily total is a gauge analysis, so its error is the gauge
network's: sparse at high elevation, undercatch in snow and wind,
and the PRISM adjustment is a climatological ratio rather than a
measurement of the day. It is the better estimate over the
mountain West in the cold season, not a truth; a comparison against
IMERG states both as estimates and the ratio as the size of the
disagreement.[^readme]

## Known issues

- The precipitation lineage differs from the rest of File A (gauge
  analysis, not NARR); a reader who assumes one source for all
  eleven fields misreads what the precipitation is.
- The hour convention above: a day summed from the stamps D 00:00
  through D 23:00 is shifted by one hour.
- The collection ends at present (the CMR extent has no end date);
  the latency behind real time is not recorded here, and a window
  that reaches the last few days is checked for absent granules
  before a total is stated.

[^cmr]: CMR collection record for NLDAS_FORA0125_H 2.0, read 2026-09-06
[^readme]: NLDAS-2 README, GES DISC hydrology documentation
[^granule]: hourly granule metadata read over Cloud OPeNDAP, 2026-09-06
[^record]: the precipitation record on open-science-pillars/marketplace issue 68
