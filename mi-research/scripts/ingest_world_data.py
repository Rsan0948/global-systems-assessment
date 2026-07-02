"""
World-scale real-data ingestion for the MI framework.

Pulls free, no-auth indicator data for every country and writes one
`data/countries/<slug>.json` per country in the schema the scorer consumes
(`indicators_by_year`). Sources:

  * World Bank WGI (0-100 anchored "SC" scores)  -> P1 (+ voice) and P5 stability
  * World Bank WDI                                -> P4 (GDP PPP, resource rents,
                                                       ODA) and P2 R&D proxy
  * UNDP HDR composite-indices time series        -> P3 education + life-exp index

WGI here is the current 0-100 anchored score (same vintage cases 21-25 use), so
values are engine-ready (no z-score mis-scale). Missing values stay null —
missing data is information, never interpolated. Existing curated country files
are MERGED additively (their context + any hand-curated years are preserved).

Run: python scripts/ingest_world_data.py
"""

from __future__ import annotations

import io
import json
import os
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "countries"
YEARS = "1996:2024"
UA = {"User-Agent": "Mozilla/5.0 (MI-research world ingest)"}

# World Bank indicator code -> engine field
WB = {
    "GOV_WGI_GE.SC": "gov_effectiveness",
    "GOV_WGI_RL.SC": "rule_of_law",
    "GOV_WGI_RQ.SC": "regulatory_quality",
    "GOV_WGI_CC.SC": "control_of_corruption",
    "GOV_WGI_PV.SC": "political_stability",
    "GOV_WGI_VA.SC": "voice_accountability",
    "NY.GDP.PCAP.PP.CD": "gdp_per_capita_ppp",
    "NY.GDP.TOTL.RT.ZS": "resource_rents_pct_gdp",
    "DT.ODA.ODAT.GN.ZS": "oda_pct_gni",
    "GB.XPD.RSDV.GD.ZS": "rd_pct_gdp",
}

# Engine fields we (may) source; anything else stays null.
ALL_FIELDS = list(dict.fromkeys(list(WB.values()) + [
    "cpi", "gii", "eci", "education_index", "life_expectancy_index", "fsi",
]))


def _get_json(url: str, tries: int = 4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode())
        except Exception as e:  # noqa: BLE001 - transient network
            if i == tries - 1:
                raise
            time.sleep(1.5 * (i + 1))


def _get_text(url: str, tries: int = 3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.read().decode("utf-8-sig", errors="replace")
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(1.5 * (i + 1))


def slug(name: str) -> str:
    s = name.lower()
    for a, b in [("'", ""), (".", ""), (",", ""), ("(", ""), (")", ""),
                 ("&", "and"), ("/", " "), ("-", " ")]:
        s = s.replace(a, b)
    return "_".join(s.split())


def fetch_countries() -> dict:
    """iso3 -> {name, iso2, region, income}. Real countries only."""
    d = _get_json(f"https://api.worldbank.org/v2/country?format=json&per_page=400")
    out = {}
    for c in d[1]:
        if c["region"]["value"] == "Aggregates":
            continue
        out[c["id"]] = {
            "name": c["name"], "iso2": c["iso2Code"],
            "region": c["region"]["value"], "income": c["incomeLevel"]["value"],
            "capital": c.get("capitalCity", ""),
        }
    return out


def fetch_wb_indicator(code: str) -> dict:
    """iso3 -> {year(str): value}. One batched request over all countries."""
    url = (f"https://api.worldbank.org/v2/country/all/indicator/{code}"
           f"?format=json&date={YEARS}&per_page=30000")
    d = _get_json(url)
    series: dict[str, dict[str, float]] = {}
    if not isinstance(d, list) or len(d) < 2 or d[1] is None:
        return series
    for row in d[1]:
        v = row["value"]
        if v is None:
            continue
        iso3 = row["countryiso3code"]
        if not iso3:
            continue
        series.setdefault(iso3, {})[row["date"]] = round(float(v), 4)
    return series


def fetch_hdr() -> dict:
    """iso3 -> {year: {education_index, life_expectancy_index}} from UNDP HDR.

    Computes the two sub-indices from the published components (goalposts per
    the HDR technical notes): LE index = (le-20)/(85-20); EDU index = mean of
    eys/18 and mys/15. Returns {} on any failure (P3 is optional here).
    """
    urls = [
        "https://hdr.undp.org/sites/default/files/2023-24_HDR/HDR23-24_Composite_indices_complete_time_series.csv",
        "https://hdr.undp.org/sites/default/files/2021-22_HDR/HDR21-22_Composite_indices_complete_time_series.csv",
    ]
    text = None
    for u in urls:
        try:
            text = _get_text(u)
            if text and "iso3" in text[:200].lower():
                break
        except Exception:
            continue
    if not text:
        return {}
    import csv
    rows = list(csv.DictReader(io.StringIO(text)))
    out: dict[str, dict[str, dict]] = {}
    for r in rows:
        iso3 = (r.get("iso3") or r.get("ISO3") or "").strip()
        if not iso3 or len(iso3) != 3:
            continue
        for y in range(1990, 2024):
            le = r.get(f"le_{y}"); eys = r.get(f"eys_{y}"); mys = r.get(f"mys_{y}")
            def f(x):
                try:
                    return float(x)
                except (TypeError, ValueError):
                    return None
            le, eys, mys = f(le), f(eys), f(mys)
            rec = {}
            if le is not None:
                rec["life_expectancy_index"] = round(max(0.0, min(1.0, (le - 20) / 65.0)), 4)
            if eys is not None and mys is not None:
                ei = (min(eys / 18.0, 1.0) + min(mys / 15.0, 1.0)) / 2.0
                rec["education_index"] = round(max(0.0, min(1.0, ei)), 4)
            if rec:
                out.setdefault(iso3, {})[str(y)] = rec
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("fetching country list...")
    countries = fetch_countries()
    print(f"  {len(countries)} real countries")

    wb_series = {}
    for code, field in WB.items():
        print(f"fetching {code} -> {field} ...")
        wb_series[field] = fetch_wb_indicator(code)
        print(f"  {sum(len(v) for v in wb_series[field].values())} country-year values")

    print("fetching UNDP HDR (P3 education + life expectancy) ...")
    try:
        hdr = fetch_hdr()
        print(f"  HDR: {len(hdr)} countries with P3 data")
    except Exception as e:  # noqa: BLE001
        hdr = {}
        print(f"  HDR unavailable ({e}); P3 left null")

    # assemble per-country year panels
    written = 0
    for iso3, meta in countries.items():
        by_year: dict[str, dict] = {}
        # collect all years seen for this country across sources
        years = set()
        for field, series in wb_series.items():
            years |= set(series.get(iso3, {}).keys())
        years |= set(hdr.get(iso3, {}).keys())
        if not years:
            continue
        for y in sorted(years):
            rec = {f: None for f in ALL_FIELDS}
            for field, series in wb_series.items():
                if y in series.get(iso3, {}):
                    rec[field] = series[iso3][y]
            for k, v in hdr.get(iso3, {}).get(y, {}).items():
                rec[k] = v
            rec["_gaps"] = [f for f in ALL_FIELDS if rec[f] is None]
            by_year[y] = rec

        slug_name = slug(meta["name"])
        path = OUT / f"{slug_name}.json"
        payload = {
            "country": meta["name"], "iso3": iso3, "iso2": meta["iso2"],
            "region": meta["region"], "income_level": meta["income"],
            "notes": "World-scale hydrate: World Bank WGI (0-100 anchored SC scores) "
                     "+ WDI + UNDP HDR composite indices. Engine-ready 0-100 WGI. "
                     "Nulls are genuine gaps (not interpolated). "
                     "CPI/GII/ECI/FSI not sourced here (non-WB).",
            "indicators_by_year": by_year,
            "data_sources": {
                "wgi": "World Bank WGI 0-100 anchored score (GOV_WGI_*.SC), 1996-2024",
                "wdi": "World Bank WDI (NY.GDP.PCAP.PP.CD, NY.GDP.TOTL.RT.ZS, DT.ODA.ODAT.GN.ZS, GB.XPD.RSDV.GD.ZS)",
                "hdr": "UNDP HDR composite-indices time series (education + life-expectancy sub-indices computed from le/eys/mys goalposts)",
            },
        }

        if path.exists():
            # MERGE additively: preserve existing curation, fill only new years/fields
            existing = json.loads(path.read_text())
            eby = existing.get("indicators_by_year", {})
            for y, rec in by_year.items():
                if y not in eby:
                    eby[y] = rec
                else:
                    for f, v in rec.items():
                        if f == "_gaps":
                            continue
                        if eby[y].get(f) is None and v is not None:
                            eby[y][f] = v
            existing["indicators_by_year"] = eby
            existing.setdefault("data_sources", {}).update(payload["data_sources"])
            existing.setdefault("_world_hydrate", True)
            path.write_text(json.dumps(existing, indent=2, ensure_ascii=False) + "\n")
        else:
            path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
        written += 1

    print(f"\nwrote/updated {written} country files in {OUT}")


if __name__ == "__main__":
    main()
