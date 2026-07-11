#!/usr/bin/env python3
"""
Historical add-ons #2 and #3 — forensic analysis of the modern temporal-holdout
errors.

#2 FALSE ALARMS (flagged vulnerable, NO crisis by 2024): are they sustained by an
   identifiable EXTERNAL SUPPORT mechanism (reserve-currency status, sovereign
   wealth + rents, security alliance, IMF programs, external patron)? If so the
   gate isn't wrong — the crisis is delayed/propped, not absent.
#3 MISSES (crisis, NOT flagged): were the crises EXTERNALLY IMPOSED (financial
   contagion, interstate/regional conflict, sanctions, commodity/pandemic shock)
   rather than internal structural decay? If so the gate measures the right thing
   but cannot capture exogenous disruption — a bounded limitation.

Bucket membership is MECHANICAL (elevated flag from the committed predictions x
crisis label from conflict_onsets + CRAG). The external-mechanism tags are a
MANUAL, interpretive classification (documented per country), not a computed
result — clearly separated below.

CRITICAL DATA CAVEAT: the crisis label is conflict-onset (UCDP/COW, to 2023) OR
CRAG sovereign default (to 2015). It therefore MISSES post-2015 economic
collapses (Venezuela 2017, Lebanon 2020, Sri Lanka 2022, Ghana 2022, Argentina
2020, Zambia 2020). Several "false alarms" below DID crisis after the label cutoff
— i.e. the gate was right and the label is blind. This inflates the false-alarm
bucket and is the biggest limitation of this forensic.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import config                               # noqa: E402  (config/robustness.json)

_OUTC_CFG = config.robustness()["outcomes"]
_UCDP_END = _OUTC_CFG["ucdp_data_end"]            # 2023
_CRAG_CUTOFF = _OUTC_CFG["crag_coverage_cutoff"]  # 2015
HIST = ROOT / "data" / "robustness" / "historical"
OUTC = ROOT / "data" / "robustness" / "outcomes"
OUT = HIST / "holdout_error_forensics.json"

# --- MANUAL, interpretive classification (documented; not computed) ---
# #2 false-alarm external-support mechanism
EXTERNAL_SUPPORT = {
    "Japan": "reserve-currency (yen) + domestic-held debt",
    "Saudi Arabia": "sovereign wealth + oil rents + US security alliance",
    "Cuba": "external patron subsidies + remittances (closed economy)",
    "Croatia": "EU accession 2013 (external anchor)",
    "Bosnia-Herzegovina": "international administration + EU anchor",
    "Argentina": "chronic IMF programs (also DEFAULTED 2014/2020 — label miss)",
    "Ghana": "IMF programs (also DEFAULTED 2022 — label miss)",
    "Mongolia": "IMF 2017 bailout",
    "Equatorial Guinea": "oil rents",
    "Venezuela": "LABEL MISS — collapsed (2017 default, state failure); gate was RIGHT",
    "Brazil": "size + FX reserves + commodity",
    "Fiji": "aid dependence", "Jamaica": "IMF programs",
    "Dominican Republic": "aid/IMF", "Honduras": "aid/remittances",
    "East Timor": "petroleum fund + UN support",
}
# #3 miss external-shock type
EXTERNAL_SHOCK = {
    "Ireland": "2008 GFC banking collapse (external financial contagion; sound institutions)",
    "Greece": "2008 GFC + eurozone rigidity (external financial + currency-union)",
    "Hungary": "2008 GFC financial crisis (external)",
    "Eritrea": "interstate/regional conflict (external)",
    "Malaysia": "Lahad Datu incursion 2013 (external militants)",
    "Yemen": "civil war + Saudi-led intervention 2015 (external military)",
    "Rwanda": "regional spillover (DRC/M23)",
    "Ethiopia": "Tigray war — arguably internal (partial exception)",
    "Mali": "Sahel jihadist insurgency + 2012 Tuareg/Libya spillover (external)",
    "Bolivia": "CRAG default label (2000s); weak/ambiguous",
    "Mauritius": "CRAG default label — questionable (stable economy)",
    "Papua New Guinea": "CRAG default label; commodity/small",
}


def _crag_default_onsets():
    try:
        import pycountry
        iso = lambda n: (pycountry.countries.lookup(n).alpha_3 if _try(n) else None)
    except ImportError:
        return {}
    crag = json.loads((OUTC / "crag_long_parsed.json").read_text())
    byc = defaultdict(dict)
    for r in crag:
        byc[r["country"]][r["year"]] = r["total"]
    out = defaultdict(set)
    for c, ys in byc.items():
        code = _iso(c)
        if not code:
            continue
        prev = 0
        for y in sorted(ys):
            if ys[y] > 0 and prev == 0:
                out[code].add(y)
            prev = ys[y]
    return out


def _iso(n):
    try:
        import pycountry
        return pycountry.countries.lookup(n).alpha_3
    except Exception:
        return None


def _try(n):
    return _iso(n) is not None


def main():
    onsets = json.loads((HIST / "conflict_onsets.json").read_text())["onsets"]
    defs = _crag_default_onsets()
    report = {"caveat": "crisis label misses post-2015 economic collapses (CRAG cutoff 2015); "
                        "some 'false alarms' DID crisis after cutoff — gate right, label blind.",
              "windows": {}}
    for yr, f in ((2004, "temporal_2004_predictions.json"), (2012, "temporal_2012_predictions.json")):
        preds = json.loads((ROOT / "data" / "robustness" / f).read_text())["predictions"]
        FP, FN = [], []
        for p in preds:
            iso, el = p["iso"], p["predictions"]["elevated_crisis_vulnerability"]
            conf = any(yr <= y <= _UCDP_END for y in onsets.get(iso, []))
            deft = any(yr <= y <= _CRAG_CUTOFF for y in defs.get(iso, []))
            cr = conf or deft
            if el and not cr:
                FP.append({"country": p["country"], "external_support": EXTERNAL_SUPPORT.get(p["country"], "UNCLASSIFIED")})
            if (not el) and cr:
                FN.append({"country": p["country"], "crisis": ("conflict" if conf else "") + ("+default" if deft else ""),
                           "external_shock": EXTERNAL_SHOCK.get(p["country"], "UNCLASSIFIED")})
        fp_ext = sum(1 for x in FP if x["external_support"] != "UNCLASSIFIED")
        fn_ext = sum(1 for x in FN if x["external_shock"] != "UNCLASSIFIED" and "internal" not in x["external_shock"])
        report["windows"][yr] = {
            "false_alarms_flagged_no_crisis": {"n": len(FP), "with_external_support": fp_ext, "cases": FP},
            "misses_crisis_not_flagged": {"n": len(FN), "external_shock_or_ambiguous": fn_ext, "cases": FN},
        }
    OUT.write_text(json.dumps(report, indent=2))
    for yr in (2004, 2012):
        w = report["windows"][yr]
        fa = w["false_alarms_flagged_no_crisis"]; ms = w["misses_crisis_not_flagged"]
        print(f"=== {yr}->2024 ===")
        print(f"  #2 false alarms: {fa['n']}, with identifiable external support: {fa['with_external_support']}")
        print(f"  #3 misses: {ms['n']}, external-shock/ambiguous: {ms['external_shock_or_ambiguous']}")
    print(f"\n-> {OUT.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
