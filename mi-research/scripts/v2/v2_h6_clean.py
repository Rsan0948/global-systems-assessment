#!/usr/bin/env python3
"""H6 re-run controlling the backsliding floor effect: restrict to countries with a real
liberal democracy to lose in 2004 (libdem_2004 >= threshold), removing already-autocratic
states (Turkmenistan/Syria/Kazakhstan...) that mechanically can't backslide. Also flags the
authoritarian-equity-inflation artifact. Read-only."""
import json, csv, sys, numpy as np
from scipy import stats
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
V2=json.load(open(ROOT/"data/v2/v2_scores.json"))["scores"]
lib=json.load(open(ROOT/"data/v2/vdem_democracy.json"))["series"]["libdem"]
NAME={r["iso3"]:r["country"] for r in csv.DictReader(open(ROOT/"../mi-pipeline/data/wb_cached.csv"))}
def ld(iso,yrs):
    s=lib.get(iso)
    if not s: return None
    s={int(k):v for k,v in s.items()}
    return next((s[y] for y in yrs if y in s),None)
rows=[]
for i,r in V2.items():
    if r["V2_Combined"] is None: continue
    d04=ld(i,range(2004,2001,-1)); d24=ld(i,range(2024,2021,-1))
    if d04 is None or d24 is None: continue
    rows.append(dict(iso=i,name=NAME.get(i,i)[:18],L=r["V2_Level"],E=r["V2_Equity"],d04=d04,bs=d24-d04))
mL=np.median([r["L"] for r in rows]); mE=np.median([r["E"] for r in rows])
def q(r): return ("HL_HE" if r["L"]>=mL and r["E"]>=mE else "HL_LE" if r["L"]>=mL else "LL_HE" if r["E"]>=mE else "LL_LE")
for r in rows: r["q"]=q(r)

out={"quadrant_medians":{"L":round(mL,1),"E":round(mE,1)},"variants":{}}
for thr in [0.0, 0.25, 0.3, 0.4]:
    sub=[r for r in rows if r["d04"]>=thr]
    qd={k:[r for r in sub if r["q"]==k] for k in ["HL_HE","HL_LE","LL_HE","LL_LE"]}
    def rate(k):
        g=qd[k]; b=sum(1 for r in g if r["bs"]<=-0.05); return b,len(g),(round(b/len(g),3) if g else None)
    rates={k:rate(k) for k in qd}
    # Fisher HL_LE vs LL_HE
    hl=rate("HL_LE"); ll=rate("LL_HE")
    fisher=None
    if hl[1]>=4 and ll[1]>=4:
        fisher=round(stats.fisher_exact([[hl[0],hl[1]-hl[0]],[ll[0],ll[1]-ll[0]]],alternative="greater")[1],4)
    # HL_LE vs rest
    rest_b=sum(rate(k)[0] for k in ["HL_HE","LL_HE","LL_LE"]); rest_n=sum(rate(k)[1] for k in ["HL_HE","LL_HE","LL_LE"])
    fisher_rest=round(stats.fisher_exact([[hl[0],hl[1]-hl[0]],[rest_b,rest_n-rest_b]],alternative="greater")[1],4) if hl[1]>=4 else None
    out["variants"][f"libdem2004>={thr}"]={"n":len(sub),
        "rates":{k:f"{rates[k][0]}/{rates[k][1]}={rates[k][2]}" for k in rates},
        "HL_LE_vs_LL_HE_fisher_p":fisher,"HL_LE_vs_rest_fisher_p":fisher_rest,
        "excluded_floor":[r["name"] for r in rows if r["d04"]<thr and r["q"]=="LL_HE"]}
(ROOT/"data/v2/v2_h6_clean.json").write_text(json.dumps(out,indent=1))
print(f"quadrant medians L={mL:.1f} E={mE:.1f}\n")
for k,v in out["variants"].items():
    print(f"[{k}] n={v['n']}")
    print(f"   rates: {v['rates']}")
    print(f"   HL_LE>LL_HE Fisher p={v['HL_LE_vs_LL_HE_fisher_p']} | HL_LE>rest p={v['HL_LE_vs_rest_fisher_p']}")
    if v["excluded_floor"]: print(f"   floor-excluded from LL_HE: {', '.join(v['excluded_floor'])}")
    print()
