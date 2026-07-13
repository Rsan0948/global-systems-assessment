#!/usr/bin/env python3
"""Robustness of the two headline stacking gains: replicate across leads k in {3,5,10},
report n and event counts, and lock the greedy-chosen set from k=5 then apply it at other
leads (no re-selection) to rule out per-lead selection luck."""
import numpy as np
import stack_screen as S

FOCUS=[("libdem_backslide","libdem","libdem","bin"),
       ("electdem_backslide","electdem","electdem","bin"),
       ("gdp_pc_growth_fwd","gdp_pc_growth","gdp_pc_growth","cont"),
       ("conflict_onset_fwd","__onset__","prior_conflict_decayed","bin")]

def events(name,raw,ctrl,kind,k):
    XB,CB,yB=S.build(name,raw,ctrl,kind,k,S.SIX,lambda i:S.half(i)=="B")
    XA,CA,yA=S.build(name,raw,ctrl,kind,k,S.SIX,lambda i:S.half(i)=="A")
    return len(yA),int(yA.sum()) if kind=="bin" else len(yA), len(yB), int(yB.sum()) if kind=="bin" else len(yB)

print("Per-lead replication. skill scored on sealed-B, incremental over AR+GDP.\n")
print(f"{'outcome':>22} {'k':>2} | {'nA':>4} {'posA':>5} {'nB':>4} {'posB':>5} | {'base':>6} {'all6':>6} {'greedy':>7} {'Δg':>7}  chosen(greedy@thisk)")
print("-"*130)
locked={}
for name,raw,ctrl,kind in FOCUS:
    for k in [3,5,10]:
        nA,posA,nB,posB=events(name,raw,ctrl,kind,k)
        a6=S.fit_eval(name,raw,ctrl,kind,k,S.SIX)
        g=S.greedy(name,raw,ctrl,kind,k)
        if not a6:
            print(f"{name:>22} {k:>2} | insufficient"); continue
        base=a6["skill_base"]
        gs=g["skill_stack"] if g else float("nan"); dg=(gs-base) if g else float("nan")
        ch=",".join(g["chosen"]) if g and g.get("chosen") else "-"
        if k==5 and g: locked[name]=g.get("chosen",[])
        print(f"{name:>22} {k:>2} | {nA:>4} {posA:>5} {nB:>4} {posB:>5} | {base:>6.3f} {a6['skill_stack']:>6.3f} {gs:>7.3f} {dg:>+7.3f}  {ch}")

print("\n=== LOCK the k=5 greedy set, apply UNCHANGED at k=3 and k=10 (no re-selection) ===")
print(f"{'outcome':>22} {'k':>2} | {'base':>6} {'locked-stack':>13} {'Δ':>7}   (set fixed from k=5)")
print("-"*80)
for name,raw,ctrl,kind in FOCUS:
    preds=locked.get(name)
    if not preds: continue
    for k in [3,5,10]:
        r=S.fit_eval(name,raw,ctrl,kind,k,preds)
        if not r: print(f"{name:>22} {k:>2} | insufficient"); continue
        print(f"{name:>22} {k:>2} | {r['skill_base']:>6.3f} {r['skill_stack']:>13.3f} {r['skill_stack']-r['skill_base']:>+7.3f}")
