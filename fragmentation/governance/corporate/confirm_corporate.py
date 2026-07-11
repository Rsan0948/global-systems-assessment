"""
Corporate CROSS-DOMAIN CONFIRMATION (Study 2B) -- prediction B.

Discovery froze a rung-1 claim on rivers + biology (+ controls, DGS), with a
sealed CROSS-DOMAIN holdout (FROZEN_DISCOVERY_CLAIM.md, prediction B). The
registered holdout was corporate (2B) + open-source (2F); 2F is DESCOPED (its
GitHub real ingest is deferred), so this runs B on corporate as the SOLE
cross-domain holdout -- a weaker but valid cross-domain test (logged as a
pre-registration amendment in results/SEALED_HOLDOUT_CORPORATE.md).

Run ONLY after the freeze, ONCE. With corporate now on real SEC EDGAR data:

    python confirm_corporate.py        # requires results/corporate_splits_edgar.json

Prediction B (FROZEN_DISCOVERY_CLAIM.md):
  B1. Corporate is individually a definable distribution, NOT pure null
      (it differs from its mechanism-free binary-default null).
  B2. Adding corporate does NOT collapse the verdict to a single universal
      constant -- I^2 stays high / the pooled CI still excludes a single named
      constant (consistent with rung 1, not rung 2/3).
"""

from __future__ import annotations

import importlib.util
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
for sub in ["discovery", "integration"]:
    sys.path.insert(0, os.path.join(ROOT, sub))

from heterogeneity import analyze                                  # noqa: E402
from trivial_null import compare                                   # noqa: E402
from ladder import assess, confirm, CONSTANTS                      # noqa: E402

# Frozen discovery reference (FROZEN_DISCOVERY_CLAIM.md, claim 1)
FROZEN_POOLED_CI = (2.97, 3.37)
FROZEN_RUNG = 1
E = math.e


def _load(modpath, name):
    spec = importlib.util.spec_from_file_location(name, modpath)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


def _real_discovery_nodes():
    """The REAL frozen-dataset ratio domains: rivers (NA) + biology (NeuroMorpho)."""
    rivers = _load(os.path.join(ROOT, "natural-systems/rivers/river_node.py"), "river2c")
    neuro = _load(os.path.join(ROOT, "natural-systems/biology/neuro_node.py"), "neuro2d")
    return [rivers.build_node()] + neuro.build_nodes()


def _corporate_node():
    corp = _load(os.path.join(HERE, "corporate_node.py"), "corp2b")
    return corp.build_node()


def confirm_B(seed: int = 99) -> dict:
    disc_nodes = _real_discovery_nodes()
    corp = _corporate_node()

    disc_data = {n.name: n.ratios for n in disc_nodes}
    disc_nulls = {n.name: n.null_sampler for n in disc_nodes}
    disc_v = assess(disc_data, null_samplers=disc_nulls, n_sims=500, seed=seed)

    # ---- B1: corporate definable distribution, differs from its binary null ----
    corp_ratios = np.asarray(corp.ratios, dtype=float)
    corp_g = float(np.exp(np.log(corp_ratios).mean()))
    corp_cv = float(corp_ratios.std(ddof=1) / corp_ratios.mean())
    definable = corp_ratios.size >= 20 and np.isfinite(corp_g) and corp_cv < 1.0
    triv = compare(analyze({"corporate": corp_ratios}),
                   {"corporate": corp.null_sampler}, n_sims=2000, seed=seed)
    corp_z = float(triv.per_domain_z["corporate"])
    disp_p = float(triv.pooled_displacement_p)
    not_pure_null = abs(corp_z) > 2.0 or disp_p < 0.05
    b1 = bool(definable and not_pure_null)

    # ---- B2: adding corporate keeps rung 1 (does NOT isolate one constant) ----
    full_data = {**disc_data, "corporate": corp_ratios}
    full_nulls = {**disc_nulls, "corporate": corp.null_sampler}
    full_v = assess(full_data, null_samplers=full_nulls, n_sims=500, seed=seed)
    principled = [c for c in full_v.constants_in_ci if c not in ("2", "4")]
    collapsed_to_constant = full_v.rung >= 2 and len(principled) == 1
    b2 = bool(full_v.rung <= 1 and not collapsed_to_constant)

    # ---- formal ladder.confirm record (CI overlap of holdout vs discovery) ----
    conf = confirm(disc_v, {"corporate": corp_ratios},
                   null_samplers={"corporate": corp.null_sampler}, n_sims=500, seed=seed)

    return {
        "discovery_rung": disc_v.rung,
        "discovery_pooled": round(disc_v.het.pooled_ratio, 3),
        "discovery_pooled_ci": [round(x, 3) for x in disc_v.het.pooled_ci],
        "frozen_reference_ci": list(FROZEN_POOLED_CI),
        "corporate_n_events": int(corp_ratios.size),
        "corporate_geom_factor": round(corp_g, 3),
        "corporate_cv": round(corp_cv, 3),
        "corporate_vs_null_z": round(corp_z, 3),
        "corporate_displacement_p": round(disp_p, 4),
        "B1_definable": bool(definable),
        "B1_not_pure_null": bool(not_pure_null),
        "B1_pass": b1,
        "full_set_rung": full_v.rung,
        "full_set_i_squared": round(full_v.het.i_squared, 3),
        "full_set_pooled_ci": [round(x, 3) for x in full_v.het.pooled_ci],
        "full_set_constants_in_ci": full_v.constants_in_ci,
        "B2_keeps_rung1_no_constant": b2,
        "B2_pass": b2,
        "ci_overlap_holdout_vs_discovery": conf["ci_overlap"],
        "CONFIRMED": bool(b1 and b2),
    }


if __name__ == "__main__":
    r = confirm_B()
    print(json.dumps(r, indent=2))
    print("\nPREDICTION B (corporate-only cross-domain holdout):")
    print("  B1 (definable, not pure null):", "PASS" if r["B1_pass"] else "FAIL")
    print("  B2 (no collapse to a constant):", "PASS" if r["B2_pass"] else "FAIL")
    print("  => B", "CONFIRMED" if r["CONFIRMED"] else "NOT fully confirmed (reported honestly)")
