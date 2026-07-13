#!/usr/bin/env python3
"""Stacking / mix-and-match screen. Fit multi-instrument models on DISCOVERY countries,
score ONLY on the SEALED confirmation half, always as INCREMENTAL skill over an AR+GDP
baseline. No in-sample numbers are ever reported (the audit's C1 trap). Configs:
  base            : AR(lagged outcome) + logGDP           <- the bar to beat
  single          : base + each instrument alone (best)
  all6            : base + all 6 instrument composites
  greedy          : base + forward-selected set (selected by A-internal CV, eval on B)
  +interaction    : does any pairwise product add held-out skill beyond mains? (add vs multiply)
Skill = held-out rank skill on B: Spearman(pred,y) for continuous, AUC for binary."""
import json, math, sys, hashlib
from pathlib import Path
import numpy as np
from scipy import stats
sys.path.insert(0,str(Path("/Users/rubensanchez/Developer/usg-sandbox-wt/mi-research")))
sys.path.insert(0,str(Path("/Users/rubensanchez/Developer/usg-sandbox-wt/mi-research/scripts/robustness")))
HERE=Path(__file__).resolve().parent
MIROOT=Path("/Users/rubensanchez/Developer/usg-sandbox-wt/mi-research")
PRED=json.load(open(HERE/"predictors.json"))
OUTC=json.load(open(HERE/"outcomes.json"))
GDPPC=json.load(open(MIROOT/"data/v2/v2_indicators.json"))["series"].get("gdp_pc_ppp",{})
BASES=[1996,2000,2004,2008,2012,2016]

def half(iso):
    return "A" if int(hashlib.sha256(iso.encode()).hexdigest(),16)%2==0 else "B"
def pv(iso,b,f):
    r=(PRED.get(iso,{}) or {}).get(str(b),(PRED.get(iso,{}) or {}).get(b)); return r.get(f) if isinstance(r,dict) else None
def ov(iso,y,f):
    r=OUTC.get(iso,{}); r=r.get(str(y),r.get(y)) if isinstance(r,dict) else None; return r.get(f) if isinstance(r,dict) else None
def lgdp(iso,b):
    v=GDPPC.get(iso,{}).get(str(b))
    try: return math.log10(float(v)) if v and float(v)>0 else None
    except: return None

# instrument composites (mix-and-match pool) and the canonical 6 for interactions
SIX=['v1_mi','v3_numer','t4_scar','t5_turb_libdem','t6_spark','dgs']
POOL=SIX+['P3','P5','durgap','youth','pts','t6_s4_military','anocracy','prior_conflict_decayed','internet','cso']

# outcomes: (name, raw_field_for_target, base_control_field, kind)
TARGETS=[
 ("life_satisfaction_fwd","life_satisfaction","life_satisfaction","cont"),
 ("gdp_pc_growth_fwd","gdp_pc_growth","gdp_pc_growth","cont"),
 ("net_migration_fwd","net_migration","net_migration","cont"),
 ("brain_health_ratio_fwd","brain_health_ratio","brain_health_ratio","cont"),
 ("libdem_backslide","libdem","libdem","bin"),        # AR control = current libdem level
 ("electdem_backslide","electdem","electdem","bin"),
 ("conflict_onset_fwd","__onset__","prior_conflict_decayed","bin"),
]
ONSETS={k:set(v) for k,v in OUTC.get("conflict_onsets_by_iso",{}).items()}

def target_val(iso,b,k,name,raw,kind):
    if name=="conflict_onset_fwd":
        s=ONSETS.get(iso); return None if s is None else (1 if any(b<y<=b+k for y in s) else 0)
    if name.endswith("_backslide"):
        a=ov(iso,b,raw); c=ov(iso,b+k,raw); return None if a is None or c is None else (1 if (c-a)<=-0.05 else 0)
    return ov(iso,b+k,raw)

def build(name,raw,ctrl,kind,k,preds,iso_filter):
    """rows: X (preds), C (ctrl,logGDP), y ; for isos in filter, all cohorts."""
    X=[];C=[];Y=[]
    for b in BASES:
        if b+k>2025: continue
        for iso in sorted(PRED):
            if iso_filter(iso) is False: continue
            xs=[pv(iso,b,p) for p in preds]
            cc=pv(iso,b,ctrl) if ctrl in POOL else ov(iso,b,ctrl)
            g=lgdp(iso,b)
            y=target_val(iso,b,k,name,raw,kind)
            if y is None or cc is None or g is None or any(v is None for v in xs): continue
            X.append([float(v) for v in xs]); C.append([float(cc),float(g)]); Y.append(float(y))
    return np.array(X),np.array(C),np.array(Y)

def zfit(M):
    mu=M.mean(0); sd=M.std(0); sd[sd==0]=1; return mu,sd
def zap(M,mu,sd): return (M-mu)/sd

def ridge_fit(X,y,lam=1.0):
    n,p=X.shape; Xi=np.column_stack([np.ones(n),X])
    P=np.eye(p+1); P[0,0]=0
    beta=np.linalg.solve(Xi.T@Xi+lam*P, Xi.T@y); return beta
def ridge_pred(X,beta): return np.column_stack([np.ones(len(X)),X])@beta

def logit_fit(X,y,lam=1.0,iters=100):
    n,p=X.shape; Xi=np.column_stack([np.ones(n),X]); beta=np.zeros(p+1)
    P=np.eye(p+1)*lam; P[0,0]=0
    for _ in range(iters):
        eta=Xi@beta; mu=1/(1+np.exp(-np.clip(eta,-30,30))); W=mu*(1-mu)+1e-6
        g=Xi.T@(mu-y)+P@beta; H=Xi.T@(Xi*W[:,None])+P
        try: step=np.linalg.solve(H,g)
        except: break
        beta-=step
        if np.max(np.abs(step))<1e-7: break
    return beta
def logit_pred(X,beta):
    eta=np.column_stack([np.ones(len(X)),X])@beta; return 1/(1+np.exp(-np.clip(eta,-30,30)))

def skill(pred,y,kind):
    if kind=="bin":
        pos=pred[y==1]; neg=pred[y==0]
        if len(pos)==0 or len(neg)==0: return None
        return float(stats.mannwhitneyu(pos,neg,alternative="two-sided").statistic/(len(pos)*len(neg)))
    return float(stats.spearmanr(pred,y).statistic)

def fit_eval(name,raw,ctrl,kind,k,preds):
    """fit on A, eval held-out skill on B, for config = base(ctrl+gdp)+preds."""
    XA,CA,yA=build(name,raw,ctrl,kind,k,preds,lambda i:half(i)=="A")
    XB,CB,yB=build(name,raw,ctrl,kind,k,preds,lambda i:half(i)=="B")
    if len(yA)<50 or len(yB)<40: return None
    if kind=="bin" and (len(set(yA))<2 or len(set(yB))<2 or yA.sum()<8 or yB.sum()<8): return None
    fit=logit_fit if kind=="bin" else lambda X,y:ridge_fit(X,y)
    pred=logit_pred if kind=="bin" else ridge_pred
    # base = controls only
    muC,sdC=zfit(CA); CAz,CBz=zap(CA,muC,sdC),zap(CB,muC,sdC)
    b0=fit(CAz,yA); sk_base=skill(pred(CBz,b0),yB,kind)
    # stack = controls + preds
    if preds:
        FA=np.column_stack([CA,XA]); FB=np.column_stack([CB,XB])
        muF,sdF=zfit(FA); FAz,FBz=zap(FA,muF,sdF),zap(FB,muF,sdF)
        bS=fit(FAz,yA); sk_stack=skill(pred(FBz,bS),yB,kind)
    else:
        sk_stack=sk_base
    return {"n_A":len(yA),"n_B":len(yB),"skill_base":round(sk_base,3),"skill_stack":round(sk_stack,3),
            "delta":round(sk_stack-sk_base,3)}

def greedy(name,raw,ctrl,kind,k):
    """forward-select from POOL by A-internal 2-fold CV improvement; final eval on B."""
    chosen=[]; improving=True
    # A-internal split by iso hash bit2
    def inA1(iso): return half(iso)=="A" and int(hashlib.sha256(iso.encode()).hexdigest(),16)//7%2==0
    def inA2(iso): return half(iso)=="A" and int(hashlib.sha256(iso.encode()).hexdigest(),16)//7%2==1
    def cvskill(preds):
        # fit on A1 eval A2 and vice versa, avg
        out=[]
        for trf,tef in [(inA1,inA2),(inA2,inA1)]:
            Xtr,Ctr,ytr=build(name,raw,ctrl,kind,k,preds,trf)
            Xte,Cte,yte=build(name,raw,ctrl,kind,k,preds,tef)
            if len(ytr)<30 or len(yte)<20: return None
            if kind=="bin" and (ytr.sum()<6 or yte.sum()<4 or len(set(yte))<2): return None
            fit=logit_fit if kind=="bin" else lambda X,y:ridge_fit(X,y); pr=logit_pred if kind=="bin" else ridge_pred
            F=np.column_stack([Ctr,Xtr]) if preds else Ctr; Fe=np.column_stack([Cte,Xte]) if preds else Cte
            mu,sd=zfit(F); b=fit(zap(F,mu,sd),ytr); s=skill(pr(zap(Fe,mu,sd),b),yte,kind)
            if s is None: return None
            out.append(s if kind=="bin" else abs(s))
        return float(np.mean(out))
    cur=cvskill([])
    if cur is None: return None
    base_cv=cur
    while improving:
        improving=False; best=None
        for p in POOL:
            if p in chosen: continue
            s=cvskill(chosen+[p])
            if s is not None and s>cur+0.005:
                if best is None or s>best[1]: best=(p,s)
        if best: chosen.append(best[0]); cur=best[1]; improving=True
    res=fit_eval(name,raw,ctrl,kind,k,chosen)
    if res: res["chosen"]=chosen; res["cv_base"]=round(base_cv,3); res["cv_final"]=round(cur,3)
    return res

def best_interaction(name,raw,ctrl,kind,k):
    """does any pairwise product of the 6 add held-out skill beyond the two mains?"""
    best=None
    for i in range(len(SIX)):
        for j in range(i+1,len(SIX)):
            a,b=SIX[i],SIX[j]
            mains=fit_eval(name,raw,ctrl,kind,k,[a,b])
            if not mains: continue
            # add interaction as a derived predictor via a temp: build with product
            XA,CA,yA=build(name,raw,ctrl,kind,k,[a,b],lambda i:half(i)=="A")
            XB,CB,yB=build(name,raw,ctrl,kind,k,[a,b],lambda i:half(i)=="B")
            if len(yA)<50 or len(yB)<40: continue
            if kind=="bin" and (yA.sum()<8 or yB.sum()<8): continue
            intA=(XA[:,0]*XA[:,1]).reshape(-1,1); intB=(XB[:,0]*XB[:,1]).reshape(-1,1)
            FA=np.column_stack([CA,XA,intA]); FB=np.column_stack([CB,XB,intB])
            mu,sd=zfit(FA); fit=logit_fit if kind=="bin" else lambda X,y:ridge_fit(X,y); pr=logit_pred if kind=="bin" else ridge_pred
            bb=fit(zap(FA,mu,sd),yA); sk_int=skill(pr(zap(FB,mu,sd),bb),yB,kind)
            d=sk_int-mains["skill_stack"]
            if best is None or abs(d)>abs(best["delta_vs_mains"]):
                best={"pair":f"{a}×{b}","skill_mains":mains["skill_stack"],"skill_with_int":round(sk_int,3),"delta_vs_mains":round(d,3)}
    return best

if __name__=="__main__":
    K=5
    report={}
    print(f"STACKING SCREEN  (lead k={K}, fit on discovery-A, scored on sealed-B, incremental over AR+GDP)\n")
    print(f"{'outcome':>24} {'kind':>4} | {'base':>6} {'best1':>6} {'all6':>6} {'greedy':>7} {'Δgreedy':>8}  chosen")
    print("-"*118)
    for name,raw,ctrl,kind in TARGETS:
        r={"kind":kind}
        base_all6=fit_eval(name,raw,ctrl,kind,K,SIX)
        if not base_all6: print(f"{name:>24} {kind:>4} | (insufficient n)"); report[name]={"note":"insufficient"}; continue
        # best single instrument
        singles={p:fit_eval(name,raw,ctrl,kind,K,[p]) for p in SIX}
        singles={p:v for p,v in singles.items() if v}
        best1=max(singles.items(),key=lambda kv:kv[1]["skill_stack"]) if singles else (None,None)
        g=greedy(name,raw,ctrl,kind,K)
        base=base_all6["skill_base"]
        b1=best1[1]["skill_stack"] if best1[1] else float("nan")
        a6=base_all6["skill_stack"]
        gs=g["skill_stack"] if g else float("nan"); dg=(g["skill_stack"]-base) if g else float("nan")
        ch=",".join(g["chosen"]) if g and g.get("chosen") else "-"
        print(f"{name:>24} {kind:>4} | {base:>6.3f} {b1:>6.3f} {a6:>6.3f} {gs:>7.3f} {dg:>+8.3f}  {ch}")
        r.update({"base":base,"best_single":{best1[0]:b1},"all6":a6,"greedy":g})
        inter=best_interaction(name,raw,ctrl,kind,K)
        r["best_interaction"]=inter
        report[name]=r
    json.dump(report,open(HERE/"stack_results.json","w"),indent=1)
    print("\n=== best pairwise INTERACTION per outcome (does multiply beat add, held-out?) ===")
    for name,r in report.items():
        it=r.get("best_interaction")
        if it: print(f"   {name:>24}: {it['pair']:>26} mains={it['skill_mains']:+.3f} +int={it['skill_with_int']:+.3f} Δ={it['delta_vs_mains']:+.3f}")
    print("\n(Δ near 0 or negative held-out = 'tiers add, don't multiply' confirmed; large + = a real multiplier)")
