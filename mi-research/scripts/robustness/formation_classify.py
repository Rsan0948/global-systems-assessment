#!/usr/bin/env python3
"""
Component A / Test A1 — STATE-FORMATION CLASSIFICATION (pre-registered).

Classifies every state in the erosion panel (COW/V-Dem/Maddison) + the temporal
holdout into a formation TYPE, using the Correlates of War State System
Membership file (states2016.csv) for the entry-year anchor and a documented,
hand-coded decolonization / institutional-tradition overlay for the TYPE.

This file IS the pre-registration of the classification. It is committed BEFORE
any split of an outcome curve is computed (Test A2/A3/A4). Every non-mechanical
call is spelled out with a one-line rationale in NOTES, and every genuinely
ambiguous case carries a FLAG so A2/A3 can be re-run with the flagged cases moved
to the other group (sensitivity analysis). The primary binary is:

  mature  = the population had prior multi-generational experience operating
            political institutions at or near the scale of the current state
            (pre-1816 sovereign; organic unification; revolution from internal
            institutional traditions; treaty partition with deep continuity;
            never-colonized deep states; settler dominions whose administrative
            class stayed; brief-but-real interwar sovereignty, e.g. the Baltics).

  post_colonial = independence >=1945 from a colonial power that drew the borders
            and removed the administrative class, OR imperial-dissolution
            successor with NO prior independent institutional tradition at its
            current scale (e.g. the Central Asian republics).

  early_post_colonial = the Latin-American / Iberian-colonial bloc that became
            independent c.1804-1903 — post-colonial by origin but with 120-220
            years of subsequent sovereign institutional development (the brief's
            explicit third group).

Groups are assigned per-state below. `india` is additionally flagged so A2/A3 run
it in EACH group separately (brief instruction). Read-only; writes its own JSON.
"""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "historical"))
from build_conflict_onsets import build_ccode_iso  # noqa: E402  (ccode -> ISO3)

COW = ROOT / "data" / "robustness" / "outcomes" / "cow" / "states2016.csv"
OUT = ROOT / "data" / "robustness" / "formation" / "state_formation.json"

# ---------------------------------------------------------------------------
# The classification.  group in {mature, post_colonial, early_post_colonial}.
# flags: free-form tags used for sensitivity re-runs. `alt_group` names the group
# the case moves to under the sensitivity analysis (None = solid, do not move).
# ---------------------------------------------------------------------------
LATAM_EARLY = {  # Iberian/French-colonial bloc, independence c.1804-1903
    "ARG", "BOL", "BRA", "CHL", "COL", "CRI", "CUB", "DOM", "ECU", "SLV",
    "GTM", "HTI", "HND", "MEX", "NIC", "PAN", "PRY", "PER", "URY", "VEN",
}

# Clearly mature: pre-1816 European core, organic unifications, never-colonized
# deep states, settler dominions, treaty-continuity splits, Baltic interwar.
MATURE = {
    # European institutional core / pre-1816 sovereign
    "AUT", "BEL", "CHE", "DNK", "ESP", "FRA", "GBR", "ITA", "DEU", "LUX",
    "NLD", "PRT", "RUS", "SWE", "NOR", "ISL", "FIN",
    # organic unification / national-revival with deep prior statehood
    "GRC", "ROU", "BGR", "HUN", "POL", "IRL", "TUR", "CZE", "SVK", "SRB",
    # Baltic — brief but real interwar sovereignty (brief: -> mature)
    "EST", "LVA", "LTU",
    # never-colonized deep Asian/African statehood
    "JPN", "CHN", "THA", "IRN", "ETH", "NPL", "AFG", "MNG",
    "KOR", "PRK", "TWN",
    # settler dominions (administrative class stayed) + US internal-tradition
    "USA", "CAN", "AUS", "NZL", "ZAF",
    # deep-state / organic-unification edges (flagged below)
    "EGY", "MAR", "OMN", "SAU", "LBR",
    # Yugoslav successors with strong inherited institutions (flagged)
    "SVN", "HRV",
}

# Everything else in the universe is post_colonial unless in the sets above.
# Explicit NOTES + FLAGS for judgment calls (documented per brief).
NOTES = {
    # --- flagged mature edges (sensitivity: could move to post_colonial) ---
    "FIN": ("mature", "post_colonial", "flag_autonomy",
            "Grand-Duchy autonomy + strong civil society before 1917; deep Nordic institutional embedding."),
    "GRC": ("mature", "post_colonial", "flag_revival",
            "1828 independence from Ottomans; classical/European institutional import + national-revival elite."),
    "ROU": ("mature", "post_colonial", "flag_revival",
            "1859/1878 union of principalities with continuous boyar/administrative tradition."),
    "BGR": ("mature", "post_colonial", "flag_revival",
            "Medieval statehood + 1878 autonomous principality; national-revival institutions."),
    "ALB": ("mature", "post_colonial", "flag_revival",
            "Ottoman-successor European state, independence 1912-13; national-revival elite (parallels GRC/BGR)."),
    "IRL": ("mature", None, "flag_uk_embedding",
            "Deep institutional embedding in the British system + Home-Rule tradition; admin class continuous."),
    "POL": ("mature", None, "flag_restored",
            "1918 restored state with deep pre-partition (Commonwealth) institutional tradition at scale."),
    "MNG": ("mature", "post_colonial", "flag_constructed_1921",
            "Continuous steppe/Buddhist theocratic statehood but 1921 state consolidated under Soviet tutelage."),
    "KOR": ("mature", None, "flag_colonial_interruption",
            "Deep Joseon statehood at scale; Japanese colonial interruption 1910-45; strong post-war build."),
    "PRK": ("mature", None, "flag_colonial_interruption",
            "Same Joseon statehood tradition; colonial interruption 1910-45."),
    "TWN": ("mature", None, "flag_roc_relocation",
            "Governed by the ROC — a state with deep mainland Chinese institutional tradition; sui generis."),
    "ZAF": ("mature", None, "flag_settler",
            "Settler-administered continuous institutions since 1910 (Union); admin class stayed (apartheid notwithstanding)."),
    "EGY": ("mature", "post_colonial", "flag_deep_state",
            "Ancient/Ottoman-Khedival bureaucratic tradition; heavy British influence 1882-1952; genuinely ambiguous."),
    "MAR": ("mature", "post_colonial", "flag_protectorate",
            "Continuous Alaouite/Makhzen statehood since 1600s; French/Spanish protectorate 1912-56 (not full colony)."),
    "TUN": ("post_colonial", "mature", "flag_protectorate",
            "Husainid Beylik under Ottoman suzerainty then French protectorate 1881-1956; weaker continuous-sovereignty claim than MAR."),
    "OMN": ("mature", "post_colonial", "flag_dynastic",
            "Continuous Omani sultanate/empire; British influence but never a formal colony/protectorate at scale."),
    "SAU": ("mature", "post_colonial", "flag_organic_unification_1932",
            "Never colonized; 1932 organic conquest-unification (Al Saud) rather than institutional continuity."),
    "LBR": ("mature", "post_colonial", "flag_settler_founded_1847",
            "Freed-American-settler republic since 1847; never decolonized; weak institutional depth (ambiguous)."),
    "SVN": ("mature", "post_colonial", "flag_dissolution_strong_inst",
            "Habsburg embedding + Yugoslav republic-level administration; wealthy, strong institutions; no prior INDEPENDENT sovereignty."),
    "HRV": ("mature", "post_colonial", "flag_dissolution_strong_inst",
            "Habsburg embedding + Yugoslav republic-level administration; no prior independent sovereignty at scale."),
    "SRB": ("mature", None, "flag_dissolution_continuity",
            "Continuity with the independent pre-1914 Kingdom of Serbia (mature tradition)."),
    "CZE": ("mature", None, "flag_treaty_split",
            "1993 velvet split; deep Bohemian/Habsburg + interwar-Czechoslovak institutional continuity."),
    "SVK": ("mature", None, "flag_treaty_split",
            "1993 velvet split; interwar + federal Czechoslovak institutional continuity."),
    "NOR": ("mature", None, "flag_treaty_1905",
            "1905 treaty separation from Sweden with deep continuous institutions (brief's mature exemplar)."),
    "USA": ("mature", None, "flag_revolution",
            "1776 revolution establishing governance from internal institutional traditions (brief's mature exemplar)."),
    "CAN": ("mature", None, "flag_settler",
            "Settler dominion; British-derived institutions continuously operated by a resident administrative class."),
    "AUS": ("mature", None, "flag_settler", "Settler dominion; continuous resident administrative class."),
    "NZL": ("mature", None, "flag_settler", "Settler dominion; continuous resident administrative class."),
    "AFG": ("mature", None, "flag_never_colonized", "Never colonized buffer state; long continuous monarchy."),
    "ETH": ("mature", None, "flag_never_colonized", "Never colonized (Italian occupation 1936-41 only); ancient continuous state."),
    "THA": ("mature", None, "flag_never_colonized", "Never colonized; continuous Siamese/Thai monarchy-state."),
    "JPN": ("mature", None, "flag_never_colonized", "Never colonized; continuous state, Meiji institutional build."),
    "CHN": ("mature", None, "flag_never_colonized", "Continuous imperial-bureaucratic tradition; never fully colonized."),
    "IRN": ("mature", None, "flag_never_colonized", "Continuous Persian statehood; never formally colonized."),
    "NPL": ("mature", None, "flag_never_colonized", "Never colonized; continuous Himalayan monarchy."),

    # --- flagged post_colonial edges (sensitivity: could move to mature) ---
    "IND": ("post_colonial", "mature", "flag_india_special",
            "Deep pre-colonial institutional traditions but current borders + unified administration are colonial; brief: run in BOTH groups."),
    "KWT": ("post_colonial", "mature", "flag_gulf_protectorate",
            "British protectorate to 1961 with continuous Al Sabah dynastic rule; local governance tradition below sovereign scale."),
    "QAT": ("post_colonial", "mature", "flag_gulf_protectorate", "British protectorate to 1971; Al Thani dynastic rule."),
    "BHR": ("post_colonial", "mature", "flag_gulf_protectorate", "British protectorate to 1971; Al Khalifa dynastic rule."),
    "ARE": ("post_colonial", "mature", "flag_gulf_protectorate", "1971 federation of Trucial protectorate emirates."),
    "YEM": ("post_colonial", "mature", "flag_mixed_north_south",
            "North (Ottoman/imamate, uncolonized) + South (British Aden colony) unified 1990; constructed unification."),
    "ISR": ("post_colonial", None, "flag_constructed_imported",
            "1948 creation; no prior state at scale but strong pre-state (Yishuv/mandate) + European-imported institutions."),
    "BIH": ("post_colonial", "mature", "flag_dissolution_constructed",
            "Constructed Dayton (1995) state; no prior independent sovereign tradition at scale."),
    "MKD": ("post_colonial", "mature", "flag_dissolution",
            "Yugoslav republic-level administration but no prior independent sovereignty; weaker institutional depth."),
    "XKX": ("post_colonial", None, "flag_dissolution_constructed",
            "2008 constructed state (not in COW states2016); no prior independent sovereign tradition."),
    # post-Soviet non-Baltic European: brief 1918-21 republics (ARM/GEO/AZE/UKR)
    # or none (BLR/MDA); none restored the way the Baltics were.
    "UKR": ("post_colonial", "mature", "flag_post_soviet_dissolution",
            "Brief 1917-21 republic; no consolidated modern sovereign institutions at scale before 1991."),
    "ARM": ("post_colonial", "mature", "flag_post_soviet_dissolution", "Brief 1918-20 republic; deep nation, no modern sovereignty at scale before 1991."),
    "GEO": ("post_colonial", "mature", "flag_post_soviet_dissolution", "Brief 1918-21 republic; no modern sovereignty at scale before 1991."),
    "AZE": ("post_colonial", "mature", "flag_post_soviet_dissolution", "Brief 1918-20 republic; no modern sovereignty at scale before 1991."),
    "BLR": ("post_colonial", None, "flag_post_soviet_constructed", "No interwar independence; constructed Soviet-successor sovereignty 1991."),
    "MDA": ("post_colonial", None, "flag_post_soviet_constructed", "No prior independent sovereignty at scale; 1991 Soviet successor."),
    # Central Asian post-Soviet — brief's explicit 'constructed' exemplars.
    "KAZ": ("post_colonial", None, "flag_central_asian_constructed", "Brief exemplar: constructed 1991 successor, no prior sovereignty at scale."),
    "UZB": ("post_colonial", None, "flag_central_asian_constructed", "Constructed 1991 successor, no prior sovereignty at scale."),
    "TKM": ("post_colonial", None, "flag_central_asian_constructed", "Constructed 1991 successor."),
    "KGZ": ("post_colonial", None, "flag_central_asian_constructed", "Constructed 1991 successor."),
    "TJK": ("post_colonial", None, "flag_central_asian_constructed", "Constructed 1991 successor."),
    "ERI": ("post_colonial", None, "flag_secession_constructed", "1993 secession from Ethiopia; constructed sovereign institutions."),
    "SSD": ("post_colonial", None, "flag_secession_constructed", "2011 secession from Sudan; constructed sovereign institutions."),
    "CUB": ("early_post_colonial", None, "flag_late_iberian",
            "Independent 1902 (from Spain/US); Iberian-colonial heritage, ~120y development — kept in the early bloc."),
    "PAN": ("early_post_colonial", None, "flag_late_iberian", "Independent 1903 (from Colombia/US); Iberian-colonial heritage."),
    "DOM": ("early_post_colonial", None, "flag_late_iberian", "Independent 1844/1865; Iberian-colonial heritage."),
    "HTI": ("early_post_colonial", None, "flag_french", "Independent 1804 from France; earliest post-colonial republic."),
}


def main():
    cc_iso, _ = build_ccode_iso()
    rows = list(csv.DictReader(COW.open()))
    sty = defaultdict(list)
    endy = defaultdict(list)
    name = {}
    for r in rows:
        iso = cc_iso.get(int(r["ccode"]))
        if iso:
            sty[iso].append(int(r["styear"]))
            endy[iso].append(int(r["endyear"]))
            name.setdefault(iso, r["statenme"])
    cow_entry = {i: min(v) for i, v in sty.items()}

    # universe = union of erosion panel + holdout (recompute here so this file is self-contained)
    def ser(v):
        return json.loads(v) if isinstance(v, str) else v
    vdem = json.loads((ROOT / "data/sources/vdem_longrun.json").read_text())
    longrun = json.loads((ROOT / "data/sources/longrun_pillars.json").read_text())
    rol = {i: ser(v["rol"]) for i, v in vdem.items() if "rol" in v}
    gdp = {i: {int(y): val for y, val in ser(v["P4_gdp"]).items()} for i, v in longrun.items() if "P4_gdp" in v}
    panel = set()
    for y in [1816, 1850, 1880, 1910, 1940, 1970, 1990]:
        panel |= {i for i in set(rol) & set(gdp) if rol[i].get(str(y)) is not None and gdp[i].get(y, 0) > 0}
    panel = {p for p in panel if not p.startswith("OWID")}
    hp = json.loads((ROOT / "data/robustness/temporal_holdout_panel.json").read_text())
    hiso = {r["iso"] for w in hp["windows"].values() for r in w}
    universe = sorted((panel | hiso) - {"HKG"})  # HKG not a sovereign state (absent from COW)

    def classify(iso):
        if iso in NOTES:
            g, alt, flag, note = NOTES[iso]
            return g, alt, flag, note
        if iso in LATAM_EARLY:
            return "early_post_colonial", None, "latam_bloc", "Iberian-colonial bloc, independence c.1810s-1840s."
        if iso in MATURE:
            return "mature", None, "mature_core", "Mature institutional core (see MATURE set)."
        # default: post-1945 decolonization from a border-drawing colonial power
        return "post_colonial", None, "decolonization_post1945", "Post-1945 independence from a colonial power (border-drawn, admin class removed)."

    out = {}
    for iso in universe:
        g, alt, flag, note = classify(iso)
        out[iso] = {
            "name": name.get(iso, iso),
            "cow_entry_year": cow_entry.get(iso),
            "group": g,
            "alt_group": alt,       # None => solid; else sensitivity target
            "flag": flag,
            "note": note,
        }

    counts = defaultdict(int)
    for v in out.values():
        counts[v["group"]] += 1
    n_flagged = sum(1 for v in out.values() if v["alt_group"] is not None)

    payload = {
        "test": "A1_state_formation_classification",
        "status": "PRE-REGISTERED (committed before any A2/A3/A4 outcome split)",
        "source_entry_year": "Correlates of War State System Membership (states2016.csv)",
        "criterion": "prior multi-generational experience operating institutions at/near current scale",
        "groups": dict(counts),
        "n_states": len(out),
        "n_flagged_for_sensitivity": n_flagged,
        "india_special": "IND is coded post_colonial with alt_group=mature; A2/A3 run it in BOTH groups (brief).",
        "states": out,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))
    print(f"classified {len(out)} states -> {dict(counts)} (flagged {n_flagged})")
    for iso in universe:
        v = out[iso]
        tag = f"  [{v['flag']}]" if v["alt_group"] else ""
        print(f"  {iso} {v['cow_entry_year']!s:>5} {v['group']:<20}{tag}")
    print(f"-> {OUT.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
