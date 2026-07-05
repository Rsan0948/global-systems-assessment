"""
Bridge runner: end-to-end analysis connecting collectivization feature vectors
to MI pillar space.

  python run.py              # full analysis with visualization
  python run.py --validate   # validation against MI reference scores only

Outputs -> results/bridge_analysis.json + results/bridge_*.png
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

from pillar_loading import (
    project_normalized, displacement, displacement_magnitude,
    profile_shape, project_type, PILLAR_NAMES, PILLAR_LABELS,
    TYPE_TEMPLATES, LOADING_MATRIX, FEATURE_NAMES,
)
from failure_bridge import (
    failure_bridge_diagnostic, active_failures, expected_safeguards,
    expected_weak_pillars, FAILURE_SAFEGUARD_MAP,
)
from organicity import organicity_diagnostic
from trajectory import (
    trajectory_profile, pathway_displacement_signature, trajectory_table,
)
from validate import validate_all, interpret_residuals

CASES_DIR = os.path.join(HERE, "..", "studies", "5_collectivization", "cases")
RESULTS = os.path.join(HERE, "results")


def load_cases() -> list[dict]:
    """Load all case JSONs from the collectivization study."""
    cases = []
    for fname in sorted(os.listdir(CASES_DIR)):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(CASES_DIR, fname)) as f:
            d = json.load(f)
        cases.append(d)
    return cases


# --- Pathway classification (mirrored from pathway_analysis.py) ---

def _integration_depth(features: list[int]) -> int:
    return sum(features[i] for i in [4, 5, 7, 10, 11, 12])


def _hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


def _classify_pathway(case: dict) -> str:
    id_pre = _integration_depth(case["features_pre"])
    flips = _hamming(case["features_pre"], case["features_post"])
    speed = case["collect_speed_years"]
    if id_pre < 5:
        return "construction"
    elif flips <= 1:
        return "restoration"
    elif speed > 150:
        return "negotiation"
    else:
        return "redesign"


# --- Visualization ---

def plot_type_profiles(path: str):
    """Radar-style bar chart showing predicted pillar profiles for each
    governance type template."""
    types = sorted(TYPE_TEMPLATES.keys())
    profiles = {t: project_type(t) for t in types}

    fig, axes = plt.subplots(2, 5, figsize=(18, 7), sharey=True)
    axes = axes.flatten()

    colors = {"P1": "#2166ac", "P2": "#4393c3", "P3": "#92c5de",
              "P4": "#d6604d", "P5": "#b2182b"}

    for ax, tname in zip(axes, types):
        vals = [profiles[tname][p] for p in PILLAR_NAMES]
        bars = ax.bar(PILLAR_NAMES, vals,
                      color=[colors[p] for p in PILLAR_NAMES])
        ax.set_ylim(0, 1.05)
        ax.set_title(tname.replace("_", "\n"), fontsize=8, fontweight="bold")
        ax.tick_params(labelsize=7)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, v + 0.02,
                    f"{v:.2f}", ha="center", fontsize=6)

    fig.suptitle("Predicted MI Pillar Profiles by Governance Type",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_validation(validation: dict, path: str):
    """Scatter plot: predicted vs actual MI pillar scores."""
    fig, axes = plt.subplots(1, 5, figsize=(18, 4), sharey=True)
    colors = {"P1": "#2166ac", "P2": "#4393c3", "P3": "#92c5de",
              "P4": "#d6604d", "P5": "#b2182b"}

    countries = sorted(validation["per_country"].keys())

    for ax, p in zip(axes, PILLAR_NAMES):
        pred = [validation["per_country"][c]["predicted"][p] for c in countries]
        act = [validation["per_country"][c]["actual"][p] for c in countries]
        ax.scatter(pred, act, color=colors[p], s=50, alpha=0.8, edgecolors="k",
                   linewidths=0.5)
        for i, c in enumerate(countries):
            ax.annotate(c[:3], (pred[i], act[i]), fontsize=5,
                        textcoords="offset points", xytext=(3, 3))

        ax.plot([0, 1], [0, 1], "k--", lw=0.8, alpha=0.5)
        ax.set_xlim(0, 1.05)
        ax.set_ylim(0, 1.05)
        ax.set_xlabel("Predicted", fontsize=9)
        if p == "P1":
            ax.set_ylabel("Actual MI Score", fontsize=9)
        corr = validation["aggregate"]["per_pillar_correlation"][p]
        ax.set_title(f"{p} (r={corr:.3f})", fontsize=10, fontweight="bold")
        ax.set_aspect("equal")
        ax.tick_params(labelsize=7)

    fig.suptitle("Structural Prediction vs Actual MI Scores (2024)",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_trajectories(trajectories: list, path: str):
    """Arrow plot showing displacement vectors in pillar space for each case,
    colored by pathway type."""
    pw_colors = {
        "construction": "#2166ac",
        "restoration": "#4dac26",
        "negotiation": "#b2abd2",
        "redesign": "#d6604d",
    }

    fig, axes = plt.subplots(1, 5, figsize=(18, 5), sharey=True)

    for ax, p in zip(axes, PILLAR_NAMES):
        for i, t in enumerate(trajectories):
            color = pw_colors.get(t.pathway, "#999999")
            pre_val = t.pre_profile[p]
            post_val = t.post_profile[p]
            ax.arrow(i, pre_val, 0, post_val - pre_val,
                     head_width=0.3, head_length=0.015,
                     fc=color, ec=color, alpha=0.7, length_includes_head=True)
            ax.plot(i, pre_val, "o", color=color, markersize=3, alpha=0.5)

        ax.set_ylim(-0.05, 1.1)
        ax.set_title(f"{p}", fontsize=10, fontweight="bold")
        ax.set_xticks(range(len(trajectories)))
        ax.set_xticklabels([t.name[:6] for t in trajectories],
                           rotation=90, fontsize=5)
        if p == "P1":
            ax.set_ylabel("Normalized pillar score", fontsize=9)

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=c, label=pw)
                       for pw, c in pw_colors.items()]
    axes[-1].legend(handles=legend_elements, fontsize=7, loc="lower right")

    fig.suptitle("Institutional Displacement Vectors in MI Pillar Space",
                 fontsize=12, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_organicity_vs_magnitude(trajectories: list, path: str):
    """Scatter: organicity vs displacement magnitude, colored by pathway."""
    pw_colors = {
        "construction": "#2166ac",
        "restoration": "#4dac26",
        "negotiation": "#b2abd2",
        "redesign": "#d6604d",
    }
    fig, ax = plt.subplots(figsize=(8, 6))
    for t in trajectories:
        color = pw_colors.get(t.pathway, "#999999")
        ax.scatter(t.organicity, t.magnitude, color=color, s=60,
                   edgecolors="k", linewidths=0.5, alpha=0.8)
        ax.annotate(t.name[:8], (t.organicity, t.magnitude), fontsize=6,
                    textcoords="offset points", xytext=(4, 4))

    ax.set_xlabel("Organicity (fraction inherited)", fontsize=10)
    ax.set_ylabel("Displacement magnitude in pillar space", fontsize=10)
    ax.set_title("Organicity vs Institutional Displacement", fontsize=12,
                 fontweight="bold")
    ax.set_xlim(-0.05, 1.1)

    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=c, label=pw)
                       for pw, c in pw_colors.items()]
    ax.legend(handles=legend_elements, fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_residual_heatmap(validation: dict, path: str):
    """Heatmap of residuals (actual - predicted) per country per pillar."""
    countries = sorted(validation["per_country"].keys())
    matrix = np.array([
        [validation["per_country"][c]["residuals"][p] for p in PILLAR_NAMES]
        for c in countries
    ])

    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(matrix, cmap="RdBu_r", vmin=-0.5, vmax=0.5, aspect="auto")
    ax.set_xticks(range(len(PILLAR_NAMES)))
    ax.set_xticklabels(PILLAR_NAMES, fontsize=9)
    ax.set_yticks(range(len(countries)))
    ax.set_yticklabels(countries, fontsize=8)

    for i in range(len(countries)):
        for j in range(len(PILLAR_NAMES)):
            val = matrix[i, j]
            color = "white" if abs(val) > 0.25 else "black"
            ax.text(j, i, f"{val:+.2f}", ha="center", va="center",
                    fontsize=7, color=color)

    ax.set_title("Residuals: Actual MI − Predicted from Structure\n"
                 "(blue = underpredicted, red = overpredicted)",
                 fontsize=11, fontweight="bold")
    fig.colorbar(im, ax=ax, shrink=0.8, label="Residual")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


# --- Main ---

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true",
                        help="run validation against MI scores only")
    args = parser.parse_args()

    os.makedirs(RESULTS, exist_ok=True)

    # 1. Validation against MI reference scores
    print("=" * 60)
    print("BRIDGE VALIDATION: Feature Vectors → MI Pillar Space")
    print("=" * 60)

    validation = validate_all()
    agg = validation["aggregate"]
    cross = agg["cross_type"]
    print(f"\nCountries validated: {agg['n_countries']}")
    print(f"Unique structural types: {cross['n_unique_types']}")
    print(f"\n--- Absolute level (form predicts capacity?) ---")
    print(f"Overall Pearson:      r = {agg['overall_correlation']:+.4f}")
    print(f"RMSE:                 {agg['rmse']:.4f}")
    print(f"MAE:                  {agg['mae']:.4f}")
    print(f"\n--- Shape prediction (form predicts WHICH pillars are strong?) ---")
    print(f"Median per-country Spearman:  {agg['median_shape_correlation']:+.4f}")
    print(f"Mean per-country Spearman:    {agg['mean_shape_correlation']:+.4f}")
    print(f"Countries with valid shape:   {agg['n_shape_valid']}")
    print(f"\n--- Cross-type ordering (different structures → different scores?) ---")
    print(f"Cross-type Pearson:    r = {cross['cross_type_correlation_pearson']:+.4f}")
    print(f"Cross-type Spearman:   r = {cross['cross_type_correlation_spearman']:+.4f}")
    print(f"\nPer-pillar detail:")
    for p in PILLAR_NAMES:
        corr = agg['per_pillar_correlation'][p]
        bias = agg['per_pillar_bias'][p]
        print(f"  {p} ({PILLAR_LABELS[p]:<25s}):  r = {corr:+.4f},  "
              f"bias = {bias:+.4f}")

    # Within-type spread (form ≠ capacity diagnostic)
    within = cross.get("within_type", {})
    if within:
        print(f"\nWithin-type spread (same structure, different capacity):")
        for label, data in within.items():
            print(f"  {label} (n={data['n']}): "
                  f"mean actual σ = {data['mean_actual_std']:.4f}")

    # Capacity realization
    print(f"\nCapacity realization (actual/predicted):")
    for country in sorted(validation["per_country"]):
        r = validation["per_country"][country]["mean_realization"]
        print(f"  {country:<15s}: {r:.2f}")

    interpretations = interpret_residuals(validation)
    print(f"\nResidual interpretations (|r| > 0.10):")
    for country, findings in sorted(interpretations.items()):
        if findings != ["within prediction bounds"]:
            print(f"  {country}:")
            for f in findings:
                print(f"    {f}")

    plot_validation(validation, os.path.join(RESULTS, "bridge_validation.png"))
    plot_residual_heatmap(validation,
                          os.path.join(RESULTS, "bridge_residuals.png"))

    if args.validate:
        with open(os.path.join(RESULTS, "bridge_validation.json"), "w") as f:
            json.dump(validation, f, indent=2, default=str)
        print(f"\nResults: {RESULTS}/bridge_validation.json")
        return

    # 2. Type profiles
    print(f"\n{'=' * 60}")
    print("GOVERNANCE TYPE PROFILES IN PILLAR SPACE")
    print("=" * 60)

    for tname in sorted(TYPE_TEMPLATES.keys()):
        profile = project_type(tname)
        shape = profile_shape(TYPE_TEMPLATES[tname])
        print(f"\n  {tname}:")
        for p in PILLAR_NAMES:
            print(f"    {p}: {profile[p]:.3f} [{shape[p]}]")

    plot_type_profiles(os.path.join(RESULTS, "bridge_type_profiles.png"))

    # 3. Load collectivization cases and compute trajectories
    print(f"\n{'=' * 60}")
    print("CYCLE TRAJECTORIES IN PILLAR SPACE")
    print("=" * 60)

    cases = load_cases()
    core_cases = [c for c in cases if not c["is_control"]]

    trajectories = []
    for case in core_cases:
        pw = _classify_pathway(case)
        t = trajectory_profile(
            case["name"], case["features_pre"], case["features_post"], pw)
        trajectories.append(t)

    trajectories.sort(key=lambda t: (t.pathway, t.name))

    print(f"\n{'Name':<25s} {'Pathway':<14s} {'Org':>5s} {'Mag':>5s} "
          f"{'Dominant':>10s}")
    print("-" * 65)
    for t in trajectories:
        print(f"  {t.name:<23s} {t.pathway:<14s} {t.organicity:>5.2f} "
              f"{t.magnitude:>5.3f} {t.dominant_shift:>10s}")

    # Pathway signatures
    signatures = pathway_displacement_signature(trajectories)
    print(f"\nPathway displacement signatures (mean across cases):")
    for pw, sig in sorted(signatures.items()):
        disp_str = "  ".join(f"{p}:{sig['mean_displacement'][p]:+.3f}"
                             for p in PILLAR_NAMES)
        print(f"  {pw} (n={sig['n']}): mag={sig['mean_magnitude']:.3f}  "
              f"org={sig['mean_organicity']:.2f}")
        print(f"    {disp_str}")

    plot_trajectories(trajectories,
                      os.path.join(RESULTS, "bridge_trajectories.png"))
    plot_organicity_vs_magnitude(
        trajectories, os.path.join(RESULTS, "bridge_organicity.png"))

    # 4. Failure-safeguard bridge
    print(f"\n{'=' * 60}")
    print("FAILURE MODE → SAFEGUARD BRIDGE")
    print("=" * 60)

    bridge_results = {}
    for case in core_cases:
        diag = failure_bridge_diagnostic(
            case["features_pre"], case["features_post"])
        bridge_results[case["name"]] = diag
        if diag["patched"] or diag["new_vulnerabilities"]:
            print(f"\n  {case['name']}:")
            if diag["patched"]:
                print(f"    Patched: {', '.join(diag['patched'])}")
                print(f"    Safeguards resolved: "
                      f"{', '.join(diag['safeguards_resolved']) or 'none'}")
            if diag["new_vulnerabilities"]:
                print(f"    New vulnerabilities: "
                      f"{', '.join(diag['new_vulnerabilities'])}")
                print(f"    Safeguards introduced: "
                      f"{', '.join(diag['safeguards_introduced']) or 'none'}")

    # 5. Organicity analysis
    print(f"\n{'=' * 60}")
    print("ORGANICITY ANALYSIS")
    print("=" * 60)

    org_results = {}
    for case in core_cases:
        od = organicity_diagnostic(
            case["features_pre"], case["features_post"], FEATURE_NAMES)
        org_results[case["name"]] = od

    # Sort by organicity
    sorted_orgs = sorted(org_results.items(), key=lambda x: x[1]["organicity"])
    print(f"\n{'Name':<25s} {'Org':>5s} {'Imposed':>7s} {'Expected CV':>11s} "
          f"{'Predictability':<15s}")
    print("-" * 68)
    for name, od in sorted_orgs:
        print(f"  {name:<23s} {od['organicity']:>5.2f} "
              f"{od['imposed_count']:>4d}/15 "
              f"{od['expected_fragmentation_cv']:>9.3f}   "
              f"{od['fragmentation_predictability']}")

    # 6. Assemble full results
    full_results = {
        "validation": validation,
        "type_profiles": {t: project_type(t) for t in sorted(TYPE_TEMPLATES)},
        "trajectories": trajectory_table(trajectories),
        "pathway_signatures": signatures,
        "failure_bridge": bridge_results,
        "organicity": org_results,
        "loading_matrix": {
            "features": FEATURE_NAMES,
            "pillars": list(PILLAR_NAMES),
            "values": LOADING_MATRIX.tolist(),
        },
    }

    with open(os.path.join(RESULTS, "bridge_analysis.json"), "w") as f:
        json.dump(full_results, f, indent=2, default=str)

    print(f"\n{'=' * 60}")
    print("BRIDGE SUMMARY")
    print("=" * 60)
    print(f"  Shape prediction (median Spearman): "
          f"{agg['median_shape_correlation']:+.4f}")
    print(f"  Cross-type correlation (Pearson):    "
          f"{cross['cross_type_correlation_pearson']:+.4f}")
    print(f"  Validation RMSE:     {agg['rmse']:.4f}")
    print(f"  Core cases analyzed: {len(core_cases)}")
    pw_summary = ", ".join(f"{k}={v['n']}" for k, v in sorted(signatures.items()))
    print(f"  Pathway types:       {pw_summary}")
    mean_org = np.mean([od["organicity"] for od in org_results.values()])
    print(f"  Mean organicity:     {mean_org:.3f}")
    print(f"\n  Full results: {RESULTS}/bridge_analysis.json")
    print(f"  Figures:       {RESULTS}/bridge_*.png")


if __name__ == "__main__":
    main()
