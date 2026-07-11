"""
Modernization Index — internal Data API (single source of truth for inputs).

Mirrors what mi/constants.LENS does for the scoring *lens*: this module is the one
place indicator DATA is read from. Case records reference (country, year); the
engine calls get_indicators() and the values are assembled live from the canonical
sources. Edit a source file (or refresh the WGI/WDI snapshot) and it propagates to
every case on the next score — no per-country copies to keep in sync.

Sources (all paths in SOURCES below — the data config):
  - WGI (2025-anchored .SC) + WDI (GDP PPP / resource rents / ODA):
        data/sources/wb_anchored.json  (committed snapshot; refresh via
        scripts/refresh_wgi_wdi.py — same World Bank API the mi-pipeline panel uses)
  - CPI, GII, ECI, FSI, HDR (Edu/LifeExp indices):
        the committed mi-pipeline panel CSVs (the shared upstream source)

ECI min/max for normalization is derived from the ECI source itself (so it tracks
the data), and exposed per-record as eci_dataset_min/eci_dataset_max.
"""
import csv
import json
import os
from pathlib import Path
from functools import lru_cache

_MI_ROOT = Path(__file__).resolve().parent.parent          # .../mi-research
_REPO_ROOT = _MI_ROOT.parent                               # worktree root

# === DATA CONFIG — the one place data locations are declared ===
SOURCES = {
    "wb_anchored": _MI_ROOT / "data" / "sources" / "wb_anchored.json",
    # Panel CSVs: env override wins, else the sibling mi-pipeline panel (shared upstream).
    "panel_dir": Path(os.environ.get("MI_PANEL_DIR", _REPO_ROOT / "mi-pipeline" / "data")),
    # Voice & Accountability (WGI 2025-anchored .SC, 0-100) for ALL 180 panel countries — P1
    # excludes VA by design, so this serves the Accountability-Gap diagnostic (V3.2). Refresh via
    # the WB API (GOV_WGI_VA.SC, source=3).
    "va_anchored": _MI_ROOT / "data" / "sources" / "va_anchored.json",
}

_VA_CACHE = None
def _va():
    global _VA_CACHE
    if _VA_CACHE is None:
        try:
            with open(SOURCES["va_anchored"]) as fh:
                _VA_CACHE = json.load(fh)
        except FileNotFoundError:
            _VA_CACHE = {}
    return _VA_CACHE

# indicator dict keys the scoring engine consumes
_ENGINE_KEYS = [
    "gov_effectiveness", "rule_of_law", "regulatory_quality", "cpi",
    "control_of_corruption", "voice_accountability", "gii", "rd_pct_gdp", "eci",
    "eci_dataset_min", "eci_dataset_max", "education_index", "life_expectancy_index",
    "gdp_per_capita_ppp", "resource_rents_pct_gdp", "oda_pct_gni",
    "political_stability", "fsi",
]


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


@lru_cache(maxsize=1)
def _wb():
    with open(SOURCES["wb_anchored"]) as fh:
        data = json.load(fh)
    by_iso = {rec["iso3"]: rec for rec in data.values()}
    by_name = {name.lower(): rec for name, rec in data.items()}
    return data, by_iso, by_name


@lru_cache(maxsize=1)
def _panel():
    pdir = SOURCES["panel_dir"]

    def col(fn, c):
        out = {}
        path = pdir / fn
        if not path.exists():
            return out
        for r in csv.DictReader(open(path, encoding="latin-1")):
            v = _f(r.get(c))
            if v is not None:
                out[(r["iso3"], r["year"])] = v
        return out

    hdr = {}
    hpath = pdir / "hdr.csv"
    if hpath.exists():
        for r in csv.DictReader(open(hpath, encoding="latin-1")):
            hdr[(r["iso3"], r["year"])] = (_f(r.get("EduIdx")), _f(r.get("LifeExpIdx")))
    eci_vals = list(col("eci.csv", "ECI").values())
    eci_min = min(eci_vals) if eci_vals else -3.53
    eci_max = max(eci_vals) if eci_vals else 2.10
    return {
        "cpi": col("cpi.csv", "CPI"), "gii": col("gii.csv", "GII"),
        "eci": col("eci.csv", "ECI"), "fsi": col("fsi.csv", "FSI"),
        "hdr": hdr, "eci_min": eci_min, "eci_max": eci_max,
    }


def country_to_iso(country: str):
    _, by_iso, by_name = _wb()
    if country in by_iso:
        return country
    rec = by_name.get(country.lower())
    return rec["iso3"] if rec else None


def available_years(country: str):
    data, by_iso, by_name = _wb()
    rec = by_iso.get(country) or by_name.get(country.lower())
    if not rec:
        return []
    yrs = set()
    for dim in rec.get("wgi", {}).values():
        yrs.update(dim.keys())
    return sorted(yrs)


def _hdr_for(iso, year, panel):
    if (iso, year) in panel["hdr"] and panel["hdr"][(iso, year)][0] is not None:
        return panel["hdr"][(iso, year)], None
    cands = [int(k[1]) for k in panel["hdr"]
             if k[0] == iso and int(k[1]) <= int(year) and panel["hdr"][k][0] is not None]
    if cands:
        ly = str(max(cands))
        return panel["hdr"][(iso, ly)], f"HDI sub-indices from {ly} (latest <= {year})"
    return (None, None), None


def get_indicators(country: str, year, with_meta: bool = False):
    """Assemble the engine-ready indicator dict for (country, year) from the sources.

    Returns None if the country/year is unknown. With with_meta=True, also returns
    _gaps and _notes. Missing values are None (never interpolated)."""
    data, by_iso, by_name = _wb()
    rec = by_iso.get(country) or by_name.get(country.lower())
    if not rec:
        return None
    iso = rec["iso3"]
    year = str(year)
    W, D = rec.get("wgi", {}), rec.get("wdi", {})
    if year not in {y for dim in W.values() for y in dim}:
        return None
    panel = _panel()
    (edi, lei), hnote = _hdr_for(iso, year, panel)
    ind = {
        "gov_effectiveness": W.get("GE", {}).get(year),
        "rule_of_law": W.get("RL", {}).get(year),
        "regulatory_quality": W.get("RQ", {}).get(year),
        "cpi": panel["cpi"].get((iso, year)),
        "control_of_corruption": W.get("CC", {}).get(year),
        "voice_accountability": W.get("VA", {}).get(year) or _va().get(iso, {}).get(str(year)),
        "gii": panel["gii"].get((iso, year)),
        "rd_pct_gdp": None,
        "eci": panel["eci"].get((iso, year)),
        "eci_dataset_min": panel["eci_min"],
        "eci_dataset_max": panel["eci_max"],
        "education_index": edi,
        "life_expectancy_index": lei,
        "gdp_per_capita_ppp": D.get("gdp", {}).get(year),
        "resource_rents_pct_gdp": D.get("rents", {}).get(year),
        "oda_pct_gni": D.get("oda", {}).get(year),
        "political_stability": W.get("PV", {}).get(year),
        "fsi": panel["fsi"].get((iso, year)),
    }
    if not with_meta:
        return ind
    gaps = [k for k, v in ind.items()
            if v is None and k not in ("eci_dataset_min", "eci_dataset_max", "rd_pct_gdp")]
    notes = ["WGI=2025-anchored .SC (data/sources/wb_anchored.json); P1 corruption uses CPI "
             "when present else WGI CtrlCorr; CPI/GII/FSI from mi-pipeline panel (grid years)."]
    if hnote:
        notes.append(hnote)
    if year not in ("1996", "2004", "2012", "2018", "2024"):
        notes.append("OFF-GRID year (panel-extension via WB API).")
    ind["_gaps"] = gaps
    ind["_notes"] = " ".join(notes)
    return ind
