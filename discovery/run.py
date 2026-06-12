"""
Calibration demo for the discovery engine.

  python run.py

Runs all three ground-truth worlds through `assess`, plus a discover->confirm
split on the universal world, and writes verdicts + a figure to ./results.
A correct engine returns rung 3 / rung 1 / rung 0 respectively.
"""

from __future__ import annotations

import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from ladder import assess, split, confirm
import scenarios

RESULTS = os.path.join(os.path.dirname(__file__), "results")


def _verdict_dict(v) -> dict:
    return {
        "rung": v.rung,
        "label": v.label,
        "reason": v.reason,
        "pooled_ratio": round(v.het.pooled_ratio, 4),
        "pooled_ci": [round(x, 4) for x in v.het.pooled_ci],
        "tau": round(v.het.tau, 4),
        "i_squared": round(v.het.i_squared, 3),
        "q_p": round(v.het.q_p, 4),
        "median_within_cv": round(float(np.median(list(v.het.within_domain_cv.values()))), 3),
        "constants_in_ci": v.constants_in_ci,
        "trivial_pooled_displacement_p": None if v.trivial is None else round(v.trivial.pooled_displacement_p, 3),
        "trivial_tau_below_null_p": None if v.trivial is None else round(v.trivial.tau_below_null_p, 3),
    }


def main() -> None:
    os.makedirs(RESULTS, exist_ok=True)
    nulls = scenarios.null_samplers()

    worlds = {
        "universal (truth: rung 3, value=e)": scenarios.universal_world(),
        "domain_specific (truth: rung 1)": scenarios.domain_specific_world(),
        "trivial (truth: rung 0)": scenarios.trivial_world(),
    }

    summary = {}
    verdicts = {}
    for label, data in worlds.items():
        v = assess(data, null_samplers=nulls, n_sims=400, seed=7)
        verdicts[label] = v
        summary[label] = _verdict_dict(v)

    # discover -> confirm on the universal world: hold out two domains
    uni = scenarios.universal_world(seed=11)
    disc_data, conf_data = split(uni, holdout=["trees", "vasculature"])
    disc_v = assess(disc_data, null_samplers={k: nulls[k] for k in disc_data}, n_sims=400, seed=7)
    conf = confirm(disc_v, conf_data, null_samplers={k: nulls[k] for k in conf_data}, n_sims=400, seed=7)
    summary["discover_then_confirm (universal)"] = conf

    with open(os.path.join(RESULTS, "engine_calibration.json"), "w") as f:
        json.dump(summary, f, indent=2)

    # figure: per-domain estimates with pooled band, one panel per world
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), sharey=True)
    for ax, (label, v) in zip(axes, verdicts.items()):
        names = [e.name for e in v.het.domains]
        vals = [e.ratio_mean for e in v.het.domains]
        ax.scatter(vals, range(len(names)), color="#333", zorder=3)
        ax.set_yticks(range(len(names)))
        ax.set_yticklabels(names, fontsize=8)
        ax.axvspan(v.het.pooled_ci[0], v.het.pooled_ci[1], color="#88aacc", alpha=0.4)
        ax.axvline(np.e, ls="--", color="green", lw=1)
        ax.text(np.e, len(names) - 0.5, " e", color="green", fontsize=8)
        ax.set_title(f"{label.split('(')[0].strip()}\n=> rung {v.rung}: {v.label}", fontsize=9)
        ax.set_xlabel("characteristic ratio")
        ax.set_xlim(1.8, 4.6)
    fig.suptitle("Discovery engine on known-truth worlds (blue band = pooled 95% CI)", fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS, "engine_calibration.png"), dpi=130)
    plt.close(fig)

    print(json.dumps(summary, indent=2))
    print("\nfigure: results/engine_calibration.png")


if __name__ == "__main__":
    main()
