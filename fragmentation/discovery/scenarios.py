"""
Three synthetic multi-domain worlds used to CALIBRATE the discovery engine.

The point is not to study these data -- it is to prove the instrument returns
the right verdict when we know the ground truth:

  * universal_world      -> a single law (all domains share value e)   => rung 3
  * domain_specific_world-> many laws (each domain lawful, values differ)=> rung 1
  * trivial_world        -> no law (domains == their mechanism-free null)=> rung 0

Each world ships with the SAME per-domain trivial-null samplers, so the engine's
triviality control is exercised identically across worlds.
"""

from __future__ import annotations

import numpy as np

DOMAINS = ["rivers", "lungs", "firms", "polities", "trees", "vasculature"]

# Mechanism-free baseline center for each domain (random-topology-like, ~3-4),
# i.e. what each domain would show with NO optimization law.
NULL_CENTERS = {"rivers": 3.9, "lungs": 3.4, "firms": 3.6,
                "polities": 3.2, "trees": 4.1, "vasculature": 3.5}
NULL_LOG_SD = 0.15

# Real characteristic values when there ARE domain-specific laws (distinct,
# and mostly displaced from the trivial baselines above).
DOMAIN_SPECIFIC_CENTERS = {"rivers": 2.2, "lungs": 2.6, "firms": 3.0,
                           "polities": 3.4, "trees": 3.8, "vasculature": 2.4}

E = float(np.e)


def _lognormal_sampler(center: float, log_sd: float):
    def sampler(n: int, rng: np.random.Generator) -> np.ndarray:
        return center * np.exp(rng.normal(0.0, log_sd, size=n))
    return sampler


def null_samplers() -> dict:
    """Per-domain mechanism-free samplers (the triviality control)."""
    return {d: _lognormal_sampler(NULL_CENTERS[d], NULL_LOG_SD) for d in DOMAINS}


def _make_world(centers, log_sd: float, n_per: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    return {d: centers[d] * np.exp(rng.normal(0.0, log_sd, size=n_per)) for d in DOMAINS}


def universal_world(n_per: int = 80, log_sd: float = 0.12, seed: int = 1) -> dict:
    return _make_world({d: E for d in DOMAINS}, log_sd, n_per, seed)


def domain_specific_world(n_per: int = 80, log_sd: float = 0.10, seed: int = 2) -> dict:
    return _make_world(DOMAIN_SPECIFIC_CENTERS, log_sd, n_per, seed)


def trivial_world(n_per: int = 80, seed: int = 3) -> dict:
    """Domains drawn from their own trivial-null samplers => no law."""
    rng = np.random.default_rng(seed)
    samplers = null_samplers()
    return {d: samplers[d](n_per, rng) for d in DOMAINS}
