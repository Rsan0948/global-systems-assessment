# Why do these systems fragment? (cited)

A literature synthesis for the census. **It carries one load-bearing, somewhat
deflationary result that reshapes how we must read the whole project** — so it is
stated first.

## 0. The load-bearing finding: a bifurcation ratio ~3–4 is *statistically near-inevitable*

A Horton bifurcation ratio in the **3–5 band is a near-automatic property of being
a binary branching tree at all** — with or without any optimization, growth law,
or function.

- **Shreve (1966, 1967)** — a *topologically random* population of channel networks
  (all distinct networks equally likely, by analogy to a perfect gas) already
  obeys Horton's law of stream numbers, with the bifurcation ratio driven toward
  **~4** purely combinatorially. *J. Geology* 74:17; 75:178.
- **Kirchner (1993)** — the decisive null. Monte-Carlo over all networks formable
  from N₁ first-order streams: **96% of bifurcation ratios fall in 3 ≤ Rb ≤ 5**,
  the range called "typical" of real rivers. Deliberately non-random subsets
  (elongated vs compact) have nearly identical Rb (3.9 vs 3.7). Conclusion:
  Horton's laws "describe virtually all possible networks… they therefore compel
  no particular conclusion about the origin or structure of stream networks."
  *Geology* 21:591.

**Implication for this census.** Measuring a clustered Rb near ~3 is, by itself,
weak evidence — it is largely what *any* tree does. This is exactly why the census
requires every system to **beat its own random-topology null** (`catalog.py`); the
"beats null" gate is not optional polish, it is the whole inferential weight. And
it is why our earlier **rung-4 result (the dimensional gap did not predict the
ratio) is consistent with the field, not a failure**: there is no predictive ratio
law to recover.

## 1. No accepted theory predicts a specific bifurcation *ratio*

Every optimization theory of branching predicts **scaling exponents or diameter
laws — never a daughter-count ratio.** Where a branching number appears, it is an
*assumed input*, not a derived constant.

| System | Principle (refs) | What it actually predicts | Predicts Rb? |
|---|---|---|---|
| Rivers | min energy dissipation / OCN (Rodríguez-Iturbe & Rinaldo 1997; Rinaldo 2014) | drainage-area exponent β≈0.45; 3 universality classes | **No** (reproduces the *range*) |
| Vasculature | Murray's law (Murray 1926; Sherman 1981) | radius law r_p³=Σr_d³ | **No** (radius, not count) |
| Metabolism | WBE space-filling fractal (West, Brown & Enquist 1997) | quarter-power allometry; β=n^−1/2, γ=n^−1/3 | **No** (n is a free input) |
| Neurons | wiring economy (Chklovskii 2002/04; Cuntz 2010); Rall (1959) | arbor shape/placement; diameter exp 3/2 | **No** |
| Trees | pipe model (Shinozaki 1964); area-preservation (Eloy 2011) | cross-section conservation; exp ≈2 | **No** |

The river-network originators themselves frame it as **"feasible optimality"** —
networks reach *locally accessible* minima — and warn that **topology alone yields
"spurious similarities"**; energy minimization buys you *universality classes
(exponent relations)*, not a number (Rinaldo, Rigon, Banavar, Maritan,
Rodríguez-Iturbe, *PNAS* 2014). WBE's quarter-power law is itself contested
(Kozłowski & Konarzewski 2004; Banavar et al. 1999, 2010; Glazier 2005).

## 2. The functional story that *is* defensible

What the lawful systems share is a **kind**, not a constant: they are all
**distribution-or-collection networks that service a space under a transport/
construction cost**, grown by a *local, iterated* process under a *universal*
physical constraint (gravity, diffusion, mechanics, wiring cost). The factor is
the equilibrium of coverage-vs-cost. This explains *that* they fragment lawfully
and *why ~3* (binary division iterated into a hierarchy) — but **not** the precise
value, which §0–1 say no theory delivers.

Binary (not trinary) branching is empirically robust: 3-D reconstructions of lung
(Metzger et al. 2008, *Nature*) and kidney (Short et al. 2014) show stereotyped
bifurcation; observed trifurcations "resolve into bifurcations" during growth
(Lang et al. 2021). *(The popular "trifurcations are mathematically non-generic"
theorem could not be sourced and one Turing-pattern model finds the opposite —
do not assert it.)*

## 3. Why engineered / designed hierarchies don't show a consistent factor

**Correct framing: self-organization vs. top-down design — NOT natural vs.
human-made.** Self-organized *human* systems (cities) show consistent scaling
(Bettencourt et al. 2007, *PNAS*; Bettencourt 2013, *Science*), so "biology vs
engineering" invites an immediate counterexample.

- The one on-point empirical paper: **Yang et al. (2017)**, engineered urban
  drainage vs natural rivers — engineered networks scale *differently* (linear
  length–area when small, exponents outside the natural band, more heterogeneous,
  non-random branching), approaching river-like statistics only as they grow and
  self-organize. arXiv:1707.04911 / *WRR*.
- **The clean Horton-Rb comparison for software / org-chart / taxonomy hierarchies
  has not been done in the literature** — our negative controls (CV 6× higher,
  Brown–Forsythe p≈10⁻²⁵¹) are a genuine contribution, not a citable echo.
- **"Self-organization compresses outcome space; design to heterogeneous
  objectives expands it"** is *our hypothesis*, supported by convergent indirect
  evidence (OCN funnels into 3 universality classes; Yang 2017's heterogeneity),
  not an established citation.

## 4. What this means for the census (the steer)

1. **Keep the "beats null" gate central** — it is the only thing that makes a
   clustered Rb meaningful (Kirchner).
2. **The ratio alone is a weak observable.** The literature's discriminating
   quantities are **linked scaling exponents** (drainage-area β, diameter laws,
   allometric exponents). The strongest future version of this census measures
   *exponents per system*, not just Rb. (Rinaldo 2014's own recommendation.)
3. **Frame the contrast as self-organized vs. designed**, and treat the
   "design expands outcome space" thesis as our hypothesis to test, not a result
   to cite.

*Reference list and per-claim verification flags: see the project notes; several
primary PDFs were paywalled and corroborated via secondary sources (flagged).*
