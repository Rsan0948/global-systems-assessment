"""
The feature-to-pillar loading matrix: the mathematical bridge between
governance structure (15 binary features) and governance capacity (5 MI pillars).

Each entry L[i,j] encodes: "if feature i is present (=1), how much does that
shift the expected score on pillar j?"  Positive = feature predicts higher
pillar score; negative = feature predicts lower score.

The loadings are THEORETICAL — derived from what each feature structurally
implies about governance capacity, not fitted to the MI data.  Validation
against actual MI scores (validate.py) measures how well structure predicts
capacity.

Normalization: raw projected scores are min-max normalized against the range
observed across the 10 governance-type templates, so the output is on [0,1]
comparable to MI pillar scores.
"""

from __future__ import annotations

import numpy as np

PILLAR_NAMES = ["P1", "P2", "P3", "P4", "P5"]
PILLAR_LABELS = {
    "P1": "Institutional Quality",
    "P2": "Innovation & Knowledge",
    "P3": "Human Capital",
    "P4": "Economic Structure",
    "P5": "Stability & Resilience",
}

FEATURE_NAMES = [
    "single_executive",           # 0
    "hereditary_succession",      # 1
    "independent_militaries",     # 2
    "independent_foreign_policy", # 3
    "shared_currency",            # 4
    "shared_legal_code",          # 5
    "unilateral_exit",            # 6
    "central_tax",                # 7
    "popular_sovereignty",        # 8
    "elected_leadership",         # 9
    "free_movement_persons",      # 10
    "free_movement_goods",        # 11
    "shared_supreme_court",       # 12
    "central_standing_army",      # 13
    "preexisting_polities",       # 14
    # --- Institutional depth features (15-18) ---
    "institutional_continuity",   # 15
    "prior_self_governance",      # 16
    "bureaucratic_inheritance",   # 17
    "literacy_at_founding",       # 18
]

N_BASE_FEATURES = 15
N_DEPTH_FEATURES = 4
N_FEATURES = 19
N_PILLARS = 5

# --- The Loading Matrix ---
#
# Rationale for each row (feature → pillar loadings):
#
# 0  single_executive: weak positive on P1 (gov effectiveness via decisive
#    authority) — but V&A can go either way, so net is small.  Slight P5
#    (unified command).
#
# 1  hereditary_succession: negative on P1 (anti-meritocratic, low V&A),
#    negative on P4 (pre-modern economies correlate), slight negative P5
#    (succession crises).
#
# 2  independent_militaries: strongly negative P5 (competing armed forces =
#    violence risk), negative P1 (weak central authority).
#
# 3  independent_foreign_policy: negative P5 (diplomatic fragmentation),
#    negative P4 (trade fragmentation), slight negative P1.
#
# 4  shared_currency: strong positive P4 (market integration, trade), moderate
#    P2 (larger market incentivizes innovation), slight P5 (economic stability).
#
# 5  shared_legal_code: strong positive P1 (rule of law, regulatory quality),
#    moderate P3 (legal protections → human development), moderate P5
#    (institutional stability), slight P4.
#
# 6  unilateral_exit: negative P5 (exit risk, institutional instability),
#    slight negative P1 and P4.
#
# 7  central_tax: moderate P4 (fiscal capacity → economic development),
#    moderate P1 (government effectiveness), slight P5.
#
# 8  popular_sovereignty: strong P1 (voice & accountability), moderate P3
#    (democratic accountability → public goods investment), moderate P2
#    (freedom → innovation).
#
# 9  elected_leadership: strong P1 (V&A, checks on power), moderate P3
#    (responsive governance → human development), slight P2 and P5.
#
# 10 free_movement_persons: moderate P3 (mobility, opportunity, human
#    development), moderate P4 (labor mobility), moderate P2 (brain
#    circulation), slight P1.
#
# 11 free_movement_goods: strong P4 (trade openness — directly measured by MI),
#    moderate P2 (market specialization → innovation).
#
# 12 shared_supreme_court: strong P1 (rule of law, judicial consistency),
#    moderate P3 (rights protections), moderate P5 (dispute resolution).
#
# 13 central_standing_army: strong P5 (monopoly on legitimate violence),
#    slight P1 (state capacity).
#
# 14 preexisting_polities: slight negative P5 (historical cleavages persist
#    as fragility), otherwise near-neutral (it's a historical fact, not a
#    current institutional property).
#
# --- Institutional depth features (15-18) ---
# These capture WHY countries with identical formal structure (e.g. Brazil and
# Switzerland, both federal republics) have vastly different governance quality.
# Form features (0-14) describe WHAT institutions exist.  Depth features
# describe HOW deep those institutions run.
#
# 15 institutional_continuity: 50+ years of unbroken constitutional operation.
#    Strong P5 (stability track record), strong P1 (institutional maturity →
#    government effectiveness), moderate P2 (stable R&D environment), moderate
#    P3 (sustained human development investment), moderate P4 (economic policy
#    continuity).
#
# 16 prior_self_governance: established tradition of self-rule before the
#    current system (the difference between democracy as learned practice vs
#    imported template).  Strong P1 (democratic norms internalized), moderate
#    P2 (culture of initiative), moderate P3 (civic engagement → public goods),
#    slight P4, moderate P5 (legitimate institutions resist shocks).
#
# 17 bureaucratic_inheritance: inherited functioning administrative apparatus
#    (Prussian tradition → Germany, vs colonial extraction → Brazil).  Strong
#    P1 (government effectiveness from day one), moderate P2/P3 (state capacity
#    enables R&D and service delivery), moderate P4 (economic management),
#    moderate P5 (institutional resilience).
#
# 18 literacy_at_founding: near-universal literacy (>90%) at institutional
#    founding.  Gates whether democratic institutions are PRACTICED or NOMINAL.
#    Moderate P1 (informed electorate), strong P2 (human capital → innovation),
#    strong P3 (directly measures human capital base), moderate P4 (productive
#    workforce), slight P5.

LOADING_MATRIX = np.array([
    #  P1    P2    P3    P4    P5
    [ 0.1,  0.0,  0.0,  0.0,  0.1],  # 0:  single_executive
    [-0.5, -0.1, -0.2, -0.3, -0.1],  # 1:  hereditary_succession
    [-0.3,  0.0,  0.0,  0.0, -0.8],  # 2:  independent_militaries
    [-0.2,  0.0,  0.0, -0.3, -0.4],  # 3:  independent_foreign_policy
    [ 0.1,  0.3,  0.1,  0.7,  0.2],  # 4:  shared_currency
    [ 0.8,  0.1,  0.3,  0.2,  0.3],  # 5:  shared_legal_code
    [-0.2,  0.0,  0.0, -0.2, -0.5],  # 6:  unilateral_exit
    [ 0.3,  0.1,  0.1,  0.5,  0.2],  # 7:  central_tax
    [ 0.7,  0.3,  0.5,  0.1,  0.0],  # 8:  popular_sovereignty
    [ 0.7,  0.2,  0.4,  0.1,  0.1],  # 9:  elected_leadership
    [ 0.2,  0.4,  0.5,  0.4,  0.0],  # 10: free_movement_persons
    [ 0.1,  0.3,  0.1,  0.8,  0.1],  # 11: free_movement_goods
    [ 0.8,  0.1,  0.3,  0.1,  0.3],  # 12: shared_supreme_court
    [ 0.1,  0.0,  0.0,  0.0,  0.8],  # 13: central_standing_army
    [ 0.0,  0.0,  0.0,  0.0, -0.2],  # 14: preexisting_polities
    # --- Depth features ---
    [ 0.4,  0.3,  0.2,  0.3,  0.5],  # 15: institutional_continuity
    [ 0.5,  0.3,  0.3,  0.1,  0.3],  # 16: prior_self_governance
    [ 0.4,  0.3,  0.3,  0.4,  0.3],  # 17: bureaucratic_inheritance
    [ 0.2,  0.5,  0.5,  0.3,  0.1],  # 18: literacy_at_founding
], dtype=float)

assert LOADING_MATRIX.shape == (N_FEATURES, N_PILLARS)

# --- Reference type templates (mirrored from feature_vector.py) ---
# Each template now includes 4 depth features (15-18) representing the
# archetype's typical institutional depth:
#   [institutional_continuity, prior_self_governance, bureaucratic_inheritance,
#    literacy_at_founding]

TYPE_TEMPLATES = {
    "personal_empire":       [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    "feudal_order":          [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    "city_state_system":     [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
    "dynastic_composite":    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    "confederation":         [0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0],
    "unitary_nation_state":  [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    "federal_republic":      [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "ideological_party":     [1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    "colonial_imperial":     [1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    "supranational_union":   [0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
}


def _compute_normalization_bounds() -> tuple[np.ndarray, np.ndarray]:
    """Compute per-pillar min/max raw scores across all type templates.

    Using templates (not all 2^15 binary vectors) grounds the normalization
    in actually-observed governance forms rather than theoretical extremes."""
    raw_scores = []
    for template in TYPE_TEMPLATES.values():
        raw = np.array(template, dtype=float) @ LOADING_MATRIX
        raw_scores.append(raw)
    all_raw = np.array(raw_scores)
    return all_raw.min(axis=0), all_raw.max(axis=0)


_RAW_MIN, _RAW_MAX = _compute_normalization_bounds()


def project(features: list[int]) -> np.ndarray:
    """Project a feature vector into raw (unnormalized) pillar space.

    Accepts 15-feature (form only) or 19-feature (form + depth) vectors.
    If 15 features are passed, depth features default to 0 (no depth bonus —
    the most conservative assumption for cases without depth data)."""
    if len(features) == N_BASE_FEATURES:
        features = list(features) + [0] * N_DEPTH_FEATURES
    if len(features) != N_FEATURES:
        raise ValueError(
            f"expected {N_BASE_FEATURES} or {N_FEATURES} features, "
            f"got {len(features)}")
    return np.array(features, dtype=float) @ LOADING_MATRIX


def project_normalized(features: list[int]) -> dict[str, float]:
    """Project features to normalized [0,1] pillar scores.

    Normalization is min-max across the 10 type templates — a federal_republic
    scores near 1.0 on most pillars, a feudal_order near 0.0.  Values outside
    [0,1] are clamped (a feature vector more extreme than any template)."""
    raw = project(features)
    denom = _RAW_MAX - _RAW_MIN
    denom[denom == 0] = 1.0
    normed = (raw - _RAW_MIN) / denom
    normed = np.clip(normed, 0.0, 1.0)
    return {p: round(float(normed[i]), 4) for i, p in enumerate(PILLAR_NAMES)}


def project_type(type_name: str) -> dict[str, float]:
    """Project a named governance type to normalized pillar scores."""
    if type_name not in TYPE_TEMPLATES:
        raise ValueError(f"unknown type: {type_name}")
    return project_normalized(TYPE_TEMPLATES[type_name])


def displacement(features_pre: list[int], features_post: list[int]) -> dict[str, float]:
    """Compute the institutional displacement vector in pillar space.

    Returns (post - pre) in normalized pillar coordinates: positive means
    the post-collectivization form is predicted to score HIGHER on that pillar."""
    pre = project_normalized(features_pre)
    post = project_normalized(features_post)
    return {p: round(post[p] - pre[p], 4) for p in PILLAR_NAMES}


def displacement_magnitude(features_pre: list[int], features_post: list[int]) -> float:
    """Euclidean magnitude of the displacement vector in pillar space."""
    d = displacement(features_pre, features_post)
    return round(float(np.sqrt(sum(v ** 2 for v in d.values()))), 4)


def profile_shape(features: list[int]) -> dict[str, str]:
    """Classify each pillar as 'strong', 'moderate', or 'weak' based on
    the normalized projection.  Thresholds: strong >= 0.65, weak <= 0.35."""
    normed = project_normalized(features)
    shape = {}
    for p, v in normed.items():
        if v >= 0.65:
            shape[p] = "strong"
        elif v <= 0.35:
            shape[p] = "weak"
        else:
            shape[p] = "moderate"
    return shape
