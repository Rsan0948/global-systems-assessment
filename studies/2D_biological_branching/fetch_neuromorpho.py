"""
REAL biology ingest (Study 2D): neuronal/dendritic arbor branching from
NeuroMorpho.org.

Each neuron's standardized CNG.swc reconstruction is a rooted tree (the SWC
`parent` pointer runs toward the soma = downstream), so the SAME Strahler/Horton
instrument used for rivers (studies/2C/horton.py) measures a per-arbor Horton
bifurcation ratio Rb with zero new statistics. One Rb per neuron is the unit of
analysis, exactly as one Rb per river basin.

Sub-domains are mechanistically-distinct cell types (pyramidal, Purkinje,
granule, ganglion, interneuron, motoneuron) -- independent natural experiments
with different dendritic growth programs, mirroring how rivers/biology treat
each subsystem as its own domain.

Caches per-arbor (rb, max_order, r2) to results/rb_bio_<celltype>.json; the raw
.swc files are not stored. Free API, no key. Run:
    python fetch_neuromorpho.py
"""

from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
sys.path.insert(0, os.path.join(HERE, "..", "2C_river_networks"))
from horton import measure_basin  # noqa: E402

API = "https://neuromorpho.org/api"
SUBDOMAINS = ["pyramidal", "Purkinje", "granule", "ganglion", "interneuron", "Motoneuron"]
TARGET_PER = 150          # successful (>=3 order) measurements wanted per sub-domain
POOL_PER = 700            # candidate neurons to consider per sub-domain
PER_ARCHIVE_CAP = 50      # avoid one lab/archive dominating a sub-domain
MIN_ORDERS = 3            # neuron arbors are smaller than river basins
_UA = {"User-Agent": "universalsystemgrade-research"}


def _get(url, timeout=40):
    return urllib.request.urlopen(urllib.request.Request(url, headers=_UA), timeout=timeout).read()


def list_neurons(cell_type: str, pool: int = POOL_PER):
    """Return [(neuron_name, archive), ...] candidates for a cell type."""
    q = urllib.parse.quote(f'cell_type:"{cell_type}"')
    out, page, size = [], 0, 500
    while len(out) < pool:
        url = f"{API}/neuron/select?q={q}&size={size}&page={page}&sort=neuron_id,asc"
        try:
            d = json.loads(_get(url))
        except Exception:
            break
        recs = d.get("_embedded", {}).get("neuronResources", [])
        if not recs:
            break
        out += [(r["neuron_name"], r["archive"]) for r in recs]
        if page >= d.get("page", {}).get("totalPages", 1) - 1:
            break
        page += 1
    return out[:pool]


def swc_to_downstream(swc: str) -> dict[int, int]:
    """SWC text -> {node_id: downstream_id}; root parent -1 -> outlet sentinel."""
    downstream = {}
    for line in swc.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        p = line.split()
        nid, parent = int(p[0]), int(p[6])
        downstream[nid] = parent if parent != -1 else -1
    return downstream


def measure_one(name: str, archive: str):
    """Download CNG.swc, measure Rb. Returns (rb, max_order, r2) or None."""
    arch = urllib.parse.quote(archive.lower())
    nm = urllib.parse.quote(name)
    url = f"{API.replace('/api','')}/dableFiles/{arch}/CNG%20version/{nm}.CNG.swc"
    try:
        swc = _get(url).decode("utf-8", "replace")
        m = measure_basin(swc_to_downstream(swc), min_orders=MIN_ORDERS)
        return (round(float(m.rb), 6), int(m.max_order), round(float(m.r_squared), 6))
    except Exception:
        return None


def fetch_subdomain(cell_type: str):
    cands = list_neurons(cell_type)
    rng = np.random.default_rng(hash(cell_type) % (2**32))
    idx = rng.permutation(len(cands))
    records, per_arch = [], {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {}
        for i in idx:
            name, archive = cands[i]
            if per_arch.get(archive, 0) >= PER_ARCHIVE_CAP:
                continue
            per_arch[archive] = per_arch.get(archive, 0) + 1
            futs[ex.submit(measure_one, name, archive)] = archive
            if len(futs) >= POOL_PER:
                break
        for f in as_completed(futs):
            r = f.result()
            if r is not None:
                records.append(list(r))
            if len(records) >= TARGET_PER:
                break
    return records


def main():
    os.makedirs(RESULTS, exist_ok=True)
    for ct in SUBDOMAINS:
        recs = fetch_subdomain(ct)
        rbs = np.array([r[0] for r in recs]) if recs else np.array([])
        payload = {
            "cell_type": ct,
            "source": "NeuroMorpho.org CNG.swc reconstructions (free API)",
            "min_orders_floor": MIN_ORDERS,
            "n_arbors": len(recs),
            "geom_mean_rb": float(np.exp(np.log(rbs).mean())) if rbs.size else None,
            "fields": ["rb", "max_order", "r_squared"],
            "records": recs,
        }
        out = os.path.join(RESULTS, f"rb_bio_{ct.lower()}.json")
        with open(out, "w") as f:
            json.dump(payload, f)
        gm = payload["geom_mean_rb"]
        print(f"{ct:12s}: {len(recs):3d} arbors  geom-mean Rb="
              f"{gm:.3f}" if gm else f"{ct:12s}: 0 arbors")


if __name__ == "__main__":
    main()
