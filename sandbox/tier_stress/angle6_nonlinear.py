#!/usr/bin/env python3
"""ANGLE 6 — NONLINEAR thresholds / tipping points. Every prior method assumed a smooth gradient.
Is there a CRITICAL CAPACITY FLOOR — a bifurcation below which democracy can't hold, where backslide
risk JUMPS rather than glides? Tests, all with libdem as a covariate (de-ceiling), OOS on held-out
countries:
  * nonparametric backslide-rate curve by capacity decile (is there a visible step?)
  * SMOOTH (linear logit) vs QUADRATIC vs best-THRESHOLD-step — which predicts best out-of-sample?
  * bootstrap the breakpoint location — concentrated (real tipping point) or diffuse (no floor)?
Capacity = rule-of-law percentile within year; backslide over k=5; base years 1900-2015 step 5."""
import numpy as np, hashlib
from scipy import stats
import common as C

BASES=list(range(1900,2016,5)); K=5
def cap_pctl(i,b):
    peers=[C.near(C.ROL,j,b) for j,_ in C.PANEL[b]]; peers=[p for p in peers if p is not None]
    v=C.near(C.ROL,i,b)
    if v is None or len(peers)<15: return None
    return float(np.mean([p<=v for p in peers]))
def backslide(i,b):
    a=C.near(C.LIB,i,b); c=C.near(C.LIB,i,b+K); return None if a is None or c is None else (1.0 if (c-a)<=-0.05 else 0.0)
def half(i): return "A" if int(hashlib.sha256(i.encode()).hexdigest(),16)%2==0 else "B"

rows=[]
for b in BASES:
    for i,_ in C.PANEL[b]:
        cp=cap_pctl(i,b); y=backslide(i,b); l=C.near(C.LIB,i,b)
        if None in (cp,y,l): continue
        rows.append((cp,y,l,half(i)))
n=len(rows); print("="*80); print(f"n={n} country-years, backslide events={int(sum(r[1] for r in rows))}"); print("="*80)

print("\n1) NONPARAMETRIC — backslide rate by capacity decile (look for a STEP vs smooth slope)")
caps=np.array([r[0] for r in rows]); ys=np.array([r[1] for r in rows])
order=np.argsort(caps)
print(f"   {'cap decile':>12} {'mean cap':>9} {'backslide rate':>15} {'n':>5}")
for d in range(10):
    idx=order[d*n//10:(d+1)*n//10]
    print(f"   {d+1:>12} {caps[idx].mean():>9.2f} {ys[idx].mean():>15.1%} {len(idx):>5}")

def logit(X,y,it=60,lam=1e-3):
    Xi=np.column_stack([np.ones(len(y))]+X); b=np.zeros(Xi.shape[1]); P=np.eye(Xi.shape[1])*lam; P[0,0]=0
    for _ in range(it):
        mu=1/(1+np.exp(-np.clip(Xi@b,-30,30))); W=mu*(1-mu)+1e-6
        try: step=np.linalg.solve(Xi.T@(Xi*W[:,None])+P, Xi.T@(mu-y)+P@b)
        except: break
        b=b-step
        if np.max(np.abs(step))<1e-8: break
    return b
def pred(X,b): return 1/(1+np.exp(-np.clip(np.column_stack([np.ones(len(X[0]))]+X)@b,-30,30)))
def auc(s,y):
    p,q=s[y==1],s[y==0]; return None if len(p)==0 or len(q)==0 else float(stats.mannwhitneyu(p,q).statistic/(len(p)*len(q)))

A=[r for r in rows if r[3]=="A"]; B=[r for r in rows if r[3]=="B"]
cA=[r[0] for r in A]; yA=np.array([r[1] for r in A]); lA=[r[2] for r in A]
cB=[r[0] for r in B]; yB=np.array([r[1] for r in B]); lB=[r[2] for r in B]

print("\n2) MODEL COMPARISON — held-out AUC on sealed countries (all include libdem covariate)")
# smooth linear
bL=logit([cA,lA],yA); aL=auc(pred([cB,lB],bL),yB)
# quadratic
bQ=logit([cA,list(np.array(cA)**2),lA],yA); aQ=auc(pred([cB,list(np.array(cB)**2),lB],bQ),yB)
# best threshold step (grid c on A by max train log-lik, eval on B)
best=None
for c in np.arange(0.15,0.86,0.05):
    stepA=[1.0 if x<c else 0.0 for x in cA]
    b=logit([stepA,lA],yA); mu=pred([stepA,lA],b); ll=float(np.sum(yA*np.log(mu+1e-9)+(1-yA)*np.log(1-mu+1e-9)))
    if best is None or ll>best[0]: best=(ll,c,b)
_,cstar,bT=best
aT=auc(pred([[1.0 if x<cstar else 0.0 for x in cB],lB],bT),yB)
print(f"   SMOOTH linear   : AUC {aL:.3f}")
print(f"   QUADRATIC       : AUC {aQ:.3f}  (Δ vs linear {aQ-aL:+.3f})")
print(f"   THRESHOLD step  : AUC {aT:.3f}  (Δ vs linear {aT-aL:+.3f})  best cutoff c*={cstar:.2f}")
winner="THRESHOLD" if (aT>aL+0.01 and aT>=aQ) else ("QUADRATIC" if aQ>aL+0.01 else "SMOOTH")
print(f"   -> best OOS model: {winner}")

print("\n3) BOOTSTRAP the breakpoint (is a tipping point WELL-IDENTIFIED or diffuse?)")
rng=np.random.default_rng(0); cs=[]
allc=np.array([r[0] for r in rows]); ally=np.array([r[1] for r in rows]); alll=np.array([r[2] for r in rows])
for _ in range(400):
    s=rng.integers(0,n,n); cc,yy,llb=allc[s],ally[s],alll[s]
    bb=None
    for c in np.arange(0.15,0.86,0.05):
        st=(cc<c).astype(float); b=logit([list(st),list(llb)],yy); mu=pred([list(st),list(llb)],b)
        ll=float(np.sum(yy*np.log(mu+1e-9)+(1-yy)*np.log(1-mu+1e-9)))
        if bb is None or ll>bb[0]: bb=(ll,c)
    cs.append(bb[1])
clo,chi=np.percentile(cs,[10,90])
print(f"   bootstrap best-cutoff: median c*={np.median(cs):.2f}, 10-90% range [{clo:.2f},{chi:.2f}] "
      f"-> {'CONCENTRATED (real threshold)' if (chi-clo)<=0.25 else 'DIFFUSE (no sharp floor -> smooth gradient)'}")

import json
json.dump({"angle":6,"n":n,"auc_smooth":round(aL,3),"auc_quadratic":round(aQ,3),"auc_threshold":round(aT,3),
           "best_cutoff":round(float(cstar),2),"winner":winner,
           "bootstrap_cut_range":[round(float(clo),2),round(float(chi),2)],
           "threshold_well_identified":bool((chi-clo)<=0.25),
           "threshold_beats_smooth":bool(aT>aL+0.01)},open("angle6_results.json","w"),indent=1)
print("\nsaved angle6_results.json")
