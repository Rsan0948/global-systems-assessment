# universalsystemgrade

A pre-registered, adversarial test program for the **e-subdivision and
dimensional-gap theory** of self-organizing hierarchical systems — the claim
that self-organizing branching systems prefer a subdivision factor near
*e* ≈ 2.718, that interior complexity out-scales interface capacity by ≈ 1
dimension, and that this gap predicts instability/fragmentation.

The program is designed so the theory **can fail**. Every prediction is paired
with a null hypothesis, an exact decision threshold, and a failure clause;
boundary conditions where the theory must *not* hold are pre-registered as
negative controls; and the headline numeric claim is committed as an
explicitly **tiered** hypothesis (sharp "*e* specifically" vs. fallback "near
3") with pre-specified rules deciding which tier the evidence supports — so
the wide-band "[2,4]" loophole can't be used to launder a weak result into a
strong one.

## Layout

```
preregistration/PREREGISTRATION.md   Phase 1: the full, falsifiable pre-analysis plan
studies/2C_river_networks/           One worked-out study, end-to-end and runnable
```

## Status

- **Phase 1 (formalize & pre-register):** drafted — `preregistration/PREREGISTRATION.md`.
  Needs a human author identity before public deposit (OSF/arXiv). Not yet deposited.
- **Study 2C (river networks):** built end-to-end. Real-data ingestion for
  HydroSHEDS is implemented; the runnable result in-repo is the pre-registered
  **power/calibration analysis** (no network needed), which the firewalled
  build environment can execute. See `studies/2C_river_networks/README.md`.
- Studies 2A/2B/2D/2E/2F, 3A/3B, 4A/4B, 5A/5B: specified in the pre-registration,
  not yet implemented.

## What was deliberately *not* claimed

The runnable numbers in this repo are a **pipeline and power demonstration on
simulated data**, not evidence about real rivers. The neutral synthetic
topology lands near 3 and the procedure correctly declines to call it *e* —
that is the honesty check, not a finding.
