"""
Hypothesis (a): The Ratchet.

The post-collectivization entity exceeds the pre-fragmentation entity in
scope -- the system doesn't just reform, it overshoots. Measured on 5
dimensions, all deterministic lookups or computations.

Statistical test: sign test across non-control cases. Are positive directions
(post > pre) more frequent than 50%?
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats

from collectivization_case import CaseProfile
from feature_vector import integration_depth, functional_breadth


@dataclass
class RatchetScore:
    name: str
    incorporation_ratio: float     # units_post / units_pre
    demographic_ratio: float       # pop_post / pop_pre
    integration_depth_pre: int     # 0-6
    integration_depth_post: int    # 0-6
    functional_breadth_pre: int    # 0-5
    functional_breadth_post: int   # 0-5
    efficiency_burst: float        # gdp_growth_post - gdp_growth_pre
    positive_dims: int             # how many of 5 dimensions are positive
    dims_detail: dict              # per-dimension: (pre, post, positive?)


def score_case(case: CaseProfile) -> RatchetScore:
    inc = case.units_post / case.units_pre if case.units_pre > 0 else float("nan")
    dem = case.pop_post / case.pop_pre if case.pop_pre > 0 else float("nan")
    id_pre = integration_depth(case.features_pre)
    id_post = integration_depth(case.features_post)
    fb_pre = functional_breadth(case.features_pre)
    fb_post = functional_breadth(case.features_post)
    eff = case.gdp_growth_post - case.gdp_growth_pre

    dims = {
        "incorporation": (inc, 1.0, inc > 1.0),
        "demographic": (dem, 1.0, dem > 1.0),
        "integration_depth": (id_pre, id_post, id_post > id_pre),
        "functional_breadth": (fb_pre, fb_post, fb_post > fb_pre),
        "economic_efficiency": (case.gdp_growth_pre, case.gdp_growth_post, eff > 0),
    }

    positive = sum(1 for _, _, p in dims.values() if p)

    return RatchetScore(
        name=case.name,
        incorporation_ratio=round(inc, 3),
        demographic_ratio=round(dem, 3),
        integration_depth_pre=id_pre,
        integration_depth_post=id_post,
        functional_breadth_pre=fb_pre,
        functional_breadth_post=fb_post,
        efficiency_burst=round(eff, 4),
        positive_dims=positive,
        dims_detail={k: (round(a, 3) if isinstance(a, float) else a,
                         round(b, 3) if isinstance(b, float) else b, p)
                     for k, (a, b, p) in dims.items()},
    )


@dataclass
class RatchetResult:
    per_case: dict[str, RatchetScore]
    n_cases: int
    total_positive: int
    total_dims: int
    sign_test_p: float
    strongest_dimensions: list[str]


def analyze(cases: list[CaseProfile]) -> RatchetResult:
    """Run the ratchet analysis across all non-control cases."""
    non_ctrl = [c for c in cases if not c.is_control]
    scores = {c.name: score_case(c) for c in non_ctrl}

    dim_names = ["incorporation", "demographic", "integration_depth",
                 "functional_breadth", "economic_efficiency"]
    dim_positive_counts = {d: 0 for d in dim_names}
    total_pos = 0
    total_dims = 0

    for s in scores.values():
        for d in dim_names:
            _, _, pos = s.dims_detail[d]
            if pos:
                dim_positive_counts[d] += 1
                total_pos += 1
            total_dims += 1

    n = len(non_ctrl)
    p = float(stats.binomtest(total_pos, total_dims, 0.5, alternative="greater").pvalue) \
        if total_dims > 0 else float("nan")

    strongest = sorted(dim_positive_counts, key=lambda d: -dim_positive_counts[d])

    return RatchetResult(
        per_case=scores,
        n_cases=n,
        total_positive=total_pos,
        total_dims=total_dims,
        sign_test_p=round(p, 4),
        strongest_dimensions=strongest[:3],
    )
