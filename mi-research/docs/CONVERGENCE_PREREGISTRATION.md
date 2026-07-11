# Convergence Confirmation — Pre-Registration

**Purpose.** Finding 14 recharacterized the 150-year "erosion of the institutional
signal" as **wealth catching up**: on the Finding-12 domestic-crisis channel,
`struct_auc` (institutions→domestic crisis) rose 0.444→0.754 (Δ+0.31, p=0.20, n.s.)
while `wealth_auc` (log GDP→domestic crisis) rose **faster**, 0.222→0.779 (Δ+0.557,
p=0.005 — the only significantly-trending component). Institutions did not lose
predictive power; GDP *gained* it, narrowing the spread. Finding 14 flagged this as a
**lead, not a closed finding**, because it emerged from a pre-registered decomposition
rather than a hypothesis with its own falsification gate.

**This program promotes-or-refutes that lead with confirmatory evidence.** The specific
claim under test:

> GDP became a progressively better predictor of domestic political crises over 150
> years because GDP evolved from measuring agricultural output (unrelated to state
> capacity) to measuring industrial-financial-service output (deeply reflective of
> state capacity). The institutional signal did not weaken. A second variable
> independently learned to predict the same outcome because it began measuring the
> same underlying construct — state capacity — from the output side.

This is **not** a residual hypothesis emerging from a failed test. It is a directional
mechanism with five independent observable implications (Tests 1–5) plus a robustness
replication (Test 6). Part 2 (Tests 7–9) asks whether the confirmed convergence is
**structurally durable or at risk of reversal**.

---

## Binding rules

1. **Pre-register Part 1 before running** (this file, sha256 on commit). Part 2 is
   analytical; its methodology (Tests 7–8) is documented here before running, Test 9 is
   an explicitly non-statistical structured assessment.
2. **Tests 1 and 2 are the Part 1 gate.** If GDP–institution correlation is NOT rising
   historically (on a like-for-like sample) AND sector composition did not shift, the
   convergence interpretation fails — **stop Part 1**.
3. **Test 3 is the mechanism test.** If GDP retains full independent predictive power
   after controlling for P1, the proxy interpretation is wrong even if the convergence
   is real. Report honestly — it would mean GDP and institutions converge as predictors
   while measuring partially different constructs.
4. **Report all results,** including partial confirmations, wrong-sign results, and
   power limits. Small/low-data samples (Test 5 agricultural economies; deep-historical
   sector data) are flagged, not hidden.
5. **Report all of Part 1 before beginning Part 2 interpretation** — Part 2's reading
   depends on whether the convergence is confirmed.
6. Diagnosis only — **no MI modifications** proposed from these results.
7. Standing repo rule: *"if it only works with tuned parameters it is probably not
   real."* No threshold is tuned to produce a confirmation; all thresholds are fixed
   below.

---

## Data (fixed — same sources as Findings 1–14, no new provenance)

- **Historical institutional proxy = V-Dem rule-of-law** (`rol`, `vdem_longrun.json`).
  This is the exact structure predictor of Findings 2/7/9/12/14.
- **Historical wealth = log Maddison GDP per capita** (`P4_gdp` in
  `longrun_pillars.json`), as in every erosion finding. Wealth score in AUC = `−log GDP`
  so that higher score → higher predicted crisis (matches committed convention).
- **Modern institutional quality = engine P1** on the MI 5-point panel
  (`decoupling/mi_5pt_panel.json`, years 1996/2004/2012/2018/2024).
- **Modern wealth = log10 GDP-pc PPP** (same panel).
- **Domestic crisis outcome = the committed Finding-12 domestic-origin onset set**
  (`contagion/crisis_classification.json`, `classification_primary`, tag `domestic`),
  25-year forward window, exactly as Finding 14 used.
- **Sector composition / financial / FDI = WDI** (`decoupling/wdi_decoupling.json`:
  `agriculture_pct_gdp`, `industry_pct_gdp`, `services_pct_gdp`, `manufacturing_pct_gdp`,
  `private_credit_pct_gdp`, `stockmkt_cap_pct_gdp`, `fdi_net_inflow_pct_gdp`), 1970–2024.
- **Resource rents = `resource_rents_pct_gdp`** (canonical panel).
- **Dysfunction outcome (Test 6) = the committed Finding-9-B2 / Finding-12 composite**:
  ANY of Polity2 decline ≥3 from peak / GDP-pc decline ≥15% from peak / UCDP onset /
  FSI increase ≥10, over the same forward window.
- **Formation groups = `formation/state_formation.json`** (mature / post_colonial /
  early_post_colonial), reused for the Test 4 industrialization proxy.

**AUC convention (frozen, identical to `varcomp_A.struct_vs_wealth_decomp`).**
`struct_auc = auc_roc(−rol, label)`; `wealth_auc = auc_roc(−logGDP, label)`. Mann-Whitney
AUC. Epoch grid 1816→1996 step 10; minimum 12 observations and both label classes present
per epoch or the epoch is dropped (same filter as the committed curve).

---

## PART 1 — Confirmatory tests

### Test 1 — GDP's correlation with institutional quality has been rising over time  *(GATE)*

**Spec.** At each epoch on the historical grid (and the 5 modern MI points), compute
Pearson and Spearman correlation between institutional quality (rol / P1) and log GDP
per capita. Report on THREE samples to separate the real trajectory from the known
decolonization composition artifact (Finding 10-T1):
(a) **pooled** all-available countries per epoch; (b) **constant** balanced set present
at all epochs; (c) **mature-only**. Compute correlation at the Finding-14 decomposition
epochs (1816, 1876, 1946, 1996) and correlate the coupling trajectory against the
`wealth_auc` trajectory from the committed `t2_split_curve` domestic curve.

**Predicted direction.** Rising institutional–GDP correlation across the historical span
on the **constant** and **mature-only** samples (the pooled sample may be depressed
1940→1970 by decolonization — Finding 10 already showed this, and it is expected, not
disconfirming). The coupling trajectory should positively track `wealth_auc`.

**Confirmation.** Constant-sample and/or mature-sample Δr > 0 across the span AND a
positive correlation (Pearson) between the epoch coupling series and the epoch
`wealth_auc` series.
**Disconfirmation.** Coupling already high in 1816/1850 with no subsequent rise on any
like-for-like sample, OR coupling trajectory uncorrelated / negatively correlated with
`wealth_auc`. (Pooled-only decline with rising constant-sample coupling is **not**
disconfirmation — it is the Finding-10 composition artifact.)

### Test 2 — GDP composition shifted from institution-independent to institution-dependent sectors  *(GATE)*

**Spec.**
- **Longitudinal:** global (and major-economy) mean agriculture / industry / services
  share of GDP per decade, WDI 1970–2024. Deep-historical trajectory (agriculture
  ~60–70% mid-19thc → ~4% today) is cited as documented economic-history context, NOT
  recomputed from committed data — flagged as context, not measurement.
- **Overlay:** align the agriculture-share decline against the `wealth_auc` rise.
- **Cross-sectional (the discriminating version):** at each modern MI point, split
  countries by agriculture share and test whether GDP's crisis-predictive power (AUC
  over domestic crises) is WEAKER in high-agriculture economies than low-agriculture
  economies.

**Predicted direction.** Agriculture share declines monotonically; industry+services
absorb it. GDP-crisis predictive power is weaker where agriculture share is higher.

**Confirmation.** Monotone (or near-monotone) agriculture decline over the WDI window
AND lower `wealth_auc`/GDP-AUC in high-agriculture than low-agriculture economies.
**Disconfirmation.** Flat sector composition, OR GDP predicts crises equally well
regardless of agriculture share.

### Test 3 — GDP predicts domestic crises THROUGH institutional quality, not independently  *(MECHANISM)*

**Spec.** At 2004 and 2012 (temporal holdout) and at each historical epoch where both
variables exist, fit three logistic regressions on domestic-crisis label:
Model 1 = P1 only; Model 2 = GDP only; Model 3 = P1 + GDP (predictors z-standardized,
same ridge L2=1e-3 as `esi_tests.logit_fit`). Report coefficients, significance
(via coefficient magnitude relative to its bootstrap SE), and AUC of each model. Track
GDP's Model-3 coefficient over epochs.

**Predicted direction (proxy interpretation).** In Model 3 the GDP coefficient shrinks
(toward non-significance) once P1 is controlled; Model-3 AUC barely exceeds Model 1
alone; GDP's independent Model-3 contribution does NOT grow over time (it shrinks or
stays near zero as GDP's signal becomes increasingly explained by its correlation with
P1).

**Reading (pre-committed, three outcomes).**
- GDP coefficient → n.s. under P1 control ⇒ **pure proxy** (strongest confirmation).
- P1 remains significant under GDP control, GDP also remains ⇒ **complementary facets**
  of the same construct (convergence real, "measures identical thing" too strong).
- GDP's independent contribution GREW over time even net of P1 ⇒ proxy interpretation
  **incomplete**; GDP captures something real P1 misses. Report honestly.

### Test 4 — The convergence follows the diffusion pattern of industrialization  *(DIFFUSION)*

**Spec.** Classify countries into early / mid / late industrializers (fixed lists
below — frozen before running). Compute `wealth_auc` separately per group per epoch on
the historical curve.

- **early** (industrialized by ~1870): GBR, FRA, DEU, USA, BEL, NLD, CHE, AUT.
- **mid** (by ~1920): JPN, RUS, ITA, SWE, NOR, DNK, ESP, CAN, AUS, CZE (Czech lands).
- **late** (post-1960): everything else in the panel (East Asia post-1960, most
  developing states).

**Predicted direction.** `wealth_auc` rises earliest in early industrializers, latest in
late industrializers.
**Confirmation.** Early-industrializer `wealth_auc` reaches high values earlier (earlier
epoch) than late industrializers.
**Disconfirmation.** `wealth_auc` rises simultaneously across all groups (convergence
global, not industrialization-timed). **Power caveat pre-committed:** early/mid groups
are small (n≈8–10 states); per-epoch AUCs will be noisy; report directional pattern with
the small-n caveat, do not over-claim significance.

### Test 5 — Agricultural economies still show the pre-convergence pattern  *(CROSS-SECTIONAL DISCRIMINATOR)*

**Spec.** In the modern panel, identify countries with agriculture > 25% of GDP (WDI).
For these, compute P1's and GDP's predictive power (AUC + point-biserial) over domestic
crises and the P1−GDP spread. Compare to the spread among industrialized/service
economies (agriculture < 10%) in the same period.

**Predicted direction.** Positive spread (institutions out-predict GDP) among
agricultural economies — resembling the 1816/1876 pattern; near-zero or negative spread
among industrial economies (convergence reached).
**Confirmation.** Spread(agricultural) > Spread(industrial), same period.
**Disconfirmation.** Spread equal or reversed.
**Power caveat pre-committed:** the agricultural-economy sample is small and concentrated
in low-data-quality regions; if the result is directionally consistent but not
significant, report the direction WITH the power caveat.

### Test 6 — Restate Finding 14 on an independent outcome variable  *(ROBUSTNESS)*

**Spec.** Recompute the `struct_auc` / `wealth_auc` decomposition using the composite
**dysfunction** outcome (Finding-9-B2 / Finding-12) instead of conflict onset, at each
epoch where the dysfunction components exist. Modern segment (Polity2 / GDP-decline /
UCDP / FSI) is fully available; deep-historical dysfunction is limited to Polity2-decline
+ GDP-decline + UCDP where those exist — flagged, not forced.

**Predicted direction.** Same pattern — `struct_auc` rising, `wealth_auc` rising
faster/further, spread narrowing.
**Confirmation.** Same qualitative pattern on the independent outcome.
**Disconfirmation.** Different pattern ⇒ the convergence is outcome-specific (holds for
conflict, not broad dysfunction). Still informative; narrows the claim.

---

## PART 2 — Durability assessment (methodology documented before running)

### Test 7 — Is the GDP–institutions coupling stable or fragile?

**Method.** In the MI panel (1996→2024), identify countries where **GDP-pc grew > 50%
while P1 moved < 0.05 or declined** — the decoupled set where wealth stopped tracking
institutions. Count them; characterize by region / income / economic type. For the
decoupled set, test whether they experienced domestic crises at higher rates than their
GDP alone would predict (residual from a GDP-only crisis model). **Durability reading:**
a handful of resource/authoritarian outliers ⇒ robust; a large and/or growing decoupled
set ⇒ historically contingent.

### Test 8 — What could decouple GDP from state capacity going forward?

**Method.** For each candidate decoupling force, test whether the P1↔GDP correlation is
weaker among exposed countries than non-exposed, and count exposed countries + trend:
(a) **resource rents** > 10% GDP; (b) **FDI** net inflows > 5% GDP; (c)
**financialization** (private credit / stock-mkt cap top tercile); (d) **digital/ICT**
(ICT service exports share where available; if unavailable, documented as a gap and
proxied best-effort). Synthesis: if multiple forces weaken the coupling and exposure is
growing, the convergence is contingent, not permanent.

### Test 9 — The AI-specific question (STRUCTURED ASSESSMENT, NOT A TEST)

Explicitly non-statistical. Enumerate the channels through which GDP currently requires
institutional quality (labor→P3, production→P1 infrastructure, trade/finance/services→P1
enforcement). For each, assess whether AI reduces the institutional dependency. Document
as a **forward-looking structural risk**, framed as: the convergence depends on GDP
requiring institutional quality; AI is a potential force that could weaken that
requirement; if it does, GDP stops being a reliable state-capacity proxy, the
convergence reverses, and the institutional signal regains its relative advantage — not
because institutions strengthened, but because GDP got noisier. Not presented as a
finding.

---

## Interpretation gates (frozen)

- **Tests 1–5 all confirm** ⇒ convergence validated from five independent angles;
  Finding 14 promoted from lead to confirmed finding; "erosion" definitively
  recharacterized as wealth catching up.
- **Tests 1–2 confirm, Test 3 shows GDP retains independent power** ⇒ convergence real
  but interpretation shifts to "GDP measures a complementary facet," not "the same
  thing."
- **Tests 1–2 fail** ⇒ Finding 14's decomposition was a data-configuration artifact;
  convergence interpretation does not hold.
- **Part 2:** Test 7 few outliers ⇒ structurally robust. Test 8 multiple active forces
  with growing exposure ⇒ historically contingent, reversible within a generation. Test
  9 frames forward risk without claiming to predict it.
