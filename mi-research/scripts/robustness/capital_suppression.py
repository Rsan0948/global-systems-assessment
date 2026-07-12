#!/usr/bin/env python3
"""
Capital-suppression sub-law test. Does "release is proportional to how long the fracture
was held shut" (demonstrated on state break-ups) extend to the economic/capital domain?

Suppression config = positive economy-institution gap (z(logGDP) - z(rol), within-year).
Episode = >=5 consecutive covered years with gap >= 0.75. Release = max GDP-pc drawdown in
[episode_end, +15]. Test 1 (GATE): Spearman(duration, drawdown) > 0, p<0.05, partial-ρ>0
net of peak_gap. Frozen spec: docs/CAPITAL_SUPPRESSION_PREREGISTRATION.md (sha256 cc53e559).
Read-only.
"""
from __future__ import annotations
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import convergence_lib as L  # noqa: E402

ROOT = L.ROOT
OUT = ROOT / "data/robustness/convergence/capital_suppression.json"
MIN_XSEC = 15
MIN_OVERLAP = 40


def build_gap_series():
    """iso -> {year: gap} where gap = z(logGDP) - z(rol), standardized within each year."""
    rol, gdp = L.load_rol_gdp()
    isos = [i for i in set(rol) & set(gdp) if not i.startswith("OWID")]
    # collect per-year cross-sections
    years = range(1789, 2023)
    gap = defaultdict(dict)
    for y in years:
        rows = []
        for iso in isos:
            r = rol[iso].get(str(y)); g = gdp[iso].get(y)
            if r is None or g is None or g <= 0:
                continue
            rows.append((iso, math.log(g), float(r)))
        if len(rows) < MIN_XSEC:
            continue
        lg = np.array([x[1] for x in rows]); rl = np.array([x[2] for x in rows])
        lgz = (lg - lg.mean()) / (lg.std() or 1); rlz = (rl - rl.mean()) / (rl.std() or 1)
        for (iso, _, _), a, b in zip(rows, lgz, rlz):
            gap[iso][y] = float(a - b)
    # restrict to countries with enough overlap
    return {i: g for i, g in gap.items() if len(g) >= MIN_OVERLAP}, gdp


def episodes(gap_series, gap_thresh, min_len):
    """Maximal runs of consecutive covered years with gap >= thresh, length >= min_len."""
    out = []
    for iso, gy in gap_series.items():
        ys = sorted(gy)
        run = []
        for i, y in enumerate(ys):
            consecutive = run and y == run[-1] + 1
            if gy[y] >= gap_thresh:
                run = (run + [y]) if consecutive else [y]
            else:
                run = []
            # close run at a break or end
            is_last = (i == len(ys) - 1)
            nxt_break = (not is_last) and (ys[i + 1] != y + 1 or gy[ys[i + 1]] < gap_thresh)
            if run and (is_last or nxt_break) and len(run) >= min_len:
                out.append((iso, run[0], run[-1], len(run),
                            max(gy[yy] for yy in run)))
                run = []
    return out


def drawdown(gdp_iso, start, horizon):
    """Max peak-to-trough % decline in GDP-pc within [start, start+horizon]."""
    ys = [y for y in range(start, start + horizon + 1) if y in gdp_iso and gdp_iso[y] > 0]
    if len(ys) < 2:
        return 0.0
    peak = -1; worst = 0.0
    for y in ys:
        v = gdp_iso[y]
        if v > peak:
            peak = v
        elif peak > 0:
            dd = (peak - v) / peak * 100
            if dd > worst:
                worst = dd
    return float(worst)


def run_cell(gap_series, gdp, dom, gap_thresh, min_len, horizon):
    eps = episodes(gap_series, gap_thresh, min_len)
    rows = []
    for iso, y0, y1, dur, pk in eps:
        dd = drawdown(gdp.get(iso, {}), y1, horizon)
        pol = 1 if any(y1 <= oy <= y1 + horizon for oy in dom.get(iso, set())) else 0
        rows.append({"iso": iso, "start": y0, "end": y1, "duration": dur,
                     "peak_gap": round(pk, 3), "drawdown_pct": round(dd, 2), "conflict": pol})
    if len(rows) < 8:
        return {"n": len(rows), "note": "too few episodes"}, rows
    dur = np.array([r["duration"] for r in rows], float)
    dd = np.array([r["drawdown_pct"] for r in rows], float)
    pk = np.array([r["peak_gap"] for r in rows], float)
    sp = stats.spearmanr(dur, dd)
    # partial Spearman(dur, dd | pk): rank residuals
    def rankresid(a, b):
        ra, rb = stats.rankdata(a), stats.rankdata(b)
        slope = np.polyfit(rb, ra, 1)
        return ra - np.polyval(slope, rb)
    pr = stats.pearsonr(rankresid(dur, pk), rankresid(dd, pk))
    return {"n": len(rows), "spearman_rho": round(float(sp.statistic), 3),
            "spearman_p": round(float(sp.pvalue), 4),
            "partial_rho_ctrl_peakgap": round(float(pr.statistic), 3),
            "partial_p": round(float(pr.pvalue), 4),
            "median_duration": float(np.median(dur)),
            "mean_drawdown": round(float(dd.mean()), 1)}, rows


def main():
    gap_series, gdp = build_gap_series()
    dom = L.domestic_years()
    # registered cell
    reg, rows = run_cell(gap_series, gdp, dom, 0.75, 5, 15)

    # Test 2 — duration vs political release
    t2 = None
    if len(rows) >= 8:
        d_yes = [r["duration"] for r in rows if r["conflict"] == 1]
        d_no = [r["duration"] for r in rows if r["conflict"] == 0]
        if len(d_yes) >= 3 and len(d_no) >= 3:
            u = stats.mannwhitneyu(d_yes, d_no, alternative="greater")
            t2 = {"n_conflict": len(d_yes), "n_none": len(d_no),
                  "mean_dur_conflict": round(float(np.mean(d_yes)), 1),
                  "mean_dur_none": round(float(np.mean(d_no)), 1),
                  "mannwhitney_p_greater": round(float(u.pvalue), 4)}

    # Test 3 — sensitivity grid
    grid = []
    for gt in [0.5, 0.75, 1.0]:
        for ml in [3, 5]:
            for hz in [10, 15, 20]:
                res, _ = run_cell(gap_series, gdp, dom, gt, ml, hz)
                grid.append({"gap_thresh": gt, "min_len": ml, "horizon": hz,
                             "n": res.get("n"), "rho": res.get("spearman_rho"),
                             "p": res.get("spearman_p"),
                             "partial_rho": res.get("partial_rho_ctrl_peakgap")})

    rhos = [c["rho"] for c in grid if c["rho"] is not None]
    pos_frac = sum(1 for r in rhos if r > 0) / len(rhos) if rhos else 0
    reg_pass = (isinstance(reg.get("spearman_rho"), float) and reg["spearman_rho"] > 0
                and reg["spearman_p"] < 0.05 and reg["partial_rho_ctrl_peakgap"] > 0)
    grid_stable = pos_frac >= 0.5
    verdict = ("PROMOTE" if (reg_pass and grid_stable)
               else "PROMOTE-fragile(registered-cell-only)" if reg_pass
               else "RETIRE-to-context-only")

    out = {"prereg_sha256": "cc53e559", "n_countries": len(gap_series),
           "registered_cell(0.75,5,15)": reg, "test2_political": t2,
           "sensitivity_grid": grid,
           "grid_positive_fraction": round(pos_frac, 2),
           "gate_registered_pass": bool(reg_pass), "grid_directionally_stable": bool(grid_stable),
           "VERDICT": verdict, "episodes": rows}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1))

    print(f"countries with gap series: {len(gap_series)}")
    print(f"\n=== TEST 1 (GATE) — registered cell (gap>=0.75, len>=5, horizon 15) ===")
    print(f"  episodes n={reg.get('n')}")
    print(f"  Spearman(duration, drawdown%) = {reg.get('spearman_rho')} (p={reg.get('spearman_p')})")
    print(f"  partial ρ | peak_gap          = {reg.get('partial_rho_ctrl_peakgap')} (p={reg.get('partial_p')})")
    print(f"  median duration={reg.get('median_duration')}yr  mean drawdown={reg.get('mean_drawdown')}%")
    print(f"  >>> registered gate pass: {reg_pass}")
    if t2:
        print(f"\n=== TEST 2 — political release ===\n  mean duration: conflict={t2['mean_dur_conflict']}yr "
              f"vs none={t2['mean_dur_none']}yr (MW p_greater={t2['mannwhitney_p_greater']})")
    print(f"\n=== TEST 3 — sensitivity grid (ρ by cell) ===")
    for c in grid:
        star = " <-REGISTERED" if (c["gap_thresh"], c["min_len"], c["horizon"]) == (0.75, 5, 15) else ""
        print(f"  gap>={c['gap_thresh']} len>={c['min_len']} hz={c['horizon']}: n={c['n']} ρ={c['rho']} p={c['p']} partial={c['partial_rho']}{star}")
    print(f"  positive-ρ fraction across grid: {pos_frac:.2f}  (directionally stable: {grid_stable})")
    print(f"\n>>> VERDICT: {verdict}")


if __name__ == "__main__":
    main()
