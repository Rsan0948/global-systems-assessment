#!/usr/bin/env python3
"""ANGLE 3 — CONTAGION / neighbour effects. Does backsliding DIFFUSE across borders? Modern era
only (adjacency = current borders). Identification:
  * temporal ordering: neighbours' PAST decline (b−k..b) -> own FUTURE backsliding (b..b+k)
  * net of own structure (libdem, rule-of-law) and own recent trend
  * DECISIVE null — SPATIAL PERMUTATION: reassign each country RANDOM neighbours; if random
    neighbours predict as well as real ones, it's regional zeitgeist, not geographic contagion.
Metric = mean per-cohort partial-Spearman(neighbour-recent-Δlibdem, own future backslide | controls),
annual base years 1990-2013, k=5."""
import numpy as np
from scipy import stats
import common as C

K=5; B0,B1=1990,2013
def lib(i,y): return C.near(C.LIB,i,y)
def rol(i,y): return C.near(C.ROL,i,y)
ISOS=[i for i in C.LIB if C.neighbors(i)]          # countries with >=1 land neighbour

def dlib(i,b):   # recent change over the trailing k years
    a,c=lib(i,b-K),lib(i,b); return None if a is None or c is None else c-a
def future_bs(i,b):
    a,c=lib(i,b),lib(i,b+K); return None if a is None or c is None else (1.0 if (c-a)<=-0.05 else 0.0)
def nbr_recent(i,b,adj):
    js=adj.get(i,[]); vals=[dlib(j,b) for j in js]; vals=[v for v in vals if v is not None]
    return float(np.mean(vals)) if vals else None

ADJ={i:C.neighbors(i) for i in ISOS}

def cohort_partial(b,adj,permute_labels=False,rng=None):
    rows=[]
    for i in ISOS:
        nr=nbr_recent(i,b,adj); y=future_bs(i,b); l=lib(i,b); r=rol(i,b); own=dlib(i,b)
        if None in (nr,y,l,r,own): continue
        rows.append((nr,y,l,r,own))
    if len(rows)<25 or len({x[1] for x in rows})<2: return None
    xs=[x[0] for x in rows]
    if permute_labels: xs=list(rng.permutation(xs))
    return C.partial_spearman(xs,[x[1] for x in rows],
                              [[x[2] for x in rows],[x[3] for x in rows],[x[4] for x in rows]])

def mean_partial(adj):
    rr=[cohort_partial(b,adj) for b in range(B0,B1+1)]; rr=[x for x in rr if x is not None]
    return (float(np.mean(rr)),len(rr)) if len(rr)>=3 else (None,0)

# observed (real adjacency)
obs,ncoh=mean_partial(ADJ)
print("="*90)
print(f"CONTAGION: neighbours' recent Δlibdem -> own future backslide | libdem, rol, own-trend")
print("="*90)
print(f"  observed mean per-cohort ρ = {obs:+.3f}  (cohorts={ncoh})   [ρ<0 = neighbours declining -> you backslide]")

# NULL 1 — label permutation (shuffle neighbour-signal across countries within cohort)
rng=np.random.default_rng(0)
lab_null=[]
for _ in range(600):
    rr=[cohort_partial(b,ADJ,permute_labels=True,rng=rng) for b in range(B0,B1+1)]; rr=[x for x in rr if x is not None]
    if len(rr)>=3: lab_null.append(np.mean(rr))
llo,lhi=np.percentile(lab_null,[2.5,97.5])
print(f"  label-perm null 95% [{llo:+.3f},{lhi:+.3f}] -> {'signal REAL' if (obs<llo or obs>lhi) else 'null'}")

# NULL 2 — SPATIAL permutation (reassign RANDOM neighbour-sets; is it GEOGRAPHIC adjacency specifically?)
keys=list(ADJ); vals=[ADJ[k] for k in keys]
spat_null=[]
rng2=np.random.default_rng(1)
for _ in range(600):
    perm=rng2.permutation(len(vals))
    radj={keys[i]:vals[perm[i]] for i in range(len(keys))}   # country i gets some other country's neighbour list
    m,_=mean_partial(radj)
    if m is not None: spat_null.append(m)
slo,shi=np.percentile(spat_null,[2.5,97.5])
print(f"  SPATIAL-perm null (random neighbours) 95% [{slo:+.3f},{shi:+.3f}]  mean={np.mean(spat_null):+.3f}")
print(f"    -> {'GEOGRAPHIC CONTAGION (real neighbours beat random)' if (obs<slo or obs>shi) else 'NOT adjacency-specific (regional/global zeitgeist, not diffusion)'}")

# extra read: raw neighbour effect WITHOUT own-structure controls (how big before controls)
def cohort_raw(b):
    rows=[(nbr_recent(i,b,ADJ),future_bs(i,b)) for i in ISOS]
    rows=[x for x in rows if None not in x]
    if len(rows)<25 or len({x[1] for x in rows})<2: return None
    return stats.spearmanr([x[0] for x in rows],[x[1] for x in rows]).statistic
raw=[cohort_raw(b) for b in range(B0,B1+1)]; raw=[x for x in raw if x is not None]
print(f"\n  (context) raw neighbour→own corr, NO controls: {np.mean(raw):+.3f}  vs net-of-structure {obs:+.3f}")

import json
json.dump({"angle":3,"obs_partial":round(obs,3),"n_cohorts":ncoh,
           "label_null":[round(llo,3),round(lhi,3)],"spatial_null":[round(slo,3),round(shi,3)],
           "adjacency_specific":bool(obs<slo or obs>shi),
           "real_vs_labelnull":bool(obs<llo or obs>lhi),"raw_no_controls":round(float(np.mean(raw)),3)},
          open(HERE_JSON:="angle3_results.json","w"),indent=1)
print("\nsaved angle3_results.json")
