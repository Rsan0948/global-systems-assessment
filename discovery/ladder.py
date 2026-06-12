"""
The four-rung ladder and the discover -> confirm split.

"Is there a theorem?" is decomposed into nested claims, each a real (weaker)
result on its own. The engine reports the HIGHEST rung the evidence supports,
and never claims a higher rung than the data earns.

  Rung 0  No theorem: within-domain scatter is large, OR the signal is
          indistinguishable from the mechanism-free trivial null.
  Rung 1  Domains are individually lawful: each domain has a concentrated
          characteristic ratio, and it differs from that domain's trivial null.
          (Heterogeneity across domains may still be high -- many small laws.)
  Rung 2  Universality: domains share one value (Cochran Q not significant,
          low I^2) AND that shared concentration exceeds the trivial null.
  Rung 3  Named constant: the pooled value's CI is tight enough to include a
          principled constant (e, 3, golden ratio, pi, ...) and exclude rivals.
  Rung 4  Mechanism (NOT decidable from ratios alone): the interior-minus-
          interface dimensional gap predicts the ratio. Requires the Study-3B
          exponent data; the engine exposes a hook but cannot self-certify it.

Critical discipline: rungs are *discovered* on a discovery partition and then
*confirmed* on a sealed holdout partition the discovery never saw. A rung that
does not survive confirmation is reported as exploratory only.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from heterogeneity import analyze, HeterogeneityResult
from trivial_null import compare, NullSampler

# principled constants to check at rung 3
CONSTANTS = {"e": math.e, "3": 3.0, "pi": math.pi, "golden^2": ((1 + 5 ** 0.5) / 2) ** 2,
             "golden": (1 + 5 ** 0.5) / 2, "2": 2.0, "4": 4.0}

CV_CONCENTRATED = 0.30        # median within-domain CV below this => "concentrated"
I2_UNIVERSAL = 0.25           # I^2 below this (with Q n.s.) => "universal"


@dataclass
class LadderVerdict:
    rung: int
    label: str
    reason: str
    het: HeterogeneityResult
    trivial: object = None
    constants_in_ci: list = field(default_factory=list)
    exploratory: bool = True       # set False only after confirm() passes


def assess(data: dict[str, np.ndarray], null_samplers: dict[str, NullSampler] | None = None,
           n_sims: int = 500, seed: int = 0) -> LadderVerdict:
    het = analyze(data)
    median_cv = float(np.median(list(het.within_domain_cv.values())))
    concentrated = median_cv < CV_CONCENTRATED

    triv = compare(het, null_samplers, n_sims=n_sims, seed=seed) if null_samplers else None
    nontrivial = None
    if triv is not None:
        median_abs_z = float(np.median([abs(z) for z in triv.per_domain_z.values()]))
        nontrivial = (triv.pooled_displacement_p < 0.05
                      or triv.tau_below_null_p < 0.05
                      or median_abs_z > 2.0)

    universal = (het.q_p > 0.05) and (het.i_squared < I2_UNIVERSAL)
    constants_in_ci = [name for name, v in CONSTANTS.items()
                       if het.pooled_ci[0] <= v <= het.pooled_ci[1]]

    # Rung 0 gates
    if not concentrated:
        return LadderVerdict(0, "no theorem",
                             f"within-domain scatter large (median CV={median_cv:.2f} >= {CV_CONCENTRATED})",
                             het, triv, constants_in_ci)
    if triv is not None and nontrivial is False:
        return LadderVerdict(0, "no theorem (trivial)",
                             "signal indistinguishable from mechanism-free null "
                             f"(pooled disp p={triv.pooled_displacement_p:.2f}, "
                             f"tau-below-null p={triv.tau_below_null_p:.2f})",
                             het, triv, constants_in_ci)

    if universal:
        if len([c for c in constants_in_ci if c not in ("2", "4")]) == 1:
            only = [c for c in constants_in_ci if c not in ("2", "4")][0]
            return LadderVerdict(3, f"named constant ~ {only}",
                                 f"universal (Q p={het.q_p:.2f}, I^2={het.i_squared:.2f}); "
                                 f"pooled CI {tuple(round(x,3) for x in het.pooled_ci)} isolates {only}",
                                 het, triv, constants_in_ci)
        return LadderVerdict(2, "universal (value not isolated)",
                             f"domains share one value (Q p={het.q_p:.2f}, I^2={het.i_squared:.2f}); "
                             f"pooled={het.pooled_ratio:.3f}, but CI admits {constants_in_ci}",
                             het, triv, constants_in_ci)

    return LadderVerdict(1, "domain-specific laws",
                         f"each domain concentrated (median CV={median_cv:.2f}) but values differ "
                         f"(Q p={het.q_p:.3f}, I^2={het.i_squared:.2f})",
                         het, triv, constants_in_ci)


def split(data: dict[str, np.ndarray], holdout: list[str]) -> tuple[dict, dict]:
    """Partition domains into (discovery, confirmation). Confirmation domains
    must not be looked at during discovery."""
    disc = {k: v for k, v in data.items() if k not in holdout}
    conf = {k: v for k, v in data.items() if k in holdout}
    return disc, conf


def confirm(discovery: LadderVerdict, holdout_data: dict[str, np.ndarray],
            null_samplers: dict[str, NullSampler] | None = None, **kw) -> dict:
    """Re-run the discovered claim on the sealed holdout and check consistency.

    For a universality/constant claim, confirmation passes if the holdout's
    pooled CI overlaps the discovery pooled CI and reaches a rung >= 2.
    """
    held = assess(holdout_data, null_samplers, **kw)
    d_lo, d_hi = discovery.het.pooled_ci
    h_lo, h_hi = held.het.pooled_ci
    ci_overlap = not (h_hi < d_lo or h_lo > d_hi)
    passed = ci_overlap and held.rung >= min(discovery.rung, 2) if discovery.rung >= 2 else ci_overlap
    discovery.exploratory = not passed
    return {
        "discovery_rung": discovery.rung,
        "discovery_pooled_ci": discovery.het.pooled_ci,
        "holdout_rung": held.rung,
        "holdout_pooled_ci": held.het.pooled_ci,
        "ci_overlap": ci_overlap,
        "confirmation_passed": bool(passed),
    }
