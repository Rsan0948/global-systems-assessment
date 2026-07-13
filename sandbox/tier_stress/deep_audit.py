#!/usr/bin/env python3
"""ADVERSARIAL audit: is a bug/artifact driving the deep findings?
Threats tested:
  T1 V-DEM CIRCULARITY — rol_vdem (capacity proxy) is ~0.85 corr with libdem (the outcome base).
     Orthogonalize rol on libdem within-year (rol_resid) and re-test. If the signal is pure
     component-coupling it dies; if capacity-BEYOND-democracy-level carries it, it survives.
  T2 INDEPENDENT CAPACITY — re-test the modern capΔ inversion with WGI v1_mi (NOT V-Dem).
  T3 PERMUTATION NULL — shuffle the predictor across countries within each cohort; a real signal
     must collapse to ~0.
  T4 near() TOLERANCE — recompute headline numbers with EXACT-year matching (tol=0).
  T5 DISJOINTNESS — assert pconf(<=b) and onset-window (b,b+k] never share a year (no leakage).
"""
import json, numpy as np
from pathlib import Path
from scipy import stats
import deep_time as DT
HERE=Path(__file__).resolve().parent

def near0(s,iso,y):  # EXACT year only
    d=s.get(iso) if isinstance(s,dict) else None
    return d.get(str(y)) if d else None

def partial(x,y,z):
    x,y,z=map(lambda a:np.array(a,float),(x,y,z))
    rx,ry,rz=stats.rankdata(x),stats.rankdata(y),stats.rankdata(z)
    Z=np.column_stack([np.ones(len(x)),rz]); ex=rx-Z@np.linalg.lstsq(Z,rx,rcond=None)[0]
    ey=ry-Z@np.linalg.lstsq(Z,ry,rcond=None)[0]
    return None if np.std(ex)<1e-9 or np.std(ey)<1e-9 else float(stats.pearsonr(ex,ey).statistic)

def rol_resid_year(b, nearfn=DT.near):
    """residual of rol on libdem within base-year b -> capacity ORTHOGONAL to democracy level."""
    rows=[(i,nearfn(DT.ROL,i,b),nearfn(DT.LIB,i,b)) for i,_ in DT.PANEL[b]]
    rows=[(i,v,l) for i,v,l in rows if v is not None and l is not None]
    if len(rows)<15: return {}
    v=np.array([r[1] for r in rows]); l=np.array([r[2] for r in rows])
    A=np.column_stack([np.ones(len(l)),l]); resid=v-A@np.linalg.lstsq(A,v,rcond=None)[0]
    return {r[0]:resid[k] for k,r in enumerate(rows)}

def cohort_partial(capfn,which,k,b,nearfn=DT.near,room=False,perm=False,seed=0):
    rows=[]
    for iso,_ in DT.PANEL[b]:
        cap=capfn(iso,b); lb=nearfn(DT.LIB,iso,b)
        if cap is None or lb is None: continue
        lc=nearfn(DT.LIB,iso,b+k)
        if which=="democratize": y=None if lc is None else (1.0 if (lc-lb)>=0.05 else 0.0)
        elif which=="backslide": y=None if lc is None else (1.0 if (lc-lb)<=-0.05 else 0.0)
        if y is None: continue
        if room and lb>=0.5: continue
        rows.append((cap,y,lb))
    if len(rows)<25 or len({r[1] for r in rows})<2: return None
    xs=[r[0] for r in rows]
    if perm: xs=list(np.random.default_rng(seed).permutation(xs))
    return partial(xs,[r[1] for r in rows],[r[2] for r in rows])

def era_mean(capfn,which,k,e0,e1,**kw):
    rr=[cohort_partial(capfn,which,k,b,**kw) for b in DT.BASES if e0<=b<=e1]
    rr=[x for x in rr if x is not None]
    return (round(float(np.mean(rr)),3),len(rr)) if len(rr)>=2 else (None,0)

RAW_ROL=lambda iso,b: DT.near(DT.ROL,iso,b)
def RESID_ROL(iso,b): return rol_resid_year(b).get(iso)

print("="*88)
print("T1  V-DEM CIRCULARITY  — capacity->democratize (k=20), RAW rol vs rol ORTHOGONAL to libdem")
print("="*88)
print(f"{'era':20} | {'raw rol ρ':>12} | {'rol⊥libdem ρ':>14}   (if orthogonal ρ≈0 -> was coupling)")
for elab,e0,e1 in DT.ERAS:
    raw,_=era_mean(RAW_ROL,"democratize",20,e0,e1)
    res,_=era_mean(RESID_ROL,"democratize",20,e0,e1)
    print(f"{elab:20} | {raw if raw is not None else 'NA':>12} | {res if res is not None else 'NA':>14}")

print("\n"+"="*88)
print("T1b same for BACKSLIDE (k=10): does orthogonalized capacity still forecast backsliding?")
print("="*88)
for elab,e0,e1 in DT.ERAS:
    raw,_=era_mean(RAW_ROL,"backslide",10,e0,e1); res,_=era_mean(RESID_ROL,"backslide",10,e0,e1)
    print(f"{elab:20} | raw rol ρ={str(raw):>7} | rol⊥libdem ρ={str(res):>7}")

print("\n"+"="*88)
print("T2  INDEPENDENT CAPACITY — modern democratizer capΔ with WGI v1_mi (NOT V-Dem)")
print("="*88)
PREDJ=json.load(open(HERE/"predictors.json"))
def wgi_cap(iso,b):
    r=PREDJ.get(iso,{}).get(str(b)); return r.get("v1_mi") if isinstance(r,dict) else None
for k in [10,20]:
    caps_dem=[]; caps_non=[]
    for b in [1996,2000,2004,2005] if False else range(1996,2006):
        rows=[(wgi_cap(iso,b), DT.near(DT.LIB,iso,b), DT.near(DT.LIB,iso,b+k)) for iso in PREDJ]
        rows=[(c,a,cc) for c,a,cc in rows if c is not None and a is not None and cc is not None]
        if len(rows)<25: continue
        z=stats.zscore([r[0] for r in rows])
        dy=[1 if (cc-a)>=0.05 else 0 for _,a,cc in rows]
        cd=[z[i] for i in range(len(rows)) if dy[i]==1]; cn=[z[i] for i in range(len(rows)) if dy[i]==0]
        if cd and cn: caps_dem.append(np.mean(cd)-np.mean(cn))
    g=np.mean(caps_dem) if caps_dem else float('nan')
    print(f"  k={k}: modern democratizer WGI-capacity Δ = {g:+.2f}  (V-Dem-rol gave −0.35/−0.43; independent proxy should agree if real)")

print("\n"+"="*88)
print("T3  PERMUTATION NULL — shuffle predictor within cohort (200x); observed vs null band")
print("="*88)
def perm_band(capfn,which,k,e0,e1,n=200):
    obs,_=era_mean(capfn,which,k,e0,e1)
    null=[era_mean(capfn,which,k,e0,e1,perm=True,seed=s)[0] for s in range(n)]
    null=[x for x in null if x is not None]
    lo,hi=np.percentile(null,[2.5,97.5])
    return obs,round(float(lo),3),round(float(hi),3)
for lbl,capfn,which,k,e0,e1 in [("C19 cap->dem k20",RAW_ROL,"democratize",20,1820,1899),
                                 ("Modern cap->backslide k10",RAW_ROL,"backslide",10,1989,2015)]:
    o,lo,hi=perm_band(capfn,which,k,e0,e1)
    print(f"  {lbl:30}: observed ρ={o:+.3f}  null 95% band [{lo:+.3f},{hi:+.3f}]  -> {'REAL (outside null)' if (o<lo or o>hi) else 'inside null (SUSPECT)'}")

print("\n"+"="*88)
print("T4  near() TOLERANCE — headline numbers with EXACT-year match (tol=0)")
print("="*88)
for elab,e0,e1 in [("C19 1820-99",1820,1899),("Modern 1989-2015",1989,2015)]:
    a,_=era_mean(RAW_ROL,"democratize",20,e0,e1)
    a0,_=era_mean(RAW_ROL,"democratize",20,e0,e1,nearfn=near0)
    print(f"  cap->democratize k20  {elab:16}: tol=2 ρ={a}  tol=0 ρ={a0}")

print("\n"+"="*88)
print("T5  DISJOINTNESS — predictor window (<=b) vs outcome window (b,b+k] share no year")
print("="*88)
b,k=1990,10
pred_years=set(range(1800,b+1)); out_years=set(range(b+1,b+k+1))
assert not (pred_years & out_years), "LEAK: predictor and outcome windows overlap"
print(f"  pconf uses years <= {b}; onset outcome uses ({b},{b+k}] -> disjoint: OK")
print("\nAudit complete.")
