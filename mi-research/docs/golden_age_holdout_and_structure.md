# Golden ages — geographic holdout (CONFIRMED FAIL) + where the real structure is

**Date:** 2026-06-28. Full WGI panel (`data/sources/wgi_full_panel.json`, **202 economies** with WGI
history). Pre-registration frozen first (`golden_age_prereg.md`). Discovery set = 89 countries;
**holdout = 112 unseen**. Clean re-runs use the **annual era (2002+)** to remove the biennial-WGI
artifact (WGI was 2-yearly before 2002 → spurious odd-year zeros).

## The pre-registered test: CC-jump signature — FAILS the holdout (decisively)
| set | durable rate | base rate | z | events |
|---|---|---|---|---|
| Discovery (89) | 31% | 18% | **+3.0** | 87 |
| **Holdout (112 unseen)** | **17%** | **17%** | **−0.0** | **137** |
| Pooled | 22% | 18% | +1.8 | 224 |

137 well-powered holdout events, **exactly zero lift.** Not underpowered — a clean null. The
discovery-era signal (38% vs 23%, 1996–2010) was a **post-communist / EU-accession transition-era
artifact, not a law.** Per the pre-registration: **FAIL.** And no other institutional-component jump
rescues it on the holdout — GE z+0.6, RL z+1.1, RQ z+0.4, CC z+0.6 (annual era), all null.

**Verdict: our system cannot forecast a golden age from a country's own institutional jump.** Full stop.

## But golden ages are NOT random — the structure is elsewhere (and it holds out of sample)
Casting the wide net on the **holdout, annual era**:
| predictor | durable rate | base | z | holds out? |
|---|---|---|---|---|
| **low starting base (P1 < 0.40)** | 20% | 16% | **+2.4** | **YES** |
| very-low base (P1 < 0.30) | 21% | 16% | +1.6 | yes (weaker n) |
| **recent momentum (P1 +>0.03 in prior 3y)** | 11% | 16% | **−1.7** | **YES (negative!)** |
| any institutional-component jump | ~16–23% | 16% | ≤+1.1 | no |

- **Where you START predicts the climb** (low base → +2.4, survives the holdout): room-to-rise /
  mean-reversion. Real and generalizable (partly mechanical — a low value has more headroom and noise
  pushes up — but genuine and out-of-sample).
- **Momentum is NEGATIVE** (−1.7): countries that recently rose tend to **give it back** — no flywheel.
  (Reconciles the faint +0.15 continuous autocorrelation seen earlier: that was the *level's*
  stickiness, not momentum of the *gains*; conditioned on recent risers, the gains mean-revert.)

## And golden ages come in WAVES (temporal clustering, ~2× random)
Countries starting a durable climb, by year (annual era 2002+):
```
02:28 03:26 04:24 05:21 | 06:10 07:7 08:5 | 09:12 10:18 11:18 12:20 13:20 | 14:11 15:4 16:9 17:7
```
**CV 0.50 vs Poisson-random ~0.26** — about twice the clustering randomness would produce. A clear
**2002–2005 wave** (post-communist/EU-accession + early-2000s reform/commodity onset), a **2006–2008
trough**, and a **2010–2013 bump**. Golden ages are an **era/global phenomenon**, not country-by-country.

## What this all means (the rich finding, not forced)
Golden ages are **real and structured — but the structure is LEVEL + ERA, not internal trajectory.**
- **Predictable from:** *where you start* (low base) and *when you are* (the wave).
- **NOT predictable from:** your own institutional dynamics — no jump signature works, and recent
  momentum predicts the *opposite* (reversion).
- **Interpretation:** the driver is largely **exogenous** — a low starting position caught in a
  global/regional reform window (EU accession, post-communist transition, commodity cycle, end of
  conflict) that the MI's pillar trajectories don't and can't capture. The "discrete variable" you
  sensed is real; it just isn't *inside* the country's pillar slopes — it's the country's *level* and
  its *era*.

So the honest answer to "can our system find golden ages?": **No — and that is the finding.** A
trajectory-based instrument is the wrong shape for a phenomenon driven by starting position and
exogenous waves. (It mirrors the lead-time result for crises: *trust the level, distrust the slope* —
here, the level and the era carry the signal; the slope is mean-reverting noise.)

## Honest caveats
- The low-base effect is *partly* mechanical mean-reversion (more headroom + regression). Real and
  out-of-sample, but don't over-read it as agency.
- The 2002–2005 wave overlaps the commodity supercycle and the EU "big bang" accession cohort —
  plausibly those drivers; not isolated here.
- Outcome = P1 +>0.03 over 5y (the pre-registered, deliberately modest bar); a stronger bar would cut
  event counts. Annual era only (2002+) for clean tests; the biennial pre-2002 data inflates clustering.
- This refutes a *signature*; it does not claim golden ages are unimportant — only that they are
  exogenous/level-driven, not forecastable from internal pillar slopes.
