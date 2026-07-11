#!/usr/bin/env python3
"""
Decoupling program — shared MI five-point pillar panel builder.

Reads the committed engine + canonical panel and materializes P1/P3/P4 (+P4* =
GDP-decontaminated) and log GDP for every country at 1996/2004/2012/2018/2024.
Read-only w.r.t. the engine. Frozen spec: docs/DECOUPLING_PREREGISTRATION.md (F1).

Emits:
  data/robustness/decoupling/mi_5pt_panel.json
    { years, balanced:[iso...], rows: { iso: { name, year: {P1,P3,P4,P4star,logGDP,gdp} } } }
"""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from mi import panel  # noqa: E402
from mi.scoring import (  # noqa: E402
    calculate_pillar_scores,
    normalize_resource_rents,
    normalize_oda,
)

YEARS = [1996, 2004, 2012, 2018, 2024]
OUT = ROOT / "data" / "robustness" / "decoupling" / "mi_5pt_panel.json"


def p4star(ind: dict):
    """P4 with GDP removed: mean of normalized resource_rents + ODA only."""
    vals = []
    r = ind.get("resource_rents_pct_gdp")
    if r is not None:
        vals.append(normalize_resource_rents(r))
    o = ind.get("oda_pct_gni")
    if o is not None:
        vals.append(normalize_oda(o))
    return sum(vals) / len(vals) if vals else None


def build():
    canon = panel._canonical()
    rows = {}
    for iso, rec in canon.items():
        name = rec["name"]
        yr = {}
        for y in YEARS:
            ind = panel.indicators_for(iso, y)
            if not ind:
                continue
            gdp = ind.get("gdp_per_capita_ppp")
            try:
                pil = calculate_pillar_scores(ind)
            except Exception:
                pil = None
            entry = {
                "P1": pil.get("P1") if pil else None,
                "P3": pil.get("P3") if pil else None,
                "P4": pil.get("P4") if pil else None,
                "P4star": p4star(ind),
                "gdp": gdp,
                "logGDP": math.log10(gdp) if (gdp and gdp > 0) else None,
            }
            yr[str(y)] = entry
        if yr:
            rows[iso] = {"name": name, "years": yr}
    balanced = sorted(
        iso for iso, r in rows.items()
        if all(
            str(y) in r["years"]
            and r["years"][str(y)]["P1"] is not None
            and r["years"][str(y)]["logGDP"] is not None
            for y in YEARS
        )
    )
    out = {"years": YEARS, "n_balanced": len(balanced),
           "balanced": balanced, "rows": rows}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1))
    return out


def load():
    if not OUT.exists():
        return build()
    return json.loads(OUT.read_text())


if __name__ == "__main__":
    o = build()
    print(f"wrote {OUT.relative_to(ROOT)}: {len(o['rows'])} countries, "
          f"{o['n_balanced']} balanced")
