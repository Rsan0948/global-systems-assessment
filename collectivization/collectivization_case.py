"""
The CaseProfile dataclass -- the shared interface for every historical
fragmentation-collectivization case.

Analogous to integration/node_api.py's DomainNode, but for a different kind
of study: this is not a ratio-based fragmentation node (it does not plug into
the ladder), but a structured historical case with feature vectors, scope
measurements, and time series.

Every field is either (a) a countable fact from historical records, (b) a
binary feature lookup from constitutional documents, or (c) a growth rate
computed from the Maddison/V-Dem datasets already in the repo. The three
judgment calls per case (periodization dates) are documented and fixed.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CaseProfile:
    name: str
    is_control: bool

    # Periodization (the ONLY judgment calls -- defined once per case)
    pre_frag_year: int
    frag_peak_year: int
    first_integration_year: int
    post_collect_year: int

    # 15 binary governance features (all fact-lookups)
    features_pre: list[int]
    features_post: list[int]

    # Ratchet dimensions (counts and ratios from historical records)
    units_pre: int
    units_peak: int
    units_post: int
    pop_pre: float
    pop_post: float
    gdp_growth_pre: float      # avg annual GDP/cap growth, 30yr before pre_frag_year
    gdp_growth_post: float     # avg annual GDP/cap growth, 30yr after post_collect_year

    # Timing / intensity (all countable)
    frag_duration_years: int
    conflicts_per_decade: float
    collect_speed_years: int
    durability_years: int

    # Time series for warning signals (from existing datasets)
    gdp_series: dict[int, float] = field(default_factory=dict)
    vdem_series: dict[int, float] = field(default_factory=dict)

    # Provenance
    sources: str = ""
    notes: str = ""
