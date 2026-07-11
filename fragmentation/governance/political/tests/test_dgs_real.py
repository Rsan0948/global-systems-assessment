"""Tests for the REAL DGS->instability result. Uses the committed real-panel
and sensitivity caches (no network, no raw downloads, no pycountry needed)."""

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
RESULTS = os.path.join(HERE, "results")

from dgs import fit_dgs


def _panel():
    raw = json.load(open(os.path.join(RESULTS, "dgs_panel_real.json")))
    return {k: np.array(v) for k, v in raw.items() if k != "_meta"}, raw.get("_meta", {})


def test_real_panel_shape():
    panel, meta = _panel()
    assert meta["n_countries"] >= 100
    assert panel["instability"].size > 500
    assert 0.05 < meta["base_rate"] < 0.6
    assert set(np.unique(panel["instability"])) <= {0, 1}


def test_dgs_is_null_on_real_data():
    # the calibrated test HAS power (detects planted synthetic effects, see
    # integration); on real data it returns a null -> a genuine negative result.
    panel, _ = _panel()
    r = fit_dgs(panel)
    assert r.lr_p > 0.05                       # DGS adds nothing beyond controls
    assert abs(r.auc_gain) < 0.05              # no out-of-sample lift


def test_sensitivity_null_is_robust():
    sens = json.load(open(os.path.join(RESULTS, "dgs_sensitivity.json")))
    assert len(sens) >= 4
    assert all(s["lr_p"] > 0.05 for s in sens)  # null across every operationalization
