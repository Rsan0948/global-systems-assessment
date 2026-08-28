#!/usr/bin/env python3
"""DEEP-TIME extension. Same math/features as the modern campaign, pushed back to 1820 using
only the deep-available signals (V-Dem regime indices 1789+, civil-society 1789+, conflict
onsets 1818+; rol_vdem as a deep CAPACITY proxy in place of the WGI-bound V1). Sweeps the lead
horizon k∈{1,3,5,10,20,30} and analyses by ERA. Metric = mean per-COHORT partial-Spearman of
the feature with the forward outcome, NET of the lagged outcome level (persistence) — one row
per country per base-year cohort, averaged across cohorts (no pseudoreplication, no p-hacking).
Descriptive discovery of WHERE/WHEN/at-what-HORIZON signal appears. Read-only."""
import json, math
from pathlib import Path
import numpy as np
from scipy import stats
HERE=Path(__file__).resolve().parent
MIROOT=HERE.parents[1]/"mi-research"
vd=json.load(open(MIROOT/"data/v2/vdem_democracy.json"))["series"]
LIB,ELECT,ROL=vd["libdem"],vd["electdem"],vd["rol_vdem"]
CSO=json.load(open(MIROOT/"data/political/political_indicators.json"))["series"]["cso_participation"]
ONS={k:set(v) for k,v in json.load(open(MIROOT/"data/robustness/historical/conflict_onsets.json"))["onsets"].items()}

def near(s,iso,y,tol=2):
    d=s.get(iso) if isinstance(s,dict) else None
    if not d: return None
    for dd in range(tol+1):
        for yy in ([y] if dd==0 else [y-dd,y+dd]):
            if str(yy) in d: return d[str(yy)]
    return None
def series_std(s,iso,y0,y1,need=6):
    d=s.get(iso) if isinstance(s,dict) else None
    if not d: return None
    v=[d[str(y)] for y in range(y0,y1+1) if str(y) in d]
    return float(np.std(v)) if len(v)>=need else None
def pconf(iso,b):
    ys=ONS.get(iso)
    return None if ys is None else float(sum(0.5**((b-y)/25) for y in ys if y<=b))

BASES=list(range(1820,2016,5))
LEADS=[1,3,5,10,20,30]
ERAS=[("C19  1820-99",1820,1899),("WorldWars 1900-44",1900,1944),
      ("ColdWar 1945-88",1945,1988),("Modern 1989-2015",1989,2015)]

ISOS=sorted(set(LIB)|set(CSO))

def predictors(iso,b):
    lib=near(LIB,iso,b);
    if lib is None: return None
    p={"lib":lib,"anocracy":4*lib*(1-lib),"cso":near(CSO,iso,b),"rol":near(ROL,iso,b),
       "elect":near(ELECT,iso,b),"turb_lib":series_std(LIB,iso,b-9,b),
       "turb_elect":series_std(ELECT,iso,b-9,b),"pconf":pconf(iso,b)}
    return p

# assemble raw predictor rows per base year, then z-normalize within each base-year cross-section
PANEL={}   # base -> list of (iso, praw)
for b in BASES:
    rows=[]
    for iso in ISOS:
        p=predictors(iso,b)
        if p: rows.append((iso,p))
    PANEL[b]=rows

ZFIELDS=["anocracy","cso","rol","turb_lib","turb_elect","pconf","lib","elect"]
def znorm(rows):
    ref={}
    for f in ZFIELDS:
        vals=[p[f] for _,p in rows if p.get(f) is not None]
        if len(vals)>=10:
            mu=float(np.mean(vals)); sd=float(np.std(vals)) or 1.0; ref[f]=(mu,sd)
    out={}
    for iso,p in rows:
        z={}
        for f in ZFIELDS:
            if p.get(f) is not None and f in ref:
                z[f]=(p[f]-ref[f][0])/ref[f][1]
        out[iso]=(p,z)
    return out
ZPANEL={b:znorm(rows) for b,rows in PANEL.items()}

def feats(iso,b):
    d=ZPANEL[b].get(iso)
    if not d: return None
    p,z=d; f=dict(z)  # raw z singles: anocracy, cso, rol, turb_lib, pconf...
    def g(a,c): return z[a]-z[c] if a in z and c in z else None
    f["gap_rol_turb"]=g("rol","turb_lib")       # capacity - turbulence (deep analog of the modern winner)
    f["gap_rol_anoc"]=g("rol","anocracy")
    f["gap_cso_turb"]=g("cso","turb_lib")
    f["gap_anoc_turb"]=g("anocracy","turb_lib")
    f["gap_cso_anoc"]=g("cso","anocracy")
    zs=[z.get(k) for k in ("anocracy","cso","rol","turb_lib") if z.get(k) is not None]
    f["dispersion"]=float(np.std(zs)) if len(zs)>=3 else None
    return f

FEATURES=["anocracy","cso","rol","turb_lib","pconf","gap_rol_turb","gap_rol_anoc",
          "gap_cso_turb","gap_anoc_turb","gap_cso_anoc","dispersion"]

def outcome(iso,b,k,which):
    lb=near(LIB,iso,b)
    if which in ("backslide","democratize"):
        lc=near(LIB,iso,b+k)
        if lb is None or lc is None: return None
        if which=="backslide":   return 1.0 if (lc-lb)<=-0.05 else 0.0
        else:                    return 1.0 if (lc-lb)>= 0.05 else 0.0
    if which=="onset":
        ys=ONS.get(iso);
        return None if ys is None else (1.0 if any(b<y<=b+k for y in ys) else 0.0)
    return None
# AR control (persistence) per outcome
def arctrl(iso,b,which):
    return near(LIB,iso,b) if which in ("backslide","democratize") else pconf(iso,b)

def partial(x,y,z):
    x=np.array(x,float);y=np.array(y,float);z=np.array(z,float)
    rx,ry,rz=stats.rankdata(x),stats.rankdata(y),stats.rankdata(z)
    Z=np.column_stack([np.ones(len(x)),rz])
    bx=np.linalg.lstsq(Z,rx,rcond=None)[0]; by=np.linalg.lstsq(Z,ry,rcond=None)[0]
    ex,ey=rx-Z@bx, ry-Z@by
    if np.std(ex)<1e-12 or np.std(ey)<1e-12: return None   # degenerate cohort (constant residual)
    return float(stats.pearsonr(ex,ey).statistic)

def cohort_rho(feat_name,which,k,b):
    rows=[]
    for iso,_ in PANEL[b]:
        f=feats(iso,b)
        if not f or f.get(feat_name) is None: continue
        y=outcome(iso,b,k,which); ar=arctrl(iso,b,which)
        if y is None or ar is None: continue
        rows.append((f[feat_name],y,ar))
    if len(rows)<25: return None
    ys=[r[1] for r in rows]
    if len(set(ys))<2: return None
    pr=partial([r[0] for r in rows],ys,[r[2] for r in rows])
    return None if pr is None else (pr, len(rows), int(sum(ys)))

def era_skill(feat_name,which,k,e0,e1):
    rhos=[];ns=[];pos=[]
    for b in BASES:
        if not (e0<=b<=e1): continue
        r=cohort_rho(feat_name,which,k,b)
        if r: rhos.append(r[0]);ns.append(r[1]);pos.append(r[2])
    if len(rhos)<2: return None
    return {"mean_rho":round(float(np.mean(rhos)),3),"n_cohorts":len(rhos),
            "med_n":int(np.median(ns)),"tot_pos":int(sum(pos)),
            "sign_frac":round(float(np.mean([np.sign(r)==np.sign(np.mean(rhos)) for r in rhos])),2)}

if __name__=="__main__":
    report={}
    for which in ["backslide","democratize","onset"]:
        print("\n"+"="*96); print(f"OUTCOME: {which}   (mean per-cohort partial-rho, net of persistence)"); print("="*96)
        # best feature per era at k=5
        print(f"\n  best deep feature per era @ k=5:")
        for elab,e0,e1 in ERAS:
            scored=[(f,era_skill(f,which,5,e0,e1)) for f in FEATURES]
            scored=[(f,s) for f,s in scored if s]
            if not scored: print(f"    {elab:20}: (insufficient)"); continue
            f,s=max(scored,key=lambda t:abs(t[1]["mean_rho"]))
            print(f"    {elab:20}: {f:14} rho={s['mean_rho']:+.3f} (cohorts={s['n_cohorts']}, medN={s['med_n']}, pos={s['tot_pos']}, sign={s['sign_frac']})")
        # lead-horizon sweep for the strongest features
        print(f"\n  LEAD-HORIZON sweep (mean rho by k), pooled all eras 1820-2015:")
        allrho={f:{} for f in FEATURES}
        for f in FEATURES:
            for k in LEADS:
                rr=[cohort_rho(f,which,k,b) for b in BASES]
                rr=[x[0] for x in rr if x]
                if len(rr)>=3: allrho[f][k]=round(float(np.mean(rr)),3)
        # show the features with the biggest |rho| at any k
        rank=sorted(FEATURES,key=lambda f:-max([abs(v) for v in allrho[f].values()] or [0]))
        print(f"    {'feature':14} " + " ".join(f"k={k:>2}" for k in LEADS))
        for f in rank[:6]:
            print(f"    {f:14} " + " ".join(f"{allrho[f].get(k,float('nan')):+.2f}" if k in allrho[f] else "  .  " for k in LEADS))
        report[which]={"lead_sweep":allrho,
                       "era_k5":{elab:{f:era_skill(f,which,5,e0,e1) for f in FEATURES} for elab,e0,e1 in ERAS}}
    json.dump(report,open(HERE/"deep_time_results.json","w"),indent=1)
    print("\nsaved deep_time_results.json")
