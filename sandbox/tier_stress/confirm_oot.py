#!/usr/bin/env python3
"""Out-of-time CONFIRMATION (prereg §4). The discovery used a country hash-split; this is the
real test — a TEMPORAL holdout the model never optimized against.
  TRAIN base years {1996,2000,2004,2008,2012}  ->  TEST base years {2016,2018} (outcomes 2021/2023).
Fit the frozen RELATIONAL model (primary) + additive-8 (secondary) + the single capacity-turbulence
gap, on TRAIN only; score once on TEST. Normalization uses only within-year predictor cross-sections
(no outcome leakage). AUC + bootstrap 95% CI + AR+GDP baseline + prereg pass/fail.

Public API (imported by tests / robustness): assemble_temporal, normalize_temporal,
matrix, fit_eval_oot.
"""
import json, math
from pathlib import Path
import numpy as np
from scipy import stats
import relational_screen as R
import combo_search as CS
import stack_screen as S

HERE=Path(__file__).resolve().parent
PRED=CS.PRED
TRAIN_BASES=[1996,2000,2004,2008,2012]
TEST_BASES=[2016,2018]
FEATSETS={
 "relational": ("rel", R.RELNAMES),
 "additive8":  ("add8", ['anocracy','P1','durgap','internet','growth_vol','t4_reversed_trust','t5_turb_libdem','t6_s4_military']),
 "cap_minus_turb": ("single","gap_v1_mi_t5_turb_libdem"),
}

def assemble_temporal(name,raw,ctrl,kind,k,train_bases=TRAIN_BASES,test_bases=TEST_BASES):
    rows=[]
    for phase,bases in [("train",train_bases),("test",test_bases)]:
        for b in bases:
            if b+k>2025: continue
            for iso in sorted(PRED):
                y=CS.target_val(iso,b,k,name,raw,kind)
                cc=S.pv(iso,b,ctrl) if ctrl in CS.POOL else S.ov(iso,b,ctrl)
                g=S.lgdp(iso,b)
                if y is None or cc is None or g is None: continue
                vals={f:S.pv(iso,b,f) for f in set(R.INSTR+R.PILLARS)}
                rows.append({"iso":iso,"b":b,"phase":phase,"y":float(y),"ctrl":float(cc),"lgdp":float(g),"v":vals})
    return rows

def normalize_temporal(rows):
    """within each base-year cross-section, z + percentile each instrument using that year's
    countries (predictors only -> no outcome leakage; this is MI's world-relative scoring)."""
    byb={}
    for r in rows: byb.setdefault(r["b"],[]).append(r)
    for b,rs in byb.items():
        for f in set(R.INSTR+R.PILLARS):
            ref=[r["v"][f] for r in rs if r["v"][f] is not None]
            if len(ref)<8:
                for r in rs: r.setdefault("z",{})[f]=None; r.setdefault("p",{})[f]=None
                continue
            mu=float(np.mean(ref)); sd=float(np.std(ref)) or 1.0; srt=np.sort(ref)
            for r in rs:
                x=r["v"][f]
                r.setdefault("z",{})[f]= None if x is None else (x-mu)/sd
                r.setdefault("p",{})[f]= None if x is None else float(np.searchsorted(srt,x)/len(srt))
    return rows

def matrix(rows,kind_of,names,phase):
    X=[];C=[];Y=[]
    for r in rows:
        if r["phase"]!=phase: continue
        if kind_of=="add8":
            vec=[r["z"].get(n) for n in names]
        elif kind_of=="single":
            fe=R.feat(r); vec=[fe.get(names)]
        else:  # rel
            fe=R.feat(r); vec=[fe.get(n) for n in names]
        if any(v is None for v in vec): continue
        X.append(vec); C.append([r["ctrl"],r["lgdp"]]); Y.append(r["y"])
    return np.array(X,float),np.array(C,float),np.array(Y,float)

def auc(sc,y):
    pos=sc[y==1]; neg=sc[y==0]
    return None if len(pos)==0 or len(neg)==0 else float(stats.mannwhitneyu(pos,neg,alternative="two-sided").statistic/(len(pos)*len(neg)))

def boot(sc,y,B=3000,seed=0):
    a=auc(sc,y); n=len(y); rng=np.random.default_rng(seed); out=[]
    for _ in range(B):
        s=rng.integers(0,n,n); aa=auc(sc[s],y[s])
        if aa is not None: out.append(aa)
    return a,float(np.percentile(out,2.5)),float(np.percentile(out,97.5))

def fit_eval_oot(name,raw,ctrl,k,kind_of,names,rows=None,lam=1.0,shuffle_seed=None):
    if rows is None: rows=normalize_temporal(assemble_temporal(name,raw,ctrl,"bin",k))
    Xtr,Ctr,ytr=matrix(rows,kind_of,names,"train")
    Xte,Cte,yte=matrix(rows,kind_of,names,"test")
    if len(ytr)<50 or len(yte)<20 or ytr.sum()<8 or yte.sum()<5: return None
    if shuffle_seed is not None:  # placebo: permute TEST labels -> expect AUC ~0.5
        yte=np.random.default_rng(shuffle_seed).permutation(yte)
    Ftr=np.column_stack([Ctr,Xtr]); Fte=np.column_stack([Cte,Xte])
    mu=Ftr.mean(0); sd=Ftr.std(0); sd[sd==0]=1
    b=S.logit_fit((Ftr-mu)/sd,ytr,lam=lam); sc=S.logit_pred((Fte-mu)/sd,b)
    a,lo,hi=boot(sc,yte)
    # AR+GDP baseline (controls only)
    mub=Ctr.mean(0); sdb=Ctr.std(0); sdb[sdb==0]=1
    bb=S.logit_fit((Ctr-mub)/sdb,ytr)
    base=auc(S.logit_pred((Cte-mub)/sdb,bb),yte)
    return {"auc":round(a,3),"ci":[round(lo,3),round(hi,3)],"base_auc":round(base,3),
            "delta":round(a-base,3),"n_train":len(ytr),"n_test":len(yte),
            "pos_train":int(ytr.sum()),"pos_test":int(yte.sum()),
            "pass":bool(lo>0.5 and (a-base)>=0.05)}

def run():
    OUT=[("libdem_backslide","libdem","libdem"),("electdem_backslide","electdem","electdem")]
    report={}
    print("OUT-OF-TIME CONFIRMATION  (train base ≤2012  ->  test base 2016/2018, k=5)\n")
    print(f"{'outcome':>20} {'model':>16} | {'AUC':>6} {'95% CI':>16} {'base':>6} {'Δ':>6} {'nTe':>4} {'posTe':>5}  PASS")
    print("-"*104)
    for name,raw,ctrl in OUT:
        rows=normalize_temporal(assemble_temporal(name,raw,ctrl,"bin",5))
        report[name]={}
        for mlabel,(kind_of,names) in FEATSETS.items():
            r=fit_eval_oot(name,raw,ctrl,5,kind_of,names,rows=rows)
            report[name][mlabel]=r
            if not r: print(f"{name:>20} {mlabel:>16} | insufficient"); continue
            print(f"{name:>20} {mlabel:>16} | {r['auc']:>6.3f} [{r['ci'][0]:.3f},{r['ci'][1]:.3f}] {r['base_auc']:>6.3f} {r['delta']:>+6.3f} {r['n_test']:>4} {r['pos_test']:>5}  {'PASS' if r['pass'] else 'no'}")
    json.dump(report,open(HERE/"confirm_oot_results.json","w"),indent=1)
    return report

if __name__=="__main__":
    run()
