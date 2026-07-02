# T3 Relational Tier — Phase-2 proof (CONSISTENCY CHECK, not validation)

**Date:** 2026-06-28. Companion to `relational_tier_spec.md`. Reproduce with
`python scripts/relational_tier.py --all`.

## What this is — and is NOT
This is a **consistency / "rescue" check by construction.** It shows the tier resolves **the very
cases it was designed to resolve** (a documented exogenous miss + a survivor). That is evidence the
tier is **internally coherent and does what it was built to do** — it is **NOT evidence that it
predicts.** Resolving cases you built the instrument around is circular as prediction; it is only
informative as a coherence test. **The real out-of-sample test is Phase 4** (the frozen v2
shock-cohort design, `random_validation_brief_v2.md`), which selects cases blind and pre-registers
the rule. Nothing here moves "consistency" to "validation."

## The result
T3 reports two exposure numbers — **structural** (raw external adversity, patron-independent) and
**net** (after patron deterrence) — plus a **response** index. The point of separating them: it keeps
"exposed but shielded" visible.

| Case | Tier | E_structural | Patron | E_net | Response | Outcome | Reading |
|------|------|:---:|:---:|:---:|:---:|---------|---------|
| **Cyprus 1974** | citable | **0.829** (high) | none | 0.863 | **0.192** (low) | invaded / partitioned | high adversity + no patron + weak response → vulnerable |
| **South Korea** | citable | **0.813** (high) | US (credible) | 0.651 | **0.658** | persists | high adversity but patron deters **and** blunts → secure |
| **Poland-Lith. 1772** | hist-proxy | **0.960** (high) | none | 0.968 | 0.393 | erased (3 partitions) | high adversity + no patron + weak response → erased |

## Why it is a clean demonstration
**Cyprus and South Korea face near-identical *structural* exposure (0.829 vs 0.813).** The internal
MI sees neither as catastrophically fragile — which is exactly why Cyprus 1974 was a flat **miss** for
an internal-only instrument. The **entire** difference between "invaded" and "persists" is the
**patron**: Cyprus's 1960 Treaty of Guarantee was structurally non-credible (Turkey was itself a
guarantor; no defender honored it); South Korea has a credible US defender that both deters the shock
and blunts it. Conditioning on exposure turns Cyprus from **miss → consistency hit** without touching
a single MI pillar. Poland-Lithuania 1772 (historical-proxy tier — Maddison economic mass + V-Dem
rule-of-law, not interpretation) shows the same shape pre-1816.

## Golden Rule — baseline byte-for-byte unchanged
T3 is a separate module; `run_retrodiction.py --validate` does not import it (`grep` confirms no
`relational` reference in any baseline path). Post-build validation:
**51 P1-ordinality → 213 Confirmed / 77 Partial / 0 Falsified** (unchanged); durability-gate 17/19;
rule-validation 8/2/2. Additive, deterministic, firewalled.

## Honest limits of this proof
- **n = 2 citable cases** (+1 proxy). A coherence demonstration, not a powered test.
- Cases were **chosen** to exhibit the contrast — the definition of a consistency check, not prediction.
- Cyprus's internal P1/P5 are recorded ordinal estimates (no 1974 WGI), per corpus convention; only
  the **exposure** layer is fully citable.
- Poland-Lithuania's population is supplied from standard historical demography (tech debt: tighten to
  the exact Maddison population series).
- Band thresholds (0.33/0.66), the E4 conflict cap (3), and the R4 depth anchor (500k km²) are
  pre-registered in `mi/relational.py`, not tuned to these cases.

## Next (Phase 3, after review)
Re-tag the full 84-case corpus by the pre-specified endo/exo rule (`relational_tier_spec.md` §C) and
test whether conditioning on exposure resolves the catalogued misses (Spain 1936, Cyprus 1974, Greece
1922, the ancient conquest collapses) — applying the frozen classification rule **before** checking
resolution. Then Phase 4: wire T3 into the v2 shock-cohort out-of-sample run.
