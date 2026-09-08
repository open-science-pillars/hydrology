# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
# ]
# ///
# Golden notebook for the load-peaks workflow (the golden-notebook
# requirement: one fixture-backed asserting script per workflow skill).
# Three frozen peak records under fixtures/peaks, each with the WATSTORE
# file the agency's own writer produced for the same gauge beside it, and
# the export checked against that file over the columns the flood
# frequency program reads. The refusals are asserted as behaviour, not
# described. Headless green via `uv run verification/peaks_export.py`;
# no network, no credential.

import marimo

__generated_with = "0.23.13"
app = marimo.App()


@app.cell
def _():
    import hashlib
    import json
    import subprocess
    import tempfile
    from pathlib import Path

    root = Path(__file__).parent / "fixtures"
    loader = root / "load_peaks.py"
    peaks = root / "peaks"
    tmp = Path(tempfile.mkdtemp(prefix="peaks_export_"))

    def load(site):
        return json.loads((peaks / f"peaks_{site}.json").read_text())

    def run(site, parameter="00060", extra=(), name="r"):
        # The loader as the skill runs it: refusals are exit 2 with a
        # REFUSED line on stderr.
        cmd = ["uv", "run", str(loader), "--peaks", str(peaks / f"peaks_{site}.json"),
               "--parameter", parameter, "--out", str(tmp / f"{name}.json"),
               "--watstore", str(tmp / f"{name}.pkf")]
        cmd += list(extra)
        p = subprocess.run(cmd, capture_output=True, text=True)
        receipt = json.loads((tmp / f"{name}.json").read_text()) if p.returncode == 0 else None
        written = (tmp / f"{name}.pkf").read_text() if p.returncode == 0 else ""
        return p.returncode, p.stderr, receipt, written

    def reference(site):
        return (peaks / f"watstore_{site}_reference.txt").read_text()

    def sha(p):
        return hashlib.sha256(p.read_bytes()).hexdigest()

    WORKED, HISTORIC, REGULATED = "03451500", "03451000", "09380000"
    return (HISTORIC, REGULATED, WORKED, load, peaks, reference, run, sha)


@app.cell
def _(HISTORIC, REGULATED, WORKED, load, peaks, sha):
    # 1. Each fixture names the agency file frozen beside it and the file
    #    is the bytes it recorded. The reference is frozen because the
    #    host that writes it is being decommissioned; a diff against a
    #    file that moved is not a diff.
    for _site in (WORKED, HISTORIC, REGULATED):
        _doc = load(_site)
        _ref = _doc["reference_file"]
        _p = peaks / _ref["name"]
        assert _p.is_file(), _ref["name"]
        assert sha(_p) == _ref["sha256"], _ref["name"]
        assert _ref["type_3_records"] > 100, (_site, _ref["type_3_records"])
        assert "decommission" in _ref["what"]
    return


@app.cell
def _(REGULATED, WORKED, load, reference):
    # 1b. Why the peak records can be parsed by fixed columns and the
    #     header record cannot. The manual gives the hydrologic unit code
    #     eight columns; the writer emits the code the site carries, and
    #     at Lees Ferry that is twelve digits, so the drainage area, the
    #     contributing area and the datum all sit four columns right of
    #     the table. The station number and the coordinates, which the
    #     frequency program reads, sit before the drift.
    _h = {}
    for _site in (WORKED, REGULATED):
        _h[_site] = [l for l in reference(_site).splitlines() if l.startswith("H")][0]
        assert _h[_site][1:16].strip() == _site
    assert len(load(WORKED)["monitoring_location"]["hydrologic_unit_code"]) == 8
    assert len(load(REGULATED)["monitoring_location"]["hydrologic_unit_code"]) == 12
    # Eight digits: the drainage area lands where the manual says.
    assert _h[WORKED][40:48] == "06010105" and _h[WORKED][48:55].strip() == "945"
    # Twelve: it does not.
    assert _h[REGULATED][40:52] == "140700061105"
    assert _h[REGULATED][48:55].strip() != "111800"
    assert _h[REGULATED][52:60].strip() == "111800.0"
    return


@app.cell
def _(WORKED, load):
    # 2. One response, two series. The stage series is the longer one and
    #    starts a century earlier, so a record length read off the
    #    unfiltered response is nearly twice the truth.
    _doc = load(WORKED)
    _by = {}
    for _r in _doc["rows"]:
        _by.setdefault(_r["parameter_code"], []).append(_r)
    assert set(_by) == {"00060", "00065"}
    _q, _h = _by["00060"], _by["00065"]
    assert len(_q) == 130 and len(_h) == 140, (len(_q), len(_h))
    assert len(_doc["rows"]) == 270
    assert {r["unit_of_measure"] for r in _q} == {"ft^3/s"}
    assert {r["unit_of_measure"] for r in _h} == {"ft"}
    assert min(r["water_year"] for r in _q) == 1896
    assert min(r["water_year"] for r in _h) == 1796, "the stage record starts a century earlier"
    assert max(r["water_year"] for r in _q) == max(r["water_year"] for r in _h) == 2025
    # The largest peak of the whole record is in its most recent years.
    _peak = max(_q, key=lambda r: r["value"])
    assert _peak["water_year"] == 2024 and abs(_peak["value"] - 113000) < 1
    assert (_peak["month"], _peak["day"]) == (9, 27)
    return


@app.cell
def _(REGULATED, load):
    # 3. A date can be unknown, and those rows are the largest floods in
    #    the record. The server still returns a `time` for them, which is
    #    why the loader reads year, month and day instead.
    _doc = load(REGULATED)
    _q = [r for r in _doc["rows"] if r["parameter_code"] == "00060"]
    _partial = [r for r in _q if r["month"] is None or r["day"] is None]
    assert len(_partial) == 1
    _p = _partial[0]
    assert _p["water_year"] == 1884 and abs(_p["value"] - 210000) < 1
    assert set(_p["qualifier"]) == {"DAYUNKNOWN", "ESTIMATED", "HISTORIC",
                                    "MONTHUNKNOWN", "REVISED"}
    assert _p["time"].startswith("1884-01-01"), "the server fills in a date it says is unknown"
    assert _p["value"] == max(r["value"] for r in _q), "and it is the largest peak in the record"
    return


@app.cell
def _(HISTORIC, load):
    # 4. The historic-information gauge: a systematic record with a
    #    century of floods in front of it, carried as historic peaks
    #    rather than dropped.
    _doc = load(HISTORIC)
    _q = [r for r in _doc["rows"] if r["parameter_code"] == "00060"]
    _hist = [r for r in _q if r["qualifier"] and "HISTORIC" in r["qualifier"]]
    _noday = [r for r in _q if r["day"] is None]
    _nomonth = [r for r in _q if r["month"] is None]
    _flagged_day = [r for r in _q if r["qualifier"] and "DAYUNKNOWN" in r["qualifier"]]
    assert min(r["water_year"] for r in _q) == 1791
    assert len(_hist) == 13, len(_hist)
    assert len(_nomonth) == 1, len(_nomonth)
    # Seven rows have no day and only six say DAYUNKNOWN: the row whose
    # month is unknown has no day either and does not say so twice. Read
    # the null, not the qualifier.
    assert len(_noday) == 7 and len(_flagged_day) == 6, (len(_noday), len(_flagged_day))
    assert _nomonth[0] in _noday and _nomonth[0] not in _flagged_day
    # Most historic peaks are estimates and one is not, so the two
    # qualifiers are independent and neither implies the other.
    assert sum(1 for r in _hist if "ESTIMATED" in r["qualifier"]) == 12

    # The code means what the manual says: before or after the
    # systematic record, or inside a break in it. Here the systematic
    # years run 1921 to 2025 with a break from 1927 to 1934, and the one
    # historic peak inside that span sits in the break.
    _sys = sorted(r["water_year"] for r in _q
                  if not (r["qualifier"] and "HISTORIC" in r["qualifier"]))
    _break = sorted(set(range(min(_sys), max(_sys) + 1)) - set(_sys))
    assert (min(_sys), max(_sys), len(_sys)) == (1921, 2025, 97)
    assert _break == list(range(1927, 1935)), _break
    for _r in _hist:
        assert _r["water_year"] < min(_sys) or _r["water_year"] in _break, _r["water_year"]

    # And the historic information does not extend the upper tail at this
    # gauge: the largest peak of the whole record, 1791 onward, is the
    # most recent one.
    assert max(r["value"] for r in _hist) == 40000
    assert max(r["value"] for r in _q) == 60800
    assert max(_q, key=lambda r: r["value"])["water_year"] == 2024
    return


@app.cell
def _(HISTORIC, REGULATED, WORKED, reference, run):
    # 5. The export against the agency's own writer, over columns 1 to 43:
    #    the station number, the date, the discharge and the qualification
    #    codes, which is everything the frequency program reads from a
    #    peak record. Anything past column 43 it ignores for this record
    #    type, and there the agency's writer diverges from the manual.
    def _cols(text):
        return {l[16:20] + l[20:22] + l[22:24]: l[:43].rstrip()
                for l in text.splitlines() if l.startswith("3")}

    _report = {}
    for _site in (WORKED, HISTORIC, REGULATED):
        _code, _err, _receipt, _written = run(_site, name=f"x{_site}")
        assert _code == 0, _err
        _mine, _theirs = _cols(_written), _cols(reference(_site))
        _common = set(_mine) & set(_theirs)
        _same = [k for k in _common if _mine[k] == _theirs[k]]
        _report[_site] = {"mine": len(_mine), "theirs": len(_theirs),
                          "common": len(_common), "identical": len(_same),
                          "only_mine": sorted(set(_mine) - set(_theirs)),
                          "only_theirs": sorted(set(_theirs) - set(_mine)),
                          "differing": sorted(k for k in _common if _mine[k] != _theirs[k]),
                          "theirs_q": {k: v[24:31].strip() for k, v in _theirs.items()}}
        print(f"{_site}: {len(_same)} of {len(_common)} shared records identical over columns 1 to 43; "
              f"{len(set(_mine) - set(_theirs))} dated only by the collection, "
              f"{len(set(_theirs) - set(_mine))} only by the agency file")
        # Every record the two agree is the same peak is byte identical
        # over the columns that matter, codes included.
        assert not _report[_site]["differing"], (_site, _report[_site]["differing"])

    # The measured shape of the agreement. The agency's file carries a
    # type 3 record for a year with a stage peak and no discharge, which
    # a discharge export has no row for; that is the 12 at Asheville,
    # every one of them a nineteenth century high-water mark. The rows
    # each service dates differently are the next cell's subject.
    assert (_report[WORKED]["mine"], _report[WORKED]["theirs"],
            _report[WORKED]["identical"]) == (130, 140, 128)
    # Ten of the twelve are nineteenth century years with a stage peak
    # and no discharge at all, which a discharge export has no row for;
    # the other two are the same peaks under the other service's date,
    # which the next cell resolves.
    assert len(_report[WORKED]["only_theirs"]) == 12
    _blank = [k for k in _report[WORKED]["only_theirs"] if not _report[WORKED]["theirs_q"][k]]
    assert len(_blank) == 10 and all(int(k[:4]) < 1900 for k in _blank), _blank
    assert (_report[HISTORIC]["mine"], _report[HISTORIC]["theirs"],
            _report[HISTORIC]["identical"]) == (110, 110, 110)
    assert (_report[REGULATED]["mine"], _report[REGULATED]["theirs"],
            _report[REGULATED]["identical"]) == (104, 104, 95)
    return


@app.cell
def _(HISTORIC, REGULATED, WORKED, load, reference, run):
    # 6. Where the two disagree it is the date and never the value, and
    #    the difference is the clock: the collection dates a peak in UTC
    #    and the agency's file in the gauge's local time, so an evening
    #    peak is filed on the next day. Small and real: a peak late on
    #    September 30 local time changes water year when read in UTC.
    import datetime as _dt

    _OFFSET = {"EST": 5, "CST": 6, "MST": 7, "PST": 8, "AKST": 9, "HST": 10}
    _shifted = 0
    for _site in (WORKED, HISTORIC, REGULATED):
        _doc = load(_site)
        _tz = _doc["monitoring_location"]["time_zone_abbreviation"]
        assert _tz in _OFFSET, (_site, _tz)
        _std = _OFFSET[_tz]
        _code, _err, _receipt, _written = run(_site, name=f"d{_site}")
        assert _code == 0, _err
        _mine = {l[16:20] + l[20:22] + l[22:24]: l for l in _written.splitlines() if l.startswith("3")}
        _theirs = {l[16:20] + l[20:22] + l[22:24]: l for l in reference(_site).splitlines()
                   if l.startswith("3")}
        _rows = {f"{int(r['year'])}{int(r['month']):02d}{int(r['day']):02d}": r
                 for r in _doc["rows"]
                 if r["parameter_code"] == "00060" and r["month"] and r["day"]}
        for _k in sorted(set(_mine) - set(_theirs)):
            _d = _dt.date(int(_k[:4]), int(_k[4:6]), int(_k[6:]))
            _prev = (_d - _dt.timedelta(days=1)).strftime("%Y%m%d")
            assert _prev in _theirs, (_site, _k, "not a one day shift")
            # Same peak: the value is identical, only the date moved.
            assert _mine[_k][24:31] == _theirs[_prev][24:31], (_site, _k)
            # And it happened in the evening: the UTC hour is inside the
            # site's offset, so locally it was still the day before.
            _hh = int(str(_rows[_k]["time_of_day"])[:2])
            assert _hh < _std, (_site, _k, _hh, _tz)
            _shifted += 1
    # Two at Asheville, none at Biltmore beside it, nine at Lees Ferry:
    # every row the two services date differently, and nothing else.
    assert _shifted == 11, _shifted
    print(f"{_shifted} peaks dated one day apart by the two services, every one of them "
          f"an evening peak with the value unchanged")
    return


@app.cell
def _(REGULATED, WORKED, run):
    # 7. The refusals, asserted as behaviour. A fit is refused over a
    #    stage series, over a regulated record, and over a record carrying
    #    historic or censored peaks, because the frequency program treats
    #    each of those differently and this is not that program.
    _c, _err, _, _ = run(WORKED, parameter="00065", extra=["--screening-fit"], name="stage")
    assert _c == 2 and "fit to discharge" in _err, _err

    _c, _err, _, _ = run(REGULATED, extra=["--screening-fit"], name="reg")
    assert _c == 2 and "operating rule" in _err, _err
    assert "--acknowledge-regulation" in _err, "the refusal names the way through"

    _c, _err, _, _ = run(REGULATED, extra=["--screening-fit", "--acknowledge-regulation"], name="reg2")
    assert _c == 2 and "historic" in _err and "censored" in _err, _err
    return


@app.cell
def _(WORKED, run):
    # 8. The screening fit itself: labelled screening, carrying what it
    #    did not implement, and quoting no quantile without an interval
    #    that contains it.
    _c, _err, _receipt, _ = run(WORKED, extra=["--screening-fit"], name="fit")
    assert _c == 0, _err
    _fit = _receipt["screening_fit"]
    assert _fit["is_bulletin_17c"] is False
    assert "expected moments" in _fit["not_implemented"]
    assert _fit["n_systematic"] == 130, _fit["n_systematic"]
    for _row in _fit["quantiles"]:
        _lo, _hi = _row["interval_90pct_cfs"]
        assert _row["label"] == "screening"
        assert _lo < _row["screening_estimate_cfs"] < _hi, _row
        assert _lo > 0
    _q100 = next(r for r in _fit["quantiles"] if r["return_period_years"] == 100)
    _q2 = next(r for r in _fit["quantiles"] if r["return_period_years"] == 2)
    assert _q100["screening_estimate_cfs"] > _q2["screening_estimate_cfs"]
    # The interval widens with the return period, which is the reason a
    # bare number is refused.
    _w = lambda r: (r["interval_90pct_cfs"][1] - r["interval_90pct_cfs"][0]) / r["screening_estimate_cfs"]
    assert _w(_q100) > _w(_q2)
    return


@app.cell
def _(WORKED, run):
    # 9. The receipt states the record before anything is fitted to it:
    #    the other series it did not use, the qualifiers the frequency
    #    program acts on, and the qualifiers that have no code in the file
    #    format at all.
    _c, _err, _receipt, _written = run(WORKED, name="receipt")
    assert _c == 0, _err
    assert _receipt["rows_in_fixture_other_parameters"]["count"] == 140
    assert _receipt["rows_in_fixture_other_parameters"]["parameters"] == ["00065"]
    assert _receipt["water_years"] == [1896, 2025]
    assert _receipt["missing_water_years"] == [], "this gauge has no gap"
    # Nothing in this record needs special handling, which is why it is
    # the worked gauge: no regulation, no urbanization, no historic
    # peaks, nothing censored. Its two EVENT rows do carry a code into
    # the file, and the frequency program is documented to ignore it.
    _acted = _receipt["qualifier_codes_acted_on_by_the_frequency_program"]
    assert _acted == {}, _acted
    assert _receipt["qualifiers_with_no_watstore_code"] == {}, \
        _receipt["qualifiers_with_no_watstore_code"]
    _c9 = [l for l in _written.splitlines() if l.startswith("3") and l[31:43].strip() == "9"]
    assert len(_c9) == 2, len(_c9)
    return


@app.cell
def _():
    # 10. Why the fit is labelled screening, in one number. Thirty
    #     independent 130 year records drawn from one log-Pearson III
    #     with a log skew of 0.3, fitted the way a session fit is
    #     fitted: the station skew alone moves the 100 year quantile by
    #     a factor of two. This is synthetic and seeded; it measures the
    #     method, not a gauge.
    import random as _random
    import statistics as _stats

    def _K(z, g):
        return (2 / g) * ((1 + g * z / 6 - g * g / 36) ** 3 - 1) if abs(g) > 1e-9 else z

    def _moments(xs):
        _m = _stats.fmean(xs)
        _s = _stats.stdev(xs)
        _n = len(xs)
        _g = (_n * sum((x - _m) ** 3 for x in xs)) / ((_n - 1) * (_n - 2) * _s ** 3)
        return _m, _s, _g

    _TRUE_G, _TRUE_M, _TRUE_S = 0.3, 4.0, 0.25
    _z100 = _stats.NormalDist().inv_cdf(0.99)
    _truth = 10 ** (_TRUE_M + _K(_z100, _TRUE_G) * _TRUE_S)
    _est, _skews = [], []
    for _seed in range(1, 31):
        _r = _random.Random(_seed)
        _xs = [_TRUE_M + _K(_r.gauss(0, 1), _TRUE_G) * _TRUE_S for _ in range(130)]
        _m, _s, _g = _moments(_xs)
        _skews.append(_g)
        _est.append(10 ** (_m + _K(_z100, _g) * _s))
    assert abs(_truth - 43283) < 1, _truth
    assert min(_skews) < -0.2 and max(_skews) > 0.8, (min(_skews), max(_skews))
    assert max(_est) / min(_est) > 2.0, max(_est) / min(_est)
    assert round(min(_est), -2) == 31100.0 and round(max(_est), -2) == 63400.0, (min(_est), max(_est))
    assert sum(1 for _q in _est if _q < _truth) == 13
    return


if __name__ == "__main__":
    app.run()
