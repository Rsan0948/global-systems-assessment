# Rivers — cross-continent holdout  [CONFIRMED 2026-06-12 — seal SPENT]

> **STATUS: confirmation complete.** The discovery claim was frozen first
> (`preregistration/FROZEN_DISCOVERY_CLAIM.md`, commit `5cff6be`), then South
> America was measured (`confirm_rivers.py`). Result: SA geom-mean Rb = **3.539**
> (vs NA discovery 3.488) — predictions A1/A2/A3 all PASS. The rivers law
> replicates on an independent continent. The SA holdout is now spent and can no
> longer serve as a clean confirmation set.

Rivers have no temporal axis, so the within-domain confirmation holdout
(PREREGISTRATION §discovery/confirmation split) is **geographic**:

- **Discovery continent:** North America (`HydroRIVERS_v10_na`). The rivers
  `DomainNode` (`river_node.build_node`) loads ONLY this continent. Its per-basin
  Rb is cached in `results/rb_real_na.json`.
- **Sealed holdout continent:** South America (`HydroRIVERS_v10_sa`). The raw
  download may sit under `data/`, but **its Rb is NOT computed or inspected
  during discovery.** There is deliberately no `results/rb_real_sa.json` until
  the confirmation stage.

## Rule
Do NOT run `compute_real_rb.py --continent sa` (or otherwise measure the holdout
continent's Rb) until the discovery verdict for rivers is frozen. At
confirmation, generate `rb_real_sa.json` and feed it through `ladder.confirm`
against the frozen discovery claim.

## Pre-registration amendment needed
The current PREREGISTRATION defines the per-domain holdout as "most-recent-20%
temporal". Rivers have no time axis; this substitutes a **cross-continent
geographic holdout** (discover NA, confirm SA). Log this as a pre-registration
amendment (with rationale) **before** the prereg is publicly deposited.
