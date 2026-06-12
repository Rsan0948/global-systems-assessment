# Study 2A — Political fragmentation (DGS → instability)

This domain does **not** contribute a clean subdivision ratio to the
universality ladder, and the README is explicit about why: a polity's
administrative hierarchy is *designed* (imposed), hence a boundary-condition
control rather than a self-organizing branching system; and raw fragmentation
successor counts conflate parent size with subdivision tendency (the USSR's 15
successors reflect its 15 republics, not a "split-15-ways" law).

Its real, **e-independent** contribution is a mechanism prediction:

> **P-INST:** does the Dimensional-Gap Score (interior economic complexity −
> interface institutional quality) predict subsequent instability *after*
> controlling for GDP per capita, population, region, and period?

`dgs.fit_dgs(panel)` runs the logistic regression, the likelihood-ratio test on
the DGS term (the pre-registered primary statistic), and an out-of-sample AUC
gain on a temporal split. `synthetic.make_panel(beta_dgs_true=...)` provides a
calibrated country-period panel with built-in GDP confounding.

**Calibration result:** with a true effect the test recovers it through the
controls (LR p ≈ 3×10⁻¹², positive but *modest* AUC gain ≈ 0.02); with no
effect it stays null (LR p ≈ 0.68). The modest AUC gain is reported honestly —
DGS adds detectable but small predictive value over the obvious confounds.

Swap in real COW / V-Dem / WGI / Atlas data via `dgs.ingest`.

```bash
pytest tests/ -q
```
