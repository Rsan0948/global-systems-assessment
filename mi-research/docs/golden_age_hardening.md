# Golden ages — hardening the "exogenous, not slope" conclusion (3 disentangling tests)

**Date:** 2026-06-28. Full WGI panel + full-panel resource rents. Climb-start = P1(t+5)−P1(t) > 0.05,
annual era 2002+. These tests disentangle the structural drivers from each other, from mean-reversion,
and across time. **Two of the three sharpen the conclusion; one overturns a label I had shipped.**

## Test 1 — is "transition" just low base in disguise? NO (it adds, net of base)
Climb rate by cell:
| base | post-communist transition | not | z |
|---|---|---|---|
| LOW (P1<0.40) | **18%** (n=105) | 10% (n=874) | **+2.7** |
| high | **11%** (n=215) | 5% (n=2404) | **+3.4** |

Post-communist transition adds climbs at **both** base levels — even high-base transition states
(Estonia, Slovenia, Czechia) climbed more than other high-base countries. **Transition is a genuine
independent exogenous driver, not a confound of mean-reversion.** ✓ hardens.

## Test 2 — is the "commodity" effect commodity-specific? NO — it's a generic era effect (label was WRONG)
| group | boom-year climb | non-boom | z |
|---|---|---|---|
| resource-RICH (rents>10%) | 9% (n=498) | 8% (n=358) | +0.6 (none) |
| resource-poor | 8% (n=1451) | 5% (n=1230) | **+3.7** |
| within boom years: rich vs poor | 9% vs 8% | | +0.4 (none) |

**Resource-rich countries had NO boom-year boost** — if anything they're the rentier-stagnant ones.
The boom-window climb boost is entirely in **resource-poor** countries. So the driver is **NOT
commodities** — it's a generic **era/wave** effect (2003–08, 2010–13) whose mechanism is *not* the
commodity cycle. **Correction:** earlier docs (`golden_age_holdout_and_structure.md`,
`v3_3_inclusion_and_global_picture.md`) credited "the commodity cycle" — that is refuted here. The era
is real; the commodity *mechanism* is not. Likely candidates instead: EU enlargement, HIPC debt relief
(~2005), post-conflict reconstructions, the post–Cold-War liberal high tide — none isolated, mechanism
**unidentified**.

## Test 3 — does low base predict in the held-out recent window? NO (it's era-conditional)
| window | low-base climb | high-base | z |
|---|---|---|---|
| discovery 2002–11 | 15% (n=561) | 6% (n=1403) | **+6.2** |
| **HELD-OUT 2012–19** | **5%** (n=418) | 6% (n=1216) | **−0.6** |

**Low base FAILS the temporal holdout.** The geographic-holdout z+2.4 (which I shipped as
"holdout-validated") was carried *entirely* by the 2002–11 wave; in 2012–19 low-base countries climb at
5% — no better than high-base. **Correction:** `ascent_potential` is **era-conditional**, not an
always-on signal; the engine caveat is updated to say so.

## The hardened, unified conclusion
Golden ages were a **2002–2011 era/wave** — a global institutional-improvement window (mechanism
**not** commodities; plausibly EU enlargement / debt relief / liberal high tide / post-conflict
rebuilds) — operating on **low-base** and especially **post-communist-transition** states. Within the
wave, low-base (z+6.2) and transition (z+2.7/+3.4) predict. **The wave ended ~2012, and since then
*nothing* forecasts a golden age — not the internal slope (refuted), not low base (dormant), nothing.**

This is the rigorous version of "exogenous, not slope": the predictive content was never in a
country's trajectory, and the structural predictors that did work were **era-bound** and are now
**dormant**. The honest standing claim is therefore *negative and era-dependent*: **we are in a
golden-age drought in which no current variable — internal or structural — reliably forecasts an
institutional climb.** That the system can find the *era* but not a *live* predictor is itself the
finding.

## What this changes
- Engine: `ascent_potential` caveat corrected to **era-conditional / currently dormant** (it flags
  structural eligibility only, with no active era to realize it). No score changes; baseline 213C/0F.
- Interpretation: the global-picture reframe stands and strengthens — not only a governance-core
  stagnation + golden-age drought, but **the drivers of climbs are themselves switched off** in the
  current era. The "commodity" attribution is retracted in favor of an unidentified era mechanism.
- Honest limits: 2012–19 holdout is the drought, so low N of climbs (right-censoring softens 2019+);
  the era mechanism is named only by candidates, not isolated; "transition" countries are few and the
  high-base transition cell is modest (n=215).
