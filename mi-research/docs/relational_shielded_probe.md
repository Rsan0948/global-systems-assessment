# Shielded-survivor probe — the 4th cell, populated (DISCRIMINATION check, not validation)

**Date:** 2026-06-28. Reproduce: `python scripts/run_shielded_probe.py`. Firewalled from the
213/77/0 baseline. Companion to `relational_tier_spec.md`, `relational_retag_phase3.md`,
`validation_run_v2_cohorts.md`.

## Why this exists
Phase 3 and the v2 cohort run both showed the same gap: the discriminating 2×2 cell — **internally
fragile + high exposure + SHIELDED → survives** — is empty in the 51-case corpus, the random 30, and
the v2 cohorts. Without it, "high-exposure cases ruptured" can't be separated from "they were
unlucky." Shielded survival is rare and undramatic, so random/cohort sampling won't return it. This
probe populates the cell **deliberately**, with its contrast, to test whether T3 *discriminates*
rather than merely *flags*.

## Status — read first
**NON-RANDOM, NON-BLIND, hand-selected — a DISCRIMINATION PROBE, NOT an out-of-sample test.** Cases
were chosen precisely because they sit in the target cell, so this **cannot** show predictive power
(the real predictive test still needs a *blind military-shock cohort*). It can show one thing: whether
T3's response-patron axis tracks survival-vs-collapse among internally-weak, highly-exposed states —
the necessary condition for T3 to be more than a flag. The shield codings follow **documented history**
(coalition restored Kuwait; Dayton/NATO protected Bosnia; no patron honored Cyprus), assigned from the
record, not from T3's output — so the discrimination is not circular.

## The completed 2×2
| case | internal (P1) | structural exposure | shield (response-patron) | outcome |
|------|:---:|:---:|:---:|---------|
| **Bosnia 1995** | 0.35 (fragile) | 0.882 (high) | **SHIELD** (Dayton/NATO) | **SURVIVED** as a state |
| **Kuwait 1990** | 0.62 (militarily indefensible) | 0.819 (high) | **SHIELD** (coalition) | invaded → **RESTORED** |
| Taiwan 1996 | 0.75 (durable) | 0.812 (high) | SHIELD (US/TRA) | persists |
| Estonia 2003 | 0.97 (durable) | 0.496 (mod) | SHIELD (NATO) | persists |
| Cyprus 1974 | 0.45 (fragile) | 0.829 (high) | none | **FELL** (partitioned) |
| Poland-Lith. 1772 | 0.18 (fragile) | 1.000 (high) | none | **FELL** (erased) |
| Afghanistan 2019 | 0.16 (fragile) | 0.444 (mod) | shield **WITHDRAWN** 2021 | **FELL** (2021) |

**The discriminating row (internally fragile + highly exposed):**
- **shielded → survives:** Bosnia (and Kuwait, militarily indefensible, restored by the coalition).
- **unshielded → falls:** Cyprus, Poland-Lithuania, Afghanistan (shield withdrawn).

Same fragility, same high exposure — **the response-patron is the entire difference between surviving
and falling.** That is the discrimination the empty cell was blocking: survival here is *not* explained
by internal strength (these states are weak) and *not* attributable to luck (the unshielded twins
fell). T3's response axis tracks it.

## What it forced in the engine (data-driven, like the earlier refinements)
**Kuwait decoupled deterrence from response.** Kuwait had **no credible deterrent** ex ante (no one
was committed to defend it → Iraq invaded) but a **decisive response patron** ex post (the coalition
expelled Iraq and restored sovereignty). The model previously tied both to one flag; it now separates
the **deterrence-patron** (E2, lowers net exposure) from the **response-patron** (R3, blunts/reverses a
shock that lands). Afghanistan is the mirror image — a response-patron *present then withdrawn*, the
withdrawal decisive.

## Honest limits
- **Purposive selection, small n** (a few per cell) — a discrimination check, not validation, not powered.
- Some CINC values are approximate (flagged in the data); Bosnia/Kuwait relative-power figures are
  order-of-magnitude.
- **Afghanistan is impure for T3** — the proximate threat was a Taliban *insurgency*, not interstate
  conquest; included as the vivid shield-withdrawal contrast, with Cyprus as the clean interstate one.
- Kuwait sits on the institutional fragile/durable line (rol 0.62) but is the clearest "couldn't defend
  itself, restored by patron" case — it belongs to the cell by *military* fragility.

## What this does and does not establish
- **Does:** T3's response-patron axis cleanly separates survival from collapse in the previously-empty
  fragile+exposed cell — the necessary condition for T3 to discriminate. Combined with the Phase-2 proof
  (Cyprus/SK structural-exposure mirror) and the Phase-3 miss-discrimination (resolves exogenous misses,
  silent on internal ones), T3 behaves coherently across all four quadrants.
- **Does NOT:** prove T3 predicts. Selection is purposive. The pending real test is a **blind
  military-shock cohort** with the deterministic relational pull (COW CINC/ATOP/ICOW) wired into the
  scoring protocol — the one design that could move T3 from "coherent" to "validated."
