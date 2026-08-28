# Modernization Index Research Platform

A quantitative diagnostic for describing how governance systems are structured and how they have responded to stress in the historical record. The research corpus contains 84 modern hindsight cases and 25 ancient interpreter-scored cases. The canonical panel contains up to 191 country records, while the current public atlas publishes 190 scored profiles.

## Public scoring contract

The public country score is **MI v3.3**. It is the mean of the five available
pillar scores, with each pillar assigned an equal 20% weight when all five are
present. Public results are grouped into five descriptive **score bands**.

The older correlation-derived weights are retained as the `v1_correlation`
sensitivity model so past work can be reproduced. They are not the public
MI v3.3 score. The separate V1 through V6 research extensions are called
**model layers**, not score classifications.

## Quick Start

```bash
# Score a country
python scripts/score_country.py --country "Estonia" --year 2024

# Compare two countries
python scripts/compare_countries.py --a "Estonia" --b "Russia" --year 2024

# Run retrodiction protocol on a case study
python scripts/run_retrodiction.py --case data/case_studies/completed/case21_haiti_dominican_republic.json

# Validate the case-study database (scorecard across completed cases)
python scripts/run_retrodiction.py --validate data/case_studies/completed/

# Find countries with similar configurations
python scripts/find_similar.py --country "Venezuela" --year 2023
```

## Project Structure

```
mi-research/
├── RESEARCH.md              # Research protocol, project state, and open work
├── MASTER_REFERENCE_ARCHITECTURE.md  # Complete MI specification, with Section 4 as the scoring source of truth
├── mi/                      # Core scoring and diagnostic engine
│   ├── constants.py         # Weights, thresholds, indicator specs
│   ├── scoring.py           # MI scoring engine
│   ├── safeguards.py        # All safeguards (A-G) + essential mods
│   └── diagnostics.py       # Configuration analysis, strategy classification
├── data/
│   ├── sources/             # Canonical panel (191 countries) + raw indicator sources
│   ├── case_studies/        # Retrodiction case studies
│   │   ├── completed/       # 84 modern hindsight-retrodictive cases
│   │   ├── ancient/         # 25 pre-modern cases (firewalled, lowest-confidence)
│   │   ├── in_progress/     # Cases being developed
│   │   └── templates/       # Template for new cases
│   └── baselines/           # Historical baseline results (do not modify)
├── sandbox/                 # Experimental modifications
│   └── experiments/         # Each experiment gets a directory
├── scripts/                 # CLI tools
└── docs/                    # Additional documentation
```

## Core Principles

1. **The 84-case modern corpus is the floor.** Any modification must not degrade performance on existing cases.
2. **Honest reporting.** Every confirmation, partial result, and falsification is documented with full reasoning.
3. **Additive improvement.** New safeguards, new case studies, new indicators extend the framework. Nothing is removed without documented justification.
4. **Reproducibility.** Given the same inputs, the scoring engine produces the same outputs. Every calculation is deterministic.

## Current Status

- **MI Version:** **MI v3.3** (live; `MI_MODEL_VERSION="v3.3"`). V3.3 = V3.2 + the **level-over-slope**
  epistemic made operational: `ascent_potential` (low base → durable-climb tendency; the one
  holdout-validated golden-age signal, z+2.4) + `movement_quality` (names windfall / hollow_stability /
  real_ascent with a distrust-the-slope caveat). The golden-age *signature* (component jumps) was
  **refuted on a pre-registered geographic holdout** (z=−0.0) and deliberately NOT added. See
  `docs/v3_3_inclusion_and_global_picture.md`, `golden_age_holdout_and_structure.md`. V3.2 = V3.1 +
  **Convergence Qualifier** on Safeguard J (gap trajectory; 92/80) + **Accountability Gap** (VA vs
  income; hypothesis). V3.1 = V3 + **Safeguard J - Durability Gate** (P4−P1, three-state), N=21
  (83/100/100). See `v3_2_convergence_and_accountability.md` + `v3_1_durability_gate.md`.
- **Corpus:** **84 case studies**, three classes scored separately by `--validate`: 51 P1-ordinality
  (213C/77P/0F) + 19 durability-gate / Safeguard-J (17/19) + 14 rule-validation A/B (8 confirmed /
  2 indeterminate / 2 falsified; 2 pre-WGI N/A). The rule-validation set (`docs/c_cases_blind_validation.md`)
  was run blind: it *strengthened* the Convergence Qualifier (the qualifier correctly handles the
  petro-state the source doc called its strongest disconfirmation - so the doc's rent-control add-on
  is unnecessary) and *refuted* the Accountability Gap as a crisis predictor (Cuba legitimacy-capped,
  no crisis) - B stays an informational hypothesis.
- **MI v3 base:** V3 = V2 + the **consolidated-pair
  high-end caution** (Mod4 extension: between two polities both P1 > 0.60, abstain on an ordinal
  call unless the gap ≥ 0.15 - derived from the Chile/Uruguay falsification; complexity-capacity:
  above the threshold, capacity differences don't predict trajectory). V2 (equal weights, graded
  Safeguard E, durability + below-floor outputs) frozen at tag `mi-v2`; V1 at `mi-v1`. Decisions:
  `docs/architectural_decisions/v2_*.md` + `v3_improvement_analysis.md`.
- **Historical ordinality cases:** **51** - 25 redone (1–25) + 26 new (26–51, incl. revisions 47 Cameroon /
  49 Mauritius / 51 Somaliland). Runs: run7 (21–25), run8 (26–35), run9 (36–51); synthesis
  `docs/v2_synthesis_51cases.md`.
- **Clean Confirmation Rate (V3):** **~73%** across 51 cases (213C/77P/**0F**), honest range 62–85%.
- **Historical directional tally:** **100%** - restored from V2's 99.7% not by hiding the lone V2
  falsification (Chile/Uruguay, kept at tag `mi-v2`) but by **bounding the P1-ordinal claim**: V3
  abstains between two consolidated polities, where a 3.5σ P1 gap was shown not to predict trajectory.
  This is a bounded hindsight-retrodictive tally, not a forward prediction rate.
  (Partly structural; capacity partly redundant with WGI standalone.)
- **P1 Ordinality / centrality:** ordinality holds **independent of weighting** (the V1 P1=0.34
  "centrality" was a sample/time-point artifact; the pillar rotates and sits in a 0.71–0.80 band).
  See `docs/architectural_decisions/v2_p1_centrality_restatement.md`.

### Recent work (expansion Batch 1, 2026-06-27)
- **Rwanda architectural decision** settled (P1 kept composite, not decomposed):
  `docs/architectural_decisions/rwanda_p1_composite_vs_decomposed.md`
  (reproducible experiment in `sandbox/experiments/rwanda_p1_decomposition/`).
- **New country data** (real WGI 2025-anchored / UNDP HDR 2025 / WB WDI / FSI 2024)
  for Haiti, Dominican Republic, Venezuela, Colombia, DR Congo, Rwanda.
- **WGI 2025 vintage note:** new cases use 2025-anchored 0-100 scores; the legacy
  baseline used percentile ranks. Do not assert an ordinal across that vintage boundary.
