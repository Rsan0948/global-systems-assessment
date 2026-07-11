# Studies 4A / 4B — Negative controls

The boundary conditions the theory **must** fail, or it explains too much to
explain anything. These nodes are `is_self_organizing=False`, so they are kept
*out* of the universality ladder and tested separately.

- **4A engineered systems** (`nodes.engineered_node`): memory/cache hierarchies,
  filesystem & DB B-tree fan-out, highway interchanges — designer-optimized, so
  predicted to span orders of magnitude rather than cluster.
- **4B imposed classifications** (`nodes.classification_node`): species/genus,
  genera/family, Dewey, Library of Congress — human categories, predicted high
  and variable.

**Test** (`controls_analysis.dispersion_contrast`): do the controls disperse
*more* than the self-organizing nodes? Brown–Forsythe (Levene-on-medians) plus a
direct CV comparison. A boundary condition is **confirmed** if controls disperse
more (p < 0.05); if a control clusters as tightly as self-organizing systems,
the boundary condition is *violated* and that is reported as a primary finding.

**Result on illustrative inputs:** controls disperse ~6× more (mean CV 1.69 vs
0.26; Brown–Forsythe p ≈ 3×10⁻²⁴) — boundary condition confirmed.

**Data (all free):** CPU/OS technical specs, B-tree/index documentation, road
network data for 4A; the GBIF/Catalogue of Life taxonomy and the published
Dewey/LoC schedules for 4B.

```bash
pytest tests/ -q
```
