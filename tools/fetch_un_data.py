#!/usr/bin/env python3
"""Download the latest World numbers for every SDG indicator.

Talks to the official UN SDG API (https://unstats.un.org/sdgapi/) and writes
a small, committed snapshot:

  data/un-series-world-latest.json

For every indicator it keeps up to three "key" data series (the first ones
the UN lists for the current database release), and for each series:

* the World (area code 1) headline value: latest and earliest year;
* the unit, as described by the API;
* how many countries or areas report data for the series.

Nothing is invented: every number in the snapshot is copied from an API
response. import_un_sdgs.py turns the snapshot into the "Latest global
numbers" block of each problem.md (without touching the network).

The script is polite: one request at a time, a pause between requests,
retries with back-off, and an on-disk cache so an interrupted run resumes.

Usage:
  python tools/fetch_un_data.py                 # fetch and write snapshot
  python tools/fetch_un_data.py --cache DIR     # where raw responses go
  python tools/fetch_un_data.py --max-series 3  # series kept per indicator
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sdg_common import DATA_DIR, code_key  # noqa: E402

API = "https://unstats.un.org/sdgapi/v1/sdg"
OUT_FILE = DATA_DIR / "un-series-world-latest.json"
PAUSE = 0.3  # seconds between live requests
USER_AGENT = ("open-problems/1.0 (+https://github.com/harrythentrepreneur/"
              "open-problems)")


class Fetcher:
    def __init__(self, cache_dir: Path) -> None:
        self.cache_dir = cache_dir
        cache_dir.mkdir(parents=True, exist_ok=True)
        self.live = 0

    def get(self, path: str, params: dict | None = None):
        url = f"{API}/{path}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        key = hashlib.sha1(url.encode()).hexdigest()
        cached = self.cache_dir / f"{key}.json"
        if cached.exists():
            return json.loads(cached.read_text(encoding="utf-8"))
        delay = 5.0
        for attempt in range(1, 6):
            try:
                time.sleep(PAUSE)
                req = urllib.request.Request(
                    url, headers={"User-Agent": USER_AGENT,
                                  "Accept": "application/json"})
                with urllib.request.urlopen(req, timeout=180) as resp:
                    raw = resp.read()
                data = json.loads(raw)
                cached.write_bytes(raw)
                self.live += 1
                return data
            except (urllib.error.URLError, TimeoutError,
                    json.JSONDecodeError, ConnectionError) as exc:
                if attempt == 5:
                    raise RuntimeError(f"giving up on {url}: {exc}") from exc
                print(f"  retry {attempt} for {url} ({exc}); "
                      f"waiting {delay:.0f}s", file=sys.stderr)
                time.sleep(delay)
                delay *= 2
        raise AssertionError("unreachable")


def countries_from_tree(tree: list) -> set[str]:
    out: set[str] = set()

    def walk(node: dict) -> None:
        if node.get("type") == "Country":
            out.add(str(node["geoAreaCode"]))
        for child in node.get("children") or []:
            walk(child)

    for root in tree:
        walk(root)
    return out


def current_series(indicator: dict) -> tuple[str, list[dict]]:
    """Series in the newest database release, in the UN's own order."""
    releases = sorted({s["release"] for s in indicator["series"]})
    latest = releases[-1] if releases else ""
    seen: dict[str, dict] = {}
    for s in indicator["series"]:
        if s["release"] == latest and s["code"] not in seen:
            seen[s["code"]] = {"code": s["code"],
                               "description": s["description"].strip()}
    return latest, list(seen.values())


def year_of(rec: dict) -> str:
    detail = (rec.get("time_detail") or "").strip()
    start = rec.get("timePeriodStart")
    year = str(int(start)) if isinstance(start, (int, float)) else str(start)
    if detail and detail != year and len(detail) <= 12:
        return detail
    return year


def headline(records: list[dict], dim_desc: dict, unit_desc: dict) -> dict:
    """Pick the headline (most 'total') breakdown of one series."""
    groups: dict[tuple, list[dict]] = {}
    for rec in records:
        dims = tuple(sorted((k, v) for k, v in (rec.get("dimensions") or {})
                            .items()))
        unit = (rec.get("attributes") or {}).get("Units", "")
        groups.setdefault((dims, unit), []).append(rec)

    def score(item):
        (dims, _unit), recs = item
        totals = 0
        for k, v in dims:
            if k == "Reporting Type":
                totals += 2 if v == "G" else 0
            elif dim_desc.get((k, v), ("", ""))[1] == "_T":
                totals += 1
        latest = max(r["timePeriodStart"] or 0 for r in recs)
        return (totals, len(recs), latest)

    (dims, unit), recs = max(groups.items(), key=score)
    recs = [r for r in recs if r.get("value") not in (None, "", "NaN")]
    if not recs:
        return {}
    recs.sort(key=lambda r: r["timePeriodStart"] or 0)
    first, last = recs[0], recs[-1]
    breakdown = [
        f"{k}: {dim_desc.get((k, v), (v, ''))[0]}"
        for k, v in dims
        if k != "Reporting Type" and dim_desc.get((k, v), ("", ""))[1] != "_T"
    ]
    return {
        "unit_code": unit,
        "unit": unit_desc.get(unit, unit),
        "breakdown": breakdown,
        "latest": {"year": year_of(last), "value": last["value"]},
        "earliest": {"year": year_of(first), "value": first["value"]},
        "observations": len(recs),
        "source": (last.get("source") or "").strip(),
    }


def run(cache: Path, max_series: int) -> int:
    f = Fetcher(cache)
    print("Fetching framework (goals, targets, indicators, series)...")
    framework = f.get("Goal/List", {"includechildren": "true"})
    tree = f.get("GeoArea/Tree")
    country_codes = countries_from_tree(tree)

    indicators = [i for g in framework for t in g["targets"]
                  for i in t["indicators"]]
    # The same indicator can appear under two targets; keep one copy.
    unique: dict[str, dict] = {}
    for ind in indicators:
        unique.setdefault(ind["code"], ind)
    codes = sorted(unique, key=code_key)

    out: dict[str, dict] = {}
    release_seen = set()
    for n, code in enumerate(codes, 1):
        ind = unique[code]
        release, series = current_series(ind)
        release_seen.add(release)
        print(f"[{n}/{len(codes)}] {code}: {len(series)} series",
              flush=True)
        world = f.get("Indicator/Data", {"indicator": code, "areaCode": "1",
                                         "pageSize": "20000"})
        if world.get("totalPages", 1) > 1:
            print(f"  warning: {code} World data has "
                  f"{world['totalPages']} pages; only page 1 used",
                  file=sys.stderr)
        dim_desc = {(d["id"], c["code"]): (c["description"], c.get("sdmx"))
                    for d in world.get("dimensions") or []
                    for c in d["codes"]}
        unit_desc = {c["code"]: c["description"]
                     for a in world.get("attributes") or []
                     if a["id"] == "Units" for c in a["codes"]}
        by_series: dict[str, list[dict]] = {}
        for rec in world.get("data") or []:
            by_series.setdefault(rec["series"], []).append(rec)

        with_world = [s for s in series if by_series.get(s["code"])]
        without = [s for s in series if not by_series.get(s["code"])]
        chosen = (with_world + without)[:max_series]
        kept = []
        for s in chosen:
            entry = dict(s)
            recs = by_series.get(s["code"])
            if recs:
                entry["world"] = headline(recs, dim_desc, unit_desc) or None
            else:
                entry["world"] = None
            areas = f.get(f"Series/{s['code']}/GeoAreas")
            entry["countries_with_data"] = len(
                {str(a["geoAreaCode"]) for a in areas or []}
                & country_codes)
            kept.append(entry)
        out[code] = {
            "description": ind["description"].strip(),
            "series_total": len(series),
            "series_with_world": len(with_world),
            "series": kept,
        }

    snapshot = {
        "source": API,
        "publisher": "United Nations Statistics Division, "
                     "SDG Global Database",
        "retrieved": dt.date.today().isoformat(),
        "database_release": sorted(release_seen)[-1],
        "note": ("World = UN area code 1. For each indicator, up to "
                 f"{max_series} series from the current release, series "
                 "with a World value first. 'world' is the headline "
                 "breakdown (totals where available); 'breakdown' lists "
                 "any dimension that is not a total. countries_with_data "
                 "= countries or areas listed by Series/{code}/GeoAreas "
                 "that the UN geo tree marks as type 'Country'."),
        "indicators": out,
    }
    OUT_FILE.write_text(json.dumps(snapshot, indent=1, ensure_ascii=False)
                        + "\n", encoding="utf-8")
    n_world = sum(1 for v in out.values() if v["series_with_world"])
    print(f"wrote {OUT_FILE.name}: {len(out)} indicators, "
          f"{n_world} with a World value; {f.live} live requests")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--cache", type=Path, default=Path(
        os.environ.get("TMPDIR", "/tmp")) / "open-problems-un-cache",
        help="directory for raw API responses (resume support)")
    parser.add_argument("--max-series", type=int, default=3)
    args = parser.parse_args(argv)
    return run(args.cache, args.max_series)


if __name__ == "__main__":
    sys.exit(main())
