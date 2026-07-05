"""
Tests for the bridge module.

Validates:
1. Loading matrix properties (dimensions, range, sign consistency)
2. Type template projections (ordering, separation)
3. Normalization bounds
4. Displacement calculations
5. Failure-safeguard consistency
6. Organicity properties
7. Validation pipeline runs
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import pytest

from pillar_loading import (
    LOADING_MATRIX, N_FEATURES, N_PILLARS, PILLAR_NAMES,
    TYPE_TEMPLATES, FEATURE_NAMES,
    project, project_normalized, project_type, displacement,
    displacement_magnitude, profile_shape,
    _RAW_MIN, _RAW_MAX,
)
from failure_bridge import (
    is_failure_active, active_failures, expected_safeguards,
    expected_weak_pillars, failure_bridge_diagnostic,
    FAILURE_SAFEGUARD_MAP, _FAILURE_PREDICATES,
)
from organicity import (
    organicity_score, imposed_features, inherited_features,
    expected_fragmentation_cv, organicity_diagnostic,
)
from trajectory import trajectory_profile, pathway_displacement_signature
from validate import validate_all, interpret_residuals, MI_REFERENCE_SCORES, POST_FEATURE_VECTORS


# =========================================================================
# Loading matrix properties
# =========================================================================

class TestLoadingMatrix:
    def test_dimensions(self):
        assert LOADING_MATRIX.shape == (N_FEATURES, N_PILLARS)

    def test_values_bounded(self):
        assert np.all(LOADING_MATRIX >= -1.0)
        assert np.all(LOADING_MATRIX <= 1.0)

    def test_no_all_zero_rows(self):
        for i in range(N_FEATURES):
            assert not np.all(LOADING_MATRIX[i] == 0), (
                f"feature {FEATURE_NAMES[i]} has all-zero loadings")

    def test_feature_names_count(self):
        assert len(FEATURE_NAMES) == N_FEATURES

    def test_pillar_names_count(self):
        assert len(PILLAR_NAMES) == N_PILLARS

    def test_hereditary_succession_negative_p1(self):
        assert LOADING_MATRIX[1, 0] < 0

    def test_popular_sovereignty_positive_p1(self):
        assert LOADING_MATRIX[8, 0] > 0

    def test_independent_militaries_negative_p5(self):
        assert LOADING_MATRIX[2, 4] < 0

    def test_central_army_positive_p5(self):
        assert LOADING_MATRIX[13, 4] > 0

    def test_shared_currency_positive_p4(self):
        assert LOADING_MATRIX[4, 3] > 0

    def test_free_movement_goods_positive_p4(self):
        assert LOADING_MATRIX[11, 3] > 0

    def test_shared_legal_code_positive_p1(self):
        assert LOADING_MATRIX[5, 0] > 0

    def test_elected_leadership_positive_p1(self):
        assert LOADING_MATRIX[9, 0] > 0


# =========================================================================
# Type template projections
# =========================================================================

class TestTypeProfiles:
    def test_all_templates_project(self):
        for tname in TYPE_TEMPLATES:
            profile = project_type(tname)
            assert len(profile) == N_PILLARS
            for p in PILLAR_NAMES:
                assert 0.0 <= profile[p] <= 1.0, (
                    f"{tname}.{p} = {profile[p]} out of bounds")

    def test_federal_republic_high_p1(self):
        profile = project_type("federal_republic")
        assert profile["P1"] > 0.7

    def test_feudal_order_low_overall(self):
        profile = project_type("feudal_order")
        mean_val = np.mean(list(profile.values()))
        assert mean_val < 0.3

    def test_federal_beats_feudal_on_all_pillars(self):
        fed = project_type("federal_republic")
        feudal = project_type("feudal_order")
        for p in PILLAR_NAMES:
            assert fed[p] > feudal[p], (
                f"federal_republic should beat feudal_order on {p}")

    def test_personal_empire_moderate_p4(self):
        profile = project_type("personal_empire")
        assert 0.3 < profile["P4"] < 0.9

    def test_city_state_system_low_p5(self):
        profile = project_type("city_state_system")
        assert profile["P5"] < 0.3

    def test_supranational_union_high_p4(self):
        profile = project_type("supranational_union")
        assert profile["P4"] > 0.5


# =========================================================================
# Normalization
# =========================================================================

class TestNormalization:
    def test_raw_min_max_shape(self):
        assert _RAW_MIN.shape == (N_PILLARS,)
        assert _RAW_MAX.shape == (N_PILLARS,)

    def test_raw_max_exceeds_min(self):
        for i in range(N_PILLARS):
            assert _RAW_MAX[i] > _RAW_MIN[i], (
                f"pillar {PILLAR_NAMES[i]}: max ({_RAW_MAX[i]}) <= "
                f"min ({_RAW_MIN[i]})")

    def test_normalization_produces_01(self):
        for tname, template in TYPE_TEMPLATES.items():
            normed = project_normalized(template)
            for p in PILLAR_NAMES:
                assert 0.0 <= normed[p] <= 1.0, (
                    f"{tname}.{p} = {normed[p]} outside [0,1]")


# =========================================================================
# Displacement
# =========================================================================

class TestDisplacement:
    def test_zero_displacement_same_vector(self):
        v = [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1]
        d = displacement(v, v)
        for p in PILLAR_NAMES:
            assert d[p] == 0.0

    def test_zero_magnitude_same_vector(self):
        v = [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1]
        assert displacement_magnitude(v, v) == 0.0

    def test_displacement_sign(self):
        feudal = list(TYPE_TEMPLATES["feudal_order"])
        federal = list(TYPE_TEMPLATES["federal_republic"])
        d = displacement(feudal, federal)
        assert d["P1"] > 0
        assert d["P5"] > 0

    def test_magnitude_positive(self):
        feudal = list(TYPE_TEMPLATES["feudal_order"])
        federal = list(TYPE_TEMPLATES["federal_republic"])
        mag = displacement_magnitude(feudal, federal)
        assert mag > 0

    def test_displacement_antisymmetric(self):
        a = list(TYPE_TEMPLATES["feudal_order"])
        b = list(TYPE_TEMPLATES["federal_republic"])
        d_ab = displacement(a, b)
        d_ba = displacement(b, a)
        for p in PILLAR_NAMES:
            assert abs(d_ab[p] + d_ba[p]) < 1e-10


# =========================================================================
# Profile shape
# =========================================================================

class TestProfileShape:
    def test_shape_categories(self):
        for tname in TYPE_TEMPLATES:
            shape = profile_shape(TYPE_TEMPLATES[tname])
            for p in PILLAR_NAMES:
                assert shape[p] in ("strong", "moderate", "weak")

    def test_federal_republic_mostly_strong(self):
        shape = profile_shape(TYPE_TEMPLATES["federal_republic"])
        strong_count = sum(1 for v in shape.values() if v == "strong")
        assert strong_count >= 3


# =========================================================================
# Failure bridge
# =========================================================================

class TestFailureBridge:
    def test_feudal_has_coordination_collapse(self):
        feudal = list(TYPE_TEMPLATES["feudal_order"])
        assert is_failure_active("coordination_collapse", feudal)

    def test_federal_no_coordination_collapse(self):
        federal = list(TYPE_TEMPLATES["federal_republic"])
        assert not is_failure_active("coordination_collapse", federal)

    def test_personal_empire_has_center_predation(self):
        empire = list(TYPE_TEMPLATES["personal_empire"])
        assert is_failure_active("center_predation", empire)

    def test_all_failure_modes_have_mappings(self):
        mapped = {m.failure_mode for m in FAILURE_SAFEGUARD_MAP}
        defined = set(_FAILURE_PREDICATES.keys())
        assert mapped == defined

    def test_expected_safeguards_nonempty_for_active_failures(self):
        feudal = list(TYPE_TEMPLATES["feudal_order"])
        safeguards = expected_safeguards(feudal)
        assert len(safeguards) > 0

    def test_diagnostic_structure(self):
        feudal = list(TYPE_TEMPLATES["feudal_order"])
        federal = list(TYPE_TEMPLATES["federal_republic"])
        diag = failure_bridge_diagnostic(feudal, federal)
        required_keys = {"pre_failures", "post_failures", "patched",
                         "new_vulnerabilities", "persistent",
                         "pre_expected_safeguards", "post_expected_safeguards",
                         "safeguards_resolved", "safeguards_introduced",
                         "pre_weak_pillars", "post_weak_pillars"}
        assert required_keys.issubset(set(diag.keys()))

    def test_feudal_to_federal_patches_coordination(self):
        feudal = list(TYPE_TEMPLATES["feudal_order"])
        federal = list(TYPE_TEMPLATES["federal_republic"])
        diag = failure_bridge_diagnostic(feudal, federal)
        assert "coordination_collapse" in diag["patched"]


# =========================================================================
# Organicity
# =========================================================================

class TestOrganicity:
    def test_identical_vectors_score_one(self):
        v = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        assert organicity_score(v, v) == 1.0

    def test_opposite_vectors_score_zero(self):
        v = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        w = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
        assert organicity_score(v, w) == 0.0

    def test_organicity_bounded(self):
        for tname_a in TYPE_TEMPLATES:
            for tname_b in TYPE_TEMPLATES:
                org = organicity_score(
                    TYPE_TEMPLATES[tname_a], TYPE_TEMPLATES[tname_b])
                assert 0.0 <= org <= 1.0

    def test_expected_cv_at_extremes(self):
        assert expected_fragmentation_cv(1.0) == pytest.approx(0.213, abs=0.01)
        assert expected_fragmentation_cv(0.0) == pytest.approx(5.767, abs=0.01)

    def test_expected_cv_monotonic(self):
        assert expected_fragmentation_cv(0.8) < expected_fragmentation_cv(0.2)

    def test_diagnostic_structure(self):
        a = list(TYPE_TEMPLATES["feudal_order"])
        b = list(TYPE_TEMPLATES["federal_republic"])
        diag = organicity_diagnostic(a, b, FEATURE_NAMES)
        assert "organicity" in diag
        assert "imposed_count" in diag
        assert "expected_fragmentation_cv" in diag
        assert diag["imposed_count"] + diag["inherited_count"] == N_FEATURES


# =========================================================================
# Trajectory
# =========================================================================

class TestTrajectory:
    def test_trajectory_profile_structure(self):
        feudal = list(TYPE_TEMPLATES["feudal_order"])
        federal = list(TYPE_TEMPLATES["federal_republic"])
        t = trajectory_profile("test", feudal, federal, "construction")
        assert t.name == "test"
        assert t.pathway == "construction"
        assert len(t.pre_profile) == N_PILLARS
        assert len(t.post_profile) == N_PILLARS
        assert t.magnitude > 0
        assert 0.0 <= t.organicity <= 1.0

    def test_restoration_near_zero_magnitude(self):
        v = list(TYPE_TEMPLATES["personal_empire"])
        t = trajectory_profile("test", v, v, "restoration")
        assert t.magnitude == 0.0
        assert t.organicity == 1.0


# =========================================================================
# Validation
# =========================================================================

class TestValidation:
    def test_validate_runs(self):
        result = validate_all()
        assert "per_country" in result
        assert "aggregate" in result
        assert result["aggregate"]["n_countries"] > 0

    def test_cross_type_correlation_positive(self):
        result = validate_all()
        cross = result["aggregate"]["cross_type"]
        assert cross["cross_type_correlation_pearson"] > 0

    def test_shape_correlation_median_positive(self):
        result = validate_all()
        assert result["aggregate"]["median_shape_correlation"] > 0

    def test_rmse_bounded(self):
        result = validate_all()
        assert result["aggregate"]["rmse"] < 0.5

    def test_all_reference_countries_validated(self):
        result = validate_all()
        for country in MI_REFERENCE_SCORES:
            assert country in result["per_country"]

    def test_interpret_residuals_runs(self):
        result = validate_all()
        interp = interpret_residuals(result)
        assert len(interp) > 0

    def test_capacity_realization_present(self):
        result = validate_all()
        for country, data in result["per_country"].items():
            assert "capacity_realization" in data
            assert "mean_realization" in data
            for p in PILLAR_NAMES:
                assert data["capacity_realization"][p] > 0

    def test_shape_correlation_per_country(self):
        result = validate_all()
        for country, data in result["per_country"].items():
            assert "shape_correlation" in data

    def test_cross_type_groups_match_unique_vectors(self):
        result = validate_all()
        cross = result["aggregate"]["cross_type"]
        unique_fvs = set(tuple(v) for v in POST_FEATURE_VECTORS.values())
        assert cross["n_unique_types"] == len(unique_fvs)

    def test_within_type_spread_for_federal_republics(self):
        result = validate_all()
        within = result["aggregate"]["cross_type"]["within_type"]
        assert len(within) > 0
        for label, data in within.items():
            assert data["n"] > 1
            assert data["mean_actual_std"] > 0
