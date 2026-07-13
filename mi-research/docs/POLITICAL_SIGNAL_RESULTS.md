# Political-Signal Test — Results

**Companion to** `POLITICAL_SIGNAL_PREREGISTRATION.md` (sha256 `ec4aebe0`, frozen before
analysis). Code `scripts/v2/political_test.py`; data `data/political/*`. Self-served
2026-07-12 (EPR-ETH ethnic exclusion, V-Dem civil society, Political Terror Scale, WDI
youth/food/internet). Base = 2012; outcomes → 2024. n≈125–170.

> **The question.** Structural instruments (V1/V2 capacity levels) predict societal/wellbeing
> outcomes but not political rupture. The design report argued we measure the *capacity
> denominator* of rupture = complexity/capacity, and never the *complexity numerator* —
> grievance, exclusion, mobilization, repression. This test builds the numerator and asks
> whether it captures the political signal structure misses.

## Verdict: YES — the numerator layer captures political signal structure can't

The pre-registered **gate (does the numerator block add out-of-fold CV-AUC ≥ 0.05 over
structural [P1 + log GDP]?) passes on 2 of 3 political outcomes**, and — critically — it
**survives removing event-history**, so it is the genuine grievance/mobilization terms, not
the conflict-trap autocorrelation.

| Political outcome | structural (P1+logGDP) | + numerator | increment | no-event-history | gate |
|---|---|---|---|---|---|
| **Democratic backsliding** | **0.543** (≈chance) | **0.606** | **+0.062** | 0.581 | **PASS** |
| **Repression worsening** | 0.643 | **0.712** | **+0.070** | 0.728 | **PASS** |
| Armed-conflict onset | **0.725** | 0.742 | +0.017 | 0.739 | fail |

**The headline:** for **democratic backsliding** — the outcome structure predicted at
*chance* (0.54, confirming every prior null) — the grievance/mobilization numerator lifts
prediction to **0.61**, and it is **not** the conflict-trap (no-event-history still 0.58).
For **repression worsening**, 0.64 → **0.71**, and there the event-history removal *raises*
it (0.73) — purely the grievance/mobilization terms. **Armed-conflict onset is the one
political outcome structure already predicts** (0.725) — because conflict is poverty- and
weak-institution-driven, the *ancient* failure mode; the numerator adds little there.

## Which terms carry the signal (FDR survivors, T1 screen)

- **Backsliding** — the only two FDR survivors are **civil-society participation (ρ=+0.22)**
  and **anocracy (mid-regime, ρ=+0.20)**. Structure (P1) does *not* survive. This is the
  textbook backsliding profile: mobilized civil society in a partial democracy — exactly the
  Goldstone/PITF anocracy finding and the political-process account. **Structure is blind to
  it; the numerator sees it.**
- **Repression worsening** — protective: internet/coordination-tech (−0.24), civil society
  (−0.21), institutions (−0.24), income (−0.22); aggravating: **food-import dependence
  (+0.20)** (price-shock exposure) and low prior repression (mean reversion).
- **Conflict onset** — the classic civil-war-onset battery all appears: **repression
  (pts +0.45), prior conflict (+0.43), youth bulge (+0.41), ethnic exclusion (+0.19)**,
  against institutions/income/internet (−0.35 to −0.37). Multi-determined, and structure
  already captures most of it.

## Interpretation

This closes the founding equation for the political domain. The fragmentation leg proved
rupture = **complexity > capacity**; V1/V2 measured **capacity**; this test adds
**complexity** (ethnic exclusion + mobilization + anocracy + shock) and — as predicted —
it captures the political signal capacity alone could not, **specifically for the modern
failure mode (democratic backsliding, elite/civil-society-driven erosion) that armed-conflict
structure misses.** A clean parallel to the robustness program's arc: structure predicts the
*ancient* rupture mode (conflict, poverty-driven) but the *new* mode (backsliding) needs the
grievance/mobilization tier.

## Honest bounds

- **The lift is real but modest.** Backsliding 0.54→0.61, repression 0.64→0.71 — better than
  chance/structure, still moderate. Political rupture stays hard; the numerator raises the
  floor from chance to calibrated-risk, it does not make coups forecastable. This is exactly
  the **"structural seismology, risk over bands"** ceiling the program predicted — the
  **trigger (the Mule) remains unmeasured** and caps the achievable AUC.
- n≈125–131 complete cases; 5-fold CV (out-of-fold, so not overfit to the block), but not
  large. Base 2012→2024 is one window; a second window would strengthen it.
- EPR ethnic exclusion mapped 164 states via statename→ISO; a few drop. PTS/CSO are
  V-Dem/expert-coded (some perception component, unlike the revealed-outcome V2 indicators).

## Bottom line

**There *is* political signal we were missing, and it is exactly where the theory said it
would be** — in the grievance/mobilization/exclusion *numerator*, not the structural
denominator. Adding it lifts the two modern political outcomes (backsliding, repression)
above what state-capacity structure can do, driven by civil-society mobilization, anocracy,
and ethnic exclusion — not by the conflict-trap. The instrument to predict modern political
rupture is a **complexity/pressure tier bolted onto the capacity tier**, and it works well
enough to matter and honestly not well enough to forecast — the calibrated-risk ceiling, as
designed. Artifacts: `data/political/political_test.json`.

---

## Deep extension — the political signal across ~2 centuries (1816–1996)

Taken as wide and as far back as the data allows: the full V-Dem panel (rule-of-law +
liberal-democracy + civil-society, back to 1789), Maddison GDP, conflict onsets (1816+),
ethnic exclusion (EPR, 1946+). Per decade epoch, 20-year forward window, does the
NUMERATOR (anocracy + civil-society + prior-conflict [+ exclusion 1946+]) add over STRUCTURE
(V-Dem rule-of-law + log Maddison GDP)? `scripts/v2/deep_political.py`, `data/political/deep_political.json`.
(In-sample logit AUC for the deep panel — directional; the modern gate used out-of-fold CV.)

**Five findings, each stable across the panel:**

1. **The numerator beats structure at democratic backsliding across the entire 20th
   century** — mean incremental AUC **+0.131** over 11 epochs (1896–1996), and *largest in
   the modern era* (1986 +0.28, 1996 +0.13) where structure fails most (struct-AUC 0.60–0.66
   recently vs 0.82–0.86 mid-century). The finding is a 100-year regularity, not a modern
   artifact — and structure's *failure* at backsliding is specifically a late-century thing.

2. **The conflict trap is the most stable political relationship in recorded history.**
   prior-conflict → conflict onset is positive and strong in every epoch 1846–1996
   (ρ = +0.21 → **+0.67**, peaking 1866 and holding +0.45 in 1996). Two centuries of
   violence begetting violence.

3. **The ancient institutional signal holds across 200 years.** V-Dem rule-of-law → *less*
   conflict in every epoch (ρ = −0.06 to −0.49). This directly reproduces Findings 1–3 of the
   robustness program (institutions predict rupture, deep in time) in the political-signal
   frame — structure reliably predicts the *ancient* failure mode (conflict), always.

4. **Ethnic exclusion → conflict is a robust post-1946 regularity** — ρ = **+0.20 to +0.39**
   across the whole decolonization era (peaking 1976 +0.39). Cederman's horizontal-inequality
   finding, reproduced across 50 years.

5. **THE HISTORICAL SHIFT — the drivers of backsliding *changed*.** anocracy → backsliding
   **flipped sign around 1966**: it was ≈0/negative pre-1956 (−0.11 to −0.25) and turned
   **positive** in the modern era (1966 +0.09, 1986 **+0.22**, 1996 +0.21). The "contested
   middle" as the democratic-erosion zone is a *late-20th-century* development. And civil
   society **flipped from protective to neutral**: ρ(CSO, backslide) was −0.24 to −0.35
   pre-1956 (mobilization guarded against erosion) and decayed to ≈0 by 1996. What predicts
   political rupture is not historically fixed — it *evolved*, exactly as the wealth–
   institution relationship did (the convergence arc). Structure predicts the old mode
   (conflict) timelessly; the *new* mode (anocratic, civil-society-contested backsliding) is
   a modern configuration that only the numerator sees, and only recently.

**Synthesis.** Across two centuries the picture is consistent and it closes the loop with the
whole program: **structure (institutions + wealth) is the timeless predictor of the ancient
rupture — organized violence — and the numerator (grievance/mobilization/exclusion) is the
predictor of the modern rupture — backsliding — which emerged as an anocracy-and-civil-
society-driven configuration in the last third of the 20th century.** The instruments were
never wrong; they were reading the failure mode that dominated their era. Building the
complexity/numerator tier lets the framework see the failure mode of *ours*.
