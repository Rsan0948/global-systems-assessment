#!/usr/bin/env python3
"""Tier 7 — Mule Archetype Derivation. Does the six-tier state SHAPE constrain the TYPE of
destabilizing actor (A1 populist / A2 military / A3 insurgent / A4 kleptocrat / A5 theocrat /
A6 external / A7 institutional)? M1 cosine-similarity same-archetype rate; M2 leave-one-out
classification of archetype from the shape vector; M4 predictions for clean countries; M5
archetype x criticality. Actor codes hand-assigned from documented modern cases (single-coder,
disclosed). Frozen spec: docs/TIER7_ARCHETYPE_PREREGISTRATION.md (sha256 02bed840)."""
from __future__ import annotations
import json, sys, itertools
import numpy as np
sys.path.insert(0,"scripts/robustness")
six={r["iso"]:r for r in json.load(open("data/political/six_tier_snapshot.json"))}

# ---- HAND-CODED dominant modern destabilization archetype (documented cases) ----
ARCH={
 # A1 civilian populist-nationalist
 "HUN":"A1","POL":"A1","TUR":"A1","VEN":"A1","IND":"A1","BRA":"A1","USA":"A1","SLV":"A1","PER":"A1",
 "PHL":"A1","SRB":"A1","LKA":"A1","BGD":"A1","SVK":"A1","ECU":"A1","BOL":"A1","GEO":"A1","MEX":"A1","IDN":"A1",
 # A2 military interventionist
 "THA":"A2","EGY":"A2","MMR":"A2","PAK":"A2","MLI":"A2","BFA":"A2","NER":"A2","GIN":"A2","SDN":"A2",
 "TCD":"A2","MRT":"A2","FJI":"A2","GAB":"A2","KOR":"A2","GNB":"A2",
 # A3 insurgent commander
 "SYR":"A3","COL":"A3","COD":"A3","SOM":"A3","YEM":"A3","ETH":"A3","NGA":"A3","MOZ":"A3","CAF":"A3","SSD":"A3","CMR":"A3",
 # A4 kleptocratic strongman
 "RUS":"A4","KAZ":"A4","AZE":"A4","BLR":"A4","KHM":"A4","COG":"A4","GNQ":"A4","TKM":"A4","UZB":"A4",
 "TJK":"A4","NIC":"A4","AGO":"A4","UGA":"A4","RWA":"A4","DJI":"A4","TGO":"A4","ZWE":"A4",
 # A5 theocratic/ideological
 "IRN":"A5","AFG":"A5",
 # A6 external intervention
 "IRQ":"A6","LBY":"A6",
 # A7 institutional capture
 "TUN":"A7","ISR":"A7",
}
TIERS=["V1","V2","V3","T4","T6"]  # T5 scoped to democracies -> used in M5
def riskvec(r):  # orient so all = risk (higher=worse)
    return [100-r["V1"],100-r["V2"],r["V3"],r["T4"],r["T6"]]
coded=[i for i in ARCH if i in six]
X=np.array([riskvec(six[i]) for i in coded],float)
mu,sd=X.mean(0),X.std(0); Z=(X-mu)/sd
labels=[ARCH[i] for i in coded]
print(f"coded events: {len(coded)} countries | archetype counts:",{a:labels.count(a) for a in sorted(set(labels))})

# ---- M1: cosine similarity same-archetype rate ----
def cos(a,b): return float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)+1e-9))
sims=[]
for i,j in itertools.combinations(range(len(coded)),2):
    c=cos(X[i],X[j]); sims.append((c,labels[i]==labels[j]))
hi=[s for c,s in sims if c>0.85]
allpairs=[s for c,s in sims]
print(f"\n=== M1 (GATE) — same-archetype rate ===")
print(f"   among cosine-similar pairs (>0.85, n={len(hi)}): {np.mean(hi):.2f} same archetype")
print(f"   among ALL pairs (baseline, n={len(allpairs)}): {np.mean(allpairs):.2f}")
print(f"   >>> lift over baseline: {np.mean(hi)-np.mean(allpairs):+.2f}")

# ---- M2: leave-one-out nearest-centroid classification ----
def loo_classify():
    correct=0; preds=[]
    for k in range(len(coded)):
        tr=[m for m in range(len(coded)) if m!=k]
        cents={}
        for a in set(labels):
            idx=[m for m in tr if labels[m]==a]
            if idx: cents[a]=Z[idx].mean(0)
        d={a:np.linalg.norm(Z[k]-c) for a,c in cents.items()}
        pred=min(d,key=d.get); preds.append(pred)
        if pred==labels[k]: correct+=1
    return correct/len(coded), preds
acc,preds=loo_classify()
maj=max(labels.count(a) for a in set(labels))/len(labels)
print(f"\n=== M2 — LOO classification of archetype from shape ===")
print(f"   out-of-sample accuracy = {acc:.2f}  (majority-class baseline {maj:.2f}, random 1/7={1/7:.2f})")
print(f"   >>> shape predicts archetype above baseline: {acc>maj}")
# per-archetype fingerprint (mean six-tier, original scale)
print("\n   archetype fingerprints (mean V1/V2/V3/T4/T5/T6):")
for a in sorted(set(labels)):
    isos=[i for i in coded if ARCH[i]==a]
    fp=[np.mean([six[i][t] for i in isos]) for t in ["V1","V2","V3","T4"]]
    t5=[six[i]["T5"] for i in isos if six[i]["T5"] is not None]
    t5m=(sum(t5)/len(t5)) if t5 else 0.0
    t6=np.mean([six[i]["T6"] for i in isos])
    print(f"   {a} (n={len(isos)}): V1={fp[0]:.0f} V2={fp[1]:.0f} V3={fp[2]:.0f} T4={fp[3]:.0f} T5={t5m:.0f} T6={t6:.0f}  e.g. {six[isos[0]]['name']}")

# ---- M4: predict archetype for CLEAN (uncoded) countries ----
cents={a:Z[[m for m in range(len(coded)) if labels[m]==a]].mean(0) for a in set(labels)}
def predict(iso):
    z=(np.array(riskvec(six[iso]),float)-mu)/sd
    d={a:np.linalg.norm(z-c) for a,c in cents.items()}
    order=sorted(d,key=d.get)
    # softmax-ish probability from inverse distance
    inv={a:1/(d[a]+.5) for a in d}; s=sum(inv.values())
    return order[0],inv[order[0]]/s,order[1],inv[order[1]]/s
print("\n=== M4 — archetype prediction for CLEAN / non-crisis countries ===")
for iso in ["NLD","DNK","NOR","CHE","DEU","CAN","JPN","URY","CRI","BWA"]:
    if iso in six and iso not in ARCH:
        a1,p1,a2,p2=predict(iso)
        print(f"   {six[iso]['name']:14s} -> {a1} (p={p1:.2f}), 2nd {a2} (p={p2:.2f})")
print("   (pre-registered: Netherlands should be far from every crisis fingerprint / low confidence)")
# check the pre-registered coded predictions via LOO
print("\n   pre-registered checks (LOO predicted vs actual):")
for iso in ["USA","KOR","POL","ISR"]:
    if iso in coded:
        k=coded.index(iso); print(f"   {six[iso]['name']:14s}: predicted {preds[k]}  actual {ARCH[iso]}  {'MATCH' if preds[k]==ARCH[iso] else 'miss'}")

# ---- M5: archetype x criticality for flickering countries ----
print("\n=== M5 — flickering (high T5) countries: archetype + criticality ===")
for iso in ["POL","ROU","KOR","BRA","LKA","MDA","THA","TUN","ARM"]:
    if iso in six and six[iso]["T5"] is not None and six[iso]["T5"]>=60:
        a=ARCH.get(iso,"(clean)")
        print(f"   {six[iso]['name']:14s} T5={six[iso]['T5']:.0f} + archetype {a}")

json.dump({"n":len(coded),"M1_similar_same_rate":round(float(np.mean(hi)),3),"M1_baseline":round(float(np.mean(allpairs)),3),
           "M2_loo_accuracy":round(acc,3),"M2_baseline":round(maj,3),
           "fingerprints":{a:{t:round(float(np.mean([six[i][t] for i in coded if ARCH[i]==a and six[i][t] is not None])),1) for t in ["V1","V2","V3","T4","T6"]} for a in sorted(set(labels))}},
          open("data/political/tier7_archetype.json","w"),indent=1)
