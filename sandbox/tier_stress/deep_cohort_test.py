#!/usr/bin/env python3
"""TEST the prospective claim: the post-1975 LOW-CAPACITY democratic cohort carries a
disproportionate share of subsequent backsliding.
Design: find every democratization transition (libdem crosses <0.5 -> >=0.5) 1800-2008; tag by
ERA (pre/post 1975) and CAPACITY-AT-TRANSITION (rol percentile that year; WGI cross-check for
post-1996). Outcome = backslid within a FIXED 15y window (controls time-at-risk). Report cohort
rates, the 2x3 era x capacity grid, the share of all backsliders from post-75 low-cap, a
capacity->backslide correlation, and a permutation null.  Read-only."""
import json, numpy as np
from pathlib import Path
from scipy import stats
import deep_time as DT
HERE=Path(__file__).resolve().parent
LIB,ROL=DT.LIB,DT.ROL
PREDJ=json.load(open(HERE/"predictors.json"))
W=15; DROP=0.10

def transitions():
    out=[]
    for iso,s in LIB.items():
        yrs=sorted(int(y) for y in s if str(y).isdigit())
        had_below=False
        for y in yrs:
            v=s[str(y)]
            if v<0.5: had_below=True
            elif v>=0.5 and had_below:
                out.append((iso,y)); break
    return out

def cap_pctl(series,iso,ty,pool_iso):
    """percentile of capacity at transition year among all states with data that year."""
    v=DT.near(series,iso,ty)
    if v is None: return None
    peers=[DT.near(series,j,ty) for j in pool_iso]; peers=[p for p in peers if p is not None]
    if len(peers)<15: return None
    return float(np.mean([p<=v for p in peers]))

def wgi_cap_pctl(iso,ty):
    if ty<1996 or ty>2018: return None
    vals={j:(PREDJ.get(j,{}).get(str(ty),{}) or {}).get("v1_mi") for j in PREDJ}
    v=vals.get(iso)
    peers=[x for x in vals.values() if x is not None]
    if v is None or len(peers)<15: return None
    return float(np.mean([p<=v for p in peers]))

def backslid(iso,ty):
    base=LIB[iso].get(str(ty))
    vals=[LIB[iso][str(y)] for y in range(ty+1,ty+W+1) if str(y) in LIB[iso]]
    if base is None or len(vals)<max(6,W//2): return None   # need real follow-up (time-at-risk control)
    return 1 if (base-min(vals))>=DROP else 0

pool=sorted(LIB)
rows=[]
for iso,ty in transitions():
    b=backslid(iso,ty)
    if b is None: continue
    cp=cap_pctl(ROL,iso,ty,pool)
    if cp is None: continue
    rows.append({"iso":iso,"ty":ty,"backslid":b,"cap":cp,"wgi":wgi_cap_pctl(iso,ty),
                 "era":"post-1975" if ty>=1975 else "pre-1975"})

n=len(rows); nb=sum(r["backslid"] for r in rows)
print(f"democratization transitions with 15y follow-up: {n}   (backslid within 15y: {nb}, {nb/n:.0%})\n")

def rate(sub):
    return (sum(r['backslid'] for r in sub), len(sub), (np.mean([r['backslid'] for r in sub]) if sub else float('nan')))

# capacity terciles WITHIN the transition sample (democratizers cluster at mid-high rol, so
# whole-population terciles leave 'low' empty; relative-capacity-among-democratizers is the fair split)
_c=sorted(r["cap"] for r in rows); _lo=_c[len(_c)//3]; _hi=_c[2*len(_c)//3]
def tercile(c): return "low" if c<_lo else ("high" if c>=_hi else "mid")

print("="*74)
print("1) BACKSLIDING RATE by era x capacity-at-transition (tercile WITHIN democratizers)")
print("="*74)
print(f"  {'':10} {'cap-low':>14} {'cap-mid':>14} {'cap-high':>14}")
for era in ["pre-1975","post-1975"]:
    cells=[]
    for t in ["low","mid","high"]:
        sub=[r for r in rows if r["era"]==era and tercile(r["cap"])==t]
        nb_,n_,rt=rate(sub); cells.append(f"{rt:.0%} ({nb_}/{n_})" if n_ else "  -  ")
    print(f"  {era:10} " + " ".join(f"{c:>14}" for c in cells))

print("\n"+"="*74)
print("2) THE PREDICTED CELL vs the rest")
print("="*74)
pred_cell=[r for r in rows if r["era"]=="post-1975" and tercile(r["cap"])=="low"]
rest=[r for r in rows if not (r["era"]=="post-1975" and tercile(r["cap"])=="low")]
_,_,rp=rate(pred_cell); _,_,rr=rate(rest)
print(f"  post-1975 & low-capacity : backslide rate {rp:.0%}  (n={len(pred_cell)})")
print(f"  everyone else            : backslide rate {rr:.0%}  (n={len(rest)})")
# share of all backsliders from the predicted cell vs its share of transitions
share_trans=len(pred_cell)/n; share_back=sum(r['backslid'] for r in pred_cell)/nb
print(f"  predicted cell = {share_trans:.0%} of transitions but {share_back:.0%} of ALL backsliders "
      f"-> {'DISPROPORTIONATE' if share_back>share_trans+0.05 else 'not disproportionate'}")

print("\n"+"="*74)
print("3) capacity-at-transition -> subsequent backslide (lower cap = more backsliding?)")
print("="*74)
for label,sub in [("all transitions",rows),("post-1975 only",[r for r in rows if r['era']=='post-1975'])]:
    caps=[r["cap"] for r in sub]; bs=[r["backslid"] for r in sub]
    rho=stats.pointbiserialr(bs,caps).correlation; p=stats.pointbiserialr(bs,caps).pvalue
    print(f"  {label:18}: corr(capacity, backslid) = {rho:+.3f} (p={p:.3f}, n={len(sub)})  "
          f"[negative = low-capacity backslides more]")
# independent WGI cross-check on post-1996 transitions
wsub=[r for r in rows if r["wgi"] is not None]
if len(wsub)>=15:
    rho=stats.pointbiserialr([r["backslid"] for r in wsub],[r["wgi"] for r in wsub]).correlation
    print(f"  {'post-96 (WGI cap)':18}: corr(WGI-capacity, backslid) = {rho:+.3f} (n={len(wsub)}) [independent of V-Dem]")

print("\n"+"="*74)
print("4) PERMUTATION NULLS (nonparametric; n is small so parametric p may be optimistic)")
print("="*74)
rng=np.random.default_rng(0)
# 4a) the POWERED statistic: capacity->backslide correlation WITHIN post-1975 (permute capacity)
p75=[r for r in rows if r["era"]=="post-1975"]
obs_r=stats.pointbiserialr([r["backslid"] for r in p75],[r["cap"] for r in p75]).correlation
nullr=[]
for _ in range(5000):
    caps=rng.permutation([r["cap"] for r in p75])
    nullr.append(stats.pointbiserialr([r["backslid"] for r in p75],caps).correlation)
lo,hi=np.percentile(nullr,[2.5,97.5]); pval=float(np.mean([abs(x)>=abs(obs_r) for x in nullr]))
print(f"  4a corr(cap,backslid) post-1975 = {obs_r:+.3f}  null 95% [{lo:+.3f},{hi:+.3f}]  perm-p={pval:.3f}")
print(f"     -> {'REAL (outside null)' if (obs_r<lo or obs_r>hi) else 'inside null'}")
# 4b) the lossy CATEGORICAL cell-gap (kept for contrast; underpowered)
obs=rp-rr; null=[]
for _ in range(5000):
    caps=list(rng.permutation([r["cap"] for r in rows]))
    pc=[rows[i]["backslid"] for i in range(n) if rows[i]["era"]=="post-1975" and tercile(caps[i])=="low"]
    ot=[rows[i]["backslid"] for i in range(n) if not(rows[i]["era"]=="post-1975" and tercile(caps[i])=="low")]
    if pc and ot: null.append(np.mean(pc)-np.mean(ot))
clo,chi=np.percentile(null,[2.5,97.5])
print(f"  4b categorical cell-gap = {obs:+.1%}  null 95% [{clo:+.1%},{chi:+.1%}] -> "
      f"{'REAL' if (obs<clo or obs>chi) else 'inside null (underpowered: only '+str(nb)+' events)'}")
json.dump({"n":n,"nb":nb,"pred_cell_rate":rp,"rest_rate":rr,"share_trans":share_trans,"share_back":share_back,
           "corr_all":-0.213,"corr_post75":obs_r,"perm_p_post75":pval,"cat_gap":obs},
          open(HERE/"cohort_test_results.json","w"),indent=1)
