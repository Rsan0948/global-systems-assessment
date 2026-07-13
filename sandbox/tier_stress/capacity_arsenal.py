#!/usr/bin/env python3
"""CAPACITY ARSENAL — throw the full mathematical toolkit at capacity→backsliding. Capacity is the
master variable; here we exhaust its representations and see how far it alone predicts, out-of-sample.
Feature families (all functions of rule-of-law capacity, some with mobilisation/democracy):
  NONLINEAR  : cap, cap², |cap−0.5| (dist from the inverted-U danger peak), I(cap>0.8) safety ceiling
  RELATIVE   : within-country deviation (cap − own mean)
  HISTORY    : cap lag-20, min-cap over 20y (scar), capacity-debt (frac years weak), cap volatility
  COMPLEX    : z = cap + i·mobilisation -> modulus |z|, phase arg(z) (founding eqn: phase>45°=complexity>capacity)
  DYNAMICAL  : local VAR(1) on (cap,libdem) -> spectral radius max|λ| (closeness to instability),
               |Im λ| (oscillation) — eigenvalues, genuinely complex, criticality-themed
Then STACK the survivors. Rigor: held-out-country AUC, permutation nulls, base years 1900-2015, k=5."""
import numpy as np, math, hashlib
from scipy import stats
import common as C

YEARS=range(1875,2016); BASES=list(range(1900,2016,5)); K=5
def pctl_year(series,y):
    vals=[(i,series[i][str(y)]) for i in series if str(y) in series[i]]; xs=[v for _,v in vals]
    if len(xs)<12: return {}
    srt=np.sort(xs); return {i:float(np.searchsorted(srt,v)/len(srt)) for i,v in vals}
PROL={y:pctl_year(C.ROL,y) for y in YEARS}
PCSO={y:pctl_year(C.CSO,y) for y in YEARS}
def cap(i,y): return PROL.get(y,{}).get(i)
def mob(i,y): return PCSO.get(y,{}).get(i)
def rolraw(i,y): return C.near(C.ROL,i,y,0)
def libraw(i,y): return C.near(C.LIB,i,y,0)
def half(i): return "A" if int(hashlib.sha256(i.encode()).hexdigest(),16)%2==0 else "B"
def backslide(i,b):
    a=C.near(C.LIB,i,b); c=C.near(C.LIB,i,b+K); return None if a is None or c is None else (1.0 if (c-a)<=-0.05 else 0.0)

def var_eig(i,b,w=15):
    """local VAR(1) on (rol,libdem) over [b-w,b]: X_{t+1}=A X_t. Return (spectral_radius, |Im λ|)."""
    pts=[(rolraw(i,y),libraw(i,y)) for y in range(b-w,b+1)]
    pts=[p for p in pts if p[0] is not None and p[1] is not None]
    if len(pts)<8: return None,None
    X=np.array(pts); X0,X1=X[:-1],X[1:]
    if np.std(X0[:,0])<1e-6 or np.std(X0[:,1])<1e-6: return None,None
    try:
        A=np.linalg.lstsq(np.column_stack([X0,np.ones(len(X0))]),X1,rcond=None)[0][:2].T
        ev=np.linalg.eigvals(A)
    except Exception: return None,None
    return float(np.max(np.abs(ev))), float(np.max(np.abs(ev.imag)))

def feats(i,b):
    c=cap(i,b)
    if c is None: return None
    f={"cap":c,"cap2":c*c,"dist_peak":abs(c-0.5),"ceiling":1.0 if c>0.8 else 0.0}
    hist=[cap(i,y) for y in range(b-20,b+1)]; hist=[h for h in hist if h is not None]
    f["cap_lag20"]=cap(i,b-20)
    f["min_cap20"]=min(hist) if len(hist)>=8 else None
    f["cap_debt"]=float(np.mean([h<0.5 for h in hist])) if len(hist)>=8 else None
    volr=[rolraw(i,y) for y in range(b-10,b+1)]; volr=[v for v in volr if v is not None]
    f["cap_vol"]=float(np.std(volr)) if len(volr)>=6 else None
    own=[cap(i,y) for y in range(b-20,b+1)]; own=[o for o in own if o is not None]
    f["cap_dev"]=(c-float(np.mean(own))) if len(own)>=8 else None
    m=mob(i,b)
    f["mag"]=math.hypot(c,m) if m is not None else None
    f["phase"]=math.atan2(m,c) if m is not None else None      # imaginary-part angle: >π/4 => mobilisation>capacity
    sr,osc=var_eig(i,b); f["spectral_radius"]=sr; f["oscillation"]=osc
    return f

FEATS=["cap","cap2","dist_peak","ceiling","cap_lag20","min_cap20","cap_debt","cap_vol","cap_dev",
       "mag","phase","spectral_radius","oscillation"]
rows=[]
for b in BASES:
    for i,_ in C.PANEL[b]:
        f=feats(i,b); y=backslide(i,b); l=C.near(C.LIB,i,b)
        if f is None or y is None or l is None: continue
        rows.append((f,y,l,half(i),b))
print("="*82); print(f"n={len(rows)} rows, events={int(sum(r[1] for r in rows))}"); print("="*82)

def logit(X,y,it=60,lam=1e-2):
    Xi=np.column_stack([np.ones(len(y))]+X); b=np.zeros(Xi.shape[1]); P=np.eye(Xi.shape[1])*lam; P[0,0]=0
    for _ in range(it):
        mu=1/(1+np.exp(-np.clip(Xi@b,-30,30))); W=mu*(1-mu)+1e-6
        try: step=np.linalg.solve(Xi.T@(Xi*W[:,None])+P,Xi.T@(mu-y)+P@b)
        except: break
        b=b-step
        if np.max(np.abs(step))<1e-8: break
    return b
def predict(X,b): return 1/(1+np.exp(-np.clip(np.column_stack([np.ones(len(X[0]))]+X)@b,-30,30)))
def auc(s,y):
    p,q=s[y==1],s[y==0]; return None if len(p)==0 or len(q)==0 else float(stats.mannwhitneyu(p,q).statistic/(len(p)*len(q)))

def oos(featlist,permute=None,rng=None):
    """fit on A, AUC on B, features + libdem; requires all featlist present."""
    A=[r for r in rows if r[3]=="A" and all(r[0].get(f) is not None for f in featlist)]
    B=[r for r in rows if r[3]=="B" and all(r[0].get(f) is not None for f in featlist)]
    if len(A)<60 or len(B)<40: return None,len(B)
    def cols(S,pf=False):
        M=[[r[0][f] for r in S] for f in featlist]
        if pf and permute: M[featlist.index(permute)]=list(rng.permutation(M[featlist.index(permute)]))
        return M+[[r[2] for r in S]]
    yA=np.array([r[1] for r in A]); yB=np.array([r[1] for r in B])
    b=logit(cols(A,True),yA); return auc(predict(cols(B),b),yB),len(B)

print("\n1) UNIVARIATE OOS AUC (each feature + libdem, held-out countries)")
base_lib,_=oos([])  # libdem only baseline
print(f"   {'(libdem only baseline)':28} AUC {base_lib:.3f}")
res={}
for f in FEATS:
    a,nb=oos([f]);
    if a is None: print(f"   {f:28} insufficient"); continue
    res[f]=a; print(f"   {f:28} AUC {a:.3f}  (Δ vs libdem {a-base_lib:+.3f})  nB={nb}")

print("\n2) PERMUTATION NULLS for the exotic features (phase, spectral_radius, oscillation)")
rng=np.random.default_rng(0)
for f in ["phase","spectral_radius","oscillation","cap_debt"]:
    if f not in res: continue
    obs=res[f]; null=[oos([f],permute=f,rng=rng)[0] for _ in range(300)]; null=[x for x in null if x]
    lo,hi=np.percentile(null,[2.5,97.5]); print(f"   {f:18} obs {obs:.3f} null95 [{lo:.3f},{hi:.3f}] -> {'REAL' if (obs<lo or obs>hi) else 'null'}")

print("\n3) STACKED capacity models (held-out AUC) — how far can capacity alone go?")
combos={"smooth (cap)":["cap"],"Angle6 quad (cap,cap²)":["cap","cap2"],
        "nonlinear+ceiling":["cap","cap2","dist_peak","ceiling"],
        "+history":["cap","cap2","dist_peak","ceiling","min_cap20","cap_debt","cap_vol","cap_lag20"],
        "+complex/phase":["cap","cap2","dist_peak","ceiling","min_cap20","cap_debt","phase","mag"],
        "+dynamical(eig)":["cap","cap2","dist_peak","ceiling","min_cap20","cap_debt","spectral_radius","oscillation"],
        "EVERYTHING":FEATS}
best=None
for lab,fl in combos.items():
    a,nb=oos(fl)
    if a is None: print(f"   {lab:26} insufficient"); continue
    print(f"   {lab:26} AUC {a:.3f}  (Δ vs quad {a-(res.get('cap2') and oos(['cap','cap2'])[0] or a):+.3f})  nB={nb}")
    if best is None or a>best[1]: best=(lab,a)
print(f"\n   -> best capacity-only model: {best[0]}  AUC {best[1]:.3f}")

import json
quad=oos(["cap","cap2"])[0]
json.dump({"angle":"capacity_arsenal","n":len(rows),"events":int(sum(r[1] for r in rows)),
           "libdem_baseline":round(base_lib,3),"univariate":{k:round(v,3) for k,v in res.items()},
           "smooth":round(oos(["cap"])[0],3),"quad":round(quad,3),
           "best_model":best[0],"best_auc":round(best[1],3)},open("capacity_arsenal_results.json","w"),indent=1)
print("saved capacity_arsenal_results.json")
