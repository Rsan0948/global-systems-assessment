"""
Pre-registered calibration / power analysis for Study 2C (runnable with NO
real data). It answers the question the whole project hinges on:

   Can the model-comparison procedure actually distinguish a true-e world
   from a true-3 world, and how many basins does that take?

Method: simulate populations of per-basin Rb with a KNOWN true center
(`synthetic.sample_basin_rbs`), run `analysis.model_comparison`, and record
(a) whether the correct point model is selected, (b) the Bayes factor against
the nearest rival, across sample sizes and dispersions. If the procedure
cannot separate e from 3 at achievable n, that is a pre-registered limitation
of the test itself and is reported as such — not hidden.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

import numpy as np

from analysis import model_comparison, _safe_bf
from synthetic import sample_basin_rbs


@dataclass
class PowerCell:
    true_center: str
    n_basins: int
    log_sd: float
    n_reps: int
    prob_correct_best: float          # P(correct point model is the best point model)
    prob_decisive: float              # P(BF vs nearest rival >= 10 in the right direction)
    median_bf_truth_vs_rival: float   # median BF(true center vs nearest competing integer)


_RIVALS = {"e": "3", "3": "e"}        # nearest competitor we must beat


def run_power_cell(
    true_name: str,
    true_center: float,
    n_basins: int,
    log_sd: float,
    n_reps: int = 200,
    base_seed: int = 1000,
) -> PowerCell:
    rival = _RIVALS[true_name]
    correct, decisive, bfs = 0, 0, []
    point_names = ["e", "3", "pi", "2", "4"]
    for r in range(n_reps):
        rb = sample_basin_rbs(n_basins, center=true_center, log_sd=log_sd, seed=base_seed + r)
        # n_boot=1: the KDE bootstrap CI is irrelevant to the power study, which
        # only needs the marginal-likelihood model selection, so keep it minimal.
        mc = model_comparison(rb, n_boot=1, seed=base_seed + r)
        best_point = max(point_names, key=lambda nm: mc.log_ml[nm])
        if best_point == true_name:
            correct += 1
        bf = _safe_bf(mc.log_ml[true_name], mc.log_ml[rival])
        bfs.append(bf)
        if bf >= 10:
            decisive += 1
    return PowerCell(
        true_center=true_name,
        n_basins=n_basins,
        log_sd=log_sd,
        n_reps=n_reps,
        prob_correct_best=correct / n_reps,
        prob_decisive=decisive / n_reps,
        median_bf_truth_vs_rival=float(np.median(bfs)),
    )


def run_grid(
    n_values=(100, 300, 1000, 3000, 10000),
    log_sds=(0.12, 0.18, 0.25),
    centers=(("e", np.e), ("3", 3.0)),
    n_reps: int = 150,
) -> list[PowerCell]:
    cells: list[PowerCell] = []
    for name, c in centers:
        for sd in log_sds:
            for n in n_values:
                cells.append(run_power_cell(name, c, n, sd, n_reps=n_reps))
    return cells


def to_json(cells: list[PowerCell]) -> str:
    return json.dumps([asdict(c) for c in cells], indent=2)
