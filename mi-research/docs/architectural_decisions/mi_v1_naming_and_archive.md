# Decision: "MI v1" is the canonical version; the hand-assigned draft weights are archived

**Status:** ADOPTED — 2026-06-27. **Decider:** user directive.

## What changed
1. **The LIVE methodology is now named "MI v1"** and is the only supported version going
   forward. "MI v1" ≡ the former **"LIVE"/v2**: correlation-derived pillar weights
   (P1 0.34 / P2 0.15 / P3 0.16 / P4 0.20 / P5 0.16) plus Mods 4 & 8 and Safeguards A–I.
   `mi/constants.WEIGHTS` is MI v1 and must always be used for scoring.
2. **The original hand-assigned draft weights are ARCHIVED** (P1 0.25 / P2 0.25 / P3 0.20 /
   P4 0.20 / P5 0.10). Previously these were labelled "v1"; that label now belongs to the
   canonical methodology, so the draft weights are renamed
   `WEIGHTS_ARCHIVED_HAND_V0` and marked **DO NOT USE FOR SCORING**. They are retained only
   for (a) the documented 25%→34% P1 provenance and (b) historical sensitivity reporting.

## Why
- One canonical version removes the v1/v2/LIVE naming ambiguity that had accumulated.
- The correlation-derived weights are the validated framework (LIVE ≥ STATIC in every run,
  per `live/runs/run6of6_definitive_synthesis_20cases.md`); making them THE version, named
  MI v1, matches how the work is actually used.

## Scope / non-effects
- **No scoring change.** `WEIGHTS` (MI v1) is numerically identical to the prior LIVE/v2
  weights. Estonia baseline verified unchanged (MI 0.793, Tier 2). The 20-case validated
  baseline is unaffected (Golden Rule satisfied).
- The sensitivity block now reports `mi_v1` (canonical), `equal_weights` (robustness
  control), and `archived_hand_v0` (historical only) — replacing the old `v1/v2/equal` keys.
- **Historical runs keep saying "LIVE".** Runs 1–6 are the immutable canonical record; they
  are not rewritten. "MI v1 = LIVE" is the bridge; new work uses the name "MI v1".

## Naming note (to avoid confusion forever)
- **MI v1** = canonical methodology = former LIVE/v2 = `WEIGHTS` (P1 0.34).
- **`WEIGHTS_ARCHIVED_HAND_V0`** = the old hand-assigned draft ("v0"), archived, not used.
