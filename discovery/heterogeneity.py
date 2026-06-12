"""
Core discovery instrument: between- vs within-domain variance decomposition.

The question "is there a theorem?" is, statistically, a question about variance
components, not about a mean. We map it onto the well-understood machinery of
random-effects meta-analysis:

  * Each DOMAIN (rivers, vasculature, firms, polities, ...) contributes one
    estimate of its characteristic subdivision ratio, with a standard error
    derived from its within-domain scatter and sample size.
  * The DerSimonian-Laird random-effects model then separates:
      - within-domain variance  (is each domain individually concentrated?  -> rung 1)
      - between-domain variance tau^2 (do domains share one value? -> rung 2)
      - the pooled value and its CI (the candidate universal constant -> rung 3)
  * Cochran's Q tests H0: all domains share a single true value (universality).
    I^2 = fraction of total variance that is between-domain.

Everything is computed on the LOG scale (ratios are positive, multiplicative),
then exponentiated back to the ratio scale for reporting.

This module is mechanism-agnostic. The "is the structure trivial?" question is
answered by `trivial_null.py`, which runs THIS same analysis on mechanism-free
simulated data and compares.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats


@dataclass
class DomainEstimate:
    name: str
    n: int
    log_mean: float          # mean of log(ratio)
    log_var: float           # sampling variance of the log-mean = s^2 / n
    ratio_mean: float        # exp(log_mean)


@dataclass
class HeterogeneityResult:
    domains: list[DomainEstimate]
    pooled_ratio: float                 # exp(random-effects pooled log-mean)
    pooled_ci: tuple[float, float]      # 95% CI on the ratio scale
    tau: float                          # between-domain SD on the log scale
    tau2: float
    i_squared: float                    # 0..1 fraction between-domain
    q_stat: float
    q_df: int
    q_p: float                          # p for "all domains share one value"
    within_domain_cv: dict              # per-domain coefficient of variation (ratio scale)


def domain_estimates(data: dict[str, np.ndarray]) -> list[DomainEstimate]:
    """data: {domain_name: array of ratio measurements (>0)}; n_d >= 2 required."""
    out: list[DomainEstimate] = []
    for name, x in data.items():
        x = np.asarray(x, dtype=float)
        if x.size < 2:
            raise ValueError(f"domain {name!r} needs >= 2 measurements")
        logx = np.log(x)
        lm = float(logx.mean())
        lv = float(logx.var(ddof=1) / x.size)         # variance of the mean
        out.append(DomainEstimate(name, int(x.size), lm, lv, float(np.exp(lm))))
    return out


def dersimonian_laird(estimates: list[DomainEstimate]) -> tuple[float, float, float, float, int, float, float]:
    """Returns (pooled_log, se_log, tau2, Q, df, I2, q_p) on the log scale."""
    y = np.array([e.log_mean for e in estimates])
    v = np.array([e.log_var for e in estimates])
    v = np.where(v <= 0, 1e-12, v)                    # guard zero-variance domains
    w = 1.0 / v
    fe = float(np.sum(w * y) / np.sum(w))
    Q = float(np.sum(w * (y - fe) ** 2))
    df = len(estimates) - 1
    C = float(np.sum(w) - np.sum(w ** 2) / np.sum(w))
    tau2 = max(0.0, (Q - df) / C) if C > 0 else 0.0
    wr = 1.0 / (v + tau2)
    pooled = float(np.sum(wr * y) / np.sum(wr))
    se = float(np.sqrt(1.0 / np.sum(wr)))
    i2 = max(0.0, (Q - df) / Q) if Q > 0 else 0.0
    q_p = float(stats.chi2.sf(Q, df)) if df > 0 else float("nan")
    return pooled, se, tau2, Q, df, i2, q_p


def analyze(data: dict[str, np.ndarray]) -> HeterogeneityResult:
    est = domain_estimates(data)
    pooled, se, tau2, Q, df, i2, q_p = dersimonian_laird(est)
    cv = {}
    for name, x in data.items():
        x = np.asarray(x, dtype=float)
        cv[name] = float(x.std(ddof=1) / x.mean())
    return HeterogeneityResult(
        domains=est,
        pooled_ratio=float(np.exp(pooled)),
        pooled_ci=(float(np.exp(pooled - 1.96 * se)), float(np.exp(pooled + 1.96 * se))),
        tau=float(np.sqrt(tau2)),
        tau2=float(tau2),
        i_squared=float(i2),
        q_stat=float(Q),
        q_df=int(df),
        q_p=float(q_p),
        within_domain_cv=cv,
    )
