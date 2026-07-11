#!/usr/bin/env python3
"""
Gold standard — Test 1 (THE GATE): does the 19-point dense erosion curve have
monetary-regime structure? Frozen spec: docs/GOLD_STANDARD_PREREGISTRATION.md.

Primary dataset = erosion_component_B.dense_curve(), committed & UNMODIFIED.
Read-only; writes data/robustness/gold_standard/t1_gate.json.
"""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts" / "robustness"))
sys.path.insert(0, str(ROOT / "scripts" / "historical"))
import erosion_component_B as B  # noqa: E402  (dense_curve, _aic_bic)

OUT = ROOT / "data" / "robustness" / "gold_standard" / "t1_gate.json"

KNOTS = [1870, 1914, 1919, 1944, 1971, 1985]  # frozen regime boundaries

# frozen slope-analysis blocks: name -> (lo, hi, is_gold)
BLOCKS = [
    ("pre_gold", 1816, 1866, False),
    ("classical_gold", 1876, 1906, True),
    ("interwar_disruption", 1916, 1936, False),
    ("bretton_woods", 1946, 1966, True),
    ("post_1971_fiat", 1976, 1996, False),
]
GOLD_YEARS = {1876, 1886, 1896, 1906, 1946, 1956, 1966}


def ols(X, y):
    """Return coefs, residuals, rss, and per-coef p-values (two-tailed t)."""
    from scipy import stats
    X = np.asarray(X, float); y = np.asarray(y, float)
    n, k = X.shape
    beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    rss = float(resid @ resid)
    dof = n - k
    ps = [None] * k
    if dof > 0:
        sigma2 = rss / dof
        cov = sigma2 * np.linalg.pinv(X.T @ X)
        se = np.sqrt(np.diag(cov))
        with np.errstate(divide="ignore", invalid="ignore"):
            t = beta / se
        ps = [float(2 * stats.t.sf(abs(tt), dof)) if s > 0 else None
              for tt, s in zip(t, se)]
    return beta, rss, ps, n, k


def slope(years, vals):
    from scipy import stats
    if len(years) < 2:
        return None
    r = stats.linregress(years, vals)
    return {"slope": float(r.slope), "p": float(r.pvalue), "n": len(years),
            "mean_level": float(np.mean(vals))}


def main():
    pts = B.dense_curve()  # UNMODIFIED committed artifact
    years = np.array([p["year"] for p in pts], float)
    spread = np.array([p["spread"] for p in pts], float)
    n = len(pts)

    # 1) per-regime OLS slopes
    block_slopes = {}
    for name, lo, hi, is_gold in BLOCKS:
        idx = [i for i, y in enumerate(years) if lo <= y <= hi]
        block_slopes[name] = {"is_gold": is_gold,
                              **(slope(years[idx], spread[idx]) or {})}
    gold_slopes = [block_slopes[b[0]]["slope"] for b in BLOCKS if b[3]]
    nongold_slopes = [block_slopes[b[0]]["slope"] for b in BLOCKS if not b[3]]
    mean_gold = float(np.mean(gold_slopes))
    mean_nongold = float(np.mean(nongold_slopes))

    # 2) single linear vs segmented (continuous piecewise) with regime knots
    ones = np.ones(n)
    Xlin = np.column_stack([ones, years])
    _, rss_lin, _, _, klin = ols(Xlin, spread)
    aic_lin, bic_lin = B._aic_bic(rss_lin, n, klin)

    hinges = [np.maximum(0.0, years - k) for k in KNOTS]
    Xseg = np.column_stack([ones, years] + hinges)
    beta_seg, rss_seg, _, _, kseg = ols(Xseg, spread)
    aic_seg, bic_seg = B._aic_bic(rss_seg, n, kseg)

    d_aic = aic_lin - aic_seg   # positive => segmented better
    d_bic = bic_lin - bic_seg

    # 3) gold-dummy regression: spread ~ year + GOLD + year:GOLD
    gold = np.array([1.0 if y in GOLD_YEARS else 0.0 for y in years])
    yc = years - years.mean()  # center year for interpretable interaction
    Xg = np.column_stack([ones, yc, gold, yc * gold])
    beta_g, rss_g, ps_g, _, _ = ols(Xg, spread)

    # directional predictions
    p1a = mean_gold < mean_nongold  # gold slopes more negative
    classical = block_slopes["classical_gold"]["slope"]
    bw = block_slopes["bretton_woods"]["slope"]
    interwar = block_slopes["interwar_disruption"]["slope"]
    fiat = block_slopes["post_1971_fiat"]["slope"]
    p1b = interwar >= max(classical, bw)          # interwar not steeper than gold
    p1c = fiat >= bw                              # post-71 not steeper than BW

    # verdict
    aic_favors_seg = d_aic >= 2
    if aic_favors_seg and p1a:
        verdict = "PASS"
    elif p1a and (ps_g[3] is not None and beta_g[3] < 0 and ps_g[3] < 0.05):
        verdict = "PARTIAL"
    elif p1a:
        verdict = "PARTIAL_weak"
    else:
        verdict = "FAIL"

    out = {
        "test": "T1_gate_regime_structure",
        "curve_source": "erosion_component_B.dense_curve() unmodified; 19 pts 1816-1996",
        "curve": pts,
        "per_regime_slopes": block_slopes,
        "mean_gold_slope": mean_gold, "mean_nongold_slope": mean_nongold,
        "model_comparison": {
            "single_linear": {"params": klin, "rss": round(rss_lin, 6),
                              "aic": round(aic_lin, 3), "bic": round(bic_lin, 3),
                              "slope": float(np.linalg.lstsq(Xlin, spread, rcond=None)[0][1])},
            "segmented_regime_knots": {"params": kseg, "rss": round(rss_seg, 6),
                                       "aic": round(aic_seg, 3), "bic": round(bic_seg, 3),
                                       "knots": KNOTS},
            "delta_aic_lin_minus_seg": round(d_aic, 3),
            "delta_bic_lin_minus_seg": round(d_bic, 3),
            "aic_favors_segmented(>=2)": bool(aic_favors_seg),
        },
        "gold_dummy_regression": {
            "form": "spread ~ 1 + year_centered + GOLD + year_centered:GOLD",
            "coef_intercept": round(float(beta_g[0]), 5),
            "coef_year": round(float(beta_g[1]), 6), "p_year": ps_g[1],
            "coef_GOLD": round(float(beta_g[2]), 5), "p_GOLD": ps_g[2],
            "coef_year_x_GOLD": round(float(beta_g[3]), 6), "p_interaction": ps_g[3],
        },
        "directional_predictions": {
            "P1a_gold_slopes_more_negative": bool(p1a),
            "P1b_interwar_not_steeper_than_gold": bool(p1b),
            "P1c_post71_not_steeper_than_BW": bool(p1c),
            "classical_gold_slope": classical, "bretton_woods_slope": bw,
            "interwar_slope": interwar, "post71_fiat_slope": fiat,
        },
        "verdict": verdict,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1))

    print("=== TEST 1 GATE — monetary-regime structure in 19-pt erosion curve ===")
    print("per-regime slopes (spread per year):")
    for name, lo, hi, is_gold in BLOCKS:
        b = block_slopes[name]
        tag = "GOLD" if is_gold else "non "
        print(f"  [{tag}] {name:20s} {lo}-{hi}: slope={b['slope']:+.6f} "
              f"level={b['mean_level']:+.4f} (n={b['n']}, p={b['p']:.3f})")
    print(f"  mean GOLD slope={mean_gold:+.6f}  vs  mean NON-GOLD slope={mean_nongold:+.6f}")
    print("\nmodel comparison (lower AIC/BIC better):")
    mc = out["model_comparison"]
    print(f"  single linear : k={mc['single_linear']['params']} rss={mc['single_linear']['rss']} "
          f"AIC={mc['single_linear']['aic']} BIC={mc['single_linear']['bic']}")
    print(f"  segmented(regime knots): k={mc['segmented_regime_knots']['params']} "
          f"rss={mc['segmented_regime_knots']['rss']} AIC={mc['segmented_regime_knots']['aic']} "
          f"BIC={mc['segmented_regime_knots']['bic']}")
    print(f"  ΔAIC(lin-seg)={mc['delta_aic_lin_minus_seg']:+.3f} "
          f"ΔBIC(lin-seg)={mc['delta_bic_lin_minus_seg']:+.3f} "
          f"-> AIC favors segmented? {mc['aic_favors_segmented(>=2)']}")
    gd = out["gold_dummy_regression"]
    print(f"\ngold-dummy: coef_GOLD={gd['coef_GOLD']:+.5f}(p={gd['p_GOLD']}) "
          f"coef_year×GOLD={gd['coef_year_x_GOLD']:+.6f}(p={gd['p_interaction']})")
    dp = out["directional_predictions"]
    print(f"\ndirectional: P1a(gold steeper)={dp['P1a_gold_slopes_more_negative']} | "
          f"P1b(interwar recovery)={dp['P1b_interwar_not_steeper_than_gold']} | "
          f"P1c(post71 recovery)={dp['P1c_post71_not_steeper_than_BW']}")
    print(f"\n>>> VERDICT: {verdict}")


if __name__ == "__main__":
    main()
