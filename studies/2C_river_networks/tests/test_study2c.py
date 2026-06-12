"""Unit tests for Study 2C. Run with: pytest -q  (from the study directory)."""

import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from horton import strahler_orders, stream_counts, horton_rb, measure_basin
from synthetic import random_coalescent_basin, sample_basin_rbs, coalescent_rb_population
from analysis import model_comparison, log_marginal_point, log_marginal_uniform


def test_strahler_simple_y():
    # Two sources (0,1) join at 2, which is the outlet.
    downstream = {0: 2, 1: 2, 2: -1}
    order = strahler_orders(downstream)
    assert order[0] == 1 and order[1] == 1
    assert order[2] == 2                      # two order-1s meet -> order 2


def test_strahler_no_promotion_on_single_tributary():
    # source 0 -> 1 -> 2(outlet); a single chain stays order 1 until a real join
    downstream = {0: 1, 1: 2, 2: -1}
    order = strahler_orders(downstream)
    assert order[0] == order[1] == order[2] == 1


def test_strahler_balanced_binary_three_levels():
    # 4 sources -> 2 junctions -> 1 outlet ; perfectly balanced
    downstream = {0: 4, 1: 4, 2: 5, 3: 5, 4: 6, 5: 6, 6: -1}
    order = strahler_orders(downstream)
    assert order[6] == 3                      # two order-2 streams meet -> 3
    counts = stream_counts(downstream, order)
    assert counts[1] == 4 and counts[2] == 2 and counts[3] == 1
    rb, r2 = horton_rb(counts)
    assert abs(rb - 2.0) < 1e-9               # perfect Rb=2, perfect fit
    assert r2 > 0.999


def test_horton_requires_three_orders():
    downstream = {0: 2, 1: 2, 2: -1}          # only orders {1,2}
    m_counts = stream_counts(downstream, strahler_orders(downstream))
    try:
        horton_rb(m_counts, min_orders=3)
        assert False, "should have raised"
    except ValueError:
        pass


def test_cycle_detection():
    downstream = {0: 1, 1: 0}                  # not a tree
    try:
        strahler_orders(downstream)
        assert False
    except ValueError:
        pass


def test_coalescent_basin_is_valid_tree():
    rng = np.random.default_rng(3)
    basin = random_coalescent_basin(64, rng)
    m = measure_basin(basin, min_orders=3)
    assert m.rb > 1.0
    assert m.max_order >= 3
    # exactly one outlet
    assert sum(1 for d in basin.values() if d == -1) == 1


def test_coalescent_population_does_not_return_e():
    # The random binary sequential-merging topology lands near 3.0, NOT at e.
    # This guards the honesty claim that the pipeline reflects the input
    # topology rather than magically returning e (2.718).
    rb = coalescent_rb_population(200, seed=7)
    assert 2.7 < np.median(rb) < 3.4


def test_model_comparison_recovers_true_center_e():
    rb = sample_basin_rbs(4000, center=math.e, log_sd=0.15, seed=11)
    mc = model_comparison(rb, n_boot=1, seed=11)
    best_point = max(["e", "3", "pi", "2", "4"], key=lambda nm: mc.log_ml[nm])
    assert best_point == "e"
    assert mc.bf_e_vs_3 > 1.0                  # e favoured over 3 when truth is e


def test_model_comparison_recovers_true_center_3():
    rb = sample_basin_rbs(4000, center=3.0, log_sd=0.15, seed=12)
    mc = model_comparison(rb, n_boot=1, seed=12)
    best_point = max(["e", "3", "pi", "2", "4"], key=lambda nm: mc.log_ml[nm])
    assert best_point == "3"
    assert mc.bf_e_vs_3 < 1.0                  # 3 favoured over e when truth is 3


def test_uniform_null_wins_on_uniform_data():
    rng = np.random.default_rng(5)
    rb = rng.uniform(1.5, 7.5, size=3000)
    assert log_marginal_uniform(rb) > log_marginal_point(rb, math.e)


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-q"]))
