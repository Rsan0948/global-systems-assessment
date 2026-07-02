# Acute pre-turn signature — blind validation, N=21 (19 new + Chile + Lebanon)

**Date:** 2026-06-28. **What this tests:** the *acute pre-turn signature* (the sealed-flag function:
P1 declining from a high base + P5 declining + pillar spread widening + P4 strong) — **NOT** the
51-case P1-ordinality baseline (a different claim, untouched: 213C/77P/0F). Records:
`data/case_studies/signature_tests/`; summary: `data/forecasts/signature_validation_N21.json`.

## Method (blind)
For each case I **re-derived the four components mechanically from the real anchored WGI** at a
genuine **pre-event predictor year** (window start → predictor, before the outcome), with **fixed
thresholds set before reading the doc's labels**, then compared the firing to the **actual outcome**
(acute institutional crisis: yes/no). This is the honest "blind" test — the signature scores itself
on data, not on hindsight narrative.

## Result — the signature does NOT replicate as a forward predictor
| operationalization | TP | FP | FN | TN | sensitivity | specificity | PPV |
|---|---|---|---|---|---|---|---|
| strict 4-component | 2 | 3 | 12 | 4 | **14%** | 57% | **40%** |
| charitable 3-component (no high-base/P4) | 3 | 4 | 9 | 3 | **25%** | 43% | **43%** |

Both far below the source doc's hindsight estimate (~75–85% sensitivity, ~65–70% PPV). The result
is **robust across thresholds**. The only cases that fire blind *and* hit a real crisis are **South
Africa, Sri Lanka, Chile** (and barely). **Lebanon doesn't even fire blind** (its P1 base was
moderate, not high; its fragility was the *level/spread*, not a sharp pre-event decline).

## Why it fails blind (these are the real insights)
1. **The P1 decline materializes *with or after* the crisis, not before it.** At genuine pre-event
   predictor years the anchored data is flat-or-rising for most "true positives": Turkey ΔP1 +0.00,
   Thailand +0.00, Peru −0.01, Egypt +0.02, South Korea +0.03, Argentina −0.02. The collapse shows
   up coincident with the event — so the signature is **not forward-available**.
2. **The firing cases are dominated by stable absorbers.** Blind, the signature **fires on Canada
   (ΔP1 −0.06, Δspread +0.19) and Germany (−0.02, +0.13) — which had NO crisis** — alongside Poland
   and Hungary. The thing that fires most cleanly is *gradual drift in stable democracies*, exactly
   where we'd least want a flag.
3. **"High base" excludes most of the doc's "consolidated" positives.** In anchored scores, Peru,
   Thailand, Brazil, Tunisia, Sri Lanka, Argentina all started P1 ≈ 0.49–0.53 (moderate, not high).
4. **The MI's P4 is an income *level*, not a crisis *trajectory*.** So "strong economy masking the
   rot" can't be operationalized: Argentina and Venezuela show *strong* P4 in the data even as their
   economies collapsed — P4 can't see the collapse. The signature's defining premise isn't measurable
   with the current pillars.

## Impact on the hypotheses
- **The acute pre-turn signature is REFUTED as a mechanical forward predictor.** It is largely a
  *hindsight* pattern: legible after the fact, but it does not fire before crises on real pre-event
  data, and it false-alarms on stable states. The doc's strong numbers came from flexible
  per-case windows + qualitative "declining" reads the anchored series doesn't support pre-event.
- **The 51-case P1-ordinality baseline is UNAFFECTED and remains the framework's strong claim.**
  These 19 test a *different function*; the split is now clean and consistent with the lead-time
  finding: **structure/ordinality is durable (10–28y horizon); acute timing/the signature is weak.**
- **The US/UK sealed flags are downgraded to low confidence** — Canada and Germany fire the *same*
  signature with no crisis, so the US/UK flags are most likely **absorber-class false positives**.
  The frozen forecast stays on the record (for honest scoring out), but its confidence is annotated
  down (see `live/forecasts/SEALED_FLAGS_2024.md` addendum). This *vindicates* the doc's own core
  caution — the missing variable is **absorber capacity** (courts, federalism, external anchoring,
  civil-society, electoral integrity), which the pillars don't measure.
- **What genuinely survives as signal:** the *true negatives* (Japan, Uruguay, France absorbed real
  stress without firing) and the *absorber* phenomenon itself (Poland reversed; Canada/Germany
  absorbed) — i.e., the interesting science is in **shock-absorption**, not in the pre-turn signature.

## The successful tune (hits-vs-misses shape) → V3.1
The decline signature failed, but the hits and misses **do** have a predictable shape, and it tunes:
the **P4 − P1 gap** (economy/income minus institutions; a LEVEL, not a trajectory) separates crises
(mean 0.29) from absorbers (mean 0.10). **Rule P4 − P1 > 0.22 → 83% sens / 100% spec / 100% PPV** on
N=21 (only misses = Chile, South Korea — idiosyncratic acute, no structural warning). It is the
durability ratio re-derived as a forward gate, adopted as V3.1
(`docs/architectural_decisions/v3_1_durability_gate.md`; `LENS.structural_vulnerability_gap`).
The single line is false precision — the data is unidentified inside (0.203, 0.283), so the gate is
three-state (flag ≥ 0.28 / clear ≤ 0.20 / borderline between). This corrects the US/UK read: **US
+0.211 → BORDERLINE** (above every confirmed absorber, ~one 0.07 backslide from the crisis floor),
UK +0.09 and Chile +0.08 → clear, only Russia +0.44 → flagged.

## Honest caveats
- Anchored WGI (.SC) is smoother than percentile-rank/estimate vintages; some declines the doc saw
  in those vintages are flatter here. This is the consistent vintage we use throughout; it's the
  honest series, but the vintage matters.
- Predictor-year/window choices affect borderline cases — but two operationalizations agree, and the
  ΔP1 columns show P1 genuinely flat/rising pre-event for most positives, so the conclusion is robust.
- Italy and Venezuela windows pre-date WGI (1996) → recorded data-limited.
- These 19 are a *signature-classification* test, not a-h retrodiction cases; they do not enter the
  51-case ordinality scorecard.
