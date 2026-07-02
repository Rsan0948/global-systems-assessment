# CLAUDE.md — monorepo guide (`universalsystemgrade`)

This repository is a **monorepo of four independent projects**. They are NOT
wired together — do not import across them. Find your project below, then read
its own `CLAUDE.md` (linked) before touching code.

| Project | What it is | Start here | Status |
|---------|-----------|-----------|--------|
| **root** (`discovery/`, `integration/`, `studies/`, `census/`, `preregistration/`) | The **fragmentation study** — the original pre-registered discovery program (branching factors of self-organizing systems). | this file + `README.md` + `preregistration/PREREGISTRATION.md` | Concluded: rung 1, no universal constant (see `CENSUS.md`, `SYNTHESIS.md`, `DEFENSIBLE_RESULTS.md`). |
| `mi_pipeline/` | MI **data pipeline** — builds the raw indicator panel from World Bank API + manual CSVs. | `mi_pipeline/CLAUDE.md` | Real panel committed. |
| `mi-research/` | MI **scoring / diagnostic / retrodiction engine** + the 51-case validation corpus. The source-of-truth spec is `MASTER_REFERENCE_ARCHITECTURE.md`. | `mi-research/CLAUDE.md` → `RESEARCH.md` | Live; canonical-panel data path. |
| `mi-website/` | The **public Next.js website** for the MI — a consumer of `mi-research` (does not re-implement scoring). | `mi-website/CLAUDE.md` → `mi-website/web/AGENTS.md` | Built + deployable (190 country pages). |

> The three `mi-*` projects are the **Modernization Index** platform (governance
> scoring). The **root** project is the unrelated fragmentation study. They share
> a conceptual origin only (the "self-organizing systems fragment in concentrated
> bands" thesis), never code.

---

# The root project: the fragmentation study

A **two-stage discovery program** testing whether there is a *lawful regularity*
in how self-organizing hierarchical systems subdivide — above what mundane
mechanisms (random topology) already produce. It is **not** a project to prove a
specific constant. The central question is decomposed into a **ladder** (rung 0
no theorem → 1 domain-specific laws → 2 universality → 3 named constant → 4
mechanism). Discovery is exploratory; whatever it finds is then **frozen and
confirmed on a sealed holdout**. The number *e* has no privileged status.
**Outcome so far:** rung 1 — each system has a stable branching factor that beats
chance, but they do not share one value (`CENSUS.md` / `SYNTHESIS.md`).

## Repository map (root project)

```
preregistration/PREREGISTRATION.md   The binding pre-analysis plan (v0.2). Read first.
README.md / CENSUS.md / SYNTHESIS.md / DEFENSIBLE_RESULTS.md   Framing + results narrative.
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
  2C_river_networks/                 rivers: Strahler/Horton + power study (real HydroSHEDS)
  2D_biological_branching/           biology_node.py (real NeuroMorpho arbors)
  2B_corporate/ 2F_opensource/       corporate + open-source (sealed holdout)
  2E_organizations/ 2A_political_fragmentation/  orgs + DGS->instability (2A is NOT a ratio node)
  3B_mechanism/ 4_negative_controls/ rung-4 mechanism test + engineered/classification controls
census/                              The fragmentation CENSUS (catalog.py, systems/, governance/).
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
  PREREGISTRATION §4. Normalize (e.g. successors per internal division).
- **Every domain must ship a mechanism-free `null_sampler`.** A finding counts
  only as the signal ABOVE that null. Random topology already clusters near 3–4
  with no law; clustering alone is not a theorem. A domain without a defensible
  null is excluded, not given a pass.
- **Rung 3 uses CI-isolation, NOT point-hypothesis Bayes factors.** Fixed-point
  Bayes factors (e vs 3) are sample-size-hackable. See
  `studies/2C_river_networks/results/INTERPRETATION.md` and PREREGISTRATION
  Appendix A. Do not reintroduce a "BF ≥ 10" criterion.
- **Discovery and confirmation use disjoint data.** Do not inspect the sealed
  holdout (open-source + corporate, plus each domain's temporal holdout) during
  discovery. Use `ladder.split` / `ladder.confirm`.
- **Report the highest rung the evidence EARNS, and no higher.** Rung 0 / rung 1
  are real, publishable findings, reported with the same prominence as a
  positive one.
- **Political fragmentation (2A) is NOT a ratio node.** Administrative hierarchy
  is designed (a boundary-condition control); its contribution is the
  e-independent DGS→instability prediction. Don't push it into the ladder.

## Conventions

- Python 3.11. Deps: `numpy`, `scipy`, `matplotlib`, `pytest`. Real river
  ingestion also needs `geopandas`/`pyogrio` (optional, import-guarded).
- **Per-study module basenames must be unique across the repo** (e.g.
  `biology_node.py`, not `node.py`) — pytest imports test modules by basename
  and collides otherwise.
- Each study is runnable standalone (`pytest tests/ -q` from its dir) and via
  the integration runner. Heavy/real data is never committed; results in
  `results/` are regenerable by one command.
- Statistics: two-tailed; exact p-values; effect sizes AND variance components;
  Benjamini–Hochberg FDR across the per-domain family; a sensitivity analysis
  for every threshold choice (PREREGISTRATION §8).

## Workflow expectations (root project)

- Run `pytest studies discovery -q -p no:cacheprovider` before committing; keep
  it green. Run `integration/run.py` and confirm it completes.
- When you wire in real data, do NOT change the downstream statistical stages —
  only the `ingest_*` function and the node's inputs.
- Commit with descriptive messages; do not open a PR unless asked.
