"""
Negative-control test: do non-self-organizing systems disperse MORE than
self-organizing ones?

Prediction (PREREGISTRATION sec.6): engineered (4A) and classification (4B)
nodes show strictly greater dispersion of log subdivision ratios than the
self-organizing nodes. We test this with Brown-Forsythe (Levene on medians),
which is robust to non-normality, plus a direct CV comparison.

A boundary condition is CONFIRMED if controls disperse more (p < 0.05). If a
control disperses no more than the self-organizing systems, the boundary
condition is violated and that is reported as a primary finding.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats


@dataclass
class DispersionContrast:
    self_org_cv: float
    control_cv: float
    brown_forsythe_stat: float
    brown_forsythe_p: float
    controls_disperse_more: bool
    per_node_cv: dict


def _log_spread(ratios: np.ndarray) -> np.ndarray:
    lr = np.log(np.asarray(ratios, float))
    return lr - np.median(lr)


def dispersion_contrast(self_org_nodes: list, control_nodes: list) -> DispersionContrast:
    so = [np.log(np.asarray(n.ratios, float)) for n in self_org_nodes]
    ct = [np.log(np.asarray(n.ratios, float)) for n in control_nodes]

    # Brown-Forsythe across the two pooled groups (abs deviations from group median)
    so_pool = np.concatenate(so)
    ct_pool = np.concatenate(ct)
    stat, p = stats.levene(so_pool, ct_pool, center="median")

    cv = lambda nodes: float(np.mean([  # noqa: E731
        np.asarray(n.ratios, float).std(ddof=1) / np.asarray(n.ratios, float).mean()
        for n in nodes]))
    so_cv, ct_cv = cv(self_org_nodes), cv(control_nodes)

    per_node = {n.name: float(np.asarray(n.ratios, float).std(ddof=1) / np.asarray(n.ratios, float).mean())
                for n in (self_org_nodes + control_nodes)}

    return DispersionContrast(
        self_org_cv=so_cv,
        control_cv=ct_cv,
        brown_forsythe_stat=float(stat),
        brown_forsythe_p=float(p),
        controls_disperse_more=bool(ct_pool.var() > so_pool.var() and p < 0.05),
        per_node_cv=per_node,
    )
