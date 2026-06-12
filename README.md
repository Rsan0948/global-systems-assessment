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
studies/2C_river_networks/           One worked-out domain node, end-to-end and runnable
```

## Status

- **Pre-registration (v0.2, discovery reframe):** drafted. Needs a human author
  identity before public deposit (OSF/arXiv). Not yet deposited.
- **Discovery engine:** built and calibrated. On known-truth synthetic worlds it
  correctly returns rung 3 (one law, isolates *e*), rung 1 (many laws), and
  rung 0 (trivial), and the discover→confirm split passes. See `discovery/`.
- **Study 2C (rivers):** built end-to-end; runnable result is a power/calibration
  analysis (real HydroSHEDS ingestion ready). It also supplied the empirical
  proof that random topology clusters near 3–4 *with no law* — the motivation for
  the triviality control.
- **Other domains (2A/2B/2D/2E/2F), mechanism test (3B), negative controls:**
  specified in the pre-registration as nodes/controls for the engine; not yet
  implemented.

## The honest caveat on all runnable numbers

Everything that runs here uses **simulated data** and proves the *instruments*,
not the theory: that the measurement pipeline doesn't manufacture *e*, and that
the discovery engine can tell "one law" from "many laws" from "no law." No claim
about real systems has been made.
