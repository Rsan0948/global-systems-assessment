# Movement signal — exploration beyond crisis (the muddle, the ascents, the hidden drift)

**Date:** 2026-06-28. **Prompt:** the corpus is all negative-tail (crises). Where's the signal in
*upward* movement, in the middle of the pack, in "stability that isn't"? **Method:** dropped the
crisis lens entirely; characterized **movement** (Δ pillars 2012→2024, with the 2018 midpoint for
momentum) across all **142** panel countries. **Status: EXPLORATORY** — descriptive structure on real
data, *not* validated predictors. Don't force-fit; several of these actively warn against over-reading.

## Finding 1 — the P3 "ratchet" masks institutional drift ("hollow stability")
- **P3 (human capital) rose in 97% of countries** (mean ΔP3 **+0.044**, the largest of any pillar),
  while **P1 (institutions) *fell* in 50%** (mean ΔP1 ≈ 0).
- Because P3 ratchets up almost everywhere, **headline MI stays flat while the governance core erodes
  underneath.** The archetype is the advanced democracies — US, UK, France, Germany, Canada, Sweden,
  Belgium, Australia, NZ all show *flat MI hiding P1 erosion masked by rising P3*.
- This is the answer to "levels that feel like stability but aren't": lived experience (health,
  education) keeps improving, so it *feels* stable, while institutions quietly slip. **Read the
  governance core (P1, or P1+P5), not headline MI**, to see it.
- ΔMI correlates with ΔP4 (+0.75), ΔP5 (+0.67), ΔP1 (+0.56), ΔP3 (+0.30) — so headline movement is
  driven by income and stability swings; the predictive pillar (P1) is a secondary driver and the
  ratcheting pillar (P3) contributes least to *direction*. Headline MI movement is a poor proxy for
  governance change.

## Finding 2 — most "golden ages" are mirages (windfall vs real ascent)
Of 32 risers (ΔMI > +0.03):
- **17 are P4-led** — almost all petrostates on an income windfall with institutions flat (Saudi,
  Iraq, Kuwait, UAE, Qatar, Azerbaijan, Kazakhstan, Angola). A rising MI here = income rose = the
  **durability gap widening**, i.e. fragility building, not progress.
- **~11 are P1/P5-led real ascents** — the rare durable climbs: Uzbekistan (P1+0.15), Côte d'Ivoire
  (post-conflict P5/P1), China (P5/P1); in the middle band: Malaysia, Romania, Albania, Indonesia,
  Dominican Republic, Greece (post-2015 institutional rebuild), Egypt, Kyrgyzstan.
- **Decompose a rise by its lead pillar before calling it good news.** P4-led = windfall (check
  Safeguard J / rents); P1/P5-led = real.

## Finding 3 — there is no momentum (institutional change is episodic)
- **corr(core movement 2012–18, core movement 2018–24) = +0.10** — essentially zero. A country
  moving up in one period is **no more likely** to keep moving. Institutional change is
  shock/episodic, **not inertial** — you cannot extrapolate a rise; golden ages have no flywheel.
- This coexists with the lead-time finding that *levels* are sticky (predictable 10–28y out): the
  level persists, but the small movements around it are not a trajectory. Forecasting implication:
  trust the level, distrust the slope.

## Finding 4 — P2 (innovation) is the only globally-declining pillar
Mean ΔP2 = **−0.026** (every other pillar flat or rising). A quiet, broad innovation-pillar slide —
sharpest among mature democracies (the earlier "innovation drag"), but global. Worth tracking; not
yet tied to any outcome.

## The candidate discrete variable — a MOVEMENT TYPOLOGY
The latent structure isn't a crisis flag; it's the **composition/quality of movement**, which the
headline level hides entirely. Four classes from the pillar-lead + core-vs-headline divergence:
- **Real ascent** — P1/P5-led rise (durable; rare).
- **Windfall** — P4-led rise, P1 flat (fragile; gap-widening; most petro "golden ages").
- **Hollow stability** — MI flat/up while the governance core (P1) erodes under the P3 ratchet (the
  advanced-democracy drift; "feels stable, isn't").
- **Genuine decline** — P5/P4-led fall (Sahel cohesion collapse; war/default shocks).
- **Ratchet rise** — P2/P3-led rise (human-capital/innovation, neither income nor institutions; e.g.
  India) — the global-development tide, not governance.

Applied to the G20, the G7 democracies (US, UK, France, Canada, Belgium, Sweden, Australia) cluster
as **hollow_stability**; China/Indonesia as **real_ascent**; Saudi as **windfall**; Brazil as
**decline** — a split the headline MI completely hides.

This is descriptive and **not yet outcome-validated** — but it cleanly separates progress-that-lasts
from income-luck and stability-that's-hollowing, none of which the MI level or the durability gap
distinguishes. Reproduce with `scripts/big_signals_scan.py --movement` (any country / set / panel).

## Honest caveats
- 142 countries × 3 timepoints (2012/2018/2024); movement over one ~12y window — short for momentum
  claims (the +0.10 is suggestive, not definitive).
- P3 from HDI sub-indices ratchets partly by construction (life-expectancy/education rarely fall) —
  the "masking" is real but partly a measurement property of P3, which is itself the point.
- No crisis outcomes attached — this is structure/typology, a *generator of hypotheses and cases*,
  not a validated rule. Natural next step: attach outcomes to the windfall and hollow-stability
  classes (do windfall ascents reverse when commodity prices fall? does hollow stability precede the
  governance-core falls?).
