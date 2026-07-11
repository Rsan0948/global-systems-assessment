#!/usr/bin/env python3
"""
Decoupling — fetch new World Bank WDI series (Tests 3, 4, 5). Read-only, cached.
Codes frozen in docs/DECOUPLING_PREREGISTRATION.md (F4).

Cache: data/robustness/decoupling/wdi_decoupling.json
  { code: { iso3: { year(str): value } } }  (aggregates excluded)
"""
from __future__ import annotations
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "robustness" / "decoupling" / "wdi_decoupling.json"

CODES = {
    "NV.AGR.TOTL.ZS": "agriculture_pct_gdp",
    "NV.IND.TOTL.ZS": "industry_pct_gdp",
    "NV.SRV.TOTL.ZS": "services_pct_gdp",
    "NV.IND.MANF.ZS": "manufacturing_pct_gdp",
    "CM.MKT.LCAP.GD.ZS": "stockmkt_cap_pct_gdp",
    "FS.AST.PRVT.GD.ZS": "private_credit_pct_gdp",
    "SE.XPD.TOTL.GD.ZS": "edu_exp_pct_gdp",
    "SH.XPD.GHED.GD.ZS": "health_pub_exp_pct_gdp",
    "GC.TAX.TOTL.GD.ZS": "tax_rev_pct_gdp",
    "NE.TRD.GNFS.ZS": "trade_openness_pct_gdp",
    "BX.KLT.DINV.WD.GD.ZS": "fdi_net_inflow_pct_gdp",
    "per_allsp.expend.gdp": "social_protection_pct_gdp",  # ASPIRE; best-effort
}

WB_COUNTRY_URL = "https://api.worldbank.org/v2/country?format=json&per_page=400"
WB_SERIES = ("https://api.worldbank.org/v2/country/all/indicator/{code}"
             "?format=json&per_page=20000&date=1970:2024")


def _get(url, retries=5):
    last = None
    for a in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "mi-decoupling/1.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 ** a)
    raise RuntimeError(f"fetch failed {url}: {last}")


def aggregates():
    data = _get(WB_COUNTRY_URL)
    return {c["id"] for c in data[1]
            if c.get("region", {}).get("value") == "Aggregates" and c.get("id")}


def main():
    agg = aggregates()
    out = {}
    for code, label in CODES.items():
        try:
            data = _get(WB_SERIES.format(code=code))
        except Exception as e:  # noqa: BLE001
            print(f"  {label} ({code}): FETCH FAILED — {e}")
            out[label] = {"_code": code, "_error": str(e)}
            continue
        series = {}
        if isinstance(data, list) and len(data) > 1 and data[1]:
            for row in data[1]:
                iso = row.get("countryiso3code")
                val = row.get("value")
                yr = row.get("date")
                if not iso or iso in agg or val is None:
                    continue
                series.setdefault(iso, {})[yr] = val
        series["_code"] = code
        out[label] = series
        n = sum(1 for k in series if not k.startswith("_"))
        print(f"  {label} ({code}): {n} countries")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=0))
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
