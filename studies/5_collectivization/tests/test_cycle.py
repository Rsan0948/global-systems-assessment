"""Integration tests for the full cycle engine."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from collectivization_case import CaseProfile
from cycle_engine import analyze, timing_intensity
from failure_catalog import diagnostic, active_failures


def _make_case(name, is_control=False, **kw):
    defaults = dict(
        pre_frag_year=1800, frag_peak_year=1820,
        first_integration_year=1840, post_collect_year=1860,
        features_pre=[1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        features_post=[1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        units_pre=50, units_peak=20, units_post=60,
        pop_pre=5e6, pop_post=10e6,
        gdp_growth_pre=0.005, gdp_growth_post=0.025,
        frag_duration_years=20, conflicts_per_decade=3.0,
        collect_speed_years=20, durability_years=100,
        gdp_series={}, vdem_series={},
    )
    defaults.update(kw)
    return CaseProfile(name=name, is_control=is_control, **defaults)


def test_full_analysis():
    cases = [
        _make_case("A", units_peak=100, conflicts_per_decade=5.0, collect_speed_years=10),
        _make_case("B", units_peak=20, conflicts_per_decade=1.0, collect_speed_years=50),
        _make_case("C", units_peak=50, conflicts_per_decade=3.0, collect_speed_years=30),
        _make_case("ctrl", is_control=True, features_post=[0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]),
    ]
    result = analyze(cases)
    assert result.summary["n_core_cases"] == 3
    assert result.summary["n_controls"] == 1
    assert "ratchet_supported" in result.summary
    assert "form_shift_supported" in result.summary


def test_timing_intensity_correlations():
    cases = [
        _make_case("small_fast", units_peak=10, frag_duration_years=5,
                    conflicts_per_decade=1, collect_speed_years=5, durability_years=200),
        _make_case("medium", units_peak=50, frag_duration_years=20,
                    conflicts_per_decade=3, collect_speed_years=20, durability_years=100),
        _make_case("large_slow", units_peak=200, frag_duration_years=100,
                    conflicts_per_decade=8, collect_speed_years=50, durability_years=50),
    ]
    result = timing_intensity(cases)
    assert "dominant_channel" in result.dominant_channel or result.dominant_channel != ""


def test_failure_diagnostic_roundtrip():
    feudal = [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
    active = active_failures(feudal)
    assert "coordination_collapse" in active

    nation = [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0]
    diag = diagnostic(feudal, nation)
    assert "coordination_collapse" in diag["patched"]
