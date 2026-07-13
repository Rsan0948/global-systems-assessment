#!/usr/bin/env python3
"""Critical Slowing Down — deep + wide + multi-angle. Tests whether the pre-rupture variance/
autocorrelation signal is a genuine COUNTDOWN (rises approaching the event, within a country's
own history) or a cross-country confound. Angles: A lead-time gradient, B within-country
baseline, C deep-historical eras (1789+), D multivariate (libdem+electdem+rol), E robustness.
Read-only."""
from __future__ import annotations
import json, sys, math
from collections import defaultdict
import numpy as np
from scipy import stats
sys.path.insert(0,"scripts/robustness"); sys.path.insert(0,".")
import convergence_lib as L
V=json.load(open("data/v2/vdem_democracy.json"))["series"]
G=json.load(open("data/v2/exploratory_outcomes.json"))["series"]["gdp_pc_growth"]

def sr(d,iso):
    s=d.get(iso);
    return {int(y):v for y,v in s.items()} if s else {}
def window(s,y0,y1):
    v=[s.get(y) for y in range(y0,y1+1)]
    return v if sum(x is not None for x in v)>=max(6,int(0.7*(y1-y0+1))) else None
def detrend(vals):
    if vals is None: return None
    idx=[i for i,v in enumerate(vals) if v is not None]
    if len(idx)<4: return None
    v=np.array([vals[i] for i in idx],float); t=np.array(idx,float)
    return v-np.polyval(np.polyfit(t,v,1),t)
def ar1(x):
    if x is None or len(x)<4 or np.std(x[:-1])==0 or np.std(x[1:])==0: return None
    return float(np.corrcoef(x[:-1],x[1:])[0,1])
def rollvar(s,y0,y1,w=5):
    out=[]
    for c in range(y0,y1-w+2):
        seg=[s.get(y) for y in range(c,c+w)]
        r=detrend(seg)
        out.append((c, float(np.var(r)) if r is not None else None))
    return [(c,v) for c,v in out if v is not None]

# ---- events ----
def backslide_events(d, lo, hi, drop=0.05, floor=0.15):
    ev=[]
    for iso in d:
        s=sr(d,iso)
        for T in range(lo,hi):
            if T in s and (T+3) in s and s[T]>=floor and (s[T+3]-s[T])<=-drop:
                # onset = first year of decline; ensure not mid-decline (rising or flat before)
                ev.append((iso,T))
    return ev
def controls(d, lo, hi, floor=0.15):
    ct=[]
    for iso in d:
        s=sr(d,iso)
        for T in range(lo,hi):
            if T in s and (T+3) in s and s[T]>=floor and (s[T+3]-s[T])>-0.01:
                ct.append((iso,T))
    return ct

LIB=V["libdem"]; ELEC=V["electdem"]; ROL=V["rol_vdem"]
print("="*72)
print("CRITICAL SLOWING DOWN — deep, wide, multi-angle (state var: V-Dem liberal democracy)")
print("="*72)

# ===== A. LEAD-TIME GRADIENT: does variance RISE approaching the event? =====
print("\n### A — LEAD-TIME GRADIENT (does variance rise as rupture approaches?) ###")
ev=backslide_events(LIB,1800,2018); ct=controls(LIB,1800,2018)
def slope_rollvar(iso,T):
    s=sr(LIB,iso); rv=rollvar(s,T-16,T-1,5)
    if len(rv)<6: return None
    xs=[c for c,_ in rv]; ys=[v for _,v in rv]
    return float(stats.linregress(xs,ys).slope)
ev_sl=[slope_rollvar(i,T) for i,T in ev]; ev_sl=[x for x in ev_sl if x is not None]
ct_sl=[slope_rollvar(i,T) for i,T in ct]; ct_sl=[x for x in ct_sl if x is not None]
print(f"  events={len(ev_sl)} controls={len(ct_sl)}")
print(f"  mean rolling-variance SLOPE (rising toward T): event={np.mean(ev_sl):.2e} vs control={np.mean(ct_sl):.2e}")
print(f"  frac events with RISING variance: {np.mean([s>0 for s in ev_sl]):.2f} vs control {np.mean([s>0 for s in ct_sl]):.2f}")
print(f"  MW p(event slope > control) = {stats.mannwhitneyu(ev_sl,ct_sl,alternative='greater').pvalue:.4f}  | AUC={L.auc_roc(ev_sl+ct_sl,[1]*len(ev_sl)+[0]*len(ct_sl)):.3f}")
# binned mean variance by lead
print("  mean detrended-variance by lead (7yr window ending at T-L), event vs control:")
for Lag in [12,9,6,3,1]:
    def vv(i,T):
        r=detrend(window(sr(LIB,i),T-Lag-7,T-Lag-1)); return float(np.var(r)) if r is not None else None
    e=[vv(i,T) for i,T in ev]; e=[x for x in e if x is not None]
    c=[vv(i,T) for i,T in ct]; c=[x for x in c if x is not None]
    print(f"    lead -{Lag:2d}yr: event var={np.median(e):.5f}  control var={np.median(c):.5f}  ratio={np.median(e)/np.median(c):.2f}")

# ===== B. WITHIN-COUNTRY BASELINE: does variance rise vs the country's OWN history? =====
print("\n### B — WITHIN-COUNTRY (pre-rupture variance / that country's own long-run variance) ###")
ratios=[]
for iso,T in ev:
    s=sr(LIB,iso)
    pre=detrend(window(s,T-10,T-1))
    if pre is None: continue
    allrv=[v for _,v in rollvar(s,min(s),max(s),8)]
    if len(allrv)<5: continue
    base=np.median(allrv)
    if base>0: ratios.append(math.log((np.var(pre)+1e-9)/(base+1e-9)))
print(f"  n={len(ratios)}  mean log(pre-var / own-baseline-var)={np.mean(ratios):+.3f}  (>0 => elevated vs self)")
print(f"  frac events with pre-var ABOVE own baseline: {np.mean([r>0 for r in ratios]):.2f}  | sign-test p={stats.binomtest(sum(r>0 for r in ratios),len(ratios)).pvalue:.4f}")

# ===== C. DEEP-HISTORICAL: does the signal hold across eras (1789+)? =====
print("\n### C — DEEP-HISTORICAL by era (variance-before-backsliding AUC) ###")
for lo,hi,name in [(1800,1918,"1800-1918"),(1919,1945,"interwar 1919-45"),(1946,1990,"1946-1990"),(1991,2018,"1991-2018")]:
    e=backslide_events(LIB,lo,hi); c=controls(LIB,lo,hi)
    def vv(i,T):
        r=detrend(window(sr(LIB,i),T-12,T-1)); return float(np.var(r)) if r is not None else None
    ve=[vv(i,T) for i,T in e]; ve=[x for x in ve if x is not None]
    vc=[vv(i,T) for i,T in c]; vc=[x for x in vc if x is not None]
    if len(ve)<10 or len(vc)<10: print(f"  {name}: too few (ev={len(ve)})"); continue
    print(f"  {name}: n_ev={len(ve)} n_ctl={len(vc)}  variance AUC={L.auc_roc(ve+vc,[1]*len(ve)+[0]*len(vc)):.3f}  MW p={stats.mannwhitneyu(ve,vc,alternative='greater').pvalue:.4f}")

# ===== D. MULTIVARIATE: combine CSD across libdem+electdem+rol =====
print("\n### D — MULTIVARIATE CSD (variance of libdem + electdem + rule-of-law combined) ###")
ev=backslide_events(LIB,1900,2018); ct=controls(LIB,1900,2018)
def multivar(i,T):
    vs=[]
    for d in [LIB,ELEC,ROL]:
        r=detrend(window(sr(d,i),T-12,T-1))
        vs.append(float(np.var(r)) if r is not None else None)
    return vs
def get(rows):
    M=[multivar(i,T) for i,T in rows]; return [m for m in M if all(x is not None for x in m)]
Me=get(ev); Mc=get(ct)
allM=np.array(Me+Mc); y=[1]*len(Me)+[0]*len(Mc)
z=(allM-allM.mean(0))/allM.std(0); combined=z.sum(1)
print(f"  n_ev={len(Me)} n_ctl={len(Mc)}")
for j,nm in enumerate(["libdem","electdem","rol"]):
    print(f"    {nm:9s} variance AUC={L.auc_roc(list(allM[:,j]),y):.3f}")
print(f"    >>> COMBINED 3-indicator CSD AUC={L.auc_roc(list(combined),y):.3f}")

print("\n### CONFLICT onset — GDP-growth variance, within-country + lead (robustness) ###")
import convergence_lib as L2
dom=L.domestic_years()
evc=[(i,T) for i in dom for T in dom[i] if 1972<=T<=2015]
def gvv(i,T,a,b):
    s=sr(G,i); r=detrend(window(s,T+a,T+b)); return float(np.var(r)) if r is not None else None
near=[gvv(i,T,-6,-1) for i,T in evc]; far=[gvv(i,T,-14,-9) for i,T in evc]
pairs=[(n,f) for n,f in zip(near,far) if n is not None and f is not None and f>0]
lr=[math.log(n/f+1e-9) for n,f in pairs if n>0]
print(f"  conflict: n={len(lr)} mean log(var_near/var_far)={np.mean(lr):+.3f} frac rising={np.mean([x>0 for x in lr]):.2f} sign p={stats.binomtest(sum(x>0 for x in lr),len(lr)).pvalue:.4f}")
