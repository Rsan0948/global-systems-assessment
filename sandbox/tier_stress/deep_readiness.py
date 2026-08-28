#!/usr/bin/env python3
"""READINESS probe for the six planned angles. Verifies data availability + alignment; flags gaps.
Read-only. Prints a per-angle readiness verdict."""
import json, numpy as np
from pathlib import Path
import deep_time as DT
HERE=Path(__file__).resolve().parent
MI=HERE.parents[1]/"mi-research"
def L(p):
    try: return json.load(open(p))
    except Exception as e: return {"__err__":str(e)}

LIB,ROL,CSO=DT.LIB,DT.ROL,DT.CSO
PREDJ=L(HERE/"predictors.json")

print("="*80); print("ANGLE 1 — DYNAMIC (rates): annual density of deep instruments"); print("="*80)
def annual_gap(series):
    gaps=[]
    for iso,s in series.items():
        ys=sorted(int(y) for y in s if str(y).isdigit() and 1900<=int(y)<=2015)
        if len(ys)<10: continue
        d=np.diff(ys); gaps.append(np.mean(d==1))  # frac of consecutive-year steps
    return np.mean(gaps), len(gaps)
for nm,s in [("libdem",LIB),("rol_vdem",ROL),("cso",CSO)]:
    frac,n=annual_gap(s); print(f"  {nm:10}: {n} countries, {frac:.0%} of year-steps are consecutive (need ~annual for d/dt)")
# WGI annual density (modern)
wgi_years=[]
for iso in PREDJ:
    ys=[int(y) for y in PREDJ[iso] if PREDJ[iso][y].get('v1_mi') is not None]
    if len(ys)>=5: wgi_years.append(np.mean(np.diff(sorted(ys))==1))
print(f"  v1_mi WGI : {len(wgi_years)} countries, {np.mean(wgi_years):.0%} consecutive (1996-2024)")

print("\n"+"="*80); print("ANGLE 2 — WITHIN-COUNTRY: cohorts per country + within-country outcome variation"); print("="*80)
percountry={}
for b in DT.BASES:
    for iso,_ in DT.PANEL[b]: percountry[iso]=percountry.get(iso,0)+1
vals=list(percountry.values())
print(f"  {len(percountry)} countries; median {np.median(vals):.0f} base-year cohorts each (max {max(vals)})")
# how many countries have >=2 backsliding-eligible obs with variation? (need within-country variance)
def within_var_ok():
    cnt=0
    for iso in percountry:
        ys=[]
        for b in DT.BASES:
            a=DT.near(LIB,iso,b); c=DT.near(LIB,iso,b+5)
            if a is not None and c is not None: ys.append(1 if (c-a)<=-0.05 else 0)
        if len(ys)>=5 and len(set(ys))>1: cnt+=1
    return cnt
print(f"  countries with >=5 obs AND within-country backslide variation: {within_var_ok()} (need these for FE)")

print("\n"+"="*80); print("ANGLE 3 — CONTAGION: adjacency + region availability"); print("="*80)
bc=L(MI/"data/political/_borders_cache.json"); t6=L(MI/"data/political/tier6_indicators.json")
print(f"  _borders_cache.json top keys: {list(bc.keys()) if isinstance(bc,dict) else type(bc)}")
if isinstance(bc,dict):
    for k in bc:
        v=bc[k]; n=len(v) if hasattr(v,'__len__') else '?'
        samp=(next(iter(v.items())) if isinstance(v,dict) and v else (v[:2] if isinstance(v,list) else v))
        print(f"     {k}: {type(v).__name__}[{n}]  e.g. {str(samp)[:90]}")
adj_key=[k for k in (bc if isinstance(bc,dict) else {}) if 'adj' in k.lower()]
print(f"  -> adjacency key: {adj_key if adj_key else 'NONE — check I2I3/haveborder'}")
cc=L(MI/"data/sources/country_context.json")
print(f"  country_context.json keys: {list(cc.keys())[:6] if isinstance(cc,dict) else type(cc)}")
if isinstance(cc,dict):
    k=next(iter(cc)); print(f"     sample {k} -> {str(cc[k])[:160]}")

print("\n"+"="*80); print("ANGLE 4 — COUNTRY ATTRIBUTES: resource, ethnic(EPR), size, age, colonial/legal"); print("="*80)
t4=L(MI/"data/political/tier4_indicators.json")["series"]
print(f"  resource_rents: {len(t6['series']['resource_rents_total'])} isos (have)")
print(f"  population(size): {len(t4['population'])} isos (have)")
epr=L(MI/"data/political/political_indicators.json")["series"].get("epr_by_statename")
eprmap=L(MI/"data/political/_epr_name_iso.json")
print(f"  EPR epr_by_statename: type={type(epr).__name__} len={len(epr) if hasattr(epr,'__len__') else '?'}")
if isinstance(epr,dict):
    k=next(iter(epr)); print(f"     {k} -> {str(epr[k])[:180]}")
print(f"  _epr_name_iso map: {len(eprmap) if isinstance(eprmap,dict) else '?'} name->iso entries")
# democracy age: derivable from LIB series start / first cross of 0.5
ages=[]
for iso,s in LIB.items():
    ys=sorted(int(y) for y in s if str(y).isdigit())
    if ys: ages.append(2015-ys[0])
print(f"  state age (from vdem series start): {len(ages)} countries, median {np.median(ages):.0f}y")
# colonial/legal origin — check country_context or anywhere
has_legal = isinstance(cc,dict) and any('legal' in str(v).lower() or 'coloni' in str(v).lower() for v in list(cc.values())[:5])
print(f"  colonial/legal origin in country_context: {'FOUND' if has_legal else 'NOT FOUND — likely a GAP'}")

print("\n"+"="*80); print("ANGLE 5 — SURVIVAL: transitions + timing"); print("="*80)
# transition = first libdem crossing <0.5 -> >=0.5; count how many + follow-up length
ntrans=0; follow=[]
for iso,s in LIB.items():
    ys=sorted(int(y) for y in s if str(y).isdigit()); had=False
    for y in ys:
        if s[str(y)]<0.5: had=True
        elif had:
            ntrans+=1; follow.append(max(ys)-y); break
print(f"  {ntrans} democratization transitions detectable; median post-transition follow-up {np.median(follow):.0f}y")
print("  timing + right-censoring computable from LIB -> Cox/discrete-hazard feasible.")

print("\n"+"="*80); print("ANGLE 6 — NONLINEAR: same data, method-only. Ready."); print("="*80)
print("  uses existing deep panel (LIB/ROL/anocracy); no new data needed.")
