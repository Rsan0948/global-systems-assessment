"""Tests for ratchet.py -- the scope ratchet hypothesis."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from collectivization_case import CaseProfile
from ratchet import score_case, analyze


def _make_case(name="test", is_control=False, **overrides):
    defaults = dict(
        pre_frag_year=1800, frag_peak_year=1810,
        first_integration_year=1830, post_collect_year=1850,
        features_pre=[1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        features_post=[1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        units_pre=100, units_peak=50, units_post=120,
        pop_pre=10_000_000, pop_post=15_000_000,
        gdp_growth_pre=0.005, gdp_growth_post=0.020,
        frag_duration_years=10, conflicts_per_decade=2.0,
        collect_speed_years=20, durability_years=100,
    )
    defaults.update(overrides)
    return CaseProfile(name=name, is_control=is_control, **defaults)


def test_score_positive():
    case = _make_case(units_post=120, pop_post=15_000_000, gdp_growth_post=0.02)
    s = score_case(case)
    assert s.positive_dims >= 3
    assert s.incorporation_ratio > 1.0
    assert s.demographic_ratio > 1.0
    assert s.efficiency_burst > 0


def test_score_negative():
    case = _make_case(units_post=50, pop_post=5_000_000, gdp_growth_post=-0.01)
    s = score_case(case)
    assert s.positive_dims <= 3


def test_analyze_separates_controls():
    core = _make_case("core", is_control=False)
    ctrl = _make_case("ctrl", is_control=True)
    result = analyze([core, ctrl])
    assert result.n_cases == 1
    assert "core" in result.per_case
    assert "ctrl" not in result.per_case


def test_analyze_sign_test():
    cases = [_make_case(f"c{i}", gdp_growth_post=0.03) for i in range(5)]
    result = analyze(cases)
    assert result.total_positive > result.total_dims / 2
