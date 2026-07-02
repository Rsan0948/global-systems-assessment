"""
Fragmentation census runner.

    python run.py

Measures, for every available branching/fragmentation system, its characteristic
factor and whether that factor is a LAWFUL fragmentation point (concentrated AND
beats its mechanism-free null -- see catalog.py). No pooling, no universality
claim: a CATALOG of natural systems and their numbers.

Systems are added as their real-data ingests land; the runner skips any whose
data is not yet present, so it always runs. Outputs -> ./results.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "integration"))
from catalog import assess_system, to_dict  # noqa: E402
import function_dim  # noqa: E402

RESULTS = os.path.join(HERE, "results")


def _load(modpath, name):
    spec = importlib.util.spec_from_file_location(name, modpath)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


def _nodes_or_skip(fn):
    """Run a node builder; return [] (and warn) if its real data isn't present."""
    try:
        out = fn()
        return out if isinstance(out, list) else [out]
    except FileNotFoundError as e:
        print(f"  [skip] {e}")
        return []
    except Exception as e:                            # noqa: BLE001
        print(f"  [skip] {type(e).__name__}: {e}")
        return []


def collect_systems():
    """(node, kind) for every available branching/fragmentation system."""
    out = []

    # --- NATURAL branching trees (measured by the shared Strahler/Horton tool) ---
    rivers = _load(os.path.join(ROOT, "studies/2C_river_networks/river_node.py"), "river2c")
    for nd in _nodes_or_skip(rivers.build_node):
        out.append((nd, "natural"))

    neuro = _load(os.path.join(ROOT, "studies/2D_biological_branching/neuro_node.py"), "neuro2d")
    for nd in _nodes_or_skip(neuro.build_nodes):
        out.append((nd, "natural"))

    # --- NEW natural systems (added as ingests land; see census/systems/) ---
    for rel, mod, builder in [
        ("systems/trees_node.py", "trees_node", "build_node"),
        ("systems/languages_node.py", "languages_node", "build_node"),
        ("systems/vessels_node.py", "vessels_node", "build_nodes"),
        ("systems/leaf_node.py", "leaf_node", "build_node"),
        ("systems/lung_node.py", "lung_node", "build_node"),
        ("systems/fungal_node.py", "fungal_node", "build_node"),
    ]:
        path = os.path.join(HERE, rel)
        if not os.path.exists(path):
            continue
        m = _load(path, mod)
        for nd in _nodes_or_skip(getattr(m, builder)):
            out.append((nd, "natural"))

    # --- CONTRAST entries (non-natural / boundary -- show what NON-lawful looks like) ---
    try:
        corp = _load(os.path.join(ROOT, "studies/2B_corporate/corporate_node.py"), "corp2b")
        for nd in _nodes_or_skip(corp.build_node):
            out.append((nd, "contrast"))
    except Exception:                                # noqa: BLE001
        pass
    try:
        nc = _load(os.path.join(ROOT, "studies/4_negative_controls/real_controls.py"), "nc4real")
        for nd in _nodes_or_skip(lambda: [nc.engineered_node(), nc.classification_node()]):
            out.append((nd, "contrast"))
    except Exception:                                # noqa: BLE001
        pass
    return out


def main():
    os.makedirs(RESULTS, exist_ok=True)
    systems = collect_systems()
    entries = []
    for i, (nd, kind) in enumerate(systems):
        e = assess_system(nd.name, nd.ratios, nd.null_sampler, kind=kind,
                          source=getattr(nd, "source", ""), seed=i)
        entries.append(e)

    natural = [e for e in entries if e.kind == "natural"]
    lawful = [e for e in natural if e.lawful]
    catalog = {
        "question": "Which natural systems have a consistent fragmentation point "
                    "(concentrated factor that beats its mechanism-free null)?",
        "n_systems": len(entries),
        "n_natural": len(natural),
        "n_lawful": len(lawful),
        "lawful_systems": [e.name for e in lawful],
        "lawful_factor_range": ([round(min(e.factor for e in lawful), 2),
                                 round(max(e.factor for e in lawful), 2)] if lawful else None),
        "function_dimension": function_dim.analyze(entries),
        "entries": [to_dict(e) for e in entries],
    }
    with open(os.path.join(RESULTS, "catalog.json"), "w") as f:
        json.dump(catalog, f, indent=2)
    _write_markdown(catalog, entries)
    _forest(entries)

    print(f"\nFragmentation census: {len(natural)} natural systems, "
          f"{len(lawful)} with a LAWFUL fragmentation point.")
    print(f"{'system':22s} {'n':>5s} {'factor':>7s} {'CV':>5s} {'null':>6s}  verdict")
    for e in entries:
        print(f"{e.name:22s} {e.n:5d} {e.factor:7.2f} {e.cv:5.2f} {e.null_factor:6.2f}  {e.verdict}")
    print("\nresults/catalog.json, results/catalog.md, results/census_forest.png")


def _write_markdown(catalog, entries):
    lines = ["# Fragmentation census\n",
             f"> {catalog['question']}\n",
             f"**{catalog['n_lawful']} of {catalog['n_natural']} natural systems** have a "
             f"lawful fragmentation point"
             + (f" (factors {catalog['lawful_factor_range'][0]}–{catalog['lawful_factor_range'][1]})."
                if catalog['lawful_factor_range'] else ".") + "\n",
             "| system | kind | n | factor | 95% CI | CV | null | vs null | lawful? |",
             "|---|---|---:|---:|---|---:|---:|:--:|:--:|"]
    for e in entries:
        mark = "✅" if e.lawful else ("⚪" if e.concentrated or e.beats_null else "❌")
        lines.append(f"| {e.name} | {e.kind} | {e.n} | **{e.factor}** | "
                     f"[{e.ci_low}, {e.ci_high}] | {e.cv} | {e.null_factor} | "
                     f"{e.direction} | {mark} |")
    lines.append("\n✅ lawful (concentrated + beats null) · ⚪ candidate · ❌ not lawful\n")
    with open(os.path.join(RESULTS, "catalog.md"), "w") as f:
        f.write("\n".join(lines))


def _forest(entries):
    entries = sorted(entries, key=lambda e: e.factor)
    fig, ax = plt.subplots(figsize=(8, max(4, 0.42 * len(entries))))
    for i, e in enumerate(entries):
        color = "#1a7f37" if e.lawful else ("#9a6700" if (e.concentrated or e.beats_null) else "#cf222e")
        ax.plot([e.ci_low, e.ci_high], [i, i], color=color, lw=2, zorder=2)
        ax.scatter([e.factor], [i], color=color, zorder=3,
                   marker=("o" if e.kind == "natural" else "s"))
        ax.scatter([e.null_factor], [i], color="grey", marker="|", s=80, zorder=3)
    ax.set_yticks(range(len(entries)))
    ax.set_yticklabels([e.name for e in entries])
    ax.set_xlabel("characteristic fragmentation factor (| = its null)")
    ax.set_title("Fragmentation census — natural systems and their numbers")
    ax.axvline(3.0, ls=":", color="#aaa", lw=1)
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS, "census_forest.png"), dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    main()
