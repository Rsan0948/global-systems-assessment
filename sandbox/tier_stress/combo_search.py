#!/usr/bin/env python3
"""Exhaustive combinatorial mix-and-match with internals broken out.
Pool = ~27 predictors (tier composites + every sub-component, deduped).
Enumerate ALL subsets of size 1..4. THREE-WAY country split (no leakage):
  FIT  (fit coefficients)  |  SEL (select the winning subset)  |  TEST (sealed, reported once).
Search ranks subsets on SEL only; final models refit on FIT+SEL and scored ONCE on TEST.
Fast search via a linear-probability model (ridge) + AUC; winners re-scored with logistic.
"""
import json, math, hashlib, itertools, sys
from pathlib import Path
import numpy as np
from scipy import stats
sys.path.insert(0,str(Path(__file__).resolve().parent))
import stack_screen as S   # reuse logit_fit, ridge_fit, pv, ov, lgdp, ONSETS

HERE=Path(__file__).resolve().parent
PRED=S.PRED; OUTC=S.OUTC; BASES=S.BASES

# ---- predictor pool: composites + internals, deduped (t4_pts==pts, t4_decayed_conflict==prior_conflict_decayed) ----
POOL=['v1_mi','P1','P2','P3','P4','P5','durgap',                              # V1 internals
      'v3_numer','anocracy','cso','pts','youth','food_imp','internet','growth_vol','prior_conflict_decayed',  # V3
      't4_scar','t4_refugee_share','t4_reversed_trust',                       # T4 (drop dup t4_pts,t4_decayed_conflict)
      't5_turb_libdem','t5_turb_electdem',                                    # T5
      't6_spark','t6_s1_geo','t6_s2_resource','t6_s3_transcendent','t6_s4_military',  # T6 internals
      'dgs']                                                                  # frag leg
NP=len(POOL)

def grp(iso):
    h=int(hashlib.sha256(iso.encode()).hexdigest(),16)%3
    return ['FIT','SEL','TEST'][h]

def target_val(iso,b,k,name,raw,kind):
    return S.target_val(iso,b,k,name,raw,kind)

def master(name,raw,ctrl,kind,k):
    """build full arrays over all (iso,cohort): P (n x NP, nan-filled), C (n x2), y, group."""
    P=[];C=[];Y=[];G=[]
    for b in BASES:
        if b+k>2025: continue
        for iso in sorted(PRED):
            y=target_val(iso,b,k,name,raw,kind)
            cc=S.pv(iso,b,ctrl) if ctrl in POOL else S.ov(iso,b,ctrl)   # control is a predictor iff in pool, else an outcome field
            g=S.lgdp(iso,b)
            if y is None or cc is None or g is None: continue
            row=[]
            for f in POOL:
                v=S.pv(iso,b,f); row.append(float(v) if v is not None else np.nan)
            P.append(row); C.append([float(cc),float(g)]); Y.append(float(y)); G.append(grp(iso))
    return np.array(P),np.array(C),np.array(Y,float),np.array(G)

def auc(score,y):
    pos=score[y==1]; neg=score[y==0]
    if len(pos)==0 or len(neg)==0: return None
    return float(stats.mannwhitneyu(pos,neg,alternative="two-sided").statistic/(len(pos)*len(neg)))
def sp(score,y): return float(stats.spearmanr(score,y).statistic)

def lpm_fit(X,y,lam=1.0):
    n,p=X.shape; Xi=np.column_stack([np.ones(n),X]); I=np.eye(p+1); I[0,0]=0
    return np.linalg.solve(Xi.T@Xi+lam*I, Xi.T@y)
def lpm_pred(X,b): return np.column_stack([np.ones(len(X)),X])@b

def zfit(M): mu=np.nanmean(M,0); sd=np.nanstd(M,0); sd[sd==0]=1; return mu,sd

def eval_subset(idx, P,C,Y,G, kind, need_fit=40, need_sel=25):
    """fit LPM on FIT rows (subset+controls present), score on SEL. returns (score, n_fit, n_sel)."""
    cols=list(idx)
    sub=P[:,cols]
    ok=~np.isnan(sub).any(1)
    def rows(gname):
        m=ok & (G==gname)
        return m
    mf=rows("FIT"); ms=rows("SEL")
    if mf.sum()<need_fit or ms.sum()<need_sel: return None
    if kind=="bin" and (Y[mf].sum()<8 or Y[ms].sum()<6 or len(set(Y[ms]))<2): return None
    Xf=np.column_stack([C[mf],sub[mf]]); Xs=np.column_stack([C[ms],sub[ms]])
    mu,sdv=zfit(Xf); Xf=(Xf-mu)/sdv; Xs=(Xs-mu)/sdv
    b=lpm_fit(Xf,Y[mf]); pr=lpm_pred(Xs,b)
    s=auc(pr,Y[ms]) if kind=="bin" else abs(sp(pr,Y[ms]))
    return (s, int(mf.sum()), int(ms.sum()))

def final_on_test(cols, P,C,Y,G, kind):
    """refit on FIT+SEL, score ONCE on sealed TEST. logistic for bin."""
    sub=P[:,cols]; ok=~np.isnan(sub).any(1)
    mtr=ok & (G!="TEST"); mte=ok & (G=="TEST")
    if mtr.sum()<40 or mte.sum()<25: return None
    if kind=="bin" and (Y[mtr].sum()<8 or Y[mte].sum()<6 or len(set(Y[mte]))<2): return None
    Xtr=np.column_stack([C[mtr],sub[mtr]]); Xte=np.column_stack([C[mte],sub[mte]])
    mu,sdv=zfit(Xtr); Xtr=(Xtr-mu)/sdv; Xte=(Xte-mu)/sdv
    if kind=="bin":
        b=S.logit_fit(Xtr,Y[mtr]); prtr=S.logit_pred(Xtr,b); pr=S.logit_pred(Xte,b)
        s=auc(pr,Y[mte])
    else:
        b=lpm_fit(Xtr,Y[mtr]); pr=lpm_pred(Xte,b); s=sp(pr,Y[mte])
        prtr=lpm_pred(Xtr,b)
    # baseline (controls only) on TEST
    Ctr=C[mtr]; Cte=C[mte]; muc,sdc=zfit(Ctr); Ctr=(Ctr-muc)/sdc; Cte=(Cte-muc)/sdc
    if kind=="bin":
        bb=S.logit_fit(Ctr,Y[mtr]); sb=auc(S.logit_pred(Cte,bb),Y[mte])
    else:
        bb=lpm_fit(Ctr,Y[mtr]); sb=sp(lpm_pred(Cte,bb),Y[mte])
    return {"skill_test":round(s,3),"base_test":round(sb,3),"delta":round(s-sb,3),
            "n_train":int(mtr.sum()),"n_test":int(mte.sum()),
            "pos_test":int(Y[mte].sum()) if kind=="bin" else None,
            "pred_test":pr.tolist(),"y_test":Y[mte].astype(int).tolist() if kind=="bin" else None}

def search(name,raw,ctrl,kind,k,maxsize=4):
    P,C,Y,G=master(name,raw,ctrl,kind,k)
    results=[]   # (score, n_fit, n_sel, idx_tuple)
    for size in range(1,maxsize+1):
        for idx in itertools.combinations(range(NP),size):
            r=eval_subset(idx,P,C,Y,G,kind)
            if r: results.append((r[0],r[1],r[2],idx))
    results.sort(key=lambda t:-t[0])
    # best per size
    best_size={}
    for score,nf,ns,idx in results:
        z=len(idx)
        if z not in best_size: best_size[z]=(score,idx,nf,ns)
    # inclusion frequency in top 1% (size>=2)
    multi=[r for r in results if len(r[3])>=2]
    top=multi[:max(20,len(multi)//100)]
    freq={f:0 for f in POOL}
    for _,_,_,idx in top:
        for i in idx: freq[POOL[i]]+=1
    incl=sorted(freq.items(),key=lambda kv:-kv[1])
    # sealed-TEST eval of best-overall and best-per-size
    def names(idx): return [POOL[i] for i in idx]
    best_overall=results[0]
    test_overall=final_on_test(list(best_overall[3]),P,C,Y,G,kind)
    per_size_test={}
    for z,(score,idx,nf,ns) in sorted(best_size.items()):
        t=final_on_test(list(idx),P,C,Y,G,kind)
        per_size_test[z]={"sel_skill":round(score,3),"preds":names(idx),"test":t}
    # full model (all pool) on TEST — regularized reference ceiling
    full_test=final_on_test(list(range(NP)),P,C,Y,G,kind)
    return {"outcome":name,"k":k,"kind":kind,"n_subsets":len(results),
            "best_overall":{"sel_skill":round(best_overall[0],3),"preds":names(best_overall[3]),"test":test_overall},
            "per_size":per_size_test,"full_model":full_test,
            "inclusion_top":incl[:12], "master_n":len(Y),
            "grp_counts":{g:int((G==g).sum()) for g in ["FIT","SEL","TEST"]}}

if __name__=="__main__":
    TARGETS=[("libdem_backslide","libdem","libdem","bin"),
             ("electdem_backslide","electdem","electdem","bin"),
             ("conflict_onset_fwd","__onset__","prior_conflict_decayed","bin"),
             ("gdp_pc_growth_fwd","gdp_pc_growth","gdp_pc_growth","cont")]
    K=5
    out={}
    for name,raw,ctrl,kind in TARGETS:
        print(f"\n{'='*80}\n{name}  (k={K}, kind={kind})")
        r=search(name,raw,ctrl,kind,K)
        out[name]=r
        gc=r["grp_counts"]
        print(f"  master rows={r['master_n']}  groups FIT/SEL/TEST={gc['FIT']}/{gc['SEL']}/{gc['TEST']}  subsets scored={r['n_subsets']}")
        bo=r["best_overall"]; t=bo["test"]
        print(f"  BEST-OVERALL (SEL-selected): {bo['preds']}")
        if t: print(f"     -> sealed TEST skill={t['skill_test']} vs base={t['base_test']} (Δ{t['delta']:+}) n_test={t['n_test']} pos={t['pos_test']}")
        print(f"  best per size (sealed TEST skill / Δ over base):")
        for z,ps in r["per_size"].items():
            tt=ps["test"]
            if tt: print(f"     size {z}: TEST={tt['skill_test']} (Δ{tt['delta']:+})  {ps['preds']}")
            else:  print(f"     size {z}: (insufficient TEST n)  {ps['preds']}")
        fm=r["full_model"]
        if fm: print(f"  FULL regularized model (all {NP}): TEST={fm['skill_test']} (Δ{fm['delta']:+}) n_test={fm['n_test']}")
        print(f"  most-included predictors in top subsets: {[f'{n}:{c}' for n,c in r['inclusion_top']]}")
    json.dump(out,open(HERE/"combo_results.json","w"),indent=1)
    print(f"\nsaved combo_results.json")
