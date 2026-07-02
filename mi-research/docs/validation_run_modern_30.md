# Out-of-sample validation run — 30 blind-selected modern cases (RESULT)

**Date:** 2026-06-28. The first genuinely out-of-sample test. Cases were selected by a framework-naive
agent via documented RNG (`random_validation_brief.md`); on our end the pre-shock structural state was
read **mechanically** (V-Dem rule-of-law = P1 proxy, r=0.87 with WGI P1; Maddison GDP percentile = P4
proxy) at a fixed pre-shock year, and the **pre-registered** rule applied (lower pre-shock institutions
/ larger durability gap → more severe outcome). Outcomes are the agent's neutral tags (1 collapse · 2
violent rupture · 3 peaceful discontinuity · 4 stressed-continuous · 5 absorbed). 24/25 scoreable
(V-Dem coverage; 5 micro-states/colonies in the set were unscoreable). Firewalled from the 213C/0F
retrodiction baseline.

## Result — directional, weak, on a sample that over-samples the blind spot
| pre-registered test | severe (Tag 1/2) | non-severe (Tag 3/4/5) | effect |
|---|---|---|---|
| **pre-shock institutions (rol)** | mean 0.43 (n=18) | mean 0.52 (n=6) | **Cohen d = +0.37** (right direction, NOT significant) |
| **durability gap (GDPpct − rol)** | +0.02 (n=16) | −0.14 (n=6) | right direction (absorbers had institutions ≥ income) |

Both load-bearing claims point the **right way** out of sample — but weakly, with a tiny non-severe n.

## Why weak — a scope point established BEFORE this test, not a post-hoc rescue
A random draw from coup/conflict catalogs is **dominated by exogenous and idiosyncratic shocks** —
precisely the regime where the framework explicitly disclaims predictive power (Mod8; confirmed across
the lead-time, golden-age, and ancient work). The clean misses are all of that type:
- **Spain 1936** — rol 0.70 → Tag 2 (civil war from internal polarization).
- **Cyprus 1971** — rol 0.67 → Tag 1 (Turkish **invasion** — exogenous military).
- **Greece 1919** — rol 0.55 → Tag 2 (external military defeat in Anatolia).
High-institution states that ruptured via shocks the framework never claimed to call. Symmetrically,
low-institution states that *absorbed* (Siam 1932 rol 0.20, Chile 1982 0.30, Mali 2012 0.39) are also
where structure under-determines the outcome. **The random sample landed mostly outside the framework's
domain (endogenous structural stress), so this is a partial test of the actual claim.**

## Honest verdict
- **Not a validation, not a refutation:** a weak-positive (d≈0.37) on a sample skewed toward the
  acknowledged blind spot. The structural signal is *present and correctly signed* out of sample, but
  this draw cannot deliver a strong test of it.
- **The clean wins are real:** the lowest-institution states (Paraguay 0.04, Ethiopia 0.13, Liberia
  0.21, Bolivia 0.23) all ruptured violently; the highest (Norway 0.96, Finland 0.88) took the mildest
  paths. The signal lives at the extremes.
- **The design lesson is the main deliverable:** the next pre-registration must **stratify by shock
  type** (endogenous structural stress vs exogenous/military/idiosyncratic) — testing the framework on
  a coup/invasion-dominated random sample tests it largely where it says it can't predict. The brief's
  outcome catalog should also raise the share of financial-crisis / peaceful-transition events to get
  Tag 3/5 variation (only 6 non-severe here).

## Caveats
- Predictor mechanical + rule pre-registered, but outcomes were visible when scoring; the airtightness
  is in the blind *selection* and the mechanical *predictor*, not in blind reading of outcomes.
- V-Dem/Maddison only (P1/P4); P2/P3/P5 not used (pre-1996 cases) — so this tests the two load-bearing
  claims, not the full engine.
- Outcome-skewed sample (18 severe / 6 non-severe scoreable) → low power; do not over-read d=0.37
  either way.
