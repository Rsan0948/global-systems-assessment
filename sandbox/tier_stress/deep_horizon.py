#!/usr/bin/env python3
"""Fine-grained horizon play on the deep panel (imports deep_time). Pins the crossover where
slow (capacity) signals overtake fast (turbulence) ones, and shows era x horizon interaction.
Metric identical to deep_time: mean per-cohort partial-rho net of persistence, + sign stability."""
import numpy as np
import deep_time as DT

KGRID=[1,2,3,5,7,10,15,20,25,30]

def sweep(feat,which):
    out={}
    for k in KGRID:
        rr=[DT.cohort_rho(feat,which,k,b) for b in DT.BASES]
        rr=[x[0] for x in rr if x]
        if len(rr)>=3:
            out[k]=(round(float(np.mean(rr)),3),len(rr),round(float(np.mean([np.sign(r)==np.sign(np.mean(rr)) for r in rr])),2))
    return out

print("="*94)
print("FAST vs SLOW signals — mean partial-rho by horizon k (pooled 1820-2015)")
print("  fast = turbulence (turb_lib) ; slow = capacity (rol) & the rol-anocracy gap")
print("="*94)
for which in ["democratize","onset","backslide"]:
    print(f"\n{which}:")
    print(f"  {'k':>4} " + "".join(f"{k:>7}" for k in KGRID))
    for feat in ["turb_lib","rol","gap_rol_anoc","anocracy"]:
        s=sweep(feat,which)
        print(f"  {feat:>12} " + "".join((f"{s[k][0]:+7.2f}" if k in s else "   .   ") for k in KGRID))

print("\n"+"="*94)
print("ERA x HORIZON — where does each headline signal live?")
print("="*94)
HEAD=[("democratize","rol","capacity->democratization (expected SLOW/generational)"),
      ("backslide","gap_rol_anoc","rule-of-law minus anocracy -> backsliding (relational)"),
      ("onset","gap_rol_anoc","rule-of-law minus anocracy -> conflict onset")]
for which,feat,desc in HEAD:
    print(f"\n{desc}\n  [{which} ~ {feat}]  mean rho (n_cohorts)")
    print(f"  {'era':22}" + "".join(f"{'k='+str(k):>10}" for k in [3,5,10,20,30]))
    for elab,e0,e1 in DT.ERAS:
        cells=[]
        for k in [3,5,10,20,30]:
            s=DT.era_skill(feat,which,k,e0,e1)
            cells.append(f"{s['mean_rho']:+.2f}({s['n_cohorts']})" if s else "   -   ")
        print(f"  {elab:22}" + "".join(f"{c:>10}" for c in cells))

print("\n"+"="*94)
print("CROSSOVER: horizon where slow (rol) overtakes fast (turb_lib) for democratization")
print("="*94)
ds_rol=sweep("rol","democratize"); ds_turb=sweep("turb_lib","democratize")
print(f"  {'k':>4} {'rol':>8} {'turb':>8}  winner")
for k in KGRID:
    if k in ds_rol and k in ds_turb:
        r,t=ds_rol[k][0],ds_turb[k][0]
        print(f"  {k:>4} {r:>+8.2f} {t:>+8.2f}  {'ROL(slow)' if abs(r)>abs(t) else 'TURB(fast)'}")
