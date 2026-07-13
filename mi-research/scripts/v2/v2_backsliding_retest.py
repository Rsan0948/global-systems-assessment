#!/usr/bin/env python3
"""Preliminary re-test of V2 hypotheses on a DEMOCRATIC-BACKSLIDING outcome (V-Dem liberal
democracy index decline 2004->2024), fetched via OWID — a rich-democracy-sensitive stress
measure the committed conflict-onset outcome misses. Not the final test (equity for rich
countries is still the income-Gini proxy; V-Party populism + PISA equity pending). Read-only."""
import json, sys, numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"scripts"/"robustness")); sys.path.insert(0,str(ROOT))
import convergence_lib as L
from mi import panel as MP
from mi.scoring import calculate_pillar_scores, calculate_mi_score
V2=json.loads((ROOT/"data/v2/v2_scores.json").read_text())["scores"]
lib=json.loads((ROOT/"data/v2/vdem_democracy.json").read_text())["series"]["libdem"]
def near(iso,y):
    s=lib.get(iso)
    if not s: return None
    s={int(k):v for k,v in s.items()}
    for d in range(4):
        for yy in ([y] if d==0 else [y-d,y+d]):
            if yy in s: return s[yy]
    return None
def backslide(iso):
    a,b=near(iso,2004),near(iso,2024)
    return None if (a is None or b is None) else (1 if (b-a)<=-0.05 else 0)
def v1(iso):
    ind=MP.indicators_for(iso,2024)
    try: return calculate_mi_score(calculate_pillar_scores(ind)) if ind else None
    except: return None
rows=[]
for i in V2:
    r=V2[i]
    if r["V2_Combined"] is None: continue
    y=backslide(i); v=v1(i)
    if None in (y,v,r["V2_Level"],r["V2_Equity"]): continue
    rows.append({"y":y,"v1":v,"vL":r["V2_Level"],"vE":r["V2_Equity"],"vC":r["V2_Combined"]})
y=[r["y"] for r in rows]
def la(cols):
    X=np.column_stack([np.ones(len(y))]+[L.zscore(c) for c in cols]); _,a,_=L.logit_fit(X,np.array(y,float)); return round(float(a),4)
res={"outcome":"V-Dem liberal-democracy decline <=-0.05, 2004->2024","n":len(rows),"n_backsliders":int(sum(y)),
 "H5":{"v1":la([[r['v1'] for r in rows]]),"v2Level":la([[r['vL'] for r in rows]]),"v2Equity":la([[r['vE'] for r in rows]]),
       "v1+v2L":la([[r['v1'] for r in rows],[r['vL'] for r in rows]]),
       "v1+v2L+v2E":la([[r['v1'] for r in rows],[r['vL'] for r in rows],[r['vE'] for r in rows]])}}
res["H5"]["equity_gain"]=round(res["H5"]["v1+v2L+v2E"]-res["H5"]["v1+v2L"],4)
medL=np.median([r["vL"] for r in rows]); medE=np.median([r["vE"] for r in rows])
q={"HL_HE":[],"HL_LE":[],"LL_HE":[],"LL_LE":[]}
for r in rows:
    k=("HL_HE" if r["vL"]>=medL and r["vE"]>=medE else "HL_LE" if r["vL"]>=medL else "LL_HE" if r["vE"]>=medE else "LL_LE")
    q[k].append(r["y"])
res["H6"]={k:{"n":len(v),"backslide_rate":round(float(np.mean(v)),3) if v else None} for k,v in q.items()}
res["H6"]["HL_LE_gt_LL_HE"]=bool(np.mean(q["HL_LE"])>np.mean(q["LL_HE"]))
(ROOT/"data/v2/v2_backsliding_retest.json").write_text(json.dumps(res,indent=1))
print(json.dumps(res,indent=1))
