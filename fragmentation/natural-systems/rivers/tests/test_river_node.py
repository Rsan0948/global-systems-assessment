"""Tests for the REAL rivers node (river_node.py). Uses the committed Rb
caches in results/; no network or raw HydroRIVERS download required."""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import river_node as rn
from horton import measure_basin


def test_fast_coalescent_is_a_valid_tree():
    rng = np.random.default_rng(0)
    d = rn._fast_coalescent_basin(60, rng)
    assert list(d.values()).count(-1) == 1            # exactly one outlet
    m = measure_basin(d, min_orders=3)                # measurable by Horton
    assert 1.5 < m.rb < 8.0


def test_real_rb_loads_and_is_positive():
    rb = rn.real_rb("na", rn.PRIMARY_MIN_ORDERS)
    assert rb.size > 100
    assert np.all(rb > 1.0)
    # higher order cut is a subset -> fewer basins
    assert rn.real_rb("na", 5).size < rb.size


def test_sensitivity_table_monotone_in_n():
    s = rn.sensitivity_table("na")
    ns = [s[mo]["n_basins"] for mo in (3, 4, 5, 6)]
    assert ns == sorted(ns, reverse=True)             # n shrinks as cut tightens
    assert all(2.0 < s[mo]["geom_mean"] < 5.0 for mo in (3, 4, 5, 6))


def test_null_sampler_shape_and_positive():
    sampler = rn.make_null_sampler(4)
    rng = np.random.default_rng(1)
    x = sampler(500, rng)
    assert x.shape == (500,)
    assert np.all(x > 1.0)
    # null sits near random-topology ~3, below the observed rivers value
    assert np.exp(np.log(x).mean()) < np.exp(np.log(rn.real_rb("na", 4)).mean())
