#!/usr/bin/env python3
"""
Candidate B — secular conflict-type shift. B1 (gate) govt vs territory incompatibility
composition; B2 signal by conflict type; B3 post-colonial civil conflict. Uses UCDP
`incompatibility` codes as-is (1=territory, 2=government). Frozen spec:
docs/VARIANCE_COMPRESSION_PREREGISTRATION.md. Read-only.
"""
from __future__ import annotations
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts" / "robustness"))
sys.path.insert(0, str(ROOT / "scripts" / "historical"))
import build_conflict_onsets as BCO  # noqa: E402
import erosion_component_B as B  # noqa: E402
from esi_tests import auc_roc  # noqa: E402

UCDP = ROOT / "data/robustness/outcomes/ucdp/UcdpPrioConflict_v24_1.csv"
FORM = ROOT / "data/robustness/formation/state_formation.json"
OUT = ROOT / "data/robustness/varcomp/candidate_B.json"
WINDOW = 25


def _ser(v):
    return json.loads(v) if isinstance(v, str) else v


def intrastate_onsets_by_incompat():
    """iso -> {'gov':set(years), 'terr':set(years)} from UCDP intrastate (type 3/4)."""
    rows = list(csv.DictReader(open(UCDP, encoding="utf-8")))
    # per (gw, conflict_id): incompatibility (constant), active years
    conf_incompat = {}
    gw_conf_years = defaultdict(lambda: defaultdict(set))
    for r in rows:
        if r["type_of_conflict"] not in ("3", "4"):
            continue
        cid = r["conflict_id"]; conf_incompat[cid] = r["incompatibility"]
        for g in r["gwno_loc"].split(","):
            g = g.strip()
            if g.isdigit():
                gw_conf_years[int(g)][cid].add(int(r["year"]))
    out = defaultdict(lambda: {"gov": set(), "terr": set()})
    for g, confs in gw_conf_years.items():
        iso = BCO.GW_ISO.get(g)
        if iso is None:
            continue
        for cid, ys in confs.items():
            inc = conf_incompat[cid]
            for y in ys:
                if (y - 1) not in ys:  # onset
                    if inc == "2":
                        out[iso]["gov"].add(y)
                    elif inc == "1":
                        out[iso]["terr"].add(y)
    return out


def b1_composition(onsets):
    epochs = list(range(1946, 2017, 10))
    per = {}
    for y in epochs:
        gov = sum(1 for iso in onsets for oy in onsets[iso]["gov"] if y <= oy < y + 10)
        terr = sum(1 for iso in onsets for oy in onsets[iso]["terr"] if y <= oy < y + 10)
        tot = gov + terr
        per[y] = {"gov": gov, "terr": terr, "territory_share": round(terr / tot, 3) if tot else None}
    ys = [y for y in epochs if per[y]["territory_share"] is not None]
    shares = [per[y]["territory_share"] for y in ys]
    tr = stats.linregress(ys, shares)
    return {"per_decade": per,
            "territory_share_trend": {"slope": float(tr.slope), "p": float(tr.pvalue)},
            "share_delta": round(shares[-1] - shares[0], 3),
            "gate_pass": bool(tr.slope > 0 and (shares[-1] - shares[0]) >= 0.05)}


def load_rol_gdp():
    vdem = json.loads(B.VDEM.read_text())
    longrun = json.loads(B.LONGRUN.read_text())
    rol = {i: _ser(v["rol"]) for i, v in vdem.items() if "rol" in v}
    gdp = {i: {int(y): val for y, val in _ser(v["P4_gdp"]).items()}
           for i, v in longrun.items() if "P4_gdp" in v}
    return rol, gdp


def b2_signal_by_type(onsets):
    """Erosion curve split by incompatibility type (1946-1996, UCDP era)."""
    rol, gdp = load_rol_gdp()
    res = {}
    for kind in ["gov", "terr"]:
        pts = []
        for y in range(1946, 1997, 10):
            rvals, gvals, labels = [], [], []
            for iso in set(rol) & set(gdp):
                if iso.startswith("OWID"):
                    continue
                r = rol[iso].get(str(y)); g0 = gdp[iso].get(y)
                if r is None or g0 is None or g0 <= 0:
                    continue
                oy_set = onsets.get(iso, {}).get(kind, set())
                lab = 1 if any(y <= oy <= y + WINDOW for oy in oy_set) else 0
                rvals.append(float(r)); gvals.append(-math.log(g0)); labels.append(lab)
            if len(rvals) < 12 or len(set(labels)) < 2:
                pts.append({"year": y, "n_pos": sum(labels), "spread": None})
                continue
            sa = auc_roc([-v for v in rvals], labels)
            wa = auc_roc(gvals, labels)
            pts.append({"year": y, "n_pos": sum(labels), "struct_auc": round(float(sa), 4),
                        "wealth_auc": round(float(wa), 4), "spread": round(float(sa - wa), 4)})
        valid = [(p["year"], p["spread"]) for p in pts if p["spread"] is not None]
        tr = (stats.linregress([v[0] for v in valid], [v[1] for v in valid])
              if len(valid) >= 3 else None)
        res[kind] = {"curve": pts,
                     "spread_trend": ({"slope": float(tr.slope), "p": float(tr.pvalue),
                                       "mean": round(float(np.mean([v[1] for v in valid])), 4)} if tr else None)}
    return res


def b3_postcolonial(onsets):
    form = json.loads(FORM.read_text())
    classes = form.get("states", form)
    grp = {iso: (v.get("group") if isinstance(v, dict) else v) for iso, v in classes.items()}
    # territory share of domestic onsets by formation group (1946+)
    out = {}
    for g in ["mature", "post_colonial", "early_post_colonial"]:
        isos = [iso for iso, gg in grp.items() if gg == g]
        gov = sum(len(onsets[iso]["gov"]) for iso in isos if iso in onsets)
        terr = sum(len(onsets[iso]["terr"]) for iso in isos if iso in onsets)
        tot = gov + terr
        out[g] = {"n_states": len(isos), "gov_onsets": gov, "terr_onsets": terr,
                  "territory_share": round(terr / tot, 3) if tot else None}
    # P1/rol-crisis signal for post-colonial vs mature (pooled 1946-1996, any domestic onset)
    rol, gdp = load_rol_gdp()
    all_dom = defaultdict(set)
    for iso in onsets:
        all_dom[iso] = onsets[iso]["gov"] | onsets[iso]["terr"]
    sig = {}
    for g in ["mature", "post_colonial"]:
        isos = {iso for iso, gg in grp.items() if gg == g}
        rvals, labels = [], []
        for y in range(1946, 1997, 10):
            for iso in (set(rol) & set(gdp) & isos):
                r = rol[iso].get(str(y))
                if r is None:
                    continue
                lab = 1 if any(y <= oy <= y + WINDOW for oy in all_dom.get(iso, set())) else 0
                rvals.append(float(r)); labels.append(lab)
        if len(set(labels)) == 2 and len(rvals) >= 12:
            pb = stats.pointbiserialr(labels, rvals)
            sig[g] = {"n": len(rvals), "n_pos": sum(labels),
                      "rol_crisis_r": round(float(pb.statistic), 4),
                      "struct_auc": round(float(auc_roc([-v for v in rvals], labels)), 4)}
        else:
            sig[g] = {"n": len(rvals), "note": "insufficient"}
    return {"territory_share_by_formation": out, "rol_signal_by_formation": sig}


def main():
    onsets = intrastate_onsets_by_incompat()
    b1 = b1_composition(onsets)
    out = {"candidate": "B_conflict_type_shift", "B1_composition": b1}
    print("=== B1 GATE — domestic conflict composition (territory share) 1946-2016 ===")
    for y, v in b1["per_decade"].items():
        print(f"  {y}: gov={v['gov']} terr={v['terr']} territory_share={v['territory_share']}")
    print(f"  territory-share trend slope={b1['territory_share_trend']['slope']:+.5f} "
          f"p={b1['territory_share_trend']['p']:.3f} Δ={b1['share_delta']}")
    print(f"  >>> B1 GATE PASS: {b1['gate_pass']}")

    # Run B2/B3 regardless (report), but flag if gate failed
    b2 = b2_signal_by_type(onsets)
    b3 = b3_postcolonial(onsets)
    out["B2_signal_by_type"] = b2
    out["B3_postcolonial"] = b3
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1))

    print("\n=== B2 — signal by conflict type (spread over 1946-1996) ===")
    for kind in ["gov", "terr"]:
        t = b2[kind]["spread_trend"]
        line = " ".join(f"{p['year']}:{p['spread'] if p['spread'] is not None else 'NA'}" for p in b2[kind]["curve"])
        print(f"  {kind}: {line}")
        if t:
            print(f"     spread slope={t['slope']:+.6f} p={t['p']:.3f} mean={t['mean']:+.4f}")

    print("\n=== B3 — post-colonial vs mature ===")
    for g, v in b3["territory_share_by_formation"].items():
        print(f"  {g}: terr_share={v['territory_share']} (gov={v['gov_onsets']} terr={v['terr_onsets']}, {v['n_states']} states)")
    for g, v in b3["rol_signal_by_formation"].items():
        print(f"  {g} rol->crisis: {v}")


if __name__ == "__main__":
    main()
