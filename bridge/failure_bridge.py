"""
Failure-mode-to-safeguard bridge: formal correspondence between the
collectivization study's 5 failure modes and the MI's safeguard system.

Each failure mode is defined as a boolean predicate over the 15-feature vector
(in studies/5_collectivization/failure_catalog.py).  Each MI safeguard is
defined as a rule over continuous indicators (in mi-research/mi/safeguards.py).

This module maps between them:
  - Which safeguards SHOULD fire when a failure mode is active?
  - Which MI pillar(s) should be depressed?
  - For modern cases where both feature vectors and MI data exist, do the
    predicted safeguard activations match the actual ones?
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FailureSafeguardMapping:
    failure_mode: str
    description: str
    expected_safeguards: list[str]
    expected_low_pillars: list[str]
    mi_indicator_signature: dict[str, str]


FAILURE_SAFEGUARD_MAP = [
    FailureSafeguardMapping(
        failure_mode="coordination_collapse",
        description="Units cannot act collectively (independent militaries + "
                    "independent foreign policy + unilateral exit)",
        expected_safeguards=["F", "Mod8"],
        expected_low_pillars=["P5"],
        mi_indicator_signature={
            "political_stability": "< 40",
            "gov_effectiveness": "< 50",
        },
    ),
    FailureSafeguardMapping(
        failure_mode="center_predation",
        description="Central authority extracts without accountability (strong "
                    "executive + central tax, no popular sovereignty, no elections)",
        expected_safeguards=["E", "G"],
        expected_low_pillars=["P1"],
        mi_indicator_signature={
            "voice_accountability": "< 30",
            "control_corruption": "< 30",
            "resource_rents": "> 15",
        },
    ),
    FailureSafeguardMapping(
        failure_mode="competitive_destruction",
        description="Units engage in mutually destructive rivalry (independent "
                    "militaries + independent diplomacy, no shared trade/movement)",
        expected_safeguards=["D"],
        expected_low_pillars=["P4", "P5"],
        mi_indicator_signature={
            "political_stability": "< 30",
            "trade_openness": "< 50",
        },
    ),
    FailureSafeguardMapping(
        failure_mode="legitimacy_vacuum",
        description="No broadly accepted basis for authority (no popular "
                    "sovereignty, no elections)",
        expected_safeguards=["C"],
        expected_low_pillars=["P1"],
        mi_indicator_signature={
            "voice_accountability": "< 25",
        },
    ),
    FailureSafeguardMapping(
        failure_mode="rigidity_sclerosis",
        description="System cannot adapt (hereditary executive, no exit, no "
                    "elections)",
        expected_safeguards=["C", "G"],
        expected_low_pillars=["P1", "P2"],
        mi_indicator_signature={
            "voice_accountability": "< 30",
            "regulatory_quality": "< 40",
        },
    ),
]


# Feature indices that trigger each failure mode (mirrored from failure_catalog.py)
_FAILURE_PREDICATES = {
    "coordination_collapse": {
        "trigger_features": [2, 3, 6],
        "trigger_absent": [],
    },
    "center_predation": {
        "trigger_features": [0, 7],
        "trigger_absent": [8, 9],
    },
    "competitive_destruction": {
        "trigger_features": [2, 3],
        "trigger_absent": [4, 10, 11],
    },
    "legitimacy_vacuum": {
        "trigger_features": [],
        "trigger_absent": [8, 9],
    },
    "rigidity_sclerosis": {
        "trigger_features": [0, 1],
        "trigger_absent": [6, 9],
    },
}


def is_failure_active(failure_mode: str, features: list[int]) -> bool:
    """Check whether a failure mode's triggering condition is present."""
    pred = _FAILURE_PREDICATES[failure_mode]
    triggers_on = all(features[i] == 1 for i in pred["trigger_features"])
    triggers_off = all(features[i] == 0 for i in pred["trigger_absent"])
    return triggers_on and triggers_off


def active_failures(features: list[int]) -> list[str]:
    """Which failure modes are triggered by this feature vector?"""
    return [fm for fm in _FAILURE_PREDICATES if is_failure_active(fm, features)]


def expected_safeguards(features: list[int]) -> list[str]:
    """Which MI safeguards should fire given this feature vector?"""
    safeguards = set()
    for mapping in FAILURE_SAFEGUARD_MAP:
        if is_failure_active(mapping.failure_mode, features):
            safeguards.update(mapping.expected_safeguards)
    return sorted(safeguards)


def expected_weak_pillars(features: list[int]) -> list[str]:
    """Which MI pillars should be depressed given the active failure modes?"""
    pillars = set()
    for mapping in FAILURE_SAFEGUARD_MAP:
        if is_failure_active(mapping.failure_mode, features):
            pillars.update(mapping.expected_low_pillars)
    return sorted(pillars)


def failure_bridge_diagnostic(features_pre: list[int],
                               features_post: list[int]) -> dict:
    """Full failure-bridge diagnostic for a pre/post pair.

    Reports which failure modes were active before, which are active after,
    which were patched, which are new, and the expected MI implications
    of each."""
    pre_active = active_failures(features_pre)
    post_active = active_failures(features_post)
    patched = [f for f in pre_active if f not in post_active]
    new_vuln = [f for f in post_active if f not in pre_active]
    persistent = [f for f in pre_active if f in post_active]

    pre_safeguards = expected_safeguards(features_pre)
    post_safeguards = expected_safeguards(features_post)
    resolved = [s for s in pre_safeguards if s not in post_safeguards]
    new_safeguards = [s for s in post_safeguards if s not in pre_safeguards]

    return {
        "pre_failures": pre_active,
        "post_failures": post_active,
        "patched": patched,
        "new_vulnerabilities": new_vuln,
        "persistent": persistent,
        "pre_expected_safeguards": pre_safeguards,
        "post_expected_safeguards": post_safeguards,
        "safeguards_resolved": resolved,
        "safeguards_introduced": new_safeguards,
        "pre_weak_pillars": expected_weak_pillars(features_pre),
        "post_weak_pillars": expected_weak_pillars(features_post),
    }
