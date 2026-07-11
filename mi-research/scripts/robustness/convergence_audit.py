#!/usr/bin/env python3
"""
ADVERSARIAL AUDIT of the convergence finding (Finding 15). Not part of the finding —
a self-attack. Probes the failure modes this repo keeps hitting:
  P1  composition artifact: does wealth-catching-up survive a CONSTANT sample?
  P2  small-n early anchors: does the wealth_auc trend survive dropping n<20 epochs?
  P3  Test-1 confirm fragility: matched-sample + detrended coupling-vs-wealth_auc.
  P4  Test-3 collinearity: VIF + coefficient stability of the "both significant" claim.
  P5  Test-8 small-n: bootstrap CIs on exposed/non-exposed coupling.
Read-only. Prints a PASS/FAIL-style verdict per probe.
"""
from __future__ import annotations
import math
import sys
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import convergence_lib as L  # noqa: E402


def decomp_on(isos, label_fn=None, epochs=None):
    label_fn = label_fn or L.domestic_label_fn()
    return L.epoch_decomp(label_fn, isos_filter=isos, epochs=epochs)


# ============================================================ P1 constant sample
def p1_constant_sample():
    print("=" * 78)
    print("PROBE 1 — COMPOSITION ARTIFACT: does wealth-catching-up survive a CONSTANT sample?")
    print("  (the pooled domestic curve grows n=12->160; if the pattern is really the")
    print("   changing sample it will VANISH on a fixed set of countries.)")
    rol, gdp = L.load_rol_gdp()
    form = L.load_formation()
    uni = set(rol) & set(gdp)
    lab = L.domestic_label_fn()

    def present(iso, y):
        return rol[iso].get(str(y)) is not None and (gdp[iso].get(y) or 0) > 0

    for anchor_lo in [1876, 1906, 1926]:
        anchors = list(range(anchor_lo, 1997, 10))
        const = {i for i in uni if not i.startswith("OWID") and all(present(i, a) for a in anchors)}
        pts = decomp_on(const, lab, epochs=anchors)
        valid = [p for p in pts if p["struct_auc"] is not None]
        if len(valid) < 4:
            print(f"  [{anchor_lo}-1996] constant n={len(const)}: too few valid epochs"); continue
        ys = [p["year"] for p in valid]
        sa = [p["struct_auc"] for p in valid]; wa = [p["wealth_auc"] for p in valid]
        st, wt = L.trend(ys, sa), L.trend(ys, wa)
        print(f"  [{anchor_lo}-1996] constant n={len(const)} (npos/epoch {valid[0]['n_pos']}..{valid[-1]['n_pos']}):")
        print(f"      struct_auc {sa[0]:.3f}->{sa[-1]:.3f} (Δ{sa[-1]-sa[0]:+.3f}, slope p={st['p']:.3f})")
        print(f"      wealth_auc {wa[0]:.3f}->{wa[-1]:.3f} (Δ{wa[-1]-wa[0]:+.3f}, slope p={wt['p']:.3f})")
        print(f"      spread {sa[0]-wa[0]:+.3f}->{sa[-1]-wa[-1]:+.3f}  "
              f"[wealth catching up = wealth Δ > struct Δ: {wa[-1]-wa[0] > sa[-1]-sa[0]}]")
    # mature-only decomposition (composition-controlled)
    mature = {i for i in uni if form.get(i) == "mature"}
    pts = decomp_on(mature, lab)
    valid = [p for p in pts if p["struct_auc"] is not None]
    ys = [p["year"] for p in valid]; sa = [p["struct_auc"] for p in valid]; wa = [p["wealth_auc"] for p in valid]
    st, wt = L.trend(ys, sa), L.trend(ys, wa)
    print(f"  [mature-only, all epochs] n={len(mature)}:")
    print(f"      struct_auc Δ{sa[-1]-sa[0]:+.3f} (p={st['p']:.3f}) | wealth_auc Δ{wa[-1]-wa[0]:+.3f} (p={wt['p']:.3f}) "
          f"| wealth-catching-up: {wa[-1]-wa[0] > sa[-1]-sa[0]}")


# ============================================================ P2 small-n anchors
def p2_small_n():
    print("=" * 78)
    print("PROBE 2 — SMALL-N EARLY ANCHORS: 1816 has n=12, npos=6 (noise). Does the")
    print("  wealth_auc trend survive dropping tiny early epochs?")
    dc = L.committed_decomp()
    for floor in [0, 20, 30, 40]:
        v = [p for p in dc if p.get("struct_auc") is not None and p["n"] >= floor]
        ys = [p["year"] for p in v]; sa = [p["struct_auc"] for p in v]; wa = [p["wealth_auc"] for p in v]
        st, wt = L.trend(ys, sa), L.trend(ys, wa)
        print(f"  n>={floor:>2} ({len(v)} epochs {ys[0]}-{ys[-1]}): "
              f"struct slope p={st['p']:.3f} Δ{sa[-1]-sa[0]:+.3f} | "
              f"wealth slope p={wt['p']:.3f} Δ{wa[-1]-wa[0]:+.3f}")


# ============================================================ P3 Test-1 confirm
def p3_coupling_confirm():
    print("=" * 78)
    print("PROBE 3 — TEST-1 CONFIRM FRAGILITY: coupling-vs-wealth_auc used mature coupling")
    print("  vs POOLED wealth_auc (sample mismatch), and both series trend up (spurious?).")
    rol, gdp = L.load_rol_gdp()
    form = L.load_formation()
    uni = set(rol) & set(gdp)
    mature = {i for i in uni if form.get(i) == "mature"}
    lab = L.domestic_label_fn()

    def coupling_series(isos):
        out = {}
        for y in L.EPOCHS:
            xs, ys = [], []
            for iso in isos:
                if iso.startswith("OWID"):
                    continue
                r = rol[iso].get(str(y)); g0 = gdp[iso].get(y)
                if r is None or g0 is None or g0 <= 0:
                    continue
                xs.append(float(r)); ys.append(math.log(g0))
            if len(xs) >= 8 and np.std(xs) > 0:
                out[y] = float(stats.pearsonr(xs, ys).statistic)
        return out

    coup_pool = coupling_series(uni)
    coup_mat = coupling_series(mature)
    wa_pool = {p["year"]: p["wealth_auc"] for p in L.committed_decomp() if p.get("wealth_auc") is not None}
    wa_mat = {p["year"]: p["wealth_auc"] for p in decomp_on(mature, lab) if p.get("wealth_auc") is not None}

    def corr(a, b, label, detrend=False):
        ys = sorted(set(a) & set(b))
        x = np.array([a[y] for y in ys]); z = np.array([b[y] for y in ys])
        if detrend:
            t = np.array(ys, float)
            x = x - np.polyval(np.polyfit(t, x, 1), t)
            z = z - np.polyval(np.polyfit(t, z, 1), t)
        r = stats.pearsonr(x, z)
        print(f"  {label}: r={r.statistic:+.3f} p={r.pvalue:.3f} (n={len(ys)})")
        return r.statistic, r.pvalue

    print("  RAW (level) correlations:")
    corr(coup_mat, wa_pool, "mature-coupling vs POOLED wealth_auc  [used in finding]")
    corr(coup_mat, wa_mat, "mature-coupling vs MATURE wealth_auc   [matched sample]")
    corr(coup_pool, wa_pool, "pooled-coupling vs POOLED wealth_auc  [matched sample]")
    print("  DETRENDED (does co-movement survive removing shared time trend?):")
    corr(coup_mat, wa_pool, "mature-coupling vs POOLED wealth_auc", detrend=True)
    corr(coup_mat, wa_mat, "mature-coupling vs MATURE wealth_auc", detrend=True)


# ============================================================ P4 collinearity
def p4_collinearity():
    print("=" * 78)
    print("PROBE 4 — TEST-3 COLLINEARITY: P1 & GDP correlate ~0.8. Are the 'both")
    print("  significant' joint coefficients stable, or collinearity-inflated noise?")
    rol, gdp = L.load_rol_gdp()
    dom = L.domestic_years()
    uni = set(rol) & set(gdp)
    for y in [2004, 2012]:  # note: historical rol/gdp panel at these years
        R, G, lab = [], [], []
        for iso in uni:
            if iso.startswith("OWID"):
                continue
            r = rol[iso].get(str(y)); g0 = gdp[iso].get(y)
            if r is None or g0 is None or g0 <= 0:
                continue
            l = 1 if any(y <= oy <= y + L.WINDOW for oy in dom.get(iso, set())) else 0
            R.append(float(r)); G.append(-math.log(g0)); lab.append(l)
        Rz, Gz = L.zscore(R), L.zscore(G)
        collin = float(stats.pearsonr(Rz, Gz).statistic)
        vif = 1.0 / (1 - collin ** 2)
        # jackknife coefficient stability of joint model
        n = len(lab); yv = np.array(lab, float)
        def fit_coef(mask):
            X = np.column_stack([np.ones(mask.sum()), -Rz[mask], Gz[mask]])
            b, _, _ = L.logit_fit(X, yv[mask]); return b[1], b[2]
        allm = np.ones(n, bool)
        p1c, gc = fit_coef(allm)
        # 20-fold jackknife
        idx = np.arange(n); rng = np.random.default_rng(0); rng.shuffle(idx)
        p1s, gcs = [], []
        for f in range(20):
            m = allm.copy(); m[idx[f::20]] = False
            a, b = fit_coef(m); p1s.append(a); gcs.append(b)
        print(f"  {y}: corr(P1,GDP)={collin:+.3f} VIF={vif:.2f} | "
              f"P1 coef={p1c:+.3f} (jk sd {np.std(p1s):.3f}) | GDP coef={gc:+.3f} (jk sd {np.std(gcs):.3f})")
        print(f"       both same sign across all jackknife folds: "
              f"P1 {all(np.sign(p1s)==np.sign(p1c))} / GDP {all(np.sign(gcs)==np.sign(gc))}")


# ============================================================ P5 Test-8 CIs
def p5_test8_ci():
    print("=" * 78)
    print("PROBE 5 — TEST-8 SMALL-N: 'only resource decouples' rests on r=0.72 (n=16) vs")
    print("  0.84 (n=70). Bootstrap CI on the difference — is it distinguishable from noise?")
    import convergence_part2 as P2
    pnl = L.load_mi_panel(); rows = pnl["rows"]
    wdi = L.load_wdi()

    def pairs(exposed_fn, want, y=2018):
        out = []
        for iso, r in rows.items():
            e = r["years"].get(str(y))
            if not e or e.get("P1") is None or e.get("logGDP") is None:
                continue
            ex = exposed_fn(iso, y)
            if ex is want:
                out.append((e["P1"], e["logGDP"]))
        return out

    def boot_r(pr, n_boot=2000, seed=0):
        if len(pr) < 6:
            return None
        rng = np.random.default_rng(seed); a = np.array(pr)
        rs = []
        for _ in range(n_boot):
            s = a[rng.integers(0, len(a), len(a))]
            if np.std(s[:, 0]) > 0 and np.std(s[:, 1]) > 0:
                rs.append(stats.pearsonr(s[:, 0], s[:, 1]).statistic)
        return np.percentile(rs, [2.5, 50, 97.5])

    def f_res(iso, y):
        v = P2.resource_rents(iso, y); return None if v is None else v > 10
    exp = pairs(f_res, True); non = pairs(f_res, False)
    ce, cn = boot_r(exp), boot_r(non)
    print(f"  resource>10%: exposed n={len(exp)} r 95%CI [{ce[0]:.2f},{ce[2]:.2f}] med {ce[1]:.2f} | "
          f"non n={len(non)} r 95%CI [{cn[0]:.2f},{cn[2]:.2f}] med {cn[1]:.2f}")
    # difference bootstrap
    rng = np.random.default_rng(1); a, b = np.array(exp), np.array(non); diffs = []
    for _ in range(2000):
        sa = a[rng.integers(0, len(a), len(a))]; sb = b[rng.integers(0, len(b), len(b))]
        if np.std(sa[:, 0]) > 0 and np.std(sb[:, 0]) > 0:
            diffs.append(stats.pearsonr(sa[:, 0], sa[:, 1]).statistic - stats.pearsonr(sb[:, 0], sb[:, 1]).statistic)
    lo, med, hi = np.percentile(diffs, [2.5, 50, 97.5])
    print(f"  Δr (exposed-non) 95%CI [{lo:+.2f}, {hi:+.2f}] med {med:+.2f} "
          f"-> {'DISTINGUISHABLE from 0' if hi < 0 or lo > 0 else 'NOT distinguishable from 0 (fragile)'}")


def main():
    p1_constant_sample()
    p2_small_n()
    p3_coupling_confirm()
    p4_collinearity()
    p5_test8_ci()
    print("=" * 78)


if __name__ == "__main__":
    main()
