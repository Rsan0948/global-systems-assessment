# Out-of-sample run v2 — shock-cohort set (RESULT)

**Date:** 2026-06-28. Scores `data/case_studies/source_reports/VALIDATION_v2_shock_cohort_modern.md`
— the shock-cohort redesign that fixes the v1 blind spots (outcome variance + origin stratification).
Reproduce: `python scripts/score_v2_cohorts.py`. Firewalled from the 213/77/0 baseline.

## Conformance to the frozen brief (`random_validation_brief_v2.md`)
Conforms: numbered pool of 22 multi-country shocks (≥20 ✓), documented RNG draw (7 cohorts), full
cohort membership / documented random subsets, **survivors reported alongside casualties** ✓, origin
+ outcome tags ✓, coverage rule satisfied (13 internal / 8 external / 6 mixed-oil). **27 observations,
not 30** — the shortfall is documented (exclusion list thinned the Tequila cohort), not silent
dropping. Selection was blind (framework-naive agent).

## Protocol
Blind selection + **mechanical predictor** (V-Dem rule-of-law at the pre-shock year, P1 proxy r=0.87
with WGI) + **pre-registered rule** (higher pre-shock institutions → better outcome tag). Same
airtightness standard as v1: it's in the blind selection and mechanical predictor, not in blind
reading of outcomes.

## Result
| slice | n | Pearson | Spearman |
|-------|--:|--------:|---------:|
| **POOLED** | 27 | **+0.16** | **+0.09** |
| internal-origin | 12 | +0.40 | +0.32 |
| external-origin | 15 | +0.66 | +0.59 |

**Within-cohort (the clean test — shock held ~constant):**
| cohort | n | Spearman | outcomes | reads |
|--------|--:|---------:|----------|-------|
| A Great Depression | 4 | **+0.77** | [2,2,2,3] | ✓ Chile (rol 0.66) took the best path; the three low-rol members ruptured |
| B 1982 debt | 4 | **+0.77** | [3,4,4,4] | ✓ Philippines (rol 0.11, Marcos) the lone discontinuity |
| C 1994 CFA | 4 | **−0.74** | [2,3,4,4] | ✗ INVERTED — but Côte d'Ivoire's rupture was a *delayed 1999 succession coup* (5y post-shock), not the devaluation |
| F 2004 tsunami | 4 | **+0.77** | [4,4,4,5] | ✓ Seychelles (rol 0.64) the lone clean absorber |
| G 2014 Ebola | 4 | **+0.77** | [4,4,4,5] | ✓ Senegal (rol 0.69) the lone clean absorber |
| D Tequila / E Oil | 1 / 6 | — | degenerate | no outcome variance (E = six entrenched autocracies, all survived) |

## Honest verdict
- **Within-cohort, the institutions→outcome rule mostly holds out of sample: 4 of 5 variance-cohorts
  concordant (~+0.77).** This is the cleanest positive the program has produced — stronger than the v1
  random run (d≈0.37) — *because* the cohort design holds the shock and era roughly constant. Caveats:
  n=4 per cohort, low absolute variance (still mostly tag 4), and Spearman is quantized at this n
  (+0.77 ≈ "top-rol member had the best outcome"). Directional, not precise.
- **Pooled is null (+0.09), and that's informative, not a failure.** The signal washes out across
  cohorts because **regime entrenchment lets low-institution autocracies absorb ECONOMIC shocks** — the
  entire oil cohort (Angola, Azerbaijan, Kazakhstan, Congo, Gabon, Eq. Guinea: rol 0.04–0.28) survived
  (all tag 4). Rule-of-law level isn't comparable across a 1929 Latin-American cohort and a 2014 African
  oil cohort, and rol does not measure the repression/rent capacity that carries an autocracy through a
  price collapse. The within-cohort frame is the correct read; the pooled number should not be
  over-read either way.
- **The one inversion (CFA) is a timing artifact** of the project's own doctrine: distrust the slope.
  Côte d'Ivoire's coup came 5 years after the shock, downstream of Houphouët-Boigny's death — a
  succession-timing event the framework explicitly disclaims.

## Second load-bearing claim — the durability gap (P4 − P1)
The first run scored only institutions (rol). This adds the **durability gap** (P4 = Maddison
GDP-percentile, P1 = rol) — *income outrunning institutions → fragile*. Rule: bigger gap → more
severe → **negative** correlation with the outcome tag. 25/27 scoreable (Maldives, Somalia lack
Maddison GDP).

| slice | n | Pearson | Spearman |
|-------|--:|--------:|---------:|
| POOLED | 25 | −0.19 | **−0.22** |
| internal-origin | 12 | −0.53 | **−0.58** |
| external-origin | 13 | −0.39 | −0.40 |
| **mean gap** | severe (tag≤2) **+0.173** | vs | non-severe **+0.041** |

**The gap is right-signed and a touch cleaner pooled (−0.22) than the institutions level (+0.09),
and moderate within internal cohorts (−0.58).** The severe-vs-non-severe gap means (+0.173 vs +0.041)
**replicate the v1-30 direction** (+0.02 vs −0.14 there) out of sample — independent corroboration of
the second claim. Same two confounds recur: the oil cohort has the *largest* gaps (mean +0.46, classic
rentier "granted prosperity") yet absorbed the economic shock (entrenchment ≠ structural durability on
a 10-yr economic window), and CFA/Côte d'Ivoire is delayed-succession noise.

**Full 5-pillar engine — coverage-blocked.** Only **5 of 27** observations are in the Data API
(Kazakhstan, Gabon, Eq. Guinea, Sri Lanka, Argentina — all tag-4 survivors, MI 0.50–0.66); the WGI
panel doesn't carry the obscure states in this draw, and the 5 covered have no outcome variance. So
the **V-Dem rol + Maddison-gap proxy is the operative engine on v2** — the same proxy the v1 runs used.

## The decisive limitation — v2 does NOT test T3
**Not one external-military/conquest shock was drawn.** Every "external" cohort is a natural-disaster
or price shock (tsunami, Ebola, oil) — exogenous to the economy, but not an invasion. The relational/
exposure tier (T3) measures exposure to external *conquest*; **it is therefore not exercised by a
single one of these 27 cases.** And the discriminating 4th cell — *internally fragile + low military
exposure (shielded) → survives* — remains **empty**: the survivors here came through **economic** shocks
via internal resilience or autocratic entrenchment, not via a patron/alliance shielding them from
conquest. So v2:
- **validates (out of sample, within-cohort) the INTERNAL engine's institutions→outcome claim** — its
  actual domain;
- **leaves T3 untested**, and confirms the earlier Phase-3 diagnosis: testing T3 needs a military-shock
  cohort (e.g. pool item #14, WWII occupations — not drawn) **plus** the deliberately-flagged
  shielded-survivor probe (Kuwait 1990, Baltic/NATO, South Korea, Finland 1939, Taiwan). v2's own draw
  is further proof that random/cohort sampling does not surface that cell.

## Next
1. Run a **military-shock cohort** for T3 (re-draw including WWII-occupation / interstate-war waves),
   with the deterministic relational pull (COW CINC/ATOP/ICOW) added to the scoring protocol.
2. Build the flagged **shielded-survivor probe** to populate the empty 4th cell (discrimination check).
3. ~~Re-score v2 on the durability gap + 5-pillar~~ **DONE** (see "Second load-bearing claim" above):
   gap is right-signed (pooled −0.22, internal −0.58) and replicates the v1-30 direction; full 5-pillar
   is coverage-blocked (5/27 in the Data API).
