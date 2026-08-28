#!/usr/bin/env python3
"""Ingest the manually-downloaded authoritative files: IMF WEO (fiscal), LIS Key Figures
(income equity). Saves data/v2/manual_indicators.json."""
import json, openpyxl, warnings, urllib.request
from pathlib import Path
warnings.filterwarnings("ignore")
ROOT=Path(__file__).resolve().parents[2]; M=ROOT/"data/v2/manual"
out={"_meta":{"sources":["IMF WEO Apr2025","LIS Key Figures 12-Jun-2026"]},"series":{}}

# ---- IMF WEO (UTF-16 tab-delimited) ----
WANT={"GGXONLB_NGDP":"weo_primary_bal","GGXWDG_NGDP":"weo_gross_debt"}
for k in WANT.values(): out["series"][k]={}
with open(M/"weoapr2025all.xls",encoding="utf-16-le",errors="replace") as f:
    lines=f.read().split("\n")
hdr=lines[0].split("\t")
# year columns: find 4-digit numeric headers
yearcols={}
for j,h in enumerate(hdr):
    h=h.strip()
    if h.isdigit() and 1980<=int(h)<=2030: yearcols[j]=int(h)
iso_j=1; subj_j=2
n=0
for line in lines[1:]:
    c=line.split("\t")
    if len(c)<10: continue
    iso=c[iso_j].strip(); subj=c[subj_j].strip()
    if subj not in WANT or len(iso)!=3: continue
    key=WANT[subj]
    for j,yr in yearcols.items():
        if j<len(c):
            v=c[j].strip().replace(",","")
            if v not in ("","n/a","--"):
                try: out["series"][key].setdefault(iso,{})[str(yr)]=float(v)
                except: pass
    n+=1
print("WEO:", {k:len(out['series'][k]) for k in WANT.values()}, "rows matched:",n)

# ---- LIS Key Figures ----
NAME2ISO={"Australia":"AUS","Austria":"AUT","Belgium":"BEL","Brazil":"BRA","Canada":"CAN",
"Chile":"CHL","China":"CHN","Colombia":"COL","Czech Republic":"CZE","Czechia":"CZE","Denmark":"DNK",
"Egypt":"EGY","Estonia":"EST","Finland":"FIN","France":"FRA","Georgia":"GEO","Germany":"DEU",
"Greece":"GRC","Guatemala":"GTM","Hungary":"HUN","Iceland":"ISL","India":"IND","Ireland":"IRL",
"Israel":"ISR","Italy":"ITA","Japan":"JPN","Lithuania":"LTU","Luxembourg":"LUX","Mexico":"MEX",
"Netherlands":"NLD","Norway":"NOR","Panama":"PAN","Paraguay":"PRY","Peru":"PER","Poland":"POL",
"Russia":"RUS","Serbia":"SRB","Slovak Republic":"SVK","Slovakia":"SVK","Slovenia":"SVN","South Africa":"ZAF",
"South Korea":"KOR","Korea":"KOR","Spain":"ESP","Sweden":"SWE","Switzerland":"CHE","Taiwan":"TWN",
"United Kingdom":"GBR","United States":"USA","Uruguay":"URY","Dominican Republic":"DOM","Ivory Coast":"CIV",
"Cote d'Ivoire":"CIV","Palestine":"PSE"}
wb=openpyxl.load_workbook(M/"lis-key-figures-workbook.xlsx",read_only=True,data_only=True)
ws=wb[wb.sheetnames[0]]
gini={}; p9010={}
rows=list(ws.iter_rows(values_only=True)); hdr2=[str(c) if c else "" for c in rows[0]]
# find columns
gcol=next((i for i,h in enumerate(hdr2) if "Gini" in h),2)
pcol=next((i for i,h in enumerate(hdr2) if "90/1" in h),5)
best={}
for r in rows[1:]:
    lbl=str(r[0]) if r[0] else ""
    if not lbl.startswith("LIS - "): continue
    body=lbl[6:].replace("_x000D_","").strip()
    # split "Country YYYY"
    parts=body.rsplit(" ",1)
    if len(parts)!=2 or not parts[1].isdigit(): continue
    name,yr=parts[0].strip(),int(parts[1]); iso=NAME2ISO.get(name)
    if not iso: continue
    if iso not in best or yr>best[iso]:
        try:
            g=float(r[gcol]); p=float(r[pcol])
            best[iso]=yr; gini[iso]=g*100; p9010[iso]=p
        except: pass
out["series"]["lis_gini"]=gini; out["series"]["lis_p90p10"]=p9010
print("LIS: countries=",len(gini),"(latest wave each)")
wb.close()

# ---- try PISA equity stat.link (Annex B1 chapter on equity) ----
try:
    req=urllib.request.Request("https://stat.link/xmrlsh", headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req,timeout=25) as r:
        print("PISA stat.link Annex B1 Ch2:", r.status, r.geturl()[:60])
except Exception as e:
    print("PISA stat.link:", type(e).__name__, str(e)[:50], "-> equity table NOT fetched (link-index only)")

(ROOT/"data/v2/manual_indicators.json").write_text(json.dumps(out))
print("saved manual_indicators.json")

# ---- PISA ESCS socio-economic score gap (math/reading/science) ----
import io as _io
PNAME={"Australia":"AUS","Austria":"AUT","Belgium":"BEL","Canada":"CAN","Chile":"CHL","Colombia":"COL",
"Costa Rica":"CRI","Czech Republic":"CZE","Czechia":"CZE","Denmark":"DNK","Estonia":"EST","Finland":"FIN",
"France":"FRA","Germany":"DEU","Greece":"GRC","Hungary":"HUN","Iceland":"ISL","Ireland":"IRL","Israel":"ISR",
"Italy":"ITA","Japan":"JPN","Korea":"KOR","Latvia":"LVA","Lithuania":"LTU","Luxembourg":"LUX","Mexico":"MEX",
"Netherlands":"NLD","New Zealand":"NZL","Norway":"NOR","Poland":"POL","Portugal":"PRT","Slovak Republic":"SVK",
"Slovenia":"SVN","Spain":"ESP","Sweden":"SWE","Switzerland":"CHE","Turkiye":"TUR","Türkiye":"TUR","Turkey":"TUR",
"United Kingdom":"GBR","United States":"USA","Brazil":"BRA","Bulgaria":"BGR","Croatia":"HRV","Cyprus":"CYP",
"Malta":"MLT","Romania":"ROU","Serbia":"SRB","Argentina":"ARG","Peru":"PER","Uruguay":"URY","Panama":"PAN",
"Georgia":"GEO","Kazakhstan":"KAZ","Malaysia":"MYS","Thailand":"THA","Indonesia":"IDN","Viet Nam":"VNM",
"Philippines":"PHL","Saudi Arabia":"SAU","Qatar":"QAT","United Arab Emirates":"ARE","Jordan":"JOR",
"Morocco":"MAR","Albania":"ALB","North Macedonia":"MKD","Montenegro":"MNE","Moldova":"MDA","Ukraine":"UKR",
"Dominican Republic":"DOM","El Salvador":"SLV","Guatemala":"GTM","Paraguay":"PRY","Hong Kong (China)":"HKG",
"Chinese Taipei":"TWN","Singapore":"SGP","Mongolia":"MNG","Jamaica":"JAM","Palestinian Authority":"PSE"}
def pisa_gaps():
    req=urllib.request.Request("https://stat.link/wh9d4z", headers={"User-Agent":"Mozilla/5.0"})
    data=urllib.request.urlopen(req,timeout=40).read()
    wb=openpyxl.load_workbook(_io.BytesIO(data), read_only=True, data_only=True)
    percountry={}
    for sh in ["Table I.B1.5.31","Table I.B1.5.34","Table I.B1.5.37"]:
        ws=wb[sh]
        for row in ws.iter_rows(min_row=10, values_only=True):
            nm=str(row[0]).replace("*","").strip() if row[0] else ""
            iso=PNAME.get(nm)
            if not iso: continue
            try: g=float(row[1])   # score dif. (socio-economic gap, 10th pct)
            except (TypeError,ValueError): continue
            percountry.setdefault(iso,[]).append(g)
    wb.close()
    return {iso:sum(v)/len(v) for iso,v in percountry.items()}
try:
    pg=pisa_gaps(); out["series"]["pisa_escs_gap"]=pg
    print("PISA ESCS gap: countries=",len(pg),"(higher=more unequal)")
except Exception as e:
    print("PISA parse failed:",type(e).__name__,str(e)[:60])
(ROOT/"data/v2/manual_indicators.json").write_text(json.dumps(out))
print("re-saved with PISA")
