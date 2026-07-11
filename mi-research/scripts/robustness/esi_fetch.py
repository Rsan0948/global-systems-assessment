#!/usr/bin/env python3
"""ESI Phase 1 — fetch the World Bank WDI/IDS series for the ESI (see ESI_PREREGISTRATION.md).

Fetches the automatable ESI indicators from the World Bank API v2 for ALL countries
across a year range (one paged call per indicator), caches raw values. IMF MONA,
SWFI, and the Systemic-Insurance categorical codings are handled separately (manual
data files). Read-only w.r.t. everything else.

    python scripts/robustness/esi_fetch.py
"""
import json
import socket
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config  # noqa: E402

OUTDIR = ROOT / "data" / "robustness" / "esi"
OUT = OUTDIR / "esi_wb_raw.json"
YEARS = "1990:2013"  # 2004 & 2012 targets + nearest-year fallback + light history
socket.setdefaulttimeout(60)

# WB code -> ESI indicator key (from config/esi.json)
WB_CODES = {
    "BX.KLT.DINV.WD.GD.ZS": "fdi_net_inflows_pct_gdp",
    "DT.ODA.ODAT.GN.ZS": "oda_pct_gni",
    "BX.TRF.PWKR.DT.GD.ZS": "remittances_pct_gdp",
    "FI.RES.TOTL.MO": "reserves_months_imports",
    "DT.DOD.ALLC.ZS": "concessional_debt_share",
    "DT.TDS.DECT.GN.ZS": "debt_service_pct_gni",
}


def wb_get(url):
    last = None
    for attempt in range(6):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.loads(r.read())
        except Exception as e:
            last = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"WB fetch failed after retries: {url}\n{last}")


def fetch_indicator(code):
    """Return {iso3: {year: value}} for one indicator, all countries, YEARS."""
    page, out, total_pages = 1, {}, 1
    while page <= total_pages:
        url = (f"https://api.worldbank.org/v2/country/all/indicator/{code}"
               f"?format=json&per_page=15000&date={YEARS}&page={page}")
        d = wb_get(url)
        if not isinstance(d, list) or len(d) < 2 or not d[1]:
            break  # WB returned metadata-only / error / empty page
        meta = d[0]
        total_pages = meta.get("pages", 1) if isinstance(meta, dict) else 1
        for row in d[1]:
            iso = row.get("countryiso3code")
            val = row.get("value")
            yr = row.get("date")
            if iso and len(iso) == 3 and val is not None:
                out.setdefault(iso, {})[int(yr)] = val
        page += 1
    return out


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    indicators = {}
    for code, key in WB_CODES.items():
        data = fetch_indicator(code)
        indicators[key] = {"wb_code": code, "values": data}
        n_iso = len(data)
        n_pts = sum(len(v) for v in data.values())
        print(f"  {key:28s} {code:22s} -> {n_iso:3d} countries, {n_pts:5d} points")
    payload = {
        "_meta": {
            "source": "World Bank API v2",
            "years": YEARS,
            "prereg": "docs/ESI_PREREGISTRATION.md",
            "spec": "config/esi.json",
            "codes": {k: v for k, v in WB_CODES.items()},
        },
        "indicators": indicators,
    }
    OUT.write_text(json.dumps(payload, indent=1))
    print(f"-> {OUT.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
