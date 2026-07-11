"""
Full end-to-end analysis of the fragmentation-collectivization cycle.

  python run.py                 # runs on pre-built case JSONs
  python run.py --build-cases   # rebuilds cases from Maddison/V-Dem first

Outputs -> results/cycle_analysis.json + results/cycle_summary.png
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from collectivization_case import CaseProfile
from cycle_engine import analyze

CASES_DIR = os.path.join(HERE, "cases")
RESULTS = os.path.join(HERE, "results")


def load_cases() -> list[CaseProfile]:
    """Load all case JSONs from cases/."""
    cases = []
    for fname in sorted(os.listdir(CASES_DIR)):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(CASES_DIR, fname)) as f:
            d = json.load(f)
        gdp = {int(y): v for y, v in d.get("gdp_series", {}).items()}
        vdem = {int(y): v for y, v in d.get("vdem_series", {}).items()}
        cases.append(CaseProfile(
            name=d["name"],
            is_control=d["is_control"],
            pre_frag_year=d["pre_frag_year"],
            frag_peak_year=d["frag_peak_year"],
            first_integration_year=d["first_integration_year"],
            post_collect_year=d["post_collect_year"],
            features_pre=d["features_pre"],
            features_post=d["features_post"],
            units_pre=d["units_pre"],
            units_peak=d["units_peak"],
            units_post=d["units_post"],
            pop_pre=d["pop_pre"],
            pop_post=d["pop_post"],
            gdp_growth_pre=d.get("gdp_growth_pre") or float("nan"),
            gdp_growth_post=d.get("gdp_growth_post") or float("nan"),
            frag_duration_years=d["frag_duration_years"],
            conflicts_per_decade=d["conflicts_per_decade"],
            collect_speed_years=d["collect_speed_years"],
            durability_years=d["durability_years"],
            gdp_series=gdp,
            vdem_series=vdem,
            sources=d.get("sources", ""),
            notes=d.get("notes", ""),
        ))
    return cases


def plot_summary(result, cases, path):
    """Two-panel summary figure: form-shift flip counts + ratchet dims."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Panel 1: Form-shift flip counts (cases vs controls)
    core = [(n, s["flip_count"]) for n, s in result.form_shift_result["per_case"].items()
            if not any(c.is_control and c.name == n for c in cases)]
    ctrl = [(n, s["flip_count"]) for n, s in result.form_shift_result["per_case"].items()
            if any(c.is_control and c.name == n for c in cases)]

    all_bars = core + ctrl
    names = [b[0] for b in all_bars]
    vals = [b[1] for b in all_bars]
    colors = ["#3366aa"] * len(core) + ["#aa3333"] * len(ctrl)

    y_pos = range(len(names))
    ax1.barh(y_pos, vals, color=colors)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(names, fontsize=8)
    ax1.set_xlabel("Feature flip count (0-15)")
    ax1.set_title("Form Shift: feature flips (blue=core, red=control)")
    ax1.invert_yaxis()

    # Panel 2: Ratchet positive dimensions
    ratchet_data = result.ratchet_result["per_case"]
    r_names = list(ratchet_data.keys())
    r_vals = [ratchet_data[n]["positive_dims"] for n in r_names]
    ax2.barh(range(len(r_names)), r_vals, color="#3366aa")
    ax2.set_yticks(range(len(r_names)))
    ax2.set_yticklabels(r_names, fontsize=8)
    ax2.set_xlabel("Positive dimensions (of 5)")
    ax2.set_title("Ratchet: dimensions where post > pre")
    ax2.axvline(2.5, ls="--", color="grey", lw=1, label="majority threshold")
    ax2.legend(fontsize=8)
    ax2.invert_yaxis()

    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build-cases", action="store_true",
                        help="rebuild case JSONs from Maddison/V-Dem before analysis")
    args = parser.parse_args()

    if args.build_cases:
        sys.path.insert(0, os.path.join(HERE, "ingest"))
        from ingest.build_cases import build_all
        build_all()

    cases = load_cases()
    if not cases:
        print("no case JSONs found in cases/; run with --build-cases first")
        sys.exit(1)

    print(f"loaded {len(cases)} cases ({sum(1 for c in cases if not c.is_control)} core, "
          f"{sum(1 for c in cases if c.is_control)} controls)")

    result = analyze(cases)

    os.makedirs(RESULTS, exist_ok=True)
    out = {
        "ratchet": result.ratchet_result,
        "form_shift": result.form_shift_result,
        "pathway": result.pathway_result,
        "timing_intensity": result.timing_intensity_result,
        "warning_signals": result.warning_signals_result,
        "summary": result.summary,
    }
    with open(os.path.join(RESULTS, "cycle_analysis.json"), "w") as f:
        json.dump(out, f, indent=2, default=str)

    plot_summary(result, cases, os.path.join(RESULTS, "cycle_summary.png"))

    print("\n" + "=" * 60)
    print("CYCLE ANALYSIS SUMMARY")
    print("=" * 60)
    print(json.dumps(result.summary, indent=2))
    print(f"\nfull results: {RESULTS}/cycle_analysis.json")
    print(f"figure:       {RESULTS}/cycle_summary.png")


if __name__ == "__main__":
    main()
