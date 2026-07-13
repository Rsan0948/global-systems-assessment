# Predictive-reach campaign — sandbox

**Question:** what do the MI apparatus and its tiers (V1 capacity, V2 conversion, V3 pressure, T4 scarring, T5 criticality, T6 spark) + the fragmentation DGS leg *actually predict* — going forward, beyond what a country's own past already tells you?

Sandbox only: branch `sandbox/predictive-reach` off `0b9ceed`; nothing here touches the real tree. Python 3.13 + numpy + scipy.

## Run it
```
python3 run_all.py            # integrity tests (hard gate) + full pipeline
python3 run_all.py --quick    # skip the ~1-min exhaustive search
python3 test_harness.py       # just the integrity/regression tests (12, all green)
```

## Method (the rigor, in one place)
- **Predict-forward:** score each instrument at year *T*, test against outcomes at *T+k* (k∈{1,3,5,10}).
- **Cohort cross-sections** (one row per country per base-year) — no pseudoreplication.
- **Three honest splits:** country-hash discovery/confirmation (`forward_screen`), a FIT/SEL/TEST third split for the combinatorial search (`combo_search`), and a **temporal holdout** for the real out-of-time test (`confirm_oot`).
- **Always net of an AR(lagged-outcome)+GDP baseline** — separates forecasting from persistence.
- **No in-sample numbers.** Every reported skill is on held-out countries or future years.

## Pipeline (dependency order)
| script | what it does | key output |
|---|---|---|
| `build_panels.py` | back-scores every tier at each year × the outcome universe (needs sibling `mi-research/`) | `predictors.json`, `outcomes.json` |
| `forward_screen.py` | univariate screen, discovery→sealed-half confirmation | `screen_confirmed.json` |
| `forecast_test.py` | AR-baseline test: forecast vs persistence | `forecast_test.json` |
| `stack_screen.py` / `stack_validate.py` | additive stacking, interactions, lead replication | `stack_*.json` |
| `combo_search.py` | exhaustive ~21k-subset search, internals broken out (three-way split) | `combo_results.json` |
| `calib.py` | bootstrap CI + calibration of the stacked model | — |
| `relational_screen.py` / `relational_validate.py` | **gaps/ratios between instruments** vs additive | `relational_results.json` |
| `confirm_oot.py` | **out-of-time temporal confirmation** | `confirm_oot_results.json` |
| `robustness.py` | rolling-origin, λ-sweep, placebo, threshold, determinism | — |
| `deep_time.py` / `deep_horizon.py` | **same math back to 1820**, lead horizon swept to k=30, by era | `deep_time_results.json` |
| `deep_democratization.py` | the capacity→democratization composition shift (saturation vs decoupling) | — |
| `deep_cohort_test.py` | prospective test: do capacity-poor post-1975 democracies backslide more? | `cohort_test_results.json` |
| `deep_audit.py` | adversarial audit: V-Dem circularity, independent-capacity cross-check, permutation null, tolerance, leakage | — |
| `angle1_dynamic.py`..`angle6_*` + `country_attrs.py` | the six deep angles (see `PREDICTION_LEDGER.md` / `READINESS.md`) | `angleN_results.json` |
| `common.py` | shared substrate for the six deep angles (data + rigor primitives, no drift) | — |
| `deep_readiness.py` | readiness probe for the six angles (see `READINESS.md`) | — |
| `test_harness.py` | integrity/regression tests | — |

## Findings (full writeup in `PREDICTION_LEDGER.md`)
1. **Two modes.** The apparatus *nowcasts* structural state superbly (ρ 0.6–0.9 on levels) but that's persistence — it **collapses under an AR baseline**. Genuine forecasting is modest (|ρ| 0.2–0.4).
2. **What it genuinely forecasts:** conflict onset (the scarring trap, to 10y), future **life-satisfaction** and **GDP growth** (capacity), emigration (durability gap). Wellbeing is the standout cross-domain reach.
3. **Mixing:** stacking cracks **democratic backsliding**, which no single tier could (AUC ~0.7). "Tiers add, don't multiply" confirmed. Exhaustive subset-hunting *overfits*; the honest winner is regularized-everything.
4. **Relational beats additive:** the **gaps/ratios between** instruments forecast backsliding better than their levels (AUC 0.72 vs 0.56) — vindicating MI's relational design. Strongest single relationship: capacity − turbulence.
5. **Out-of-time verdict (the real test):** the relational edge **confirms in 2 of 3 rolling-origin windows** (+0.11 to +0.16) but **fails on the 2016–2023 wave** — diagnostically, because that wave hit wealthy democracies and the level+wealth baseline is already saturated. Not overfitting (λ-robust), not leakage (placebo ~0.5).

## Caveats carried throughout
DGS iso recovered by population-fingerprint (144 isos); `v3_numer` omits EPR ethnic-exclusion (network); T4/T6 are z-sum operationalizations, not the exact published snapshots; life-satisfaction panel starts 2011; backsliding event counts are modest (wide CIs). These are **leads to pre-register**, not causal claims.
