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

Across all seven self-organizing nodes the ladder returns **rung 1 —
"domain-specific laws"**: each domain is individually concentrated (median
CV ≈ 0.17) but the values differ (I² ≈ 0.97), so it is *many small laws*, not
one universal constant. This is a realistic, instructive verdict and exactly the
kind of "weaker but real" result the ladder exists to surface.

The **negative controls** confirm the boundary condition: engineered and
classification systems disperse ~6× more than the self-organizing nodes (mean
CV 1.69 vs 0.26; Brown–Forsythe p ≈ 3×10⁻²⁴).

The **rung-4 mechanism test** correctly reports it *cannot run* on the
illustrative placeholder exponents (they are ~constant) — it needs real exponent
estimates. The **predictive calibrations** all behave: DGS→instability and
corporate-survival each detect a true effect through their controls and stay null
without one; the gap→factor test recovers a true link and is null without one.

Everything here runs on **simulated / literature-summary inputs** and proves the
pipeline, not the theory. Replacing each node's inputs with raw measurements
(via the studies' `ingest_*` hooks) and honoring the sealed-holdout discipline
is what would turn a run into a result.

```bash
pip install numpy scipy matplotlib pytest
python run.py
```
