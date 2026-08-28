"""
REAL-DATA ingest for Study 2B (corporate split factor) from SEC EDGAR.

Run once to produce the committed cache `results/corporate_splits_edgar.json`;
`corporate_node.build_node` then loads that cache offline (same pattern as the
rivers / NeuroMorpho ingests -- the raw network fetch is NOT part of CI, only
the small derived cache is committed and replayed).

    python ingest_edgar.py --start 2001 --end 2024

Observable (PREREGISTRATION sec.4, unchanged from the placeholder node):
    split factor = (resulting viable public entities) / (parent reportable
                   internal divisions) * SCALE
                 = E / S * 3.0
a comparable RATIO -- successors per internal division -- never a raw count.

Pipeline (all free SEC EDGAR endpoints, no login; identifying User-Agent only):
  1. EDGAR full-text search (efts.sec.gov) -> every INITIAL Form 10-12B
     (registration of a spun-off company; one filing == one SpinCo).
  2. For each SpinCo, fetch its Information Statement and extract the PARENT
     ("...being distributed by [PARENT]", "a subsidiary of [PARENT]", ...).
  3. Resolve the parent name -> CIK (EDGAR company_tickers.json).
  4. Group SpinCos by parent CIK -> a split EVENT; successors E = 1 (the parent
     continues) + (# SpinCos it spun off in the window). Serial/simultaneous
     break-ups (Tyco, GE, DuPont, Danaher) give E > 2; the common single
     spin-off gives E = 2.
  5. Parse the parent's reportable-segment count S from its 10-K text
     (XBRL `NumberOfReportableSegments` is NOT tagged by the large firms that
     spin off, so the count is read from the 10-K narrative).
  6. factor = E / S * 3.0, one value per parent that executed a spin-off.

Mechanism-free null (shipped by the node): a "binary-by-default" process -- the
mundane expectation that a firm splits in TWO relative to its actual segment
structure. Same real S distribution, E drawn from ~2 + small Poisson noise. The
corporate signal counts only as the part of E/S that exceeds this binary
baseline (i.e. firms that fragment into MORE than two viable pieces per
division). This is the triviality control (PREREGISTRATION sec.3).
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import time
import urllib.parse
import urllib.request
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
CACHE = os.path.join(RESULTS, "corporate_splits_edgar.json")

UA = os.environ.get(
    "USG_HTTP_USER_AGENT",
    "universalsystemgrade research; contact via github.com/Rsan0948/universalsystemgrade",
)
SCALE = 3.0                        # same unit scaling as the placeholder node
_NUMWORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
             "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}


# ----------------------------------------------------------------- HTTP helper
def _get(url: str, tries: int = 5) -> bytes:
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": UA, "Accept-Encoding": "gzip, deflate"})
            r = urllib.request.urlopen(req, timeout=60)
            data = r.read()
            if r.headers.get("Content-Encoding") == "gzip":
                data = gzip.decompress(data)
            return data
        except Exception as e:                       # noqa: BLE001 - network retry
            last = e
            time.sleep(1.0 + i * 1.5)
    raise last


def _text(html: bytes) -> str:
    t = html.decode("utf-8", "ignore")
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"&nbsp;|&#160;|&#xa0;", " ", t)
    return re.sub(r"\s+", " ", t)


# -------------------------------------------------------- step 1: SpinCo list
def list_spincos(start: int, end: int, throttle: float = 0.15) -> list[dict]:
    """Every INITIAL Form 10-12B filing in [start, end] (drop /A amendments)."""
    out, seen = [], set()
    for yr in range(start, end + 1):
        frm = 0
        while True:
            u = ("https://efts.sec.gov/LATEST/search-index?forms=10-12B"
                 f"&startdt={yr}-01-01&enddt={yr}-12-31&from={frm}")
            try:
                d = json.loads(_get(u))
            except Exception:                        # noqa: BLE001
                break
            hits = d["hits"]["hits"]
            for h in hits:
                s = h["_source"]
                if s["form"] != "10-12B":
                    continue
                cik = s["ciks"][0]
                if cik in seen:
                    continue
                seen.add(cik)
                out.append({"cik": cik.lstrip("0"),
                            "name": s["display_names"][0].split("  (CIK")[0].strip(),
                            "date": s["file_date"], "adsh": s["adsh"]})
            tot = d["hits"]["total"]["value"]
            frm += len(hits)
            if frm >= tot or not hits:
                break
            time.sleep(throttle)
        time.sleep(throttle)
    return out


# ------------------------------------------------- step 2: parent from filing
_PARENT_PATS = [
    r"being distributed by\s+([A-Z][A-Za-z0-9&.,'\-]+(?: [A-Z][A-Za-z0-9&.,'\-]+){0,4})",
    r"distribution by\s+([A-Z][A-Za-z0-9&.,'\-]+(?: [A-Z][A-Za-z0-9&.,'\-]+){0,4})",
    r"a (?:wholly[- ]owned )?subsidiary of\s+([A-Z][A-Za-z0-9&.,'\-]+(?: [A-Z][A-Za-z0-9&.,'\-]+){0,4})",
    r"separation from\s+([A-Z][A-Za-z0-9&.,'\-]+(?: [A-Z][A-Za-z0-9&.,'\-]+){0,4})",
    r"stockholders of\s+([A-Z][A-Za-z0-9&.,'\-]+(?: [A-Z][A-Za-z0-9&.,'\-]+){0,4})\s+(?:in connection|as of)",
]
_STOP = {"the", "our", "this", "each", "all", "such", "its", "their", "common"}


def _normalize_parent(v: str) -> str:
    v = v.strip().rstrip(".,").strip()
    v = re.sub(r"\s+(Inc|Corp|Corporation|Company|Co|Holdings|Group|plc|Ltd|LLC|L\.P|LP|N\.V|S\.A)\b\.?.*$",
               "", v).strip()
    return v


def parent_of(spinco: dict) -> str | None:
    cik, adsh = spinco["cik"], spinco["adsh"].replace("-", "")
    base = f"https://www.sec.gov/Archives/edgar/data/{cik}/{adsh}/"
    try:
        items = json.loads(_get(base + "index.json"))["directory"]["item"]
    except Exception:                                # noqa: BLE001
        return None
    htms = [(it["name"], int(it.get("size", 0) or 0)) for it in items
            if it["name"].lower().endswith((".htm", ".html"))
            and "index" not in it["name"].lower()]
    htms.sort(key=lambda x: -x[1])
    for dn, _ in htms[:2]:                            # largest 1-2 docs = info statement
        try:
            t = _text(_get(base + dn))
        except Exception:                            # noqa: BLE001
            continue
        for p in _PARENT_PATS:
            m = re.search(p, t)
            if m:
                v = _normalize_parent(m.group(1))
                if len(v) > 3 and v.lower() not in _STOP:
                    return v
    return None


# ----------------------------------------- step 3: parent name -> CIK resolver
def load_ticker_index() -> dict:
    d = json.loads(_get("https://www.sec.gov/files/company_tickers.json"))
    idx = {}
    for v in d.values():
        idx[_normalize_parent(v["title"]).upper()] = v["cik_str"]
    return idx


def _token_set(s: str) -> set:
    return {w for w in re.split(r"[^A-Z0-9]+", s.upper()) if len(w) > 1}


def resolve_cik(name: str, idx: dict) -> int | None:
    """Resolve a parent name to a CIK: exact, then token-overlap, then EDGAR
    company search as a fallback (handles delisted / renamed parents)."""
    import difflib
    key = _normalize_parent(name).upper()
    if key in idx:
        return idx[key]
    m = difflib.get_close_matches(key, list(idx.keys()), n=1, cutoff=0.82)
    if m:
        return idx[m[0]]
    # token-set containment (e.g. "EXELON" vs "EXELON" within longer titles)
    kt = _token_set(key)
    if kt:
        best, bestj = None, 0.0
        for title, cik in idx.items():
            tt = _token_set(title)
            if not tt:
                continue
            j = len(kt & tt) / len(kt | tt)
            if j > bestj:
                best, bestj = cik, j
        if bestj >= 0.6:
            return best
    # fallback: EDGAR company search by name
    try:
        u = ("https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company="
             + urllib.parse.quote(key) + "&type=10-K&output=atom&count=1")
        t = _get(u).decode("utf-8", "ignore")
        mm = re.search(r"CIK=(\d+)", t) or re.search(r"<cik>(\d+)</cik>", t)
        if mm:
            return int(mm.group(1))
    except Exception:                                # noqa: BLE001
        pass
    return None


# ------------------------------------------- step 5: parent reportable segments
def _segments_from_text(t: str) -> int | None:
    t = t.lower()
    cands = []
    for m in re.finditer(
            r"(\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)"
            r"\s+reportable\s+(?:operating\s+|business\s+)?segments", t):
        w = m.group(1)
        v = _NUMWORDS.get(w, int(w) if w.isdigit() else None)
        if v and 1 <= v <= 12:
            cands.append(v)
    for m in re.finditer(
            r"(?:operate|manage|organized|report|aggregated into|have)\s+"
            r"(?:our business\s+|results\s+|operations\s+)?(?:in|into|through|as|under)?\s*"
            r"(one|two|three|four|five|six|seven|eight|nine|ten|\d{1,2})\s+"
            r"(?:reportable\s+|business\s+|operating\s+)?segments", t):
        w = m.group(1)
        v = _NUMWORDS.get(w, int(w) if w.isdigit() else None)
        if v and 1 <= v <= 12:
            cands.append(v)
    if not cands:
        return None
    return Counter(cands).most_common(1)[0][0]


def reportable_segments(cik: int, near_year: int | None = None) -> int | None:
    """Read the parent's reportable-segment count S from its 10-K narrative,
    preferring the 10-K filed closest to (and at or before) the spin-off year."""
    cik10 = str(cik).zfill(10)
    try:
        sub = json.loads(_get(f"https://data.sec.gov/submissions/CIK{cik10}.json"))
    except Exception:                                # noqa: BLE001
        return None
    recent = sub["filings"]["recent"]
    tenks = [(recent["filingDate"][i], recent["accessionNumber"][i].replace("-", ""),
              recent["primaryDocument"][i])
             for i, f in enumerate(recent["form"]) if f == "10-K" and recent["primaryDocument"][i]]
    if not tenks:
        return None
    if near_year is not None:
        # prefer the latest 10-K filed on/before near_year+1, else closest
        tenks.sort(key=lambda x: (abs(int(x[0][:4]) - near_year), int(x[0][:4]) > near_year))
    for date, acc, doc in tenks[:3]:                 # try up to 3 nearest 10-Ks
        base = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc}/"
        try:
            s = _segments_from_text(_text(_get(base + doc)))
        except Exception:                            # noqa: BLE001
            s = None
        if s:
            return s
        time.sleep(0.05)
    return None


# --------------------------------------------------------------- orchestration
def ingest(start: int = 2001, end: int = 2024, throttle: float = 0.12,
           verbose: bool = True) -> dict:
    log = (lambda *a: print(*a)) if verbose else (lambda *a: None)
    log(f"[1/5] listing 10-12B SpinCos {start}-{end} ...")
    spincos = list_spincos(start, end, throttle)
    log(f"      {len(spincos)} SpinCos")

    log("[2/5] extracting parents from information statements ...")
    by_parent: dict[str, list[dict]] = defaultdict(list)
    parsed = 0
    for i, sc in enumerate(spincos):
        par = parent_of(sc)
        if par:
            sc["parent_raw"] = par
            by_parent[par.upper()].append(sc)
            parsed += 1
        if verbose and (i + 1) % 50 == 0:
            log(f"      {i+1}/{len(spincos)} scanned, {parsed} parents parsed")
        time.sleep(throttle)
    log(f"      parsed parent for {parsed}/{len(spincos)} SpinCos; "
        f"{len(by_parent)} distinct parents")

    log("[3/5] resolving parent CIKs ...")
    idx = load_ticker_index()

    log("[4/5+5] grouping events and reading parent segment counts ...")
    events, seg_cache = [], {}
    for pkey, scs in by_parent.items():
        name = scs[0]["parent_raw"]
        cik = resolve_cik(name, idx)
        if cik is None:
            continue
        ev_year = min(int(sc["date"][:4]) for sc in scs)
        if cik not in seg_cache:
            seg_cache[cik] = reportable_segments(cik, near_year=ev_year)
            time.sleep(throttle)
        S = seg_cache[cik]
        if not S:
            continue
        E = 1 + len(scs)                              # parent continues + spuncos
        years = sorted({sc["date"][:4] for sc in scs})
        events.append({
            "parent": name, "parent_cik": int(cik),
            "successors_E": int(E), "segments_S": int(S),
            "factor": round(E / S * SCALE, 4),
            "spincos": [sc["name"] for sc in scs],
            "years": years,
        })
    events.sort(key=lambda e: e["parent"])
    ratios = [e["factor"] for e in events]
    payload = {
        "observable": "split factor = resulting viable entities E per parent "
                      "reportable segment S, scaled x%.1f (PREREGISTRATION sec.4)" % SCALE,
        "scale": SCALE,
        "source": "SEC EDGAR full-text search (10-12B) + 10-K segment narrative",
        "window": [start, end],
        "coverage": {
            "spincos_listed": len(spincos),
            "parents_parsed": parsed,
            "distinct_parents": len(by_parent),
            "events_with_segments": len(events),
        },
        "fields": ["parent", "parent_cik", "successors_E", "segments_S", "factor"],
        "events": events,
        "ratios": ratios,
        "real_S_pool": sorted(int(e["segments_S"]) for e in events),
    }
    os.makedirs(RESULTS, exist_ok=True)
    with open(CACHE, "w") as f:
        json.dump(payload, f, indent=2)
    log(f"\nwrote {CACHE}: {len(events)} split events")
    if ratios:
        import statistics
        log("      factor: n=%d min=%.2f median=%.2f max=%.2f" % (
            len(ratios), min(ratios), statistics.median(ratios), max(ratios)))
        log("      E distribution: %s" % dict(sorted(Counter(e["successors_E"] for e in events).items())))
        log("      S distribution: %s" % dict(sorted(Counter(e["segments_S"] for e in events).items())))
    return payload


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, default=2001)
    ap.add_argument("--end", type=int, default=2024)
    ap.add_argument("--throttle", type=float, default=0.12)
    ingest(**vars(ap.parse_args()))
