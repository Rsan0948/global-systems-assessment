"""
Modernization Index — Scoring Engine

Core calculation logic for scoring countries across five pillars.
Deterministic: given same inputs, always produces same outputs.
"""

import math
import json
from pathlib import Path
from typing import Optional
from mi.constants import (WEIGHTS, WEIGHTS_ARCHIVED_HAND_V0, WEIGHTS_EQUAL, TIERS, LENS,
                          WEIGHTS_V2_EQUAL, V2_ERA_LEADER, V2_ELEVATED_WEIGHT, MI_ACTIVE_WEIGHTING)

_PILLARS = ["P1", "P2", "P3", "P4", "P5"]


def _era_for(year) -> str:
    """Bucket a stress-event year to the nearest measured rotation era."""
    try:
        y = int(year)
    except (TypeError, ValueError):
        return "2018"
    return "2012" if y <= 2015 else ("2018" if y <= 2021 else "2024")


def v2_timevarying_weights(event_year):
    """Option B: elevate the era's most-central pillar; split the rest equally."""
    leader = V2_ERA_LEADER[_era_for(event_year)]
    rest = (1.0 - V2_ELEVATED_WEIGHT) / 4
    return {p: (V2_ELEVATED_WEIGHT if p == leader else rest) for p in _PILLARS}


def resolve_weights(weighting: str = None, event_year=None) -> dict:
    """Resolve the active weighting scheme to a weights dict (the single selector)."""
    mode = weighting or MI_ACTIVE_WEIGHTING
    if mode == "v1":
        return WEIGHTS
    if mode == "timevarying":
        return v2_timevarying_weights(event_year)
    return WEIGHTS_V2_EQUAL  # "equal" (V2 default; equal wins ties)


def normalize_wgi(score: float) -> float:
    """Normalize WGI percentile/anchored score to 0-1."""
    return score / 100.0


def normalize_cpi(score: float) -> float:
    """Normalize CPI score to 0-1."""
    return score / 100.0


def normalize_gii(score: float) -> float:
    """Normalize Global Innovation Index to 0-1."""
    return score / 100.0


def normalize_eci(score: float, dataset_min: float = LENS["eci_default_min"], dataset_max: float = LENS["eci_default_max"]) -> float:
    """Min-max normalize Economic Complexity Index."""
    if dataset_max == dataset_min:
        return 0.5
    # Clamp to [0,1]: an ECI outside the supplied dataset range must not push a
    # pillar score negative or >1 (e.g. DR Congo ECI < dataset_min). Pass the
    # dataset min/max via indicators (eci_dataset_min/max) for cross-dataset consistency.
    norm = (score - dataset_min) / (dataset_max - dataset_min)
    return max(0.0, min(1.0, norm))


def normalize_gdp_ppp(gdp: float, dataset_min_log: float = None, dataset_max_log: float = None) -> float:
    """Log-transform then min-max normalize GDP per capita PPP."""
    if gdp <= 0:
        return 0.0
    log_gdp = math.log(gdp)
    if dataset_min_log is None or dataset_max_log is None:
        # Fixed absolute reference range from the LENS config (~$500 to ~$150,000)
        dataset_min_log = math.log(LENS["gdp_ppp_floor"])
        dataset_max_log = math.log(LENS["gdp_ppp_ceiling"])
    if dataset_max_log == dataset_min_log:
        return 0.5
    return (log_gdp - dataset_min_log) / (dataset_max_log - dataset_min_log)


def normalize_resource_rents(rents_pct: float) -> float:
    """Invert resource rents: lower dependence = higher score."""
    return 1.0 - min(rents_pct / LENS["resource_rents_full_dependence_pct"], 1.0)


def normalize_oda(oda_pct: float) -> float:
    """Invert ODA: lower dependence = higher score."""
    return 1.0 - min(oda_pct / LENS["oda_full_dependence_pct"], 1.0)


def normalize_fsi(fsi: float) -> float:
    """Invert FSI: lower fragility = higher score."""
    return 1.0 - (fsi / LENS["fsi_max"])


def calculate_pillar_scores(indicators: dict) -> dict:
    """
    Calculate pillar scores from raw indicator values.

    Args:
        indicators: dict with keys matching indicator names and raw values.
                    Missing values should be None, not omitted.

    Returns:
        dict with pillar scores (P1-P5), each 0-1 scale.
        Also includes metadata about which indicators were available.
    """
    result = {}
    gaps = []

    # P1 — Institutional Quality
    p1_values = []
    for key in ["gov_effectiveness", "rule_of_law", "regulatory_quality"]:
        val = indicators.get(key)
        if val is not None:
            p1_values.append(normalize_wgi(val))
        else:
            gaps.append(f"P1:{key}")

    # CPI or WGI Control of Corruption
    cpi = indicators.get("cpi")
    coc = indicators.get("control_of_corruption")
    if cpi is not None:
        p1_values.append(normalize_cpi(cpi))
    elif coc is not None:
        p1_values.append(normalize_wgi(coc))
    else:
        gaps.append("P1:corruption_control")

    result["P1"] = sum(p1_values) / len(p1_values) if p1_values else None

    # P2 — Innovation & Knowledge Economy
    p2_values = []
    gii = indicators.get("gii")
    rd = indicators.get("rd_pct_gdp")
    if gii is not None:
        p2_values.append(normalize_gii(gii))
    elif rd is not None:
        # Track 2 proxy — normalize R&D as proportion (typical range 0-5%)
        p2_values.append(min(rd / 5.0, 1.0))
    else:
        gaps.append("P2:innovation_index")

    eci = indicators.get("eci")
    eci_min = indicators.get("eci_dataset_min", LENS["eci_default_min"])
    eci_max = indicators.get("eci_dataset_max", LENS["eci_default_max"])
    if eci is not None:
        p2_values.append(normalize_eci(eci, eci_min, eci_max))
    else:
        gaps.append("P2:economic_complexity")

    result["P2"] = sum(p2_values) / len(p2_values) if p2_values else None

    # P3 — Human Capital
    p3_values = []
    for key in ["education_index", "life_expectancy_index"]:
        val = indicators.get(key)
        if val is not None:
            p3_values.append(val)  # Already 0-1
        else:
            gaps.append(f"P3:{key}")

    result["P3"] = sum(p3_values) / len(p3_values) if p3_values else None

    # P4 — Economic Structure & Independence
    p4_values = []
    gdp = indicators.get("gdp_per_capita_ppp")
    if gdp is not None:
        p4_values.append(normalize_gdp_ppp(gdp))
    else:
        gaps.append("P4:gdp_per_capita_ppp")

    rents = indicators.get("resource_rents_pct_gdp")
    if rents is not None:
        p4_values.append(normalize_resource_rents(rents))
    else:
        gaps.append("P4:resource_rents")

    oda = indicators.get("oda_pct_gni")
    if oda is not None:
        p4_values.append(normalize_oda(oda))
    else:
        gaps.append("P4:oda")

    result["P4"] = sum(p4_values) / len(p4_values) if p4_values else None

    # P5 — Stability & Resilience
    p5_values = []
    pol_stab = indicators.get("political_stability")
    if pol_stab is not None:
        p5_values.append(normalize_wgi(pol_stab))
    else:
        gaps.append("P5:political_stability")

    fsi = indicators.get("fsi")
    if fsi is not None:
        p5_values.append(normalize_fsi(fsi))
    else:
        gaps.append("P5:fsi")

    result["P5"] = sum(p5_values) / len(p5_values) if p5_values else None

    result["gaps"] = gaps
    return result


def calculate_mi_score(pillar_scores: dict, weights: dict = None) -> Optional[float]:
    """
    Calculate composite MI score from pillar scores.

    Args:
        pillar_scores: dict with P1-P5 values (0-1 each)
        weights: weight dict (defaults to the active V2 weighting; pass explicitly to override)

    Returns:
        Weighted composite score, or None if insufficient pillars available.
    """
    if weights is None:
        weights = resolve_weights()

    available = {k: v for k, v in pillar_scores.items()
                 if k in weights and v is not None}

    if len(available) < LENS["min_pillars_for_mi"]:  # need enough pillars for a meaningful score
        return None

    # Weight and normalize by available weights
    total_weight = sum(weights[k] for k in available)
    score = sum(available[k] * weights[k] for k in available) / total_weight

    return score


def calculate_pillar_spread(pillar_scores: dict) -> Optional[float]:
    """Calculate spread between highest and lowest pillar scores."""
    values = [v for k, v in pillar_scores.items()
              if k.startswith("P") and v is not None]
    if len(values) < 2:
        return None
    return max(values) - min(values)


def get_configuration_profile(pillar_scores: dict) -> list:
    """
    Get pillars ranked from strongest to weakest.

    Returns:
        List of (pillar_name, score) tuples, sorted descending.
    """
    scored = [(k, v) for k, v in pillar_scores.items()
              if k.startswith("P") and v is not None]
    return sorted(scored, key=lambda x: x[1], reverse=True)


def get_tier(mi_score: float) -> dict:
    """Determine which tier a country falls into based on MI score."""
    for tier_num in sorted(TIERS.keys()):
        if mi_score >= TIERS[tier_num]["m_score_min"]:
            return {"tier": tier_num, "name": TIERS[tier_num]["name"]}
    # Below all thresholds
    return {"tier": 6, "name": "Below Floor"}


def score_country(indicators: dict, weights: dict = None, event_year=None) -> dict:
    """
    Full scoring pipeline for a single country at a single time point.

    Args:
        indicators: dict of raw indicator values
        weights: optional explicit weight override
        event_year: stress-event year (used only by the time-varying weighting)

    Returns:
        Complete diagnostic output including pillars, MI score, spread,
        configuration, tier, and data gaps.
    """
    pillars = calculate_pillar_scores(indicators)
    eff_weights = weights if weights is not None else resolve_weights(event_year=event_year)
    mi_score = calculate_mi_score(pillars, eff_weights)
    spread = calculate_pillar_spread(pillars)
    config = get_configuration_profile(pillars)

    result = {
        "pillar_scores": {k: v for k, v in pillars.items() if k.startswith("P")},
        "mi_score": mi_score,
        "pillar_spread": spread,
        "configuration": config,
        "tier": get_tier(mi_score) if mi_score is not None else None,
        "data_gaps": pillars.get("gaps", []),
        "weights_used": eff_weights,
        "weighting_mode": MI_ACTIVE_WEIGHTING if weights is None else "explicit",
    }

    # Sensitivity across all weighting schemes (active V2 + the alternatives + frozen V1).
    if weights is None:
        result["sensitivity"] = {
            "v2_equal": calculate_mi_score(pillars, WEIGHTS_V2_EQUAL),
            "v2_timevarying": calculate_mi_score(pillars, v2_timevarying_weights(event_year)),
            "v1": calculate_mi_score(pillars, WEIGHTS),
            "archived_hand_v0": calculate_mi_score(pillars, WEIGHTS_ARCHIVED_HAND_V0),
        }

    return result


def load_country_data(country_name: str, year: int = None) -> Optional[dict]:
    """Load country indicator data via the internal Data API (single source).

    Indicators are assembled live from the canonical sources (mi.datasource);
    there are no per-country copy files to keep in sync. Falls back to a legacy
    data/countries/<name>.json only if the Data API has nothing for that country.
    """
    from mi import datasource  # lazy import to avoid any import cycle

    if year is not None:
        ind = datasource.get_indicators(country_name, year, with_meta=True)
        if ind is not None:
            return ind
    else:
        years = datasource.available_years(country_name)
        if years:
            return {
                "country": country_name,
                "iso3": datasource.country_to_iso(country_name),
                "indicators_by_year": {
                    y: datasource.get_indicators(country_name, y, with_meta=True) for y in years
                },
            }

    # Legacy fallback: a static country file (deprecated; the Data API is canonical)
    filepath = Path(__file__).parent.parent / "data" / "countries" / (
        country_name.lower().replace(" ", "_") + ".json")
    if not filepath.exists():
        return None
    with open(filepath) as f:
        data = json.load(f)
    if year is not None:
        return data.get("indicators_by_year", {}).get(str(year))
    return data
