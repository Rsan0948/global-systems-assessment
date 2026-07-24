"""Tests for treekit.rb_per_root — the parent-map -> Horton-Rb reducer
used for languages, admin hierarchies, and other tree-topology systems.
"""

import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "census", "systems"))
sys.path.insert(0, os.path.join(HERE, "..", "natural-systems", "rivers"))

from treekit import rb_per_root  # noqa: E402


def _perfect_binary_parent_map(order_k, offset=0):
    n_nodes = 2 ** order_k - 1
    parent = {offset: None}
    for i in range(1, n_nodes):
        parent[offset + i] = offset + (i - 1) // 2
    return parent


def test_perfect_binary_tree_gives_rb_two():
    out = rb_per_root(_perfect_binary_parent_map(5), min_orders_floor=3, min_nodes=6)
    assert len(out) == 1
    rb, max_order = out[0]
    assert rb == pytest.approx(2.0, abs=1e-6)
    assert max_order == 5


def test_small_tree_skipped():
    parent = {0: None, 1: 0, 2: 1, 3: 2}
    assert rb_per_root(parent, min_orders_floor=3, min_nodes=6) == []


def test_comb_tree_skipped_too_few_orders():
    parent = {0: None}
    for i in range(1, 6):
        parent[i] = i - 1
    for i in range(6):
        parent[100 + i] = i
    assert rb_per_root(parent, min_orders_floor=3, min_nodes=6) == []


def test_multiple_roots_measured_independently():
    parent = {}
    parent.update(_perfect_binary_parent_map(5, offset=0))
    parent.update(_perfect_binary_parent_map(4, offset=1000))
    out = rb_per_root(parent, min_orders_floor=3, min_nodes=6)
    assert len(out) == 2
    assert all(rb == pytest.approx(2.0, abs=1e-6) for rb, _ in out)
    assert sorted(mo for _, mo in out) == [4, 5]
