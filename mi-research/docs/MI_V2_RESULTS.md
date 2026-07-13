# Modernization Index V2 — Functional Conversion — Results

**Companion to** `MI_V2_PREREGISTRATION.md` (sha256 `93c87741`, frozen before any hypothesis
was run). Engine `scripts/v2/v2_engine.py`; hypotheses `scripts/v2/v2_hypotheses.py`; data
`data/v2/{v2_indicators,v2_scores,v2_hypotheses}.json`. Fetched live 2026-07-12.

> **V2 is a new instrument with zero inherited validation.** It measures *function*
> (conversion of capacity into citizen outcomes, and for whom) — not *state* (V1). It makes
> no pre-modern claims. This is its first, honest, self-earned validation pass.

---

## ⟐ Authoritative-data update (2026-07-12) — read this first

The initial pass ran on proxy equity (income-Gini) and a WDI/conflict outcome. The three
blocking datasets were then obtained and ingested (`scripts/v2/ingest_manual.py`):
**IMF WEO Apr-2025** (real primary balance + gross debt → F1, 188/194 countries),
**PISA 2022 ESCS socio-economic score gaps** (real developed-country education equity, 57
countries — fetched through stat.link), and **LIS Key Figures** (disposable-income Gini +
P90/P10, 49 countries). F2 equity is now **real (non-proxy) for 132 countries** (DHS
quintiles for the developing world + PISA for the rich world), and a **democratic-
backsliding outcome** (V-Dem liberal-democracy decline 2004→2024) was added as the
rich-democracy-sensitive stress measure conflict-onset misses.

**What changed, and what didn't:**
- **H4 (construct validity) still PASSES** on the authoritative data (cross-model ρ: Level
  0.965 / Equity 0.960 / Combined 0.962). V2 is a real construct.
- **The continuous equity tests stay NULL on both outcomes.** V2-Equity adds +0.01 (conflict)
  / −0.006 (backsliding) over V1+V2-Level. Real equity data did **not** make the linear
  equity signal appear. V1 (AUC 0.807) still dominates conflict; **nothing predicts
  backsliding linearly** (V1 itself only 0.53 — democratic erosion is not a capacity failure).
- **H6 (the configurational headline) CONFIRMS on backsliding, and the real data *sharpened*
  it.** Backslide rate by quadrant: **HL-LE 0.50 > LL-LE 0.32 > HL-HE 0.30 > LL-HE 0.19** —
  exactly the pre-registered ordering: *capability + inequality (the "American configuration")
  is the most democratic-erosion-prone; capability + equity and incapability + equity are the
  most stable.* The upgrade from proxy to real equity moved HL-LE-vs-LL-HE from 0.44/0.25 to
  **0.50/0.19** (a 2.6× gap). **But it is underpowered — n=16 per off-diagonal quadrant,
  Fisher p≈0.14 — a large effect that does not reach significance.** On the *conflict* outcome
  H6 does not hold (HL-LE 0.54 < LL-HE 0.62), consistent with the thesis being about
  legitimacy/erosion, not armed conflict.

**Two artifacts found on inspection of the actual country-level data — both material:**
- **Authoritarian-equity inflation.** Because DHS/PISA equity is absent for closed states,
  their equity runs on income-Gini, and *managed-economy official Gini is low* — so
  repressive states score spuriously high on equity/conversion: **Belarus (equity 100),
  UAE (95), Jordan (100), Turkmenistan (96), Syria (92)**. These pad the top of the ranking
  and the "converts above its structure" list (Syria V2 68 vs V1 36; Belarus 82 vs 61). The
  equity dimension is **gameable by authoritarian statistics** — a real flaw.
- **Backsliding floor effect.** The LL-HE ("equal but incapable") quadrant looked unusually
  stable (0.19 backslide) partly because it contained states that were *already autocracies
  with no liberal democracy left to lose* (Turkmenistan, Syria, Kazakhstan, Algeria, Iraq) —
  they mechanically can't backslide.

**H6 re-run controlling the floor effect (`scripts/v2/v2_h6_clean.py`) — the signal does NOT
survive.** Restricting to countries with a real democracy to lose in 2004 (libdem ≥ 0.25),
LL-HE's backslide rate **jumps from 0.19 to 0.40** (the floored autocracies removed), and the
HL-LE-vs-LL-HE contrast goes from Fisher **p=0.068 → p=0.50**. Across the sensitivity grid
(libdem₂₀₀₄ ≥ 0.25/0.3/0.4) the quadrants compress to HL-LE 0.54 / LL-LE 0.39 / HL-HE 0.34 /
LL-HE 0.40 — **HL-LE stays numerically highest but is statistically indistinguishable from
the rest** (HL-LE-vs-rest p=0.17–0.28). And on the diagonal, **HL-HE (high-equity, capable)
backslid at 30% including the worst cases in the dataset — Hungary (−0.43), Poland (−0.20),
Greece, Germany, Italy, Spain** — so "equity protects" is directly contradicted.

**Refined verdict (final for this pass):** the equity thesis is **not supported once its two
artifacts are controlled.** The apparent HL-LE signal was substantially a floor effect
(already-autocratic states padding the LL-HE "stable" count), and the equity dimension itself
is inflated for closed states. What survives is weak and honest: HL-LE (capable + unequal) is
the *numerically* most backsliding-prone quadrant in every cut, but the clean comparison is
**null (p≈0.5)**, and high-equity capable states (Hungary, Poland) backslide as hard as any.
So V2 earns **construct validity (H4) and a genuine US/Botswana/Namibia diagnostic**, but its
central distributional claim — that unequal delivery from a capable system is what drives the
stress V1 can't explain — **is not established**, and its equity dimension needs
authoritarian-robust indicators before it can be trusted. The authoritative data removed the
"untestable" excuse and the answer, honestly, is: **the equity thesis does not hold in the
data as measured.** Everything below is the original proxy-data pass, retained for record.

---

## Verdict in one paragraph

**V2 is a real construct that mostly fails to justify itself as a predictor — and the
single most important reason is a data gap, stated plainly.** The construct-validity gate
(H4) **passes cleanly**: the six functional pillars compose into one coherent score across
three independent weighting schemes (cross-model Spearman ρ ≥ 0.96 for Level, ≥ 0.98 for
Equity and Combined) — V2 measures *something* single and stable. But every predictive
hypothesis is **null or near-null**: pillar balance adds nothing (H1), the V1−V2 gap does
not beat V1 alone and the equity gap is *not* the stronger half (H3), V2-Equity adds
**+0.004 AUC** over V1+V2-Level (H5), and the headline HL-LE configuration shows **exactly
the same** domestic-stress rate as LL-HE (H6, both 0.60). **V1 alone (AUC 0.807) dominates
everything V2 offers.** The honest cause is twofold and disqualifying for the equity thesis
specifically: (1) the real distributional data (DHS wealth-quintile) exists **only for
developing countries**, so every rich country — including the US showcase — runs its equity
dimension on an income-Gini *proxy*; and (2) the committed outcome (armed-conflict onset)
does not capture the populism/legitimacy stress the equity thesis is about, and is nearly
empty for rich democracies. So the equity-drives-instability claim was **not refuted so much
as left untestable where it mattered**, and comes back null in the data that does exist. What
survives: **construct validity, a modest independent signal in V2-Level (health/fiscal
conversion), the protective HL-HE quadrant, and an illuminating US case.**

---

## H4 — Cross-model construct validity (GATE) — **PASS**

Pairwise Spearman ρ across weighting schemes V2a (equal), V2b (correlation-derived), V2c
(analyst), computed **separately** for Level, Equity, Combined:

| dimension | a~b | a~c | b~c | min ρ | n |
|---|---|---|---|---|---|
| **Level** | 0.986 | 0.986 | 0.957 | **0.957** | 116 |
| **Equity** | 0.987 | 0.994 | 0.984 | **0.984** | 71 |
| **Combined** | 0.993 | 0.993 | 0.979 | **0.979** | 116 |

All ≥ 0.95. **V2 is a single coherent construct on all three dimensions** — the equity
dimension in particular composes tightly (ρ ≥ 0.98), so V2-Equity is a real composite, not a
loose profile of independent facets. This matches (a touch below) V1's ρ ≥ 0.99 standard.
Gate passes; predictive tests proceed. *(Caveat: the Equity n=71 is the developing-country
subset with real quintile data; see coverage.)*

## H1 — Pillar balance beyond level — **NULL**

Spread (SD of pillar scores) AUC = 0.49 (chance); V2-Combined + spread (0.618) **< V2-Combined
alone** (0.624). Unlike V1's validated configuration thesis, **V2 pillar *balance* carries no
predictive signal** for domestic stress. Reported as a clean null.

## H3 — The V1−V2 gap, decomposed — **NULL (and reversed)**

| predictor | AUC |
|---|---|
| V1 only | **0.807** |
| V2-Combined only | 0.624 |
| V1−V2-Level gap | 0.632 |
| V1−V2-Equity gap | 0.593 |

The gap does **not** beat V1 alone, and the **equity** gap is *less* predictive than the
**level** gap — the opposite of the pre-registered expectation that "looks-governed-but-
delivers-unequally" is where the frustration lives. In this data, it isn't.

## H5 — Does V2-Equity add beyond V1 + V2-Level? — **NULL**

| model | AUC |
|---|---|
| V1 | 0.807 |
| V2-Level | 0.635 |
| V2-Equity | 0.594 |
| V1 + V2-Level | 0.839 |
| **V1 + V2-Level + V2-Equity** | **0.842** |

**V2-Level adds a modest +0.032 over V1** (health/fiscal conversion carries *some* independent
signal — the one positive). **V2-Equity adds +0.004** — nothing. The equity dimension does not
capture predictive information beyond institutions and average conversion.

## H6 — Does HL-LE predict stress better than LL-HE? — **NULL**

Median split (L=50.4, E=58.2). Domestic-stress rate by quadrant:

| quadrant | n | stress rate |
|---|---|---|
| **HL-HE** (high level, high equity) | 48 | **0.354** |
| HL-LE (high level, low equity) | 10 | 0.600 |
| LL-HE (low level, high equity) | 10 | 0.600 |
| LL-LE (low level, low equity) | 47 | 0.532 |

**HL-LE = LL-HE, exactly (0.60 vs 0.60).** The instrument's central, most-counterintuitive
claim — that unequal delivery from a capable system is *more* destabilizing than equal
delivery from an incapable one — is **not supported**. The one robust directional finding:
**HL-HE is clearly the most stable quadrant** (0.354 vs 0.53–0.60) — good conversion for
everyone is protective. *(Caveat: the off-diagonal quadrants have n=10 each — underpowered;
6/10 vs 6/10. And "stress" here is conflict-onset, which barely fires for the rich HL-LE
democracies the hypothesis targets.)*

## H2 — Fiscal durability gate — **DEFERRED (not run)**

Requires a **longitudinal** V2 (F1 decline predicting later F2–F6 decline); this pass
computed V2 at the latest cross-section only. The fiscal Level indicators have deep WDI
history, so H2 is buildable in a follow-up by re-running the engine at an earlier anchor —
flagged, not claimed.

---

## The US showcase (the case the instrument was built to illuminate)

| | V1 | V2-Level | V2-Equity | V2-Combined |
|---|---|---|---|---|
| **United States** | **0.779** (Tier 2, looks well-governed) | 61.1 | 61.2 | 61.1 |

Pillar decomposition (Level / Equity / score):

| pillar | L | E | score | note |
|---|---|---|---|---|
| F1 Fiscal | 35.1 | 35.3* | 35.2 | deficits + debt; low |
| **F2 Human Dev** | **25.4** | — | 25.4 | **near worst-in-class: spends most on health, converts least** |
| F3 Infrastructure | 92.0 | 100 | 95.9 | high |
| F4 Security | 50.9 | 35.3* | 42.3 | high homicide for a rich state |
| F5 Environment | 70.0 | 100 | 83.7 | high |
| F6 Social Contract | 93.0 | 35.3* | 57.3 | low OOP, but income-proxy equity drags |

`*` = income-Gini proxy (real health/education quintile equity unavailable for the US).

**The real finding is the V1−V2 gap, not the HL-LE label.** The US *looks* well-governed (V1
0.779, top-tier) but *converts* mediocrely (V2 61), and the gap is driven by **F1 fiscal (35)
and F2 health-conversion (25)** — the US spends the most and delivers the least efficiently.
On a *conversion* instrument the US is therefore **not "high-level"** at all — a genuine
tension with the spec's HL-LE expectation, which assumed level = outcomes. Level = *efficiency*
here, and the US is inefficient. That is arguably the most honest thing V2 says: the American
pattern is not "capable system, unequal delivery" — it is **"expensive system, inefficient
delivery, with a structural veneer (V1) that outruns its functional reality (V2)."**

---

## Coverage & honest limitations (the load-bearing caveats)

- **Level: Track-1, ~150–240 countries.** Robust, all WDI/OWID revealed-outcome.
- **Equity: real only for developing countries.** The DHS wealth-quintile data (F2 health,
  ~83 countries with real equity) does **not** exist for rich countries. Every developed
  country's equity dimension is the **income-Gini proxy** + urban-rural infra (which ceilings
  near parity). So V2-Equity for the rich world is essentially an income-inequality index, not
  the multi-domain distributional measure the spec envisioned. **The equity thesis is therefore
  untestable for its own target population (rich HL-LE democracies).**
- **F1/F4/F6 equity is proxy (income-Gini), not pillar-specific.** Tax progressivity/CEQ,
  subnational homicide dispersion, OOP-by-quintile were unreachable (IMF/OECD/CEQ blocked;
  DHS not applicable to rich states).
- **The outcome is wrong for the thesis.** Armed-conflict onset does not measure
  populism/legitimacy stress in rich democracies — exactly where the equity claim lives — so
  H5/H6 are doubly under-powered for their intended purpose.
- **IMF WEO / WID / OECD-SDMX are blocked from this environment** (403); fiscal ran on WDI
  (debt coverage weak); Ease-of-Doing-Business is retired from the WB API; COFOG public-order
  spending and court efficiency unavailable → **F4 Level is degraded (homicide-only)**.

## Bottom line

V2 **earns partial standing**: it is a *valid, coherent construct* (H4), and V2-Level adds a
small but real increment over V1 (average conversion — chiefly fiscal and health — carries
independent signal). But its **central novel claim — that a distributional/equity dimension
predicts the domestic political stress V1 can't explain — is not supported in the data that
exists, and cannot yet be tested in the data that doesn't** (rich-country quintile outcomes +
a populism-sensitive outcome variable). The most valuable artifact is the **US profile**:
high structural veneer, mediocre conversion, an inefficiency gap concentrated in fiscal and
health. **Reported as a largely-null first pass with a passing construct gate — V2 is real,
but has not yet shown it adds predictive value over V1, and its equity ambition awaits data
that is currently out of reach.** No V1 changes proposed; V1 remains frozen.

**Next data acquisition to make the equity thesis testable:** OECD/PISA SES gaps, OECD health-
by-income, LIS/CEQ fiscal incidence, WHO Health Inequality Monitor quintile series for
high-income countries — plus a rich-democracy stress outcome (V-Party populism, protest
counts, or Polity/V-Dem backsliding) in place of conflict onset.
