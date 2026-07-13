# FINAL REPORT — the predictive-reach campaign, end to end

One question drove everything: *what do the MI apparatus and its tiers actually predict, forward, beyond what a country's own past already tells you?* The answer, arrived at across ~40 analyses and hardened with permutation nulls, out-of-sample splits, and 31 regression tests: **capacity is the master variable — it acts as a within-country, nonlinear state with a safety ceiling near the 80th percentile, and it dominates every rival explanation, every fancy transform, and 200 years of history.**

Sandbox: branch `sandbox/predictive-reach`. Standing rigor: cohort cross-sections (no pseudoreplication), always net of an AR(lagged)+GDP baseline, held-out-country or out-of-time evaluation, permutation nulls, no in-sample numbers. Every real finding *and* every null is locked by a test in `test_harness.py` (31/31).

---

## PART A — The predictive-reach screen (what the tiers forecast)

**A1. Two modes — nowcast vs forecast.** Of 911 confirmed univariate hits, **577 collapsed under an AR baseline** (persistence fingerprints: `cso→libdem_level` 0.81→0.01, `youth→fertility` 0.90→−0.12). The apparatus *nowcasts* structural state superbly (ρ 0.6–0.9 on levels) but that is persistence, not forecasting.

**A2. What it genuinely forecasts (survives AR baseline).** 171 level hits + 163 change/event forecasts. Standouts (incremental ρ, out-of-sample):
- **Conflict onset** — the scarring trap, forward to 10y (`prior_conflict_decayed→onset` +0.23→+0.41).
- **Life-satisfaction** 5–10y (capacity P3 +0.41; scarring −0.39; spark −0.28) — wellbeing is the biggest cross-domain reach.
- **GDP growth** 3–10y (capacity, +0.22–0.25); **emigration** (durability gap → net migration −0.26).

**A3. Stacking cracks backsliding — which no single tier could.** Best single tier ~0.55 AUC; regularized ensemble **AUC 0.68–0.72**. "Tiers add, don't multiply" (interactions ≈0 held-out); exhaustive 21k-subset search *overfits* (best-4-subset 0.54 < regularized-all).

**A4. Relational beats additive.** Gaps/ratios *between* instruments forecast backsliding far better than their levels: **REL 0.72 vs ADD 0.56** (libdem), replicated k=3/5/10. Strongest single relationship: **capacity − turbulence**. Founding equation as one number (complexity−capacity) too coarse (0.47–0.56) — needs the specific pairwise gaps.

**A5. Out-of-time confirmation (the real test).** Temporal holdout, rolling origin (Δ = relational − AR+GDP baseline):
| train → test | libdem Δ | electdem Δ | baseline |
|---|---|---|---|
| ≤2004 → 2008/2012 | **+0.142** | **+0.115** | 0.56 |
| ≤2008 → 2012 | **+0.147** | **+0.161** | 0.50 |
| ≤2012 → 2016/2018 | −0.121 | −0.022 | **0.77 (saturated)** |
Confirms in **2 of 3 windows**; fails only on the 2016–2023 wave because it hit wealthy democracies and the level+wealth baseline was already saturated. λ-robust (not overfitting), placebo ~0.50 (no leakage). Calibration: frozen-8 AUC 0.69–0.72 but top-risk quintile non-monotone → **triage, not backslider-naming**.

---

## PART B — Deep time (same math back to 1820)

**B1. Different ruptures run on different clocks.** Democratization has a fast channel (turbulence, ρ +0.12 at k≤10, decays to 0 by k=30) and a slow one (capacity, ~0 short-term → **+0.16 at k=30**), crossing at **~12–15 years**. Backsliding is all-horizon and intensifying. Conflict is long-horizon (capacity−anocracy gap ρ −0.04 at k=5 → **−0.14 at k=30**).

**B2. The capacity→democratization *composition inversion*.** Prior-capacity gap of future democratizers: **+0.62 (19th c.) → −0.43 (modern)** — robust with independent WGI (**−0.58/−0.62**), permutation-real. Mechanism: saturation (**86%** of high-capacity states already democratic by the modern era) + genuine decoupling. Audit-corrected: the raw "channel died to 0" was rol/libdem multicollinearity; the real, robust finding is the composition shift. **The post-1945 spread of democratic form to institutionally weak states created the fragile democracies that make capacity→backsliding thrive.**

**B3. Prospective third-wave test.** 81 democratization transitions (17 backslid). Capacity-at-transition → subsequent backsliding: **ρ=−0.32, perm-p=0.035 (post-1975)**; the post-75 low-capacity cohort = **33% of transitions but 53% of all backsliders**. Categorical version underpowered (17 events) — the continuous gradient is what's real.

**B4. Adversarial audit.** No leakage, permutation-real, `near()`-tolerance-robust; independent-WGI cross-check confirmed the composition inversion; one overstated framing ("channel died") corrected.

---

## PART C — The six angles

| # | Angle | Verdict | Key number |
|---|---|---|---|
| **1** | Dynamic (rates) | **NULL** — founding equation is a *state*, not a *rate* | static gap real (−0.09, perm-p 0); velocity adds nothing (−0.017, perm-p 0.31) |
| **2** | Within-country FE | **REAL** — capacity–mobilization gap predicts *within* a country, invisible between | WITHIN ρ=−0.081 (perm-p 0), BETWEEN −0.006; rol-alone = ceiling artifact (killed by libdem control) |
| **3** | Contagion | **NULL** — waves are global, not neighbour diffusion | neighbour effect +0.024; real neighbours ≈ random neighbours |
| **4** | Attributes | **CAPACITY DOMINATES** — rivals null or capacity-mediated | resource/ethnic/size null net of capacity; legal-origin gradient 0%→13% collapses to ±0.03 residual |
| **5** | Survival / age | **PARTIAL** — hazard front-loaded but capacity-driven | hazard 0.057/yr (0–4y) → 0.001/yr (40y+); capacity coef −1.32; age entangled (perm-p 0.57, 52 events) |
| **6** | Nonlinear | **REAL & STRONG** — inverted-U, danger at mid-capacity | linear AUC 0.63 → **quadratic 0.74 (+0.10)**; safety ceiling ~80th pctl, bootstrap [0.80,0.85] |

---

## PART D — The capacity arsenal

**D1. How far capacity alone goes.** Full mathematical toolkit → **OOS AUC 0.746** (libdem baseline 0.705). Winning form: nonlinear (inverted-U + safety ceiling) + a trace of history.
- **Single strongest feature in the whole campaign: the safety ceiling `I(cap>0.80)` — AUC 0.732**, beating democracy level itself.
- **The exotic math is null:** complex `z=cap+i·mobilisation` phase = **0.571** (worse than useless); dynamical VAR(1) eigenvalues (spectral radius, oscillation) ~0.68 (null). Kitchen-sink "EVERYTHING" (0.712) < disciplined nonlinear+history (0.746).

**D2. Relational-vs-additive boundary.** ADDITIVE 0.746 vs RELATIONAL 0.732 — relational does *not* beat additive for transforms of a single variable. **"Relational > additive" is scope-limited to combining DIFFERENT instruments** (distinct faces whose imbalance is the signal); for one variable, additive with a nonlinear basis is correct.

---

## THE SYNTHESIS

**Capacity is the master variable, and we now know exactly how it works:**
1. as a **within-country state deviation** (Angle 2) — *not* a rate (Angle 1), *not* contagious (Angle 3);
2. **nonlinearly**, with peak rupture risk at *mid*-capacity and a hard safety ceiling near the 80th percentile (Angle 6, arsenal);
3. **dominating every rival** — resource curse, ethnic division, size, legal origin, and age all fold into it (Angles 4, 5);
4. and its power is **simple** — not hiding in phase space, spectral structure, or complex dynamics (arsenal).

**The big-picture arrow:** the post-1945 world spread democratic *form* faster than state *capacity*, producing a stock of capacity-poor democracies. That decoupling both killed the old capacity→democratization channel and created exactly the population where capacity now predicts backsliding. The democratic recession is not a mysterious mood; it is form re-equilibrating to capacity. **The single most actionable, testable statement: a democracy above the ~80th percentile of rule-of-law capacity rarely backslides; the danger zone is the partially-institutionalized middle.**

*Everything here is a lead validated under controls (held-out / out-of-time / permutation), not a causal claim. Data caveats per section. Reproduce: `run_all.py` then `run_angles.py`; verify: `test_harness.py` (31/31).*
