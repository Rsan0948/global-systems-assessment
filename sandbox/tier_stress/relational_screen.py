#!/usr/bin/env python3
"""Relational / ratio test. Instead of stacking instruments as independent additive terms,
build the GAPS and RATIOS *between* them — the way MI relates its pillars (durability gap
P4-P1, complexity>capacity). Normalize each instrument MI-style (within-year, TRAIN-only
reference -> no leakage), then:
  * the founding equation as ONE number: matching_gap = complexity - capacity
  * pairwise gaps/ratios between the V's/T's
  * cross-tier discordance + tier-profile dispersion (imbalance, the V2 idea)
Compare RELATIONAL vs ADDITIVE vs BOTH on the sealed TEST third; plus univariate matching_gap.
"""
import json, math, hashlib, itertools
from pathlib import Path
import numpy as np
from scipy import stats
import combo_search as CS
import stack_screen as S
HERE=Path(__file__).resolve().parent
PRED=CS.PRED; BASES=CS.BASES

# the six instrument composites + the two pillars used for the internal durability gap
INSTR=['v1_mi','v3_numer','t4_scar','t5_turb_libdem','t6_spark','dgs']
CAP='v1_mi'; PRESS='v3_numer'; SCAR='t4_scar'; TURB='t5_turb_libdem'; SPARK='t6_spark'
PILLARS=['P1','P2','P3','P4','P5']

def grp(iso): return ['FIT','SEL','TEST'][int(hashlib.sha256(iso.encode()).hexdigest(),16)%3]

def assemble(name,raw,ctrl,kind,k):
    """rows with base year kept, so we can normalize within each cohort cross-section."""
    rows=[]
    for b in BASES:
        if b+k>2025: continue
        for iso in sorted(PRED):
            y=CS.target_val(iso,b,k,name,raw,kind)
            cc=S.pv(iso,b,ctrl) if ctrl in CS.POOL else S.ov(iso,b,ctrl)
            g=S.lgdp(iso,b)
            if y is None or cc is None or g is None: continue
            vals={f:S.pv(iso,b,f) for f in set(INSTR+PILLARS)}
            rows.append({"iso":iso,"b":b,"grp":grp(iso),"y":float(y),"ctrl":float(cc),"lgdp":float(g),"v":vals})
    return rows

def normalize(rows):
    """per base-year: z-score and percentile each instrument using TRAIN(non-TEST) reference."""
    byb={}
    for r in rows: byb.setdefault(r["b"],[]).append(r)
    for b,rs in byb.items():
        for f in set(INSTR+PILLARS):
            train=[r["v"][f] for r in rs if r["grp"]!="TEST" and r["v"][f] is not None]
            if len(train)<8:
                for r in rs: r.setdefault("z",{})[f]=None; r.setdefault("p",{})[f]=None
                continue
            mu=float(np.mean(train)); sd=float(np.std(train)) or 1.0; srt=np.sort(train)
            for r in rs:
                x=r["v"][f]
                r.setdefault("z",{})[f]= None if x is None else (x-mu)/sd
                r.setdefault("p",{})[f]= None if x is None else float(np.searchsorted(srt,x)/len(srt))
    return rows

def feat(r):
    """build the relational feature dict for one row (None if inputs missing)."""
    z=r["z"]; p=r["p"]; f={}
    def zz(a): return z.get(a)
    def pp(a): return p.get(a)
    def gap(a,b): return None if zz(a) is None or zz(b) is None else zz(a)-zz(b)
    def ratio(a,b):
        pa,pb=pp(a),pp(b)
        return None if pa is None or pb is None else (pa+0.05)/(pb+0.05)
    # complexity = mean of the three numerator/environment tiers; capacity = V1
    comp=[zz(PRESS),zz(SCAR),zz(SPARK)]
    comp=[c for c in comp if c is not None]
    cap=zz(CAP)
    f["matching_gap"]= (float(np.mean(comp))-cap) if comp and cap is not None else None      # THE founding equation
    f["complexity_ratio"]= ratio_mean(p, [PRESS,SCAR,SPARK], CAP)
    # pairwise gaps between instruments
    for a,b in itertools.combinations(INSTR,2):
        f[f"gap_{a}_{b}"]=gap(a,b)
    # key theory ratios
    f["ratio_press_cap"]=ratio(PRESS,CAP)
    f["ratio_scar_cap"]=ratio(SCAR,CAP)
    f["ratio_spark_cap"]=ratio(SPARK,CAP)
    f["ratio_spark_turb"]=ratio(SPARK,TURB)     # spark density vs criticality (density/ripeness)
    f["ratio_press_scar"]=ratio(PRESS,SCAR)
    # imbalance / dispersion (the V2 Level-Equity idea, generalized across tiers)
    zs=[zz(i) for i in INSTR if zz(i) is not None]
    f["tier_dispersion"]= float(np.std(zs)) if len(zs)>=4 else None
    ps=[z.get(pi) for pi in PILLARS if z.get(pi) is not None]
    f["pillar_dispersion"]= float(np.std(ps)) if len(ps)>=4 else None
    # internal durability gap (P4-P1), MI's Safeguard J, normalized
    f["durability_gap"]= gap("P4","P1")
    # cross-tier rank discordance
    f["discord_press_cap"]= None if pp(PRESS) is None or pp(CAP) is None else abs(pp(PRESS)-pp(CAP))
    return f

def ratio_mean(p, num_list, den):
    nums=[p.get(x) for x in num_list if p.get(x) is not None]
    d=p.get(den)
    if not nums or d is None: return None
    return (float(np.mean(nums))+0.05)/(d+0.05)

def build_matrix(rows, feature_names, use):
    """use='rel' -> relational feats; 'add' -> raw instruments; 'both'; or a single feat name list."""
    X=[];C=[];Y=[];Gp=[]
    for r in rows:
        if use=="add":
            vec=[r["z"].get(i) for i in INSTR]
        elif use=="rel":
            fe=feat(r); vec=[fe.get(n) for n in feature_names]
        elif use=="both":
            fe=feat(r); vec=[r["z"].get(i) for i in INSTR]+[fe.get(n) for n in feature_names]
        else:  # single feature name
            fe=feat(r); vec=[fe.get(use)]
        if any(v is None for v in vec): continue
        X.append(vec); C.append([r["ctrl"],r["lgdp"]]); Y.append(r["y"]); Gp.append(r["grp"])
    return np.array(X,float),np.array(C,float),np.array(Y,float),np.array(Gp)

def auc(sc,y):
    pos=sc[y==1];neg=sc[y==0]
    return None if len(pos)==0 or len(neg)==0 else float(stats.mannwhitneyu(pos,neg,alternative="two-sided").statistic/(len(pos)*len(neg)))
def evalm(X,C,Y,G,kind):
    if len(X)==0: return None
    mtr=G!="TEST"; mte=G=="TEST"
    if mtr.sum()<40 or mte.sum()<25: return None
    if kind=="bin" and (Y[mtr].sum()<8 or Y[mte].sum()<6 or len(set(Y[mte]))<2): return None
    F=np.column_stack([C,X]); mu=F[mtr].mean(0); sd=F[mtr].std(0); sd[sd==0]=1
    Ftr=(F[mtr]-mu)/sd; Fte=(F[mte]-mu)/sd
    # base = controls only
    Cb=C; mub=Cb[mtr].mean(0); sdb=Cb[mtr].std(0); sdb[sdb==0]=1
    Cbtr=(Cb[mtr]-mub)/sdb; Cbte=(Cb[mte]-mub)/sdb
    if kind=="bin":
        b=S.logit_fit(Ftr,Y[mtr]); s=auc(S.logit_pred(Fte,b),Y[mte])
        bb=S.logit_fit(Cbtr,Y[mtr]); sb=auc(S.logit_pred(Cbte,Y[mte]) if False else S.logit_pred(Cbte,bb),Y[mte])
    else:
        b=CS.lpm_fit(Ftr,Y[mtr]); s=float(stats.spearmanr(CS.lpm_pred(Fte,b),Y[mte]).statistic)
        bb=CS.lpm_fit(Cbtr,Y[mtr]); sb=float(stats.spearmanr(CS.lpm_pred(Cbte,bb),Y[mte]).statistic)
    return {"skill":round(s,3),"base":round(sb,3),"delta":round(s-sb,3),"n_test":int(mte.sum()),
            "pos":int(Y[mte].sum()) if kind=="bin" else None}

TARGETS=[("libdem_backslide","libdem","libdem","bin"),
         ("electdem_backslide","electdem","electdem","bin"),
         ("conflict_onset_fwd","__onset__","prior_conflict_decayed","bin"),
         ("gdp_pc_growth_fwd","gdp_pc_growth","gdp_pc_growth","cont"),
         ("life_satisfaction_fwd","life_satisfaction","life_satisfaction","cont")]

RELNAMES=["matching_gap","complexity_ratio","ratio_press_cap","ratio_scar_cap","ratio_spark_cap",
          "ratio_spark_turb","ratio_press_scar","tier_dispersion","pillar_dispersion","durability_gap",
          "discord_press_cap"]+[f"gap_{a}_{b}" for a,b in itertools.combinations(INSTR,2)]

def run_main():
 report={}
 K=5
 print(f"RELATIONAL vs ADDITIVE (k={K}, sealed-TEST, incremental over AR+GDP)\n")
 print(f"{'outcome':>22} {'kind':>4} | {'ADD-6':>7} {'REL':>7} {'BOTH':>7} | {'matchgap_uni':>13} {'best_single_rel':>28}")
 print("-"*118)
 for name,raw,ctrl,kind in TARGETS:
    rows=normalize(assemble(name,raw,ctrl,kind,K))
    add=evalm(*build_matrix(rows,RELNAMES,"add"),kind)
    rel=evalm(*build_matrix(rows,RELNAMES,"rel"),kind)
    both=evalm(*build_matrix(rows,RELNAMES,"both"),kind)
    mg=evalm(*build_matrix(rows,RELNAMES,"matching_gap"),kind)
    singles={}
    for fn in RELNAMES:
        e=evalm(*build_matrix(rows,RELNAMES,fn),kind)
        if e: singles[fn]=e["skill"]
    bestrel=max(singles.items(),key=lambda kv:kv[1]) if singles else ("-",float("nan"))
    def g(e): return f"{e['skill']:.3f}" if e else "  -  "
    print(f"{name:>22} {kind:>4} | {g(add):>7} {g(rel):>7} {g(both):>7} | {g(mg):>13} {bestrel[0]+' '+format(bestrel[1],'.3f'):>28}")
    report[name]={"add":add,"rel":rel,"both":both,"matching_gap_uni":mg,"best_single_rel":{bestrel[0]:bestrel[1]},"rel_singles":singles}
 json.dump(report,open(HERE/"relational_results.json","w"),indent=1)
 print("\nNote: 'best_single_rel' scans each relational feature on TEST (optimistic; a scan, not a held-out pick).")
 print("The honest comparisons are ADD-6 vs REL vs BOTH vs matchgap_uni (all fixed a-priori designs).")

if __name__=="__main__":
    run_main()
