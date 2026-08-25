# CLAUDE.md - monorepo guide (`universalsystemgrade`)

> Claims authority: `mi-research/docs/CLAIMS_LEDGER.md`. The 109-case
> number means 84 modern hindsight-retrodictive cases plus 25 ancient
> interpreter-scored cases. The 67 blind out-of-sample observations and
> 12 relational records are separate.

This repository is **one research platform with three empirical legs plus
infrastructure**. The legs do **not** import each other's code - each is
independently runnable and testable - but they ARE one intellectual project:
how complex systems accumulate and release structural complexity. Find your leg
below, read its own guide before touching code, and do not wire imports across
legs.

| Leg / component | What it is | Start here | Status |
|---|---|---|---|
| **Modernization Index** - `mi-research/` | MI **scoring / diagnostic / retrodiction engine** + the 109-case historical corpus (84 modern hindsight-retrodictive + 25 ancient interpretive). Source-of-truth spec: `MASTER_REFERENCE_ARCHITECTURE.md`. | `mi-research/CLAUDE.md` → `RESEARCH.md` | Live (V3.3); canonical-panel data path. |
| - `mi-pipeline/` | MI **data pipeline** - builds the raw indicator panel from the World Bank API + manual CSVs. | `mi-pipeline/CLAUDE.md` | Real panel committed. |
| - `mi-website/` | The **public Next.js website** for the MI - a consumer of `mi-research`, does not re-implement scoring. | `mi-website/CLAUDE.md` → `mi-website/web/AGENTS.md` | Built + deployable (190+ country pages). |
| **Fragmentation** - `fragmentation/` | The pre-registered discovery program on how self-organizing vs designed systems subdivide (branching factors, dispersion dial, census). | `fragmentation/README.md` → `SYNTHESIS.md` → `preregistration/PREREGISTRATION.md` | Concluded: rung 1, no universal constant. Census ongoing. |
| **Collectivization** - `collectivization/` | 30-case comparative study of fragmentation→collectivization cycles across civilizations (institutional-ceiling model). | `collectivization/README.md` | Active - engine + case data complete. |

> **They share a conceptual origin - the complexity–capacity matching principle
> - not code.** The fragmentation research is the *physics*, the MI is the
> *state* measurement, the collectivization study is the *process*. Keeping them
> import-decoupled is deliberate; do not merge the codebases.

## Directory map

```
mi-research/           MI scoring/diagnostic/retrodiction engine + 109-case corpus
mi-pipeline/           MI raw-indicator data pipeline (World Bank API + CSVs)
mi-website/            Next.js public website (consumer of mi-research)
fragmentation/         The fragmentation discovery program
  discovery/           THE CORE ENGINE. Domain-agnostic (heterogeneity, trivial_null, ladder)
  integration/         Node interface + runner: assemble all nodes -> ladder + controls
  preregistration/     The binding pre-analysis plan (v0.2) + frozen discovery claim
  census/              The fragmentation CENSUS (catalog.py, systems/, governance/)
  natural-systems/     Self-organizing branching domains
    rivers/            Strahler/Horton + power study (real HydroRIVERS)
    biology/           biology_node.py + neuro_node.py (real NeuroMorpho arbors)
    mechanism/         Rung-4 mechanism test (does the dimensional gap predict the factor?)
    negative-controls/ Engineered + classification controls (boundary conditions)
  governance/          Designed/institutional fracture domains
    political/         DGS -> instability mechanism test (2A; NOT a ratio node)
    corporate/         Corporate split factor + survival/hazard (sealed holdout)
    organizations/     Inter-echelon org scaling ratio
    opensource/        Viable-fork factor (boundary probe; real crawl deferred)
  CENSUS.md SYNTHESIS.md README.md   Framing + results narrative
  DGS_AND_SAFEGUARD_J.md             How Study 2A's DGS relates to the MI's Safeguard J
collectivization/      Fragmentation-collectivization cycle study (own top-level project)
README.md CLAUDE.md DEFENSIBLE_RESULTS.md   Repo front door + this guide + all-project results
```

## How the pieces connect (intellectual, not code)

The unifying claim (`fragmentation/SYNTHESIS.md`, `mi-research/MASTER_REFERENCE_ARCHITECTURE.md`
§1): a growing system's interior complexity outruns its interface capacity; the
mismatch must be released as subdivision. Grown systems vent continuously (tight
fracturing); designed systems suppress the venting (dispersed, catastrophic
fracturing proportional to suppression and engineering).

- **Fragmentation → physics.** Self-assembly (rivers, neurons, trees, languages)
  fractures in a tight band that beats chance; designed governance fractures
  dispersedly, severity scaling with engineering (the grown-vs-designed dial).
- **MI → state.** The five-pillar index operationalizes complexity–capacity
  matching as a country instrument. Safeguard J (the P4–P1 durability gate) is
  the same idea as Study 2A's dimensional-gap-score; the MI's composite pillars
  recover signal the raw 2A proxies miss (`fragmentation/DGS_AND_SAFEGUARD_J.md`).
- **Collectivization → process.** Predecessor institutional depth (a P1-like
  variable) governs how a fragmented polity reconsolidates.

---

# Hard rules per leg (these encode the science - do not break them)

## Fragmentation (`fragmentation/`)

- **The observable is a comparable ratio (factor), never a raw count.**
  PREREGISTRATION §4. Normalize (e.g. successors per internal division).
- **Every domain must ship a mechanism-free `null_sampler`.** A finding counts
  only as signal ABOVE that null. Random topology already clusters near 3–4 with
  no law; clustering alone is not a theorem. A domain without a defensible null
  is excluded, not given a pass.
- **Rung 3 uses CI-isolation, NOT point-hypothesis Bayes factors.** Fixed-point
  Bayes factors (e vs 3) are sample-size-hackable. See
  `fragmentation/natural-systems/rivers/results/INTERPRETATION.md` and
  PREREGISTRATION Appendix A. Do not reintroduce a "BF ≥ 10" criterion.
- **Discovery and confirmation use disjoint data.** Do not inspect the sealed
  holdout (open-source + corporate, plus each domain's temporal holdout) during
  discovery. Use `ladder.split` / `ladder.confirm`.
- **Report the highest rung the evidence EARNS, and no higher.** Rung 0 / rung 1
  are real, publishable findings, reported with the same prominence as a positive
  one.
- **Political fragmentation (governance/political) is NOT a ratio node.**
  Administrative hierarchy is designed (a boundary-condition control); its
  contribution is the e-independent DGS→instability prediction. Don't push it
  into the ladder.
- **Per-study module basenames must be unique across the repo** (e.g.
  `biology_node.py`, not `node.py`) - pytest imports test modules by basename and
  collides otherwise.
- **Each study is runnable standalone** (`pytest tests/ -q` from its dir) and via
  the integration runner. Heavy/real data is never committed; `results/` is
  regenerable by one command.

## Modernization Index (`mi-research/`, `mi-pipeline/`, `mi-website/`)

- **Do not change the MI version number or any safeguard definitions** without an
  explicit validation pass. The historical corpus is 109 cases (84 modern hindsight-retrodictive + 25 ancient interpretive).
- **Do not rename files inside `mi-research/`** - `MASTER_REFERENCE_ARCHITECTURE.md`
  and others are referenced by path elsewhere.
- The engine reads the committed panel from the sibling `mi-pipeline/` at build
  time (path constants in `mi/datasource.py`, `mi/global_systems.py`, and several
  `scripts/`). If `mi-pipeline/` moves, update those path constants.
- `mi-website/` is a **consumer** - it does not re-implement scoring. The scheduled
  refresh (`.github/workflows/update-mi-data.yml` → `mi-website/scripts/refresh_and_build.py`)
  regenerates the dataset and commits it; a push triggers the Vercel deploy.
- Preserve all honest nulls and falsifications (golden-age signature refuted on
  holdout; accountability-gap falsified by Cuba) - they are scientific-integrity
  artifacts.

## Collectivization (`collectivization/`)

- The 15 binary governance features and reference type-templates are **fixed
  before any case is coded** (the pre-registration equivalent) - see
  `feature_vector.py`. Do not tune them to fit a case.
- The framework is **diagnostic/structural, not predictive**. It classifies forms
  and measures restructuring magnitude; it does not predict specific outcomes.
- Real GDP/governance series come from Maddison/V-Dem; feature vectors from
  documents. Do not substitute synthetic data for missing real data - flag the
  gap.

## Conventions (all legs)

- Python 3.11. Deps: `numpy`, `scipy`, `matplotlib`, `pytest` (+ `requests` for
  the pipeline, `geopandas`/`pyogrio` optional for river ingest).
- Statistics: two-tailed; exact p-values; effect sizes AND variance components;
  BH-FDR across a test family; a sensitivity analysis for every threshold choice.
- Commit with descriptive messages; do not open a PR unless asked.

## Workflow expectations

- Before committing, run the affected leg's tests from its directory and keep
  them green: `pytest -q -p no:cacheprovider`. For fragmentation, also run
  `fragmentation/integration/run.py` and `fragmentation/census/run.py` and
  confirm they complete (neither has a pytest suite).
- When you wire in real data, do NOT change the downstream statistical stages -
  only the `ingest_*` function and the node's inputs.
