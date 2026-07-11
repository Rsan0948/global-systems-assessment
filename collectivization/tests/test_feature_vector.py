"""Tests for feature_vector.py -- governance feature encoding and type assignment."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from feature_vector import (
    validate, hamming, classify, flip_count, flipped_features,
    integration_depth, functional_breadth, legitimacy_flips,
    N_FEATURES, TYPE_TEMPLATES, FEATURE_NAMES,
)


def test_feature_count():
    assert N_FEATURES == 15
    assert len(FEATURE_NAMES) == 15
    for name, template in TYPE_TEMPLATES.items():
        assert len(template) == 15, f"{name} template has wrong length"


def test_validate_rejects_wrong_length():
    with pytest.raises(ValueError):
        validate([0, 1])


def test_validate_rejects_non_binary():
    with pytest.raises(ValueError):
        validate([2] + [0] * 14)


def test_hamming_identical():
    a = [0] * 15
    assert hamming(a, a) == 0


def test_hamming_opposite():
    a = [0] * 15
    b = [1] * 15
    assert hamming(a, b) == 15


def test_classify_exact_match():
    for name, template in TYPE_TEMPLATES.items():
        assigned, dist = classify(template)
        assert assigned == name, f"template for {name} classified as {assigned}"
        assert dist == 0


def test_classify_near_match():
    feudal = list(TYPE_TEMPLATES["feudal_order"])
    feudal[0] = 0  # flip one feature
    assigned, dist = classify(feudal)
    assert dist <= 2  # should still be close to feudal_order


def test_flip_count_basic():
    pre = [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1]  # feudal-ish
    post = [1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1]  # federal-ish
    fc = flip_count(pre, post)
    assert fc > 0
    assert fc == len(flipped_features(pre, post))


def test_integration_depth():
    all_integrated = [0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0]
    assert integration_depth(all_integrated) == 6

    none_integrated = [0] * 15
    assert integration_depth(none_integrated) == 0


def test_functional_breadth():
    full = list(TYPE_TEMPLATES["federal_republic"])
    assert functional_breadth(full) >= 4

    empty = list(TYPE_TEMPLATES["city_state_system"])
    assert functional_breadth(empty) == 0


def test_legitimacy_flips():
    pre = [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # hereditary monarch
    post = [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0]  # elected, popular sov
    lf = legitimacy_flips(pre, post)
    assert lf >= 3  # features 1, 7, 8, 9 should flip
