# Study 2D — Biological branching (domain node)

A discovery-engine node (see `../../discovery/`) for self-organizing biological
hierarchies: bronchial trees, vascular beds, botanical branching.

- **Observable:** branching ratio (comparable factor, per pre-registration §4).
- **Trivial null:** random binary branching topology (~3), so the biological
  signal counts only if it sits away from this baseline.
- **Mechanism input:** carries illustrative interior/interface scaling exponents
  (Murray's law → interior ~3, interface ~2, gap ~1) for the rung-4 test (3B).

`node.build_node()` returns a `DomainNode`. Measurements are currently sampled
from literature-reported summary statistics (documented ranges, not invented
precision); replace with raw morphometry / FIA data via `node.ingest_fia` (and
analogous hooks) in an environment with data access.

```bash
pytest tests/ -q
```
