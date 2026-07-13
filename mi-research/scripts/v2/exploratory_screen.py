#!/usr/bin/env python3
"""Disciplined 'throw it at the wall' screen: many V1/V2 predictors x many niche outcomes,
full Spearman matrix, BH-FDR across the entire family, then every FDR survivor re-tested
with GDP-per-capita partialled out (the development confounder). Report all. Read-only."""
import json, csv, sys, math, numpy as np
from scipy import stats
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT)); sys.path.insert(0,str(ROOT/"scripts/robustness"))
from mi import panel as MP
from mi.scoring import calculate_pillar_scores, calculate_mi_score
import convergence_lib as L
V2=json.load(open(ROOT/"data/v2/v2_scores.json"))["scores"]
IND=json.load(open(ROOT/"data/v2/v2_indicators.json"))["series"]
EXO=json.load(open(ROOT/"data/v2/exploratory_outcomes.json"))["series"]
vdem=json.load(open(ROOT/"data/v2/vdem_democracy.json"))["series"]
NAME={r["iso3"]:r["country"] for r in csv.DictReader(open(ROOT/"../mi-pipeline/data/wb_cached.csv"))}

def latest(ser,iso,lo=2015,hi=2024):
    s=ser.get(iso) if ser else None
    if not s: return None
    for y in range(hi,lo-1,-1):
        if str(y) in s: return s[str(y)]
    return None
def chg(ser,iso,y0,y1,tol=3):
    s=ser.get(iso) if ser else None
    if not s: return None
    def near(y):
        for d in range(tol+1):
            for yy in ([y] if d==0 else [y-d,y+d]):
                if str(yy) in s: return s[str(yy)]
        return None
    a,b=near(y0),near(y1); return None if a is None or b is None else b-a
def series_stat(ser,iso,y0,y1,fn):
    s=ser.get(iso) if ser else None
    if not s: return None
    v=[s[str(y)] for y in range(y0,y1+1) if str(y) in s]
    return fn(v) if len(v)>=5 else None
def maxdd(ser,iso,y0,y1):
    s=ser.get(iso) if ser else None
    if not s: return None
    v=[s[str(y)] for y in range(y0,y1+1) if str(y) in s and s[str(y)]>0]
    if len(v)<4: return None
    peak=-1;worst=0
    for x in v:
        peak=max(peak,x)
        if peak>0: worst=max(worst,(peak-x)/peak*100)
    return worst

# ---------- PREDICTORS (latest / 2024) ----------
dom=L.domestic_years()
pred={}
for iso in V2:
    r=V2[iso]
    ind=MP.indicators_for(iso,2024)
    if not ind: continue
    try: pil=calculate_pillar_scores(ind); v1=calculate_mi_score(pil)
    except: continue
    if v1 is None or r["V2_Combined"] is None: continue
    p={"v1":v1*100,"P1":pil.get("P1"),"P2":pil.get("P2"),"P3":pil.get("P3"),"P4":pil.get("P4"),"P5":pil.get("P5"),
       "vL":r["V2_Level"],"vE":r["V2_Equity"],"vC":r["V2_Combined"]}
    for f in ["F1","F2","F3","F4","F5","F6"]: p[f]=r["pillars"][f]["score"]
    p["gap_v1_vC"]=v1*100-r["V2_Combined"]
    p["gap_v1_vE"]=v1*100-r["V2_Equity"]
    p["imbalance_LE"]=abs(r["V2_Level"]-r["V2_Equity"])
    ps=[r["pillars"][f]["score"] for f in ["F1","F2","F3","F4","F5","F6"] if r["pillars"][f]["score"] is not None]
    p["v2_spread"]=float(np.std(ps)) if len(ps)>=4 else None
    p["_gdp"]=latest(IND.get("gdp_pc_ppp"),iso)
    pred[iso]={k:v for k,v in p.items() if v is not None}

# ---------- OUTCOMES ----------
outc={}
for iso in pred:
    o={}
    o["d_libdem"]=chg(vdem.get("libdem"),iso,2004,2024)
    o["d_electdem"]=chg(vdem.get("electdem"),iso,2004,2024)
    o["d_rol_vdem"]=chg(vdem.get("rol_vdem"),iso,2004,2024)
    o["gdp_growth_mean"]=series_stat(EXO.get("gdp_pc_growth"),iso,2010,2024,np.mean)
    o["gdp_growth_vol"]=series_stat(EXO.get("gdp_pc_growth"),iso,2010,2024,lambda v:float(np.std(v)))
    o["gdp_maxdrawdown"]=maxdd(IND.get("gdp_pc_ppp"),iso,2004,2024)
    o["inflation_vol"]=series_stat(EXO.get("inflation"),iso,2010,2024,lambda v:float(np.std(v)))
    o["gross_savings"]=latest(EXO.get("gross_savings"),iso)
    o["fdi_in"]=latest(EXO.get("fdi_in"),iso)
    o["fertility"]=latest(EXO.get("fertility"),iso)
    o["d_life_exp"]=chg(IND.get("le"),iso,2004,2024)
    o["suicide"]=latest(EXO.get("suicide"),iso)
    o["life_satisfaction"]=latest(EXO.get("life_satisfaction"),iso)
    o["unemployment"]=latest(EXO.get("unemployment"),iso)
    o["conflict_onset_0424"]=1 if any(2004<=y<=2024 for y in dom.get(iso,set())) else 0
    outc[iso]={k:v for k,v in o.items() if v is not None}

PREDS=["v1","P1","P2","P3","P4","P5","vL","vE","vC","F1","F2","F3","F4","F5","F6","gap_v1_vC","gap_v1_vE","imbalance_LE","v2_spread"]
OUTS=["d_libdem","d_electdem","d_rol_vdem","gdp_growth_mean","gdp_growth_vol","gdp_maxdrawdown","inflation_vol",
      "gross_savings","fdi_in","fertility","d_life_exp","suicide","life_satisfaction","unemployment","conflict_onset_0424"]

def partial_spearman(x,y,z):
    """Spearman(x,y | z) via rank residuals."""
    rx,ry,rz=stats.rankdata(x),stats.rankdata(y),stats.rankdata(z)
    ex=rx-np.polyval(np.polyfit(rz,rx,1),rz); ey=ry-np.polyval(np.polyfit(rz,ry,1),rz)
    return stats.pearsonr(ex,ey)

tests=[]
for P in PREDS:
    for O in OUTS:
        xy=[(pred[i][P],outc[i][O],pred[i].get("_gdp")) for i in pred
            if P in pred[i] and O in outc[i] and pred[i].get("_gdp")]
        if len(xy)<25: continue
        x=[a for a,_,_ in xy]; y=[b for _,b,_ in xy]
        if len(set(y))<3: continue
        sp=stats.spearmanr(x,y)
        tests.append({"pred":P,"out":O,"n":len(xy),"rho":float(sp.statistic),"p":float(sp.pvalue),
                      "x":x,"y":y,"g":[math.log10(c) for _,_,c in xy]})
# BH-FDR
ps=sorted(range(len(tests)),key=lambda i:tests[i]["p"]); m=len(tests)
crit=None
for rank,idx in enumerate(ps,1):
    if tests[idx]["p"]<=rank/m*0.05: crit=tests[idx]["p"]
for t in tests: t["fdr_sig"]=(t["p"]<=crit) if crit else False

survivors=[t for t in tests if t["fdr_sig"]]
# partial out GDP for survivors
for t in survivors:
    pr=partial_spearman(t["x"],t["y"],t["g"])
    t["partial_rho"]=round(float(pr.statistic),3); t["partial_p"]=round(float(pr.pvalue),4)
    t["survives_gdp_control"]=bool(pr.pvalue<0.05 and np.sign(pr.statistic)==np.sign(t["rho"]))

out={"n_tests":m,"n_fdr_survivors":len(survivors),"fdr_crit_p":crit,
     "survivors":sorted([{k:round(t[k],3) if isinstance(t[k],float) else t[k]
                          for k in ["pred","out","n","rho","p","partial_rho","partial_p","survives_gdp_control"]}
                         for t in survivors],key=lambda d:-abs(d["rho"]))}
(ROOT/"data/v2/exploratory_screen.json").write_text(json.dumps(out,indent=1))
print(f"total tests: {m} | BH-FDR(0.05) survivors: {len(survivors)} (crit p<={crit})\n")
print(f"{'predictor':>12} {'outcome':>20} {'n':>4} {'rho':>7} {'p':>9} | {'partial|GDP':>11} {'p':>7} survives?")
print("-"*90)
for d in out["survivors"]:
    print(f"{d['pred']:>12} {d['out']:>20} {d['n']:>4} {d['rho']:>+7.3f} {d['p']:>9.1e} | {d['partial_rho']:>+11.3f} {d['partial_p']:>7.3f} {'YES' if d['survives_gdp_control'] else 'no'}")
