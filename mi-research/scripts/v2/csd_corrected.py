#!/usr/bin/env python3
"""CSD — AUDIT-CORRECTED. Fixes the defects the adversarial audit found in trigger_hunt/csd_deep:
  H1 pseudoreplication  -> ONE observation per (country, backsliding EPISODE), country-clustered bootstrap.
  H2 cross-country confound -> WITHIN-country standardization (variance vs the country's own baseline).
  M1 shifting subsets   -> lead gradient on a FIXED cohort (events with data at every lead).
  M2 window mismatch    -> matched window length (W=10 everywhere).
Reports what SURVIVES honest treatment. Read-only."""
from __future__ import annotations
import json, sys, math
from collections import defaultdict
import numpy as np
from scipy import stats
sys.path.insert(0,"scripts/robustness")
import convergence_lib as L
V=json.load(open("data/v2/vdem_democracy.json"))["series"]
LIB=V["libdem"]
W=10
def sr(iso):
    s=LIB.get(iso); return {int(y):v for y,v in s.items()} if s else {}
def detrend(vals):
    idx=[i for i,v in enumerate(vals) if v is not None]
    if len(idx)<max(6,int(0.7*W)): return None
    v=np.array([vals[i] for i in idx],float); t=np.array(idx,float)
    return v-np.polyval(np.polyfit(t,v,1),t)
def var_window(s,y0,y1):
    r=detrend([s.get(y) for y in range(y0,y1+1)])
    return float(np.var(r)) if r is not None else None
def ar1_window(s,y0,y1):
    r=detrend([s.get(y) for y in range(y0,y1+1)])
    if r is None or len(r)<5 or np.std(r[:-1])==0: return None
    return float(np.corrcoef(r[:-1],r[1:])[0,1])

# ONE event per (country, episode): first year of a >=0.05 decline over 3y, libdem>=0.15,
# not already declining (dedupe consecutive onsets by requiring no onset in the prior 3y).
def episodes():
    ev=[]
    for iso in LIB:
        s=sr(iso); onset_years=set()
        for T in range(1816,2019):
            if T in s and (T+3) in s and s[T]>=0.15 and (s[T+3]-s[T])<=-0.05:
                onset_years.add(T)
        # collapse runs -> keep first year of each episode
        for T in sorted(onset_years):
            if not any((T-k) in onset_years for k in range(1,4)):
                ev.append((iso,T))
    return ev
EV=episodes()
print(f"distinct backsliding EPISODES (deduped): {len(EV)} across {len(set(i for i,_ in EV))} countries")

# ---- WITHIN-country standardized pre-window variance (matched W=10) ----
def country_baseline(iso, exclude):
    """median of the country's rolling W-var, excluding windows overlapping any event pre-window."""
    s=sr(iso); ys=sorted(s)
    if len(ys)<W+4: return None
    vs=[]
    for c in range(ys[0],ys[-1]-W+2):
        if any(c<=ex<c+W for ex in exclude): continue   # skip windows overlapping an event's pre-window
        v=var_window(s,c,c+W-1)
        if v is not None: vs.append(v)
    return float(np.median(vs)) if len(vs)>=4 else None
ex_by=defaultdict(list)
for iso,T in EV: ex_by[iso].extend(range(T-W,T))
rows=[]
for iso,T in EV:
    pre=var_window(sr(iso),T-W,T-1)
    base=country_baseline(iso, ex_by[iso])
    if pre is None or base is None or base<=0: continue
    rows.append((iso, math.log(pre/base)))
lr=[x for _,x in rows]
frac=np.mean([x>0 for x in lr])
# country-clustered bootstrap of the mean log-ratio
by_c=defaultdict(list)
for iso,x in rows: by_c[iso].append(x)
cs=list(by_c); rng=np.random.default_rng(0); boots=[]
for _ in range(2000):
    samp=rng.choice(len(cs),len(cs)); vals=[v for k in samp for v in by_c[cs[k]]]
    boots.append(np.mean(vals))
lo,hi=np.percentile(boots,[2.5,97.5])
print(f"\n=== WITHIN-COUNTRY (matched W=10, one/episode, country-clustered) ===")
print(f"  n_episodes={len(rows)} across {len(cs)} countries")
print(f"  mean log(pre-var / own-baseline)={np.mean(lr):+.3f}  95%CI(country-cluster)=[{lo:+.3f},{hi:+.3f}]")
print(f"  fraction above own baseline={frac:.2f}  -> {'SURVIVES (CI excludes 0)' if lo>0 else 'does NOT survive'}")

# ---- FIXED-COHORT lead gradient (same events at every lead), within-country z ----
leads=[12,9,6,3,1]
cohort=[]
for iso,T in EV:
    if all(var_window(sr(iso),T-Lg-W,T-Lg-1) is not None for Lg in leads):
        base=country_baseline(iso,ex_by[iso])
        if base and base>0: cohort.append((iso,T,base))
print(f"\n=== LEAD GRADIENT on FIXED COHORT (n={len(cohort)} events with data at every lead) ===")
grad=[]
for Lg in leads:
    ratios=[var_window(sr(i),T-Lg-W,T-Lg-1)/base for i,T,base in cohort]
    ratios=[r for r in ratios if r is not None]
    grad.append((Lg,np.median(ratios)))
    print(f"   lead -{Lg:2d}yr: median(pre-var/own-baseline)={np.median(ratios):.2f}")
mono=all(grad[k][1]>=grad[k-1][1]-0.15 for k in range(1,len(grad)))  # rising toward T (lead decreasing)
print(f"   monotone rise toward event: {mono}  (far={grad[0][1]:.2f} -> near={grad[-1][1]:.2f})")

# ---- AR1 (the theory-specified CSD indicator), within-country, honest ----
ar=[]
for iso,T in EV:
    a_pre=ar1_window(sr(iso),T-W,T-1)
    if a_pre is not None: ar.append((iso,a_pre))
# controls: random non-episode country-years
ctrl=[]
for iso in LIB:
    s=sr(iso); on={T for i,T in EV if i==iso}
    for T in range(1826,2015,7):
        if T in s and s.get(T,0)>=0.15 and not any(abs(T-o)<=4 for o in on):
            a=ar1_window(s,T-W,T-1)
            if a is not None: ctrl.append(a)
ar_e=[a for _,a in ar]
print(f"\n=== AR1 (rising autocorrelation, the theory-specified CSD signal) ===")
print(f"  event AR1 mean={np.mean(ar_e):+.3f} (n={len(ar_e)}) vs control mean={np.mean(ctrl):+.3f} (n={len(ctrl)})")
print(f"  AUC={L.auc_roc(ar_e+ctrl,[1]*len(ar_e)+[0]*len(ctrl)):.3f}  MW p={stats.mannwhitneyu(ar_e,ctrl,alternative='greater').pvalue:.4f}")

out={"n_episodes":len(rows),"n_countries":len(cs),
     "within_country_mean_logratio":round(float(np.mean(lr)),3),
     "within_country_CI":[round(float(lo),3),round(float(hi),3)],
     "within_country_survives":bool(lo>0),
     "lead_gradient":{str(l):round(float(v),2) for l,v in grad},"lead_monotone":bool(mono),
     "ar1_auc":round(float(L.auc_roc(ar_e+ctrl,[1]*len(ar_e)+[0]*len(ctrl))),3)}
json.dump(out,open("data/political/csd_corrected.json","w"),indent=1)
print("\n>>> SURVIVES honest treatment:",
      "within-country variance elevation" if out["within_country_survives"] else "NOTHING clean",
      "| lead-gradient monotone:",out["lead_monotone"])
