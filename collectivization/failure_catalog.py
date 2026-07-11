"""
Feature-to-failure linkage: the error-patching engine.

Each failure mode is defined as a boolean predicate over the 15-feature
governance vector. No interpretation -- pure predicate evaluation.

For a given (features_pre, features_post) pair, reports which failure modes
were active in the old form and which were patched by the new form.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FailureMode:
    name: str
    description: str
    trigger_features: list[int]    # feature indices that must be 1
    trigger_absent: list[int]      # feature indices that must be 0
    patch_features: list[int]      # features that must flip (any 2+) to patch

    def is_active(self, features: list[int]) -> bool:
        """Is this failure mode's triggering condition present?"""
        triggers_on = all(features[i] == 1 for i in self.trigger_features)
        triggers_off = all(features[i] == 0 for i in self.trigger_absent)
        return triggers_on and triggers_off

    def is_patched(self, pre: list[int], post: list[int]) -> bool:
        """Did the post-collectivization form flip enough patch features?"""
        if not self.is_active(pre):
            return False
        flipped = sum(pre[i] != post[i] for i in self.patch_features)
        return flipped >= 2


FAILURE_MODES = [
    FailureMode(
        name="coordination_collapse",
        description="Units cannot act collectively when needed (independent "
                    "militaries, independent foreign policy, easy exit)",
        trigger_features=[2, 3, 6],  # indep militaries, indep foreign, unilateral exit
        trigger_absent=[],
        patch_features=[2, 3, 6],    # post-collect flips at least 2 of these 3 to 0
    ),
    FailureMode(
        name="center_predation",
        description="Central authority extracts without accountability "
                    "(strong executive + direct tax, no popular sovereignty, no elections)",
        trigger_features=[0, 7],     # single executive, central tax
        trigger_absent=[8, 9],       # no popular sovereignty, no elections
        patch_features=[8, 9],       # post-collect flips at least one (but we check 2 for rigor)
    ),
    FailureMode(
        name="competitive_destruction",
        description="Units engage in mutually destructive rivalry "
                    "(independent militaries/diplomacy, no shared currency/trade/movement)",
        trigger_features=[2, 3],     # independent militaries, independent foreign policy
        trigger_absent=[4, 10, 11],  # no shared currency, no free movement, no free goods
        patch_features=[4, 10, 11],  # post-collect flips at least 2 of these 3 to 1
    ),
    FailureMode(
        name="legitimacy_vacuum",
        description="No broadly accepted basis for authority "
                    "(no popular sovereignty, no elections, and the prior legitimacy "
                    "basis has eroded)",
        trigger_features=[],
        trigger_absent=[8, 9],       # no popular sovereignty, no elections
        patch_features=[8, 9],       # post-collect introduces a new legitimacy mechanism
    ),
    FailureMode(
        name="rigidity_sclerosis",
        description="System cannot adapt to changed conditions "
                    "(no exit, hereditary executive locked in, no elections)",
        trigger_features=[0, 1],     # single executive, hereditary
        trigger_absent=[6, 9],       # no exit, no elections
        patch_features=[1, 6, 9],    # post-collect flips hereditary or adds elections/exit
    ),
]


def active_failures(features: list[int]) -> list[str]:
    """Which failure modes are triggered by this feature vector?"""
    return [fm.name for fm in FAILURE_MODES if fm.is_active(features)]


def patched_failures(pre: list[int], post: list[int]) -> list[str]:
    """Which failure modes were active in pre and patched by post?"""
    return [fm.name for fm in FAILURE_MODES if fm.is_patched(pre, post)]


def unpatched_failures(pre: list[int], post: list[int]) -> list[str]:
    """Which failure modes were active in pre but NOT patched by post?"""
    return [fm.name for fm in FAILURE_MODES
            if fm.is_active(pre) and not fm.is_patched(pre, post)]


def new_vulnerabilities(pre: list[int], post: list[int]) -> list[str]:
    """Which failure modes are active in post but were NOT active in pre?
    These are the NEW vulnerabilities introduced by the collectivization."""
    return [fm.name for fm in FAILURE_MODES
            if fm.is_active(post) and not fm.is_active(pre)]


def diagnostic(pre: list[int], post: list[int]) -> dict:
    """Full failure-mode diagnostic for a case."""
    return {
        "active_pre": active_failures(pre),
        "active_post": active_failures(post),
        "patched": patched_failures(pre, post),
        "unpatched": unpatched_failures(pre, post),
        "new_vulnerabilities": new_vulnerabilities(pre, post),
    }
