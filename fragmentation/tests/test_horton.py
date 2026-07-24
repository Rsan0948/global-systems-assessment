"""Known-value tests for the shared Strahler/Horton instrument.

The fragmentation leg's demonstrated claim (rivers Rb 4.55 +/- 0.24, the
grown-vs-designed dispersion dial) rests entirely on horton.py. These
tests pin its math against analytically known trees: a perfect binary
tree of Strahler order k has exactly N_w = 2^(k-w) streams per order,
so the Horton regression must return Rb = 2 with r^2 = 1.
"""

import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
RIVERS = os.path.join(HERE, "..", "natural-systems", "rivers")
sys.path.insert(0, RIVERS)

from horton import strahler_orders, stream_counts, horton_rb, measure_basin  # noqa: E402


def perfect_binary_downstream(order_k):
    """Perfect binary tree of Strahler order k (2^(k-1) leaves, 2^k - 1 nodes)."""
    n_nodes = 2 ** order_k - 1
    ds = {0: -1}
    for i in range(1, n_nodes):
        ds[i] = (i - 1) // 2
    return ds


def test_perfect_binary_orders_and_counts():
    ds = perfect_binary_downstream(5)
    order = strahler_orders(ds)
    assert max(order.values()) == 5
    counts = stream_counts(ds, order)
    assert counts == {1: 16, 2: 8, 3: 4, 4: 2, 5: 1}


def test_perfect_binary_rb_is_exactly_two():
    m = measure_basin(perfect_binary_downstream(5), min_orders=3)
    assert m.rb == pytest.approx(2.0, rel=1e-9)
    assert m.r_squared == pytest.approx(1.0, abs=1e-12)
    assert m.max_order == 5
    assert m.n_nodes == 31


def test_horton_rb_regression_exact_on_perfect_counts():
    rb, r2 = horton_rb({1: 32, 2: 16, 3: 8, 4: 4, 5: 2, 6: 1})
    assert rb == pytest.approx(2.0, rel=1e-9)
    assert r2 == pytest.approx(1.0, abs=1e-12)


def test_min_orders_enforced():
    with pytest.raises(ValueError):
        horton_rb({1: 4, 2: 1}, min_orders=3)


def test_comb_tree_has_too_few_orders():
    """A maximally asymmetric (comb) tree is order 2 throughout -> excluded."""
    ds = {0: -1}
    for i in range(1, 6):
        ds[i] = i - 1          # internal chain
    for i in range(6):
        ds[100 + i] = i        # one leaf hanging off each internal node
    with pytest.raises(ValueError):
        measure_basin(ds, min_orders=3)


def test_cycle_rejected():
    with pytest.raises(ValueError):
        strahler_orders({0: 1, 1: 0})


def test_unknown_downstream_rejected():
    with pytest.raises(ValueError):
        strahler_orders({0: 7})
