# Architectural Decision: P1 stays a single composite (Rwanda decision)

**Status:** DECIDED — proceed composite. Decomposition rejected for now (additive flag recommended instead).
**Date:** 2026-06-27
**Decider:** research agent (this expansion). Flagged for orchestrator review (see "Open question for the user").
**Gates:** This decision was required before scoring Batches 1–6 (per `docs/expansion_plan/case_revisions...md`).

---

## The question
Should P1 (Institutional Quality, 34%) remain a single composite, or be decomposed into:
- **P1a — capacity** = mean(Government Effectiveness, Regulatory Quality)
- **P1b — accountability** = mean(Rule of Law, Voice & Accountability, Control of Corruption)?

Rwanda is the stress case: a developmental-authoritarian state with high government
effectiveness and corruption control but low voice — "exactly the configuration that can break an
ordinal P1 prediction" (proposal). The proposal mandated settling this *before* the batches and
warned the case "can be embarrassed either way."

## What was done
Real, current public indicators were collected for Rwanda (and the rest of Batch 1):
WGI **2025 revision** anchored 0-100 scores (World Bank source 3, `GOV_WGI_*.SC`), UNDP HDR 2025
HDI sub-indices, World Bank WDI (GDP PPP / resource rents / ODA), Fund for Peace FSI 2024.
Rwanda was then scored both ways and compared. Reproducible experiment + numbers:
`sandbox/experiments/rwanda_p1_decomposition/` (`run_experiment.py`, `results.md`).

## Evidence

| | P1 composite | P1a capacity | P1b accountability | cap−acc gap |
|---|---|---|---|---|
| **Rwanda 2023** | 0.594 | 0.589 | 0.558 | **+0.030** |
| Rwanda 1996 | 0.295 | 0.278 | 0.296 | −0.018 |

Rwanda's WGI 2023 (anchored 0-100 / estimate): GE 59.3/+0.41 · RQ 58.4/+0.23 · RL 58.2/+0.07 ·
CC 61.6/+0.68 · **VA 47.6/−0.53** · PV 66.5/+0.04. Standard errors ≈ 0.14–0.19 on the estimate scale.

Four reasons the decomposition is **not clearly better**, and one reason it is **risky**:

1. **The capacity/accountability gap is inside the margin of error.** +0.030 on the 0-1 scale is
   well within the Mod4 margin (0.10). Per the framework's own abstention rule, we may not assert
   capacity > accountability for Rwanda — so the split carries no robust ordinal signal. Across
   *all* of Batch 1 every entity's gap is within margin (Colombia +0.050, Haiti −0.058, DR +0.035,
   Venezuela ±0.04–0.05) — Rwanda is not even an outlier.
2. **The vintage matters and the canonical vintage shrinks the puzzle.** The proposal's "65th-pct
   effectiveness vs bottom-tier voice" rests on legacy *percentile ranks*. The 2025 WGI revision
   replaced those with anchored scores and moved Rwanda's Voice estimate from ≈ −0.9 to −0.53. In
   the current canonical data the effectiveness/voice chasm is a ~3-point gap, not a chasm.
3. **It changes no prediction.** Splitting the 0.34 P1 weight into 0.17+0.17 moves Rwanda's MI
   0.579→0.571 and DRC's 0.338→0.347; the Rwanda ≫ DRC ordinal (gap ≈ 0.24) is unchanged.
4. **The composite already excludes Voice.** P1 (current) = GE, RL, RQ, CC — no VA. So the
   composite never over-credited Rwanda for accountability; the *only* new thing decomposition
   does is inject VA, lowering P1b and pushing toward a **fragility** call. Rwanda's realized
   two-decade stability and HDI 0.189→0.578 refute that call (proposal scenario b). The composite
   is therefore the *better* predictor of the realized outcome, not the worse one.
5. **Golden-Rule risk.** Restructuring P1 changes P1 everywhere, including confirmed
   high-capacity/low-voice baseline cases (Singapore #7, the framework's cleanest positive
   confirmation). Injecting VA risks degrading those — a regression the Golden Rule forbids unless
   the new cases prove a *clear* gain, which they do not.

## Decision
**P1 remains a single composite.** Proceed to score Batches 1–6 on the existing architecture.

The genuine residual — a *latent, not-yet-realized* accountability/voice deficit that the
realized record has not yet cashed out — is captured as a **forward-looking reversal-risk flag**,
not a pillar change. Recommended (additive, deferred until tested):

> **Safeguard C extension (proposed, NOT yet implemented):** extend the reversal-risk flag to
> *non-transition developmental-authoritarian* states exhibiting a capacity-leads-accountability
> profile (high GE/CC, depressed VA) even when `is_democratic_transition` is false. Output a
> qualitative "latent reversal/ succession risk" flag — never an ordinal P1 change.

Per the proposal's own threshold ("formally split P1 only if Rwanda, Vietnam, **and** Singapore
all require ad hoc exceptions"), the trigger is not met: composite P1 predicts Rwanda's realized
stability correctly with no ad hoc exception. **Vietnam (Case 31) and the Gulf/Singapore cases
should re-test the proposed Safeguard-C extension in later batches before any structural change.**

## Caveats (kept intact per integrity rules)
- Directional/ordinal only; the capacity/accountability sub-gaps are within the WGI margin and are
  reported as *abstentions*, not rankings (Mod4).
- WGI 2025 vintage break: new cases use 2025-anchored scores; the 20-case baseline used legacy
  percentile ranks. Do not assert an ordinal across that vintage boundary.
- This is one case's worth of evidence on a structural question; the recommendation is to keep the
  cheaper, reversible option (composite + a flag) and accumulate Vietnam/Gulf/Singapore evidence
  before considering an irreversible structural split.

## Open question for the user
This is a structural call made provisionally from evidence. If you want P1 decomposed for
*reporting* purposes (showing capacity vs accountability sub-scores alongside the composite,
without changing the scoring/weights), that is a low-risk additive display change I can make. A
full structural split changing the weights is **not** recommended on current evidence.
