import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "..", "biology"))

from nodes import engineered_node, classification_node
from controls_analysis import dispersion_contrast


def _tight_node(center):
    # a stand-in self-organizing node: tight branching ratio
    class N:
        name = "tight"
        ratios = center * np.exp(np.random.default_rng(0).normal(0, 0.12, 40))
    return N()


def test_controls_disperse_more_than_self_organizing():
    so = [_tight_node(2.9), _tight_node(3.1)]
    ctrl = [engineered_node(), classification_node()]
    r = dispersion_contrast(so, ctrl)
    assert r.control_cv > r.self_org_cv
    assert r.controls_disperse_more is True
    assert r.brown_forsythe_p < 0.05


def test_control_nodes_excluded_flag():
    assert engineered_node().is_self_organizing is False
    assert classification_node().is_self_organizing is False


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-q"]))
