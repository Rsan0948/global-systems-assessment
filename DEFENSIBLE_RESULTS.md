# Defensible results so far

> **Scope disclaimer.** This summarizes what the current pipeline supports, sorted
> by how much weight each claim can bear. Real-data results are flagged; simulated
> nodes prove the *pipeline*, not the theory. The cross-domain pooled number is
> **not** a finding about real systems (see "What is NOT defensible yet").
> Numbers below were verified against a live re-run of `integration/run.py`.

## What's genuinely defensible (real data)

### 1. Rivers — the one fully confirmed result
- Real HydroRIVERS (HydroSHEDS): North America = 3,412 basins, South America =
  2,256 basins, measured by Strahler/Horton bifurcation ratio (Rb).
- Discovery (NA): geom-mean Rb = **3.488**.
- Frozen in git (`preregistration/FROZEN_DISCOVERY_CLAIM.md`, commit `5cff6be`)
  **before** the SA holdout was touched, with three falsifiable predictions.
- Confirmation (SA, sealed holdout): geom-mean Rb = **3.539**. Predictions
  A1 (beats random null), A2 (in [3.2, 3.8]), A3 (above e) **all passed**.
- This is the only result that cleared the full discovery → sealed-confirmation
  discipline. The "~3.5 for natural systems" intuition lives here, and it holds.

### 2. Biology — real, discovery-stage, not yet holdout-confirmed
- Real NeuroMorpho.org reconstructions, 6 cell types × 150 arbors each, measured
  by the *same* Horton instrument as rivers.

  | cell type   | Rb    |
  |-------------|-------|
  | motoneuron  | 3.743 |
  | pyramidal   | 3.685 |
  | purkinje    | 3.445 |
  | interneuron | 3.275 |
  | ganglion    | 3.216 |
  | granule     | 2.917 |

- Each concentrated (CV ≈ 0.17–0.25) and at/above the ~3.0 random-merging null.
- Real and meaningful, but no frozen cross-holdout confirmation yet — a discovery
  finding, not a confirmed one.

### 3. The boundary-condition control holds (real)
- Real NCBI taxonomy + engineered specs (non-self-organizing).
- They disperse ~22× more: control mean CV = **5.77** vs self-organizing
  **0.26**; Brown–Forsythe p ≈ 1e-252.
- Cleanest single piece of evidence: self-organizing systems concentrate,
  designed/arbitrary ones don't.

### 4. The DGS → instability prediction is a real, defensible NULL
- Real ECI + V-Dem + World Bank + UCDP panel, n = 713, 144 countries.
- Dimensional-gap adds nothing beyond GDP + population + governance
  (β = 0.107, p = 0.42, AUC gain 0.0; robust across 5 sensitivity specs).
- A correctly reported negative result.

## How we got them (methodology)

- **Observable:** one Horton/Strahler bifurcation ratio per unit (basin, arbor) —
  a comparable factor, never a raw count. Identical code (`studies/2C_river_networks/horton.py`)
  for rivers and neurons.
- **Null-anchored:** every domain ships a mechanism-free null (random-coalescent /
  random binary merging) run through the same instrument; it lands at ~3.0, so
  only signal *above* that counts. The pipeline's honesty check confirms neutral
  topology → ~2.98 and the procedure declines to call it *e*.
- **Ladder verdict:** DerSimonian–Laird between/within-domain variance + Q-test
  decides the rung.
- **Rung 3 = CI-isolation, not Bayes factors** — the misspecification probe showed
  fixed-point BFs hack toward whichever value is nearer as n grows, so they were
  dropped.
- **Discovery/confirmation are disjoint**, enforced by the git freeze + sealed
  holdout.

## What is NOT defensible yet

- **Corporate (2.04), organizations (3.20), open-source (2.79) are synthetic** —
  `rng`-generated placeholders; real EDGAR/GitHub ingests not built. Pipeline only.
- Therefore the **cross-domain pooled 3.162 / "Rung 1" verdict is contaminated** —
  it mixes 7 real nodes with 3 simulated ones. The pooled cross-domain number is
  **not** a claim about real systems.
- The committed `integration/results/integration_summary.json` `note` field
  ("all other domains simulated") is **stale** — biology is in fact real. Doc bug.

## Bottom line

Restricted to **real self-organizing data (rivers + 6 neuron types)**: each domain
is tightly concentrated, every one sits at/above the ~3.0 mundane null, they span
**~2.9–3.7**, and they **do not share a single value** (motoneuron 3.74 vs granule
2.92) — that's **Rung 1, domain-specific laws**, not a universal constant, and the
pooled CI excludes *e*. Rivers specifically ≈ 3.5 and is holdout-confirmed; that's
the strongest, cleanest result.
