"""Public scoring contract tests for MI v3.3."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mi.constants import CANONICAL_WEIGHTS, MI_CANONICAL_WEIGHTING, MI_MODEL_VERSION  # noqa: E402
from mi.scoring import get_score_band, get_tier, resolve_weights, score_country  # noqa: E402


def test_public_version_and_weights_are_explicit():
    assert MI_MODEL_VERSION == "v3.3"
    assert MI_CANONICAL_WEIGHTING == "equal"
    assert CANONICAL_WEIGHTS == {f"P{i}": 0.20 for i in range(1, 6)}
    assert resolve_weights() == CANONICAL_WEIGHTS
    assert resolve_weights("canonical_equal") == CANONICAL_WEIGHTS
    assert resolve_weights("v2_equal") == CANONICAL_WEIGHTS


def test_unknown_weighting_mode_fails_loudly():
    with pytest.raises(ValueError, match="unknown weighting mode"):
        resolve_weights("typo")


@pytest.mark.parametrize(
    ("score", "number", "name"),
    [
        (0.80, 1, "Highly Modernized"),
        (0.60, 2, "Durable"),
        (0.40, 3, "Mixed"),
        (0.20, 4, "Fragile"),
        (0.00, 5, "Floor"),
    ],
)
def test_public_score_bands(score, number, name):
    assert get_score_band(score) == {"band": number, "name": name}
    assert get_tier(score) == {"tier": number, "name": name}


def test_score_country_reports_canonical_contract():
    indicators = {
        "gov_effectiveness": 80,
        "rule_of_law": 80,
        "regulatory_quality": 80,
        "control_of_corruption": 80,
        "gii": 80,
        "education_index": 0.8,
        "life_expectancy_index": 0.8,
        "gdp_per_capita_ppp": 30000,
        "resource_rents": 5,
        "oda": 1,
        "political_stability": 80,
        "fsi": 24,
    }
    result = score_country(indicators)
    assert result["model_version"] == "v3.3"
    assert result["weighting_mode"] == "equal"
    assert result["weights_used"] == CANONICAL_WEIGHTS
    assert result["score_band"]["band"] == result["tier"]["tier"]
    assert set(result["sensitivity"]) == {
        "v2_equal",
        "v2_timevarying",
        "v1",
        "archived_hand_v0",
    }
    assert result["sensitivity"]["v2_equal"] == result["mi_score"]
