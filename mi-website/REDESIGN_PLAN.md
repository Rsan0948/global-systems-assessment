# MI Website — Redesign Plan (v0.3 sprint)

**Date:** 2026-07-05 · **Status:** implemented, retained as a design record
**Supersedes nothing in `DESIGN_SPEC.md`** — this is the execution plan that closes the gap
between the current live site (a June 30 / July 1 snapshot) and the research the engine
actually produces today.

## The problem, in one paragraph

The site is a static consumer of a precomputed JSON dataset built by
`mi-research/scripts/build_site_dataset.py`. That build surfaces a thin slice of the engine:
MI, five pillars, tier, three chips (tier / durability / shape), indicators, "similar"
countries, and a relational read for ~12 case-study countries. Meanwhile the engine and the
research program produce **far more** — the full safeguard suite, strategy classification,
vulnerability grading, movement quality, weighting sensitivity, a 109-case validation corpus,
global-systems measurement, golden-age structure, and a brand-new fragmentation-collectivization
/ institutional-ceiling study. None of that reaches a visitor. On top of that the site is
**not touch-usable** (the hero world map is hover-only) and its one "interactive" feature
(`ScoreProfile`, "watch the engine grade this country") is a timed animation of precomputed
numbers — it computes nothing.

The unifying diagnosis (owner's framing): **the case-study engine was built to be applied to
modern states, but the site keeps case studies and modern states artificially separate.** The
safeguard ⇄ case linkage already exists in the data on both sides (each safeguard carries its
derivation case in code; each case records which safeguards fired and why) — nobody joined it.

## Hard constraints (do not break)

- **No scoring math in JS.** The Python engine in `mi-research/mi/` is the single source of
  truth. The site regenerates the dataset; it never re-implements scoring. The one honest
  exception is the *what-if sandbox*, which recomputes only the parts that are already public
  and trivial: MI = mean(pillars) and the tier thresholds (both already in `lib/config.ts`).
  It never claims to recompute pillars from raw indicators (the normalization isn't shipped).
- **Determinism.** Same inputs → same dataset. Sorted iteration, stable tiebreaks.
- **Honesty as a feature.** A safeguard we can't evaluate reads **"not assessed,"** never a
  false "clear." Missing data is shown, never faked. Confidence tiers stay visible.
- **The collectivization study is its own top-level project** (`collectivization/`),
  one of the platform's three empirical legs alongside the MI and the fragmentation
  research. It shares the complexity–capacity principle with the MI but no code. It
  appears on the site as its own *findings* content, never wired into country scoring.

---

## SPRINT 1 — this pass: surface the whole engine, make it interactive, make it mobile

### 1A. Data layer (Python — the spine everything reads)
Extend `build_site_dataset.py` (and add two curated inputs) so each country file carries:
- `safeguards`: **all 11** (A–J + Mod4/Mod8) via `evaluate_all_safeguards`, each with
  `status` ∈ {firing, clear, not_assessed}, the explanation, the modification, and the
  `derivation` (origin case). `not_assessed` when the safeguard needs a context input we lack.
- `strategy`: `classify_strategy` (porosity / suppression+tier / complexity-control / ambiguous).
- `vulnerability`: `assess_vulnerability` — risk level (low→critical), flags, critical
  combinations (e.g. low-P1 + rents = Libya/South-Sudan profile).
- `sensitivity`: the four-weighting block already computed by `score_country` and currently
  dropped (v2_equal / v2_timevarying / v1 / archived_hand_v0).
- `movement`: `movement_quality` vs a prior-year score (2014 → 2024) — computable for ~85
  countries; `null` (→ "not assessed") for the rest.
- `accountability_gap`, and the graded `durability_gate` (flagged/borderline/clear), replacing
  the current binary earned/granted chip's role while keeping the chip.
- **New curated input `country_context.json`** (option B): per-iso3 context flags
  (is_democratic, has_federalism/devolution/power_sharing, is_island, population,
  immigration_policy, under_external_admin(+details), neighbor_threat_level(+details),
  is_democratic_transition, growth_trajectory, resource_rents_pct_revenue,
  fragmentation_mechanism, prior_porosity_period, external_backstop, n_successor_states,
  is_authoritarian, military_dominant). Seeded for the ~40–50 highest-interest states
  (Ukraine, Taiwan, Armenia, Tunisia, Bosnia, Myanmar, Ethiopia, the Gulf, Switzerland,
  Belgium, Singapore, …), grounded in the case corpus + well-established facts. Conservative:
  unknown → omitted → "not assessed."
- **New static `derivations.json`**: safeguard/strategy → origin case(s) + the "why" (joined
  from the code `derivation` strings and the case JSONs' `key_test` / `analysis`). This is the
  case-study ⇄ modern-state bridge, made literal.

### 1B. Country profile overhaul (the heart)
- **Safeguard Board** replaces the 3-chip fingerprint as the centerpiece: all 11 safeguards as
  tiles in three visual states (firing / clear / not-assessed). Every tile drills to: what it
  means · the deterministic rule · **the case study that produced it and why** · how many
  countries share it.
- **Diagnostics panel**: strategy (with failure mode + examples), vulnerability risk badge +
  critical-combination callouts, movement quality ("real ascent vs hollow"), and the durability
  gate graded.
- **Sensitivity strip**: "the score under four weighting schemes" — robustness, in-line.

### 1C. Genuine interactivity — the What-If sandbox
Replace `ScoreProfile` with `WhatIf`: sliders on the five pillars **and** on pillar weights
that live-recompute MI, tier, and the radar. Honest ("you're re-weighting the published
pillars, not re-deriving them"), with a reset-to-actual and a shareable state. This is the
honest version of what ScoreProfile pretended to be.

### 1D. Mobile
- `WorldMap`: a touch model — tap selects + shows a pinned readout card (not hover), tap-again
  or a CTA opens the country; larger hit areas; fix the "Hover a country…" copy.
- `AtlasTable`: responsive — the 8-column table collapses to stacked cards under `sm`.
- `Radar`: fluid (viewBox-scaled, label padding) instead of a fixed raster.

### 1E. Program-level pages (the heavyweight additions get a presence)
- **`/research`** hub: distilled static pages for **Global Systems** ("state of the world"),
  **Golden Ages** (level+era, and the honest slope-signature holdout failure), the
  **Collectivization / institutional-ceiling** study (pathway durability, ρ=−0.84, warning
  signals), and the **substrate thesis** (PROJECT_SYNTHESIS capstone).
- **`/validation`**: the 109-case corpus (84 modern + 25 ancient) scorecard + the blind
  out-of-sample runs — the receipts and the candid limits.

---

## SPRINT 2 — next pass (owner-scheduled): the Case-Study Explorer

A dedicated section where **every** case is browsable and explorable — all 84 modern, all 25
ancient, and all 30 collectivization polities — each with its full record (pre-event state,
predictions, verification, which safeguards fired and why, confidence tier). This is the
natural completion of the case-study ⇄ modern-state bridge and the destination the profile
Safeguard Board tiles and the /validation and /research pages all link into. Explicitly
deferred to its own sprint.

## Backlog / later
- Expand `country_context.json` toward full coverage (turns more safeguards from "not assessed"
  to a verdict, per country).
- Relational (T3) coverage beyond the ~12 hand-built records.
- Signals feed (structural-change over time) — needs accrued history.
- Wire the scheduled pipeline (`refresh_and_build.py` + the GH Action) to auto-refresh.

## Verification for Sprint 1
1. `python mi-research/scripts/build_site_dataset.py` regenerates the dataset deterministically.
2. `cd mi-website/web && npm run build` builds all static pages clean.
3. Spot-check: a firing safeguard on a real state (e.g. Ukraine → predatory neighbor) links to
   its derivation case; the what-if sandbox moves MI/tier/radar; the map is tappable on a
   narrow viewport; `/research` and `/validation` render.
