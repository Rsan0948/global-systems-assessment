"""
Regression tests for the indicator-scale guard and normalizer clamps
(mi/scoring.py). Ported from the main-branch fix so this engine is equally
robust to the WGI z-score-vs-percentile mis-scale that flipped case ordinals,
plus the P4/P5 over-range bug (GDP/capita above the ceiling pushed P4 > 1).
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mi.scoring import (calculate_pillar_scores, detect_scale_issues,
                        normalize_gdp_ppp, normalize_fsi, score_country)


def test_negative_wgi_hard_fails():
    with pytest.raises(ValueError, match="rule_of_law=-0.38"):
        calculate_pillar_scores({"rule_of_law": -0.38, "cpi": 31})


def test_over_100_hard_fails():
    with pytest.raises(ValueError, match="out of|outside"):
        calculate_pillar_scores({"gov_effectiveness": 137})


def test_positive_zscore_flagged_not_fatal():
    hard, soft = detect_scale_issues({"gov_effectiveness": 1.19, "rule_of_law": 1.53})
    assert hard == []
    assert len(soft) == 2 and all("suspiciously low" in s for s in soft)


def test_legacy_cpi_flagged():
    hard, soft = detect_scale_issues({"cpi": 4.3})
    assert hard == [] and any("legacy" in s for s in soft)


def test_clean_0_100_input_no_issues():
    ind = {"gov_effectiveness": 45.45, "rule_of_law": 46.64,
           "regulatory_quality": 46.04, "control_of_corruption": 44.42,
           "political_stability": 62.58}
    hard, soft = detect_scale_issues(ind)
    assert hard == [] and soft == []


def test_gdp_ppp_clamped_to_one():
    # GDP/capita above the ceiling (Luxembourg/Singapore/Qatar) must not push
    # P4 > 1. Previously normalize_gdp_ppp(160000) returned 1.011.
    assert normalize_gdp_ppp(160000) == 1.0
    assert normalize_gdp_ppp(500000) == 1.0
    assert 0.0 <= normalize_gdp_ppp(50000) <= 1.0


def test_fsi_clamped_nonnegative():
    assert normalize_fsi(120) == 0.0
    assert normalize_fsi(130) == 0.0  # beyond max must not go negative


def test_all_pillars_in_unit_interval():
    # A very rich, very stable country must still keep every pillar in [0,1].
    ind = {"gov_effectiveness": 95, "rule_of_law": 95, "regulatory_quality": 95,
           "control_of_corruption": 95, "political_stability": 95,
           "gdp_per_capita_ppp": 160000, "resource_rents_pct_gdp": 0,
           "oda_pct_gni": 0, "eci": 2.5, "education_index": 0.99,
           "life_expectancy_index": 0.99, "fsi": 15}
    ps = score_country(ind)["pillar_scores"]
    for k, v in ps.items():
        assert v is None or 0.0 <= v <= 1.0, f"{k}={v} out of [0,1]"
