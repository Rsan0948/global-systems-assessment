#!/usr/bin/env python3
"""
Modernization Index — Complete Data Pipeline
=============================================
Pulls raw indicator data from public APIs and local CSV files,
normalizes per the MI methodology, scores every country-year
observation under both v1 (anchor-based) and v2 (percentile-GPA),
and outputs the complete dataset.

Usage:
    1. pip install pandas requests openpyxl numpy scipy
    2. Place manual data files in ./data/ (see README or --setup)
    3. python mi_pipeline.py

The pipeline will:
    - Pull WGI + WDI indicators from the World Bank API
    - Load CPI, GII, FSI, ECI, HDR data from local CSVs
    - Merge into a master country-year panel
    - Normalize, score, and output to ./output/
"""

import os
import sys
import json
import time
import logging
import argparse
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from scipy import stats as scipy_stats

warnings.filterwarnings("ignore", category=FutureWarning)
logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s")
log = logging.getLogger("mi")

# ── directories ──────────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent
DATA_DIR   = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# ── time points ──────────────────────────────────────────────────
TIME_POINTS = [1996, 2004, 2012, 2018, 2024]

# ── World Bank API indicator codes ───────────────────────────────
# Each entry: label -> (indicator_code, source_id).
# source_id is None for the default WDI database (source 2) and 3 for the
# Worldwide Governance Indicators database.
#
# NOTE (2026-06): The World Bank restructured the WGI database. The legacy
# percentile-rank codes (GE.PER.RNK, RL.PER.RNK, …) now return HTTP-200 with
# "The indicator was not found. It may have been deleted or archived." The
# current WGI database (source 3) publishes a 0–100 governance *score* under
# the GOV_WGI_<dim>.SC codes. These scores are the direct successor to the old
# percentile ranks (e.g. 2023: Switzerland 91.0, Singapore 95.3, Lebanon 28.7),
# share the 0–100 range, and so the existing "÷ 100" normalization is unchanged
# and correct. iso3 for source 3 lives in `countryiso3code`, not `country.id`.
WB_INDICATORS = {
    # WGI 0–100 governance scores (successor to the percentile ranks), source 3
    "GovEff":    ("GOV_WGI_GE.SC", 3),
    "RuleLaw":   ("GOV_WGI_RL.SC", 3),
    "RegQual":   ("GOV_WGI_RQ.SC", 3),
    "CtrlCorr":  ("GOV_WGI_CC.SC", 3),
    "PolStab":   ("GOV_WGI_PV.SC", 3),
    # WDI (default source)
    "GDPpcPPP":  ("NY.GDP.PCAP.PP.CD", None),
    "ResRents":  ("NY.GDP.TOTL.RT.ZS", None),
    "ODA":       ("DT.ODA.ODAT.GN.ZS", None),
    "RD":        ("GB.XPD.RSDV.GD.ZS", None),
}

# ── scoring weights ──────────────────────────────────────────────
V1_WEIGHTS = {"P1": 0.25, "P2": 0.25, "P3": 0.20, "P4": 0.20, "P5": 0.10}
V2_WEIGHTS = {"P1": 0.34, "P2": 0.15, "P3": 0.16, "P4": 0.20, "P5": 0.16}

# ── anchor countries ─────────────────────────────────────────────
CEILING_COUNTRY = "Switzerland"
FLOOR_COUNTRY   = "Lebanon"

# ── ISO-3 helpers ────────────────────────────────────────────────
# Mapping common names to ISO-3 alpha codes used by the World Bank
COMMON_NAME_TO_ISO3 = {
    "Switzerland": "CHE", "Lebanon": "LBN", "Singapore": "SGP",
    "Sweden": "SWE", "Denmark": "DNK", "Finland": "FIN",
    "Germany": "DEU", "Japan": "JPN", "Netherlands": "NLD",
    "Austria": "AUT", "Norway": "NOR", "Ireland": "IRL",
    "United Kingdom": "GBR", "Taiwan": "TWN", "South Korea": "KOR",
    "Luxembourg": "LUX", "United States": "USA", "Hong Kong": "HKG",
    "France": "FRA", "Canada": "CAN", "Belgium": "BEL",
    "New Zealand": "NZL", "Australia": "AUS", "Estonia": "EST",
    "Poland": "POL", "Israel": "ISR", "China": "CHN",
    "Chile": "CHL", "Qatar": "QAT", "Romania": "ROU",
    "Malaysia": "MYS", "Saudi Arabia": "SAU", "Turkey": "TUR",
    "Brazil": "BRA", "India": "IND", "Russia": "RUS",
    "Iran": "IRN", "Ukraine": "UKR", "Egypt": "EGY",
    "Nigeria": "NGA", "Iraq": "IRQ", "Mexico": "MEX",
    "Indonesia": "IDN", "Vietnam": "VNM", "Thailand": "THA",
    "Philippines": "PHL", "Colombia": "COL", "Peru": "PER",
    "Argentina": "ARG", "South Africa": "ZAF", "Kenya": "KEN",
    "Ecuador": "ECU", "Costa Rica": "CRI", "Uruguay": "URY",
    "Czech Republic": "CZE", "Czechia": "CZE",
    "Slovakia": "SVK", "Slovenia": "SVN", "Lithuania": "LTU",
    "Latvia": "LVA", "Croatia": "HRV", "Hungary": "HUN",
    "Bulgaria": "BGR", "Serbia": "SRB", "Greece": "GRC",
    "Portugal": "PRT", "Spain": "ESP", "Italy": "ITA",
    "Cyprus": "CYP", "Malta": "MLT", "Iceland": "ISL",
    "Kuwait": "KWT", "Bahrain": "BHR", "Oman": "OMN",
    "United Arab Emirates": "ARE", "Jordan": "JOR", "Tunisia": "TUN",
    "Morocco": "MAR", "Algeria": "DZA", "Pakistan": "PAK",
    "Bangladesh": "BGD", "Sri Lanka": "LKA", "Cambodia": "KHM",
    "Myanmar": "MMR", "Ethiopia": "ETH", "Tanzania": "TZA",
    "Ghana": "GHA", "Senegal": "SEN", "Rwanda": "RWA",
    "Uganda": "UGA", "Mozambique": "MOZ", "Madagascar": "MDG",
    "Dominican Republic": "DOM", "Guatemala": "GTM",
    "Honduras": "HND", "El Salvador": "SLV", "Panama": "PAN",
    "Paraguay": "PRY", "Bolivia": "BOL", "Venezuela": "VEN",
    "Trinidad and Tobago": "TTO", "Jamaica": "JAM",
    "Georgia": "GEO", "Armenia": "ARM", "Azerbaijan": "AZE",
    "Kazakhstan": "KAZ", "Uzbekistan": "UZB",
    "Mongolia": "MNG", "Nepal": "NPL",
    "Botswana": "BWA", "Mauritius": "MUS", "Namibia": "NAM",
    "Zambia": "ZMB", "Zimbabwe": "ZWE", "Cameroon": "CMR",
    "Côte d'Ivoire": "CIV", "Ivory Coast": "CIV",
}


# ═══════════════════════════════════════════════════════════════════
#  SECTION 1 — DATA FETCHERS
# ═══════════════════════════════════════════════════════════════════

# The World Bank `country/all` endpoint returns regional and income-group
# AGGREGATES (World, OECD members, Arab World, Sub-Saharan Africa, …) alongside
# real countries. Many of their codes are 3 letters (WLD, EUU, OED, …) so a bare
# `len(iso3) == 3` filter lets them through — they then appear in the master panel
# as if they were countries. They never survive into the scored set (they lack the
# manual indicators, so they exceed the gap threshold), but they pollute the master
# CSV and the "total countries with any data" counts. We exclude them at the source.
#
# Authoritative list is fetched once from the WB country metadata endpoint (entries
# whose region is "Aggregates"); a static fallback is used only if that call fails.
# NOTE: we exclude *aggregates specifically* rather than keeping only a fixed list of
# countries, so legitimately-listed-elsewhere territories (e.g. Taiwan, absent from
# the WB country list but present in ECI/GII) are NOT dropped.
_WB_AGGREGATE_FALLBACK = frozenset({
    "WLD", "ARB", "CEB", "CSS", "EAP", "EAR", "EAS", "ECA", "ECS", "EMU", "EUU",
    "FCS", "HIC", "HPC", "IBD", "IBT", "IDA", "IDB", "IDX", "INX", "LAC", "LCN",
    "LDC", "LIC", "LMC", "LMY", "LTE", "MEA", "MIC", "MNA", "NAC", "OED", "OSS",
    "PRE", "PSS", "PST", "SAS", "SSA", "SSF", "SST", "TEA", "TEC", "TLA", "TMN",
    "TSA", "TSS", "UMC", "AFE", "AFW", "EAR", "LMY",
})
_wb_aggregate_cache = None


def wb_aggregate_codes() -> frozenset:
    """ISO3 codes that are World Bank *aggregates* (regions / income groups),
    to be excluded from the country panel. Fetched once from the WB country
    metadata endpoint; falls back to a static list if the call fails."""
    global _wb_aggregate_cache
    if _wb_aggregate_cache is not None:
        return _wb_aggregate_cache
    try:
        resp = requests.get(
            "https://api.worldbank.org/v2/country?format=json&per_page=400",
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        codes = {
            c.get("id") for c in data[1]
            if c.get("region", {}).get("value") == "Aggregates" and c.get("id")
        }
        if codes:
            _wb_aggregate_cache = frozenset(codes)
            log.info(f"WB aggregate filter: {len(codes)} aggregate codes excluded")
            return _wb_aggregate_cache
        log.warning("WB country list returned no aggregates; using static fallback.")
    except Exception as e:
        log.warning(f"Could not fetch WB country list ({e}); using static aggregate fallback.")
    _wb_aggregate_cache = _WB_AGGREGATE_FALLBACK
    return _wb_aggregate_cache


def fetch_world_bank(indicator_code: str, years: list[int],
                     retries: int = 3, per_page: int = 500,
                     source: int = None) -> pd.DataFrame:
    """Pull a single World Bank indicator for all countries at given years.
    Returns DataFrame with columns: [iso3, country, year, value].

    `source` selects the World Bank database (None = default WDI; 3 = WGI).
    The WGI database requires the explicit `&source=` parameter."""

    # WGI uses biennial years pre-2002; request a range to catch them
    year_min, year_max = min(years), max(years)
    url = (
        f"https://api.worldbank.org/v2/country/all/indicator/{indicator_code}"
        f"?date={year_min}:{year_max}&format=json&per_page={per_page}"
    )
    if source is not None:
        url += f"&source={source}"

    rows = []
    page = 1
    total_pages = 1
    aggregates = wb_aggregate_codes()

    while page <= total_pages:
        paged_url = f"{url}&page={page}"
        for attempt in range(retries):
            try:
                resp = requests.get(paged_url, timeout=30)
                resp.raise_for_status()
                data = resp.json()
                break
            except Exception as e:
                if attempt == retries - 1:
                    log.warning(f"Failed after {retries} attempts for {indicator_code}: {e}")
                    return pd.DataFrame(columns=["iso3", "country", "year", "value"])
                time.sleep(2 ** attempt)

        if not isinstance(data, list) or len(data) < 2 or data[1] is None:
            break

        total_pages = data[0].get("pages", 1)
        for rec in data[1]:
            # iso3: WDI puts the 3-letter code in country.id; WGI (source 3)
            # leaves country.id as a 2-letter code and carries iso3 in
            # `countryiso3code`. Prefer the explicit iso3 field when present.
            iso3 = (rec.get("countryiso3code") or "").strip() \
                or (rec.get("country", {}) or {}).get("id")
            name = rec.get("country", {}).get("value")
            year = int(rec.get("date", 0))
            val  = rec.get("value")
            if (val is not None and iso3 and len(iso3) == 3
                    and iso3 not in aggregates):
                rows.append({"iso3": iso3, "country": name,
                             "year": year, "value": float(val)})
        page += 1
        time.sleep(0.25)  # rate-limit politeness

    df = pd.DataFrame(rows)
    if df.empty:
        return df
    # keep only requested years (snap WGI biennial to nearest target)
    df = _snap_to_target_years(df, years)
    return df


def _snap_to_target_years(df: pd.DataFrame, targets: list[int],
                          max_gap: int = 2) -> pd.DataFrame:
    """For each country, pick the closest available year to each target
    (within max_gap). Handles WGI biennial pre-2002."""
    out = []
    for (iso3, country), grp in df.groupby(["iso3", "country"]):
        avail = grp.set_index("year")["value"]
        for t in targets:
            candidates = avail.loc[
                (avail.index >= t - max_gap) & (avail.index <= t + max_gap)
            ]
            if candidates.empty:
                continue
            best_year = min(candidates.index, key=lambda y: abs(y - t))
            out.append({"iso3": iso3, "country": country,
                        "year": t, "value": candidates[best_year],
                        "source_year": best_year})
    return pd.DataFrame(out)


def fetch_all_world_bank() -> pd.DataFrame:
    """Pull all World Bank indicators and pivot into one row per country-year."""
    frames = {}
    for label, (code, source) in WB_INDICATORS.items():
        log.info(f"Fetching World Bank: {label} ({code})")
        df = fetch_world_bank(code, TIME_POINTS, source=source)
        if df.empty:
            log.warning(f"  ⚠ No data returned for {label}")
        else:
            log.info(f"  ✓ {len(df)} obs across {df['iso3'].nunique()} countries")
        frames[label] = df

    # merge all into wide format
    merged = None
    for label, df in frames.items():
        if df.empty:
            continue
        chunk = df[["iso3", "country", "year", "value"]].rename(
            columns={"value": label}
        )
        if merged is None:
            merged = chunk
        else:
            merged = merged.merge(chunk, on=["iso3", "country", "year"], how="outer")
    return merged if merged is not None else pd.DataFrame()


# ── Manual CSV loaders ───────────────────────────────────────────

def load_cpi(path: Path = None) -> pd.DataFrame:
    """Load Transparency International CPI data.
    Expected CSV columns: iso3, country, year, CPI (0-100 scale)."""
    path = path or DATA_DIR / "cpi.csv"
    if not path.exists():
        log.warning(f"CPI file not found at {path}. See README for download instructions.")
        return pd.DataFrame(columns=["iso3", "country", "year", "CPI"])
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    required = {"iso3", "country", "year", "CPI"}
    if not required.issubset(set(df.columns)):
        # try common alternate column names
        col_map = {}
        for c in df.columns:
            cl = c.lower().strip()
            if cl in ("iso3", "iso", "code", "country_code"): col_map[c] = "iso3"
            elif cl in ("country", "country_name", "name"): col_map[c] = "country"
            elif cl in ("year",): col_map[c] = "year"
            elif cl in ("cpi", "score", "cpi_score", "cpi score"): col_map[c] = "CPI"
        df = df.rename(columns=col_map)
    df["CPI"] = pd.to_numeric(df["CPI"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    log.info(f"CPI: loaded {len(df)} rows from {path.name}")
    return df[["iso3", "country", "year", "CPI"]].dropna(subset=["CPI"])


def load_gii(path: Path = None) -> pd.DataFrame:
    """Load WIPO Global Innovation Index data.
    Expected CSV: iso3, country, year, GII (0-100)."""
    path = path or DATA_DIR / "gii.csv"
    if not path.exists():
        log.warning(f"GII file not found at {path}.")
        return pd.DataFrame(columns=["iso3", "country", "year", "GII"])
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    col_map = {}
    for c in df.columns:
        cl = c.lower().strip()
        if cl in ("iso3", "iso", "code", "country_code"): col_map[c] = "iso3"
        elif cl in ("country", "country_name", "name", "economy"): col_map[c] = "country"
        elif cl in ("year", "edition"): col_map[c] = "year"
        elif cl in ("gii", "score", "gii_score", "gii score"): col_map[c] = "GII"
    df = df.rename(columns=col_map)
    df["GII"] = pd.to_numeric(df["GII"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    log.info(f"GII: loaded {len(df)} rows from {path.name}")
    return df[["iso3", "country", "year", "GII"]].dropna(subset=["GII"])


def load_eci(path: Path = None) -> pd.DataFrame:
    """Load Harvard Growth Lab Atlas ECI data.
    Expected CSV: iso3, country, year, ECI."""
    path = path or DATA_DIR / "eci.csv"
    if not path.exists():
        log.warning(f"ECI file not found at {path}.")
        return pd.DataFrame(columns=["iso3", "country", "year", "ECI"])
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    col_map = {}
    for c in df.columns:
        cl = c.lower().strip()
        if cl in ("iso3", "iso", "code", "country_code", "location_code"): col_map[c] = "iso3"
        elif cl in ("country", "country_name", "name", "location_name"): col_map[c] = "country"
        elif cl in ("year",): col_map[c] = "year"
        elif cl in ("eci", "eci_value", "economic_complexity_index"): col_map[c] = "ECI"
    df = df.rename(columns=col_map)
    df["ECI"] = pd.to_numeric(df["ECI"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    log.info(f"ECI: loaded {len(df)} rows from {path.name}")
    return df[["iso3", "country", "year", "ECI"]].dropna(subset=["ECI"])


def load_hdr(path: Path = None) -> pd.DataFrame:
    """Load UNDP HDR Education Index and Life Expectancy Index.
    Expected CSV: iso3, country, year, EduIdx (0-1), LifeExpIdx (0-1)."""
    path = path or DATA_DIR / "hdr.csv"
    if not path.exists():
        log.warning(f"HDR file not found at {path}.")
        return pd.DataFrame(columns=["iso3", "country", "year", "EduIdx", "LifeExpIdx"])
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    col_map = {}
    for c in df.columns:
        cl = c.lower().strip()
        if cl in ("iso3", "iso", "code", "country_code"): col_map[c] = "iso3"
        elif cl in ("country", "country_name", "name"): col_map[c] = "country"
        elif cl in ("year",): col_map[c] = "year"
        elif cl in ("eduidx", "education_index", "edu_index", "education index"):
            col_map[c] = "EduIdx"
        elif cl in ("lifeexpidx", "life_expectancy_index", "le_index",
                     "life expectancy index"):
            col_map[c] = "LifeExpIdx"
    df = df.rename(columns=col_map)
    for col in ("EduIdx", "LifeExpIdx"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    log.info(f"HDR: loaded {len(df)} rows from {path.name}")
    cols = [c for c in ["iso3", "country", "year", "EduIdx", "LifeExpIdx"] if c in df.columns]
    return df[cols]


def load_fsi(path: Path = None) -> pd.DataFrame:
    """Load Fund for Peace Fragile States Index.
    Expected CSV: iso3, country, year, FSI (0-120, higher = more fragile)."""
    path = path or DATA_DIR / "fsi.csv"
    if not path.exists():
        log.warning(f"FSI file not found at {path}.")
        return pd.DataFrame(columns=["iso3", "country", "year", "FSI"])
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    col_map = {}
    for c in df.columns:
        cl = c.lower().strip()
        if cl in ("iso3", "iso", "code", "country_code"): col_map[c] = "iso3"
        elif cl in ("country", "country_name", "name"): col_map[c] = "country"
        elif cl in ("year",): col_map[c] = "year"
        elif cl in ("fsi", "total", "fsi_total", "score"): col_map[c] = "FSI"
    df = df.rename(columns=col_map)
    df["FSI"] = pd.to_numeric(df["FSI"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    log.info(f"FSI: loaded {len(df)} rows from {path.name}")
    return df[["iso3", "country", "year", "FSI"]].dropna(subset=["FSI"])


# ═══════════════════════════════════════════════════════════════════
#  SECTION 2 — MERGE
# ═══════════════════════════════════════════════════════════════════

def merge_all(wb: pd.DataFrame, cpi: pd.DataFrame, gii: pd.DataFrame,
              eci: pd.DataFrame, hdr: pd.DataFrame, fsi: pd.DataFrame) -> pd.DataFrame:
    """Merge all indicator DataFrames into a single master panel on (iso3, year)."""
    master = wb.copy() if not wb.empty else pd.DataFrame(columns=["iso3", "country", "year"])

    for ext_df in [cpi, gii, eci, hdr, fsi]:
        if ext_df.empty:
            continue
        # standardize join keys
        ext = ext_df.copy()
        merge_cols = ["iso3", "year"]
        value_cols = [c for c in ext.columns if c not in ("iso3", "country", "year")]
        ext_merge = ext[merge_cols + value_cols]
        if master.empty:
            master = ext.copy()
        else:
            master = master.merge(ext_merge, on=merge_cols, how="outer")

    # fill country names from any source where available
    if "country_x" in master.columns:
        master["country"] = master["country_x"].fillna(master.get("country_y"))
        master.drop(columns=[c for c in master.columns if c.startswith("country_")],
                    inplace=True, errors="ignore")

    # determine track
    master["Track"] = master["year"].apply(lambda y: 1 if y >= 2012 else 2)

    # snap ECI to target years (it has annual data)
    if "ECI" in master.columns:
        master = _snap_eci_years(master)

    return master.sort_values(["iso3", "year"]).reset_index(drop=True)


def _snap_eci_years(df: pd.DataFrame, max_gap: int = 3) -> pd.DataFrame:
    """ECI has annual data. Snap each country's annual ECI to the nearest
    target year (within ``max_gap`` years), then keep only target-year rows.

    The previous implementation kept *only* rows whose year was exactly a
    target year and discarded everything else — so a country whose latest ECI
    sits on, say, 2023 rather than 2024 lost its ECI entirely. Here we instead
    carry the nearest available annual value onto each target-year row (mirrors
    the nearest-year logic in ``_snap_to_target_years``) before dropping the
    off-target rows."""
    # Per-country annual ECI series (only rows that actually carry an ECI value).
    eci_long = df.loc[df["ECI"].notna(), ["iso3", "year", "ECI"]]
    snapped = {}  # (iso3, target_year) -> snapped ECI value
    for iso3, grp in eci_long.groupby("iso3"):
        avail = grp.groupby("year")["ECI"].mean()  # collapse any dup years
        for t in TIME_POINTS:
            window = avail.loc[(avail.index >= t - max_gap) & (avail.index <= t + max_gap)]
            if window.empty:
                continue
            best_year = min(window.index, key=lambda y: abs(y - t))
            snapped[(iso3, t)] = window[best_year]

    out = df[df["year"].isin(TIME_POINTS)].copy()
    # Overwrite ECI on the surviving target-year rows with the snapped value
    # (an exact-year match snaps to itself, so already-aligned values are kept).
    out["ECI"] = [snapped.get((iso3, year), np.nan)
                  for iso3, year in zip(out["iso3"], out["year"])]
    return out


# ═══════════════════════════════════════════════════════════════════
#  SECTION 3 — NORMALIZE
# ═══════════════════════════════════════════════════════════════════

def normalize(master: pd.DataFrame) -> pd.DataFrame:
    """Apply MI normalization rules to raw indicators.
    Adds normalized columns prefixed with 'n_'."""
    df = master.copy()

    # ── WGI percentile ranks: ÷ 100 ─────────────────────────
    for col in ["GovEff", "RuleLaw", "RegQual", "CtrlCorr", "PolStab"]:
        if col in df.columns:
            df[f"n_{col}"] = df[col] / 100.0

    # ── CPI: ÷ 100 ──────────────────────────────────────────
    if "CPI" in df.columns:
        df["n_CPI"] = df["CPI"] / 100.0

    # ── GII: ÷ 100 ──────────────────────────────────────────
    if "GII" in df.columns:
        df["n_GII"] = df["GII"] / 100.0

    # ── R&D: min-max across full dataset ─────────────────────
    if "RD" in df.columns:
        rd_vals = df["RD"].dropna()
        if len(rd_vals) > 1:
            rd_min, rd_max = rd_vals.min(), rd_vals.max()
            df["n_RD"] = (df["RD"] - rd_min) / (rd_max - rd_min) if rd_max > rd_min else 0.5
        else:
            df["n_RD"] = np.nan

    # ── ECI: min-max across full dataset ─────────────────────
    if "ECI" in df.columns:
        eci_vals = df["ECI"].dropna()
        if len(eci_vals) > 1:
            eci_min, eci_max = eci_vals.min(), eci_vals.max()
            df["n_ECI"] = (df["ECI"] - eci_min) / (eci_max - eci_min) if eci_max > eci_min else 0.5
        else:
            df["n_ECI"] = np.nan

    # ── Education Index: already 0-1 ─────────────────────────
    if "EduIdx" in df.columns:
        df["n_EduIdx"] = df["EduIdx"]

    # ── Life Expectancy Index: already 0-1 ────────────────────
    if "LifeExpIdx" in df.columns:
        df["n_LifeExpIdx"] = df["LifeExpIdx"]

    # ── GDP per capita PPP: log-transform, then min-max ──────
    if "GDPpcPPP" in df.columns:
        df["log_GDP"] = np.log(df["GDPpcPPP"].clip(lower=100))
        gdp_vals = df["log_GDP"].dropna()
        if len(gdp_vals) > 1:
            g_min, g_max = gdp_vals.min(), gdp_vals.max()
            df["n_GDPpcPPP"] = (df["log_GDP"] - g_min) / (g_max - g_min) if g_max > g_min else 0.5
        else:
            df["n_GDPpcPPP"] = np.nan

    # ── Resource rents: inverted — 1 - min(rents/50, 1) ──────
    if "ResRents" in df.columns:
        df["n_ResRents"] = 1.0 - (df["ResRents"] / 50.0).clip(upper=1.0)

    # ── ODA: inverted — 1 - min(ODA/20, 1) ───────────────────
    #    High-income non-recipients: treat as 0 → score = 1.0
    if "ODA" in df.columns:
        df["n_ODA"] = 1.0 - (df["ODA"].fillna(0) / 20.0).clip(upper=1.0)

    # ── FSI: inverted — 1 - (FSI / 120) ──────────────────────
    if "FSI" in df.columns:
        df["n_FSI"] = 1.0 - (df["FSI"] / 120.0)

    return df


# ═══════════════════════════════════════════════════════════════════
#  SECTION 4 — PILLAR SCORES
# ═══════════════════════════════════════════════════════════════════

def compute_pillars(df: pd.DataFrame) -> pd.DataFrame:
    """Compute pillar scores based on track assignment."""
    out = df.copy()

    # ── P1: Institutional Quality ─────────────────────────────
    # Track 1: mean(GovEff, RuleLaw, RegQual, CPI)
    # Track 2: mean(GovEff, RuleLaw, RegQual, CtrlCorr)
    p1_cols_t1 = ["n_GovEff", "n_RuleLaw", "n_RegQual", "n_CPI"]
    p1_cols_t2 = ["n_GovEff", "n_RuleLaw", "n_RegQual", "n_CtrlCorr"]

    out["P1"] = np.nan
    mask_t1 = out["Track"] == 1
    mask_t2 = out["Track"] == 2

    avail_t1 = [c for c in p1_cols_t1 if c in out.columns]
    avail_t2 = [c for c in p1_cols_t2 if c in out.columns]

    if avail_t1:
        out.loc[mask_t1, "P1"] = out.loc[mask_t1, avail_t1].mean(axis=1, skipna=True)
    if avail_t2:
        out.loc[mask_t2, "P1"] = out.loc[mask_t2, avail_t2].mean(axis=1, skipna=True)

    # ── P2: Innovation & Knowledge Economy ────────────────────
    # Track 1: mean(GII, ECI)
    # Track 2: mean(RD, ECI)
    p2_t1 = [c for c in ["n_GII", "n_ECI"] if c in out.columns]
    p2_t2 = [c for c in ["n_RD", "n_ECI"]  if c in out.columns]

    out["P2"] = np.nan
    if p2_t1:
        out.loc[mask_t1, "P2"] = out.loc[mask_t1, p2_t1].mean(axis=1, skipna=True)
    if p2_t2:
        out.loc[mask_t2, "P2"] = out.loc[mask_t2, p2_t2].mean(axis=1, skipna=True)

    # ── P3: Human Capital ─────────────────────────────────────
    p3_cols = [c for c in ["n_EduIdx", "n_LifeExpIdx"] if c in out.columns]
    if p3_cols:
        out["P3"] = out[p3_cols].mean(axis=1, skipna=True)
    else:
        out["P3"] = np.nan

    # ── P4: Economic Structure & Independence ─────────────────
    p4_cols = [c for c in ["n_GDPpcPPP", "n_ResRents", "n_ODA"] if c in out.columns]
    if p4_cols:
        out["P4"] = out[p4_cols].mean(axis=1, skipna=True)
    else:
        out["P4"] = np.nan

    # ── P5: Stability & Resilience ────────────────────────────
    # Track 1: mean(PolStab, FSI)
    # Track 2: PolStab alone
    p5_t1 = [c for c in ["n_PolStab", "n_FSI"] if c in out.columns]
    out["P5"] = np.nan
    if p5_t1:
        out.loc[mask_t1, "P5"] = out.loc[mask_t1, p5_t1].mean(axis=1, skipna=True)
    if "n_PolStab" in out.columns:
        out.loc[mask_t2, "P5"] = out.loc[mask_t2, "n_PolStab"]

    return out


# ═══════════════════════════════════════════════════════════════════
#  SECTION 5 — SCORING
# ═══════════════════════════════════════════════════════════════════

def score_v1(df: pd.DataFrame) -> pd.DataFrame:
    """Model v1: anchor-based scoring.
    raw = weighted sum of pillars
    M = (raw - raw_Lebanon_2024) / (raw_Switzerland_2024 - raw_Lebanon_2024)
    No clamping."""
    out = df.copy()
    pillars = ["P1", "P2", "P3", "P4", "P5"]

    # raw composite
    out["v1_raw"] = sum(out[p] * V1_WEIGHTS[p] for p in pillars)

    # find anchor raws from 2024
    ceil_mask = (out["country"] == CEILING_COUNTRY) & (out["year"] == 2024)
    floor_mask = (out["country"] == FLOOR_COUNTRY) & (out["year"] == 2024)

    # try iso3 if country name didn't match
    if ceil_mask.sum() == 0:
        ceil_mask = (out["iso3"] == "CHE") & (out["year"] == 2024)
    if floor_mask.sum() == 0:
        floor_mask = (out["iso3"] == "LBN") & (out["year"] == 2024)

    if ceil_mask.sum() == 0 or floor_mask.sum() == 0:
        log.warning("⚠ Cannot find Switzerland or Lebanon 2024 for v1 anchoring. "
                     "v1_MScore will be the un-anchored raw composite.")
        out["v1_MScore"] = out["v1_raw"]
        return out

    raw_ceil  = out.loc[ceil_mask, "v1_raw"].values[0]
    raw_floor = out.loc[floor_mask, "v1_raw"].values[0]

    # Fail loudly when an anchor's raw composite is NaN. If Switzerland or
    # Lebanon 2024 is missing any pillar input, v1_raw is NaN, which would make
    # `spread` NaN and silently collapse the *entire* v1_MScore column to NaN
    # with no warning. A NaN anchor means the anchoring is undefined — halt
    # rather than emit a result-shaped non-result.
    if np.isnan(raw_ceil) or np.isnan(raw_floor):
        raise ValueError(
            "v1 anchoring failed: anchor raw composite is NaN "
            f"({CEILING_COUNTRY} 2024 raw={raw_ceil}, {FLOOR_COUNTRY} 2024 raw={raw_floor}). "
            "An anchor is missing one or more pillar inputs, so v1_MScore cannot be "
            "computed. Check the pillar coverage for the anchor countries before scoring."
        )

    spread = raw_ceil - raw_floor

    if abs(spread) < 1e-9:
        log.warning("⚠ Zero spread between ceiling and floor. Check data.")
        out["v1_MScore"] = out["v1_raw"]
        return out

    out["v1_MScore"] = (out["v1_raw"] - raw_floor) / spread
    log.info(f"v1 anchors: Switzerland raw={raw_ceil:.4f}, Lebanon raw={raw_floor:.4f}, "
             f"spread={spread:.4f}")
    return out


def score_v2(df: pd.DataFrame) -> pd.DataFrame:
    """Model v2: percentile-GPA scoring.
    Within each year's cohort, percentile-rank each indicator,
    convert to GPA (0-4), compute weighted pillar GPAs."""
    out = df.copy()

    # indicators that need percentile ranking (all normalized)
    # For inverted indicators, higher n_ already = better, so rank ascending is correct
    indicator_cols = [c for c in out.columns if c.startswith("n_")]

    for year in out["year"].unique():
        mask = out["year"] == year
        cohort = out.loc[mask]
        for col in indicator_cols:
            vals = cohort[col].dropna()
            if len(vals) < 3:
                continue
            # percentile rank (0-100) — higher = better
            pctile = vals.rank(pct=True) * 100
            gpa = pctile / 100.0 * 4.0
            out.loc[pctile.index, f"gpa_{col}"] = gpa

    # pillar GPAs
    # P1 — use track-appropriate indicators
    mask_t1 = out["Track"] == 1
    mask_t2 = out["Track"] == 2

    p1_gpa_t1 = [f"gpa_n_{c}" for c in ["GovEff", "RuleLaw", "RegQual", "CPI"]
                 if f"gpa_n_{c}" in out.columns]
    p1_gpa_t2 = [f"gpa_n_{c}" for c in ["GovEff", "RuleLaw", "RegQual", "CtrlCorr"]
                 if f"gpa_n_{c}" in out.columns]

    out["P1_GPA"] = np.nan
    if p1_gpa_t1: out.loc[mask_t1, "P1_GPA"] = out.loc[mask_t1, p1_gpa_t1].mean(axis=1)
    if p1_gpa_t2: out.loc[mask_t2, "P1_GPA"] = out.loc[mask_t2, p1_gpa_t2].mean(axis=1)

    p2_gpa_t1 = [f"gpa_n_{c}" for c in ["GII", "ECI"] if f"gpa_n_{c}" in out.columns]
    p2_gpa_t2 = [f"gpa_n_{c}" for c in ["RD", "ECI"]  if f"gpa_n_{c}" in out.columns]
    out["P2_GPA"] = np.nan
    if p2_gpa_t1: out.loc[mask_t1, "P2_GPA"] = out.loc[mask_t1, p2_gpa_t1].mean(axis=1)
    if p2_gpa_t2: out.loc[mask_t2, "P2_GPA"] = out.loc[mask_t2, p2_gpa_t2].mean(axis=1)

    p3_gpa = [f"gpa_n_{c}" for c in ["EduIdx", "LifeExpIdx"] if f"gpa_n_{c}" in out.columns]
    out["P3_GPA"] = out[p3_gpa].mean(axis=1) if p3_gpa else np.nan

    p4_gpa = [f"gpa_n_{c}" for c in ["GDPpcPPP", "ResRents", "ODA"] if f"gpa_n_{c}" in out.columns]
    out["P4_GPA"] = out[p4_gpa].mean(axis=1) if p4_gpa else np.nan

    p5_gpa_t1 = [f"gpa_n_{c}" for c in ["PolStab", "FSI"] if f"gpa_n_{c}" in out.columns]
    out["P5_GPA"] = np.nan
    if p5_gpa_t1: out.loc[mask_t1, "P5_GPA"] = out.loc[mask_t1, p5_gpa_t1].mean(axis=1)
    if "gpa_n_PolStab" in out.columns:
        out.loc[mask_t2, "P5_GPA"] = out.loc[mask_t2, "gpa_n_PolStab"]

    # weighted composite GPA
    gpa_pillars = ["P1_GPA", "P2_GPA", "P3_GPA", "P4_GPA", "P5_GPA"]
    weights = [V2_WEIGHTS["P1"], V2_WEIGHTS["P2"], V2_WEIGHTS["P3"],
               V2_WEIGHTS["P4"], V2_WEIGHTS["P5"]]
    out["v2_GPA"] = sum(out[p] * w for p, w in zip(gpa_pillars, weights))

    return out


def compute_diagnostics(df: pd.DataFrame) -> pd.DataFrame:
    """Add pillar spread, configuration profile, and gap counts."""
    out = df.copy()
    pillars = ["P1", "P2", "P3", "P4", "P5"]

    # pillar spread (std dev of the 5 pillar scores)
    pillar_matrix = out[pillars]
    out["pillar_spread"] = pillar_matrix.std(axis=1, skipna=True)

    # configuration profile: rank order of pillars (strongest first)
    def config_profile(row):
        vals = {p: row[p] for p in pillars if pd.notna(row[p])}
        if not vals:
            return ""
        ranked = sorted(vals, key=vals.get, reverse=True)
        return ">".join(ranked)

    out["config_profile"] = out.apply(config_profile, axis=1)

    # Count gaps (missing indicators per row) against the *canonical expected*
    # indicator set per track — NOT against whichever columns happen to exist.
    # If an entire source CSV is absent (e.g. hdr.csv), its columns never enter
    # the panel; gating on `c in out.columns` would then make the gap invisible
    # and every affected country would falsely report gap_count = 0 / scoreable
    # while its pillar went silently NaN. A missing column is itself a gap, so
    # `row.get(c)` returns None for an absent indicator and pd.isna counts it.
    raw_indicators = ["GovEff", "RuleLaw", "RegQual", "PolStab",
                      "EduIdx", "LifeExpIdx", "GDPpcPPP", "ResRents"]
    # track-dependent
    t1_extra = ["CPI", "GII", "ECI", "ODA", "FSI"]
    t2_extra = ["CtrlCorr", "RD", "ECI", "ODA"]

    def _expected(row):
        return raw_indicators + (t1_extra if row.get("Track") == 1 else t2_extra)

    def count_gaps(row):
        return sum(1 for c in _expected(row) if pd.isna(row.get(c)))

    out["gap_count"] = out.apply(count_gaps, axis=1)

    def list_gaps(row):
        gaps = [c for c in _expected(row) if pd.isna(row.get(c))]
        return "; ".join(gaps) if gaps else ""

    out["gaps_noted"] = out.apply(list_gaps, axis=1)

    return out


# ═══════════════════════════════════════════════════════════════════
#  SECTION 6 — COVERAGE REPORT
# ═══════════════════════════════════════════════════════════════════

def coverage_report(df: pd.DataFrame) -> str:
    """Generate a text coverage report."""
    lines = ["\n" + "=" * 70, "  MODERNIZATION INDEX — COVERAGE REPORT", "=" * 70]

    for year in TIME_POINTS:
        ydf = df[df["year"] == year]
        scoreable = ydf[ydf["gap_count"] <= 2]
        unscorable = ydf[ydf["gap_count"] > 2]
        track = 1 if year >= 2012 else 2
        lines.append(f"\n{'─' * 50}")
        lines.append(f"  {year} (Track {track})")
        lines.append(f"  Total countries with any data: {len(ydf)}")
        lines.append(f"  Scoreable (≤2 gaps):           {len(scoreable)}")
        lines.append(f"  Not scoreable (>2 gaps):       {len(unscorable)}")

        if len(unscorable) > 0:
            lines.append(f"  Excluded countries and missing indicators:")
            for _, row in unscorable.iterrows():
                name = row.get("country", row.get("iso3", "?"))
                lines.append(f"    {name}: missing [{row['gaps_noted']}]")

    # regional summary
    lines.append(f"\n{'─' * 50}")
    lines.append("  REGIONAL COVERAGE (2024)")
    yr2024 = df[(df["year"] == 2024) & (df["gap_count"] <= 2)]
    # rough region mapping by iso3 prefix
    regions = {
        "Europe": ["ALB","AND","AUT","BLR","BEL","BIH","BGR","HRV","CYP","CZE",
                    "DNK","EST","FIN","FRA","DEU","GRC","HUN","ISL","IRL","ITA",
                    "XKX","LVA","LTU","LUX","MLT","MDA","MNE","NLD","MKD","NOR",
                    "POL","PRT","ROU","RUS","SRB","SVK","SVN","ESP","SWE","CHE",
                    "GBR","UKR"],
        "East Asia & Pacific": ["AUS","BRN","KHM","CHN","FJI","HKG","IDN","JPN",
                                "KOR","LAO","MYS","MNG","MMR","NZL","PHL","SGP",
                                "TWN","THA","VNM"],
        "Americas": ["ARG","BOL","BRA","CAN","CHL","COL","CRI","CUB","DOM","ECU",
                     "SLV","GTM","HND","JAM","MEX","NIC","PAN","PRY","PER","TTO",
                     "URY","USA","VEN"],
        "Middle East & N. Africa": ["DZA","BHR","EGY","IRN","IRQ","ISR","JOR","KWT",
                                     "LBN","LBY","MAR","OMN","QAT","SAU","TUN",
                                     "ARE","YEM"],
        "South Asia": ["AFG","BGD","BTN","IND","MDV","NPL","PAK","LKA"],
        "Sub-Saharan Africa": ["AGO","BEN","BWA","BFA","BDI","CMR","CPV","CAF",
                                "TCD","COM","COD","COG","CIV","DJI","GNQ","ERI",
                                "SWZ","ETH","GAB","GMB","GHA","GIN","GNB","KEN",
                                "LSO","LBR","MDG","MWI","MLI","MRT","MUS","MOZ",
                                "NAM","NER","NGA","RWA","STP","SEN","SYC","SLE",
                                "ZAF","SSD","SDN","TZA","TGO","UGA","ZMB","ZWE"],
    }
    for region, codes in regions.items():
        count = yr2024[yr2024["iso3"].isin(codes)].shape[0]
        lines.append(f"  {region}: {count} countries scored")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════
#  SECTION 7 — ANALYTICAL FINDINGS (Phase 6)
# ═══════════════════════════════════════════════════════════════════

def analytical_findings(df: pd.DataFrame) -> str:
    """Run the Phase 6 checks on the scored dataset."""
    lines = ["\n" + "=" * 70, "  MODERNIZATION INDEX — ANALYTICAL FINDINGS", "=" * 70]
    scoreable = df[df["gap_count"] <= 2].copy()

    # ── Thesis 1: Institutional centrality ────────────────────
    lines.append("\n── THESIS 1: Institutional Centrality ──")
    pillars = ["P1", "P2", "P3", "P4", "P5"]
    yr2024 = scoreable[scoreable["year"] == 2024]

    if len(yr2024) >= 10:
        corr_matrix = yr2024[pillars].corr(method="pearson").abs()
        avg_corr = {}
        for p in pillars:
            others = [c for c in pillars if c != p]
            avg_corr[p] = corr_matrix.loc[p, others].mean()

        ranked = sorted(avg_corr.items(), key=lambda x: x[1], reverse=True)
        lines.append(f"  Average |r| with other pillars (2024, n={len(yr2024)}):")
        for p, r in ranked:
            marker = " ◄ HIGHEST" if p == ranked[0][0] else ""
            lines.append(f"    {p}: {r:.3f}{marker}")

        if ranked[0][0] == "P1":
            lines.append("  → CONFIRMED: P1 (Institutional Quality) is most central")
        else:
            lines.append(f"  → NOTE: {ranked[0][0]} is most central, not P1")
    else:
        lines.append("  Insufficient data for correlation analysis")

    # ── Thesis 2: Resource penalty ────────────────────────────
    lines.append("\n── THESIS 2: Resource Penalty ──")
    if "ResRents" in yr2024.columns and "P1" in yr2024.columns:
        valid = yr2024[["ResRents", "P1"]].dropna()
        if len(valid) >= 10:
            r, p = scipy_stats.pearsonr(valid["ResRents"], valid["P1"])
            lines.append(f"  Pearson r(ResRents, P1): {r:.3f}  (p={p:.4f}, n={len(valid)})")
            if r < -0.2 and p < 0.05:
                lines.append("  → CONFIRMED: Significant negative resource-institutions association")
            else:
                lines.append("  → WEAK/NOT CONFIRMED at this sample size")

            # also check ResRents vs overall v1
            valid2 = yr2024[["ResRents", "v1_MScore"]].dropna()
            if len(valid2) >= 10:
                r2, p2 = scipy_stats.pearsonr(valid2["ResRents"], valid2["v1_MScore"])
                lines.append(f"  Pearson r(ResRents, v1_MScore): {r2:.3f}  (p={p2:.4f})")
    else:
        lines.append("  Insufficient data for resource penalty analysis")

    # ── Thesis 3: Configuration (spread vs stability) ─────────
    lines.append("\n── THESIS 3: Configuration (Spread vs. Trajectory Stability) ──")
    countries_multi = scoreable.groupby("iso3").filter(lambda g: len(g) >= 3)
    if len(countries_multi["iso3"].unique()) >= 10:
        traj = []
        for iso3, grp in countries_multi.groupby("iso3"):
            grp = grp.sort_values("year")
            if "v1_MScore" in grp.columns and grp["v1_MScore"].notna().sum() >= 3:
                spread_mean = grp["pillar_spread"].mean()
                # trajectory stability = inverse of std of period-over-period changes
                changes = grp["v1_MScore"].diff().dropna()
                if len(changes) >= 2:
                    traj_vol = changes.std()
                    traj.append({"iso3": iso3, "avg_spread": spread_mean,
                                 "traj_volatility": traj_vol})

        if len(traj) >= 10:
            traj_df = pd.DataFrame(traj)
            r, p = scipy_stats.pearsonr(traj_df["avg_spread"], traj_df["traj_volatility"])
            lines.append(f"  Pearson r(avg_pillar_spread, trajectory_volatility): {r:.3f}  "
                         f"(p={p:.4f}, n={len(traj_df)})")
            if r > 0.2 and p < 0.1:
                lines.append("  → SUPPORTED: Higher spread associates with less stable trajectories")
            else:
                lines.append("  → Not clearly supported at this sample size")
        else:
            lines.append("  Insufficient longitudinal coverage for spread-stability test")
    else:
        lines.append("  Insufficient longitudinal coverage")

    # ── Surprising profiles ───────────────────────────────────
    lines.append("\n── SURPRISING PROFILES (2024) ──")
    if len(yr2024) > 0 and "v1_MScore" in yr2024.columns:
        # high GDP but low MI
        if "GDPpcPPP" in yr2024.columns:
            gdp_75 = yr2024["GDPpcPPP"].quantile(0.75)
            mi_median = yr2024["v1_MScore"].median()
            surprises = yr2024[(yr2024["GDPpcPPP"] > gdp_75) & (yr2024["v1_MScore"] < mi_median)]
            if len(surprises) > 0:
                lines.append("  High GDP but below-median MI (resource/luck penalty candidates):")
                for _, row in surprises.iterrows():
                    name = row.get("country", row.get("iso3"))
                    lines.append(f"    {name}: GDP ${row['GDPpcPPP']:,.0f}, "
                                 f"MI={row['v1_MScore']:.3f}")

        # low GDP but high MI
        if "GDPpcPPP" in yr2024.columns:
            gdp_25 = yr2024["GDPpcPPP"].quantile(0.25)
            mi_75 = yr2024["v1_MScore"].quantile(0.75)
            # "Structural overperformers" = bottom-quartile GDP yet top-quartile
            # MI. The threshold here is mi_75 (the computed quantile), matching
            # the variable's intent; the previous code computed mi_75 but then
            # filtered on mi_median, leaving the quantile unused and the label
            # inconsistent.
            overperformers = yr2024[(yr2024["GDPpcPPP"] < gdp_25) & (yr2024["v1_MScore"] > mi_75)]
            if len(overperformers) > 0:
                lines.append("  Low GDP but top-quartile MI (structural overperformers):")
                for _, row in overperformers.iterrows():
                    name = row.get("country", row.get("iso3"))
                    lines.append(f"    {name}: GDP ${row['GDPpcPPP']:,.0f}, "
                                 f"MI={row['v1_MScore']:.3f}")

    # ── Tier distribution ─────────────────────────────────────
    lines.append("\n── TIER DISTRIBUTION (2024) ──")
    if "v1_MScore" in yr2024.columns:
        tiers = {
            "Tier 1 (≥0.80)": yr2024[yr2024["v1_MScore"] >= 0.80],
            "Tier 2 (0.60-0.79)": yr2024[(yr2024["v1_MScore"] >= 0.60) & (yr2024["v1_MScore"] < 0.80)],
            "Tier 3 (0.40-0.59)": yr2024[(yr2024["v1_MScore"] >= 0.40) & (yr2024["v1_MScore"] < 0.60)],
            "Tier 4 (0.20-0.39)": yr2024[(yr2024["v1_MScore"] >= 0.20) & (yr2024["v1_MScore"] < 0.40)],
            "Tier 5 (0.00-0.19)": yr2024[(yr2024["v1_MScore"] >= 0.00) & (yr2024["v1_MScore"] < 0.20)],
            "Below Floor (<0.00)": yr2024[yr2024["v1_MScore"] < 0.00],
        }
        for label, tier_df in tiers.items():
            countries = sorted(tier_df["country"].dropna().tolist()) if "country" in tier_df.columns else []
            lines.append(f"  {label}: {len(tier_df)} countries")
            if countries:
                lines.append(f"    {', '.join(countries[:15])}")
                if len(countries) > 15:
                    lines.append(f"    ... and {len(countries) - 15} more")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════
#  SECTION 8 — OUTPUT
# ═══════════════════════════════════════════════════════════════════

def write_outputs(df: pd.DataFrame, report: str, findings: str):
    """Write CSV, Excel, and reports to output directory."""

    # ── Master CSV ────────────────────────────────────────────
    # select key columns for the clean output
    key_cols = ["iso3", "country", "year", "Track",
                # raw indicators
                "GovEff", "RuleLaw", "RegQual", "CPI", "CtrlCorr",
                "GII", "RD", "ECI",
                "EduIdx", "LifeExpIdx",
                "GDPpcPPP", "ResRents", "ODA",
                "PolStab", "FSI",
                # pillar scores
                "P1", "P2", "P3", "P4", "P5",
                # v1
                "v1_raw", "v1_MScore",
                # v2
                "P1_GPA", "P2_GPA", "P3_GPA", "P4_GPA", "P5_GPA", "v2_GPA",
                # diagnostics
                "pillar_spread", "config_profile", "gap_count", "gaps_noted"]

    export_cols = [c for c in key_cols if c in df.columns]
    export = df[export_cols].copy()

    # sort by year, then by v1_MScore descending
    sort_cols = ["year"]
    if "v1_MScore" in export.columns:
        sort_cols.append("v1_MScore")
        export = export.sort_values(sort_cols, ascending=[True, False])
    else:
        export = export.sort_values(sort_cols)

    csv_path = OUTPUT_DIR / "mi_master_dataset.csv"
    export.to_csv(csv_path, index=False, float_format="%.4f")
    log.info(f"✓ Master CSV written to {csv_path}")

    # ── Scoreable-only CSV ────────────────────────────────────
    scoreable = export[export["gap_count"] <= 2] if "gap_count" in export.columns else export
    score_path = OUTPUT_DIR / "mi_scored_countries.csv"
    scoreable.to_csv(score_path, index=False, float_format="%.4f")
    log.info(f"✓ Scored countries CSV written to {score_path}")

    # ── Excel workbook ────────────────────────────────────────
    xlsx_path = OUTPUT_DIR / "mi_complete.xlsx"
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        export.to_excel(writer, sheet_name="Master", index=False)
        scoreable.to_excel(writer, sheet_name="Scored (≤2 gaps)", index=False)

        # per-year sheets
        for year in TIME_POINTS:
            ydf = scoreable[scoreable["year"] == year]
            if len(ydf) > 0:
                ydf.to_excel(writer, sheet_name=str(year), index=False)

    log.info(f"✓ Excel workbook written to {xlsx_path}")

    # ── Reports ───────────────────────────────────────────────
    report_path = OUTPUT_DIR / "mi_coverage_report.txt"
    with open(report_path, "w") as f:
        f.write(report)
    log.info(f"✓ Coverage report written to {report_path}")

    findings_path = OUTPUT_DIR / "mi_analytical_findings.txt"
    with open(findings_path, "w") as f:
        f.write(findings)
    log.info(f"✓ Analytical findings written to {findings_path}")


# ═══════════════════════════════════════════════════════════════════
#  SECTION 9 — SETUP HELPER
# ═══════════════════════════════════════════════════════════════════

def print_setup_instructions():
    """Print instructions for preparing manual data files."""
    instructions = """
╔══════════════════════════════════════════════════════════════════════╗
║          MODERNIZATION INDEX PIPELINE — DATA SETUP                 ║
╚══════════════════════════════════════════════════════════════════════╝

The pipeline automatically pulls WGI + WDI data from the World Bank API.
Five additional data sources require manual CSV downloads.

Place all files in: {data_dir}/

── 1. CPI (cpi.csv) ────────────────────────────────────────────────
   Source:  https://www.transparency.org/en/cpi/
   Action:  Download the full dataset → save as cpi.csv
   Columns needed: iso3, country, year, CPI
   Notes:   Only 2012+ is comparable. For pre-2012, the pipeline
            uses WGI Control of Corruption (pulled automatically).

── 2. GII (gii.csv) ────────────────────────────────────────────────
   Source:  https://www.wipo.int/global_innovation_index/en/
            → download the data Excel → export to CSV
   Columns: iso3, country, year, GII (the 0-100 overall score)
   Notes:   Available from 2007 only. For 1996/2004 the pipeline
            uses R&D expenditure (pulled automatically from WDI).

── 3. ECI (eci.csv) ────────────────────────────────────────────────
   Source:  https://atlas.hks.harvard.edu/data-downloads/
            OR Harvard Dataverse: doi:10.7910/DVN/XTAQMC
   Columns: iso3, country, year, ECI
   Notes:   Use the Harvard Growth Lab Atlas (NOT OEC).
            Annual data available from ~1995. The pipeline will
            snap to target years (1996, 2004, 2012, 2018, 2024).
            ⚠ Pin to pre-2026 methodology vintage.

── 4. HDR (hdr.csv) ────────────────────────────────────────────────
   Source:  https://hdr.undp.org/data-center/documentation-and-downloads
            → download the statistical annex tables
   Columns: iso3, country, year, EduIdx, LifeExpIdx
   Notes:   Both are 0-1 sub-indices of the HDI. Available for
            ~193 countries, recomputed back through the 1990s.

── 5. FSI (fsi.csv) ────────────────────────────────────────────────
   Source:  https://fragilestatesindex.org/excel/
   Columns: iso3, country, year, FSI (the 0-120 total score)
   Notes:   Available from 2005 only. For 1996/2004, the pipeline
            uses WGI Political Stability alone (pulled automatically).

══════════════════════════════════════════════════════════════════════
COLUMN NAME FLEXIBILITY:
  The loaders will attempt to auto-detect common column name
  variations (e.g. "country_name", "score", "location_code").
  But the cleanest path is to use the exact column names above.

AFTER PLACING FILES, RUN:
  python mi_pipeline.py

TO SEE THIS HELP AGAIN:
  python mi_pipeline.py --setup
══════════════════════════════════════════════════════════════════════
""".format(data_dir=DATA_DIR)
    print(instructions)


# ═══════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Modernization Index Data Pipeline")
    parser.add_argument("--setup", action="store_true",
                        help="Print data setup instructions and exit")
    parser.add_argument("--skip-api", action="store_true",
                        help="Skip World Bank API calls (use only local CSVs)")
    parser.add_argument("--data-dir", type=str, default=None,
                        help="Override data directory path")
    parser.add_argument("--output-dir", type=str, default=None,
                        help="Override output directory path")
    args = parser.parse_args()

    if args.setup:
        print_setup_instructions()
        return

    global DATA_DIR, OUTPUT_DIR
    if args.data_dir:
        DATA_DIR = Path(args.data_dir)
    if args.output_dir:
        OUTPUT_DIR = Path(args.output_dir)
    OUTPUT_DIR.mkdir(exist_ok=True)

    log.info("=" * 60)
    log.info("  MODERNIZATION INDEX — DATA PIPELINE")
    log.info("=" * 60)

    # ── Step 1: Fetch World Bank data ─────────────────────────
    if args.skip_api:
        log.info("Skipping World Bank API (--skip-api flag set)")
        # try loading from a cached file
        wb_cache = DATA_DIR / "wb_cached.csv"
        if wb_cache.exists():
            wb_data = pd.read_csv(wb_cache)
            log.info(f"Loaded cached WB data: {len(wb_data)} rows")
        else:
            wb_data = pd.DataFrame()
            log.warning("No cached WB data found. World Bank indicators will be missing.")
    else:
        log.info("Fetching World Bank indicators (WGI + WDI)...")
        wb_data = fetch_all_world_bank()
        if not wb_data.empty:
            # cache for future runs
            wb_cache = DATA_DIR / "wb_cached.csv"
            wb_data.to_csv(wb_cache, index=False)
            log.info(f"Cached WB data to {wb_cache}")

    # ── Step 2: Load manual CSVs ──────────────────────────────
    log.info("Loading manual data files...")
    cpi_data = load_cpi()
    gii_data = load_gii()
    eci_data = load_eci()
    hdr_data = load_hdr()
    fsi_data = load_fsi()

    # ── Step 3: Merge ─────────────────────────────────────────
    log.info("Merging all data sources...")
    master = merge_all(wb_data, cpi_data, gii_data, eci_data, hdr_data, fsi_data)
    log.info(f"Master panel: {len(master)} country-year observations, "
             f"{master['iso3'].nunique()} unique countries")

    if master.empty:
        log.error("No data collected. Run 'python mi_pipeline.py --setup' for instructions.")
        return

    # ── Step 4: Normalize ─────────────────────────────────────
    log.info("Normalizing indicators...")
    master = normalize(master)

    # ── Step 5: Pillar scores ─────────────────────────────────
    log.info("Computing pillar scores...")
    master = compute_pillars(master)

    # ── Step 6: Score v1 and v2 ───────────────────────────────
    log.info("Scoring v1 (anchor-based)...")
    master = score_v1(master)

    log.info("Scoring v2 (percentile-GPA)...")
    master = score_v2(master)

    # ── Step 7: Diagnostics ───────────────────────────────────
    log.info("Computing diagnostics...")
    master = compute_diagnostics(master)

    # ── Step 8: Reports ───────────────────────────────────────
    log.info("Generating coverage report...")
    report = coverage_report(master)
    print(report)

    log.info("Running analytical findings (Phase 6)...")
    findings = analytical_findings(master)
    print(findings)

    # ── Step 9: Write outputs ─────────────────────────────────
    log.info("Writing output files...")
    write_outputs(master, report, findings)

    # ── Summary ───────────────────────────────────────────────
    scoreable = master[master["gap_count"] <= 2] if "gap_count" in master.columns else master
    log.info("")
    log.info("=" * 60)
    log.info("  PIPELINE COMPLETE")
    log.info("=" * 60)
    log.info(f"  Total country-year observations: {len(master)}")
    log.info(f"  Scoreable observations (≤2 gaps): {len(scoreable)}")
    log.info(f"  Unique countries scored: {scoreable['iso3'].nunique()}")
    for year in TIME_POINTS:
        n = len(scoreable[scoreable["year"] == year])
        log.info(f"    {year}: {n} countries")
    log.info(f"\n  Output files in: {OUTPUT_DIR}/")
    log.info(f"    mi_master_dataset.csv")
    log.info(f"    mi_scored_countries.csv")
    log.info(f"    mi_complete.xlsx")
    log.info(f"    mi_coverage_report.txt")
    log.info(f"    mi_analytical_findings.txt")


if __name__ == "__main__":
    main()
