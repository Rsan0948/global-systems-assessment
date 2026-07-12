#!/usr/bin/env python3
"""Fetch the HARD V2 sources beyond plain WDI level: WB wealth-quintile equity (DHS),
OWID PISA + incarceration. Merges into data/v2/v2_indicators.json."""
import urllib.request, json, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
F = ROOT/"data/v2/v2_indicators.json"
out = json.loads(F.read_text())

def wb(code, tries=6):
    url=f"https://api.worldbank.org/v2/country/all/indicator/{code}?format=json&per_page=20000"
    for t in range(tries):
        try:
            req=urllib.request.Request(url, headers={"User-Agent":"research"})
            with urllib.request.urlopen(req, timeout=70) as r:
                d=json.loads(r.read().decode())
            if isinstance(d,list) and len(d)>1 and d[1]: return d[1]
            time.sleep(3)
        except Exception:
            time.sleep(4)
    return None

# WB wealth-quintile equity (Q1=poorest, Q5=richest)
QUINT={
 "eq_measles_q1":"SH.IMM.MEAS.Q1.ZS","eq_measles_q5":"SH.IMM.MEAS.Q5.ZS",
 "eq_birth_q1":"SH.STA.BRTC.Q1.ZS","eq_birth_q5":"SH.STA.BRTC.Q5.ZS",
 "eq_stunt_q1":"SH.STA.STNT.Q1.ZS","eq_stunt_q5":"SH.STA.STNT.Q5.ZS",
 "eq_antenatal_q1":"SH.STA.ANVC.Q1.ZS","eq_antenatal_q5":"SH.STA.ANVC.Q5.ZS",
}
for name,code in QUINT.items():
    rows=wb(code); 
    if not rows: print(name,"FAIL"); continue
    ser={}
    for r in rows:
        iso=r.get("countryiso3code"); v=r.get("value")
        if iso and len(iso)==3 and v is not None: ser.setdefault(iso,{})[r["date"]]=v
    out["series"][name]=ser
    print(f"{name}: countries={len(ser)}")
    time.sleep(0.4)

# OWID CSVs (confirmed slugs)
def owid(slug, tries=4):
    for t in range(tries):
        try:
            req=urllib.request.Request(f"https://ourworldindata.org/grapher/{slug}.csv", headers={"User-Agent":"Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read().decode("utf-8","replace")
        except Exception:
            time.sleep(3)
    return None
import csv, io
def parse_owid(txt, valcol=3):
    ser={}
    rd=csv.reader(io.StringIO(txt)); rows=list(rd); hdr=rows[0]
    for row in rows[1:]:
        if len(row)<4: continue
        iso=row[1]; yr=row[2]; val=row[valcol] if valcol<len(row) else ""
        if len(iso)==3 and val not in ("",None):
            try: ser.setdefault(iso,{})[yr]=float(val)
            except: pass
    return ser, hdr
for name,slug in [("incarceration","prison-population-rate"),("pisa_math","pisa-test-score-mean-performance-on-the-mathematics-scale")]:
    txt=owid(slug)
    if not txt: print(name,"FAIL"); continue
    ser,hdr=parse_owid(txt)
    out["series"][name]=ser
    print(f"{name}: countries={len(ser)} (col={hdr[3] if len(hdr)>3 else '?'})")

F.write_text(json.dumps(out))
print("\nmerged. total series:",len(out["series"]))
