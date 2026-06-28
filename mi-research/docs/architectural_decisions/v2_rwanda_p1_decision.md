# V2 Architectural Decision: P1 stays composite (Rwanda/Vietnam/Singapore/Gulf)

**Status:** DECIDED — keep P1 composite in V2. Decomposition flagged as a **V3 research question**.
**Date:** 2026-06-28 · **Gates:** required before the V2 50-case (here: 35-case) retrodiction.

## The test
Per the V2 spec: score P1 as composite **and** decomposed into state capacity (Government
Effectiveness + Regulatory Quality) vs. institutional accountability (Rule of Law + Voice +
Control of Corruption), across the four/five cases where the effectiveness/voice split is
supposed to matter most. Implement decomposition in V2 **only if it produces materially better
predictions across all of them**; otherwise keep composite (Safeguard C catches the reversal
risk from low voice) and note decomposition for V3.

## Evidence (2024, MI v2 anchored data)

| entity | P1 composite | capacity (GE,RQ) | accountability (RL,VA,CC) | cap − acc | outside Mod4 margin? |
|---|---|---|---|---|---|
| Rwanda | 0.582 | 0.586 | 0.552 | **+0.034** | no (abstain) |
| Vietnam | 0.479 | 0.501 | 0.440 | **+0.061** | no (abstain) |
| Singapore | 0.874 | 0.921 | 0.756 | **+0.165** | yes |
| Saudi Arabia | 0.631 | 0.663 | 0.511 | **+0.152** | yes |
| UAE | 0.705 | 0.742 | 0.597 | **+0.146** | yes |

## Findings
1. **The split is real but NOT uniform.** Capacity exceeds accountability in all five, but the gap
   is *large and outside the WGI margin* only for Singapore/Saudi/UAE; for Rwanda and Vietnam it is
   *inside* the margin (Mod4 → abstain). So there is no single "decompose everywhere" signal — the
   condition "materially better across **all**" is not met.
2. **Decomposition would not improve predictions of the realized outcomes.** All five are *stable*
   (no reversal/collapse). Decomposition's only new input is injecting Voice, which lowers the
   accountability sub-score and biases toward a **fragility** call — directly contradicted by their
   realized stability + development. Composite is the better predictor of what actually happened.
3. **The composite already excludes Voice** (P1 = GE, RL, RQ, CC). So it is not "fooled" by the
   capacity/voice split in the first place; decomposition adds risk, not accuracy, for scoring.
4. **The residual is genuine but latent and prospective.** Low voice plausibly raises *future*
   succession/reversal risk — but that is unrealized, hence not scorable now. It belongs to V3
   (test if/when a high-capacity/low-voice state actually reverses), and meanwhile is handled
   qualitatively by Safeguard C (+ the proposed non-transition developmental-authoritarian extension).

## Decision
**P1 remains a single composite in V2.** Decomposition is documented as a **V3 research question**
(prospective: does injecting accountability/voice improve predictions once a low-voice high-capacity
state reverses?). This matches the V1 decision and is reinforced by the broader 5-state V2 evidence.

*Reproduce:* re-run the table above via `mi.datasource` + `mi.scoring.calculate_pillar_scores`
for the five entities at 2024 (data in `data/sources/wb_anchored.json`).
