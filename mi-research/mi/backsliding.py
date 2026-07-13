"""Backsliding-risk diagnostic (v0.1) — ADDITIVE to MI v3.3.

Productizes the two robust, out-of-sample-validated findings about democratic
backsliding from the 2026-07 predictive-reach research sprint
(see repo `sandbox/tier_stress/FINAL_REPORT.md`):

  1. NONLINEAR capacity -> the master signal. Backsliding risk vs rule-of-law
     capacity is an INVERTED-U: highest at MID capacity (partially-institutionalised
     / hybrid states) and low at both extremes. A capacity SAFETY CEILING near the
     80th percentile: above it, backsliding is rare (that single feature reached
     out-of-sample AUC 0.73; the full nonlinear model 0.74 — the strongest, cleanest
     signal found across ~40 analyses and 200 years).
  2. RELATIONAL (secondary) -> capacity relative to civic voice/mobilisation. The
     research used V-Dem civil-society participation (NOT in the canonical panel);
     here proxied by rule_of_law vs voice_accountability, both from the canonical
     panel. Flagged as a proxy.

INVARIANTS: this module does NOT alter pillar scoring, MI weights, tiers, or
safeguards. It reads ONLY through `mi.panel` (the single canonical source). It
reports risk given structural position; it makes NO claim of calibrated
probabilities or timing (backsliding triggers are unpredictable — "the Mule").
"""
from __future__ import annotations
from typing import Optional
from statistics import mean, pstdev
from mi import panel as _panel

# Empirical 5y backsliding hazard by capacity DECILE (rule-of-law percentile), from the
# deep panel 1900-2015 (Angle 6, `sandbox/tier_stress/deep_time`/`angle6_nonlinear`). The
# inverted-U: peak at mid-capacity, low at both ends. Fractions (per country-year at risk).
EMPIRICAL_HAZARD_BY_DECILE = (0.023, 0.018, 0.043, 0.069, 0.102,
                              0.092, 0.089, 0.087, 0.053, 0.038)
SAFETY_CEILING_PCTL = 0.80      # above this rule-of-law percentile, backsliding is rare
DANGER_LO, DANGER_HI = 0.35, 0.65   # the mid-capacity peak-risk band (hybrid/anocratic)
CAPACITY_INDICATOR = "rule_of_law"
MOBILISATION_PROXY = "voice_accountability"   # proxy for civil-society mobilisation (flagged)

_UNIVERSE_CACHE: dict = {}


def _universe(year: int, indicator: str) -> dict:
    """iso3 -> indicator value across the scored universe at `year` (single source)."""
    key = (year, indicator)
    if key not in _UNIVERSE_CACHE:
        out = {}
        for iso, _raw, _disp, ind, _tier in _panel.iter_universe(year):
            v = ind.get(indicator)
            if isinstance(v, (int, float)):
                out[iso] = float(v)
        _UNIVERSE_CACHE[key] = out
    return _UNIVERSE_CACHE[key]


def _percentile(value: float, pool: list) -> float:
    if not pool:
        return None
    return sum(1 for p in pool if p <= value) / len(pool)


def _zscore(value: float, pool: list) -> Optional[float]:
    if len(pool) < 10:
        return None
    mu = mean(pool)
    sd = pstdev(pool) or 1.0
    return (value - mu) / sd


def _hazard_from_percentile(p: float) -> float:
    """Interpolate the empirical inverted-U hazard curve at capacity percentile p in [0,1]."""
    x = min(max(p, 0.0), 1.0) * 10 - 0.5           # decile-centre coordinate
    lo = int(max(0, min(9, x // 1)))
    hi = min(9, lo + 1)
    frac = max(0.0, min(1.0, x - lo))
    return EMPIRICAL_HAZARD_BY_DECILE[lo] * (1 - frac) + EMPIRICAL_HAZARD_BY_DECILE[hi] * frac


def _band(pctl: float, hazard: float) -> str:
    if pctl is None:
        return "unknown"
    if pctl >= SAFETY_CEILING_PCTL:
        return "protected"                          # above the safety ceiling
    if DANGER_LO <= pctl <= DANGER_HI:
        return "danger-zone"                        # mid-capacity hybrid: peak risk
    if hazard >= 0.06:
        return "elevated"
    return "low-base"                               # low capacity: little democratic form to lose


def backsliding_risk(name_or_iso: str, year: int = _panel.YEAR) -> Optional[dict]:
    """Structural backsliding-risk read for a country. Reads only the canonical panel.

    Returns None if the country/indicator is absent. The read is a STRUCTURAL POSITION,
    not a calibrated probability: `backslide_hazard_5y` is the empirical rate for the
    country's capacity decile, `safety_ceiling` is the headline (above 80th pctl = rare),
    `danger_zone` flags the mid-capacity peak, and `relational_capacity_gap` (a proxy)
    is capacity minus civic-voice — positive = institutionalised, negative = mobilisation
    running ahead of capacity (the risk direction).
    """
    ind = _panel.indicators_for(name_or_iso, year)
    if not ind:
        return None
    cap = ind.get(CAPACITY_INDICATOR)
    if not isinstance(cap, (int, float)):
        return None
    cap_pool = list(_universe(year, CAPACITY_INDICATOR).values())
    pctl = _percentile(float(cap), cap_pool)
    hazard = _hazard_from_percentile(pctl) if pctl is not None else None
    band = _band(pctl, hazard) if hazard is not None else "unknown"

    # relational (proxy): capacity vs civic-voice, z-scored within the universe
    rel_gap = None
    mob = ind.get(MOBILISATION_PROXY)
    if isinstance(mob, (int, float)):
        z_cap = _zscore(float(cap), cap_pool)
        z_mob = _zscore(float(mob), list(_universe(year, MOBILISATION_PROXY).values()))
        if z_cap is not None and z_mob is not None:
            rel_gap = round(z_cap - z_mob, 3)

    return {
        "iso3": _panel._resolve_iso(name_or_iso),
        "year": year,
        "capacity_rule_of_law": round(float(cap), 1),
        "capacity_percentile": round(pctl, 3) if pctl is not None else None,
        "backslide_hazard_5y": round(hazard, 3) if hazard is not None else None,
        "safety_ceiling": bool(pctl is not None and pctl >= SAFETY_CEILING_PCTL),
        "danger_zone": bool(pctl is not None and DANGER_LO <= pctl <= DANGER_HI),
        "band": band,
        "relational_capacity_gap": rel_gap,
        "relational_note": "capacity − voice_accountability (z); VA is a proxy for civil-society mobilisation (not in canonical panel)",
        "provenance": "backsliding v0.1; additive to MI v3.3; empirical inverted-U + 80th-pctl safety ceiling from the 2026-07 predictive-reach sprint. Structural position, not a calibrated probability.",
    }


def universe_backsliding(year: int = _panel.YEAR) -> list:
    """Backsliding read for every scored country, sorted safest-first (highest capacity pctl)."""
    rows = [backsliding_risk(iso, year) for iso in _universe(year, CAPACITY_INDICATOR)]
    rows = [r for r in rows if r]
    return sorted(rows, key=lambda r: -(r["capacity_percentile"] or 0))
