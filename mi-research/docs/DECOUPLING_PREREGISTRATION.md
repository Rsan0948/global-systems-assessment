# Wealth–Institution Decoupling — Pre-Registration

**Purpose.** Test whether the ~150-year erosion of the institutional signal
(Findings 2/7: structure-minus-wealth spread declines, Pearson **r = −0.847,
p = 0.033**) is explained by a **progressive structural decoupling of wealth from
institutional quality**, driven by three mechanisms operating across generations:
**(1) industrialization** (wealth generation with reduced dependence on domestic
institutions), **(2) financialization** (returns earnable independent of any
society's governance), and **(3) institutional reorientation** (institutions
retargeting from political-stability/public-welfare optimization toward
capital-facilitation).

This is structurally distinct from every prior robustness test. **Finding 8 (ESI)**
tested whether country-level external *capital flows* masked the signal — null.
**Finding 9 (A/B/C)** tested whether the *sample changed* (composition), the
*consequences changed* (state-death elimination), or the *measurement degraded*
(perception lag) — each ≈0%, residual ≈100%. This program tests whether the
**underlying wealth↔institution relationship genuinely weakened** because the
*mechanisms of wealth generation decoupled from institutional quality*.

**Mechanism is lagged, generational, systemic — NOT country-level immediate.** The
naive form ("country X industrialized → X's institutions weakened") is expected to
be null and is not the hypothesis. Early industrializers likely saw institutions
*strengthen* first (new wealth reinforced familiar institutional channels); the
decoupling accrues across generations as capital learns to operate with less
institutional dependency. **All tests measure the relationship *between variables*
changing *across the system over time*, never immediate within-country effects.**

---

## Binding rules

1. **Pre-register before running.** This document is committed **before** any test
   below is computed. sha256 recorded on commit.
2. **No tuning.** Equal weights, first pass. No optimization of weights, thresholds,
   or specifications to produce a result. Every threshold below is fixed here.
3. **Report all results, including nulls.** If a test is null, it is reported as
   null with magnitude and direction.
4. **Do not conflate the eight tests.** Each is independently positive or negative.
   Individual verdicts precede synthesis.
5. **Power honesty.** The modern trend tests have **N = 5 time points**. A trend in
   the predicted direction that is not significant at N=5 is reported as
   **directional (underpowered)** — NOT as a null. A null is claimed only when the
   effect is ≈0 or wrong-signed (below the materiality floor defined per test).
6. **Gate.** Tests 1 & 2 establish whether the *phenomenon* (decoupling) is real.
   Tests 3 & 4 identify the *channels*. Test 5 identifies the *institutional
   mechanism*. If Tests 1 **and** 2 are both null, the headline verdict is
   "decoupling hypothesis fails at the first gate"; Tests 3–5 are still reported for
   completeness but cannot rescue a failed phenomenon.
7. **Two-tailed, exact p-values, effect sizes.** BH-FDR noted across the test family
   in synthesis. Determinism: no randomness anywhere (no seeds needed).

---

## Data foundations (fixed here)

**F1 — MI five-point panel.** Time points **1996, 2004, 2012, 2018, 2024**. Pillars
computed by the committed engine `mi.scoring.calculate_pillar_scores` on
`data/sources/canonical_panel.json` via `mi.panel.indicators_for(iso, year)`. No
engine changes.
- **P1** (institutional quality) = mean of normalized gov_effectiveness,
  rule_of_law, regulatory_quality, corruption (CPI or WGI control-of-corruption).
  **Pure institutional; contains no GDP.**
- **P3** (human capital) = mean of education_index, life_expectancy_index (0–1).
- **P4** (economic structure) = mean of normalized gdp_per_capita_ppp,
  resource_rents, ODA. **Contains normalized GDP** — see Test 5B caveat.
- **Wealth** = `gdp_per_capita_ppp`; analyses use **log10(GDP-pc-PPP)**.
- **Primary universe = the balanced panel**: countries with non-null P1 and GDP at
  **all five** points (**N = 83**; 76 also have P3 & P4 at all five). **Sensitivity
  universe** = all-available-per-year (N ≈ 87/88/88/86/184). The balanced panel is
  primary so a trend is not an artifact of the 2024 jump from 88→184 countries.

**F2 — Historical panel (Test 1 deep extension).** V-Dem rule-of-law (`rol`,
`data/sources/vdem_longrun.json`) as the institutional proxy; log Maddison
GDP-pc (`P4_gdp`, `data/sources/longrun_pillars.json`) as wealth. Anchors
**1850, 1880, 1910, 1940, 1970** (matching the Finding-2 decay-curve anchors; the
brief's 1850/1900/1950 are a subset). Common-set per anchor (both series present).
These are rough proxies; the hypothesis predicts a **large** coupling change, so
rough proxies are informative. Institutional proxy here is V-Dem rule-of-law, a
subcomponent of P1 — a construct-continuity caveat noted in results.

**F3 — Temporal holdout (Tests 3, 4).** The committed `temporal_holdout_panel.json`
— windows **2004** and **2012**, ~89/90 countries, per-country **P1**, **P4**,
`crisis` (`ucdp_onset OR crag_default`, capital-coupled per Finding 3). The
**dysfunction** outcome (Finding 9 B2: ANY of Polity2 −≥3 / GDP-pc −≥15% from peak /
UCDP onset / FSI +≥10) is reconstructed with the committed
`erosion_component_B.py` spec and used as the **secondary, less capital-coupled**
outcome. Signal predictors are sign-standardized: **neg-P1** = (1 − P1) (low
institutional quality → crisis) and **neg-logGDP** = −log10(GDP) (low wealth →
crisis), so higher predictor = higher predicted risk; AUC is discrimination of the
crisis/dysfunction label.

**F4 — New indicators (World Bank WDI API v2, stdlib urllib, cached).** Fetched
read-only into `data/robustness/decoupling/wdi_decoupling.json`. WB *aggregate*
codes excluded. Exact codes fixed here:

| label | WB code | used in |
|---|---|---|
| agriculture % GDP | `NV.AGR.TOTL.ZS` | Test 3 |
| industry % GDP | `NV.IND.TOTL.ZS` | Test 3 |
| services % GDP | `NV.SRV.TOTL.ZS` | Test 3 |
| manufacturing % GDP | `NV.IND.MANF.ZS` | Test 3 |
| stock-mkt cap % GDP | `CM.MKT.LCAP.GD.ZS` | Tests 4, 5C |
| domestic credit to private sector % GDP | `FS.AST.PRVT.GD.ZS` | Tests 4, 5C |
| govt education exp % GDP | `SE.XPD.TOTL.GD.ZS` | Test 5C, 5D |
| public health exp % GDP | `SH.XPD.GHED.GD.ZS` | Test 5C, 5D |
| tax revenue % GDP | `GC.TAX.TOTL.GD.ZS` | Test 5C (context) |
| trade openness % GDP | `NE.TRD.GNFS.ZS` | Test 5C |
| FDI net inflows % GDP | `BX.KLT.DINV.WD.GD.ZS` | Test 5C |

`resource_rents_pct_gdp` (already in the canonical panel) is the extraction marker
for Test 3. **Social-protection spending** (Test 5C): attempt WB ASPIRE
`per_allsp.expend.gdp` best-effort; if unavailable, the people-orientation index
drops to the education+health mean and this is documented (no substitution with
synthetic data).

---

## Test 1 — P1–GDP coupling weakening over time

**Claim.** If wealth is progressively less dependent on institutions, the
cross-sectional P1↔wealth correlation declines over time.

**Spec.** At each of the 5 MI points (balanced panel), compute Pearson **r** and
Spearman **ρ** between P1 and log10(GDP-pc-PPP), plus **R²** (= r²; variance in log
GDP explained by P1). Fit an OLS linear trend of r vs year (N=5): report slope,
intercept, p. Repeat on the sensitivity universe. Historical extension (F2): same
Pearson/Spearman at anchors 1850/1880/1910/1940/1970.

**Nonlinearity check (fixed).** Also report r for the two halves (1996–2012 vs
2012–2024) and eyeball an early-flat/late-decline vs uniform-decline pattern. No
model selection — descriptive only.

**Expected if hypothesis true.** r and R² **decline** over time (modern and/or
historical). **Supported (significant):** trend slope < 0 with p < 0.05.
**Supported (directional, underpowered):** slope < 0, Δr = r(2024) − r(1996) ≤
−0.05 (materiality floor), p ≥ 0.05 at N=5. **Null:** |Δr| < 0.05 or slope ≥ 0
(coupling stable or strengthening).

---

## Test 2 — Institutional variance at income levels widening

**Claim.** In 1850 you could only be rich with good institutions → rich countries
cluster tightly at high P1. If decoupled, rich countries in 2024 show **wide** P1
variance (rich-with-strong vs rich-with-weak institutions).

**Spec.** At each point, split the balanced panel into GDP-pc-PPP **quartiles**.
For the **top** income quartile compute **SD** and **IQR** of P1. Plot dispersion
vs year; OLS trend slope. Repeat for the **bottom** quartile.

**Expected if hypothesis true.** Top-quartile P1 **dispersion widens** (SD slope >
0). **Supported:** SD slope > 0 with Δ(SD) = SD(2024) − SD(1996) ≥ +0.02
(materiality floor). **Null:** |Δ(SD)| < 0.02 or narrowing. **Asymmetry read
(fixed):** if bottom-quartile dispersion also widens → decoupling is
**bidirectional**; if only top widens → **asymmetric** (wealth decoupled, poverty
did not). Reported, not a pass/fail gate.

---

## Test 3 — Economic composition moderates the signal

**Claim.** The signal is stronger for institution-intensive economies, weaker for
institution-light ones (extraction, finance, tech, export-manufacturing).

**Operationalization (fixed; coarse-data caveat disclosed).** WB 3-sector data
cannot separate finance/tech from broad services, so the split uses the cleanly
institution-light components available:
- **institution-light share** = `resource_rents_pct_gdp` + `NV.IND.MANF.ZS`
  (extraction + export-manufacturing), at the window year (2004/2012), % GDP summed.
- Split the holdout into **Group L** (institution-light, above-median light share)
  vs **Group H** (institution-heavy, below-median light share).

**Test.** Run the institutional signal separately per group on the 2004 & 2012
holdout: **neg-P1 AUC**, **neg-logGDP (wealth) AUC**, and **neg-P1 minus wealth
AUC**, for the **crisis** outcome (primary) and **dysfunction** outcome (secondary).

**Expected if hypothesis true.** neg-P1 AUC and (neg-P1 − wealth) AUC are **higher
in Group H** (institution-heavy) than Group L. **Supported:** (neg-P1 − wealth) AUC
gap between H and L ≥ +0.05 in the hypothesized direction in ≥1 window. **Null:** no
material H−L difference (|Δ| < 0.05) or reversed. **Aggregate composition trend
(fixed, secondary):** report global mean institution-light share at 2004 vs 2012
(rising light share = shifting composition contributes to aggregate erosion).

---

## Test 4 — Financial depth moderates the signal

**Claim (financialization).** Deeper financial markets give capital more channels
to return independent of governance → financial depth **weakens** the institutional
signal.

**Financial-depth index (fixed).** mean of `CM.MKT.LCAP.GD.ZS` and
`FS.AST.PRVT.GD.ZS` at the window year, each min-max normalized to [0,1] across the
holdout sample, then averaged (equal weight). Missing one component → use the other;
missing both → dropped.

**Models (holdout, 2004 & 2012; crisis primary, dysfunction secondary).** Logistic
regression (IRLS, deterministic), predictors standardized:
- **M1:** crisis ~ neg-P1
- **M2:** crisis ~ neg-P1 + findepth
- **M3:** crisis ~ neg-P1 + findepth + (neg-P1 × findepth)

**Key = the M3 interaction coefficient.** Because neg-P1 is oriented so that higher
= more crisis risk, "institutions matter **less** where finance is deep" means the
neg-P1 slope **shrinks** as findepth rises → the interaction coefficient is
**negative**. **Supported (financialization):** interaction coefficient < 0 in ≥1
window (report p; N≈90 gives real but modest power). **Null:** interaction ≥ 0 or
≈0. Report full coefficients + AUCs for all three models.

**System-level (fixed, secondary).** Mean financial depth at 1996/2004/2012/2018/
2024 (balanced panel) plotted against the Finding-7 erosion; **diffusion test**
(signal weakening earlier in early-financializers) flagged **underpowered** with 5
points and reported descriptively only.

---

## Test 5 — Institutional reorientation from people to capital

**5A — P1↔P3 decoupling.** Pearson/Spearman P1 vs P3 at the 5 points (balanced
panel, 76-country P3 subset); OLS trend. **Expected:** **declining** (institutions
still functional but less people-oriented). **Supported:** slope < 0, Δr ≤ −0.05.
**Null:** |Δr| < 0.05 or rising.

**5B — P1↔P4 tightening.** Pearson/Spearman P1 vs P4 at the 5 points; OLS trend.
**Expected:** **rising** (institutions increasingly predict economic structure).
**CAVEAT (fixed):** P4 contains normalized GDP, so P1↔P4 partly re-expresses the
Test-1 P1↔GDP coupling. **Therefore also compute P1 vs P4\*** where **P4\*** =
mean of normalized resource_rents + ODA **only** (GDP removed), as the
GDP-decontaminated version. Interpret 5A and 5B **jointly**: the diagnostic
signature of reorientation is **5A falling while 5B (or the GDP-decontaminated
P1↔P4\*) rises**. **Supported:** 5B slope > 0, Δr ≥ +0.05. **Null:** |Δr| < 0.05.

**5C — Direct orientation.** Two indices (equal-weight, each component min-max
normalized [0,1] across the per-year sample, then averaged):
- **people-orientation** = mean(edu exp %GDP, public health exp %GDP, [social
  protection %GDP if available]).
- **capital-orientation** = mean(financial depth [Test 4 index], trade openness
  %GDP, FDI net inflows %GDP).

At each point (use the years with WDI coverage; health is ~2000+, so effective
points ≈ 2004/2012/2018/2024) compute corr(P1, people-index) and corr(P1,
capital-index). Plot both. **Expected:** P1↔capital **strengthening** while
P1↔people **weakening**. **Supported:** capital-corr slope > 0 AND people-corr slope
< 0 (both directional; Δ ≥ 0.05 either). **Null:** both stable. **V-Dem
(best-effort):** state-ownership `v2clstown` and market/welfare indices attempted
only if a compact V-Dem source is reachable offline; otherwise documented as not
run (the WDI indices are the primary 5C instrument).

**5D — Washington-Consensus (1979) inflection.** For available countries, compute
people-orientation spending (edu + public-health %GDP) and capital metrics
(financial depth, trade openness, FDI) at **1970/1980/1990/2000/2010/2020**; plot;
inspect for an inflection ~1979–1985. **Coverage limitation acknowledged up front:**
WB public-health series begins ~2000 and pre-1996 WDI coverage is sparse — 5D will
be **coverage-bounded**; report what exists rather than forcing a result.
Structural-adjustment subgroup (IMF/HIPC-conditionality countries vs never) is a
best-effort split using a fixed documented list; if the list or pre-1996 data is too
thin, 5D reports the limitation instead of a spurious inflection. **Supported:**
visible people-spending downshift / capital-metric upshift around 1979–1985.
**Null / underpowered:** no inflection or insufficient coverage (labeled).

---

## Synthesis (fixed structure)

After all eight tests, build the table (rows: T1, T2, T3, T4, 5A, 5B, 5C, 5D;
columns: what-it-measures / result / supports-hypothesis Y/N/partial). Verdict
logic (frozen):

- **T1 & T2 positive** → decoupling **phenomenon confirmed**.
- **T3 & T4 positive** → industrial & financial **channels confirmed**.
- **5A–5D positive** → institutional **reorientation confirmed**.
- **T1–T2 positive, T3–5 null** → decoupling real, **proposed mechanisms wrong**.
- **T1–T2 null** → decoupling hypothesis **fails at the gate**; erosion cause remains
  open (residual stays ≈100% per Finding 9).

Diagnosis only — **no framework changes** proposed from this session. All artifacts
under `data/robustness/decoupling/`; code under `scripts/robustness/decoupling_*.py`;
results narrative appended to `docs/ROBUSTNESS_RESULTS.md` as **Finding 10** and a
standalone `docs/DECOUPLING_RESULTS.md`.
