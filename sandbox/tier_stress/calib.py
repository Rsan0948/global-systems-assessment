#!/usr/bin/env python3
"""B — firm up the backsliding-ensemble AUC: bootstrap CI on sealed TEST, calibration curve,
lambda sensitivity, and a frozen-parsimonious set vs the full regularized model.
Three-way FIT/SEL/TEST split from combo_search (TEST is sealed)."""
import json, numpy as np
from pathlib import Path
from scipy import stats
import combo_search as CS
import stack_screen as S
HERE=Path(__file__).resolve().parent
POOL=CS.POOL

# consensus frozen set from the combinatorial inclusion-frequency (both backsliding outcomes)
FROZEN=['anocracy','P1','durgap','internet','growth_vol','t4_reversed_trust','t5_turb_libdem','t6_s4_military']

def cols(names): return [POOL.index(n) for n in names]

def auc(score,y):
    pos=score[y==1]; neg=score[y==0]
    if len(pos)==0 or len(neg)==0: return None
    return float(stats.mannwhitneyu(pos,neg,alternative="two-sided").statistic/(len(pos)*len(neg)))

def fit_predict(name,raw,ctrl,kind,k,idx,lam):
    P,C,Y,G=CS.master(name,raw,ctrl,kind,k)
    sub=P[:,idx]; ok=~np.isnan(sub).any(1)
    mtr=ok&(G!="TEST"); mte=ok&(G=="TEST")
    Xtr=np.column_stack([C[mtr],sub[mtr]]); Xte=np.column_stack([C[mte],sub[mte]])
    mu=Xtr.mean(0); sd=Xtr.std(0); sd[sd==0]=1
    Xtr=(Xtr-mu)/sd; Xte=(Xte-mu)/sd
    b=S.logit_fit(Xtr,Y[mtr],lam=lam)
    pr=S.logit_pred(Xte,b)
    return pr, Y[mte].astype(int), int(mtr.sum())

def boot_auc(pr,y,B=2000):
    a=auc(pr,y); n=len(y); idx=np.arange(n)
    seeds=np.random.default_rng(0)
    boots=[]
    for _ in range(B):
        s=seeds.integers(0,n,n)
        aa=auc(pr[s],y[s])
        if aa is not None: boots.append(aa)
    lo,hi=np.percentile(boots,[2.5,97.5])
    return a,lo,hi

def calib(pr,y,q=5):
    order=np.argsort(pr); pr=pr[order]; y=y[order]
    bins=np.array_split(np.arange(len(y)),q)
    rows=[]
    for bi in bins:
        rows.append((float(pr[bi].mean()), float(y[bi].mean()), len(bi)))
    return rows

def lambda_scan(name,raw,ctrl,kind,k,idx):
    out={}
    for lam in [0.3,1.0,3.0,10.0]:
        pr,y,ntr=fit_predict(name,raw,ctrl,kind,k,idx,lam)
        out[lam]=round(auc(pr,y),3)
    return out

for name,raw,ctrl in [("libdem_backslide","libdem","libdem"),("electdem_backslide","electdem","electdem")]:
    print(f"\n{'='*70}\n{name} (k=5)")
    for label,names in [("FROZEN-8",FROZEN),("FULL-27",POOL)]:
        idx=cols(names) if label=="FROZEN-8" else list(range(len(POOL)))
        pr,y,ntr=fit_predict(name,raw,ctrl,"bin",5,idx,1.0)
        a,lo,hi=boot_auc(pr,y)
        print(f"  [{label}] n_train={ntr} n_test={len(y)} pos_test={int(y.sum())}")
        print(f"     TEST AUC={a:.3f}  95% bootstrap CI [{lo:.3f}, {hi:.3f}]")
        if label=="FROZEN-8":
            print(f"     lambda sensitivity (AUC): {lambda_scan(name,raw,ctrl,'bin',5,idx)}")
            print(f"     calibration (mean predicted -> observed rate, n):")
            for mp,ob,nn in calib(pr,y,5):
                bar="#"*int(ob*20)
                print(f"        p~{mp:.2f} -> obs {ob:.2f} (n={nn}) {bar}")
