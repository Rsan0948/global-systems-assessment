# universalsystemgrade

A pre-registered, **two-stage discovery program** asking whether there is a
*lawful regularity* in how self-organizing hierarchical systems subdivide —
above what mundane mechanisms already produce.

The project was reframed from *confirming a specific theorem* (that the
subdivision constant is *e* ≈ 2.718) to **discovering whether there is a theorem
at all**, and if so, what kind. The central question is decomposed into a ladder
of nested claims, each a genuine result on its own:

```
rung 0  no theorem (scatter, or indistinguishable from a mechanism-free null)
rung 1  domain-specific laws  (each domain lawful, values differ)
rung 2  universality          (domains share one value, beating the null)
rung 3  named constant        (pooled CI isolates a principled constant)
rung 4  mechanism             (the dimensional gap predicts the value)
```

Discovery is exploratory; whatever it finds is then **frozen and confirmed on a
sealed holdout** the discovery never saw. The number *e* has no privileged
status — it may emerge as the pooled estimate, or not.

## Layout

```
preregistration/PREREGISTRATION.md   The two-stage discovery pre-analysis plan (v0.2)
discovery/                           Reusable core instrument: variance-components
                                     decomposition + trivial-null control + the ladder
integration/                         Node interface + runner: assemble all nodes -> ladder
studies/2C_river_networks/           River branching: pipeline + power/calibration
studies/2D_biological_branching/     Biology node (bronchial/vascular/botanical)
studies/2A_political_fragmentation/  DGS -> instability mechanism test
studies/2B_corporate/                Corporate split factor + survival/hazard test
studies/2E_organizations/            Inter-echelon org scaling ratio
studies/2F_opensource/               Viable-fork factor (boundary probe)
studies/3B_mechanism/                Rung-4: does the dimensional gap predict the factor?
studies/4_negative_controls/         Engineered (4A) + classification (4B) controls
```

## Status

- **Pre-registration (v0.2, discovery reframe):** drafted. Needs a human author
  identity before public deposit (OSF/arXiv). Not yet deposited.
- **Discovery engine:** built and calibrated. On known-truth synthetic worlds it
  correctly returns rung 3 (one law, isolates *e*), rung 1 (many laws), and
  rung 0 (trivial), and the discover→confirm split passes. See `discovery/`.
- **Study 2C (rivers):** built end-to-end; runnable result is a power/calibration
  analysis (real HydroSHEDS ingestion ready). Supplied the empirical proof that
  random topology clusters near 3–4 *with no law* — motivating the triviality
  control.
- **Domain nodes built (2D biology, 2B corporate, 2E organizations, 2F
  open-source):** all on literature-summary inputs, each with a mechanism-free
  trivial null and a real-data ingestion hook.
- **Study 2A (political):** the DGS→instability mechanism test, built and
  calibrated. Honestly *not* a ratio node — administrative hierarchy is designed,
  so it's a boundary-condition control, not self-organizing branching.
- **Study 2B / corporate survival:** hazard test recovers a true complexity
  effect (HR ≈ 1.65) and is null without one.
- **Study 3B (mechanism, rung 4):** built and calibrated — recovers a true
  gap→factor link and is null without one.
- **Negative controls (4A engineered, 4B classification):** built; on
  illustrative inputs the controls disperse ~6× more than self-organizing
  systems (Brown–Forsythe p ≈ 3×10⁻²⁴) — boundary condition confirmed.
- **Integration:** assembles all seven self-organizing nodes through the engine.
  On illustrative inputs the ladder returns **rung 1 (domain-specific laws)** —
  each domain concentrated, but values differ (I² ≈ 0.97). See `integration/`.
- **Remaining (needs you / real data):** swap each node's inputs for real
  measurements via the ingestion hooks; real exponent estimates for the rung-4
  test; the sealed-holdout confirmation pass; and the public deposit. See the
  "What you need to do" section below.

## The honest caveat on all runnable numbers

Everything that runs here uses **simulated data** and proves the *instruments*,
not the theory: that the measurement pipeline doesn't manufacture *e*, and that
the discovery engine can tell "one law" from "many laws" from "no law." No claim
about real systems has been made.
