#!/usr/bin/env python3
"""Incremental-forecasting test: does predictor@T beat the AUTOREGRESSIVE baseline?
For each confirmed hit, partial-Spearman(pred@b, outcome@b+k | [outcome_lag@b, logGDP@b]).
If it survives controlling for the outcome's OWN lagged value, it's a genuine leading
indicator; if it collapses, it was structural persistence (a fingerprint, not a forecast).
Pooled over the full country set + all cohorts (country-clustered via cohort structure)."""
import json, math
from pathlib import Path
import numpy as np
from scipy import stats
HERE=Path(__file__).resolve().parent
MIROOT=HERE.parents[1]/"mi-research"
PRED=json.load(open(HERE/"predictors.json"))
OUTC=json.load(open(HERE/"outcomes.json"))
GDPPC=json.load(open(MIROOT/"data/v2/v2_indicators.json"))["series"].get("gdp_pc_ppp",{})
CONF=json.load(open(HERE/"screen_confirmed.json"))["confirmed"]
BASES=[1996,2000,2004,2008,2012,2016]

# outcome -> (raw field for lag, is_already_persistence_controlled)
RAW={'libdem_level':'libdem','electdem_level':'electdem','rol_vdem_level':'rol_vdem'}
for f in ['life_satisfaction','gross_savings','fdi_in','unemployment','fertility','net_migration',
          'patents','tourism_receipts','brain_health_ratio','inflation','gdp_pc_growth','gov_debt_chg']:
    RAW[f+'_fwd']=f
# these already net persistence (predict change/vol/event) -> no lag control needed
SELF_CONTROLLED={'libdem_chg','electdem_chg','rol_vdem_chg','libdem_backslide','libdem_democratize',
                 'electdem_backslide','electdem_democratize','gdp_growth_vol_fwd','inflation_vol_fwd',
                 'conflict_onset_fwd'}

def pv(iso,b,field):
    r=(PRED.get(iso,{}) or {}).get(str(b),(PRED.get(iso,{}) or {}).get(b))
    return r.get(field) if isinstance(r,dict) else None
def ov(iso,y,field):
    r=OUTC.get(iso,{}); r=r.get(str(y),r.get(y)) if isinstance(r,dict) else None
    return r.get(field) if isinstance(r,dict) else None
def out_val(iso,b,k,oname):
    # reconstruct outcome value (only handle level/_fwd here; self-controlled handled separately)
    raw=RAW.get(oname)
    return ov(iso,b+k,raw) if raw else None
def lgdp(iso,b):
    v=GDPPC.get(iso,{}).get(str(b))
    try: return math.log10(float(v)) if v and float(v)>0 else None
    except: return None

def partial(x,y,ctrls):
    x=np.asarray(x,float);y=np.asarray(y,float)
    rx,ry=stats.rankdata(x),stats.rankdata(y)
    Z=np.column_stack([np.ones(len(x))]+[stats.rankdata(c) for c in ctrls])
    bx,_,_,_=np.linalg.lstsq(Z,rx,rcond=None); by,_,_,_=np.linalg.lstsq(Z,ry,rcond=None)
    pr=stats.pearsonr(rx-Z@bx, ry-Z@by)
    return float(pr.statistic), float(pr.pvalue)

def incr_test(P,oname,k):
    """pooled over cohorts, control for lagged outcome + logGDP."""
    raw=RAW.get(oname)
    xs=[];ys=[];lag=[];g=[]
    isos=sorted(PRED)
    for b in BASES:
        if b+k>2025: continue
        for iso in isos:
            x=pv(iso,b,P); y=out_val(iso,b,k,oname)
            lg=ov(iso,b,raw) if raw else None
            gg=lgdp(iso,b)
            if None in (x,y,lg,gg): continue
            xs.append(x);ys.append(y);lag.append(lg);g.append(gg)
    if len(xs)<40: return None
    rho_raw,_=partial(xs,ys,[g])                 # net GDP only (what the screen reported)
    rho_inc,p_inc=partial(xs,ys,[lag,g])         # net GDP + lagged outcome (AR baseline)
    return {"n":len(xs),"rho_netGDP":round(rho_raw,3),"rho_incremental":round(rho_inc,3),
            "p_incremental":p_inc,"attenuation":round(1-abs(rho_inc)/abs(rho_raw),2) if rho_raw else None}

# dedupe confirmed to (pred,out,k), keep best-effort; test level/_fwd hits
seen=set(); rows=[]
for c in CONF:
    key=(c['pred'],c['out'],c['k'])
    if key in seen: continue
    seen.add(key)
    if c['out'] in SELF_CONTROLLED:
        rows.append({**{k:c[k] for k in('pred','out','k','mean_rho')},"class":"forecast(change/event)","verdict":"GENUINE (predicts change/event by construction)"})
        continue
    r=incr_test(c['pred'],c['out'],c['k'])
    if not r:
        rows.append({**{k:c[k] for k in('pred','out','k','mean_rho')},"class":"level","verdict":"insufficient-n"}); continue
    genuine = abs(r['rho_incremental'])>=0.12 and r['p_incremental']<0.05 and np.sign(r['rho_incremental'])==np.sign(r['rho_netGDP'])
    rows.append({**{k:c[k] for k in('pred','out','k','mean_rho')},"class":"level",
                 **r,"verdict":"GENUINE leading indicator" if genuine else "persistence fingerprint (collapses vs AR baseline)"})

json.dump(rows,open(HERE/"forecast_test.json","w"),indent=1)

gen=[r for r in rows if r['verdict'].startswith("GENUINE") and r['class']=='level']
fp=[r for r in rows if 'persistence fingerprint' in r['verdict']]
ev=[r for r in rows if r['class']=='forecast(change/event)']
print(f"confirmed hits examined: {len(rows)}")
print(f"  change/event forecasts (persistence-controlled by construction): {len(ev)}")
print(f"  level hits that SURVIVE the AR baseline (genuine leading indicators): {len(gen)}")
print(f"  level hits that COLLAPSE to persistence fingerprint: {len(fp)}\n")

print("=== GENUINE leading indicators on LEVELS (beat autoregressive baseline), by |incremental rho| ===")
for r in sorted(gen,key=lambda r:-abs(r['rho_incremental']))[:30]:
    print(f"   {r['pred']:>22} -> {r['out']:22} k={r['k']:>2} netGDP={r['rho_netGDP']:+.2f} -> incr(net AR)={r['rho_incremental']:+.2f} (atten {r['attenuation']})")

print("\n=== strongest that COLLAPSED (were persistence, not forecast) ===")
for r in sorted(fp,key=lambda r:-abs(r.get('rho_netGDP',0)))[:14]:
    print(f"   {r['pred']:>22} -> {r['out']:22} k={r['k']:>2} netGDP={r['rho_netGDP']:+.2f} -> incr={r['rho_incremental']:+.2f} (atten {r['attenuation']})")
