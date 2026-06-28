"""
Relational / Exposure Tier (T3) — a THIRD measurement tier, firewalled from the MI.

Where the country-level MI measures how a polity is built INTERNALLY (P1-P5), and the system-level
Global Systems Measurement measures the world system, T3 measures a polity's RELATIONAL position:
how exposed it is to externally-imposed shock (invasion/conquest), and how well it could absorb one.

It exists because the MI is an internal instrument and is therefore blind to exogenous conflict — the
signal lives in a relational layer BETWEEN units that the internal instrument never had. T3 is that
layer. It turns "an external power defeated us" (a flat miss) into "conditioned on exposure" (a
consistency hit): Cyprus 1974 was internally OK-ish but highly exposed with no credible patron ->
invaded; South Korea is comparably exposed but patron-shielded -> persists.

HARD DISCIPLINE (see docs/relational_tier_spec.md):
  - FIREWALLED & ADDITIVE: T3 READS the MI pillars (P1, P5) and external relational data; it NEVER
    writes a pillar/safeguard/score, and run_retrodiction.py --validate never imports it. The
    213/77/0 baseline path is byte-for-byte independent of this module.
  - NOT A VERDICT-CHANGER: output is two indices (Exposure E, Response R) + a joint reading. No MI
    delta, no pass/fail.
  - RISK GAUGE, NOT A WAR-PREDICTOR: E conditions on WHO is exposed; it does NOT call WHEN a war
    starts. The initiator's decision is the irreducible kernel ("trust the level, distrust the slope"
    on the relational layer). E is a standing probabilistic exposure, never a forecast.
  - THREE PROVENANCE TIERS surfaced on every output: citable (COW/ATOP/ICOW/SIPRI, >=1816) >
    historical-proxy (Maddison economic mass + V-Dem, pre-1816 real data) > interpreted (hindsight).
    Only citable-tier records may enter a clean-proof claim.

Deterministic, pure-Python stdlib. Mirrors the durability.py / global_systems.py tier pattern.
"""
import json
import statistics as st
from pathlib import Path

from mi import datasource as ds
from mi.scoring import score_country

_SRC = Path(__file__).resolve().parent.parent / "data" / "sources" / "relational"

# --- pre-registered constants (fixed here, not tuned) ---
BAND_LOW = 0.33          # [0, 0.33) low
BAND_HIGH = 0.66         # [0.33, 0.66) moderate ; [0.66, 1.0] high
E4_CONFLICT_CAP = 3      # neighborhood conflicts saturating the [0,1] component
R4_DEPTH_ANCHOR_KM2 = 500_000.0  # area at/above which strategic depth saturates (~France-scale)


def _load(name):
    try:
        return json.load(open(_SRC / name))
    except FileNotFoundError:
        return {}


def _band(x):
    if x is None:
        return "n/a"
    if x < BAND_LOW:
        return "low"
    return "moderate" if x < BAND_HIGH else "high"


def load_records():
    """All T3 records across the citable and historical-proxy tiers, keyed 'Unit@Year'."""
    recs = {}
    for fname in ("exposure_inputs.json", "historical_proxy_inputs.json"):
        d = _load(fname)
        for k, v in d.items():
            if k == "_meta":
                continue
            recs[k] = v
    return recs


# ----------------------------------------------------------------------------- exposure (E1-E5)
def _e1_relative_power(blk):
    """Relative military/material power vs the most-capable plausible adversary. Higher = weaker = more exposed."""
    method = blk.get("method")
    if method == "cinc":
        own = blk["own_cinc"]
        adv = blk["adversary_cinc"]
        denom = own + adv
        return (adv / denom) if denom else None
    if method == "economic_mass":
        own = blk["own"]["gdppc"] * blk["own"]["population_millions"]
        adv = sum(a["gdppc"] * a["population_millions"] for a in blk["adversaries"])
        denom = own + adv
        return (adv / denom) if denom else None
    return None


def _patron_strength(exposure):
    """1.0 if a credible external defender exists, else 0.0. Shared by E2 (deters) and R3 (blunts)."""
    return 1.0 if exposure.get("E2_patron", {}).get("credible_external_defender") else 0.0


def compute_exposure(record):
    """Exposure indices in [0,1] (higher = more exposed).

    Two numbers, because the patron acts on two distinct things (see spec A1, the double-count):
      - E_structural: the raw external ADVERSITY a unit faces (E1 power, E3 border, E4 neighborhood,
        E5 faultline) — patron-INDEPENDENT. "How exposed are you, ignoring who protects you."
      - E (net): structural adversity AFTER the patron's DETERRENCE (adds E2). "How likely is a shock
        actually attempted." A credible patron lowers E below E_structural.
    The patron's BLUNTING effect (separate from deterrence) lives on the Response axis (R3). Splitting
    deterrence (E) from blunting (R) while keeping structural adversity (E_structural) visible is what
    makes 'exposed but shielded' legible: Cyprus and South Korea have near-identical E_structural; the
    patron is the entire difference.
    """
    ex = record["exposure"]
    e1 = _e1_relative_power(ex["E1_relative_power"])
    patron_present = _patron_strength(ex) == 1.0
    e2 = 1.0 - _patron_strength(ex)                                  # no patron -> more exposed (deterrence)
    e3 = 1.0 if ex["E3_contested_border"].get("active_claim_against") else 0.0
    e4 = min(ex["E4_neighborhood"].get("active_conflicts_contiguous", 0) / E4_CONFLICT_CAP, 1.0)
    e5 = 1.0 if ex["E5_great_power_faultline"].get("on_faultline") else 0.0
    comps = {"E1_relative_power": e1, "E2_patron_deterrence": e2, "E3_contested_border": e3,
             "E4_neighborhood": e4, "E5_great_power_faultline": e5}
    structural = [v for k, v in comps.items() if k != "E2_patron_deterrence" and v is not None]
    net = [v for v in comps.values() if v is not None]
    E_struct = sum(structural) / len(structural) if structural else None
    E_net = sum(net) / len(net) if net else None
    return {"E": E_net, "band": _band(E_net),
            "E_structural": E_struct, "structural_band": _band(E_struct),
            "patron_present": patron_present, "components": comps}


# ----------------------------------------------------------------------------- response (R1-R4)
def _get_pillars(unit, year, record):
    """P1/P5 for the response axis. Recorded internal_pillars first (historical), else LIVE Data API."""
    rec_p = record.get("internal_pillars", {})
    p1, p5 = rec_p.get("P1"), rec_p.get("P5")
    if p1 is not None or p5 is not None:
        return {"P1": p1, "P5": p5}, f"recorded internal read ({record.get('provenance_tier','?')} tier)"
    # live read
    for y in (year, 2018, 2024, 2012):
        ind = ds.get_indicators(unit, y)
        if ind:
            ps = score_country(ind, event_year=y)["pillar_scores"]
            return {"P1": ps.get("P1"), "P5": ps.get("P5")}, f"live Data API @ {y}"
    return {"P1": None, "P5": None}, "unavailable"


def compute_response(record, unit, year):
    """Response index R in [0,1] (higher = better able to absorb a shock), equal-weighted mean of available sub-indicators."""
    pillars, p_src = _get_pillars(unit, year, record)
    ex = record["exposure"]
    r1 = pillars.get("P5")                                           # cohesion
    r2 = pillars.get("P1")                                           # mobilization capacity
    r3 = _patron_strength(ex)                                        # patron intervention credibility
    depth_blk = record.get("response", {}).get("R4_strategic_depth", {})
    area = depth_blk.get("area_km2")
    r4 = min(area / R4_DEPTH_ANCHOR_KM2, 1.0) if area else None      # strategic depth
    comps = {"R1_cohesion_P5": r1, "R2_mobilization_P1": r2,
             "R3_patron_credibility": r3, "R4_strategic_depth": r4}
    present = [v for v in comps.values() if v is not None]
    R = sum(present) / len(present) if present else None
    return {"R": R, "band": _band(R), "components": comps, "pillar_source": p_src}


# ----------------------------------------------------------------------------- joint reading
def _joint_reading(E_struct, R, patron_present):
    """Placement on (structural exposure x response), with the patron as the bridge between them.
    Keyed on E_structural (raw adversity) not net E, so 'exposed but shielded' stays visible.
    Descriptive only — NO verdict, NO MI delta."""
    if E_struct is None or R is None:
        return "insufficient data for a joint reading."
    sb, rb = _band(E_struct), _band(R)
    if sb == "high" and patron_present:
        return ("HIGH structural exposure but PATRON-SHIELDED: raw adversity is severe, yet a credible "
                "external defender both DETERS the shock (lowers net exposure) and BLUNTS it (lifts response). "
                "Persistence despite exposure is the expected reading here (e.g. South Korea).")
    if sb == "high" and not patron_present and rb in ("low", "moderate"):
        return ("HIGH structural exposure + NO patron + weak response: standing vulnerability to "
                "externally-imposed shock that the internal MI does not see. If a shock lands, little absorbs "
                "it. This is the configuration that turns an internal 'OK' read into an external miss — "
                "Cyprus 1974, Poland-Lithuania 1772.")
    if sb == "high" and not patron_present and rb == "high":
        return ("HIGH structural exposure + NO patron, but strong INTERNAL response (cohesion/capacity): "
                "can survive a shock on its own resources (the cohesion-shielded path, e.g. Finland 1939).")
    if sb in ("low", "moderate"):
        return f"structural exposure={sb}, response={rb}: relationally lower-risk on this axis."
    return f"structural exposure={sb}, response={rb}: read the components."


def relational_reading(unit, year=None, record=None):
    """Full T3 reading for a unit. Pass a record directly, or look it up by 'Unit@Year' / unit+year."""
    if record is None:
        recs = load_records()
        key = f"{unit}@{year}" if year is not None else unit
        record = recs.get(key)
        if record is None and year is None:
            # bare unit name given — find the (single) matching 'Unit@Year' key
            matches = [k for k in recs if k.split("@")[0] == unit]
            if len(matches) == 1:
                key = matches[0]
                unit, year = key.split("@")[0], int(key.split("@")[1])
                record = recs[key]
        if record is None:
            raise KeyError(f"no T3 record for '{key}'. Available: {sorted(recs)}")
    exposure = compute_exposure(record)
    response = compute_response(record, unit, year)
    return {
        "unit": unit,
        "year": year,
        "provenance_tier": record.get("provenance_tier", "unknown"),
        "label": record.get("label", ""),
        "exposure": exposure,
        "response": response,
        "joint_reading": _joint_reading(exposure["E_structural"], response["R"], exposure["patron_present"]),
        "outcome_factual": record.get("outcome_factual", ""),
        "DISCLAIMER": ("Risk gauge, NOT a war-predictor: conditions on WHO is exposed, not WHEN a war "
                       "starts. Firewalled from the MI — reads pillars, changes no MI score. "
                       f"Provenance tier: {record.get('provenance_tier','unknown')}."),
    }
