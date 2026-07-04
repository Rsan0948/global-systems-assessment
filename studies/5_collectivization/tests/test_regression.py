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
from pathway_analysis import classify_pathway, score_case as pw_score

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
    # Expansion cases (randomly selected, seed=42)
    "exp_netherlands.json": ("colonial_imperial", "supranational_union"),
    "exp_spain.json": ("personal_empire", "colonial_imperial"),
    "exp_india_mughal.json": ("personal_empire", "personal_empire"),
    "exp_india_maurya.json": ("city_state_system", "personal_empire"),
    "exp_zulu_kingdom.json": ("city_state_system", "personal_empire"),
    "exp_poland_lithuania.json": ("personal_empire", "federal_republic"),
    "exp_persia_safavid.json": ("personal_empire", "personal_empire"),
    "exp_france.json": ("personal_empire", "colonial_imperial"),
    "exp_vietnam.json": ("personal_empire", "personal_empire"),
    "exp_ethiopia.json": ("personal_empire", "personal_empire"),
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
    # Expansion cases
    "exp_netherlands.json", "exp_spain.json", "exp_india_mughal.json",
    "exp_india_maurya.json", "exp_zulu_kingdom.json",
    "exp_poland_lithuania.json", "exp_persia_safavid.json",
    "exp_france.json", "exp_vietnam.json", "exp_ethiopia.json",
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


# =========================================================================
# Expansion case stability
# =========================================================================

EXPANSION_CASE_FILES = [f for f in ALL_CASE_FILES if f.startswith("exp_")]


@pytest.mark.parametrize("filename", EXPANSION_CASE_FILES)
def test_expansion_cases_not_controls(filename):
    case = _load_case(filename)
    assert not case.is_control


def test_restoration_cases_zero_flips():
    for fname in ["exp_india_mughal.json", "exp_persia_safavid.json"]:
        case = _load_case(fname)
        s = fs_score(case)
        assert s.flip_count == 0, f"{fname} should have zero flips (restoration case)"
        assert not s.type_changed


def test_netherlands_form_shift():
    case = _load_case("exp_netherlands.json")
    s = fs_score(case)
    assert s.type_changed
    assert s.flip_count == 9
    assert len(s.failure_diagnostic["new_vulnerabilities"]) == 0


def test_poland_lithuania_form_shift():
    case = _load_case("exp_poland_lithuania.json")
    s = fs_score(case)
    assert s.type_changed
    assert s.flip_count == 8


def test_india_maurya_ratchet():
    case = _load_case("exp_india_maurya.json")
    s = ratchet_score(case)
    assert s.positive_dims == 3
    assert s.integration_depth_post == 6


def test_zulu_fast_collectivization():
    case = _load_case("exp_zulu_kingdom.json")
    assert case.collect_speed_years == 12


def test_france_slow_collectivization():
    case = _load_case("exp_france.json")
    assert case.collect_speed_years == 447


def test_expanded_pool_form_shift_supported():
    from cycle_engine import analyze as cycle_analyze
    cases_dir = os.path.join(HERE, "..", "cases")
    all_cases = []
    for fname in sorted(os.listdir(cases_dir)):
        if fname.endswith(".json"):
            all_cases.append(_load_case(fname))
    assert len(all_cases) == 20
    result = cycle_analyze(all_cases)
    assert result.summary["form_shift_supported"]
    assert result.summary["n_core_cases"] == 16
    assert result.summary["n_controls"] == 4


# =========================================================================
# Pathway classification stability
# =========================================================================

EXPECTED_PATHWAYS = {
    # Construction: low predecessor depth, must build new institutions
    "germany.json": "construction",
    "italy.json": "construction",
    "china.json": "construction",
    "japan.json": "construction",
    "european_union.json": "construction",
    "exp_netherlands.json": "construction",
    "exp_zulu_kingdom.json": "construction",
    "exp_india_maurya.json": "construction",
    # Restoration: high predecessor depth, fast, same type
    "exp_india_mughal.json": "restoration",
    "exp_persia_safavid.json": "restoration",
    "exp_vietnam.json": "restoration",
    "exp_ethiopia.json": "restoration",
    # Negotiation: high predecessor depth, slow collectivization
    "exp_france.json": "negotiation",
    "exp_spain.json": "negotiation",
    "exp_poland_lithuania.json": "negotiation",
    # Redesign: high predecessor depth, fast, deliberate form-shift
    "united_states.json": "redesign",
}


@pytest.mark.parametrize("filename,expected", list(EXPECTED_PATHWAYS.items()))
def test_pathway_classification_stability(filename, expected):
    case = _load_case(filename)
    assert classify_pathway(case) == expected


def test_restorations_have_zero_net_patch():
    for fname, pathway in EXPECTED_PATHWAYS.items():
        if pathway == "restoration":
            case = _load_case(fname)
            s = pw_score(case)
            assert s.failures_patched == 0, f"{fname}: expected 0 patched"
            assert s.new_vulnerabilities == 0, f"{fname}: expected 0 new"


def test_restorations_have_zero_integration_loss():
    for fname, pathway in EXPECTED_PATHWAYS.items():
        if pathway == "restoration":
            case = _load_case(fname)
            s = pw_score(case)
            assert s.integration_features_lost == 0


def test_depth_predicts_flips():
    from pathway_analysis import analyze as pw_analyze
    cases_dir = os.path.join(HERE, "..", "cases")
    all_cases = [_load_case(f) for f in sorted(os.listdir(cases_dir)) if f.endswith(".json")]
    r = pw_analyze(all_cases)
    assert r.depth_flip_p < 0.001
    assert r.depth_flip_rho < -0.7


def test_speed_predicts_integration_loss():
    from pathway_analysis import analyze as pw_analyze
    cases_dir = os.path.join(HERE, "..", "cases")
    all_cases = [_load_case(f) for f in sorted(os.listdir(cases_dir)) if f.endswith(".json")]
    r = pw_analyze(all_cases)
    assert r.speed_integration_loss_p < 0.05
    assert r.speed_integration_loss_rho > 0.7
