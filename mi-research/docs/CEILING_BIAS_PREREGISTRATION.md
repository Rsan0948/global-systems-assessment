# WGI Ceiling-Bias — Pre-Registration

**Purpose.** Test whether **WGI perception-based P1 systematically overstates
institutional *decline* for high-P1 (top-of-distribution) countries** relative to
revealed-outcome functional indicators. Hypothesis: near the ceiling, expectations are
so high that any salient governance failure produces a disproportionate *perception*
drop, even when *functional* performance is unchanged — so the top-tier declines in the
divergence scan (Netherlands −2.0, New Zealand −2.8, and the Nordics) may overstate real
functional deterioration.

**Distinct from Finding 9-C.** 9-C showed WGI *out-predicts* revealed outcomes
**cross-sectionally** (perceptions rank countries better at a moment). This asks a
**longitudinal** question: do perceptions and revealed outcomes **diverge over time
specifically at the top**? Cross-sectional superiority and longitudinal ceiling-bias are
not contradictory.

**This bears directly on my own prior work:** the divergence scan (`divergence_scan_full.json`)
flagged the US, Netherlands, UK, mature democracies as declining on WGI-P1. If ceiling
bias is real, some of that is an instrument artifact. Either result is a publishable
finding about WGI; **report whichever way it comes out.**

---

## Binding rules

1. **Pre-register before running** (sha256 on commit).
2. **Primary revealed proxy is pre-committed to TAX REVENUE %GDP** (broadest coverage).
   Education expenditure and LPI are robustness checks. **Do not** pick the proxy or the
   normalization that yields the desired result.
3. **Report the Netherlands regardless of direction.** If NL's functional decline matches
   its perception decline, say so.
4. Salient-events annotation (Step 5) is **interpretive context, not a causal test** — I
   document temporal coincidence only, never claim an event "caused" the perception drop.
5. **Revealed outcomes are not ground truth** either (tax %GDP moves with policy/rate
   changes; LPI with investment cycles). Both WGI and revealed are imperfect proxies for
   the same latent construct. Framed accordingly.
6. Diagnosis only — no engine changes proposed from the result itself.

---

## Data (fixed)

- **WGI P1** = mean of GovEff / RuleLaw / RegQual / CtrlCorr (0–100 percentile),
  `mi-pipeline/data/wb_cached.csv`, 1996–2024.
- **Revealed outcomes** (`data/robustness/convergence/revealed_outcomes.json`, fetched
  from WB API v2 2026-07-12): **tax_rev_pct_gdp** `GC.TAX.TOTL.GD.ZS` (primary, 194
  countries), **gov_edu_exp_pct_gdp** `SE.XPD.TOTL.GD.ZS` (robustness, 245),
  **lpi_overall** `LP.LPI.OVRL.XQ` (robustness, 212, biennial 2007–2022; usable from the
  2012 time point). **Ease-of-Doing-Business `IC.BUS.DFRN.XQ` is unavailable** — retired
  from the WB API ("deleted or archived") — documented gap, not substituted.
- Time points: 1996 / 2004 / 2012 / 2018 / 2024, nearest available within ±3 years.
- Universe for percentile ranking = real countries in `wb_cached.csv` (WB aggregates
  excluded).

## Construction (fixed)

- **Groups by 1996 WGI-P1:** rank all countries with 1996 P1; **Top-20** (ranks 1–20),
  **Middle** (ranks 41–60), **Bottom-20** (lowest 20). Ties broken by ISO alphabetical.
- **Common scale:** each revealed indicator is **cross-sectionally percentile-ranked
  (0–100) within real countries each year**, matching WGI's own percentile construction,
  so ΔWGI and Δrevealed are both in *percentile points*. Primary revealed-P1 = **tax
  percentile**; robustness revealed-P1 = mean of available {tax, edu, lpi} percentiles.
- **Trajectory:** Δ from the 1996 baseline at each time point, for WGI-P1 and revealed-P1.
- **Perception gap (per country)** = **ΔWGI − Δrevealed** over 1996→2024. Negative gap =
  perception fell more than function ⇒ perception overstates decline. (Matches the task's
  definition: WGI −2.0 vs revealed −0.5 → gap −1.5.)

## Tests

- **Step 4 (GATE) — ceiling bias.** Mann-Whitney U (one-sided: Top-20 gap **more
  negative** than Middle) on per-country perception gaps, + Welch t-test + **Cliff's
  delta** effect size. **Confirmed** if Top-20 gap is significantly more negative than
  Middle (p < 0.05) with non-trivial effect. **Not confirmed** otherwise.
- **Step 5 — country profiles.** NL, Denmark, New Zealand, Finland, Norway, Switzerland
  (+ any top-10): WGI vs revealed trajectory + gap per time point; NL annotated with
  salient events (toeslagenaffaire ~2019-20, housing ~2015+, nitrogen 2019+, COVID
  2020-22, immigration, Groningen) as temporal context only, plus **absolute raw tax +
  education change** (the "is it functionally declining at all" check).
- **Step 6 — impact on MI longitudinal findings.** (a) recompute the mature-state erosion
  decomposition with revealed-P1; (b) recompute the divergence scan with revealed-P1 —
  how many of the qualifiers survive, and do NL/UK/FR/DE drop off.
- **Step 7 — floor effect.** Bottom-20 perception gap. If revealed decline **exceeds**
  perception decline at the bottom (positive-ish gap there vs negative at top), WGI
  **compresses** the true range — overstating decline at the top, understating at the
  bottom.

## Interpretation gates (frozen)

- **Ceiling bias confirmed (Step 4):** WGI overstates decline at the top. Recommend
  revealed-outcome P1 for *longitudinal* trajectory (retain WGI for cross-sectional
  ranking) or a ceiling correction. The Netherlands' (and peers') structural assessment
  improves toward "functionally stable, perceptually declining."
- **Not confirmed:** top-tier WGI decline is real/functional, not just perceptual; the
  divergence-scan mature-democracy declines stand.
- **Floor effect (Step 7)** reported independently as an instrument-compression finding.
