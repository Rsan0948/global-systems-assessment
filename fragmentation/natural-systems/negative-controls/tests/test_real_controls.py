"""Tests for the REAL negative-control nodes (real_controls.py). Uses the
committed NCBI taxonomy fan-out cache; no network required."""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import real_controls as rc
from controls_analysis import dispersion_contrast


def test_engineered_spans_orders_of_magnitude():
    r = np.asarray(rc.engineered_node().ratios, float)
    assert r.min() <= 5 and r.max() >= 500            # real design params 2 -> ~1000+
    assert r.std(ddof=1) / r.mean() > 0.8             # high dispersion


def test_classification_is_real_taxonomy_and_highly_dispersed():
    node = rc.classification_node()
    r = np.asarray(node.ratios, float)
    assert r.size > 1000                              # real taxonomy fan-out sample
    assert np.all(r >= 2)                             # branching points only
    assert r.std(ddof=1) / r.mean() > 2.0             # CV far above any self-org node


def test_controls_disperse_more_than_tight_self_org():
    # two deliberately tight "self-organizing" stand-ins (CV ~ rivers/biology)
    rng = np.random.default_rng(0)
    so = [type("N", (), {"name": "a", "ratios": 3.5 * np.exp(rng.normal(0, 0.18, 200))})(),
          type("N", (), {"name": "b", "ratios": 3.0 * np.exp(rng.normal(0, 0.18, 200))})()]
    controls = [rc.engineered_node(), rc.classification_node()]
    res = dispersion_contrast(so, controls)
    assert res.controls_disperse_more
    assert res.control_cv > res.self_org_cv
    assert res.brown_forsythe_p < 1e-6
