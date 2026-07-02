"""
Hydrate case-study entity indicators from the world panel (data/countries/*.json).

Fills ONLY null indicator slots on each case entity, from the World-Bank-sourced
world panel at the case's pre-event year (or nearest available year within +-3).
Existing non-null values (hand curation + prior scale corrections) are preserved.
Every fill is recorded in an `_hydrated_from_world` provenance block on the entity.

Two cases (18, 19) are "current comparative trajectory" studies whose own notes
use 2024-endpoint WGI, so their fill-year is pinned to 2024 for vintage
consistency across their entities.

Run: python scripts/hydrate_cases_from_world.py
"""

from __future__ import annotations

import glob
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COUNTRIES = ROOT / "data" / "countries"
CASES = ROOT / "data" / "case_studies" / "completed"

# case entity name -> world country-file slug. Historical/sub-national entities
# map to their modern sovereign; defunct/pre-WGI entities map to None (skip).
ALIAS = {
    "Estonia": "estonia", "Russia": "russian_federation", "Ukraine": "ukraine",
    "Slovenia": "slovenia", "Croatia": "croatia", "Serbia": "serbia",
    "Bosnia-Herzegovina": "bosnia_and_herzegovina", "Czech Republic": "czechia",
    "Slovakia": "slovak_republic", "Tunisia": "tunisia", "Egypt": "egypt_arab_rep",
    "Libya": "libya", "Sudan": "sudan", "South Sudan": "south_sudan",
    "Pakistan": "pakistan", "Bangladesh": "bangladesh", "Singapore": "singapore",
    "Malaysia": "malaysia", "Ethiopia": "ethiopia", "Eritrea": "eritrea",
    "Serbia ": "serbia", "Kosovo": "kosovo", "Indonesia": "indonesia",
    "East Timor": "timor_leste", "Nigeria": "nigeria", "South Africa": "south_africa",
    "Northern Ireland (UK)": "united_kingdom", "Germany": "germany",
    "Spain (Catalonia)": "spain", "Belgium": "belgium", "Latvia": "latvia",
    "Kazakhstan": "kazakhstan", "Uzbekistan": "uzbekistan", "India": "india",
    "Myanmar": "myanmar", "Haiti": "haiti", "Dominican Republic": "dominican_republic",
    "Venezuela": "venezuela", "Colombia": "colombia", "DR Congo": "dr_congo",
    "Rwanda": "rwanda",
}

YEAR_OVERRIDE = {"case18": 2024, "case19": 2024}  # current-comparative endpoint cases

INDICATORS = ["gov_effectiveness", "rule_of_law", "regulatory_quality",
              "control_of_corruption", "political_stability", "voice_accountability",
              "gdp_per_capita_ppp", "resource_rents_pct_gdp", "oda_pct_gni",
              "rd_pct_gdp", "education_index", "life_expectancy_index",
              "cpi", "eci", "fsi"]


def build_index():
    """slug (filename stem) -> loaded country dict; also index modern iso3 names."""
    idx = {}
    for p in glob.glob(str(COUNTRIES / "*.json")):
        idx[Path(p).stem] = json.loads(Path(p).read_text())
    return idx


def nearest_year(iby: dict, target: int) -> str | None:
    if not iby:
        return None
    yrs = sorted(int(y) for y in iby)
    best = min(yrs, key=lambda y: abs(y - target))
    return str(best) if abs(best - target) <= 3 else None


def parse_tp(tp) -> int | None:
    if tp is None:
        return None
    s = str(tp)
    for tok in s.replace("/", " ").split():
        if tok.isdigit() and len(tok) == 4:
            return int(tok)
    return None


def main():
    idx = build_index()
    filled_cells = 0
    skipped = []
    for f in sorted(glob.glob(str(CASES / "case*.json"))):
        d = json.loads(Path(f).read_text())
        case_id = os.path.basename(f).split("_")[0]
        tp = YEAR_OVERRIDE.get(case_id) or parse_tp(d.get("pre_event", {}).get("time_point"))
        if tp is None:
            continue
        changed = False
        for name, ent in d.get("pre_event", {}).get("entities", {}).items():
            slug = ALIAS.get(name)
            if slug is None or slug not in idx:
                skipped.append(f"{case_id}/{name} (no country file)")
                continue
            iby = idx[slug].get("indicators_by_year", {})
            y = nearest_year(iby, tp)
            if y is None:
                skipped.append(f"{case_id}/{name} (no data near {tp})")
                continue
            src = iby[y]
            ind = ent.setdefault("indicators", {})
            prov = []
            for k in INDICATORS:
                if ind.get(k) is None and src.get(k) is not None:
                    ind[k] = src[k]
                    prov.append({"indicator": k, "value": src[k]})
            if prov:
                ent.setdefault("_hydrated_from_world", {"source_slug": slug,
                    "source_year": y, "target_year": tp,
                    "note": "null slots filled from World Bank / HDR world panel",
                    "filled": []})["filled"].extend(prov)
                filled_cells += len(prov)
                changed = True
        if changed:
            Path(f).write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
    print(f"filled {filled_cells} null cells across cases")
    if skipped:
        print("\nskipped (reported honestly):")
        for s in skipped:
            print("  -", s)


if __name__ == "__main__":
    main()
