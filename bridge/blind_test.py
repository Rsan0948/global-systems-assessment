"""
BLIND VALIDATION: 10 new countries not in the training/calibration set.

Feature vectors coded from institutional structure knowledge ALONE,
without reference to MI scores.  Then predictions are compared against
actual canonical MI pillar scores (2024).

This tests whether the loading matrix + depth features generalize
beyond the 12 countries used to develop/validate the model.
"""

from __future__ import annotations

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
from pillar_loading import project_normalized, PILLAR_NAMES, FEATURE_NAMES

# =========================================================================
# STEP 1: Code feature vectors BLIND (from institutional knowledge only)
# =========================================================================
#
# 19 features:
#   0: single_executive
#   1: hereditary_succession
#   2: independent_militaries
#   3: independent_foreign_policy
#   4: shared_currency
#   5: shared_legal_code
#   6: unilateral_exit
#   7: central_tax
#   8: popular_sovereignty
#   9: elected_leadership
#  10: free_movement_persons
#  11: free_movement_goods
#  12: shared_supreme_court
#  13: central_standing_army
#  14: preexisting_polities
#  15: institutional_continuity (50+ years unbroken constitutional order)
#  16: prior_self_governance (population had self-rule tradition)
#  17: bureaucratic_inheritance (inherited functioning admin, not extraction)
#  18: literacy_at_founding (>90% literacy at institutional founding)

BLIND_FEATURE_VECTORS = {
    # SOUTH KOREA: Presidential republic (1987 constitution, 6th Republic)
    # single_exec=1 (president), no hereditary, unified military/foreign,
    # own currency (won), unified legal code, no exit, central tax,
    # popular sovereignty, elected president, free movement (internal),
    # free trade (internal), supreme court, standing army,
    # no significant preexisting sub-polities (unified peninsula)
    # Depth: continuity=0 (1987 is ~37 yrs, not 50+), prior_self_gov=0
    # (Japanese colonial rule then military dictatorships — democratic
    # self-governance tradition is short), bureaucratic_inherit=0
    # (Japanese colonial admin was extractive), literacy=0 (not >90% in 1948)
    "South Korea": [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0,
                    0, 0, 0, 0],

    # SWEDEN: Constitutional monarchy (parliamentary, 1974 Instrument of Gov)
    # single_exec=0 (parliamentary system, PM + ceremonial king),
    # hereditary=0 (political succession not hereditary), unified mil/foreign,
    # own currency (krona, not in eurozone), unified legal code, no exit,
    # central tax, popular sovereignty, elected parliament,
    # free movement (Schengen), free trade (EU single market),
    # supreme court (Supreme Court since 1789), standing army,
    # no preexisting polities (unitary state, no historical sub-kingdoms)
    # Depth: continuity=1 (unbroken since 1809 constitution lineage),
    # prior_self_gov=1 (Riksdag tradition since 1435),
    # bureaucratic_inherit=1 (strong Swedish state apparatus),
    # literacy=1 (near-universal literacy by 18th century)
    "Sweden": [0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0,
               1, 1, 1, 1],

    # MEXICO: Federal presidential republic (1917 constitution)
    # single_exec=1 (president), no hereditary, unified mil/foreign,
    # own currency (peso), shared legal code (civil law), no exit,
    # central tax (federal), popular sovereignty, elected president,
    # free movement internal, free trade internal, supreme court,
    # standing army, preexisting polities=1 (31 states, historical
    # indigenous polities, complex federalism)
    # Depth: continuity=1 (1917 constitution unbroken 100+ years),
    # prior_self_gov=0 (300 years colonial rule, then instability,
    # limited democratic tradition before PRI), bureaucratic_inherit=0
    # (colonial extraction apparatus), literacy=0 (not >90% in 1917)
    "Mexico": [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1,
               1, 0, 0, 0],

    # INDIA: Federal parliamentary republic (1950 constitution)
    # single_exec=0 (parliamentary, PM is exec, president ceremonial),
    # no hereditary, unified mil/foreign, own currency (rupee),
    # shared legal code (common law + constitution), no exit,
    # central tax, popular sovereignty, elected parliament,
    # free movement (internal), free trade (internal), supreme court,
    # standing army, preexisting_polities=1 (states, princely states history)
    # Depth: continuity=0 (1950 is 74 yrs, borderline — but given
    # Emergency period 1975-77 and massive institutional stress, code 0),
    # Actually 74 years is >50. Let me code 1 for continuity.
    # prior_self_gov=0 (British colonial rule; limited self-governance
    # tradition at mass level despite ancient kingdoms),
    # bureaucratic_inherit=1 (inherited the Indian Civil Service, a
    # functioning admin apparatus from British Raj — unlike extraction-only),
    # literacy=0 (literacy ~18% at independence in 1947)
    "India": [0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1,
              1, 0, 1, 0],

    # SINGAPORE: Parliamentary republic (1965 independence)
    # single_exec=0 (parliamentary, PM is exec, president elected but
    # largely ceremonial), no hereditary, unified mil/foreign,
    # own currency (SGD), shared legal code, no exit (city-state),
    # central tax, popular_sovereignty=0 (dominant party state, elections
    # held but heavily constrained — PAP monopoly, limited genuine V&A),
    # elected_leadership=1 (elections do happen, even if tilted),
    # free movement (city-state, N/A internally — code 1),
    # free trade (extreme trade openness), supreme court (Court of Appeal),
    # standing army, preexisting_polities=0 (city-state, no sub-units)
    # Depth: continuity=1 (unbroken since 1965, 59 yrs — close but yes),
    # prior_self_gov=0 (colonial port, no self-governance tradition),
    # bureaucratic_inherit=1 (inherited British colonial admin that was
    # relatively functional for a port city — Lee Kuan Yew built on it),
    # literacy=0 (multilingual population, not >90% English literacy
    # at founding in 1965; ~60% literacy then)
    "Singapore": [0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0,
                  1, 0, 1, 0],

    # CHILE: Unitary presidential republic (1980 constitution, amended)
    # single_exec=1 (president), no hereditary, unified mil/foreign,
    # own currency (peso), shared legal code, no exit (unitary),
    # central tax, popular sovereignty, elected president,
    # free movement, free trade, supreme court (Corte Suprema),
    # standing army, preexisting_polities=0 (unitary state, no federalism)
    # Depth: continuity=0 (1980 constitution from Pinochet era, democratic
    # transition 1990 — only 34 yrs of democratic operation),
    # prior_self_gov=1 (Chile had strong democratic tradition 1830s-1973,
    # one of Latin America's oldest), bureaucratic_inherit=1 (inherited
    # functioning state apparatus — Chile's state was relatively strong),
    # literacy=0 (not >90% in 1990 transition — actually ~95% by 1990,
    # borderline. Let me code 1.)
    "Chile": [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0,
              0, 1, 1, 1],

    # POLAND: Parliamentary republic (1997 constitution, semi-presidential)
    # single_exec=1 (president has real powers, semi-presidential),
    # no hereditary, unified mil/foreign, own currency (zloty),
    # shared legal code, no exit, central tax,
    # popular sovereignty, elected president+parliament,
    # free movement (EU/Schengen), free trade (EU single market),
    # supreme court, standing army, preexisting_polities=0 (unitary)
    # Depth: continuity=0 (1997 constitution, only 27 years; before that
    # communist People's Republic), prior_self_gov=0 (partitioned 1795-1918,
    # brief interwar democracy, then communist rule — limited democratic
    # tradition), bureaucratic_inherit=0 (communist-era bureaucracy was
    # ideological, not merit-based administrative tradition),
    # literacy=1 (near-universal by 1997 — communist era achieved mass
    # education)
    "Poland": [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0,
               0, 0, 0, 1],

    # NIGERIA: Federal presidential republic (1999 constitution, 4th Republic)
    # single_exec=1 (president), no hereditary (political),
    # unified mil/foreign, own currency (naira), shared legal code
    # (common law + sharia in north — code 0 for fragmented legal),
    # no exit, central tax, popular_sovereignty=1 (elections held),
    # elected_leadership=1, free movement (internal),
    # free trade (internal), shared supreme court, standing army,
    # preexisting_polities=1 (36 states, massive ethnic/regional diversity)
    # Depth: continuity=0 (1999 = 25 yrs, prior coups/military rule),
    # prior_self_gov=0 (colonial creation, no unified self-governance
    # tradition), bureaucratic_inherit=0 (colonial extraction apparatus),
    # literacy=0 (literacy ~57% even now, far below 90% at 1999 founding)
    "Nigeria": [1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1,
                0, 0, 0, 0],

    # NORWAY: Constitutional monarchy (parliamentary, 1814 constitution)
    # single_exec=0 (parliamentary, PM + ceremonial king),
    # hereditary=0 (political power not hereditary), unified mil/foreign,
    # own currency (krone, not eurozone), shared legal code, no exit,
    # central tax, popular sovereignty, elected Storting,
    # free movement (Schengen/EEA), free trade (EEA single market),
    # supreme court, standing army, preexisting_polities=0 (unitary)
    # Depth: continuity=1 (1814 constitution, 210+ years unbroken),
    # prior_self_gov=1 (Norse/Viking assemblies, strong local governance
    # tradition), bureaucratic_inherit=1 (Danish/Swedish admin tradition,
    # functioning apparatus), literacy=1 (near-universal by 19th century,
    # Lutheran education)
    "Norway": [0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0,
               1, 1, 1, 1],

    # TURKEY: Presidential republic (2017 constitutional change, effective 2018)
    # single_exec=1 (executive president since 2018), no hereditary,
    # unified mil/foreign, own currency (lira), shared legal code,
    # no exit, central tax, popular_sovereignty=1 (elections),
    # elected_leadership=1 (president elected), free movement (internal),
    # free trade (internal, customs union with EU), supreme court
    # (Constitutional Court), standing army,
    # preexisting_polities=0 (unitary state, no federalism)
    # Depth: continuity=0 (2018 presidential system is only 6 years;
    # even the 1982 constitution had multiple coups — 1960, 1971, 1980,
    # 1997 soft coup), prior_self_gov=0 (Ottoman sultanate → military
    # tutelage, limited democratic tradition at mass level),
    # bureaucratic_inherit=1 (Ottoman/Tanzimat bureaucratic tradition was
    # relatively functional — inherited strong state apparatus),
    # literacy=0 (Latin script adoption 1928, mass literacy campaign still
    # ongoing into 1950s — not >90% at 1923 founding)
    "Turkey": [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0,
               0, 0, 1, 0],
}

# =========================================================================
# STEP 2: Actual MI pillar scores (2024) — GROUND TRUTH
# (From canonical MI scoring engine, not seen during feature coding above)
# =========================================================================

BLIND_MI_SCORES = {
    "South Korea":  {"P1": 0.728, "P2": 0.760, "P3": 0.938, "P4": 0.842, "P5": 0.753},
    "Sweden":       {"P1": 0.834, "P2": 0.696, "P3": 0.949, "P4": 0.923, "P5": 0.762},
    "Mexico":       {"P1": 0.405, "P2": 0.496, "P3": 0.780, "P4": 0.811, "P5": 0.537},
    "India":        {"P1": 0.517, "P2": 0.568, "P3": 0.695, "P4": 0.544, "P5": 0.454},
    "Singapore":    {"P1": 0.874, "P2": 0.754, "P3": 0.923, "P4": 1.000, "P5": 0.828},
    "Chile":        {"P1": 0.673, "P2": 0.473, "P3": 0.894, "P4": 0.751, "P5": 0.664},
    "Poland":       {"P1": 0.625, "P2": 0.586, "P3": 0.903, "P4": 0.812, "P5": 0.684},
    "Nigeria":      {"P1": 0.356, "P2": 0.196, "P3": 0.538, "P4": 0.508, "P5": 0.250},
    "Norway":       {"P1": 0.850, "P2": 0.568, "P3": 0.956, "P4": 0.866, "P5": 0.813},
    "Turkey":       {"P1": 0.445, "P2": 0.570, "P3": 0.839, "P4": 0.791, "P5": 0.408},
}


# =========================================================================
# STEP 3: Run predictions and compare
# =========================================================================

def _rankdata(arr):
    arr = np.asarray(arr, dtype=float)
    order = np.argsort(arr)
    ranks = np.empty(len(arr), dtype=float)
    ranks[order] = np.arange(1, len(arr) + 1, dtype=float)
    for val in np.unique(arr):
        mask = arr == val
        if np.sum(mask) > 1:
            ranks[mask] = np.mean(ranks[mask])
    return ranks


def _spearman(x, y):
    rx = _rankdata(x)
    ry = _rankdata(y)
    if np.std(rx) == 0 or np.std(ry) == 0:
        return float("nan")
    return float(np.corrcoef(rx, ry)[0, 1])


def run_blind_test():
    print("=" * 72)
    print("BLIND VALIDATION: 10 countries not in calibration set")
    print("=" * 72)
    print()

    all_pred = []
    all_actual = []
    shape_corrs = []

    for country in sorted(BLIND_FEATURE_VECTORS):
        features = BLIND_FEATURE_VECTORS[country]
        predicted = project_normalized(features)
        actual = BLIND_MI_SCORES[country]

        pred_vec = [predicted[p] for p in PILLAR_NAMES]
        act_vec = [actual[p] for p in PILLAR_NAMES]
        all_pred.extend(pred_vec)
        all_actual.extend(act_vec)

        residuals = {p: round(actual[p] - predicted[p], 3) for p in PILLAR_NAMES}
        mae = np.mean([abs(r) for r in residuals.values()])

        shape_rho = _spearman(pred_vec, act_vec)
        shape_corrs.append(shape_rho)

        print(f"--- {country} ---")
        print(f"  Predicted: " + "  ".join(
            f"{p}={predicted[p]:.3f}" for p in PILLAR_NAMES))
        print(f"  Actual:    " + "  ".join(
            f"{p}={actual[p]:.3f}" for p in PILLAR_NAMES))
        print(f"  Residuals: " + "  ".join(
            f"{p}={residuals[p]:+.3f}" for p in PILLAR_NAMES))
        print(f"  MAE={mae:.3f}  Shape rho={shape_rho:.3f}")
        print()

    # Aggregate stats
    pred_arr = np.array(all_pred)
    act_arr = np.array(all_actual)

    pearson = float(np.corrcoef(pred_arr, act_arr)[0, 1])
    spearman_overall = _spearman(all_pred, all_actual)
    rmse = float(np.sqrt(np.mean((pred_arr - act_arr) ** 2)))
    mae = float(np.mean(np.abs(pred_arr - act_arr)))

    print("=" * 72)
    print("AGGREGATE RESULTS (blind holdout, N=10 countries, 50 data points)")
    print("=" * 72)
    print(f"  Overall Pearson r:       {pearson:.4f}")
    print(f"  Overall Spearman rho:    {spearman_overall:.4f}")
    print(f"  RMSE:                    {rmse:.4f}")
    print(f"  MAE:                     {mae:.4f}")
    print(f"  Median shape correlation: {np.median(shape_corrs):.4f}")
    print(f"  Mean shape correlation:   {np.mean(shape_corrs):.4f}")
    print()

    # Per-pillar correlation
    print("  Per-pillar cross-country Pearson:")
    for i, p in enumerate(PILLAR_NAMES):
        p_pred = [all_pred[j * 5 + i] for j in range(10)]
        p_act = [all_actual[j * 5 + i] for j in range(10)]
        r = float(np.corrcoef(p_pred, p_act)[0, 1])
        print(f"    {p}: r = {r:.4f}")
    print()

    # Comparison with calibration set
    print("  COMPARISON WITH CALIBRATION SET (12 countries):")
    print("    Calibration Pearson:    ~0.35")
    print(f"    Blind test Pearson:     {pearson:.4f}")
    print("    Calibration RMSE:       ~0.196")
    print(f"    Blind test RMSE:        {rmse:.4f}")
    print()

    # Interpretive summary
    print("=" * 72)
    print("INTERPRETATION")
    print("=" * 72)
    if pearson > 0.3:
        print("  The model GENERALIZES: blind-test correlation is comparable")
        print("  to calibration-set performance.")
    elif pearson > 0.1:
        print("  PARTIAL generalization: weaker than calibration but still")
        print("  capturing meaningful variance.")
    else:
        print("  POOR generalization: model does not transfer to new countries.")
    print()

    # Notable residual patterns
    print("  NOTABLE PATTERNS:")
    for country in sorted(BLIND_FEATURE_VECTORS):
        predicted = project_normalized(BLIND_FEATURE_VECTORS[country])
        actual = BLIND_MI_SCORES[country]
        for p in PILLAR_NAMES:
            r = actual[p] - predicted[p]
            if abs(r) > 0.25:
                direction = "EXCEEDS" if r > 0 else "FALLS SHORT of"
                print(f"    {country} {p}: actual {direction} prediction "
                      f"by {abs(r):.2f}")

    return {
        "pearson": pearson,
        "spearman": spearman_overall,
        "rmse": rmse,
        "mae": mae,
        "median_shape": float(np.median(shape_corrs)),
    }


if __name__ == "__main__":
    run_blind_test()
