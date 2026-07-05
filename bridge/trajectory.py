"""
Cycle trajectories in pillar space: visualize and classify the
fragmentation-collectivization cycle as a path through MI's 5 dimensions.

Each case traces: pre-fragmentation point → post-collectivization point.
The displacement vector and its shape characterize the transition type.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from pillar_loading import (
    project_normalized, displacement, displacement_magnitude,
    PILLAR_NAMES, PILLAR_LABELS,
)
from organicity import organicity_score


@dataclass
class TrajectoryProfile:
    name: str
    pre_profile: dict[str, float]
    post_profile: dict[str, float]
    displacement: dict[str, float]
    magnitude: float
    dominant_shift: str
    organicity: float
    pathway: str


def classify_shift_direction(disp: dict[str, float]) -> str:
    """Which pillar experienced the largest absolute shift?"""
    if not disp:
        return "none"
    return max(disp, key=lambda p: abs(disp[p]))


def trajectory_profile(name: str,
                        features_pre: list[int],
                        features_post: list[int],
                        pathway: str = "") -> TrajectoryProfile:
    """Compute the full trajectory profile for a single case."""
    pre = project_normalized(features_pre)
    post = project_normalized(features_post)
    disp = displacement(features_pre, features_post)
    mag = displacement_magnitude(features_pre, features_post)
    org = organicity_score(features_pre, features_post)
    dominant = classify_shift_direction(disp)

    return TrajectoryProfile(
        name=name,
        pre_profile=pre,
        post_profile=post,
        displacement=disp,
        magnitude=mag,
        dominant_shift=dominant,
        organicity=org,
        pathway=pathway,
    )


def pathway_displacement_signature(trajectories: list[TrajectoryProfile]) -> dict:
    """Compute the mean displacement vector per pathway type.

    This reveals whether pathways have characteristic directional signatures
    in pillar space (e.g., construction shifts P1/P5; restoration shifts nothing)."""
    pathways = {}
    for t in trajectories:
        if t.pathway not in pathways:
            pathways[t.pathway] = []
        pathways[t.pathway].append(t)

    signatures = {}
    for pw, cases in sorted(pathways.items()):
        if not cases:
            continue
        mean_disp = {}
        for p in PILLAR_NAMES:
            vals = [c.displacement[p] for c in cases]
            mean_disp[p] = round(float(np.mean(vals)), 4)
        mean_mag = round(float(np.mean([c.magnitude for c in cases])), 4)
        mean_org = round(float(np.mean([c.organicity for c in cases])), 4)
        signatures[pw] = {
            "n": len(cases),
            "mean_displacement": mean_disp,
            "mean_magnitude": mean_mag,
            "mean_organicity": mean_org,
            "dominant_shifts": [c.dominant_shift for c in cases],
        }
    return signatures


def trajectory_table(trajectories: list[TrajectoryProfile]) -> list[dict]:
    """Flatten trajectories into a list of dicts for tabular output."""
    rows = []
    for t in trajectories:
        row = {
            "name": t.name,
            "pathway": t.pathway,
            "organicity": t.organicity,
            "magnitude": t.magnitude,
            "dominant_shift": t.dominant_shift,
        }
        for p in PILLAR_NAMES:
            row[f"pre_{p}"] = t.pre_profile[p]
            row[f"post_{p}"] = t.post_profile[p]
            row[f"disp_{p}"] = t.displacement[p]
        rows.append(row)
    return rows
