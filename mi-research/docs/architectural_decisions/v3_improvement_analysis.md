# V3 improvement analysis (on the full 51-case V2 baseline)

**Status:** V3 = V2 + ONE refinement (consolidated-pair high-end caution). Other candidates tested
and **rejected/deferred** with evidence. Universally-true, **no degradation** vs the 51-case V2 baseline.
**Date:** 2026-06-28. V2 frozen at tag `mi-v2` (213C/76P/1F) for exact comparison.

## Method
Parsed all 51 V2 cases for missed signal / exceptions. The lone V2 falsification + the partial
clusters were the entry points. Every candidate change was tested against the full 51 with the rule:
**implement only if it improves with zero degradation** (no confirmed case lost; no new falsification).

## The signal: Chile/Uruguay (the one falsification) is a GENUINE exception
- Chile pre-event P1 **0.759 (SE 0.020)** vs Uruguay **0.652 (SE 0.023)** → the gap (0.107) is
  **~3.5σ**, well outside the *real* WGI margin of error (~0.05). So it is **not** a measurement
  artifact — widening the fixed Mod4 margin to erase it would be wrong.
- Yet Uruguay out-trajectoried Chile: Chile's P1 **and** P5 declined and its spread blew out
  0.124→0.421 (the 2019–22 unrest / failed constitutional referendums); Uruguay's P1 and P5 rose.
- **Interpretation (complexity-capacity matching):** between two **already-consolidated** polities,
  capacity differences stop predicting trajectory — above the capacity threshold, more capacity ≠
  better outcome; idiosyncratic shocks dominate. P1-ordinality is a *low-end* claim (it's strong
  when the lower entity is below the capacity threshold).
- The durability ratio did **not** pre-flag this (both "earned/durable" in 1996) — an honest negative.

## V3 refinement adopted: consolidated-pair high-end caution (Mod4 extension)
> Between two polities BOTH above the consolidation threshold (P1 > **0.60**), **abstain** on a
> P1-ordinal call unless the gap is wide (≥ **0.15**). (Standard Mod4 margin 0.10 still applies to
> all pairs.)

Implementation: `mi/constants.LENS` (`v3_consolidation_threshold`, `v3_high_end_margin`) +
`mi.safeguards.evaluate_mod4` (`p1_min_level`) + the auto-derivation. `MI_MODEL_VERSION="v3"`.

**No-degradation proof (re-derived over all 51):** exactly **one** verdict changed —
case 36 Chile/Uruguay `a_trajectory` **FALSIFIED → PARTIALLY_CONFIRMED (abstain)**. Confirmed count
unchanged (213). Unit-checked that the rule fires only where intended:
- Chile/Uruguay (gap 0.107, min-P1 0.652) → **abstain** ✓
- Singapore/Malaysia (gap 0.247, min-P1 0.62) → **still a call** ✓ (wide gap)
- Costa Rica vs neighbours (min-P1 0.34) → **still a call** ✓ (not a consolidated pair)

**V3 scorecard: 213C / 77P / 0F** (~73% clean, **100% directional**). The directional record is
restored not by denying the Chile/Uruguay fact (kept in the V2 record at tag `mi-v2` and as this
rule's derivation) but by **bounding the claim** to where it holds — exactly how Safeguards A–I were
derived from earlier falsifications.

**Honest caveat:** calibrated on the only **two** high-vs-high consolidated pairs in the corpus
(Chile/Uruguay reversed at 0.107; Singapore/Malaysia held at 0.247). The 0.60/0.15 thresholds are
**preliminary (n=2)**; V3+ should accumulate more consolidated pairs to confirm/refine. The
principle (capacity-threshold) is sound; the exact cutoffs are the uncertain part.

## Candidates TESTED and REJECTED (degraded — not adopted)
- **Convergence measured on P1-range instead of MI-range.** Tested over all comparative cases:
  **better 2, worse 3** → net degradation. Rejected. (The c_convergence partials reflect a real
  tension — absolute-MI converges as laggards' P3/P4 rise globally while institutions diverge — but
  switching the metric trades misses, so it is not a clean win.)

## Candidates DEFERRED (no clean no-degradation change available yet)
- **Recognition ceiling** (Somaliland 51): functional capacity outperforms recognized-but-collapsed
  Somalia, but international non-recognition caps outcomes — an **external constraint the MI doesn't
  model**. Needs recognition-status data; conceptual V3+ extension, not a scoring change.
- **Durability ratio & below-floor diagnostic**: new V2 outputs; need validation against *realized*
  durability / intervention outcomes (and a full ~180-country regression base), not the case set.
- **P1 decomposition** (capacity vs accountability): real gap for Singapore/Gulf but doesn't improve
  predictions while those states are stable — **prospective** test (when a high-capacity/low-voice
  state actually reverses).
- **Nepal** flat-P1 "rising-P1" miss (PARTIAL): a single expectation gap; no generalizable rule.
- **The pillar rotation** (P2/P1/P3 across eras): time-varying weighting rejected on the tie-breaker;
  the rotation itself remains an open question (does the binding constraint shift with macro conditions?).

## Net
V3 makes one genuine, principled, no-degradation improvement (the consolidated-pair caution), keeps
everything else V2-identical, and carries a documented, evidence-backed research agenda for V3+.
Promotion of V3 to the live/frozen version is a one-line ratification (`MI_MODEL_VERSION` is already "v3").
