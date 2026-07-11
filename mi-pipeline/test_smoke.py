#!/usr/bin/env python3
"""
Synthetic-data smoke test for the four documented mi_pipeline fixes.
=====================================================================
This does NOT touch the network or any real CSVs. It builds tiny synthetic
panels that exercise each fix in isolation, so the fixes can be proven before
the first real run.

Run standalone:
    python test_smoke.py        # prints PASS/FAIL per fix, exits non-zero on any failure

Or under pytest:
    pytest test_smoke.py -q

Covers:
  1. gap counter sees entirely-absent data sources (not just absent values)
  2. v1 anchoring fails loudly when an anchor's raw composite is NaN
  3. ECI off-target years are snapped to the nearest target year, not dropped
  4. the "structural overperformers" block uses the top-quartile (mi_75) threshold
"""

import numpy as np
import pandas as pd

import mi_pipeline as mp


# ─────────────────────────────────────────────────────────────────
#  Fix 1 — gap counter is blind to an entirely-absent source
# ─────────────────────────────────────────────────────────────────
def test_gap_counter_sees_absent_source():
    """Build a Track-1 panel with every indicator EXCEPT the HDR pair
    (EduIdx / LifeExpIdx) — i.e. hdr.csv was never provided, so those columns
    never exist. The affected pillar (P3) must go NaN AND each row must report
    exactly 2 gaps (the two missing HDR indicators), not 0."""
    rows = []
    for i, iso3 in enumerate(["AAA", "BBB", "CCC", "DDD"]):
        rows.append({
            "iso3": iso3, "country": f"Country{iso3}", "year": 2024, "Track": 1,
            # base raw indicators present (NOTE: no EduIdx / LifeExpIdx columns)
            "GovEff": 60 + i, "RuleLaw": 55 + i, "RegQual": 58 + i, "PolStab": 50 + i,
            "GDPpcPPP": 30000 + 1000 * i, "ResRents": 2.0 + i,
            # track-1 extras present
            "CPI": 60 + i, "GII": 50 + i, "ECI": 1.0 + 0.1 * i, "ODA": 0.0, "FSI": 40 + i,
        })
    panel = pd.DataFrame(rows)

    panel = mp.normalize(panel)
    panel = mp.compute_pillars(panel)
    panel = mp.compute_diagnostics(panel)

    assert panel["P3"].isna().all(), "P3 should be all-NaN when HDR source is absent"
    assert (panel["gap_count"] == 2).all(), (
        f"gap_count should be 2 (EduIdx+LifeExpIdx absent), got "
        f"{panel['gap_count'].tolist()}"
    )
    assert panel["gaps_noted"].str.contains("EduIdx").all()
    assert panel["gaps_noted"].str.contains("LifeExpIdx").all()


# ─────────────────────────────────────────────────────────────────
#  Fix 2 — v1 anchoring fails loudly on a NaN anchor raw
# ─────────────────────────────────────────────────────────────────
def test_v1_anchoring_raises_on_nan_anchor():
    """Switzerland 2024 is missing a pillar input (P1 = NaN) → v1_raw NaN →
    anchoring is undefined. score_v1 must raise, not silently emit all-NaN."""
    rows = [
        # ceiling anchor with a missing pillar → NaN raw
        {"iso3": "CHE", "country": "Switzerland", "year": 2024,
         "P1": np.nan, "P2": 0.9, "P3": 0.95, "P4": 0.8, "P5": 0.85},
        # floor anchor fully populated
        {"iso3": "LBN", "country": "Lebanon", "year": 2024,
         "P1": 0.30, "P2": 0.35, "P3": 0.55, "P4": 0.40, "P5": 0.20},
        # an ordinary country
        {"iso3": "USA", "country": "United States", "year": 2024,
         "P1": 0.70, "P2": 0.75, "P3": 0.80, "P4": 0.78, "P5": 0.65},
    ]
    df = pd.DataFrame(rows)
    raised = False
    try:
        mp.score_v1(df)
    except ValueError as e:
        raised = True
        assert "anchor" in str(e).lower() and "nan" in str(e).lower()
    assert raised, "score_v1 must raise ValueError when an anchor raw is NaN"


def test_v1_anchoring_succeeds_when_anchors_present():
    """Sanity: with both anchors fully populated, scoring still works and
    Switzerland maps to 1.0, Lebanon to 0.0."""
    rows = [
        {"iso3": "CHE", "country": "Switzerland", "year": 2024,
         "P1": 0.90, "P2": 0.90, "P3": 0.95, "P4": 0.80, "P5": 0.85},
        {"iso3": "LBN", "country": "Lebanon", "year": 2024,
         "P1": 0.30, "P2": 0.35, "P3": 0.55, "P4": 0.40, "P5": 0.20},
        {"iso3": "USA", "country": "United States", "year": 2024,
         "P1": 0.70, "P2": 0.75, "P3": 0.80, "P4": 0.78, "P5": 0.65},
    ]
    out = mp.score_v1(pd.DataFrame(rows))
    che = out.loc[out["iso3"] == "CHE", "v1_MScore"].iloc[0]
    lbn = out.loc[out["iso3"] == "LBN", "v1_MScore"].iloc[0]
    assert abs(che - 1.0) < 1e-9, f"Switzerland anchor should be 1.0, got {che}"
    assert abs(lbn - 0.0) < 1e-9, f"Lebanon anchor should be 0.0, got {lbn}"


# ─────────────────────────────────────────────────────────────────
#  Fix 3 — ECI off-target years are snapped, not dropped
# ─────────────────────────────────────────────────────────────────
def test_eci_snaps_to_nearest_target_year():
    """FOO has ECI only on 2023 (one year off 2024) → must snap onto the 2024
    target row. BAR has ECI exactly on 2018 → kept. BAZ has ECI only on 2009
    (>3 yrs from any target) → stays NaN. Off-target rows are dropped."""
    rows = [
        # FOO: a target-year row (from WB) with no ECI, plus an annual ECI on 2023
        {"iso3": "FOO", "year": 2024, "ECI": np.nan},
        {"iso3": "FOO", "year": 2023, "ECI": 1.5},
        # BAR: ECI exactly on a target year
        {"iso3": "BAR", "year": 2018, "ECI": 0.8},
        # BAZ: target-year row plus an ECI far from any target year
        {"iso3": "BAZ", "year": 2024, "ECI": np.nan},
        {"iso3": "BAZ", "year": 2009, "ECI": 2.2},
    ]
    df = pd.DataFrame(rows)
    snapped = mp._snap_eci_years(df)

    # only target years survive
    assert set(snapped["year"].unique()).issubset(set(mp.TIME_POINTS))
    assert 2023 not in snapped["year"].values and 2009 not in snapped["year"].values

    foo_2024 = snapped[(snapped["iso3"] == "FOO") & (snapped["year"] == 2024)]["ECI"].iloc[0]
    assert abs(foo_2024 - 1.5) < 1e-9, f"FOO 2024 ECI should snap to 1.5, got {foo_2024}"

    bar_2018 = snapped[(snapped["iso3"] == "BAR") & (snapped["year"] == 2018)]["ECI"].iloc[0]
    assert abs(bar_2018 - 0.8) < 1e-9, f"BAR 2018 ECI should be 0.8, got {bar_2018}"

    baz_2024 = snapped[(snapped["iso3"] == "BAZ") & (snapped["year"] == 2024)]["ECI"].iloc[0]
    assert pd.isna(baz_2024), f"BAZ 2024 ECI should stay NaN (no value within gap), got {baz_2024}"


# ─────────────────────────────────────────────────────────────────
#  Fix 4 — structural overperformers use the top-quartile threshold
# ─────────────────────────────────────────────────────────────────
def _overperformer_section(findings: str):
    """Return the lines listed under the 'structural overperformers' header."""
    lines = findings.splitlines()
    out, capture = [], False
    for ln in lines:
        if "structural overperformers" in ln:
            capture = True
            continue
        if capture:
            if ln.strip().startswith("──") or ln.strip().startswith("=="):
                break
            if ln.strip() == "" or ln.strip().endswith(":"):
                break
            out.append(ln)
    return "\n".join(out)


def test_overperformers_use_top_quartile():
    """Build a 2024 cohort where:
      - LOWP: bottom-quartile GDP, MI above the 75th pct  → IS an overperformer
      - MIDP: bottom-quartile GDP, MI above median but below 75th pct
              → would have shown under the old (mi_median) code; must NOT now.
    """
    # MI scores 0.10..0.90 over 9 fillers; 75th pct ~0.70, median 0.50.
    fillers = []
    mis = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]
    for i, mi in enumerate(mis):
        fillers.append({
            "iso3": f"F{i:02d}", "country": f"Filler{i}", "year": 2024, "Track": 1,
            "gap_count": 0, "pillar_spread": 0.1,
            "P1": mi, "P2": mi, "P3": mi, "P4": mi, "P5": mi,
            "v1_MScore": mi, "GDPpcPPP": 20000 + i * 5000, "ResRents": 3.0,
        })
    # low-GDP cases (GDP below the 25th percentile of the cohort)
    low_gdp = 1000
    lowp = {"iso3": "LWP", "country": "Lowperf", "year": 2024, "Track": 1,
            "gap_count": 0, "pillar_spread": 0.1,
            "P1": 0.85, "P2": 0.85, "P3": 0.85, "P4": 0.85, "P5": 0.85,
            "v1_MScore": 0.85, "GDPpcPPP": low_gdp, "ResRents": 3.0}        # above 75th pct
    midp = {"iso3": "MDP", "country": "Midperf", "year": 2024, "Track": 1,
            "gap_count": 0, "pillar_spread": 0.1,
            "P1": 0.60, "P2": 0.60, "P3": 0.60, "P4": 0.60, "P5": 0.60,
            "v1_MScore": 0.60, "GDPpcPPP": low_gdp + 200, "ResRents": 3.0}   # median<MI<75th

    df = pd.DataFrame(fillers + [lowp, midp])
    findings = mp.analytical_findings(df)

    assert "top-quartile MI (structural overperformers)" in findings, \
        "overperformers label should read 'top-quartile MI'"
    section = _overperformer_section(findings)
    assert "Lowperf" in section, "Lowperf (above 75th pct) must be listed as an overperformer"
    assert "Midperf" not in section, (
        "Midperf (above median but below 75th pct) must NOT be listed — proves the "
        "filter uses mi_75, not mi_median"
    )


# ─────────────────────────────────────────────────────────────────
#  Hardening — World Bank aggregate codes are excluded from the panel
# ─────────────────────────────────────────────────────────────────
def test_wb_aggregate_fallback_set():
    """The static fallback aggregate set (used when the WB country-list call
    fails) must contain the well-known regional/income aggregates and must NOT
    contain real countries — so World/OECD/Arab World never leak into the panel
    as countries, while Switzerland/Lebanon/USA/Taiwan are kept."""
    agg = mp._WB_AGGREGATE_FALLBACK
    for code in ["WLD", "EUU", "OED", "ARB", "SSA", "LIC", "HIC", "MEA"]:
        assert code in agg, f"{code} should be flagged as a WB aggregate"
    for code in ["USA", "CHE", "LBN", "TWN", "SGP", "NGA"]:
        assert code not in agg, f"{code} is a real country, must not be excluded"


# ─────────────────────────────────────────────────────────────────
#  standalone runner
# ─────────────────────────────────────────────────────────────────
def _run_all():
    tests = [
        ("fix 1: gap counter sees absent source", test_gap_counter_sees_absent_source),
        ("fix 2: v1 raises on NaN anchor", test_v1_anchoring_raises_on_nan_anchor),
        ("fix 2: v1 succeeds with anchors", test_v1_anchoring_succeeds_when_anchors_present),
        ("fix 3: ECI snaps to nearest target", test_eci_snaps_to_nearest_target_year),
        ("fix 4: overperformers use top quartile", test_overperformers_use_top_quartile),
        ("hardening: WB aggregates excluded", test_wb_aggregate_fallback_set),
    ]
    failures = 0
    for name, fn in tests:
        try:
            fn()
            print(f"PASS  {name}")
        except AssertionError as e:
            failures += 1
            print(f"FAIL  {name}\n      {e}")
        except Exception as e:  # noqa: BLE001
            failures += 1
            print(f"ERROR {name}\n      {type(e).__name__}: {e}")
    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    return failures


if __name__ == "__main__":
    import sys
    sys.exit(1 if _run_all() else 0)
