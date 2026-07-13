"""Tests for the backsliding-risk diagnostic (mi/backsliding.py). Validates the empirical
inverted-U, the 80th-percentile safety ceiling, sensible country reads, and — critically —
that the module is ADDITIVE: it does not alter MI pillar scoring / tiers / safeguards."""
import pytest
from mi import backsliding as B
from mi import panel as P
from mi.scoring import score_country


def test_hazard_curve_is_inverted_u():
    """peak risk at mid-capacity, low at both extremes (Angle 6)."""
    mid = B._hazard_from_percentile(0.45)
    lo = B._hazard_from_percentile(0.05)
    hi = B._hazard_from_percentile(0.95)
    assert mid > lo and mid > hi, f"expected inverted-U, got lo={lo} mid={mid} hi={hi}"
    assert 0.0 <= B._hazard_from_percentile(1.5) <= 0.12   # clamps out-of-range


def test_safety_ceiling_flag():
    nl = B.backsliding_risk("Netherlands", 2024)
    dk = B.backsliding_risk("Denmark", 2024)
    assert nl and nl["safety_ceiling"] and nl["capacity_percentile"] >= 0.80
    assert dk and dk["safety_ceiling"]


def test_hungary_in_danger_zone():
    """Hungary — the textbook 2010s backslider — should land in the mid-capacity danger zone."""
    hu = B.backsliding_risk("Hungary", 2024)
    assert hu and hu["danger_zone"] and hu["band"] == "danger-zone"
    assert hu["backslide_hazard_5y"] >= B.backsliding_risk("Denmark", 2024)["backslide_hazard_5y"]


def test_read_shape_and_bounds():
    r = B.backsliding_risk("Portugal", 2024)
    assert r is not None
    assert {"capacity_percentile", "backslide_hazard_5y", "safety_ceiling",
            "danger_zone", "band", "relational_capacity_gap", "provenance"} <= set(r)
    assert 0.0 <= r["capacity_percentile"] <= 1.0
    assert B.backsliding_risk("Nowhereistan", 2024) is None   # absent country -> None


def test_universe_sorted_safest_first():
    u = B.universe_backsliding(2024)
    assert len(u) > 100
    pctls = [r["capacity_percentile"] for r in u]
    assert pctls == sorted(pctls, reverse=True)


def test_additive_does_not_change_scoring():
    """importing/using backsliding must not perturb MI scoring (frozen v3.3)."""
    ind = P.indicators_for("Estonia", 2024)
    before = score_country(ind)["mi_score"]
    _ = B.backsliding_risk("Estonia", 2024)          # exercise the module
    after = score_country(ind)["mi_score"]
    assert before == after and before is not None
