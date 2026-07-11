"""Tests for warning_signals.py -- fragmentation pressure indicators."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from warning_signals import (
    check_efficiency_decay,
    check_integration_reversal,
    check_legitimacy_erosion,
    analyze_case,
    WarningSignal,
    WarningResult,
    _rolling_growth,
)


# --- check_efficiency_decay ---

def test_efficiency_decay_fires_on_sustained_decline():
    gdp = {}
    for y in range(1800, 1870):
        gdp[y] = 100 * (1.02 ** (y - 1800))
    for y in range(1870, 1920):
        gdp[y] = gdp[1869] * (1.005 ** (y - 1869))
    sig = check_efficiency_decay(gdp, post_collect_year=1830)
    assert sig.fired


def test_efficiency_decay_silent_on_steady_growth():
    gdp = {y: 100 * (1.02 ** (y - 1800)) for y in range(1800, 1950)}
    sig = check_efficiency_decay(gdp, post_collect_year=1830)
    assert not sig.fired


def test_efficiency_decay_empty_series():
    sig = check_efficiency_decay({}, post_collect_year=1900)
    assert not sig.fired
    assert "insufficient" in sig.detail


def test_efficiency_decay_no_baseline_window():
    gdp = {y: 100.0 for y in range(1700, 1750)}
    sig = check_efficiency_decay(gdp, post_collect_year=1800)
    assert not sig.fired
    assert "no GDP data" in sig.detail or "insufficient" in sig.detail


def test_efficiency_decay_brief_dip_does_not_fire():
    gdp = {}
    for y in range(1800, 1900):
        gdp[y] = 100 * (1.02 ** (y - 1800))
    for y in range(1900, 1902):
        gdp[y] = gdp[1899] * (1.015 ** (y - 1899))
    for y in range(1902, 1950):
        gdp[y] = gdp[1901] * (1.03 ** (y - 1901))
    sig = check_efficiency_decay(gdp, post_collect_year=1830)
    assert not sig.fired


# --- check_integration_reversal ---

def test_integration_reversal_fires_on_two_plus_reversals():
    post = [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    later = [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    sig = check_integration_reversal(post, later)
    assert sig.fired
    assert "2 features" in sig.detail


def test_integration_reversal_silent_on_one_reversal():
    post = [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    later = [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0]
    sig = check_integration_reversal(post, later)
    assert not sig.fired


def test_integration_reversal_no_later_vector():
    post = [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    sig = check_integration_reversal(post, None)
    assert not sig.fired
    assert "no later" in sig.detail


def test_integration_reversal_identical_vectors():
    vec = [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    sig = check_integration_reversal(vec, list(vec))
    assert not sig.fired


# --- check_legitimacy_erosion ---

def test_legitimacy_erosion_fires_on_decline():
    vdem = {y: 0.8 - 0.004 * (y - 1900) for y in range(1900, 1960)}
    sig = check_legitimacy_erosion(vdem, post_collect_year=1890)
    assert sig.fired
    assert "V-Dem dropped" in sig.detail


def test_legitimacy_erosion_silent_on_improvement():
    vdem = {y: 0.3 + 0.005 * (y - 1900) for y in range(1900, 1960)}
    sig = check_legitimacy_erosion(vdem, post_collect_year=1890)
    assert not sig.fired


def test_legitimacy_erosion_insufficient_data():
    vdem = {y: 0.5 for y in range(1900, 1910)}
    sig = check_legitimacy_erosion(vdem, post_collect_year=1890)
    assert not sig.fired
    assert "insufficient" in sig.detail


def test_legitimacy_erosion_empty_series():
    sig = check_legitimacy_erosion({}, post_collect_year=1900)
    assert not sig.fired


def test_legitimacy_erosion_flat_does_not_fire():
    vdem = {y: 0.5 for y in range(1900, 1960)}
    sig = check_legitimacy_erosion(vdem, post_collect_year=1890)
    assert not sig.fired


# --- analyze_case ---

def test_analyze_case_aggregation():
    gdp = {y: 100 * (1.02 ** (y - 1800)) for y in range(1800, 1950)}
    vdem = {y: 0.5 for y in range(1900, 1960)}
    post = [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    r = analyze_case("test", gdp, vdem, post, 1830)
    assert isinstance(r, WarningResult)
    assert r.case_name == "test"
    assert isinstance(r.any_fired, bool)
    assert isinstance(r.all_fired, bool)


def test_analyze_case_all_empty():
    post = [0] * 15
    r = analyze_case("empty", {}, {}, post, 2000)
    assert not r.any_fired
    assert not r.all_fired


# --- _rolling_growth ---

def test_rolling_growth_basic():
    gdp = {y: 100 * (1.03 ** (y - 1900)) for y in range(1900, 1950)}
    rg = _rolling_growth(gdp, window=10)
    assert len(rg) > 0
    for rate in rg.values():
        assert abs(rate - 0.03) < 0.01


def test_rolling_growth_empty():
    assert _rolling_growth({}) == {}


def test_rolling_growth_single_point():
    assert _rolling_growth({2000: 100.0}) == {}
