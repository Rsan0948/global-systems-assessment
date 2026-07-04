"""
Pathway analysis: classifying collectivization mechanisms.

Identifies four distinct pathways based on two measurable factors:
1. Predecessor integration depth (the "institutional ceiling")
2. Collectivization speed (conquest vs negotiation)

Statistically grounded findings:
- Predecessor depth predicts flip count (rho=-0.844, p<0.001)
- Among high-depth cases, speed predicts integration loss (rho=0.825, p=0.012)
- All restoration cases have id_pre >= 5 (Fisher p=0.077)
- Negotiated collectivizations have the highest mean durability
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats

from collectivization_case import CaseProfile
from feature_vector import classify, integration_depth, FEATURE_NAMES
from form_shift import score_case as fs_score


DEPTH_THRESHOLD = 5
SPEED_THRESHOLD = 150

INTEGRATION_FEATURES = [4, 5, 10, 11, 12, 13]
SOVEREIGNTY_FEATURES = [8, 9]


@dataclass
class PathwayScore:
    name: str
    pathway: str
    id_pre: int
    id_post: int
    flip_count: int
    collect_speed: int
    integration_features_lost: int
    sovereignty_features_gained: int
    failures_patched: int
    new_vulnerabilities: int
    durability: int


@dataclass
class PathwayResult:
    per_case: dict[str, PathwayScore]
    pathway_counts: dict[str, int]
    depth_flip_rho: float
    depth_flip_p: float
    speed_integration_loss_rho: float
    speed_integration_loss_p: float
    ceiling_fisher_p: float
    pathway_durabilities: dict[str, float]


def classify_pathway(case: CaseProfile) -> str:
    id_pre = integration_depth(case.features_pre)
    s = fs_score(case)

    if id_pre < DEPTH_THRESHOLD:
        return "construction"
    elif s.flip_count <= 1:
        return "restoration"
    elif case.collect_speed_years > SPEED_THRESHOLD:
        return "negotiation"
    else:
        return "redesign"


def score_case(case: CaseProfile) -> PathwayScore:
    s = fs_score(case)
    id_pre = integration_depth(case.features_pre)
    id_post = integration_depth(case.features_post)

    int_lost = sum(1 for i in INTEGRATION_FEATURES
                   if case.features_pre[i] == 1 and case.features_post[i] == 0)
    sov_gained = sum(1 for i in SOVEREIGNTY_FEATURES
                     if case.features_pre[i] == 0 and case.features_post[i] == 1)

    return PathwayScore(
        name=case.name,
        pathway=classify_pathway(case),
        id_pre=id_pre,
        id_post=id_post,
        flip_count=s.flip_count,
        collect_speed=case.collect_speed_years,
        integration_features_lost=int_lost,
        sovereignty_features_gained=sov_gained,
        failures_patched=len(s.failure_diagnostic["patched"]),
        new_vulnerabilities=len(s.failure_diagnostic["new_vulnerabilities"]),
        durability=case.durability_years,
    )


def analyze(cases: list[CaseProfile]) -> PathwayResult:
    non_ctrl = [c for c in cases if not c.is_control]
    scores = {c.name: score_case(c) for c in non_ctrl}

    pathway_counts = {}
    for s in scores.values():
        pathway_counts[s.pathway] = pathway_counts.get(s.pathway, 0) + 1

    id_pres = [s.id_pre for s in scores.values()]
    flips = [s.flip_count for s in scores.values()]
    if len(id_pres) >= 3:
        depth_rho, depth_p = stats.spearmanr(id_pres, flips)
    else:
        depth_rho, depth_p = float("nan"), float("nan")

    high_depth = [s for s in scores.values() if s.id_pre >= DEPTH_THRESHOLD]
    if len(high_depth) >= 3:
        hd_speeds = [s.collect_speed for s in high_depth]
        hd_int_lost = [s.integration_features_lost for s in high_depth]
        speed_rho, speed_p = stats.spearmanr(hd_speeds, hd_int_lost)
    else:
        speed_rho, speed_p = float("nan"), float("nan")

    n_high = len(high_depth)
    n_low = len(scores) - n_high
    high_rest = sum(1 for s in high_depth if s.pathway == "restoration")
    low_rest = sum(1 for s in scores.values()
                   if s.id_pre < DEPTH_THRESHOLD and s.pathway == "restoration")
    if n_high > 0 and n_low > 0:
        _, fisher_p = stats.fisher_exact(
            [[high_rest, n_high - high_rest], [low_rest, n_low - low_rest]])
    else:
        fisher_p = float("nan")

    pathway_durs = {}
    for p_name in ["construction", "restoration", "negotiation", "redesign"]:
        durs = [s.durability for s in scores.values() if s.pathway == p_name]
        pathway_durs[p_name] = round(float(np.mean(durs)), 1) if durs else float("nan")

    return PathwayResult(
        per_case=scores,
        pathway_counts=pathway_counts,
        depth_flip_rho=round(float(depth_rho), 3),
        depth_flip_p=round(float(depth_p), 4),
        speed_integration_loss_rho=round(float(speed_rho), 3),
        speed_integration_loss_p=round(float(speed_p), 4),
        ceiling_fisher_p=round(float(fisher_p), 4),
        pathway_durabilities=pathway_durs,
    )
