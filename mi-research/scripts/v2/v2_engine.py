#!/usr/bin/env python3
"""
MI V2 engine — functional-conversion instrument (Level + Equity). Builds 6 pillars, each
an output/input Level ratio + an Equity dimension, geometric-mean composite; V2-Level,
V2-Equity, V2-Combined; three weighting schemes (V2a/b/c); track flags. Separate from the
frozen V1 engine. Frozen spec: docs/MI_V2_PREREGISTRATION.md (sha256 93c87741). Read-only.

Writes data/v2/v2_scores.json.
"""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
IND = json.loads((ROOT / "data/v2/v2_indicators.json").read_text())["series"]
OUT = ROOT / "data/v2/v2_scores.json"


def latest(iso, key, lo=2014, hi=2024):
    s = IND.get(key, {}).get(iso)
    if not s:
        return None
    for y in range(hi, lo - 1, -1):
        if str(y) in s:
            return s[str(y)]
    return None


def change5(iso, key):
    """5-yr change (latest minus ~5yr earlier)."""
    s = IND.get(key, {}).get(iso)
    if not s:
        return None
    yrs = sorted(int(y) for y in s)
    if not yrs:
        return None
    y1 = yrs[-1]
    prev = [y for y in yrs if y <= y1 - 4]
    if not prev:
        return None
    return s[str(y1)] - s[str(prev[-1])]


def all_isos():
    isos = set()
    for k, ser in IND.items():
        isos |= set(ser.keys())
    return sorted(i for i in isos if len(i) == 3 and not i.startswith("_"))


# ---------- raw ratio/level construction (direction-corrected: higher = better) ----------
def raw_level(iso):
    g = lambda k: latest(iso, k)
    gdp = g("gdp_pc_ppp")
    out = {}
    # F1 fiscal (collective sustainability measures)
    f1 = {}
    if g("f1_cash_bal_gdp") is not None:
        f1["cash_bal"] = g("f1_cash_bal_gdp")
    if g("f1_interest_rev") is not None:
        f1["interest"] = -g("f1_interest_rev")            # lower better
    dch = change5(iso, "f1_debt_gdp")
    if dch is not None:
        f1["debt_traj"] = -dch                             # rising debt bad
    out["F1"] = f1
    # F2 human development (conversion ratios, log input)
    f2 = {}
    hp = g("health_pc")
    if hp and hp > 0:
        li = math.log10(hp)
        if g("le") is not None:
            f2["health_le"] = g("le") / li
        if g("infant_mort") is not None:
            f2["health_infant"] = (100 - min(g("infant_mort"), 100)) / li
    ep = g("edu_pc_prim")
    if ep and ep > 0:
        le_ = math.log10(ep)
        if g("hci_lays") is not None:
            f2["edu_hci"] = g("hci_lays") / le_
        elif g("literacy") is not None:
            f2["edu_lit"] = (g("literacy") / 100) / le_
    out["F2"] = f2
    # F3 infrastructure
    f3 = {}
    if g("power_loss") is not None:
        f3["power"] = -g("power_loss")                     # lower loss better
    if g("water_smng") is not None:
        f3["water"] = g("water_smng")
    if g("lpi_infra") is not None:
        f3["lpi"] = g("lpi_infra")                         # perception-flagged
    if g("bbnd_p100") is not None and gdp and gdp > 0:
        f3["bbnd_conv"] = g("bbnd_p100") / math.log10(gdp)
    out["F3"] = f3
    # F4 security (degraded: homicide only; incarceration handled separately)
    f4 = {}
    if g("homicide") is not None:
        f4["safety"] = -math.log1p(g("homicide"))          # lower homicide better
    out["F4"] = f4
    # F5 environment
    f5 = {}
    if g("co2_gdp") is not None:
        f5["co2"] = -g("co2_gdp")                           # lower intensity better
    if g("pm25") is not None:
        f5["air"] = -math.log1p(g("pm25"))
    fch = change5(iso, "forest")
    if fch is not None:
        f5["forest_traj"] = fch
    rch = change5(iso, "renew")
    if rch is not None:
        f5["renew_traj"] = rch
    out["F5"] = f5
    # F6 social contract
    f6 = {}
    if g("oop_health") is not None:
        f6["oop"] = -g("oop_health")                        # lower OOP better
    if g("sp_cov") is not None:
        f6["sp_cov"] = g("sp_cov")
    out["F6"] = f6
    return out


def raw_equity(iso):
    g = lambda k: latest(iso, k)
    out = {}
    # income anchor (proxy for F1/F4/F6): 100 - Gini
    gini = g("gini")
    income_eq = (100 - gini) if gini is not None else None
    # F2 health equity (Q1 poorest / Q5 richest; stunting inverted)
    def ratio(q1, q5, invert=False):
        a, b = g(q1), g(q5)
        if a is None or b is None or b == 0:
            return None
        r = (b / a) if invert else (a / b)
        return min(r, 1.0) * 100
    f2e = [x for x in [ratio("eq_measles_q1", "eq_measles_q5"),
                       ratio("eq_birth_q1", "eq_birth_q5"),
                       ratio("eq_antenatal_q1", "eq_antenatal_q5"),
                       ratio("eq_stunt_q1", "eq_stunt_q5", invert=True)] if x is not None]
    # F3 infra equity (rural/urban)
    def ru(r, u):
        a, b = g(r), g(u)
        if a is None or b is None or b == 0:
            return None
        return min(a / b, 1.0) * 100
    f3e = [x for x in [ru("elc_rural", "elc_urban"), ru("water_rural", "water_urban"),
                       ru("cleanfuel_rural", "cleanfuel_urban")] if x is not None]
    # F5 equity (clean fuel gap)
    f5e = [x for x in [ru("cleanfuel_rural", "cleanfuel_urban")] if x is not None]
    out["F2"] = np.mean(f2e) if f2e else None
    out["F3"] = np.mean(f3e) if f3e else None
    out["F5"] = np.mean(f5e) if f5e else None
    out["F1"] = income_eq   # proxy
    out["F4"] = income_eq   # proxy
    out["F6"] = income_eq   # proxy
    out["_income_anchor"] = income_eq
    out["_f2_real"] = bool(f2e)
    out["_f3_real"] = bool(f3e)
    return out


def normalize_5_95(values):
    """min-max anchored to 5th/95th pct; returns func mapping raw->0..100."""
    arr = np.array([v for v in values if v is not None], float)
    if len(arr) < 8:
        return None
    lo, hi = np.percentile(arr, 5), np.percentile(arr, 95)
    if hi == lo:
        return None
    return lambda v: float(np.clip((v - lo) / (hi - lo) * 100, 0, 100))


def cap95(values):
    arr = np.array([v for v in values if v is not None], float)
    return float(np.percentile(arr, 95)) if len(arr) >= 8 else None


def build():
    isos = all_isos()
    # raw level/equity per country
    rl = {i: raw_level(i) for i in isos}
    re = {i: raw_equity(i) for i in isos}

    # cap ratio indicators at 95th pct (F2 conversion ratios), then normalize each sub-indicator
    pillars = ["F1", "F2", "F3", "F4", "F5", "F6"]
    subkeys = {p: sorted({k for i in isos for k in rl[i].get(p, {})}) for p in pillars}

    # apply 95th caps to F2 conversion ratios
    for p in ["F2"]:
        for k in subkeys[p]:
            cap = cap95([rl[i][p].get(k) for i in isos])
            if cap:
                for i in isos:
                    if k in rl[i][p]:
                        rl[i][p][k] = min(rl[i][p][k], cap)

    # normalizers per sub-indicator
    norml = {}
    for p in pillars:
        for k in subkeys[p]:
            norml[(p, k)] = normalize_5_95([rl[i][p].get(k) for i in isos])
    # equity normalizers per pillar
    norme = {p: normalize_5_95([re[i].get(p) for i in isos]) for p in pillars}

    scored = {}
    for i in isos:
        rec = {"pillars": {}, "tracks": {}}
        # Level per pillar
        Lvals = {}
        for p in pillars:
            comp = []
            for k, v in rl[i].get(p, {}).items():
                f = norml.get((p, k))
                if f and v is not None:
                    comp.append(f(v))
            Lvals[p] = float(np.mean(comp)) if comp else None
        # Equity per pillar
        Evals = {}
        for p in pillars:
            v = re[i].get(p)
            f = norme.get(p)
            Evals[p] = f(v) if (f and v is not None) else None
        # pillar composite
        for p in pillars:
            L, E = Lvals[p], Evals[p]
            if L is None:
                score = None
            elif E is None:
                score = L  # level-only, flagged
            elif p == "F1":
                score = 0.70 * L + 0.30 * E
            else:
                score = math.sqrt(max(L, 0) * max(E, 0))
            equity_real = (re[i].get("_f2_real") if p == "F2" else
                           re[i].get("_f3_real") if p in ("F3", "F5") else
                           (E is not None and p in ("F1", "F4", "F6") and "proxy"))
            rec["pillars"][p] = {"L": round(L, 1) if L is not None else None,
                                 "E": round(E, 1) if E is not None else None,
                                 "score": round(score, 1) if score is not None else None,
                                 "equity_source": ("real" if equity_real is True else
                                                   "proxy(income)" if equity_real == "proxy" else
                                                   "none")}
        # overall
        Ls = [Lvals[p] for p in pillars if Lvals[p] is not None]
        Es = [Evals[p] for p in pillars if Evals[p] is not None]
        Ss = [rec["pillars"][p]["score"] for p in pillars if rec["pillars"][p]["score"] is not None]
        v2L = float(np.mean(Ls)) if len(Ls) >= 4 else None
        v2E = float(np.mean(Es)) if len(Es) >= 3 else None
        v2C = math.sqrt(v2L * v2E) if (v2L is not None and v2E is not None) else None
        n_pillars = len(Ss)
        track = "T1" if n_pillars == 6 else "T2" if n_pillars >= 4 else "T3"
        rec.update({"V2_Level": round(v2L, 1) if v2L is not None else None,
                    "V2_Equity": round(v2E, 1) if v2E is not None else None,
                    "V2_Combined": round(v2C, 1) if v2C is not None else None,
                    "n_pillars": n_pillars, "track": track,
                    "_L": Lvals, "_E": Evals})
        scored[i] = rec

    out = {"_meta": {"prereg_sha256": "93c87741", "n_countries": len(scored),
                     "pillars": pillars}, "scores": scored}
    OUT.write_text(json.dumps(out, indent=1))
    # summary
    t1 = sum(1 for r in scored.values() if r["track"] == "T1")
    withL = sum(1 for r in scored.values() if r["V2_Level"] is not None)
    withE = sum(1 for r in scored.values() if r["V2_Equity"] is not None)
    withC = sum(1 for r in scored.values() if r["V2_Combined"] is not None)
    f2real = sum(1 for r in scored.values() if r["pillars"]["F2"]["equity_source"] == "real")
    print(f"scored {len(scored)} countries | Track1={t1} | V2-Level={withL} V2-Equity={withE} V2-Combined={withC}")
    print(f"F2 real (non-proxy) equity: {f2real} countries")
    # show a few known cases
    for i in ["USA", "NLD", "DNK", "NOR", "CHE", "CRI", "BRA", "ZAF", "SGP", "DEU", "GBR"]:
        if i in scored:
            r = scored[i]
            print(f"  {i}: L={r['V2_Level']} E={r['V2_Equity']} C={r['V2_Combined']} track={r['track']} "
                  f"(F2 L/E={r['pillars']['F2']['L']}/{r['pillars']['F2']['E']}[{r['pillars']['F2']['equity_source']}])")


if __name__ == "__main__":
    build()
