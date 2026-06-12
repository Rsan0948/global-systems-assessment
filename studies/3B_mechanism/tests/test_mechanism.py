import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mechanism import estimate_exponents, gap_predicts_factor


def test_estimate_exponents_recovers_slopes():
    rng = np.random.default_rng(0)
    size = np.exp(rng.uniform(1, 6, size=200))
    interior = size ** 3.0 * np.exp(rng.normal(0, 0.05, size=200))
    interface = size ** 2.0 * np.exp(rng.normal(0, 0.05, size=200))
    fit = estimate_exponents(size, interior, interface)
    assert abs(fit.interior_exp - 3.0) < 0.1
    assert abs(fit.interface_exp - 2.0) < 0.1
    assert abs(fit.gap - 1.0) < 0.15


def test_gap_predicts_factor_detects_link():
    rng = np.random.default_rng(1)
    gaps = rng.uniform(0.6, 1.4, size=12)
    log_factors = 1.0 + 0.5 * (gaps - 1.0) + rng.normal(0, 0.04, size=12)
    r = gap_predicts_factor(gaps, log_factors)
    assert r.slope_ci[0] > 0           # slope CI excludes 0 -> gap predicts factor
    assert r.slope_p < 0.05


def test_gap_predicts_factor_null():
    rng = np.random.default_rng(2)
    gaps = rng.uniform(0.6, 1.4, size=12)
    log_factors = 1.0 + rng.normal(0, 0.04, size=12)   # no dependence on gap
    r = gap_predicts_factor(gaps, log_factors)
    assert r.slope_ci[0] <= 0 <= r.slope_ci[1]         # CI includes 0


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-q"]))
