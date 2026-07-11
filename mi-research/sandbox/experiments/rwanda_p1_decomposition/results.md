# Experiment results — P1 composite vs. decomposed (Rwanda architectural decision)

**Date:** 2026-06-27 · **Engine:** LIVE · **Data:** committed mi-pipeline panel (commit 9487dd0), WGI 2025-anchored, panel grid to 2024. Voice from WGI API (panel omits it).
**Reproduce:** `python sandbox/experiments/rwanda_p1_decomposition/run_experiment.py`

## Hypothesis
Decomposing P1 into capacity (Gov Effectiveness + Regulatory Quality) and accountability
(Rule of Law + Voice + Control of Corruption) predicts Rwanda — and the effectiveness/voice
"split-profile" class — better than the current single composite. Falsified if the split
produces no robust differential signal and/or does not change predictions.

## Results

| entity / year | P1 composite | P1a capacity | P1b accountability | cap−acc | within Mod4 margin (0.10)? |
|---|---|---|---|---|---|
| Rwanda 1996 | 0.295 | 0.278 | 0.296 | −0.018 | **YES → abstain** |
| Rwanda 2024 | 0.582 | 0.586 | 0.552 | +0.034 | **YES → abstain** |
| DR Congo 2024 | 0.255 | 0.265 | 0.273 | −0.007 | YES |
| Venezuela 1996 | 0.392 | 0.406 | 0.432 | −0.026 | YES |
| Venezuela 2024 | 0.192 | 0.238 | 0.199 | +0.039 | YES |
| Colombia 2024 | 0.476 | 0.521 | 0.489 | +0.032 | YES |
| Haiti 2024 | 0.223 | 0.220 | 0.269 | −0.050 | YES |
| Dominican Republic 2024 | 0.502 | 0.555 | 0.522 | +0.032 | YES |

**Ordinal-stability / Golden-Rule check (2024), splitting the 0.34 P1 weight into 0.17+0.17:**
Rwanda MI 0.503 → 0.499; DR Congo MI 0.313 → 0.317. The Rwanda ≫ DRC ordinal (gap ≈ 0.19) is
preserved unchanged.

## Findings
1. **In the 2025-anchored WGI vintage, Rwanda's capacity/accountability gap is +0.034 — inside
   the Mod4 margin of error, and *smaller* than Colombia (+0.032..+0.056), and of opposite sign to
   Haiti (−0.050).**
   Rwanda is not a capacity/voice outlier in the current canonical data. The "high effectiveness +
   bottom-tier voice" picture in the proposal rests on the *legacy percentile-rank* vintage; the
   2025 revision moved Rwanda's Voice estimate from ≈ −0.9 to −0.53 and compresses the tails.
2. **Every Batch-1 entity's gap is within the Mod4 margin.** Per the framework's own
   abstention discipline, the framework must NOT assert capacity > accountability ordinally for
   any of them — so a decomposed P1 carries no robust ordinal information here.
3. **Decomposition changes no prediction.** MI moves ≤ 0.005 and no ordinal flips.
4. **The current composite already excludes Voice.** Decomposition's only new input is *injecting*
   VA into accountability, which lowers Rwanda's P1b and biases toward a fragility call —
   exactly the miscall the proposal warned of (scenario b), which Rwanda's realized two-decade
   stability + HDI 0.189→0.578 refutes.

## Verdict
**Decomposition REJECTED (not clearly better).** Proceed with composite P1. The residual —
a genuine but *latent, not-yet-realized* voice/accountability deficit — is a forward-looking
reversal-risk flag, not a structural pillar change. See
`docs/architectural_decisions/rwanda_p1_composite_vs_decomposed.md`.
