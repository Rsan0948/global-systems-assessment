import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from corporate_node import build_node
from survival import fit_hazard, make_firm_panel


def test_node_builds():
    nd = build_node()
    assert nd.name == "corporate"
    assert np.all(nd.ratios > 0)
    assert nd.gap is not None


def test_hazard_detects_complexity_effect():
    res = fit_hazard(make_firm_panel(beta_true=0.6, seed=1))
    assert res.hazard_ratio > 1.0
    assert res.lr_p < 0.01


def test_hazard_null_when_absent():
    res = fit_hazard(make_firm_panel(beta_true=0.0, seed=1))
    assert res.lr_p > 0.05


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-q"]))
