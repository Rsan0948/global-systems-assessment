#!/usr/bin/env python3
"""CAPACITY ARSENAL — relational redo. The arsenal combined capacity features by ADDITIVE stacking,
which the campaign found suboptimal vs RELATIONAL combination (gaps/ratios/products). Here we relate
the capacity dimensions to each other and compare, out-of-sample:
  ADDITIVE  : stack the level features in a logit (what the arsenal did) -> the 0.746 baseline
  RELATIONAL: ratios/gaps/products BETWEEN the capacity dimensions (resilience, scar-ratio, debt-
              weighted capacity, stability=level/volatility, safe×far, long-change) + capacity−mobilisation
  BOTH
Same rigor: held-out-country AUC, 1900-2015, k=5. Caveat: 'relational>additive' was proven for
DIFFERENT instruments; extending it to transforms of ONE variable is the open question here."""
import numpy as np, math, hashlib
from scipy import stats
import common as C

YEARS=range(1875,2016); BASES=list(range(1900,2016,5)); K=5
def pctl_year(series,y):
    vals=[(i,series[i][str(y)]) for i in series if str(y) in series[i]]; xs=[v for _,v in vals]
    if len(xs)<12: return {}
    srt=np.sort(xs); return {i:float(np.searchsorted(srt,v)/len(srt)) for i,v in vals}
PROL={y:pctl_year(C.ROL,y) for y in YEARS}; PCSO={y:pctl_year(C.CSO,y) for y in YEARS}
def cap(i,y): return PROL.get(y,{}).get(i)
def mob(i,y): return PCSO.get(y,{}).get(i)
def half(i): return "A" if int(hashlib.sha256(i.encode()).hexdigest(),16)%2==0 else "B"
def backslide(i,b):
    a=C.near(C.LIB,i,b); c=C.near(C.LIB,i,b+K); return None if a is None or c is None else (1.0 if (c-a)<=-0.05 else 0.0)

def feats(i,b):
    c=cap(i,b)
    if c is None: return None
    hist=[cap(i,y) for y in range(b-20,b+1)]; hist=[h for h in hist if h is not None]
    volr=[C.near(C.ROL,i,y,0) for y in range(b-10,b+1)]; volr=[v for v in volr if v is not None]
    if len(hist)<8 or len(volr)<6: return None
    mn=min(hist); debt=float(np.mean([h<0.5 for h in hist])); vol=float(np.std(volr))
    lag=cap(i,b-20); m=mob(i,b)
    if lag is None or m is None: return None
    dist=abs(c-0.5); ceil=1.0 if c>0.8 else 0.0
    return {
      # LEVEL (additive set)
      "cap":c,"cap2":c*c,"dist_peak":dist,"ceiling":ceil,"min_cap":mn,"debt":debt,"vol":vol,"lag":lag,
      # RELATIONAL (ratios/gaps/products between the dimensions)
      "resilience":c-mn,                     # gap: how far above historical worst
      "scar_ratio":mn/(c+0.05),              # ratio: worst relative to now
      "debt_cap":c*(1-debt),                 # product: strength discounted by time-in-weakness
      "stability":c/(1+vol),                 # ratio: level per unit volatility
      "safe_far":ceil*dist,                  # product: above ceiling AND far from danger
      "long_change":c-lag,                   # gap over 20y
      "capmob_gap":c-m,                      # founding-eqn relational: capacity vs mobilisation
    }

rows=[]
for b in BASES:
    for i,_ in C.PANEL[b]:
        f=feats(i,b); y=backslide(i,b); l=C.near(C.LIB,i,b)
        if f is None or y is None or l is None: continue
        rows.append((f,y,l,half(i)))
print(f"n={len(rows)} rows, events={int(sum(r[1] for r in rows))}\n")

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
def oos(featlist):
    A=[r for r in rows if r[3]=="A"]; B=[r for r in rows if r[3]=="B"]
    cols=lambda S:[[r[0][f] for r in S] for f in featlist]+[[r[2] for r in S]]
    yA=np.array([r[1] for r in A]); yB=np.array([r[1] for r in B])
    return auc(predict(cols(B),logit(cols(A),yA)),yB)

ADD=["cap","cap2","dist_peak","ceiling","min_cap","debt","vol","lag"]
REL=["resilience","scar_ratio","debt_cap","stability","safe_far","long_change","dist_peak","ceiling"]
sets={"ADDITIVE (levels, the arsenal way)":ADD,
      "RELATIONAL (ratios/gaps/products)":REL,
      "RELATIONAL + capacity−mobilisation":REL+["capmob_gap"],
      "BOTH":ADD+REL+["capmob_gap"]}
print(f"{'combination strategy':40} {'held-out AUC':>12}")
print("-"*54)
out={}
for lab,fl in sets.items():
    a=oos(fl); out[lab]=round(a,3); print(f"{lab:40} {a:>12.3f}")
add=out["ADDITIVE (levels, the arsenal way)"]; rel=out["RELATIONAL (ratios/gaps/products)"]
print(f"\n  relational − additive = {rel-add:+.3f}  -> "
      f"{'RELATIONAL WINS (consistent with earlier finding)' if rel>add+0.005 else ('ADDITIVE holds (relational edge does NOT extend to single-variable transforms)' if add>rel+0.005 else 'TIE')}")

import json
json.dump({"analysis":"capacity_relational","n":len(rows),"results":out,"relational_minus_additive":round(rel-add,3)},
          open("capacity_relational_results.json","w"),indent=1)
print("saved capacity_relational_results.json")
