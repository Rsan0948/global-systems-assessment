# Tier 6 — Spark Probability (spark density) — Pre-Registration

**The final tier, and the one that shrinks the Mule.** Tiers 1–4 measure *vulnerability*, Tier
5 measures *criticality* (how close). Tier 6 measures **spark density** — the structural rate
at which potential triggering events arrive at or emerge within a country. The *specific* spark
(which vendor, which election) stays idiosyncratic — but the *rate* (Israel receives more
potential triggers/year than Iceland) is a structural property of geography, resources, identity
contestation, and military dynamics. **The spark is random; the spark density is measurable.**

Frozen before analysis. sha256 on commit.

## Binding rules
1. Pre-register sub-dimensions, equal weights, interaction terms before testing.
2. **Equal weights across S1–S4; never optimize.**
3. **S4 = internal-risk × (1 − external-deterrence)** — net, never collapsed; report components.
4. **S3 (transcendent contestation) is hand-coded** from mechanical proxies (UNESCO religious
   sites, CIA/HIIK territorial-dispute lists, historical atlases). Every coding decision is
   documented in the engine; it is the most interpretive sub-dimension — flagged as such.
5. T6 inherits no validation. It earns its place via its own tests, or it is reported null.
6. Higher T6 = more sparks/time = worse (consistent with V3/T4/T5).

## Data (reachable + hand-coded)
- **S1 Geographic exposure:** neighbour mean (V3 + T4) via land-border adjacency
  (geodatasource borders); refugees *hosted* / population (OWID/UNHCR + WDI pop); maritime
  insulation (island / #land-borders). *(Regional 1000km conflict density approximated by
  neighbour pressure — disclosed proxy.)*
- **S2 Resource incentive:** total natural-resource rents %GDP (WDI NY.GDP.TOTL.RT.ZS);
  export concentration proxied by (inverse) Economic Complexity Index (committed); **strategic-
  resource flag hand-coded** (oil/gas/uranium/lithium/cobalt/strategic-waterway).
- **S3 Transcendent contestation [hand-coded]:** religious-site density (Jerusalem/Mecca/
  Varanasi/Rome/Lhasa…), active external territorial claims (Kashmir/Taiwan/Crimea/W.Sahara/
  Golan…), historical-contestation weight. Extreme for a few (Israel/India/China/Russia/
  Iraq/Ukraine), ~0 for most — as theory predicts.
- **S4 Military dynamics:** internal = mil-spend %GDP (WDI) + coup-proneness (hand-coded from
  known coup history, Powell-Thyne unreachable) + military-in-politics; external deterrence =
  **alliance tier hand-coded** (NATO/US-treaty-ally/nuclear=100; major-non-NATO=70; regional=40;
  none=10) + geographic defensibility. Net = internal × (1 − deterrence/100).

**Coverage:** Track-2 target (S1+S2 mechanical near-universal; S3+S4 hand-coded for ~156).
Composite = equal-weight mean of available sub-dimensions, 0–100 (5th/95th pct).

## Pre-registered hypotheses (outcome = crisis onset [conflict or backsliding] 2013–2024)
- **T6-1 — independence.** Does T6 add AUC over T5 for crisis onset (T5 vs T6 vs T5+T6)?
- **T6-2 — explains T5 false negatives.** Flickering (high T5) countries that did NOT tip —
  are they disproportionately low-T6 (spark-sparse: near the edge but nothing pushes)?
- **T6-3 — explains T5 false positives.** Non-flickering (low T5) countries that DID rupture —
  are they disproportionately high-T6 (pushed by external sparks before internal criticality)?
- **T6-4 (CAPSTONE) — the T5 × T6 interaction.** Regress crisis onset on T5, T6, T5×T6. Is the
  interaction positive/significant (criticality × spark-density = the sharpest pre-crisis
  configuration)? Compare full six-tier model AUC vs any subset.
- **T6-5 — is transcendent contestation (S3) the irreducible Mule-adjacent driver?** Which
  sub-dimension carries the most independent power after controlling for the others?
- **T6-6 — Netherlands = minimum spark density** (bottom decile of T6): peaceful maritime
  neighbourhood, no resource prize, no transcendent contestation, NATO-deterred, no coup
  tradition. A sanity check on the construct.

## Interpretation gate (frozen)
- **T6-1/T6-4 pass** ⇒ spark density carries independent timing information and the
  criticality×spark-density interaction is the highest-resolution pre-crisis signal the
  framework can produce — the Mule shrinks from "the trigger is unknowable" to "the *specific*
  spark is unknowable but its *arrival rate* is structural and measured."
- **Null** ⇒ spark density adds environmental context but not timing power; report honestly —
  the Mule is bigger than hoped and T6 is a descriptor, not a predictor.
