#!/usr/bin/env python3
"""Robustness battery for the out-of-time backsliding confirmation. Characterizes WHY the
relational model fails OOT: rolling-origin splits, regularization sweep, placebo, threshold
sensitivity, and determinism. Everything scored on genuinely future test cohorts."""
import json, numpy as np
from pathlib import Path
import confirm_oot as O
import relational_screen as R
HERE=Path(__file__).resolve().parent
OUT=[("libdem_backslide","libdem","libdem"),("electdem_backslide","electdem","electdem")]
REL=("rel",R.RELNAMES); CT=("single","gap_v1_mi_t5_turb_libdem")

def one(name,raw,ctrl,kind_of,names,train,test,lam=1.0,shuffle=None,thr=0.05):
    # threshold override handled by monkeypatching target via a custom assemble
    rows=O.normalize_temporal(O.assemble_temporal(name,raw,ctrl,"bin",5,train,test))
    if thr!=0.05:
        rows=_rethreshold(rows,name,raw,test+train,thr)
    return O.fit_eval_oot(name,raw,ctrl,5,kind_of,names,rows=rows,lam=lam,shuffle_seed=shuffle)

def _rethreshold(rows,name,raw,bases,thr):
    # recompute y with a different backslide threshold
    for r in rows:
        a=R.S.ov(r["iso"],r["b"],raw); c=R.S.ov(r["iso"],r["b"]+5,raw)
        r["y"]=float(1 if (a is not None and c is not None and (c-a)<=-thr) else 0)
    return rows

print("="*80)
print("1) ROLLING-ORIGIN temporal splits (relational λ=1 vs AR+GDP base; Δ = model−base)")
print("="*80)
SPLITS=[([1996,2000,2004],[2008,2012]),([1996,2000,2004,2008],[2012]),
        ([1996,2000,2004,2008,2012],[2016,2018])]
print(f"{'outcome':>20} {'train->test':>26} | {'REL':>6} {'base':>6} {'Δ':>7} {'nTe':>4} {'posTe':>5}")
for name,raw,ctrl in OUT:
    for tr,te in SPLITS:
        r=one(name,raw,ctrl,*REL,tr,te)
        if not r: print(f"{name:>20} {str(min(tr))+'-'+str(max(tr))+' -> '+str(te):>26} | insufficient"); continue
        print(f"{name:>20} {str(min(tr))+'-'+str(max(tr))+' -> '+str(te):>26} | {r['auc']:>6.3f} {r['base_auc']:>6.3f} {r['delta']:>+7.3f} {r['n_test']:>4} {r['pos_test']:>5}")

print("\n"+"="*80)
print("2) REGULARIZATION sweep on the 2016/2018 OOT split — does more λ rescue it?")
print("="*80)
print(f"{'outcome':>20} | " + " ".join(f"λ={l:>4}" for l in [1,3,10,30,100]) + "   (Δ vs base)")
for name,raw,ctrl in OUT:
    row=[]
    for lam in [1,3,10,30,100]:
        r=one(name,raw,ctrl,*REL,[1996,2000,2004,2008,2012],[2016,2018],lam=lam)
        row.append(f"{r['delta']:+.3f}" if r else "  -  ")
    print(f"{name:>20} | " + " ".join(f"{v:>7}" for v in row))

print("\n"+"="*80)
print("3) PLACEBO — permute TEST labels (10 seeds); relational AUC should collapse to ~0.5")
print("="*80)
for name,raw,ctrl in OUT:
    aucs=[]
    for s in range(10):
        r=one(name,raw,ctrl,*REL,[1996,2000,2004,2008,2012],[2016,2018],shuffle=s)
        if r: aucs.append(r["auc"])
    print(f"   {name:>20}: placebo AUC mean={np.mean(aucs):.3f} range[{min(aucs):.3f},{max(aucs):.3f}]  (want ~0.5)")

print("\n"+"="*80)
print("4) THRESHOLD sensitivity on OOT split (backslide cut 0.03/0.05/0.07)")
print("="*80)
print(f"{'outcome':>20} | " + " ".join(f"thr={t}" for t in [0.03,0.05,0.07]) + "   (REL / base)")
for name,raw,ctrl in OUT:
    cells=[]
    for thr in [0.03,0.05,0.07]:
        r=one(name,raw,ctrl,*REL,[1996,2000,2004,2008,2012],[2016,2018],thr=thr)
        cells.append(f"{r['auc']:.2f}/{r['base_auc']:.2f}" if r else " - ")
    print(f"{name:>20} | " + " ".join(f"{c:>11}" for c in cells))

print("\n"+"="*80)
print("5) DETERMINISM — re-run the headline OOT eval twice, compare")
print("="*80)
a=one("libdem_backslide","libdem","libdem",*REL,[1996,2000,2004,2008,2012],[2016,2018])
b=one("libdem_backslide","libdem","libdem",*REL,[1996,2000,2004,2008,2012],[2016,2018])
print(f"   run1 AUC={a['auc']} run2 AUC={b['auc']}  -> {'DETERMINISTIC' if a['auc']==b['auc'] else 'NONDETERMINISTIC!'}")
