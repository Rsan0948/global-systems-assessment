#!/usr/bin/env python3
"""
Convergence confirmation — PART 2 (durability, Tests 7-8). Given Part 1 confirmed
the convergence (with a complementary-facet qualification), assess whether it is
structurally durable or at risk of reversal. Test 9 (AI) is analytical — in the
write-up, not here. Frozen spec: docs/CONVERGENCE_PREREGISTRATION.md. Read-only.

Writes data/robustness/convergence/part2.json.
"""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import convergence_lib as L  # noqa: E402
from mi import panel as MP  # noqa: E402

ROOT = L.ROOT
OUT = ROOT / "data/robustness/convergence/part2.json"


def resource_rents(iso, year):
    for y in [year, year - 1, year - 2, year + 1, year + 2]:
        ind = MP.indicators_for(iso, y)
        if ind and ind.get("resource_rents_pct_gdp") is not None:
            try:
                return float(ind["resource_rents_pct_gdp"])
            except (TypeError, ValueError):
                pass
    return None


# ============================================================ Test 7
def test7():
    pnl = L.load_mi_panel(); rows = pnl["rows"]
    ctx = json.loads((ROOT / "data/sources/country_context.json").read_text())
    dom = L.domestic_years()
    recs = []
    for iso, r in rows.items():
        y0, y1 = r["years"].get("1996"), r["years"].get("2024")
        if not y0 or not y1:
            continue
        g0, g1 = y0.get("gdp"), y1.get("gdp")
        p0, p1 = y0.get("P1"), y1.get("P1")
        if None in (g0, g1, p0, p1) or g0 <= 0:
            continue
        growth = g1 / g0 - 1.0
        dP1 = p1 - p0
        crisis = 1 if any(1996 <= oy <= 2024 for oy in dom.get(iso, set())) else 0
        recs.append({"iso": iso, "name": r["name"], "growth": growth, "dP1": dP1,
                     "logGDP96": y0.get("logGDP"), "crisis": crisis,
                     "resource_rents": resource_rents(iso, 2018),
                     "is_democratic": ctx.get(iso, {}).get("is_democratic")})
    # crisis-vs-GDP residual: GDP-only logit on all balanced countries
    y = np.array([r["crisis"] for r in recs], float)
    g = L.zscore([r["logGDP96"] for r in recs])
    X = np.column_stack([np.ones(len(recs)), g])
    b, auc, _ = L.logit_fit(X, y)
    p_pred = 1.0 / (1.0 + np.exp(-(X @ b)))
    for i, r in enumerate(recs):
        r["gdp_pred_crisis"] = float(p_pred[i]); r["residual"] = r["crisis"] - float(p_pred[i])

    def summarize(label, decoupled):
        coupled = [r for r in recs if r not in decoupled]
        dec_res = [r["residual"] for r in decoupled] or [0]
        cou_res = [r["residual"] for r in coupled] or [0]
        n_resource = sum(1 for r in decoupled if (r["resource_rents"] or 0) >= 10)
        n_autocracy = sum(1 for r in decoupled if r["is_democratic"] is False)
        n_outlier = sum(1 for r in decoupled if (r["resource_rents"] or 0) >= 10 or r["is_democratic"] is False)
        return {
            "criterion": label, "n_decoupled": len(decoupled),
            "decoupled_share": round(len(decoupled) / len(recs), 3),
            "mean_residual_decoupled": round(float(np.mean(dec_res)), 4),
            "mean_residual_coupled": round(float(np.mean(cou_res)), 4),
            "decoupled_crisis_more_than_gdp_predicts": bool(np.mean(dec_res) > np.mean(cou_res)),
            "outlier_breakdown": {"resource>=10%": n_resource, "autocracy": n_autocracy,
                                  "either_outlier": n_outlier, "non_outlier": len(decoupled) - n_outlier},
            "countries": sorted(
                [{"name": r["name"], "growth_pct": round(r["growth"] * 100, 1), "dP1": round(r["dP1"], 3),
                  "resource_rents": round(r["resource_rents"], 1) if r["resource_rents"] is not None else None,
                  "is_democratic": r["is_democratic"], "crisis": r["crisis"], "residual": round(r["residual"], 3)}
                 for r in decoupled], key=lambda d: d["dP1"]),
        }

    # Literal pre-registered criterion (non-discriminating — disclosed)
    literal = [r for r in recs if r["growth"] > 0.5 and r["dP1"] < 0.05]
    # Sharper cut: governance actually DECLINED while wealth grew substantially
    sharp = [r for r in recs if r["growth"] > 0.5 and r["dP1"] < -0.03]
    return {
        "n_balanced": len(recs), "gdp_only_crisis_auc": round(float(auc), 4),
        "literal_prereg": summarize("growth>50% AND dP1<0.05 (PRE-REGISTERED)", literal),
        "literal_note": ("Over the 28-yr window GDP-pc PPP grows >50% for nearly every country "
                         "while WGI-based P1 is sticky, so the pre-registered threshold is met by "
                         "69% of the panel and does not discriminate. Reported faithfully; the sharp "
                         "cut below isolates the meaningful 'wealth up, governance DOWN' set."),
        "sharp_governance_decline": summarize("growth>50% AND dP1<-0.03 (wealth up, governance down)", sharp),
    }


# ============================================================ Test 8
def coupling_pearson(pairs):
    if len(pairs) < 8:
        return None, len(pairs)
    xs = [p[0] for p in pairs]; ys = [p[1] for p in pairs]
    if np.std(xs) == 0 or np.std(ys) == 0:
        return None, len(pairs)
    return round(float(stats.pearsonr(xs, ys).statistic), 4), len(pairs)


def test8():
    pnl = L.load_mi_panel(); rows = pnl["rows"]
    wdi = L.load_wdi()
    years = [1996, 2024]
    forces = {}

    def force_split(name, exposed_fn, ref_year=2018):
        """P1<->logGDP coupling among exposed vs non-exposed at ref_year; exposure counts 1996 vs 2024."""
        exp_pairs, non_pairs = [], []
        for iso, r in rows.items():
            e = r["years"].get(str(ref_year))
            if not e or e.get("P1") is None or e.get("logGDP") is None:
                continue
            ex = exposed_fn(iso, ref_year)
            if ex is None:
                continue
            (exp_pairs if ex else non_pairs).append((e["P1"], e["logGDP"]))
        r_exp, n_exp = coupling_pearson(exp_pairs)
        r_non, n_non = coupling_pearson(non_pairs)
        # exposure counts over time
        counts = {}
        for y in years:
            c = 0; tot = 0
            for iso in rows:
                ex = exposed_fn(iso, y)
                if ex is not None:
                    tot += 1
                    if ex:
                        c += 1
            counts[y] = {"n_exposed": c, "n_total": tot}
        weaker = (r_exp is not None and r_non is not None and r_exp < r_non)
        return {"ref_year": ref_year, "coupling_exposed": r_exp, "n_exposed_set": n_exp,
                "coupling_non_exposed": r_non, "n_non_set": n_non,
                "coupling_weaker_when_exposed": bool(weaker),
                "exposure_counts": counts,
                "exposure_growing": bool(counts[years[-1]]["n_exposed"] > counts[years[0]]["n_exposed"])}

    # a. resource rents > 10%
    def f_resource(iso, y):
        v = resource_rents(iso, y)
        return None if v is None else v > 10
    forces["a_resource_rents>10%"] = force_split("resource", f_resource)

    # b. FDI net inflows > 5%
    def f_fdi(iso, y):
        v = L.wdi_val(wdi, "fdi_net_inflow_pct_gdp", iso, y)
        return None if v is None else v > 5
    forces["b_FDI>5%"] = force_split("fdi", f_fdi)

    # c. financialization: private credit > 100% GDP (deep financial sector)
    def f_fin(iso, y):
        v = L.wdi_val(wdi, "private_credit_pct_gdp", iso, y)
        return None if v is None else v > 100
    forces["c_private_credit>100%"] = force_split("financialization", f_fin)

    # d. digital/ICT: NO committed ICT-service-export indicator. Proxy = services share > 60%
    # (documented gap; services-heavy economies as the closest available signal).
    def f_svc(iso, y):
        v = L.wdi_val(wdi, "services_pct_gdp", iso, y)
        return None if v is None else v > 60
    forces["d_services>60%_(ICT_proxy)"] = force_split("services", f_svc)

    return {"forces": forces,
            "ICT_gap_note": "No ICT-service-exports indicator is committed; the digital force is proxied by services>60% GDP and flagged as a gap, not a measurement of ICT decoupling."}


def main():
    out = {"test7_coupling_fragility": test7(), "test8_decoupling_forces": test8()}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1))

    t7 = out["test7_coupling_fragility"]
    print("=== TEST 7 — GDP-P1 coupling fragility (1996->2024) ===")
    print(f"  balanced={t7['n_balanced']}  gdp-only crisis AUC={t7['gdp_only_crisis_auc']}")
    for key in ["literal_prereg", "sharp_governance_decline"]:
        s = t7[key]
        print(f"  [{s['criterion']}]")
        print(f"     n_decoupled={s['n_decoupled']} (share={s['decoupled_share']}) outliers={s['outlier_breakdown']}")
        print(f"     crisis residual: decoupled={s['mean_residual_decoupled']} vs coupled={s['mean_residual_coupled']} "
              f"(decoupled crisis MORE: {s['decoupled_crisis_more_than_gdp_predicts']})")
    print(f"  NOTE: {t7['literal_note']}")
    print("  sharp-cut countries (governance down, wealth up):")
    for d in t7["sharp_governance_decline"]["countries"]:
        print(f"    {d['name']:<22} g={d['growth_pct']:>6}%  dP1={d['dP1']:+.3f}  res={d['resource_rents']}  "
              f"democ={d['is_democratic']}  crisis={d['crisis']}  resid={d['residual']:+.2f}")

    t8 = out["test8_decoupling_forces"]
    print("\n=== TEST 8 — decoupling forces (P1<->GDP coupling, exposed vs non-exposed @2018) ===")
    for name, f in t8["forces"].items():
        print(f"  {name}: exposed r={f['coupling_exposed']} (n={f['n_exposed_set']}) | "
              f"non-exposed r={f['coupling_non_exposed']} (n={f['n_non_set']}) | "
              f"weaker={f['coupling_weaker_when_exposed']} | "
              f"exposure {f['exposure_counts'][1996]['n_exposed']}->{f['exposure_counts'][2024]['n_exposed']} "
              f"(growing={f['exposure_growing']})")


if __name__ == "__main__":
    main()
