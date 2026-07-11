# Study 3B — The mechanism test (ladder rung 4)

The test that decides whether a recurring number is a **law** or a coincidence.
A constant that shows up across domains can still be three unrelated processes
landing near the same value. It becomes a theorem only if a mechanism
*predicts* it — here, the **dimensional gap**: interior complexity scaling as
size^a, interface capacity as size^(a−1), gap Δ ≈ 1, with Δ predicting the
subdivision factor.

- `mechanism.estimate_exponents(size, interior_proxy, interface_proxy)` —
  per-domain: recover the interior and interface scaling exponents and their gap
  by log-log regression against system size.
- `mechanism.gap_predicts_factor(gaps, log_factors)` — cross-domain: test
  whether Δ predicts log(subdivision factor) (slope CI excludes 0) and whether
  the gaps cluster at 1.

**Calibration:** recovers exponents (3.0 / 2.0, gap 1.0) from synthetic
allometry; detects a true gap→factor link (slope CI excludes 0, p ≈ 2×10⁻⁷,
R² ≈ 0.94) and returns null when factor is independent of gap.

This is the apex of the ladder: only a positive rung-4 result licenses calling
the regularity a theorem rather than a recurring number.

```bash
pytest tests/ -q
```
