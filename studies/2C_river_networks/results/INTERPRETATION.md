# Study 2C — interpretation of the runnable (simulated) results

These results are from **simulated data**. They say nothing about real rivers.
They are the pre-registration's required calibration/power analysis plus a
pipeline check. Read them as "does the measuring instrument work and is it
honest," not as evidence for or against the theory.

## 1. Pipeline demo (`pipeline_summary.json`, `pipeline_demo_rb.png`)

Run on 1,500 basins of neutral random-coalescent topology (no *e* built in):

- center (KDE mode) ≈ **2.98**, 95% CI ≈ **[2.96, 2.99]**
- best point model = **"3"**; **Tier 2** (CI isolates a small value but it is
  **not** *e*; *e* = 2.718 lies outside the CI)

This is the honesty check passing: a neutral topology lands near 3, and the
procedure **declines to call it *e***. If this demo had returned Tier 1, the
instrument would be manufacturing the answer, and we would not trust it on
real data.

## 2. Power grid (`power_grid.json`, `power_curve.png`)

Under **ideal conditions** — per-basin Rb drawn exactly lognormal around an
exact center — the procedure separates a true-*e* world from a true-3 world
with essentially **100% power even at n = 100**, and Bayes factors blow up to
10³⁰–∞. *Do not read this as "the test is easy and we're fine."* It is the
opposite warning: the test is **over-certain** precisely because the simulated
world has zero model misspecification. Real basins are not exactly lognormal
around one fixed center, so these BFs are unrealistically large.

## 3. The misspecification probe — why the Tier criterion was changed

We simulated a true center of **2.85**, i.e. *between* e (2.718) and 3.0, so
**neither point hypothesis is correct**:

| n basins | picks "e" | picks "3" | median BF(e:3) |
|---------:|----------:|----------:|---------------:|
| 300      | 61%       | 39%       | 11             |
| 1000     | 62%       | 38%       | 1.8 × 10²      |
| 3000     | 68%       | 32%       | 1.3 × 10⁷      |

The point-model Bayes factor **diverges toward *e*** as n grows, "decisively"
endorsing a value that is **wrong**. This is the classic pathology of fixed
point hypotheses with large samples: the test rewards *nearer*, not *correct*.

**Consequence (acted on before any real data):** the Tier-1 criterion in the
pre-registration was changed from "BF(e vs 3) ≥ 10" to "the 95% CI on the
center **includes e and excludes both 3 and π**." Under the new criterion, a
true-2.85 world correctly *fails* Tier 1 because its center CI tightens around
2.85 and excludes *e*. Point-model Bayes factors are retained only as
descriptive fit statistics.

## 4. What real HydroSHEDS data is still needed to decide

Nothing here tests the theory. To do that, run `python run.py --hydrosheds
<layer>` on real data and read off:

- the center CI of the pooled real-basin Rb distribution, and
- which Tier it triggers.

The pre-registered expectation is sobering for the strong claim: the river
literature commonly reports Rb ≈ 4, and **if the real center CI includes 4 and
excludes *e*, Tier 1 fails in the domain that was supposed to be its strongest
evidence.** That clause is fixed in advance, which is the entire point.
