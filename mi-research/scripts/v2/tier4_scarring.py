#!/usr/bin/env python3
"""Tier 4 — Structural Scarring. Does accumulated conflict damage (S1 history w/ decay + S2
trust + S3 displacement + S4 state-perpetration) predict conflict RECURRENCE beyond current
capacity (V1) and pressure (V3)? Base 2012 -> conflict onset 2013-2024. Decay half-life is a
tested parameter. Frozen spec: docs/TIER4_SCARRING_PREREGISTRATION.md (sha256 3f6d0907)."""
from __future__ import annotations
import json, csv, sys, math
from collections import defaultdict
from pathlib import Path
import numpy as np
from scipy import stats
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT)); sys.path.insert(0,str(ROOT/"scripts/robustness"))
import convergence_lib as L
POL=json.load(open(ROOT/"data/political/political_indicators.json"))["series"]
T4=json.load(open(ROOT/"data/political/tier4_indicators.json"))["series"]
lib=json.load(open(ROOT/"data/v2/vdem_democracy.json"))["series"]["libdem"]
NM=json.load(open(ROOT/"data/political/_epr_name_iso.json"))
EPRc={NM[k]:v["excluded_pop_share"] for k,v in POL["epr_by_statename"].items() if k in NM}
NAME={r["iso3"]:r["country"] for r in csv.DictReader(open(ROOT/"../mi-pipeline/data/wb_cached.csv"))}
WBC=defaultdict(dict)
for r in csv.DictReader(open(ROOT/"../mi-pipeline/data/wb_cached.csv")): WBC[r["iso3"]][r["year"]]=r
WGI=["GovEff","RuleLaw","RegQual","CtrlCorr"]
def p1(iso,y=2012):
    r=WBC.get(iso,{}).get(str(y));
    if not r: return None
    v=[r.get(k) for k in WGI]; return None if any(x in(None,"") for x in v) else float(np.mean([float(x) for x in v]))
def gdp(iso,y=2012):
    r=WBC.get(iso,{}).get(str(y)); v=r.get("GDPpcPPP") if r else None
    return float(v) if v not in(None,"") else None
def near(d,iso,y,tol=6):
    s=d.get(iso) if isinstance(d,dict) else None
    if not s: return None
    s={int(k):v for k,v in s.items()}
    for dd in range(tol+1):
        for yy in ([y] if dd==0 else [y-dd,y+dd]):
            if yy in s: return s[yy]
    return None
def libv(iso,y=2012):
    return near({k:v for k,v in lib.items()},iso,y,4)
# onsets by iso with origin
CL=json.load(open(ROOT/"data/robustness/contagion/crisis_classification.json"))["classification_primary"]
onsets=defaultdict(list)   # iso -> [(year, is_domestic)]
for key,orig in CL.items():
    iso,yr=key.split("|"); onsets[iso].append((int(yr),"domestic" in orig))
def dom_onset(iso,y0,y1): return 1 if any(y0<=yr<=y1 and dm for yr,dm in onsets.get(iso,[])) else 0

BASE=2012
def build(halflife):
    lam=math.log(2)/halflife
    pop=T4.get("population",{}); ref=T4.get("refugees_origin",{}); trust=T4.get("trust",{}); pts=POL.get("pts",{})
    rows=[]
    for iso in sorted(set(WBC)|set(onsets)):   # REPRODUCIBILITY: pin row order (was hash-randomized)
        P1=p1(iso); G=gdp(iso); lb=libv(iso)
        if P1 is None or G is None or lb is None: continue
        # S1: decay-weighted prior onsets (civil 1.0, interstate 0.5), before BASE
        s1=sum((1.0 if dm else 0.5)*math.exp(-lam*(BASE-yr)) for yr,dm in onsets.get(iso,[]) if yr<BASE)
        # S4: decay-weighted years PTS>=4 before BASE (state perpetration)
        s4=sum(math.exp(-lam*(BASE-y)) for y in range(1976,BASE) if (near(pts,iso,y,0) or 0)>=4)
        # S2 trust (inverted), S3 refugees %pop + youth x recency
        tr=near(trust,iso,BASE,8)
        rf=near(ref,iso,BASE,4); pp=near(pop,iso,BASE,2)
        refshare=(rf/pp*100) if (rf is not None and pp) else None
        yv=near(POL.get("youth_0014"),iso,BASE)
        recency=max((math.exp(-lam*(BASE-yr)) for yr,dm in onsets.get(iso,[]) if yr<BASE), default=0)
        youth_x=(yv*recency) if yv is not None else None
        rows.append({"iso":iso,"name":NAME.get(iso,iso),"P1":P1,"lg":math.log10(G),
            "ano":4*lb*(1-lb),"cso":near(POL.get("cso_participation"),iso,BASE),
            "excl":EPRc.get(iso),"youth":yv,
            "s1":s1,"s4":s4,"trust":tr,"refshare":refshare,"youth_x":youth_x,
            "raw_prior":dom_onset(iso,BASE-20,BASE-1),
            "conflict":dom_onset(iso,BASE+1,2024)})
    # normalize sub-dims 0-100
    def pctf(vals):
        a=np.array([v for v in vals if v is not None],float); lo,hi=np.percentile(a,5),np.percentile(a,95)
        return (lambda v: float(np.clip((v-lo)/(hi-lo)*100,0,100))) if hi>lo else (lambda v:50.0)
    nS1=pctf([r["s1"] for r in rows]); nS4=pctf([r["s4"] for r in rows])
    nref=pctf([r["refshare"] for r in rows if r["refshare"] is not None]); nyx=pctf([r["youth_x"] for r in rows if r["youth_x"] is not None])
    # AUDIT H4 FIX: S2 (distrust) must be 5/95 percentile-normalized like S1/S3/S4. Previously it
    # was raw 100-trust (median ~77, floor ~25 vs ~50 for the normalized dims), which pushed the
    # composite ~5pts up specifically for WVS-surveyed (stabler) countries -> spurious "scarring".
    nS2=pctf([100-r["trust"] for r in rows if r["trust"] is not None])
    for r in rows:
        r["S1"]=nS1(r["s1"]); r["S4"]=nS4(r["s4"])
        r["S2"]=nS2(100-r["trust"]) if r["trust"] is not None else None
        s3=[x for x in [nref(r["refshare"]) if r["refshare"] is not None else None, nyx(r["youth_x"]) if r["youth_x"] is not None else None] if x is not None]
        r["S3"]=float(np.mean(s3)) if s3 else None
        # composite with available dims, weights renormalized
        w={"S1":.40,"S2":.20,"S3":.20,"S4":.20}; num=den=0
        for k in ["S1","S2","S3","S4"]:
            if r[k] is not None: num+=w[k]*r[k]; den+=w[k]
        r["S"]=num/den if den else None
        r["track"]=sum(1 for k in ["S1","S2","S3","S4"] if r[k] is not None)
    return rows

def cv_auc(cols,y,k=5,seed=0):
    y=np.array(y,float); n=len(y); idx=np.arange(n); rng=np.random.default_rng(seed); rng.shuffle(idx)
    X=np.column_stack([np.ones(n)]+[L.zscore(c) for c in cols]); aucs=[]
    for f in range(k):
        te=np.array_split(idx,k)[f]; tr=np.setdiff1d(idx,te)
        if len(set(y[tr].tolist()))<2 or len(set(y[te].tolist()))<2: continue
        b,_,_=L.logit_fit(X[tr],y[tr]); p=1/(1+np.exp(-(X[te]@b))); aucs.append(L.auc_roc(p,y[te]))
    return round(float(np.mean(aucs)),4) if aucs else None

# ---- T4-3: decay half-life sweep (S1-only AUC for conflict) ----
print("=== T4-3 — decay half-life sweep (S1 conflict-history AUC for conflict onset) ===")
best=None
for hl in [15,25,50,75]:
    rows=build(hl); sub=[r for r in rows if r["conflict"] is not None]
    y=[r["conflict"] for r in sub]; a=L.auc_roc([r["S1"] for r in sub],y)
    print(f"   half-life {hl}y: S1-AUC={a:.3f} (n={len(sub)})")
    if best is None or a>best[1]: best=(hl,a)
print(f"   >>> optimal half-life: {best[0]}y (AUC {best[1]:.3f})\n")

rows=build(best[0])
sub=[r for r in rows if r["conflict"] is not None and r["S"] is not None]
y=[r["conflict"] for r in sub]
print(f"n={len(sub)} conflict_pos={sum(y)} | tracks:",{t:sum(1 for r in sub if r['track']==t) for t in [1,2,3,4]})

# ---- T4-1 (GATE): incremental AUC ----
# AUDIT H5 FIX: previously missing cso/excl/youth were imputed as raw 0. For excl (EPR share in
# [0,1]) and youth, 0 is the MINIMUM ("no excluded group"), not a neutral value -> it coded
# data-gap countries as low-risk, weakening the V1+V3 baseline and mechanically enlarging the
# Tier-4 increment. Impute the observed MEAN instead (z-scores to ~0, genuinely neutral).
def meanimp(key):
    obs=[r[key] for r in sub if r.get(key) is not None]
    mu=float(np.mean(obs)) if obs else 0.0
    return [r[key] if r.get(key) is not None else mu for r in sub]
V1=[[r["P1"] for r in sub],[r["lg"] for r in sub]]
V3=[meanimp("ano"),meanimp("cso"),meanimp("excl"),meanimp("youth")]
T4c=[[r["S"] for r in sub]]
def rep_cv(cols,seeds=range(50)):
    a=[cv_auc(cols,y,seed=sd) for sd in seeds]; a=[x for x in a if x is not None]
    return float(np.mean(a)) if a else None
a_v1=rep_cv(V1); a_v3=rep_cv(V3); a_v1v3=rep_cv(V1+V3); a_all=rep_cv(V1+V3+T4c)
# increment CI over seeds
inc=[cv_auc(V1+V3+T4c,y,seed=sd)-cv_auc(V1+V3,y,seed=sd) for sd in range(50)]
lo,hi=np.percentile(inc,[2.5,97.5])
print(f"\n=== T4-1 (GATE) — incremental AUC (50-seed repeated 5-fold CV, mean-imputed) ===")
print(f"   V1={a_v1:.4f}  V3={a_v3:.4f}  V1+V3={a_v1v3:.4f}  V1+V3+Tier4={a_all:.4f}")
print(f"   increment={np.mean(inc):+.4f} CI[{lo:+.4f},{hi:+.4f}] pos-frac={np.mean([x>0 for x in inc]):.2f}  PASS(CI>0)={lo>0}")

# ---- T4-6 (crux): does S mediate the raw prior-conflict binary? ----
yy=np.array(y,float); n=len(yy)
def logit_coef(cols):
    X=np.column_stack([np.ones(n)]+[L.zscore(c) for c in cols]); b,_,_=L.logit_fit(X,yy)
    # bootstrap SE
    rng=np.random.default_rng(0); bs=[]
    for _ in range(300):
        ix=rng.integers(0,n,n)
        if len(set(yy[ix].tolist()))<2: continue
        bb,_,_=L.logit_fit(X[ix],yy[ix]); bs.append(bb)
    se=np.std(bs,axis=0)
    return b,se
rawcol=[r["raw_prior"] for r in sub]; Scol=[r["S"] for r in sub]
b_raw,se_raw=logit_coef([rawcol])
b_both,se_both=logit_coef([rawcol,Scol])
print(f"\n=== T4-6 (crux) — does the composite S mediate the raw conflict-trap binary? ===")
print(f"   raw_prior alone:      coef={b_raw[1]:+.3f} (z={b_raw[1]/se_raw[1]:+.2f})")
print(f"   raw_prior + S-Score:  raw coef={b_both[1]:+.3f} (z={b_both[1]/se_both[1]:+.2f})  S coef={b_both[2]:+.3f} (z={b_both[2]/se_both[2]:+.2f})")
print(f"   >>> raw binary {'SURVIVES (composite under-captures the trap)' if abs(b_both[1]/se_both[1])>2 else 'ABSORBED by S (mediated)'}")

# ---- T4-4: does Tier4 flag the conflicts V1+V3 miss? ----
Xv=np.column_stack([np.ones(n)]+[L.zscore(c) for c in V1+V3]); bb,_,_=L.logit_fit(Xv,yy); pv=1/(1+np.exp(-(Xv@bb)))
missed=[r["S"] for r,p,yl in zip(sub,pv,y) if yl==1 and p<np.median(pv)]
quiet=[r["S"] for r,p,yl in zip(sub,pv,y) if yl==0]
print(f"\n=== T4-4 — does Tier4 flag conflicts V1+V3 missed? ===")
print(f"   missed-conflict mean Tier4={np.mean(missed):.1f} (n={len(missed)}) vs correctly-quiet mean={np.mean(quiet):.1f}  (higher=Tier4 catches them)")

out={"prereg":"3f6d0907","optimal_halflife":best[0],"n":len(sub),
     "T4_3_sweep":{hl:round(L.auc_roc([r["S1"] for r in build(hl) if r["conflict"] is not None],[r["conflict"] for r in build(hl) if r["conflict"] is not None]),3) for hl in [15,25,50,75]},
     "T4_1":{"V1":a_v1,"V3":a_v3,"V1+V3":a_v1v3,"V1+V3+T4":a_all,"increment":round(a_all-a_v1v3,4),"pass":bool(a_all-a_v1v3>=0.03)},
     "T4_6":{"raw_alone_z":round(b_raw[1]/se_raw[1],2),"raw_with_S_z":round(b_both[1]/se_both[1],2),"S_z":round(b_both[2]/se_both[2],2)},
     "T4_4":{"missed_conflict_meanT4":round(float(np.mean(missed)),1),"quiet_meanT4":round(float(np.mean(quiet)),1)},
     "scores":[{"iso":r["iso"],"name":r["name"],"S":round(r["S"],1) if r["S"] is not None else None,"S1":round(r["S1"],1),"track":r["track"]} for r in sorted(rows,key=lambda x:-(x["S"] or 0))]}
(ROOT/"data/political/tier4_scarring.json").write_text(json.dumps(out,indent=1))
print("\n=== most-scarred (S-Score) ===")
for r in sorted([r for r in rows if r["S"] is not None],key=lambda x:-x["S"])[:15]:
    print(f"   {r['name']:22s} S={r['S']:4.0f}  (S1={r['S1']:.0f} S2={r['S2'] if r['S2'] is not None else '-'} S3={r['S3'] if r['S3'] is not None else '-':} S4={r['S4']:.0f}) track{r['track']}")
