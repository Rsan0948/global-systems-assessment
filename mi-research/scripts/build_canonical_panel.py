#!/usr/bin/env python3
"""
Build the ONE canonical indicator panel the engine reads at runtime.

Consolidates the previously-stitched governance sources (wb_anchored +
mi_pipeline panel + wgi_full_panel) plus HDR into a single file,
`data/sources/canonical_panel.json`, with the tier precedence
(A wb_anchored > B mi_pipeline > C wgi_full_panel) resolved HERE, once, at build
time. The runtime (`mi.panel`, the CLIs, build_site_dataset) then reads only this
file — no live multi-source stitching, no coverage-tier logic scattered around.

The raw sources under data/sources/ remain as the ingest inputs for this script
(re-run it when they refresh); they are no longer read at runtime.

Fidelity: per country, the 2024 record is exactly the former runtime merge
(`assemble`, below) and other years are exactly `datasource.get_indicators`, so
re-pointing the runtime at this file leaves every score unchanged.

Run: python scripts/build_canonical_panel.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mi import datasource as ds
from mi.panel import DISPLAY_FIX, YEAR

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "sources"
CSV_PATH = ROOT.parent / "mi_pipeline" / "output" / "mi_scored_countries.csv"
OUT = SRC / "canonical_panel.json"

# --- source-tier ingest (build-time only; the runtime reads the built panel) ---
NAME_FIX = {  # micro-states/territories not named by any source
    "AND": "Andorra", "ATG": "Antigua and Barbuda", "ABW": "Aruba", "BHS": "Bahamas",
    "BMU": "Bermuda", "CYM": "Cayman Islands", "GRL": "Greenland", "KIR": "Kiribati",
    "MAC": "Macao", "MHL": "Marshall Islands", "NRU": "Nauru", "PLW": "Palau",
    "PRI": "Puerto Rico", "SMR": "San Marino", "KNA": "St Kitts and Nevis",
    "VIR": "US Virgin Islands",
}


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _panel_yr(panel_rec, key, yr=YEAR):
    b = panel_rec.get(key)
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
    """Return (indicators, tier_label): A wb_anchored > B mi_pipeline > C wgi_full_panel."""
    if name in wb:
        ind = ds.get_indicators(name, year)
        return (ind or {}), "A"
    panel_rec = fp.get(iso, {})
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
            v = _panel_yr(panel_rec, col, year)
            if v is not None:
                ind[key] = v
    for key, col in [("gdp_per_capita_ppp", "gdp"), ("political_stability", "PV"),
                     ("voice_accountability", "VA"), ("resource_rents_pct_gdp", "rents")]:
        v = _panel_yr(panel_rec, col, year)
        if v is not None and key not in ind:
            ind[key] = v
    return ind, ("B" if r else "C")


def build():
    wb, fp, csv_rows, names = load_universe(YEAR)
    countries = {}
    for iso in sorted(names):
        name = names[iso]
        iby = {}
        # primary year: the full multi-tier merge (A > B > C)
        ind, tier = assemble(iso, name, wb, fp, csv_rows, YEAR)
        if ind:
            iby[str(YEAR)] = ind
        # other years: WGI-anchored series for the curated Data-API countries
        for y in ds.available_years(name):
            if y == str(YEAR):
                continue
            gi = ds.get_indicators(name, int(y))
            if gi:
                iby[y] = gi
        if iby:
            countries[iso] = {
                "iso3": iso,
                "name": name,
                "display": DISPLAY_FIX.get(name, name),
                "source_tier": tier if str(YEAR) in iby else None,
                "indicators_by_year": iby,
            }
    # Dedupe countries that appear under more than one iso code for the same
    # display name (e.g. Kosovo as both OWID_KOS and XKX). Keep the standard
    # 3-letter iso3, merge the alias's year data into it, drop the alias.
    import re as _re
    by_disp = {}
    for iso, rec in countries.items():
        by_disp.setdefault(rec["display"], []).append(iso)
    for disp, isos in by_disp.items():
        if len(isos) < 2:
            continue
        std = sorted(isos, key=lambda i: (bool(_re.fullmatch(r"[A-Z]{3}", i)) is False, i))[0]
        for other in isos:
            if other == std:
                continue
            for y, ind in countries[other]["indicators_by_year"].items():
                countries[std]["indicators_by_year"].setdefault(y, ind)
            del countries[other]

    payload = {
        "meta": {
            "primary_year": YEAR,
            "source": "canonical merge of World Bank WGI/WDI (anchored) + mi_pipeline "
                      "panel (CPI/GII/ECI/R&D/HDR) + wgi_full_panel; tier precedence "
                      "A>B>C resolved at build time",
            "n_countries": len(countries),
        },
        "countries": countries,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n")
    full = sum(1 for c in countries.values()
               if str(YEAR) in c["indicators_by_year"])
    print(f"wrote {OUT} — {len(countries)} countries ({full} with a {YEAR} record)")


if __name__ == "__main__":
    build()
