# Modernization Index Validation — Run 7: Expansion Batch 1 (Cases 21–25)

> First expansion run beyond the 20-case baseline. Cases per
> `docs/expansion_plan/` recommended sequence: 21 Haiti/DR, 22 Venezuela,
> 23 Colombia, 24 DRC/Rwanda, 25 Rwanda.
>
> **Data source (consistency):** all inputs come from the **committed
> `mi_pipeline/` panel (commit 9487dd0)** — `wb_cached.csv` (WGI 2025-anchored +
> WDI), `cpi.csv`, `gii.csv` (2012/2018/2024), `eci.csv`, `hdr.csv`, `fsi.csv`,
> assembled in `output/mi_scored_countries.csv` — on the panel year grid
> (1996/2004/2012/2018/**2024**). Voice & Accountability is pulled from the WGI
> API (the panel omits it) for the P1-decomposition test only. The mi-research
> engine **reproduces the panel's P1/P2/P3/P5 exactly**; P4 differs by a small,
> documented monotonic rescaling (mi-research uses a fixed absolute GDP reference
> range vs the panel's dataset-relative min-max) — ordinality preserved. Country
> files: `data/countries/*.json`. P1 corruption uses CPI (matches the panel).
>
> The Rwanda architectural decision (P1 composite vs. decomposed) was settled
> FIRST — `docs/architectural_decisions/rwanda_p1_composite_vs_decomposed.md`:
> **P1 kept composite**, so the engine and the 20-case baseline are unchanged.

## TL;DR
- **The P1 ordinal core holds in every case where the gap exceeds the WGI
  margin.** Dominican Republic (P1 0.456 → 0.502) ordinally beat Haiti (0.296 →
  0.223); Rwanda (0.295 → 0.582) ordinally beat DR Congo (0.199 → 0.255);
  Venezuela's P1 collapse (0.392 → 0.192) tracked the largest peacetime economic
  collapse on record. Where the pre-event gap was *inside* the margin (DRC vs.
  Rwanda in 1996, gap 0.096 < 0.10) the framework correctly **abstained** under
  Mod4 and predicted divergence-over-time rather than a near-term ranking.
- **Two honest data-integrity flags carry as much weight as the confirmations.**
  (1) Venezuela's composite MI (0.48) *understates* its collapse because GDP per
  capita has been unpublished since 2011 — P4 is gap-inflated to 0.98; the real
  signal is the P1/P5 collapse and a record pillar spread (0.79). Missing data is
  information: the unpublished-GDP gap *is* the collapse. (2) Rwanda's
  confirmation is partly prospective — its predicted *latent* reversal risk is not
  yet falsifiable, so we code it open, not triumphant.
- **Batch clean confirmation ~75%** (best estimate), directional ~100% with no
  outright falsification — consistent with, and subject to, the same caveats as
  the 20-case baseline (capacity partly redundant with WGI standalone; near-
  absence of falsification is partly structural). Reported as a range, ordinal/
  directional only. (The naive per-letter `--validate` tally reads higher; see
  `data/case_studies/completed/README.md` — do not headline it.)

## Key Findings
1. **Haiti/DR is a clean shared-island confirmation at the low end of P1.** A wide,
   margin-exceeding P1 gap (0.16 in 1996) mapped to divergent outcomes: DR rose to
   Tier 2 (MI 0.585 → 0.617) while Haiti's P1 fell further (0.296 → 0.223) into
   **Tier 4** and state collapse (PM assassinated 2021, gang control of
   Port-au-Prince by 2024). HDI 0.776 (DR) vs 0.554 (Haiti).
2. **Venezuela confirms the rentier-collapse thesis but exposes a measurement
   trap.** Safeguard E fires bidirectionally (oil ≈ 60% of fiscal revenue → P1
   treated as unreliable). P1 fell 0.392 → 0.192 and pillar spread blew out to
   0.79 (the widest in the combined corpus). But the composite MI barely moved
   (0.57 → 0.48) because the GDP-per-capita gap leaves P4 artificially at 0.98 — a
   case the framework would *mis-rank* without the explicit gap flag.
3. **Colombia is a passing hard stress-test of Safeguard I (porosity-with-
   backstop).** Flat national P1 (~0.48, Tier 3) with a sovereign backstop
   predicted localized violence resurgence in FARC-vacated periphery *without*
   permanent secession — exactly the post-2016 pattern (social-leader
   assassinations, ELN/dissident expansion) against a stable centre.
4. **DRC/Rwanda is a textbook Mod4-then-divergence sequence.** 1996 P1 gap (0.096)
   was inside the margin → abstain; by 2024 the gap (0.327) is decisive and the
   reconstruction outcomes diverged sharply (Rwanda Tier 4 → 3; DRC stays Tier 4).
   Safeguard D (predatory neighbour) confirmed by Rwanda-backed M23 in eastern DRC.
5. **Rwanda does NOT embarrass the framework — under composite P1.** The proposal's
   "high effectiveness / bottom-tier voice" worry is mild in the 2025-anchored
   vintage (capacity−accountability gap +0.034, inside the margin). Composite P1
   (0.582) correctly predicts realized stability + human-development gains; the
   voice deficit is a latent, not-yet-realized reversal flag.

## Details

### CASE 21 — Haiti vs. Dominican Republic (shared-island divergence; pre-event 1996)

**1. Pre-event indicators (1996; panel, WGI 2025-anchored 0-100)**

| Indicator | Haiti | Dominican Republic |
|---|---|---|
| WGI Gov Effectiveness | 25.95 | 45.45 |
| WGI Rule of Law | 32.96 | 46.64 |
| WGI Regulatory Quality | 32.25 | 46.04 |
| WGI Political Stability | 48.78 | 62.58 |
| GDP per capita PPP | ~$2,070 | ~$5,161 |
| HDI (latest) | 0.554 | 0.776 |

**2. Calculated scores** — Haiti 1996: P1 0.296 → **MI 0.427** (Tier 3), spread
0.258. DR 1996: P1 0.456 → **MI 0.585** (Tier 3). **P1 gap 0.160 > 0.10 margin →
Mod4 does NOT abstain; ordinal warranted.** (1996 P5 = political stability alone;
FSI pre-2006 unavailable — Track 2, flagged not interpolated.)

**3. Safeguards** — none triggered mechanically (no fragmentation event, low rents,
no external admin). Haiti's vulnerability is endogenous low-P1.

**4. Blind predictions** — (a) **DR > Haiti** trajectory (P1 ordinality, gap above
margin). (b) Violence RISK higher for Haiti (P1 bottom-third → critical), Mod8:
risk not agency. (c) **Divergence.** (d) Haiti's primary failure dimension =
P1/institutions. (e)–(h) N/A.

**5. Post-event (2024)** — Haiti: P1 0.296 → 0.223, **MI 0.427 → 0.398 (Tier 4)**,
spread → 0.363; state collapse. DR: P1 0.456 → 0.502, **MI 0.585 → 0.617 (Tier 2)**.

**6. Scoring** — (a) **CONFIRMED** (DR Tier 2; Haiti slips to Tier 4). (b)
**CONFIRMED** (Haiti gang collapse vs DR peace). (c) **CONFIRMED** (divergence). (d)
**CONFIRMED** (Haiti P1 the floor pillar).

**7. Case finding** — Shared-geography natural experiment passes cleanly; P1 gap
comfortably outside the margin.

### CASE 22 — Venezuela (rentier capture and collapse; pre-event 1996)

**1. Pre-event indicators (1996)** — GE 37.16, RL 43.43, RQ 44.04, CC 32.08, VA
54.03, PV 56.43; resource rents ≈ 24% GDP, oil ≈ 60% of fiscal revenue; HDI 0.690.

**2. Calculated scores** — 1996: P1 0.392, P4 0.701, P5 0.564 → **MI 0.569** (Tier
3), spread 0.310. 2018: P1 0.191, spread **0.801**. 2024: P1 0.192, P5 0.304, spread
**0.789**, **MI 0.476** (Tier 3). **GDP per capita unpublished since 2011 → P4
computed from rents+ODA only → P4 artificially 0.98.**

**3. Safeguards** — **E (rentier capture) TRIGGERED, bidirectional**: oil ≈ 60% of
revenue (>50%) → measured P1 unreliable; the positive arm (low P1 + rents → rent-
funded cohesion) also flags. G: authoritarian-reversal mechanism.

**4. Blind predictions** — (a) **Sharp negative trajectory.** (b) Elevated
violence/repression RISK (Mod8). (c) Divergence from its own path. (d) P1 collapse
+ rentier P4 distortion; **flag: composite MI will UNDERSTATE the collapse while GDP
is unpublished — read P1, P5, spread.** (e) No territorial fragmentation (intact
authoritarian state).

**5. Post-event** — 88% GDP contraction 2013–2020 (IMF), ~7.7M emigrants,
hyperinflation, Maduro entrenchment, contested 2024 election — **no territorial
breakup**. P1 0.392 → 0.192; P5 0.564 → 0.304; spread → 0.79.

**6. Scoring** — (a) **CONFIRMED** on direction; **PARTIAL** on composite MI
magnitude (gap-inflated P4 masks the depth — coded partial, limitation stated).
(b) **CONFIRMED.** (d) **CONFIRMED** (E textbook). (e) **CONFIRMED** (no fragmentation).

**7. Case finding** — Confirms the resource-curse-collapse thesis and surfaces the
batch's key methodological lesson: a missing-data gap can flatter a collapsing
state. The fix is the discipline the framework already mandates — flag the gap,
never interpolate, lean on P1/P5/spread.

### CASE 23 — Colombia (FARC peace; peripheral porosity-with-backstop; pre-event 2012)

**1. Pre-event indicators (2012)** — GE 49.30, RL 49.26, RQ 58.36, VA 55.93, PV
43.15; GDP PPP ~$12,093; resource rents ~8% GDP; HDI 0.748. (P1 corruption uses CPI.)

**2. Calculated scores** — 2012: P1 0.482, P3 0.752, P4 0.794, P5 0.364 → **MI
0.573** (Tier 3), spread 0.430. 2024: P1 0.476 (flat), **MI 0.588** (Tier 3),
spread 0.405.

**3. Safeguards** — **I (porosity-with-backstop) TRIGGERED**: sovereign central
state retains a military/constitutional backstop while ceding de facto control of
FARC-vacated periphery → predict re-consolidation attempts / recurrence, not
permanent secession.

**4. Blind predictions** — (a) Stable-to-improving national trajectory. (b)
**Localized** violence RISK in the periphery, not national civil war (Mod8). (I)
peripheral violence resurgence, no secession; backstop holds the centre. (h)
sub-state turbulence below collapse threshold.

**5. Post-event** — 2016 Havana accord; FARC demobilized; **social-leader and
ex-combatant assassinations surged** as ELN, FARC dissidents and clan groups moved
into vacated zones; "paz total" stalled; centre and macro-stability held (P1 flat,
Tier 3).

**6. Scoring** — (a) **CONFIRMED.** (b) **CONFIRMED** (localized periphery violence,
no national war). (I) **CONFIRMED** (recurrence-prone peripheral violence, no
permanent secession — the backstop held the centre but not the periphery).

**7. Case finding** — Safeguard I survives a case explicitly chosen to *falsify* it.

### CASE 24 — DR Congo vs. Rwanda (Central Africa divergence; pre-event 1996)

**1. Pre-event indicators (1996)** — DRC: GE 19.37, RL 26.78, RQ 22.46, CC 10.85,
PV 20.25; GDP PPP ~$526; rents ~36% GDP; HDI 0.386. Rwanda: GE 25.95, RL 30.75, RQ
29.74, CC 31.59, PV 30.16; GDP PPP ~$499; rents ~13% GDP; HDI 0.297.

**2. Calculated 1996 scores** — DRC: P1 0.199 → **MI 0.276** (Tier 4), spread 0.197.
Rwanda: P1 0.295 → **MI 0.329** (Tier 4), spread 0.338. **P1 gap = 0.096 < 0.10
margin → Mod4 ABSTAIN on the 1996 near-term ranking; predict divergence over the
reconstruction horizon instead.**

**3. Safeguards** — **D (predatory neighbour) TRIGGERED** for DRC (Rwanda/M23 in the
east). **E** flags DRC (rents ~39% GDP + low P1 → bidirectional). B not applicable.

**4. Blind predictions** — (a) **ABSTAIN at 1996**; predict **divergence** with
Rwanda the likelier riser. (b) Both high violence RISK. (c) **Divergence.** (d) DRC
fails on P1 + rentier P4; Rwanda's residual risk is voice (latent). (D) DRC outcome
partly exogenous (predatory neighbour).

**5. Post-event (2024)** — Rwanda MI 0.329 → 0.503 (Tier 4→3), P1 0.295 → 0.582,
HDI 0.297 → 0.578, GDP $499 → ~$3,400. DRC MI 0.276 → 0.313 (Tier 4), P1 0.199 →
0.255, HDI 0.386 → 0.522; chronic eastern conflict (M23).

**6. Scoring** — (a) 1996 abstention **CONFIRMED as correct discipline**; divergence
prediction **CONFIRMED** (2024 gap 0.327, decisive). (b) **CONFIRMED.** (c)
**CONFIRMED.** (d) **CONFIRMED.** (D) **CONFIRMED** (Rwanda-backed M23).

**7. Case finding** — Clean Mod4 → divergence sequence: the framework refuses a
too-close 1996 ranking, then is vindicated by a decisive 2024 gap.

### CASE 25 — Rwanda (developmental authoritarianism; the architectural stress case)

**1. Pre-event** — 1996 (post-genocide floor): P1 0.295, MI 0.329 (Tier 4). 2024:
GE 58.1, RL 58.7, RQ ≈59.1, **CC 60.5**, **VA 46.5**, PV 65.1; HDI 0.578; GDP PPP
~$3,400; rents ~4% GDP.

**2. Calculated 2024 scores** — Composite P1 **0.582**; P3 0.624, P4 0.429, P5 0.483
→ **MI 0.503** (Tier 3), spread 0.309. Decomposition test: capacity (GE,RQ) 0.586
vs. accountability (RL,VA,CC) 0.552 — gap **+0.034, inside the margin** (see
architectural decision doc).

**3. Safeguards** — G (suppression typology): legal/institutional, "managed".
**Proposed (not yet implemented) Safeguard-C extension** would flag a latent
reversal/succession risk for this high-capacity/low-voice profile even though
`is_democratic_transition` is false — recommended for testing on Vietnam/Gulf/
Singapore before any code change.

**4. Blind predictions** — (a) **Stability-with-latent-reversal-risk.** (b) Low
near-term violence RISK; elevated *succession/reversal* risk from the voice deficit
(latent). (d) Residual vulnerability = accountability/voice, NOT capacity.
**Falsification conditions (pre-registered):** (i) collapse *despite* high
effectiveness; (ii) liberalization *despite* low voice.

**5. Post-event** — Two decades of stability, no turnover; HDI 0.189 (1994) → 0.578
(2023); strong growth; low measured corruption; continued tight political control
(VA 46.5). Neither falsification condition has occurred.

**6. Scoring** — (a) **CONFIRMED** (realized stability + development; composite P1
predicts this correctly — decomposition would have biased toward a fragility miscall
the record refutes). (b) **CONFIRMED** near-term; reversal-risk prediction
**OPEN/PROSPECTIVE**. (d) **CONFIRMED** structurally (voice is the depressed dimension).

**7. Case finding** — Rwanda is *not* the framework-breaker the proposal feared —
scored on the canonical 2025-anchored vintage with P1 composite. The honest residual
is that part of this "confirmation" is prospective.

## Batch scorecard (this run)
- Discrete predictions scored: ~24. Clean CONFIRMED ~18 (~75%); PARTIAL ~2
  (Venezuela MI-magnitude; one DRC/Rwanda 1996-abstention coded as discipline);
  OPEN/prospective ~2 (Rwanda reversal); **FALSIFIED: 0**.
- Directional accuracy ~100%, with the standing caveat that near-zero falsification
  is partly structural.
- P1 ordinality: confirmed in every case where the gap exceeded the margin (21, 22
  self, 23 self, 24-2024, 25); correctly **abstained** where it did not (24-1996).
- The naive per-letter `--validate` tally reads higher (~90%); that is the generous
  end and must not be headlined — see `data/case_studies/completed/README.md`.

## Recommendations
1. **Adopt the GDP-gap discipline as a standing rule.** When a headline economic
   indicator is unpublished (Venezuela), annotate that the composite MI is unreliable
   and read P1/P5/spread. Consider an engine flag that marks MI when P4 is missing
   its GDP component.
2. **Carry Rwanda's reversal-risk prediction as a tracked prospective forecast** with
   the two pre-registered falsification conditions; re-test the proposed Safeguard-C
   extension on Vietnam (31), the Gulf (42) and Singapore (49) in later batches.
3. **Keep P1 composite** (architectural decision); do not split P1 on current evidence.

## Caveats (carried forward)
- **Cross-project consistency:** inputs come from the committed `mi_pipeline/` panel;
  mi-research reproduces the panel's P1/P2/P3/P5 (P4 differs by a documented
  monotonic rescaling — fixed absolute GDP reference vs dataset-relative). Ordinality
  unaffected.
- **WGI 2025 vintage break.** Batch-1 P1/P5 inputs use 2025-revised anchored scores;
  the 20-case baseline (estonia.json + runs 1–6) used legacy percentile ranks. Never
  assert an ordinal across the vintage boundary.
- **Capacity partly redundant with WGI standalone** — same caveat as the baseline.
- **Zero-falsification is partly by construction** — directional claims are hard to
  falsify; a limitation, not a strength.
- **Missing data flagged, never interpolated:** Venezuela GDP (post-2011), pre-2006
  FSI (Track 2), GII pre-2012, and the ECI/HDR lag — each recorded as a gap, not filled.
- **Confirmation reported as a range** (batch ~75%); the naive per-letter validate
  count is the generous end and is not the headline.
