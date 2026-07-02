"""
Regression tests for the indicator-scale guard (mi/scoring.py).

Before this guard, the normalizers silently divided any input by 100, so a raw
WGI *estimate* (z-score, e.g. rule_of_law=1.53) normalized to 0.0153 and a
negative estimate produced a negative "quality" score. That flipped at least one
case's P1 ordinal (case18 Baltics vs Central Asia) and made single-entity cases
(e.g. Germany) score at the floor. These tests lock in that:
  1. out-of-domain values (negative / >100) hard-fail instead of scoring garbage;
  2. in-range-but-suspicious signatures (WGI <= 3, legacy CPI <= 10) are flagged;
  3. correctly-scaled 0-100 inputs score normally with no warnings.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mi.scoring import (calculate_pillar_scores, detect_scale_issues,
                        normalize_eci, normalize_gdp_ppp, normalize_fsi, score_country)


def test_negative_wgi_hard_fails():
    # A raw WGI estimate (z-score) below zero is impossible on the 0-100 scale.
    with pytest.raises(ValueError, match="rule_of_law=-0.38"):
        calculate_pillar_scores({"rule_of_law": -0.38, "cpi": 31})


def test_over_100_hard_fails():
    with pytest.raises(ValueError, match="out of|outside"):
        calculate_pillar_scores({"gov_effectiveness": 137})


def test_positive_zscore_flagged_not_fatal():
    # 1.53 is in [0,100] so it cannot be auto-rejected, but it is almost
    # certainly a raw estimate (a functioning state is never at the 1.5th
    # percentile). It must be surfaced as a warning.
    hard, soft = detect_scale_issues({"gov_effectiveness": 1.19, "rule_of_law": 1.53})
    assert hard == []
    assert len(soft) == 2
    assert all("suspiciously low" in s for s in soft)


def test_legacy_cpi_flagged():
    hard, soft = detect_scale_issues({"cpi": 4.3})
    assert hard == []
    assert any("legacy" in s and "cpi" in s for s in soft)


def test_clean_0_100_input_no_issues():
    ind = {"gov_effectiveness": 45.45, "rule_of_law": 46.64,
           "regulatory_quality": 46.04, "control_of_corruption": 44.42,
           "cpi": 44.42, "political_stability": 62.58}
    hard, soft = detect_scale_issues(ind)
    assert hard == [] and soft == []
    r = score_country(ind)
    assert r["pillar_scores"]["P1"] is not None
    assert r["scale_warnings"] == []


def test_normalizers_clamped_to_unit_interval():
    # GDP above the ceiling and ECI outside the reference range must not push
    # a pillar out of [0,1] (Luxembourg P4, DR Congo P2 were the real cases).
    assert normalize_gdp_ppp(160000) == 1.0
    assert normalize_eci(3.0) == 1.0 and normalize_eci(-3.0) == 0.0
    assert normalize_fsi(130) == 0.0
    ps = score_country({"gov_effectiveness": 95, "rule_of_law": 95,
                        "regulatory_quality": 95, "gdp_per_capita_ppp": 160000,
                        "resource_rents_pct_gdp": 0, "oda_pct_gni": 0,
                        "eci": -3.0, "rd_pct_gdp": 0.1})["pillar_scores"]
    for k, v in ps.items():
        assert v is None or 0.0 <= v <= 1.0, f"{k}={v} out of [0,1]"


def test_genuine_floor_percentile_scores_with_warning():
    # Sudan 2010 political stability = 0.9th percentile (Darfur) is REAL data on
    # the 0-100 absolute scale, not a mis-entered z-score. It must still score
    # (at the floor), carrying an advisory warning rather than being rejected.
    r = score_country({"political_stability": 0.9, "fsi": 111.0})
    assert r["pillar_scores"]["P5"] is not None
    assert r["pillar_scores"]["P5"] < 0.1  # floor stability, correctly low
    assert len(r["scale_warnings"]) == 1
