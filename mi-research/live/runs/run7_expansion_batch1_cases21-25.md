# Modernization Index Validation — Run 7: Expansion Batch 1 (Cases 21–25)

> First expansion run beyond the 20-case baseline. Cases per
> `docs/expansion_plan/` recommended sequence: 21 Haiti/DR, 22 Venezuela,
> 23 Colombia, 24 DRC/Rwanda, 25 Rwanda. All five scored on **freshly collected,
> real public indicators** (World Bank WGI 2025-anchored, UNDP HDR 2025, World
> Bank WDI, Fund for Peace FSI 2024) committed as `data/countries/*.json`. The
> Rwanda architectural decision (P1 composite vs. decomposed) was settled FIRST —
> see `docs/architectural_decisions/rwanda_p1_composite_vs_decomposed.md`: **P1
> kept composite**, so the engine and the 20-case baseline are unchanged.

## TL;DR
- **The P1 ordinal core holds across all five cases where the gap exceeds the WGI
  margin.** Dominican Republic (P1 0.456 → 0.500) ordinally beat Haiti (0.296 →
  0.222); Rwanda (0.295 → 0.594) ordinally beat DR Congo (0.199 → 0.253);
  Venezuela's P1 collapse (0.380 → 0.210) tracked the largest peacetime economic
  collapse on record. Where the pre-event gap was *inside* the margin (DRC vs.
  Rwanda in 1996, gap 0.096 < 0.10) the framework correctly **abstained** under
  Mod4 and predicted divergence-over-time rather than a near-term ranking.
- **Two honest data-integrity flags carry as much weight as the confirmations.**
  (1) Venezuela's composite MI (0.49) *understates* its collapse because GDP per
  capita has been unpublished since 2011 — P4 is gap-inflated to 0.87; the real
  signal is the P1/P5 collapse and a near-record pillar spread (0.66). Missing
  data is information: the unpublished-GDP gap *is* the collapse. (2) Rwanda's
  confirmation is partly prospective — its predicted *latent* reversal risk is not
  yet falsifiable, so we code it open, not triumphant.
- **Confirmation across the ~24 discrete predictions in this batch is ~70–80%
  clean** (best estimate ~75%), directional accuracy ~100% with no outright
  falsification — consistent with, and subject to, the same caveats as the 20-case
  baseline (partly redundant with WGI standalone; near-absence of falsification is
  partly structural). Reported as a range, ordinal/directional only.

## Key Findings
1. **Haiti/DR is a clean shared-island confirmation at the low end of P1.** A wide,
   margin-exceeding P1 gap (0.16 in 1996) mapped to divergent outcomes: DR pulled
   into upper-middle-income stability (GDP PPP $5.2k → $25.8k, HDI 0.776) while
   Haiti's P1 fell further (0.296 → 0.222) into state collapse (PM assassinated
   2021, gang takeover of Port-au-Prince by 2024). The MI gap widened from 0.17 to
   0.24 — divergence confirmed.
2. **Venezuela confirms the rentier-collapse thesis but exposes a measurement
   trap.** Safeguard E fires bidirectionally (oil ≈ 60% of fiscal revenue → P1
   treated as unreliable). P1 fell 0.380 → 0.210 and pillar spread blew out to
   0.66 (the widest in the combined corpus). But the composite MI barely moved
   (0.55 → 0.49) because the GDP-per-capita gap leaves P4 artificially high — a
   case the framework would *mis-rank* without the explicit gap flag.
3. **Colombia is a passing hard stress-test of Safeguard I (porosity-with-
   backstop).** Moderate, flat national P1 (0.491) with a sovereign backstop
   predicted localized violence resurgence in FARC-vacated periphery *without*
   permanent secession — exactly the post-2016 pattern (social-leader
   assassinations, ELN/dissident expansion) against a stable centre.
4. **DRC/Rwanda is a textbook Mod4-then-divergence sequence.** 1996 P1 gap (0.096)
   was inside the margin → abstain; by 2023 the gap (0.341) is decisive and the
   reconstruction outcomes diverged sharply. Safeguard D (predatory neighbour)
   confirmed by Rwanda-backed M23 in eastern DRC.
5. **Rwanda does NOT embarrass the framework — under composite P1.** The proposal's
   "high effectiveness / bottom-tier voice" worry is much milder in the 2025-
   anchored vintage (capacity−accountability gap +0.030, inside the margin).
   Composite P1 (0.594) correctly predicts realized stability + human-development
   gains; the voice deficit is a latent, not-yet-realized reversal flag.

## Details

### CASE 21 — Haiti vs. Dominican Republic (shared-island divergence; pre-event 1996)

**1. Pre-event indicators (1996; WGI 2025-anchored 0-100, UNDP, WB WDI)**

| Indicator | Haiti | Dominican Republic |
|---|---|---|
| WGI Gov Effectiveness | 25.02 | 45.45 |
| WGI Rule of Law | 32.96 | 46.64 |
| WGI Regulatory Quality | 32.25 | 46.04 |
| WGI Control of Corruption | 28.31 | 44.42 |
| WGI Political Stability | 48.78 | 62.58 |
| GDP per capita PPP | $2,070 | $5,161 |
| HDI / LE index / Edu index | 0.479 / 0.556 / 0.377 | 0.631 / 0.763 / 0.489 |
| Resource rents %GDP | 0.94 | 0.70 |

**2. Calculated 1996 scores** — Haiti: P1 0.296, P3 0.467, P4 0.554, P5 0.488 →
**MI 0.424** (Tier 3), spread 0.258. DR: P1 0.456, P3 0.626, P4 0.791, P5 0.626 →
**MI 0.597** (Tier 3), spread 0.334. *(P5 1996 = political stability alone; FSI
pre-2006 unavailable — Track 2, flagged not interpolated. P2 gap both.)*
**P1 gap 0.160 > 0.10 margin → Mod4 does NOT abstain; ordinal warranted.**

**3. Safeguards** — None triggered mechanically (no fragmentation event, low rents,
no external admin). Haiti vulnerability is endogenous low-P1, not a safeguard case.

**4. Blind predictions** — (a) **DR > Haiti** trajectory (P1 ordinality, gap above
margin). (b) Violence RISK higher for Haiti (P1 bottom-third → critical), Mod8: risk
not agency. (c) **Divergence** (P1 gap above 0.15). (d) Haiti's primary failure
dimension = P1/institutions; DR succeeds on P4/P1. (e)–(h) N/A (no fragmentation,
no transition, no suppression event, no sub-state turbulence).

**5. Post-event data (2023)**

| | Haiti 1996→2023 | DR 1996→2023 |
|---|---|---|
| MI | 0.424 → 0.415 | 0.597 → 0.657 (Tier 2) |
| P1 | 0.296 → 0.222 | 0.456 → 0.500 |
| P5 | 0.488 → 0.315 | 0.626 → 0.618 |
| GDP PPP | $2,070 → $3,292 | $5,161 → $25,840 |
| HDI | 0.479 → 0.554 | 0.631 → 0.776 |

**6. Scoring** — (a) **CONFIRMED** (DR upper-middle-income/Tier 2; Haiti stagnant,
P1 falling). (b) **CONFIRMED** (Haiti: 2021 presidential assassination, gang
control of the capital, 2024 state collapse; DR peaceful). (c) **CONFIRMED** (MI
gap 0.17 → 0.24; GDP ratio ~2.5× in 1996 → ~7.8× in 2023). (d) **CONFIRMED**
(Haiti's P1 the floor pillar; DR's P4/P1 the engine).

**7. Case finding** — The Acemoglu-style natural experiment passes cleanly: shared
island, divergent institutions, divergent outcomes, and a P1 gap comfortably
outside the margin. Caveat: P2 (innovation) is a gap for both; the result rests on
P1/P3/P4/P5.

### CASE 22 — Venezuela (rentier capture and collapse; pre-event ~1998)

**1. Pre-event indicators (1998)** — GE 33.43, RL 43.88, RQ 42.87, CC 31.63, VA
54.65, PV 57.33; GDP PPP (1996) $13,824; resource rents 23.84% GDP, oil ≈ 60% of
fiscal revenue; HDI (1996) 0.690. *(1998 HDI sub-indices not isolated → P3 gap at
1998, flagged; FSI pre-2006 N/A.)*

**2. Calculated scores** — 1998: P1 0.380, P4 0.802, P5 0.573 → **MI 0.545** (Tier
3), spread 0.423. 2018: P1 0.185, P5 0.409, **spread 0.692**; **MI 0.494**. 2023:
P1 0.210, P5 0.364, spread 0.662, **MI 0.492** (Tier 3). **GDP per capita
unpublished since 2011 → P4 computed from rents+ODA only → P4 artificially 0.87.**

**3. Safeguards** — **E (rentier capture) TRIGGERED, bidirectional**: oil ≈ 60% of
revenue (>50%) → measured P1 unreliable; the positive arm (low P1 + rents → rent-
funded cohesion, Chávez/Maduro loyalty buying) also flags. G: authoritarian
reversal mechanism present.

**4. Blind predictions** — (a) **Sharp negative trajectory** (P1 falling + rentier
capture on a commodity shock). (b) Elevated violence/repression RISK as P1 falls
(Mod8: risk, not agency). (c) Divergence from its own prior path. (d) Primary
failure = P1 collapse compounded by rentier P4 distortion; **explicit flag: the
composite MI will UNDERSTATE the collapse while GDP is unpublished — read P1, P5,
and spread, not MI.** (e) No territorial fragmentation predicted (state stays
intact, authoritarian).

**5. Post-event** — Real outcome: 88% GDP contraction 2013–2020 (IMF), ~7.7M
emigrants, hyperinflation, Maduro entrenchment, contested 2024 election — but **no
territorial breakup**. P1 0.380 → 0.210; P5 0.573 → 0.364; spread → 0.66.

**6. Scoring** — (a) **CONFIRMED** on direction (P1/P5 collapse), **PARTIAL** on
the composite MI magnitude (gap-inflated P4 masks the depth — coded partial and the
limitation stated plainly). (b) **CONFIRMED** (repression, mass exodus). (d)
**CONFIRMED** (E textbook). (e) **CONFIRMED** (intact authoritarian state, no
fragmentation).

**7. Case finding** — Confirms the resource-curse-collapse thesis AND surfaces the
batch's most important methodological lesson: a missing-data gap can flatter a
collapsing state. The fix is the discipline the framework already mandates — flag
the gap, never interpolate, and lean on P1/P5/spread.

### CASE 23 — Colombia (FARC peace; peripheral porosity-with-backstop; pre-event 2012)

**1. Pre-event indicators (2012)** — GE 49.30, RL 49.26, RQ 58.36, CC 39.56, VA
55.93, PV 43.15; GDP PPP $12,093; resource rents 8.3% GDP; HDI 0.748.

**2. Calculated scores** — 2012: P1 0.491, P3 0.752, P4 0.794, P5 0.431 → **MI
0.599** (Tier 3), spread 0.363. 2023: P1 0.491 (flat), MI **0.621** (Tier 2),
spread 0.399.

**3. Safeguards** — **I (porosity-with-backstop) TRIGGERED**: sovereign central
state retains a military/constitutional backstop while ceding de facto control of
FARC-vacated periphery → predict re-consolidation attempts / recurrence, not
permanent secession. (G classifies the mechanism as unclassified-suppression; the
operative safeguard here is I.)

**4. Blind predictions** — (a) Stable-to-improving national trajectory (mid P1,
above the capacity gate). (b) **Localized** violence RISK in the periphery, not
national civil war (Mod8: risk not agency). (g)/(I): porosity-with-backstop →
peripheral violence resurgence, no secession; backstop holds the centre. (h)
Sub-state turbulence plausible but below collapse threshold.

**5. Post-event** — 2016 Havana accord; FARC demobilized; **social-leader and
ex-combatant assassinations surged** as ELN, FARC dissidents and clan groups moved
into vacated zones; "paz total" stalled; the central state and macro-stability held
(P1 flat, MI rose to Tier 2).

**6. Scoring** — (a) **CONFIRMED** (stable centre, Tier 2). (b) **CONFIRMED**
(localized periphery violence, no national war). (I) **CONFIRMED** (recurrence-
prone peripheral violence, no permanent secession — the backstop translated into
centre stability but not peripheral control, exactly the Safeguard I shape).

**7. Case finding** — Safeguard I survives a case explicitly chosen to *falsify* it.
The failure mode it predicts (capacity vacuum in ceded territory despite a stable
sovereign) is precisely what occurred.

### CASE 24 — DR Congo vs. Rwanda (Central Africa divergence; pre-event 1996)

**1. Pre-event indicators (1996)** — DRC: GE 19.37, RL 26.78, RQ 22.46, CC 10.85,
PV 20.25; GDP PPP $526; rents 36.3% GDP; HDI 0.386. Rwanda: GE 25.95, RL 30.75, RQ
29.74, CC 31.59, PV 30.16; GDP PPP $499; rents 12.56% GDP; HDI 0.297.

**2. Calculated 1996 scores** — DRC: P1 0.199 → **MI 0.277** (Tier 4), spread 0.197.
Rwanda: P1 0.295 → **MI 0.284** (Tier 4), spread 0.052. **P1 gap = 0.096 < 0.10
margin → Mod4 ABSTAIN on the 1996 near-term ranking; predict divergence over the
reconstruction horizon instead.**

**3. Safeguards** — **D (predatory neighbour) TRIGGERED** for DRC (Rwanda/M23 in the
east). **E** flags DRC (rents 38.8% GDP + low P1 → bidirectional). B not applicable
(no successor-state fragmentation).

**4. Blind predictions** — (a) **ABSTAIN at 1996** (gap within margin); predict
**divergence** as reconstruction proceeds, with Rwanda the likelier riser given its
marginally higher, and faster-consolidating, P1. (b) Both high violence RISK
(Great Lakes wars). (c) **Divergence**. (d) DRC fails on P1 + rentier P4; Rwanda's
risk is the accountability/voice deficit (latent). (D) DRC outcome partly exogenous
(predatory neighbour) — separate from endogenous capacity.

**5. Post-event (2023)** — Rwanda MI 0.284 → 0.579 (Tier 4→3), P1 0.295 → 0.594,
HDI 0.297 → 0.578, GDP $499 → $3,399. DRC MI 0.277 → 0.338 (Tier 4), P1 0.199 →
0.253, HDI 0.386 → 0.522, GDP $526 → $1,731; chronic eastern conflict (M23).

**6. Scoring** — (a) 1996 abstention **CONFIRMED as correct discipline** (the gap
was genuinely too close to call ex ante); divergence prediction **CONFIRMED** (2023
gap 0.341, decisive). (b) **CONFIRMED** (both violent; DRC east still at war). (c)
**CONFIRMED**. (d) **CONFIRMED** (DRC P1 floor; Rwanda's residual risk is voice,
not capacity). (D) **CONFIRMED** (Rwanda-backed M23).

**7. Case finding** — A clean demonstration of the Mod4 → divergence sequence: the
framework refuses a too-close 1996 ranking, then is vindicated by a decisive 2023
gap. The pairing also isolates the effectiveness/voice question that motivated the
architectural decision (Case 25).

### CASE 25 — Rwanda (developmental authoritarianism; the architectural stress case)

**1. Pre-event indicators** — 1996 (post-genocide floor): P1 0.295, MI 0.284 (Tier
4). 2023: GE 59.29 (+0.41 est), RL 58.19 (+0.07), RQ 58.41 (+0.23), **CC 61.64
(+0.68)**, **VA 47.62 (−0.53)**, PV 66.54; HDI 0.578; GDP PPP $3,399; rents 4% GDP.

**2. Calculated 2023 scores** — Composite P1 **0.594**; P3 0.623, P4 0.587, P5 0.492
→ **MI 0.579** (Tier 3), spread 0.132 (narrow — a balanced, capacity-led profile).
Decomposition test: capacity (GE,RQ) 0.589 vs. accountability (RL,VA,CC) 0.558 —
gap **+0.030, inside the margin** (see architectural decision doc).

**3. Safeguards** — G (suppression typology): legal/institutional, "managed"
(Tier 2-ish). **Proposed (not yet implemented) Safeguard-C extension** would flag a
latent reversal/succession risk for this high-capacity/low-voice profile even though
`is_democratic_transition` is false — recommended for testing on Vietnam/Gulf/
Singapore before any code change.

**4. Blind predictions** — (a) **Stability-with-latent-reversal-risk**: high
effectiveness/corruption-control drive a positive trajectory; (b) low violence RISK
near-term given high PV and effectiveness, but elevated *succession/reversal* risk
from the voice deficit (latent). (d) Primary residual vulnerability = accountability/
voice, NOT capacity. **Falsification conditions (pre-registered):** (i) collapse
*despite* high effectiveness; (ii) liberalization *despite* low voice.

**5. Post-event** — Two decades of stability, no turnover; HDI 0.189 (1994) → 0.578
(2023); strong growth; low measured corruption; continued tight political control
(VA −0.53). Neither falsification condition has occurred.

**6. Scoring** — (a) **CONFIRMED** (realized stability + development; composite P1
predicts this correctly — the decomposition would have biased toward a fragility
miscall the record refutes). (b) **CONFIRMED** near-term; reversal-risk prediction
**OPEN/PROSPECTIVE** (latent, not yet falsifiable). (d) **CONFIRMED** structurally
(voice is the depressed dimension).

**7. Case finding** — Rwanda is *not* the framework-breaker the proposal feared —
once scored on the canonical 2025-anchored vintage and with P1 kept composite. The
honest residual is that part of this "confirmation" is prospective: the predicted
latent reversal risk cannot be scored until it resolves, so it is logged as an open
forecast, not a closed win.

## Batch scorecard (this run)
- Discrete predictions scored: ~24. Clean CONFIRMED ~18 (~75%); PARTIAL ~2
  (Venezuela MI-magnitude; one DRC/Rwanda 1996-abstention coded as discipline);
  OPEN/prospective ~2 (Rwanda reversal; carried forward); **FALSIFIED: 0**.
- Directional accuracy ~100%, with the standing caveat that near-zero falsification
  is partly structural (the framework is directional/ordinal and hard to falsify).
- P1 ordinality: confirmed in every case where the gap exceeded the margin (21, 22,
  23 self, 24-2023, 25); correctly **abstained** where it did not (24-1996).

## Recommendations
1. **Adopt the GDP-gap discipline as a standing rule.** When a headline economic
   indicator is unpublished (Venezuela), annotate that the composite MI is unreliable
   and read P1/P5/spread. Consider a future engine flag that down-weights or marks
   MI when P4 is missing its GDP component.
2. **Carry Rwanda's reversal-risk prediction as a tracked prospective forecast** with
   the two pre-registered falsification conditions, and re-test the proposed
   Safeguard-C extension on Vietnam (31), the Gulf (42) and Singapore (49) in later
   batches before any structural change.
3. **Keep P1 composite** (architectural decision); do not split P1 on current
   evidence.

## Caveats (carried forward)
- **WGI 2025 vintage break.** All Batch-1 P1/P5 inputs use the 2025-revised anchored
  0-100 scores (`GOV_WGI_*.SC`); the 20-case baseline (estonia.json + runs 1–6) used
  legacy percentile ranks. The two are *not* directly comparable in level — never
  assert an ordinal across the vintage boundary. The framework's scoring mechanics
  are unaffected (both are 0-100), only absolute MI levels shift.
- **Capacity partly redundant with WGI standalone** — the same caveat as the baseline.
- **Zero-falsification is partly by construction** — directional claims are hard to
  falsify; this is a limitation, not a strength.
- **Missing data flagged, never interpolated:** Venezuela GDP (post-2011), 1998 HDI
  sub-indices, pre-2006 FSI (Track 2), and P2 (innovation/ECI) for all five — each
  recorded as a gap in the country files, not filled.
- **P3 sub-indices** are computed from UNDP HDR 2025 raw components via the standard
  UNDP formulas (LE index, education index); they track but do not exactly equal
  UNDP's published rounded sub-indices.
- **Resource-rents context** uses the most recent published WB value where the
  scoring year's value is unavailable (annotated in each file), not an interpolation.
