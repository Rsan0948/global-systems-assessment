"""
Corporate predictive test: does organizational complexity ratio predict a
subsequent split / acquisition / failure? (PREREGISTRATION Study 2B survival
part.)

Implements a discrete-time hazard model (logistic hazard) as a dependency-light
stand-in for Cox proportional hazards: P(event in period t | survived) ~
logit(complexity_ratio + size + sector + period). The hazard ratio for the
complexity term is exp(beta). This avoids a lifelines dependency while giving
the same coefficient interpretation.

`make_firm_panel(beta_true=...)` generates a calibrated firm-period panel so we
can verify the test recovers a true complexity effect and is null without one.
Swap in real EDGAR/Compustat survival data via the same schema.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

# reuse the IRLS logistic + LR machinery from the political node
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "political"))
from dgs import _irls, _dummies  # noqa: E402


@dataclass
class HazardResult:
    n: int
    beta_complexity: float
    hazard_ratio: float
    lr_stat: float
    lr_p: float


def fit_hazard(panel: dict) -> HazardResult:
    y = np.asarray(panel["event"], dtype=float)
    sector = _dummies(panel["sector"])
    period = _dummies(panel["period"])
    controls = np.column_stack([np.ones_like(y), panel["log_size"], sector, period])
    full = np.column_stack([controls, panel["complexity_ratio"]])
    _, ll_r = _irls(controls, y)
    bf, ll_f = _irls(full, y)
    from scipy.stats import chi2
    lr = 2.0 * (ll_f - ll_r)
    return HazardResult(int(y.size), float(bf[-1]), float(np.exp(bf[-1])),
                        float(lr), float(chi2.sf(lr, 1)))


def make_firm_panel(n_firms: int = 600, n_periods: int = 8,
                    beta_true: float = 0.5, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    N = n_firms * n_periods
    log_size = rng.normal(7.0, 1.4, size=N)
    sector = rng.integers(0, 8, size=N)
    period = rng.integers(0, n_periods, size=N)
    # complexity ratio = segments / management levels; correlates weakly w/ size
    complexity_ratio = _z(0.3 * (log_size - 7.0) + rng.normal(0, 1, size=N))
    eta = -2.8 + beta_true * complexity_ratio - 0.2 * (log_size - 7.0)
    p = 1.0 / (1.0 + np.exp(-eta))
    event = (rng.random(N) < p).astype(int)
    return {"event": event, "log_size": log_size, "sector": sector,
            "period": period, "complexity_ratio": complexity_ratio}


def _z(x):
    return (x - x.mean()) / x.std()
