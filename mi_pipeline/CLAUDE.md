# CLAUDE.md — Modernization Index pipeline (local-agent guide)

This directory is a **self-contained scaffold** for a separate project from the
rest of this repo (which is the `universalsystemgrade` fragmentation study). It
does not import from, or share data with, anything outside `mi_pipeline/`. A
local agent picking this up should treat this folder as the project root.

## What this is

A pipeline that builds a Modernization Index (MI) country-year panel across 150+
countries × 5 time points (1996, 2004, 2012, 2018, 2024). It pulls 9 indicators
from the World Bank API, loads 5 manually-downloaded CSVs, merges/normalizes/
scores under two models (v1 anchor-based, v2 percentile-GPA), and writes CSV +
Excel + text reports to `./output/`. Full methodology is in `README.md`.

## How to run (local machine, open network)

```bash
cd mi_pipeline
pip install -r requirements.txt
python mi_pipeline.py --setup          # prints the 5 manual-download instructions
# download cpi.csv, gii.csv, eci.csv, hdr.csv, fsi.csv into ./data/
python mi_pipeline.py                  # ~5 min first run (WB API is rate-limited)
```

Outputs land in `./output/`. After the first successful run, `./data/wb_cached.csv`
exists and `python mi_pipeline.py --skip-api` reuses it.

## Why it was NOT run in the remote sandbox (confirmed, not assumed)

1. **Network policy blocks the data source.** `api.worldbank.org` returns HTTP 403
   from the sandbox proxy — the policy whitelists package registries (pypi, npm)
   and Anthropic only. The automated WGI/WDI pull returns empty there.
2. **The 5 manual CSVs require human downloads** from interactive portals
   (Transparency International, WIPO, Harvard Atlas, UNDP, Fund for Peace). This
   is a manual step on any machine.

The code itself is sound — it was smoke-tested in the sandbox with synthetic data
(full end-to-end: merge → normalize → pillars → v1/v2 → diagnostics → findings all
run clean). What could not run is the *real data acquisition*.

## Known issues — FIX THESE BEFORE TRUSTING THE FIRST REAL RUN

Ordered by severity. Items 1–3 can silently produce a result-shaped non-result.

1. **The gap counter is blind to entirely-absent data sources.** `compute_diagnostics`
   counts a missing indicator only via `c in out.columns` — so if a whole CSV is
   absent (e.g. you forgot `hdr.csv`), its columns never exist, `count_gaps`
   ignores them, and **every country reports `gap_count = 0` / "scoreable"** while
   the affected pillar (P3 here) goes silently NaN. Verified in the sandbox:
   WB-only input → P3 all-NaN yet gap_count 0 for all rows, and `v1_MScore`
   collapses to **all-NaN** because the Switzerland/Lebanon anchors are NaN.
   → Fix: count gaps against the canonical expected indicator set per track, not
     against whichever columns happen to exist.

2. **v1 anchoring fails silently when the anchors are NaN.** If Switzerland or
   Lebanon 2024 lack any pillar input, `v1_raw` is NaN → `spread` is NaN → the
   division yields all-NaN `v1_MScore` with no warning (the existing guards only
   catch *missing rows* and *zero spread*, not NaN). → Add an explicit non-NaN
   check on both anchor raws and fail loudly.

3. **ECI off-target years are dropped, not snapped.** `_snap_eci_years` keeps only
   rows whose year is exactly in `TIME_POINTS`; the README promises annual ECI is
   "snapped to target years." If your `eci.csv` carries annual values, the
   non-target years are silently discarded (and any country whose ECI sits on,
   say, 2023 not 2024 loses ECI). → Either pre-filter `eci.csv` to exactly the 5
   target years, or reuse the nearest-year logic in `_snap_to_target_years`.

4. **`analytical_findings` — `mi_75` computed but unused.** In the "structural
   overperformers" block, `mi_75 = yr2024["v1_MScore"].quantile(0.75)` is computed
   but the filter then uses `mi_median`. Likely intended `> mi_75`. Decide and make
   it consistent.

5. **Minor:** `from io import StringIO` is imported but unused; `COMMON_NAME_TO_ISO3`
   is defined but never referenced (country→ISO3 mapping is never actually applied,
   so CSVs really do need an `iso3` column as the README states).

## Conventions

- Python 3.11; deps pinned in `requirements.txt`.
- `./data/` (inputs) and `./output/` (artifacts) **are committed** to the repo as of
  2026-06-28. The real acquired panel and generated outputs live in version control;
  see `DATA_PROVENANCE.md` for exactly how each input was sourced. (This reverses the
  earlier "stay local" convention — the parent fragmentation study still keeps its raw
  data out of git, but `mi_pipeline/` does not.)
- Don't wire MI data into the parent fragmentation study; they are unrelated.
