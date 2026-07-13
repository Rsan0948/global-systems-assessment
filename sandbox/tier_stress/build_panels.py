#!/usr/bin/env python3
"""
build_panels.py — MECHANICAL panel construction for a predictive-reach screen.

Builds:
  predictors.json  = {iso: {year: {field: value}}}     years 1996..2024
  outcomes.json    = {iso: {year: {field: value}}}      years 1996..2025
  panels_coverage.json + printed coverage summary

Predictor instruments (each scored AT year T, not just 2024):
  V1  : the real MI engine (mi.panel + mi.scoring)
  V3  : grievance/mobilization numerator (mirror scripts/v2/political_test.py)
  T4  : structural scarring     (mirror scripts/v2/tier4_scarring.py)
  T5  : criticality turbulence  (mirror scripts/v2/csd_corrected.py)
  T6  : spark density           (mirror scripts/v2/tier6_spark.py)
  DGS : fragmentation leg (governance/political dgs_panel_real.json, iso recovered
        by population fingerprint since the cached panel dropped the iso column)

NO statistics / correlations / AUC computed here. Panels + coverage only.
Run from the mi-research/ directory:  python <this>/build_panels.py
Read-only w.r.t. mi/, data/, scripts/. Outputs written next to this script.
"""
from __future__ import annotations
import sys, os, json, math, csv
from collections import defaultdict

sys.path.insert(0, ".")
sys.path.insert(0, "scripts/robustness")

import numpy as np
import convergence_lib as L
from mi import panel as MP
from mi.scoring import calculate_pillar_scores, calculate_mi_score

ROOT = os.path.abspath(".")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
DGS_PANEL = "/Users/rubensanchez/Developer/usg-sandbox-wt/fragmentation/governance/political/results/dgs_panel_real.json"

PRED_YEARS = list(range(1996, 2025))      # 1996..2024
PRED_YEARS_SET = set(PRED_YEARS)
OUT_YEARS = list(range(1996, 2026))       # 1996..2025

# ---------------------------------------------------------------- helpers
def load(p):
    with open(p) as f:
        return json.load(f)

def near(d, iso, y, tol=3):
    """political_test.py near() helper: value at year y within +/-tol, nearest first."""
    s = d.get(iso) if isinstance(d, dict) else None
    if not s:
        return None
    if all(str(k).isdigit() for k in s):
        s = {int(k): v for k, v in s.items()}
    for dd in range(tol + 1):
        for yy in ([y] if dd == 0 else [y - dd, y + dd]):
            if yy in s:
                return s[yy]
    return None

def zcol(values):
    """z-score a cross-section that may contain None -> mean-impute None (z~0), return per-row z.
    Returns (list_of_z_or_None_if_all_missing, set_of_indices_imputed)."""
    obs = [v for v in values if v is not None]
    if len(obs) < 2:
        return [None] * len(values), set()
    mu = float(np.mean(obs)); sd = float(np.std(obs))
    if sd <= 0:
        return [0.0 if v is not None else 0.0 for v in values], {i for i, v in enumerate(values) if v is None}
    imp = {i for i, v in enumerate(values) if v is None}
    out = [((v if v is not None else mu) - mu) / sd for v in values]
    return out, imp

# ---------------------------------------------------------------- sources
POL = load("data/political/political_indicators.json")["series"]
EXO = load("data/v2/exploratory_outcomes.json")["series"]
VDEM = load("data/v2/vdem_democracy.json")["series"]
LIB = VDEM["libdem"]; ELE = VDEM["electdem"]; ROL = VDEM["rol_vdem"]
T4D = load("data/political/tier4_indicators.json")["series"]
T6D = load("data/political/tier6_indicators.json")["series"]
BORDERS_CACHE = load("data/political/_borders_cache.json")   # committed adjacency (ISO3)
ADJ = {k: set(v) for k, v in BORDERS_CACHE["adj"].items()}

dom = L.domestic_years()                                     # {iso: set(onset_years)}

# universe of isos from the MI panel (extract iso from the (iso,name,name,ind,tier) tuples)
UNIVERSE = sorted({t[0] for t in MP.iter_universe()})

def decayed_conflict(iso, T, halflife=25.0):
    """sum over past onset years y<=T of 0.5**((T-y)/halflife) (V3/T4 event-history leg)."""
    ys = dom.get(iso, set())
    return sum(0.5 ** ((T - y) / halflife) for y in ys if y <= T)

# ================================================================ PREDICTORS
predictors = {iso: {} for iso in UNIVERSE}

# ---- V1: real engine, per (iso, T) -------------------------------------
v1_fail = 0
for iso in UNIVERSE:
    for T in PRED_YEARS:
        try:
            ind = MP.indicators_for(iso, T)
            if not ind:
                continue
            pil = calculate_pillar_scores(ind)
            mi = calculate_mi_score(pil)
            rec = {}
            if mi is not None:
                rec["v1_mi"] = float(mi)
            for p in ("P1", "P2", "P3", "P4", "P5"):
                if pil.get(p) is not None:
                    rec[p] = float(pil[p])
            if pil.get("P4") is not None and pil.get("P1") is not None:
                rec["durgap"] = float(pil["P4"] - pil["P1"])
            if rec:
                predictors[iso].setdefault(T, {}).update(rec)
        except Exception:
            v1_fail += 1
            continue

# ---- V3 numerator (mirror political_test.py), per (iso, T) --------------
# raw sub-components first, then per-year cross-sectional z -> v3_numer
V3_COMPS = ["anocracy", "cso", "pts", "youth", "food_imp", "internet", "growth_vol", "prior_conflict_decayed"]
v3_raw = {T: {} for T in PRED_YEARS}   # T -> iso -> {comp: val}
for iso in UNIVERSE:
    for T in PRED_YEARS:
        lib = near(LIB, iso, T, tol=3)
        anocracy = 4 * lib * (1 - lib) if lib is not None else None
        # growth_vol: std of gdp_pc_growth over 13 years ending at T, need >=5
        gser = EXO.get("gdp_pc_growth", {}).get(iso, {})
        gvals = [gser.get(str(y)) for y in range(T - 12, T + 1)]
        gvals = [x for x in gvals if x is not None]
        growth_vol = float(np.std(gvals)) if len(gvals) >= 5 else None
        comp = {
            "anocracy": anocracy,
            "cso": near(POL.get("cso_participation", {}), iso, T, tol=3),
            "pts": near(POL.get("pts", {}), iso, T, tol=3),
            "youth": near(POL.get("youth_0014", {}), iso, T, tol=3),
            "food_imp": near(POL.get("food_imports", {}), iso, T, tol=3),
            "internet": near(POL.get("internet", {}), iso, T, tol=3),
            "growth_vol": growth_vol,
            "prior_conflict_decayed": decayed_conflict(iso, T),
        }
        v3_raw[T][iso] = comp

# per-year z of each component, then row-mean of available z -> v3_numer
for T in PRED_YEARS:
    isos = UNIVERSE
    zmats = {}
    for c in V3_COMPS:
        col = [v3_raw[T][iso][c] for iso in isos]
        z, _ = zcol(col)
        zmats[c] = z
    for i, iso in enumerate(isos):
        raw = v3_raw[T][iso]
        rec = {}
        for c in V3_COMPS:
            if raw[c] is not None:
                rec[c] = float(raw[c])
        zs = [zmats[c][i] for c in V3_COMPS if raw[c] is not None and zmats[c][i] is not None]
        if zs:
            rec["v3_numer"] = float(np.mean(zs))
        if rec:
            predictors[iso].setdefault(T, {}).update(rec)

# ---- T4 scarring (mirror tier4_scarring.py) ----------------------------
# sub-components: decayed_conflict, reversed_trust(100-trust), refugees_share, pts(state perp)
# z-sum across isos at each year; mean-impute missing within the year cross-section (H5 fix).
T4_IMPUTED = defaultdict(lambda: defaultdict(int))  # comp -> year -> n_imputed
POP4 = T4D.get("population", {}); REFO = T4D.get("refugees_origin", {}); TRUST = T4D.get("trust", {})
PTS = POL.get("pts", {})
for T in PRED_YEARS:
    isos = UNIVERSE
    raw = {}
    for iso in isos:
        tr = near(TRUST, iso, T, tol=8)
        rf = near(REFO, iso, T, tol=4); pp = near(POP4, iso, T, tol=2)
        refshare = (rf / pp * 100) if (rf is not None and pp) else None
        raw[iso] = {
            "t4_decayed_conflict": decayed_conflict(iso, T),
            "t4_reversed_trust": (100 - tr) if tr is not None else None,
            "t4_refugee_share": refshare,
            "t4_pts": near(PTS, iso, T, tol=3),
        }
    comps = ["t4_decayed_conflict", "t4_reversed_trust", "t4_refugee_share", "t4_pts"]
    zmats = {}
    for c in comps:
        col = [raw[iso][c] for iso in isos]
        z, imp = zcol(col)
        zmats[c] = z
        T4_IMPUTED[c][T] = len(imp)
    for i, iso in enumerate(isos):
        rec = {}
        for c in comps:
            if raw[iso][c] is not None:
                rec[c] = float(raw[iso][c])
        # z-sum over ALL comps (missing mean-imputed to ~0 per H5 fix) if any component present
        if any(raw[iso][c] is not None for c in comps):
            rec["t4_scar"] = float(sum(zmats[c][i] for c in comps if zmats[c][i] is not None))
        if rec:
            predictors[iso].setdefault(T, {}).update(rec)

# ---- T5 turbulence (mirror csd_corrected.py) ---------------------------
def turb(series, iso, T, W=10, need=6):
    s = series.get(iso, {})
    vals = [s.get(str(y)) for y in range(T - W + 1, T + 1)]
    vals = [v for v in vals if v is not None]
    return float(np.std(vals)) if len(vals) >= need else None
for iso in UNIVERSE:
    for T in PRED_YEARS:
        rec = {}
        tl = turb(LIB, iso, T); te = turb(ELE, iso, T)
        if tl is not None:
            rec["t5_turb_libdem"] = tl
        if te is not None:
            rec["t5_turb_electdem"] = te
        if rec:
            predictors[iso].setdefault(T, {}).update(rec)

# ---- T6 spark (mirror tier6_spark.py) ----------------------------------
# Static hand-coded dims from the script (S3 transcendent, deterrence, coup, strategic-resource).
S3_HAND = {"ISR":100,"PSE":95,"IND":85,"TWN":90,"CHN":70,"IRQ":72,"UKR":72,"RUS":62,"SAU":68,"IRN":58,
"TUR":52,"SYR":58,"ARM":55,"AZE":50,"CYP":58,"XKX":58,"SRB":45,"PAK":58,"MAR":48,"LBN":48,"GEO":45,
"JOR":48,"EGY":42,"BIH":42,"MDA":42,"GRC":38,"ITA":40,"NPL":34,"LKA":36,"MMR":42,"ESP":35,"ETH":40,
"YEM":36,"AFG":45,"SDN":38,"KOR":35,"PRK":35,"VAT":60,"KHM":30,"THA":28,"COD":30,"MLI":30,"SOM":32}
NATO = {"USA","GBR","FRA","DEU","ITA","ESP","POL","ROU","NLD","BEL","GRC","PRT","CZE","HUN","SVK","BGR",
"HRV","SVN","LTU","LVA","EST","DNK","NOR","ISL","LUX","ALB","MNE","MKD","TUR","CAN","FIN","SWE"}
US_TREATY = {"JPN","KOR","AUS","PHL","THA","NZL"}
NUCLEAR = {"USA","RUS","CHN","GBR","FRA","IND","PAK","ISR","PRK"}
MAJOR_ALLY = {"ISR":85,"TWN":80,"JOR":70,"EGY":70,"QAT":75,"KWT":75,"SAU":70,"ARE":75,"BHR":75,"UKR":60,
"KAZ":50,"SGP":65,"MAR":55,"TUN":45,"COL":55,"ARG":45,"BRA":40,"VNM":40}
def deter(i):
    if i in NATO or i in US_TREATY or i in NUCLEAR: return 100
    if i in MAJOR_ALLY: return MAJOR_ALLY[i]
    if i in {"MDA","SRB","BIH","GEO","ARM","AZE"}: return 30
    return 15
COUP = {"THA":90,"SDN":95,"MMR":90,"MLI":90,"BFA":92,"NER":85,"GIN":88,"PAK":82,"TUR":70,"EGY":72,
"BGD":62,"NGA":55,"GHA":45,"MRT":75,"GNB":88,"TCD":70,"CAF":70,"COD":55,"HTI":70,"FJI":80,"COM":85,
"MDG":55,"HND":50,"BOL":55,"VEN":45,"GTM":45,"PER":40,"ECU":40,"ZWE":40,"UGA":45,"SSD":60,"LBY":55,
"IRQ":50,"SYR":45,"YEM":55,"AFG":60,"GNQ":45,"GAB":55,"TGO":50,"BEN":40,"BDI":55,"RWA":45,"NPL":40}
STRAT = {"SAU":90,"RUS":85,"IRN":85,"IRQ":85,"VEN":80,"KWT":85,"ARE":80,"QAT":85,"NGA":75,"AGO":70,
"LBY":80,"KAZ":80,"DZA":75,"AZE":70,"COD":85,"BOL":60,"CHL":65,"ARG":50,"AUS":55,"NOR":55,"GNQ":70,
"TCD":50,"SSD":70,"YEM":45,"OMN":70,"TKM":75,"BRN":75,"EGY":60,"PAN":70,"SGP":55,"DJI":55,"TUR":45}
MIL = T6D.get("mil_spend", {}); RRENT = T6D.get("resource_rents_total", {}); REFH = T6D.get("refugees_hosted", {})
for T in PRED_YEARS:
    isos = UNIVERSE
    raw = {}
    for iso in isos:
        # S1 geographic: refugee-share (time-varying) + maritime insulation (static border count)
        rh = near(REFH, iso, T, tol=3); pp = near(POP4, iso, T, tol=2)
        refshare = min(rh / pp * 100, 30) if (rh and pp) else 0.0
        nland = len(ADJ.get(iso, set()))
        maritime = 1.0 if nland == 0 else max(0.0, 1 - nland / 8)
        s1 = 0.25 * (refshare / 30 * 100) + 0.20 * (1 - maritime) * 60   # neighbour-contagion term omitted
        # S2 resource: rents (time-varying) + strategic-resource hand value
        rr = near(RRENT, iso, T, tol=3) or 0.0
        s2 = min(rr * 3, 100) * 0.5 + STRAT.get(iso, 0) * 0.5
        # S3 transcendent (static hand)
        s3 = float(S3_HAND.get(iso, 3))
        # S4 military net = internal(coup + mil_spend) x (1 - deterrence)
        ms = near(MIL, iso, T, tol=3)
        ms = ms if ms is not None else 1.5
        internal = 0.5 * COUP.get(iso, 8) + 0.5 * min(ms * 8, 100)
        s4 = internal * (1 - deter(iso) / 100)
        raw[iso] = {"t6_s1_geo": s1, "t6_s2_resource": s2, "t6_s3_transcendent": s3, "t6_s4_military": s4}
    comps = ["t6_s1_geo", "t6_s2_resource", "t6_s3_transcendent", "t6_s4_military"]
    zmats = {}
    for c in comps:
        z, _ = zcol([raw[iso][c] for iso in isos])
        zmats[c] = z
    for i, iso in enumerate(isos):
        rec = {c: float(raw[iso][c]) for c in comps}
        zs = [zmats[c][i] for c in comps if zmats[c][i] is not None]
        if zs:
            rec["t6_spark"] = float(sum(zs))
        predictors[iso].setdefault(T, {}).update(rec)

# ---- DGS (fragmentation leg): recover iso by population fingerprint -----
# The cached dgs_panel_real.json DROPPED the iso column; _meta has no per-row iso.
# Recover iso by matching each row's log_pop (== log(SP.POP.TOTL)) to log(tier4 population)
# at the same anchor period (near-exact, tol 1e-3), disambiguating ties by GDPpcPPP then by
# cross-period consistency. eci is NOT separable (only z(eci)-z(polyarchy) is stored).
DGS = load(DGS_PANEL)
try:
    import pycountry
    VALID_ISO3 = {c.alpha_3 for c in pycountry.countries}
except Exception:
    VALID_ISO3 = set(POP4.keys())  # fallback
# GDPpcPPP for tie-break (World Bank cached CSV)
WBC = defaultdict(dict)
try:
    with open("../mi-pipeline/data/wb_cached.csv") as f:
        for r in csv.DictReader(f):
            WBC[r["iso3"]][r["year"]] = r
except Exception:
    pass

dgs_rows = list(zip(DGS["dgs"], DGS["log_pop"], DGS["log_gdppc"], DGS["period"]))
# pass 1: unique/dominant population match
def pop_candidates(period, target_lp, tol=1e-3):
    P = str(period); c = []
    for iso, ser in POP4.items():
        if iso not in VALID_ISO3:
            continue
        v = ser.get(P)
        if v and v > 0:
            d = abs(math.log(v) - target_lp)
            if d < tol:
                c.append((iso, d))
    c.sort(key=lambda x: x[1])
    return c

assigned = [None] * len(dgs_rows)
dgs_ambiguous = 0; dgs_unmatched = 0
pending = []
for idx, (dv, lp, lg, per) in enumerate(dgs_rows):
    c = pop_candidates(per, lp)
    if not c:
        dgs_unmatched += 1
        continue
    if len(c) == 1 or c[1][1] - c[0][1] > 1e-3:
        assigned[idx] = c[0][0]
    else:
        pending.append((idx, per, lg, [x[0] for x in c]))

# confident-iso set for cross-period consistency
confident = {a for a in assigned if a}
for idx, per, lg, cands in pending:
    P = str(per)
    # tie-break 1: GDPpcPPP log-distance
    scored = []
    for iso in cands:
        r = WBC.get(iso, {}).get(P); g = r.get("GDPpcPPP") if r else None
        if g not in (None, ""):
            scored.append((iso, abs(math.log(float(g)) - lg)))
    scored.sort(key=lambda x: x[1])
    if len(scored) >= 2 and scored[1][1] - scored[0][1] > 0.15:
        assigned[idx] = scored[0][0]
        continue
    # tie-break 2: cross-period consistency (exactly one candidate seen confidently elsewhere)
    seen = [iso for iso in cands if iso in confident]
    if len(seen) == 1:
        assigned[idx] = seen[0]
        continue
    dgs_ambiguous += 1  # leave DGS null for this row

# broadcast each anchor's DGS to years [period, period+4] (window=5, non-overlapping anchors)
dgs_assigned_rows = 0
for idx, (dv, lp, lg, per) in enumerate(dgs_rows):
    iso = assigned[idx]
    if iso is None or iso not in predictors:
        continue
    dgs_assigned_rows += 1
    for T in range(per, per + 5):
        if T in PRED_YEARS_SET:
            predictors[iso].setdefault(T, {})["dgs"] = float(dv)

# ================================================================ OUTCOMES
outcomes = {iso: {} for iso in UNIVERSE}
EXO_FIELDS = ["gdp_pc_growth", "inflation", "gross_savings", "fdi_in", "gov_debt_chg",
              "net_migration", "fertility", "life_satisfaction", "suicide", "unemployment",
              "patents", "tourism_receipts", "brain_health_ratio"]
for iso in UNIVERSE:
    for T in OUT_YEARS:
        rec = {}
        # vdem levels (exact-year only; no near-fill for raw outcome levels)
        for fld, ser in (("libdem", LIB), ("electdem", ELE), ("rol_vdem", ROL)):
            v = ser.get(iso, {}).get(str(T))
            if v is not None:
                rec[fld] = float(v)
        # exploratory outcome levels
        for fld in EXO_FIELDS:
            v = EXO.get(fld, {}).get(iso, {}).get(str(T))
            if v is not None:
                rec[fld] = float(v)
        # exact-year domestic conflict onset flag
        rec["conflict_onset"] = 1 if T in dom.get(iso, set()) else 0
        if rec:
            outcomes[iso][T] = rec

# raw onset-year sets per iso (sorted lists for determinism) for windowed-onset derivation
conflict_onsets_by_iso = {iso: sorted(dom.get(iso, set())) for iso in UNIVERSE if dom.get(iso)}

# ================================================================ VALIDATION: V1 vs mi_5pt_panel
mi5 = load("data/robustness/decoupling/mi_5pt_panel.json")["rows"]
CHECK_YEARS = [1996, 2004, 2012, 2018, 2024]
# ~10 countries that appear in the 5pt panel with multiple years
cand = [i for i in ["EST", "NOR", "USA", "DEU", "FRA", "GBR", "JPN", "CHL", "POL", "ZAF",
                    "BRA", "IND", "MEX", "TUR", "KOR"] if i in mi5]
sanity = {"compared_cells": 0, "matched": 0, "max_abs_diff": 0.0, "mismatches": [], "countries": []}
for iso in cand:
    yrs = mi5[iso].get("years", {})
    for Y in CHECK_YEARS:
        ref = yrs.get(str(Y))
        if not ref:
            continue
        mine = predictors.get(iso, {}).get(Y, {})
        for p in ("P1", "P3", "P4"):
            rv = ref.get(p); mv = mine.get(p)
            if rv is None or mv is None:
                continue
            sanity["compared_cells"] += 1
            d = abs(float(rv) - float(mv))
            sanity["max_abs_diff"] = max(sanity["max_abs_diff"], d)
            if d <= 1e-4:
                sanity["matched"] += 1
            else:
                sanity["mismatches"].append({"iso": iso, "year": Y, "pillar": p,
                                             "ref": round(float(rv), 4), "mine": round(float(mv), 4),
                                             "diff": round(d, 4)})
    sanity["countries"].append(iso)

# ================================================================ COVERAGE
def field_coverage(panel, years):
    """field -> {n_cells, n_isos, year_min, year_max}."""
    stat = defaultdict(lambda: {"n_cells": 0, "isos": set(), "years": set()})
    for iso, ymap in panel.items():
        for y, rec in ymap.items():
            for fld, v in rec.items():
                if v is None:
                    continue
                s = stat[fld]
                s["n_cells"] += 1; s["isos"].add(iso); s["years"].add(int(y))
    out = {}
    for fld, s in stat.items():
        yrs = sorted(s["years"])
        out[fld] = {"n_cells": s["n_cells"], "n_isos": len(s["isos"]),
                    "year_span": [yrs[0], yrs[-1]] if yrs else None,
                    "flag_low_iso": len(s["isos"]) < 30}
    return out

pred_cov = field_coverage(predictors, PRED_YEARS)
out_cov = field_coverage(outcomes, OUT_YEARS)

# fully-instrumented core: (iso,year) with ALL of the 6 core instruments non-null
CORE = ["v1_mi", "v3_numer", "t4_scar", "t5_turb_libdem", "t6_spark", "dgs"]
total_pred_rows = sum(len(ymap) for ymap in predictors.values())
core_rows = 0
for iso, ymap in predictors.items():
    for y, rec in ymap.items():
        if all(rec.get(c) is not None for c in CORE):
            core_rows += 1

coverage = {
    "years_predictors": [PRED_YEARS[0], PRED_YEARS[-1]],
    "years_outcomes": [OUT_YEARS[0], OUT_YEARS[-1]],
    "n_isos_universe": len(UNIVERSE),
    "predictor_fields": pred_cov,
    "outcome_fields": out_cov,
    "total_predictor_rows": total_pred_rows,
    "fully_instrumented_core_rows": core_rows,
    "core_fields": CORE,
    "v1_engine_failures": v1_fail,
    "v1_sanity_check": sanity,
    "dgs_recovery": {
        "n_rows_total": len(dgs_rows),
        "n_rows_assigned_iso": dgs_assigned_rows,
        "n_unmatched": dgs_unmatched,
        "n_ambiguous_left_null": dgs_ambiguous,
        "method": "population-fingerprint (log SP.POP.TOTL, tol 1e-3) + GDPpcPPP/cross-period tie-break",
        "granularity": "5-year anchors {1996,2001,2006,2011,2016}; each broadcast to [anchor, anchor+4]",
        "eci_separable": False,
    },
    "t4_imputed_per_year": {c: dict(sorted(T4_IMPUTED[c].items())) for c in T4_IMPUTED},
    "notes": [
        "V3 EPR ethnic-exclusion component OMITTED (needs live ICR network fetch).",
        "T4 uses z-sum of [decayed_conflict, reversed_trust(100-trust), refugee_share, pts]; "
        "missing components mean-imputed within each year's cross-section (audit H5 fix).",
        "T6 uses z-sum of [s1_geo(refugee-share+maritime), s2_resource(rents+STRAT), "
        "s3_transcendent(hand), s4_military(coup+mil_spend x (1-deterrence))]; the S1 "
        "neighbour-contagion sub-term is OMITTED (it needs the static five_tier snapshot, "
        "not a listed time-varying input). S3/S4 hand-coded dicts are static across years.",
        "DGS iso recovered by population fingerprint; iso column was dropped from the cached panel. "
        "eci not separable (only z(eci)-z(polyarchy) stored).",
    ],
}

# ================================================================ WRITE
def jkeys(panel):
    """stringify year keys, sorted iso + sorted year for deterministic output."""
    return {iso: {str(y): panel[iso][y] for y in sorted(panel[iso])}
            for iso in sorted(panel) if panel[iso]}

pred_out = jkeys(predictors)
pred_out["_conflict_onsets_by_iso"] = None  # placeholder; onsets live on outcomes side
out_out = jkeys(outcomes)
out_out["conflict_onsets_by_iso"] = {iso: conflict_onsets_by_iso[iso] for iso in sorted(conflict_onsets_by_iso)}
del pred_out["_conflict_onsets_by_iso"]

with open(os.path.join(OUT_DIR, "predictors.json"), "w") as f:
    json.dump(pred_out, f, sort_keys=True, indent=0)
with open(os.path.join(OUT_DIR, "outcomes.json"), "w") as f:
    json.dump(out_out, f, sort_keys=True, indent=0)
with open(os.path.join(OUT_DIR, "panels_coverage.json"), "w") as f:
    json.dump(coverage, f, sort_keys=True, indent=1)

# ================================================================ PRINT SUMMARY
print("=" * 72)
print("PANEL BUILD COMPLETE")
print(f"  universe isos: {len(UNIVERSE)}   predictor years {PRED_YEARS[0]}-{PRED_YEARS[-1]}   "
      f"outcome years {OUT_YEARS[0]}-{OUT_YEARS[-1]}")
print(f"  total predictor (iso,year) rows: {total_pred_rows}")
print(f"  fully-instrumented core rows (all of {CORE}): {core_rows}")
print(f"  V1 engine failures (try/except skips): {v1_fail}")
print("-" * 72)
print("PREDICTOR field coverage: field -> (n_cells, n_isos, year_span)  [* = <30 isos]")
for fld in sorted(pred_cov):
    c = pred_cov[fld]
    flag = " *LOW-ISO" if c["flag_low_iso"] else ""
    print(f"   {fld:24s} {c['n_cells']:6d}  isos={c['n_isos']:4d}  span={c['year_span']}{flag}")
print("-" * 72)
print("OUTCOME field coverage:")
for fld in sorted(out_cov):
    c = out_cov[fld]
    flag = " *LOW-ISO" if c["flag_low_iso"] else ""
    print(f"   {fld:24s} {c['n_cells']:6d}  isos={c['n_isos']:4d}  span={c['year_span']}{flag}")
print("-" * 72)
print("V1 sanity vs mi_5pt_panel (P1/P3/P4 @ {1996,2004,2012,2018,2024}):")
print(f"   compared cells={sanity['compared_cells']}  matched(<=1e-4)={sanity['matched']}  "
      f"max_abs_diff={sanity['max_abs_diff']:.2e}  countries={sanity['countries']}")
if sanity["mismatches"]:
    print(f"   MISMATCHES ({len(sanity['mismatches'])}): {sanity['mismatches'][:5]}")
print("-" * 72)
print("DGS iso recovery:", coverage["dgs_recovery"])
print("=" * 72)

