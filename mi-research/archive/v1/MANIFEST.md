# MI v1 — FROZEN ARCHIVE (2026-06-28)

This directory is a **frozen snapshot of the MI v1 corpus** — the methodology, configuration,
data vintage, and the 25 completed case studies as they stood before Phase 2 / the V2 model.
Do not edit anything under `archive/`. It exists so V2 work can overwrite the live files while
V1 remains readable and reproducible, and so V1↔V2 can be compared (and the Golden Rule checked:
V2 must not regress this baseline).

## Provenance
- **Git commit:** `acf3447c147b4b7506f1790bc9d6c43aa9cdc771`
- **Git tag:** `mi-v1` (annotated; checkout to restore the exact engine code of this state)
- **Branch:** `mi-research-batch1-rwanda-expansion` (PR #8)
- **Date frozen:** 2026-06-28

## What MI v1 is
- **Methodology:** MI v1 = the former "LIVE"/v2 — correlation-derived pillar weights
  (P1 0.34 / P2 0.15 / P3 0.16 / P4 0.20 / P5 0.16) + Mods 4 & 8 + Safeguards A–I.
  The old hand-assigned draft weights are archived (not used). Full lens in `config_frozen.json`.
- **Data:** World Bank **2025-anchored** WGI/WDI + the committed `mi_pipeline` panel
  (CPI/GII/ECI/FSI/HDR), assembled live via the internal Data API. Frozen WGI/WDI snapshot:
  `data_sources/wb_anchored.json`.
- **Architecture:** one lens config (`mi/constants.LENS`); one data source (Data API); case
  records reference `(country, year)` with locked predictions; mechanical verdicts auto-derived,
  judgment verdicts individually re-examined on real data.

## Results (this frozen state)
- **25 completed case studies** (`case_studies/`): 20 baseline (cases 1–20) + Batch 1 (21–25).
- **Aggregate:** see `validate_scorecard.txt` — **109 Confirmed / 38 Partial / 0 Falsified
  ≈ 74% clean, ~100% directional**. Honest range 62–85%; zero falsifications (partly by
  construction); capacity partly redundant with WGI standalone.
- **Estonia reference:** MI **0.778**, Tier 2 (2024, anchored). (Legacy percentile-vintage was 0.793.)
- **Rwanda architectural decision:** P1 kept composite (see `docs/`).

## Contents
- `config_frozen.json` — exact MI v1 weights + LENS + tiers + safeguard thresholds.
- `case_studies/` — the 25 completed records (reference-based, real-data-scored, judgment-refreshed).
- `data_sources/wb_anchored.json` — frozen WGI/WDI snapshot (reproduces V1 even if the live source
  is refreshed for V2).
- `runs/` — the Batch-1 run writeup. `docs/` — architectural decisions + the Rwanda experiment.
- `validate_scorecard.txt` — the frozen validation output.

## Reproduce V1
```bash
git checkout mi-v1        # restores the exact engine + data of this state
cd mi-research && python scripts/run_retrodiction.py --validate data/case_studies/completed/
```
