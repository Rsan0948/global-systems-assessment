#!/usr/bin/env python3
"""Robustness of the relational-beats-additive backsliding result: REL model across leads
k in {3,5,10} with bootstrap 95% CI on sealed TEST, and the single capacity-turbulence gap."""
import numpy as np
from scipy import stats
import relational_screen as R

def boot(pr,y,B=2000):
    a=R.auc(pr,y); n=len(y); rng=np.random.default_rng(0); out=[]
    for _ in range(B):
        s=rng.integers(0,n,n); aa=R.auc(pr[s],y[s])
        if aa is not None: out.append(aa)
    return a,np.percentile(out,2.5),np.percentile(out,97.5)

def rel_pred(name,raw,ctrl,k,use):
    rows=R.normalize(R.assemble(name,raw,ctrl,"bin",k))
    X,C,Y,G=R.build_matrix(rows,R.RELNAMES,use)
    mtr=G!="TEST"; mte=G=="TEST"
    if mtr.sum()<40 or mte.sum()<25 or Y[mte].sum()<6: return None
    F=np.column_stack([C,X]); mu=F[mtr].mean(0); sd=F[mtr].std(0); sd[sd==0]=1
    b=R.S.logit_fit((F[mtr]-mu)/sd,Y[mtr]); pr=R.S.logit_pred((F[mte]-mu)/sd,b)
    return pr,Y[mte]

print("Relational backsliding model — lead replication + bootstrap CI (sealed TEST)\n")
print(f"{'outcome':>20} {'k':>2} | {'ADD-6':>6} {'REL':>6} | {'REL 95% CI':>20} {'cap-turb gap':>12} n_test pos")
print("-"*92)
for name,raw,ctrl in [("libdem_backslide","libdem","libdem"),("electdem_backslide","electdem","electdem")]:
    for k in [3,5,10]:
        add=rel_pred(name,raw,ctrl,k,"add"); rel=rel_pred(name,raw,ctrl,k,"rel")
        cg=rel_pred(name,raw,ctrl,k,"gap_v1_mi_t5_turb_libdem")
        if not rel: print(f"{name:>20} {k:>2} | insufficient"); continue
        a_add=R.auc(*add) if add else float("nan")
        a,lo,hi=boot(*rel)
        acg=R.auc(*cg) if cg else float("nan")
        print(f"{name:>20} {k:>2} | {a_add:>6.3f} {a:>6.3f} | [{lo:>.3f}, {hi:>.3f}]      {acg:>12.3f}  {len(rel[1])}   {int(rel[1].sum())}")
