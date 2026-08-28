#!/usr/bin/env python3
"""Shared, aligned substrate for the six deep-angle analyses. Every angle imports from here so
the data access, normalization, and rigor primitives are IDENTICAL across angles (no drift).
Builds on deep_time (LIB/ROL/CSO/ONS/near/PANEL/ZPANEL/ERAS/BASES/partial). Read-only.
"""
import json, numpy as np
from pathlib import Path
from scipy import stats
import deep_time as DT

HERE=Path(__file__).resolve().parent
MI=HERE.parents[1]/"mi-research"

# ---- re-export the deep panel primitives (single source of truth) ----
LIB, ROL, CSO, ONS = DT.LIB, DT.ROL, DT.CSO, DT.ONS
near, PANEL, ZPANEL = DT.near, DT.PANEL, DT.ZPANEL
ERAS, BASES = DT.ERAS, DT.BASES
def anocracy(iso,b):
    l=near(LIB,iso,b); return None if l is None else 4*l*(1-l)
def pconf(iso,b): return DT.pconf(iso,b)

# ---- WGI capacity (modern, independent of V-Dem) ----
_PRED=json.load(open(HERE/"predictors.json"))
def wgi(iso,b,field="v1_mi"):
    r=_PRED.get(iso,{}).get(str(b)); return r.get(field) if isinstance(r,dict) else None
PRED=_PRED

# ---- static country attributes (Angle 4 moderators) ----
_t6=json.load(open(MI/"data/political/tier6_indicators.json"))["series"]
_t4=json.load(open(MI/"data/political/tier4_indicators.json"))["series"]
_pi=json.load(open(MI/"data/political/political_indicators.json"))["series"]
RENTS=_t6["resource_rents_total"]; POP=_t4["population"]; EPR=_pi.get("epr_by_statename",{})
_epr_name_iso=json.load(open(MI/"data/political/_epr_name_iso.json"))
_ISO_EPR={_epr_name_iso[n]:EPR[n] for n in EPR if n in _epr_name_iso}   # iso -> {excluded_pop_share,n_groups,...}
def resource_rents(iso,b): return near(RENTS,iso,b)
def population(iso,b): return near(POP,iso,b)
def ethnic(iso,field="excluded_pop_share"):
    d=_ISO_EPR.get(iso); return d.get(field) if isinstance(d,dict) else None
def state_age(iso,b):
    ys=[int(y) for y in LIB.get(iso,{}) if str(y).isdigit()]
    return (b-min(ys)) if ys else None
def dem_age(iso,b):
    """age of the CURRENT uninterrupted democratic spell at year b: consecutive years up to b
    with libdem>=0.5. None if not democratic at b. (Not first-ever crossing — handles re-democratizers
    like Poland: 2010 spell dates to 1989, not interwar.)"""
    s=LIB.get(iso,{})
    if str(b) not in s or s[str(b)]<0.5: return None
    age=0; y=b
    while str(y) in s and s[str(y)]>=0.5:
        age+=1; y-=1
    return age-1  # years since the spell's first democratic year

# ---- adjacency (Angle 3; current borders -> modern-era only) ----
_bc=json.load(open(MI/"data/political/_borders_cache.json"))
ADJ={k:list(v) for k,v in _bc.get("adj",{}).items()}   # iso3 -> [neighbor iso3]
HAVE_BORDER=set(_bc.get("haveborder",[]))
def neighbors(iso): return ADJ.get(iso,[])

# ---- rigor primitives (identical across angles) ----
def partial_spearman(x,y,ctrls):
    """Spearman(x,y | ctrls) via rank residuals; ctrls = list of arrays. None if degenerate."""
    x=np.asarray(x,float); y=np.asarray(y,float)
    rx,ry=stats.rankdata(x),stats.rankdata(y)
    Z=np.column_stack([np.ones(len(x))]+[stats.rankdata(np.asarray(c,float)) for c in ctrls])
    ex=rx-Z@np.linalg.lstsq(Z,rx,rcond=None)[0]; ey=ry-Z@np.linalg.lstsq(Z,ry,rcond=None)[0]
    if np.std(ex)<1e-12 or np.std(ey)<1e-12: return None
    return float(stats.pearsonr(ex,ey).statistic)

def perm_null(observed, recompute, n=2000, seed=0, two_sided=True):
    """generic permutation test. `recompute(rng)` returns a shuffled statistic (or None)."""
    rng=np.random.default_rng(seed); null=[recompute(rng) for _ in range(n)]
    null=[v for v in null if v is not None]
    if not null: return {"p":None,"lo":None,"hi":None,"n":0}
    lo,hi=np.percentile(null,[2.5,97.5])
    p=float(np.mean([abs(v)>=abs(observed) for v in null])) if two_sided else float(np.mean([v>=observed for v in null]))
    return {"p":round(p,4),"lo":round(float(lo),4),"hi":round(float(hi),4),"n":len(null),
            "real":bool(observed<lo or observed>hi)}

def velocity(series,iso,year,window=10):
    """OLS slope of a series over the trailing `window` years ending at `year` (per-year rate)."""
    s=series.get(iso) if isinstance(series,dict) else None
    if not s: return None
    pts=[(y,s[str(y)]) for y in range(year-window+1,year+1) if str(y) in s]
    if len(pts)<max(4,window//2): return None
    ys=np.array([p[0] for p in pts],float); vs=np.array([p[1] for p in pts],float)
    if np.std(ys)==0: return None
    return float(np.polyfit(ys,vs,1)[0])

def zwithin_year(valfn, b, isos=None):
    """z-score a value function across countries at base year b (predictors only, no leakage)."""
    rows=[(iso,valfn(iso,b)) for iso,_ in PANEL[b]] if isos is None else [(i,valfn(i,b)) for i in isos]
    vals=[v for _,v in rows if v is not None]
    if len(vals)<10: return {}
    mu=float(np.mean(vals)); sd=float(np.std(vals)) or 1.0
    return {iso:(v-mu)/sd for iso,v in rows if v is not None}

if __name__=="__main__":
    print("common.py substrate OK:")
    print(f"  deep instruments: LIB/ROL/CSO {len(LIB)}/{len(ROL)}/{len(CSO)} isos, BASES {BASES[0]}-{BASES[-1]}")
    print(f"  WGI isos: {sum(1 for i in PRED)}  adjacency: {len(ADJ)} isos  EPR: {len(_ISO_EPR)} isos")
    print(f"  attrs: rents {len(RENTS)}, pop {len(POP)}")
    print(f"  velocity(LIB,'USA',2000)={velocity(LIB,'USA',2000):+.4f}/yr  dem_age('POL',2010)={dem_age('POL',2010)}")
