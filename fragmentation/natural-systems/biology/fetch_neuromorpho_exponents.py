"""
REAL allometric-exponent ingest for the rung-4 mechanism test (Study 2D / 3B).

The rung-4 apex (PREREGISTRATION sec.5) asks whether the interior-minus-interface
DIMENSIONAL GAP predicts the subdivision factor across domains. The placeholder
exponents were constant (gap=1) so the test could not run ("insufficient
exponent variation"). This estimates REAL per-cell-type exponents directly from
the NeuroMorpho CNG.swc 3-D reconstructions:

  * interior complexity  -> total dendritic LENGTH L (wire filling the arbor)
  * interface / boundary -> number of terminal TIPS (the arbor's sampling field)
  * system size          -> spatial RADIUS R (max Euclidean soma->node distance)

Per cell type, across its arbors, fit (OLS on logs):
    interior_exp  = d log L     / d log R       (how wiring scales with extent)
    interface_exp = d log(tips) / d log R       (how the terminal field scales)
    gap  Delta    = interior_exp - interface_exp

These vary by cell type (planar Purkinje vs 3-D pyramidal), giving the real
exponent variation the cross-cell-type gap->factor regression needs. Cached to
results/bio_exponents.json; neuro_node loads it. Free API, no key.

    python fetch_neuromorpho_exponents.py
"""

from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
CACHE = os.path.join(RESULTS, "bio_exponents.json")

API = "https://neuromorpho.org/api"
SUBDOMAINS = ["pyramidal", "Purkinje", "granule", "ganglion", "interneuron", "Motoneuron"]
TARGET_PER = 90
POOL_PER = 300
_UA = {"User-Agent": "universalsystemgrade-research"}


def _get(url, timeout=40):
    return urllib.request.urlopen(urllib.request.Request(url, headers=_UA), timeout=timeout).read()


def list_neurons(cell_type: str, pool: int = POOL_PER):
    q = urllib.parse.quote(f'cell_type:"{cell_type}"')
    out, page = [], 0
    while len(out) < pool:
        url = f"{API}/neuron/select?q={q}&size=500&page={page}&sort=neuron_id,asc"
        try:
            d = json.loads(_get(url))
        except Exception:                            # noqa: BLE001
            break
        recs = d.get("_embedded", {}).get("neuronResources", [])
        if not recs:
            break
        out += [(r["neuron_name"], r["archive"]) for r in recs]
        if page >= d.get("page", {}).get("totalPages", 1) - 1:
            break
        page += 1
    return out[:pool]


def arbor_metrics(name: str, archive: str):
    """(radius, total_length, n_tips) from the CNG.swc reconstruction, or None."""
    arch = urllib.parse.quote(archive.lower())
    nm = urllib.parse.quote(name)
    url = f"https://neuromorpho.org/dableFiles/{arch}/CNG%20version/{nm}.CNG.swc"
    try:
        swc = _get(url).decode("utf-8", "replace")
    except Exception:                                # noqa: BLE001
        return None
    nodes, parent = {}, {}
    for ln in swc.splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        p = ln.split()
        if len(p) < 7:
            continue
        nid = int(p[0])
        nodes[nid] = np.array([float(p[2]), float(p[3]), float(p[4])])
        parent[nid] = int(p[6])
    if len(nodes) < 10:
        return None
    soma = nodes[min(nodes)]
    nchild: dict[int, int] = {}
    for nid, par in parent.items():
        if par != -1:
            nchild[par] = nchild.get(par, 0) + 1
    length = 0.0
    radius = 0.0
    tips = 0
    for nid, par in parent.items():
        if par != -1 and par in nodes:
            length += float(np.linalg.norm(nodes[nid] - nodes[par]))
        radius = max(radius, float(np.linalg.norm(nodes[nid] - soma)))
        if nchild.get(nid, 0) == 0:
            tips += 1
    if length <= 0 or radius <= 0 or tips < 2:
        return None
    return (radius, length, tips)


def _ols_slope(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """Slope and its standard error for y ~ a + b x."""
    n = x.size
    xm, ym = x.mean(), y.mean()
    sxx = float(((x - xm) ** 2).sum())
    b = float(((x - xm) * (y - ym)).sum() / sxx)
    a = ym - b * xm
    resid = y - (a + b * x)
    s2 = float((resid ** 2).sum() / (n - 2))
    se = float(np.sqrt(s2 / sxx))
    return b, se


def fit_cell_type(cell_type: str) -> dict | None:
    cands = list_neurons(cell_type)
    rows = []
    with ThreadPoolExecutor(max_workers=10) as ex:
        futs = {ex.submit(arbor_metrics, n, a): n for n, a in cands}
        for f in as_completed(futs):
            r = f.result()
            if r is not None:
                rows.append(r)
            if len(rows) >= TARGET_PER:
                break
    if len(rows) < 20:
        return None
    arr = np.array(rows)
    logR = np.log(arr[:, 0])
    interior, interior_se = _ols_slope(logR, np.log(arr[:, 1]))   # length ~ R
    interface, interface_se = _ols_slope(logR, np.log(arr[:, 2]))  # tips ~ R
    return {"cell_type": cell_type, "n": len(rows),
            "interior_exp": round(interior, 4), "interior_se": round(interior_se, 4),
            "interface_exp": round(interface, 4), "interface_se": round(interface_se, 4),
            "gap": round(interior - interface, 4)}


def main():
    os.makedirs(RESULTS, exist_ok=True)
    out = {}
    for ct in SUBDOMAINS:
        r = fit_cell_type(ct)
        if r:
            out[ct.lower()] = r
            print(f"{ct:12s} n={r['n']:3d} interior={r['interior_exp']:.2f} "
                  f"interface={r['interface_exp']:.2f} gap={r['gap']:.2f}")
        else:
            print(f"{ct:12s} insufficient arbors")
    payload = {
        "source": "NeuroMorpho.org CNG.swc 3-D reconstructions (free API)",
        "observable": "interior=log(total dendritic length)/log(radius); "
                      "interface=log(n_terminal_tips)/log(radius); gap=interior-interface",
        "cell_types": out,
    }
    with open(CACHE, "w") as f:
        json.dump(payload, f, indent=2)
    gaps = [v["gap"] for v in out.values()]
    print(f"\nwrote {CACHE}: {len(out)} cell types, gap range "
          f"[{min(gaps):.2f}, {max(gaps):.2f}], std={np.std(gaps, ddof=1):.3f}")


if __name__ == "__main__":
    main()
