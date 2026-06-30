#!/usr/bin/env python3
"""
Build the published dataset the website consumes — the engine, run in public.

Runs the validated MI engine over every scoreable country and emits:
  web/public/data/countries.json        — summary array (index + map)
  web/public/data/country/<slug>.json   — full per-country record
  web/public/data/meta.json             — build metadata

The website is a PURE CONSUMER of this output. No scoring math lives in JS.
Deterministic: same engine + same data -> same JSON.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mi import datasource as ds
from mi.scoring import (score_country, get_tier, get_configuration_profile,
                        calculate_pillar_spread)
from mi.durability import durability_ratio

OUT = Path(__file__).resolve().parent.parent.parent / "mi-website" / "web" / "public" / "data"
YEAR = 2024

PILLAR_NAMES = {
    "P1": "Institutions", "P2": "Economic Complexity", "P3": "Human Capital",
    "P4": "Economic Structure", "P5": "Stability & Resilience",
}
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


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def all_countries():
    data, _, _ = ds._wb()
    return data


def chips_for(name, pillars, mi, tier, ind, residual, spread, weakest):
    """The classifier fingerprint — every chip the engine can set deterministically from the data."""
    chips = []
    chips.append({"key": "tier", "label": f"Tier {tier}: {TIER_LABEL.get(tier,'')}",
                  "valence": "good" if tier <= 2 else "warn" if tier == 3 else "bad",
                  "why": "Modernization Index band (equal-weighted pillars).",
                  "rule": "MI score binned into 5 tiers."})
    if residual is not None:
        granted = residual < -0.03
        chips.append({"key": "durability",
                      "label": "Granted prosperity" if granted else "Earned prosperity",
                      "valence": "bad" if granted else "good",
                      "why": ("Wealth has outrun institutions — historically fragile." if granted
                              else "Institutions match or exceed what income predicts — durable."),
                      "rule": "Sign of MI residual vs. log-GDP regression (the durability gap)."})
    if spread is not None:
        shape = ("Balanced" if spread < 0.15 else "Some imbalance" if spread < 0.35 else "Lopsided")
        chips.append({"key": "shape", "label": f"{shape} · weakest: {PILLAR_NAMES.get(weakest, weakest)}",
                      "valence": "good" if spread < 0.15 else "warn" if spread < 0.35 else "bad",
                      "why": "Spread between strongest and weakest pillar; the country's structural shape.",
                      "rule": "max(pillar) − min(pillar)."})
    rents = ind.get("resource_rents_pct_gdp")
    if rents is not None and rents >= 10:
        chips.append({"key": "resource", "label": "Resource-dependent", "valence": "warn",
                      "why": f"Resource rents ≈ {rents:.0f}% of GDP — prosperity leans on extraction.",
                      "rule": "resource rents ≥ 10% of GDP."})
    oda = ind.get("oda_pct_gni")
    if oda is not None and oda >= 5:
        chips.append({"key": "aid", "label": "Aid-dependent", "valence": "warn",
                      "why": f"Official aid ≈ {oda:.0f}% of GNI.", "rule": "ODA ≥ 5% of GNI."})
    return chips


def verdict(tier, residual, spread, weakest):
    parts = []
    parts.append({1: "Highly modernized", 2: "Structurally durable", 3: "Mixed structural profile",
                  4: "Structurally fragile", 5: "At the structural floor"}.get(tier, ""))
    if residual is not None:
        parts.append("prosperity outrunning institutions" if residual < -0.03
                     else "prosperity matched by institutions" if residual > 0.03 else "prosperity roughly in line with institutions")
    if spread is not None and spread >= 0.35:
        parts.append(f"lopsided ({PILLAR_NAMES.get(weakest, weakest).lower()} the weak point)")
    return " — ".join(p for p in parts if p) + "."


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "country").mkdir(exist_ok=True)
    summaries = []
    wb = all_countries()
    for name, meta in wb.items():
        ind = ds.get_indicators(name, YEAR)
        if not ind:
            continue
        s = score_country(ind, event_year=YEAR)
        pillars = s["pillar_scores"]
        mi = s["mi_score"]
        if mi is None:
            continue
        tier = get_tier(mi)["tier"]
        spread = calculate_pillar_spread(pillars)
        config = get_configuration_profile(pillars)
        weakest = config[-1][0] if config else None
        try:
            d = durability_ratio(name, YEAR)
            residual = d.get("residual") if isinstance(d, dict) else None
        except Exception:
            residual = None
        present = [p for p in ["P1", "P2", "P3", "P4", "P5"] if pillars.get(p) is not None]
        missing = [p for p in ["P1", "P2", "P3", "P4", "P5"] if pillars.get(p) is None]
        chips = chips_for(name, pillars, mi, tier, ind, residual, spread, weakest)

        slug = slugify(name)
        summary = {
            "slug": slug, "name": name, "iso3": meta.get("iso3"),
            "mi": round(mi, 3), "tier": tier,
            "pillars": {p: (round(pillars[p], 3) if pillars.get(p) is not None else None)
                        for p in ["P1", "P2", "P3", "P4", "P5"]},
            "chips": chips, "coverage": {"present": len(present), "total": 5, "missing": missing},
        }
        summaries.append(summary)

        indicators = []
        for k, v in ind.items():
            if k.endswith("_min") or k.endswith("_max") or v is None:
                continue
            indicators.append({"key": k, "value": v, "source": INDICATOR_SOURCES.get(k, "—")})
        full = dict(summary)
        full.update({
            "verdict": verdict(tier, residual, spread, weakest),
            "spread": round(spread, 3) if spread is not None else None,
            "residual": round(residual, 3) if residual is not None else None,
            "config": [[p, round(v, 3)] for p, v in config],
            "pillar_names": PILLAR_NAMES,
            "indicators": indicators,
            "data_year": YEAR,
        })
        json.dump(full, open(OUT / "country" / f"{slug}.json", "w"), indent=1)

    summaries.sort(key=lambda r: r["mi"], reverse=True)
    json.dump(summaries, open(OUT / "countries.json", "w"), indent=1)
    json.dump({"built": date.today().isoformat(), "count": len(summaries),
               "engine": "MI v3.3", "data_vintage": "WGI 2025-anchored",
               "note": "Generated by the validated mi-research engine. World total ~195 states; the "
                       "rest are not yet scored (data coverage) — shown dark, not graded."},
              open(OUT / "meta.json", "w"), indent=1)
    print(f"Wrote {len(summaries)} countries -> {OUT}")


if __name__ == "__main__":
    build()
