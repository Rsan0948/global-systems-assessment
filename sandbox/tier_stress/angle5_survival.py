#!/usr/bin/env python3
"""ANGLE 5 — SURVIVAL / hazard of democratic breakdown by DEMOCRACY AGE (current spell).
Discrete-time hazard: each democratic country-year (libdem>=0.5) is at risk; the EVENT is spell
termination (libdem drops below 0.5 next year). Right-censored (ongoing spells / data end contribute
at-risk years, no event). Questions:
  1) SHAPE — does hazard DECLINE with age (front-loaded fragility / consolidation) or stay flat?
  2) Is it AGE or CAPACITY? — does the age effect survive controlling for rule-of-law capacity,
     or are 'young democracies' and 'capacity-poor democracies' the same statement?
Within-country permutation null (shuffle events within each country -> respects clustering)."""
import numpy as np, math
from scipy import stats
import common as C

YEARS=range(1900,2019)
def zrol_year(y):
    vals=[(i,C.ROL[i][str(y)]) for i in C.ROL if str(y) in C.ROL[i]]
    xs=[v for _,v in vals]
    if len(xs)<10: return {}
    mu=float(np.mean(xs)); sd=float(np.std(xs)) or 1.0
    return {i:(v-mu)/sd for i,v in vals}
ZROL={y:zrol_year(y) for y in YEARS}

def build():
    rows=[]
    for iso in C.LIB:
        for y in YEARS:
            age=C.dem_age(iso,y)                 # current-spell age; None if not democratic
            if age is None: continue
            ln=C.near(C.LIB,iso,y+1)
            if ln is None: continue              # censored: no next-year obs
            event=1.0 if ln<0.5 else 0.0         # spell terminates next year
            cap=ZROL[y].get(iso)
            if cap is None: continue
            rows.append(dict(iso=iso,y=y,age=age,event=event,cap=cap))
    return rows
ROWS=build()

def logit(Xcols,y,iters=60,lam=1e-3):
    X=np.column_stack([np.ones(len(y))]+Xcols); b=np.zeros(X.shape[1]); P=np.eye(X.shape[1])*lam; P[0,0]=0
    for _ in range(iters):
        mu=1/(1+np.exp(-np.clip(X@b,-30,30))); W=mu*(1-mu)+1e-6
        g=X.T@(mu-y)+P@b; H=X.T@(X*W[:,None])+P
        try: step=np.linalg.solve(H,g)
        except: break
        b=b-step
        if np.max(np.abs(step))<1e-8: break
    return b

y=np.array([r["event"] for r in ROWS]); logage=np.array([math.log(1+r["age"]) for r in ROWS])
cap=np.array([r["cap"] for r in ROWS])
n_events=int(y.sum()); n_risk=len(y)
print("="*84)
print(f"Democratic person-years at risk: {n_risk}   breakdown events: {n_events}   base hazard {y.mean():.3f}/yr")
print("="*84)

print("\n1) HAZARD by democracy-age bin (spell termination rate per year at risk)")
print(f"   {'age bin':>10} {'at-risk':>9} {'events':>7} {'hazard/yr':>11}")
for lo,hi in [(0,4),(5,9),(10,19),(20,39),(40,300)]:
    m=[(lo<=r["age"]<=hi) for r in ROWS]; ar=sum(m); ev=sum(r["event"] for r,mm in zip(ROWS,m) if mm)
    label=f"{lo}-{hi}" if hi<300 else f"{lo}+"
    print(f"   {label:>10} {ar:>9} {int(ev):>7} {(ev/ar if ar else 0):>11.3f}")

print("\n2) DISCRETE-TIME LOGIT hazard  (coef<0 on log-age = front-loaded / consolidation)")
b1=logit([logage],y); print(f"   event ~ log_age            : age coef = {b1[1]:+.3f}")
b2=logit([logage,cap],y); print(f"   event ~ log_age + capacity : age coef = {b2[1]:+.3f}   capacity coef = {b2[2]:+.3f}")
print(f"   -> age effect {'SURVIVES capacity control' if abs(b2[1])>0.5*abs(b1[1]) and np.sign(b2[1])==np.sign(b1[1]) else 'is ABSORBED by capacity'}"
      f" (shrinks {b1[1]:+.3f} -> {b2[1]:+.3f})")

print("\n3) WITHIN-COUNTRY PERMUTATION NULL for the age coef (shuffle events within each country)")
by_iso={}
for i,r in enumerate(ROWS): by_iso.setdefault(r["iso"],[]).append(i)
rng=np.random.default_rng(0); null=[]
for _ in range(800):
    ysh=y.copy()
    for idxs in by_iso.values():
        if len(idxs)>1: ysh[idxs]=y[np.array(idxs)][rng.permutation(len(idxs))]
    null.append(logit([logage],ysh)[1])
lo,hi=np.percentile(null,[2.5,97.5]); p=float(np.mean([abs(v)>=abs(b1[1]) for v in null]))
print(f"   observed age coef {b1[1]:+.3f}   null 95% [{lo:+.3f},{hi:+.3f}]  perm-p={p:.4f} -> {'REAL' if (b1[1]<lo or b1[1]>hi) else 'null'}")

# robustness: erosion event (Δlibdem<=-0.10 over next 3y) instead of hard exit
def erosion():
    yy=[]
    for r in ROWS:
        a=C.near(C.LIB,r["iso"],r["y"]); c=C.near(C.LIB,r["iso"],r["y"]+3)
        yy.append(1.0 if a is not None and c is not None and (a-c)>=0.10 else 0.0)
    return np.array(yy)
ye=erosion(); be=logit([logage],ye); be2=logit([logage,cap],ye)
print(f"\n4) ROBUSTNESS — soft EROSION event (Δlibdem≤−0.10 / 3y): age coef {be[1]:+.3f} -> +cap {be2[1]:+.3f} (cap {be2[2]:+.3f})")

haz_young=sum(r["event"] for r in ROWS if r["age"]<=4)/max(1,sum(1 for r in ROWS if r["age"]<=4))
haz_old=sum(r["event"] for r in ROWS if r["age"]>=40)/max(1,sum(1 for r in ROWS if r["age"]>=40))
import json
json.dump({"angle":5,"n_risk":n_risk,"n_events":n_events,
           "hazard_young_0_4":round(haz_young,3),"hazard_old_40plus":round(haz_old,3),
           "age_coef":round(float(b1[1]),3),"age_coef_net_capacity":round(float(b2[1]),3),
           "capacity_coef":round(float(b2[2]),3),"age_perm_p":round(p,4),
           "age_real":bool(b1[1]<lo or b1[1]>hi),
           "age_absorbed_by_capacity":bool(abs(b2[1])<=0.5*abs(b1[1]) or np.sign(b2[1])!=np.sign(b1[1])),
           "erosion_age_coef":round(float(be[1]),3),"erosion_age_net_cap":round(float(be2[1]),3)},
          open("angle5_results.json","w"),indent=1)
print("\nsaved angle5_results.json")
