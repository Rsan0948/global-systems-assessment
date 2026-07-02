# CLAUDE.md — MI Research Platform (agent guide)

The **scoring + diagnostic + retrodiction engine** for the Modernization Index
(MI): it consumes per-country governance indicators and produces MI scores,
pillar diagnostics, safeguard evaluations, and case-study validation. Separate
from the sibling `mi_pipeline/` (raw data build) and the root fragmentation
study — do not wire them together.

## Read first (in order)

1. **`RESEARCH.md`** — standing operating manual for research agents here.
2. **`MASTER_REFERENCE_ARCHITECTURE.md`** — source-of-truth spec. **Section 4**
   is the full MI specification.
3. This file — code/data layout + invariants.

## Quick start (verified)

```bash
cd mi-research
python scripts/score_country.py --country "Estonia" --year 2024   # ✓ MI 0.775, Tier 2
python scripts/compare_countries.py --a Estonia --b Norway
python scripts/find_similar.py --country Norway --top 5
python scripts/run_retrodiction.py --validate data/case_studies/completed/
```

Pure-Python stdlib for the scoring path — no third-party deps.

## The data path (ONE canonical store)

Indicators come from a **single file**, `data/sources/canonical_panel.json`,
read by **`mi/panel.py`** (the only runtime reader). Everything else in
`data/sources/` (`wb_anchored.json`, `wgi_full_panel.json`, `vdem_longrun.json`,
…) plus the sibling `mi_pipeline/` CSV are **build inputs**, not read at runtime.

```
raw sources ─► scripts/build_canonical_panel.py ─► data/sources/canonical_panel.json ─► mi/panel.py ─► engine
```

- `build_canonical_panel.py` resolves the source tiers (A wb_anchored > B
  mi_pipeline > C wgi_full_panel) + HDR **once, at build time**, and dedupes
  multi-iso countries. Re-run it when a raw source refreshes.
- `mi/panel.py` exposes `indicators_for(name_or_iso, year)`, `country_record`,
  `all_indicators`, `iter_universe`. `scoring.load_country_data` and the CLIs
  read through it. **There are no per-country data files** — do not re-add a
  `data/countries/` directory (that was removed; the panel supersedes it).

## Engine (`mi/`)

- `scoring.py` — `score_country`, `calculate_pillar_scores`, the normalizers
  (all clamp to [0,1]), `detect_scale_issues` (the scale guard), and
  `resolve_weights` (MI v2 equal default; time-varying option).
- `constants.py` — `LENS` (all thresholds/goalposts in one place), weight
  schemes, `TIERS`.
- `safeguards.py` — the lettered safeguards (A–J) + Mod4/Mod8. `diagnostics.py`
  — `full_diagnostic`, strategy/vulnerability. `durability.py` — the earned-vs-
  granted durability gap.
- `panel.py` — canonical-panel reader (above). `datasource.py` — WGI-anchored
  source reader (build-time). `relational.py` / `global_systems.py` — the T3
  relational layer and system-level (golden-age / global-systems) research
  modules (not part of country scoring).

## Scripts (`scripts/`)

- **Data/site build:** `build_canonical_panel.py` → `build_site_dataset.py` →
  `build_similar.py` → `build_relational.py` (the website's
  `scripts/refresh_and_build.py` chains these). `refresh_wgi_wdi.py` refreshes
  the raw WGI/WDI source.
- **CLIs:** `score_country.py`, `compare_countries.py`, `find_similar.py`,
  `run_retrodiction.py` (all cover any country in the panel; default `--year 2024`).
- Research/exploration scripts (`score_v2_cohorts.py`, `big_signals_scan.py`,
  `retag_corpus.py`, …) back the docs.

## Data + docs

- `data/case_studies/completed/` — the **51-case validation corpus** (case01…).
  `data/case_studies/templates/` — the case template. `data/baselines/`,
  `data/forecasts/` — reference results / prospective forecasts.
- `docs/` — the research history (start at `SYSTEM_STATE.md` and `HANDOFF.md`;
  `PROJECT_SYNTHESIS.md` is the capstone). `live/runs/` — canonical run writeups.
  `archive/v1/` — the frozen MI v1 (do not edit).
- `tests/test_scale_guard.py` — engine regression tests (`pytest tests/ -q`).

## Invariants (do not break)

1. **The 51-case corpus is the floor.** No change may degrade an existing case.
2. **0-100 indicator scale.** WGI/CPI/GII inputs are 0–100; the scale guard hard-
   fails out-of-domain values and flags suspicious ones. Never feed raw WGI
   estimates (z-scores). All pillar normalizers clamp to [0,1].
3. **Deterministic.** Same inputs → same outputs; the site build is stable
   across runs. Keep it that way (sorted iteration, stable tiebreaks).
4. **One data store.** The canonical panel is it; raw sources are build inputs.
5. **Honest reporting; additive improvement.** Document every result; extend
   rather than remove; don't claim timing or calibrated probabilities.
