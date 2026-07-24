"""Verdict-discipline tests for the census assessor (catalog.py).

Pins the lawfulness gate: concentrated AND beats-null, with honest
symmetric reporting of the failure modes (trivial vs dispersed), and
the fact that LAWFUL includes systems displaced BELOW their null
(the corporate-splits lesson). Synthetic null samplers only; no data.
"""

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "census"))

from catalog import assess_system  # noqa: E402


def _normal_sampler(mu, sigma):
    def sampler(n, rng):
        return rng.normal(mu, sigma, size=n)
    return sampler


def test_concentrated_but_trivial_is_not_lawful():
    rng = np.random.default_rng(7)
    ratios = rng.normal(2.2, 0.05, size=60)
    e = assess_system("synthetic-trivial", ratios, _normal_sampler(2.2, 0.05),
                      n_sims=500, seed=7)
    assert e.concentrated is True
    assert e.beats_null is False
    assert e.lawful is False
    assert "trivial" in e.verdict


def test_concentrated_and_beats_null_is_lawful_above():
    rng = np.random.default_rng(11)
    ratios = rng.normal(4.5, 0.2, size=50)
    e = assess_system("synthetic-lawful", ratios, _normal_sampler(2.5, 0.2),
                      n_sims=500, seed=11)
    assert e.concentrated is True
    assert e.beats_null is True
    assert e.lawful is True
    assert e.direction == "above"
    assert "LAWFUL" in e.verdict


def test_lawful_includes_displacement_below_null():
    """Corporate-splits lesson: below the null is still lawful."""
    rng = np.random.default_rng(13)
    ratios = rng.normal(2.0, 0.1, size=50)
    e = assess_system("synthetic-below", ratios, _normal_sampler(3.5, 0.2),
                      n_sims=500, seed=13)
    assert e.lawful is True
    assert e.direction == "below"


def test_dispersed_system_is_not_lawful_even_beating_null():
    rng = np.random.default_rng(17)
    ratios = np.exp(rng.normal(np.log(4.0), 0.7, size=60))  # CV ~ 0.79
    e = assess_system("synthetic-dispersed", ratios, _normal_sampler(2.0, 0.1),
                      n_sims=500, seed=17)
    assert e.beats_null is True
    assert e.concentrated is False
    assert e.lawful is False
    assert "dispersed" in e.verdict


def test_nonpositive_ratios_filtered():
    e = assess_system("synthetic-filter", [2.0, 2.1, 0.0, -3.0, 2.2],
                      _normal_sampler(2.1, 0.1), n_sims=100, seed=3)
    assert e.n == 3


def test_single_ratio_does_not_crash_and_is_not_lawful():
    e = assess_system("synthetic-n1", [3.0], _normal_sampler(3.0, 0.1),
                      n_sims=100, seed=5)
    assert e.n == 1
    assert e.lawful is False


def test_determinism_same_seed_same_result():
    rng = np.random.default_rng(23)
    ratios = rng.normal(3.8, 0.25, size=40)
    a = assess_system("det", ratios, _normal_sampler(2.9, 0.2), n_sims=300, seed=23)
    b = assess_system("det", ratios, _normal_sampler(2.9, 0.2), n_sims=300, seed=23)
    assert (a.factor, a.null_factor, a.beats_null_p) == (b.factor, b.null_factor, b.beats_null_p)
