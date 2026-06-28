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

## Final verdict

**Rung 1 — domain-specific laws. No universal constant; no mechanism shown.**
Self-organizing domains are each individually concentrated but do **not** share
one value (I² ≈ 0.98); the pooled CI excludes *e*. Both pre-registered
confirmations have been run and are **spent**:

- **Prediction A (rivers, cross-continent):** **CONFIRMED.** South America
  reproduces the North-America finding (geom Rb 3.539; A1/A2/A3 pass).
- **Prediction B (cross-domain holdout = corporate):** **B1 fail, B2 pass — not
  fully confirmed.** On 108 real SEC EDGAR spin-off events, corporate splitting
  is **indistinguishable from its mechanism-free binary-default null** (a trivial
  domain), but adding it **keeps the verdict at rung 1** — it does not collapse
  to universality or isolate a constant. Reported symmetrically.

The program was *built to be able to conclude "no theorem of a universal
constant,"* and that is where the real data lands: a real regularity within some
domains (rivers, biology), no shared law across them, and no mechanism
demonstrated.

## What is real vs. simulated

- **REAL data:** rivers (2C, HydroRIVERS, both continents), biology (2D,
  NeuroMorpho, 6 cell types), negative controls (4, NCBI taxonomy + specs),
  DGS (2A, ECI+V-Dem+WB+UCDP), and **corporate (2B, SEC EDGAR, 108 splits)**.
- **SIMULATED / deferred:** organizations (2E, doctrine-table literature values);
  open-source (2F) — real-ingest code is committed but the GitHub crawl is
  **deferred** (descoped from holdout B, logged as a prereg amendment).
- **Rung-4 mechanism test → RUN on real allometry, result NULL.** Real
  dimensional gaps were estimated per biology cell type from the NeuroMorpho
  CNG.swc 3-D reconstructions (interior = total dendritic length ~ radius;
  interface = terminal tips ~ radius; `fetch_neuromorpho_exponents.py`). Across
  the 6 cell types the gap does **not** predict the subdivision factor
  (slope 0.14, 95% CI [−0.07, 0.35], p = 0.15) — **no rung-4 mechanism.** The
  gaps themselves are consistent with the dimensional prediction Δ≈1 (mean 0.66,
  CI [0.15, 1.18]), but the gap→factor link is absent. The full *cross-domain*
  apex (rivers + corporate exponents too) is not run — those need raw spatial
  re-ingest beyond the committed caches.

## Scope explicitly closed out

This study is concluded at the confirmation + mechanism stages above. Genuinely
out of reach here (not done): the **2F open-source** real crawl (needs a GitHub
token), the **cross-domain** rung-4 extension to rivers/corporate (needs raw
spatial re-ingest), real **2E** doctrine parsing (low value), and the public
**OSF/arXiv deposit** (needs a human author identity). Each is a clean future
extension, not a blocker — the engine, the real-data nodes, the spent
confirmations, and a real (null) mechanism test are all in place.
