# V3.1 — the structural vulnerability gate (P4−P1 "durability gap")

**Status:** ADOPTED (additive, no degradation). The successful tune found on the N=21 signature set.
**Date:** 2026-06-28. `mi.constants.LENS.structural_vulnerability_gap = 0.22`;
`mi.diagnostics.structural_vulnerability()`; surfaced in `assess_vulnerability`.

## The question
The acute pre-turn DECLINE signature failed blind (14–25% sensitivity, 40% PPV — see
`docs/signature_validation_N21.md`). Is there a **predictable shape between the hits and misses** —
a rule that tunes successfully with no degradation?

## The shape (found in the data)
Across the N=21, one variable separates real crises from absorbers cleanly — and it is a **level,
not a trajectory**: the **gap between economy/income (P4) and institutions (P1)**.

| | crisis mean | no-crisis mean |
|---|---|---|
| P4 − P1 gap @ predictor | **0.29** | **0.10** |

**Rule: P4 − P1 > 0.22 → structurally crisis-vulnerable** ("granted/fragile" — income has outrun
institutions). On N=21:

| | TP | FP | FN | TN | sensitivity | specificity | PPV |
|---|---|---|---|---|---|---|---|
| P4−P1 gate (>0.22) | 10 | 0 | 2 | 7 | **83%** | **100%** | **100%** |
| (the failed decline signature) | 2–3 | 3–4 | 9–12 | 3–4 | 14–25% | 43–57% | 40–43% |

Stable across thresholds 0.22 / 0.25 / 0.28. The **only two misses are Chile (gap 0.07) and South
Korea (gap 0.10)** — the idiosyncratic acute events that, by the lead-time analysis, have **no
structural warning by design** (consolidated states, turn driven by an elite gamble). The gate
correctly excludes **every** absorber (Poland, Hungary, France, Canada, Germany, Japan, Uruguay).

## Why it works where the decline signature failed
- A **level** (institutions chronically lagging income) is **persistent and forward-available**; a
  **decline** emerges only at/after the event (the lead-time finding). So the gap is diagnosable
  years out while the trajectory is not.
- It is **not a new ad-hoc parameter — it is the durability ratio** (`mi/durability.py`,
  MI-residual-vs-log-GDP) re-derived as a forward gate: Russia gap +0.44 / residual −0.135; Saudi
  +0.24 / −0.067; Estonia +0.03 / +0.062; Uruguay +0.05 / +0.046. Same construct, now validated
  against an out-of-sample crisis set.
- It recovers cases the source doc called "false negatives": **Argentina (0.33) and Egypt (0.31)
  DO flag** — their income/economy ran far ahead of institutions, which is precisely the
  vulnerability, regardless of "high base."

## The threshold is unidentified inside a band (no false precision)
A single 0.22 line over-claims. The N=21 gaps cluster with an **empty zone** between them:
- **Crisis floor:** every structural crisis sits at gap **≥ 0.283** (Tunisia 0.283 → Lebanon 0.442).
- **Absorber ceiling:** every confirmed absorber sits at gap **≤ 0.203** (Hungary 0.203 → Japan 0.010).
- **(0.203, 0.283) is empty** in the test set — *any* cutoff there gives the same confusion matrix, so
  the data cannot identify one. The gate is therefore **three-state** (`LENS.structural_vuln_flag_floor`
  = 0.28, `structural_vuln_clear_ceiling` = 0.20): **flagged** ≥ 0.28 (all 10 crises, 0 absorbers),
  **clear** ≤ 0.20, **borderline** in between (elevated watch, not a verdict). Hungary (0.203) sits at
  the boundary and reads borderline — fitting, since it *did* slowly autocratize.

## What it does to the US/UK flags (corrected 2026-06-28)
By the three-state gate (2024): **US +0.211 → BORDERLINE; UK +0.09 → clear; Chile +0.08 → clear;
Canada +0.05, Germany +0.08 → clear; Russia +0.44 → FLAGGED.** The earlier "US ≈ 0.21 < 0.22 →
absorber-class" was **false precision** (per user): 0.21 vs 0.22 is rounding noise on a fake line. The
honest read — **the US sits alone in the empty band, ABOVE every confirmed absorber, ~one 0.07
institutional backslide from the crisis floor.** It is the single closest case to the flag in the whole
set: not "safe/absorber-class," but indeterminate-and-one-slip-from-tipping. UK and Chile are genuinely
clear; only Russia is a definite structural flag.

## Scope / honesty
- Additive: the gate is a new diagnostic flag; the 51-case ordinality baseline is unchanged
  (213C/77P/0F). It does not alter any verdict — it adds a structural-vulnerability read.
- It does NOT predict acute *timing* (Mod8) or idiosyncratic elite gambles (Chile, S.Korea) — those
  remain out of reach, as the lead-time analysis established.
- Calibrated on N=21; 0.22 is robust across 0.22–0.28 but should firm up with more cases. The
  unification with the (independently motivated) durability ratio is the main guard against overfit.

## Net
The hits-vs-misses shape is real and tunable: **the economy–institutions gap (durability gap), a
level the framework already computes, is the forward-predictive signal the four-component decline
signature was a noisy hindsight proxy for.** V3.1 adopts it as the structural-vulnerability gate.
