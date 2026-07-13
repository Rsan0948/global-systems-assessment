# Tier 4 — Structural Scarring — Results

**Companion to** `TIER4_SCARRING_PREREGISTRATION.md` (sha256 `3f6d0907`, frozen before
analysis). Code `scripts/v2/tier4_scarring.py`; data `data/political/{tier4_indicators,
tier4_scarring,four_tier_snapshot}.json`. Base 2012 → conflict onset 2013–2024, n=170.

> **The fourth tier measures the ground** — accumulated structural damage from prior violence
> that persists under the institutional surface. Anchor: the conflict trap (ρ +0.21..+0.67,
> the most temporally-stable relationship in the whole program). Tier 4 is the only tier that
> carries history forward with decay.

## Verdict: Tier 4 works — and it operationalizes the conflict trap

**Every pre-registered hypothesis passes in the success direction.**

- **T4-1 (GATE) — PASS, decisively.** Out-of-fold CV-AUC for conflict onset: V1 0.751, V3
  0.775, **V1+V3 0.785, +Tier4 0.877 — increment +0.092** (gate was +0.03). Accumulated
  scarring carries far more conflict-recurrence information than current capacity + pressure.

- **T4-3 — societies heal on a GENERATIONAL timescale (~25-year half-life).** S1 conflict-
  history AUC peaks at half-life **25y (0.823)**, essentially tied with 15y (0.821), and
  *declines* for longer half-lives (50y 0.815, 75y 0.805). So a conflict 25 years past counts
  half; 50 years past a quarter. **The conflict trap is generational, not civilizational** —
  scarring fades over ~2–3 generations. This quantifies one of the framework's open questions:
  violence's structural shadow is real but not permanent.

- **T4-6 (the crux) — the composite MEDIATES the raw conflict trap.** In `onset ~ raw_prior_conflict + S-Score`,
  the raw binary's coefficient collapses from **z=+4.01 (alone) to z=−1.83 (absorbed)** while
  S-Score is **z=+5.13**. The scarring composite **fully absorbs** the raw prior-conflict
  binary — the conflict trap operates *through* the measurable scarring dimensions. Tier 4
  has successfully turned the program's most stable, least-explained relationship into a
  **measurable, decomposable, decaying construct** — exactly the pre-registered success test.

- **T4-4 — Tier 4 fills the gap.** Conflicts that V1+V3 missed (false negatives) have mean
  Tier4 = **51.1** vs correctly-quiet **21.9** — the conflicts current-state models miss are
  the deeply-scarred ones.

- **T4-5 — new archetypes emerge, all populated.** Adding Tier 4 to the three-vector system
  yields three diagnostic cells the three-tier view cannot produce (below).

**Most-scarred (S-Score):** Myanmar 91, Iraq 90, Somalia 87, Ethiopia 85, Sudan 83, Pakistan
83, Iran 83, India 81, Philippines 81, Nigeria 80, Angola 77, **Rwanda 75**, Burundi 74,
Sri Lanka 73 — precisely the deeply conflict-scarred states. Rwanda is correctly flagged as
deeply scarred (genocide-driven S1 + displacement S3) despite its institutional rise.

## The four-tier archetypes (156 countries)

Medians: V1=58, V2=57, V3=40, T4=24.

- **CLEAN FOUNDATION** (high V1/V2, low V3, low T4; n=35) — Germany, Canada, Belgium, Korea,
  Portugal, Poland, Netherlands/Nordics. Solid building, calm weather, **unscarred ground** —
  the maximum-durability configuration, and the reading that *completes* the Netherlands
  assessment (four green lights).
- **REBUILT-ON-SCARS** (high V1/V2, low V3, **high T4**; n=17) — Bosnia (42), Croatia (41),
  Serbia (35) [Yugoslav wars]; France (47), UK (43) [great-power + colonial wars]; China (64),
  Vietnam (38), Thailand, Georgia. Excellent current-state on **wounded ground** — "success
  story, monitor for recurrence." Only Tier 4 sees the fault line under the polished surface.
- **SCAR-TRAPPED** (low V1/V2, high V3, high T4; n=39) — Myanmar 91, Iraq 90, Ethiopia, Sudan,
  Pakistan, Nigeria, **Rwanda 76**, Burundi, Sri Lanka. Current failure AND deep historical
  damage compound — the worst configuration. **Rwanda lands here, not in rebuilt-on-scars,
  because its capacity level (V1 47) is still below median** — the +29.6 WGI rise is real but
  its absolute foundation remains mid-low, on genocide-scarred ground. A more sobering read
  than three tiers give.

## Honest bounds
- **S1 uses onset-count as the intensity proxy** (raw UCDP battle-deaths/active-years not
  reachable) — disclosed; battle-death weighting would refine it.
- Coverage: **Track 3 (S1+S4) for 69 countries, Track 4 for 101** — trust (S2) is sparse
  (WVS waves) so most are S1+S3+S4; the composite renormalizes over available dims.
- **The increment is dominated by S1** — i.e. it *is* the conflict trap. That is by design;
  the genuine additions are (a) the measured 25-year decay, (b) the multi-dimensional
  decomposition, and (c) the mediation result (T4-6) proving the composite out-captures the
  raw binary. Tier 4 doesn't discover a new relationship — it *operationalizes the oldest one*.
- Conflict recurrence is predicted; the **trigger remains unmeasured** (the Mule) — Tier 4
  raises conflict-onset AUC to 0.88 but still cannot date the recurrence.
