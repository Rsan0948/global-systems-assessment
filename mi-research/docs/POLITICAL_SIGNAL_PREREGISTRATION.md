# Political-Signal Test — Pre-Registration

**The question.** The exploratory screen showed V1/V2 (state-capacity *levels*) predict
societal/wellbeing outcomes but **nothing political** net of income. The design report argued
we measure the **capacity denominator** of the founding equation (rupture = complexity >
capacity) but never the **complexity numerator** — organized grievance, mobilization,
group exclusion, repression, expectation-shock. **This test builds the numerator layer from
real data and asks whether it captures the political signal the structural instruments miss —
and, critically, whether it adds *incrementally* over the structural predictors.**

Frozen before analysis. sha256 on commit.

## Binding rules
1. Pre-register before running.
2. **The gate is INCREMENT, not raw prediction.** Numerator predictors correlating with
   political outcomes is not enough (they may just proxy development). The test is whether a
   **numerator block adds AUC over a structural block (P1 + log GDP)** in a joint model.
3. **BH-FDR across the full screen; every survivor re-tested controlling P1 + log GDP.**
4. **Report all nulls.** If the numerator layer also fails, that is the finding — political
   rupture may be beyond structural *and* grievance measurement (trigger-dominated = the Mule).
5. Forward-ish design: predictors at a **~2010 base**, outcomes over **2010/2012 → 2024**, to
   avoid using the future to predict the past. V2 has no time series → excluded from the
   forward test (structural control = engine P1 + log GDP at the base).

## Data (staged, `data/political/political_indicators.json` + committed sources)
**Numerator / dynamic predictors (base ~2010):**
- **Ethnic exclusion** — EPR-ETH (`icr.ethz.ch`): country share of population in
  POWERLESS/DISCRIMINATED/SELF-EXCLUDED ethnic groups; discriminated share; #excluded groups.
  Re-aggregated at the base year.
- **Mobilization capacity** — V-Dem Civil Society Participation index (OWID); internet users %.
- **Repression** — Political Terror Scale (level + 10-yr change).
- **Anocracy (opportunity)** — V-Dem liberal-democracy, entered **nonlinearly**
  (inverted-U: `4·libdem·(1−libdem)`, max at mid-regime) — the PITF/Goldstone finding.
- **Event-history** — prior domestic conflict onset (committed UCDP/COW, in the decade
  *before* the base) as a predictor.
- **Expectation-shock** — GDP-pc growth volatility + deceleration in the pre-base decade (WDI).
- **Youth bulge** — population 0–14 % (WDI).
- **Food-import dependence** — food imports % merchandise imports (WDI).

**Structural control block:** engine **P1** + **log GDP-pc** at the base.

**Political outcomes (base → 2024):**
- **Democratic backsliding** — Δ V-Dem liberal-democracy (decline ≥ 0.05 = 1).
- **Domestic conflict onset** — committed UCDP/COW domestic onset in the outcome window (binary).
- **Repression worsening** — Δ PTS ≥ +1 over the window (binary).

## Tests
- **T1 — screen.** Spearman of every predictor × every political outcome; BH-FDR; survivors
  re-tested partialling out **P1 + log GDP**.
- **T2 (GATE) — incremental value.** For each outcome, logistic AUC of: (a) structural
  block [P1 + logGDP]; (b) + numerator block [EPR + CSO + PTS + anocracy + event-history +
  youth + food + shock]. **Gate = numerator block adds AUC ≥ 0.05 over structural, on ≥1
  political outcome, out-of-fold** (5-fold CV AUC to avoid overfitting the block).
- **T3 — which numerator terms carry it** (multivariate coefficients, net of P1+logGDP).

## Interpretation gates (frozen)
- **T2 passes** ⇒ the numerator layer captures political signal the structural instruments
  miss; report which terms and build it into the program as the "complexity" tier.
- **T2 fails** ⇒ even grievance/mobilization/exclusion + event-history does not lift political
  prediction beyond structure+income; political rupture is trigger-dominated within reach of
  these instruments (the Mule ceiling is near). Either result is reported plainly.
- **Event-history caveat pre-committed:** if prior conflict is the *only* thing that adds,
  that is the well-known conflict-trap autocorrelation, not a new grievance finding — report
  it as such and test the numerator block *excluding* event-history separately.
