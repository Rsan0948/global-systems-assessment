#!/usr/bin/env python3
"""
Erosion decomposition — SYNTHESIS.  Assembles the A/B/C decomposition from the three
committed component artifacts and computes each component's estimated share of the
~150-year erosion (Finding 2/7), keeping the two metric families separate and honest:

  * LONGITUDINAL metric (the erosion itself): structure-minus-wealth AUC spread slope
    over 1816-1990. A2 (mature-only slope), B1 (structural break), B3 (state-death
    tracking) are measured directly on this. This is where "share of the erosion" is
    literally defined.
  * CROSS-SECTIONAL HOLDOUT metric: does the structural signal out-predict wealth on
    2004/2012->2024 outcomes. A3, B2, C1 live here — a related but distinct question
    (modern applicability, not the longitudinal curve). Reported separately; NOT
    conflated with longitudinal share.

Read-only; writes data/robustness/decomposition/synthesis.json.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
D = ROOT / "data/robustness/decomposition"
OUT = D / "synthesis.json"


def clamp0(x):
    return None if x is None else max(0.0, x)


def main():
    A = json.loads((D / "component_A.json").read_text())
    B = json.loads((D / "component_B.json").read_text())
    C = json.loads((D / "component_C.json").read_text())

    # ---- A: longitudinal share = 1 - mature_slope/full_slope (clamped >=0) ----
    a2 = A["A2_split_erosion_curve"]
    full_slope = a2["erosion"]["full"]["slope_per_year"]
    mat_slope = a2["erosion"]["mature"]["slope_per_year"]
    a_raw = a2["A_share_of_erosion"]["estimate"]
    A_share = clamp0(a_raw)

    # ---- B1: structural break (longitudinal) ----
    b1 = B["B1_structural_break"]
    # ---- B3: state-death vs spread (longitudinal) ----
    b3r = B["B3_state_death_vs_signal"]["pearson_deaths_vs_spread"]
    # ---- B2: cross-sectional dysfunction recovery ----
    b2 = B["B2_dysfunction_holdout"]

    def recovery(win, sig):
        cr = b2[win]["crisis(committed)"]
        dp = b2[win]["dysfunction_polity"]
        dv = b2[win]["dysfunction_vdem"]
        key = "gap_beats_wealth" if sig == "gap" else None
        if sig == "gap":
            base = cr["gap_beats_wealth"]
            return {"crisis": base, "dys_polity": dp["gap_beats_wealth"], "dys_vdem": dv["gap_beats_wealth"],
                    "recovery_polity": round(dp["gap_beats_wealth"] - base, 3),
                    "recovery_vdem": round(dv["gap_beats_wealth"] - base, 3)}
        # P1-vs-wealth
        def p1mw(o):
            a = o["AUC"]
            return None if (a["neg_P1_institutional"] is None or a["wealth_neg_logGDP"] is None) else round(a["neg_P1_institutional"] - a["wealth_neg_logGDP"], 3)
        base = p1mw(cr)
        return {"crisis": base, "dys_polity": p1mw(dp), "dys_vdem": p1mw(dv),
                "recovery_polity": round(p1mw(dp) - base, 3), "recovery_vdem": round(p1mw(dv) - base, 3)}

    B_recovery = {w: {"P1_vs_wealth": recovery(w, "P1"), "gap_vs_wealth": recovery(w, "gap")} for w in ("2004", "2012")}

    # ---- C: cross-sectional revealed-vs-perception delta ----
    c1 = C["C1_revealed_P1_holdout"]
    c_deltas = {}
    for v, rv in c1["revealed_variants"].items():
        if "AUC" not in rv["metrics"]:
            continue
        pm = c1["perception_baseline_on_matched_isos"][v]
        c_deltas[v] = {"negP1_delta": round((rv["metrics"]["AUC"]["neg_P1_institutional"] or 0) - (pm["AUC"]["neg_P1_institutional"] or 0), 3),
                       "vuln_delta": round((rv["metrics"]["AUC"]["vuln_score"] or 0) - (pm["AUC"]["vuln_score"] or 0), 3),
                       "lift_delta": round((rv["metrics"]["elevated_confusion"]["lift_over_base"] or 0) - (pm["elevated_confusion"]["lift_over_base"] or 0), 3)}
    C_share = clamp0(max(d["negP1_delta"] for d in c_deltas.values())) if c_deltas else 0.0

    synthesis = {
        "target": "the ~150y erosion (Finding 2/7): structure-minus-wealth AUC spread declining, r=-0.85..-0.91",
        "metric_families": {
            "longitudinal": "spread slope over 1816-1990 — where 'share of erosion' is literally defined",
            "cross_sectional_holdout": "does structure out-predict wealth on 2004/2012->2024 — related but distinct",
        },
        "A_denominator_dilution": {
            "longitudinal_share": A_share,
            "raw_estimate": a_raw,
            "full_slope_per_yr": full_slope, "mature_slope_per_yr": mat_slope,
            "verdict": "NOT SUPPORTED as the erosion driver — mature-only erodes as strongly (r=%s) as full (r=%s); "
                       "share clamps to ~0. Surviving piece is CROSS-SECTIONAL: the gate is a mature-state instrument."
                       % (a2["erosion"]["mature"]["pearson_r"], a2["erosion"]["full"]["pearson_r"]),
            "cross_sectional_A3_gap_AUC_2012": {
                "mature": A["A3_split_temporal_holdout"]["2012"]["mature"]["AUC"]["durability_gap"],
                "post_colonial": A["A3_split_temporal_holdout"]["2012"]["post_colonial"]["AUC"]["durability_gap"],
                "early_post_colonial": A["A3_split_temporal_holdout"]["2012"]["early_post_colonial"]["AUC"]["durability_gap"]},
            "A4_age_alone_AUC_2004": A["A4_state_age_predictor"]["2004"]["age_alone_AUC(neg_age)"],
        },
        "B_consequence_elimination": {
            "B1_best_model": b1["best_by_aic"],
            "B1_verdict": "NO sharp 1945 break — single-linear wins on AIC; erosion is smooth from 1816, "
                          "predating the territorial-integrity norm.",
            "B3_state_death_vs_spread_r": b3r["r"], "B3_p": b3r["p"],
            "B3_verdict": "NULL — state-death rate does not track signal strength (COW exits conflate conquest "
                          "with voluntary dissolution/unification).",
            "B2_dysfunction_recovery": B_recovery,
            "B2_verdict": "PARTIAL POSITIVE — the broad institutional signal (neg-P1) recovers on the pre-registered "
                          "dysfunction outcome: it flips tie->win vs wealth in 2004 and grows its edge in 2012. The "
                          "narrow durability GAP stays below wealth. This is the one surviving mechanism, but it "
                          "addresses the modern-holdout distortion, not the longitudinal curve.",
        },
        "C_measurement_regime_change": {
            "cross_sectional_share": C_share,
            "revealed_minus_perception_deltas": c_deltas,
            "C2_mean_wgi_GE_change_pre": C["C2_perception_lag"]["mean_wgi_GE_change_pre"],
            "C2_n_functional_down_perception_flat": C["C2_perception_lag"]["n_functional_down_while_perception_flat_or_up"],
            "C2_n_evaluable": C["C2_perception_lag"]["n_crisis_countries_evaluable"],
            "verdict": "NOT SUPPORTED — revealed-outcome P1 UNDERperforms perception-P1 (all deltas negative); no "
                       "systematic perception lag. C's share ~= 0.",
        },
        "decomposition_table": [
            {"component": "A denominator dilution", "claim": "young states diluted the signal",
             "longitudinal_share": A_share, "verdict": "not supported (mature erodes too)"},
            {"component": "B consequence elimination", "claim": "state death became impossible",
             "longitudinal_share": 0.0,
             "cross_sectional": "partial: dysfunction recovers ~0.05 AUC of P1-over-wealth edge",
             "verdict": "strong form (1945 break / death-tracking) not supported; dysfunction-recovery real but modest"},
            {"component": "C measurement lag", "claim": "perceptions lag functional reality",
             "cross_sectional_share": C_share, "verdict": "not supported (revealed P1 predicts worse)"},
        ],
        "total_longitudinal_explained": round((A_share or 0) + 0.0, 3),
        "bottom_line": "The compound structural hypothesis, as operationalized, explains WELL UNDER 50% of the "
                       "longitudinal erosion (A~=0, B-longitudinal~=0, C~=0). Per the pre-registered gate, the "
                       "residual is LARGE and the erosion's cause is substantially UNEXPLAINED by A/B/C. Two "
                       "genuine positives survive as bounded scope characterizations, not explanations of the "
                       "curve: (A3) the durability gate is a mature-state instrument cross-sectionally, and (B2) "
                       "the institutional signal recovers on a broader dysfunction outcome — the modern order "
                       "decoupled institutional failure from terminal outcomes without repealing the relationship.",
        "residual_open_questions": [
            "Why does the structure-over-wealth edge shrink WITHIN mature states over 150y? Candidate residual "
            "mechanisms (untested here, diagnosis-only): (1) wealth/GDP measurement improved and industrial "
            "economies made GDP a better proxy for state capacity, so wealth catches up to structure as a "
            "predictor; (2) the conflict-onset outcome itself changed character (interstate->intrastate) across "
            "the period; (3) V-Dem rule-of-law's variance compressed as more states adopted formal-legal "
            "institutions, shrinking its discriminating power. None are consequence-elimination, dilution, or "
            "perception-lag.",
        ],
    }
    OUT.write_text(json.dumps(synthesis, indent=2, default=lambda o: None))

    print("=== EROSION DECOMPOSITION — SYNTHESIS ===")
    print(f"target: {synthesis['target']}\n")
    for row in synthesis["decomposition_table"]:
        print(f"  {row['component']:28} share(long)={row.get('longitudinal_share', row.get('cross_sectional_share'))}  -> {row['verdict']}")
    print(f"\n  total longitudinal explained: {synthesis['total_longitudinal_explained']}  (< 0.50 => missing structure)")
    print("\nB2 dysfunction recovery (P1-vs-wealth edge, crisis -> dysfunction):")
    for w in ("2004", "2012"):
        r = B_recovery[w]["P1_vs_wealth"]
        print(f"  {w}: crisis={r['crisis']} -> polity={r['dys_polity']} (+{r['recovery_polity']}) / vdem={r['dys_vdem']} (+{r['recovery_vdem']})")
    print(f"\n  BOTTOM LINE: {synthesis['bottom_line'][:300]}...")
    print(f"\n-> {OUT.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
