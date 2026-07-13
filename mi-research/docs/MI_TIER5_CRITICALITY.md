# Tier 5 — Criticality (the timing tier) + the Criticality Principle

> **⚠ AUDIT CORRECTION (2026-07-12) — read before the claims below.** An adversarial audit found
> the original CSD "countdown" headline (*variance rises monotonically 3.6×→7.4×, 84% within-
> country, AUC 0.689, every era*) was compromised by cross-country confounding, pseudoreplication
> (overlapping windows counted independent → fake p-values), and a lead gradient on shifting
> subsets. The corrected analysis (`scripts/v2/csd_corrected.py` → `data/political/csd_corrected.json`;
> country-clustered, one obs per backsliding *episode*, matched windows, fixed cohort) shows:
> **within-country variance IS elevated before backsliding (81% of 240 episodes, country-clustered
> 95% CI excludes 0) — the signal survives — but it is NOT a clean monotonic countdown, the
> theory-canonical AR1 indicator is NULL (AUC 0.51, p=0.33), and the effect is partly mechanical.**
> Out-of-fold, T5 alone is near-chance as a cross-country predictor (AUC 0.48). Tier 5 flags
> *turbulence/ripeness before rupture*, diagnostically and within-country — NOT a calibrated
> accelerating clock. Treat every "countdown / monotonic / AUC 0.689 / 84%" statement below as
> superseded by this banner.

**A fifth tier, and unlike any of the first four.** V1–V4 all answer *how vulnerable?* —
capacity, delivery, pressure, scarring, each a state or a stock. **Tier 5 answers *how
close?*** It is the only tier that speaks to *timing*, and it is grounded in a founding rule
the program's own physics implied but never stated:

> **The Criticality Principle.** A system approaching rupture *slows down* — the fluctuations
> in its state variables grow in amplitude and memory (rising variance and autocorrelation) as
> it nears its critical threshold. You cannot predict the spark that tips it, but you can
> measure how close the system is to the slope where any spark cascades — and that measure
> **accelerates toward the release.**

This is self-organized-criticality theory (the sandpile of the fragmentation leg) applied to
the political time series. It is the program's answer to "the Mule": the *spark* stays
unmeasurable, but the *ripeness* does not.

Built + validated 2026-07-12. Pre-registration/hunt `TRIGGER_HUNT_RESULTS.md`; code
`scripts/v2/{trigger_hunt,csd_deep}.py`.

## The empirical warrant (why this tier is real)

Critical slowing down before **democratic backsliding** is one of the most robust regularities
in the whole program (615 events, V-Dem 1800–2018):
- **It is a countdown.** Pre-rupture variance ratio (event÷control) rises *monotonically*:
  3.6× at −12y → 4.9× at −6y → **7.4× the year before collapse.**
- **It is within-country.** Pre-rupture variance exceeds a country's *own* baseline in **84%**
  of events (p<1e-4) — not a cross-country confound.
- **It is temporally invariant.** Significant in every era, 1800–2018 (AUC 0.62–0.67).
- **It is multivariate.** Liberal-democracy, electoral-democracy, and rule-of-law all carry it
  (~0.65) — the whole regime slows together.
- **It is backsliding-specific.** The same test on conflict (GDP-growth) goes null
  within-country — CSD applies to *slow tipping-point slides* (democratic erosion), not to
  exogenous, spark-driven armed conflict.

## What Tier 5 measures

- **Score** = the recent (last ~12y) detrended **variance of the regime state variables**
  (V-Dem liberal-democracy + electoral-democracy + rule-of-law), normalized 0–100; higher =
  more critical = flickering harder = closer to a democratic tipping point. A rising-variance
  trend (the acceleration) is the secondary signal.
- **Scope:** meaningful only where there is a democracy to lose (libdem ≥ 0.15). Deep
  autocracies score **N/A** — they are post-collapse; there is no slope left to slide down.
- **Direction:** higher = worse (consistent with V3/T4).

## Why it is indispensable — it catches what the other four miss

Tier 5 flags **capable, stable-looking democracies that are quietly oscillating toward a tip**
— exactly the cases the first four tiers score green. As of 2024 the most-critical include
**Poland (T5 85), Korea (69), Brazil (85), Romania (77)** — all *Clean Foundation* on capacity/
pressure/scarring, yet flickering hard. (Korea's Dec-2024 martial-law crisis is the flicker
made real.) And the contested middle — **Thailand, Tunisia, Armenia, Moldova, Sri Lanka** —
lights up at the ceiling. No other tier, or the four combined, produces this reading, because
they measure *state*; only Tier 5 measures *approach*.

## Honest bounds
- **A phenomenon, not a clock.** AUC ~0.65 — decisive as a regularity, modest as a classifier.
  It says "the ground has gone critical and is getting more so," not the year or the spark.
- **Backsliding-scoped.** It is not a universal rupture-timer; conflict's trigger is exogenous.
- **The spark holds.** Which event tips a critical democracy, and exactly when, remains the
  irreducible half of the Mule. Tier 5 raises the alarm; it does not name the day.

## Invariants
1. V1–V4 frozen; Tier 5 is additive.
2. Tier 5 is a **timing/risk** signal — report as "how close," never as a date.
3. Preserve the boundary: criticality is measurable; the spark is not.
