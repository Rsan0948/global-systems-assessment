"""
REAL ingest for the 2A DGS -> instability test.

Builds the country-period panel that fit_dgs() consumes, from four free
sources, merged on (ISO3, year):

  interior proxy   : Harvard Atlas Economic Complexity Index (eci_hs92)
                     -> data/harvard_eci.csv (Harvard Dataverse)
  interface proxy  : V-Dem electoral democracy index (polyarchy)
                     -> data/vdem_polyarchy.csv (Our World in Data)
  controls         : GDP per capita + population (World Bank API)
  instability      : UCDP/PRIO Armed Conflict Dataset (internal conflict)
                     -> data/UcdpPrioConflict_v*.csv

DGS = z(ECI) - z(polyarchy), standardized across the panel. The outcome is
instability in a forward window (t+1 .. t+W): does the country experience an
internal armed conflict? Anchors are spaced W years apart so the windows do NOT
overlap (no outcome autocorrelation). Caches the panel to
results/dgs_panel_real.json. Raw downloads under data/ are git-ignored.

Run: python ingest_dgs.py
"""

from __future__ import annotations

import csv
import glob
import json
import os
import urllib.request

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
RESULTS = os.path.join(HERE, "results")

ANCHORS = [1996, 2001, 2006, 2011, 2016]    # 5-yr spacing
WINDOW = 5                                  # forward instability window (non-overlapping)
_UA = {"User-Agent": "Mozilla/5.0 research"}

# UCDP location names that pycountry can't resolve directly -> ISO3
_ALIASES = {
    "russia (soviet union)": "RUS", "yemen (north yemen)": "YEM",
    "yemen (south yemen)": "YEM", "cambodia (kampuchea)": "KHM",
    "myanmar (burma)": "MMR", "dr congo (zaire)": "COD", "zimbabwe (rhodesia)": "ZWE",
    "madagascar (malagasy)": "MDG", "serbia (yugoslavia)": "SRB",
    "macedonia, fyr": "MKD", "bosnia-herzegovina": "BIH", "ivory coast": "CIV",
    "vietnam (north vietnam)": "VNM", "vietnam (south vietnam)": "VNM",
    "united states of america": "USA", "kingdom of eswatini (swaziland)": "SWZ",
    "hyderabad": "IND", "guinea-bissau": "GNB",
}


def _iso3(name: str) -> str | None:
    import pycountry
    base = name.split("(")[0].strip()
    key = name.strip().lower()
    if key in _ALIASES:
        return _ALIASES[key]
    if base.lower() in _ALIASES:
        return _ALIASES[base.lower()]
    try:
        return pycountry.countries.lookup(base).alpha_3
    except LookupError:
        try:
            return pycountry.countries.search_fuzzy(base)[0].alpha_3
        except Exception:
            return None


# ----------------------------------------------------------------- sources
def load_eci() -> dict:
    """{(iso3, year): eci_hs92}."""
    out = {}
    with open(os.path.join(DATA, "harvard_eci.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            v = row.get("eci_hs92")
            if v not in (None, "", "NA"):
                out[(row["country_iso3_code"], int(row["year"]))] = float(v)
    return out


def load_vdem():
    """({(iso3, year): polyarchy}, {iso3: region})."""
    val, region = {}, {}
    with open(os.path.join(DATA, "vdem_polyarchy.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            code = row["code"]
            v = row.get("electdem_vdem__estimate_best")
            if code and len(code) == 3 and v not in (None, "", "NA"):
                val[(code, int(row["year"]))] = float(v)
                if row.get("owid_region"):
                    region[code] = row["owid_region"]
    return val, region


def fetch_worldbank(indicator: str) -> dict:
    """{(iso3, year): value} from the World Bank API, cached to data/."""
    cache = os.path.join(DATA, f"wb_{indicator}.json")
    if os.path.exists(cache):
        rows = json.load(open(cache))
    else:
        rows, page = [], 1
        while True:
            url = (f"https://api.worldbank.org/v2/country/all/indicator/{indicator}"
                   f"?format=json&date=1995:2023&per_page=15000&page={page}")
            d = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=_UA), timeout=60).read())
            meta = d[0]
            rows += [(r["countryiso3code"], r["date"], r["value"]) for r in (d[1] or [])]
            if page >= meta.get("pages", 1):
                break
            page += 1
        os.makedirs(DATA, exist_ok=True)
        json.dump(rows, open(cache, "w"))
    return {(c, int(y)): float(v) for c, y, v in rows if c and v is not None}


def load_conflict_years(min_intensity: int = 1) -> set:
    """{(iso3, year)} with an internal armed conflict (UCDP type 3/4).
    min_intensity=1 -> any conflict; 2 -> war-level (>=1000 battle deaths)."""
    path = glob.glob(os.path.join(DATA, "*Conflict*.csv"))[0]
    out = set()
    with open(path, encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(f):
            if row.get("type_of_conflict") not in ("3", "4"):
                continue                                  # internal / internationalized-internal
            if int(row["intensity_level"]) < min_intensity:
                continue
            year = int(row["year"])
            for loc in row["location"].split(","):
                iso = _iso3(loc)
                if iso:
                    out.add((iso, year))
    return out


# ------------------------------------------------------------------- panel
def build_real_panel(anchors=None, window: int = WINDOW, min_intensity: int = 1) -> dict:
    anchors = ANCHORS if anchors is None else anchors
    anchor_set = set(anchors)
    eci = load_eci()
    vdem, region_map = load_vdem()
    gdppc = fetch_worldbank("NY.GDP.PCAP.CD")
    pop = fetch_worldbank("SP.POP.TOTL")
    conflict = load_conflict_years(min_intensity)

    region_levels = {r: i for i, r in enumerate(sorted(set(region_map.values())))}
    rows = []
    for (iso, year), eci_v in eci.items():
        if year not in anchor_set:
            continue
        key = (iso, year)
        if key not in vdem or key not in gdppc or key not in pop or iso not in region_map:
            continue
        if gdppc[key] <= 0 or pop[key] <= 0:
            continue
        instable = int(any((iso, y) in conflict for y in range(year + 1, year + 1 + window)))
        rows.append({
            "iso": iso, "eci": eci_v, "polyarchy": vdem[key],
            "log_gdppc": np.log(gdppc[key]), "log_pop": np.log(pop[key]),
            "region": region_levels[region_map[iso]],
            "decade": (year // 10), "period": year, "instability": instable,
        })

    eci_arr = np.array([r["eci"] for r in rows])
    pol_arr = np.array([r["polyarchy"] for r in rows])
    dgs = _z(eci_arr) - _z(pol_arr)
    panel = {
        "dgs": dgs,
        "log_gdppc": np.array([r["log_gdppc"] for r in rows]),
        "log_pop": np.array([r["log_pop"] for r in rows]),
        "region": np.array([r["region"] for r in rows]),
        "decade": np.array([r["decade"] for r in rows]),
        "period": np.array([r["period"] for r in rows]),
        "instability": np.array([r["instability"] for r in rows]),
    }
    panel["_meta"] = {
        "n_obs": len(rows), "n_countries": len({r["iso"] for r in rows}),
        "n_conflict_country_years": len(conflict),
        "base_rate": float(np.mean(panel["instability"])),
        "anchors": list(anchors), "window": window,
        "sources": "Harvard ECI + V-Dem (OWID) + World Bank + UCDP/PRIO ACD",
    }
    return panel


def _z(x: np.ndarray) -> np.ndarray:
    return (x - x.mean()) / x.std()


# (name, anchors, window, min_intensity) -- PREREGISTRATION §8 sensitivity grid
SENS_SPECS = [
    ("5yr windows, any conflict (primary)", [1996, 2001, 2006, 2011, 2016], 5, 1),
    ("3yr windows, any conflict", [1996, 1999, 2002, 2005, 2008, 2011, 2014, 2017], 3, 1),
    ("10yr windows, any conflict", [1996, 2006], 10, 1),
    ("5yr windows, war only (>=2)", [1996, 2001, 2006, 2011, 2016], 5, 2),
    ("annual anchors, 5yr window", list(range(1996, 2018)), 5, 1),
]


def cache_panel():
    panel = build_real_panel()
    out = {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in panel.items()}
    os.makedirs(RESULTS, exist_ok=True)
    json.dump(out, open(os.path.join(RESULTS, "dgs_panel_real.json"), "w"))
    m = panel["_meta"]
    print(f"real DGS panel: {m['n_obs']} obs, {m['n_countries']} countries, "
          f"base instability rate {m['base_rate']:.3f}, "
          f"{m['n_conflict_country_years']} conflict country-years")
    return panel


def cache_sensitivity():
    from dgs import fit_dgs
    rows = []
    for name, anchors, window, mi in SENS_SPECS:
        p = build_real_panel(anchors=anchors, window=window, min_intensity=mi)
        r = fit_dgs({k: v for k, v in p.items() if k != "_meta"})
        rows.append({"spec": name, "n": r.n, "base_rate": p["_meta"]["base_rate"],
                     "beta_dgs": round(r.beta_dgs, 4), "lr_p": r.lr_p,
                     "auc_gain": round(r.auc_gain, 4) if r.auc_gain == r.auc_gain else None})
    json.dump(rows, open(os.path.join(RESULTS, "dgs_sensitivity.json"), "w"), indent=2)
    print("sensitivity: DGS LR-p across specs =", [round(x["lr_p"], 3) for x in rows])
    return rows


if __name__ == "__main__":
    cache_panel()
    cache_sensitivity()
