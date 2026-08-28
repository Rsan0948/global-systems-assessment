# MI Data-Flow & Source-of-Truth Map

**Purpose.** One authoritative map of the mi-research engine + its mi-pipeline feed:
every script, what it reads, what it writes, where every tunable parameter lives, and
where the same information is stored more than once. Built as the blueprint for the
source-of-truth normalization refactor. Read this before touching data or config.

**Scope.** `mi-research/` (engine `mi/`, `scripts/`, `data/`) + the sibling
`mi-pipeline/data/` feed. The other three legs (fragmentation, collectivization,
mi-website consumer) are out of scope — they are import-decoupled by design.

**Status.** Descriptive as of 2026-07-11 (commit `2e1224a`). Companion to the refactor
plan; update when the reader-unification (Phase B) lands.

---

## 1. The two-reader problem (the core disease)

The intended architecture is *"one canonical runtime store: `canonical_panel.json`, read by
`mi/panel.py`."* That is **only half true.**

```
                         ┌─────────────────────────────┐
  main scoring path ───► │ mi/panel.py                 │ ──► canonical_panel.json   (RUNTIME truth #1)
  (score_country, CLIs)  └─────────────────────────────┘
                         ┌─────────────────────────────┐
  durability / relational│ mi/datasource.py            │ ──► wb_anchored.json
  / global_systems  ───► │ (live multi-source stitch)  │  +  va_anchored.json       (RUNTIME truth #2)
                         └─────────────────────────────┘  +  mi-pipeline/data/*.csv
                         ┌─────────────────────────────┐
  global_systems only ─► │ reads mi_scored_countries.csv│ (a THIRD path, into pipeline output/)
                         └─────────────────────────────┘
```

`mi/durability.py` and `mi/relational.py` call `datasource.get_indicators()` at
runtime, which reads `wb_anchored.json` + `va_anchored.json` + the pipeline CSVs live —
**not** the canonical panel. Two country→ISO resolvers exist
(`panel._resolve_iso` vs `datasource.country_to_iso`); `DISPLAY_FIX` is duplicated
between `panel.py` and `build_canonical_panel.py`. Unifying on the canonical panel is
**Phase B** (needs a corpus regression pass — see refactor plan).

---

## 2. Read → write data-flow graph

### Build / data path (canonical)
| Script | Reads | Writes |
|---|---|---|
| `refresh_wgi_wdi.py` | `wb_anchored.json` + World Bank API | `wb_anchored.json` |
| `fetch_alt_indicators.py` | World Bank API | `robustness/alt_indicators.json` |
| `build_canonical_panel.py` | `wb_anchored.json`, `wgi_full_panel.json`, `vdem_longrun.json`, `../mi-pipeline/output/mi_scored_countries.csv` (via `mi.datasource`) | **`sources/canonical_panel.json`** |
| `build_site_dataset.py` | canonical panel (via `mi.panel`), `country_context.json`, `safeguard_derivations.json` | `../mi-website/web/public/data/{countries.json, country/<slug>.json, meta.json}` |
| `build_relational.py` | `mi.relational` records + site `country/<slug>.json` | site `country/<slug>.json` (adds `relational`) |
| `build_similar.py` | site `countries.json` + per-country JSON | site `country/<slug>.json` (adds `similar`) |

### Robustness (generate → grade)
| Script | Reads | Writes |
|---|---|---|
| `prospective_freeze.py` ★ | canonical panel (via `mi.panel`), prereg (hash) | `robustness/prospective_2024_predictions.json` — **defines `predict()`** |
| `temporal_holdout.py <year>` ★ | canonical panel, `prospective_freeze.predict` | `robustness/temporal_{2004,2012}_predictions.json` |
| `data/robustness/outcomes/grade.py` ★ | `temporal_{2004,2012}_predictions.json`, `gdp_pcap_ppp_kd_raw.json`, `ucdp/UcdpPrioConflict_v24_1.csv`, `crag_long_parsed.json`, `../mi-pipeline/data/fsi.csv` | `robustness/temporal_grade_report.json` |
| `derive_claim.py` | `case_studies/completed/*.json` (via engine), prereg | `robustness/derived_claims.json` |
| `grade_claims.py` | `derived_claims.json`, `case_studies/completed/*.json` | `robustness/grade_report.json` |
| `strat_safeguards.py` | `case_studies/completed/*.json` (via `derive_claim._score_ref`) | `robustness/safeguard_stratification.json` |
| `substitute.py` | `alt_indicators.json`, canonical panel | `robustness/substitution_results.json` |

### Historical
| Script | Reads | Writes |
|---|---|---|
| `build_conflict_onsets.py` ★ | `ucdp/UcdpPrioConflict_v24_1.csv`, `cow/*.csv` | `historical/conflict_onsets.json` |
| `conflict_outcome.py` | `historical/conflict_onsets.json` | (library) |
| `epoch_panel.py` | `vdem_longrun.json`, `longrun_pillars.json` | `historical/decay_curve.json` |
| `decay_curve_conflict.py` | `vdem_longrun.json`, `longrun_pillars.json`, `conflict_outcome` | `historical/decay_curve_conflict.json` |
| `inversion_test.py` | `case_studies/ancient/ancient_cases.json` | `historical/inversion_test.json` |
| `durability_ancient.py` | `case_studies/ancient/ancient_cases.json` | `historical/durability_ancient.json` |
| `holdout_error_forensics.py` | `historical/conflict_onsets.json`, `crag_long_parsed.json`, `temporal_{2004,2012}_predictions.json` | `historical/holdout_error_forensics.json` |

★ = touches the frozen pre-registration outputs; a refactor of these must regenerate
byte-identical artifacts (verify with a diff) or it has broken a frozen result.

**Missing edge (the recurring-pain root):** `grade.py` builds a full joined per-country
panel `_rows = {iso, mi_score, P1, P4, vuln, elevated, ucdp, crag, crisis}` in memory,
then **discards it** (`grade.py:305,319` drop `_rows` before writing). The committed
`temporal_grade_report.json` keeps only ISO *lists* + a FP *count*. Every downstream
analysis (ESI Test 2A/2B, forensics) must re-run the whole grader to recover a table
that already existed. **Fix: persist `_rows` as `temporal_holdout_panel.json`.**

---

## 3. Source-of-truth register — REDUNDANT DATA

Same information, stored N times. "Authoritative" = which copy a refactor should keep.

| Information | Copies (file → field) | Authoritative | Dedup target |
|---|---|---|---|
| WGI gov (GE/RL/RQ/CC) | `wgi_full_panel.json`; `wb_anchored.wgi.*`; `wb_cached.csv`; `canonical.gov_effectiveness…` | `canonical_panel.json` | retire `wgi_full_panel` at runtime; re-point `datasource` |
| Voice & Accountability | `va_anchored.json`; `wb_anchored.wgi.VA`; `wgi_full_panel.VA`; `canonical.voice_accountability` | `canonical.voice_accountability` | retire `va_anchored.json` runtime read |
| Political stability (PV) | `wb_anchored.wgi.PV`; `wgi_full_panel.PV`; `wb_cached.PolStab`; `canonical.political_stability` | `canonical.political_stability` | — |
| **GDP per capita PPP** | `wb_anchored.wdi.gdp`; `wgi_full_panel.gdp`; `longrun_pillars.P4_gdp`; `wb_cached.GDPpcPPP`; `gdp_pcap_ppp_kd_raw.json`; `canonical.gdp_per_capita_ppp` | `canonical` (2024 scoring); `gdp_pcap_ppp_kd_raw.json` (robustness outcome) | **5 copies** — highest-value dedup |
| Resource rents | `wb_anchored.wdi.rents`; `wgi_full_panel.rents`; `wb_cached.ResRents`; `canonical.resource_rents_pct_gdp` | `canonical` | — |
| Rule of law (concept) | WGI `RL` (multiple) **vs** V-Dem `vdem_longrun.rol` | two *definitions* — keep both, label | not dedupable |
| CPI/GII/ECI/FSI | pipeline CSVs **and** live `datasource` read **and** canonical tier-B | `canonical` (A/B); FSI lives ONLY in `fsi.csv` | re-point `datasource` |
| HDI edu/life-exp | `hdr.csv`; `longrun_pillars.P3_*`; `canonical.education_index/life_expectancy_index` | `canonical` (2024) | — |
| CRAG outcome | `crag-2017.xlsx` (raw) + `crag_long_parsed.json` (derived) | xlsx source; json cache | keep both (raw+cache) |
| UCDP conflict | `ucdp-prio-acd-241-csv.zip` + extracted `.csv` | extracted CSV | drop zip (redundant archive) |

---

## 4. Config register — WHERE EVERY TUNABLE LIVES

Config is spread across **four kinds of location**. The goal is one owner per concern.

### 4a. Engine scoring parameters — `mi/constants.py` (Python, stdlib; the intended home)
- `LENS` (≈40 keys) — normalization denominators (rents 50, oda 20, fsi 120, gdp 500/150000),
  capacity cutoffs (`p1_bottom_third` 0.33, `p1_median` 0.50), spread cuts (0.50/0.35),
  Safeguard-J band (`structural_vuln_flag_floor` 0.28, `structural_vuln_clear_ceiling` 0.20,
  `structural_vulnerability_gap` 0.22 [**false-precision, back-compat only**], converge deadband 0.01),
  Mod4 margin 0.10, VA gaps (−0.50 / −0.20), etc.
- `SAFEGUARD_THRESHOLDS` — E/C/F blocks. ⚠ **unit inconsistency**: E is PERCENT (15/25/50),
  C & F are FRACTIONS (0.30/0.25). Normalize on consolidation.
- Module-level: `WEIGHTS` (P1 .34/P2 .15/P3 .16/P4 .20/P5 .16), `WEIGHTS_EQUAL`,
  `WEIGHTS_V2_EQUAL`, `V2_ERA_LEADER`, `V2_ELEVATED_WEIGHT` 0.30, `MI_ACTIVE_WEIGHTING`,
  `ASCENT_LOW_BASE` 0.40, `GLOBAL_*`, `TIERS`, `ANCHOR_*`, `BASELINE`.

### 4b. Engine INLINE magic numbers — NOT in LENS (must reference logic to extract)
| File | Literal | Meaning |
|---|---|---|
| `scoring.py` | `2015`/`2021` | era bucket cutoffs (parallel to `V2_ERA_LEADER`) |
| `scoring.py` | `/5.0` | P2 R&D-proxy denominator (R&D 0–5% GDP) |
| `scoring.py` | `<=3`, `<=10` | scale-guard soft-warn cutoffs (WGI, CPI) |
| `safeguards.py` | `<=4` | Safeguard-B successor-fragment cap |
| `diagnostics.py` | `0.03` (×3) | movement-quality deadband |
| `diagnostics.py` | `0.80`, `1.5`, `0.15` | strategy-confidence, VA scale-detect, convergence |
| `durability.py` | `±0.02`, `5` | earned/granted residual band, min reference set |
| `relational.py` | `0.33`, `0.66`, `3`, `500000` | exposure bands, conflict cap, depth anchor |
| `global_systems.py` | `0.15`/`-0.15`, `0.06`/`0.04` | inst climb/decline, texture cuts |

### 4c. Robustness / analysis parameters — currently HARDCODED IN SCRIPTS (Phase-A target)
These are **not scoring math** — they are the analysis-layer decisions. Consolidate into one config.
| Parameter | Value | Currently in |
|---|---|---|
| Mechanical rule set: J flag/clear | 0.28 / 0.20 | `prospective_freeze` (hardcoded), `derive_claim` (from LENS), `durability_ancient` (hardcoded), LENS |
| Mechanical rule set: P1 decline/improve | 0.30 / 0.50 | `prospective_freeze` **and** `derive_claim` (both hardcoded, NOT in LENS) |
| Mechanical rule set: spread high/low | 0.25 / 0.15 | `prospective_freeze`; site build uses 0.15/0.35 |
| Vulnerability score → elevated | `sum(conditions) >= 1` | `prospective_freeze.predict()` |
| Crisis definition | `UCDP onset OR CRAG default` | `grade.py`, prereg prose |
| CRAG coverage cutoff | 2015 | `grade.py`, re-hardcoded in `holdout_error_forensics.py` |
| UCDP window end | 2023 | `grade.py` |
| Decay-curve anchors/window | `[1816,1850,1880,1910,1940,1970,1990]` / 25 | `decay_curve_conflict.py` |
| Econ-rupture anchors/window/collapse | `[1800,1850,1900,1950,1980]` / 30 / 0.80 | `epoch_panel.py` |
| Safeguard tier thresholds | ≥15 / 8–14 / 4–7 / 1–3 | `strat_safeguards.py` |

### 4d. Embedded per-case DATA literals in code (should be data files)
- `score_v2_cohorts.OBS` — 27-row `(iso3, year, cohort, origin, outcome_tag)` table.
- `run_shielded_probe.PROBE` — 7 `Unit@Year` keys.
- `retag_corpus.REVIEWED_TAGS` — 12-case manual override dict.

---

## 5. Duplicated-mapping register — CODE↔ISO LOOKUPS

| Map | Duplicated in | Notes |
|---|---|---|
| **`GW_ISO`** (Gleditsch-Ward → ISO3, ~137) | `data/robustness/outcomes/grade.py:11-33` **and** `scripts/historical/build_conflict_onsets.py:35-59` | verbatim copy; historical version is a strict superset (+8). **Consolidate.** |
| CRAG name → ISO3 (~30) | `grade.py:92-103` (`name_to_iso.manual`) | hand-maintained |
| COW StateNme → ISO3 (~90) | `build_conflict_onsets.py` (`COW_NAME_MANUAL`) | hand-maintained |
| Country → support/shock prose (~29) | `holdout_error_forensics.py` (`EXTERNAL_SUPPORT`/`EXTERNAL_SHOCK`) | interpretive, name-keyed |
| `DISPLAY_FIX` (~25) | `mi/panel.py:21-30` **and** `build_canonical_panel.py` | reader/builder duplicate |

All the name→ISO dicts overlap on the same hard cases (Congo, Côte d'Ivoire, Korea,
Yemen). **Consolidate into one `iso_map` module** with `gw_to_iso()` + `name_to_iso()`.

---

## 6. Duplicated / conflicting CONSTANTS

- **ECI min/max defined 3×**: LENS `-2.5/+2.5`; `datasource` fallback `-3.53/+2.10`; data-derived at runtime. (**conflict**)
- **`0.33` for 3 unrelated gates**: `LENS.p1_bottom_third`, `E.positive_p1_ceiling`, `relational.BAND_LOW`.
- **Institutional `0.15`**: `GLOBAL_ENGINE_THRESH.institutions` vs inline in `_inst_forward_net`.
- **Safeguard-J P4−P1 gate implemented twice**: `safeguards.evaluate_safeguard_j` vs `diagnostics.structural_vulnerability`.
- **"Durability" concept twice**: `durability.py` (GDP-residual) vs Safeguard J (pillar-gap) — same idea, two engines.
- **Version strings, 3 notions**: `__init__.__version__="1.0.0-live"`, `MI_MODEL_VERSION="v3.3"`, `BASELINE["version"]`.

---

## 7. Runtime vs build-time vs output (what a refactor may/may not move)

- **RUNTIME (read during scoring):** `canonical_panel.json` (panel path); `wb_anchored.json`
  + `va_anchored.json` + pipeline CSVs (datasource path — the leak); `vdem_longrun.json` +
  `longrun_pillars.json` (global_systems); `sources/relational/*.json`.
- **BUILD-TIME ONLY:** `wgi_full_panel.json` (tier C), `country_context.json`,
  `safeguard_derivations.json`, `wb_cached.csv`.
- **COMMITTED OUTPUTS (regenerable — never hand-edit):** everything under `robustness/`
  + `robustness/historical/`, `crag_long_parsed.json`, `forecasts/*.json`,
  `case_studies/ancient/*_report.json`.
- **RAW INPUTS (external, non-regenerable):** `outcomes/cow/*.csv`, `ucdp/*.csv`,
  `crag-2017.xlsx`, `gdp_pcap_ppp_kd_raw.json`, `alt_indicators.json`.

---

## 8. Refactor targets, by risk

**Phase A — safe, additive, no scoring-math change (unblocks downstream work): ✅ LANDED.**
Every frozen artifact regenerates byte-identically; engine tests 8/8.
1. ✅ This map.
2. ✅ `config/robustness.json` + `config/__init__.py` loader — consolidates §4c
   (analysis-layer params) into one file with a `verify_consistency()` guard that asserts
   the J thresholds equal `LENS`. Consumers: prospective_freeze, derive_claim,
   durability_ancient, strat_safeguards, decay_curve_conflict, epoch_panel,
   holdout_error_forensics, grade.py.
3. ✅ `lib/iso_map.py` — consolidates §5 GW/CRAG/COW maps (`GW_ISO_BASE` /
   `GW_ISO_EXTENDED` / `CRAG_NAME_MANUAL` / `COW_NAME_MANUAL` / `name_to_iso`); grade.py +
   build_conflict_onsets import it. Verified against the originals via ast.
4. ✅ Joined holdout panel persisted — `grade.py` writes
   `data/robustness/temporal_holdout_panel.json` (89 rows/window: iso, mi_score, P1, P4,
   vuln, elevated J-gate flag, ucdp, crag, crisis). The single source ESI + forensics read.

**Phase B — engine-touching (behind the 84-case corpus regression gate):**

5. **Reader unification (§1) — EMPIRICALLY RESOLVED, deliberately NOT forced.** A
   divergence audit compared `datasource.py`'s live stitch against `canonical_panel.json`
   for every overlapping country-year-indicator: **6,685 values, ZERO divergences.** The
   two readers *agree on values* — canonical is a faithful superset. But they differ in
   **scope by design**: `datasource` serves the curated ~91-country `wb_anchored` set;
   canonical covers 191. Re-pointing `datasource` at canonical would **expand
   `durability`'s OLS reference set by ~100 country-years → change every residual → change
   the durability-gate corpus (sig01–19)**. That is a *behavior change requiring corpus
   re-validation*, not a refactor — so it is **deferred as a validated change, not done as
   cleanup**. The "two conflicting truths" worry is dissolved: there is one truth at two
   scopes. (Audit is reproducible; see the Phase B commit.)
6. **Inline magic-number extraction (§4b) — ✅ DONE (behavior-preserving).** Consolidated
   into `LENS`: `rd_full_pct` (5.0), `movement_deadband` (0.03, was inline ×3),
   `strategy_confidence_p1` (0.80), `va_scale_detect` (1.5), `convergence_range` (0.15),
   `durability_residual_band` (0.02), `durability_min_reference` (5). Verified: full 191-
   country engine snapshot **byte-identical hash**, corpus artifacts unchanged, tests 8/8.
   Still deferred (lower value / higher touch): scale-guard cutoffs (3/10), era cutoffs
   (2015/2021), Safeguard-B fragment cap (4), the double Safeguard-J impl, and the
   `SAFEGUARD_THRESHOLDS` percent-vs-fraction unit normalization.
7. Retire redundant runtime data copies (§3) — coupled to item 5; deferred with it.

**Eventual — the MCP layer:** a thin wrapper over the normalized substrate exposing
`get_panel`, `get_holdout_panel`, `get_config`. Built last, over a clean layer.
