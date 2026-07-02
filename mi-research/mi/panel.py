"""
Multi-tier indicator assembly — the full-coverage data path.

`mi.datasource` only resolves the WGI-anchored curated set directly. The full
~190-country coverage comes from assembling three tiers:

  A. wb_anchored (canonical Data API, via mi.datasource.get_indicators)
  B. the mi_pipeline scored panel CSV (full indicator family)
  C. wgi_full_panel (WGI institutions + gdp/PV/VA/rents)

`build_site_dataset.py` uses `load_universe` + `assemble` to build the site;
`indicators_for(name_or_iso, year)` wraps them so the CLIs and
`scoring.load_country_data` get the SAME full coverage the site has (instead of
failing for any country outside the curated Data API set, e.g. Norway).
Deterministic given fixed source data.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from mi import datasource as ds

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "sources"
CSV_PATH = ROOT.parent / "mi_pipeline" / "output" / "mi_scored_countries.csv"
YEAR = 2024

NAME_FIX = {  # micro-states/territories not named by any source
    "AND": "Andorra", "ATG": "Antigua and Barbuda", "ABW": "Aruba", "BHS": "Bahamas",
    "BMU": "Bermuda", "CYM": "Cayman Islands", "GRL": "Greenland", "KIR": "Kiribati",
    "MAC": "Macao", "MHL": "Marshall Islands", "NRU": "Nauru", "PLW": "Palau",
    "PRI": "Puerto Rico", "SMR": "San Marino", "KNA": "St Kitts and Nevis",
    "VIR": "US Virgin Islands",
}
# Clean raw World Bank / source names into readable display names.
DISPLAY_FIX = {
    "Lao PDR": "Laos", "Iran, Islamic Rep.": "Iran", "Congo, Rep.": "Republic of the Congo",
    "Congo, Dem. Rep.": "DR Congo", "Kyrgyz Republic": "Kyrgyzstan", "Slovak Republic": "Slovakia",
    "Egypt, Arab Rep.": "Egypt", "Yemen, Rep.": "Yemen", "Venezuela, RB": "Venezuela",
    "Russian Federation": "Russia", "Korea, Rep.": "South Korea", "Korea, Dem. People's Rep.": "North Korea",
    "Gambia, The": "Gambia", "Bahamas, The": "Bahamas", "Brunei Darussalam": "Brunei",
    "Syrian Arab Republic": "Syria", "Viet Nam": "Vietnam", "Macao SAR": "Macao",
    "Hong Kong SAR, China": "Hong Kong", "Turkiye": "Turkey", "Micronesia, Fed. Sts.": "Micronesia",
    "St. Lucia": "St Lucia", "St. Vincent and the Grenadines": "St Vincent & Grenadines",
}


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _panel_yr(panel, key, yr=YEAR):
    b = panel.get(key)
    if isinstance(b, dict):
        ys = [int(y) for y in b if int(y) <= yr]
        return b[str(max(ys))] if ys else None
    return b


def load_universe(year=YEAR):
    wb = json.load(open(SRC / "wb_anchored.json"))
    fp = json.load(open(SRC / "wgi_full_panel.json"))
    vd = json.load(open(SRC / "vdem_longrun.json"))
    csv_rows = {}  # iso3 -> latest-year row (prefer Track 1)
    for r in csv.DictReader(open(CSV_PATH)):
        if int(r["year"]) != year:
            continue
        iso = r["iso3"]
        if iso not in csv_rows or r["Track"] == "1":
            csv_rows[iso] = r
    names = {}
    for nm, v in wb.items():
        if v.get("iso3"):
            names[v["iso3"]] = nm
    for iso, r in csv_rows.items():
        names.setdefault(iso, r["country"])
    for iso, v in vd.items():
        if isinstance(v, dict) and v.get("name"):
            names.setdefault(iso, v["name"])
    names.update(NAME_FIX)
    return wb, fp, csv_rows, names


def assemble(iso, name, wb, fp, csv_rows, year=YEAR):
    """Return (indicators, tier_label) using the best available source. wb countries use the canonical API."""
    if name in wb:
        ind = ds.get_indicators(name, year)
        return (ind or {}), "A"
    panel = fp.get(iso, {})
    ind = {}
    r = csv_rows.get(iso)
    if r:  # tier B: full indicator family
        for key, col in [("gov_effectiveness", "GovEff"), ("rule_of_law", "RuleLaw"),
                         ("regulatory_quality", "RegQual"), ("control_of_corruption", "CtrlCorr"),
                         ("cpi", "CPI"), ("gii", "GII"), ("rd_pct_gdp", "RD"), ("eci", "ECI"),
                         ("education_index", "EduIdx"), ("life_expectancy_index", "LifeExpIdx")]:
            v = _f(r.get(col))
            if v is not None:
                ind[key] = v
    else:  # tier C: WGI institutions only
        for key, col in [("gov_effectiveness", "GE"), ("rule_of_law", "RL"),
                         ("regulatory_quality", "RQ"), ("control_of_corruption", "CC")]:
            v = _panel_yr(panel, col, year)
            if v is not None:
                ind[key] = v
    # shared from wgi_full_panel: gdp / political stability / voice / rents
    for key, col in [("gdp_per_capita_ppp", "gdp"), ("political_stability", "PV"),
                     ("voice_accountability", "VA"), ("resource_rents_pct_gdp", "rents")]:
        v = _panel_yr(panel, col, year)
        if v is not None and key not in ind:
            ind[key] = v
    return ind, ("B" if r else "C")


_RESOLVER = None


def _resolver(names):
    """name/display/iso (case-insensitive) -> iso3, over the full universe."""
    global _RESOLVER
    if _RESOLVER is not None:
        return _RESOLVER
    m = {}
    for iso, raw in names.items():
        m[iso.upper()] = iso
        m[raw.lower()] = iso
        disp = DISPLAY_FIX.get(raw)
        if disp:
            m[disp.lower()] = iso
    _RESOLVER = m
    return m


def all_indicators(year: int = YEAR):
    """iso3 -> (display-ish name, indicator dict) for every country in the universe."""
    wb, fp, csv_rows, names = load_universe(year)
    out = {}
    for iso in sorted(names):
        ind, _tier = assemble(iso, names[iso], wb, fp, csv_rows, year)
        if ind:
            out[iso] = (DISPLAY_FIX.get(names[iso], names[iso]), ind)
    return out


def indicators_for(name_or_iso: str, year: int = YEAR):
    """Full-coverage indicators for any country the site covers (all tiers).

    Accepts a raw source name, a display name (e.g. "DR Congo"), or an iso3.
    Returns the indicator dict, or None if the country is not in the universe.
    """
    wb, fp, csv_rows, names = load_universe(year)
    key = str(name_or_iso).strip()
    iso = _resolver(names).get(key.upper()) or _resolver(names).get(key.lower())
    if iso is None:
        iso = ds.country_to_iso(key)  # last resort
    if iso is None or iso not in names:
        return None
    ind, _tier = assemble(iso, names[iso], wb, fp, csv_rows, year)
    return ind or None
