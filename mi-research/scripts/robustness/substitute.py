"""
Plan 1 — Alternative-indicator substitution (frozen pre-registration).

Tests whether MI country rankings survive replacing the "liberal-institutional /
perception-based" indicators (WGI, GII, FSI) with conceptually different
"revealed-outcome" indicators (tax take, education spend, logistics performance,
high-tech exports, homicide).

READ-ONLY SEAM (zero edits to scoring math):
    ind = dict(mi.panel.indicators_for(country, 2024))   # panel.py:58
    ind[key] = <percentile-ranked alternative>           # mutate the flat dict
    mi.scoring.score_country(ind)                          # scoring.py:324

FROZEN CHOICES (docs/ROBUSTNESS_PREREGISTRATION.md, "Plan 1"):
  * Rescaling: every alternative series -> 0-100 cross-country PERCENTILE RANK
    before injection (mirrors WGI construction; satisfies scale guard scoring.py:114).
  * Substitutions:
      P1 individual   : WGI GovEff/RuleLaw/RegQual block -> one revealed series
                        (a) tax rev %GDP  (b) govt edu exp %GDP  (c) LPI
      P1 max-divergence: GovEff->tax, RuleLaw->edu, RegQual->LPI simultaneously
      P2 GII -> high-tech exports
      P5 FSI -> homicide rate
  * Primary output = THE MOVERS (are big movers the contested cases?), not rho.
  * Income-partialling: residual rank = rank minus what log GDP-pc PPP predicts;
    do the RESIDUAL ranks survive substitution?
  * Secondary: Spearman rho vs original ranking.
  * Baseline: GDP-per-capita-only ranking vs original MI.

Outputs data/robustness/substitution_results.json. Edits NO scoring math.
"""
from __future__ import annotations
import json
import math
from pathlib import Path

import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))  # make `mi` importable when run as a script

from mi import panel, scoring  # noqa: E402

ALT = ROOT / "data" / "robustness" / "alt_indicators.json"
OUT = ROOT / "data" / "robustness" / "substitution_results.json"
YEAR = 2024

# WGI P1 institutional-quality keys (the perception-based block under charge).
P1_WGI = ["gov_effectiveness", "rule_of_law", "regulatory_quality"]

# Normatively-contested cases (prereg names Gulf states, Singapore, China, Rwanda,
# Hungary; task adds Vietnam, Belarus, "etc."). CORE = explicitly named; EXTENDED
# adds well-known high-capacity-autocracy / illiberal cases for context.
CONTESTED_CORE = {
    "ARE", "SAU", "QAT", "KWT", "BHR", "OMN",   # Gulf states
    "SGP", "CHN", "RWA", "HUN", "VNM", "BLR",   # named individually
}
CONTESTED_EXTENDED = CONTESTED_CORE | {
    "KAZ", "AZE", "RUS", "TUR", "ETH", "VEN", "NIC", "CUB", "IRN", "THA",
}


def pct_rank(values: dict[str, float]) -> dict[str, float]:
    """Cross-country percentile rank -> 0-100 (higher value => higher rank).
    Average ranks for ties; mirrors WGI's percentile-rank construction."""
    isos = list(values.keys())
    arr = np.array([values[i] for i in isos], dtype=float)
    order = arr.argsort()
    ranks = np.empty(len(arr), dtype=float)
    ranks[order] = np.arange(len(arr), dtype=float)
    # average-rank tie handling
    # (small N; do it simply)
    from collections import defaultdict
    groups = defaultdict(list)
    for idx, v in enumerate(arr):
        groups[v].append(idx)
    for v, idxs in groups.items():
        if len(idxs) > 1:
            avg = np.mean([ranks[i] for i in idxs])
            for i in idxs:
                ranks[i] = avg
    n = len(arr)
    if n == 1:
        return {isos[0]: 50.0}
    return {isos[i]: float(ranks[i] / (n - 1) * 100.0) for i in range(n)}


def spearman(a: list[float], b: list[float]) -> float:
    """Spearman rho via Pearson on ranks (numpy only)."""
    ra = _rankdata(a)
    rb = _rankdata(b)
    return float(np.corrcoef(ra, rb)[0, 1])


def _rankdata(x: list[float]) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    order = x.argsort()
    ranks = np.empty(len(x), dtype=float)
    ranks[order] = np.arange(1, len(x) + 1, dtype=float)
    from collections import defaultdict
    groups = defaultdict(list)
    for i, v in enumerate(x):
        groups[v].append(i)
    for v, idxs in groups.items():
        if len(idxs) > 1:
            avg = np.mean([ranks[i] for i in idxs])
            for i in idxs:
                ranks[i] = avg
    return ranks


def mi_ranks(scores: dict[str, float]) -> dict[str, int]:
    """iso -> rank (1 = highest MI)."""
    ordered = sorted(scores, key=lambda i: scores[i], reverse=True)
    return {iso: r + 1 for r, iso in enumerate(ordered)}


def residual_ranks(scores: dict[str, float], loggdp: dict[str, float]) -> dict[str, float]:
    """Rank of (MI residual after regressing MI on log GDP-pc PPP). 1 = highest residual."""
    isos = [i for i in scores if i in loggdp]
    y = np.array([scores[i] for i in isos])
    x = np.array([loggdp[i] for i in isos])
    slope, intercept = np.polyfit(x, y, 1)
    resid = {isos[k]: float(y[k] - (slope * x[k] + intercept)) for k in range(len(isos))}
    ordered = sorted(resid, key=lambda i: resid[i], reverse=True)
    return {iso: r + 1 for r, iso in enumerate(ordered)}


def score_universe(build_ind) -> dict[str, float]:
    """Score every country; build_ind(iso, base_ind) -> mutated dict or None (skip).
    Returns iso -> mi_score for countries with a computable MI."""
    out = {}
    for iso, (display, base) in panel.all_indicators(YEAR).items():
        ind = build_ind(iso, dict(base))
        if ind is None:
            continue
        res = scoring.score_country(ind)
        if res["mi_score"] is not None:
            out[iso] = res["mi_score"]
    return out


def main():
    alt = json.loads(ALT.read_text())["indicators"]
    universe = panel.all_indicators(YEAR)  # iso -> (display, ind)
    display = {iso: universe[iso][0] for iso in universe}

    # Percentile-rank each alternative series over its full available country set.
    pct = {}
    for label, blob in alt.items():
        vals = {iso: d["value"] for iso, d in blob["data"].items()}
        pct[label] = pct_rank(vals)

    # log GDP-pc PPP (income control), from the panel.
    loggdp = {}
    for iso, (disp, ind) in universe.items():
        g = ind.get("gdp_per_capita_ppp")
        if g and g > 0:
            loggdp[iso] = math.log(g)

    # ---- Baseline: original MI over the full universe ----
    orig = score_universe(lambda iso, ind: ind)
    print(f"Baseline original MI: N={len(orig)}")

    # ---- GDP-only baseline ranking ----
    gdp_only = {iso: universe[iso][1].get("gdp_per_capita_ppp")
                for iso in orig if universe[iso][1].get("gdp_per_capita_ppp")}
    common_g = [i for i in orig if i in gdp_only]
    rho_gdp = spearman([orig[i] for i in common_g], [gdp_only[i] for i in common_g])

    # ---- substitution run definitions ----
    def run_p1_single(alt_label):
        def build(iso, ind):
            if iso not in pct[alt_label]:
                return None
            v = pct[alt_label][iso]
            for k in P1_WGI:
                ind[k] = v
            return ind
        return build

    def run_p1_maxdiv(iso, ind):
        if not all(iso in pct[l] for l in ("tax_rev_pct_gdp", "gov_edu_exp_pct_gdp", "lpi_overall")):
            return None
        ind["gov_effectiveness"] = pct["tax_rev_pct_gdp"][iso]
        ind["rule_of_law"] = pct["gov_edu_exp_pct_gdp"][iso]
        ind["regulatory_quality"] = pct["lpi_overall"][iso]
        return ind

    def run_p2_gii(iso, ind):
        if iso not in pct["hightech_exp_pct"]:
            return None
        ind["gii"] = pct["hightech_exp_pct"][iso]
        return ind

    def run_p5_fsi(iso, ind):
        if iso not in pct["homicide_per100k"]:
            return None
        # higher homicide -> higher percentile -> normalize_fsi(x)=1-x/120 -> lower P5.
        # direction preserved: more violence = worse stability.
        ind["fsi"] = pct["homicide_per100k"][iso]
        return ind

    runs = {
        "P1_tax_revenue":        run_p1_single("tax_rev_pct_gdp"),
        "P1_education_exp":      run_p1_single("gov_edu_exp_pct_gdp"),
        "P1_lpi":                run_p1_single("lpi_overall"),
        "P1_maxdivergence":      run_p1_maxdiv,
        "P2_gii_to_hightech":    run_p2_gii,
        "P5_fsi_to_homicide":    run_p5_fsi,
    }

    results = {"_meta": {"year": YEAR, "n_baseline": len(orig),
                         "seam": "panel.indicators_for (panel.py:58) -> mutate dict -> "
                                 "scoring.score_country (scoring.py:324)",
                         "rescaling": "0-100 cross-country percentile rank",
                         "gdp_only_baseline_rho_vs_MI": rho_gdp,
                         "gdp_only_baseline_N": len(common_g)},
               "runs": {}}

    for name, build in runs.items():
        sub = score_universe(build)
        # run universe = countries with BOTH original MI and a substituted MI
        common = [i for i in orig if i in sub]
        N = len(common)
        rho = spearman([orig[i] for i in common], [sub[i] for i in common])

        # movers: ranks recomputed WITHIN the run universe for fair comparison
        orig_sub_universe = {i: orig[i] for i in common}
        r_orig = mi_ranks(orig_sub_universe)
        r_sub = mi_ranks(sub if set(sub) == set(common) else {i: sub[i] for i in common})
        movers = []
        for i in common:
            dr = r_sub[i] - r_orig[i]  # + = fell in rank (worse), - = rose
            movers.append((i, display[i], r_orig[i], r_sub[i], dr,
                           i in CONTESTED_CORE, i in CONTESTED_EXTENDED))
        movers.sort(key=lambda t: abs(t[4]), reverse=True)

        # income-residual test: do residual ranks survive substitution?
        common_res = [i for i in common if i in loggdp]
        ro = residual_ranks({i: orig[i] for i in common_res}, loggdp)
        rs = residual_ranks({i: sub[i] for i in common_res}, loggdp)
        rho_resid = spearman([ro[i] for i in common_res], [rs[i] for i in common_res])

        # contested-case concentration among big movers
        top20 = movers[:20]
        contested_in_top20 = sum(1 for m in top20 if m[6])
        contested_core_in_top20 = sum(1 for m in top20 if m[5])
        # mean |rank move| for contested-core vs rest
        core_moves = [abs(m[4]) for m in movers if m[5]]
        rest_moves = [abs(m[4]) for m in movers if not m[6]]
        results["runs"][name] = {
            "N": N,
            "rho_MI_rank": rho,
            "rho_income_residual_rank": rho_resid,
            "N_residual": len(common_res),
            "top_movers": [
                {"iso": m[0], "country": m[1], "rank_orig": m[2], "rank_sub": m[3],
                 "rank_change": m[4], "direction": ("fell" if m[4] > 0 else "rose" if m[4] < 0 else "flat"),
                 "contested_core": m[5], "contested_ext": m[6]}
                for m in movers[:25]
            ],
            "contested_in_top20": contested_in_top20,
            "contested_core_in_top20": contested_core_in_top20,
            "mean_abs_move_contested_core": float(np.mean(core_moves)) if core_moves else None,
            "mean_abs_move_noncontested": float(np.mean(rest_moves)) if rest_moves else None,
            "max_abs_move": abs(movers[0][4]) if movers else 0,
        }
        print(f"{name:22s} N={N:4d}  rho={rho:.4f}  rho_resid={rho_resid:.4f}  "
              f"maxmove={abs(movers[0][4]) if movers else 0}  "
              f"contested_core_in_top20={contested_core_in_top20}")

    OUT.write_text(json.dumps(results, indent=2))
    print(f"\nGDP-only baseline rho vs original MI: {rho_gdp:.4f} (N={len(common_g)})")
    print(f"Wrote {OUT}")
    return results


if __name__ == "__main__":
    main()
