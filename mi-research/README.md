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

- **MI Version:** **MI v2** (live; `MI_ACTIVE_WEIGHTING="equal"`). Equal pillar weights, graded
  Safeguard E (E-1/E-2), refined Strategy 3, + two new outputs (durability ratio, below-floor
  diagnostic). V1 (correlation-derived weights) is frozen at tag `mi-v1` / `archive/v1`. Decisions:
  `docs/architectural_decisions/v2_*.md`; synthesis: `docs/v2_synthesis_35cases.md`.
- **Validated Cases:** **35 under V2** — 25 redone (cases 1–25) + 10 new (26–35, Batch 2+3:
  Ghana/CDI, Malaysia, Argentina, Lebanon, Iraq, Vietnam, Korea/Taiwan, Fiji, Bolivia, Aceh).
  See `live/runs/run8_v2_batch2-3_cases26-35.md`.
- **Clean Confirmation Rate (V2):** **~74%** across 35 cases (154C/53P/0F), within the honest
  62–85% range; **zero falsifications** across 207 predictions. The 25 redone tie V1 exactly
  (weighting immaterial); the 10 new are ~75% clean.
- **Directional Accuracy:** ~100% (zero falsifications) — partly structural; capacity partly
  redundant with WGI standalone.
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
