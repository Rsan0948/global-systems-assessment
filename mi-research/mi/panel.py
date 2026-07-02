"""
Runtime reader for the canonical MI indicator panel — the single data store.

The engine (`scoring.load_country_data`), the CLIs, and `build_site_dataset`
read country indicators from ONE file: `data/sources/canonical_panel.json`,
built by `scripts/build_canonical_panel.py` (which resolves the source tiers
A>B>C once, at build time). This module is that single read path — no live
multi-source stitching. `DISPLAY_FIX` (raw source name -> readable name) lives
here because both this reader and the builder need it.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "data" / "sources" / "canonical_panel.json"
YEAR = 2024

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

_CANON = None
_RESOLVER = None


def _canonical():
    global _CANON
    if _CANON is None:
        with open(CANONICAL) as f:
            _CANON = json.load(f)["countries"]
    return _CANON


def _resolve_iso(name_or_iso):
    """name / display name / iso3 (case-insensitive) -> iso3, or None."""
    global _RESOLVER
    if _RESOLVER is None:
        m = {}
        for iso, rec in _canonical().items():
            m[iso.upper()] = iso
            m[rec["name"].lower()] = iso
            m[rec.get("display", rec["name"]).lower()] = iso
        _RESOLVER = m
    key = str(name_or_iso).strip()
    return _RESOLVER.get(key.upper()) or _RESOLVER.get(key.lower())


def indicators_for(name_or_iso: str, year: int = YEAR):
    """Indicators for any country in the canonical panel; None if absent.

    Accepts a raw source name, a display name (e.g. "DR Congo"), or an iso3.
    """
    iso = _resolve_iso(name_or_iso)
    if iso is None:
        return None
    return _canonical()[iso]["indicators_by_year"].get(str(year)) or None


def country_record(name_or_iso: str):
    """Full canonical entry {country, iso3, indicators_by_year}, or None."""
    iso = _resolve_iso(name_or_iso)
    if iso is None:
        return None
    rec = _canonical()[iso]
    return {"country": rec["name"], "iso3": iso,
            "indicators_by_year": rec["indicators_by_year"]}


def all_indicators(year: int = YEAR):
    """iso3 -> (display name, indicator dict) for countries with data at `year`."""
    out = {}
    for iso, rec in _canonical().items():
        ind = rec["indicators_by_year"].get(str(year))
        if ind:
            out[iso] = (rec.get("display", rec["name"]), ind)
    return out


def iter_universe(year: int = YEAR):
    """Yield (iso, raw_name, display_name, indicators, source_tier) for build_site_dataset."""
    for iso in sorted(_canonical()):
        rec = _canonical()[iso]
        ind = rec["indicators_by_year"].get(str(year))
        if ind:
            yield iso, rec["name"], rec.get("display", rec["name"]), ind, rec.get("source_tier")
