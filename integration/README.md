# Integration

Wires the domain nodes into the discovery engine and runs the full pipeline:

  **assemble nodes → discovery ladder → verdict**, plus the two mechanism
  calibrations (DGS→instability, gap→factor).

- `node_api.py` — the shared `DomainNode` interface every study implements
  (name, ratios, mechanism-free `null_sampler`, optional scaling exponents).
- `nodes_literature.py` — illustrative nodes (rivers, bronchial, vascular,
  botanical) built from literature summary statistics so the pipeline runs
  without network access.
- `run.py` — one command: ladder verdict + DGS calibration + mechanism
  calibration + a forest plot, all to `results/`.

## What the run shows (`results/integration_summary.json`, `.png`)

On the illustrative literature nodes the ladder returns **rung 0 — "no theorem
(trivial)"**: although the ratios cluster near 3, the between-domain
concentration is *no tighter than the mechanism-free null* (tau-below-null
p ≈ 1.0), so the triviality control correctly declines to call free
combinatorics a law. This is the discipline working as designed — clustering
near 3 is **not** evidence of a theorem on its own.

The DGS test detects a true instability effect through the controls and is null
without one; the mechanism test recovers a true gap→factor link and is null
without one.

Everything here runs on **simulated / literature-summary inputs** and proves the
pipeline, not the theory. Replacing each node's inputs with raw measurements
(via the studies' `ingest_*` hooks) and honoring the sealed-holdout discipline
is what would turn a run into a result.

```bash
pip install numpy scipy matplotlib pytest
python run.py
```
