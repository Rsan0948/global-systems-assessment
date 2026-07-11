import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dgs import fit_dgs, _auc
from panel import make_panel
import numpy as np


def test_dgs_detected_when_present():
    res = fit_dgs(make_panel(beta_dgs_true=0.7, seed=1))
    assert res.beta_dgs > 0.2          # right sign, nontrivial magnitude
    assert res.lr_p < 0.01             # LR test detects it through controls
    assert res.auc_gain > 0            # out-of-sample improvement


def test_dgs_null_when_absent():
    res = fit_dgs(make_panel(beta_dgs_true=0.0, seed=1))
    assert res.lr_p > 0.05             # no false positive


def test_auc_basic():
    y = np.array([0, 0, 1, 1])
    s = np.array([0.1, 0.2, 0.8, 0.9])
    assert _auc(y, s) == 1.0
    assert _auc(y, -s) == 0.0


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-q"]))
