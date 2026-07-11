#!/usr/bin/env python3
"""
Contagion — Test 1: re-derive conflict onsets WITH a domestic/external origin tag,
using the SAME inclusion logic as build_conflict_onsets.py, and verify the union
reproduces the committed baseline (143 iso, 1176 events). Frozen scheme:
docs/CONTAGION_PREREGISTRATION.md.

Primary: DOMESTIC = COW intra + UCDP type 3/4 ; EXTERNAL = COW inter + UCDP type 1/2.
Sensitivity variants (S1 type4->external, S2 type1->excluded) also materialized.
Writes data/robustness/contagion/crisis_classification.json.
"""
from __future__ import annotations
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts" / "historical"))
import build_conflict_onsets as BCO  # noqa: E402  (GW_ISO, build_ccode_iso)

OUTC = ROOT / "data" / "robustness" / "outcomes"
COW = OUTC / "cow"
COMMITTED = ROOT / "data" / "robustness" / "historical" / "conflict_onsets.json"
OUT = ROOT / "data" / "robustness" / "contagion" / "crisis_classification.json"

# UCDP type_of_conflict -> origin (primary scheme)
UCDP_ORIGIN = {"1": "external", "2": "external", "3": "domestic", "4": "domestic"}


def ucdp_typed():
    """(iso, year) -> set of origins, per committed onset logic, tagged by type.
    Also S1 (type4->external) and S2 (type1 excluded) variants."""
    rows = list(csv.DictReader(open(OUTC / "ucdp" / "UcdpPrioConflict_v24_1.csv", encoding="utf-8")))
    conf_type = {}
    gw_conf_years = defaultdict(lambda: defaultdict(set))
    for r in rows:
        y = int(r["year"]); cid = r["conflict_id"]
        conf_type[cid] = r["type_of_conflict"]
        for g in r["gwno_loc"].split(","):
            g = g.strip()
            if g.isdigit():
                gw_conf_years[int(g)][cid].add(y)
    # onset per conflict per gw
    events = []  # (iso, year, source, type, origin_primary, origin_s1, origin_s2)
    for g, confs in gw_conf_years.items():
        iso = BCO.GW_ISO.get(g)
        if iso is None:
            continue
        for cid, ys in confs.items():
            t = conf_type[cid]
            for y in ys:
                if (y - 1) not in ys:  # onset
                    prim = UCDP_ORIGIN[t]
                    s1 = "external" if t == "4" else prim
                    s2 = None if t == "1" else prim  # S2 excludes extrasystemic
                    events.append((iso, y, "ucdp", f"ucdp_type{t}", prim, s1, s2))
    return events


def cow_typed():
    ccode_iso = BCO.build_ccode_iso()[0] if isinstance(BCO.build_ccode_iso(), tuple) else BCO.build_ccode_iso()
    events = []

    def add(cc_raw, years, source, origin):
        cc = (cc_raw or "").strip()
        if not (cc and cc.lstrip("-").isdigit()):
            return
        cc = int(cc)
        if cc <= 0:
            return
        iso = ccode_iso.get(cc)
        if iso is None:
            return
        for y in years:
            events.append((iso, y, source, source, origin, origin, origin))

    for r in csv.DictReader(open(COW / "Inter-StateWarData_v4.0.csv", encoding="latin-1")):
        ys = BCO._years_from_row(r, ["StartYear1", "StartYear2"])
        add(r.get("ccode"), ys, "cow_inter", "external")
    for r in csv.DictReader(open(COW / "Intra-StateWarData_v4.1.csv", encoding="latin-1")):
        ys = BCO._years_from_row(r, ["StartYear1", "StartYear2"])
        add(r.get("CcodeA"), ys, "cow_intra", "domestic")
        add(r.get("CcodeB"), ys, "cow_intra", "domestic")
    return events


def build():
    events = ucdp_typed() + cow_typed()
    # aggregate to (iso, year) -> origin sets for primary + sensitivity
    def agg(field_idx):
        m = defaultdict(set)
        for e in events:
            origin = e[field_idx]
            if origin is None:
                continue
            m[(e[0], e[1])].add(origin)
        return m
    prim = agg(4); s1 = agg(5); s2 = agg(6)

    # per-iso year lists (union) to verify against committed baseline
    union = defaultdict(set)
    for (iso, y) in prim:
        union[iso].add(y)
    union = {iso: sorted(ys) for iso, ys in union.items()}

    # committed baseline check
    committed = json.loads(COMMITTED.read_text())["onsets"]
    comm_pairs = {(iso, y) for iso, ys in committed.items() for y in ys}
    mine_pairs = set(prim.keys())
    missing = comm_pairs - mine_pairs   # in committed, not reproduced
    extra = mine_pairs - comm_pairs     # reproduced, not in committed

    def serial(m):
        return {f"{iso}|{y}": sorted(origins) for (iso, y), origins in
                sorted(m.items())}

    out = {
        "scheme": "DOMESTIC=COW intra + UCDP type3/4; EXTERNAL=COW inter + UCDP type1/2",
        "baseline_check": {
            "committed_pairs": len(comm_pairs), "reproduced_pairs": len(mine_pairs),
            "missing_from_repro": len(missing), "extra_vs_committed": len(extra),
            "missing_examples": sorted(f"{i}|{y}" for i, y in missing)[:15],
            "extra_examples": sorted(f"{i}|{y}" for i, y in extra)[:15],
        },
        "counts": {
            "total_onset_pairs": len(prim),
            "domestic_pairs": sum(1 for o in prim.values() if "domestic" in o),
            "external_pairs": sum(1 for o in prim.values() if "external" in o),
            "both_pairs": sum(1 for o in prim.values() if len(o) == 2),
        },
        "classification_primary": serial(prim),
        "classification_S1_type4_external": serial(s1),
        "classification_S2_type1_excluded": serial(s2),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=0))
    return out


if __name__ == "__main__":
    o = build()
    bc = o["baseline_check"]; c = o["counts"]
    print("=== crisis classification (Test 1) ===")
    print(f"committed pairs={bc['committed_pairs']} reproduced={bc['reproduced_pairs']} "
          f"missing={bc['missing_from_repro']} extra={bc['extra_vs_committed']}")
    if bc["missing_from_repro"] or bc["extra_vs_committed"]:
        print("  missing ex:", bc["missing_examples"])
        print("  extra ex:", bc["extra_examples"])
    print(f"onset pairs={c['total_onset_pairs']} | domestic={c['domestic_pairs']} "
          f"external={c['external_pairs']} both={c['both_pairs']}")
