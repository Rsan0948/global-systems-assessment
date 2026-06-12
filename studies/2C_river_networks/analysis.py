"""
Statistics for Study 2C, implementing the §3/§6 analysis plan.

- `kde_mode_ci`        : mode of the pooled Rb distribution with a bootstrap CI.
- `log_marginal_*`     : Bayesian marginal likelihoods for competing models of
                          the distribution's center.
- `model_comparison`   : Bayes factors of center in {e, 3, pi, 2, 4} vs a
                          free-center model and a uniform null, plus the
                          pre-registered Tier decision (§1.1).

Likelihood model (frozen here, before data): per-basin Rb is lognormal,
ln(Rb) ~ Normal(mu, sigma). A point-center model M_k fixes mu = ln(k) and
integrates sigma against a half-Normal(scale=0.3) prior. The free-center
model integrates mu against Normal(ln 3, 0.5) and sigma as above; its extra
parameter is penalised automatically by the marginal likelihood (Occam). The
uniform null is Rb ~ Uniform(1.2, 10) on the Rb scale. All likelihoods are
densities w.r.t. the observed Rb, so the Bayes factors are valid.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from scipy import stats
from scipy.special import logsumexp

E = math.e
PI = math.pi
CANDIDATES = {"e": E, "3": 3.0, "pi": PI, "2": 2.0, "4": 4.0}


def _safe_bf(log_num: float, log_den: float) -> float:
    """exp(log_num - log_den), saturating to +/-inf instead of overflowing."""
    d = log_num - log_den
    if d > 700:
        return math.inf
    if d < -700:
        return 0.0
    return math.exp(d)

# Priors (frozen in the pre-registration).
_SIGMA_GRID = np.linspace(0.02, 0.9, 120)
_SIGMA_PRIOR_SCALE = 0.30          # half-Normal scale on log-sd
_MU_GRID = np.log(np.linspace(1.8, 6.0, 160))
_MU_PRIOR_MEAN = math.log(3.0)
_MU_PRIOR_SD = 0.5
_UNIFORM_LO, _UNIFORM_HI = 1.2, 10.0


def _suff_stats(logx: np.ndarray) -> tuple[int, float, float]:
    """Sufficient statistics (n, sum logx, sum logx^2) for the lognormal."""
    return logx.size, float(np.sum(logx)), float(np.sum(logx ** 2))


def _loglik_from_stats(stats_tuple: tuple[int, float, float], mu: float, sigma: float) -> float:
    """Sum of log lognormal densities (w.r.t. Rb) from sufficient statistics.

    sum_i (logx_i - mu)^2 = S2 - 2 mu S1 + n mu^2, so each (mu, sigma) costs
    O(1) instead of O(n) — essential for the n=10k power cells.
    """
    n, s1, s2 = stats_tuple
    quad = s2 - 2 * mu * s1 + n * mu * mu
    return (
        -s1
        - n * math.log(sigma)
        - 0.5 * n * math.log(2 * math.pi)
        - quad / (2 * sigma ** 2)
    )


def _sigma_log_weights() -> tuple[np.ndarray, np.ndarray]:
    """(sigma grid, normalised log prior weights) for a half-Normal prior."""
    dens = stats.halfnorm.pdf(_SIGMA_GRID, scale=_SIGMA_PRIOR_SCALE)
    w = dens / dens.sum()
    return _SIGMA_GRID, np.log(w)


def log_marginal_point(rb: np.ndarray, k: float) -> float:
    """log marginal likelihood of point-center model M_k."""
    ss = _suff_stats(np.log(rb))
    mu = math.log(k)
    sig, logw = _sigma_log_weights()
    terms = np.array([logw[j] + _loglik_from_stats(ss, mu, sig[j]) for j in range(sig.size)])
    return float(logsumexp(terms))


def log_marginal_free(rb: np.ndarray) -> float:
    """log marginal likelihood of the free-center model."""
    ss = _suff_stats(np.log(rb))
    sig, sig_logw = _sigma_log_weights()
    mu_dens = stats.norm.pdf(_MU_GRID, loc=_MU_PRIOR_MEAN, scale=_MU_PRIOR_SD)
    mu_logw = np.log(mu_dens / mu_dens.sum())
    terms = np.empty(_MU_GRID.size * sig.size)
    idx = 0
    for i in range(_MU_GRID.size):
        for j in range(sig.size):
            terms[idx] = mu_logw[i] + sig_logw[j] + _loglik_from_stats(ss, _MU_GRID[i], sig[j])
            idx += 1
    return float(logsumexp(terms))


def log_marginal_uniform(rb: np.ndarray) -> float:
    """log marginal likelihood of the uniform null on [1.2, 10]."""
    if np.any((rb < _UNIFORM_LO) | (rb > _UNIFORM_HI)):
        return -np.inf
    return float(rb.size * math.log(1.0 / (_UNIFORM_HI - _UNIFORM_LO)))


def kde_mode_ci(
    rb: np.ndarray,
    n_boot: int = 1000,
    grid: np.ndarray | None = None,
    seed: int = 0,
) -> tuple[float, float, float]:
    """Mode of the Rb distribution (via Gaussian KDE on log Rb) with a
    percentile bootstrap 95% CI. Returns (mode, lo, hi)."""
    if grid is None:
        grid = np.linspace(1.5, 8.0, 1300)
    loggrid = np.log(grid)

    def _mode(sample: np.ndarray) -> float:
        kde = stats.gaussian_kde(np.log(sample))
        return float(grid[np.argmax(kde(loggrid))])

    point = _mode(rb)
    rng = np.random.default_rng(seed)
    boots = np.array([_mode(rng.choice(rb, size=rb.size, replace=True)) for _ in range(n_boot)])
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return point, float(lo), float(hi)


@dataclass
class ModelComparison:
    log_ml: dict[str, float]
    bayes_factors_vs_best: dict[str, float]
    best_model: str
    bf_e_vs_3: float
    bf_e_vs_pi: float
    mode: float
    mode_ci: tuple[float, float]
    tier: int
    tier_reason: str
    extras: dict = field(default_factory=dict)


def model_comparison(rb: np.ndarray, n_boot: int = 1000, seed: int = 0) -> ModelComparison:
    """Full §3 model comparison + the §1.1 Tier decision for this domain.

    Tier decision (THIS domain only; the paper aggregates across domains):
      Tier 1 if the bootstrap 95% CI on the center INCLUDES e and EXCLUDES
              both 3 and pi -- i.e. the data localise the center to e
              specifically, not merely "nearer e than 3".
      Tier 0 if the uniform null is the best model, or the center CI lies
              outside [2, 4].
      Tier 2 otherwise (a small-value center is established but not separated
              to e).

    Why CI-separation, not point-model Bayes factors: with fixed-point models
    and large n, BF(e vs 3) diverges toward whichever value is *nearer* the
    true center even when neither is correct (a true center of 2.85 yields
    BF(e:3) growing past 1e7), so a "BF >= 10" bar is sample-size-hackable.
    A credible interval on the center instead narrows around the TRUE value,
    so a true-2.85 world fails Tier 1 (CI excludes both e and 3) as it should.
    The point-model Bayes factors are still reported below as descriptive
    model-fit statistics, but they do not drive the Tier decision.
    """
    log_ml = {name: log_marginal_point(rb, k) for name, k in CANDIDATES.items()}
    log_ml["free"] = log_marginal_free(rb)
    log_ml["uniform"] = log_marginal_uniform(rb)

    best = max(log_ml, key=log_ml.get)
    bf_vs_best = {m: _safe_bf(log_ml[m], log_ml[best]) for m in log_ml}
    bf_e_3 = _safe_bf(log_ml["e"], log_ml["3"])
    bf_e_pi = _safe_bf(log_ml["e"], log_ml["pi"])

    mode, lo, hi = kde_mode_ci(rb, n_boot=n_boot, seed=seed)
    e_in = lo <= E <= hi
    three_in = lo <= 3.0 <= hi
    pi_in = lo <= PI <= hi

    if best == "uniform" or hi < 2.0 or lo > 4.0:
        tier, reason = 0, f"uniform null best or center CI [{lo:.2f},{hi:.2f}] outside [2,4]"
    elif e_in and not three_in and not pi_in:
        tier, reason = 1, f"center CI [{lo:.2f},{hi:.2f}] includes e, excludes 3 and pi"
    else:
        tier, reason = 2, f"center CI [{lo:.2f},{hi:.2f}] does not isolate e (3 in CI={three_in})"

    return ModelComparison(
        log_ml=log_ml,
        bayes_factors_vs_best=bf_vs_best,
        best_model=best,
        bf_e_vs_3=bf_e_3,
        bf_e_vs_pi=bf_e_pi,
        mode=mode,
        mode_ci=(lo, hi),
        tier=tier,
        tier_reason=reason,
    )
