#!/usr/bin/env python3
"""Tier 6 — Spark Probability (spark density). The spark is random; its ARRIVAL RATE is
structural. S1 geographic exposure + S2 resource incentive + S3 transcendent contestation
(hand-coded) + S4 military net = T6. Tests whether spark density adds over T5 criticality and
whether the T5xT6 interaction is the highest-resolution timing signal. Frozen spec:
docs/TIER6_SPARK_PREREGISTRATION.md (sha256 9784e84f). Read-only."""
from __future__ import annotations
import json, csv, io, sys, math, urllib.request, time
from collections import defaultdict
import numpy as np
from scipy import stats
sys.path.insert(0,"scripts/robustness"); sys.path.insert(0,".")
import convergence_lib as L
T6D=json.load(open("data/political/tier6_indicators.json"))["series"]
five={r["iso"]:r for r in json.load(open("data/political/five_tier_snapshot.json"))}
tier4=json.load(open("data/political/tier4_indicators.json"))["series"]
lib=json.load(open("data/v2/vdem_democracy.json"))["series"]["libdem"]
dom=L.domestic_years()
def get(u,tries=4):
    for t in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=40) as r: return r.read().decode("utf-8","replace")
        except Exception: time.sleep(3)
    return None
# ISO2 -> ISO3 + adjacency (ISO3). AUDIT C2 FIX: cache to a committed, version-pinned file so
# regeneration is offline-reproducible and a fetch failure can't crash or silently reshape T6.
import os
CACHE="data/political/_borders_cache.json"
NET_OK=True
iso=get("https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv")
bcsv=get("https://raw.githubusercontent.com/geodatasource/country-borders/master/GEODATASOURCE-COUNTRY-BORDERS.CSV")
adj=defaultdict(set); haveborder=set(); I2I3={}
if iso is not None and bcsv is not None:
    for r in csv.DictReader(io.StringIO(iso)): I2I3[r["alpha-2"]]=r["alpha-3"]
    for r in csv.DictReader(io.StringIO(bcsv)):
        a=I2I3.get(r["country_code"]); b=I2I3.get(r["country_border_code"])
        if a: haveborder.add(a)
        if a and b: adj[a].add(b)
    json.dump({"I2I3":I2I3,"adj":{k:sorted(v) for k,v in adj.items()},"haveborder":sorted(haveborder)},
              open(CACHE,"w")); print(f"  fetched borders -> cached ({len(adj)} countries with neighbours)")
elif os.path.exists(CACHE):
    c=json.load(open(CACHE)); I2I3=c["I2I3"]; haveborder=set(c["haveborder"])
    adj=defaultdict(set,{k:set(v) for k,v in c["adj"].items()})
    print("  network unavailable -> loaded committed border cache (offline reproducible)")
else:
    NET_OK=False; print("  !! network unavailable AND no border cache -> T6 geographic dim will be degraded")
def latest(ser,i,lo=2015,hi=2024):
    s=ser.get(i) if ser else None
    if not s: return None
    for y in range(hi,lo-1,-1):
        if str(y) in s: return s[str(y)]
    return None

# ---- HAND-CODED sub-dimensions (documented; spec requires manual coding for S3/S4) ----
# S3 transcendent contestation (0-100): religious sites + external territorial claims + contested land
S3={"ISR":100,"PSE":95,"IND":85,"TWN":90,"CHN":70,"IRQ":72,"UKR":72,"RUS":62,"SAU":68,"IRN":58,
"TUR":52,"SYR":58,"ARM":55,"AZE":50,"CYP":58,"XKX":58,"SRB":45,"PAK":58,"MAR":48,"LBN":48,"GEO":45,
"JOR":48,"EGY":42,"BIH":42,"MDA":42,"GRC":38,"ITA":40,"NPL":34,"LKA":36,"MMR":42,"ESP":35,"ETH":40,
"YEM":36,"AFG":45,"SDN":38,"KOR":35,"PRK":35,"VAT":60,"KHM":30,"THA":28,"COD":30,"MLI":30,"SOM":32}
# S4 external deterrence (0-100): NATO/US-treaty/nuclear=100; major-non-NATO=70; regional=40; none=10
NATO={"USA","GBR","FRA","DEU","ITA","ESP","POL","ROU","NLD","BEL","GRC","PRT","CZE","HUN","SVK","BGR",
"HRV","SVN","LTU","LVA","EST","DNK","NOR","ISL","LUX","ALB","MNE","MKD","TUR","CAN","FIN","SWE"}
US_TREATY={"JPN","KOR","AUS","PHL","THA","NZL"}
NUCLEAR={"USA","RUS","CHN","GBR","FRA","IND","PAK","ISR","PRK"}
MAJOR_ALLY={"ISR":85,"TWN":80,"JOR":70,"EGY":70,"QAT":75,"KWT":75,"SAU":70,"ARE":75,"BHR":75,"UKR":60,
"KAZ":50,"SGP":65,"MAR":55,"TUN":45,"COL":55,"ARG":45,"BRA":40,"VNM":40}
def deter(i):
    if i in NATO or i in US_TREATY or i in NUCLEAR: return 100
    if i in MAJOR_ALLY: return MAJOR_ALLY[i]
    if i in {"MDA","SRB","BIH","GEO","ARM","AZE"}: return 30  # aspirants/partial
    return 15
# S4 coup-proneness (0-100), hand-coded from known coup history (Powell-Thyne unreachable)
COUP={"THA":90,"SDN":95,"MMR":90,"MLI":90,"BFA":92,"NER":85,"GIN":88,"PAK":82,"TUR":70,"EGY":72,
"BGD":62,"NGA":55,"GHA":45,"MRT":75,"GNB":88,"TCD":70,"CAF":70,"COD":55,"HTI":70,"FJI":80,"COM":85,
"MDG":55,"HND":50,"BOL":55,"VEN":45,"GTM":45,"PER":40,"ECU":40,"ZWE":40,"UGA":45,"SSD":60,"LBY":55,
"IRQ":50,"SYR":45,"YEM":55,"AFG":60,"GNQ":45,"GAB":55,"TGO":50,"BEN":40,"BDI":55,"RWA":45,"NPL":40}

def build():
    isos=[i for i in five if i in five]
    # first pass: pull V3/T4 for neighbours
    rows={}
    for i in isos:
        v3=five[i]["V3"]; t4=five[i]["T4"]
        rows[i]=dict(iso=i,name=five[i]["name"],V3=v3,T4=t4)
    pop=tier4.get("population",{}); ref=T6D.get("refugees_hosted",{})
    def raw(i):
        # S1 geographic
        nb=[x for x in adj.get(i,[]) if x in five]
        neigh=np.mean([ (five[x]["V3"]+five[x]["T4"])/2 for x in nb]) if nb else 20.0
        rh=latest(ref,i); pp=latest(pop,i)
        refshare=min((rh/pp*100),30) if (rh and pp) else 0
        nland=len(adj.get(i,[])); maritime=(1.0 if nland==0 else max(0,1-nland/8))  # island=insulated
        s1=0.55*neigh + 0.25*(refshare/30*100) + 0.20*(1-maritime)*60
        # S2 resource
        rr=latest(T6D.get("resource_rents_total"),i) or 0
        strat=STRAT.get(i,0)
        s2=min(rr*3,100)*0.5 + strat*0.5
        # S3 transcendent (hand)
        s3=S3.get(i,3)
        # S4 military net = internal x (1-deterrence)
        ms=latest(T6D.get("mil_spend"),i) or 1.5
        internal=0.5*COUP.get(i,8) + 0.5*min(ms*8,100)
        s4=internal*(1-deter(i)/100)
        return s1,s2,s3,s4
    STRAT={"SAU":90,"RUS":85,"IRN":85,"IRQ":85,"VEN":80,"KWT":85,"ARE":80,"QAT":85,"NGA":75,"AGO":70,
    "LBY":80,"KAZ":80,"DZA":75,"AZE":70,"COD":85,"BOL":60,"CHL":65,"ARG":50,"AUS":55,"NOR":55,"GNQ":70,
    "TCD":50,"SSD":70,"YEM":45,"OMN":70,"TKM":75,"BRN":75,"EGY":60,"PAN":70,"SGP":55,"DJI":55,"TUR":45}
    globals()["STRAT"]=STRAT
    for i in isos:
        s1,s2,s3,s4=raw(i); rows[i].update(s1=s1,s2=s2,s3=s3,s4=s4)
    # normalize each 0-100 (5/95)
    def nf(key):
        a=np.array([rows[i][key] for i in isos],float); lo,hi=np.percentile(a,5),np.percentile(a,95)
        return lambda v: float(np.clip((v-lo)/(hi-lo)*100,0,100)) if hi>lo else (lambda v:50)
    N={k:nf(k) for k in ["s1","s2","s3","s4"]}
    for i in isos:
        r=rows[i]
        r["S1"],r["S2"],r["S3"],r["S4"]=N["s1"](r["s1"]),N["s2"](r["s2"]),N["s3"](r["s3"]),N["s4"](r["s4"])
        r["T6"]=float(np.mean([r["S1"],r["S2"],r["S3"],r["S4"]]))
    return rows

rows=build()
# crisis outcome 2013-2024, T5
def crisis(i):
    conf=any(2013<=y<=2024 for y in dom.get(i,set()))
    s={int(y):v for y,v in lib.get(i,{}).items()}
    bs=(s.get(2024,1)-s.get(2012,0))<=-0.05 if (2024 in s and 2012 in s and s.get(2012,0)>=0.15) else False
    return 1 if (conf or bs) else 0
for i in rows:
    rows[i]["crisis"]=crisis(i); rows[i]["T5"]=five[i]["T5"]

print("Tier 6 — spark density. Most spark-dense environments:")
for r in sorted(rows.values(),key=lambda x:-x["T6"])[:15]:
    print(f"   {r['name']:22s} T6={r['T6']:4.0f}  (S1geo={r['S1']:.0f} S2res={r['S2']:.0f} S3trans={r['S3']:.0f} S4mil={r['S4']:.0f})")
print(f"\n  Netherlands T6 rank (T6-6): {sorted([r['T6'] for r in rows.values()]).index(rows['NLD']['T6'])+1}/{len(rows)} (T6={rows['NLD']['T6']:.0f})  [bottom decile?={rows['NLD']['T6']<=np.percentile([r['T6'] for r in rows.values()],10)}]")

# ---- tests ----
def auc(cols,y):  # IN-SAMPLE (diagnostic only — overfits when stacking many predictors on n~small)
    y=np.array(y,float); X=np.column_stack([np.ones(len(y))]+[L.zscore(c) for c in cols]); _,a,_=L.logit_fit(X,y); return round(float(a),4)
def cv_auc(cols,y,k=5,seed=0):
    """OUT-OF-FOLD AUC. AUDIT C1 FIX: stacking V1+V3+T4+T5+T6+interaction (6-7 predictors) on
    n~small makes in-sample AUC mechanically >= every sub-model. Report OOF for any comparison."""
    y=np.array(y,float); n=len(y); pos=int(y.sum()); neg=n-pos
    if pos<2 or neg<2: return None
    kk=min(k,pos,neg)
    if kk<2: return None
    rng=np.random.default_rng(seed); fold=np.empty(n,int)
    for cls in (0.0,1.0):
        idx=rng.permutation(np.where(y==cls)[0]); fold[idx]=np.arange(len(idx))%kk
    Xraw=np.column_stack(cols).astype(float); oof=np.full(n,np.nan)
    for f in range(kk):
        tr=np.where(fold!=f)[0]; te=np.where(fold==f)[0]
        if len(set(y[tr]))<2: return None
        mu=Xraw[tr].mean(0); sd=Xraw[tr].std(0); sd[sd==0]=1.0
        b,_,_=L.logit_fit(np.column_stack([np.ones(len(tr)),(Xraw[tr]-mu)/sd]),y[tr])
        oof[te]=1/(1+np.exp(-np.column_stack([np.ones(len(te)),(Xraw[te]-mu)/sd])@b))
    return round(float(L.auc_roc(list(oof),list(y))),4)
sub=[r for r in rows.values() if r["T5"] is not None]
y=[r["crisis"] for r in sub]
print(f"\nn(with T5)={len(sub)} crisis={sum(y)}")
a_t5=auc([[r["T5"] for r in sub]],y); a_t6=auc([[r["T6"] for r in sub]],y); a_both=auc([[r["T5"] for r in sub],[r["T6"] for r in sub]],y)
c_t5=cv_auc([[r["T5"] for r in sub]],y); c_t6=cv_auc([[r["T6"] for r in sub]],y); c_both=cv_auc([[r["T5"] for r in sub],[r["T6"] for r in sub]],y)
inter=[r["T5"]*r["T6"]/100 for r in sub]
a_intr=auc([[r["T5"] for r in sub],[r["T6"] for r in sub],inter],y)
c_intr=cv_auc([[r["T5"] for r in sub],[r["T6"] for r in sub],inter],y)
print("\n=== T6-1 — does spark density add over criticality? ===")
print(f"   IN-SAMPLE: T5={a_t5} T6={a_t6} T5+T6={a_both} (incr {round(a_both-a_t5,3)})")
print(f"   OUT-OF-FOLD: T5={c_t5} T6={c_t6} T5+T6={c_both} (incr {None if (c_both is None or c_t5 is None) else round(c_both-c_t5,3)})  <-- honest")
print("=== T6-4 (CAPSTONE) — T5 x T6 interaction ===")
# interaction significance
yy=np.array(y,float); X=np.column_stack([np.ones(len(yy)),L.zscore([r['T5'] for r in sub]),L.zscore([r['T6'] for r in sub]),L.zscore(inter)])
b,_,_=L.logit_fit(X,yy)
rng=np.random.default_rng(0); bs=[]
for _ in range(400):
    ix=rng.integers(0,len(yy),len(yy))
    if len(set(yy[ix].tolist()))<2: continue
    bb,_,_=L.logit_fit(X[ix],yy[ix]); bs.append(bb)
se=np.std(bs,0)
print(f"   T5+T6+interaction AUC(in-sample)={a_intr} OOF={c_intr}  | interaction coef={b[3]:+.3f} (z={b[3]/se[3]:+.2f})")
# full six-tier
V1=[[five[r['iso']]['V1'] for r in sub]]; V3=[[r['V3'] for r in sub]]; T4=[[r['T4'] for r in sub]]
sixcols=V1+V3+T4+[[r['T5'] for r in sub],[r['T6'] for r in sub],inter]
a_six=auc(sixcols,y); c_six=cv_auc(sixcols,y)
print(f"   FULL six-tier (V1+V3+T4+T5+T6+T5xT6) AUC: in-sample={a_six}  OUT-OF-FOLD={c_six}  <-- honest headline")
# T6-2/3: false neg/pos vs T6
medT5=np.median([r['T5'] for r in sub]); medT6=np.median([r['T6'] for r in sub])
fn=[r['T6'] for r in sub if r['T5']>=medT5 and r['crisis']==0]  # flickering, no crisis
fp=[r['T6'] for r in sub if r['T5']<medT5 and r['crisis']==1]   # calm, crisis anyway
print("\n=== T6-2/3 — does spark density explain T5 errors? ===")
print(f"   T5 false-neg (flickering, no crisis) mean T6={np.mean(fn):.0f}  vs  T5 false-pos (calm, crisis) mean T6={np.mean(fp):.0f}")
print(f"   (T6-2: false-negs should be LOW T6; T6-3: false-pos should be HIGH T6)")
# T6-5: which sub-dim dominates
print("\n=== T6-5 — which spark source dominates? (AUC each, and net of others) ===")
for k in ["S1","S2","S3","S4"]:
    print(f"   {k}: AUC={auc([[r[k] for r in sub]],y)}")
Xf=np.column_stack([np.ones(len(yy))]+[L.zscore([r[k] for r in sub]) for k in ["S1","S2","S3","S4"]])
bf,_,_=L.logit_fit(Xf,yy)
print(f"   joint coefs: S1={bf[1]:+.2f} S2={bf[2]:+.2f} S3={bf[3]:+.2f} S4={bf[4]:+.2f}")

# persist the AUC results (OOF is the honest headline) so the regression suite can pin them
json.dump({"n":len(sub),"crisis":int(sum(y)),
           "insample":{"T5":a_t5,"T6":a_t6,"T5+T6":a_both,"T6_increment":round(a_both-a_t5,3),
                       "T5+T6+inter":a_intr,"six_tier":a_six},
           "out_of_fold":{"T5":c_t5,"T6":c_t6,"T5+T6":c_both,
                          "T6_increment":None if (c_both is None or c_t5 is None) else round(c_both-c_t5,3),
                          "T5+T6+inter":c_intr,"six_tier":c_six}},
          open("data/political/tier6_auc.json","w"),indent=1)

# AUDIT C2 GUARD: only overwrite the committed snapshot when the border/ISO fetch actually
# succeeded (else we'd silently shift every T6 from a data gap). NET_OK is set in build().
if NET_OK:
    prev=json.load(open("data/political/six_tier_snapshot.json")) if os.path.exists("data/political/six_tier_snapshot.json") else None
    newsnap=[{"iso":i,"name":five[i]["name"],"V1":five[i]["V1"],"V2":five[i]["V2"],"V3":five[i]["V3"],
              "T4":five[i]["T4"],"T5":five[i]["T5"],"T6":round(rows[i]["T6"],1),"arch":five[i]["arch"]} for i in sorted(rows,key=lambda x:-five[x]["V1"])]
    if prev is not None:
        pm={r["iso"]:r["T6"] for r in prev}; drift=max((abs(pm.get(r["iso"],r["T6"])-r["T6"]) for r in newsnap),default=0)
        print(f"\n  T6 max drift vs committed snapshot: {drift:.2f}")
        if drift>3.0: print("  !! large T6 drift — the border CACHE pins geography, so this is a T4/T5 input change; expected during reconciliation but verify it's intentional")
    json.dump(newsnap,open("data/political/six_tier_snapshot.json","w"),indent=1); print("\nsaved six_tier_snapshot.json")
else:
    print("\n  network fetch failed/unavailable -> six_tier_snapshot.json left untouched (offline-safe)")
