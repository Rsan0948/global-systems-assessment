#!/usr/bin/env python3
"""
Build a single cross-era conflict-ONSET table {iso3: sorted[onset_years]} by
merging UCDP/PRIO ACD (1946-2023) with Correlates of War (1816-2007).

ONSET semantics:
  * UCDP: a conflict-year for a conflict that was INACTIVE the prior year
    (reuses the exact logic from data/robustness/outcomes/grade.py).
  * COW:  each state's war-participation StartYear (and StartYear2 re-entry) is a
    discrete war onset. Inter-State (v4.0) + Intra-State (v4.1) are used, matching
    the task spec. Extra-State is fetched but excluded (colonial/extra-territorial).

Country keying:
  * UCDP gwno_loc  -> ISO3 via the Gleditsch-Ward map (GW_ISO, from grade.py).
  * COW  ccode     -> ISO3 via COW-country-codes.csv StateNme -> pycountry
    (+ a manual override dict for historical/renamed states). NOT hand-curated
    per-war; the mapping is name-based and auditable.

Writes data/robustness/historical/conflict_onsets.json with provenance +
join-loss diagnostics. Read-only w.r.t. all source files.
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

import pycountry

ROOT = Path(__file__).resolve().parents[2]
OUTC = ROOT / "data" / "robustness" / "outcomes"
COW = OUTC / "cow"
OUT = ROOT / "data" / "robustness" / "historical" / "conflict_onsets.json"

# ---------- Gleditsch-Ward country number -> ISO3 (copied verbatim from grade.py) ----------
GW_ISO = {
 2:'USA',20:'CAN',40:'CUB',41:'HTI',42:'DOM',70:'MEX',90:'GTM',91:'HND',92:'SLV',
 93:'NIC',95:'PAN',100:'COL',101:'VEN',110:'GUY',130:'ECU',135:'PER',140:'BRA',
 145:'BOL',150:'PRY',155:'CHL',160:'ARG',165:'URY',200:'GBR',205:'IRL',210:'NLD',
 211:'BEL',212:'LUX',220:'FRA',225:'CHE',230:'ESP',235:'PRT',255:'DEU',290:'POL',
 305:'AUT',310:'HUN',316:'CZE',317:'SVK',325:'ITA',338:'MLT',339:'ALB',341:'MNE',
 343:'MKD',344:'HRV',345:'SRB',346:'BIH',349:'SVN',350:'GRC',352:'CYP',355:'BGR',
 359:'MDA',360:'ROU',365:'RUS',366:'EST',367:'LVA',368:'LTU',369:'UKR',370:'BLR',
 371:'ARM',372:'GEO',373:'AZE',375:'FIN',380:'SWE',385:'NOR',390:'DNK',395:'ISL',
 402:'CPV',404:'GNB',411:'GNQ',420:'GMB',432:'MLI',433:'SEN',434:'BEN',435:'MRT',
 436:'NER',437:'CIV',438:'GIN',439:'BFA',450:'LBR',451:'SLE',452:'GHA',461:'TGO',
 471:'CMR',475:'NGA',481:'GAB',482:'CAF',483:'TCD',484:'COG',490:'COD',500:'UGA',
 501:'KEN',510:'TZA',516:'BDI',517:'RWA',520:'SOM',522:'DJI',530:'ETH',531:'ERI',
 540:'AGO',541:'MOZ',551:'ZMB',552:'ZWE',553:'MWI',560:'ZAF',565:'NAM',570:'LSO',
 571:'BWA',572:'SWZ',580:'MDG',590:'MUS',600:'MAR',615:'DZA',616:'TUN',620:'LBY',
 625:'SDN',626:'SSD',630:'IRN',640:'TUR',645:'IRQ',651:'EGY',652:'SYR',660:'LBN',
 663:'JOR',666:'ISR',670:'SAU',678:'YEM',680:'YEM',690:'KWT',692:'BHR',694:'QAT',
 696:'ARE',698:'OMN',700:'AFG',701:'TKM',702:'KGZ',703:'TJK',704:'UZB',705:'KAZ',
 710:'CHN',712:'MNG',713:'TWN',731:'PRK',732:'KOR',740:'JPN',750:'IND',760:'BTN',
 770:'PAK',771:'BGD',775:'MMR',780:'LKA',781:'MDV',790:'NPL',800:'THA',811:'KHM',
 812:'LAO',816:'VNM',820:'MYS',830:'SGP',840:'PHL',850:'IDN',860:'TLS',900:'AUS',
 910:'PNG',920:'NZL',990:'WSM',
 # extensions beyond grade.py's map (onset-bearing gwno absent there):
 52:'TTO',55:'GRD',94:'CRI',115:'SUR',581:'COM',751:'IND',817:'VNM',835:'BRN',
}

# ---------- COW StateNme -> ISO3 manual overrides (historical / renamed / merged states) ----------
COW_NAME_MANUAL = {
 'German Federal Republic':'DEU','German Democratic Republic':'DEU','Prussia':'DEU',
 'Germany (Prussia)':'DEU','Baden':'DEU','Bavaria':'DEU','Saxony':'DEU','Wuerttemburg':'DEU',
 'Hesse Electoral':'DEU','Hesse Grand Ducal':'DEU','Hesse-Kassel (Electoral)':'DEU',
 'Hesse-Darmstadt (Ducal)':'DEU','Mecklenburg Schwerin':'DEU','Hanover':'DEU',
 'Austria-Hungary':'AUT','Yugoslavia':'SRB','Serbia':'SRB','Rumania':'ROU',
 'Russia (Soviet Union)':'RUS','Russia':'RUS','Korea':'KOR',
 "Korea, People's Republic of":'PRK','Korea, Republic of':'KOR',
 'Democratic Republic of the Congo':'COD','Congo':'COG','Zaire':'COD',
 'Vietnam, Democratic Republic of':'VNM','Republic of Vietnam':'VNM',
 'Democratic Republic of Vietnam':'VNM','Vietnam':'VNM',
 'Iran (Persia)':'IRN','Turkey (Ottoman Empire)':'TUR','Turkey':'TUR','Kyrgyzstan':'KGZ',
 'Cote D’Ivoire':'CIV','Ivory Coast':'CIV','Cote d’Ivoire':'CIV',
 'Tanzania':'TZA','Tanzania/Tanganyika':'TZA','Myanmar (Burma)':'MMR','Burma':'MMR',
 'Cambodia (Kampuchea)':'KHM','Cambodia':'KHM','Sri Lanka (Ceylon)':'LKA',
 'Zimbabwe (Rhodesia)':'ZWE','Yemen Arab Republic':'YEM','Yemen':'YEM',
 "Yemen People's Republic":'YEM','Yemen People’s Republic':'YEM',
 'Macedonia':'MKD','Macedonia (FYROM)':'MKD','Bosnia and Herzegovina':'BIH',
 'Laos':'LAO','Moldova':'MDA','Belarus (Byelorussia)':'BLR','Cape Verde':'CPV',
 'Sao Tome and Principe':'STP','Surinam':'SUR','Trinidad and Tobago':'TTO',
 'Papal States':'ITA','Two Sicilies':'ITA','Sardinia':'ITA','Modena':'ITA',
 'Parma':'ITA','Tuscany':'ITA','Ethiopia':'ETH','Abyssinia':'ETH','East Timor':'TLS',
 'Swaziland':'SWZ','Gambia':'GMB','United States of America':'USA','United Kingdom':'GBR',
 'Czechoslovakia':'CZE','Kosovo':'SRB','Zanzibar':'TZA','Brunei':'BRN',
 'St. Lucia':'LCA','St. Vincent and the Grenadines':'VCT','Antigua & Barbuda':'ATG',
 'St. Kitts and Nevis':'KNA',
}


def build_ccode_iso():
    """ccode -> ISO3 from COW-country-codes.csv (name-based, override dict for oddities)."""
    out = {}
    unmapped = []
    for r in csv.DictReader(open(COW / "COW-country-codes.csv", encoding="latin-1")):
        cc = int(r["CCode"])
        nm = r["StateNme"].strip()
        if nm in COW_NAME_MANUAL:
            out[cc] = COW_NAME_MANUAL[nm]
            continue
        try:
            out[cc] = pycountry.countries.lookup(nm).alpha_3
        except Exception:
            unmapped.append((cc, nm))
    return out, unmapped


def ucdp_onsets():
    """Reuse grade.py logic: gwno_loc -> onset years (year active, prior year not)."""
    rows = list(csv.DictReader(open(OUTC / "ucdp" / "UcdpPrioConflict_v24_1.csv", encoding="utf-8")))
    gw_conf_years = defaultdict(lambda: defaultdict(set))
    for r in rows:
        y = int(r["year"]); cid = r["conflict_id"]
        for g in r["gwno_loc"].split(","):
            g = g.strip()
            if g.isdigit():
                gw_conf_years[int(g)][cid].add(y)
    gw_onset = defaultdict(set)
    for g, confs in gw_conf_years.items():
        for cid, ys in confs.items():
            for y in ys:
                if (y - 1) not in ys:
                    gw_onset[g].add(y)
    iso_onset = defaultdict(set)
    unmapped_gw = set()
    for g, ys in gw_onset.items():
        iso = GW_ISO.get(g)
        if iso is None:
            unmapped_gw.add(g)
        else:
            iso_onset[iso] |= ys
    return iso_onset, sorted(unmapped_gw)


def _years_from_row(row, year_fields):
    out = set()
    for f in year_fields:
        v = (row.get(f) or "").strip()
        if v and v.lstrip("-").isdigit():
            iv = int(v)
            if 1500 <= iv <= 2025:
                out.add(iv)
    return out


def cow_onsets(ccode_iso):
    """Inter-State (v4.0) + Intra-State (v4.1) onsets per ISO3. Onset = StartYear{1,2}."""
    iso_onset = defaultdict(set)
    unmapped_cc = defaultdict(int)  # ccode -> count of onset-events lost

    def add(cc_raw, years):
        cc = (cc_raw or "").strip()
        if not (cc and cc.lstrip("-").isdigit()):
            return
        cc = int(cc)
        if cc <= 0:  # -8 / -9 = non-state actor or missing
            return
        iso = ccode_iso.get(cc)
        if iso is None:
            unmapped_cc[cc] += 1
            return
        iso_onset[iso] |= years

    # Inter-State: one row per state-participation, field 'ccode'
    for r in csv.DictReader(open(COW / "Inter-StateWarData_v4.0.csv", encoding="latin-1")):
        ys = _years_from_row(r, ["StartYear1", "StartYear2"])
        add(r.get("ccode"), ys)

    # Intra-State: CcodeA (usually govt) + CcodeB (usually rebel, often <0)
    for r in csv.DictReader(open(COW / "Intra-StateWarData_v4.1.csv", encoding="latin-1")):
        ys = _years_from_row(r, ["StartYear1", "StartYear2"])
        add(r.get("CcodeA"), ys)
        add(r.get("CcodeB"), ys)

    return iso_onset, dict(sorted(unmapped_cc.items()))


def main():
    ccode_iso, cc_name_unmapped = build_ccode_iso()
    ucdp, unmapped_gw = ucdp_onsets()
    cow, unmapped_cc = cow_onsets(ccode_iso)

    merged = defaultdict(set)
    for src in (ucdp, cow):
        for iso, ys in src.items():
            merged[iso] |= ys

    onsets = {iso: sorted(ys) for iso, ys in sorted(merged.items())}
    all_years = sorted({y for ys in merged.values() for y in ys})

    report = {
        "dataset": "cross_era_conflict_onsets",
        "provenance": {
            "ucdp": "UCDP/PRIO ACD v24.1 (coverage 1946-2023); onset = conflict active in "
                    "year & inactive prior year; gwno_loc -> ISO3 via Gleditsch-Ward map",
            "cow_inter": "Correlates of War Inter-State War Data v4.0 (1816-2007); onset = "
                         "state-participation StartYear1/StartYear2",
            "cow_intra": "Correlates of War Intra-State War Data v4.1 (1816-2007); onset = "
                         "CcodeA/CcodeB (positive ccodes) StartYear1/StartYear2",
            "cow_excluded": "Extra-State War Data v4.0 fetched but excluded (extra-territorial/colonial)",
            "ccode_to_iso3": "COW-country-codes.csv StateNme -> pycountry + manual overrides",
        },
        "counts": {
            "iso3_with_onsets": len(onsets),
            "total_onset_events": sum(len(v) for v in onsets.values()),
            "year_span": [all_years[0], all_years[-1]] if all_years else None,
            "n_iso_ucdp": len(ucdp),
            "n_iso_cow": len(cow),
        },
        "join_losses": {
            "ucdp_unmapped_gwno": unmapped_gw,
            "cow_unmapped_ccode_in_wardata": unmapped_cc,
            "cow_countrycode_names_unmapped": [f"{cc}:{nm}" for cc, nm in cc_name_unmapped],
        },
        "onsets": onsets,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2))

    print(f"iso3 with onsets: {len(onsets)}  events: {report['counts']['total_onset_events']}  "
          f"span: {report['counts']['year_span']}")
    print(f"UCDP isos: {len(ucdp)}  COW isos: {len(cow)}")
    print(f"unmapped gwno (UCDP): {unmapped_gw}")
    print(f"unmapped ccode in war data (COW): {unmapped_cc}")
    print(f"-> {OUT.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
