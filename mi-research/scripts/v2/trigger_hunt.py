#!/usr/bin/env python3
"""TRIGGER HUNT. The 'Mule' = the spark that converts structural pressure into rupture at a
specific time. Claim: unmeasurable. But criticality theory says you can't predict WHICH grain
triggers the avalanche, yet you CAN measure how close the pile is to the critical slope via
CRITICAL SLOWING DOWN — rising lag-1 autocorrelation (AR1) and variance in the state variable
as a system nears a tipping point (Scheffer/Dakos universal early-warning signals). This hunts
that signal in political systems: do CSD indicators rise before conflict onset / backsliding?
Read-only. NOT the spark — the ripeness for a spark."""
from __future__ import annotations
import json, sys, math
from collections import defaultdict
import numpy as np
from scipy import stats
sys.path.insert(0, "scripts/robustness"); sys.path.insert(0, ".")
import convergence_lib as L
G=json.load(open("data/v2/exploratory_outcomes.json"))["series"]["gdp_pc_growth"]
LIB=json.load(open("data/v2/vdem_democracy.json"))["series"]["libdem"]
dom=L.domestic_years()

def series(d, iso, y0, y1):
    s=d.get(iso)
    if not s: return None
    out=[]
    for y in range(y0, y1+1):
        v=s.get(str(y)) if str(y) in s else (s.get(y) if y in s else None)
        out.append(v)
    return out if sum(v is not None for v in out)>=8 else None

def detrend(vals):
    idx=[i for i,v in enumerate(vals) if v is not None]
    v=np.array([vals[i] for i in idx],float); t=np.array(idx,float)
    if len(v)<8: return None
    resid=v-np.polyval(np.polyfit(t,v,1),t)
    return resid

def ar1(x):
    if len(x)<4: return None
    a,b=x[:-1],x[1:]
    if np.std(a)==0 or np.std(b)==0: return None
    return float(np.corrcoef(a,b)[0,1])

def csd(vals):
    """CSD indicators on a pre-window: AR1, variance, and their rising trend (2nd half - 1st half)."""
    r=detrend(vals)
    if r is None or len(r)<10: return None
    half=len(r)//2
    a_full=ar1(r); v_full=float(np.var(r))
    a1,a2=ar1(r[:half]), ar1(r[half:]); v1,v2=np.var(r[:half]), np.var(r[half:])
    return {"ar1":a_full,"var":v_full,
            "d_ar1":(a2-a1) if (a1 is not None and a2 is not None) else None,
            "d_var":(v2-v1)/v1 if v1>0 else None,
            "skew":float(stats.skew(r))}

def onset(iso,y0,y1): return any(y0<=y<=y1 for y in dom.get(iso,set()))

def run(statename, D, backsliding=False):
    ev,ctl=[],[]
    isos=set(D)&(set(LIB) if backsliding else set(D))
    for iso in D:
        yrs=range(1972,2016)
        for T in yrs:
            pre=series(D,iso,T-12,T-1)
            if pre is None: continue
            c=csd(pre)
            if c is None or c["ar1"] is None: continue
            if backsliding:
                l0=LIB.get(iso,{}).get(str(T)); l3=LIB.get(iso,{}).get(str(T+3))
                if l0 is None or l3 is None or l0<0.15: continue
                is_ev=(l3-l0)<=-0.05; is_ctl=(l3-l0)>-0.01
            else:
                is_ev=onset(iso,T,T+1); is_ctl=not onset(iso,T-3,T+3)
            if is_ev: ev.append(c)
            elif is_ctl: ctl.append(c)
    res={"n_event":len(ev),"n_control":len(ctl)}
    for k in ["ar1","var","d_ar1","d_var","skew"]:
        e=[c[k] for c in ev if c.get(k) is not None]; cc=[c[k] for c in ctl if c.get(k) is not None]
        if len(e)<15 or len(cc)<15: continue
        u=stats.mannwhitneyu(e,cc,alternative="greater")
        # AUC = P(event indicator > control)
        auc=float(L.auc_roc(e+cc,[1]*len(e)+[0]*len(cc)))
        res[k]={"event_mean":round(float(np.mean(e)),4),"control_mean":round(float(np.mean(cc)),4),
                "MW_p_greater":round(float(u.pvalue),4),"AUC":round(auc,3),"n_e":len(e)}
    # combined CSD score (z-sum of ar1 + var + d_ar1), AUC for the event
    rows=[(c,1) for c in ev]+[(c,0) for c in ctl]
    def z(vals):
        a=np.array(vals,float); return (a-np.nanmean(a))/np.nanstd(a)
    have=[(c,y) for c,y in rows if all(c.get(k) is not None for k in ["ar1","var","d_ar1"])]
    if len(have)>=40:
        score=z([c["ar1"] for c,_ in have])+z([c["var"] for c,_ in have])+z([c["d_ar1"] for c,_ in have])
        y=[y for _,y in have]
        res["combined_CSD_AUC"]=round(float(L.auc_roc(list(score),y)),3)
        res["combined_n"]=len(have)
    return res

print("="*70)
print("TRIGGER HUNT — Critical Slowing Down before rupture")
print("(rising AR1 / variance = system nearing a tipping point; NOT the spark)")
print("="*70)
print("\n### CONFLICT ONSET — state variable = annual GDP-pc growth ###")
r=run("gdp_growth",G,backsliding=False)
print(f"  events={r['n_event']}  controls={r['n_control']}")
for k in ["ar1","var","d_ar1","d_var","skew"]:
    if k in r: print(f"   {k:6s}: event={r[k]['event_mean']:+.3f} vs control={r[k]['control_mean']:+.3f} | MW p(greater)={r[k]['MW_p_greater']} | AUC={r[k]['AUC']}")
if "combined_CSD_AUC" in r: print(f"   >>> COMBINED CSD score AUC = {r['combined_CSD_AUC']} (n={r['combined_n']})")

print("\n### DEMOCRATIC BACKSLIDING — state variable = annual liberal-democracy ###")
r2=run("libdem",LIB,backsliding=True)
print(f"  events={r2['n_event']}  controls={r2['n_control']}")
for k in ["ar1","var","d_ar1","d_var","skew"]:
    if k in r2: print(f"   {k:6s}: event={r2[k]['event_mean']:+.3f} vs control={r2[k]['control_mean']:+.3f} | MW p(greater)={r2[k]['MW_p_greater']} | AUC={r2[k]['AUC']}")
if "combined_CSD_AUC" in r2: print(f"   >>> COMBINED CSD score AUC = {r2['combined_CSD_AUC']} (n={r2['combined_n']})")

json.dump({"conflict_gdp":r,"backsliding_libdem":r2},open("data/political/trigger_hunt.json","w"),indent=1)
