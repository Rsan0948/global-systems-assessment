"""
The triviality control -- the single most important guard in the whole program.

We already have direct evidence that clustering near 3-4 is available "for
free": neutral random binary topology lands at ~3, Shreve's random-topology
model at ~4, with no optimization law anywhere (see natural-systems/rivers). So a finding
of the form "self-organizing systems cluster near k" is, by itself, possibly a
combinatorial tautology rather than a theorem.

This module quantifies the part of the signal that survives ABOVE a
mechanism-free baseline. For each domain you supply a `null_sampler` -- a
callable that returns mechanism-free simulated ratio measurements for that
domain (random topology / random merging / size-only scaling). We then:

  1. run the same heterogeneity analysis on many null draws to get the null
     distribution of (pooled value, between-domain tau), and
  2. report where the OBSERVED statistics sit relative to that null:
       * per-domain: does the observed ratio differ from the domain's own
         trivial-null ratio?  (is the domain doing something non-trivial?)
       * cross-domain: is the observed between-domain spread SMALLER than the
         null's?  (do real domains coincide more than independent trivial
         processes would -- i.e. is there a non-trivial universal pull?)
       * is the observed pooled value displaced from the null pooled value?
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from heterogeneity import analyze

NullSampler = Callable[[int, np.random.Generator], np.ndarray]


@dataclass
class TrivialNullResult:
    obs_pooled: float
    null_pooled_mean: float
    null_pooled_ci: tuple[float, float]
    pooled_displacement_p: float        # P(null pooled as far from null-center as observed)
    obs_tau: float
    null_tau_mean: float
    null_tau_ci: tuple[float, float]
    tau_below_null_p: float             # P(null tau <= observed tau): small => real is MORE concentrated
    per_domain_z: dict                  # observed vs domain's own null, in null-SD units


def run_null(
    null_samplers: dict[str, NullSampler],
    n_per_domain: dict[str, int],
    n_sims: int = 500,
    seed: int = 0,
) -> tuple[np.ndarray, np.ndarray, dict]:
    """Simulate the trivial-null world `n_sims` times; return arrays of pooled
    ratio and tau, plus per-domain null ratio samples."""
    rng = np.random.default_rng(seed)
    pooled, taus = [], []
    per_domain_vals: dict[str, list[float]] = {k: [] for k in null_samplers}
    for _ in range(n_sims):
        data = {}
        for name, sampler in null_samplers.items():
            x = np.asarray(sampler(n_per_domain[name], rng), dtype=float)
            data[name] = x
            per_domain_vals[name].append(float(np.exp(np.log(x).mean())))
        res = analyze(data)
        pooled.append(res.pooled_ratio)
        taus.append(res.tau)
    return np.array(pooled), np.array(taus), {k: np.array(v) for k, v in per_domain_vals.items()}


def compare(
    observed,                       # HeterogeneityResult
    null_samplers: dict[str, NullSampler],
    n_sims: int = 500,
    seed: int = 0,
) -> TrivialNullResult:
    n_per = {e.name: e.n for e in observed.domains}
    null_pooled, null_tau, null_domain = run_null(null_samplers, n_per, n_sims, seed)

    nc = float(np.median(null_pooled))
    disp_p = float(np.mean(np.abs(null_pooled - nc) >= abs(observed.pooled_ratio - nc)))
    tau_below_p = float(np.mean(null_tau <= observed.obs_tau)) if hasattr(observed, "obs_tau") \
        else float(np.mean(null_tau <= observed.tau))

    per_z = {}
    for e in observed.domains:
        nd = null_domain[e.name]
        sd = nd.std(ddof=1) or 1e-9
        per_z[e.name] = float((e.ratio_mean - nd.mean()) / sd)

    return TrivialNullResult(
        obs_pooled=float(observed.pooled_ratio),
        null_pooled_mean=nc,
        null_pooled_ci=(float(np.percentile(null_pooled, 2.5)), float(np.percentile(null_pooled, 97.5))),
        pooled_displacement_p=disp_p,
        obs_tau=float(observed.tau),
        null_tau_mean=float(np.median(null_tau)),
        null_tau_ci=(float(np.percentile(null_tau, 2.5)), float(np.percentile(null_tau, 97.5))),
        tau_below_null_p=tau_below_p,
        per_domain_z=per_z,
    )
