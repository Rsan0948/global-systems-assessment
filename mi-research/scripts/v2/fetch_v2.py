#!/usr/bin/env python3
"""V2 coverage audit + fetch. Pulls reliably-available Level+Equity indicators from WB WDI.
Saves latest value per country (2010-2024) + full series where needed for trajectories.
Read-only w.r.t. everything else."""
import urllib.request, json, time, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/v2/v2_indicators.json"

IND = {
 # F1 fiscal (level)
 "f1_cash_bal_gdp":"GC.NLD.TOTL.GD.ZS","f1_interest_rev":"GC.XPN.INTP.RV.ZS","f1_debt_gdp":"GC.DOD.TOTL.GD.ZS",
 # F2 human dev (level)
 "le":"SP.DYN.LE00.IN","health_pc":"SH.XPD.CHEX.PC.CD","infant_mort":"SP.DYN.IMRT.IN",
 "hci_lays":"HD.HCI.LAYS","literacy":"SE.ADT.LITR.ZS","edu_pc_prim":"SE.XPD.PRIM.PC.ZS",
 # F3 infra (level)
 "power_loss":"EG.ELC.LOSS.ZS","water_smng":"SH.H2O.SMDW.ZS","bbnd_p100":"IT.NET.BBND.P2",
 "mobile_p100":"IT.CEL.SETS.P2","lpi_infra":"LP.LPI.INFR.XQ",
 # F4 security (level)
 "homicide":"VC.IHR.PSRC.P5",
 # F5 environment (level)
 "co2_gdp":"EN.GHG.CO2.RT.GDP.PP.KD","pm25":"EN.ATM.PM25.MC.M3","forest":"AG.LND.FRST.ZS","renew":"EG.FEC.RNEW.ZS",
 "cleanfuel":"EG.CFT.ACCS.ZS",
 # F6 social contract (level)
 "oop_health":"SH.XPD.OOPC.CH.ZS","sp_cov":"per_allsp.cov_pop_tot","industry_gdp":"NV.IND.TOTL.ZS",
 # Equity (fetchable): income distribution
 "inc_share_low20":"SI.DST.FRST.20","inc_share_top20":"SI.DST.05TH.20","gini":"SI.POV.GINI",
 # Equity: urban-rural infra gaps
 "elc_rural":"EG.ELC.ACCS.RU.ZS","elc_urban":"EG.ELC.ACCS.UR.ZS",
 "water_rural":"SH.H2O.SMDW.RU.ZS","water_urban":"SH.H2O.SMDW.UR.ZS",
 "cleanfuel_rural":"EG.CFT.ACCS.RU.ZS","cleanfuel_urban":"EG.CFT.ACCS.UR.ZS",
 # helpers
 "gdp_pc_ppp":"NY.GDP.PCAP.PP.CD",
}

def wb(code, tries=5):
    url=f"https://api.worldbank.org/v2/country/all/indicator/{code}?format=json&per_page=20000"
    for t in range(tries):
        try:
            req=urllib.request.Request(url, headers={"User-Agent":"research"})
            with urllib.request.urlopen(req, timeout=70) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            if t==tries-1: return {"_error":str(e)}
            time.sleep(4)

out={"_meta":{"source":"WB WDI v2","fetched":"2026-07-12"},"series":{},"coverage":{}}
for name,code in IND.items():
    d=wb(code)
    if isinstance(d,dict) and "_error" in d:
        out["coverage"][name]={"code":code,"error":d["_error"]}; print(f"{name} ({code}): ERROR {d['_error']}"); continue
    if not isinstance(d,list) or len(d)<2 or d[1] is None:
        msg=d[0].get("message") if isinstance(d[0],dict) else "no data"
        out["coverage"][name]={"code":code,"error":str(msg)[:80]}; print(f"{name} ({code}): NO DATA {str(msg)[:60]}"); continue
    ser={}
    for r in d[1]:
        iso=r.get("countryiso3code"); v=r.get("value")
        if not iso or len(iso)!=3 or v is None: continue
        ser.setdefault(iso,{})[r["date"]]=v
    out["series"][name]=ser
    # latest-value coverage (most recent year 2010-2024 per country)
    def latest(s):
        for y in range(2024,2009,-1):
            if str(y) in s: return s[str(y)]
        return None
    cov=sum(1 for iso in ser if latest(ser[iso]) is not None)
    out["coverage"][name]={"code":code,"n_latest_2010_2024":cov,"n_any":len(ser)}
    print(f"{name} ({code}): latest-cov={cov}  any={len(ser)}")
    time.sleep(0.3)

OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(out))
print("\nsaved",OUT)
