"""Regression and data-stability tests.

Pin the results of the 10-case dataset to catch unintended changes to
scoring logic, failure predicates, or type assignment. If a test here breaks,
it means an upstream module changed behavior -- that may be intentional, but
must be verified.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json
import math
import pytest

from collectivization_case import CaseProfile
from feature_vector import classify, TYPE_TEMPLATES, N_FEATURES, hamming
from failure_catalog import active_failures, diagnostic
from ratchet import score_case as ratchet_score
from form_shift import score_case as fs_score

HERE = os.path.dirname(os.path.abspath(__file__))
CASES_DIR = os.path.join(HERE, "..", "cases")


def _load_case(filename):
    path = os.path.join(CASES_DIR, filename)
    with open(path) as f:
        d = json.load(f)
    gdp = {int(y): v for y, v in d.get("gdp_series", {}).items()}
    vdem = {int(y): v for y, v in d.get("vdem_series", {}).items()}
    return CaseProfile(
        name=d["name"], is_control=d["is_control"],
        pre_frag_year=d["pre_frag_year"], frag_peak_year=d["frag_peak_year"],
        first_integration_year=d["first_integration_year"],
        post_collect_year=d["post_collect_year"],
        features_pre=d["features_pre"], features_post=d["features_post"],
        units_pre=d["units_pre"], units_peak=d["units_peak"],
        units_post=d["units_post"],
        pop_pre=d["pop_pre"], pop_post=d["pop_post"],
        gdp_growth_pre=d.get("gdp_growth_pre") or float("nan"),
        gdp_growth_post=d.get("gdp_growth_post") or float("nan"),
        frag_duration_years=d["frag_duration_years"],
        conflicts_per_decade=d["conflicts_per_decade"],
        collect_speed_years=d["collect_speed_years"],
        durability_years=d["durability_years"],
        gdp_series=gdp, vdem_series=vdem,
    )


# =========================================================================
# Type-assignment stability: every case must classify the same way
# =========================================================================

EXPECTED_TYPES = {
    "germany.json": ("feudal_order", "federal_republic"),
    "italy.json": ("city_state_system", "unitary_nation_state"),
    "united_states.json": ("supranational_union", "federal_republic"),
    "european_union.json": ("city_state_system", "supranational_union"),
    "china.json": ("feudal_order", "personal_empire"),
    "japan.json": ("feudal_order", "personal_empire"),
    "ctrl_middle_east_post_ottoman.json": ("personal_empire", "city_state_system"),
    "ctrl_sub_saharan_africa.json": ("colonial_imperial", "city_state_system"),
    "ctrl_post_soviet.json": ("ideological_party", "city_state_system"),
    "ctrl_greek_poleis.json": ("colonial_imperial", "city_state_system"),
}


@pytest.mark.parametrize("filename,expected", list(EXPECTED_TYPES.items()))
def test_type_assignment_stability(filename, expected):
    case = _load_case(filename)
    pre_type, _ = classify(case.features_pre)
    post_type, _ = classify(case.features_post)
    assert pre_type == expected[0], f"{filename}: pre-type {pre_type} != {expected[0]}"
    assert post_type == expected[1], f"{filename}: post-type {post_type} != {expected[1]}"


# =========================================================================
# Feature vector stability: vectors must not change
# =========================================================================

EXPECTED_FEATURES = {
    "germany.json": {
        "pre": [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
        "post": [1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    },
    "united_states.json": {
        "pre": [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        "post": [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    },
}


@pytest.mark.parametrize("filename", list(EXPECTED_FEATURES.keys()))
def test_feature_vector_stability(filename):
    case = _load_case(filename)
    expected = EXPECTED_FEATURES[filename]
    assert case.features_pre == expected["pre"], f"{filename} pre-features changed"
    assert case.features_post == expected["post"], f"{filename} post-features changed"


# =========================================================================
# Ratchet dimension stability
# =========================================================================

def test_germany_ratchet_dimensions():
    case = _load_case("germany.json")
    s = ratchet_score(case)
    assert s.positive_dims == 4
    assert s.demographic_ratio > 1.5
    assert s.integration_depth_post > s.integration_depth_pre

def test_usa_ratchet_dimensions():
    case = _load_case("united_states.json")
    s = ratchet_score(case)
    assert s.positive_dims == 5
    assert s.incorporation_ratio > 1.0

def test_japan_ratchet_dimensions():
    case = _load_case("japan.json")
    s = ratchet_score(case)
    assert s.demographic_ratio > 3.0
    assert s.integration_depth_post == 6


# =========================================================================
# Form-shift stability
# =========================================================================

def test_germany_form_shift():
    case = _load_case("germany.json")
    s = fs_score(case)
    assert s.type_changed
    assert s.flip_count == 11
    assert "coordination_collapse" in s.failure_diagnostic["patched"]
    assert "competitive_destruction" in s.failure_diagnostic["patched"]
    assert len(s.failure_diagnostic["new_vulnerabilities"]) == 0


def test_italy_form_shift():
    case = _load_case("italy.json")
    s = fs_score(case)
    assert s.type_changed
    assert s.flip_count == 15
    assert s.legitimacy_flips == 5


def test_usa_form_shift():
    case = _load_case("united_states.json")
    s = fs_score(case)
    assert s.type_changed
    assert s.flip_count == 4
    assert len(s.failure_diagnostic["new_vulnerabilities"]) == 0


def test_ctrl_middle_east_introduces_vulnerabilities():
    case = _load_case("ctrl_middle_east_post_ottoman.json")
    s = fs_score(case)
    assert "coordination_collapse" in s.failure_diagnostic["new_vulnerabilities"]
    assert "competitive_destruction" in s.failure_diagnostic["new_vulnerabilities"]


def test_ctrl_post_soviet_introduces_vulnerabilities():
    case = _load_case("ctrl_post_soviet.json")
    s = fs_score(case)
    assert "coordination_collapse" in s.failure_diagnostic["new_vulnerabilities"]


# =========================================================================
# Failure catalog stability
# =========================================================================

def test_feudal_order_active_failures():
    feudal = list(TYPE_TEMPLATES["feudal_order"])
    active = active_failures(feudal)
    assert "coordination_collapse" in active
    assert "competitive_destruction" in active


def test_federal_republic_active_failures():
    federal = list(TYPE_TEMPLATES["federal_republic"])
    active = active_failures(federal)
    assert "coordination_collapse" not in active
    assert "competitive_destruction" not in active


def test_personal_empire_active_failures():
    empire = list(TYPE_TEMPLATES["personal_empire"])
    active = active_failures(empire)
    assert "center_predation" in active


def test_city_state_system_active_failures():
    css = list(TYPE_TEMPLATES["city_state_system"])
    active = active_failures(css)
    assert "coordination_collapse" in active


# =========================================================================
# Template integrity
# =========================================================================

def test_all_templates_distinct():
    templates = list(TYPE_TEMPLATES.values())
    for i in range(len(templates)):
        for j in range(i + 1, len(templates)):
            assert templates[i] != templates[j], (
                f"templates {list(TYPE_TEMPLATES.keys())[i]} and "
                f"{list(TYPE_TEMPLATES.keys())[j]} are identical")


def test_all_templates_have_15_features():
    for name, template in TYPE_TEMPLATES.items():
        assert len(template) == N_FEATURES, f"{name}: {len(template)} features"


def test_template_self_classification():
    for name, template in TYPE_TEMPLATES.items():
        assigned, dist = classify(template)
        assert assigned == name, f"{name} classifies as {assigned}"
        assert dist == 0, f"{name} has distance {dist} to itself"


def test_templates_minimum_separation():
    KNOWN_CLOSE_PAIRS = {
        ("ideological_party", "personal_empire"),
        ("dynastic_composite", "feudal_order"),
        ("federal_republic", "unitary_nation_state"),
    }
    names = list(TYPE_TEMPLATES.keys())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            pair = tuple(sorted([names[i], names[j]]))
            d = hamming(TYPE_TEMPLATES[names[i]], TYPE_TEMPLATES[names[j]])
            if pair in KNOWN_CLOSE_PAIRS:
                assert d >= 1
            else:
                assert d >= 2, (
                    f"{names[i]} and {names[j]} are only {d} apart — "
                    f"ambiguous classification risk")


# =========================================================================
# Case JSON data integrity
# =========================================================================

ALL_CASE_FILES = [
    "germany.json", "italy.json", "united_states.json",
    "european_union.json", "china.json", "japan.json",
    "ctrl_middle_east_post_ottoman.json", "ctrl_sub_saharan_africa.json",
    "ctrl_post_soviet.json", "ctrl_greek_poleis.json",
]


@pytest.mark.parametrize("filename", ALL_CASE_FILES)
def test_case_json_loadable(filename):
    case = _load_case(filename)
    assert len(case.features_pre) == 15
    assert len(case.features_post) == 15
    assert all(f in (0, 1) for f in case.features_pre)
    assert all(f in (0, 1) for f in case.features_post)


@pytest.mark.parametrize("filename", ALL_CASE_FILES)
def test_case_periodization_order(filename):
    case = _load_case(filename)
    assert case.pre_frag_year <= case.frag_peak_year
    assert case.pre_frag_year < case.post_collect_year
    if not case.is_control:
        assert case.frag_peak_year <= case.first_integration_year
    assert case.first_integration_year <= case.post_collect_year


@pytest.mark.parametrize("filename", ALL_CASE_FILES)
def test_case_positive_counts(filename):
    case = _load_case(filename)
    assert case.units_pre > 0
    assert case.units_peak > 0
    assert case.units_post > 0
    assert case.pop_pre > 0
    assert case.pop_post > 0


@pytest.mark.parametrize("filename", ALL_CASE_FILES)
def test_case_control_flag_matches_filename(filename):
    case = _load_case(filename)
    if filename.startswith("ctrl_"):
        assert case.is_control, f"{filename} should be a control"
    else:
        assert not case.is_control, f"{filename} should not be a control"
