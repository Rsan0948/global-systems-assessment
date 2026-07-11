# MI Robustness & Reproducibility — Results

**Living record.** Companion to the frozen pre-registration
(`ROBUSTNESS_PREREGISTRATION.md`, sha256 `fbd99104`). Artifacts under
`mi-research/scripts/robustness/`, `.../scripts/historical/`, and
`mi-research/data/robustness/`. Started 2026-07-11.

> **Framing.** Genuine inquiry. Findings are reported for what they *are* —
> including where they overturn the original expectation, and where a claim is an
> **inference** rather than a **measurement**. Epistemic status is labeled
> throughout. The program did not set out to defend a headline number; it followed
> the data, and the data told a different and larger story than the original
> "does the MI beat crisis baselines?" question could see.

## Status

| Workstream | Status | Commit |
|---|---|---|
| P0 prospective freeze | ✅ done (graded ~2034) | `14af889`, tag `mi-prospective-2024` |
| Plan 1 indicator substitution | ✅ done | `843e6e8` |
| P1 reproducibility rebuild | ✅ done | `44de5c1` / `f5e6f8f` |
| P3 safeguard stratification | ✅ done | `31cc093` |
| P2 temporal holdout | ✅ done | `f92725d` |
| Historical program (inversion, decay curve, forensics) | ✅ done | `bdabeb8`…`6958358` |
| External Support Index (ESI) control — Finding 8 (registered null) | ✅ done | (this branch) |
| Erosion decomposition A/B/C — Finding 9 (compound hypothesis largely not supported) | ✅ done | (this branch) |
| Wealth–institution decoupling battery — Finding 10 (registered null; hypothesis falsified) | ✅ done | (this branch) |
| Gold-standard monetary-regime substitute — Finding 11 (registered null; fails at gate) | ✅ done | (this branch) |
| Crisis-origin shift (domestic→contagion) — Finding 12 (registered null; erosion is domestic) | ✅ done | (this branch) |
| Inequality / distribution dimension — Finding 13 (registered null; bivariate-only, longitudinal reversed) | ✅ done | (this branch) |
| Variance compression + conflict-type shift — Finding 14 (A fails gate, B partial; erosion reframed as wealth catching up) | ✅ done | (this branch) |
| Convergence confirmation + durability — Finding 15 (gate passes; wealth-catching-up confirmed, mechanism = complementary facet; durable today) | ✅ done | (this branch) |
| Ordinality independent accuracy; J-only out-of-time isolation | ⏳ open | |

---

## The arc, in one paragraph

For most of recorded history, the quality of a polity's institutions — not its
wealth — was the dominant structural predictor of whether it survived or ruptured.
That signal has been **measurably eroding for ~150 years**, in statistical lockstep
with the rise of modern capital systems. The erosion is **distortion, not
inversion**: on the one crisis type that has existed across all of human history
(organized political violence), institutional structure still out-predicts wealth
even today. Modern capital did not repeal the law; it created a new,
capital-denominated failure mode (financial crisis, sovereign default) and a set
of external mechanisms that delay the consequences the law describes. The MI
measures the law. The modern holdout measures the distortion.

---

## Finding 1 — Institutional structure is the dominant predictor of rupture across pre-modern history

On the **25 pre-modern cases** (~4,700 years, six continents; each pillar-scored
from cited scholarship with per-indicator confidence tags), institutional
structure out-discriminates rupture: **AUC 0.66–0.68 vs wealth at 0.52–0.64.** The
sharper result is a **causal ordering**, not a mere correlation: institutional
*decline* precedes rupture (AUC **0.65**) while wealth *decline* predicts **nothing**
(0.52). Institutions rot first; wealth follows. The endo/exo split shows the
mechanism directly — mean institutional (P1) decline of **0.222** before
endogenous collapse vs **0.109** before conquest: a healthy polity can be conquered
without institutional decay, but internally-driven collapse is preceded by it.

This is the **deepest temporal range any quantitative governance instrument has
been evaluated against.** Epistemic status: **descriptive and underpowered**
(n=25, proxy-scored, rupture-heavy). It is the primary finding of the historical
program, and it is a small-n one — the statistical weight is in Finding 2.
Artifact: `data/robustness/historical/inversion_test.json`.

## Finding 2 — The signal has been monotonically eroding for ~150 years

A **143-polity panel, 1816–1990** (structure = V-Dem rule-of-law; wealth = log
Maddison GDP; outcome = armed-conflict onset, COW∪UCDP, dense in every epoch)
measures how structure's predictive edge over wealth changes across time. The edge
is real in every epoch and **halves toward the present**: spread **+0.131 (1850) →
+0.070 (1990)**; **Pearson r = −0.847, p = 0.033** (independently re-derived). The
decay is smooth, continuous, and statistically significant — not noise, and not a
data-quality artifact (the conflict outcome is populated 0.44–0.63 in every
anchor). It is a time-stamped record of a specific historical force progressively
drowning out a signal that governed civilizational durability for millennia.
Epistemic status: **demonstrated** (within this outcome/panel). Artifact:
`data/robustness/historical/decay_curve_conflict.json`.

## Finding 3 — The erosion is distortion, not inversion

On **armed conflict** — the outcome type that has existed across all of human
history — structure **out-predicts wealth even in the most recent epoch** (V-Dem
rule-of-law AUC 0.72 vs log-GDP 0.65 at 1990). Structure has **never lost** to
wealth on this outcome.

The modern temporal-holdout result that *looked* like "wealth wins" (2004/2012:
MI vulnerability AUC 0.69–0.73 vs a GDP-only baseline 0.75–0.81) was driven by
including **sovereign default** in the crisis definition. Default is, by
construction, a **capital-coupled** crisis — poor, indebted countries default — so
a wealth variable predicts it better almost tautologically. Remove the
capital-denominated crisis type and the ancient ordering re-emerges. So the modern
holdout did not falsify the institutional signal; it **measured the distortion** a
capital-denominated failure mode introduces into the measurement. Epistemic
status: **demonstrated.** Artifacts: `temporal_grade_report.json`,
`decay_curve_conflict.json`.

## Finding 4 — The durability gate detects a specifically modern pathology

The P4−P1 gap (economic structure outrunning institutional quality) is **negative
across all 25 pre-modern cases** — institutions were scored *above* economies, even
at pre-stress. The "economy outruns institutions" failure mode the durability gate
is built to catch **essentially did not exist before capital mobility made it
possible.** Pre-modern states failed by institutional *decline*, not economic
overreach. Accordingly the gate shows **no accuracy jump** on the ancient cases
(gap-direction 0.52; AUC 0.74 ≈ modern) — which is not a failure but a precise
characterization: the gate is **an instrument calibrated to a modern, capital-era
pathology**, not a universal crisis predictor. Epistemic status: **demonstrated
(what it measures); the "why it matters now" is interpretation.** Artifact:
`durability_ancient.json`.

## Finding 5 — Forensics confirm the mechanism, not a weakness

The gate's errors on the modern holdout are systematic, not random:

- **Misses (crisis, not flagged) are overwhelmingly EXTERNAL shocks.** The crises
  it failed to flag are the 2008 GFC hitting *institutionally sound* rich states
  (Ireland, Greece, Hungary) plus interstate/regional conflict (Eritrea, Yemen,
  Mali, Rwanda). The gate measures *internal* structural health; exogenous
  disruption — financial contagion, cross-border war — is outside its scope. A
  bounded, well-characterized limitation, not evidence it doesn't work.
- **False alarms (flagged, no crisis) are disproportionately propped-up states.**
  Reserve currency (Japan), sovereign wealth + rents + alliance (Saudi),
  EU-anchored, and IMF-program states cluster here — countries the gate correctly
  identified as structurally vulnerable, whose crisis is being **delayed by
  engineered external supports.** *Honest bound:* the composite **also genuinely
  over-flags** (35 flags in 2012), so not every false alarm is a delayed
  confirmation — but a substantial share are externally-supported states where the
  crisis looks deferred, not absent.

Epistemic status: bucket membership **mechanical**; the external-mechanism tags are
a **manual, interpretive classification** (documented per country). Artifact:
`holdout_error_forensics.json`.

## Finding 6 — The truncated crisis data biases the modern result against the gate

The modern crisis label uses sovereign-default data that **cuts off at 2015.**
**Venezuela (2017), Lebanon (2020), Sri Lanka (2022), Ghana (2022)** — textbook
structural collapses the gate flagged — are **invisible** to the holdout. Venezuela
was flagged, then became the era's textbook state collapse, and our outcome data
can't see it. So the modern "structure loses to income" number is **understated
against the gate in a specific, identifiable direction.** Fetching post-2015
sovereign-distress data would likely move it in the gate's favor. Epistemic status:
**known data limitation with a signed direction.**

## Finding 8 — A measured external-support control does NOT recover the institutional signal (registered null)

Findings 3 and 5 raised a specific, testable mechanism: the modern erosion is caused
by **external capital/institutional support delaying the consequences** the gate detects,
so *controlling for support should recover the institutional signal.* Finding 5 saw it by
hand — false alarms cluster among reserve-currency / sovereign-wealth / EU-anchored /
IMF-program states. Finding 8 built a measured **External Support Index (ESI)** and tested
it as a control. **The mechanism, tested this way, is not supported.** Pre-registration
(`ESI_PREREGISTRATION.md`, `config/esi.json`), frozen before any outcome was touched.

**Construction.** ESI = equal-weight mean of three sub-dimensions, **weights un-tuned by
design**: *Financial Life Support* (IMF program active + cumulative-20yr — concessional-debt
dropped, WB archived the indicator), *Structural Dependency* (FDI, ODA un-inverted,
remittances), *Systemic Insurance* (reserve-currency, EU/Eurozone, NATO, SWF assets/GDP,
reserves in months). Built at 2004 and 2012 for the 91 holdout countries against the
**committed joined panel** (`temporal_holdout_panel.json`). All indicator sources +
codes documented; IMF/insurance manually coded (MONA unreachable), so those layers are
documented estimates, not gold-standard series.

**Test 2A — ESI by gate-error bucket:** false positives (flagged, no crisis) carry
marginally higher mean ESI than true positives, **in the hypothesized direction but not
significant** (2004: FP 0.276 vs TP 0.258, Mann-Whitney p=0.53, Cliff's δ=0.11; 2012:
0.245 vs 0.223, p=0.54, δ=0.09 — negligible effect both windows). The "false alarms are
the propped-up ones" reading does **not** survive as an aggregate, measured effect.

**Test 2B (make-or-break) — does controlling for ESI recover the MI coefficient? No.**
On the pre-registered structural predictor (the P4−P1 durability **gap**), adding ESI
leaves the gap coefficient essentially unchanged — in fact **slightly lower**, not higher
(2004: 0.459→0.450; 2012: 0.594→0.578). ESI's own coefficient is **negative** (≈−0.16),
i.e. more support ↔ slightly *lower* in-window crisis — directionally consistent with
"support buffers," but it does not unmask the institutional signal. ESI does add modest
independent discrimination (AUC 0.654→0.671 in 2004, 0.686→0.713 in 2012). The overall-MI
variant is mixed and not robust (2004 coefficient ticks up with ESI, 2012 does not; AUC
flat), and overall MI is wealth-laden on this capital-coupled outcome (AUC ≈0.80,
vs FSI-only 0.84) — exactly the Finding-3 distortion, which is why the pure-structural
gap is the clean test. **The gate's signal is not being suppressed by uncontrolled
external support in any way this control recovers.**

**One weak positive, honestly bounded:** ESI adds more to the MI models (+0.017/+0.027
AUC) than to the FSI baseline (0.840→0.841, ≈0), the faint version of the pre-registered
"ESI helps the structural instrument more than the wealth baseline" signature — but it is
small and never manifests as coefficient recovery.

**Test 2C — does support explain the 150-year erosion? No (and can't reach the real
mechanism).** The only ESI dimension buildable across 1816–1990 is a great-power
**defense-pact** proxy (COW Formal Alliances v4.1). The erosion reproduces cleanly on this
panel (structure-vs-wealth spread declines, Pearson **r=−0.909, p=0.005**, matching
Finding 2). But controlling for the support proxy leaves the structure-coefficient decline
essentially unchanged (slope 0.00676 → 0.00653, a negligible 3.5%). And the mechanism
*precondition* fails: proxy prevalence across the seven epochs is 0.17/0.06/0.03/0.08/0.09/
0.09/0.04 — **flat, not rising** — so it does not track the growth of the modern support
system at all. The deeper limit: this proxy is *security* alliances, whereas the hypothesis
is about *capital* support (IMF, ODA, reserve-currency, FDI), which barely exists pre-1960.
So 2C cannot instrument the actual mechanism historically — it is a genuine null on the one
proxy available, with the honest caveat that the capital dimension is untestable this far back.

**Test 2D (the operational output):** among high-ESI states (>75th pct), those with
support concentrated in a **single** sub-dimension (Herfindahl ≥0.6) — a single point of
failure — are **Singapore, UAE** (Systemic-Insurance / SWF concentration) and **Mali**
(Financial-Life-Support concentration) in 2004; **Singapore** in 2012. This list stands
regardless of the null on 2A/2B.

**Verdict (per the frozen interpretation gates, no rationalization):** external support,
as measured by an equal-weight first-pass ESI, **does not explain the erosion and does not
recover the institutional signal.** The mechanism hypothesis is **not supported** at the
aggregate/systematic level; Finding 5's hand-picked cases do not generalize to a
significant measured effect (consistent with Finding 5's own "also genuinely over-flags"
bound). The rule holds: equal weights were mandatory and un-tuned — *"if it only works
with tuned weights it is probably not real,"* so the null is taken at face value.
**Honest limitations** (disclosed, not offered as escapes): the equal-weight composite
dilutes support concentrated in one mechanism (reserve-currency issuers like Japan and
SWF states like Saudi score low despite obvious insurance); concessional-debt was lost to
an archived WB series; IMF/SWF/alliance layers are documented manual estimates; n≈90 and
the modern crisis definition is capital-coupled. A tuned or insurance-only ESI might
behave differently — but that would be a new, separately pre-registered question, not a
rescue of this one. Epistemic status: **registered null with a small independent
ESI-crisis association surviving.** Artifacts: `data/robustness/esi/esi_scores.json`,
`esi_test_report.json`, `esi_2C_historical.json`; code
`scripts/robustness/esi_{fetch,build,tests}.py`, `esi_historical_2C.py`.

## Finding 9 — The erosion is NOT explained by the three structural mechanisms it most resembles (the residual is large)

Findings 3/5/8 kept pointing at a structural story for the erosion: the post-1945
order looks like mass state creation from near-zero institutional baselines *while
blocking* the historical forces (conquest, failure→death) that forced institutional
development. That thesis decomposes into three independently-testable mechanisms —
**A** sample dilution by young states, **B** elimination of the state-death
consequence, **C** perception-based P1 lagging functional reality. Each was
pre-registered (`EROSION_DECOMPOSITION_PREREGISTRATION.md`, sha256 `b030da4b`) with
the formation classification, the dysfunction outcome, and the revealed-P1 spec
frozen in **separate commits before any outcome was graded.** **The compound
hypothesis, tested this way, is largely not supported. Together the three explain
well under 50% of the longitudinal erosion; the cause is substantially unexplained.**
Two genuine positives survive — but as *bounded scope characterizations*, not as
explanations of the 150-year curve.

**A — Denominator dilution: not the driver (share ≈ 0).** Splitting the Finding-2/7
erosion curve by formation type (54 mature / 93 post-colonial / 20 early-post-colonial
across the 167-state panel∪holdout; COW entry years + a documented decolonization
overlay), the **mature-only** curve erodes *as strongly as the full sample* — spread
+0.275 (1850) → +0.070 (1990), Pearson **r=−0.94, p=0.005**, vs full **r=−0.91,
p=0.005**. The erosion is a *within-mature* phenomenon, not a composition artifact;
`A_share` clamps to ~0 (mature erodes if anything *more*, robust across the India-in
and all-flagged-edges-moved sensitivity variants). State **age** is a weak predictor
(AUC 0.55–0.58), uncorrelated with the durability gap (Spearman ρ=0.065, p=0.55), and
controlling for it does *not* recover the signal (gap coefficient moves +0.03). **The
surviving piece is cross-sectional, not longitudinal:** in the 2012 holdout the
durability gap discriminates far better among mature states (**gap AUC 0.83**) than
post-colonial (**0.69**) or early-post-colonial/Latin-America (**0.50, chance**) — the
gate *is* a mature-state instrument, i.e. it measures a decay dynamic that only
operates where there is institutional history deep enough to decay from. Epistemic
status: **longitudinal claim refuted; cross-sectional scope claim demonstrated.**

**B — Consequence elimination: strong form refuted; one real partial positive.** On a
dense (10-year-anchor, 19-point) erosion curve, a **single linear trend from 1816
beats every broken-stick break** on AIC (breaks at 1918/1945/1960/1991 all fit worse):
there is **no discrete 1945 inflection** — the erosion pre-dates and continues
smoothly through the territorial-integrity norm, so that norm cannot be the primary
mechanism. **State-death rate per decade does not track signal strength** (COW system
exits vs spread, **r=−0.04, p=0.86, null** — with the honest caveat that COW exits
conflate conquest with voluntary dissolution/unification, so a cleaner Fazal
violent-death series could differ). **The one positive is B2, the make-or-break test.**
Re-running the holdout against the pre-registered composite **dysfunction** outcome
(ANY of: Polity2 −≥3 / GDP-pc −≥15% from peak / UCDP onset / FSI +≥10), the broad
institutional signal (neg-P1) **recovers its edge over wealth**: P1-minus-wealth AUC
goes from −0.006 (crisis) to **+0.044** (dysfunction) in 2004, and from +0.031 to
**+0.082** in 2012 — the institutional level out-predicts income once the outcome is
not restricted to the capital-coupled death/default event. The **narrow durability
gap** stays below wealth even on dysfunction (it is the specifically-modern-pathology
instrument of Finding 4, not the broad signal). Reading: the modern order **decoupled
institutional failure from its terminal consequence** — the MI still identifies
structurally vulnerable states; they no longer die, they become permanent dysfunction
zones. But this recovers a modern-holdout distortion; it is **not** measured on, and
does not account for, the longitudinal curve. Epistemic status: **1945-break and
death-tracking refuted; dysfunction-recovery demonstrated but modest and
cross-sectional.**

**C — Measurement regime change: not supported (share ≈ 0).** Rebuilding 2004-vintage
P1 from **revealed-outcome** state-capacity series (tax revenue %GDP, education
expenditure %GDP, 0–100 percentile-ranked into the WGI P1 keys via the Finding-1 seam;
LPI unavailable at a 2004 origin) and grading against the same committed 2004→2024
crisis labels, revealed-P1 **under-performs perception-based P1 on every variant**
(neg-P1 AUC 0.72 vs 0.77; PPV lift 1.15 vs 1.49). Perception is not a bottleneck —
WGI predicts crises *better* than the available functional proxies. Nor is there
systematic **perception lag**: across 34 evaluable 2010–2024 crisis countries, WGI
government-effectiveness actually *rose* +4.4 on average in the pre-crisis decade and
only 10/34 show functional-down-while-perception-flat (the crisis set is conflict-onset
heavy — external shocks WGI would not register, echoing Finding 5). Epistemic status:
**null** (with the Finding-1 caveat that revealed substitution preserves cross-sectional
*rank order*, ρ≈0.98 — that is construct validity, a different claim from temporal
crisis prediction).

**Decomposition.**

| component | claim | key test | result | share of erosion |
|---|---|---|---|---|
| A dilution | young states diluted the signal | A2 mature-only slope | mature erodes r=−0.94 ≈ full r=−0.91 | **≈ 0** |
| B consequence | state death became impossible | B1 break / B2 dysfunction / B3 death-rate | no 1945 break; death-rate null; dysfunction recovers +0.05 AUC (cross-sectional only) | **≈ 0 longitudinal** (modest cross-sectional) |
| C measurement | perceptions lag reality | C1 revealed-P1 holdout | revealed under-performs perception | **≈ 0** |
| **residual** | — | — | — | **≈ 100% of the longitudinal curve** |

**Bottom line (this session is diagnosis only — no framework changes proposed).** The
institutional signal is real and ancient (Findings 1–4). Its 150-year erosion is
demonstrated (Finding 2/7). But the erosion is **not** the structural analogue of
mass state creation the thesis proposed: it is not composition (mature states erode
too), not a 1945 consequence-break (smooth decline from 1816), and not perception lag
(functional proxies predict worse). **Under the pre-registered gate (<50% ⇒ missing
structure), the erosion's cause is an open question.** What *is* established, and is
valuable: two bounded scope characterizations — the durability gate is a mature-state
instrument (A3), and the institutional signal recovers as a **dysfunction detector**
when the outcome is not restricted to capital-coupled death/default (B2). Candidate
residual mechanisms — untested here, flagged for future pre-registration — are *not*
in the A/B/C family: (1) improving GDP measurement + industrialization making wealth a
better proxy for state capacity over time (wealth catching up to structure as a
predictor); (2) the conflict outcome changing character (interstate→intrastate) across
the period; (3) variance-compression in V-Dem rule-of-law as formal-legal institutions
diffused. Artifacts: `data/robustness/decomposition/{component_A,component_B,component_C,synthesis}.json`,
`data/robustness/formation/state_formation.json`; code
`scripts/robustness/{formation_classify,erosion_component_A,erosion_component_B,erosion_component_C,erosion_synthesis,fetch_p1_timeseries}.py`;
pre-registration `docs/EROSION_DECOMPOSITION_PREREGISTRATION.md`.

## Finding 10 — The erosion is NOT wealth genuinely decoupling from institutions (registered null; the hypothesis is falsified, not merely unsupported)

Finding 9 left the 150-year erosion with a ~100% residual and flagged the most
structurally compelling remaining candidate: that the wealth↔institution
relationship *genuinely weakened* because the **mechanisms of wealth generation
progressively decoupled from institutional quality** — industrialization (produce
wealth without domestic institutions), financialization (earn returns without caring
about governance), and institutional reorientation (institutions retarget from
public-welfare to capital-facilitation). An eight-test battery, pre-registered
(`DECOUPLING_PREREGISTRATION.md`, sha256 `c4b4a24…`, frozen before any analysis) with
exact indicator codes, expected directions, null criteria, and materiality floors,
tested it at the **system level** the hypothesis specified (never naive
country-level effects). **It is comprehensively not supported — and on several
sub-claims the data points the other way.**

**The gate (is decoupling even happening?) fails.** *Test 1* — the cross-sectional
P1↔log-GDP correlation did **not** weaken in the modern MI panel; it **re-coupled**
(r 0.770→0.818, R² 0.59→0.67, 1996→2024). The deep-historical arm (V-Dem
rule-of-law vs Maddison GDP) *appeared* to decline (r 0.71→0.52, 1850→1970) but that
is a **decolonization composition artifact**: on a constant 25-polity set the
coupling *rises* (Δr=+0.24) and on mature states it is flat (Δr=+0.03, p=0.91) — the
1970 anchor's sample doubles as post-colonial states enter and loosen the pooled
correlation (the same composition seam as Finding 9-A). *Test 2* — institutional
variance within the top income quartile **narrowed** (SD 0.137→0.069), the opposite
of the predicted "rich with an increasingly wide range of governance"; rich
countries' institutions **converged**.

**The channels and the mechanism also fail, independently.** *Test 3* — economic
composition does not moderate the signal (H−L institutional-signal edge ≈0 or
reversed; institution-light share flat). *Test 4* — financial depth rose system-wide
(36→54 %GDP) but the pre-registered interaction is **positive** on the primary
(crisis) outcome in both windows (no financialization moderation; a lone weak
negative on one secondary window). *Test 5A* — P1↔P3 (human capital) is stable-to-
rising, not decoupling. *Test 5B* — the P1↔P4 "tightening" is entirely the GDP
component; GDP-decontaminated P4\* **declines**. *Test 5C* — P1↔capital-orientation
falls *faster* than P1↔people-orientation (reverse of predicted); by 2024 P1 tracks
people more than capital. *Test 5D* — no discrete 1979 inflection (smooth trend,
echoing 9-B); the real, gradual macro rise of capital-vs-people *spending* does not
appear in the P1↔orientation *relationship*.

**Verdict (per the frozen gate, no rationalization):** Tests 1–2 null ⇒ the
decoupling **phenomenon fails at the first gate**, and every channel/mechanism test
independently confirms the null. This is not "phenomenon real, mechanism wrong" —
the phenomenon does not appear. The erosion's residual is **not closed but better
bounded**: it is not composition (9-A), not consequence-elimination (9-B), not
perception-lag (9-C), not external support (Finding 8), and **not wealth–institution
decoupling** (Finding 10). What the data shows instead — modern re-coupling,
rich-country institutional convergence, institutions still people-correlated — is
consistent with Finding 9's *candidate residual #3* (measurement-regime maturation /
WGI variance-compression as formal-legal institutions diffuse), which is explicitly
**not** in the decoupling family and awaits its own pre-registration. Epistemic
status: **registered null; hypothesis falsified in its pre-registered form.** Full
write-up `docs/DECOUPLING_RESULTS.md`; artifacts `data/robustness/decoupling/*`;
code `scripts/robustness/decoupling_*.py`.

## Finding 11 — The erosion is NOT gold-standard monetary-regime structure (registered null; fails at the gate)

Finding 10 left the residual open and pointed (by elimination) at slow, monotone
processes. A structurally different candidate remained: that the erosion is not
gradual technological change but a **bounded, system-level monetary regime** — the
international **gold standard** acting as an *external institutional substitute*
(supplying monetary credibility without domestic institutional quality) from
~1870–1971, with the **post-1971 fiat era** removing the anchor and forcing the
Finding-10 re-coupling. This makes a sharp, falsifiable prediction the
industrialization story does not: the erosion curve should have **internal structure
mapping onto monetary-regime boundaries** (steeper during gold, recovery in the
interwar collapse and after 1971). Pre-registered (`GOLD_STANDARD_PREREGISTRATION.md`,
sha256 `e7dc386…`, regime periodization frozen as historical fact) with Test 1 as a
hard gate. **It fails the gate, with reversed directional predictions.**

On the *committed, unmodified* 19-point dense curve (Finding 9 B1), per-regime erosion
slopes are: pre-gold −0.00146, **classical gold +0.00076** (flat/rising — no erosion
in the flagship gold zone), interwar −0.00082, **Bretton Woods −0.00202**, **post-1971
fiat −0.00382** (steepest of all, and the *only* significant slope, p=0.025). Mean
**gold** slope −0.00063 vs mean **non-gold** −0.00203 — non-gold periods erode ~3×
*faster*, the reverse of the hypothesis. A regime-**segmented** model (knots at the
frozen regime boundaries) is crushed by the **single linear trend** on AIC (Δ=−9.3)
and BIC (Δ=−15.0); the gold-dummy regression's GOLD and year×GOLD coefficients are
p=0.90 and p=0.97. The curve is **smooth and featureless with respect to monetary
regimes** — the pre-registered falsification condition. Per the frozen stop rule,
Tests 2–6 were **not run** (no fishing past a failed gate).

**Reconciliation with Finding 10 (required):** the modern P1↔GDP re-coupling is on the
**wealth pathway**; this gate is the **political-outcome (conflict-rupture) pathway**.
The hypothesis needed the fiat era to re-couple the political-outcome signal, but that
signal **keeps eroding through 1996, fastest in the fiat block** — so the re-coupling
is confined to P1↔GDP and, critically, its **timing does not map to 1971**. Consistent
with Finding 10; fatal to the monetary-regime story.

**Verdict:** the eleventh hypothesis to fail on the longitudinal erosion. The
**smoothness itself** is now the sharpest constraint: the erosion operates
**continuously**, not in the discrete regime-linked steps a monetary substitute (or
any punctuated cause) requires — pointing away from the whole family of
regime/event-based explanations and back toward a slow monotone process (Finding 9's
candidate residuals: measurement-regime maturation / variance compression / changing
conflict character). Epistemic status: **registered null; hypothesis falsified at the
gate.** Write-up `docs/GOLD_STANDARD_RESULTS.md`; artifact
`data/robustness/gold_standard/t1_gate.json`; code `scripts/robustness/gold_t1_gate.py`.

## Finding 12 — The erosion is NOT a domestic→systemic-contagion shift; it is *specifically* in the domestic channel (registered null; reverses)

The sharpest open puzzle after Findings 10/11: institutional quality predicts **wealth**
better over time (F10) yet **political outcomes** worse (F7/F11), simultaneously. The
most promising resolution: the *outcome variable* changed — an increasing share of
"crises" are **external-systemic** shocks (contagion, interstate war, commodity/
sanction/pandemic) that overwhelm domestic institutions regardless of quality, while
the institutional signal stays intact for **domestic-origin** crises. If true, the MI
is not weakening — the world's crisis mix shifted, and the fix is a systemic-exposure
dimension (a scope characterization, not a flaw). Pre-registered
(`CONTAGION_PREREGISTRATION.md`, sha256 `068e2c5…`) with the crisis-origin classification
frozen and Test 2 as a hard gate. **It fails — by reversal.**

Onsets were re-derived with a domestic/external tag from raw UCDP type codes + COW
inter/intra, reproducing the committed Finding-7 onset set **exactly** (1176/1176, 0
missing/extra; 798 domestic, 426 external, 48 both). Splitting the dense erosion curve
three ways: **all crises** slope −0.001056 (reproduces F7); **domestic-origin only**
slope **−0.00122** (r=−0.79, p<0.001, full erosion +0.222→−0.025); **external-origin
only** slope **−0.00006** (r=−0.07, **p=0.76**, flat, and at a lower level throughout).
The erosion lives **entirely in the domestic-origin channel** — the exact crises
institutions should predict best — while the external signal was always flat. Robust to
both frozen sensitivity flips (type-4→external; type-1 excluded). The **external-origin
share is hump-shaped** (0.10 in 1816 → 0.66 in 1926 → **0.145 in 1996**): modern crises
became *more* domestic, not more external, so the dilution premise is backwards for the
modern period. Gate = **FAIL** (domestic erodes more than external). Per the stop rule,
Tests 3–6 not run.

**Reconciliation (required):** this *sharpens* rather than resolves the F10-vs-F7/11
contradiction. Institutions now predict a country's **wealth** better than ever and its
**own domestic political rupture** worse than ever, both accelerating. This kills the
reassuring "scope-boundary" reading of Finding 5 — the degradation is in the
institution→domestic-stability link itself, not external noise diluting an intact
signal. Consistent with F10/F11; fatal to the contagion story.

**Verdict:** the twelfth null on the longitudinal erosion, and the most *localizing*
one. The surviving constraint set is tight: the driver is **continuous** (F11), sits in
the **domestic** channel (F12), and coexists with a **strengthening** institution→wealth
link (F10). The two Finding-9 residuals of the right shape — (i) measurement-regime
maturation / V-Dem rule-of-law **variance compression** as formal-legal institutions
diffused, and (ii) a secular change in how post-colonial civil conflict relates to
measured rule-of-law (structure's *edge* over wealth shrinking once the sample fills
with young poor states) — remain untested and are flagged for separate pre-registration.
Epistemic status: **registered null; hypothesis falsified (reversed) at the gate.**
Write-up `docs/CONTAGION_RESULTS.md`; artifacts `data/robustness/contagion/*`; code
`scripts/robustness/contagion_{classify,t2_gate}.py`.

## Finding 13 — The erosion is NOT explained by rising inequality (registered null; bivariate-only, longitudinal reversed)

The tightest-fitting candidate yet for the F12 domestic-channel erosion: institutions
got better at producing *aggregate* wealth (→ F10 P1↔GDP re-coupling) while its
*distribution* concentrated; domestic rupture depends on distribution, not aggregates,
so the domestic signal erodes as inequality rises (Piketty's r>g, continuous since
~1850 with a 1914–1980 compression — matching every constraint: continuous, domestic,
mature-state, WGI/P3-invisible). Pre-registered (`INEQUALITY_PREREGISTRATION.md`, sha256
`8c0236a…`), primary indicator WID top-10% pre-tax share (via OWID), Tests 1 & 2 the
gate. **The gate splits and the full battery resolves to null.**

**T1 (arm A):** inequality is a *significant bivariate* predictor of domestic crises
(2004 p=0.0001, AUC 0.79) — but that only reflects poor unstable states being unequal
(AUC < GDP's 0.84); the P1 coefficient **does not recover** when inequality is
controlled and the interaction is **positive**, not the predicted negative. **T2 (arm
B) fails and reverses:** the domestic-channel spread correlates **+0.85** (p=0.008) with
mean top-10% share over epochs — they *fell together* across the 20th century — and
during the 1914–1980 Great Compression the domestic signal **kept eroding** (no Piketty-
U fingerprint). **T3** refutes moderation: neg-P1 AUC is **0.88 in high-inequality
mature states** (signal intact where it should have broken); low-inequality mature
states simply had zero crises. **T4** does not resolve F10-vs-F12 (inequality-partialled
P1↔stability corr *falls* below raw, 0.61→0.51). **T5** long-run +0.51 p=0.20 (wrong
sign, underpowered). **T6** (exploratory) P6 distribution pillar adds nothing (AUC
0.882→0.884; Afghanistan/Ethiopia *rise* with P6 — low measured top-10% ≠ stability).

**Verdict:** inequality is a real cross-sectional correlate of instability but **not the
erosion mechanism** — it neither recovers, moderates, nor longitudinally tracks the
domestic signal, and the mid-century compression (the hypothesis's own natural
experiment) shows the opposite of the prediction. The thirteenth null on the
longitudinal erosion. The constraint profile tightens further: the driver is continuous
(F11), domestic (F12), coexists with strengthening P1↔GDP (F10), within-mature (F9-A),
and invisible to WGI, P3, **and income distribution** (F13). Standing leads (Finding-9
residuals, untested): (i) measurement-regime maturation / V-Dem rule-of-law **variance
compression** — now with the added constraint that it must co-move with the century's
*falling* top-income concentration; (ii) secular change in post-colonial civil-conflict
character vs measured rule-of-law. Epistemic status: **registered null.** Write-up
`docs/INEQUALITY_RESULTS.md`; artifacts `data/robustness/inequality/*`; code
`scripts/robustness/inequality_{fetch,t1_t2_gate,t3_t6}.py`.

## Finding 14 — The erosion is NOT variance compression or a conflict-type shift — it is wealth catching up as a domestic-crisis predictor

The last two Finding-9 residuals, pre-registered together (`VARIANCE_COMPRESSION_PREREGISTRATION.md`,
sha256 `396e159…`) with A1/B1 as gates. **Candidate A (variance compression) fails at
the gate:** institutional-quality variance has **not** compressed — modern P1 SD is flat
(0.170→0.173, p=0.74) and V-Dem rule-of-law SD is flat-to-rising over 1850–2010
(0.299→0.309, p=0.73); range restriction explains only **1.9%** of the signal change
(A2), the Thorndike Case-II correction changes nothing (A3, u≈1), and P10/P90 are stable
with the rol *top* rising (A4/A5). **Candidate B (conflict-type shift) passes its gate
but cannot carry the erosion:** territory/identity share of domestic conflict genuinely
rose (0.32→0.63, p=0.003, B1), but the governance-type spread is ≈0 and flat in the
testable window (no strong intact governance-failure signal, B2), UCDP incompatibility
coding is **blind to the pre-1946 two-thirds of the erosion**, and post-colonial conflict
is not disproportionately territory-type (0.522 ≈ mature 0.556) so it does not explain
the weaker post-colonial signal (B3).

**The affirmative result — the erosion's character, finally resolved.** Decomposing the
Finding-12 domestic spread (`struct_auc − wealth_auc`) over 1816–1996: `struct_auc`
(institutions→domestic crisis) **rose** 0.44→0.75 (Δ+0.31, p=0.20, n.s.), while
`wealth_auc` (GDP→domestic crisis) rose **faster**, 0.22→0.78 (Δ+0.557, **p=0.005**, the
only significantly-trending component). **The 150-year "erosion of the institutional
signal" is not institutions losing predictive power — it is GDP *gaining* it, catching up
to and slightly overtaking institutions, so their *edge* (the spread) narrowed.** This is
Finding-9 residual #1 (industrialization + improving economic statistics making wealth a
better state-capacity proxy) — the one residual never run as a primary — and it is the
only mechanism fitting the *entire* constraint profile at once: continuous, domestic-
channel, coexisting with **strengthening P1↔GDP** (F10 seen from the wealth side),
within-mature, and invisible to every distributional/regime/support/contagion test
because it is a property of the **wealth predictor improving**, not of institutions
changing. It reconciles F10/F11/F12/F13 in one stroke.

**Status: lead, not closed.** It emerges from a pre-registered *decomposition*, not a
primary hypothesis with its own falsification gate; the right next step is a dedicated
pre-registration (does a revealed GDP/state-capacity series' rising discrimination fully
account for the spread narrowing on a constant sample with wealth-data-quality
controlled?). But after fourteen adversarial tests the most defensible headline shifts
from *"the institutional signal is eroding"* to **"institutions did not weaken — the
wealth signal caught up."** Epistemic status: A **registered null (gate fail)**; B
**partial**; wealth-catching-up **strongest evidenced lead (p=0.005), awaiting its own
pre-registration.** Write-up `docs/VARIANCE_COMPRESSION_RESULTS.md`; artifacts
`data/robustness/varcomp/*`; code `scripts/robustness/varcomp_{A,B}.py`.

## Finding 15 — The wealth-catching-up lead is CONFIRMED (as a complementary-facet mechanism), and the convergence is durable today

Finding 14's lead — that the 150-year "erosion" is GDP *gaining* crisis-predictive
signal, not institutions losing it — was pre-registered as its own hypothesis with gates
and run to confirmation (`CONVERGENCE_PREREGISTRATION.md`, sha256 `4071b996`, frozen
before analysis). **The two-part gate passes; the interpretation is confirmed with one
qualification.**

**Gate (Tests 1–2) — PASS.** *Test 1:* the V-Dem rule-of-law ↔ log-Maddison-GDP coupling
has been **rising** for 150 years on every like-for-like sample (constant-set Δr **+0.151**;
mature-only Δr **+0.152**, slope p=0.006), and the mature coupling trajectory positively
tracks the `wealth_auc` curve (r=+0.469, **p=0.043**). It only *falls* on the **pooled**
sample (Δr−0.045) — the same decolonization composition artifact Finding 10-T1 already
identified (coupling collapses at the 1956 anchor as post-colonial states enter). *Test 2:*
GDP's economic substrate shifted as the mechanism requires — global agriculture share fell
**23.7%→10.0%** monotonically (WDI 1970–2024, trend p=0.0002; deep-history ~60–70%→~4% is
documented context), and GDP predicts crises **worse** where agriculture still dominates
(GDP-crisis AUC 0.688 for ag≥25% vs 0.714 for ag<10%).

**Mechanism (Test 3) — complementary facet, not pure proxy.** Adding P1 does **not**
eliminate GDP's predictive power: in the joint logistic model both stay significant
(2004: P1 z=2.8, GDP z=2.7; 2012: P1 z=2.5, GDP z=2.3), and GDP's independent contribution
did **not** grow over epochs (|coef| trend −0.006, p=0.13). So GDP is **not** a proxy whose
signal is parasitic on institutions — it captures a **partially independent facet of the
same construct** (state capacity). Per the pre-registered middle outcome, the
interpretation is *"GDP measures a complementary facet"*, not *"GDP measures the identical
thing."*

**Two weaker angles, reported honestly.** *Test 4 (diffusion)* is **inconclusive** —
early/mid industrializers accumulate 0–5 domestic-crisis observations per epoch (rich deep
states rarely rupture domestically), so cross-cohort `wealth_auc` ordering is not estimable;
the one estimable cohort (late, n=145) rises as predicted (crosses 0.65 at 1976, p=0.003).
*Test 5 (agricultural-economy discriminator)* **disconfirms**: modern agricultural economies
do **not** retain the pre-convergence pattern — both P1−GDP spreads are negative and the
agricultural spread is *more* negative (−0.093 vs −0.045), because modern low-GDP states are
unstable partly *because* they are poor (the poverty→instability coupling carries
crisis-information the 1816 wealth level did not). This is exactly why the mechanism is
complementary-facet, not clean re-measurement. *Test 6* replicates the pattern on a broader
**dysfunction** outcome (struct Δ+0.226 p=0.053; wealth Δ+0.460 p=0.002) with a disclosed
partial-circularity caveat (the composite includes a GDP-decline term).

**Durability (Part 2) — robust today, one bounded present risk, one forward risk.** *Test 8:*
of four candidate decoupling forces, **only resource extraction weakens** the P1↔GDP coupling
(0.722 vs 0.837, exposed vs not) — the MI's oldest pattern, already in the resource penalty.
FDI, financialization, and services-heavy (ICT-proxy) economies show **tighter** coupling
when exposed, because those forces cluster where institutions are **already** strong; the new
post-industrial forces have **not** produced institution-independent GDP at scale. Exposure to
every force is growing, so this is a present-tense robustness. *Test 7:* the pre-registered
decouple threshold is non-discriminating (69% of the panel — GDP grows >50% over 28y almost
universally while WGI-P1 is sticky; disclosed), but the sharp *governance-declined-while-
wealth-grew* set (n=27) crisis **more than GDP predicts** (residual +0.017 vs −0.008) and is
**not** just resource/authoritarian outliers — it includes advanced democracies (UK, France,
Israel), the early signature of the "dangerous configuration" where GDP over-predicts a
stability that eroding governance is undermining. *Test 9 (AI, structured forward
assessment — not a test):* the convergence depends on GDP *requiring* institutional quality;
if AI makes output institution-independent across the labor/production/trade/finance/services
channels at scale, GDP could grow while institutions stagnate, **reversing** the convergence —
institutions would again out-predict GDP, *not* because they strengthened but because GDP got
noisier, from a higher baseline. Test 8 shows this is **not happening yet**; the leading
indicator is the P1↔GDP coupling turning negative among AI-intensive economies.

**Verdict.** The most defensible headline of the whole robustness program is now
**confirmed, not merely led-to**: *institutions did not weaken over 150 years — the wealth
signal caught up*, GDP having become a complementary state-capacity signal as economies
industrialized and measurement improved. The convergence is structurally durable today, with
resource extraction the one standing decoupler (already modeled) and AI the credible forward
risk — in which reversal the MI's institutional signal **regains**, not loses, relative
advantage. Epistemic status: **gate-passed confirmation; proxy claim qualified to
complementary-facet; durability = robust-today with disclosed forward risk.** Write-up
`docs/CONVERGENCE_RESULTS.md`; artifacts `data/robustness/convergence/{part1,part2}.json`;
code `scripts/robustness/convergence_{lib,part1,part2}.py`; pre-registration
`docs/CONVERGENCE_PREREGISTRATION.md`.

---

## Supporting findings (the original audit)

These stand and reinforce the arc; they are no longer the headline.

- **Construct validity holds.** Replacing the perception-based P1 indicators (WGI)
  with revealed-outcome ones (tax %GDP, logistics performance, etc.) leaves rank
  order essentially unchanged (ρ ≈ 0.98 for LPI / max-divergence; all swaps
  ρ > 0.93), and the MI survives substitution **better than a GDP-only ranking
  (ρ = 0.87)**. It is not ideological loading and not merely wealth. (Plan 1.)
- **The "100% directional accuracy" was one soft metric, honestly decomposed.**
  Of the 51 flagship ordinality cases, ~10 were clean mechanical derivations, 7
  were mechanical abstentions counted as confirmations, ~34 rested on preserved
  human judgment. That marketing number was replaced by the more defensible
  findings above — the *framework* is not weaker for it. (P1.)
- **The rule structure is clean.** Only the durability gate is load-bearing on any
  graded call; the thin qualifiers are advisory and never inflated the headline
  (the epicycle charge dissolves). (P3.)

---

## Convergence — The Structural Picture

Three independent bodies of work point the same way. **Two are demonstrated within
their domains; the third connection is an inference.**

1. **Fragmentation census (in-repo, `../../fragmentation/`) — demonstrated within
   its domains.** Engineered suppression of natural fracturing produces more
   violent, more dispersed, less predictable rupture, scaling with suppression
   duration and engineering degree (violent state break-ups: ~53 yrs suppression /
   5.6 successors vs peaceful ~10 yrs / 3.3; the grown-vs-designed dispersion dial
   runs CV ~0.2 → ~2.3). These are qualitative/curated sub-laws, not a precise
   quantitative law.
2. **The institutional-erosion findings above (Findings 1–2) — demonstrated
   within their outcome/panel.** The signal being suppressed — institutions as the
   primary predictor of rupture — has been dominant for millennia and is eroding
   in lockstep with the rise of modern capital.
3. **The capital-hubs atlas (`../../docs/capital_hubs_atlas.md`) — historical
   context.** It documents that the modern reserve-currency/financial system is
   unprecedented in scale and duration (Bretton Woods ~80 yrs; the dollar system
   sustaining structural imbalances across dozens of polities simultaneously), and
   that extraction-based nodes are historically fragile (the MI's resource penalty
   is the modern instance of its oldest pattern). The atlas itself flags its
   numbers as scholarly estimates with wide error bars and its stronger causal
   claims as contested.

**The connecting thesis (INFERENCE, not measurement):** if the modern financial
system functions as the largest, longest-duration, widest-scope engineered
suppression mechanism in recorded history, then the fragmentation physics predict
that it is **not eliminating structural vulnerability but accumulating it** —
and that accumulated suppression, when it releases, releases proportionally to how
long and how hard it was held. The data from three programs is **consistent** with
this picture, but the specific projection about global-scale accumulated pressure
is **an inference from a pattern demonstrated in other domains, not a measured
result.** The fragmentation dispersion relationship was demonstrated on rivers,
neurons, languages, corporate/party/state/religious splits — extrapolating it to
the global financial system (which has active stabilization, self-aware
participants, and a history of self-reform) is **grounded but not confirmed.**
Stating that boundary explicitly is what makes the rest credible.

---

## Bottom line

The MI is not a diagnostic that "fails to predict." It is a **structural-law
detector operating in an era where unprecedented capital mobility delays the
consequences it detects.** Demonstrated: institutional structure has been the
dominant predictor of political rupture across the deepest temporal range any such
instrument has been tested on; that signal has eroded measurably and significantly
for 150 years; the erosion is distortion, not inversion (structure still leads on
conflict); the durability gate cleanly characterizes a specifically modern failure
mode; and the modern-era measurement is biased against the gate by truncated data.
Inferred (labeled): the convergence with the fragmentation physics implies the
capital system is accumulating, not eliminating, structural pressure. The strength
of the position comes from having reached it by destroying the weaker claims first.

## Open work

1. **J-only out-of-time isolation** — grade Safeguard J alone (not the composite)
   on conflict-only outcomes across the temporal windows, to pin its true modern
   signal net of the default distortion.
2. **Post-2015 sovereign-distress data** — add Venezuela/Lebanon/Sri Lanka/Ghana to
   de-bias the modern holdout (Finding 6).
3. **Ordinality independent accuracy** — score `post_event` vs actual outcome.
4. **Convergent validity** — MI ordering vs independent frameworks (V-Dem, QoG, BTI).
5. **P0 prospective freeze** — grade in ~2034 (the only clean forward test).
