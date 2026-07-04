"""Tests for form_shift.py -- the form-shift hypothesis."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from collectivization_case import CaseProfile
from form_shift import score_case, analyze


def _make_case(name, is_control, features_pre, features_post):
    return CaseProfile(
        name=name, is_control=is_control,
        pre_frag_year=1800, frag_peak_year=1810,
        first_integration_year=1830, post_collect_year=1850,
        features_pre=features_pre, features_post=features_post,
        units_pre=10, units_peak=5, units_post=1,
        pop_pre=1e6, pop_post=2e6,
        gdp_growth_pre=0.01, gdp_growth_post=0.02,
        frag_duration_years=10, conflicts_per_decade=2.0,
        collect_speed_years=20, durability_years=100,
    )


def test_type_change_detected():
    feudal = [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
    nation = [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0]
    s = score_case(_make_case("test", False, feudal, nation))
    assert s.type_changed
    assert s.flip_count >= 8


def test_no_change_detected():
    vec = [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    s = score_case(_make_case("test", False, vec, vec))
    assert not s.type_changed
    assert s.flip_count == 0


def test_failure_patching():
    feudal = [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
    nation = [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0]
    s = score_case(_make_case("test", False, feudal, nation))
    assert len(s.failure_diagnostic["patched"]) > 0


def test_cases_vs_controls():
    feudal = [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
    nation = [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0]
    frag = [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]

    core = _make_case("core", False, feudal, nation)
    ctrl = _make_case("ctrl", True, feudal, frag)
    result = analyze([core, ctrl])
    assert result.cases_mean_flips > result.controls_mean_flips
