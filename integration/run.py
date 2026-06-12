"""
Full end-to-end integration across every built node.

  python run.py

Pipeline:
  1. assemble all self-organizing domain nodes -> discovery ladder -> verdict
  2. negative-control contrast (self-organizing vs engineered + classification)
  3. mechanism (rung-4) test applied to the assembled nodes' exponents
  4. predictive calibrations: DGS->instability (2A), corporate survival (2B)
  5. mechanism calibration (gap->factor recovers truth / null)

Everything runs on simulated / literature-summary inputs and proves the
PIPELINE, not the theory. Outputs -> ./results.
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
for sub in ["", "../discovery",
            "../studies/2A_political_fragmentation", "../studies/2B_corporate",
            "../studies/2E_organizations", "../studies/2F_opensource",
            "../studies/3B_mechanism", "../studies/4_negative_controls"]:
    sys.path.insert(0, os.path.join(HERE, sub))

from node_api import assemble                                     # noqa: E402
from ladder import assess                                         # noqa: E402
from dgs import fit_dgs                                           # noqa: E402
from panel import make_panel                                     # noqa: E402
from survival import fit_hazard, make_firm_panel                 # noqa: E402
from mechanism import gap_predicts_factor                        # noqa: E402
import importlib.util                                             # noqa: E402

RESULTS = os.path.join(HERE, "results")


def _load(modpath, name):
    spec = importlib.util.spec_from_file_location(name, modpath)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m            # required so @dataclass introspection resolves
    spec.loader.exec_module(m)
    return m


def all_self_org_nodes():
    rivers = _load(os.path.join(HERE, "../studies/2C_river_networks/river_node.py"), "river2c")
    neuro = _load(os.path.join(HERE, "../studies/2D_biological_branching/neuro_node.py"), "neuro2d")
    nodes = [rivers.build_node()]                                # REAL rivers (HydroRIVERS NA)
    nodes += neuro.build_nodes()                                 # REAL biology (NeuroMorpho arbors)
    corporate = _load(os.path.join(HERE, "../studies/2B_corporate/corporate_node.py"), "corp2b")
    organizations = _load(os.path.join(HERE, "../studies/2E_organizations/org_node.py"), "org2e")
    opensource = _load(os.path.join(HERE, "../studies/2F_opensource/oss_node.py"), "oss2f")
    nodes += [corporate.build_node(), organizations.build_node(), opensource.build_node()]
    return nodes


def control_nodes():
    nc = _load(os.path.join(HERE, "../studies/4_negative_controls/nodes.py"), "nc4")
    return [nc.engineered_node(), nc.classification_node()]


def ladder_block(nodes):
    data, nulls = assemble(nodes)                                 # self-org only
    v = assess(data, null_samplers=nulls, n_sims=400, seed=7)
    return {
        "rung": v.rung, "label": v.label, "reason": v.reason,
        "pooled_ratio": round(v.het.pooled_ratio, 4),
        "pooled_ci": [round(x, 4) for x in v.het.pooled_ci],
        "i_squared": round(v.het.i_squared, 3), "q_p": round(v.het.q_p, 4),
        "constants_in_ci": v.constants_in_ci,
        "per_domain": {e.name: round(e.ratio_mean, 3) for e in v.het.domains},
    }, v


def negative_control_block(self_org, controls):
    nc = _load(os.path.join(HERE, "../studies/4_negative_controls/controls_analysis.py"), "nca4")
    r = nc.dispersion_contrast(self_org, controls)
    return {
        "self_org_mean_cv": round(r.self_org_cv, 3),
        "control_mean_cv": round(r.control_cv, 3),
        "brown_forsythe_p": r.brown_forsythe_p,
        "controls_disperse_more": r.controls_disperse_more,
        "per_node_cv": {k: round(v, 3) for k, v in r.per_node_cv.items()},
    }


def mechanism_on_assembled(nodes):
    with_exp = [n for n in nodes if n.gap is not None]
    gaps = np.array([n.gap for n in with_exp])
    log_factors = np.array([np.log(np.exp(np.log(n.ratios).mean())) for n in with_exp])
    if gaps.std(ddof=1) < 0.05:
        return {"status": "insufficient exponent variation",
                "note": "illustrative placeholder exponents are ~constant (gap~1); "
                        "the cross-domain gap->factor test needs REAL exponent estimates "
                        "(Study 3B estimator on raw allometry) to run meaningfully.",
                "n_domains_with_exponents": int(gaps.size)}
    r = gap_predicts_factor(gaps, log_factors)
    return {"slope": round(r.slope, 3), "slope_ci": [round(x, 3) for x in r.slope_ci],
            "slope_p": r.slope_p, "gap_consistent_with_1": r.gap_consistent_with_1}


def predictive_calibrations():
    dgs = {}
    for label, beta in [("true_effect", 0.6), ("null_effect", 0.0)]:
        res = fit_dgs(make_panel(beta_dgs_true=beta, seed=4))
        dgs[label] = {"beta_dgs": round(res.beta_dgs, 3), "lr_p": res.lr_p,
                      "auc_gain": round(res.auc_gain, 3)}
    surv = {}
    for label, beta in [("true_effect", 0.5), ("null_effect", 0.0)]:
        res = fit_hazard(make_firm_panel(beta_true=beta, seed=4))
        surv[label] = {"hazard_ratio": round(res.hazard_ratio, 3), "lr_p": res.lr_p}
    mech = {}
    rng = np.random.default_rng(5)
    for label, slope_true in [("gap_predicts", 0.5), ("no_link", 0.0)]:
        g = rng.uniform(0.6, 1.4, size=12)
        lf = 1.0 + slope_true * (g - 1.0) + rng.normal(0, 0.05, size=12)
        r = gap_predicts_factor(g, lf)
        mech[label] = {"slope_ci": [round(x, 3) for x in r.slope_ci], "slope_p": r.slope_p}
    return {"dgs_instability": dgs, "corporate_survival": surv, "mechanism_gap_factor": mech}


def main():
    os.makedirs(RESULTS, exist_ok=True)
    self_org = all_self_org_nodes()
    controls = control_nodes()

    ladder_summary, v = ladder_block(self_org)
    summary = {
        "ladder_on_self_organizing_nodes": ladder_summary,
        "negative_controls": negative_control_block(self_org, controls),
        "mechanism_on_assembled_nodes": mechanism_on_assembled(self_org),
        "predictive_calibrations": predictive_calibrations(),
        "note": "MIXED inputs: rivers = REAL (HydroRIVERS NA, discovery continent); "
                "all other domains still simulated / literature-summary placeholders. "
                "Not yet a cross-domain finding about real systems. Sealed holdout "
                "(corporate, open-source, rivers cross-continent) untouched.",
    }
    with open(os.path.join(RESULTS, "integration_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    # forest plot: self-org domains + control dispersion
    fig, ax = plt.subplots(figsize=(8, 5))
    names = [e.name for e in v.het.domains]
    vals = [e.ratio_mean for e in v.het.domains]
    ax.scatter(vals, range(len(names)), color="#333", zorder=3, label="self-organizing")
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names)
    ax.axvspan(v.het.pooled_ci[0], v.het.pooled_ci[1], color="#88aacc", alpha=0.4, label="pooled 95% CI")
    ax.axvline(np.e, ls="--", color="green", lw=1, label="e")
    ax.axvline(3.0, ls=":", color="grey", lw=1, label="3")
    ax.set_xscale("log")
    ax.set_xlabel("characteristic subdivision factor (log scale)")
    ax.set_title(f"Self-organizing domains => rung {v.rung}: {v.label}")
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS, "integration_forest.png"), dpi=130)
    plt.close(fig)

    print(json.dumps(summary, indent=2))
    print("\nfigure: results/integration_forest.png")


if __name__ == "__main__":
    main()
