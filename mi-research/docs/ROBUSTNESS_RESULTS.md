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
| P3 safeguard stratification | ✅ done | `31cc093` |
| P2 temporal holdout | ✅ done (partial null) | (this commit) |

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

## Finding 5 — Safeguard stratification: only the durability gate is load-bearing (P3)

Every rule tagged by how many of the 82 derivable modern cases it fires on
(`data/robustness/safeguard_stratification.json`), tiered by the frozen thresholds:

- **Structural (15+):** G suppression (43), **J durability (42)**, D neighbor-shock (15); Mod8 (82, always-on — degenerate standing constraint).
- **Validated (8–14):** C reversal-risk (13).
- **Provisional (4–7):** E rentier (6), F turbulence (5), A external-admin (4).
- **Hypothesis (1–3):** B capacity-gate (3), I porosity-backstop (1).
- **Inert (0):** Mod4 margin-abstain (never fires in this corpus).

**Load-bearing truth:** only **J** changes a graded call; every other rule is
advisory (`generate_predictions` ignores its `safeguards` arg; tier from
`mi_score` only). So "strong-rules-only accuracy" == "full accuracy" — pulling the
thin qualifiers (B, I, Mod4) out of the headline changes nothing, because they
were never contributing to it. The one load-bearing rule (J) is both Structural
and the +25.7-pt crisis signal. The epicycle charge dissolves: the thin rules
aren't propping up the number, and the rule the framework leans on is the
best-supported one. Weak qualifiers carry promotion/demotion criteria for
real-time upgrade as the corpus grows (the self-correcting ledger).

## Finding 4 — The rule-validation family does not beat base rate (P1)

The 14 rule-validation cases: recomputed accuracy **60% vs a 66.7% majority
baseline (−6.7 points)**. Honestly reported weakness.

---

## Finding 6 — Temporal holdout: a partial null; the structural signal doesn't beat trivial baselines (P2)

Scored every country with only 2004 / 2012 data, applied the frozen mechanical
rule set, graded ->2024 against real outcomes (World Bank GDP-pc growth; UCDP
conflict onset through 2023; BoC-CRAG sovereign default through 2015). Reduced-
contamination retrodiction, not clean out-of-sample. Verified from the persisted
report (`data/robustness/temporal_grade_report.json`):

| crisis discrimination (AUC) | 2004→2024 (N=89) | 2012→2024 (N=90) |
|---|---|---|
| **MI vulnerability score (0–3)** | 0.732 | 0.689 |
| GDP-per-capita-only (poorer⇒crisis) | **0.806** | **0.748** |
| FSI-only (more fragile⇒crisis) | n/a (FSI starts 2012) | **0.840** |

- The MI's structural vulnerability carries **weak, real** forward signal (AUC
  ~0.69–0.73; top-vulnerability quartile crisis-enriched at 0.76/0.60 vs base
  0.54/0.41; PPV lift 1.16–1.33×), but **fails the pre-registered bar**: a
  one-variable income model and an FSI-only model both discriminate crises
  *better* in every window where available.
- **Trajectory→growth: no signal** — the Safeguard-J trajectory call predicted
  relative GDP growth at 0.75×/0.95× of the majority baseline (no lift).
- The two windows overlap, so they are consistency, not independent confirmation;
  both point the same way.

**Reconciliation with Finding 3 (the durability gate).** Finding 3's strong
result (+25.7 pts, zero false positives) is on the **19 curated durability-gate
validation cases**. This full-universe, out-of-time test — which includes the same
P4−P1 gap inside the composite — says the structural signal does **not** generalize
to beat trivial predictors on the open field. So the durability gate is best read
as a **real but narrow** signal (strong on cases resembling its validation set,
weak as a general crisis predictor), not a crystal ball. A clean J-only out-of-time
isolation is the remaining step.

## Finding 7 — Historical program: was the signal cleaner before capital? (mostly yes)

Tests whether the structural signal was stronger pre-modern and has eroded as a
mobile capital order decoupled prosperity from institutions. Artifacts under
`data/robustness/historical/`.

- **Inversion (25 pre-modern cases):** structure out-discriminates rupture vs
  wealth (AUC 0.66–0.68 vs 0.52–0.64) — the *inverse* of the modern holdout.
  Institutional *decline* predicts collapse (0.65); wealth decline is chance
  (0.52). Endo/exo split shows the mechanism: institutional decay 0.222 before
  endogenous collapse vs 0.109 before conquest.
- **Decay curve (1816–1990, conflict onset, COW∪UCDP, 143 polities):** structure
  (V-Dem rule-of-law) beats wealth (log GDP) at predicting conflict in **every**
  epoch, but the margin **halves** toward the present — spread +0.131 (1850) →
  +0.070 (1990); Pearson r = −0.847, p = 0.033 (independently verified). **Soft
  decay confirmed; NOT a sign flip** — wealth never overtakes structure on
  conflict alone (the modern "wealth wins" result was driven by sovereign default,
  a wealth-coupled crisis, being in that outcome).
- **Durability gate on the 25 cases:** no pre-modern jump (gap-direction accuracy
  0.52, AUC 0.74 ≈ modern). Reason is substantive: the P4−P1 gap is *negative*
  across all cases — the economy-outruns-institutions failure mode the gate
  detects is itself a modern/capital-era phenomenon; pre-modern collapse came from
  institutional decline, not economic overreach.
- **Holdout error forensics:** the gate's **misses** (crises it didn't flag) are
  overwhelmingly *external* shocks — 2008 GFC financial contagion in
  sound-institution states (Ireland, Greece, Hungary) + interstate/regional
  conflict — a bounded limitation, not a flaw. Its **false alarms** are partly
  externally-supported states (reserve currency, SWF/rents, EU/IMF anchors), but
  the composite also genuinely over-flags.
- **Caveat that partially rehabilitates the modern gate:** the modern crisis label
  (CRAG default to 2015 + conflict) **misses post-2015 economic collapses**
  (Venezuela 2017, Lebanon 2020, Sri Lanka 2022, Ghana 2022) that the gate DID
  flag — so the earlier "partial null" likely **understates** the gate; its best
  recent hits are invisible to the outcome data.

**Net:** the *soft* form of the "capital distorted the signal" thesis holds across
independent tests — structure's edge over wealth is real in every era and erodes
significantly toward the present, and the modern failure mode is capital-shaped.
The *strong* form (wealth fully overtakes structure) does not hold on clean
outcomes.

## Bottom line so far

After the full audit, the honest position:

- **What holds:** the construct is **not ideologically loaded and not merely
  wealth** (survives indicator substitution at ρ≈0.98, better than a GDP-only
  ranking). The safeguard structure is clean — thin rules are advisory and don't
  inflate the headline (the epicycle charge dissolves).
- **What doesn't:** the "100% directional accuracy" is mostly abstentions and
  human judgment, not a clean automated result. And out-of-time (temporal
  holdout), the structural vulnerability signal is **weak and does not beat a
  trivial income or fragility baseline** at crisis prediction; the trajectory
  prediction has no forward signal. The durability gate's strong 19-case result
  does not generalize.

**Net:** the MI is a **coherent, source-robust descriptive instrument** with one
real-but-narrow predictive signal (the durability gate on cases like its
validation set). It is **not** a validated general forward-predictive instrument —
a simple "poor and fragile states have more crises" model does as well or better.
That is a more credible and more useful position than "100% accurate," and it is
honestly arrived at.

## Open work

1. **Convergent validity (Charge 1 next):** check MI ordering against independent
   *frameworks* (V-Dem, QoG, Bertelsmann) — framework-level, not indicator-level.
2. **Ordinality independent accuracy** — score `post_event`, compare pre-P1
   ordering to actual post-outcome ordering.
3. **J-only out-of-time isolation** — grade Safeguard J alone (not the composite)
   against crises in the temporal windows, to fix its true generalization.
4. **P0 prospective freeze** — grade in ~2034 (the only clean forward test).
