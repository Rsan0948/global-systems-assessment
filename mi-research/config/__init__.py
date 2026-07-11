"""Analysis-layer configuration for the MI robustness program.

Single source of truth for the *analysis-layer* parameters — the frozen mechanical
rule set, outcome/crisis definitions, grading choices, and historical epoch panels.
This is NOT scoring math; scoring goalposts live in ``mi/constants.py`` (``LENS``).

Usage (from any script that has the mi-research root on ``sys.path``):

    import config
    R = config.robustness()               # the whole dict
    rs = config.rule_set()                # mechanical_rule_set block
    R["outcomes"]["crag_coverage_cutoff"] # -> 2015

Stdlib-only (json), matching the engine's no-third-party-deps invariant.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

_CONFIG_DIR = Path(__file__).resolve().parent
_ROBUSTNESS_JSON = _CONFIG_DIR / "robustness.json"


@lru_cache(maxsize=1)
def robustness() -> dict:
    """Return the parsed robustness config (cached)."""
    return json.loads(_ROBUSTNESS_JSON.read_text())


def rule_set() -> dict:
    """The frozen mechanical rule set block (J/spread/P1 thresholds)."""
    return robustness()["mechanical_rule_set"]


def verify_consistency() -> None:
    """Assert the analysis-layer J thresholds match the engine's LENS goalposts.

    Guards against drift between ``config/robustness.json`` and ``mi/constants.py``.
    Best-effort: silently returns if the engine package is not importable (e.g. the
    config is read in a context without the engine on the path).
    """
    try:
        from mi.constants import LENS
    except Exception:
        return
    rs = rule_set()
    assert rs["j_flag_floor"] == LENS["structural_vuln_flag_floor"], (
        f"j_flag_floor {rs['j_flag_floor']} != LENS {LENS['structural_vuln_flag_floor']}"
    )
    assert rs["j_clear_ceiling"] == LENS["structural_vuln_clear_ceiling"], (
        f"j_clear_ceiling {rs['j_clear_ceiling']} != LENS {LENS['structural_vuln_clear_ceiling']}"
    )
