import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from org_node import build_node


def test_org_node():
    nd = build_node()
    assert nd.name == "organizations"
    assert np.all(nd.ratios > 0)
    assert 2.5 < float(np.exp(np.log(nd.ratios).mean())) < 4.5    # doctrine ratios ~3-4


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-q"]))
