#!/usr/bin/env python3
"""Predict-forward discovery screen (Phase 1) + confirmation (Phase 2).

Design (encodes the audit's lessons):
  * COHORT CROSS-SECTIONS, not pooled country-years -> no pseudoreplication (H1).
    base grid b in {1996,2000,2004,2008,2012,2016}; each (b,lead k) is ONE row/country.
  * DISCOVERY/CONFIRMATION country split (hash iso). Discover on half A, confirm on half B.
  * GDPpc always PARTIALLED (partial-Spearman on rank residuals).
  * BH-FDR across the whole discovery family.
  * A cell (predictor,outcome,k) is a DISCOVERY hit only if: FDR-sig on combined-cohort p
    AND sign-stable across cohorts (>=70% same sign, >=2 cohorts).
  * Confirmation = same stat on half B, one-sided in the discovered direction, p<.05.
Read-only w.r.t. the repo; writes only under sandbox/tier_stress/."""
import json, sys, math, hashlib
from pathlib import Path
import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
MIROOT = Path("/Users/rubensanchez/Developer/usg-sandbox-wt/mi-research")

PRED = json.load(open(HERE/"predictors.json"))
OUTC = json.load(open(HERE/"outcomes.json"))
# GDPpc for partialling (read-only from repo source)
V2IND = json.load(open(MIROOT/"data/v2/v2_indicators.json"))["series"]
GDPPC = V2IND.get("gdp_pc_ppp", {})
# conflict onset years per iso (top-level in outcomes.json per spec)
ONSETS = {k: set(v) for k, v in OUTC.get("conflict_onsets_by_iso", {}).items()} if isinstance(OUTC, dict) else {}

BASES = [1996, 2000, 2004, 2008, 2012, 2016]
LEADS = [1, 3, 5, 10]
NMIN = 25            # min countries in a cohort cross-section
SIGN_STABLE = 0.70   # fraction of cohorts that must share the effect sign

def half(iso):
    """deterministic discovery(A)/confirmation(B) country split."""
    h = int(hashlib.sha256(iso.encode()).hexdigest(), 16)
    return "A" if h % 2 == 0 else "B"

def gv(d, iso, year):
    s = d.get(iso) if isinstance(d, dict) else None
    if not s: return None
    return s.get(str(year), s.get(year))

def gdppc(iso, year):
    v = gv(GDPPC, iso, year)
    try: return math.log10(float(v)) if v and float(v) > 0 else None
    except Exception: return None

# ---- discover predictor fields dynamically (numeric, present) ----
def predictor_fields():
    fields = {}
    for iso, byyr in PRED.items():
        if not isinstance(byyr, dict): continue
        for yr, rec in byyr.items():
            if not isinstance(rec, dict): continue
            for k, v in rec.items():
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    fields[k] = fields.get(k, 0) + 1
    return sorted(fields, key=lambda k: -fields[k])

PFIELDS = predictor_fields()

# ---- outcome constructors: (name, kind, fn(iso,b,k)->value) ----
ECON_LEVEL = ["life_satisfaction", "gross_savings", "fdi_in", "unemployment",
              "fertility", "net_migration", "patents", "tourism_receipts",
              "brain_health_ratio", "inflation", "gdp_pc_growth", "gov_debt_chg"]
REGIME = ["libdem", "electdem", "rol_vdem"]

def oget(iso, year, field):
    rec = OUTC.get(iso, {})
    if not isinstance(rec, dict): return None
    yr = rec.get(str(year), rec.get(year))
    if not isinstance(yr, dict): return None
    return yr.get(field)

def build_outcomes():
    outs = []
    # regime: forward level, forward change, backslide/democratize binaries
    for f in REGIME:
        outs.append((f"{f}_level", "cont", lambda iso,b,k,f=f: oget(iso,b+k,f)))
        outs.append((f"{f}_chg",   "cont", lambda iso,b,k,f=f: (oget(iso,b+k,f)-oget(iso,b,f)) if oget(iso,b+k,f) is not None and oget(iso,b,f) is not None else None))
    # backsliding / democratization on libdem+electdem
    for f in ["libdem", "electdem"]:
        def _bs(iso,b,k,f=f):
            a,c = oget(iso,b,f), oget(iso,b+k,f)
            return None if a is None or c is None else (1 if (c-a)<=-0.05 else 0)
        def _dm(iso,b,k,f=f):
            a,c = oget(iso,b,f), oget(iso,b+k,f)
            return None if a is None or c is None else (1 if (c-a)>= 0.05 else 0)
        outs.append((f"{f}_backslide", "bin", _bs))
        outs.append((f"{f}_democratize", "bin", _dm))
    # econ/wellbeing forward levels + forward change
    for f in ECON_LEVEL:
        outs.append((f"{f}_fwd", "cont", lambda iso,b,k,f=f: oget(iso,b+k,f)))
    # gdp growth volatility + max drawdown over the forward window
    def _gvol(iso,b,k):
        v=[oget(iso,y,"gdp_pc_growth") for y in range(b+1,b+k+1)]; v=[x for x in v if x is not None]
        return float(np.std(v)) if len(v)>=max(3,k//2) else None
    outs.append(("gdp_growth_vol_fwd","cont",_gvol))
    def _infvol(iso,b,k):
        v=[oget(iso,y,"inflation") for y in range(b+1,b+k+1)]; v=[x for x in v if x is not None]
        return float(np.std(v)) if len(v)>=max(3,k//2) else None
    outs.append(("inflation_vol_fwd","cont",_infvol))
    # conflict onset within forward window
    def _onset(iso,b,k):
        ons=ONSETS.get(iso)
        if ons is None: return None
        return 1 if any(b < y <= b+k for y in ons) else 0
    outs.append(("conflict_onset_fwd","bin",_onset))
    return outs

OUTCOMES = build_outcomes()

def partial_spearman(x, y, z):
    """Spearman(x,y | z) via rank residuals; returns (rho, p, n)."""
    x=np.asarray(x,float); y=np.asarray(y,float); z=np.asarray(z,float)
    rx,ry,rz = stats.rankdata(x), stats.rankdata(y), stats.rankdata(z)
    Z=np.column_stack([np.ones(len(x)), rz])
    bx,_,_,_=np.linalg.lstsq(Z,rx,rcond=None); by,_,_,_=np.linalg.lstsq(Z,ry,rcond=None)
    ex,ey = rx-Z@bx, ry-Z@by
    pr=stats.pearsonr(ex,ey)
    return float(pr.statistic), float(pr.pvalue), len(x)

def rank_auc(pred, y):
    """AUC of continuous pred vs binary y (Mann-Whitney)."""
    y=np.asarray(y); pred=np.asarray(pred,float)
    pos=pred[y==1]; neg=pred[y==0]
    if len(pos)==0 or len(neg)==0: return None
    u=stats.mannwhitneyu(pos,neg,alternative="two-sided").statistic
    return float(u/(len(pos)*len(neg)))

def cohort_stat(P, oc, k, b, iso_set):
    """one cohort cross-section. returns dict or None."""
    name, kind, fn = oc
    rows=[]
    for iso in iso_set:
        pv = (PRED.get(iso,{}) or {}).get(str(b), (PRED.get(iso,{}) or {}).get(b))
        if not isinstance(pv, dict): continue
        x = pv.get(P)
        if x is None or not isinstance(x,(int,float)): continue
        yv = fn(iso, b, k)
        if yv is None: continue
        g = gdppc(iso, b)
        if g is None: continue
        rows.append((float(x), float(yv), g))
    if len(rows) < NMIN: return None
    x=[r[0] for r in rows]; y=[r[1] for r in rows]; z=[r[2] for r in rows]
    if kind=="bin" and len(set(y))<2: return None
    if len(set(x))<3: return None
    rho,p,n = partial_spearman(x,y,z)
    res={"b":b,"n":n,"partial_rho":round(rho,4),"p":p}
    if kind=="bin":
        res["auc"]=round(rank_auc(x,y),4) if rank_auc(x,y) is not None else None
        res["n_pos"]=int(sum(y))
    return res

def combined(cohorts):
    """Stouffer-combine cohort partial-p (two-sided) with sign; require sign stability."""
    if not cohorts: return None
    signs=[np.sign(c["partial_rho"]) for c in cohorts if c["partial_rho"]!=0]
    if not signs: return None
    dom=1 if sum(s>0 for s in signs)>=sum(s<0 for s in signs) else -1
    frac=sum(s==dom for s in signs)/len(signs)
    # Stouffer Z on one-sided p in the dominant direction
    zs=[]
    for c in cohorts:
        pp=max(min(c["p"],1-1e-9),1e-9)
        z=stats.norm.isf(pp/2)*np.sign(c["partial_rho"])
        zs.append(z*dom)  # align to dominant dir
    Z=sum(zs)/math.sqrt(len(zs))
    p_comb=float(stats.norm.sf(Z))  # one-sided in dominant dir
    return {"n_cohorts":len(cohorts),"dir":int(dom),"sign_frac":round(frac,3),
            "mean_rho":round(float(np.mean([c['partial_rho'] for c in cohorts])),4),
            "p_combined":p_comb,"cohorts":cohorts}

def run_family(iso_set):
    """screen every (P,outcome,k) over cohorts for the given country set."""
    cells=[]
    for P in PFIELDS:
        for oc in OUTCOMES:
            for k in LEADS:
                cohorts=[]
                for b in BASES:
                    if b+k>2025: continue
                    r=cohort_stat(P, oc, k, b, iso_set)
                    if r: cohorts.append(r)
                comb=combined(cohorts)
                if comb and comb["n_cohorts"]>=2:
                    cells.append({"pred":P,"out":oc[0],"kind":oc[1],"k":k, **comb})
    return cells

def bh_fdr(cells, key="p_combined", q=0.05):
    m=len(cells); order=sorted(range(m), key=lambda i:cells[i][key]); crit=None
    for rank,i in enumerate(order,1):
        if cells[i][key] <= rank/m*q: crit=cells[i][key]
    for c in cells: c["fdr_sig"]=bool(crit and c[key]<=crit)
    return crit

if __name__=="__main__":
    isos_all=sorted((set(PRED)|set(OUTC.keys()))-{"conflict_onsets_by_iso"})
    A={i for i in isos_all if half(i)=="A"}
    B={i for i in isos_all if half(i)=="B"}
    print(f"predictor fields ({len(PFIELDS)}): {PFIELDS}")
    print(f"outcome vars ({len(OUTCOMES)}): {[o[0] for o in OUTCOMES]}")
    print(f"discovery isos(A)={len(A)}  confirmation isos(B)={len(B)}\n")

    # ---- PHASE 1: discovery on A ----
    disc=run_family(A)
    crit=bh_fdr(disc)
    hits=[c for c in disc if c["fdr_sig"] and c["sign_frac"]>=SIGN_STABLE]
    hits.sort(key=lambda c:c["p_combined"])
    print(f"PHASE 1 discovery: {len(disc)} cells tested, BH-FDR crit p<={crit}, "
          f"{sum(c['fdr_sig'] for c in disc)} FDR-sig, {len(hits)} sign-stable hits\n")

    # ---- PHASE 2: confirm hits on B ----
    confirmed=[]
    for h in hits:
        oc=next(o for o in OUTCOMES if o[0]==h["out"])
        cohorts=[]
        for b in BASES:
            if b+h["k"]>2025: continue
            r=cohort_stat(h["pred"], oc, h["k"], b, B)
            if r: cohorts.append(r)
        cb=combined(cohorts)
        rec={**h, "confirm": cb}
        if cb and cb["n_cohorts"]>=2 and cb["dir"]==h["dir"] and cb["p_combined"]<0.05 and cb["sign_frac"]>=SIGN_STABLE:
            rec["CONFIRMED"]=True; confirmed.append(rec)
        else:
            rec["CONFIRMED"]=False
    confirmed.sort(key=lambda c:(c["out"], c["pred"], c["k"]))

    json.dump({"discovery_all":disc,"discovery_hits":hits}, open(HERE/"screen_discovery.json","w"), indent=1)
    json.dump({"n_confirmed":len(confirmed),"confirmed":confirmed,
               "hits_tested":[{k:h[k] for k in ('pred','out','k','dir','mean_rho','p_combined','sign_frac')} for h in hits]},
              open(HERE/"screen_confirmed.json","w"), indent=1)

    print(f"PHASE 2 confirmation on sealed half B: {len(confirmed)}/{len(hits)} hits confirmed\n")
    print(f"{'predictor':>22} {'outcome':>24} {'k':>3} {'dir':>4} {'rhoA':>7} {'pA':>9} {'rhoB':>7} {'pB':>9}")
    print("-"*95)
    for c in confirmed:
        cb=c["confirm"]
        print(f"{c['pred']:>22} {c['out']:>24} {c['k']:>3} {c['dir']:>+4} {c['mean_rho']:>+7.3f} {c['p_combined']:>9.1e} "
              f"{cb['mean_rho']:>+7.3f} {cb['p_combined']:>9.1e}")
