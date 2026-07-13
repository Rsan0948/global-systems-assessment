# Prediction Ledger — what the apparatus actually predicts (predict-forward)

Sandbox `sandbox/predictive-reach` off `0b9ceed`. Method: every instrument back-scored at year *T* → every outcome at *T+k* (k∈{1,3,5,10}), cohort cross-sections (base grid 1996–2016, one row/country/cohort — no pseudoreplication), GDPpc-partialled, BH-FDR, sign-stable across cohorts, **confirmed on a sealed country-half**, then an **autoregressive-baseline test** (control for the outcome's own lagged value) to separate forecasting from persistence.

## The one finding that reframes everything

The apparatus predicts in **two different modes**, and they were being conflated:

| Mode | What it is | Effect size | Verdict |
|---|---|---|---|
| **Structural fingerprint** | Instrument co-persists with a regime/development **level** | ρ **0.6–0.9** | Powerful **nowcast/classifier**; *collapses under an AR baseline* → NOT a forecast |
| **Leading indicator** | Instrument forecasts **change/events**, or a level **beyond its own persistence** | \|ρ\| **0.20–0.41** | **Genuine forecast** — survives sealed-half + AR baseline |

577 of 911 confirmed associations are mode-1 fingerprints (e.g. `cso→libdem_level` 0.81 → 0.01 net-AR; `youth→fertility` 0.90 → −0.12). Real, useful for *classifying* a polity's structural state — but not prediction. The genuine predictive reach is mode-2, below.

## Genuine predictive reach, per instrument (survives sealed-half + AR baseline)

| Instrument | What it genuinely forecasts (lead) | Dir | incr ρ |
|---|---|---|---|
| **V1 Capacity** (MI, P2/P3/P5) | **life satisfaction** (5–10y), **GDP growth** (3–10y), FDI inflow (10y) | + | .23–.41 |
| **V3 Pressure** | **youth-bulge → lower GDP growth** (3–10y); numerator → brain-health decline (10y); internet → higher life-sat | ± | .21–.27 |
| **T4 Scarring** | **conflict onset / recurrence** (1–10y, THE trap); **lower future life satisfaction** (5–10y); lower brain-health (10y) | − (wellbeing) / + (conflict) | .24–.41 |
| **T5 Turbulence** | *(nothing survives as a forecast)* — weak positive on regime **level** = persistence only | — | — |
| **T6 Spark** | **lower future life satisfaction** (3–10y, incl. military & transcendent sub-scores); weak **democratic erosion** (10y, beyond persistence) | − | .22–.28 |
| **DGS** (frag leg) | strong on regime level but **collapses to persistence**; no genuine leading indicator survived | — | — |

## The "V2 → wellbeing"-class discoveries (the surprises)

The V2-predicts-wellbeing accident generalizes — **wellbeing is the outcome the whole apparatus forecasts best beyond persistence**:

1. **Life satisfaction (5–10y out) is forecast by the entire stack** — up by capacity (P3 +0.41, P5, MI), down by scarring (t4_scar −0.39), down by spark density (t6_spark −0.28, transcendent-spark −0.29). Every leg of the founding equation leaves a decade-long wellbeing signature. *(Caveat: life-sat panel is 2011+, so k=10 leans on few cohorts and a short AR control — strongest as a lead, weaker as a sealed claim.)*
2. **Capacity → GDP growth (3–10y)** — MI/P2/P3 forecast higher future growth net of GDP level *and* growth persistence (+0.22–0.25). Modest but genuine.
3. **Durability gap → emigration** — `durgap` (earned-vs-granted institutions) forecasts net-migration outflow 3–10y out (−0.26). Novel; the P4−P1 gate reads as future exit pressure.
4. **Spark density → future malaise** — T6, built to score coup/conflict trigger arrival, forecasts *lower life satisfaction* a half-decade out. A political-instability instrument doubling as a wellbeing bellwether.
5. **Scarring suppresses human capital for a decade** — t4_scar → lower brain-health and life-sat at 10y, beyond persistence; the conflict trap has a wellbeing tail, not just a violence tail.

## Stacking / mix-and-match — the ensemble cracks a ceiling the parts couldn't

Every configuration fit on discovery countries, scored ONLY on the sealed half, incremental over an **AR(lagged-outcome)+GDP** baseline (`stack_screen.py`, `stack_validate.py`). No in-sample numbers (the audit's C1 trap).

**Headline: democratic backsliding becomes forecastable by the ENSEMBLE, not any single tier.** The audit and the univariate screen agreed no single instrument forecasts backsliding. But a stacked model does:

| Outcome | AR+GDP base | best single | **locked stack** (AUC, held-out) | replicates k=3/5/10? |
|---|---|---|---|---|
| **libdem_backslide** | 0.48 (chance) | 0.55 | **0.66 / 0.73 / 0.66** | ✅ +0.09→+0.27 all leads |
| **electdem_backslide** | 0.56 | 0.62 | **0.74 / 0.71 / 0.74** | ✅ +0.14 all leads |
| gdp_pc_growth (5y) | 0.04 | 0.04 | 0.24 | ⚠️ fragile — negative at k=10 |
| conflict_onset | 0.75 (trap) | 0.81 | 0.81 | ✅ small consistent +0.03 |

The recurring backsliding ingredients: **anocracy + internet + cso + pts (V3 pressure) + t6_spark (T6) + dgs (frag leg) + durgap/P3/P5 (V1 capacity)** — it takes pressure *and* spark *and* capacity *and* the DGS together. **The tiers are complementary, not redundant; backsliding is multi-causal, so only the full stack sees it.** That is the scientific payoff: the Mule shrinks not by a better single instrument but by reading all faces of the equation at once.

**Interactions add almost nothing held-out — "tiers add, don't multiply" confirmed at scale** (matches the audit's T5×T6 null). The lone exception: **v1_mi × t4_scar (capacity × scarring)** genuinely lifts backsliding AUC (+0.08 held-out) — a real, modest multiplier.

### Exhaustive combinatorial search (all ~21k subsets, internals broken out, three-way FIT/SEL/TEST split)
Broke every tier into its sub-components (27-predictor pool) and enumerated all subsets size 1–4, selecting on one country group and reporting on a **sealed third**. Findings:
- **Subset-hunting OVERFITS its selection set.** The best-on-SEL 4-predictor combo lands at only ~0.54 TEST AUC — *worse* than a regularized full model. There is no magic 4-subset.
- **The robust winner is "everything, regularized."** Full-27 ridge-logistic → **electdem TEST AUC 0.715, libdem 0.684** (chosen a-priori, never touched TEST). A **frozen 8-internal** consensus set matches it: **electdem 0.705 [0.602–0.801], libdem 0.692 [0.595–0.786]**, λ-insensitive.
- **Decomposing composites was worth it** — it isolated the load-bearing internals: `anocracy` (single best, libdem AUC 0.68 alone), `P1`, `internet`, `growth_vol`, `t4_reversed_trust`, `t5_turbulence`, `t6_s4_military`/`t6_s3_transcendent`. The signal lives in specific sub-components, not the headline tier scores.
- **Calibration ceiling (honest):** discrimination is carried by the *low-risk* bins — the model reliably flags the stable majority (bottom quintiles 0–4% backsliding) but the top predicted-risk quintile is **non-monotone** (17% < the middle's 35%). AUC~0.7 = good triage, **not** a backslider-namer.

Frozen for confirmation in `PREREG_BACKSLIDING.md` (true out-of-time 2016/2018 holdout). Event counts are modest (~19–22 in the sealed third) → CIs are wide; this is a confirmation candidate, not a headline number yet.

### Relational / ratio features — the RELATIONSHIPS beat the levels (the best model found)
Instead of stacking instruments additively, build the **gaps and ratios *between* them**, MI-style (normalize each to a comparable within-year scale using train-only reference, then relate) — pressure/capacity, complexity/capacity, cross-tier discordance, tier-profile dispersion, the durability gap. `relational_screen.py` / `relational_validate.py`.

| backsliding (sealed TEST AUC) | ADD-6 (levels stacked) | **REL (relationships)** |
|---|---|---|
| libdem k=3/5/10 | 0.51 / 0.56 / 0.48 | **0.62 / 0.72 / 0.70** |
| electdem k=3/5/10 | 0.64 / 0.66 / 0.60 | **0.76 / 0.74 / 0.70** |

- **Relational features beat the additive stack at every lead, both outcomes** (+0.10–0.22), CIs excluding 0.5 at k=5/10 (libdem k=5 0.720 [0.602–0.825]). With ~11 interpretable features it **matches/beats the 27-predictor regularized stack** — a better *and* cleaner model. REL ≈ BOTH → the raw levels add nothing once you have the relationships. **This vindicates the MI relational philosophy: for regime change, the discordances between structures carry the signal, not the levels.**
- **Strongest single relationship: capacity − turbulence** (`v1_mi − t5_turb`, AUC ~0.68) — low capacity *relative to* regime turbulence = the backslider. Recurs across both outcomes.
- **The founding equation as ONE number (complexity − capacity) is too coarse** (AUC 0.47–0.56) — the thesis works relationally only when the *specific pairwise* gaps are kept, not collapsed to a single matching-gap.
- **Relational structure helps ONLY backsliding** — conflict is saturated by the trap (REL≈ADD≈0.89), growth is fragile, wellbeing is persistence-bound. It's specifically the multi-causal, level-resistant outcome that the relationships unlock.

### OUT-OF-TIME CONFIRMATION (the real test) — `confirm_oot.py`, `robustness.py`
The country-hash split can let same-era countries sit in both train and test. The honest test is a **temporal holdout** — train on past base years, predict a genuinely future backsliding wave. Rolling-origin results (Δ = relational model − AR+GDP baseline, on future cohorts):

| train → test cohort | libdem Δ | electdem Δ | baseline AUC |
|---|---|---|---|
| ≤2004 → 2008/2012 | **+0.142** | **+0.115** | 0.56 (weak) |
| ≤2008 → 2012 | **+0.147** | **+0.161** | 0.50 (weak) |
| ≤2012 → 2016/2018 | −0.121 | −0.022 | **0.77 (saturated)** |

**Verdict: the structural relationships DO forecast backsliding out-of-time — confirmed in 2 of 3 windows (+0.11 to +0.16).** They fail *only* on the 2016/2018 wave, and diagnostically so: established wealthy democracies eroded, so the level+wealth baseline already predicts it (0.77) and structural signal is redundant. **The apparatus adds the most forecasting value precisely when backsliding is NOT obvious from a country's democracy level and wealth.**

Hardening that backs this reading:
- **Not overfitting** — a λ sweep (1→100) does not rescue 2016/2018 (Δ stays −0.10 to −0.13); it's baseline redundancy, not variance.
- **No leakage** — placebo (permuted test labels) collapses to AUC ~0.50 (0.497/0.491).
- **Threshold-robust** (0.03/0.05/0.07 same pattern) and **deterministic** (identical re-runs).

Honest boundary restated: **no single tier forecasts regime change; the tiers *read relationally* do, out-of-time, except when level-persistence has already saturated the signal (the 2016–2023 wave).**

## DEEP TIME — same math back to 1820, and the horizon swept wide (`deep_time.py`, `deep_horizon.py`)
Pushed the identical feature math back to **1820** (V-Dem regime indices + civil-society 1789+, conflict onsets 1818+; `rol_vdem` as a deep CAPACITY proxy since WGI is modern-bound), leads out to **k=30**, analysed by era. Metric = mean per-cohort partial-Spearman net of persistence (one row/country/cohort → no pseudoreplication). ~200 years, 62 states in 1820 rising to 174. Descriptive discovery (AR-only control; no deep GDP).

**The net-new finding: different ruptures run on different clocks — invisible to the modern k≤10 window.**

- **Democratization has a FAST and a SLOW channel that cross over at ~12–15 years.** Turbulence (fast) predicts near-term opening (ρ +0.10–0.12 at k≤10) then **decays to ~0 by k=25–30**. Rule-of-law capacity (slow) is ~0 short-term but **rises monotonically to +0.16 at k=30**. This empirically resolves the program's "capacity = generational timescale" claim: capacity's democratizing signal *only exists at 15–30-year leads*.
- **…and the slow capacity→democratization channel has FADED.** Era×horizon: `rol→democratize@k30` was **+0.22 in the 19th century, +0.18 interwar, +0.05 Cold War, ~0 modern.** Structural capacity used to forecast generational democratization; it no longer does.
- **Backsliding is the mirror image — deep, INTENSIFYING, and horizon-wide.** The relational **rule-of-law − anocracy gap** forecasts backsliding in every era, strengthening monotonically: C19 ~−0.10 → interwar −0.15 → Cold War −0.24 → **modern −0.25 to −0.31 (out to k=20)**. The relational backsliding signal is not a modern artifact; it's a 120-year phenomenon that has become *more* structurally predictable and reaches a generation out.
- **Conflict onset is a LONG-horizon structural signal.** The capacity−anocracy gap and turbulence forecast conflict onset **better at 20–30-year leads than at 5** (gap ρ −0.04 at k=5 → −0.14 at k=30; turbulence +0.03 → +0.10). Anocracy *flips*: mildly protective short-term, risk-seeding long-term. Structural conditions today seed conflict a generation later.

**Summary of the clocks:** democratization = fast(turbulence)/slow(capacity) split, slow channel decaying since 1900; backsliding = all-horizon, intensifying, relational; conflict = generational/long-horizon. Caveats: AR-only (no deep GDP), modest descriptive ρ, 19th-c n smaller, modern long-k thin (k=30 ≈ 2 cohorts). Leads, not claims — but they hold across ~200 years and are sign-stable within era.

### Why the slow capacity→democratization channel died after ~1945 (`deep_democratization.py`)
The decisive follow-up. Two mechanisms, both confirmed, one substantive:

| era | corr(rol,lib) | % high-cap already democratic | ρ(cap→dem \| room to move) | prior-capacity Δ of democratizers |
|---|---|---|---|---|
| C19 1820–99 | +0.85 | **3%** | +0.14 | **+0.62** |
| Interwar 1900–44 | +0.81 | 19% | +0.11 | +0.66 |
| Cold War 1945–88 | +0.85 | 44% | +0.08 | +0.28 |
| Modern 1989–2015 | +0.89 | **86%** | **+0.04** | **−0.43** |

1. **Saturation (mechanical):** by the modern era **86% of high-capacity states are already democratic** — the top of the relationship is censored, they can't democratize further.
2. **Composition inversion (substantive, decisive, audited):** the prior-capacity gap of future democratizers **flips from +0.62 (19th c.) to −0.43 (modern)** — and this survives the adversarial audit: re-run with **independent WGI capacity** (not V-Dem) it is **−0.58/−0.62** (even stronger), and it beats a permutation null. 19th-century democratizers were high-capacity states (democracy as the fruit of a built rule-of-law state); modern democratizers are institutionally *weak* states. The third wave (democratization rate 0.18→0.42) swept in low-capacity states via exogenous shocks (decolonization, Soviet collapse), not endogenous capacity.

> **⚠ AUDIT CORRECTION (`deep_audit.py`).** The stronger claim that "capacity→democratization *died* to ~0" was partly an **artifact of rol/libdem multicollinearity** (corr 0.89): the raw partial-ρ fade (+0.14→+0.02) is unstable. Orthogonalizing rol from libdem, capacity *still* predicts modern democratization (**+0.10**). So the channel did not die — capacity still matters. What is robust is the **composition shift**: modern democratization now *targets* low-capacity states. Frame it as WHERE democratization happens, not capacity losing predictive power.

**This closes the loop with the backsliding finding.** Modern democratization landing on low-capacity states produces a growing stock of **capacity-poor democracies** — exactly the population where the capacity−anocracy relational gap now predicts backsliding (independent WGI capacity, OOT-confirmed, intensifying). The two deep-time findings are one mechanism: **the post-1945 spread of democratic *form* to institutionally weak states created the fragile democracies that make capacity→backsliding thrive.** (Audit status: composition inversion + backsliding signal = robust to independent capacity, permutation null, tolerance, leakage checks; the "channel died" framing = corrected.)

### Prospective test of the extrapolation — do capacity-poor NEW democracies actually backslide more? (`deep_cohort_test.py`)
Identified every democratization transition (libdem crosses <0.5→≥0.5) 1800–2008 with 15y follow-up (**81 transitions, 17 backslid**), tagged by era and capacity-at-transition (rol percentile; libdem≈0.5 for all, so the coupling is differenced out at the crossing).
- **Pre-1975 democratizers had NO low-capacity members** (all mid/high — democracy was capacity-gated). **Post-1975 opened the low-capacity lane** (27/45), and within it capacity sorts fate: low **33%** backslide, mid **6%**, high **0%**.
- **Capacity-at-transition predicts subsequent backsliding, significant in the post-1975 cohort:** ρ=−0.32, **permutation-p=0.035** (survives the nonparametric null). The post-1975 low-capacity cohort = **33% of transitions but 53% of all backsliders.**
- **Honest limit:** only 17 events in 200 years → the strong *categorical* "this cell dominates" contrast is **inside** its permutation null (underpowered). The continuous gradient is what's real; the prediction is **supported at the resolution the data bears, not more.**

## Six deep angles (post-campaign extension; `common.py` substrate, `READINESS.md`)

### Angle 1 — the DYNAMIC founding equation (rates/velocities) → **NULL** (`angle1_dynamic.py`)
"Complexity outruns capacity" is a rate statement; tested it as one. **Mismatch velocity = v(civil-society) − v(rule-of-law)** (Huntington's participation-vs-institutionalization gap) does **not** forecast backsliding (ρ≈0.00, perm-p 0.87–0.98). The **decisive test**: the *static* level gap (rol−cso) is real (ρ=−0.09, perm-p=0.0) but the **velocity adds nothing over it** (ρ=−0.017, perm-p=0.31) — same sample, so a true null, not low power. Components (v_rol, v_cso), acceleration, and the modern independent WGI-velocity version are all null. Lone whisper: mismatch-velocity → conflict onset ρ=+0.038 (perm-p=0.02, right direction, negligible size).
> **The founding equation is a STATE relationship, not a RATE one.** Rupture risk is set by *where* a polity sits in capacity–complexity space, not *how fast* it moves through it. This validates the static relational gaps as the right operationalization and closes the "is the thesis dynamical?" question: empirically, no.

### Angle 2 — WITHIN-COUNTRY fixed effects → **REAL (and cross-section-invisible)** (`angle2_within.py`)
Decomposed the capacity→backsliding association into POOLED / BETWEEN (across country means) / WITHIN (mean per-country over-time partial, each country its own control), non-overlapping 5y windows, **netting libdem level per country** (kills the ceiling/mean-reversion artifact), within-country permutation null.
- **Capacity–mobilization GAP (rol−cso): WITHIN ρ=−0.081 (perm-p=0.0, REAL) while BETWEEN=−0.006 (zero).** A country backslides when its *own* institutions fall behind its *own* mobilization — a within-country dynamic **invisible in the cross-section**. Only the fixed-effects design sees it.
- **Rule-of-law capacity ALONE: within +0.098 → +0.002 (null) after the libdem control** — that was a ceiling artifact. It's the *gap* that carries the within signal, not the level of capacity.
> **Refines Angle 1:** not the *rate* of the gap (velocity, null) but its *level relative to the country's own baseline* (within deviation, real). The relational framing holds at the within-country level, and reveals signal the between-country analysis missed. Caveat: V-Dem-based (libdem control does the de-circularizing); modern independent WGI within-country is underpowered (28y).

### Angle 3 — CONTAGION / neighbour effects → **NULL** (`angle3_contagion.py`)
Does backsliding diffuse across borders? Neighbours' recent Δlibdem → own future backsliding, net of own structure, modern era. **ρ=+0.024 (near zero), inside the label-permutation null. Decisive test — the SPATIAL permutation: real neighbours predict no better than RANDOM neighbours** (random-neighbour mean +0.001; observed inside the [−0.055,+0.061] band).
> **The waves are global zeitgeist, not spatial diffusion.** The rising synchrony (`deep_time` wave R²) reflects *global common shocks* hitting everyone at once (Cold War's end, global economic tides, transnational ideology) — **not** neighbour-to-neighbour spread. Everyone moves together in *time*, not because their *neighbours* pushed them. Scope: tests land-border adjacency only (trade/colonial/linguistic networks untested), modern era.

### Angle 4 — country ATTRIBUTES → **CAPACITY DOMINATES ITS RIVALS** (`angle4_attributes.py`, `country_attrs.py`)
Tested the classic competing explanations for democratic fragility as predictors + moderators, net of the capacity gap + libdem.
- **Main effects — all NULL net of capacity:** resource dependence (ρ=−0.04, "resource curse" doesn't add), ethnic exclusion (+0.01), ethnic #groups (+0.02), population/size (+0.06 borderline). Only `state_age` is real (+0.10) but it's a noisy proxy (V-Dem series start) and confounded.
- **Legal origin — striking raw gradient that is CAPACITY-MEDIATED.** Backslide rate Scandinavian **0%** → German 5.6% → English 7.9% → French 11% → Socialist **12.9%**. But net of the capacity gap + libdem the residuals **collapse to ±0.03** (Socialist +0.034, English −0.024, rest ~0). Legal tradition doesn't cause stability; the capacity those traditions built does.
- **Moderation:** age moderates — the capacity gap predicts backsliding more strongly in *older* democracies (young ones are fragile more capacity-independently). Suggestive (noisy).
> **Capacity is the master variable.** Every standard rival — resource curse, ethnic division, size, legal origin — is either null net of capacity or downstream of it. The capacity/capacity-gap story survives adversarial competition from the usual suspects. Caveats: modern era; legal origin hand-coded (external, best-effort); ethnic is a snapshot; age proxies noisy.

### Angle 5 — SURVIVAL / hazard by democracy age → **front-loaded, but capacity is the robust driver** (`angle5_survival.py`)
Discrete-time breakdown hazard (spell termination), right-censored, 3406 democratic person-years, **52 events**.
- **Descriptively strongly front-loaded:** hazard 0–4y = **0.057/yr** → 40y+ = **0.001/yr** (~50×), monotonic. Young democracies are far more fragile.
- **Capacity is the robust hazard reducer** (logit coef **−1.32**); for gradual *erosion*, controlling for capacity nearly halves the age effect (−0.215→−0.105).
- **Age-per-se is NOT cleanly separable.** The within-country permutation puts the age coef inside its null (perm-p=0.57) — because failed democracies are short-lived, young ages are mechanically over-represented among breakdowns. With 52 events, "young" can't be disentangled from "capacity-poor + structurally short-lived."
> **Consistent with Angle 4: it's capacity, more than age itself, that confers robustness.** "Young democracies are fragile" largely restates "capacity-poor, short-lived democracies are fragile." The front-loading is real and visible but entangled with survival structure. Caveat: 52 events; V-Dem-based capacity.

### Angle 6 — NONLINEAR thresholds → **STRONG (inverted-U; danger in the middle)** (`angle6_nonlinear.py`)
The whole campaign used smooth methods (rank corr, linear logit). Angle 6 finds they **underestimated capacity by ~0.10 AUC.**
- **The capacity→backsliding curve is an INVERTED-U:** backslide rate 2.3% (lowest-capacity decile) → **10.2% (mid, ~decile 5)** → 3.8% (highest). Peak risk at *mid-capacity* (partially-institutionalized/hybrid states); both extremes safe. The capacity-space analog of the anocracy instability curve — and it survives netting out libdem level.
- **Nonlinear beats smooth out-of-sample** (held-out countries): linear AUC **0.632** → **quadratic 0.736 (+0.103)**, threshold-step 0.724.
- **Well-identified capacity "safety ceiling"** ~80th percentile (bootstrap [0.80,0.85], concentrated): above it, backsliding is rare.
> **The biggest untapped signal was the nonlinearity.** Capacity's relationship to rupture is a hump, not a slope — mid-capacity is the danger zone. Every earlier backsliding model (AUC ~0.7) leaves ~0.10 AUC on the table by treating capacity linearly. This sharpens rather than overturns the capacity thesis.

### Capacity arsenal — everything thrown at capacity → **AUC 0.746; signal is nonlinear, not exotic** (`capacity_arsenal.py`)
Exhausted the mathematics of capacity→backsliding (held-out-country AUC, 1900–2015, 239 events): nonlinear, relative, history/multipliers, complex-valued, dynamical eigenvalues, stacked.
- **Capacity alone reaches OOS AUC 0.746** (libdem baseline 0.705; Angle-6 quad 0.734). Capacity, fully exploited, is nearly the whole backsliding story.
- **Strongest single feature: the safety ceiling `I(cap>0.80)` — AUC 0.732, beating libdem itself.** Above the 80th capacity percentile, backsliding is rare. Distance-from-danger-peak `|cap−0.5|` (0.717) also beats libdem. The inverted-U is where the signal lives.
- **History adds a whisper** (+0.012): min-capacity (scar), capacity-debt (time spent weak), volatility.
- **The exotic math is NULL.** The complex representation `z=cap+i·mobilisation` → phase `arg(z)` = 0.571 (worse than useless); dynamical VAR(1) eigenvalues (spectral radius = closeness to instability, oscillation) sit at the null boundary (~0.68, add nothing). Kitchen-sink "EVERYTHING" (0.712) *underperforms* the disciplined nonlinear+history model.
> **Capacity's power is real, strong, and SIMPLE** — an inverted-U with a hard safety ceiling ~80th percentile plus a trace of history. It is NOT hiding in phase space, spectral structure, or complex dynamics. The imaginary number is elegant and empty. The signal was never fancy; it was nonlinear.

**Relational-vs-additive boundary** (`capacity_relational.py`). The arsenal combined capacity features by *additive* stacking; we'd found relational combination superior for *instruments*, so we re-tested. **ADDITIVE 0.746 vs RELATIONAL 0.732 (−0.014)** — relational does NOT beat additive here, and adding the capacity−mobilisation gap makes it worse (0.722). Resolution: **"relational > additive" is scope-limited to combining DIFFERENT instruments** (distinct faces whose *imbalance* is the signal — the founding equation is a ratio of two different things). For transforms of a *single* variable there are no independent faces in tension, so relating them injects noise; additive stacking with nonlinear basis is correct. The arsenal's 0.746 additive result stands, now for the right reason.

## Six-angle synthesis
**Capacity is the master variable, and this is *how* it works:** as a **within-country state deviation** (Angle 2, not a rate — Angle 1), **nonlinearly** with peak risk at mid-capacity (Angle 6), **dominating every rival explanation** (Angle 4) and the **age effect** (Angle 5), and driven by **global common shocks, not neighbour contagion** (Angle 3). Score: 3 real (2,4,6), 1 dominant-null-of-rivals (4), 2 informative nulls (1,3), 1 entangled-partial (5).

## Honest boundaries (the ceiling stands)
- **Regime *change* is near the ceiling for any SINGLE instrument** (all univariate Δ-outcomes \|ρ\|≤0.19) — but the **ensemble stack partially breaks it** (backsliding AUC ~0.7, above). The honest statement is now: *no one tier forecasts regime change; the tiers together do, modestly.* Democratization (the positive direction) stays unforecastable even stacked.
- **T5 and DGS carry no genuine forecast** — their strength is fingerprinting present structure. Matches the audit's "T5 near-chance cross-country."
- These are **robust forward associations under two controls (GDP + AR)**, on a country holdout — *leads to pre-register*, not causal claims. Multiplicity was FDR-controlled but the survivor set is large; treat individual mode-2 hits as candidate registrations.
- Data caveats: DGS iso recovered by population-fingerprint (144 isos); v3_numer omits EPR ethnic-exclusion; T4/T6 use z-sum operationalizations, not the exact published snapshots.

## Files
`COVERAGE_MAP.md` · `build_panels.py`→`predictors.json`/`outcomes.json` · `forward_screen.py`→`screen_discovery.json`/`screen_confirmed.json` · `forecast_test.py`→`forecast_test.json` · `analyze.py`
