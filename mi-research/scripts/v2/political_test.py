#!/usr/bin/env python3
"""Political-signal test. Does the grievance/mobilization NUMERATOR layer (ethnic exclusion,
mobilization, repression, anocracy, event-history, shock, youth, food) add political-
prediction power over structural (P1 + logGDP)? Forward-ish: ~2010 base -> 2024 outcomes.
Frozen spec: docs/POLITICAL_SIGNAL_PREREGISTRATION.md (sha256 ec4aebe0). Read-only."""
from __future__ import annotations
import json, csv, sys, math, urllib.request, io
from collections import defaultdict
from pathlib import Path
import numpy as np
from scipy import stats
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT)); sys.path.insert(0,str(ROOT/"scripts/robustness"))
import convergence_lib as L
POL=json.load(open(ROOT/"data/political/political_indicators.json"))["series"]
EXO=json.load(open(ROOT/"data/v2/exploratory_outcomes.json"))["series"]
lib=json.load(open(ROOT/"data/v2/vdem_democracy.json"))["series"]["libdem"]
WB={r["iso3"]:r for r in []}
# WGI P1 + GDP from wb_cached (per iso per year)
WBC=defaultdict(dict)
for r in csv.DictReader(open(ROOT/"../mi-pipeline/data/wb_cached.csv")):
    WBC[r["iso3"]][r["year"]]=r
WGI=["GovEff","RuleLaw","RegQual","CtrlCorr"]
def p1(iso,y):
    r=WBC.get(iso,{}).get(str(y))
    if not r: return None
    v=[r.get(k) for k in WGI]
    return None if any(x in(None,"") for x in v) else float(np.mean([float(x) for x in v]))
def gdp(iso,y):
    r=WBC.get(iso,{}).get(str(y)); v=r.get("GDPpcPPP") if r else None
    return float(v) if v not in(None,"") else None
def near(d,iso,y,tol=3):
    s=d.get(iso) if isinstance(d,dict) else None
    if not s: return None
    s={int(k):v for k,v in s.items()} if all(str(k).isdigit() for k in s) else s
    for dd in range(tol+1):
        for yy in ([y] if dd==0 else [y-dd,y+dd]):
            if yy in s: return s[yy]
    return None

# EPR re-aggregate at base 2008 (via gwid->iso using GW numeric proxy: map by statename)
NAME2ISO=json.load(open(ROOT/"data/political/_epr_name_iso.json")) if (ROOT/"data/political/_epr_name_iso.json").exists() else {}
def epr_excl(base=2008):
    raw=urllib.request.urlopen(urllib.request.Request("https://icr.ethz.ch/data/epr/core/EPR-2021.csv",
        headers={"User-Agent":"Mozilla/5.0"}),timeout=60).read().decode("utf-8","replace")
    rows=list(csv.DictReader(io.StringIO(raw)))
    per=defaultdict(list)
    for r in rows:
        try: fr,to=int(r["from"]),int(r["to"])
        except: continue
        if fr<=base<=to: per[r["statename"]].append(r)
    out={}
    for st,grps in per.items():
        iso=NAME2ISO.get(st)
        if not iso: continue
        exc=sum(float(g["size"]) for g in grps if g["status"] in("POWERLESS","DISCRIMINATED","SELF-EXCLUSION") and g["size"] not in("","NA"))
        out[iso]=exc
    return out

# domestic onsets by iso->years
dom=L.domestic_years()
def onset(iso,y0,y1): return 1 if any(y0<=y<=y1 for y in dom.get(iso,set())) else 0

BASE=2012
EPR=epr_excl(2008)
print("EPR mapped to ISO:",len(EPR))

isos=sorted(set(WBC)|set(lib))   # REPRODUCIBILITY FIX: was set-iteration order (hash-randomized
                                 # across runs) -> the single-seed CV fold split, and thus the gate
                                 # AUCs, were non-deterministic run-to-run. Sort pins row order.
rows=[]
for iso in isos:
    P1b=p1(iso,BASE); Gb=gdp(iso,BASE)
    if P1b is None or Gb is None or Gb<=0: continue
    lb=near({k:v for k,v in lib.items()},iso,BASE)
    if lb is None: continue
    # predictors
    growth=[EXO.get("gdp_pc_growth",{}).get(iso,{}).get(str(y)) for y in range(2000,2013)]
    growth=[x for x in growth if x is not None]
    pr={
     "P1":P1b,"logGDP":math.log10(Gb),
     "ethnic_excl":EPR.get(iso),
     "cso":near(POL.get("cso_participation",{}),iso,BASE),
     "internet":near(POL.get("internet",{}),iso,BASE),
     "pts":near(POL.get("pts",{}),iso,BASE),
     "pts_chg":( (near(POL.get("pts",{}),iso,2012) or 0)-(near(POL.get("pts",{}),iso,2000) or 0) ) if near(POL.get("pts",{}),iso,2000) is not None else None,
     "anocracy":4*lb*(1-lb),
     "prior_conflict":onset(iso,2000,2012),
     "growth_vol":float(np.std(growth)) if len(growth)>=5 else None,
     "youth":near(POL.get("youth_0014",{}),iso,BASE),
     "food_imp":near(POL.get("food_imports",{}),iso,BASE),
    }
    # outcomes 2010/2012 -> 2024
    l24=near({k:v for k,v in lib.items()},iso,2024)
    o={
     "backslide":(1 if (l24-lb)<=-0.05 else 0) if l24 is not None else None,
     "conflict_1224":onset(iso,2013,2024),
     "repression_worsen":( 1 if ((near(POL.get("pts",{}),iso,2024) or 0)-(near(POL.get("pts",{}),iso,2012) or 0))>=1 else 0) if near(POL.get("pts",{}),iso,2024) is not None and pr["pts"] is not None else None,
    }
    rows.append({"iso":iso,"pred":pr,"out":o})

NUM=["ethnic_excl","cso","internet","pts","pts_chg","anocracy","prior_conflict","growth_vol","youth","food_imp"]
OUTS=["backslide","conflict_1224","repression_worsen"]
print("n countries:",len(rows))

# ---- T1 screen ----
def col(key,rows_): return [r for r in rows_]
tests=[]
for P in NUM+["P1","logGDP"]:
    for O in OUTS:
        xy=[(r["pred"][P],r["out"][O],r["pred"]["P1"],r["pred"]["logGDP"]) for r in rows
            if r["pred"].get(P) is not None and r["out"].get(O) is not None]
        if len(xy)<30 or len(set(b for _,b,_,_ in xy))<2: continue
        x=[a for a,_,_,_ in xy]; y=[b for _,b,_,_ in xy]
        sp=stats.spearmanr(x,y)
        # AUDIT M4 FIX: previously rz/rx were computed then DISCARDED, so the reported rho was the
        # uncontrolled bivariate marginal. Compute a real partial-Spearman: rank everything, regress
        # rank-x and rank-y each on [rank-P1, rank-logGDP] (with intercept), correlate the residuals.
        if P not in ("P1","logGDP"):
            rx=stats.rankdata(x); ry=stats.rankdata(y)
            Z=np.column_stack([np.ones(len(xy)),stats.rankdata([c for _,_,c,_ in xy]),stats.rankdata([d for _,_,_,d in xy])])
            bx,_,_,_=np.linalg.lstsq(Z,rx,rcond=None); by,_,_,_=np.linalg.lstsq(Z,ry,rcond=None)
            ex=rx-Z@bx; ey=ry-Z@by
            pr=stats.pearsonr(ex,ey)
            prho=round(float(pr.statistic),3); pp=float(pr.pvalue)
        else:
            prho=None; pp=None   # can't partial a control out of itself
        tests.append({"pred":P,"out":O,"n":len(xy),"rho":round(float(sp.statistic),3),"p":float(sp.pvalue),
                      "partial_rho":prho,"partial_p":pp})
ps=sorted(tests,key=lambda t:t["p"]); m=len(tests); crit=None
for rank,t in enumerate(ps,1):
    if t["p"]<=rank/m*0.05: crit=t["p"]
for t in tests: t["fdr"]=bool(crit and t["p"]<=crit)
# AUDIT M4 FIX: BH-FDR on the PARTIAL p (net of P1+logGDP) — this is the honest survivor set.
pt=[t for t in tests if t.get("partial_p") is not None]
pps=sorted(pt,key=lambda t:t["partial_p"]); mp=len(pps); pcrit=None
for rank,t in enumerate(pps,1):
    if t["partial_p"]<=rank/mp*0.05: pcrit=t["partial_p"]
for t in tests: t["fdr_partial"]=bool(pcrit and t.get("partial_p") is not None and t["partial_p"]<=pcrit)

# ---- T2 gate: 5-fold CV AUC structural vs +numerator ----
def cv_auc(Xcols,y,k=5,seed=0):
    y=np.array(y,float); n=len(y); idx=np.arange(n)
    rng=np.random.default_rng(seed); rng.shuffle(idx)
    folds=np.array_split(idx,k); aucs=[]
    X=np.column_stack([np.ones(n)]+[L.zscore(c) for c in Xcols])
    for f in range(k):
        te=folds[f]; tr=np.setdiff1d(idx,te)
        if len(set(y[tr].tolist()))<2 or len(set(y[te].tolist()))<2: continue
        b,_,_=L.logit_fit(X[tr],y[tr])
        p=1/(1+np.exp(-(X[te]@b)))
        aucs.append(L.auc_roc(p,y[te]))
    return round(float(np.mean(aucs)),4) if aucs else None
def repeated_gate(struct,numer,y,seeds=range(50)):
    """AUDIT M5 FIX: the single-seed 5-fold CV was a fragile point estimate. Repeat over 50 seeds,
    report mean structural/+numerator AUC, the increment distribution (mean + 95% CI), and the
    fraction of seeds with a positive increment. The gate passes only if the CI lower bound > 0."""
    s_a,sn_a,inc=[],[],[]
    for sd in seeds:
        a_s=cv_auc(struct,y,seed=sd); a_sn=cv_auc(struct+numer,y,seed=sd)
        if a_s is None or a_sn is None: continue
        s_a.append(a_s); sn_a.append(a_sn); inc.append(a_sn-a_s)
    if not inc: return None
    lo,hi=np.percentile(inc,[2.5,97.5])
    return {"auc_structural":round(float(np.mean(s_a)),4),"auc_struct+numerator":round(float(np.mean(sn_a)),4),
            "increment_mean":round(float(np.mean(inc)),4),"increment_CI":[round(float(lo),4),round(float(hi),4)],
            "frac_seeds_positive":round(float(np.mean([x>0 for x in inc])),3),
            "gate_pass(CI>0)":bool(lo>0)}

gate={}
for O in OUTS:
    sub=[r for r in rows if r["out"].get(O) is not None and all(r["pred"].get(p) is not None for p in ["P1","logGDP"]+NUM)]
    if len(sub)<40: gate[O]={"n":len(sub),"note":"too few complete"}; continue
    y=[r["out"][O] for r in sub]
    struct=[[r["pred"]["P1"] for r in sub],[r["pred"]["logGDP"] for r in sub]]
    numer=[[r["pred"][p] for r in sub] for p in NUM]
    numer_noeh=[[r["pred"][p] for r in sub] for p in NUM if p!="prior_conflict"]
    g=repeated_gate(struct,numer,y)
    g["n"]=len(sub); g["n_pos"]=int(sum(y))
    g["auc_struct+num_no_eventhistory"]=cv_auc(struct+numer_noeh,y)
    gate[O]=g

out={"prereg":"ec4aebe0","n":len(rows),"T1_fdr_crit":crit,"T1_fdr_partial_crit":pcrit,
     "T1_survivors":sorted([t for t in tests if t["fdr"]],key=lambda t:t["p"]),
     "T1_survivors_partial":sorted([t for t in tests if t["fdr_partial"]],key=lambda t:t["partial_p"]),
     "T1_all":sorted(tests,key=lambda t:t["p"]),"T2_gate":gate}
(ROOT/"data/political/political_test.json").write_text(json.dumps(out,indent=1))
print(f"\n=== T1 screen: {m} tests, BIVARIATE FDR survivors (crit p<={crit}) ===")
for t in out["T1_survivors"]:
    pr=f"{t['partial_rho']:+.3f}" if t.get('partial_rho') is not None else "  n/a"
    print(f"   {t['pred']:15s} -> {t['out']:18s} rho={t['rho']:+.3f} p={t['p']:.4f} | partial(net P1+GDP) rho={pr} {'[survives]' if t['fdr_partial'] else '[GONE net of controls]'}")
if not out["T1_survivors"]: print("   (none survive FDR)")
print(f"\n=== T1 PARTIAL survivors (net of P1+logGDP, the honest set, crit p<={pcrit}) ===")
for t in out["T1_survivors_partial"]:
    print(f"   {t['pred']:15s} -> {t['out']:18s} partial_rho={t['partial_rho']:+.3f} partial_p={t['partial_p']:.4f} n={t['n']}")
if not out["T1_survivors_partial"]: print("   (none survive the partial FDR — T1 marginals were all confounded by capacity/wealth)")
print(f"\n=== T2 GATE: numerator over structural (P1+logGDP), 50-seed repeated 5-fold CV ===")
for O,g in gate.items():
    if "note" in g: print(f"   {O}: {g}"); continue
    print(f"   {O:18s} n={g['n']} pos={g['n_pos']}: structural={g['auc_structural']}  +numerator={g['auc_struct+numerator']}  "
          f"increment={g['increment_mean']:+.4f} CI{g['increment_CI']} pos-frac={g['frac_seeds_positive']}  PASS(CI>0)={g['gate_pass(CI>0)']}")
