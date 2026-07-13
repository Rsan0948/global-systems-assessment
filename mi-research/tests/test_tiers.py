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
    assert us["T4"] == pytest.approx(50.0, abs=1.5)   # scarring (audit H4: S2 now percentile-normalized)
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
    """political_test T2 gate (audit M5 fix): 50-seed repeated CV with a CI. The numerator layer
    adds over structural for backsliding & repression with a CI lower bound above 0; conflict does
    not (structure already predicts conflict). Encodes the honest, reproducible result."""
    r = _load("political/political_test.json")["T2_gate"]
    bs = r["backslide"]; rep = r["repression_worsen"]
    assert bs["auc_struct+numerator"] > bs["auc_structural"]     # numerator helps backsliding
    assert bs["increment_mean"] >= 0.05
    assert bs["increment_CI"][0] > 0 and bs["gate_pass(CI>0)"]   # robust to reshuffling
    assert bs["frac_seeds_positive"] >= 0.95
    assert rep["increment_CI"][0] > 0 and rep["gate_pass(CI>0)"]
    # conflict is honestly NOT passed by the numerator (structure already carries it)
    assert not r["conflict_1224"]["gate_pass(CI>0)"]


def test_political_signal_partial_survivors_committed():
    """political_test T1 (audit M4 fix): net of P1+logGDP, the CORE V3 signals survive
    (anocracy+cso->backslide, pts/prior-conflict/youth->conflict) while the confounded marginals
    (internet, ethnic_excl, food_imp) drop out."""
    o = _load("political/political_test.json")
    surv = {(t["pred"], t["out"]) for t in o["T1_survivors_partial"]}
    assert ("anocracy", "backslide") in surv
    assert ("cso", "backslide") in surv
    assert ("prior_conflict", "conflict_1224") in surv
    # confounded-by-capacity marginals must NOT be in the partial survivor set
    assert ("internet", "conflict_1224") not in surv
    assert ("food_imp", "repression_worsen") not in surv


def test_csd_corrected_honest_signal():
    """CSD, audit-corrected (H1/H2/M1/M2). Within-country variance elevation before backsliding
    SURVIVES (country-clustered CI excludes 0), but the theory-canonical AR1 indicator is NULL
    and the lead gradient is NOT a clean monotonic countdown. This is the corrected, weaker,
    honest finding that replaces the 'monotonic 3.6x->7.4x, AUC 0.689' claim."""
    r = _load("political/csd_corrected.json")
    assert r["within_country_survives"] and r["within_country_CI"][0] > 0   # real within-country
    assert r["within_country_mean_logratio"] > 0
    assert r["ar1_auc"] < 0.60          # AR1 does NOT discriminate — the honest null
    assert r["lead_monotone"] is False  # elevated but not a clean accelerating countdown


def test_tier4_operationalizes_conflict_trap():
    """tier4 (audit H4/H5 fix): S2 percentile-normalized, missing V3 covariates mean-imputed,
    50-seed repeated CV. Still adds over V1+V3 and still mediates the raw prior-conflict binary."""
    r = _load("political/tier4_scarring.json")
    assert r["T4_1"]["increment"] >= 0.03
    assert r["T4_1"]["pass"]
    assert r["optimal_halflife"] in (15, 25, 50, 75)
    # raw binary absorbed by S (|z| of raw drops when S added)
    assert abs(r["T4_6"]["raw_with_S_z"]) < abs(r["T4_6"]["raw_alone_z"])


def test_deep_political_oof_below_insample():
    """deep_political (audit C1 fix): the headline is OUT-OF-FOLD, and OOF increments must be
    below the (inflated) in-sample ones. Guards against a regression back to resubstitution AUC."""
    rows = _load("political/deep_political.json")
    for OUT in ("backslide", "conflict"):
        oof = [r[OUT]["increment"] for r in rows
               if OUT in r and r[OUT].get("increment") is not None and r[OUT]["n"] >= 25]
        ins = [r[OUT]["increment_insample"] for r in rows
               if OUT in r and r[OUT].get("increment_insample") is not None and r[OUT]["n"] >= 25]
        assert oof and ins
        assert float(np.mean(oof)) < float(np.mean(ins))   # OOF is the honest, smaller number
    # backsliding numerator signal is weak-positive OOF, not the old inflated +0.131
    bs = [r["backslide"]["increment"] for r in rows
          if "backslide" in r and r["backslide"].get("increment") is not None and r["backslide"]["n"] >= 25]
    assert 0.0 < float(np.mean(bs)) < 0.12


def test_tier6_oof_present_and_honest():
    """tier6 (audit C1 fix): the six-tier headline AUC is reported OUT-OF-FOLD and is materially
    below the in-sample number (which mechanically rises with predictors). T6 still adds over T5
    out-of-fold."""
    r = _load("political/tier6_auc.json")
    assert r["out_of_fold"]["six_tier"] < r["insample"]["six_tier"]
    assert r["out_of_fold"]["six_tier"] > 0.55            # still beats chance
    assert r["out_of_fold"]["T6_increment"] > 0          # spark density adds over criticality OOF


def test_v2_construct_validity_committed():
    """v2_hypotheses committed: cross-model ρ >= 0.90 on Level/Equity/Combined (H4 gate)."""
    h4 = _load("v2/v2_hypotheses.json")["H4_cross_model"]
    for dim in ["L", "E", "score"]:
        assert h4[dim]["min_rho"] >= 0.90, dim
