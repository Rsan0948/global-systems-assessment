"""
Hypothesis (b): The Form Shift.

Post-collectivization governance is never a restoration of the
pre-fragmentation type. The system invents a new form, specifically patching
the failure modes exposed by the fragmentation.

Three sub-dimensions, all deterministic:
  1. Feature flip count (0-15)
  2. Legitimacy basis shift (flips in features 0,1,7,8,9)
  3. Failure patching (count of diagnosed failures that were fixed)

Statistical test: Mann-Whitney U comparing flip counts in cases vs. controls.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats

from collectivization_case import CaseProfile
from feature_vector import (
    flip_count, flipped_features, classify, legitimacy_flips,
)
from failure_catalog import diagnostic


@dataclass
class FormShiftScore:
    name: str
    type_pre: str
    type_pre_distance: int
    type_post: str
    type_post_distance: int
    type_changed: bool
    flip_count: int
    flipped_features: list[str]
    legitimacy_flips: int
    failure_diagnostic: dict


def score_case(case: CaseProfile) -> FormShiftScore:
    t_pre, d_pre = classify(case.features_pre)
    t_post, d_post = classify(case.features_post)
    fc = flip_count(case.features_pre, case.features_post)
    ff = flipped_features(case.features_pre, case.features_post)
    lf = legitimacy_flips(case.features_pre, case.features_post)
    diag = diagnostic(case.features_pre, case.features_post)

    return FormShiftScore(
        name=case.name,
        type_pre=t_pre,
        type_pre_distance=d_pre,
        type_post=t_post,
        type_post_distance=d_post,
        type_changed=(t_pre != t_post),
        flip_count=fc,
        flipped_features=ff,
        legitimacy_flips=lf,
        failure_diagnostic=diag,
    )


@dataclass
class FormShiftResult:
    per_case: dict[str, FormShiftScore]
    cases_mean_flips: float
    controls_mean_flips: float
    mann_whitney_u: float
    mann_whitney_p: float
    all_cases_shifted_type: bool
    patching_rate: float           # fraction of cases where >= 1 failure was patched


def analyze(cases: list[CaseProfile]) -> FormShiftResult:
    """Run the form-shift analysis across all cases (including controls)."""
    scores = {c.name: score_case(c) for c in cases}

    case_flips = [scores[c.name].flip_count for c in cases if not c.is_control]
    ctrl_flips = [scores[c.name].flip_count for c in cases if c.is_control]

    if case_flips and ctrl_flips:
        u, p = stats.mannwhitneyu(case_flips, ctrl_flips, alternative="greater")
    else:
        u, p = float("nan"), float("nan")

    non_ctrl_scores = [scores[c.name] for c in cases if not c.is_control]
    all_shifted = all(s.type_changed for s in non_ctrl_scores) if non_ctrl_scores else False
    n_patched = sum(1 for s in non_ctrl_scores if s.failure_diagnostic["patched"])
    patch_rate = n_patched / len(non_ctrl_scores) if non_ctrl_scores else 0.0

    return FormShiftResult(
        per_case=scores,
        cases_mean_flips=round(float(np.mean(case_flips)), 1) if case_flips else 0.0,
        controls_mean_flips=round(float(np.mean(ctrl_flips)), 1) if ctrl_flips else 0.0,
        mann_whitney_u=round(float(u), 1),
        mann_whitney_p=round(float(p), 4),
        all_cases_shifted_type=all_shifted,
        patching_rate=round(patch_rate, 2),
    )
