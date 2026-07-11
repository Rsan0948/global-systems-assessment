#!/usr/bin/env python3
"""
Inequality — fetch WID top-10%/top-1% pre-tax income shares (via OWID grapher
republication of WID) + WB Gini (SI.POV.GINI). Read-only, cached. Frozen sources:
docs/INEQUALITY_PREREGISTRATION.md. Writes data/robustness/inequality/inequality.json:
  { top10: {iso:{year:val}}, top1:{...}, gini_wb:{...} }
"""
from __future__ import annotations
import csv
import io
import json
import time
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "robustness" / "inequality" / "inequality.json"

OWID = {
    "top10": "income-share-top-10-before-tax-wid",
    "top1": "income-share-top-1-before-tax-wid",
}
WB_GINI = ("https://api.worldbank.org/v2/country/all/indicator/SI.POV.GINI"
           "?format=json&per_page=20000&date=1960:2024")
WB_COUNTRY_URL = "https://api.worldbank.org/v2/country?format=json&per_page=400"


def _get(url, decode=True, retries=5):
    last = None
    for a in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 mi/1.0"})
            with urllib.request.urlopen(req, timeout=45) as r:
                data = r.read()
                return data.decode("utf-8", "replace") if decode else data
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 ** a)
    raise RuntimeError(f"fetch failed {url}: {last}")


def owid_series(slug):
    url = f"https://ourworldindata.org/grapher/{slug}.csv?csvType=full&useColumnShortNames=true"
    rows = list(csv.DictReader(io.StringIO(_get(url))))
    valcol = [c for c in rows[0].keys() if c.startswith("share_top")][0]
    ser = defaultdict(dict)
    for r in rows:
        iso = r.get("code"); v = r.get(valcol)
        if iso and len(iso) == 3 and v not in (None, ""):
            try:
                ser[iso][r["year"]] = float(v)
            except ValueError:
                pass
    return dict(ser)


def wb_aggregates():
    data = json.loads(_get(WB_COUNTRY_URL))
    return {c["id"] for c in data[1]
            if c.get("region", {}).get("value") == "Aggregates" and c.get("id")}


def wb_gini():
    agg = wb_aggregates()
    data = json.loads(_get(WB_GINI))
    ser = defaultdict(dict)
    if isinstance(data, list) and len(data) > 1 and data[1]:
        for r in data[1]:
            iso = r.get("countryiso3code"); v = r.get("value")
            if iso and iso not in agg and v is not None:
                ser[iso][r["date"]] = v
    return dict(ser)


def main():
    out = {"_source": "WID top-shares via OWID grapher; WB SI.POV.GINI"}
    for k, slug in OWID.items():
        out[k] = owid_series(slug)
        print(f"  {k}: {len(out[k])} countries")
    out["gini_wb"] = wb_gini()
    print(f"  gini_wb: {len(out['gini_wb'])} countries")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=0))
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
