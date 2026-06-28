# Modernization Index Research Platform

A quantitative diagnostic framework for measuring how complex governance systems respond to structural stress. Validated across 20 modern case studies and 5 ancient empires.

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
├── RESEARCH.md              # Standing instructions for AI research agents
├── MASTER_REFERENCE_ARCHITECTURE.md  # Complete MI specification — Section 4 (source of truth; the old "FRAMEWORK.md" reference resolves here)
├── mi/                      # Core scoring and diagnostic engine
│   ├── constants.py         # Weights, thresholds, indicator specs
│   ├── scoring.py           # MI scoring engine
│   ├── safeguards.py        # All safeguards (A-G) + essential mods
│   └── diagnostics.py       # Configuration analysis, strategy classification
├── data/
│   ├── countries/           # Country indicator data (JSON per country)
│   ├── case_studies/        # Retrodiction case studies
│   │   ├── completed/       # Validated cases (the 20-case baseline)
│   │   ├── in_progress/     # Cases being developed
│   │   └── templates/       # Template for new cases
│   └── baselines/           # Validated baseline results (do not modify)
├── sandbox/                 # Experimental modifications
│   └── experiments/         # Each experiment gets a directory
├── scripts/                 # CLI tools
└── docs/                    # Additional documentation
```

## Core Principles

1. **The 20-case baseline is the floor.** Any modification must not degrade performance on existing cases.
2. **Honest reporting.** Every result — confirmation, partial, falsification — is documented with full reasoning.
3. **Additive improvement.** New safeguards, new case studies, new indicators extend the framework. Nothing is removed without documented justification.
4. **Reproducibility.** Given the same inputs, the scoring engine produces the same outputs. Every calculation is deterministic.

## Current Status

- **MI Version:** **MI v3.2** (live; `MI_MODEL_VERSION="v3.2"`). V3.2 = V3.1 + the **Convergence
  Qualifier** on Safeguard J (gap TRAJECTORY: closing = developmental catch-up vs widening = fragility;
  92% sens / 80% spec) + the **Accountability Gap** diagnostic (VA vs income; "capacity without
  consent" — a hypothesis, informational). V3.1 = V3 + **Safeguard J — the Durability Gate** (P4−P1
  gap, three-state flag/clear/borderline), N=21 (83/100/100; = durability ratio re-derived). See
  `docs/architectural_decisions/v3_2_convergence_and_accountability.md` + `v3_1_durability_gate.md`.
- **Corpus:** **70 case studies** = 51 P1-ordinality (`completed/`, stress_type ≠ durability_gate_test)
  + 19 durability-gate / Safeguard-J tests (stress_type=durability_gate_test). `--validate` reports
  the two classes separately.
- **MI v3 base:** V3 = V2 + the **consolidated-pair
  high-end caution** (Mod4 extension: between two polities both P1 > 0.60, abstain on an ordinal
  call unless the gap ≥ 0.15 — derived from the Chile/Uruguay falsification; complexity-capacity:
  above the threshold, capacity differences don't predict trajectory). V2 (equal weights, graded
  Safeguard E, durability + below-floor outputs) frozen at tag `mi-v2`; V1 at `mi-v1`. Decisions:
  `docs/architectural_decisions/v2_*.md` + `v3_improvement_analysis.md`.
- **Validated Cases:** **51** — 25 redone (1–25) + 26 new (26–51, incl. revisions 47 Cameroon /
  49 Mauritius / 51 Somaliland). Runs: run7 (21–25), run8 (26–35), run9 (36–51); synthesis
  `docs/v2_synthesis_51cases.md`.
- **Clean Confirmation Rate (V3):** **~73%** across 51 cases (213C/77P/**0F**), honest range 62–85%.
- **Directional Accuracy:** **100%** — restored from V2's 99.7% not by hiding the lone V2
  falsification (Chile/Uruguay, kept at tag `mi-v2`) but by **bounding the P1-ordinal claim**: V3
  abstains between two consolidated polities, where a 3.5σ P1 gap was shown not to predict trajectory.
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
