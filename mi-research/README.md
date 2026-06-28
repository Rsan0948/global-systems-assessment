# Modernization Index Research Platform

A quantitative diagnostic framework for measuring how complex governance systems respond to structural stress. Validated across 20 modern case studies and 5 ancient empires.

## Quick Start

```bash
# Score a country
python scripts/score_country.py --country "Estonia" --year 2024

# Compare two countries
python scripts/compare_countries.py --a "Estonia" --b "Russia" --year 2024

# Run retrodiction protocol on a case study
python scripts/run_retrodiction.py --case case_studies/in_progress/your_case.json

# Find countries with similar configurations
python scripts/find_similar.py --country "Ukraine" --year 2020
```

## Project Structure

```
mi-research/
├── RESEARCH.md              # Standing instructions for AI research agents
├── FRAMEWORK.md             # Complete MI specification (source of truth)
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

- **MI Version:** LIVE (with Mods 4, 8 and Safeguards A-I)
- **Validated Cases:** 20 modern + 5 ancient (proxy)
- **Clean Confirmation Rate:** ~78% (range 62-85%)
- **Directional Accuracy:** ~100% (zero falsifications)
- **P1 Ordinality:** 20/20 cases confirmed
