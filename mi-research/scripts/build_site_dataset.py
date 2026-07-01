#!/usr/bin/env python3
"""
Build the published dataset the website consumes - the engine, run in public, over ALL available data.

Coverage tiers (every country gets a page; gaps are shown, never faked):
  A. wb_anchored (full indicators)        -> canonical via datasource.get_indicators
  B. mi_pipeline panel (full indicators)  -> assembled by iso3 (P1/P2/P3) + wgi_full_panel (gdp/PV/rents)
  C. wgi_full_panel only (WGI institutions + gdp) -> partial pillars, gaps shown
The validated mi-research engine (score_country) is the single source of truth; this script only
ASSEMBLES inputs and calls it. Deterministic.

Emits to web/public/data: countries.json, country/<slug>.json, meta.json
"""
import csv
import json
import math
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mi import datasource as ds
from mi.scoring import (score_country, get_tier, get_configuration_profile,
                        calculate_pillar_spread)
from mi.diagnostics import structural_vulnerability, below_floor_diagnostic, ascent_potential

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "sources"
CSV_PATH = ROOT.parent / "mi_pipeline" / "output" / "mi_scored_countries.csv"
OUT = ROOT.parent / "mi-website" / "web" / "public" / "data"
YEAR = 2024

PILLAR_NAMES = {"P1": "Institutions", "P2": "Economic Complexity", "P3": "Human Capital",
                "P4": "Economic Structure", "P5": "Stability & Resilience"}
TIER_LABEL = {1: "Highly Modernized", 2: "Durable", 3: "Mixed", 4: "Fragile", 5: "Floor"}
INDICATOR_SOURCES = {
    "gov_effectiveness": "World Bank WGI", "rule_of_law": "World Bank WGI",
    "regulatory_quality": "World Bank WGI", "control_of_corruption": "World Bank WGI",
    "voice_accountability": "World Bank WGI", "political_stability": "World Bank WGI",
    "cpi": "Transparency International", "gii": "WIPO Global Innovation Index",
    "rd_pct_gdp": "World Bank WDI", "eci": "Harvard Atlas (ECI)",
    "education_index": "UNDP HDR", "life_expectancy_index": "UNDP HDR",
    "gdp_per_capita_ppp": "World Bank WDI", "resource_rents_pct_gdp": "World Bank WDI",
    "oda_pct_gni": "World Bank WDI", "fsi": "Fund for Peace FSI",
}
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


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


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


def load_universe():
    wb = json.load(open(SRC / "wb_anchored.json"))
    fp = json.load(open(SRC / "wgi_full_panel.json"))
    vd = json.load(open(SRC / "vdem_longrun.json"))
    csv_rows = {}  # iso3 -> latest-year row (prefer Track 1)
    for r in csv.DictReader(open(CSV_PATH)):
        if int(r["year"]) != YEAR:
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


def assemble(iso, name, wb, fp, csv_rows):
    """Return (indicators, tier_label) using the best available source. wb countries use the canonical API."""
    if name in wb:
        ind = ds.get_indicators(name, YEAR)
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
            v = _panel_yr(panel, col)
            if v is not None:
                ind[key] = v
    # shared from wgi_full_panel: gdp / political stability / voice / rents
    for key, col in [("gdp_per_capita_ppp", "gdp"), ("political_stability", "PV"),
                     ("voice_accountability", "VA"), ("resource_rents_pct_gdp", "rents")]:
        v = _panel_yr(panel, col)
        if v is not None and key not in ind:
            ind[key] = v
    return ind, ("B" if r else "C")


def chips_for(ind, tier, residual, spread, weakest, present):
    chips = [{"key": "tier", "label": f"Tier {tier}: {TIER_LABEL.get(tier,'')}",
              "valence": "good" if tier <= 2 else "warn" if tier == 3 else "bad",
              "why": "Modernization Index band (equal-weighted pillars).", "rule": "MI score binned into 5 tiers."}]
    if present < 5:
        chips.append({"key": "partial", "label": f"Partial data · {present}/5 pillars", "valence": "neutral",
                      "why": ("Scored on the pillars we have data for. Its score is not directly comparable "
                              "to a fully-measured country - the missing pillars are unmeasured, not zero."),
                      "rule": f"{5 - present} of 5 pillars lack public data."})
    if residual is not None:
        granted = residual < -0.03
        chips.append({"key": "durability", "label": "Granted prosperity" if granted else "Earned prosperity",
                      "valence": "bad" if granted else "good",
                      "why": ("Wealth has outrun institutions - historically fragile." if granted
                              else "Institutions roughly match or exceed what income predicts - durable."),
                      "rule": "MI residual vs. the log-GDP regression (the durability gap): below -0.03 → granted, "
                              "otherwise earned (a ±0.03 tolerance treats near-zero gaps as in-line)."})
    if spread is not None:
        shape = "Balanced" if spread < 0.15 else "Some imbalance" if spread < 0.35 else "Lopsided"
        chips.append({"key": "shape", "label": f"{shape} · weakest: {PILLAR_NAMES.get(weakest, weakest)}",
                      "valence": "good" if spread < 0.15 else "warn" if spread < 0.35 else "bad",
                      "why": "Spread between the strongest and weakest pillar - the country's structural shape.",
                      "rule": "max(pillar) - min(pillar)."})
    rents = ind.get("resource_rents_pct_gdp")
    if rents is not None and rents >= 10:
        chips.append({"key": "resource", "label": "Resource-dependent", "valence": "warn",
                      "why": f"Resource rents ≈ {rents:.0f}% of GDP - prosperity leans on extraction.",
                      "rule": "resource rents ≥ 10% of GDP."})
    oda = ind.get("oda_pct_gni")
    if oda is not None and oda >= 5:
        chips.append({"key": "aid", "label": "Aid-dependent", "valence": "warn",
                      "why": f"Official aid ≈ {oda:.0f}% of GNI.", "rule": "ODA ≥ 5% of GNI."})
    return chips


def build_checks(pillars, mi, ind, weakest):
    """The deterministic diagnostic checks the engine runs on every country - the
    'rules firing' you see in a case study, computed from the pillars alone."""
    checks = []
    p1, p4 = pillars.get("P1"), pillars.get("P4")

    # 1. Durability gate (does income outrun institutions?)
    sv = structural_vulnerability(pillars)
    if p1 is not None and p4 is not None and sv:
        st = sv.get("status")
        gap = round(p4 - p1, 2)
        if st == "flagged":
            status, detail = "flag", ("Income has outrun institutions. This is the classic structural fragility "
                                      "signal: wealth the institutions cannot anchor tends not to last.")
        elif st == "borderline":
            status, detail = "info", ("Income runs somewhat ahead of institutions - a gap worth watching, though "
                                      "not yet a clear warning.")
        else:
            status, detail = "clear", "Institutions keep pace with the country's income. No durability warning here."
        checks.append({"key": "durability", "title": "Durability gate", "status": status,
                       "headline": f"income vs institutions {gap:+.2f}", "detail": detail})

    # 2. Configuration (the shape of a failure, when there is one)
    bf = below_floor_diagnostic(pillars, mi)
    if bf and bf.get("reading"):
        detail = (bf.get("reading", "") + " " + bf.get("prescription", "")).replace("—", "-").replace("*", "").strip()
        checks.append({"key": "config", "title": "Configuration", "status": "flag",
                       "headline": bf.get("configuration", "").replace("_", " "), "detail": detail})

    # 3. Weakest link
    if weakest:
        nm = PILLAR_NAMES.get(weakest, weakest)
        checks.append({"key": "weak", "title": "Weakest link", "status": "info",
                       "headline": f"{nm} is lowest",
                       "detail": f"{nm} is the pillar dragging the score down. A chain breaks at its weakest link, "
                                 "so this is where the structural risk concentrates."})

    # 4. Room to rise (low-base eligibility)
    ap = ascent_potential(pillars)
    if ap:
        if ap.get("low_base"):
            checks.append({"key": "ascent", "title": "Room to rise", "status": "info", "headline": "low base",
                           "detail": "Starting from a low institutional base, the country is structurally eligible "
                                     "to climb. This is eligibility, not a forecast - the effect only showed up "
                                     "strongly in the 2000s global growth wave."})
        else:
            checks.append({"key": "ascent", "title": "Room to rise", "status": "info", "headline": "already high",
                           "detail": "The base is already high, so large structural jumps from here are historically rare."})

    # 5. Rentier check (prosperity leaning on extraction)
    rents = ind.get("resource_rents_pct_gdp")
    if rents is not None and rents >= 10:
        checks.append({"key": "rentier", "title": "Rentier check", "status": "flag",
                       "headline": f"resource rents ~{rents:.0f}% of GDP",
                       "detail": "A large share of prosperity comes from extracting resources rather than from "
                                 "institutions or a complex economy. Historically this masks structural weakness - "
                                 "the money can vanish with a price swing."})
    return checks


def verdict(tier, residual, spread, weakest):
    parts = [{1: "Highly modernized", 2: "Structurally durable", 3: "Mixed structural profile",
              4: "Structurally fragile", 5: "At the structural floor"}.get(tier, "")]
    if residual is not None:
        parts.append("prosperity outrunning institutions" if residual < -0.03
                     else "prosperity matched by institutions" if residual > 0.03
                     else "prosperity roughly in line with institutions")
    if spread is not None and spread >= 0.35:
        parts.append(f"lopsided ({PILLAR_NAMES.get(weakest, weakest).lower()} the weak point)")
    return " - ".join(p for p in parts if p) + "."


def fit_durability(points):
    """OLS MI ~ a + b*ln(gdp) across all scored countries -> residual per country."""
    xs = [math.log(g) for _, m, g in points if g and g > 0]
    ys = [m for _, m, g in points if g and g > 0]
    n = len(xs)
    if n < 5:
        return {}
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx if sxx else 0
    a = my - b * mx
    out = {}
    for iso, m, g in points:
        if g and g > 0:
            out[iso] = m - (a + b * math.log(g))
    return out


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "country").mkdir(exist_ok=True)
    wb, fp, csv_rows, names = load_universe()
    iso_universe = set(names) & (set(fp) | {v["iso3"] for v in wb.values() if v.get("iso3")} | set(csv_rows))

    scored = []  # (iso, name, ind, pillars, mi, tier, source)
    points = []
    for iso in iso_universe:
        name = names.get(iso)
        if not name:
            continue
        ind, source = assemble(iso, name, wb, fp, csv_rows)
        if not ind:
            continue
        s = score_country(ind, event_year=YEAR)
        mi = s["mi_score"]
        if mi is None:
            continue
        pillars = s["pillar_scores"]
        scored.append((iso, name, ind, pillars, mi, get_tier(mi)["tier"], source))
        points.append((iso, mi, ind.get("gdp_per_capita_ppp")))

    residuals = fit_durability(points)

    summaries = []
    for iso, name, ind, pillars, mi, tier, source in scored:
        spread = calculate_pillar_spread(pillars)
        config = get_configuration_profile(pillars)
        weakest = config[-1][0] if config else None
        residual = residuals.get(iso)
        present = [p for p in ["P1", "P2", "P3", "P4", "P5"] if pillars.get(p) is not None]
        missing = [p for p in ["P1", "P2", "P3", "P4", "P5"] if pillars.get(p) is None]
        chips = chips_for(ind, tier, residual, spread, weakest, len(present))
        display = DISPLAY_FIX.get(name, name)  # readable name for the site; `name` stays the data key
        slug = slugify(display)
        summary = {
            "slug": slug, "name": display, "iso3": iso, "mi": round(mi, 3), "tier": tier,
            "pillars": {p: (round(pillars[p], 3) if pillars.get(p) is not None else None)
                        for p in ["P1", "P2", "P3", "P4", "P5"]},
            "chips": chips, "coverage": {"present": len(present), "total": 5, "missing": missing},
        }
        summaries.append(summary)
        indicators = [{"key": k, "value": v, "source": INDICATOR_SOURCES.get(k, "-")}
                      for k, v in ind.items()
                      if not (k.endswith("_min") or k.endswith("_max")) and v is not None]
        full = dict(summary)
        full.update({
            "verdict": verdict(tier, residual, spread, weakest),
            "spread": round(spread, 3) if spread is not None else None,
            "residual": round(residual, 3) if residual is not None else None,
            "config": [[p, round(v, 3)] for p, v in config],
            "pillar_names": PILLAR_NAMES, "indicators": indicators, "data_year": YEAR,
            "source_tier": source, "checks": build_checks(pillars, mi, ind, weakest),
        })
        json.dump(full, open(OUT / "country" / f"{slug}.json", "w"), indent=1)

    # full-coverage countries first (comparable), then partial - each by MI desc
    summaries.sort(key=lambda r: (r["coverage"]["present"] == 5, r["mi"]), reverse=True)
    json.dump(summaries, open(OUT / "countries.json", "w"), indent=1)
    json.dump({"built": date.today().isoformat(), "count": len(summaries), "engine": "MI v3.3",
               "data_vintage": "WGI 2025-anchored", "world_states": 195,
               "note": "Generated by the validated mi-research engine over all available public data. "
                       "Countries with partial data show fewer pillars - gaps are shown, never faked."},
              open(OUT / "meta.json", "w"), indent=1)
    full5 = sum(1 for s in summaries if s["coverage"]["present"] == 5)
    print(f"Wrote {len(summaries)} countries ({full5} with all 5 pillars) -> {OUT}")


if __name__ == "__main__":
    build()
