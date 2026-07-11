# The Fragmentation Census

**Restructured question (2026-06-27).** The project began as a test for a
*universal* subdivision constant across self-organizing systems. The real data
**rejected** that: no shared value (I² ≈ 0.98), the pooled CI excludes *e*, and
the rung-4 mechanism test came back null. What *survived* — robustly — is the
per-system finding: **rivers and neurons each have a stable, characteristic
branching factor that beats chance.**

So the question is restructured around that survivor:

> **Which natural systems have a consistent fragmentation point — a characteristic
> branching/splitting factor that is *concentrated* AND *beats its own
> mechanism-free null* — and what is each one's number?**

This is a **census**, not a universality test. No pooling, no shared-constant
claim, no ladder. Each system stands alone and earns a place iff:

1. **Concentrated** — within-system CV < 0.30 (it *has* a characteristic value), and
2. **Beats its null** — that value is significantly displaced (two-sided
   bootstrap p < 0.05) from the system's mechanism-free random-topology null
   (so it is not just free combinatorics — random binary trees already sit ~3).

Systems that are concentrated but sit *at* their null are reported as
**candidate — trivial**; dispersed systems as **candidate — dispersed**. The
catalog reports the honest verdict for every system, lawful or not.

## How a system is measured
Any rooted branching tree is fed to the shared Horton–Strahler instrument
(`natural-systems/rivers/horton.py`) — the *same* code that measures rivers
and neurons — yielding one bifurcation ratio Rb per individual. A system's
fragmentation factor is the geometric mean across its individuals.

## Current catalog (seed)
`python census/run.py` → `census/results/catalog.md` + `census_forest.png`.

Lawful so far: **rivers (3.49)** and **six neuron cell types (2.9–3.7)** — seven
natural systems, all with a concentrated factor that beats the ~3.0 null.
Contrast (non-lawful) entries — corporate splits, engineered specs, taxonomic
classification — show what *failing* the bar looks like.

## Being added (real, free, no-login data)
Botanical trees · blood vessels (retinal) · leaf venation · lung airways ·
fungal/mycelial networks. Each is wired as a `census/systems/<x>_node.py` that
exposes `ratios` (per-individual Rb) and a mechanism-free `null_sampler`; the
runner picks it up automatically.
