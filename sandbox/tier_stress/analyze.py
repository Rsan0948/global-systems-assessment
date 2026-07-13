#!/usr/bin/env python3
"""Curate the confirmed screen into a landscape: by instrument, by outcome, dedupe, surprises."""
import json
from pathlib import Path
from collections import defaultdict
HERE=Path(__file__).resolve().parent
C=json.load(open(HERE/"screen_confirmed.json"))["confirmed"]

# map predictor -> instrument
INSTR={
 'v1_mi':'V1','P1':'V1','P2':'V1','P3':'V1','P4':'V1','P5':'V1','durgap':'V1',
 'v3_numer':'V3','anocracy':'V3','cso':'V3','pts':'V3','youth':'V3','food_imp':'V3','internet':'V3','growth_vol':'V3','prior_conflict_decayed':'V3',
 't4_scar':'T4','t4_decayed_conflict':'T4','t4_pts':'T4','t4_refugee_share':'T4','t4_reversed_trust':'T4',
 't5_turb_libdem':'T5','t5_turb_electdem':'T5',
 't6_spark':'T6','t6_s1_geo':'T6','t6_s2_resource':'T6','t6_s3_transcendent':'T6','t6_s4_military':'T6',
 'dgs':'DGS',
}
def dom(o):
    if o.startswith(('libdem','electdem','rol_vdem')): return 'REGIME'
    if o=='conflict_onset_fwd': return 'CONFLICT'
    return 'ECON/WELLBEING'

def eff(c):  # min |rho| across the two halves = conservative effect
    return min(abs(c['mean_rho']), abs(c['confirm']['mean_rho']))

for c in C:
    c['instr']=INSTR.get(c['pred'],'?'); c['odom']=dom(c['out']); c['eff']=eff(c)

print(f"TOTAL confirmed: {len(C)}\n")

print("=== confirmed by INSTRUMENT x outcome-domain (count) ===")
grid=defaultdict(lambda: defaultdict(int))
for c in C: grid[c['instr']][c['odom']]+=1
insts=['V1','V3','T4','T5','T6','DGS']
doms=['REGIME','CONFLICT','ECON/WELLBEING']
print(f"{'':6}"+"".join(f"{d:>18}" for d in doms))
for I in insts:
    print(f"{I:6}"+"".join(f"{grid[I][d]:>18}" for d in doms))

print("\n=== confirmed by OUTCOME (count, max conservative-effect) ===")
byout=defaultdict(list)
for c in C: byout[c['out']].append(c)
for o in sorted(byout,key=lambda o:-max(x['eff'] for x in byout[o])):
    xs=byout[o]; best=max(xs,key=lambda x:x['eff'])
    print(f"   {o:26} n={len(xs):3}  best={best['pred']:>22} eff={best['eff']:.2f} k={best['k']}")

print("\n=== STRONGEST confirmed (min-half |rho|>=0.30), deduped-ish, by instrument ===")
strong=[c for c in C if c['eff']>=0.30]
strong.sort(key=lambda c:-c['eff'])
seen=set()
for c in strong:
    key=(c['pred'],c['out'])
    if key in seen: continue
    seen.add(key)
    print(f"   [{c['instr']:3}] {c['pred']:>22} -> {c['out']:24} k={c['k']:>2} "
          f"rhoA={c['mean_rho']:+.2f} rhoB={c['confirm']['mean_rho']:+.2f} eff={c['eff']:.2f}")

print("\n=== SURPRISES: political/structural tier -> ECON/WELLBEING or cross-domain, eff>=0.25 ===")
surp=[c for c in C if c['odom'] in ('ECON/WELLBEING',) and c['instr'] in ('V3','T4','T6','DGS','T5') and c['eff']>=0.25]
# best per (pred,out)
bp={}
for c in surp:
    k=(c['pred'],c['out'])
    if k not in bp or c['eff']>bp[k]['eff']: bp[k]=c
for c in sorted(bp.values(),key=lambda c:-c['eff']):
    print(f"   [{c['instr']:3}] {c['pred']:>22} -> {c['out']:24} k={c['k']:>2} eff={c['eff']:.2f}")

print("\n=== T5 (turbulence) and DGS — did the weak/leg instruments predict anything? ===")
for I in ['T5','DGS']:
    xs=[c for c in C if c['instr']==I]
    print(f"   {I}: {len(xs)} confirmed. top:")
    for c in sorted(xs,key=lambda c:-c['eff'])[:6]:
        print(f"      {c['pred']:>16} -> {c['out']:24} k={c['k']:>2} eff={c['eff']:.2f} rhoA={c['mean_rho']:+.2f} rhoB={c['confirm']['mean_rho']:+.2f}")

print("\n=== V1 capacity: what does the flagship predict forward? ===")
xs=[c for c in C if c['instr']=='V1']
bp={}
for c in xs:
    k=(c['pred'],c['out'])
    if k not in bp or c['eff']>bp[k]['eff']: bp[k]=c
for c in sorted(bp.values(),key=lambda c:-c['eff'])[:14]:
    print(f"   {c['pred']:>8} -> {c['out']:24} k={c['k']:>2} eff={c['eff']:.2f}")
