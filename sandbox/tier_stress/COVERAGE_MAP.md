# Phase 0 — Coverage map (predictive-reach campaign)

Sandbox worktree `sandbox/predictive-reach` off `0b9ceed`. Read-only probes only; nothing in the repo mutated.

## Predictors — back-score feasibility (score at year T)

| Instrument | Year-T score from | Window / coverage | Feasibility |
|---|---|---|---|
| **V1 Capacity** (MI, P1–P5, durability gap P4−P1) | `mi` engine via `panel.indicators_for(iso, T)` | 1996–2024 annual, 191 ctry | **STRONG** — free via engine, verified |
| **V2 Conversion** (Level, Equity, Combined, F1–F6, imbalance) | `v2_indicators.json` (recompute) | ~2005–2024 (early sparse) | MODERATE |
| **V3 Pressure** (numerator: anocracy, cso, pts, youth, food-imp, internet, ethnic-excl) | `political_indicators.json` | modern strong; cso→1789, pts 1976–2022 | **STRONG** (modern) |
| **T4 Scarring** (decayed conflict, trust, refugees, state-perp) | `tier4_indicators.json` + `conflict_onsets.json` | trust 1984+/115 ctry; conflict deep | MODERATE |
| **T5 Criticality** (trailing variance of libdem/electdem) | `vdem_democracy.json` | any T, 176 ctry, deep | **STRONG** |
| **T6 Spark** (mil-spend, resource-rents, refugees-hosted, borders) | `tier6_indicators.json` | 1970+, slow-moving | **STRONG** |
| **T7 Archetype** (categorical) | `six_tier_snapshot.json` | cross-section only | WEAK — excluded from forward screen |
| **DGS** (fragmentation leg) = z(ECI)−z(polyarchy) | `dgs_panel_real.json` | per (iso, period), forward-framed | **STRONG** |
| **ECI** (bonus, econ complexity) | DGS ingest | | MODERATE |
| Collectivization | 30 civilizational cases | not country-year | EXCLUDED (too coarse) |

## Outcome universe (value at year T+k)

- **Regime** (`vdem_democracy`, 176 ctry, 1789–2025): libdem / electdem / rol → level, Δ (backsliding vs democratization), trailing volatility.
- **Conflict** (`conflict_onsets`, 143 ctry, 1818–2023): onset-in-window binary, recurrence.
- **Econ/wellbeing** (`exploratory_outcomes`, 1960–2025): gdp_pc_growth, growth-vol, max-drawdown, inflation, inflation-vol, gross_savings, fdi_in, gov_debt_chg, net_migration, fertility, life_satisfaction (2011+), suicide (2000+), unemployment, patents, tourism_receipts, brain_health_ratio.

→ ~30–40 derived outcome variables.

## Panels
- **Primary (annual):** 1996–2020, leads k∈{1,3,5,10}. All tiers scoreable, full outcome set.
- **Deep (regime/conflict outcomes only):** ~1900–2010 with V1-proxy + V3 numerator + T5.

## Rigor harness
- **Discovery/confirmation split:** 191 countries hashed into half A (discover) / half B (confirm) — deterministic, sealed during discovery.
- **OOF:** country-clustered CV inside discovery (never resubstitution — the audit's core lesson).
- **Confounder:** GDPpc always partialled (partial-Spearman on rank residuals).
- **Multiplicity:** BH-FDR across the full discovery family.
- **Pooling — cohort cross-sections (avoids the H1 pseudoreplication trap):** fixed base-year grid b∈{1996,2000,2004,2008,2012,2016}; for each (b, lead k) form ONE row per country = (predictor@b, outcome@b+k). Each cohort is a clean cross-section (each country once). A predictor "predicts" an outcome at lead k only if the effect is FDR-significant AND sign-stable across cohorts (built-in replication) AND survives on the sealed confirmation-country half. No country-year is ever double-counted as independent.

## Tier year-T operationalizations (mirror the published composites, parametrized by year)
- **V1**: `mi.panel.indicators_for(iso,T)` → `calculate_pillar_scores`/`calculate_mi_score` → MI, P1–P5, durgap=P4−P1. Exact.
- **V3 numerator**: per `political_test.py` — anocracy=4·lib·(1−lib), cso, pts, youth, food_imp, internet, growth_vol(trailing), prior_conflict(decayed) + z-sum composite.
- **T4 scarring**: per `tier4_scarring.py` — decayed conflict (25y half-life) + trust(rev) + refugees_origin/pop + state-perp(pts).
- **T5 turbulence**: per `csd_corrected.py` — trailing 10y std of libdem/electdem ending at T.
- **T6 spark**: per `tier6_spark.py` — mil_spend, resource_rents, refugees_hosted, border adjacency (slow-moving).
- **DGS**: z(ECI)−z(polyarchy) from `dgs_panel_real.json`.
- Documented as *year-T operationalizations*, not the exact published cross-sectional snapshots — discovery instruments, not headline recomputations.
