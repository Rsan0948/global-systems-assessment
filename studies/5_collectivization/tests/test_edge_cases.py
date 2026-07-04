"""Edge-case and error-handling tests across all modules.

Covers: invalid inputs, boundary values, empty collections, NaN propagation,
single-element arrays, and degenerate case configurations.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import math
import pytest
import numpy as np

from collectivization_case import CaseProfile
from feature_vector import (
    validate, hamming, classify, flip_count, flipped_features,
    integration_depth, functional_breadth, legitimacy_flips,
    N_FEATURES, TYPE_TEMPLATES, FEATURE_NAMES,
)
from failure_catalog import (
    active_failures, patched_failures, unpatched_failures,
    new_vulnerabilities, diagnostic, FAILURE_MODES,
)
from ratchet import score_case as ratchet_score, analyze as ratchet_analyze
from form_shift import score_case as fs_score, analyze as fs_analyze, _net_patch_score
from cycle_engine import timing_intensity, analyze as cycle_analyze


def _case(**kw):
    defaults = dict(
        name="edge", is_control=False,
        pre_frag_year=1800, frag_peak_year=1820,
        first_integration_year=1840, post_collect_year=1860,
        features_pre=[0] * 15, features_post=[0] * 15,
        units_pre=10, units_peak=5, units_post=10,
        pop_pre=1e6, pop_post=2e6,
        gdp_growth_pre=0.01, gdp_growth_post=0.02,
        frag_duration_years=20, conflicts_per_decade=2.0,
        collect_speed_years=20, durability_years=100,
        gdp_series={}, vdem_series={},
    )
    defaults.update(kw)
    return CaseProfile(**defaults)


# =========================================================================
# feature_vector edge cases
# =========================================================================

class TestFeatureVectorEdges:

    def test_validate_empty_list(self):
        with pytest.raises(ValueError):
            validate([])

    def test_validate_too_long(self):
        with pytest.raises(ValueError):
            validate([0] * 16)

    def test_validate_negative_values(self):
        with pytest.raises(ValueError):
            validate([-1] + [0] * 14)

    def test_validate_float_values(self):
        with pytest.raises(ValueError):
            validate([0.5] + [0] * 14)

    def test_hamming_all_zeros(self):
        assert hamming([0] * 15, [0] * 15) == 0

    def test_hamming_all_ones(self):
        assert hamming([1] * 15, [1] * 15) == 0

    def test_classify_all_zeros(self):
        name, dist = classify([0] * 15)
        assert isinstance(name, str)
        assert dist >= 0

    def test_classify_all_ones(self):
        name, dist = classify([1] * 15)
        assert isinstance(name, str)
        assert dist >= 0

    def test_flip_count_max(self):
        a = [0] * 15
        b = [1] * 15
        assert flip_count(a, b) == 15

    def test_flipped_features_returns_all(self):
        a = [0] * 15
        b = [1] * 15
        ff = flipped_features(a, b)
        assert len(ff) == 15
        assert set(ff) == set(FEATURE_NAMES)

    def test_flipped_features_returns_none(self):
        a = [0] * 15
        assert flipped_features(a, list(a)) == []

    def test_integration_depth_all_ones(self):
        assert integration_depth([1] * 15) == 6

    def test_integration_depth_all_zeros(self):
        assert integration_depth([0] * 15) == 0

    def test_functional_breadth_all_ones(self):
        assert functional_breadth([1] * 15) == 4

    def test_functional_breadth_all_zeros(self):
        assert functional_breadth([0] * 15) == 1

    def test_legitimacy_flips_max(self):
        a = [0] * 15
        b = [1] * 15
        assert legitimacy_flips(a, b) == 5

    def test_classify_deterministic(self):
        vec = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        r1 = classify(vec)
        r2 = classify(vec)
        assert r1 == r2

    def test_type_templates_all_valid(self):
        for name, template in TYPE_TEMPLATES.items():
            validate(template)


# =========================================================================
# failure_catalog edge cases
# =========================================================================

class TestFailureCatalogEdges:

    def test_all_zeros_active_failures(self):
        result = active_failures([0] * 15)
        assert isinstance(result, list)

    def test_all_ones_active_failures(self):
        result = active_failures([1] * 15)
        assert isinstance(result, list)

    def test_diagnostic_identical_vectors(self):
        vec = [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
        d = diagnostic(vec, vec)
        assert d["patched"] == []
        assert d["new_vulnerabilities"] == []
        assert d["active_pre"] == d["active_post"]

    def test_diagnostic_complete_reversal(self):
        a = [0] * 15
        b = [1] * 15
        d = diagnostic(a, b)
        assert isinstance(d["active_pre"], list)
        assert isinstance(d["active_post"], list)

    def test_unpatched_subset_of_active_pre(self):
        pre = [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
        post = [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1]
        d = diagnostic(pre, post)
        for f in d["unpatched"]:
            assert f in d["active_pre"]

    def test_new_vulnerabilities_not_in_active_pre(self):
        pre = [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
        post = [1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1]
        d = diagnostic(pre, post)
        for f in d["new_vulnerabilities"]:
            assert f not in d["active_pre"]

    def test_failure_mode_predicates_consistent(self):
        for fm in FAILURE_MODES:
            assert len(fm.patch_features) > 0
            for idx in fm.trigger_features + fm.trigger_absent + fm.patch_features:
                assert 0 <= idx < 15


# =========================================================================
# ratchet edge cases
# =========================================================================

class TestRatchetEdges:

    def test_zero_units_pre(self):
        case = _case(units_pre=0, units_peak=5, units_post=10)
        s = ratchet_score(case)
        assert math.isnan(s.incorporation_ratio)

    def test_zero_pop_pre(self):
        case = _case(pop_pre=0, pop_post=1e6)
        s = ratchet_score(case)
        assert math.isnan(s.demographic_ratio)

    def test_negative_growth(self):
        case = _case(gdp_growth_pre=0.02, gdp_growth_post=-0.01)
        s = ratchet_score(case)
        assert s.efficiency_burst < 0

    def test_nan_growth(self):
        case = _case(gdp_growth_pre=float("nan"), gdp_growth_post=float("nan"))
        s = ratchet_score(case)
        assert math.isnan(s.efficiency_burst)

    def test_equal_pre_post(self):
        case = _case(
            units_pre=50, units_post=50,
            pop_pre=1e6, pop_post=1e6,
            gdp_growth_pre=0.01, gdp_growth_post=0.01,
            features_pre=[0]*15, features_post=[0]*15,
        )
        s = ratchet_score(case)
        assert s.positive_dims == 0

    def test_analyze_empty_list(self):
        r = ratchet_analyze([])
        assert r.n_cases == 0
        assert r.total_dims == 0

    def test_analyze_only_controls(self):
        cases = [_case(name="c1", is_control=True), _case(name="c2", is_control=True)]
        r = ratchet_analyze(cases)
        assert r.n_cases == 0

    def test_analyze_single_case(self):
        r = ratchet_analyze([_case(name="solo")])
        assert r.n_cases == 1
        assert r.total_dims == 5


# =========================================================================
# form_shift edge cases
# =========================================================================

class TestFormShiftEdges:

    def test_identical_features(self):
        vec = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        case = _case(features_pre=vec, features_post=list(vec))
        s = fs_score(case)
        assert s.flip_count == 0
        assert not s.type_changed
        assert s.legitimacy_flips == 0

    def test_analyze_no_controls(self):
        cases = [_case(name=f"c{i}") for i in range(3)]
        r = fs_analyze(cases)
        assert math.isnan(r.mann_whitney_p)
        assert math.isnan(r.net_patch_p)

    def test_analyze_no_cases(self):
        cases = [_case(name=f"ctrl{i}", is_control=True) for i in range(3)]
        r = fs_analyze(cases)
        assert r.cases_mean_flips == 0.0
        assert math.isnan(r.mann_whitney_p)

    def test_analyze_empty(self):
        r = fs_analyze([])
        assert r.cases_mean_flips == 0.0

    def test_net_patch_score_no_patches_no_vulns(self):
        case = _case(features_pre=[0]*15, features_post=[0]*15)
        s = fs_score(case)
        assert _net_patch_score(s) == 0

    def test_net_patch_score_negative(self):
        pre = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        post = [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
        case = _case(features_pre=pre, features_post=post)
        s = fs_score(case)
        nps = _net_patch_score(s)
        assert isinstance(nps, int)


# =========================================================================
# timing_intensity edge cases
# =========================================================================

class TestTimingIntensityEdges:

    def test_fewer_than_three_cases(self):
        cases = [_case(name="only1"), _case(name="only2")]
        r = timing_intensity(cases)
        assert r.dominant_channel == "insufficient_cases"

    def test_all_identical_values(self):
        cases = [_case(name=f"c{i}", units_peak=50, frag_duration_years=20,
                       conflicts_per_decade=3.0, collect_speed_years=20,
                       durability_years=100) for i in range(5)]
        r = timing_intensity(cases)
        assert isinstance(r.dominant_channel, str)

    def test_controls_excluded(self):
        cases = [
            _case(name="core1", units_peak=10),
            _case(name="core2", units_peak=50),
            _case(name="core3", units_peak=100),
            _case(name="ctrl1", is_control=True, units_peak=999),
        ]
        r = timing_intensity(cases)
        assert r.dominant_channel != "insufficient_cases"


# =========================================================================
# cycle_engine full-pipeline edge cases
# =========================================================================

class TestCycleEngineEdges:

    def test_single_core_no_controls(self):
        cases = [_case(name="solo")]
        result = cycle_analyze(cases)
        assert result.summary["n_core_cases"] == 1
        assert result.summary["n_controls"] == 0

    def test_all_controls(self):
        cases = [_case(name=f"c{i}", is_control=True) for i in range(3)]
        result = cycle_analyze(cases)
        assert result.summary["n_core_cases"] == 0

    def test_empty_cases(self):
        result = cycle_analyze([])
        assert result.summary["n_core_cases"] == 0

    def test_summary_keys_always_present(self):
        cases = [
            _case(name="a"), _case(name="b"), _case(name="c"),
            _case(name="ctrl", is_control=True),
        ]
        result = cycle_analyze(cases)
        required = {"ratchet_supported", "form_shift_supported",
                    "all_types_shifted", "dominant_mechanism_channel",
                    "warning_signals_hit_rate", "n_core_cases", "n_controls"}
        assert required.issubset(result.summary.keys())
