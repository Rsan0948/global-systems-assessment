#!/usr/bin/env python3
"""
Refresh the WGI/WDI source snapshot the Data API reads from.

Pulls the World Bank 2025-anchored WGI (.SC, 6 dims) + WDI (GDP PPP / resource
rents / ODA) for every entity already in data/sources/wb_anchored.json and rewrites
that file. This is the "pull straight from source" step: run it to propagate fresh
World Bank data to every case (mi.datasource reads this file; no per-country copies).

Vintage-consistent with the mi-pipeline panel (same World Bank API + .SC series).

    python scripts/refresh_wgi_wdi.py            # refresh existing entities
    python scripts/refresh_wgi_wdi.py --add COD  # also add an ISO3 (by code)
"""
import argparse
import json
import sys
import time
import urllib.request
from pathlib import Path

SNAP = Path(__file__).resolve().parent.parent / "data" / "sources" / "wb_anchored.json"
WGI = {"GE": "GOV_WGI_GE.SC", "RL": "GOV_WGI_RL.SC", "RQ": "GOV_WGI_RQ.SC",
       "CC": "GOV_WGI_CC.SC", "VA": "GOV_WGI_VA.SC", "PV": "GOV_WGI_PV.SC"}
WDI = {"gdp": "NY.GDP.PCAP.PP.CD", "rents": "NY.GDP.TOTL.RT.ZS", "oda": "DT.ODA.ODAT.GN.ZS"}


def _get(url):
    for _ in range(6):
        try:
            with urllib.request.urlopen(url, timeout=45) as r:
                return json.load(r)
        except Exception:
            time.sleep(2)
    return None


def _series(iso, code, source):
    src = "&source=3" if source else ""
    d = _get(f"https://api.worldbank.org/v2/country/{iso}/indicator/{code}"
             f"?format=json{src}&date=1996:2024&per_page=80")
    if isinstance(d, list) and len(d) > 1 and d[1]:
        return {r["date"]: round(r["value"], 2) for r in d[1] if r and r.get("value") is not None}
    return {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--add", action="append", default=[], help="ISO3 codes to add (name=ISO via --name)")
    ap.add_argument("--name", action="append", default=[], help="display name(s) matching --add order")
    args = ap.parse_args()

    snap = json.loads(SNAP.read_text()) if SNAP.exists() else {}
    # name -> iso for existing
    targets = {name: rec["iso3"] for name, rec in snap.items()}
    for i, iso in enumerate(args.add):
        nm = args.name[i] if i < len(args.name) else iso
        targets[nm] = iso

    for name, iso in targets.items():
        rec = {"iso3": iso, "wgi": {}, "wdi": {}}
        for k, code in WGI.items():
            rec["wgi"][k] = _series(iso, code, source=True)
        for k, code in WDI.items():
            rec["wdi"][k] = _series(iso, code, source=False)
        snap[name] = rec
        print(f"refreshed {name} ({iso}) — {len(rec['wgi']['GE'])} WGI years", flush=True)

    SNAP.write_text(json.dumps(snap, indent=2))
    print(f"wrote {SNAP} ({len(snap)} entities)")


if __name__ == "__main__":
    main()
