# Source reports — raw research inputs (provenance for the corpus)

The original case-study research, produced by external/framework-aware or framework-naive agents and
delivered as documents. Copied here so they're findable + version-controlled. **These are RAW INPUTS** —
the scored, structured records live in `../completed/` (51 ordinality + 19 durability-gate + 14
rule-validation) and `../ancient/ancient_cases.json` (25, firewalled). Original filenames were
`compass_artifact_wf-<id>_text_markdown.md`.

## Validation sets (what the current work runs ON)
- **`VALIDATION_v2_shock_cohort_modern.md`** — the v2 shock-cohort out-of-sample set ("Polity-Shock
  Observations via Shock-Cohort Sampling"). **The proper test.** Verify it follows
  `../../docs/random_validation_brief_v2.md` (cohorts, survivors included, origin tags, RNG), then score
  **both ways** (engine-only and engine+T3), within-cohort + pooled, split by origin. Score before reading outcomes.
- **`VALIDATION_v1_30_random_modern.md`** — the first blind random 30 ("30 Randomly-Selected Polity-Shock
  Case Studies"). Engine-only result already in `../../docs/validation_run_modern_30.md` (directional but
  weak; sample over-sampled the exogenous blind spot). This is the set to **re-run WITH T3** as a
  *consistency check* (does T3 flag the engine-alone misses — Spain/Cyprus/Greece — as high exposure?).
- **`VALIDATION_v1_10_random_ancient.md`** — first blind ancient 10. Result in
  `../../docs/validation_run_ancient_10.md` (near-zero outcome variance; can't validate).

## Source reports behind the existing corpus (provenance, already scored)
- `orig_five_case_*.md` (6 files) + `baseline20_run{1..6}of6_*.md` (6) + `expansion_30_new_cases_to_50baseline.md`
  → the **51-case P1-ordinality baseline** (`../completed/case01-51`).
- `signature_19_acute_preturn_N21.md` → the **19 durability-gate / Safeguard-J** cases (`sig01-19`).
- `ruleval_15_convergence_accountability.md` → the **14 rule-validation A/B** cases (`rv01-14`).
- `ancient_original_5_premodern.md` + `ancient_25_premodern_sourcing.md` → the **ancient tier**
  (`../ancient/ancient_cases.json`, firewalled, lowest-confidence).

## Note
All are MI-project reports. The validation sets were selected by **framework-naive** agents (the
airtight part); the earlier corpus reports were not blind and are hindsight-calibrated — see
`../../docs/validation_run_modern_30.md` and `PROJECT_SYNTHESIS.md` on why the retrodiction is a
consistency baseline, not out-of-sample validation.
