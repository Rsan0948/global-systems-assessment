# CLAUDE.md — working guide for this repository

This file orients an agent working in `universalsystemgrade`. Read it before
touching code. Read `README.md` for the project's scientific framing and
`preregistration/PREREGISTRATION.md` for the binding analysis plan.

> **Unrelated sub-projects** (separate from the fragmentation study — do not wire
> any of them together). Each has its own `CLAUDE.md`; a local agent working on
> one should read that, not this file:
> - `mi_pipeline/` — Modernization Index *data pipeline* (builds the raw indicator
>   panel from World Bank API + manual CSVs).
> - `mi-research/` — Modernization Index *scoring/diagnostic/retrodiction engine*
>   (consumes per-country data → MI scores + case-study validation). Carries the
>   `MASTER_REFERENCE_ARCHITECTURE.md` source-of-truth spec.
> - `mi-website/` — the planned public *website* for the Modernization Index
>   (pre-development; currently just `DESIGN_SPEC.md`). Consumes `mi-research`'s
>   engine/data and `mi_pipeline`'s ingestion — it does not re-implement them.

## What this project is (in one paragraph)

A **two-stage discovery program** testing whether there is a *lawful regularity*
in how self-organizing hierarchical systems subdivide — above what mundane
mechanisms (random topology) already produce. It is **not** a project to prove a
specific constant. The central question is decomposed into a **ladder** (rung 0
no theorem → 1 domain-specific laws → 2 universality → 3 named constant → 4
mechanism). Discovery is exploratory; whatever it finds is then **frozen and
confirmed on a sealed holdout**. The number *e* has no privileged status.

## Repository map

```
preregistration/PREREGISTRATION.md   The binding pre-analysis plan (v0.2). Read first.
discovery/                           THE CORE ENGINE. Domain-agnostic.
  heterogeneity.py                   DerSimonian-Laird between/within-domain variance
  trivial_null.py                    mechanism-free baseline comparison (the key control)
  ladder.py                          the 4-rung verdict + split()/confirm() discipline
  scenarios.py, run.py               known-truth calibration of the engine
integration/                         Wires domain nodes INTO the engine.
  node_api.py                        the shared DomainNode interface (every study implements it)
  nodes_literature.py                rivers + biology subsystem nodes
  run.py                             assembles ALL nodes -> ladder + controls + calibrations
studies/                             One directory per domain ("node") or test.
  2C_river_networks/                 rivers: Strahler/Horton + power study (real HydroSHEDS hook)
  2D_biological_branching/           biology_node.py
  2B_corporate/                      corporate_node.py + survival.py (hazard test)
  2E_organizations/                  org_node.py
  2F_opensource/                     oss_node.py (boundary probe)
  2A_political_fragmentation/        dgs.py (DGS->instability) + panel.py (NOT a ratio node)
  3B_mechanism/                      mechanism.py (rung-4: does the gap predict the factor?)
  4_negative_controls/               nodes.py + controls_analysis.py (engineered/classification)
```

## How the pieces connect

1. Each **study** exposes a `DomainNode` (see `integration/node_api.py`):
   `name`, `ratios` (the comparable subdivision FACTOR — a ratio, never a raw
   count), a mechanism-free `null_sampler(n, rng)`, optional scaling exponents,
   and `is_self_organizing` (False for negative controls).
2. `integration/run.py` collects the nodes, calls `discovery.ladder.assess`,
   runs the negative-control dispersion contrast, the rung-4 mechanism test, and
   the predictive calibrations, then writes `integration/results/`.
3. The engine never knows or cares which domain it's looking at. To add a
   domain, write a node; do not modify the engine.

## Hard rules (these encode the science — do not break them)

- **The observable is a comparable ratio (factor), never a raw count.**
  PREREGISTRATION §4. A raw successor/fork count conflates parent size with
  subdivision tendency. Normalize (e.g. successors per internal division).
- **Every domain must ship a mechanism-free `null_sampler`.** A finding counts
  only as the signal ABOVE that null. Random topology already clusters near 3–4
  with no law (proven in `studies/2C_river_networks`); clustering alone is not a
  theorem. A domain without a defensible null is excluded, not given a pass.
- **Rung 3 uses CI-isolation, NOT point-hypothesis Bayes factors.** Fixed-point
  Bayes factors (e vs 3) diverge toward the nearer value with sample size even
  when neither is correct — they are sample-size-hackable. See
  `studies/2C_river_networks/results/INTERPRETATION.md` and PREREGISTRATION
  Appendix A. Do not reintroduce a "BF ≥ 10" criterion.
- **Discovery and confirmation use disjoint data.** Do not inspect the sealed
  holdout (open-source + corporate, plus each domain's most-recent-20% temporal
  holdout) during discovery. Use `ladder.split` / `ladder.confirm`.
- **Report the highest rung the evidence EARNS, and no higher.** Rung 0 / rung 1
  are real, publishable findings. Symmetric reporting: a "no theorem" verdict
  goes in the title/abstract with the same prominence as a positive one.
- **Anything runnable here is on simulated / literature-summary inputs and
  proves the PIPELINE, not the theory.** Never present a calibration number as a
  finding about real systems. Keep that disclaimer in outputs.
- **Political fragmentation (2A) is NOT a ratio node.** Administrative hierarchy
  is designed (a boundary-condition control); its contribution is the
  e-independent DGS→instability prediction. Don't push it into the ladder.

## Conventions

- Python 3.11. Deps: `numpy`, `scipy`, `matplotlib`, `pytest` (install with
  `pip install numpy scipy matplotlib pytest`). Real river ingestion also needs
  `geopandas`/`pyogrio` (optional, import-guarded).
- **Per-study module basenames must be unique across the repo** (e.g.
  `biology_node.py`, not `node.py`) — pytest imports test modules by basename
  and collides otherwise. Same reason `2A`'s panel is `panel.py` not
  `synthetic.py`.
- Each study is runnable standalone (`pytest tests/ -q` from its dir) and via
  the integration runner. Tests insert the study dir on `sys.path`.
- Heavy/real data is never committed. Generators are seeded; results in
  `results/` are regenerable by one command.
- Statistics: two-tailed; exact p-values; effect sizes AND variance components
  reported; Benjamini–Hochberg FDR across the per-domain family; a sensitivity
  analysis for every threshold choice (PREREGISTRATION §8).

## Real-data ingestion hooks (all free sources; see the handoff prompt)

Each `ingest_*` raises `NotImplementedError` with the source it expects:
`studies/2C_river_networks/ingest.load_hydrosheds_reaches` (HydroSHEDS),
`2D .../biology_node.ingest_fia` (FIA + morphometry),
`2B .../corporate_node.ingest_edgar` (SEC EDGAR + Wikipedia),
`2F .../oss_node.ingest_github` (GitHub API / GH Archive),
`2A .../dgs.ingest` (COW + V-Dem + WGI + Harvard Atlas). No Crunchbase, no
GHTorrent (both avoided deliberately).

## Workflow expectations

- Develop on the branch `claude/five-phase-preregistered-research-jaw43r`.
- Run `pytest studies discovery -q -p no:cacheprovider` before committing; keep
  it green. Run `integration/run.py` and confirm it completes.
- Commit with descriptive messages; do not open a PR unless asked.
- When you wire in real data, do NOT change the downstream statistical stages —
  only the `ingest_*` function and the node's inputs.
