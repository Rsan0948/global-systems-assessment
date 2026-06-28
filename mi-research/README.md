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

- **MI Version:** **MI v1** — the canonical methodology (correlation-derived weights +
  Mods 4, 8 and Safeguards A-I; formerly "LIVE"/v2). The old hand-assigned draft weights are
  archived (`WEIGHTS_ARCHIVED_HAND_V0`, not used). See
  `docs/architectural_decisions/mi_v1_naming_and_archive.md`.
- **Validated Cases:** 20 modern + 5 ancient (proxy), now backed by structured JSON
  records in `data/case_studies/completed/`; **+5 expansion cases (Batch 1, cases
  21-25)** scored on fresh real data — see `live/runs/run7_expansion_batch1_cases21-25.md`.
- **Clean Confirmation Rate:** ~78% (range 62-85%) on the baseline; Batch-1 ~75%.
- **Directional Accuracy:** ~100% (zero falsifications) — note this is partly
  structural (directional claims are hard to falsify) and partly redundant with WGI standalone.
- **P1 Ordinality:** 20/20 baseline; confirmed in every Batch-1 case where the gap
  exceeded the WGI margin (and correctly abstained, per Mod4, where it did not).

### Recent work (expansion Batch 1, 2026-06-27)
- **Rwanda architectural decision** settled (P1 kept composite, not decomposed):
  `docs/architectural_decisions/rwanda_p1_composite_vs_decomposed.md`
  (reproducible experiment in `sandbox/experiments/rwanda_p1_decomposition/`).
- **New country data** (real WGI 2025-anchored / UNDP HDR 2025 / WB WDI / FSI 2024)
  for Haiti, Dominican Republic, Venezuela, Colombia, DR Congo, Rwanda.
- **WGI 2025 vintage note:** new cases use 2025-anchored 0-100 scores; the legacy
  baseline used percentile ranks. Do not assert an ordinal across that vintage boundary.
