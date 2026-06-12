import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from node import build_node


def test_node_builds_positive_ratios():
    nd = build_node(seed=0)
    assert nd.name == "biology"
    assert np.all(nd.ratios > 0)
    assert nd.ratios.size >= 50
    assert 2.0 < float(np.exp(np.log(nd.ratios).mean())) < 4.0


def test_node_has_gap_for_mechanism_test():
    nd = build_node()
    assert nd.gap is not None
    assert 0.5 < nd.gap < 1.5          # interior - interface ~ 1


def test_null_sampler_runs():
    nd = build_node()
    rng = np.random.default_rng(0)
    x = nd.null_sampler(50, rng)
    assert x.size == 50 and np.all(x > 0)


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-q"]))
