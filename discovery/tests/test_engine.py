"""Tests for the discovery engine. Run: pytest -q (from discovery/)."""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from heterogeneity import analyze
from ladder import assess, split, confirm
import scenarios


def test_homogeneous_domains_low_heterogeneity():
    # all domains at the same value -> Q not significant, low I^2
    data = {d: 2.718 * np.exp(np.random.default_rng(i).normal(0, 0.1, 80))
            for i, d in enumerate(["a", "b", "c", "d"])}
    res = analyze(data)
    assert res.q_p > 0.05
    assert res.i_squared < 0.4
    assert 2.5 < res.pooled_ratio < 2.95


def test_spread_domains_high_heterogeneity():
    centers = {"a": 2.2, "b": 2.8, "c": 3.4, "d": 4.0}
    data = {d: c * np.exp(np.random.default_rng(ord(d)).normal(0, 0.08, 80))
            for d, c in centers.items()}
    res = analyze(data)
    assert res.q_p < 1e-3
    assert res.i_squared > 0.8


def test_universal_world_reaches_rung3_e():
    v = assess(scenarios.universal_world(), null_samplers=scenarios.null_samplers(),
               n_sims=200, seed=7)
    assert v.rung == 3
    assert "e" in v.constants_in_ci
    assert "3" not in v.constants_in_ci      # CI must exclude the rival

def test_domain_specific_world_reaches_rung1():
    v = assess(scenarios.domain_specific_world(), null_samplers=scenarios.null_samplers(),
               n_sims=200, seed=7)
    assert v.rung == 1


def test_trivial_world_reaches_rung0():
    v = assess(scenarios.trivial_world(), null_samplers=scenarios.null_samplers(),
               n_sims=200, seed=7)
    assert v.rung == 0


def test_confirm_passes_on_consistent_holdout():
    uni = scenarios.universal_world(seed=11)
    nulls = scenarios.null_samplers()
    disc_data, conf_data = split(uni, holdout=["trees", "vasculature"])
    disc_v = assess(disc_data, null_samplers={k: nulls[k] for k in disc_data}, n_sims=150, seed=7)
    out = confirm(disc_v, conf_data, null_samplers={k: nulls[k] for k in conf_data}, n_sims=150, seed=7)
    assert out["ci_overlap"] is True


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-q"]))
