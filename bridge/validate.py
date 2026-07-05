"""
Validation: compare feature-vector-predicted pillar profiles against actual
MI scores for modern cases where both data sources exist.

The validation answers three distinct questions:

1. SHAPE PREDICTION (per-country Spearman): does the model predict which
   pillars are strong vs weak for each country?

2. CROSS-TYPE ORDERING (cross-type Pearson): when countries have different
   institutional structures, do structurally stronger forms predict higher
   actual scores?

3. CAPACITY REALIZATION: the ratio actual/predicted reveals how fully a
   country realizes its structural potential.  Ratio < 1 means paper
   institutions (form without capacity).  Ratio > 1 means cultural/
   historical factors exceed what structure alone predicts.

The RESIDUAL (actual - predicted) is itself informative: a large positive
residual on P2 means the country has more innovation capacity than its
formal structure would suggest.

Key finding: binary features capture institutional FORM, not governance
CAPACITY.  Countries with identical formal structures (e.g., Brazil and
Switzerland are both federal republics) can have very different MI scores.
The gap IS the diagnostic — it measures how much governance quality comes
from factors beyond formal institutional design.
"""

from __future__ import annotations

from collections import defaultdict

import numpy as np

from pillar_loading import project_normalized, PILLAR_NAMES

# Actual MI pillar scores (2024) from the canonical panel.
# These are the GROUND TRUTH for validation.
MI_REFERENCE_SCORES = {
    "Germany": {"P1": 0.7996, "P2": 0.7243, "P3": 0.9508, "P4": 0.8751, "P5": 0.7376},
    "United States": {"P1": 0.7312, "P2": 0.6741, "P3": 0.9092, "P4": 0.9382, "P5": 0.6427},
    "France": {"P1": 0.7211, "P2": 0.6871, "P3": 0.9067, "P4": 0.8467, "P5": 0.6888},
    "Italy": {"P1": 0.6333, "P2": 0.6394, "P3": 0.9027, "P4": 0.8451, "P5": 0.6784},
    "Japan": {"P1": 0.8044, "P2": 0.7377, "P3": 0.9246, "P4": 0.8144, "P5": 0.7993},
    "Netherlands": {"P1": 0.8294, "P2": 0.6389, "P3": 0.9393, "P4": 0.9480, "P5": 0.7321},
    "Switzerland": {"P1": 0.8456, "P2": 0.7457, "P3": 0.9560, "P4": 0.9612, "P5": 0.8265},
    "Australia": {"P1": 0.8195, "P2": 0.5036, "P3": 0.9562, "P4": 0.8022, "P5": 0.7944},
    "Canada": {"P1": 0.7975, "P2": 0.6471, "P3": 0.9336, "P4": 0.8523, "P5": 0.8019},
    "Brazil": {"P1": 0.4512, "P2": 0.5082, "P3": 0.7893, "P4": 0.6661, "P5": 0.4746},
    "Argentina": {"P1": 0.4893, "P2": 0.4409, "P3": 0.8779, "P4": 0.7203, "P5": 0.6216},
    "Spain": {"P1": 0.6665, "P2": 0.6104, "P3": 0.9166, "P4": 0.8333, "P5": 0.6480},
}

# Post-collectivization feature vectors for the same countries
# (from studies/5_collectivization/cases/*.json)
POST_FEATURE_VECTORS = {
    "Germany": [1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    "United States": [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    "France": [1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0],
    "Italy": [1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    "Japan": [1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    "Netherlands": [0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    "Switzerland": [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    "Australia": [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    "Canada": [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    "Brazil": [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    "Argentina": [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    "Spain": [1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0],
}


def _rankdata(arr):
    """Rank data with average tie-breaking (numpy-only, no scipy needed)."""
    arr = np.asarray(arr, dtype=float)
    order = np.argsort(arr)
    ranks = np.empty(len(arr), dtype=float)
    ranks[order] = np.arange(1, len(arr) + 1, dtype=float)
    for val in np.unique(arr):
        mask = arr == val
        if np.sum(mask) > 1:
            ranks[mask] = np.mean(ranks[mask])
    return ranks


def _spearman(x, y):
    """Spearman rank correlation, numpy-only."""
    rx = _rankdata(x)
    ry = _rankdata(y)
    if np.std(rx) == 0 or np.std(ry) == 0:
        return float("nan")
    return float(np.corrcoef(rx, ry)[0, 1])


def _shape_correlation(predicted, actual):
    """Per-country Spearman: does the model predict which pillars are strong
    vs weak?  With 5 pillars this tests SHAPE, not absolute level."""
    pred = [predicted[p] for p in PILLAR_NAMES]
    act = [actual[p] for p in PILLAR_NAMES]
    return round(_spearman(pred, act), 4)


def _capacity_realization(predicted, actual):
    """Ratio actual/predicted per pillar.

    > 1 means country exceeds structural prediction (cultural/historical edge).
    < 1 means below structural prediction (paper institutions).
    Predicted values below 0.05 are floored to avoid near-zero division."""
    result = {}
    for p in PILLAR_NAMES:
        pred = max(predicted[p], 0.05)
        result[p] = round(actual[p] / pred, 4)
    return result


def validate_all() -> dict:
    """Run validation across all countries with both feature vectors and MI scores.

    Returns per-country and aggregate results including shape prediction
    (Spearman), capacity realization, and cross-type analysis."""
    results = {}
    all_predicted = []
    all_actual = []

    for country in sorted(MI_REFERENCE_SCORES):
        if country not in POST_FEATURE_VECTORS:
            continue

        predicted = project_normalized(POST_FEATURE_VECTORS[country])
        actual = MI_REFERENCE_SCORES[country]

        residuals = {p: round(actual[p] - predicted[p], 4)
                     for p in PILLAR_NAMES}
        abs_residuals = {p: abs(residuals[p]) for p in PILLAR_NAMES}

        shape_corr = _shape_correlation(predicted, actual)
        realization = _capacity_realization(predicted, actual)

        pred_vec = [predicted[p] for p in PILLAR_NAMES]
        act_vec = [actual[p] for p in PILLAR_NAMES]
        all_predicted.extend(pred_vec)
        all_actual.extend(act_vec)

        results[country] = {
            "predicted": predicted,
            "actual": actual,
            "residuals": residuals,
            "mean_absolute_residual": round(
                float(np.mean(list(abs_residuals.values()))), 4),
            "largest_residual_pillar": max(abs_residuals, key=abs_residuals.get),
            "largest_residual_value": round(
                float(max(abs_residuals.values())), 4),
            "shape_correlation": shape_corr,
            "capacity_realization": realization,
            "mean_realization": round(
                float(np.mean(list(realization.values()))), 4),
        }

    pred_arr = np.array(all_predicted)
    act_arr = np.array(all_actual)

    if len(pred_arr) > 2:
        correlation = float(np.corrcoef(pred_arr, act_arr)[0, 1])
        rmse = float(np.sqrt(np.mean((pred_arr - act_arr) ** 2)))
        mae = float(np.mean(np.abs(pred_arr - act_arr)))
    else:
        correlation = float("nan")
        rmse = float("nan")
        mae = float("nan")

    per_pillar_corr = {}
    for i, p in enumerate(PILLAR_NAMES):
        p_pred = [results[c]["predicted"][p] for c in results]
        p_act = [results[c]["actual"][p] for c in results]
        if len(p_pred) > 2:
            per_pillar_corr[p] = round(
                float(np.corrcoef(p_pred, p_act)[0, 1]), 4)
        else:
            per_pillar_corr[p] = float("nan")

    per_pillar_bias = {}
    for p in PILLAR_NAMES:
        residuals = [results[c]["residuals"][p] for c in results]
        per_pillar_bias[p] = round(float(np.mean(residuals)), 4)

    # Shape prediction aggregate
    shape_corrs = [results[c]["shape_correlation"] for c in results
                   if not np.isnan(results[c]["shape_correlation"])]
    median_shape = round(float(np.median(shape_corrs)), 4) if shape_corrs else float("nan")
    mean_shape = round(float(np.mean(shape_corrs)), 4) if shape_corrs else float("nan")

    cross_type = _cross_type_analysis(results)

    return {
        "per_country": results,
        "aggregate": {
            "n_countries": len(results),
            "overall_correlation": round(correlation, 4),
            "rmse": round(rmse, 4),
            "mae": round(mae, 4),
            "per_pillar_correlation": per_pillar_corr,
            "per_pillar_bias": per_pillar_bias,
            "median_shape_correlation": median_shape,
            "mean_shape_correlation": mean_shape,
            "n_shape_valid": len(shape_corrs),
            "cross_type": cross_type,
        },
    }


def _cross_type_analysis(results: dict) -> dict:
    """Separate cross-type from within-type variation.

    Countries with different feature vectors should show cross-type correlation
    (structural differences predict score differences).  Countries with the SAME
    feature vector only differ by capacity realization — the model gives them
    identical predictions, so all variance is from non-structural factors."""
    groups = defaultdict(list)
    for country in results:
        fv_key = tuple(POST_FEATURE_VECTORS[country])
        groups[fv_key].append(country)

    # Cross-type: one point per (type, pillar) using group mean actuals
    type_predicted = []
    type_actual = []
    for fv_key, countries in groups.items():
        for p in PILLAR_NAMES:
            mean_pred = float(np.mean(
                [results[c]["predicted"][p] for c in countries]))
            mean_act = float(np.mean(
                [results[c]["actual"][p] for c in countries]))
            type_predicted.append(mean_pred)
            type_actual.append(mean_act)

    if len(type_predicted) > 2:
        cross_corr_pearson = round(
            float(np.corrcoef(type_predicted, type_actual)[0, 1]), 4)
        cross_corr_spearman = round(
            _spearman(type_predicted, type_actual), 4)
    else:
        cross_corr_pearson = float("nan")
        cross_corr_spearman = float("nan")

    # Within-type: for groups with >1 country, measure actual MI spread
    within_type = {}
    for fv_key, countries in groups.items():
        if len(countries) > 1:
            label = "/".join(sorted(countries))
            spreads = {}
            realizations = {}
            for p in PILLAR_NAMES:
                actual_vals = [results[c]["actual"][p] for c in countries]
                spreads[p] = round(float(np.std(actual_vals)), 4)
                real_vals = [results[c]["capacity_realization"][p]
                             for c in countries]
                realizations[p] = round(float(np.std(real_vals)), 4)
            within_type[label] = {
                "n": len(countries),
                "per_pillar_actual_std": spreads,
                "mean_actual_std": round(
                    float(np.mean(list(spreads.values()))), 4),
                "per_pillar_realization_std": realizations,
            }

    return {
        "n_unique_types": len(groups),
        "cross_type_correlation_pearson": cross_corr_pearson,
        "cross_type_correlation_spearman": cross_corr_spearman,
        "type_groups": {
            "/".join(sorted(cs)): len(cs) for cs in groups.values()},
        "within_type": within_type,
    }


def interpret_residuals(validation_result: dict) -> dict:
    """Interpret what the residuals tell us.

    Large positive residual = country has MORE capacity than structure predicts
    (cultural/historical factors).
    Large negative residual = country has LESS capacity than structure predicts
    (structure without substance — paper institutions)."""
    interpretations = {}
    for country, data in validation_result["per_country"].items():
        findings = []
        for p in PILLAR_NAMES:
            r = data["residuals"][p]
            if abs(r) < 0.1:
                continue
            direction = "exceeds" if r > 0 else "falls short of"
            findings.append(
                f"{p}: actual {direction} structural prediction by {abs(r):.2f}")

        real = data.get("mean_realization", 1.0)
        if real < 0.8:
            findings.append(
                f"capacity realization {real:.0%} — significant form-capacity gap")
        elif real > 1.1:
            findings.append(
                f"capacity realization {real:.0%} — non-structural factors "
                f"boost governance beyond institutional design")

        interpretations[country] = findings if findings else [
            "within prediction bounds"]
    return interpretations
