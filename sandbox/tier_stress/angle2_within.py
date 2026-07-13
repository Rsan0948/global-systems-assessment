#!/usr/bin/env python3
"""ANGLE 2 — WITHIN-COUNTRY identification. All prior results are cross-country; this asks whether
a country backslides when ITS OWN capacity dips below its OWN historical norm (fixed effects),
removing every cross-country confound. Decomposes the association into:
  POOLED   : corr over all (country,time)                 [what we mostly reported]
  BETWEEN  : corr across country MEANS                     [are high-capacity countries just stabler?]
  WITHIN   : mean of per-country over-time corr            [does a country's OWN dip predict its OWN fall?]
Non-overlapping windows (step=k) so within-country obs are ~independent; per-country ρ then averaged
(one number per country -> no pseudoreplication); within-country permutation null (shuffle time in
each country). Predictors: rol capacity (deep), rol−cso gap (deep), WGI v1_mi (modern, independent)."""
import numpy as np
from scipy import stats
import common as C

def zyear(series, lo=1880, hi=2020):
    """within-year z of a series across countries, for each year."""
    Z={}
    for y in range(lo,hi+1):
        vals=[(i,series[i][str(y)]) for i in series if str(y) in series[i]]
        xs=[v for _,v in vals]
        if len(xs)<10: continue
        mu=float(np.mean(xs)); sd=float(np.std(xs)) or 1.0
        Z[y]={i:(v-mu)/sd for i,v in vals}
    return Z
ZROL=zyear(C.ROL); ZCSO=zyear(C.CSO)

def backslide(iso,y,k):
    a=C.near(C.LIB,iso,y); c=C.near(C.LIB,iso,y+k)
    return None if a is None or c is None else (1.0 if (c-a)<=-0.05 else 0.0)

def predval(kind,iso,y):
    if kind=="rol":  return ZROL.get(y,{}).get(iso)
    if kind=="gap":
        a,b=ZROL.get(y,{}).get(iso),ZCSO.get(y,{}).get(iso); return None if a is None or b is None else a-b
    if kind=="wgi":
        r=C.PRED.get(iso,{}).get(str(y)); return r.get("v1_mi") if isinstance(r,dict) else None

def series_for(kind,k,y0,y1,isos):
    """per country -> list of (P,Y,lib) at non-overlapping base years (step=k). lib = libdem level,
    used to net out within-country ceiling/mean-reversion (high-libdem years have more room to fall)."""
    out={}
    for iso in isos:
        pts=[]
        for y in range(y0,y1+1,k):
            P=predval(kind,iso,y); Y=backslide(iso,y,k); lib=C.near(C.LIB,iso,y)
            if P is not None and Y is not None and lib is not None: pts.append((P,Y,lib))
        if len(pts)>=8: out[iso]=pts
    return out

def _within_partial(pts):
    """per-country partial-Spearman(P, Y | libdem level). None if degenerate."""
    if len({p[1] for p in pts})<2: return None
    return C.partial_spearman([p[0] for p in pts],[p[1] for p in pts],[[p[2] for p in pts]])

def decompose(kind,k,y0,y1,isos,nmin_var=8):
    S=series_for(kind,k,y0,y1,isos)
    within=[]
    for iso,pts in S.items():
        if len(pts)<nmin_var: continue
        r=_within_partial(pts)
        if r is not None and not np.isnan(r): within.append(r)
    means=[(np.mean([p[0] for p in pts]),np.mean([p[1] for p in pts])) for pts in S.values() if len(pts)>=nmin_var]
    between=stats.spearmanr([m[0] for m in means],[m[1] for m in means]).statistic if len(means)>=15 else None
    allP=[p[0] for pts in S.values() for p in pts]; allY=[p[1] for pts in S.values() for p in pts]
    pooled=stats.spearmanr(allP,allY).statistic if len(allP)>=30 else None
    return {"within_mean":round(float(np.mean(within)),3) if within else None,"n_within":len(within),
            "between":round(float(between),3) if between is not None else None,"n_between":len(means),
            "pooled":round(float(pooled),3) if pooled is not None else None,"series":S}

def within_perm(S,nmin_var,n=1000,seed=0):
    """within-country permutation: shuffle Y within each country, recompute the mean partial(P,Y|lib)."""
    rng=np.random.default_rng(seed)
    good=[(iso,pts) for iso,pts in S.items() if len(pts)>=nmin_var and len({p[1] for p in pts})>=2]
    obs=[_within_partial(pts) for _,pts in good]; obs=float(np.mean([r for r in obs if r is not None and not np.isnan(r)]))
    null=[]
    for _ in range(n):
        rs=[]
        for iso,pts in good:
            ysh=list(rng.permutation([p[1] for p in pts]))
            r=C.partial_spearman([p[0] for p in pts],ysh,[[p[2] for p in pts]])
            if r is not None and not np.isnan(r): rs.append(r)
        if rs: null.append(np.mean(rs))
    lo,hi=np.percentile(null,[2.5,97.5]); p=float(np.mean([abs(v)>=abs(obs) for v in null]))
    return obs,round(float(lo),3),round(float(hi),3),round(p,4)

DEEP=sorted(set(C.LIB)&set(C.ROL))
print("="*94)
print("DEEP (1900-2010, non-overlapping 5y windows).  ρ<0 = lower capacity -> more backsliding")
print("="*94)
print(f"  {'predictor':22} {'POOLED':>8} {'BETWEEN':>9} {'WITHIN':>8} {'within 95% null':>20} {'perm-p':>7}")
for kind,lab in [("rol","rule-of-law capacity"),("gap","rol−cso gap")]:
    d=decompose(kind,5,1900,2010,DEEP)
    o,lo,hi,pp=within_perm(d["series"],8)
    print(f"  {lab:22} {str(d['pooled']):>8} {str(d['between']):>9} {o:>+8.3f} {f'[{lo:+.2f},{hi:+.2f}]':>20} {pp:>7}  "
          f"(n_between={d['n_between']}, n_within={d['n_within']})")

print("\n"+"="*94)
print("MODERN INDEPENDENT (WGI v1_mi, 1996-2016 step3, k=5) — thin but de-circularized")
print("="*94)
dm=decompose("wgi",5,1996,2016,list(C.PRED))
# modern uses step=k inside series_for; override with step 3 by re-deriving (few years) -> reuse k=5 windows
if dm["within_mean"] is not None:
    o,lo,hi,pp=within_perm(dm["series"],6,n=800)
    print(f"  WGI capacity          POOLED={dm['pooled']}  BETWEEN={dm['between']}  WITHIN={o:+.3f} [{lo:+.2f},{hi:+.2f}] perm-p={pp} (n_within={dm['n_within']})")
else:
    print("  insufficient within-country modern obs (WGI only 1996-2024)")

print("\nVerdict logic: BETWEEN<0 & WITHIN≈0 -> composition (stabler countries, not a within dynamic).")
print("              WITHIN<0 (outside null) -> real: a country's OWN capacity dip precedes its OWN backsliding.")
