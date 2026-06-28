# CLAUDE.md — MI Research Platform (agent guide)

A **self-contained research platform**, separate from everything else in this
repo. It is NOT the same project as the sibling `mi_pipeline/` (that one builds
the raw indicator dataset from World Bank + manual CSVs); this one is the
**scoring + diagnostic + retrodiction engine** that consumes per-country
indicator data and produces MI scores, configuration analysis, and case-study
validation. It is also distinct from the `universalsystemgrade` fragmentation
study at the repo root — though the master architecture doc ties them together
conceptually (rivers Rb ≈ 3.5 → the "self-organizing systems fragment in
concentrated bands" thesis the MI operationalizes). Do not wire these projects'
code together.

## Read these first (in order)

1. **`RESEARCH.md`** — standing instructions for AI research agents working on
   this platform. This is your operating manual; follow it.
2. **`MASTER_REFERENCE_ARCHITECTURE.md`** — the source-of-truth spec and full
   intellectual scaffolding (book + companion guide). **Section 4** is the
   complete MI specification. The `README.md` refers to a `FRAMEWORK.md` "source
   of truth" that was never shipped in the upload — that reference resolves to
   this document (Section 4).
3. **`README.md`** — quick start + project structure.

## Quick start (verified working)

```bash
cd mi-research
python scripts/score_country.py --country "Estonia" --year 2024   # ✓ MI 0.778, Tier 2 (MI v1, 2025-anchored)
python scripts/run_retrodiction.py --validate data/case_studies/completed/
```

No third-party deps for the scoring path (pure-Python stdlib). Indicator data is
served by the internal **Data API** (`mi/datasource.py`), which assembles values
live from the canonical sources — `data/sources/wb_anchored.json` (World Bank
2025-anchored WGI/WDI; refresh via `scripts/refresh_wgi_wdi.py`) + the committed
`mi_pipeline/` panel CSVs. There are no per-country copy files. The scoring *lens*
lives in `mi/constants.LENS` (one place; propagates on re-score). Methodology is
**MI v1** (the former "LIVE"; old hand weights archived). NB: Estonia is 0.778 on
the consistent 2025-anchored vintage — the legacy 0.793 used percentile-rank inputs.

## Core principles (from README — honor these)

1. **The 20-case baseline is the floor.** No modification may degrade performance
   on existing cases.
2. **Honest reporting.** Every result — confirmation, partial, or falsification —
   is documented with full reasoning.
3. **Additive improvement.** Extend (new safeguards/cases/indicators); don't
   remove without documented justification.
4. **Reproducibility.** Scoring is deterministic: same inputs → same outputs.

## State of this scaffold — what's here vs. what an agent must add

This is a **seed**, not the full validated corpus. Present:
- Engine: `mi/` (`constants.py`, `scoring.py`, `safeguards.py`, `diagnostics.py`).
- Scripts: `score_country.py`, `run_retrodiction.py`.
- Data: **only** `data/countries/estonia.json` and one case-study template.
- Empty (`.gitkeep`) slots matching the documented layout:
  `data/case_studies/{completed,in_progress}`, `data/baselines`,
  `sandbox/experiments`, `docs`.

Gaps to be aware of (the README/quick-start over-promises relative to the upload):
- **The 20-case baseline is NOT included** — `data/case_studies/completed/` and
  `data/baselines/` are empty. The "~78% confirmation, 20/20 P1 ordinality"
  claims cannot be reproduced here until those cases are added. Treat them as the
  target to rebuild, not as present evidence.
- **Only Estonia has country data.** Any other `--country` will fail until you add
  `data/countries/<name>.json` (follow the `estonia.json` shape).
- **Two README-referenced scripts don't exist:** `scripts/compare_countries.py`
  and `scripts/find_similar.py`. Build them (or correct the README) before
  relying on those commands.

## Fix already applied

`mi/safeguards.py` had an invalid f-string format specifier
(`{p1:.3f if p1 else 'N/A'}`) that crashed `full_diagnostic` — i.e. the headline
`score_country.py` command failed out of the box. Corrected to
`{f'{p1:.3f}' if p1 else 'N/A'}`. Verified by scoring Estonia end-to-end. No
scoring logic was changed.

## Conventions

- `data/` holds JSON inputs/cases; generated experiment results under
  `sandbox/experiments/*/results/` are gitignored (see `.gitignore`).
- Keep changes additive and deterministic per the principles above.
