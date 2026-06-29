# SYSTEM STATE — the whole MI system, consolidated

**Date:** 2026-06-28. One-page map of everything that exists: measurement tiers, every case/observation
count, the epistemic status of each, the engine modules, and the honest disposition. Read with
`HANDOFF.md` (mechanics + next steps) and `PROJECT_SYNTHESIS.md` (what it means).

## 1. Three measurement tiers
1. **Country MI** (`mi/scoring.py` + `safeguards.py` + `diagnostics.py`): P1–P5, Safeguards A–J,
   Mod4/Mod8. The internal structural instrument.
2. **System** (`mi/global_systems.py` + `durability.py`): world-system gauge + the durability ratio
   (MI residual vs log-GDP). Exploratory/proxy.
3. **Relational / exposure (T3)** (`mi/relational.py`, NEW this session): the external-conflict layer
   the internal instrument was blind to. Exposure (structural vs net) × Response, firewalled, never
   changes an MI score. Spec: `relational_tier_spec.md`.

## 2. Case / observation inventory (counted, not estimated)

### A. Internal corpus — 84 scored case studies (`data/case_studies/completed/`)
Hindsight-calibrated retrodiction: outcomes known at scoring, LENS tuned to fit. **Reproducible, NOT
out-of-sample.** Report as a range (~62–85%), never a forecast.
| class | n | result |
|-------|--:|--------|
| P1-ordinality (case01–51) — **the baseline** | 51 | **213 C / 77 P / 0 F** |
| durability-gate / Safeguard-J (sig01–19) | 19 | 17/19 correct |
| rule-validation A/B (rv01–14) | 14 | 8 C / 2 indet / 2 F |

### B. Ancient tier — 25 cases (`data/case_studies/ancient/`)
**Firewalled.** Interpreter-scored, hindsight, lowest confidence. Never merged into the baseline;
informs hypotheses only.

### C. Out-of-sample — 67 observations (the GENUINE tests; blind selection)
| run | n | result | doc |
|-----|--:|--------|-----|
| v1 random modern | 30 (24/25 scoreable) | directional, weak (d≈0.37); landed in the blind spot | `validation_run_modern_30.md` |
| v1 random ancient | 10 | directional, weak (zero outcome variance) | `validation_run_ancient_10.md` |
| v2 shock-cohort | 27 | **within-cohort 4/5 concordant (~+0.77); pooled null (+0.09)** — internal engine validated within-cohort; entrenched autocracies absorb economic shocks | `validation_run_v2_cohorts.md` |

### D. Relational tier T3 — 12 records (this session; all firewalled)
| group | n | members | status |
|-------|--:|---------|--------|
| Phase-2 proof (citable) | 2 | Cyprus 1974, South Korea | consistency — the structural-exposure mirror |
| historical-proxy | 1 | Poland-Lithuania 1772 | Maddison + V-Dem proxy, flagged |
| Phase-3 misses | 4 | Greece 1919, Spain 1936, Portugal 1926, Venezuela 1948 | T3 discriminates: resolves exogenous, silent on internal |
| 4th-cell probe | 5 | Kuwait, Bosnia, Taiwan, Estonia, Afghanistan | non-random discrimination probe — shield flips outcome |

**Totals:** ~188 scored polity-shock observations (84 + 25 + 67 + 12). ~5 T3 records re-examine v1
polities through the new lens (not net-new), so **~183 distinct**.

## 3. Epistemic ladder (what each tier can claim)
- **Out-of-sample (67) — the only genuine tests.** Verdict: the internal institutions→outcome claim
  is *directionally positive*, strongest within v2 cohorts; not yet a powered validation. One
  pre-registered forward test (golden-age signature) FAILED; the sealed US/UK flags are pending.
- **Internal corpus (84) — strong cross-era CONSISTENCY, not validation.** Determinism = reproducibility,
  not freedom from overfitting.
- **Ancient (25) + T3 (12) — firewalled.** Consistency checks / discrimination probes. T3 behaves
  coherently across all four quadrants of the (durability × exposure) 2×2, but every T3 result is a
  consistency/probe claim — never validation (selection is purposive or the layer was built around the
  cases). The pending real T3 test is a **blind military-shock cohort** with the relational pull wired
  into scoring.

## 4. T3 arc this session (commits ce8fcdc → 4a0af87)
spec → Phase-2 proof (Cyprus/SK mirror; structural vs net exposure) → Phase-3 corpus re-tag (corpus is
~92% endogenous; blind spot selected out) + miss-discrimination → v2 out-of-sample scoring (internal
engine validated within-cohort; T3 *untested* — no military shock drawn) → 4th-cell shielded-survivor
probe (T3 discriminates; deterrence-patron decoupled from response-patron). All additive; baseline
213/77/0 byte-for-byte unchanged at every step.

## 5. Engine modules & scripts
`mi/`: `constants.py` `scoring.py` `safeguards.py` `diagnostics.py` `datasource.py` `durability.py`
`global_systems.py` **`relational.py`** (T3).
`scripts/`: `score_country.py` `run_retrodiction.py` `global_systems.py` `big_signals_scan.py`
`compare_countries.py` `find_similar.py` `refresh_wgi_wdi.py` · **`relational_tier.py`**
**`retag_corpus.py`** **`score_v2_cohorts.py`** **`run_shielded_probe.py`** (this session).
Data sources: `data/sources/` (WGI/V-Dem/Maddison panels) + **`data/sources/relational/`** (4 T3 files).
Provenance of every research input: `data/case_studies/source_reports/INDEX.md` (21 reports).

## 6. Standing integrity (unchanged)
Never commit to main · additive only, never degrade 213/77/0 (re-run `--validate`) · firewall ancient
+ all proxy/probe work · score from citable data, not AI judgment · report retrodiction as a range,
never a forecast · out-of-sample = blind selection + mechanical predictor + pre-registered rule.

## 7. What's genuinely pending
1. **Blind military-shock cohort** for T3 (the one design that tests it out-of-sample; v2 drew none).
2. **Full-engine pass on v2** (durability gap P4−P1 + 5-pillar where WGI covers) — tests the *second*
   load-bearing claim; only the institutions claim was scored on v2.
3. Sealed US/UK durability flags (`live/forecasts/`, score-out ~2030 — do not re-tune).
