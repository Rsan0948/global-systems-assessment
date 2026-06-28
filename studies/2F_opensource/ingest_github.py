"""
REAL-DATA ingest for Study 2F (open-source viable-fork factor) from GitHub.

Run once to produce the committed cache `results/oss_forks_github.json`;
`oss_node.build_node` then loads it offline (same commit-the-derived-cache
pattern as rivers / NeuroMorpho / EDGAR -- the network crawl is not part of CI).

    python ingest_github.py                 # unauthenticated (60 req/hr, paced)
    GITHUB_TOKEN=ghp_xxx python ingest_github.py   # 5000 req/hr, larger n

Why the GitHub REST API and NOT GH Archive (per the handoff "loop me in"):
GH Archive ForkEvents are dominated by automated FORK-SPAM (botnets mass-fork
exploit/spam repos hundreds of times per hour) and carry no lifetime star count
(`forkee.stargazers_count` is ~0 at fork creation). The registered observable
needs the >stars VIABILITY filter -- exactly what removes that spam -- which
requires lifetime stars. The REST endpoint
    GET /repos/{owner}/{repo}/forks?sort=stargazers
returns a parent's forks sorted by current stars, giving the viability filter
directly. (Verified: GH Archive alone cannot define a "viable fork".)

Observable (PREREGISTRATION sec.4 / node doc, boundary probe):
    factor_parent = number of VIABLE forks of a popular parent repo,
where a viable fork is one whose own star count crossed a popularity threshold
(it attracted an independent following, not just a mirror/spam copy). This is
the software analogue of a branching ratio (viable children per parent).

Viability threshold: the node doc says "e.g. >100 stars" -- an illustrative
bar. Empirically >100-star forks are rare (most popular repos have 0), so the
PRIMARY threshold is >=10 stars ("a genuine independent following; filters the
0-star fork-spam"), with the full sensitivity {5,25,50,100} carried in the cache
(PREREGISTRATION sec.8). Parents with zero viable forks are popular projects
that did not viably subdivide; the ladder ratios use parents with >=1 viable
fork (the "projects above threshold" selection in the node doc).

Mechanism-free null (shipped by the node): the SAME preferential-attachment
process -- the boundary-probe high bar. Software has near-zero replication cost
(PREREGISTRATION sec.6), so the theory predicts it should NOT cleanly govern;
viable forks are expected heavy-tailed (PA), plausibly indistinguishable from
this null. A finding counts only if observed concentration BEATS PA.
"""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
CACHE = os.path.join(RESULTS, "oss_forks_github.json")

UA = "universalsystemgrade research (rubmatsan2001@gmail.com)"
PRIMARY_THRESHOLD = 10
SENS_THRESHOLDS = [5, 10, 25, 50, 100]


def _headers() -> dict:
    h = {"User-Agent": UA, "Accept": "application/vnd.github+json",
         "X-GitHub-Api-Version": "2022-11-28"}
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if tok:
        h["Authorization"] = f"Bearer {tok}"
    return h


def _get(url: str, tries: int = 6):
    """GET with rate-limit-aware waiting (sleeps until X-RateLimit-Reset)."""
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=_headers())
            r = urllib.request.urlopen(req, timeout=50)
            return json.loads(r.read()), dict(r.headers)
        except urllib.error.HTTPError as e:                       # noqa: PERF203
            hdrs = dict(e.headers or {})
            if e.code in (403, 429) and hdrs.get("X-RateLimit-Remaining") == "0":
                reset = int(hdrs.get("X-RateLimit-Reset", "0"))
                wait = max(5, reset - int(time.time()) + 3) if reset else 60
                print(f"      rate limited; sleeping {wait}s for reset ...", flush=True)
                time.sleep(min(wait, 3700))
                continue
            if e.code in (403, 429, 502, 503):
                time.sleep(5 + i * 5)
                continue
            raise
        except Exception:                                         # noqa: BLE001
            time.sleep(3 + i * 3)
    raise RuntimeError(f"failed: {url}")


# ----------------------------------------------------- step 1: popular parents
def popular_parents(target: int) -> list[dict]:
    """Spread of popular repos across star bands via the Search API."""
    bands = ["1000..2500", "2500..6000", "6000..15000", "15000..50000", "50000..400000"]
    out, seen = [], set()
    page_each = max(1, target // (len(bands) * 100) + 1)
    for band in bands:
        for pg in range(1, page_each + 1):
            q = urllib.parse.quote(f"stars:{band} forks:>50")
            url = (f"https://api.github.com/search/repositories?q={q}"
                   f"&sort=stars&order=desc&per_page=100&page={pg}")
            try:
                d, _ = _get(url)
            except Exception:                                     # noqa: BLE001
                break
            for r in d.get("items", []):
                fn = r["full_name"]
                if fn in seen:
                    continue
                seen.add(fn)
                out.append({"parent": fn, "parent_stars": r["stargazers_count"],
                            "total_forks": r["forks_count"]})
            time.sleep(2.0)                                        # search: ~30/min cap
    return out


# ----------------------------------------------- step 2: viable forks per parent
def viable_forks(parent: str) -> dict | None:
    """Return star counts of the parent's most-starred forks (page 1, sorted
    desc -- captures every fork above any threshold we test)."""
    url = f"https://api.github.com/repos/{parent}/forks?sort=stargazers&per_page=100"
    try:
        forks, _ = _get(url)
    except Exception:                                             # noqa: BLE001
        return None
    if not isinstance(forks, list):
        return None
    return {"fork_stars": sorted((f.get("stargazers_count", 0) for f in forks), reverse=True),
            "n_forks_page1": len(forks)}


# --------------------------------------------------------------- orchestration
def ingest(target_parents: int = 120, verbose: bool = True) -> dict:
    log = (lambda *a: print(*a, flush=True)) if verbose else (lambda *a: None)
    authed = bool(os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"))
    log(f"[1/2] fetching popular parent repos (authed={authed}) ...")
    parents = popular_parents(target_parents)
    log(f"      {len(parents)} candidate parents")

    log("[2/2] counting viable forks per parent (sorted by stars) ...")
    records = []
    for i, p in enumerate(parents):
        vf = viable_forks(p["parent"])
        if vf is None:
            continue
        stars = vf["fork_stars"]
        counts = {str(t): int(sum(s >= t for s in stars)) for t in SENS_THRESHOLDS}
        records.append({**p, "top_fork_stars": stars[0] if stars else 0,
                        "n_forks_page1": vf["n_forks_page1"], "viable_counts": counts})
        if verbose and (i + 1) % 20 == 0:
            log(f"      {i+1}/{len(parents)} parents scanned, {len(records)} usable")
        time.sleep(0.2)

    # ladder ratios at the primary threshold: parents with >=1 viable fork
    pt = str(PRIMARY_THRESHOLD)
    ratios = [r["viable_counts"][pt] for r in records if r["viable_counts"][pt] >= 1]
    sens = {}
    for t in SENS_THRESHOLDS:
        vals = [r["viable_counts"][str(t)] for r in records if r["viable_counts"][str(t)] >= 1]
        sens[str(t)] = {"n_parents_with_viable": len(vals),
                        "mean": round(sum(vals) / len(vals), 3) if vals else None,
                        "max": max(vals) if vals else 0}

    payload = {
        "observable": "viable forks per popular parent repo (branching ratio); "
                      "viable = fork stars >= threshold (PREREGISTRATION sec.4, boundary probe)",
        "primary_threshold_stars": PRIMARY_THRESHOLD,
        "sensitivity_thresholds": SENS_THRESHOLDS,
        "source": "GitHub REST API /repos/{p}/forks?sort=stargazers (lifetime stars); "
                  "GH Archive rejected -- fork-spam + no lifetime stars",
        "authed": authed,
        "coverage": {"parents_scanned": len(parents), "parents_usable": len(records),
                     "parents_with_viable_primary": len(ratios)},
        "sensitivity": sens,
        "fields": ["parent", "parent_stars", "total_forks", "top_fork_stars", "viable_counts"],
        "records": records,
        "ratios": ratios,
    }
    os.makedirs(RESULTS, exist_ok=True)
    with open(CACHE, "w") as f:
        json.dump(payload, f, indent=2)
    log(f"\nwrote {CACHE}")
    if ratios:
        import statistics
        log("      primary thr>=%d: n=%d parents, viable-fork count min=%d median=%.1f max=%d"
            % (PRIMARY_THRESHOLD, len(ratios), min(ratios), statistics.median(ratios), max(ratios)))
        log("      sensitivity n(with viable): " + str({k: v["n_parents_with_viable"] for k, v in sens.items()}))
    return payload


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=int, default=120)
    ingest(target_parents=ap.parse_args().target)
