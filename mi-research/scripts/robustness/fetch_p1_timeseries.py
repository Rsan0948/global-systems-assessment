#!/usr/bin/env python3
"""
Fetch FULL TIME SERIES of revealed-outcome P1 state-capacity indicators for
Component C (C1 2004-vintage rebuild + C2 perception-lag). Unlike
fetch_alt_indicators.py (which keeps only the latest value), this keeps every year.

    GC.TAX.TOTL.GD.ZS   tax revenue % GDP
    SE.XPD.TOTL.GD.ZS   govt education expenditure % GDP

Cache: data/robustness/outcomes/p1_revealed_timeseries.json  {label: {iso3: {year: val}}}.
Stdlib urllib. Aggregates excluded via the WB country list.
"""
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "robustness"))
from fetch_alt_indicators import _get_json, wb_aggregate_codes  # noqa: E402

OUT = ROOT / "data" / "robustness" / "outcomes" / "p1_revealed_timeseries.json"
INDICATORS = {
    "tax_rev_pct_gdp": "GC.TAX.TOTL.GD.ZS",
    "gov_edu_exp_pct_gdp": "SE.XPD.TOTL.GD.ZS",
}
YEAR_MIN, YEAR_MAX = 1994, 2024


def fetch_series(code, aggregates):
    base = (f"https://api.worldbank.org/v2/country/all/indicator/{code}"
            f"?date={YEAR_MIN}:{YEAR_MAX}&format=json&per_page=1000")
    page, total = 1, 1
    out = {}
    while page <= total:
        data = _get_json(f"{base}&page={page}")
        meta = data[0]
        total = meta.get("pages", 1)
        for row in (data[1] or []):
            iso = row.get("countryiso3code")
            val = row.get("value")
            yr = row.get("date")
            if not iso or iso in aggregates or val is None:
                continue
            out.setdefault(iso, {})[int(yr)] = float(val)
        page += 1
        time.sleep(0.2)
    return out


def main():
    aggregates = wb_aggregate_codes()
    result = {}
    for label, code in INDICATORS.items():
        s = fetch_series(code, aggregates)
        result[label] = s
        cov04 = sum(1 for iso in s if any(y in s[iso] for y in range(2002, 2007)))
        print(f"{label} ({code}): {len(s)} countries; {cov04} with a value in [2002,2006]")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"_meta": {"source": "WB API v2", "year_range": [YEAR_MIN, YEAR_MAX]},
                               "series": result}, indent=2))
    print(f"-> {OUT.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
