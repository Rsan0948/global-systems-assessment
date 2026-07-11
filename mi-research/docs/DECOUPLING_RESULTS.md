# Wealth–Institution Decoupling — Results

**Companion to the frozen pre-registration** `DECOUPLING_PREREGISTRATION.md`
(sha256 `c4b4a24…`, committed before any analysis). Artifacts under
`data/robustness/decoupling/`; code `scripts/robustness/decoupling_*.py`.
Diagnosis only — **no framework changes proposed.**

> **Verdict up front.** The hypothesis that the 150-year institutional-signal
> erosion is explained by a progressive **decoupling of wealth from institutional
> quality** (via industrialization, financialization, and institutional
> reorientation) is **comprehensively not supported.** All eight tests come back
> null, reversed, or — in the one arm that initially looked positive — an artifact
> of decolonization composition. The residual from Finding 9 stays open. The data
> does more than fail to support the hypothesis: on several sub-claims it points the
> **other way** (in the WGI era wealth and institutions *re-coupled*, rich
> countries' institutions *converged*, and institutions remained *people-*
> correlated). Per the pre-registered gate, the hypothesis **fails at the first
> gate (Tests 1–2)**; Tests 3–5 are reported for completeness and reinforce the null.

---

## The gate — is the phenomenon (decoupling) even real?

### Test 1 — P1↔GDP coupling over time — NULL (modern re-coupling); historical "decline" is composition

**Modern MI panel (balanced, N=83).** Pearson r of P1 vs log₁₀(GDP-pc-PPP):

| year | 1996 | 2004 | 2012 | 2018 | 2024 |
|---|---|---|---|---|---|
| r | 0.770 | 0.753 | 0.734 | 0.783 | **0.818** |
| R² | 0.593 | 0.567 | 0.539 | 0.613 | **0.669** |

Trend slope **+0.0016/yr** (p=0.32); Δr(2024−1996) = **+0.047**. The coupling did
**not** weaken — it dipped 1996–2012 then *strengthened* to a period high. Per the
frozen criterion (null if slope ≥ 0), this is a **NULL, in fact mild re-coupling.**
Institutions explain *more* of the variance in wealth in 2024 (R²=0.67) than in 1996
(R²=0.59). Identical pattern on the all-available sensitivity universe.

**Historical panel (V-Dem rule-of-law vs log Maddison GDP, 1850–1970).** The pooled
common set *does* show a decline — r 0.713→0.829(1880)→0.744→0.595→0.522, Δr=−0.191,
slope −0.0021/yr (p=0.106) — the only arm that looked positive. **It does not
survive a composition control** (`t1_historical_robust.json`):

| sample | 1850 | 1880 | 1910 | 1940 | 1970 | Δr |
|---|---|---|---|---|---|---|
| **Full common set** (n grows 34→141) | 0.713 | 0.829 | 0.744 | 0.595 | 0.522 | **−0.191** |
| **Balanced** (same 25 polities all anchors) | 0.629 | 0.806 | 0.886 | 0.847 | 0.872 | **+0.243** |
| **Mature-only** (Finding 9-A classes) | 0.726 | 0.781 | 0.867 | 0.691 | 0.756 | **+0.03** (p=0.91) |

The 1970 anchor's sample **doubles** (n=57→141) as post-colonial states enter — and
those low-GDP, institutionally-variable states loosen the *pooled* correlation. On a
**constant** set of polities the coupling *rises* (Δr=+0.24); on **mature** states it
is flat. The historical "decoupling" is the **decolonization composition effect**
Finding 9-A already isolated — not a within-polity weakening of the wealth↔
institution link. **T1 verdict: NULL** (modern), **composition artifact**
(historical). *The mechanism was pre-registered to be lagged/systemic, not
country-level; it was tested at the system level and the system did not decouple.*

### Test 2 — Institutional variance at income levels — NULL / reversed (rich-country convergence)

SD of P1 within the **top income quartile** of the balanced panel:

| year | 1996 | 2004 | 2012 | 2018 | 2024 |
|---|---|---|---|---|---|
| top-quartile SD(P1) | 0.137 | 0.139 | 0.143 | 0.092 | **0.069** |
| bottom-quartile SD(P1) | 0.096 | 0.089 | 0.095 | 0.095 | 0.110 |

Top-quartile dispersion **narrowed** (Δ=−0.068, slope −0.0025/yr) — the exact
*opposite* of the hypothesis (which predicted *widening*: "you can be rich with an
increasingly wide range of institutional quality"). Rich countries cluster **more**
tightly around high P1 in 2024 than in 1996. Bottom-quartile dispersion is flat
(Δ=+0.014, below the 0.02 floor). **T2 verdict: NULL, reversed** — no
"rich-with-weak-institutions" spreading; if anything institutional **convergence**
among the wealthy (plausibly WGI variance-compression as formal-legal institutions
diffuse — a Finding-9 candidate residual, not decoupling).

> **Gate result:** Tests 1 and 2 are both null (and mildly anti-hypothesis). Under
> the frozen gate the decoupling **phenomenon is not established**; the erosion's
> cause remains open. Tests 3–5 below cannot rescue a phenomenon that does not
> appear, and they don't.

---

## The channels — industrialization & financialization

### Test 3 — Economic composition moderates the signal — NULL / reversed

Split the 2004/2012 holdout by institution-light share (`resource_rents` +
`manufacturing` %GDP). Institutional signal edge = neg-P1 AUC − wealth AUC, by group:

| window | group | crisis edge | dysfunction edge |
|---|---|---|---|
| 2004 | H (institution-heavy) | −0.040 | −0.035 |
| 2004 | L (institution-light) | +0.047 | +0.120 |
| 2012 | H | +0.024 | +0.092 |
| 2012 | L | +0.027 | +0.075 |

**H−L signal edge:** 2004 = −0.087 (crisis) / −0.155 (dysf); 2012 = −0.003 / +0.017.
Predicted ≥ +0.05 (signal stronger in institution-heavy economies). Observed:
**≈0 or reversed** — in 2004 the institutional signal is actually *stronger* in
institution-light economies. Median institution-light share is **flat** across the
window (19.0%→18.9%), so there is no compositional shift toward institution-light
production either. **T3 verdict: NULL** (2012) / reversed (2004). Sector type does
not mediate the institutional relationship in the predicted direction.

### Test 4 — Financial depth moderates the signal — NULL on the primary outcome

Logistic M3 (crisis ~ neg-P1 + findepth + neg-P1×findepth) on the holdout. The
financialization prediction is a **negative** interaction (institutions matter less
where finance is deep):

| window | outcome | interaction coef | reading |
|---|---|---|---|
| 2004 | crisis (primary) | **+0.359** | positive → null |
| 2004 | dysfunction | −0.062 | negative but negligible |
| 2012 | crisis (primary) | **+0.031** | positive → null |
| 2012 | dysfunction | −0.317 | negative (only meaningful case) |

On the **pre-registered primary outcome (crisis)** the interaction is **positive in
both windows** — the opposite of financialization (consistent with Finding 3: the
crisis outcome is capital-coupled, so institutions co-move with wealth there). A
negative interaction appears only on the secondary dysfunction outcome, and
materially only in 2012. **Not robust. T4 verdict: NULL** on the primary test; a
lone weak negative on one secondary window is not the mechanism.

**Honest bound (the ingredient is real).** System financial depth *did* rise across
the balanced panel — 35.7→43.8→50.4→50.2→54.2 %GDP (1996→2024). Financialization
happened; it simply does not measurably weaken the institutional signal. (Echoes
Finding 8: a measured capital/support variable does not recover or suppress the
signal.)

---

## The mechanism — institutional reorientation from people to capital

### Test 5A — P1↔P3 (human-capital) decoupling — NULL

Pearson r(P1, P3): 0.772 → 0.791 → 0.783 → 0.780 → **0.813** (Δ=+0.041, rising).
Predicted *declining* (institutions less people-oriented). Observed **stable-to-
rising**. Well-governed states invest in their people as reliably as ever.
**NULL, reversed.**

### Test 5B — P1↔P4 tightening — NULL once GDP is removed

r(P1, P4) rises 0.717→0.818 (Δ=+0.101) — *looks* like reorientation toward capital.
But P4 **contains normalized GDP**, so this just re-expresses the Test-1 P1↔GDP
re-coupling. The **GDP-decontaminated** P4\* (resource-rents + ODA only) goes the
**other way**: r(P1, P4\*) = 0.561→0.511→0.447→0.482 (slope −0.0043/yr). The apparent
"tightening" is an artifact of the GDP component. **NULL for reorientation.**

### Test 5C — Direct people- vs capital-orientation — NULL / reversed

r(P1, people-orientation) and r(P1, capital-orientation) [WDI indices; social-
protection unavailable so people = edu+health, per prereg]:

| year | 2004 | 2012 | 2018 | 2024 |
|---|---|---|---|---|
| P1 ↔ people | 0.742 | 0.674 | 0.671 | 0.650 |
| P1 ↔ capital | 0.620 | 0.624 | 0.578 | 0.449 |

(1996 dropped — health coverage n=50.) Predicted: capital-corr **up**, people-corr
**down**. Observed: from 2004 on **both decline**, and **capital declines faster**
(−0.17 vs −0.09) — the reverse of the prediction. By 2024 P1 tracks people-
orientation (0.65) *more* than capital-orientation (0.45). **NULL, reversed.**
V-Dem state-ownership/welfare indices were **not run** (no compact offline source;
pre-registered as best-effort — WDI is the primary 5C instrument, and it is clean).

### Test 5D — Washington-Consensus (1979) inflection — no break (gradual macro trend only)

Cross-country mean spending, 1970–2020:

| year | 1970 | 1980 | 1990 | 2000 | 2010 | 2020 |
|---|---|---|---|---|---|---|
| education %GDP | 3.56 | 4.14 | 3.78 | 4.14 | 4.41 | 4.54 |
| capital metrics (trade+FDI+credit) | 25.8 | 32.6 | 35.4 | 40.1 | 52.4 | 47.2 |

Education spending **rises gently** through and past 1979 — no downshift. Capital
metrics rise **smoothly** (~2×) with **no discrete 1979–85 inflection** (consistent
with Finding 9-B: a single linear trend beats every broken-stick break). In relative
terms capital-orientation *did* outgrow people-orientation over 50 years — a real,
**gradual** macro fact — but (i) there is no policy-timed break, and (ii) it does
**not** appear in the P1↔orientation *relationship* (5C is null/reversed). Public-
health data begins ~2000, so pre-2000 people-spending is education-only:
**coverage-bounded** as pre-registered. **NULL** on the policy-inflection claim.

---

## Synthesis

| test | what it measures | result | supports hypothesis? |
|---|---|---|---|
| **1** P1–GDP coupling | is wealth decoupling from institutions? | modern **re-couples** (Δr +0.05, R² 0.59→0.67); historical decline is **composition** (vanishes on constant/mature sample) | **No** |
| **2** variance at income | can you be rich with bad institutions? | top-quartile P1 dispersion **narrows** (0.137→0.069) | **No (reversed)** |
| **3** economic composition | does sector type moderate the signal? | H−L signal edge ≈0 / reversed; light-share flat | **No** |
| **4** financial depth | does financialization weaken the signal? | primary-outcome interaction **positive** both windows; findepth rose 36→54%GDP but no moderation | **No** |
| **5A** P1–P3 decoupling | are institutions less people-oriented? | r stable-to-rising (0.77→0.81) | **No (reversed)** |
| **5B** P1–P4 tightening | are institutions more capital-oriented? | rise is a GDP artifact; GDP-clean P4\* **declines** | **No** |
| **5C** direct orientation | which master do institutions serve? | P1↔capital falls *faster* than P1↔people | **No (reversed)** |
| **5D** 1979 inflection | did policy drive reorientation? | no discrete break; gradual macro trend only | **No** |

**Interpretation (per the frozen guide).** Tests 1–2 are null → the decoupling
**phenomenon fails at the first gate**. The proposed channels (3–4) and mechanism
(5A–5D) independently return null, so this is not "phenomenon real, mechanisms
wrong" — the phenomenon itself does not appear in the data at the system level the
hypothesis specified. The elegant three-force story (industrialization →
financialization → institutional reorientation, each reinforcing the others across
150 years) is **falsified as an explanation of the erosion**, in the specific and
falsifiable form pre-registered.

**What the data actively shows instead (all *anti*-decoupling).**
1. In the WGI era (1996–2024) wealth and institutions **re-coupled** (r 0.77→0.82,
   R² 0.59→0.67) rather than decoupled.
2. Rich countries' institutions **converged** (top-quartile P1 SD 0.137→0.069), the
   opposite of "rich with an increasingly wide range of governance."
3. Institutions remain **people-correlated** (P1↔P3 stable-to-rising; P1↔people ≥
   P1↔capital by 2024).
4. Once decolonization composition is controlled, historical wealth↔institution
   coupling is **stable or rising**, not eroding.

These are consistent with a **measurement-maturation / variance-compression** reading
(WGI perception increasingly anchored on observable state capacity as formal-legal
institutions diffused) — which is Finding 9's *candidate residual #3*, explicitly
**not** in the decoupling family and **not tested here**. It remains a hypothesis for
separate pre-registration.

**Bottom line.** Finding 9 left the 150-year erosion's cause open with a ~100%
residual. This program tested the most structurally compelling candidate for that
residual — wealth genuinely decoupling from institutions — and it **does not hold**.
The residual is not closed; it is now **better bounded**: the erosion is not
composition (9-A), not consequence-elimination (9-B), not perception-lag (9-C), not
external support (Finding 8), and **not wealth–institution decoupling** (this
program). The strongest surviving leads are the ones this test *incidentally
strengthened by elimination*: measurement-regime maturation (variance compression /
perception re-anchoring on wealth), and the change in the *character* of the conflict
outcome across the period — both flagged in Finding 9 and both awaiting their own
frozen pre-registration.

## Artifacts

- Code: `scripts/robustness/decoupling_{panel,fetch,t1_t2,t1_hist_robust,t3_t4,t5}.py`
- Data: `data/robustness/decoupling/{mi_5pt_panel,wdi_decoupling,t1_coupling,
  t1_historical_robust,t2_variance,t3_composition,t4_financial,t5_reorientation}.json`
- Pre-registration: `docs/DECOUPLING_PREREGISTRATION.md` (frozen, sha256 `c4b4a24…`)
