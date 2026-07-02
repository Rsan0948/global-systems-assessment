"""
Supplementary indicator ingestion (non-World-Bank sources), merged into the
world panel `data/countries/*.json`:

  * CPI  — Transparency International Corruption Perceptions Index, via OWID
           (0-100, 2012+). Fills P1's corruption sub-indicator (engine prefers
           cpi over WGI control-of-corruption).
  * ECI  — Harvard Atlas Economic Complexity Index (eci_hs92), from the local
           `studies/2A_political_fragmentation/data/harvard_eci.csv`. Adds P2's
           second indicator (~-2.5..+2.5, engine min-max normalizes).
  * FSI  — Fund for Peace Fragile States Index "Total" (0-120), per-year xlsx.
           Adds P5's second indicator (engine inverts: lower fragility = higher).

GII is deliberately NOT ingested: WIPO publishes only PDFs / an interactive
explorer, with no free authoritative machine-readable time series. P2's
innovation slot keeps the R&D-expenditure proxy (the spec's track-2 substitute)
rather than a non-authoritative third-party mirror. Missing values stay null.

Run: python scripts/ingest_supplementary.py
"""

from __future__ import annotations

import csv
import glob
import io
import json
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COUNTRIES = ROOT / "data" / "countries"
ECI_CSV = ROOT.parent / "studies" / "2A_political_fragmentation" / "data" / "harvard_eci.csv"
UA = {"User-Agent": "Mozilla/5.0 (MI-research supplementary ingest)"}

FSI_URLS = [
    "https://fragilestatesindex.org/wp-content/uploads/2023/06/FSI-2023-DOWNLOAD.xlsx",
    "https://fragilestatesindex.org/wp-content/uploads/2022/07/fsi-2022-download.xlsx",
    "https://fragilestatesindex.org/wp-content/uploads/2021/05/fsi-2021.xlsx",
    "https://fragilestatesindex.org/wp-content/uploads/2020/05/fsi-2020.xlsx",
    "https://fragilestatesindex.org/wp-content/uploads/2019/04/fsi-2019.xlsx",
    "https://fragilestatesindex.org/wp-content/uploads/2018/04/fsi-2018.xlsx",
] + [f"https://fragilestatesindex.org/wp-content/uploads/data/fsi-{y}.xlsx"
     for y in range(2017, 2005, -1)]


def _get(url: str, binary=False, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                return r.read() if binary else r.read().decode("utf-8-sig", errors="replace")
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(1.5 * (i + 1))


def load_country_index():
    """Return (files, name2iso3). name2iso3 maps normalized names -> iso3."""
    files, name2iso3 = {}, {}
    for p in glob.glob(str(COUNTRIES / "*.json")):
        d = json.loads(Path(p).read_text())
        iso3 = d.get("iso3")
        if not iso3:
            continue
        files[iso3] = Path(p)
        name2iso3[_norm(d["country"])] = iso3
    # FSI naming quirks -> iso3
    for name, iso in {
        "congo democratic republic": "COD", "congo republic": "COG",
        "cote divoire": "CIV", "ivory coast": "CIV", "slovak republic": "SVK",
        "korea republic": "KOR", "korea democratic republic": "PRK",
        "russia": "RUS", "syria": "SYR", "iran": "IRN", "venezuela": "VEN",
        "cape verde": "CPV", "swaziland": "SWZ", "eswatini": "SWZ",
        "macedonia": "MKD", "north macedonia": "MKD", "kyrgyz republic": "KGZ",
        "micronesia": "FSM", "brunei darussalam": "BRN", "the gambia": "GMB",
        "gambia": "GMB", "laos": "LAO", "moldova": "MDA", "tanzania": "TZA",
        "bolivia": "BOL", "egypt": "EGY", "yemen": "YEM", "vietnam": "VNM",
        "czech republic": "CZE", "united states": "USA", "cabo verde": "CPV",
        "sao tome and principe": "STP", "guinea bissau": "GNB",
        "israel and west bank": "ISR", "turkey": "TUR", "turkiye": "TUR",
        "somalia": "SOM", "slovakia": "SVK", "kyrgyzstan": "KGZ",
        "north korea": "PRK", "south korea": "KOR", "bahamas": "BHS",
        "palestine": "PSE", "west bank and gaza": "PSE",
    }.items():
        name2iso3.setdefault(name, iso)
    return files, name2iso3


def _norm(s: str) -> str:
    import unicodedata
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    s = s.lower().strip()
    s = re.sub(r"[,\.\(\)'`]", "", s)
    s = s.replace("&", "and").replace("-", " ")
    s = re.sub(r"\brep\b", "republic", s)
    s = re.sub(r"\bdem\b", "democratic", s)
    return " ".join(s.split())


def fetch_cpi() -> dict:
    """iso3 -> {year: cpi 0-100}."""
    t = _get("https://ourworldindata.org/grapher/TI-corruption-perception-index.csv?csvType=full")
    out = {}
    for r in csv.DictReader(io.StringIO(t)):
        iso3, y = r.get("Code"), r.get("Year")
        v = r.get("Corruption Perceptions Index")
        if iso3 and len(iso3) == 3 and v not in (None, ""):
            out.setdefault(iso3, {})[y] = round(float(v), 2)
    return out


def fetch_eci() -> dict:
    """iso3 -> {year: eci value}. Prefer hs92, fall back hs12/sitc."""
    out = {}
    with open(ECI_CSV, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            iso3, y = r.get("country_iso3_code"), r.get("year")
            v = r.get("eci_hs92") or r.get("eci_hs12") or r.get("eci_sitc")
            if iso3 and y and v not in (None, ""):
                try:
                    out.setdefault(iso3, {})[y] = round(float(v), 4)
                except ValueError:
                    pass
    return out


def fetch_fsi(name2iso3: dict) -> tuple[dict, set]:
    """iso3 -> {year: fsi total 0-120}. Returns (data, unmatched_names)."""
    import openpyxl
    out, unmatched = {}, set()
    for url in FSI_URLS:
        try:
            raw = _get(url, binary=True)
            wb = openpyxl.load_workbook(io.BytesIO(raw), read_only=True, data_only=True)
            ws = wb.active
            rows = ws.iter_rows(values_only=True)
            header = [str(h or "").strip().lower() for h in next(rows)]
            ci = header.index("country"); yi = header.index("year"); ti = header.index("total")
            for row in rows:
                if row[ci] is None or row[ti] is None:
                    continue
                iso3 = name2iso3.get(_norm(str(row[ci])))
                if not iso3:
                    unmatched.add(str(row[ci]))
                    continue
                yr = row[yi]
                yr = yr.year if hasattr(yr, "year") else int(yr)
                out.setdefault(iso3, {})[str(yr)] = round(float(row[ti]), 2)
        except Exception as e:  # noqa: BLE001
            print(f"  FSI {url.split('/')[-1]}: FAILED ({e})")
    return out, unmatched


def merge_into_panel(files, cpi, eci, fsi):
    added = {"cpi": 0, "eci": 0, "fsi": 0}
    for iso3, path in files.items():
        d = json.loads(path.read_text())
        iby = d.setdefault("indicators_by_year", {})
        changed = False
        for field, series in (("cpi", cpi), ("eci", eci), ("fsi", fsi)):
            for y, v in series.get(iso3, {}).items():
                rec = iby.setdefault(y, {})
                if rec.get(field) is None:
                    rec[field] = v
                    if "_gaps" in rec and field in rec["_gaps"]:
                        rec["_gaps"].remove(field)
                    added[field] += 1
                    changed = True
        if changed:
            d.setdefault("data_sources", {}).update({
                "cpi": "Transparency International CPI via OWID (0-100, 2012+)",
                "eci": "Harvard Atlas Economic Complexity Index eci_hs92 (~-2.5..+2.5)",
                "fsi": "Fund for Peace Fragile States Index Total (0-120)",
            })
            path.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
    return added


def main():
    files, name2iso3 = load_country_index()
    print(f"{len(files)} country files indexed")
    print("fetching CPI (OWID)...");   cpi = fetch_cpi();  print(f"  {sum(len(v) for v in cpi.values())} values, {len(cpi)} countries")
    print("loading ECI (Harvard)...")
    eci = fetch_eci();  print(f"  {sum(len(v) for v in eci.values())} values, {len(eci)} countries")
    print("fetching FSI (Fund for Peace, 18 xlsx)...")
    fsi, unmatched = fetch_fsi(name2iso3)
    print(f"  {sum(len(v) for v in fsi.values())} values, {len(fsi)} countries")
    if unmatched:
        print(f"  FSI unmatched names ({len(unmatched)}): {sorted(unmatched)[:20]}")
    added = merge_into_panel(files, cpi, eci, fsi)
    print(f"\nmerged into panel: {added}")


if __name__ == "__main__":
    main()
