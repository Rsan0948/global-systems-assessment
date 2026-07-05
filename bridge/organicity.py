"""
Organicity scoring: quantifying how much of a post-collectivization system
was GROWN (inherited from predecessor) versus IMPOSED (constructed anew).

This connects to the fragmentation study's strongest finding — the dispersion
contrast (self-organizing CV 0.21 vs designed CV 5.77) — by providing a
per-case measure of institutional "designedness."

Higher organicity → expect tighter (more predictable) fracturing if the
system fragments again.  Lower organicity → expect wider dispersion,
less predictable breakup.
"""

from __future__ import annotations

import numpy as np


def organicity_score(features_pre: list[int],
                     features_post: list[int]) -> float:
    """Fraction of features in the post vector that match the pre vector.

    1.0 = pure restoration (all features inherited).
    0.0 = total redesign (every feature changed).

    This is 1 - (hamming_distance / N_FEATURES)."""
    n = len(features_pre)
    if n != len(features_post):
        raise ValueError("feature vectors must have equal length")
    same = sum(features_pre[i] == features_post[i] for i in range(n))
    return round(same / n, 4)


def imposed_features(features_pre: list[int],
                     features_post: list[int],
                     feature_names: list[str]) -> list[str]:
    """Which specific features were changed (imposed/constructed)?"""
    return [feature_names[i] for i in range(len(features_pre))
            if features_pre[i] != features_post[i]]


def inherited_features(features_pre: list[int],
                       features_post: list[int],
                       feature_names: list[str]) -> list[str]:
    """Which specific features were kept (inherited/organic)?"""
    return [feature_names[i] for i in range(len(features_pre))
            if features_pre[i] == features_post[i]]


# Dispersion contrast reference values from integration/results
SELF_ORGANIZING_CV = 0.213
DESIGNED_CV = 5.767


def expected_fragmentation_cv(organicity: float) -> float:
    """Predicted CV of branching factors if this system fragments again.

    Linear interpolation between the empirical self-organizing and designed
    CVs.  This is a FIRST-ORDER APPROXIMATION — the actual relationship
    may be nonlinear, but we need data to determine the shape.

    organicity=1.0 → CV ≈ 0.21 (grown, tight fracturing)
    organicity=0.0 → CV ≈ 5.77 (designed, dispersed fracturing)"""
    return round(
        SELF_ORGANIZING_CV + (1.0 - organicity) * (DESIGNED_CV - SELF_ORGANIZING_CV),
        3,
    )


def organicity_diagnostic(features_pre: list[int],
                           features_post: list[int],
                           feature_names: list[str]) -> dict:
    """Full organicity diagnostic for a case."""
    org = organicity_score(features_pre, features_post)
    return {
        "organicity": org,
        "imposed_count": sum(features_pre[i] != features_post[i]
                             for i in range(len(features_pre))),
        "inherited_count": sum(features_pre[i] == features_post[i]
                               for i in range(len(features_pre))),
        "imposed_features": imposed_features(features_pre, features_post, feature_names),
        "inherited_features": inherited_features(features_pre, features_post, feature_names),
        "expected_fragmentation_cv": expected_fragmentation_cv(org),
        "fragmentation_predictability": "high" if org > 0.7 else (
            "moderate" if org > 0.4 else "low"),
    }
