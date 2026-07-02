# Experiment results — P1 composite vs. decomposed (Rwanda architectural decision)

**Date:** 2026-06-27 · **Engine:** LIVE · **Data:** WGI 2025-anchored 0-100 (`.SC`), committed country files.
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
| Rwanda 2023 | 0.594 | 0.589 | 0.558 | +0.030 | **YES → abstain** |
| DR Congo 2023 | 0.253 | 0.271 | 0.281 | −0.010 | YES |
| Venezuela 1998 | 0.380 | 0.381 | 0.434 | −0.052 | YES |
| Venezuela 2023 | 0.210 | 0.243 | 0.205 | +0.038 | YES |
| Colombia 2023 | 0.491 | 0.538 | 0.487 | +0.050 | YES |
| Haiti 2023 | 0.222 | 0.214 | 0.272 | −0.058 | YES |
| Dominican Republic 2023 | 0.500 | 0.539 | 0.505 | +0.035 | YES |

**Ordinal-stability / Golden-Rule check (2023), splitting the 0.34 P1 weight into 0.17+0.17:**
Rwanda MI 0.579 → 0.571; DR Congo MI 0.338 → 0.347. The Rwanda ≫ DRC ordinal (gap ≈ 0.24) is
preserved unchanged.

## Findings
1. **In the 2025-anchored WGI vintage, Rwanda's capacity/accountability gap is +0.030 — inside
   the Mod4 margin of error, and *smaller* than Colombia (+0.050), Haiti (−0.058) or Venezuela.**
   Rwanda is not a capacity/voice outlier in the current canonical data. The "high effectiveness +
   bottom-tier voice" picture in the proposal rests on the *legacy percentile-rank* vintage; the
   2025 revision moved Rwanda's Voice estimate from ≈ −0.9 to −0.53 and compresses the tails.
2. **Every Batch-1 entity's gap is within the Mod4 margin.** Per the framework's own
   abstention discipline, the framework must NOT assert capacity > accountability ordinally for
   any of them — so a decomposed P1 carries no robust ordinal information here.
3. **Decomposition changes no prediction.** MI moves ≤ 0.01 and no ordinal flips.
4. **The current composite already excludes Voice.** Decomposition's only new input is *injecting*
   VA into accountability, which lowers Rwanda's P1b and biases toward a fragility call —
   exactly the miscall the proposal warned of (scenario b), which Rwanda's realized two-decade
   stability + HDI 0.189→0.578 refutes.

## Verdict
**Decomposition REJECTED (not clearly better).** Proceed with composite P1. The residual —
a genuine but *latent, not-yet-realized* voice/accountability deficit — is a forward-looking
reversal-risk flag, not a structural pillar change. See
`docs/architectural_decisions/rwanda_p1_composite_vs_decomposed.md`.
