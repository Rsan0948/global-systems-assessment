"""
One-command driver for Study 2C.

  python run.py             # runs everything: pipeline demo, power study, plots
  python run.py --quick     # smaller reps/grid for a fast smoke run

Outputs land in ./results: JSON tables and PNG figures, all regenerable from
the fixed seeds (per analysis standard §6.7).

With real HydroSHEDS data available, add:
  python run.py --hydrosheds /path/to/HydroRIVERS_v10.gdb
which routes through ingest.load_hydrosheds_reaches instead of the synthetic
coalescent demo. The statistical stages are identical.
"""

from __future__ import annotations

import argparse
import json
import os

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from analysis import CANDIDATES, model_comparison
from power import run_grid, to_json
from synthetic import coalescent_rb_population

RESULTS = os.path.join(os.path.dirname(__file__), "results")


def pipeline_demo(n_basins: int, seed: int = 0) -> dict:
    """Run the full measurement+stats pipeline on neutral coalescent topology.

    This exercises Strahler ordering, Horton estimation, and model comparison
    end-to-end on REAL tree topology. It is a pipeline check, not evidence
    about rivers: the coalescent model has no e built in, so whatever center it
    returns (empirically ~3 for this neutral topology) is a property of random
    binary merging, not support for the theory.
    """
    rb = coalescent_rb_population(n_basins, seed=seed)
    mc = model_comparison(rb, n_boot=400, seed=seed)
    summary = {
        "n_basins": int(rb.size),
        "rb_mean": float(rb.mean()),
        "rb_median": float(np.median(rb)),
        "mode": mc.mode,
        "mode_ci95": list(mc.mode_ci),
        "best_model": mc.best_model,
        "bf_e_vs_3": mc.bf_e_vs_3,
        "bf_e_vs_pi": mc.bf_e_vs_pi,
        "tier": mc.tier,
        "tier_reason": mc.tier_reason,
        "log_marginal_likelihoods": mc.log_ml,
    }
    # figure: Rb histogram with candidate centers marked
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(rb, bins=40, density=True, alpha=0.6, color="#4477aa")
    for name, k in CANDIDATES.items():
        ax.axvline(k, ls="--", lw=1, alpha=0.7)
        ax.text(k, ax.get_ylim()[1] * 0.92, name, ha="center", fontsize=8)
    ax.axvline(mc.mode, color="black", lw=2, label=f"mode={mc.mode:.2f}")
    ax.set_xlabel("Horton bifurcation ratio Rb")
    ax.set_ylabel("density")
    ax.set_title(f"Pipeline demo on random-coalescent basins (n={rb.size})")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS, "pipeline_demo_rb.png"), dpi=130)
    plt.close(fig)
    return summary


def power_study(quick: bool) -> list:
    if quick:
        cells = run_grid(n_values=(100, 1000), log_sds=(0.18,), n_reps=40)
    else:
        cells = run_grid(n_reps=150)
    # figure: P(decisive BF>=10) vs n, for each true center at the middle sd
    fig, ax = plt.subplots(figsize=(7, 4))
    for name in ("e", "3"):
        sd = 0.18
        pts = [(c["n_basins"], c["prob_decisive"]) for c in
               json.loads(to_json(cells)) if c["true_center"] == name and c["log_sd"] == sd]
        pts.sort()
        if pts:
            xs, ys = zip(*pts)
            ax.plot(xs, ys, marker="o", label=f"true center = {name}")
    ax.axhline(0.8, ls=":", color="grey", label="80% power")
    ax.set_xscale("log")
    ax.set_xlabel("number of basins")
    ax.set_ylabel("P(Bayes factor vs nearest rival >= 10)")
    ax.set_title("Power to decisively distinguish e from 3 (log_sd=0.18)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS, "power_curve.png"), dpi=130)
    plt.close(fig)
    return json.loads(to_json(cells))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--hydrosheds", default=None, help="path to HydroSHEDS layer (real data)")
    args = ap.parse_args()
    os.makedirs(RESULTS, exist_ok=True)

    if args.hydrosheds:
        from ingest import load_hydrosheds_reaches, iter_basin_measurements
        basins = load_hydrosheds_reaches(args.hydrosheds)
        rb = np.array([rb for _, rb, _, _ in iter_basin_measurements(basins)])
        mc = model_comparison(rb)
        demo = {"source": "hydrosheds", "n_basins": int(rb.size), "tier": mc.tier,
                "tier_reason": mc.tier_reason, "mode": mc.mode, "mode_ci95": list(mc.mode_ci),
                "best_model": mc.best_model, "bf_e_vs_3": mc.bf_e_vs_3, "bf_e_vs_pi": mc.bf_e_vs_pi}
    else:
        demo = pipeline_demo(n_basins=200 if args.quick else 1500)

    power = power_study(args.quick)

    with open(os.path.join(RESULTS, "pipeline_summary.json"), "w") as f:
        json.dump(demo, f, indent=2)
    with open(os.path.join(RESULTS, "power_grid.json"), "w") as f:
        json.dump(power, f, indent=2)

    print("=== Study 2C ===")
    print(json.dumps(demo, indent=2))
    print(f"\npower grid: {len(power)} cells written to results/power_grid.json")
    print("figures: results/pipeline_demo_rb.png, results/power_curve.png")


if __name__ == "__main__":
    main()
