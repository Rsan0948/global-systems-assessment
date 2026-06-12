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

**Data — no Crunchbase needed.** The original plan listed Crunchbase for startup
data, but it is paywalled. This domain runs entirely on **free** sources:
SEC EDGAR (every US public company's 8-K/10-12B spin-off filings and 10-K
business-segment counts) and Wikipedia's spin-off list as a cross-check. Wire
them via `corporate_node.ingest_edgar`.

```bash
pytest tests/ -q
```
