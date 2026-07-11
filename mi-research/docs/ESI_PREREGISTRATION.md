# External Support Index (ESI) — Pre-Registration

**Status:** FROZEN on commit. Binding. The construction below (indicators, sources,
normalization, aggregation) is fixed in `config/esi.json` and this file **before** any
test against outcomes is run. Tests are committed and run in a separate, later step
(generate-before-grade). Companion to `ROBUSTNESS_PREREGISTRATION.md`.

## Hypothesis

The institutional signal's measured erosion in the modern era (ROBUSTNESS_RESULTS
Findings 2–3) is caused by **external capital and institutional support mechanisms that
delay the consequences of structural misalignment.** If correct, controlling for external
support should **recover the institutional signal** — the MI's structural scores should
predict crises significantly better once we account for how much outside support a country
was receiving. Finding 5 already shows, by manual classification, that the durability
gate's false alarms cluster among propped-up states (reserve currency, sovereign wealth,
EU-anchored, IMF-program). ESI operationalizes that classification into a measured control.

## Construction (frozen — see `config/esi.json` for exact codes)

Three sub-dimensions, each a different mechanism of external support. **All indicators
normalized to [0,1], higher = more support.**

- **A — Financial Life Support (active intervention):** IMF program active (binary),
  IMF cumulative years / 20 (chronic dependence), concessional debt share.
  *Debt-service burden is EXCLUDED from the primary ESI* (its sign is ambiguous — high
  service can mean "someone keeps lending" or "approaching default"); it enters only a
  labelled sensitivity variant.
- **B — Structural Dependency (chronic substitution):** FDI net inflows %GDP, ODA %GNI
  (un-inverted vs MI scoring), remittances %GDP. *Export-partner HHI is DEFERRED for
  Phase 1* (skip-if-not-programmatic, per task) and flagged as a future addition.
- **C — Systemic Insurance (implicit guarantees):** reserve-currency status, EU/Eurozone
  membership (tiered), NATO/major-alliance membership (tiered), SWF assets %GDP,
  reserves in months of imports. C is manually coded once for all countries (stable).

**Aggregation (frozen, NOT optimized):** within each sub-dimension, the **mean of the
available normalized indicators**. ESI = **equal-weight mean of the three sub-dimension
scores**. Weights are deliberately equal and un-tuned. If the mechanism is real, even a
crude equal-weight composite shows it; if it only works with tuned weights, it is probably
not real.

**Missing data (Track-2, frozen):** degrade gracefully, never impute. Use whatever
indicators are available for a country-year; a sub-dimension with zero available
indicators is null; ESI = mean of the non-null sub-dimensions. Coverage documented per
country-year in the build output.

**Panel:** ESI is built at the temporal-holdout base years (**2004** primary, **2012**
secondary) for the countries in `data/robustness/temporal_holdout_panel.json`, plus (best
effort) historical proxies for Test 2C.

## Tests (frozen, run in this exact order; all reported regardless of outcome)

The joined outcomes come from `data/robustness/temporal_holdout_panel.json` (per country:
MI structural scores P1/P4, gate flag `elevated`, `vuln` 0–3, `crisis`). The crisis
definition is the frozen one (UCDP onset OR CRAG default within window); **not re-derived.**

- **2A — Does ESI predict which countries the gate gets wrong?** Split the gate's 2004
  errors into TP / FP / FN / TN; compute mean ESI per bucket. Hypothesis: **FP ESI ≫ TP
  ESI** (countries flagged-but-no-crisis are the propped-up ones). Mann-Whitney U + t-test
  between FP and TP ESI; **report effect size (Cliff's δ / Cohen's d), not just p.**
- **2B — Does controlling for ESI recover the institutional signal? (make-or-break.)**
  Logistic regressions predicting `crisis` on the full 2004 panel:
  - Model 1: MI structural score only.
  - Model 2: MI structural score + ESI.
  - Model 3: MI structural score + ESI + (MI × ESI) interaction.
  Compare AUC-ROC across models. **Primary readout: does the MI coefficient increase (in
  magnitude, correct sign) when ESI is added?** If yes, the signal was suppressed by
  uncontrolled support and controlling recovers it. Also run GDP-per-capita + ESI and
  FSI + ESI; if ESI helps the MI more than the simple baselines, the MI carries structural
  information visible once support noise is removed. ("MI structural score" = the pillar
  composite used in the holdout; specified concretely in the test script before running.)
- **2C — Does ESI explain the 150-year erosion?** If an ESI (or crude proxy: formal
  alliance / colonial-imperial membership / international lending program) can be built at
  the historical anchors, check whether the decay curve (`decay_curve_conflict.json`)
  flattens when ESI is controlled. Fully flattens → erosion explained by capital-system
  growth; partial → part of the story; no change → different cause, hypothesis revised.
- **2D — Concentration and fragility.** For countries above the 75th ESI percentile,
  compute a Herfindahl-style concentration index across the three sub-dimensions (and
  across sources). Report the distribution; flag countries with **both high ESI and high
  concentration** — single-point-of-failure dependence. This list is the most operationally
  relevant output.

## Interpretation gates (fixed in advance)

- **2B shows signal recovery** → state plainly: the modern erosion is explained by external
  capital support; controlling for it recovers the pre-modern relationship; MI structural
  scores are predictive once the distortion is accounted for. (Strongest result in the
  program.)
- **2B shows no recovery** → state plainly: external support does not explain the erosion;
  the mechanism hypothesis needs revision. Report the null; do not rationalize.
- **2A positive but 2B null** → the mechanism operates case-by-case (propped-up states are
  individually identifiable) but not systematically; supports ESI as a diagnostic **flag**,
  not a control variable.

## Rules (binding)

1. **Do not optimize ESI weights** to maximize signal recovery. Equal weights, first pass.
2. **Do not iterate on crisis definitions.** Use the frozen holdout definition verbatim.
3. **Report all tests regardless of outcome.** The null is as important as the confirmation.
4. **Every indicator source documented** with exact variable codes + URLs (`config/esi.json`).
5. **Reproducible** from committed code + data. Generate the ESI + tests, commit, then grade.
6. Result documented as **Finding 8** in `ROBUSTNESS_RESULTS.md`, whatever it says.

## Coverage honesty

FDI is sparse pre-1970; SWF data barely exists pre-2000; IMF MONA covers 1952–present;
concessional-debt/IDS covers debtor-reporting countries only (high-income issuers absent →
concessional share treated as 0, documented). Coverage is reported per indicator and per
country-year; thin coverage is disclosed, not hidden.
