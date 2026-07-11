# Inequality as the Missing Distribution Dimension — Results

**Companion to** `INEQUALITY_PREREGISTRATION.md` (sha256 `8c0236a…`, frozen before
analysis). Artifacts `data/robustness/inequality/`; code
`scripts/robustness/inequality_{fetch,t1_t2_gate,t3_t6}.py`. Diagnosis only — **no
framework changes** (Test 6 exploratory; P6 **not** adopted).

> **Verdict: registered null (the 13th). Inequality is a real bivariate correlate of
> domestic instability but is NOT the erosion mechanism.** The gate split — inequality
> has a cross-sectional association with domestic crises (arm A, p=0.0001), but the
> longitudinal arm **fails and reverses** (arm B): the domestic-channel erosion moves
> *with* top-income concentration over the century (Pearson **+0.85**), not against it,
> and the mid-century Great Compression produced **no** signal recovery. Every mechanism
> test (P1 recovery, interaction, mature-state moderation, partial-correlation
> resolution, P6 lift) is null. The hypothesis does not explain the erosion.

---

## Test 1 — Does inequality predict domestic crises? (GATE arm A) — bivariate yes, mechanism no

Logistic on the holdout, outcome = domestic-origin crisis (Finding-12 classification):

| window | M2 ineq-only (coef / AUC / p) | M1→M3 P1 recovery | M4 interaction |
|---|---|---|---|
| 2004 (n=63, base 0.40) | 1.12 / 0.79 / **p=0.0001** | **−0.03** (no recovery) | +0.33 (positive, null) |
| 2012 (n=72, base 0.29) | 0.76 / 0.72 / p=0.006 | −0.02 (no recovery) | +0.01 (null) |

Inequality (top-10% share) **is a significant bivariate predictor** of domestic crises
— but this is the unsurprising fact that poor, unstable states are unequal (its AUC 0.79
does **not** beat GDP-only 0.84). The two *mechanism* signatures both fail: the P1
coefficient **does not recover** when inequality is controlled (M1→M3 ≈ 0), and the
M4 interaction is **positive**, not the predicted negative (good institutions are **not**
shown to "protect less" under high inequality). Arm A passes the letter of the gate
("inequality has signal") but not its mechanism.

## Test 2 — Does the domestic erosion track inequality over time? (GATE arm B) — FAILS, reversed

Finding-12 domestic-channel spread vs mean WID top-10% share (major economies) by epoch:

| epoch | 1916 | 1936 | 1956 | 1976 | 1996 |
|---|---|---|---|---|---|
| domestic spread | 0.135 | 0.109 | 0.056 | −0.013 | −0.025 |
| top-10% (majors) | 47.6 | 41.2 | 33.6 | 30.1 | 35.6 |

**Correlation = +0.85 (p=0.008) — positive, the reverse of the predicted negative.**
Inequality and the domestic signal **fell together** across the 20th century. The
Piketty-U fingerprint is **absent**: during the 1914–1980 Great Compression (top-10%
47→30) the domestic signal **kept eroding** (0.135→−0.013) instead of recovering; the
compression-era mean spread (0.066) is *lower* than the high-inequality pre-1914 tail
(0.092). This is the sharpest disconfirmation — the natural experiment the hypothesis
most relied on (mid-century compression → signal recovery) shows the opposite. **Arm B
fails.**

**Gate = split** (arm A weak-pass, arm B fail). Per the frozen rule, proceed to Tests
3–6 with caution; they resolve the split decisively toward null.

## Test 3 — Inequality within mature states — REFUTES moderation

Split mature states (F9-A) at the median top-10%; neg-P1 AUC over domestic crises:

| window | low-inequality mature | high-inequality mature |
|---|---|---|
| 2004 | n=16, **0 crises** (AUC undefined) | n=15, 5 crises, **neg-P1 AUC 0.88** |
| 2012 | n=17, **0 crises** | n=16, 4 crises, **neg-P1 AUC 0.79** |

The hypothesis predicted the signal **weak** in high-inequality mature states (inequality
breaks it). Instead the signal is **strong** there (AUC 0.79–0.88), and low-inequality
mature states (Nordics etc.) simply had **no domestic crises to predict**. So inequality
*sorts which mature states have crises* (a bivariate association) but **does not weaken
the institutional signal** — it is intact precisely where the hypothesis said it should
have broken. **Refutes the moderation claim.**

## Test 4 — Does controlling inequality resolve F10-vs-F12? — NO

Raw vs inequality-partialled P1↔domestic-stability correlation:

| window | raw r | partial r (\|inequality) |
|---|---|---|
| 2004 | +0.606 | +0.507 |
| 2012 | +0.471 | +0.408 |

Controlling for inequality **lowers** the P1↔stability correlation (inequality shares
some of P1's variance), rather than **preserving/recovering** it. Inequality is not the
missing variable that would keep the institutional signal intact once distribution is
accounted for. **The F10-vs-F12 contradiction is not resolved.**

## Test 5 — Long-run (deep subset) — underpowered, wrong sign

Finding-7 all-crisis spread vs deep-subset (US, FR, SE, IN, RU, GB, DE) mean top-10%:
Pearson **+0.51, p=0.20** (3–7 countries; underpowered). Same reversed direction as
Test 2, not significant. No support.

## Test 6 — Exploratory P6 distribution pillar — adds nothing (EXPLORATORY)

P6 = 1 − normalized top-10% share, equal-weight sixth pillar, 2024. Domestic-crisis
discrimination: **5-pillar AUC 0.882 → 6-pillar AUC 0.884** (+0.002, negligible).
Country movers are directionally sensible (USA −0.039, ARE −0.045; Sweden +0.017, Norway
+0.017) — but **Afghanistan, Ethiopia, Nigeria, Guinea-Bissau *rise* with P6**, because
low *measured* top-10% share does not imply stability in conflict-ridden states. That is
precisely why a distribution pillar does not improve domestic prediction. **Exploratory
— P6 is not adopted; not a confirmed improvement.**

---

## Synthesis

| test | prediction if correct | result | supports? |
|---|---|---|---|
| 1 inequality predicts domestic crises | significant + P1 recovers | significant (p=0.0001) but **no P1 recovery**, interaction positive | bivariate only |
| 2 tracks erosion over time | negative corr, Piketty-U | **+0.85** (reversed); no U-fingerprint | **No** |
| 3 within mature states | signal weak where inequality high | signal **strong** (AUC 0.88) where inequality high | **No (refuted)** |
| 4 resolves F10-vs-F12 | partial corr stable/rising | partial **< raw** | **No** |
| 5 long-run | correlation holds across span | +0.51, p=0.20 | **No** |
| 6 P6 exploratory | 6-pillar beats 5-pillar | 0.882 → 0.884 | **No** |

**Interpretation.** Inequality has a genuine but modest **cross-sectional** association
with domestic instability — poor, unstable states are unequal — but it is **not** the
mechanism that severs institution→stability while preserving institution→wealth. It does
not recover the institutional signal (T1/T4), does not moderate it (T3), does not track
the longitudinal erosion (T2, reversed), and adds nothing as a distribution pillar (T6).
The single most decisive result is the **mid-century Great Compression**: the one period
where the hypothesis makes a sharp, differentiated prediction (falling inequality →
recovering signal), the domestic signal **kept eroding**, and inequality and the signal
**fell together** (+0.85) rather than trading off.

## Bottom line

The **thirteenth** hypothesis to fail on the longitudinal erosion. The constraint
profile is now even tighter — the driver is **continuous** (F11), sits in the
**domestic** channel (F12), coexists with **strengthening** P1↔GDP (F10), operates
**within mature states** (F9-A), and is invisible to WGI, to P3, **and to income
distribution** (F13). Whatever severs the institution→domestic-stability link is not
external support, monetary regime, systemic contagion, or wealth concentration. The two
Finding-9 residuals of the right shape remain the standing leads, now with one added
constraint apiece: (i) **measurement-regime maturation / V-Dem rule-of-law variance
compression** — note it must co-move with the 20th-century *decline* in top-income
concentration, since both fell together; (ii) the **secular change in post-colonial
civil-conflict character** relative to measured rule-of-law. Both remain untested and
are the right next pre-registrations. The phenomenon stands as the most precisely
bounded open question in the program: real, smooth, monotone, domestic, and — after
thirteen adversarial tests — uncaused.

## Artifacts

- Code: `scripts/robustness/inequality_{fetch,t1_t2_gate,t3_t6}.py`
- Data: `data/robustness/inequality/{inequality,t1_signal,t2_longitudinal,t3_t6}.json`
- Pre-registration: `docs/INEQUALITY_PREREGISTRATION.md` (frozen, sha256 `8c0236a…`)
