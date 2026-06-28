# V3.3 — including the level/slope findings properly + does it change the global picture?

**Date:** 2026-06-28. `MI_MODEL_VERSION = "v3.3"`. Additive; the 51-case ordinality baseline is
unchanged (213C/77P/0F), Estonia 0.775. This folds the crisis-lead-time + golden-age work into the
engine **honestly** — adding what validated, refusing what didn't.

## How it's included (and what we deliberately do NOT add)
The unifying, validated epistemic across both programs: **trust the level, distrust the slope.** The
*level* (and the durability gap) carries the predictive content; the *slope* (year-to-year movement)
is mean-reverting noise. Operationalized as:

1. **`ascent_potential(pillars)`** — the *one holdout-validated* golden-age signal: a low institutional
   base (P1 < 0.40) carries elevated room-to-rise (mean-reversion; holdout z+2.4). Flags **eligibility,
   not a forecast** — realized ascent needs an exogenous trigger (transition/commodity era), and recent
   momentum predicts the *opposite* (reversion).
2. **`movement_quality(pillars, prior)`** — the movement typology (real_ascent / windfall /
   ratchet_rise / hollow_stability / decline) **with an explicit distrust-the-slope caveat**. Lets a
   reader see that a rising headline MI is usually income windfall or the P3 human-capital ratchet,
   not governance.
3. **NOT added — the golden-age *signature*.** The CC/component-jump predictor was **refuted on a
   pre-registered geographic holdout** (z=−0.0, 137 events). Adding it would be dishonest. Golden ages
   are exogenous (level + era + commodity), not an internal slope — so the engine flags the *level*
   (ascent_potential) and *names* the movement (movement_quality), and stops there.

Both surface in `full_diagnostic` (movement_quality when a prior timepoint is supplied via
`context["prior_pillars"]`). Breadth tool unchanged: `scripts/big_signals_scan.py --movement`.

## Does it change the global picture?
**The scores and rankings: NO** — everything is additive; no country's MI or verdict moves. **The
trajectory story: YES, profoundly.** Read through the validated lens, "global progress" looks very
different:

| read | headline (naive) | validated lens |
|---|---|---|
| global institutions 2012→24 | MI rising (mean +0.011) | **P1 core FLAT (+0.001); eroding in 50% of countries** |
| what's driving the rise | "improvement" | the **P3 human-capital ratchet** (+0.044, rose in 97%) + **commodity P4** |
| golden ages | — | **drought**: 25 durable climb-starts/yr in 2002–05 → **7/yr in 2015–19** |
| "stable" countries | stable | **45 economies in hollow stability** (institutions eroding while income rose) |

So the global picture flips from *"slow broad improvement"* to **"human-capital and commodity gains
masking a decade of governance-core stagnation, a golden-age drought, and widespread hollow
stability."** The levels didn't change; the *meaning of the movement* did.

## Detail & color
- **The institutions are flat, not rising.** Across 203 economies, mean ΔP1 over 2012–24 is +0.001 —
  statistically nothing — and **half of all countries' institutions eroded.** The apparent global MI
  rise is almost entirely the human-capital pillar (life expectancy/education ratchet up nearly
  everywhere) plus the commodity-era income bump. Strip those and governance has gone sideways-to-down.
- **We're in a golden-age drought.** Durable institutional climbs came in a **2002–05 wave** (post-
  communist transition + EU "big bang" accession + the commodity supercycle onset), a 2006–08 trough,
  a 2010–13 echo, and have since **collapsed to ~7/yr** — a third of the wave rate. The conditions that
  made golden ages (a reform era + a rising commodity tide acting on low-base states) are not present
  in 2014+. This is consistent with the V-Dem "global democratic recession" but measured on the
  governance core, and it explains *why*: the exogenous engines stopped.
- **Hollow stability is the dominant mode of the rich and middling world.** 45 economies show
  institutions eroding while income held or rose — Turkey, Mexico, Chile, Cyprus, several Caribbean
  states, and (from the earlier core analysis) the US/UK/France/Germany cluster. Their citizens
  experience stability (health/education keep improving) while the governance core quietly slips —
  the level the MI now names explicitly (`movement_quality = hollow_stability`).
- **The few real ascents are structural, not earned-by-trajectory.** China, Indonesia (P1/P5-led) and
  the rare middle-band climbers exist, but they're low-base states catching an era — not countries
  that "turned it around" through their own momentum (which mean-reverts).

## Honest limits
- This reframes *interpretation*, not the scores — the MI's levels/rankings and the 51-case baseline
  stand. v3.3 adds reading-discipline diagnostics, not new verdicts.
- ΔP1 ≈ 0 is a real-but-modest window (12y); the P3 ratchet is partly a measurement property of HDI
  sub-indices; the golden-age "drought" partly reflects that recent climbs need 5y+ forward data to
  confirm (right-censoring softens 2019+). The direction is robust; the magnitudes are a window.
