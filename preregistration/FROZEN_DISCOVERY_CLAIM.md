# Frozen discovery claim — carried into confirmation

**Frozen: 2026-06-12, before any holdout was inspected.** This file is the
internal pre-registration of the confirmation test: the discovery-stage claims
below are fixed here, in git, *before* the sealed holdouts are measured. The
holdouts must not be re-inspected or re-tuned after this commit. (A public
OSF/arXiv deposit of this same claim is optional and only adds a third-party
timestamp; it is not required for the confirmation to be honest.)

## Discovery dataset (already measured, committed)
- **Rivers (2C):** HydroRIVERS, North America, n=1219 basins (≥4 Strahler orders).
- **Biology (2D):** NeuroMorpho, 6 cell types × 150 arbors.
- **Negative controls (4):** real NCBI taxonomy fan-out + real engineered specs.
- **DGS (2A):** real ECI+V-Dem+WB+UCDP panel.

## Frozen quantitative claims
1. **Rung 1 — domain-specific laws.** Self-organizing domains are individually
   concentrated (CV ~0.2) but do NOT share one value (I²≈0.98). Pooled ratio
   ~3.16, 95% CI ≈ [2.97, 3.37].
2. **Not e.** Every self-organizing domain that beats its triviality null sits
   ABOVE e (2.718); the pooled CI excludes e.
3. **Lawful band ~3.3–3.7**, above the random-topology null (~3.0).
4. **Boundary condition:** non-self-organizing controls disperse far more
   (≥6× CV) than self-organizing domains.
5. **DGS mechanism:** the dimensional-gap → instability prediction is NULL.

## Pre-registered confirmation predictions (what the SEALED holdouts must show)

### A. Rivers cross-continent holdout = South America (within-domain)
An independent continent must REPRODUCE the rivers discovery finding:
- **A1.** SA rivers beat the random-topology null (one-sided p < 0.05).
- **A2.** SA geom-mean Rb consistent with NA: in **[3.2, 3.8]** (NA was 3.49).
- **A3.** SA sits **above e** (geom-mean Rb > 2.718, and the bulk of basins above e).
PASS = A1 ∧ A2 ∧ A3.

### B. Cross-domain holdout = corporate (2B) + open-source (2F)
Held out entirely during discovery (no real data ingested yet). On real data:
- **B1.** Each is individually a definable distribution (not pure null).
- **B2.** They do NOT collapse the verdict to a single universal constant — i.e.
  adding them keeps I² high / pooled CI still excludes a single named constant
  (consistent with rung 1, not rung 2/3).
NOTE: B requires building the SEC EDGAR (2B) and GitHub (2F) real ingests; only
then is B run. A can be run immediately (SA already downloaded).

---

## Confirmation log (appended after the freeze — does NOT alter the claims above)

- **2026-06-12 — Prediction A (rivers, South America):** CONFIRMED. A1/A2/A3 all
  pass (SA geom Rb 3.539). See `studies/2C_river_networks/results/SEALED_HOLDOUT.md`.
  The SA holdout is SPENT.
- **2026-06-27 — Prediction B (cross-domain): RUN ONCE; corporate-only.** 2F
  open-source was descoped (GitHub real ingest deferred), so B was run on
  **corporate (2B) alone** as the cross-domain holdout — a pre-registration
  amendment (weaker, conservative). Result on 108 real SEC EDGAR split events:
  **B1 FAIL** (corporate is indistinguishable from its binary-default null,
  displacement p=0.23 → trivial/rung-0), **B2 PASS** (adding corporate keeps
  rung 1, I²=0.98, isolates no constant). **B NOT fully confirmed**; the
  rung-1 / no-universal-constant verdict stands. The corporate cross-domain
  holdout is now SPENT. See `studies/2B_corporate/results/SEALED_HOLDOUT_CORPORATE.md`.
