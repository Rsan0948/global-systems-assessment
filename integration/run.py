"""
End-to-end integration: assemble domain nodes -> discovery ladder -> verdict,
plus the two mechanism/calibration tests (DGS->instability, gap->factor).

  python run.py

Writes results to ./results. Everything here runs on simulated / literature-
summary inputs and proves the PIPELINE, not the theory.
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "discovery"))
sys.path.insert(0, os.path.join(HERE, "..", "studies", "2A_political_fragmentation"))
sys.path.insert(0, os.path.join(HERE, "..", "studies", "3B_mechanism"))

from node_api import assemble                       # noqa: E402
from nodes_literature import literature_nodes        # noqa: E402
from ladder import assess                            # noqa: E402
from dgs import fit_dgs                               # noqa: E402
from panel import make_panel                         # noqa: E402
from mechanism import gap_predicts_factor            # noqa: E402

RESULTS = os.path.join(HERE, "results")


def ladder_run() -> dict:
    nodes = literature_nodes(seed=0)
    data, nulls = assemble(nodes)
    v = assess(data, null_samplers=nulls, n_sims=400, seed=7)
    return {
        "rung": v.rung, "label": v.label, "reason": v.reason,
        "pooled_ratio": round(v.het.pooled_ratio, 4),
        "pooled_ci": [round(x, 4) for x in v.het.pooled_ci],
        "i_squared": round(v.het.i_squared, 3), "q_p": round(v.het.q_p, 4),
        "constants_in_ci": v.constants_in_ci,
        "per_domain": {e.name: round(e.ratio_mean, 3) for e in v.het.domains},
    }, v, nodes


def dgs_calibration() -> dict:
    out = {}
    for label, beta in [("true_effect", 0.6), ("null_effect", 0.0)]:
        res = fit_dgs(make_panel(beta_dgs_true=beta, seed=4))
        out[label] = {
            "beta_dgs": round(res.beta_dgs, 3), "lr_stat": round(res.lr_stat, 2),
            "lr_p": res.lr_p, "auc_full": round(res.auc_full, 3),
            "auc_reduced": round(res.auc_reduced, 3), "auc_gain": round(res.auc_gain, 3),
        }
    return out


def mechanism_calibration() -> dict:
    """Show the gap->factor test recovers a true link and is null without one."""
    rng = np.random.default_rng(5)
    out = {}
    for label, slope_true in [("gap_predicts", 0.5), ("no_link", 0.0)]:
        gaps = rng.uniform(0.6, 1.4, size=12)
        log_factors = 1.0 + slope_true * (gaps - 1.0) + rng.normal(0, 0.05, size=12)
        r = gap_predicts_factor(gaps, log_factors)
        out[label] = {
            "slope": round(r.slope, 3), "slope_ci": [round(x, 3) for x in r.slope_ci],
            "slope_p": r.slope_p, "r_squared": round(r.r_squared, 3),
            "gap_mean_ci": [round(x, 3) for x in r.gap_mean_ci],
            "gap_consistent_with_1": r.gap_consistent_with_1,
        }
    return out


def main() -> None:
    os.makedirs(RESULTS, exist_ok=True)
    ladder_summary, v, nodes = ladder_run()
    dgs = dgs_calibration()
    mech = mechanism_calibration()

    summary = {
        "ladder_on_literature_nodes": ladder_summary,
        "dgs_instability_calibration": dgs,
        "mechanism_gap_factor_calibration": mech,
        "note": "Simulated / literature-summary inputs. Proves the pipeline, not the theory.",
    }
    with open(os.path.join(RESULTS, "integration_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    # forest plot of the assembled domains
    fig, ax = plt.subplots(figsize=(7, 4))
    names = [e.name for e in v.het.domains]
    vals = [e.ratio_mean for e in v.het.domains]
    ax.scatter(vals, range(len(names)), color="#333", zorder=3)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names)
    ax.axvspan(v.het.pooled_ci[0], v.het.pooled_ci[1], color="#88aacc", alpha=0.4,
               label="pooled 95% CI")
    ax.axvline(np.e, ls="--", color="green", lw=1, label="e")
    ax.axvline(3.0, ls=":", color="grey", lw=1, label="3")
    ax.set_xlabel("characteristic branching ratio")
    ax.set_title(f"Assembled domains => rung {v.rung}: {v.label}")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS, "integration_forest.png"), dpi=130)
    plt.close(fig)

    print(json.dumps(summary, indent=2))
    print("\nfigure: results/integration_forest.png")


if __name__ == "__main__":
    main()
