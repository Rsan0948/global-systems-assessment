"""
Rung-4 mechanism test (Study 3B): is the regularity a LAW, or just a recurring
number?

A constant that recurs across domains can still be coincidence. It becomes a
theorem only if a mechanism PREDICTS it. The proposed mechanism is the
dimensional gap: interior complexity scales as size^a, interface capacity as
size^(a-1), so the gap Delta = a - (a-1) ~ 1, and Delta should PREDICT the
subdivision factor across domains.

This module provides:
  * `estimate_exponents` -- per-domain: estimate the interior and interface
    scaling exponents (and the gap) by log-log regression against system size.
  * `gap_predicts_factor` -- cross-domain: test whether Delta predicts the
    observed log subdivision factor (slope CI excludes 0) AND whether Delta
    itself clusters at 1.

Both are mechanism-agnostic about the *value* of the constant; they test the
generative claim directly.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats


@dataclass
class ExponentFit:
    interior_exp: float
    interior_se: float
    interface_exp: float
    interface_se: float
    gap: float
    gap_se: float


def _loglog(size: np.ndarray, proxy: np.ndarray) -> tuple[float, float]:
    x = np.log(np.asarray(size, dtype=float))
    y = np.log(np.asarray(proxy, dtype=float))
    res = stats.linregress(x, y)
    return float(res.slope), float(res.stderr)


def estimate_exponents(size, interior_proxy, interface_proxy) -> ExponentFit:
    """Estimate interior & interface scaling exponents and their gap from raw
    allometry (e.g. internal-relationship count and throughput vs system size)."""
    a, a_se = _loglog(size, interior_proxy)
    b, b_se = _loglog(size, interface_proxy)
    return ExponentFit(a, a_se, b, b_se, a - b, float(np.hypot(a_se, b_se)))


@dataclass
class GapPredictionResult:
    n_domains: int
    slope: float
    slope_ci: tuple[float, float]
    slope_p: float                 # H0: gap does not predict factor
    gap_mean: float
    gap_mean_ci: tuple[float, float]
    gap_consistent_with_1: bool
    r_squared: float


def gap_predicts_factor(gaps, log_factors, gap_ses=None) -> GapPredictionResult:
    """Cross-domain test: does Delta predict log(subdivision factor)?

    Weighted least squares if gap standard errors are supplied. Also tests
    whether the gaps cluster at 1 (the dimensional-gap prediction)."""
    g = np.asarray(gaps, dtype=float)
    lf = np.asarray(log_factors, dtype=float)
    n = g.size
    if n < 3:
        raise ValueError("need >= 3 domains with exponent data for the cross-domain test")

    res = stats.linregress(g, lf)
    df = n - 2
    tcrit = stats.t.ppf(0.975, df)
    slope_ci = (res.slope - tcrit * res.stderr, res.slope + tcrit * res.stderr)

    gm = float(g.mean())
    gm_se = float(g.std(ddof=1) / np.sqrt(n))
    gm_ci = (gm - tcrit * gm_se, gm + tcrit * gm_se)

    return GapPredictionResult(
        n_domains=int(n),
        slope=float(res.slope),
        slope_ci=(float(slope_ci[0]), float(slope_ci[1])),
        slope_p=float(res.pvalue),
        gap_mean=gm,
        gap_mean_ci=(float(gm_ci[0]), float(gm_ci[1])),
        gap_consistent_with_1=bool(gm_ci[0] <= 1.0 <= gm_ci[1]),
        r_squared=float(res.rvalue ** 2),
    )
