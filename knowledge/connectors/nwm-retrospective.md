---
type: connector
title: "The NOAA National Water Model retrospective, version 3.0, on AWS (observations server)"
description: "Daily mean streamflow at one reach through nwm_retrospective_streamflow, read anonymously from the public bucket noaa-nwm-retrospective-3-0-pds: a zarr store of hourly channel output for 2,776,734 reaches over 385,704 hours from 1979-02-01, chunked 672 hours by 30,000 reaches, integers scaled by 0.01 to cubic metres per second with the fill -999900, keyed by NHDPlus v2 ComID and carrying a gage_id axis that names the USGS gauge on a reach. It is model output, not an observation."
tags: [connector, nwm, national-water-model, retrospective, streamflow, noaa, aws, zarr, mcp, observations]
generated: { by: process:claude-code, at: 2026-09-15T14:00:00Z }
status: draft
citation:
  access_date_required: true
  authority: https://noaa-nwm-retrospective-3-0-pds.s3.amazonaws.com/
  data: "NOAA National Water Model Retrospective, version 3.0 (WRF-Hydro v5.3.0-alpha1 output), NOAA Open Data Dissemination program on Amazon Web Services, bucket noaa-nwm-retrospective-3-0-pds, CHRTOUT zarr store, accessed {access_date}"
  note: "no dataset DOI was found on the bucket; the retrospective version and the store's TITLE attribute are the identity the tool returns, and the registry page for the bucket was outside the drafting session's reach"
stale_after: 2027-03-15
sources:
  - id: bucket-layout
    resource: "https://noaa-nwm-retrospective-3-0-pds.s3.amazonaws.com/?list-type=2&delimiter=/"
    title: "The bucket listing read 2026-09-15: domains Alaska, CONUS, Hawaii and PR; under CONUS a netcdf tree (CHANOBS, CHRTOUT, FORCING, GWOUT, LAKEOUT, LDASOUT, RTOUT, hourly files of about 47 MB each under CHRTOUT/<year>/) and a zarr tree (chrtout, forcing, gwout, lakeout, ldasout, rtout); Alaska carries the same zarr stores"
  - id: zmetadata
    resource: https://noaa-nwm-retrospective-3-0-pds.s3.amazonaws.com/CONUS/zarr/chrtout.zarr/.zmetadata
    title: "The consolidated metadata of the CONUS chrtout store read 2026-09-15: TITLE 'OUTPUT FROM WRF-Hydro v5.3.0-alpha1', code_version v5.3.0-alpha1; streamflow int32 of shape [385704, 2776734] chunked [672, 30000], zstd level 9, C order, scale_factor 0.01, add_offset 0, fill and missing value -999900, units m3 s-1, valid range 0 to 5000000; time int64 in hours since 1979-02-01T01:00:00 on the proleptic Gregorian calendar, chunked 672; feature_id int64 in one chunk, NHDPlus v2 ComIDs within CONUS and arbitrary reach ids outside it; gage_id fixed 15-byte strings in one chunk (67 KB compressed); latitude and longitude float32 in one chunk each (8.8 MB compressed)"
  - id: chunk-sizes
    resource: "https://noaa-nwm-retrospective-3-0-pds.s3.amazonaws.com/?list-type=2&prefix=CONUS/zarr/chrtout.zarr/streamflow/&max-keys=6"
    title: "Object sizes read 2026-09-15: streamflow chunks 0.0, 0.1 and 0.10 of 3.9, 9.2 and 6.1 MB; feature_id/0 of 2.9 MB; time chunks of about 720 bytes"
  - id: lees-ferry-probe
    resource: https://noaa-nwm-retrospective-3-0-pds.s3.amazonaws.com/CONUS/zarr/chrtout.zarr/streamflow/0.72
    title: "Live decode 2026-09-15 of the first time chunk for the reach carrying gage_id 09380000 (Colorado River at Lees Ferry): feature index 2164136, feature_id 20733845, chunk column 72 offset 4136; 8,660 reaches carry a gauge id; the daily means for February 1979 sit near 507 m3/s on every day while the USGS daily record for 09380000 over the same days runs from 282 to 606 m3/s (9,980 to 21,400 ft3/s), the model holding a near-constant release below Glen Canyon Dam where the gauge records the operations"
  - id: usgs-lees-ferry
    resource: "https://api.waterdata.usgs.gov/ogcapi/v0/collections/daily/items?monitoring_location_id=USGS-09380000&parameter_code=00060&datetime=1979-02-01/1979-03-01&f=json"
    title: "The USGS daily discharge at 09380000 for February 1979, read 2026-09-15 for the comparison above"
  - id: streamflow-connector
    resource: usgs-water.md
    title: "This bundle's Water Data API streamflow connector: the gauge of record the retrospective is confronted with, and its units"
  - id: regulated-gauge
    resource: ../gotchas/nwis-regulated-gauge.md
    title: "This bundle's gotcha on regulated gauges: flow statistics below a dam measure operations, which is what the Lees Ferry comparison shows"
  - id: server
    resource: https://github.com/open-science-pillars/core/blob/9fad9ab515e05aef5be73076ef24ca4a9ad83f5f/connectors/observations_mcp.py
    title: "The observations server carrying nwm_retrospective_streamflow (contract 0.5.0): the chunk plan, the zarr decode, the daily aggregation, the chunk budget of fourteen, and the recorded fixture (the store metadata, the first time chunk, the gage_id axis and the Lees Ferry column of chunk 0.72)"
---

# The National Water Model retrospective on AWS

`nwm_retrospective_streamflow` reads daily mean streamflow for one
reach from the NOAA National Water Model retrospective, version 3.0,
on the public bucket `noaa-nwm-retrospective-3-0-pds`, anonymously
over HTTPS.[^bucket-layout] There is no API: the retrospective is a
zarr store (and, beside it, the hourly netCDF files it was built
from), so the tool reads objects, and what it reads is bounded and
named in every response.[^zmetadata][^server] Verified live
2026-09-15 at the reach that carries the Lees Ferry gauge.[^lees-ferry-probe]

**This is model output.** The store's title is "OUTPUT FROM WRF-Hydro
v5.3.0-alpha1"; the values are one simulation's channel routing under
one forcing.[^zmetadata] At Lees Ferry in February 1979 the model
holds a near-constant 507 m3/s on every day while the gauge of record
runs between 282 and 606 m3/s, because the reach sits below Glen
Canyon Dam and the retrospective carries the model's reservoir
treatment where the gauge records the
operations.[^lees-ferry-probe][^usgs-lees-ferry][^regulated-gauge] A
retrospective series is a term to confront the gauge with, never a
substitute for it.

**Layout (read 2026-09-15).** Four domains: CONUS, Alaska, Hawaii and
PR, each with netcdf and zarr trees.[^bucket-layout] The CONUS channel
store `CONUS/zarr/chrtout.zarr` holds `streamflow` as 32-bit integers
of shape 385,704 hours by 2,776,734 reaches, chunked 672 hours (28
days) by 30,000 reaches, zstd-compressed, with `scale_factor` 0.01
and `add_offset` 0 to cubic metres per second and the fill
-999900.[^zmetadata] The time axis is hours since
1979-02-01T01:00:00 on the proleptic Gregorian calendar, so the
record runs to 2023-02-01T00:00 and the first calendar day has 23
hours.[^zmetadata] `feature_id` is the NHDPlus v2 ComID within CONUS
and an arbitrary reach id outside it; `gage_id` is a 15-byte string
per reach, blank on all but 8,660 of them, naming the USGS gauge the
model assigns to the reach.[^zmetadata][^lees-ferry-probe] A
streamflow chunk is 4 to 9 MB compressed; the feature index is 2.9
MB; a time chunk is 720 bytes.[^chunk-sizes]

**What one call costs.** The store metadata and the reach index
arrays once per process, then for each 28-day chunk in the window one
streamflow object and its time object, under a budget of fourteen
chunks (about 392 days); a wider window, or one outside the axis, is
refused before any chunk is read, with the budget or the axis
named.[^server] The reach is found by `feature_id` on the feature
axis or by a USGS gauge number on the `gage_id` axis; the response
carries both, the index, the chunk keys read, the retrospective
version and the store's title.[^server] Rows are the mean of the
hourly values within each UTC calendar day with the fill excluded and
the hours counted, so a partial day is visible.[^server]

**The hourly files.** Under `CONUS/netcdf/CHRTOUT/<year>/` the same
output is one file per hour of about 47 MB each, every reach in every
file; a point series is far cheaper from the zarr store, and the tool
does not read the files.[^bucket-layout]

**Composition.** The model's daily flow beside the gauge of record
and the SWOT reach series: three answers to one question about a
river, each with its provenance, and the regulated-gauge gotcha
saying which one measures operations.[^streamflow-connector][^regulated-gauge]

[^bucket-layout]: the bucket listing, read 2026-09-15
[^zmetadata]: the CONUS chrtout store's consolidated metadata, read 2026-09-15
[^chunk-sizes]: object sizes listed 2026-09-15
[^lees-ferry-probe]: live decode of chunk 0.72 at the Lees Ferry reach, 2026-09-15
[^usgs-lees-ferry]: USGS daily discharge at 09380000, February 1979, read 2026-09-15
[^streamflow-connector]: this bundle's Water Data API streamflow connector
[^regulated-gauge]: this bundle's regulated gauge gotcha
[^server]: the observations server source
