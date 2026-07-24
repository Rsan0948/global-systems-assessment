# Reproducing the results

Everything in this repo is deterministic where it matters: fixed sample
windows, frozen null-sampler seeds, and version-locked scored artifacts.
This page is the fresh-clone path for each leg. If your numbers differ
from the stated expectations, that is a finding — open an issue with the
commit SHA and the leg you ran.

## Setup

```bash
git clone https://github.com/Rsan0948/universalsystemgrade.git
cd universalsystemgrade
python -m pip install -r requirements.txt   # Python 3.11+
```

Optional geospatial layers (atlas tiles, geography bridges) additionally
need `geopandas` and `pyogrio`.

---

## Leg A — Fragmentation census

```bash
cd fragmentation/census && python run.py
```

Expected: the run grows (or refreshes) `fragmentation/census/results/` and
prints the census table across natural, language, and social systems.
Headline expectation: rivers Rb 4.55 ± 0.24 (σ/μ ≈ 0.053, confirmed);
languages Rb 3.40, CV 0.20 (discovery, in the grown band); corporate
splits 2.16 / party splits 2.06 (below the band, curated-tier). Every
discovery claim must beat the frozen Kirchner random-tree null — see
`fragmentation/preregistration/` and `fragmentation/governance/`.

```bash
cd ../integration && python run.py
```

Expected: `integration/results/` and a short report. Current status is a
**working correlation family, not a claim**: tree-shape vs. complexity
r = 0.95 (5/5 known + 5/8 extras) and vs. function r = 0.73 (7/7 known).

## Leg B — Modernization Index

Score one country end to end:

```bash
cd mi-research
python scripts/score_country.py --country "Estonia" --year 2024
```

Expected: a per-pillar table (V1/V2/V3 on the 0–100 display scale), T4
scarring, the durability gap (P4−P1), the 3-year trajectory, the sealed
engineered-suppression flag, and an archetype call.

Backsliding danger-zone diagnostic (curated-tier finding: inverted-U in
rule-of-law capacity, safety ceiling near the 80th percentile):

```bash
python scripts/assess_backsliding.py --country "Hungary"
```

Run the test suite:

```bash
pytest -q -p no:cacheprovider tests/
```

Expected: all tests pass (`test_tiers.py`, `test_scale_guard.py`,
`test_backsliding.py`). Tests run on the canonical panel snapshots
committed under `mi-research/data/` — no network access needed.

Rebuilding the **full** upstream panel (V-Dem ~15M rows, WDI bulk, WGI
refresh) is the heavier path: see `mi-pipeline/README.md` and
`scripts/refresh_wgi_wdi.py`. You do not need it to reproduce the
published findings.

## Leg C — Collectivization

```bash
cd collectivization
python run.py
pytest -q -p no:cacheprovider tests/
```

Expected: `results/cycle_analysis.json` and `results/cycle_summary.png`
recomputed from the frozen casebook — 109 formation cycles over 30 coded
cases, Hamming-distance template matching against four frozen pathway
templates, plus cycle reports for the formation cycles. Headline curated
expectations: deep predecessor → restoration (ρ = −0.84, n=30, curated);
negotiated unions ~2× more durable than conquests (308 vs 156 yrs, n=4,
exhibition-only).

---

## What "reproduced" means here — and what it does not

Re-running the pipelines confirms **internal consistency**: same code,
same frozen inputs, same numbers. It does not by itself confirm external
validity. The honest caveats, stated where a replicator will trip over
them:

- Historical tiers (ancient n=25, supercycle n=3) are interpreter-scored
  with hindsight. Independent recoding is the single most valuable
  external contribution — see CONTRIBUTING.md.
- T1 gap thresholds (0.20/0.28) were derived on a development set; the
  17/19 success count is hindsight-calibrated, not a forecast record.
- The sealed forward flags (US/UK/Chile acute; RU/BY/KG/ML floor) have
  not yet met their trigger windows; the acute-timing signature behind
  them is calibrated on n=2 turns (disclosed in
  `mi-research/data/forecasts/sealed_flags_2024.json`).
- `mi-research/sandbox/` and root `sandbox/` are exploratory — failures
  live there permanently and are not shipped claims.

The grading discipline is in `mi-research/docs/curated/` (claims ledger)
and `mi-research/RESEARCH.md`. The commit history is itself part of the
audit trail — hypotheses were frozen, tested, and sometimes killed in
sequence; nothing was squashed away.
