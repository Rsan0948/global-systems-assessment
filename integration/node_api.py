"""
The shared interface every domain node implements so it plugs into the
discovery engine identically.

A DomainNode bundles the three things the engine (discovery/ladder.py) needs:
  * name           : the domain label
  * ratios()       : observed subdivision FACTORS (comparable across domains;
                     see PREREGISTRATION.md sec.4 -- a ratio, never a raw count)
  * null_sampler   : a mechanism-free generator null_sampler(n, rng) -> ratios,
                     i.e. what this domain would look like with no law (sec.3)
  * exponents()    : OPTIONAL (interior_exp, interface_exp) for the rung-4
                     mechanism test; None if the domain has no exponent data.

Each node also declares `is_self_organizing`: boundary-condition controls
(engineered systems, imposed classifications) set this False and are *expected*
to be explained by their trivial null (rung 0).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

import numpy as np

NullSampler = Callable[[int, np.random.Generator], np.ndarray]


@dataclass
class DomainNode:
    name: str
    ratios: np.ndarray
    null_sampler: NullSampler
    is_self_organizing: bool = True
    interior_exp: Optional[float] = None      # scaling exponent of interior complexity
    interface_exp: Optional[float] = None     # scaling exponent of interface capacity
    interior_exp_se: Optional[float] = None
    interface_exp_se: Optional[float] = None
    source: str = ""

    def to_engine(self) -> tuple[str, np.ndarray, NullSampler]:
        return self.name, np.asarray(self.ratios, dtype=float), self.null_sampler

    @property
    def gap(self) -> Optional[float]:
        """Dimensional gap Delta = interior - interface, if both measured."""
        if self.interior_exp is None or self.interface_exp is None:
            return None
        return self.interior_exp - self.interface_exp


def lognormal_null(center: float, log_sd: float = 0.15) -> NullSampler:
    """Convenience mechanism-free sampler: lognormal around a baseline center."""
    def sampler(n: int, rng: np.random.Generator) -> np.ndarray:
        return center * np.exp(rng.normal(0.0, log_sd, size=n))
    return sampler


def assemble(nodes: list[DomainNode], self_organizing_only: bool = True) -> tuple[dict, dict]:
    """Return (data, null_samplers) dicts keyed by node name, ready for
    discovery.ladder.assess. By default includes only self-organizing nodes
    (boundary-condition controls are analyzed separately)."""
    data, nulls = {}, {}
    for nd in nodes:
        if self_organizing_only and not nd.is_self_organizing:
            continue
        name, ratios, sampler = nd.to_engine()
        data[name] = ratios
        nulls[name] = sampler
    return data, nulls
