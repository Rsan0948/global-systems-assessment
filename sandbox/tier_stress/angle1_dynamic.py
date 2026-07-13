#!/usr/bin/env python3
"""ANGLE 1 — the DYNAMIC founding equation. 'Complexity outruns capacity' is a RATE statement;
we only ever tested it as a static gap. Here: velocities (10y OLS slopes) of the deep instruments,
and the MISMATCH VELOCITY = v(civil-society mobilization) − v(rule-of-law capacity) — participation
accelerating past institutionalization (MI founding equation == Huntington's gap). Tests:
  A) does mismatch-velocity forecast backsliding / conflict, by era + pooled (permutation null)?
  B) THE decisive test — does the RATE add OVER the static level gap (rol−cso) + persistence?
  C) acceleration (2nd-order) — does it add?
  D) modern INDEPENDENT check — velocity(V3 pressure) − velocity(V1 WGI capacity), de-circularized.
Metric = mean per-cohort partial-Spearman; consistent with the rest of the campaign."""
import numpy as np
from scipy import stats
import common as C

WIN=10
def v_rol(i,b): return C.velocity(C.ROL,i,b,WIN)
def v_cso(i,b): return C.velocity(C.CSO,i,b,WIN)
def mismatch(i,b):
    a,r=v_cso(i,b),v_rol(i,b); return None if a is None or r is None else a-r
def accel(i,b):
    """change in mismatch-velocity: mismatch over recent 10y minus prior 10y."""
    now=mismatch(i,b); past=mismatch(i,b-WIN); return None if now is None or past is None else now-past

def outcome(i,b,k,which):
    lb=C.near(C.LIB,i,b)
    if which=="backslide":
        lc=C.near(C.LIB,i,b+k); return None if lb is None or lc is None else (1.0 if (lc-lb)<=-0.05 else 0.0)
    ys=C.ONS.get(i); return None if ys is None else (1.0 if any(b<y<=b+k for y in ys) else 0.0)

def cohort_rows(b,which,k):
    zrol=C.zwithin_year(lambda i,bb=b: C.near(C.ROL,i,bb),b)
    zcso=C.zwithin_year(lambda i,bb=b: C.near(C.CSO,i,bb),b)
    out=[]
    for iso,_ in C.PANEL[b]:
        mm=mismatch(iso,b); lib=C.near(C.LIB,iso,b); y=outcome(iso,b,k,which)
        if mm is None or lib is None or y is None: continue
        sg=None if iso not in zrol or iso not in zcso else zrol[iso]-zcso[iso]
        out.append(dict(iso=iso,mm=mm,vrol=v_rol(iso,b),vcso=v_cso(iso,b),acc=accel(iso,b),
                        lib=lib,rol=C.near(C.ROL,iso,b),sgap=sg,y=y))
    return out

_CACHE={}
def get_cohorts(which,k):
    """build cohort rows ONCE per (which,k); permutations reuse them (velocities/z-norms not recomputed)."""
    key=(which,k)
    if key not in _CACHE:
        _CACHE[key]=[(b,cohort_rows(b,which,k)) for b in C.BASES]
    return _CACHE[key]

def mean_partial(feat,ctrls,which,k,e0=1820,e1=2015,permute=False,rng=None):
    rhos=[]
    for b,allrows in get_cohorts(which,k):
        if not (e0<=b<=e1): continue
        rows=[r for r in allrows if r[feat] is not None and all(r[c] is not None for c in ctrls)]
        if len(rows)<25 or len({r["y"] for r in rows})<2: continue
        xs=[r[feat] for r in rows]
        if permute: xs=list(rng.permutation(xs))
        pr=C.partial_spearman(xs,[r["y"] for r in rows],[[r[c] for r in rows] for c in ctrls])
        if pr is not None: rhos.append(pr)
    return (float(np.mean(rhos)),len(rhos)) if len(rhos)>=2 else (None,len(rhos))

def report(feat,ctrls,which,k,label):
    obs,ncoh=mean_partial(feat,ctrls,which,k)
    if obs is None: print(f"  {label:52} insufficient"); return
    pn=C.perm_null(obs,lambda rng:mean_partial(feat,ctrls,which,k,permute=True,rng=rng)[0],n=800)
    tag="REAL" if pn["real"] else "null"
    print(f"  {label:52} ρ={obs:+.3f} (cohorts={ncoh})  perm-p={pn['p']} [{pn['lo']:+.2f},{pn['hi']:+.2f}] {tag}")

print("="*92); print("A) MISMATCH-VELOCITY  v(cso)−v(rol)  → outcome, net of persistence (libdem level)"); print("="*92)
for which,k in [("backslide",5),("backslide",10),("onset",10)]:
    report("mm",["lib"],which,k,f"{which} k={k}: mismatch-vel | libdem")

print("\n"+"="*92); print("B) DECISIVE — does the RATE add OVER the static level gap (rol−cso) + persistence?"); print("="*92)
for which,k in [("backslide",5),("backslide",10)]:
    report("sgap",["lib"],which,k,f"{which} k={k}: STATIC gap(rol−cso) | libdem   [the level baseline]")
    report("mm",["lib","sgap"],which,k,f"{which} k={k}: mismatch-VEL | libdem + static gap  [rate's add]")

print("\n"+"="*92); print("C) components + ACCELERATION"); print("="*92)
for which,k in [("backslide",10)]:
    report("vrol",["lib"],which,k,f"{which} k={k}: v(rol) alone (capacity erosion) | libdem")
    report("vcso",["lib"],which,k,f"{which} k={k}: v(cso) alone (mobilization surge) | libdem")
    report("acc",["lib","mm"],which,k,f"{which} k={k}: ACCELERATION | libdem + mismatch-vel")

print("\n"+"="*92); print("D) MODERN INDEPENDENT — velocity(V3 pressure)−velocity(V1 WGI capacity), de-circularized"); print("="*92)
MV1={i:{y:C.PRED[i][y]["v1_mi"] for y in C.PRED[i] if C.PRED[i][y].get("v1_mi") is not None} for i in C.PRED}
MV3={i:{y:C.PRED[i][y]["v3_numer"] for y in C.PRED[i] if C.PRED[i][y].get("v3_numer") is not None} for i in C.PRED}
def mm_wgi(i,b):
    a=C.velocity(MV3,i,b,WIN); r=C.velocity(MV1,i,b,WIN); return None if a is None or r is None else a-r
def modern_rows(b,k):
    out=[]
    for i in C.PRED:
        m=mm_wgi(i,b); lib=C.near(C.LIB,i,b); cap=(C.PRED[i].get(str(b),{}) or {}).get("v1_mi")
        lc=C.near(C.LIB,i,b+k)
        if None in (m,lib,cap) or lc is None: continue
        out.append((m,1.0 if (lc-lib)<=-0.05 else 0.0,lib,cap))
    return out
def modern_partial(k,permute=False,rng=None):
    rhos=[]
    for b in range(2006,2015):
        rows=modern_rows(b,k)
        if len(rows)<25 or len({r[1] for r in rows})<2: continue
        xs=[r[0] for r in rows]
        if permute: xs=list(rng.permutation(xs))
        pr=C.partial_spearman(xs,[r[1] for r in rows],[[r[2] for r in rows],[r[3] for r in rows]])
        if pr is not None: rhos.append(pr)
    return (float(np.mean(rhos)),len(rhos)) if len(rhos)>=2 else (None,len(rhos))
o,nc=modern_partial(5)
if o is not None:
    pn=C.perm_null(o,lambda rng:modern_partial(5,True,rng)[0],n=800)
    print(f"  backslide k=5: mismatch-vel(WGI) | libdem+WGI-cap  ρ={o:+.3f} (cohorts={nc}) perm-p={pn['p']} {'REAL' if pn['real'] else 'null'}")
else:
    print("  modern independent: insufficient cohorts (WGI velocity needs 10y history 1996+)")
print("\nHypothesis: mismatch-vel >0 (participation outrunning institutionalization) -> more backsliding (ρ>0).")
