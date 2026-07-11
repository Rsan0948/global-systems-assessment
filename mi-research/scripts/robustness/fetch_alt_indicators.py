"""
Fetch alternative ("revealed-outcome") indicators from the World Bank API v2.

Plan 1 of the frozen pre-registration (docs/ROBUSTNESS_PREREGISTRATION.md).
Read-only w.r.t. the engine: this script only FETCHES and CACHES raw indicator
series. All rescaling / injection / scoring happens in substitute.py.

Indicators (frozen in the prereg):
    GC.TAX.TOTL.GD.ZS   tax revenue % GDP          (P1 substitute a)
    SE.XPD.TOTL.GD.ZS   govt education exp % GDP    (P1 substitute b)
    LP.LPI.OVRL.XQ      Logistics Performance Index (P1 substitute c; snap to wave)
    TX.VAL.TECH.MF.ZS   high-tech exports % mfg exp (P2/GII substitute)
    VC.IHR.PSRC.P5      intentional homicide /100k  (P5/FSI substitute)

Cache: data/robustness/alt_indicators.json
Uses stdlib urllib (requests is not installed in this venv).
"""
from __future__ import annotations
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # mi-research/
OUT = ROOT / "data" / "robustness" / "alt_indicators.json"

# label -> (WB code, latest_target_year, min_year_to_scan)
INDICATORS = {
    "tax_rev_pct_gdp":   ("GC.TAX.TOTL.GD.ZS", 2024, 2015),
    "gov_edu_exp_pct_gdp": ("SE.XPD.TOTL.GD.ZS", 2024, 2015),
    "lpi_overall":       ("LP.LPI.OVRL.XQ",    2023, 2016),  # LPI waves; 2023 is latest
    "hightech_exp_pct":  ("TX.VAL.TECH.MF.ZS", 2024, 2015),
    "homicide_per100k":  ("VC.IHR.PSRC.P5",    2024, 2015),
}

WB_COUNTRY_URL = "https://api.worldbank.org/v2/country?format=json&per_page=400"


def _get_json(url: str, retries: int = 4):
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "mi-robustness/1.0"})
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 ** attempt)
    raise RuntimeError(f"Failed to fetch {url}: {last}")


def wb_aggregate_codes() -> set:
    """ISO3 codes that are WB *aggregates* (regions/income groups) — excluded."""
    data = _get_json(WB_COUNTRY_URL)
    codes = {
        c.get("id") for c in data[1]
        if c.get("region", {}).get("value") == "Aggregates" and c.get("id")
    }
    return codes


def fetch_indicator(code: str, year_min: int, year_max: int, aggregates: set) -> dict:
    """Return {iso3: {"value": float, "year": int}} using the LATEST available
    year within [year_min, year_max] for each country. Aggregates excluded."""
    base = (f"https://api.worldbank.org/v2/country/all/indicator/{code}"
            f"?date={year_min}:{year_max}&format=json&per_page=500")
    page, total_pages = 1, 1
    best: dict[str, tuple[int, float]] = {}
    while page <= total_pages:
        data = _get_json(f"{base}&page={page}")
        if not isinstance(data, list) or len(data) < 2 or data[1] is None:
            break
        total_pages = data[0].get("pages", 1)
        for rec in data[1]:
            iso3 = (rec.get("countryiso3code") or "").strip() \
                or (rec.get("country", {}) or {}).get("id")
            val = rec.get("value")
            try:
                yr = int(rec.get("date", 0))
            except (TypeError, ValueError):
                continue
            if val is None or not iso3 or len(iso3) != 3 or iso3 in aggregates:
                continue
            v = float(val)
            # keep the most recent year per country
            if iso3 not in best or yr > best[iso3][0]:
                best[iso3] = (yr, v)
        page += 1
        time.sleep(0.25)
    return {iso: {"value": v, "year": y} for iso, (y, v) in best.items()}


def main():
    aggregates = wb_aggregate_codes()
    print(f"WB aggregate codes excluded: {len(aggregates)}")
    out = {"_meta": {"aggregates_excluded": len(aggregates),
                     "source": "World Bank API v2 (WDI)",
                     "fetched": time.strftime("%Y-%m-%d %H:%M:%S")},
           "indicators": {}}
    for label, (code, ymax, ymin) in INDICATORS.items():
        series = fetch_indicator(code, ymin, ymax, aggregates)
        yrs = {}
        for iso, d in series.items():
            yrs[d["year"]] = yrs.get(d["year"], 0) + 1
        out["indicators"][label] = {
            "code": code, "year_range": [ymin, ymax],
            "n_countries": len(series),
            "year_distribution": dict(sorted(yrs.items())),
            "data": series,
        }
        print(f"{label:22s} {code:20s} N={len(series):4d}  years={dict(sorted(yrs.items()))}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()
