# HANDOFF — Modernization Index (MI) project: state, method, next steps

**Updated: 2026-06-28.** Single landing page for an agent picking this up. Read this, then
`PROJECT_SYNTHESIS.md` (what it all means), then the doc(s) for whatever you're doing.

## 0. Environment / mechanics
- **Working dir:** `/Users/rubensanchez/Developer/usg-mi-research-wt/mi-research` (isolated worktree).
- **Branch:** `mi-research-batch1-rwanda-expansion` (PR #8 open). **NEVER commit to main.** Commit msgs
  end with `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.
- **Python:** `/Users/rubensanchez/Developer/HelicOps_Live/.venv/bin/python` (stdlib only for scoring).
- **Validate the corpus:** `python scripts/run_retrodiction.py --validate data/case_studies/completed/`
- **Score a country:** `python scripts/score_country.py --country "Estonia" --year 2024` (→ MI 0.775).
- **System gauge:** `python scripts/global_systems.py [--year Y]`. **Breadth:** `python scripts/big_signals_scan.py --set g20 [--movement]`.

## 1. What the project IS (one paragraph)
A **structural diagnostic of how governed systems withstand stress** — *who is durable/fragile and why* —
**not a forecaster** (it does not predict timing, fortune/golden ages, or exogenous-shock ruptures). Its
distinguishing property is being a **coherent, high-dimensional, self-contextualizing space** (breadth +
relationships + multiple gravity centers + preserved contradiction + a spine), populated **deterministically
from citable external data** (WGI/V-Dem/Maddison), not AI judgment. Spine epistemic: **trust the level,
distrust the slope.** Full framing: `PROJECT_SYNTHESIS.md`.

## 2. Engine state — MI v3.3
`mi/` : `constants.py` (LENS dict + GLOBAL_* + ASCENT_LOW_BASE; `MI_MODEL_VERSION="v3.3"`), `scoring.py`,
`safeguards.py` (A–J + Mod4/Mod8), `diagnostics.py`, `datasource.py` (the Data API), `durability.py`,
`global_systems.py`.
- Pillars P1–P5 (equal-weighted MI). Safeguards A–G, **I** (porosity-backstop), **J** (durability gate,
  P4−P1, three-state flag/clear/borderline + V3.2 convergence qualifier), Mod4 (margin/consolidated-pair),
  Mod8 (violence/agency). Diagnostics: `structural_vulnerability`, `accountability_gap` (HYPOTHESIS),
  `ascent_potential` (low base, era-conditional), `movement_quality` (typology + distrust-slope caveat).
- **Two measurement tiers:** country-level (the MI) + **system-level** (Global Systems Measurement:
  engines / container [trailing + FORWARD] / texture / movement distribution).

## 3. Data sources (`data/sources/`)
- `wb_anchored.json` — WGI(2025-anchored) + WDI for the ~91 case/G-set/validation countries (refresh:
  `scripts/refresh_wgi_wdi.py`). `va_anchored.json` — Voice&Accountability, 180. `wgi_full_panel.json`
  — 202 economies (WGI GE/RL/RQ/CC/VA/PV + gdp + rents). `vdem_longrun.json` — V-Dem rule-of-law +
  liberal-democracy, 1789–2025 (rol vs WGI P1 **r=0.87**). `longrun_pillars.json` — Maddison GDP (1820+),
  life-expectancy (1543+), schooling, literacy. Sibling panel: `../mi_pipeline/output/mi_scored_countries.csv`
  (5-pillar, ~180 countries; **consume DATA only — do not wire the two projects' code together**).

## 4. Corpus state (`data/case_studies/`)
`completed/` = **84 cases, 3 classes** (validate scores them separately):
- **51 P1-ordinality** (`case01`–`case51`): the retrodiction baseline → **213C / 77P / 0F**.
- **19 durability-gate / Safeguard-J** (`sig01`–`sig19`): 17/19 correct.
- **14 rule-validation A/B** (`rv01`–`rv14`): 8 confirmed / 2 indeterminate / 2 falsified.
`ancient/ancient_cases.json` = **25 ancient cases** (+ 5 originals referenced) — **FIREWALLED**:
lowest-confidence, interpreter-scored, hindsight; **never** merged into the 213C/0F baseline.

## 5. Findings disposition (honest tiers)
- **BEDROCK** (survived a pre-registered holdout + cross-era consistency to 2686 BCE): the **durability
  gap** (income outrunning institutions → fragile) and the **container** (institutions absorb vs rupture;
  P1-ordinality *within scope*). Suppression typology + porosity-vs-suppression also strong cross-era.
- **EPISTEMIC:** trust the LEVEL, distrust the SLOPE (crises + golden ages + ancients all converge).
- **DIED / RETRACTED** (chased, tested, killed — this is the credibility): golden-age *signature*
  (refuted on geographic holdout, z=−0.0), modernization sequence (autocorrelation artifact), commodity
  driver of golden ages (retracted — resource-rich were immune), 1900-1910≈now parallel (dissolved;
  stasis vs churn), micro n-expansion (floor/ceiling-confounded), modifier delta (≈ durability gap
  re-expressed). Docs: `golden_age_*`, `globalization_supercycle_shape.md`, `modifier_delta_exploration.md`.
- **GLOBAL PICTURE (proxy, exploratory):** governance globally flat-to-eroding, masked by the P3
  human-capital ratchet ("hollow stability"); golden-age drought; mid-deceleration on a non-strengthening
  container. `v3_3_inclusion_and_global_picture.md`, `longrun_golden_age_cycles.md`.

## 6. Validation status — READ THIS
- **The retrodiction (213C/0F) is OVERSTATED if read as validation.** It is hindsight-calibrated
  (outcomes known at scoring; LENS thresholds tuned to fit). Determinism = reproducibility, NOT freedom
  from overfitting. Report as a **range (~62–85%), never a single number, never a forecast.**
- **First genuine out-of-sample runs done:** 30 blind modern (`validation_run_modern_30.md`) + 10 blind
  ancient (`validation_run_ancient_10.md`). Result: **directional but weak, sample landed in the blind
  spot.** Random coup/conflict catalogs over-sample (a) exogenous shocks (the framework's blind spot) and
  (b) memorable collapses (near-zero outcome variance). Not a validation, not a refutation.
- **The fix is frozen:** `random_validation_brief_v2.md` — **shock-cohort sampling** (pick the shock,
  take the whole cohort incl. survivors; stratify by internal/external origin; prefer post-1995 cohorts
  for full-pillar data). This is the test that could move "consistency" → "validation."
- The pre-registered out-of-sample protocol BRIEFS (sent to framework-naive agents) are frozen:
  `random_validation_brief.md` (v1), `random_validation_brief_v2.md`, `ancient_validation_brief.md`.

## 7. NEXT STEPS (in order)
1. **Build the RELATIONAL / EXPOSURE tier (the "war/conflict indicator layer").** The framework is blind
   to *exogenous conflict* only because it's an internal instrument — the signal exists in a relational
   layer we never built (this is a SCOPE choice, not impossibility). Decompose: (a) shock OCCURRENCE —
   alliance/patron protection [COW alliances], relative military power [COW CINC], bad-neighborhood/
   conflict-diffusion, contested borders/irredentism [ICOW], strategic geography/resources, great-power
   fault-line; (b) shock RESPONSE — cohesion (P5), mobilization (P1), patron intervention, strategic
   depth. **Existing toeholds:** Safeguard A (external admin), Safeguard I (backstop patron), the
   confederacy-fragility finding. **The field exists:** ViEWS, ACLED, PITF (~80% @2y), COW CINC. Goal:
   turn "exogenous defeats us" into "conditioned on exposure" so Cyprus/Poland-Lithuania become HITS not
   misses. Irreducible kernel: the specific actor's decision to start a specific war (timing) — distrust
   the slope. → spec it as a **third tier**; build deterministic indicators from citable sources.
2. **Run the v2 (shock-cohort) modern cases** when they arrive: deterministic pre-shock pull + the
   pre-registered rule (lower institutions / bigger durability gap → more severe outcome), compare
   **within cohort** (the clean within-shock natural experiment) AND pooled, **split by origin tag**.
   Log predictions before reading outcomes. Optionally write/run an **ancient v2** (shock-cohorts —
   Mongol invasions, Black Death, Bronze-Age collapse — survivor-inclusive).
3. **Score any new case studies given**, using the same blind/deterministic protocols + the firewall.
4. **Re-examine the ENTIRE corpus through the relational lens:** re-tag every existing case by shock
   origin (endogenous/exogenous) and exposure; re-test whether *conditioning on exposure* resolves the
   known misses (Spain 1936, Cyprus 1974, Greece 1922; the ancient exogenous-conquest collapses). This
   could shrink the blind spot retroactively and is the most promising path to strengthening validation.

## 8. Standing integrity rules (do not break)
- **Never commit to main.** Additive only; **no change may degrade the 213C/77P/0F baseline** (Golden
  Rule — re-run validate and prove it). Deterministic + reproducible.
- **Firewall the ancient tier** (and all proxy/exploratory work) from the validated baseline.
- **Score from citable external data, not AI judgment** (ancient tier is the flagged exception).
- **Honest reporting:** retrodiction as a range, never a forecast; report confirmations AND falsifications;
  retract overclaims in place (leave the trail). Out-of-sample = blind selection + mechanical predictor +
  pre-registered rule; score pre-shock before revealing outcome.
- **Sealed forecasts pending:** US/UK durability flags (`live/forecasts/SEALED_FLAGS_2024.md`, score-out
  ~2030 — do NOT re-tune).
