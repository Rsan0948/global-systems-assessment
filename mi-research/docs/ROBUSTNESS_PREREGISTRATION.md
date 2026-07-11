# MI Robustness & Reproducibility Program — Pre-Registration

**Status:** FROZEN 2026-07-11. Binding. Every threshold, outcome definition, data
source, and success criterion below was fixed *before* any result was generated;
results commits reference this file's git hash. Changes after freeze are recorded
as dated amendments at the bottom, never silent edits.

**Framing (agreed):** this is a genuine inquiry, not a defense. "The MI is weaker
than claimed" is an acceptable, publishable output. Nulls and reproduction gaps
are reported at the same prominence as confirmations.

**Cross-cutting integrity rules (apply to every workstream):**
1. **Pre-registration as code.** Configs (thresholds, outcome defs, sources) are
   frozen in a committed file; each run emits a hash of its config into its output.
2. **Generate before grade.** Predictions / substituted scores / recomputed claims
   are produced and committed in one step *before* the step that grades them can
   see outcomes. Two commits, ordered.
3. **Lift over a dumb baseline on every headline number.** No raw accuracy is ever
   reported alone; it is always accompanied by what a trivial model (majority
   class, GDP-per-capita-only, FSI-only) already achieves. The claim is the lift.
4. **Read-only w.r.t. scoring math.** No workstream edits the normalizers, weights,
   or pillar formulas. Analysis lives in new scripts/modules. The one exception is
   Priority 1 (the claim-derivation rebuild), which is *additive* (a new module),
   spec-driven, and does not alter `scoring.py`.
5. **The 84-case modern corpus floor is preserved.** Nothing degrades an existing
   case; the engine stays deterministic.

---

## Priority 0 — Prospective freeze (start immediately; graded in ~2034)

The only genuinely uncontaminated test. Cost now ≈ zero; value grows with time.

- **Freeze:** git tag the current engine (`mi-robustness-prereg-<date>`).
- **Predictions:** for all 191 scored countries at 2024, emit mechanical
  predictions using the frozen rule set below, commit them now.
- **Grade (future):** in ~2034, against the frozen outcome definitions below.

---

## Priority 1 — Reproducibility rebuild (prerequisite for P2 & P3)

**Why:** the reported "100% directional accuracy across 109 cases" is currently
tallied from static `verification{}` codings baked into each case JSON, and the
script that derived them is no longer in the repo. The safeguards do not feed the
graded directional calls (`generate_predictions` ignores its `safeguards` arg;
`tier` derives only from `mi_score`). So the headline number is not presently
recomputable from the engine.

**Task:** build `derive_claim(engine_output) -> {directional_call, tier,
abstention, risk_level}` as a live, recomputable function.

**THE CRITICAL DISCIPLINE — spec-driven, not label-driven.** The derivation is
implemented *from the written specification* (`MASTER_REFERENCE_ARCHITECTURE.md`
§4, `RESEARCH.md`, the safeguard/Mod definitions in `mi/safeguards.py`), frozen,
and **only then** compared to the frozen `verification{}` codings. It is NOT
reverse-engineered to reproduce them — doing so would just re-fit to 100%. The
derivation is committed before the comparison is run.

**Pre-registered report (whatever it says):**
- Reproduction rate: of 109 cases, how many does the spec-driven claim reproduce
  vs the frozen coding. Report the number. If < 100%, the delta is a finding.
- Directional accuracy of the recomputed claims vs actual case outcomes, **with
  baseline lift** (vs a P1-ordinality-only and a GDP-per-capita-only predictor).
- Whether the safeguards change any recomputed claim (this is most of P3's answer).

---

## Plan 1 — Alternative-indicator substitution (unblocked; runs in parallel)

Addresses the normative-loading charge. Read-only seam: mutate the dict from
`panel.indicators_for(country, year)`, call `score_country(dict)` — zero edits to
normalizers or weights.

- **Rescaling (frozen):** every alternative series is converted to a 0–100
  **cross-country percentile rank** before injection (mirrors WGI's own
  construction; satisfies the scale guard at `scoring.py:114` and preserves pillar
  semantics). The driver owns this; the engine is untouched.
- **Substitutions (frozen), P1 (where the normative charge lives):**
  - WGI GovEff/RuleLaw/RegQual → **tax revenue % GDP** (`GC.TAX.TOTL.GD.ZS`)
  - → **govt education expenditure % GDP** (`SE.XPD.TOTL.GD.ZS`)
  - → **Logistics Performance Index** (`LP.LPI.OVRL.XQ`, snap to nearest wave)
  - **Maximum-divergence run:** all P1 WGI keys → revealed-outcome set simultaneously.
- **Secondary substitutions:** P2 GII → high-tech exports (`TX.VAL.TECH.MF.ZS`);
  P5 FSI → homicide rate (`VC.IHR.PSRC.P5`). Patents (`IP.PAT.RESD`) treated as
  optional (discontinued post-2021, raw counts).
- **PRIMARY output = the movers, not ρ.** For each substitution: which countries
  move most, and **are they the normatively-contested ones** (Gulf states,
  Singapore, China, Rwanda, Hungary, etc.). A high ρ that hides large movement in
  exactly the contested cases means the charge *lands*.
- **Income-partialling (frozen):** the real test is whether a country's
  **residual rank** (rank minus what GDP-per-capita PPP predicts) survives
  substitution — separating "measures institutions" from "measures wealth."
- **Secondary output:** Spearman ρ vs original ranking, per substitution and for
  the max-divergence run. Interpretation fixed in advance: ρ > 0.90 across all →
  source-robust *only if* the movers are not concentrated in contested cases;
  ρ < 0.85 → flagged, with the two readings (original indicator load-bearing *vs*
  substitute measures a different construct) disentangled via the movers.
- **Baseline:** GDP-per-capita-only ranking, to show the MI is not merely income.
- **Coverage (accepted):** tax 143, education 187, high-tech 176, homicide 149,
  LPI 164, GDP-pc 190 (of 191 at 2024). Report N per run; `min_pillars_for_mi=3`.

---

## Plan 3 — Safeguard stratification (after Priority 1)

Depends on the recomputable claim from P1.

- **Tier thresholds (frozen BEFORE counts):** Structural ≥15 cases · Validated
  8–14 · Provisional 4–7 · Hypothesis 1–3. A rule's "case count" = number of the
  109 cases where disabling it changes the recomputed claim (call / tier /
  abstention).
- **Mechanism:** leave-one-out via the read-only wrap-and-blank seam over
  `evaluate_all_safeguards`. Missing context that rules need to fire (e.g.
  `p1_comparison_gap` for Mod4) is derived mechanically from the case entities' P1
  and documented.
- **Interaction caveat (frozen):** leave-one-out measures *marginal* contribution
  and undercounts interacting rules; a grouped-ablation pass accompanies it, and
  no interacting rule is labeled "provisional" on the LOO count alone.
- **Reported:** strong-rules-only (Structural+Validated) directional accuracy vs
  full; marginal contribution per rule; a falsifiability schedule for every
  Hypothesis-tier rule (what promotes it, what kills it). Headline becomes e.g.
  "X% on strong rules; Y% with provisional/hypothesis rules; N rules tracked."

---

## Plan 2 — Temporal holdout (after Priority 1)

**Labeled honestly as reduced-contamination retrodiction, not clean out-of-sample.**
Vintage contamination is accepted: historical panel values are the 2025/2026 WB
revision back-filled, not original vintage (unavoidable from committed data).

- **Engine:** current engine with **forced V1 weights** (from
  `archive/v1/config_frozen.json` via `resolve_weights`). Labeled "V1-weighted,
  current-engine" — not strict V1 (contamination already caps purity; not worth a
  `git checkout mi-v1` worktree or WGI vintage archaeology).
- **Panel:** the 90 countries with a 2004 record (all 90 also have 1996). P1, P4,
  P3, P5 fully real; P2 (innovation) thin (ECI-only) → design centers on P1,
  P4−P1 gap, and pillar spread; MI composite treated as WGI+GDP-driven historically.
- **Predictions:** mechanical, from 2004 scores, using the frozen rule set below.
- **Outcomes (frozen sources, picked before any alignment):**
  - GDP-per-capita PPP change 2004→2024 (World Bank, pipeline's own source)
  - Armed-conflict onset 2004–2024 (**UCDP/PRIO ACD**, static CSV-zip; ≥25
    battle-deaths new-conflict threshold)
  - Sovereign default 2004–2024 (**Bank of Canada CRAG** database)
  - Institutional change (WGI) reported as **secondary and flagged circular**
    (P1 is built from WGI), never as a headline.
- **Baselines (lift required):** majority-class base rate; GDP-per-capita-2004-only;
  FSI-2004-only (for crisis). MI structural vulnerability must beat these.
- **Reporting:** full confusion matrix (sensitivity, specificity, PPV, NPV), base
  rate, AUC-ROC, run on ALL 90 countries with no exclusions.
- **Design B (rolling windows)** only if Design A validates; its windows overlap
  heavily and are reported as consistency, not independent confirmations.

---

## Shared mechanical rule set (used by P0 prospective and P2 temporal)

Applied identically to any score-set at time T. No case-by-case judgment.

- **Durability/trajectory:** reuse Safeguard J's gap (P4 − P1) and its existing
  thresholds (flag_floor 0.28 / clear_ceiling 0.20). J-flagged (economy outruns
  institutions) → predict stress/underperformance; J-clear → predict sustain/improve.
- **Volatility:** pillar spread > 0.25 → high volatility; spread < 0.15 → stable.
- **Level:** P1 < 0.30 → predict stagnation/decline; P1 > 0.50 → capacity to improve.
- **Configuration:** balanced (spread < 0.15) → predict durability.

Outcome operationalizations, fixed before grading:
- **Relative growth:** GDP-pc-PPP change over the window, above/below the
  cross-country median = improve/decline.
- **Crisis (binary headline):** UCDP onset OR CRAG default event within the window.
  Conflict-onset and sovereign-default are ALSO reported as separate outcomes
  (never only the OR'd form), so no signal is lost to the disjunction.
