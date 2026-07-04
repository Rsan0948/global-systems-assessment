"""
The cycle engine: ties the three hypotheses together and produces cross-case
analysis.

Consumes CaseProfile objects, runs ratchet / form-shift / timing-intensity /
warning-signal analyses, and outputs a unified result.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats

from collectivization_case import CaseProfile
import ratchet
import form_shift
import warning_signals


@dataclass
class TimingIntensityResult:
    spearman_matrix: dict[str, dict]
    dominant_channel: str


def _spearman(x, y):
    """Spearman rank correlation with p-value. Returns (rho, p)."""
    x, y = np.array(x, dtype=float), np.array(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask], y[mask]
    if len(x) < 3:
        return float("nan"), float("nan")
    rho, p = stats.spearmanr(x, y)
    return round(float(rho), 3), round(float(p), 4)


def timing_intensity(cases: list[CaseProfile]) -> TimingIntensityResult:
    """Hypothesis (c): Spearman correlations between fragmentation depth
    dimensions and collectivization strength dimensions."""
    non_ctrl = [c for c in cases if not c.is_control]
    if len(non_ctrl) < 3:
        return TimingIntensityResult({}, "insufficient_cases")

    frag_dims = {
        "unit_count": [float(c.units_peak) for c in non_ctrl],
        "duration": [float(c.frag_duration_years) for c in non_ctrl],
        "conflict_intensity": [c.conflicts_per_decade for c in non_ctrl],
    }
    from feature_vector import integration_depth
    collect_dims = {
        "speed": [float(c.collect_speed_years) for c in non_ctrl],
        "depth": [float(integration_depth(c.features_post)) for c in non_ctrl],
        "durability": [float(c.durability_years) for c in non_ctrl],
    }

    matrix = {}
    for fk, fv in frag_dims.items():
        for ck, cv in collect_dims.items():
            key = f"{fk}_vs_{ck}"
            if ck == "speed":
                rho, p = _spearman(fv, [-s for s in cv])
            else:
                rho, p = _spearman(fv, cv)
            matrix[key] = {"rho": rho, "p": p}

    channel_scores = {
        "coordination_failure": abs(matrix.get("unit_count_vs_speed", {}).get("rho", 0)),
        "institutional_learning": abs(matrix.get("duration_vs_depth", {}).get("rho", 0)),
        "trauma": abs(matrix.get("conflict_intensity_vs_depth", {}).get("rho", 0)),
    }
    dominant = max(channel_scores, key=channel_scores.get)

    return TimingIntensityResult(matrix, dominant)


@dataclass
class CycleAnalysis:
    ratchet_result: dict
    form_shift_result: dict
    timing_intensity_result: dict
    warning_signals_result: dict
    summary: dict


def analyze(cases: list[CaseProfile]) -> CycleAnalysis:
    """Full cross-case cycle analysis."""
    r = ratchet.analyze(cases)
    f = form_shift.analyze(cases)
    t = timing_intensity(cases)

    ws_results = {}
    for c in cases:
        if c.is_control:
            continue
        w = warning_signals.analyze_case(
            c.name, c.gdp_series, c.vdem_series,
            c.features_post, c.post_collect_year)
        ws_results[c.name] = {
            "efficiency_decay": {"fired": w.efficiency_decay.fired,
                                 "detail": w.efficiency_decay.detail},
            "integration_reversal": {"fired": w.integration_reversal.fired,
                                     "detail": w.integration_reversal.detail},
            "legitimacy_erosion": {"fired": w.legitimacy_erosion.fired,
                                   "detail": w.legitimacy_erosion.detail},
            "any_fired": w.any_fired,
        }

    signals_fired = sum(1 for v in ws_results.values() if v["any_fired"])
    signals_total = len(ws_results)

    ratchet_dict = {
        "per_case": {name: {
            "positive_dims": s.positive_dims,
            "incorporation_ratio": s.incorporation_ratio,
            "demographic_ratio": s.demographic_ratio,
            "integration_depth": f"{s.integration_depth_pre} -> {s.integration_depth_post}",
            "functional_breadth": f"{s.functional_breadth_pre} -> {s.functional_breadth_post}",
            "efficiency_burst": s.efficiency_burst,
        } for name, s in r.per_case.items()},
        "sign_test_p": r.sign_test_p,
        "strongest_dimensions": r.strongest_dimensions,
    }

    fs_dict = {
        "per_case": {name: {
            "type_pre": s.type_pre,
            "type_post": s.type_post,
            "type_changed": s.type_changed,
            "flip_count": s.flip_count,
            "flipped_features": s.flipped_features,
            "legitimacy_flips": s.legitimacy_flips,
            "failures_patched": s.failure_diagnostic["patched"],
            "new_vulnerabilities": s.failure_diagnostic["new_vulnerabilities"],
        } for name, s in f.per_case.items()},
        "cases_mean_flips": f.cases_mean_flips,
        "controls_mean_flips": f.controls_mean_flips,
        "mann_whitney_p": f.mann_whitney_p,
        "all_cases_shifted_type": f.all_cases_shifted_type,
        "patching_rate": f.patching_rate,
        "net_patch_cases": f.net_patch_cases,
        "net_patch_controls": f.net_patch_controls,
        "net_patch_u": f.net_patch_u,
        "net_patch_p": f.net_patch_p,
    }

    ti_dict = {
        "spearman_matrix": t.spearman_matrix,
        "dominant_channel": t.dominant_channel,
    }

    summary = {
        "ratchet_supported": r.sign_test_p < 0.05,
        "form_shift_supported": f.net_patch_p < 0.10,
        "all_types_shifted": f.all_cases_shifted_type,
        "dominant_mechanism_channel": t.dominant_channel,
        "warning_signals_hit_rate": round(signals_fired / signals_total, 2)
        if signals_total > 0 else None,
        "n_core_cases": len([c for c in cases if not c.is_control]),
        "n_controls": len([c for c in cases if c.is_control]),
    }

    return CycleAnalysis(
        ratchet_result=ratchet_dict,
        form_shift_result=fs_dict,
        timing_intensity_result=ti_dict,
        warning_signals_result=ws_results,
        summary=summary,
    )
