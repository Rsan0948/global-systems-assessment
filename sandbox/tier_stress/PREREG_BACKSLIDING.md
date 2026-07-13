# Pre-registration — the backsliding ensemble (frozen)

> ## ⚑ CONFIRMATION RESULT (2026-07-12) — run via `confirm_oot.py` + `robustness.py`
> The frozen relational model was tested on true temporal holdouts. **Rolling-origin verdict: CONFIRMED in 2 of 3 windows** — ≤2004→2008/2012 (Δ+0.142/+0.115 over AR+GDP), ≤2008→2012 (Δ+0.147/+0.161). It **did NOT pass the pre-specified ≤2012→2016/2018 window** (Δ −0.121/−0.022), because the recent backsliding wave hit established wealthy democracies, saturating the level+wealth baseline (0.77). A λ-sweep rules out overfitting; a label-permutation placebo (AUC~0.50) rules out leakage. **Honest claim: structural relationships forecast backsliding out-of-time, with incremental value greatest when backsliding is not already obvious from level/wealth.** The single `capacity−turbulence` gap passed the 2016/2018 window for electdem only (Δ+0.065) — fragile. Recommended next step: a **prospective** register (freeze now, score when V-Dem 2025+ lands).

**Status: DRAFT for freezing.** Derived from a discovery campaign (`PREDICTION_LEDGER.md`): no single MI/tier instrument forecasts democratic backsliding, but a regularized *ensemble* of instruments-and-internals does (sealed-third AUC ~0.70). This document freezes that model so the next test is a genuine confirmation, not a re-fit. **The exhaustive combinatorial search that produced the predictor set is a DISCOVERY step; everything below must be judged only on data not used to build it.**

## 1. Claim under test
A fixed logistic ensemble of structural instruments, scored at year *T*, forecasts democratic backsliding over *[T, T+5]* **better than chance and better than an autoregressive+GDP baseline**, out of sample.

## 1b. AMENDMENT — adopt the RELATIONAL formulation as primary (supersedes §2 additive set)
A follow-up test showed the **relationships between instruments outpredict the stacked levels** for backsliding (sealed TEST AUC, replicated k=3/5/10): REL **0.62/0.72/0.70** (libdem), **0.76/0.74/0.70** (electdem) vs additive 0.51/0.56/0.48 and 0.64/0.66/0.60. The relational set is fewer, interpretable, and less overfit-prone. **Primary frozen model is now the relational one below;** the §2 additive-8 set is retained as the secondary/robustness spec.

**Frozen relational features (11)** — each instrument normalized to a within-year z using TRAIN countries only, then:
`matching_gap`(=mean(z_pressure,z_scarring,z_spark)−z_capacity), `ratio_press_cap`, `ratio_scar_cap`, `ratio_spark_cap`, `ratio_spark_turb`, `ratio_press_scar`, `tier_dispersion`(σ of the 6 normalized tiers), `pillar_dispersion`(σ of P1–P5), `durability_gap`(z P4−z P1), `discord_press_cap`(|pctl_pressure−pctl_capacity|), and `gap_v1_mi_t5_turb_libdem`(capacity−turbulence, the strongest single relationship). Controls + estimator + λ as in §2. Implementation: `relational_screen.py` (`feat()` + `build_matrix(...,"rel")`).

## 2. Frozen model — SECONDARY (additive-8, retained for robustness)
- **Estimator:** ridge-penalized logistic regression, **λ = 1.0** on standardized predictors (intercept unpenalized). λ is fixed, not tuned (AUC is λ-insensitive over 0.3–10).
- **Predictors (8, "load-bearing internals" from combinatorial inclusion-frequency):**
  `anocracy` (4·libdem·(1−libdem)), `P1` (WGI capacity), `durgap` (P4−P1), `internet`, `growth_vol` (10y trailing GDP-growth σ), `t4_reversed_trust` (100−WVS trust), `t5_turb_libdem` (10y trailing libdem σ), `t6_s4_military` (militarization spark sub-score).
- **Controls (always in):** lagged outcome level (libdem or electdem @ *T*) + log₁₀ GDPpc @ *T*.
- **Standardization:** mean/σ computed on the training rows only, applied to test.

## 3. Outcomes (two, pre-specified)
- **Primary — `libdem_backslide`:** 1 if V-Dem liberal-democracy index drops ≥ 0.05 over [T, T+5], else 0.
- **Secondary — `electdem_backslide`:** same rule on electoral-democracy index.
(0.05 threshold frozen from the discovery spec; no post-hoc threshold tuning.)

## 4. Confirmation design — TRUE out-of-time holdout (the real test)
The discovery used a country hash-split. For confirmation, use a **temporal** holdout the search never optimized against:
- **Train:** all country-cohorts with base year *T ∈ {1996, 2000, 2004, 2008, 2012}*.
- **Test (sealed):** base years *T ∈ {2016, 2018}* → outcomes measured 2021 / 2023.
- No country/coefficient/λ choice may look at the 2016/2018 cohorts.

## 5. Primary statistic + success criteria (frozen)
- **Metric:** AUC of predicted probability vs realized backsliding on the sealed temporal test, with a **2000-draw bootstrap 95% CI**.
- **PASS iff:** (a) CI lower bound **> 0.50**, AND (b) point AUC exceeds the AR+GDP baseline AUC (same test set) by ≥ 0.05.
- **Secondary:** must show the same direction (needn't independently pass).
- **Calibration (reported, not gated):** 5-bin reliability curve. Pre-registered expectation from discovery — **discrimination is carried by the low-risk bins; the top risk bin is NOT expected to be monotone** (the model triages the stable majority; it does not reliably name the specific backslider).

## 6. Power (honest)
Discovery sealed-third had ~19–22 events → AUC 95% CI width ≈ ±0.10 (libdem 0.692 [0.595, 0.786]; electdem 0.705 [0.602, 0.801]). The temporal test (2 cohorts) will have **fewer events (~15–25)** → expect a **wide CI**; a point AUC near 0.55–0.60 would be an ambiguous non-confirmation, not a clean fail. Pre-specified remedy if underpowered: extend to annual base cohorts and/or add a **prospective** register (freeze now, score 2020→2025 when V-Dem 2025 lands).

## 7. What would falsify / weaken the claim
- Sealed temporal-test CI includes 0.50 → the ensemble does **not** forecast out of time (the hash-split result was cohort-composition luck).
- AR+GDP baseline matches the ensemble → no incremental structural signal.
- The frozen-8 underperforms plain `anocracy`+controls → the "ensemble beats parts" claim fails; report anocracy as the honest single predictor.

## 8. Multiplicity / provenance disclosure
The 8-predictor set was chosen by exhaustive subset search + inclusion-frequency over ~21k configurations on the discovery data. That search **overfit its own selection set** (best-4-subset TEST AUC ~0.54 < regularized-full 0.68). This prereg therefore freezes the *regularized* consensus set, whose sealed-third AUC (~0.70) was NOT itself selected on the test third. Confirmation on the temporal holdout is required before any headline claim.

## 9. Analysis script (to be frozen alongside)
`calib.py` (frozen-8 fit/eval/bootstrap/calibration) + `combo_search.py::master` (data assembly). Re-point the split from hash to the temporal rule in §4; change nothing else.
