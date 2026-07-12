# Modernization Index V2 — Functional Conversion (Level + Equity) — Pre-Registration

**A new instrument, not a modification of V1.** V1 (frozen) measures *state* — the levels
and balance of a country's structural configuration. V2 measures *function* — how
effectively a state **converts capacity into citizen outcomes**, and **for whom**. Every
V2 Level indicator is an output/input ratio (revealed-outcome, near-zero perception). Every
pillar also carries an **Equity** dimension (how evenly the conversion is distributed).
V2 starts with **zero validation credit** and must earn its own; it does **not** inherit
V1's 109-case historical corpus and makes **no** pre-modern claims.

Frozen before any hypothesis is run. sha256 on commit.

---

## Binding rules (from the spec)

1. **Freeze V1.** V2 is separate; no V1 changes from V2 findings.
2. **Equal weights first.** Do not tune weights to maximize prediction.
3. **Pre-register all hypotheses before testing** (this file).
4. **Report all results including nulls** (cross-model failure, gap non-prediction, etc.).
5. **Do not claim V2 is validated by V1's corpus.**
6. **Report coverage honestly; do not fill gaps with bad proxies.** Where an equity
   dimension has no real data, it is flagged unavailable, not fabricated.
7. **Run Hypothesis 4 (construct validity) FIRST** as a gate; if it fails, stop and
   diagnose before any predictive test.
8. Equity measures distributional **outcomes**, not policies; do **not** assume equity is
   always good (test it); the incarceration indicator is an **outcome** measure, no causal
   claim.

---

## Data actually held (coverage audit, WB WDI + WB wealth-quintile + OWID, fetched 2026-07-12)

`data/v2/v2_indicators.json`. IMF WEO / WID / OECD-SDMX are **blocked from this environment**
(403); their intended indicators are substituted from WDI where possible or flagged as gaps.

**LEVEL (Track-1 for all six pillars):**
- **F1 Fiscal:** cash surplus/deficit %GDP `GC.NLD.TOTL.GD.ZS` (175); interest %revenue
  `GC.XPN.INTP.RV.ZS` (188); central-govt debt %GDP `GC.DOD.TOTL.GD.ZS` (84, trajectory).
  *(IMF WEO primary-balance/gross-debt blocked → WDI fiscal used; debt coverage is the
  weak indicator.)*
- **F2 Human Development:** life expectancy (260), health exp pc PPP (236), infant
  mortality (239), HCI learning-adjusted years (172), adult literacy (173), education exp
  per primary student (186), **PISA math** (87, OWID — finer top discrimination).
- **F3 Infrastructure:** power T&D losses (192), safely-managed water (175), LPI infra
  sub-index (211, **perception-flagged — the one perception indicator in V2**), broadband
  /100 (251), mobile /100 (253).
- **F4 Security:** homicide /100k (229); **incarceration rate** (219, OWID prison brief).
  *(COFOG public-order spending + court efficiency blocked → homicide un-ratioed +
  incarceration; F4 Level is degraded, flagged.)*
- **F5 Environment:** CO2 per GDP `EN.GHG.CO2.RT.GDP.PP.KD` (234), PM2.5 (243), forest %
  (257, trajectory), renewable share (255, trajectory).
- **F6 Social Contract:** out-of-pocket health % of health exp (236), social-protection
  coverage `per_allsp.cov_pop_tot` (128). *(Housing = OECD-only, omitted.)*

**EQUITY (real where noted; flagged where proxy/unavailable):**
- **Income distribution (universal cross-cutting anchor):** Gini (165), income share
  lowest-20% / top-20% (165). Used as the F1 and F6 equity proxy and a cross-check.
- **F2 Health equity (REAL, developing ~100–111):** WB wealth-quintile — measles
  immunization Q1/Q5 (104), skilled birth attendance Q1/Q5 (111), stunting Q1/Q5 (98),
  antenatal care Q1/Q5 (110). Equity = poorest(Q1)/richest(Q5) ratio (stunting inverted).
- **F3 Infrastructure equity (REAL, broad):** urban-rural gaps — electricity access
  R/U (256), clean fuels R/U (232), safely-managed water R/U (110–129). Equity = rural/urban.
- **F5 Environment equity (PARTIAL):** clean-fuel urban-rural gap. PM2.5-by-SES unavailable.
- **F1 / F4 / F6 equity:** no pillar-specific distributional data reachable (tax
  progressivity/CEQ, subnational homicide dispersion, OOP-by-quintile all blocked/absent)
  → these pillars use the **income-distribution anchor** as their equity dimension, or run
  Level-only where even that is missing. **Flagged as proxy, not pillar-specific.**
- **Developed-country health/education equity** (PISA-SES-gap, OECD health-by-income) is
  the documented **frontier gap**; developed countries' equity leans on income-Gini +
  urban-rural (which ceiling near 1), so equity *discrimination at the very top is limited*
  — flagged, not hidden.

---

## Construction (fixed)

- **Ratios (Level):** output/input. Diminishing-returns inputs (health/education spend)
  entered as **log(input)** per spec; ratios **capped at the 95th percentile** of the
  cross-sectional distribution each year to stop outliers dominating. Direction-corrected
  so higher = better conversion.
- **Trajectories:** debt (5-yr change, inverted), forest (5-yr change), renewable (5-yr change).
- **Normalization:** each indicator → 0–100 by **min-max anchored to the 5th/95th
  percentiles** of the global cross-section at the latest year (below 5th → 0, above 95th → 100).
- **Equity indicator:** ratio disadvantaged/advantaged (or rural/urban, Q1/Q5), → 0–100
  (100 = parity). Then percentile-normalized like Level.
- **Pillar Level (L)** = equal-weight mean of available normalized Level indicators.
  **Pillar Equity (E)** = equal-weight mean of available normalized Equity indicators.
- **Pillar Score** = **geometric mean of L and E** for F2–F6; **0.70·L + 0.30·E** for F1
  (fiscal is primarily collective) — this 70/30 is pre-registered and sensitivity-tested.
- **Overall:** **V2-Level** = mean of the six pillar L; **V2-Equity** = mean of the six
  pillar E; **V2-Combined** = geometric mean of V2-Level and V2-Equity. All three reported.
- **Tracks:** T1 = all six pillars from primary indicators; T2 = ≥1 pillar degraded; T3 =
  ≤3 pillars computable (pillar scores only, no overall). Every country-year flagged.
- **Weighting schemes (H4):** V2a equal; V2b correlation-derived; V2c analyst-assigned
  (F1 0.22, F2 0.22, F6 0.18, F3 0.16, F4 0.12, F5 0.10 — fiscal + human-dev + social
  contract weighted up as most durability-relevant). Computed for Level, Equity, Combined.

## Outcome for predictive tests

Domestic political stress = the committed **dysfunction outcome** (Finding 9-B2 / F12
composite: Polity2 −≥3 / GDP-pc −≥15% / UCDP onset / FSI +≥10) and the committed
domestic-onset set, forward window, as used in Findings 12/14/15.

---

## Pre-registered hypotheses

- **H4 (GATE — run FIRST).** Cross-model validation ρ ≥ 0.95 (pairwise Spearman across
  V2a/b/c), **separately for Level, Equity, Combined**. ρ ≥ 0.95 ⇒ single construct.
  0.90–0.95 ⇒ coherent-but-noisy. **< 0.90 ⇒ STOP** — the dimension is a profile of
  semi-independent facets, not a composite; diagnose before proceeding.
- **H1.** V2 pillar **balance** predicts domestic stress beyond level: regress stress on
  (a) V2-Combined, (b) Combined spread (SD of pillar scores), (c) both, (d) full
  decomposition (V2-Level + V2-Equity + Level-spread + Equity-spread). Spread adds power?
- **H2.** F1 (fiscal) deterioration while F2–F6 hold predicts subsequent conversion
  collapse (the fiscal durability gate): countries with F1 down ≥1 SD while mean(F2–F6)
  stable/improving → do they show F2–F6 decline within the window? Test honestly (Japan
  counter-case).
- **H3.** The **V1−V2 gap** predicts domestic stress, decomposed into V1−V2-Level and
  **V1−V2-Equity**; expected: the equity gap (looks-governed but delivers-unequally) is
  the stronger predictor.
- **H5.** **V2-Equity adds predictive power beyond V1 AND V2-Level** (AUC gain ≥ 0.05 for
  V1+V2-Level+V2-Equity over V1+V2-Level).
- **H6 (the headline).** The **HL-LE** configuration (high Level, low Equity) predicts
  domestic stress **better than low Level alone** — HL-LE countries show *more* stress than
  LL-HE despite higher average outcomes. (Unequal delivery from a capable system is more
  destabilizing than equal delivery from an incapable one.)

## Interpretation gates (frozen)

- H4 ≥ 0.95 on all three ⇒ V2 is a real construct; proceed. Equity < 0.90 while
  Level/Combined pass ⇒ **V2-Equity is a profile, not a composite** — report as such.
- H6 confirmed ⇒ the instrument's central claim (equity gap drives instability that V1
  can't fully explain) holds; the US as HL-LE is the showcase. H6 null ⇒ report honestly:
  average level, not distribution, is what predicts.
- Every pillar/dimension reports its **coverage track**; conclusions restricted to the
  countries with real (non-proxy) equity data are stated separately from proxy-equity ones.
