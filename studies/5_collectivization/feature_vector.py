"""
The 15 binary governance features and type-assignment engine.

Each feature is verifiable from constitutional documents, legal codes, or
observable institutional facts. Two researchers reading the same documents
check the same boxes.

Feature definitions and reference type templates are fixed BEFORE coding
any case (the pre-registration equivalent).
"""

from __future__ import annotations

import numpy as np

FEATURE_NAMES = [
    "single_executive",           # 0: single individual holds supreme executive authority
    "hereditary_succession",      # 1: executive succession is hereditary
    "independent_militaries",     # 2: constituent units maintain independent militaries
    "independent_foreign_policy", # 3: constituent units maintain independent foreign policy
    "shared_currency",            # 4: shared currency exists
    "shared_legal_code",          # 5: binding shared legal code applies to individuals
    "unilateral_exit",            # 6: constituent units can unilaterally exit
    "central_tax",                # 7: central tax collection reaches individuals directly
    "popular_sovereignty",        # 8: authority justified by popular sovereignty
    "elected_leadership",         # 9: leadership selected by election
    "free_movement_persons",      # 10: free movement of persons across internal boundaries
    "free_movement_goods",        # 11: free movement of goods (no internal tariffs)
    "shared_supreme_court",       # 12: shared supreme court / final legal arbiter
    "central_standing_army",      # 13: central government controls standing army
    "preexisting_polities",       # 14: constituent units existed as independent polities
]

N_FEATURES = len(FEATURE_NAMES)
assert N_FEATURES == 15

# Reference templates: idealized archetypes. Real cases are assigned to the
# nearest type by Hamming distance -- no subjective judgment.
TYPE_TEMPLATES = {
    "personal_empire":       [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1],
    "feudal_order":          [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    "city_state_system":     [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    "dynastic_composite":    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    "confederation":         [0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1],
    "unitary_nation_state":  [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    "federal_republic":      [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    "ideological_party":     [1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1],
    "colonial_imperial":     [1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
    "supranational_union":   [0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
}


def validate(features: list[int]) -> None:
    """Raise on invalid feature vector."""
    if len(features) != N_FEATURES:
        raise ValueError(f"expected {N_FEATURES} features, got {len(features)}")
    if not all(f in (0, 1) for f in features):
        raise ValueError("all features must be 0 or 1")


def hamming(a: list[int], b: list[int]) -> int:
    """Hamming distance between two binary feature vectors."""
    return sum(x != y for x, y in zip(a, b))


def classify(features: list[int]) -> tuple[str, int]:
    """Assign the nearest governance type by Hamming distance.
    Returns (type_name, distance). Ties broken alphabetically."""
    validate(features)
    best_name, best_dist = "", N_FEATURES + 1
    for name, template in sorted(TYPE_TEMPLATES.items()):
        d = hamming(features, template)
        if d < best_dist:
            best_name, best_dist = name, d
    return best_name, best_dist


def flip_count(pre: list[int], post: list[int]) -> int:
    """Total number of features that changed between pre and post."""
    validate(pre)
    validate(post)
    return hamming(pre, post)


def flipped_features(pre: list[int], post: list[int]) -> list[str]:
    """Names of features that flipped."""
    validate(pre)
    validate(post)
    return [FEATURE_NAMES[i] for i in range(N_FEATURES) if pre[i] != post[i]]


def integration_depth(features: list[int]) -> int:
    """Sum of integration-related features (4,5,7,10,11,12).
    Scale 0-6, fully deterministic."""
    validate(features)
    return sum(features[i] for i in [4, 5, 7, 10, 11, 12])


def functional_breadth(features: list[int]) -> int:
    """Count of integrated functional domains (military, economic, legal,
    movement, diplomatic). Scale 0-5."""
    validate(features)
    military = features[13]                   # central standing army
    economic = 1 if (features[4] and features[11]) else 0  # currency + free goods
    legal = features[5]                       # shared legal code
    movement = features[10]                   # free movement of persons
    diplomatic = 1 - features[3]              # NOT independent foreign policy
    return military + economic + legal + movement + diplomatic


LEGITIMACY_FEATURES = [0, 1, 7, 8, 9]

def legitimacy_flips(pre: list[int], post: list[int]) -> int:
    """Count flips in the legitimacy-basis subset (features 0,1,7,8,9)."""
    validate(pre)
    validate(post)
    return sum(pre[i] != post[i] for i in LEGITIMACY_FEATURES)
