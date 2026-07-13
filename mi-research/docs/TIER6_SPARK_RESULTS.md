# Tier 6 — Spark Probability — Results

Frozen prereg sha256 `9784e84f`. Code `scripts/v2/tier6_spark.py`; data
`data/political/{tier6_indicators,six_tier_snapshot}.json`. n=114 (T5-scored democracies),
crisis = conflict-or-backsliding 2013–2024.

> **The claim:** the spark is idiosyncratic, but the *rate* at which potential triggers arrive
> is structural (Israel > Iceland) — geography, resources, transcendent contestation, military
> dynamics, all measurable. Tier 6 = spark density.

## Verdict: the tier EARNS its place as a predictor — the fancy hypotheses do not

**Face validity is strong.** Most spark-dense: **Iraq 93** (all four sub-dims maxed), Iran 81,
DR Congo 79, Sudan 73, Chad 70, Mali 68, Algeria 65, Myanmar 63, Egypt 63, **Armenia 63**
(Nagorno-Karabakh), Russia 61, Afghanistan 57, **Ukraine 54** (Crimea/Donbas). Exactly the
conflict-ridden, resource-rich, transcendently-contested, coup-prone environments.

- **T6-6 (Netherlands) — PASS.** Netherlands T6 = **2**, rank **8/156, bottom decile.** Peaceful
  maritime neighbourhood, no resource prize, no transcendent contestation, NATO-deterred, no
  coup tradition — the lowest-spark-density major economy. The construct behaves.
- **T6-1 — spark density is a strong, INDEPENDENT crisis predictor.** T6-alone AUC = **0.652**;
  it **adds +0.22 over T5** criticality. Spark density carries real crisis information that
  proximity-to-tipping does not. (T5 alone is weak here, 0.41, because the mixed cross-sectional
  outcome dilutes its backsliding-specific countdown — see Tier 5's own validation.)
- **T6-4 — the six-tier ensemble is the best model, but the interaction hypothesis FAILS.**
  The **full six-tier model (V1+V3+T4+T5+T6+T5×T6) reaches AUC 0.712** — beating every subset,
  so the complete architecture does add up. BUT the pre-registered **T5×T6 interaction is
  negative and non-significant** (coef −0.68, z=−1.07) — "criticality × spark-density is the
  sharpest configuration" is **not supported.** The tiers combine *additively*, not in the clean
  multiplicative way theorized.

## The nulls (reported, per the rules)
- **T6-2/3 — NULL.** Spark density does **not** explain Tier 5's errors: flickering-but-no-crisis
  countries (mean T6 24) and calm-but-crisis countries (mean T6 26) have *the same* spark density.
  The theory that low-T6 protects critical systems / high-T6 pushes calm ones is not borne out.
- **T6-5 — REFUTED (and this is the interesting one).** The predicted dominance of **transcendent
  contestation (S3)** does not hold. **Geography (S1) dominates** (AUC 0.637, joint coef +0.48);
  S2 resources 0.57, **S3 transcendent 0.55**, S4 military 0.50. The most powerful spark-density
  source is a violent *neighbourhood*, not sacred/contested *ground*. The novel S3 dimension is
  real and face-valid (Israel/Iraq/Armenia/Ukraine top it) but **secondary** — identity-driven
  meaning is a genuine spark source, just not the master one.

## Honest bounds
- **S1 uses neighbour V3+T4**, so part of its predictive power is **conflict diffusion / spatial
  autocorrelation** (a country's crises correlate with its neighbours') — a real channel, but it
  blurs the line between "exogenous spark density" and "you're in a bad region." Disclosed.
- **S3/S4 are hand-coded** (religious sites, territorial claims, alliances, coup-proneness) — the
  most interpretive inputs; documented in the engine, but not mechanical.
- Cross-sectional, mixed outcome, n=114. A cleaner test would separate conflict from backsliding
  and use the proper T5 countdown.

## What it does to the Mule
Tier 6 **shrinks the Mule as claimed** — the *arrival rate* of triggers is structural,
measurable, and independently predictive of crisis (AUC 0.65, +0.22 over criticality). "The
trigger is unmeasurable" becomes "the **specific spark** is unmeasurable, but its **arrival rate
is a structural property of geography, resources, and contestation.**" What it does **not** do:
confirm the elegant capstone (criticality×spark-density multiplier) or crown transcendent
meaning as the master driver. The honest picture is plainer and still valuable: **six structural
layers, best used together (AUC 0.71), reduce the Mule to a fraction — the moment stays dark, but
the density of moments is lit.**
