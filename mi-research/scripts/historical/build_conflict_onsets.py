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
import sys
from collections import defaultdict
from pathlib import Path

import pycountry

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from lib.iso_map import GW_ISO_EXTENDED as GW_ISO, COW_NAME_MANUAL  # noqa: E402

OUTC = ROOT / "data" / "robustness" / "outcomes"
COW = OUTC / "cow"
OUT = ROOT / "data" / "robustness" / "historical" / "conflict_onsets.json"

# GW_ISO (Gleditsch-Ward -> ISO3, extended) and COW_NAME_MANUAL now live in lib/iso_map.py.


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
