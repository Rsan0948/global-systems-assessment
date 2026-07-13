#!/usr/bin/env python3
"""Political signal, taken as WIDE and as FAR BACK as the data allows. Deep V-Dem panel
(1816-2004, every 10y, 20y forward outcome window). Per epoch: does the grievance/
mobilization NUMERATOR (anocracy + civil-society + prior-conflict [+ ethnic exclusion 1946+])
add out-of-sample AUC over STRUCTURE (V-Dem rule-of-law + log Maddison GDP) for predicting
democratic backsliding and domestic conflict onset? Tracks how each relationship evolves
across two centuries. Read-only."""
from __future__ import annotations
import json, csv, sys, math
from collections import defaultdict
from pathlib import Path
import numpy as np
from scipy import stats
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT)); sys.path.insert(0,str(ROOT/"scripts/robustness"))
import convergence_lib as L
rol,gdp=L.load_rol_gdp()                       # V-Dem rule-of-law, Maddison GDP (deep)
lib=json.load(open(ROOT/"data/v2/vdem_democracy.json"))["series"]["libdem"]
POL=json.load(open(ROOT/"data/political/political_indicators.json"))["series"]
cso=POL["cso_participation"]
dom=L.domestic_years()

def gv(d,iso,y):
    s=d.get(iso)
    if not s: return None
    return s.get(str(y)) if str(y) in s else (s.get(y) if y in s else None)
def onset(iso,y0,y1): return 1 if any(y0<=y<=y1 for y in dom.get(iso,set())) else 0

# EPR (1946+) exclusion at a given base year
import urllib.request, io
NM=json.load(open(ROOT/"data/political/_epr_name_iso.json"))
_raw=urllib.request.urlopen(urllib.request.Request("https://icr.ethz.ch/data/epr/core/EPR-2021.csv",headers={"User-Agent":"Mozilla/5.0"}),timeout=60).read().decode("utf-8","replace")
EPR_ROWS=list(csv.DictReader(io.StringIO(_raw)))
def excl(iso,base):
    per=defaultdict(list)
    for r in EPR_ROWS:
        try: fr,to=int(r["from"]),int(r["to"])
        except: continue
        if fr<=base<=to and NM.get(r["statename"])==iso: per[iso].append(r)
    grps=per.get(iso)
    if not grps: return None
    return sum(float(g["size"]) for g in grps if g["status"] in("POWERLESS","DISCRIMINATED","SELF-EXCLUSION") and g["size"] not in("","NA"))

def auc(scores,y): return float(L.auc_roc(scores,y))
def logit_auc_insample(cols,y):
    y=np.array(y,float); X=np.column_stack([np.ones(len(y))]+[L.zscore(c) for c in cols])
    _,a,_=L.logit_fit(X,y); return a
def cv_logit_auc(cols,y,k=5,seed=0):
    """OUT-OF-FOLD AUC. AUDIT C1 FIX: the previous logit_auc fit+scored on the same rows
    (in-sample resubstitution), which -> AUC 1.0 at small n_pos and a spurious +increment.
    Here we z-score INSIDE each fold on train stats, fit on train, score held-out, pool OOF
    predictions, then AUC. Returns None when a fold can't be formed (too few of either class)."""
    y=np.array(y,float); n=len(y); pos=int(y.sum()); neg=n-pos
    if pos<2 or neg<2: return None
    kk=min(k,pos,neg)
    if kk<2: return None
    rng=np.random.default_rng(seed)
    # stratified fold assignment
    fold=np.empty(n,int)
    for cls in (0.0,1.0):
        idx=np.where(y==cls)[0]; idx=rng.permutation(idx)
        fold[idx]=np.arange(len(idx))%kk
    Xraw=np.column_stack(cols).astype(float)
    oof=np.full(n,np.nan)
    for f in range(kk):
        tr=np.where(fold!=f)[0]; te=np.where(fold==f)[0]
        if len(set(y[tr]))<2: return None
        mu=Xraw[tr].mean(0); sd=Xraw[tr].std(0); sd[sd==0]=1.0
        Xtr=np.column_stack([np.ones(len(tr)),(Xraw[tr]-mu)/sd])
        Xte=np.column_stack([np.ones(len(te)),(Xraw[te]-mu)/sd])
        b,_,_=L.logit_fit(Xtr,y[tr])
        oof[te]=1/(1+np.exp(-Xte@b))
    return float(L.auc_roc(list(oof),list(y)))

WIN=20
epochs=list(range(1816,2005,10))
results=[]
for T in epochs:
    universe=sorted(set(rol)&set(gdp))   # REPRODUCIBILITY: pin order (was hash-randomized set)
    rec=[]
    for iso in universe:
        if iso.startswith("OWID"): continue
        r=gv(rol,iso,T); g=gv(gdp,iso,T); lb=gv(lib,iso,T)
        if r is None or g is None or g<=0 or lb is None: continue
        c=gv(cso,iso,T)
        pr=dict(rol=float(r),lg=math.log(g),ano=4*lb*(1-lb),cso=c,pc=onset(iso,T-WIN,T),
                excl=excl(iso,T) if T>=1946 else None,lb=lb)
        l2=gv(lib,iso,T+WIN)
        pr["backslide"]=(1 if (l2-lb)<=-0.05 else 0) if (l2 is not None and lb>=0.10) else None
        pr["conflict"]=onset(iso,T+1,T+WIN)
        rec.append(pr)
    row={"epoch":T,"n":len(rec)}
    for OUT in ["backslide","conflict"]:
        sub=[r for r in rec if r[OUT] is not None and r["cso"] is not None]
        if len(sub)<20 or len(set(r[OUT] for r in sub))<2:
            row[OUT]={"n":len(sub),"note":"insufficient"}; continue
        y=[r[OUT] for r in sub]
        struct=[[r["rol"] for r in sub],[r["lg"] for r in sub]]
        numer=[[r["ano"] for r in sub],[r["cso"] for r in sub],[r["pc"] for r in sub]]
        # AUDIT C1 FIX: headline is now OUT-OF-FOLD; in-sample kept only as a diagnostic.
        a_s=cv_logit_auc(struct,y); a_sn=cv_logit_auc(struct+numer,y)
        a_s_is=logit_auc_insample(struct,y); a_sn_is=logit_auc_insample(struct+numer,y)
        # key bivariate correlations
        def sp(key):
            xy=[(r[key],r[OUT]) for r in sub if r.get(key) is not None]
            if len(xy)<15 or len(set(b for _,b in xy))<2: return None
            return round(float(stats.spearmanr([a for a,_ in xy],[b for _,b in xy]).statistic),3)
        oof_ok = a_s is not None and a_sn is not None
        row[OUT]={"n":len(sub),"n_pos":int(sum(y)),
                  "auc_struct":round(a_s,3) if a_s is not None else None,
                  "auc_struct+numer":round(a_sn,3) if a_sn is not None else None,
                  "increment":round(a_sn-a_s,3) if oof_ok else None,
                  "auc_struct_insample":round(a_s_is,3),"auc_struct+numer_insample":round(a_sn_is,3),
                  "increment_insample":round(a_sn_is-a_s_is,3),
                  "rho_anocracy":sp("ano"),"rho_cso":sp("cso"),"rho_prior_conflict":sp("pc"),
                  "rho_rol":sp("rol"),"rho_exclusion":sp("excl")}
    results.append(row)

(ROOT/"data/political/deep_political.json").write_text(json.dumps(results,indent=1))
print("DEEP POLITICAL PANEL — numerator vs structure across ~2 centuries (20y forward window)\n")
for OUT in ["backslide","conflict"]:
    print(f"===== {OUT.upper()} =====   (OOF = out-of-fold; IS = in-sample diagnostic)")
    print(f"  {'epoch':>5} {'n':>4} {'pos':>4} | {'OOFs':>5} {'OOF+n':>6} {'OOFincr':>7} | {'ISincr':>6} | {'ρ:anoc':>7} {'ρ:cso':>6} {'ρ:priorC':>8}")
    for row in results:
        d=row.get(OUT,{})
        if "auc_struct_insample" not in d: continue
        oof_s=f"{d['auc_struct']:.2f}" if d['auc_struct'] is not None else "  - "
        oof_sn=f"{d['auc_struct+numer']:.2f}" if d['auc_struct+numer'] is not None else "  - "
        oof_i=f"{d['increment']:+.2f}" if d['increment'] is not None else "  -  "
        print(f"  {row['epoch']:>5} {d['n']:>4} {d['n_pos']:>4} | {oof_s:>5} {oof_sn:>6} {oof_i:>7} | {d['increment_insample']:>+6.2f} | "
              f"{(d['rho_anocracy'] if d['rho_anocracy'] is not None else 0):>+7.2f} {(d['rho_cso'] or 0):>+6.2f} {(d['rho_prior_conflict'] or 0):>+8.2f}")
    # summary: mean increment where n>=25, OOF vs in-sample side by side
    oof_incs=[row[OUT]["increment"] for row in results if OUT in row and row[OUT].get("increment") is not None and row[OUT]["n"]>=25]
    is_incs=[row[OUT]["increment_insample"] for row in results if OUT in row and row[OUT].get("increment_insample") is not None and row[OUT]["n"]>=25]
    om=np.mean(oof_incs) if oof_incs else float('nan')
    print(f"  >>> mean OOF increment (n>=25): {om:+.3f} over {len(oof_incs)} epochs  |  mean IN-SAMPLE: {np.mean(is_incs):+.3f} (inflated) over {len(is_incs)}")
    print(f"      OOF increment >0 in {sum(1 for x in oof_incs if x>0)}/{len(oof_incs)} epochs\n")
