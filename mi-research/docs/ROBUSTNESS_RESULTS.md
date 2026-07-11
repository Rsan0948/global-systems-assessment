# MI Robustness & Reproducibility — Results

**Living record.** Companion to the frozen pre-registration
(`ROBUSTNESS_PREREGISTRATION.md`, sha256 `fbd99104`). Records what each workstream
found. Raw artifacts live in `mi-research/scripts/robustness/` (code) and
`mi-research/data/robustness/` (outputs). Started 2026-07-11.

> **Framing:** genuine inquiry, not defense. "The MI is weaker than claimed" is an
> acceptable, reported outcome. Every headline number is reported with its cost
> and its baseline.

## Status

| Workstream | Status | Commit |
|---|---|---|
| P0 prospective freeze | ✅ done (graded ~2034) | `14af889`, tag `mi-prospective-2024` |
| Plan 1 indicator substitution | ✅ done | `843e6e8` |
| P1 reproducibility rebuild | ✅ done (generate `44de5c1`, grade `f5e6f8f`) | |
| Ordinality independent accuracy | ⏳ open (needs `post_event` re-scoring) | |
| P3 safeguard stratification | ⏳ open (unblocked by P1 derivation) | |
| P2 temporal holdout | ⏳ open | |

---

## Finding 1 — The construct is largely source-robust (Plan 1)

Replacing the perception-based P1 indicators (WGI) with revealed-outcome ones
(tax %GDP, education spend, logistics performance, high-tech exports, homicide),
percentile-rescaled and re-scored across ~190 countries (read-only seam, zero
scoring-math edits):

- Every substitution holds rank correlation **ρ > 0.93**; logistics performance
  and the balanced max-divergence composite hold **ρ ≈ 0.98** with income-residual
  ρ ≈ 0.93, and the normatively-contested cases (Singapore, Gulf, China) barely move.
- The MI survives substitution **better than a GDP-per-capita-only ranking
  (ρ = 0.87)** — it is not merely wealth.
- The normative-loading charge lands **only** under a single fiscal-size proxy
  (tax revenue), which also sinks Switzerland/Germany/USA by ~25 ranks — i.e.
  construct drift, not a WGI perception artifact.
- Weakest substitutes (flagged): GII→high-tech (residual ρ 0.73), education-spend
  (0.78).

**Verdict:** the "it's Western-liberal ideology / it's just wealth" charges do
**not** generally land. Artifacts: `data/robustness/substitution_results.json`.

---

## Finding 2 — The "100% directional accuracy" is heterogeneous (P1)

The reported "100% across 109 cases" is tallied from static `verification{}`
codings; the script that derived them is gone from the repo. A spec-driven
rebuild (`scripts/robustness/derive_claim.py`, built without reading the codings,
frozen before grading) shows the headline is **not a single recomputable number.**

**The 51 P1-ordinality cases (the backbone) by how the coding was actually made:**

| basis | count | recomputable? |
|---|---|---|
| clean mechanical auto-derivation (definite ordering) | ~10 | yes |
| mechanical **abstention** (Mod4 "too close to call") — counted as confirmed | 7 | it's a non-call |
| human judgment preserved (auto-derivation skipped) | 9 | no |
| free-text narrative confirmation | 25 | no |

So the mechanically-recomputable core of the ordinality claim is **~20%**, not 100%.

**The safeguards are advisory** — they do not feed the graded output.
`generate_predictions()` ignores its `safeguards` argument; `tier` derives only
from `mi_score`; disabling any rule moves 0/85 corpus entities.

Artifacts: `data/robustness/derived_claims.json`, `grade_report.json`.

---

## Finding 3 — The durability gate is the genuine jewel (P1)

Safeguard J (flags when economic structure outruns institutional quality, the
P4−P1 gap), 19 cases, cleanly recomputable:

- Reproduces the original call **18/19**.
- Recomputed against actual crises: **88.9% accuracy vs a 63.2% base rate =
  +25.7 points lift**, with **zero false positives** (when J flags, a crisis
  followed) and 2 false negatives.

This is a real, defensible, base-rate-beating predictive signal — the strongest
survivor of the audit.

---

## Finding 4 — The rule-validation family does not beat base rate (P1)

The 14 rule-validation cases: recomputed accuracy **60% vs a 66.7% majority
baseline (−6.7 points)**. Honestly reported weakness.

---

## Bottom line so far

The MI is **weaker than its "100%" headline but stronger than its critics' worst
case.** The headline is mostly abstentions and human judgment, not a clean
automated result; but the construct is not ideologically loaded or merely wealth,
and the durability gate is a genuine, recomputable, base-rate-beating signal. The
defensible position is narrower and more credible than "100% accurate."

## Open work

1. **Ordinality independent accuracy** — score `post_event`, compare pre-P1
   ordering to actual post-outcome ordering (the one clean accuracy number the
   ordinality claim still owes).
2. **P3 safeguard stratification** — now unblocked; expected to confirm most
   safeguards move few graded calls.
3. **P2 temporal holdout** — reduced-contamination retrodiction, 2004→2024.
