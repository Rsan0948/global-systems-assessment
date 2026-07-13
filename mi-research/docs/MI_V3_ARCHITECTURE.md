# Modernization Index V3 — Structural Pressure (the complexity tier)

**A third instrument, complementary to V1 and V2.** V1 measures *capacity* (institutional
structure). V2 measures *conversion* (how efficiently and equitably capacity becomes citizen
outcomes). **V3 measures *pressure*** — the grievance/mobilization/opportunity "complexity"
term of the founding equation (rupture = complexity > capacity). V1/V2 are the denominator;
**V3 is the numerator.** It is the instrument that predicts the *modern political rupture mode
— democratic backsliding and repression — that state-capacity structure is blind to.**

Built and validated 2026-07-12. Pre-registration `POLITICAL_SIGNAL_PREREGISTRATION.md`
(sha256 `ec4aebe0`); results `POLITICAL_SIGNAL_RESULTS.md`; engine
`scripts/v2/{political_test,deep_political}.py`; data `data/political/*`.

## Why it exists

V1/V2 predict societal/wellbeing outcomes (demographics, life satisfaction) but were **null
on every political outcome net of income** (backsliding, conflict, repression). The design
report (`docs/POLITICAL_SIGNAL_PREREGISTRATION.md` + session record) diagnosed why: we had
operationalized only the *capacity* half of rupture = complexity > capacity, never the
*complexity* half — organized grievance, mobilization, group exclusion, opportunity. V3 is
that half, built from real data, and it **passed its pre-registered gate.**

## The five components (the theoretical decomposition of rupture)

Each is a revealed or expert-coded measure of the pressure a polity is containing:

- **G — Grievance.** Ethnic/horizontal exclusion: EPR-ETH share of population in
  powerless/discriminated/self-excluded groups; discriminated share; income Gini (cross-cut).
  *(Cederman/Gurr horizontal inequality.)*
- **M — Mobilization.** Capacity of the aggrieved to organize: V-Dem civil-society
  participation; internet/coordination penetration; youth bulge (population 0–14 %).
  *(Tilly/McAdam political-process theory.)*
- **O — Opportunity.** Anocracy — regime in the contested middle: `4·libdem·(1−libdem)`,
  maximal at partial democracy; institutional weakness (inverse rule-of-law).
  *(Goldstone/PITF anocracy; the strongest single backsliding predictor.)*
- **H — History / momentum.** Event autocorrelation: prior domestic conflict (last ~20y);
  prior repression trajectory (ΔPTS). *(The conflict/coup trap.)*
- **S — Shock.** Expectation violation: GDP-growth volatility/deceleration; food-import
  dependence (price-shock exposure). *(Davies J-curve.)*

**Data (real, self-served):** EPR-ETH (`icr.ethz.ch`), V-Dem civil-society + liberal-
democracy (OWID), Political Terror Scale, WDI (youth, food imports, internet, growth),
committed UCDP/COW conflict onsets. Note: several inputs are expert-coded (V-Dem/PTS carry a
perception component, unlike V2's revealed-outcome indicators) — flagged, not hidden.

## What it predicts, and how well

The pre-registered gate — **does the V3 numerator block add out-of-fold CV-AUC ≥ 0.05 over
structural [P1 + log GDP]?** — **passes on the two modern political rupture modes**:

| Outcome | structure (V1+income) | + V3 | increment | verdict |
|---|---|---|---|---|
| **Democratic backsliding** | 0.54 (≈chance) | **0.61** | **+0.06** | **PASS** |
| **Repression worsening** | 0.64 | **0.71** | **+0.07** | **PASS** |
| Armed-conflict onset | 0.72 | 0.74 | +0.02 | fail (structure already gets it) |

Both survive removing event-history ⇒ genuine grievance/mobilization, not the conflict-trap.
The FDR-surviving backsliding predictors are **anocracy + civil-society mobilization**;
structure (P1) does not survive. Armed conflict — the *ancient*, poverty-driven mode — is
already structure-predictable; V3 owns the *modern* mode.

**Deep validation (1816–1996, `deep_political.py`):** the V3 numerator beats structure at
backsliding across the entire 20th century (mean incremental AUC **+0.131**, 11 epochs),
largest where structure fails most (modern). The conflict-trap (+0.21..+0.67) and
rule-of-law→less-conflict (−0.06..−0.49) hold across 200 years; ethnic exclusion→conflict is
robust post-1946 (+0.20..+0.39). **The drivers evolved:** anocracy→backsliding flipped from
≈0/negative (pre-1956) to **+0.22** (modern) — the "contested middle" as the erosion zone is
a late-20th-century configuration.

## Honest bounds (load-bearing)

- **Calibrated risk, not forecast.** The lift is real but modest (0.61/0.71). V3 raises the
  floor from chance to *risk over bands*, it does **not** make coups datable. The **trigger
  (the "Mule") stays unmeasured** and caps the achievable AUC — this is physics, not a data
  gap (Tunisia had the configuration for years; Bouazizi's spark is in no dataset).
- Some inputs are expert-coded (V-Dem/PTS) → V3 is less "revealed-outcome-pure" than V2.
- Validated on modern out-of-fold CV + a deep in-sample panel; a second forward window and a
  populist-vote outcome (V-Party) would strengthen it further.

## Invariants (do not break)
1. **V1 and V2 are frozen.** V3 is additive; it changes no V1/V2 score.
2. V3 is a **pressure/risk** instrument — it predicts *directional risk over horizons*, never
   timing (Mod8 discipline inherited from V1). Report as risk, not forecast.
3. Preserve the honest ceiling: the trigger is unmeasured by design.
