#!/usr/bin/env python3
"""ESI Phase 1 — build the External Support Index per config/esi.json (frozen spec).

Combines the WB raw cache (esi_wb_raw.json) + manual coding (manual_coding.json)
into per-country-year ESI scores at the temporal-holdout base years (2004, 2012).

Aggregation (frozen, NOT optimized): within each sub-dimension, mean of AVAILABLE
normalized indicators; ESI = equal-weight mean of the available sub-dimensions.
All indicators in [0,1], higher = more support. Track-2: degrade gracefully, no imputation.

    python scripts/robustness/esi_build.py
"""
import json
import sys
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config  # noqa: E402

ESIDIR = ROOT / "data" / "robustness" / "esi"
WB_RAW = ESIDIR / "esi_wb_raw.json"
MANUAL = ESIDIR / "manual_coding.json"
OUT = ESIDIR / "esi_scores.json"
PANEL = ROOT / "data" / "robustness" / "temporal_holdout_panel.json"

YEARS = [2004, 2012]
FALLBACK = 3           # nearest-year search radius for WB values
PCTL_CEILING = 0.90    # ceiling = 90th percentile of pooled distribution (spec)


def nearest(values_by_year, target, radius=FALLBACK):
    """Value at target year, else nearest within +/-radius (closest wins, earlier on tie)."""
    if not values_by_year:
        return None
    yv = {int(y): v for y, v in values_by_year.items()}
    if target in yv:
        return yv[target]
    for d in range(1, radius + 1):
        for cand in (target - d, target + d):
            if cand in yv:
                return yv[cand]
    return None


def pooled_ceiling(pairs):
    """90th-percentile ceiling over a list of non-null, non-negative values."""
    xs = sorted(v for v in pairs if v is not None)
    if not xs:
        return None
    idx = min(len(xs) - 1, int(round(PCTL_CEILING * (len(xs) - 1))))
    return xs[idx] or 1.0


def clamp01(x):
    return max(0.0, min(1.0, x))


def main():
    wb = json.loads(WB_RAW.read_text())["indicators"]
    manual = json.loads(MANUAL.read_text())["countries"]
    panel = json.loads(PANEL.read_text())
    isos = sorted({r["iso"] for w in panel["windows"].values() for r in w})

    def wb_val(key, iso, year):
        d = wb.get(key, {}).get("values", {}).get(iso)
        return nearest(d, year) if d else None

    # --- ceilings from pooled panel distribution (documented) ---
    from mi.constants import LENS
    ODA_FULL = LENS["oda_full_dependence_pct"]  # 20.0 (mirror MI normalizer scale, un-inverted)

    def collect(key, transform=lambda v: v):
        out = []
        for iso in isos:
            for y in YEARS:
                v = wb_val(key, iso, y)
                if v is not None:
                    out.append(transform(v))
        return out

    fdi_ceil = pooled_ceiling(collect("fdi_net_inflows_pct_gdp", lambda v: max(0.0, v)))
    rem_ceil = pooled_ceiling(collect("remittances_pct_gdp", lambda v: max(0.0, v)))
    res_ceil = pooled_ceiling(collect("reserves_months_imports", lambda v: max(0.0, v)))
    swf_vals = [manual.get(iso, {}).get("swf_assets_pct_gdp", {}).get(str(y))
                for iso in isos for y in YEARS]
    swf_ceil = pooled_ceiling([v for v in swf_vals if v])

    ceilings = {"fdi_pct_gdp": fdi_ceil, "remittances_pct_gdp": rem_ceil,
                "reserves_months_imports": res_ceil, "swf_assets_pct_gdp": swf_ceil,
                "oda_full_dependence_pct": ODA_FULL, "percentile": PCTL_CEILING}

    def m(iso, field, year):
        return manual.get(iso, {}).get(field, {}).get(str(year))

    records = {}
    for iso in isos:
        by_year = {}
        for y in YEARS:
            # ----- Sub-A: Financial Life Support (primary: imf_active, imf_cumulative, concessional) -----
            a = {}
            imf_act = m(iso, "imf_program_active", y)
            if imf_act is not None:
                a["imf_program_active"] = clamp01(float(imf_act))
            imf_cum = m(iso, "imf_cumulative_years_20yr", y)
            if imf_cum is not None:
                a["imf_cumulative_20yr"] = clamp01(imf_cum / 20.0)
            conc = wb_val("concessional_debt_share", iso, y)
            if conc is not None:
                a["concessional_debt_share"] = clamp01(conc / 100.0)

            # ----- Sub-B: Structural Dependency (fdi, oda un-inverted, remittances) -----
            b = {}
            fdi = wb_val("fdi_net_inflows_pct_gdp", iso, y)
            if fdi is not None and fdi_ceil:
                b["fdi_net_inflows_pct_gdp"] = clamp01(max(0.0, fdi) / fdi_ceil)
            oda = wb_val("oda_pct_gni", iso, y)
            if oda is not None:
                b["oda_pct_gni"] = clamp01(max(0.0, oda) / ODA_FULL)
            rem = wb_val("remittances_pct_gdp", iso, y)
            if rem is not None and rem_ceil:
                b["remittances_pct_gdp"] = clamp01(max(0.0, rem) / rem_ceil)

            # ----- Sub-C: Systemic Insurance (reserve ccy, EU, NATO, SWF, reserves) -----
            c = {}
            for field, key in (("reserve_currency", "reserve_currency"),
                               ("eu_eurozone", "eu_eurozone"),
                               ("nato_alliance", "nato_alliance")):
                v = m(iso, field, y)
                if v is not None:
                    c[key] = clamp01(float(v))
            swf = m(iso, "swf_assets_pct_gdp", y)
            if swf is not None and swf_ceil:
                c["swf_assets_pct_gdp"] = clamp01(swf / swf_ceil)
            res = wb_val("reserves_months_imports", iso, y)
            if res is not None and res_ceil:
                c["reserves_months_imports"] = clamp01(max(0.0, res) / res_ceil)

            subs = {}
            if a:
                subs["A_financial_life_support"] = round(mean(a.values()), 4)
            if b:
                subs["B_structural_dependency"] = round(mean(b.values()), 4)
            if c:
                subs["C_systemic_insurance"] = round(mean(c.values()), 4)
            esi = round(mean(subs.values()), 4) if subs else None
            by_year[y] = {
                "ESI": esi,
                "sub_dimensions": subs,
                "n_sub_available": len(subs),
                "indicators": {"A": {k: round(v, 4) for k, v in a.items()},
                               "B": {k: round(v, 4) for k, v in b.items()},
                               "C": {k: round(v, 4) for k, v in c.items()}},
            }
        records[iso] = by_year

    payload = {
        "_meta": {
            "workstream": "ESI_build",
            "spec": "config/esi.json",
            "prereg": "docs/ESI_PREREGISTRATION.md",
            "years": YEARS,
            "n_countries": len(isos),
            "aggregation": "sub-dim = mean of available indicators; ESI = mean of available sub-dims (equal weight, un-tuned)",
            "ceilings_documented": {k: (round(v, 4) if isinstance(v, float) else v) for k, v in ceilings.items()},
            "excluded_from_primary": ["debt_service_pct_gni (sign-ambiguous)", "export_partner_hhi (deferred)"],
        },
        "esi": records,
    }
    OUT.write_text(json.dumps(payload, indent=1))
    # coverage summary
    for y in YEARS:
        scored = [iso for iso in isos if records[iso][y]["ESI"] is not None]
        full3 = [iso for iso in isos if records[iso][y]["n_sub_available"] == 3]
        print(f"{y}: ESI scored {len(scored)}/{len(isos)} countries; {len(full3)} with all 3 sub-dims")
    print(f"ceilings: FDI={fdi_ceil}, remit={rem_ceil}, reserves={res_ceil}, swf={swf_ceil}")
    print(f"-> {OUT.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
