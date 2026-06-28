#!/usr/bin/env python3
"""
big_signals_scan.py — V3.2 signals across the full 180-country panel.

Operationalizes (A) the Convergence Qualifier on Safeguard J's durability gap (P4-P1 level + its
TRAJECTORY: closing=developmental catch-up vs widening=fragility) and (B) the Accountability Gap
(VA vs income; "capacity without consent" — HYPOTHESIS) for any panel country, reading the committed
mi_pipeline panel + data/sources/va_anchored.json. Breadth tool — distinct from the per-case engine.

Usage:
  python scripts/big_signals_scan.py --country China
  python scripts/big_signals_scan.py --set g20        # G7+G10+G20
  python scripts/big_signals_scan.py --set panel --flagged-only
"""
import argparse, csv, json, os, sys
from pathlib import Path

MI = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(MI))
from mi.constants import LENS  # noqa: E402

PANEL = Path(os.environ.get("MI_PANEL_DIR", MI.parent / "mi_pipeline" / "data")).parent / "output" / "mi_scored_countries.csv"
VA = json.load(open(MI / "data" / "sources" / "va_anchored.json"))
GSET = ["USA","CAN","GBR","FRA","DEU","ITA","JPN","BEL","NLD","SWE","CHE","ARG","AUS","BRA","CHN",
        "IND","IDN","MEX","RUS","SAU","ZAF","KOR","TUR"]

rows = {(r["iso3"], r["year"]): r for r in csv.DictReader(open(PANEL, encoding="latin-1"))}
names = {r["iso3"]: r["country"] for r in rows.values()}
def fnum(x):
    try: return float(x)
    except (TypeError, ValueError): return None

def gap(iso, y):
    r = rows.get((iso, y))
    if not r: return None
    p1, p4 = fnum(r["P1"]), fnum(r["P4"])
    return (p4 - p1) if (p1 is not None and p4 is not None) else None

def j_status(g):
    return "FLAGGED" if g >= LENS["structural_vuln_flag_floor"] else \
           "clear" if g <= LENS["structural_vuln_clear_ceiling"] else "BORDERLINE"

def convergence(iso, y_now="2024", y_prior="2012"):
    g1, g0 = gap(iso, y_now), gap(iso, y_prior)
    if g1 is None or g0 is None: return None, None
    dg = g1 - g0; dead = LENS["structural_vuln_converge_deadband"]
    return dg, ("widening" if dg > dead else "closing" if dg < -dead else "static")

def acct(iso, y="2024"):
    va = VA.get(iso, {}).get(y); g4 = None
    r = rows.get((iso, y))
    p4 = fnum(r["P4"]) if r else None
    if va is None or p4 is None: return None
    va01 = va / 100.0; vp4 = va01 - p4
    st = "legitimacy_capped" if vp4 <= LENS["va_legitimacy_cap_p4"] else \
         "accountability_lag" if vp4 <= LENS["va_accountability_lag_p4"] else "balanced"
    return va01, vp4, st

PILL = ["P1", "P2", "P3", "P4", "P5"]
def _pillars(iso, y):
    r = rows.get((iso, y))
    if not r:
        return None
    v = {p: fnum(r[p]) for p in PILL}
    return v if all(x is not None for x in v.values()) else None

def movement(iso, y_now="2024", y_prior="2012"):
    """EXPLORATORY movement typology (docs/movement_signal_exploration.md). Descriptive, not a
    validated predictor: real_ascent (P1/P5-led rise) / windfall (P4-led rise, institutions flat) /
    hollow_stability (flat MI, governance core P1 eroding under the P3 ratchet) / decline / stable."""
    a, b = _pillars(iso, y_prior), _pillars(iso, y_now)
    if not a or not b:
        return None
    dmi = sum(b.values()) / 5 - sum(a.values()) / 5
    dp = {p: b[p] - a[p] for p in PILL}
    lead = max(dp, key=dp.get)
    if dmi > 0.03:
        cls = ("real_ascent" if lead in ("P1", "P5")
               else "windfall" if lead == "P4"
               else "ratchet_rise")   # P2/P3-led: human-capital/innovation, not income or institutions
    elif dmi < -0.03:
        cls = "decline"
    elif dp["P1"] <= -0.03:
        cls = "hollow_stability"
    else:
        cls = "stable"
    return {"dMI": round(dmi, 3), "lead": lead, "dP1": round(dp["P1"], 3),
            "dP3": round(dp["P3"], 3), "dP4": round(dp["P4"], 3), "class": cls}

def report_movement(iso):
    m = movement(iso)
    if not m:
        print(f"{names.get(iso, iso):16} no movement data"); return
    print(f"{names.get(iso, iso):16} {m['class']:16} dMI={m['dMI']:+.3f} lead={m['lead']} "
          f"dP1={m['dP1']:+.2f} dP3={m['dP3']:+.2f} dP4={m['dP4']:+.2f}")

def report(iso):
    g = gap(iso, "2024")
    if g is None:
        print(f"{names.get(iso, iso):16} no 2024 panel data"); return
    dg, direction = convergence(iso)
    a = acct(iso)
    js = j_status(g)
    refined = ""
    if js in ("FLAGGED", "BORDERLINE") and direction:
        refined = "developmental_catchup" if direction == "closing" else "fragile"
    va_s = f"VA={a[0]:.2f} VA-P4={a[1]:+.2f} {a[2]}" if a else "VA=n/a"
    dgs = f"dgap={dg:+.2f} {direction}" if dg is not None else "dgap=n/a"
    print(f"{names.get(iso, iso):16} gap={g:+.2f} [{js}] {dgs} {('-> '+refined) if refined else '':24} {va_s}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--country")
    ap.add_argument("--set", choices=["g20", "panel"])
    ap.add_argument("--flagged-only", action="store_true")
    ap.add_argument("--movement", action="store_true",
                    help="EXPLORATORY movement typology (real_ascent/windfall/hollow_stability/decline)")
    args = ap.parse_args()
    rep = report_movement if args.movement else report
    if args.country:
        iso = args.country if args.country in rows or args.country in VA else \
              next((i for i, n in names.items() if n.lower() == args.country.lower()), args.country)
        rep(iso)
    else:
        isos = GSET if args.set == "g20" else sorted({i for i, _ in rows})
        print(("EXPLORATORY movement typology — docs/movement_signal_exploration.md" if args.movement
               else "V3.2 signals — durability gap + convergence (A) + accountability gap (B)") + "\n")
        for iso in isos:
            if args.movement:
                rep(iso); continue
            g = gap(iso, "2024")
            if g is None: continue
            if args.flagged_only and g < LENS["structural_vuln_clear_ceiling"]: continue
            report(iso)
