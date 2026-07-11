# Study 2B — Corporate fragmentation

Two contributions:

1. **Ratio node** for the universality ladder — viable resulting entities per
   corporate split, normalized by reported 10-K business segments (so a giant
   conglomerate breaking into many pieces is comparable to a small two-way
   spin-off, not dominating on raw size). `corporate_node.build_node()`.
2. **Predictive test** — does organizational complexity ratio (segments ÷
   management levels) predict a subsequent split / acquisition / failure?
   `survival.fit_hazard` runs a discrete-time logistic-hazard model (a
   dependency-light stand-in for Cox PH) with an LR test on the complexity term.

**Calibration:** the hazard model recovers a true complexity effect
(hazard ratio ≈ 1.65, LR p ≈ 2×10⁻¹³) and is null without one (p ≈ 0.44).

**Data — REAL (SEC EDGAR), no Crunchbase.** `corporate_node.build_node()` loads
the committed cache `results/corporate_splits_edgar.json`, produced by
`ingest_edgar.py` from **free** SEC EDGAR endpoints (no login):

- EDGAR full-text search (`efts.sec.gov`) → every initial Form **10-12B**
  (one filing = one spun-off SpinCo);
- each SpinCo's information statement → the **parent** ("distributed by …");
- group SpinCos by parent → successors **E** = 1 + spuncos;
- the parent's **reportable-segment count S** from its 10-K narrative;
- split factor = **E / S** × 3 (successors per internal division — a comparable
  ratio, never a raw count). Mechanism-free **binary-default null** (firms split
  in two relative to their real segment structure).

Regenerate: `python ingest_edgar.py --start 2001 --end 2024`.

**Cross-domain confirmation (prediction B).** Corporate is the sealed
cross-domain holdout. With real data wired, `confirm_corporate.py` runs B
(B1: definable distribution, not pure null; B2: adding it keeps rung 1 / isolates
no constant). See `results/SEALED_HOLDOUT_CORPORATE.md` — **the seal is now
SPENT.** (2F open-source, the registered co-holdout, is descoped/deferred.)

```bash
pytest tests/ -q
python confirm_corporate.py
```
