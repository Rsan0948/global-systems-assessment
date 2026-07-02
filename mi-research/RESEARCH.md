# RESEARCH.md — Standing Instructions for AI Research Agents

You are a research agent working on the Modernization Index (MI) framework. This document tells you what the framework is, what's been done, what needs doing, and how to do it.

## Your Mission

Continue testing, iterating, and improving the MI framework through:
1. Finding and running new case studies that stress-test underdeveloped areas
2. Testing proposed modifications against the existing baseline
3. Looking for patterns across the case study database that suggest new safeguards
4. Identifying where the framework is weakest and designing cases to probe those weaknesses
5. Documenting everything honestly

## The Golden Rule

**Any modification that improves performance on new cases but degrades it on existing cases is REJECTED.** The 20-case baseline is the floor. Improvements must be additive.

---

## What the Framework Is

The MI scores countries across five pillars measuring structural properties of governance:

| Pillar | Weight | What it measures |
|--------|--------|------------------|
| P1 — Institutional Quality | 34% | Government effectiveness, rule of law, regulatory quality, corruption control |
| P2 — Innovation & Knowledge Economy | 15% | R&D/GII, economic complexity |
| P3 — Human Capital | 16% | Education, life expectancy |
| P4 — Economic Structure & Independence | 20% | GDP per capita, resource rents (inverted), ODA (inverted) |
| P5 — Stability & Resilience | 16% | Political stability, fragile states index (inverted) |

The weights are correlation-derived from the data itself. P1 at 34% (up from initial 25%) reflects institutional quality being the most central variable (avg |r| = 0.79-0.80).

### Core Predictions

1. Pre-event P1 ordinally predicts post-stress outcomes (higher P1 = better trajectory)
2. Low P1 predicts violent rather than peaceful outcomes
3. Wide pillar spread predicts structural vulnerability
4. High resource dependence (P4) compounds institutional weakness
5. Framework is directional/ordinal only — no timing, no exact magnitudes
6. Underlying principle: complexity-capacity matching

### The Seven Safeguards

- **A — External Administration:** Flag WGI scores under international administration as potentially reflecting administrator capacity, not indigenous capacity.
- **B — Capacity Gate:** Low fragment count (2-4) coded as "manageable" ONLY when P1 exceeds bottom third of Rule of Law. Below that, even low counts can be catastrophic.
- **C — Reversal Risk (graded):** Democratic transition + weak P4 = reversal risk. Resource rents >30% OR stagnant growth = PROBABLE reversal. Youth unemployment >25% = compounding.
- **D — Predatory Neighbor:** Low-P1 state bordering aggressive power. Framework diagnoses vulnerability, not the shock itself.
- **E — Rentier Capture (BIDIRECTIONAL):** Negative: rents >25-30% GDP inflate P1. Positive: rents can buy cohesion in low-P1 states (rent-stabilization).
- **F — Sub-State Turbulence:** High-P1 states: flag "managed instability" when anti-system vote >25%, repeated executive collapse, or regional divergence >30% GDP per capita.
- **G — Suppression vs Prevention (THREE-TIER):** Tier 1 Military (force), Tier 2 Institutional/Legal (law), Tier 3 Prevention/Porosity (institutional design). Re-suppression after porosity = worst path.

### Essential Modifications (LIVE version)

- **Mod4 — Margin-of-Error Gate:** P1 ordinality claim applies ONLY when gap exceeds margin. Narrow-gap cases = abstain, don't predict.
- **Mod8 — Violence Risk/Agency Split:** Framework predicts violence RISK, not violence AGENCY (who initiates). Separate these in all predictions.
- **Safeguard I — Porosity-with-Backstop:** When fragmenting state has external backstop patron, predict re-suppression rather than permanent secession. Confirmed by Ethiopia/Tigray and Myanmar.

---

## What's Been Done

### Modern Case Studies (20 validated)

**Group A — Traditional Fragmentation:**
1. Post-Soviet (Estonia/Russia/Ukraine) — P1 ordinality confirmed
2. Yugoslavia (Slovenia/Croatia/Serbia/Bosnia) — 4-way ordinal confirmed; Safeguard A derived from Bosnia
3. Velvet Divorce (Czech/Slovakia) — high P1 = peaceful confirmed
4. Arab Spring (Tunisia/Egypt/Libya) — P1 ranking predicted outcomes; Safeguard C derived from Tunisia
5. Sudan/South Sudan — catastrophic confirmed; Safeguard B derived
6. Pakistan/Bangladesh — engineered bifurcated state failure confirmed
7. Singapore/Malaysia — flagship positive case; complexity-control thesis confirmed
8. Ethiopia/Eritrea — both low-P1, both poor trajectory confirmed

**Group B — Recursive/Suppressed:**
9. Serbia/Kosovo — recursive fragmentation; Safeguard A for UNMIK
10. Indonesia/East Timor — violence-source misattribution found (Mod8 derived)
11. Ethiopia/Tigray — recursive fragmentation; re-suppression confirmed; Safeguard I confirmed
12. Nigeria/Biafra — military suppression; rent-stabilization found (Safeguard E bidirectional)

**Group C — Non-Traditional:**
13. South Africa — institutional reconstruction; capacity lagging complexity confirmed
14. Northern Ireland/GFA — fragmentation prevention through porosity confirmed; Safeguard F derived
15. German Reunification — fusion; persistent east-west gap confirmed; Safeguard F confirmed
16. Spain/Catalonia — institutional/legal suppression (Tier 2); de-escalation confirmed
17. Belgium — extreme porosity; no hard limit found; Safeguard F confirmed

**Group D — Comparative:**
18. Baltics vs Central Asia — institutional choice > resource endowment confirmed
19. India/Pakistan/Bangladesh — continental-scale P1 ordinality confirmed; Safeguard C confirmed (Bangladesh)

**Group E — Prospective:**
20. Myanmar — re-suppression after porosity = catastrophic, confirmed prospectively; Safeguard I confirmed

### Ancient Extension (5 cases, ordinal proxy)
- Rome (East vs West), Han China, Abbasid Caliphate, Mongol Empire, Inca Empire
- Verdict: "strong heuristic, weak oracle"
- P1 ordinality held in 4.5/5; configuration thesis confirmed in all 5

### Branching Empirics
- River bifurcation ratio: Rb = 3.488 (discovery), 3.539 (confirmation, sealed holdout)
- Neuron arbors: 6 cell types, Rb range 2.917-3.743
- Self-organizing CV ≈ 0.26 vs engineered CV ≈ 5.77 (22x, p ≈ 1e-252)
- DGS → instability: null result (honest, documented)

### Aggregate Results
- Clean confirmation: ~78% (range 62-85%)
- Directional accuracy: ~100% (zero falsifications across ~130 predictions)
- P1 ordinality: 20/20 modern cases
- LIVE outperforms STATIC in every comparison

### Expansion — Batch 1 (cases 21-25, 2026-06-27)
- **Architectural decision settled first:** P1 kept as a single composite (NOT
  decomposed into capacity/accountability). Evidence: in the 2025-anchored WGI,
  Rwanda's capacity-accountability gap is +0.030 — inside the Mod4 margin — and
  decomposition changes no ordinal. See
  `docs/architectural_decisions/rwanda_p1_composite_vs_decomposed.md` (reproducible
  experiment in `sandbox/experiments/rwanda_p1_decomposition/`). The engine and the
  20-case baseline are therefore UNCHANGED.
- **Scored on fresh real data** (WGI 2025-anchored / UNDP HDR 2025 / WB WDI / FSI 2024,
  committed as `data/countries/*.json`): 21 Haiti/DR, 22 Venezuela, 23 Colombia,
  24 DRC/Rwanda, 25 Rwanda. Writeup: `live/runs/run7_expansion_batch1_cases21-25.md`.
  Batch scorecard ~75% clean, 0 falsifications; Safeguard I (Colombia) and the
  Mod4-then-divergence sequence (DRC/Rwanda 1996) both validated. Open prospective
  forecast: Rwanda latent reversal risk (voice deficit).
- **Structured JSON case records** now exist in `data/case_studies/completed/` for the
  20 baseline cases (transcribed from `live/runs/`) plus the 5 new cases — the README
  no longer over-promises them.
- **WGI 2025 vintage break:** new cases use anchored 0-100 scores; the legacy baseline
  used percentile ranks. Never assert an ordinal across that boundary.

---

## What Needs Doing

### Priority 1 — Geographic and Temporal Gaps

The case study database is concentrated in Europe, the Middle East, Africa, and post-Soviet space. Underdeveloped areas:

- **Latin America:** No case studies. Test on: Colombia/FARC peace process, Venezuelan state collapse, Chilean democratic transition/reversal, Argentine institutional oscillation, Mexican cartel-state dynamics.
- **East Asia:** Only Singapore/Malaysia tested. Test on: Korean War/division (1950-53), Taiwan's democratic transition, Hong Kong's re-suppression after porosity (2020 National Security Law — a DIRECT test of Safeguard I and re-suppression finding).
- **Caribbean/Pacific Islands:** Test the complexity-control thesis on island nations with natural geographic constraints.
- **Pre-modern cases beyond the current five:** Test on Ottoman Empire fragmentation, Spanish Empire dissolution, British Empire decolonization patterns, Austro-Hungarian dissolution.

### Priority 2 — Framework Improvements

- **Factionalism indicator:** Goldstone et al. (2010) found partial-democracy-with-factionalism is the strongest single predictor of instability onset. The MI doesn't capture this. Test whether adding a factionalism measure improves accuracy.
- **Ideology/legitimacy variable:** The ancient extension flagged this as missing. The Mandate of Heaven, caliphal religious legitimacy, and democratic legitimacy all shape outcomes in ways the MI doesn't measure.
- **Timing indicators:** The framework's biggest gap. Can leading indicators (rate of P1 decline, P5 trajectory slope, economic delivery metrics) provide even crude timing estimates?
- **Sub-national application:** Apply the MI to states/provinces within large heterogeneous countries (US states, Indian states, Chinese provinces, Italian regions).
- **Safeguard H (Centrifugal/Centripetal):** Test for incremental value over Safeguard F. Drop if redundant.

### Priority 3 — Data Expansion

- Expand country coverage beyond the current 85 snapshot / 27 longitudinal
- Reconcile with the 2025 WGI revision (new anchored scores vs legacy percentile ranks)
- Add time points: 2025 data as it becomes available
- Identify proxy indicators for countries with incomplete data

### Priority 4 — Prospective Predictions

- Identify 5-10 countries the MI currently flags as approaching fragmentation or reversal thresholds
- Document the predictions formally with falsification conditions
- Track over time

---

## How to Do It

### Running a New Case Study

1. **Select the case.** Choose based on what it tests that existing cases don't — a new geographic region, a new stress type, a new safeguard test.

2. **Create the case file.** Copy `data/case_studies/templates/case_template.json` to `data/case_studies/in_progress/`. Fill in metadata.

3. **Phase 1 — Pre-event scoring.** Collect all available indicators at the pre-event time point. Use `python scripts/score_country.py` to calculate pillar scores, MI, spread, configuration. Apply all safeguards.

4. **Phase 2 — Predictions.** Based ONLY on pre-event data, generate specific falsifiable predictions (a-h). Write them down BEFORE looking at post-event data. This is critical for intellectual honesty.

5. **Phase 3 — Verification.** Collect post-event data. Score each prediction as confirmed, partially confirmed, or falsified. Explain what failures reveal.

6. **Document.** Write up the complete case study with all data, predictions, results, and analysis. Save to the case study directory.

7. **Baseline check.** If proposing any framework modification based on the case, rerun the retrodiction protocol against all existing cases to verify no degradation.

### Testing a Modification

1. **Create experiment directory** in `sandbox/experiments/` with a descriptive name.
2. **Document the hypothesis:** What modification are you testing? What specific improvement do you expect? What would falsify it?
3. **Implement the modification** by extending the relevant module in `mi/`.
4. **Run against the 20-case baseline.** Compare MODIFIED vs LIVE accuracy.
5. **If improvement with no degradation:** Document fully and flag for review.
6. **If degradation on any existing case:** Reject. Document the negative result (negative results are valuable).

### Proposing a New Safeguard

1. **Identify the failure:** Which case did the framework mispredict? What specifically went wrong?
2. **Hypothesize the correction:** What condition, if checked, would have caught the error?
3. **Formalize:** Write trigger conditions, modification logic, and falsification criteria.
4. **Test against existing cases:** Would the new safeguard have incorrectly triggered on any case where the framework was already correct?
5. **Test against new cases:** Find at least 2-3 additional cases where the safeguard is relevant. Does it improve predictions?
6. **Document:** Full derivation history, validation record, and practical output.

### Coding Standards

- **CONFIRMED:** Prediction matched outcome on the specific dimension predicted.
- **PARTIALLY CONFIRMED:** Direction correct but magnitude, form, or timing significantly different.
- **FALSIFIED:** Prediction contradicted by outcome.
- When ambiguous between confirmed and partial, code as **partial**.
- When ambiguous between partial and falsified, code as **partial** but note the ambiguity.
- Every coding decision must include specific cited evidence.

---

## What NOT to Do

- **Don't modify files in `data/baselines/`.** These are the validated reference results.
- **Don't claim timing predictions.** The framework explicitly cannot predict when events occur.
- **Don't use the MI for calibrated probabilities.** It produces ordinal rankings, not calibrated forecasts.
- **Don't cherry-pick cases.** Choose cases that STRESS-TEST the framework, not cases designed to confirm it.
- **Don't interpolate missing data.** Missing data is information. Report gaps explicitly.
- **Don't overclaim.** A framework that honestly reports 78% is more valuable than one that claims 95%.
- **Don't modify the LIVE framework without running the full 20-case baseline check.**

---

## Key References

### Academic Foundations
- Huntington, *Political Order in Changing Societies* (1968) — the intellectual ancestor
- Goldstone et al., "A Global Model for Forecasting Political Instability," *AJPS* 54(1), 2010
- Cederman, Wimmer & Min, "Why Do Ethnic Groups Rebel?" *World Politics* 62(1), 2010
- Svolik, "Authoritarian Reversals and Democratic Consolidation," *APSR* 102(2), 2008
- Nye, *Soft Power* (2004)
- Taleb, *Antifragile* (2012)
- Kennedy, *The Rise and Fall of the Great Powers* (1987)

### Data Sources
- World Bank Worldwide Governance Indicators (WGI) — P1 and P5 inputs
- Transparency International Corruption Perceptions Index (CPI) — P1 input
- WIPO Global Innovation Index (GII) — P2 input
- Harvard/OEC Economic Complexity Index (ECI) — P2 input
- UNDP Human Development Report (Education Index, Life Expectancy Index) — P3 inputs
- World Bank World Development Indicators (GDP PPP, resource rents, ODA) — P4 inputs
- Fund for Peace Fragile States Index (FSI) — P5 input

### Existing Comparable Tools
- Fragile States Index: broader coverage, no predictive architecture
- PITF/Goldstone: better onset forecasting (~80%), no cross-type comparability
- V-Dem: richer democracy measurement (531 indicators), no fragmentation diagnostic
- WGI standalone: MI's capacity construct substantially redundant with WGI; MI's value-add is complexity-capacity matching, cross-type comparability, and safeguard system
- ViEWS: calibrated probabilistic forecasting at grid-cell level; MI cannot match this
