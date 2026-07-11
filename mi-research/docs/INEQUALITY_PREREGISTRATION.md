# Inequality as the Missing Distribution Dimension — Pre-Registration

**Purpose.** Test whether **rising inequality** explains the erosion of the
institutional signal *in the domestic channel* (Finding 12: domestic-origin slope
−0.00122, p<0.001; external flat) by **mechanically severing** the institution →
domestic-stability link while **preserving** the institution → aggregate-wealth link
(Finding 10: P1↔GDP r 0.770→0.818). Mechanism: institutions have become better at
producing *aggregate* wealth (→ P1↔GDP re-couples) while the *distribution* of that
output concentrated; domestic political rupture is driven by distribution, not
aggregates, so the domestic signal erodes as concentration rises.

**The constraint profile the mechanism must satisfy (from 12 prior findings).**
continuous from ~1850 no regime breaks (F7/F11); domestic channel specifically (F12);
coexists with strengthening P1↔GDP (F10); present within mature states (F9-A); invisible
to WGI (measures function, not distribution) and to P3 (measures *average* human
capital, not distribution); not external support / monetary regime / contagion
(F8/F11/F12). Inequality (r>g, Piketty's ~200-yr dynamic with a 1914–1980 compression)
fits each — this pre-registration tests whether it actually does the work.

---

## Binding rules

1. **Pre-register before running;** committed before any analysis (sha256 on commit).
2. **Tests 1 & 2 are the gate.** If **both** fail → stop. If one passes/one fails →
   proceed with caution, flagged partial.
3. **One primary indicator, fixed here** (no shopping for the one that works): **WID
   top-10% pre-tax national income share**. WB Gini is a **labeled sensitivity** only,
   run *after* the primary.
4. **No imputation.** Country-years without inequality data are **excluded and
   documented**, never filled.
5. **No tuning** (Test 5/6 indices equal-weight). **Test 6 is EXPLORATORY** — a P6
   distribution pillar is *not* added to the framework on the basis of this analysis.
6. **Report all results,** including cross-sectional-yes / longitudinal-no splits and
   power limits (WID coverage is thin pre-1950 and for several majors, e.g. UK/DE from
   ~1981, JP sparse — disclosed up front).
7. Diagnosis only — **no framework changes** this session.

---

## Data (fixed here)

- **Primary inequality = WID top-10% pre-tax income share**, via the Our World in Data
  grapher republication of WID (`income-share-top-10-before-tax-wid`, column
  `share_top_10…before_tax…`), cached to `data/robustness/inequality/`. Coverage
  (confirmed): 156 countries; deep history USA 1913+, FRA 1910+, SWE 1935+, RUS 1820+,
  IND 1923+; modern breadth 62 (2004) / 84 (2012). Top-1% share
  (`income-share-top-1-before-tax-wid`) cached as a secondary robustness indicator.
- **Sensitivity inequality = WB Gini** `SI.POV.GINI` (broader modern coverage, thin
  pre-1990), used only for labeled robustness on the modern cross-sectional tests.
- **Domestic-crisis outcome = the Finding-12 classification** (domestic-origin conflict
  onset: COW intra + UCDP type 3/4). For the holdout (Tests 1/4) the forward windows
  are the committed temporal-holdout windows (2004→2024, 2012→2024); domestic-crisis =
  ≥1 domestic-origin onset in window. Secondary internal-dysfunction composite =
  {Polity2 −≥3, V-Dem libdem −≥0.10, domestic-origin onset} (external GDP/FSI drops
  excluded, since those can be shock-driven).
- **Pillars / panel / holdout / erosion machinery**: the committed engine, the MI
  5-point panel (`decoupling_panel`), the temporal holdout, and the Finding-12
  domestic-channel spread series — all used **unmodified**.
- **Nearest-year join**: inequality at origin year, else nearest within ±3 years.

---

## Test 1 — Does inequality predict domestic crises? (GATE arm A)

Logistic (holdout 2004 primary, 2012 secondary; predictors standardized), outcome =
domestic-origin crisis in the forward window. neg-P1 = (1−P1) so higher = more risk;
INEQ = top-10% share (higher = more concentration).
- **M1** dom ~ neg-P1
- **M2** dom ~ INEQ
- **M3** dom ~ neg-P1 + INEQ
- **M4** dom ~ neg-P1 + INEQ + neg-P1×INEQ

Report coefficients (+p), and AUCs for M1–M4 vs neg-logGDP-only and FSI-only baselines.

**PASS (arm A):** INEQ is a **significant** (p<0.05) predictor of domestic crises in the
predicted direction (higher inequality → more crisis) in the primary window, **OR** the
neg-P1 coefficient **materially increases** M1→M3 (≥ +15% relative) with an AUC gain
(signal recovery when distribution is controlled). **Secondary confirmations
(reported, not required):** M4 interaction **negative** (good institutions protect less
under high inequality); MI+INEQ beats GDP-only and FSI-only.
**FAIL (arm A):** INEQ non-significant **and** neg-P1 coefficient does not recover.

## Test 2 — Does the domestic-channel erosion track inequality over time? (GATE arm B)

Take the **Finding-12 domestic-channel spread** at each epoch (the 19-point curve,
1816–1996). Compute mean WID top-10% share across the deep-coverage major economies at
each epoch (whatever has continuous WID data; effective span ≈1920–2020 given coverage
— disclosed). Overlay; compute Pearson correlation between the two series across shared
epochs.

**PASS (arm B):** **negative** correlation, Pearson **r ≤ −0.4** across shared epochs
(rising inequality ↔ declining domestic signal). **Piketty-U fingerprint (reported):**
does the domestic spread run *higher* during the 1914–1980 compression and *lower* in
the high-inequality pre-1914 / post-1980 tails? **FAIL (arm B):** |r| < 0.4 or wrong
sign; in particular, if the domestic spread keeps falling monotonically *through* the
mid-century inequality compression (no mid-century signal recovery), the U-curve
fingerprint is absent → fail.
**Sensitivity (reported):** Sweden (strong compressor) vs USA (weak) — did the more
compressing country's signal hold better? — the discriminator of "inequality
specifically" vs "mid-century conditions generally."

**Gate rule:** both A & B fail → **STOP** (13th null). One passes → proceed to Tests
3–6, flagged partial (cross-sectional-yes/longitudinal-no, or vice-versa, reported
explicitly).

---

## Test 3 — Inequality explains erosion WITHIN mature states *(if gate)*

Mature-state sample (F9-A classification). At each MI point split mature states at the
median top-10% share (low vs high inequality); compute the institutional signal over
domestic crises per group. **Support:** signal strong in low-inequality mature states,
weak in high-inequality; Nordics (low Gini, high P1) in "works" group, US/UK (high Gini,
high P1) in "eroded" group. **Null:** no group difference.

## Test 4 — Does controlling for inequality resolve F10-vs-F12? *(if gate)*

At each MI point (1996–2024) cross-sectional: domestic-stress ~ P1 + logGDP + INEQ.
Track the **P1↔domestic-stability partial correlation controlling for inequality**
across the five points vs the **raw** P1↔domestic-stability correlation (declining per
F12). Domestic-stress = internal composite (Polity/libdem backslide + domestic onset
count; FSI internal sub-index if available). **Support:** raw correlation declines but
the inequality-controlled **partial correlation is stable/rising** — inequality is the
missing variable. **Null:** partial correlation declines too.

## Test 5 — Long-run inequality vs the full erosion curve *(if gate)*

Deep-coverage subset (US, FR, SE, IN, RU, + any with pre-1950 WID). Correlate the
Finding-7 spread and mean inequality across the full available span. **Check 1914–1980
specifically** for the compression-vs-signal fingerprint. **Power limitation
acknowledged:** 3–19 countries pre-1950 — report direction + note constraint, do not
overclaim.

## Test 6 — Inequality as a candidate MI dimension (EXPLORATORY ONLY) *(if gate)*

Construct P6 = 1 − normalized top-10% share (higher = more equal). Add equal-weight to
the five pillars, rescore 2024. Does six-pillar MI predict domestic outcomes better
than five-pillar? Which countries move most (expect US down, Nordics hold/up)?
**EXPLORATORY** — flag as a candidate for future pre-registered validation only; do
**not** adopt P6.

---

## Synthesis (frozen)

Table T1–T6 (measure / prediction / result / supports?). Verdict:
- **T1 & T2 both fail** → hypothesis dead; **13th registered null**; stop.
- **T1 & T2 pass, T3 & T4 pass** → inequality is the distribution variable that converts
  institutional function into domestic stability; the MI measures function correctly and
  misses distribution — a scope characterization + extension path (P6 candidate), not a
  flaw.
- **T1 pass / T2 fail** → inequality matters cross-sectionally but does not explain the
  *longitudinal* erosion (reported as such).

Artifacts `data/robustness/inequality/`; code `scripts/robustness/inequality_*.py`;
narrative `docs/INEQUALITY_RESULTS.md` + Finding 13 of `docs/ROBUSTNESS_RESULTS.md`.
