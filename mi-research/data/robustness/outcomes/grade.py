#!/usr/bin/env python3
"""Grade frozen temporal-holdout predictions vs real outcomes. Read-only w.r.t. scoring math."""
import csv, json, os, sys
from collections import defaultdict, Counter
import pycountry

HERE = os.path.dirname(os.path.abspath(__file__))
ROB = os.path.dirname(HERE)
MI_ROOT = os.path.dirname(os.path.dirname(ROB))  # mi-research/
sys.path.insert(0, MI_ROOT)
from lib.iso_map import GW_ISO_BASE as GW_ISO, CRAG_NAME_MANUAL  # noqa: E402
from lib import iso_map                                          # noqa: E402
import config                                                   # noqa: E402  (config/robustness.json)

# Analysis-layer config (config/robustness.json) — outcome/crisis defs + grading choices.
_OUT = config.robustness()["outcomes"]
_GRD = config.robustness()["grading"]
UCDP_END = _OUT["ucdp_data_end"]  # 2023 (UCDP v24.1 coverage end)

# ---------- load predictions ----------
def load_pred(f):
    return json.load(open(os.path.join(ROB, f)))

pred2004 = load_pred('temporal_2004_predictions.json')
pred2012 = load_pred('temporal_2012_predictions.json')

# ---------- GDP growth ----------
gdp_raw = json.load(open(os.path.join(HERE,'gdp_pcap_ppp_kd_raw.json')))
gdp = defaultdict(dict)  # iso -> year -> value
for r in gdp_raw:
    if r['value'] is not None and r['iso3'] and len(r['iso3'])==3:
        gdp[r['iso3']][r['year']] = r['value']

def gdp_growth(iso, y0, y1):
    a=gdp.get(iso,{}).get(y0); b=gdp.get(iso,{}).get(y1)
    if a is None or b is None or a<=0: return None
    return (b-a)/a

# ---------- UCDP onsets ----------
ucdp_rows = list(csv.DictReader(open(os.path.join(HERE,'ucdp','UcdpPrioConflict_v24_1.csv'),encoding='utf-8')))
# per gwno: conflict_id -> set of active years
gw_conf_years = defaultdict(lambda: defaultdict(set))
for r in ucdp_rows:
    y=int(r['year']); cid=r['conflict_id']
    for g in r['gwno_loc'].split(','):
        g=g.strip()
        if g.isdigit():
            gw_conf_years[int(g)][cid].add(y)
# onset years per gwno = year present but year-1 absent for that conflict_id
gw_onset_years = defaultdict(set)
for g, confs in gw_conf_years.items():
    for cid, ys in confs.items():
        for y in ys:
            if (y-1) not in ys:
                gw_onset_years[g].add(y)
# map to iso
iso_onset_years = defaultdict(set)
unmapped_gw = set()
for g, ys in gw_onset_years.items():
    iso = GW_ISO.get(g)
    if iso is None:
        unmapped_gw.add(g)
    else:
        iso_onset_years[iso] |= ys

def ucdp_onset(iso, y0, y1):  # any NEW onset with onset-year in [y0,y1]
    ys = iso_onset_years.get(iso,set())
    return any(y0 <= y <= y1 for y in ys)

# ---------- CRAG default onsets ----------
crag = json.load(open(os.path.join(HERE,'crag_long_parsed.json')))
crag_country_years = defaultdict(dict)  # country -> year -> total
for r in crag:
    crag_country_years[r['country']][r['year']] = r['total']
# map CRAG country name -> iso3
def name_to_iso(name):
    return iso_map.name_to_iso(name, CRAG_NAME_MANUAL)
crag_iso = {}
crag_unmapped = set()
for cname in crag_country_years:
    iso=name_to_iso(cname)
    if iso: crag_iso.setdefault(iso, cname)
    else: crag_unmapped.add(cname)

CRAG_CUTOFF = _OUT["crag_coverage_cutoff"]  # 2015 (2016 present but only 13 records -> incomplete)
def crag_default_onset(iso, y0, y1):
    cname = crag_iso.get(iso)
    if cname is None: return None  # no CRAG coverage for this iso
    ys = crag_country_years[cname]
    y1c = min(y1, CRAG_CUTOFF)
    hit=False
    for y in range(max(y0,min(ys) if ys else y0), y1c+1):
        cur=ys.get(y,0.0); prev=ys.get(y-1,0.0)
        if cur>0 and prev<=0:
            hit=True
    return hit

# ---------- metric helpers ----------
def confusion(y_true, y_pred):
    tp=sum(1 for t,p in zip(y_true,y_pred) if t and p)
    fp=sum(1 for t,p in zip(y_true,y_pred) if (not t) and p)
    fn=sum(1 for t,p in zip(y_true,y_pred) if t and (not p))
    tn=sum(1 for t,p in zip(y_true,y_pred) if (not t) and (not p))
    n=len(y_true); pos=tp+fn
    sens=tp/(tp+fn) if tp+fn else float('nan')
    spec=tn/(tn+fp) if tn+fp else float('nan')
    ppv=tp/(tp+fp) if tp+fp else float('nan')
    npv=tn/(tn+fn) if tn+fn else float('nan')
    acc=(tp+tn)/n if n else float('nan')
    return dict(TP=tp,FP=fp,FN=fn,TN=tn,N=n,pos=pos,base_rate=pos/n if n else float('nan'),
                sensitivity=sens,specificity=spec,PPV=ppv,NPV=npv,accuracy=acc)

def auc_roc(scores, labels):
    # Mann-Whitney U based AUC (handles ties)
    pos=[s for s,l in zip(scores,labels) if l]
    neg=[s for s,l in zip(scores,labels) if not l]
    if not pos or not neg: return float('nan')
    # rank all
    allv=sorted(scores)
    from bisect import bisect_left,bisect_right
    # average-rank
    order=sorted(range(len(scores)), key=lambda i:scores[i])
    ranks=[0.0]*len(scores)
    i=0
    while i<len(scores):
        j=i
        while j+1<len(scores) and scores[order[j+1]]==scores[order[i]]: j+=1
        avg=(i+j)/2.0+1
        for k in range(i,j+1): ranks[order[k]]=avg
        i=j+1
    sumpos=sum(ranks[i] for i in range(len(scores)) if labels[i])
    npos=len(pos); nneg=len(neg)
    auc=(sumpos - npos*(npos+1)/2)/(npos*nneg)
    return auc

def threshold_sweep(scores, labels):
    out=[]
    for score in _GRD["vuln_threshold_sweep_scores"]:  # score>=1,>=2,>=3
        thr=score-0.5
        yp=[s>=thr for s in scores]
        cm=confusion(labels, yp)
        out.append(dict(threshold=f"score>={score}", **cm))
    return out

# ---------- run one window ----------
# ---------- FSI (Fragile States Index) for FSI-only baseline (available 2012+) ----------
FSI = defaultdict(dict)
try:
    for r in csv.DictReader(open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE)))),'mi-pipeline','data','fsi.csv'))):
        FSI[r['iso3']][int(r['year'])] = float(r['FSI'])
except Exception as e:
    print('FSI load failed', e)

def run_window(pred, base_year, out_year, ucdp_start, label):
    recs = pred['predictions']
    rows=[]
    dropped_gdp=[]
    for p in recs:
        iso=p['iso']
        g=gdp_growth(iso, base_year, out_year)
        ucdp=ucdp_onset(iso, ucdp_start, UCDP_END)
        crag_ev=crag_default_onset(iso, ucdp_start, out_year)  # None if no coverage
        crag_bool = bool(crag_ev) if crag_ev is not None else False
        crisis = bool(ucdp) or crag_bool
        rows.append(dict(iso=iso, country=p['country'], mi_score=p.get('mi_score'), growth=g,
                         vuln=p['predictions']['vulnerability_score_0_3'],
                         elevated=p['predictions']['elevated_crisis_vulnerability'],
                         trajectory=p['predictions']['trajectory'],
                         P1=p['P1'], P4=p['P4'],
                         ucdp=bool(ucdp), crag=crag_bool, crag_cov=(crag_ev is not None),
                         crisis=crisis))
        if g is None: dropped_gdp.append(iso)

    # ---- Trajectory vs growth ----
    gr = [r for r in rows if r['growth'] is not None]
    med = sorted(x['growth'] for x in gr)[len(gr)//2] if gr else None
    # improve = growth above median
    traj_rows=[r for r in gr if r['trajectory'] in ('sustain_or_improve','stress')]
    def improved(r): return r['growth'] > med
    traj_correct=sum(1 for r in traj_rows if (r['trajectory']=='sustain_or_improve' and improved(r))
                                          or (r['trajectory']=='stress' and not improved(r)))
    traj_acc = traj_correct/len(traj_rows) if traj_rows else float('nan')
    # base rate of "improve" among traj_rows
    improve_base = sum(1 for r in traj_rows if improved(r))/len(traj_rows) if traj_rows else float('nan')
    # majority-class baseline for trajectory (predict everyone improves OR everyone declines)
    maj_traj = max(improve_base, 1-improve_base)

    # ---- Crisis prediction (vuln score) ----
    labels=[r['crisis'] for r in rows]
    scores=[r['vuln'] for r in rows]
    N=len(rows); pos=sum(labels); base=pos/N
    maj_base=max(base,1-base)
    # binary predictor from elevated flag
    cm_elev=confusion(labels,[r['elevated'] for r in rows])
    # binary from vuln>=2 (the "elevated" default in engine likely == vuln>=2); report sweep
    sweep=threshold_sweep(scores,labels)
    auc=auc_roc(scores,labels)
    # PPV lift over base rate for elevated flag
    lift_elev = (cm_elev['PPV']/base) if base>0 else float('nan')

    # separate UCDP / CRAG
    ucdp_pos=sum(1 for r in rows if r['ucdp'])
    crag_cov_rows=[r for r in rows if r['crag_cov']]
    crag_pos=sum(1 for r in rows if r['crag'])

    # ---- Design C: crisis quartile ----
    # top-quartile vulnerability by vuln score. vuln is 0-3; take top 25% by score rank.
    srt=sorted(rows, key=lambda r:r['vuln'], reverse=True)
    q=max(1,round(N*_GRD["top_quartile_frac"]))
    # handle ties at boundary: include all with vuln >= threshold value at rank q
    thr_val=srt[q-1]['vuln']
    topq=[r for r in rows if r['vuln']>=thr_val]
    crisis_in_topq=sum(1 for r in topq if r['crisis'])
    frac_topq_crisis = crisis_in_topq/len(topq) if topq else float('nan')
    crisis_rows=[r for r in rows if r['crisis']]
    topq_iso=set(r['iso'] for r in topq)
    frac_crisis_topq = sum(1 for r in crisis_rows if r['iso'] in topq_iso)/len(crisis_rows) if crisis_rows else float('nan')

    # ---- Baselines: GDP-per-capita base-year (poorer=>crisis) ----
    # rank by base-year gdp; predict crisis for bottom quartile (poorest)
    gdp_rows=[r for r in rows if gdp.get(r['iso'],{}).get(base_year) is not None]
    gdp_vals={r['iso']:gdp[r['iso']][base_year] for r in gdp_rows}
    # AUC of "poverty score" = -gdp predicting crisis
    gdp_labels=[r['crisis'] for r in gdp_rows]
    gdp_pov_scores=[-gdp_vals[r['iso']] for r in gdp_rows]
    gdp_auc=auc_roc(gdp_pov_scores, gdp_labels)
    # bottom-quartile-poorest as crisis predictor
    poor_sorted=sorted(gdp_rows, key=lambda r:gdp_vals[r['iso']])
    qq=max(1,round(len(gdp_rows)*_GRD["top_quartile_frac"]))
    poorest=set(r['iso'] for r in poor_sorted[:qq])
    gdp_pred=[r['iso'] in poorest for r in gdp_rows]
    cm_gdp=confusion(gdp_labels, gdp_pred)

    # ---- FSI-only baseline (higher FSI = more fragile => crisis); only if base_year FSI exists ----
    fsi_baseline=None
    fsi_rows=[r for r in rows if FSI.get(r['iso'],{}).get(base_year) is not None]
    if fsi_rows:
        fsi_vals={r['iso']:FSI[r['iso']][base_year] for r in fsi_rows}
        fsi_labels=[r['crisis'] for r in fsi_rows]
        fsi_auc=auc_roc([fsi_vals[r['iso']] for r in fsi_rows], fsi_labels)
        fsi_sorted=sorted(fsi_rows, key=lambda r:fsi_vals[r['iso']], reverse=True)  # most fragile first
        qf=max(1,round(len(fsi_rows)*_GRD["top_quartile_frac"]))
        frag=set(r['iso'] for r in fsi_sorted[:qf])
        cm_fsi=confusion(fsi_labels,[r['iso'] in frag for r in fsi_rows])
        fsi_baseline=dict(n=len(fsi_rows), auc=fsi_auc, top_quartile_fragile_confusion=cm_fsi)

    # correctly flagged vs missed (by elevated flag)
    flagged_correct=[r['iso'] for r in rows if r['elevated'] and r['crisis']]
    missed=[r['iso'] for r in rows if (not r['elevated']) and r['crisis']]
    false_alarms=[r['iso'] for r in rows if r['elevated'] and (not r['crisis'])]

    return dict(
        label=label, base_year=base_year, out_year=out_year, N=N,
        ucdp_window=[ucdp_start,UCDP_END], crag_window=[ucdp_start,min(out_year,CRAG_CUTOFF)],
        dropped_gdp_iso=dropped_gdp,
        trajectory=dict(n=len(traj_rows), growth_median=med, accuracy=traj_acc,
                        improve_base_rate=improve_base, majority_baseline=maj_traj,
                        lift=traj_acc/maj_traj if maj_traj else float('nan')),
        crisis=dict(base_rate=base, n_pos=pos, N=N, majority_baseline=maj_base,
                    ucdp_pos=ucdp_pos, crag_pos=crag_pos, crag_covered_n=len(crag_cov_rows),
                    elevated_flag_confusion=cm_elev, elevated_lift_over_baserate=lift_elev,
                    vuln_threshold_sweep=sweep, auc_roc=auc),
        design_C=dict(topq_n=len(topq), topq_vuln_threshold=thr_val,
                      frac_topq_with_crisis=frac_topq_crisis,
                      frac_crisis_in_topq=frac_crisis_topq,
                      n_crisis=len(crisis_rows)),
        baselines=dict(majority_class=maj_base,
                       gdp_poorest_quartile_confusion=cm_gdp,
                       gdp_poverty_auc=gdp_auc,
                       fsi_only=fsi_baseline),
        countries=dict(flagged_correct=sorted(flagged_correct),
                       missed_crises=sorted(missed),
                       false_alarms_n=len(false_alarms),
                       crisis_countries=sorted(r['iso'] for r in crisis_rows)),
        _rows=rows,
    )

_W = _OUT["windows"]
W2004 = run_window(pred2004, _W["2004"]["base"], _W["2004"]["out"], _W["2004"]["base"], "2004->2024")
W2012 = run_window(pred2012, _W["2012"]["base"], _W["2012"]["out"], _W["2012"]["base"], "2012->2024")

# Persist the joined per-country holdout panel (the table grade.py builds then otherwise
# discards). One row per country per window; the single source ESI + forensics read from.
holdout_panel=dict(
    generated="temporal holdout joined per-country panel (Plan 2)",
    note=("one row per country per window; fields: iso, country, mi_score, P1, P4, "
          "vuln(0-3), elevated(J-gate flag), ucdp(onset), crag(default), crag_cov, "
          "crisis(=ucdp OR crag), growth, trajectory"),
    crisis_definition=_OUT["crisis_definition"],
    windows={"2004": W2004["_rows"], "2012": W2012["_rows"]},
)
json.dump(holdout_panel, open(os.path.join(ROB,'temporal_holdout_panel.json'),'w'), indent=1, default=str)

report=dict(
    generated="temporal holdout grading (Plan 2)",
    sources=dict(gdp="World Bank NY.GDP.PCAP.PP.KD (constant PPP)",
                 conflict="UCDP/PRIO ACD v24.1 (coverage 1946-2023; 2024 unavailable)",
                 default="Bank of Canada CRAG 2017 update (coverage ->2016; effective cutoff 2015)"),
    crag_coverage_cutoff=CRAG_CUTOFF,
    ucdp_unmapped_gw_codes=sorted(unmapped_gw),
    crag_unmapped_countries=sorted(crag_unmapped),
    window_2004=  {k:v for k,v in W2004.items() if k!='_rows'},
    window_2012=  {k:v for k,v in W2012.items() if k!='_rows'},
)
json.dump(report, open(os.path.join(ROB,'temporal_grade_report.json'),'w'), indent=1, default=str)

# ---- console summary ----
for W in (W2004,W2012):
    print("\n==============",W['label'],"N=",W['N'],"==============")
    c=W['crisis']
    print(f"CRISIS base rate {c['base_rate']:.3f} ({c['n_pos']}/{c['N']}) | UCDP+={c['ucdp_pos']} CRAG+={c['crag_pos']} (CRAG covered {c['crag_covered_n']})")
    print(f"  majority baseline acc={c['majority_baseline']:.3f}  AUC(vuln 0-3)={c['auc_roc']:.3f}")
    ce=c['elevated_flag_confusion']
    print(f"  elevated-flag: TP{ce['TP']} FP{ce['FP']} FN{ce['FN']} TN{ce['TN']} | sens={ce['sensitivity']:.2f} spec={ce['specificity']:.2f} PPV={ce['PPV']:.2f} NPV={ce['NPV']:.2f} acc={ce['accuracy']:.2f}")
    print(f"  elevated PPV lift over base rate = {c['elevated_lift_over_baserate']:.2f}x")
    for s in c['vuln_threshold_sweep']:
        print(f"    {s['threshold']}: sens={s['sensitivity']:.2f} spec={s['specificity']:.2f} PPV={s['PPV']:.2f} acc={s['accuracy']:.2f} (TP{s['TP']}/FP{s['FP']}/FN{s['FN']}/TN{s['TN']})")
    t=W['trajectory']
    print(f"TRAJECTORY(n={t['n']}): acc={t['accuracy']:.3f} vs majority {t['majority_baseline']:.3f} (lift {t['lift']:.2f}x); improve base {t['improve_base_rate']:.3f}; growth median {t['growth_median']:.3f}")
    d=W['design_C']
    print(f"DESIGN C: top-quartile(n={d['topq_n']},vuln>={d['topq_vuln_threshold']}): {d['frac_topq_with_crisis']:.2f} had crisis; {d['frac_crisis_in_topq']:.2f} of {d['n_crisis']} crises were top-quartile")
    b=W['baselines']
    cg=b['gdp_poorest_quartile_confusion']
    print(f"BASELINE GDP-poorest-quartile: sens={cg['sensitivity']:.2f} spec={cg['specificity']:.2f} PPV={cg['PPV']:.2f} acc={cg['accuracy']:.2f}; GDP-poverty AUC={b['gdp_poverty_auc']:.3f}")
    if b['fsi_only']:
        f=b['fsi_only']; cf=f['top_quartile_fragile_confusion']
        print(f"BASELINE FSI-only(n={f['n']}): AUC={f['auc']:.3f}; top-quartile-fragile sens={cf['sensitivity']:.2f} spec={cf['specificity']:.2f} PPV={cf['PPV']:.2f} acc={cf['accuracy']:.2f}")
    else:
        print(f"BASELINE FSI-only: unavailable (FSI series starts 2012; no {W['base_year']} data)")
    print(f"  MISSED crises (elevated=F, crisis=T): {W['countries']['missed_crises']}")
print("\nunmapped GW codes:",sorted(unmapped_gw))
print("report written")
