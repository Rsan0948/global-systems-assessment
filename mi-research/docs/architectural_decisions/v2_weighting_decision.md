# V2 Weighting Decision: equal weights (Option A)

**Status:** DECIDED — V2 uses **equal weights** (P1–P5 = 0.20 each). `MI_ACTIVE_WEIGHTING="equal"`.
**Date:** 2026-06-28.

## The choice
- **Option A — equal weights.** All five pillars sit in a tight 0.71–0.80 correlation band at
  143 countries with no permanent leader; equal is simple, defensible, empirically supported.
- **Option B — time-varying.** Elevate the era's most-central pillar (2012→P2, 2018→P1, 2024→P3;
  leader 0.30, rest 0.175). Ambitious: treats the rotation as a feature.
- Rule: run both; better accuracy with no degradation wins; **ties → equal (simplicity)**.

## Retrodiction result (mechanical a/c verdicts, multi-entity cases)
| weighting | scorecard | clean | directional |
|---|---|---|---|
| **A — equal** | 14C / 8P / 0F | 64% | 100% |
| **B — time-varying** | 14C / 8P / 0F | 64% | 100% |

**Zero per-case differences.** The era-elevation (~0.10) never changes an entity ordering — the
P1 gaps dominate the ranking, and convergence/divergence calls are unchanged. The two are
**statistically indistinguishable**.

## Decision
**Equal weights win on the tie-breaker** (simplicity; identical accuracy, no degradation). The
absence of any difference is itself consistent with the V2 thesis: the pillars are co-equal in a
tight band with no permanent leader, so the *weighting* is not where the predictive signal lives —
**the P1 ordinality finding holds regardless of how the pillars are weighted** (see the P1-centrality
restatement). Time-varying weighting is not adopted; the rotation remains an open V3 question
(does the binding constraint shift with global macro conditions?).

*Reproduce:* `python` over `mi.scoring` with `WEIGHTS_V2_EQUAL` vs `v2_timevarying_weights(era)`
for each multi-entity case's pre/post MI (data via `mi.datasource`).
