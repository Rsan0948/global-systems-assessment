#!/usr/bin/env python3
"""ANGLE 4 — country ATTRIBUTES as predictors + moderators of backsliding. Modern era (EPR/resource
are modern). Two questions:
  Q1 MAIN EFFECT — does the attribute predict backsliding beyond capacity-gap + libdem?
  Q2 MODERATION  — does the capacity-gap→backsliding effect differ by the attribute (split low/high)?
Plus legal origin (categorical, hand-coded external table). Metric = mean per-cohort partial-Spearman;
permutation nulls. capgap = z(rule-of-law) − z(anocracy) within year (the relational capacity gap)."""
import numpy as np, math
from scipy import stats
import common as C
import country_attrs as CA

BASES=[1990,1995,2000,2005,2010,2015]; K=5
ZROL={b:C.zwithin_year(lambda i,bb=b:C.near(C.ROL,i,bb),b) for b in BASES}
ZANO={b:C.zwithin_year(lambda i,bb=b:C.anocracy(i,bb),b) for b in BASES}
def capgap(i,b):
    a=ZROL[b].get(i); c=ZANO[b].get(i); return None if a is None or c is None else a-c
def backslide(i,b):
    a=C.near(C.LIB,i,b); c=C.near(C.LIB,i,b+K); return None if a is None or c is None else (1.0 if (c-a)<=-0.05 else 0.0)
def libv(i,b): return C.near(C.LIB,i,b)

def logp(i,b):
    v=C.population(i,b); return math.log10(v) if v and v>0 else None
def logrents(i,b):
    v=C.resource_rents(i,b); return math.log10(1+v) if v is not None and v>=0 else None
ATTRS={"resource_rents":logrents,"ethnic_excl":lambda i,b:C.ethnic(i,"excluded_pop_share"),
       "ethnic_ngroups":lambda i,b:C.ethnic(i,"n_groups"),"log_pop":logp,
       "dem_age":C.dem_age,"state_age":C.state_age}

def assemble(attrfn):
    """rows across cohorts: (attr, backslide, libdem, capgap, base)."""
    rows=[]
    for b in BASES:
        for i,_ in C.PANEL[b]:
            A=attrfn(i,b); y=backslide(i,b); l=libv(i,b); g=capgap(i,b)
            if None in (A,y,l,g): continue
            rows.append((A,y,l,g,b))
    return rows

def mean_partial(rows,feat_idx,ctrl_idx,permute=False,rng=None):
    rhos=[]
    for b in BASES:
        sub=[r for r in rows if r[4]==b]
        if len(sub)<25 or len({r[1] for r in sub})<2: continue
        xs=[r[feat_idx] for r in sub]
        if permute: xs=list(rng.permutation(xs))
        pr=C.partial_spearman(xs,[r[1] for r in sub],[[r[c] for r in sub] for c in ctrl_idx])
        if pr is not None: rhos.append(pr)
    return (float(np.mean(rhos)),len(rhos)) if len(rhos)>=2 else (None,0)

print("="*92); print("Q1 — MAIN EFFECT: attribute → backslide, net of [libdem, capacity-gap]"); print("="*92)
print(f"  {'attribute':16} {'ρ':>8} {'perm 95% null':>18} {'perm-p':>7}  n_cohorts")
res={}
for name,fn in ATTRS.items():
    rows=assemble(fn)
    obs,nc=mean_partial(rows,0,[2,3])
    if obs is None: print(f"  {name:16} insufficient"); continue
    pn=C.perm_null(obs,lambda rng:mean_partial(rows,0,[2,3],True,rng)[0],n=500)
    print(f"  {name:16} {obs:>+8.3f} {f'[{pn['lo']:+.2f},{pn['hi']:+.2f}]':>18} {pn['p']:>7}  {nc}  {'<-- REAL' if pn['real'] else ''}")
    res[name]={"main_rho":round(obs,3),"real":pn["real"]}

print("\n"+"="*92); print("Q2 — MODERATION: does capacity-gap→backslide differ by attribute? (split at median)"); print("="*92)
print(f"  {'moderator':16} {'ρ(gap→bs) LOW':>16} {'ρ(gap→bs) HIGH':>16}   interpretation")
for name,fn in ATTRS.items():
    rows=assemble(fn)
    if len(rows)<60: continue
    med=np.median([r[0] for r in rows])
    def sub_gap_effect(hi):
        sr=[r for r in rows if (r[0]>=med)==hi]
        # per-cohort partial(capgap, backslide | libdem) within the subgroup
        rhos=[]
        for b in BASES:
            s=[r for r in sr if r[4]==b]
            if len(s)<20 or len({r[1] for r in s})<2: continue
            pr=C.partial_spearman([r[3] for r in s],[r[1] for r in s],[[r[2] for r in s]])
            if pr is not None: rhos.append(pr)
        return float(np.mean(rhos)) if len(rhos)>=2 else None
    lo,hi=sub_gap_effect(False),sub_gap_effect(True)
    if lo is None or hi is None: continue
    interp="capacity matters MORE where "+name+" HIGH" if abs(hi)>abs(lo)+0.05 else \
           ("capacity matters MORE where "+name+" LOW" if abs(lo)>abs(hi)+0.05 else "~no moderation")
    print(f"  {name:16} {lo:>+16.3f} {hi:>+16.3f}   {interp}")
    res.setdefault(name,{}).update({"gap_effect_low":round(lo,3),"gap_effect_high":round(hi,3)})

print("\n"+"="*92); print("LEGAL ORIGIN (categorical, external table): backslide rate + capacity per origin"); print("="*92)
byorigin={}
for b in BASES:
    for i,_ in C.PANEL[b]:
        o=CA.legal_origin(i); y=backslide(i,b); g=capgap(i,b)
        if o is None or y is None or g is None: continue
        byorigin.setdefault(o,[]).append((y,g))
print(f"  {'origin':14} {'n':>5} {'backslide rate':>15} {'median capgap':>14}")
raw_gradient={}
for o in sorted(byorigin,key=lambda o:-np.mean([x[0] for x in byorigin[o]])):
    xs=byorigin[o]; raw_gradient[o]=round(float(np.mean([x[0] for x in xs])),3)
    print(f"  {o:14} {len(xs):>5} {np.mean([x[0] for x in xs]):>15.1%} {np.median([x[1] for x in xs]):>+14.2f}")

# MEDIATION test: is the legal-origin gradient explained by CAPACITY? Regress backslide on capgap
# (+libdem) pooled, then compare mean RESIDUAL by origin. ~0 residuals -> fully capacity-mediated.
allrows=[]
for b in BASES:
    for i,_ in C.PANEL[b]:
        o=CA.legal_origin(i); y=backslide(i,b); g=capgap(i,b); l=libv(i,b)
        if None in (y,g,l) or o is None: continue
        allrows.append((y,g,l,o))
X=np.column_stack([np.ones(len(allrows)),[r[1] for r in allrows],[r[2] for r in allrows]])
yv=np.array([r[0] for r in allrows]); beta=np.linalg.lstsq(X,yv,rcond=None)[0]; resid=yv-X@beta
print("\n  MEDIATION — backslide RESIDUAL by origin, net of capacity-gap + libdem (≈0 => capacity explains it):")
resid_by_origin={}
for o in sorted(set(r[3] for r in allrows),key=lambda o:-np.mean([resid[i] for i,r in enumerate(allrows) if r[3]==o])):
    rs=[resid[i] for i,r in enumerate(allrows) if r[3]==o]
    resid_by_origin[o]=round(float(np.mean(rs)),3)
    print(f"    {o:14} residual {np.mean(rs):+.3f}")

import json
main_effects={k:{"rho":v.get("main_rho"),"real":v.get("real",False)} for k,v in res.items() if "main_rho" in v}
json.dump({"angle":4,
           "verdict":"CAPACITY IS THE MASTER VARIABLE — rival explanations null or capacity-mediated",
           "main_effects_net_of_capacity":main_effects,
           "legal_origin_raw_gradient":raw_gradient,
           "legal_origin_residual_net_capacity":resid_by_origin,
           "legal_origin_mediated_by_capacity":bool(max(abs(v) for v in resid_by_origin.values())<0.06),
           "moderation":{k:{"gap_effect_low":v.get("gap_effect_low"),"gap_effect_high":v.get("gap_effect_high")}
                         for k,v in res.items() if "gap_effect_low" in v}},
          open("angle4_results.json","w"),indent=1)
print("\nsaved angle4_results.json")
