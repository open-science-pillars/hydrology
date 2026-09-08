---
type: dataset
title: "USGS annual peak streamflow (the peaks collection)"
description: "One row per gauge, parameter and water year: the largest instantaneous discharge and the largest stage, served together in one response, with a qualifier vocabulary that decides which peaks a frequency analysis may use. Partial dates are first class, the record reaches back past the systematic gauge, and the fixed-width file that flood-frequency software reads is served only by the host being decommissioned."
tags: [usgs, peaks, flood-frequency, watstore, peakfq, streamflow, hydrology]
generated: { by: claude-code/opus-5, at: 2026-09-07T23:30:00Z }
verified: { by: human:PaulMRamirez, at: 2026-09-08T04:19:42Z }
resource: https://api.waterdata.usgs.gov/ogcapi/v0/collections/peaks
version: "USGS Water Data API peaks collection, api-version 0.72.0, probed live 2026-09-07 through dataretrieval 1.3.0 (waterdata.get_peaks)"
status: stable
stale_after: 2027-03-07
citation:
  access_date_required: true
  authority: https://waterdata.usgs.gov/
  data: "U.S. Geological Survey, USGS Water Data for the Nation: U.S. Geological Survey National Water Information System database, accessed {access_date}"
  doi: "10.5066/F7P55KJN"
  note: "the access date matters because peaks are revised: a row carrying REVISED has already changed once, and the record's most recent years can still change"
sources:
  - id: api
    resource: https://api.waterdata.usgs.gov/ogcapi/v0/collections/peaks
    title: "The peaks collection and its OpenAPI schema, probed live 2026-09-07: the field list, the collection description, and the qualifier field's declared type"
  - id: manual
    resource: https://pubs.usgs.gov/tm/2006/tm4b4/tm4b4.pdf
    title: "Flynn, K.M., Kirby, W.H., and Hummel, P.R., 2006, User's Manual for Program PeakFQ: USGS Techniques and Methods 4-B4; tables B.2, B.3 and B.4 (the WATSTORE station header, station option and peak-flow record formats and the qualification codes)"
  - id: legacy
    resource: https://nwis.waterdata.usgs.gov/nwis/peak
    title: "USGS Water Services peak output, format hn2: the WATSTORE peak file as the agency's own writer produces it, read 2026-09-07 for 42 gauges; this host is being decommissioned in a window from 2026-11 to 2027-02"
  - id: connector
    resource: ../connectors/usgs-water.md
    title: "This bundle's Water Data API connector concept: paging, the optional key, the rate limits and the decommission window"
  - id: measurement
    resource: https://github.com/open-science-pillars/marketplace/issues/73
    title: "The vocabulary and mapping measurement: 134,722 rows scanned for the qualifier vocabulary and 3,525 rows aligned against the agency's own WATSTORE writer"
---

# USGS annual peak streamflow

**Identity.** The `peaks` collection of the USGS Water Data API serves
annual peak values: for each gauge, parameter and water year, the
largest instantaneous value observed between October 1 and September
30.[^api] It is the standard input to flood frequency analysis, and it
is a different record from the daily and continuous collections, with
its own qualifiers, its own dates and its own revisions. Reached
through `dataretrieval.waterdata.get_peaks` or the collection's items
endpoint; the connector concept holds the paging, the key and the rate
limits.[^connector]

## One response, two series

A query without a parameter returns **both** the peak discharge
(00060, `ft^3/s`) and the peak stage (00065, `ft`), interleaved, with
identical column names. Measured 2026-09-07 at French Broad River at
Asheville (USGS-03451500): 270 rows, of which 130 are discharge for
water years 1896 through 2025 and 140 are stage for 1796 through
2025.[^api] The stage series is the longer one, and it starts a
century earlier.

The two are not the same event, and the collection's own description
says so: the annual peak flow may not occur when the maximum water
level does, because of backwater, tidal effects and rating
changes.[^api] The stage series carries its own qualifiers for exactly
this, including one that says the gage height is not the height that
went with the peak discharge. Ask for a parameter.

## The date can be unknown, and those are the rows that matter

`month` and `day` are nullable, and null means unknown rather than
missing. At Swannanoa River at Biltmore (USGS-03451000) the record
reaches back to water year 1791; 6 of its 110 discharge peaks have no
day and 1 has no month.[^api] At Colorado River at Lees Ferry
(USGS-09380000) the largest peak in the record, 210,000 ft3/s in 1884,
has neither, and carries `[DAYUNKNOWN, ESTIMATED, HISTORIC,
MONTHUNKNOWN, REVISED]`.[^api]

A null month implies a null day, and the qualifiers do not say so
twice: at Swannanoa 7 discharge rows have no day while only 6 carry
DAYUNKNOWN, the seventh being the row whose month is unknown. Read the
null fields, not the qualifier list, to know what is known.

These are historic peaks: floods known from newspapers, high-water
marks and local accounts, from before or between the years the gauge
operated. A frequency analysis carries them as historic information,
which is worth more than a typical year of record. A loader that
filters on a parsable date drops the largest flood in the record and
raises nothing.

**The `time` field is not a date you can trust on those rows.** For
the 1884 Lees Ferry peak the server returns `"time": "1884-01-01"`
with `month` and `day` null and the qualifiers saying both are
unknown.[^api] The field is documented only as the date an observation
represents, with no note that it is filled in when the date is not
known.[^api] Read `year`, `month` and `day`, and treat `time` as
derived.

## The qualifier vocabulary

`qualifier` is declared in the API schema as a string; the server
returns a **JSON array**, and a row carries zero, one or several
codes.[^api] The schema gives no vocabulary. Measured over 134,722
rows in seven regions on 2026-09-07, the collection uses 34 distinct
codes.[^measurement] Fifteen of them correspond to the peak-flow
qualification codes that flood-frequency software reads; the rest come
from the wider observation vocabulary (BACKWATER, DATUMCHANGE,
DIFFDATUM, GHNOTASSCPKQ, NOTMAXGH, BLWMIN, DEBRIS, ICE, DRY, ZEROFLOW,
EQUIP, TEST, UNAVAIL, DISCONTINUED, PARTIAL_RECORD, OPPORTUNISTIC,
FORCEINTERPOLATION, RATINGDEV, FLOOD) and have no peak-file
equivalent.

The correspondence below was **derived, not recalled**: for 42 gauges
the collection's rows were aligned against the WATSTORE file the
agency's own writer produces for the same gauge, and the table is what
rows carrying exactly one code on each side showed, checked against
every row carrying several.[^measurement][^legacy] The code column is
defined in the PeakFQ manual, table B.4, except where noted.[^manual]

| Qualifier | Code | Meaning (manual, table B.4) |
|---|---|---|
| MAXDAILYMEAN | 1 | discharge is a maximum daily average |
| ESTIMATED | 2 | discharge is an estimate |
| DAMFAILURE | 3 | discharge affected by dam failure |
| LESSTHAN | 4 | less than the indicated value, the minimum recordable discharge |
| UNKNOWNREGULATION | 5 | affected to an unknown degree by regulation or diversion |
| REGULATED | 6 | affected by regulation or diversion |
| HISTORIC | 7 | a historic peak, before or between the systematic record |
| GREATERTHAN | 8 | actually greater than the indicated value |
| EVENT | 9 | snowmelt, hurricane, ice jam or debris dam breakup |
| YEARUNKNOWN | A | year of occurrence unknown or not exact |
| DAYUNKNOWN | Bd | the manual defines B for month or day unknown; the agency's writer narrows it |
| MONTHUNKNOWN | Bm | as above |
| URBAN | C | record affected by urbanization, mining, agriculture or channelization |
| OTHERAGENCY | F | not in the manual's table; the agency's writer emits it |
| REVISED | R | not in the manual's table; the agency's writer emits it |

Codes D (base discharge changed) and E (only the annual maximum
available) are in the manual and were not observed in the sample.

## The codes decide which peaks are analysed

This is why the mapping is worth deriving rather than guessing.
PeakFQ applies special handling to codes 3, 4, 6, 7, 8 and C, and
ignores the rest.[^manual] Peaks flagged regulated (6) or urbanized
(C) are **excluded from the analysis** unless the station option
record carries the K option; a historic peak (7) is only used if a
historic period length is supplied, and without one the historic peaks
are ignored and any high outliers are treated as ordinary systematic
peaks.[^manual] A qualifier mapped to the wrong character does not
raise an error. It changes which peaks enter the fit, and the curve
comes back looking reasonable either way.

## The file the software reads is served by the host that is closing

The peaks collection serves JSON, GeoJSON and CSV. It does not serve
the fixed-width WATSTORE peak file that PeakFQ reads. The legacy Water
Services host still writes one, at `nwis/peak?format=hn2`, and that
host is being decommissioned in a window from 2026-11 to
2027-02.[^legacy][^connector] So the writer that a peak file can be
checked against is going away, and after it does, producing that file
from the collection is on whoever needs it.

The record layout is in the manual: for a peak record, column 1 is the
identifier `3`, columns 2 to 16 the station number, 17 to 20 the year,
21 to 22 the month and 23 to 24 the day (blank when unknown), 25 to 31
the discharge right justified, and 32 to 43 the qualification codes.
Columns 44 to 75 hold gage height and its codes and are ignored by
PeakFQ for this record type.[^manual] Measured against the agency's own
output on 2026-09-07: columns 1 through 43 follow the manual exactly;
in the ignored range the writer diverges, placing a five-character
gage-height code string in columns 52 to 56 where the manual gives
four, and the annual peak gage height in columns 69 to 73 where the
manual's field ends at 71.[^measurement]

The station header record drifts the same way and for a plainer
reason. The manual allots eight columns to the hydrologic unit code at
columns 41 to 48; the writer emits the code the site's record carries,
which is twelve digits at some gauges. At Lees Ferry the drainage
area, the contributing area and the datum therefore sit four columns
to the right of where the table says.[^measurement] The consequence
for anyone reading these files: the peak records can be parsed by
fixed columns and the header record cannot. PeakFQ reads the station
number and the latitude and longitude from that record, all of which
sit before the drift.

## Agreement between the two services

For 42 gauges, 3,525 peak discharge rows matched a record in the
agency's WATSTORE file by year, month and day. **No value disagreed**
by more than 0.5 ft3/s. The qualifiers disagreed on 7 rows at one
gauge, where the legacy file carries code 5 (regulation to an unknown
degree) and the collection carries no qualifier at all.[^measurement]
That is a small number and a real one: the information is in the file
that is being retired and not in the service that replaces it.

## Uncertainty

A peak is a single instantaneous value read from a rating curve at the
top of its range, which is where a rating is least constrained. The
record carries the qualifiers that matter rather than an error bar:
ESTIMATED says the value was not measured directly, MAXDAILYMEAN says
it is a daily average standing in for an instantaneous peak, LESSTHAN
and GREATERTHAN say the true value is outside a bound, and REVISED
says the number already changed once. There is no uncertainty field
and no published per-value uncertainty. Any statement of flood
magnitude carries the qualifiers of the peaks it rests on, and any
frequency estimate carries a confidence interval, because the sampling
uncertainty of a 100-year quantile from a century of record is the
dominant term and is far larger than the measurement error of any
single peak.

## Known issues

- The response holds two parameters unless one is asked for, and their
  units differ. See the two-series gotcha.
- `time` carries a fabricated date on rows whose month or day is
  unknown.
- The qualifier field is declared a string and served as an array.
- `peak_since` is null on most rows and populated on a few; where it
  is present it names the year since which the peak has stood as the
  record, which is historic information and not a measurement.
- The keyless rate-limit bucket is real: a session of a few hundred
  requests without a key returned HTTP 429 on 2026-09-07, and
  dataretrieval raises `QuotaExhausted` with a resumable partial
  frame rather than retrying. The connector concept describes the two
  buckets.[^connector]

[^api]: the peaks collection and its OpenAPI schema, probed live
[^manual]: the PeakFQ user's manual, tables B.2, B.3 and B.4
[^legacy]: the legacy Water Services peak output in WATSTORE format
[^connector]: this bundle's Water Data API connector concept
[^measurement]: the vocabulary and mapping measurement record
