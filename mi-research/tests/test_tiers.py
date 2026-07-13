"""Regression + robustness tests for the multi-tier framework and the political-signal /
convergence work built this session. Offline: reads committed artifacts + exercises the pure
functions in convergence_lib. No network. Run: pytest tests/test_tiers.py -q
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts" / "robustness"))
import convergence_lib as L  # noqa: E402

DATA = ROOT / "data"


def _load(p):
    return json.loads((DATA / p).read_text())


# ----------------------------------------------------------------- pure functions
def test_auc_roc_bounds_and_separation():
    # perfect separation -> 1.0; inverted -> 0.0; identical -> 0.5
    assert L.auc_roc([1, 2, 3, 4], [0, 0, 1, 1]) == pytest.approx(1.0)
    assert L.auc_roc([4, 3, 2, 1], [0, 0, 1, 1]) == pytest.approx(0.0)
    assert L.auc_roc([1, 1, 1, 1], [0, 0, 1, 1]) == pytest.approx(0.5)
    # monotone in signal strength
    a = L.auc_roc([1, 2, 3, 4, 5, 6], [0, 0, 0, 1, 1, 1])
    assert a > 0.9


def test_zscore_properties():
    z = L.zscore([1, 2, 3, 4, 5])
    assert abs(float(np.mean(z))) < 1e-9
    assert float(np.std(z)) == pytest.approx(1.0, abs=1e-9)
    # degenerate (all equal) does not crash / no NaN
    z0 = L.zscore([3, 3, 3])
    assert not np.any(np.isnan(z0))


def test_logit_fit_recovers_signal():
    rng = np.random.default_rng(0)
    n = 300
    x = rng.normal(size=n)
    y = (1 / (1 + np.exp(-(1.5 * x))) > rng.uniform(size=n)).astype(float)
    X = np.column_stack([np.ones(n), x])
    b, auc, _ = L.logit_fit(X, y)
    assert b[1] > 0.5          # positive coefficient recovered
    assert auc > 0.7           # discriminates


# ----------------------------------------------------------------- Finding 14 reproduction
def test_convergence_lib_reproduces_finding14_decomposition():
    """The committed struct/wealth domestic curve must be reproduced exactly by the lib."""
    pts = L.epoch_decomp(L.domestic_label_fn())
    committed = {p["year"]: p for p in L.committed_decomp()}
    matched = 0
    for p in pts:
        if p["struct_auc"] is None:
            continue
        c = committed.get(p["year"])
        if not c or c.get("struct_auc") is None:
            continue
        assert p["struct_auc"] == pytest.approx(c["struct_auc"], abs=1e-3), p["year"]
        assert p["wealth_auc"] == pytest.approx(c["wealth_auc"], abs=1e-3), p["year"]
        matched += 1
    assert matched >= 15
    # the Finding-14 endpoints
    ep = {p["year"]: p for p in L.committed_decomp()}
    assert ep[1816]["struct_auc"] == pytest.approx(0.4444, abs=1e-3)
    assert ep[1996]["wealth_auc"] == pytest.approx(0.7788, abs=1e-3)


# ----------------------------------------------------------------- snapshot integrity
@pytest.fixture(scope="module")
def snapshots():
    four = {r["iso"]: r for r in _load("political/four_tier_snapshot.json")}
    five = {r["iso"]: r for r in _load("political/five_tier_snapshot.json")}
    six = {r["iso"]: r for r in _load("political/six_tier_snapshot.json")}
    return four, five, six


def test_snapshot_completeness(snapshots):
    four, five, six = snapshots
    assert len(six) == 156
    assert len(four) == len(five) == len(six)


def test_snapshot_value_ranges(snapshots):
    _, _, six = snapshots
    for iso, r in six.items():
        for k in ["V1", "V2", "V3", "T4", "T6"]:
            assert 0 <= r[k] <= 100, (iso, k, r[k])
        if r["T5"] is not None:
            assert 0 <= r["T5"] <= 100, (iso, r["T5"])


def test_cross_artifact_consistency(snapshots):
    """V1-V4 must agree across the four/five/six-tier snapshots; T5 across five/six."""
    four, five, six = snapshots
    common = set(four) & set(five) & set(six)
    assert len(common) >= 150
    for iso in common:
        for k in ["V1", "V2", "V3", "T4"]:
            vals = [four[iso][k], five[iso][k], six[iso][k]]
            assert max(vals) - min(vals) <= 0.6, (iso, k, vals)
        # T5 present/absent must agree, and match where present
        a, b = five[iso]["T5"], six[iso]["T5"]
        assert (a is None) == (b is None), iso
        if a is not None:
            assert abs(a - b) <= 0.6, iso


def test_headline_anchors_stable(snapshots):
    """Pin the values that back the reported analysis so a regression is caught."""
    _, _, six = snapshots
    us = six["USA"]
    assert us["V1"] == pytest.approx(77.9, abs=1.0)   # capable
    assert us["T4"] == pytest.approx(56.3, abs=1.5)   # Loaded Spring scarring
    nl = six["NLD"]
    assert nl["V3"] < 25 and nl["T4"] < 25 and (nl["T5"] or 0) < 5  # clean on risk axes
    assert nl["T6"] < 10                               # minimum spark density (bottom decile)
    assert six["IRQ"]["T6"] > 85                       # Iraq = max spark density


def test_scarring_directionality(snapshots):
    """T4 must flag the deeply conflict-scarred states well above the clean core."""
    _, _, six = snapshots
    scarred = np.mean([six[i]["T4"] for i in ["IRQ", "MMR", "ETH", "SDN", "RWA"]])
    clean = np.mean([six[i]["T4"] for i in ["NLD", "DNK", "NOR", "CHE", "SWE"]])
    assert scarred - clean > 40


def test_flickering_cases_present(snapshots):
    """Tier 5 must flag the imminent-tipping democracies (Poland/Korea/Romania high, calm core ~0)."""
    _, _, six = snapshots
    for i in ["POL", "KOR", "ROU"]:
        assert six[i]["T5"] is not None and six[i]["T5"] >= 60, i
    for i in ["DNK", "SWE", "DEU", "JPN"]:
        assert (six[i]["T5"] or 0) <= 5, i


# ----------------------------------------------------------------- results-artifact invariants
def test_political_signal_gate_committed():
    """political_test committed result: numerator adds over structural on the modern outcomes."""
    r = _load("political/political_test.json")["T2_gate"]
    bs = r["backslide"]; rep = r["repression_worsen"]
    assert bs["auc_struct+numerator"] > bs["auc_structural"]      # numerator helps backsliding
    assert bs["increment"] >= 0.03
    assert rep["increment"] >= 0.03


def test_csd_trigger_signal_committed():
    """trigger_hunt committed result: variance is a positive early-warning for backsliding."""
    r = _load("political/trigger_hunt.json")["backsliding_libdem"]
    assert r["var"]["AUC"] > 0.6                     # variance discriminates
    assert r["var"]["event_mean"] > r["var"]["control_mean"]   # rises before rupture
    assert r["ar1"]["AUC"] > 0.5


def test_tier4_operationalizes_conflict_trap():
    """tier4 committed: adds over V1+V3 and mediates the raw prior-conflict binary."""
    r = _load("political/tier4_scarring.json")
    assert r["T4_1"]["increment"] >= 0.03
    assert r["optimal_halflife"] in (15, 25, 50, 75)
    # raw binary absorbed by S (|z| of raw drops when S added)
    assert abs(r["T4_6"]["raw_with_S_z"]) < abs(r["T4_6"]["raw_alone_z"])


def test_v2_construct_validity_committed():
    """v2_hypotheses committed: cross-model ρ >= 0.90 on Level/Equity/Combined (H4 gate)."""
    h4 = _load("v2/v2_hypotheses.json")["H4_cross_model"]
    for dim in ["L", "E", "score"]:
        assert h4[dim]["min_rho"] >= 0.90, dim
