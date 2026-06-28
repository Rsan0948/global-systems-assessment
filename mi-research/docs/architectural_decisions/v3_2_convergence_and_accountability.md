# V3.2 — Convergence Qualifier (adopted) + Accountability Gap (hypothesis)

**Date:** 2026-06-28. `MI_MODEL_VERSION = "v3.2"`. Both came out of the G7/G10/G20 exploration
(`docs/big_boys_exploration_G7_G20.md`). **A is adopted** (validated, additive); **B is an
informational hypothesis** (no crisis evidence yet). Neither changes any existing verdict —
51-case ordinality baseline (213C/77P/0F) and the 19 durability-gate verdicts (17/19) are unchanged.

## A — Convergence Qualifier (refines Safeguard J) — ADOPTED
A flagged durability gap (P4 − P1) means **opposite things by trajectory**. Refining Safeguard J with
the gap's direction over a ~5–10y window:
- **CLOSING** (gap narrowing, P1 rising) → *developmental catch-up* — institutions building toward
  income; downgrade the structural-crisis weight.
- **WIDENING / static** (the grant eroding, income outrunning institutions) → *fragility* — confirm/escalate.

**Validation (flagged states, known outcomes):** 92% sensitivity / 80% specificity.
- Closing → no crisis: China, India, Indonesia, Italy (recovering). Widening/static → crisis: Russia,
  Mexico, Brazil, South Africa, Turkey, Tunisia, Sri Lanka, Egypt, Thailand, Argentina, Lebanon.
- **Two instructive errors:** *Saudi* (widening via an oil-income windfall with P1 *rising* — a rentier
  overshoot, not decay → FP) and *Peru* (gap closing but a political-churn crisis → FN). Both refine
  scope rather than break the rule: the dangerous widening is P1-falling decay, not P4-surge windfall.

**Implementation:** `evaluate_safeguard_j(pillars, context)` adds a `convergence` block when
`context["prior_pillars"]={"P1":..,"P4":..}` (a prior timepoint) is supplied — `direction`
(`LENS.structural_vuln_converge_deadband`=0.01) and `refined` ∈ {developmental_catchup, fragile}.
Back-compat: with no prior, the static three-state stands. Breadth: `scripts/big_signals_scan.py`.

## B — Accountability Gap ("capacity without consent") — HYPOTHESIS, informational
P1 deliberately excludes Voice & Accountability (VA); among high-capacity states VA is the only axis
separating democracies from rich authoritarians. **VA − P4** (accountability vs income):
- **≤ −0.50 legitimacy-capped:** Saudi (−0.63), Russia (−0.58), China (−0.57), Turkey (−0.51) —
  delivers economically with no accountability channel. Hypothesized **brittle/sudden** failure mode
  (succession/legitimacy shock), **orthogonal** to the durability gap: China is *closing* its gap
  (A says developmental) **and** legitimacy-capped (B says brittle) — the two axes measure different
  things and correctly disagree.
- −0.20 to −0.50 lag; > −0.16 balanced (all of W. Europe, Japan, Canada, Australia).

**Status: hypothesis.** No crisis evidence yet (Saudi/China haven't broken; Russia/Turkey backslid,
consistent). Surfaced as an **informational diagnostic, never a verdict** — `diagnostics.accountability_gap()`,
in `full_diagnostic`, and in the panel scan. Targets a future case class (see corpus coverage gaps).

**Wiring:** VA for all 180 panel countries committed at `data/sources/va_anchored.json` (WGI
GOV_WGI_VA.SC, 2025-anchored); `datasource.get_indicators` now serves `voice_accountability` with a
va_anchored fallback for any panel country; `scripts/big_signals_scan.py` computes both A and B for
any country / the G-set / the whole panel.

## Integrity
Additive only; deterministic; no verdict changed. A is validated and live in the engine; B is an
explicitly-labeled hypothesis with no crisis validation. Source-vintage note: `full_diagnostic`
(wb_anchored) and the panel scan can differ slightly on VA/P4 (different snapshots) — near boundaries
(e.g. Turkey ~−0.45 vs −0.51) the lag/cap label can flip; both are "low-accountability."
