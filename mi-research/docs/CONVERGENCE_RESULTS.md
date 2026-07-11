# Convergence Confirmation — Results

**Companion to** the frozen pre-registration `CONVERGENCE_PREREGISTRATION.md`
(sha256 `4071b996`). Artifacts: `data/robustness/convergence/{part1,part2}.json`;
code `scripts/robustness/{convergence_lib,convergence_part1,convergence_part2}.py`.
Started 2026-07-11.

> **The question.** Finding 14 recharacterized the 150-year "erosion of the
> institutional signal" as **wealth catching up**: `struct_auc` (institutions→domestic
> crisis) rose 0.44→0.75 (p=0.20, n.s.) while `wealth_auc` (GDP→domestic crisis) rose
> **faster**, 0.22→0.78 (p=0.005). It emerged from a decomposition, not a hypothesis
> with its own gate. This program promotes-or-refutes it with confirmatory evidence
> (Part 1) and then asks whether the convergence is structurally durable (Part 2).

---

## Verdict in one paragraph

**The convergence is confirmed; the pure-proxy mechanism is qualified to a
*complementary-facet* mechanism.** The two pre-registered gates pass: the
institution↔GDP coupling has been *rising* for 150 years on like-for-like samples (it
only *falls* on the pooled sample, which is the already-documented decolonization
composition artifact), and GDP's economic substrate shifted from agriculture toward
industry/services exactly as the mechanism requires, with GDP predicting crises
**worse** where agriculture still dominates. But the mechanism test (Test 3) shows GDP
retains **independent** predictive power after controlling for institutions — so GDP did
not become a *pure* proxy measuring the identical construct; it measures a
**complementary facet** of state capacity. Two of the five confirmatory angles are
weaker: the diffusion test is underpowered (rich early-industrializers rarely rupture
domestically), and the sharp cross-sectional analog **disconfirms** (modern agricultural
economies do *not* retain the pre-convergence pattern, because modern poverty itself
carries crisis-information the 1816 wealth level did not). The most defensible headline
from Finding 14 — *"institutions did not weaken; the wealth signal caught up"* — **holds**.
The stronger reading — *"GDP became the same measurement as institutions"* — **does not**.
On durability: the convergence is **robust today** (only resource-extraction decouples
wealth from institutions, and that is already in the MI's resource penalty), but a
**bounded present risk** (states where governance actually declined while wealth grew
now crisis more than GDP predicts) and a **forward structural risk** (AI-driven
institution-independent output) are flagged.

---

## PART 1 — Confirmation

### Test 1 — GDP↔institution coupling has been rising for 150 years  *(GATE — PASS)*

Correlation of V-Dem rule-of-law with log Maddison GDP per capita, per epoch, on three
samples:

| sample | 1816/1850 → 1996 | Δr | trend |
|---|---|---|---|
| **pooled** (all available) | 0.729 → 0.684 | **−0.045** | slope −0.0013, **p=0.001** (declining) |
| **constant** (30 states, all anchors) | 0.682 → 0.834 | **+0.151** | slope +0.0005, p=0.68 |
| **mature** (54 states) | 0.641 → 0.793 | **+0.152** | slope +0.0013, **p=0.006** (rising) |

The pooled decline is the **decolonization composition artifact** — the coupling
collapses at 1956 (r=0.435) as post-colonial states flood the panel, the exact seam
Finding 10-T1 already characterized. On any **like-for-like** sample (constant or
mature) the coupling **rises**. The mature coupling trajectory **positively tracks the
`wealth_auc` trajectory** (Pearson r=+0.469, **p=0.043**); the pooled series does not
(r=−0.199, p=0.41) — again the composition artifact. Modern MI panel (Finding 10)
independently corroborates: P1↔GDP r 0.770→0.818, 1996→2024. **Confirmed:** GDP has
been becoming a better proxy for institutional quality continuously, on samples that
hold composition fixed.

### Test 2 — GDP's sector composition shifted institution-independent → institution-dependent  *(GATE — PASS)*

Global (country-equal-weighted) sector shares, WDI 1970–2024:

| decade | agriculture % | industry % | services % |
|---|---|---|---|
| 1970 | 23.7 | 26.0 | 44.2 |
| 1990 | 17.0 | 28.0 | 48.9 |
| 2010 | 10.5 | 26.2 | 55.7 |
| 2024 | 10.0 | 25.1 | 57.0 |

Agriculture share fell **monotonically** (trend −0.26 pts/yr, **p=0.0002**); services
absorbed the shift. (Deep-historical context — agriculture ~60–70% of GDP in the
mid-19th century → ~4% in advanced economies today — is documented economic history,
cited but not recomputed here.) **Cross-sectional discriminator:** pooled across the MI
years, GDP's crisis-predictive AUC is **lower in high-agriculture economies** (ag ≥ 25%:
AUC 0.688) than **low-agriculture** ones (ag < 10%: AUC 0.714). GDP is a weaker
crisis-predictor exactly where it still measures farm output. **Confirmed.**

**→ Gate passes (Tests 1 & 2). The convergence interpretation stands. Part 1 proceeds.**

### Test 3 — Does GDP predict crises THROUGH institutions?  *(MECHANISM — complementary facets, NOT pure proxy)*

Three logistic models on domestic crises (predictors z-standardized, ridge L2=1e-3;
coefficient z from bootstrap SE):

| window | M1 P1 AUC | M2 GDP AUC | M3 both AUC | M3 P1 coef (z) | M3 GDP coef (z) |
|---|---|---|---|---|---|
| 2004 | 0.758 | 0.759 | 0.787 | 0.729 (**2.8**) | 0.665 (**2.7**) |
| 2012 | 0.727 | 0.725 | 0.753 | 0.615 (**2.5**) | 0.576 (**2.3**) |

**Both P1 and GDP remain significant when controlled for each other.** GDP's coefficient
does **not** collapse under P1 control — so GDP is **not** a pure proxy whose signal is
entirely parasitic on institutions. M3 adds ~0.025–0.029 AUC over P1 alone: modest but
real independent contribution. Across the historical epochs, GDP's independent |coef|
trend is **−0.006/epoch (p=0.13)** — flat-to-shrinking, not growing. **Reading (the
pre-registered middle outcome):** GDP and institutions each capture a partially
independent facet of the same underlying construct (state capacity). The convergence is
real; the interpretation is *"GDP measures a complementary facet"*, not *"GDP measures
the identical thing."*

### Test 4 — Does the convergence follow industrialization diffusion?  *(INCONCLUSIVE — underpowered)*

`wealth_auc` per epoch by industrializer cohort. **Early** (GBR/FRA/DEU/USA/…, n=8) and
**mid** (JPN/RUS/ITA/…, n=10) industrializers accumulate only **0–5 domestic-crisis
observations per epoch** — below the estimation floor — because rich, institutionally
deep states rarely rupture domestically. Every early/mid per-epoch `wealth_auc` is
therefore undefined. Only the **late** cohort (n=145, the mass of the panel) is
estimable: `wealth_auc` rises 0.50→0.78, first crossing 0.65 at **1976** (trend +0.0024,
**p=0.003**). The sharp cross-cohort *ordering* prediction is **not testable** at this
crisis base rate — the very stability of early industrializers (consistent with the
thesis) starves the test. Reported as inconclusive per the pre-committed small-n caveat;
the one estimable cohort behaves as predicted.

### Test 5 — Do agricultural economies still show the pre-convergence pattern?  *(DISCONFIRMS)*

Modern panel, P1−GDP spread over domestic crises:

| group | struct_auc | wealth_auc | **spread** | n / n_pos |
|---|---|---|---|---|
| agricultural (ag ≥ 25%) | 0.596 | 0.688 | **−0.093** | 50 / 22 |
| industrial (ag < 10%) | 0.669 | 0.714 | **−0.045** | 319 / 30 |

The prediction was a **positive** spread among agricultural economies (institutions
out-predicting GDP, as in 1816). Instead **both spreads are negative** and the
agricultural spread is **more** negative — GDP out-predicts institutions in agricultural
economies at least as much as in industrial ones. **Disconfirmed.** The sharp
cross-sectional analog of the historical pattern does not hold, and the reason is
informative: modern low-GDP agricultural states are unstable *partly because they are
poor* — the poverty→instability coupling gives modern GDP crisis-information that the
1816 agricultural *wealth level* did not carry. This is why the mechanism is
complementary-facet (Test 3), not pure-proxy: modern GDP's crisis signal is a blend of
improved state-capacity measurement **and** the poverty-instability coupling, not a
clean reproduction of "GDP now measures institutions."

### Test 6 — Restate on an independent outcome  *(CONFIRMS, with a disclosed caveat)*

Recomputing the decomposition on a composite **dysfunction** outcome (conflict onset OR
GDP-pc decline ≥15% from peak in window) instead of conflict onset alone: `struct_auc`
Δ **+0.226** (slope p=0.053) and `wealth_auc` Δ **+0.460** (slope **p=0.002**) — the same
qualitative pattern (both rise; wealth rises faster and is the significant trend).
**Caveat (disclosed):** the historical dysfunction composite includes a GDP-decline term,
which mechanically assists the GDP predictor; the modern four-part dysfunction outcome
(Finding 9-B2, with Polity/FSI) is not buildable across 1816–1996. The qualitative
convergence survives — importantly `struct_auc` also rises — but the wealth-auc margin
here is partly circular and should not be read quantitatively.

### Part 1 scorecard

| Test | Angle | Result |
|---|---|---|
| 1 | coupling trajectory (GATE) | **CONFIRM** (like-for-like; pooled = artifact) |
| 2 | sector composition (GATE) | **CONFIRM** |
| 3 | mediation / mechanism | **complementary facets** (not pure proxy) |
| 4 | industrialization diffusion | inconclusive (underpowered) |
| 5 | agricultural-economy discriminator | **DISCONFIRM** (poverty-instability coupling) |
| 6 | dysfunction replication | **CONFIRM** (partial circularity caveat) |

**Part 1 conclusion.** Finding 14's core recharacterization — *institutions did not lose
predictive power; wealth gained it* — is **confirmed**: `struct_auc` did not decline, the
coupling rose on like-for-like samples, and the economic substrate shifted as required.
The mechanism is **GDP becoming a complementary state-capacity signal** — through
industrialization/financialization *and* improved economic measurement *and* the
poverty-instability coupling — not GDP becoming a literal re-measurement of institutions.
Finding 14 is **promoted from lead to confirmed finding, with the proxy claim qualified
to complementary-facet.**

---

## PART 2 — Durability

### Test 7 — Is the coupling stable or fragile?

The **pre-registered** decoupling threshold (GDP grew >50% while P1 moved <0.05) is
**non-discriminating**: over the 28-year window GDP-pc PPP grows >50% for nearly every
country while WGI-based P1 is sticky, so **57/83 (69%)** of the panel "qualifies" and the
residual test is null (+0.001 vs −0.002). Disclosed, not hidden. A **sharp cut** —
governance actually **declined** while wealth grew (dP1 < −0.03, growth > 50%, n=27) —
is the meaningful set: these states crisis **more than GDP alone predicts** (mean crisis
residual **+0.017 vs −0.008** for the rest). Crucially this set is **not** just
resource/authoritarian outliers (only 4/27 are resource ≥10%; 0 coded autocracies) — it
includes **advanced democracies** whose WGI slipped over 2008–2024 and who then had
crises GDP did not foresee (UK residual +0.86, France +0.85, Israel +0.85, Turkey +0.73,
Thailand +0.65, Egypt +0.52). This is a small but real instance of the **dangerous
configuration** the pre-registration named: GDP predicting stability that governance
decline is quietly undermining. Modest (conflict-heavy crisis label; small residual), so
reported as a directional early signal, not a quantified effect.

### Test 8 — What could decouple GDP from state capacity going forward?

P1↔GDP coupling among **exposed vs non-exposed** countries (2018), plus exposure growth:

| force | coupling (exposed) | coupling (non-exposed) | weaker? | exposure 1996→2024 |
|---|---|---|---|---|
| **resource rents > 10%** | **0.722** | **0.837** | **YES** | 21 → 24 (growing) |
| FDI > 5% | 0.945 | 0.764 | no | 28 → 43 (growing) |
| private credit > 100% (financialization) | 0.936 | 0.766 | no | 6 → 19 (growing) |
| services > 60% (ICT proxy) | 0.869 | 0.671 | no | 35 → 65 (growing) |

**Only resource extraction weakens the coupling** — resource rents generate GDP without
institutional infrastructure, so wealth and institutions decouple among petro/mineral
states. This is the MI's **oldest pattern**, already captured by the resource penalty.
The **new post-industrial forces do NOT currently decouple** wealth from institutions —
FDI, deep finance, and services-heavy economies show *tighter* coupling when exposed,
because those forces cluster in economies that **already** have strong institutions. The
convergence is therefore **structurally robust today**: the one active decoupler is old
and modeled; the hypothesized modern decouplers have not (yet) produced
institution-independent GDP at scale. **Exposure to every force is growing**, so the
robustness is a present-tense statement, not a permanent guarantee.

**Disclosed gap:** no ICT-service-exports indicator is committed; the digital force is
proxied by services share > 60% and flagged as a gap, not a measurement of ICT-specific
decoupling.

### Test 9 — The AI question  *(STRUCTURED FORWARD ASSESSMENT — not a statistical test)*

The convergence depends on one structural fact: **GDP currently requires institutional
quality**. Enumerated channels and AI's potential to erode each:

| channel | current institutional dependency | does AI reduce it? |
|---|---|---|
| labor | educated workforce ← public education (P3) | **yes** — AI substitutes for educated labor, weakening the P3 dependency |
| physical production | factories ← permits, inspection, infrastructure (P1) | partial — AI enables more remote/digital production, reducing physical-infrastructure dependency |
| trade / contracts | enforcement, customs, courts (P1) | partial — automated/peer-to-peer settlement could reduce contract-enforcement dependency |
| finance | central banking, regulation, legal enforcement (P1) | ambiguous — AI could reduce *or* increase regulatory dependency depending on implementation |
| services | consumer protection, licensing, dispute resolution (P1) | partial — automated compliance cuts some dependency, creates new ones |

If AI reduces institutional dependency across several channels **simultaneously and at
scale**, GDP could grow while institutional quality stagnates — reopening the spread, but
from the **opposite direction** to the historical pattern. In 1816 institutions
out-predicted GDP because GDP did not yet measure state capacity. In an AI-decoupled
future GDP could predict crises **worse** than institutions because GDP would **stop**
measuring state capacity. The convergence would **reverse**: institutions would again
out-predict GDP — **not because institutions strengthened, but because GDP got noisier**
— from a higher baseline for both.

**Framing (per the pre-registration).** This is a forward-looking structural risk, not a
finding. Test 8's evidence is that **it is not happening yet**: the digital/services
proxy shows *tighter*, not weaker, coupling, and the modern forces cluster in
high-institution economies. The risk is real, bounded, and monitorable: the leading
indicator would be the P1↔GDP coupling among digital/AI-intensive economies **turning
negative** while their GDP grows — the moment institution-independent output reaches
scale. The MI's institutional signal is the instrument that would **regain relative
advantage** precisely in that scenario.

---

## Bottom line

Finding 14 survives confirmation and is promoted: **institutions did not weaken over 150
years — the wealth signal caught up**, as GDP's economic substrate industrialized and its
measurement improved, so that GDP became a **complementary** (not identical) state-capacity
signal. The convergence is **structurally durable today** — the only force that decouples
wealth from institutions is resource extraction, which the MI already models — but it is a
**present-tense** durability: exposure to post-industrial forces is growing, a set of
states (including advanced democracies) where governance is quietly declining already
crisis more than their wealth predicts, and AI is a credible forward force that could
reverse the convergence by making GDP institution-independent. In that reversal the MI's
institutional signal does not lose relevance — it **regains** it.
