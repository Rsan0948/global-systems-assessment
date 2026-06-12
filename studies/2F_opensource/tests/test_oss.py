import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from oss_node import build_node


def test_oss_node_heavy_tailed():
    nd = build_node()
    assert nd.name == "opensource"
    assert np.all(nd.ratios >= 2)
    # boundary probe: expected to be MORE dispersed than a tight branching law
    cv = nd.ratios.std(ddof=1) / nd.ratios.mean()
    assert cv > 0.2


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-q"]))
