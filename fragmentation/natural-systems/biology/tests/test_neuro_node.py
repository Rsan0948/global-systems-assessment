"""Tests for the REAL biology nodes (neuro_node.py) + SWC parsing. Uses the
committed NeuroMorpho Rb caches in results/; no network required."""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import neuro_node as nn
from fetch_neuromorpho import swc_to_downstream


def test_swc_parse_root_and_topology():
    # 3-point SWC: node 1 = soma (root), 2 and 3 are children of 1
    swc = "# comment\n1 1 0 0 0 1 -1\n2 3 1 0 0 1 1\n3 3 0 1 0 1 1\n"
    d = swc_to_downstream(swc)
    assert d == {1: -1, 2: 1, 3: 1}          # parent pointer -> downstream; root -> -1


def test_available_cell_types_excludes_null_pool():
    cts = nn.available_cell_types()
    assert "null_pool" not in cts
    assert len(cts) >= 5                      # the six fetched sub-domains


def test_real_rb_positive_and_concentrated():
    for ct in nn.available_cell_types():
        rb = nn.real_rb(ct, nn.PRIMARY_MIN_ORDERS)
        assert rb.size >= 2
        assert np.all(rb > 1.0)
        assert rb.std(ddof=1) / rb.mean() < 0.6   # individually concentrated


def test_build_nodes_and_null_sampler():
    nodes = nn.build_nodes()
    assert len(nodes) >= 5
    n0 = nodes[0]
    assert n0.name.startswith("neuro_")
    assert n0.is_self_organizing
    # real allometric exponents now wired (rung-4); gap is a finite number
    assert n0.interior_exp is not None and n0.gap is not None
    rng = np.random.default_rng(0)
    x = n0.null_sampler(300, rng)
    assert x.shape == (300,) and np.all(x > 1.0)
