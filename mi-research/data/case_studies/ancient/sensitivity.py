#!/usr/bin/env python3
"""Sensitivity analysis for Track 3 ancient cases.

Instead of point-estimate MI scores, computes plausible BANDS by varying
each indicator within confidence-based uncertainty margins:

  HIGH confidence:     ±0.10  (well-attested, multiple sources agree)
  MODERATE confidence: ±0.15  (reasonable evidence, some interpretation)
  LOW confidence:      ±0.25  (sparse evidence, significant guesswork)

For each case/timepoint:
  1. Computes worst-case (all indicators at low end) and best-case (high end)
     pillar and MI scores
  2. Reports the MI band as [low, high]
  3. Checks whether the band is narrow enough that the qualitative conclusion
     (relative ranking, tier) is stable regardless of disagreement

The key claim: "even if you disagree with every indicator coding within
reasonable bounds, the MI stays within this band."
"""
import json, math
from pathlib import Path

WEIGHTS = {"P1": 0.34, "P2": 0.15, "P3": 0.16, "P4": 0.20, "P5": 0.16}

UNCERTAINTY = {
    "HIGH": 0.10,
    "MODERATE": 0.15,
    "LOW": 0.25,
}

def clamp(v): return max(0.0, min(1.0, v))

def mi_from_pillars(pillars):
    total_w = sum(WEIGHTS[p] for p in WEIGHTS if p in pillars)
    return sum(pillars[p] * WEIGHTS[p] for p in WEIGHTS if p in pillars) / total_w

def analyze_case(case, tp_key):
    tp = case[tp_key]
    point_pillars = {}
    low_pillars = {}
    high_pillars = {}
    details = {}

    for pillar in WEIGHTS:
        indicators = tp[pillar]["indicators"]
        point_vals = []
        low_vals = []
        high_vals = []
        ind_details = {}

        for ind_key, ind_data in indicators.items():
            val = ind_data["value"]
            unc = UNCERTAINTY[ind_data["confidence"]]
            lo = clamp(val - unc)
            hi = clamp(val + unc)

            point_vals.append(val)
            low_vals.append(lo)
            high_vals.append(hi)

            ind_details[ind_key] = {
                "value": val,
                "confidence": ind_data["confidence"],
                "uncertainty": unc,
                "range": [round(lo, 2), round(hi, 2)],
            }

        point_pillars[pillar] = sum(point_vals) / len(point_vals)
        low_pillars[pillar] = sum(low_vals) / len(low_vals)
        high_pillars[pillar] = sum(high_vals) / len(high_vals)
        details[pillar] = {
            "point": round(point_pillars[pillar], 3),
            "band": [round(low_pillars[pillar], 3), round(high_pillars[pillar], 3)],
            "indicators": ind_details,
        }

    mi_point = mi_from_pillars(point_pillars)
    mi_low = mi_from_pillars(low_pillars)
    mi_high = mi_from_pillars(high_pillars)

    return {
        "mi_point": round(mi_point, 3),
        "mi_band": [round(mi_low, 3), round(mi_high, 3)],
        "mi_width": round(mi_high - mi_low, 3),
        "pillars": details,
    }


def main():
    data_path = Path(__file__).parent / "ancient_cases.json"
    cases = json.load(open(data_path))

    all_results = []

    print("=" * 100)
    print("TRACK 3 SENSITIVITY ANALYSIS — Confidence-Based MI Bands")
    print("Uncertainty: HIGH ±0.10 | MODERATE ±0.15 | LOW ±0.25")
    print("=" * 100)

    for case in cases:
        name = case["name"]
        for tp_key in ["peak", "pre_stress"]:
            result = analyze_case(case, tp_key)
            result["case"] = name
            result["timepoint"] = tp_key
            all_results.append(result)

    # Sort by MI point for ranking
    peak_results = sorted(
        [r for r in all_results if r["timepoint"] == "peak"],
        key=lambda r: r["mi_point"], reverse=True
    )

    print(f"\n{'─' * 100}")
    print(f"  PEAK MI RANKINGS (with confidence bands)")
    print(f"{'─' * 100}")
    print(f"  {'Rank':<5} {'Case':<30} {'MI':>6} {'Band':>16} {'Width':>7}  {'Overlap?':<30}")

    prev_band = None
    for i, r in enumerate(peak_results):
        overlap = ""
        if prev_band:
            if r["mi_band"][1] >= prev_band[0]:
                overlap = f"↕ overlaps #{i} above"
        print(f"  {i+1:<5} {r['case']:<30} {r['mi_point']:>6.3f} "
              f"[{r['mi_band'][0]:.3f}–{r['mi_band'][1]:.3f}] "
              f"{r['mi_width']:>6.3f}  {overlap}")
        prev_band = r["mi_band"]

    # Show pillar-level detail for a few cases
    print(f"\n{'─' * 100}")
    print(f"  PILLAR BAND DETAIL (selected cases)")
    print(f"{'─' * 100}")

    for case in cases[:5]:
        name = case["name"]
        r = next(x for x in all_results if x["case"] == name and x["timepoint"] == "peak")
        print(f"\n  {name} [peak] — MI {r['mi_point']:.3f} [{r['mi_band'][0]:.3f}–{r['mi_band'][1]:.3f}]")
        for p in ["P1", "P2", "P3", "P4", "P5"]:
            pd = r["pillars"][p]
            print(f"    {p}: {pd['point']:.3f} [{pd['band'][0]:.3f}–{pd['band'][1]:.3f}]")
            for ind_key, ind in pd["indicators"].items():
                print(f"      {ind_key:<25} {ind['value']:.2f} ±{ind['uncertainty']:.2f} "
                      f"[{ind['range'][0]:.2f}–{ind['range'][1]:.2f}]  {ind['confidence']}")

    # Check ranking stability: do bands overlap?
    print(f"\n{'=' * 100}")
    print(f"RANKING STABILITY ANALYSIS")
    print(f"{'=' * 100}")

    stable_pairs = 0
    unstable_pairs = 0
    total_pairs = 0

    for i in range(len(peak_results)):
        for j in range(i + 1, len(peak_results)):
            total_pairs += 1
            r1 = peak_results[i]
            r2 = peak_results[j]
            if r1["mi_band"][0] <= r2["mi_band"][1]:
                unstable_pairs += 1
            else:
                stable_pairs += 1

    print(f"  Pairwise ranking comparisons (peak): {total_pairs}")
    print(f"  Stable (bands don't overlap):  {stable_pairs} ({100*stable_pairs/total_pairs:.0f}%)")
    print(f"  Overlapping (could swap rank): {unstable_pairs} ({100*unstable_pairs/total_pairs:.0f}%)")

    # ── Natural tier breaks ──
    # Score every adjacent gap by three measures:
    #   1. point_gap:   difference between adjacent point estimates
    #   2. band_gap:    lower-bound of higher case minus upper-bound of lower case
    #                   (positive = no overlap; negative = overlap)
    #   3. overlap_pct: what fraction of the narrower band is consumed by overlap
    #                   (0% = clean break; 100% = one band is inside the other)
    gaps = []
    for i in range(len(peak_results) - 1):
        r1 = peak_results[i]      # higher-ranked
        r2 = peak_results[i + 1]  # lower-ranked
        point_gap = r1["mi_point"] - r2["mi_point"]
        band_gap = r1["mi_band"][0] - r2["mi_band"][1]
        overlap = max(0, r2["mi_band"][1] - r1["mi_band"][0])
        narrower = min(r1["mi_width"], r2["mi_width"])
        overlap_pct = (overlap / narrower * 100) if narrower > 0 else 0
        gaps.append({
            "position": i,
            "above": r1["case"],
            "below": r2["case"],
            "point_gap": round(point_gap, 3),
            "band_gap": round(band_gap, 3),
            "overlap_pct": round(overlap_pct, 1),
            "score": point_gap,
        })

    # Pick the best N-1 cuts (for N tiers). Choose cuts at the widest
    # point-estimate gaps, but penalize cuts where bands heavily overlap.
    gaps_ranked = sorted(gaps, key=lambda g: g["score"], reverse=True)

    # Try 3, 4, and 5 tiers; pick the one where each tier has ≥2 members
    # and the weakest cut still has a reasonable score.
    def build_tiers(n_cuts, min_group=3):
        """Pick top n_cuts gaps, skipping any that would create a group < min_group."""
        chosen = []
        for g in gaps_ranked:
            trial = sorted(chosen + [g["position"]])
            # check all resulting groups
            starts = [0] + [c + 1 for c in trial]
            ends = [c + 1 for c in trial] + [len(peak_results)]
            sizes = [e - s for s, e in zip(starts, ends)]
            if all(sz >= min_group for sz in sizes):
                chosen.append(g["position"])
            if len(chosen) == n_cuts:
                break
        cuts = sorted(chosen)
        tiers = []
        start = 0
        for cut in cuts:
            tiers.append(peak_results[start:cut + 1])
            start = cut + 1
        tiers.append(peak_results[start:])
        return tiers, cuts

    # Try increasing numbers of cuts; build_tiers now skips gaps that create
    # groups smaller than 3, so we just need max tier ≤ 10.
    best_n = 3
    for n in range(3, min(8, len(peak_results) // 3)):
        tiers_try, cuts_try = build_tiers(n, min_group=3)
        if len(cuts_try) < n:
            break  # ran out of valid gaps
        max_size = max(len(t) for t in tiers_try)
        if max_size <= 10:
            best_n = n
            break
        best_n = n  # keep going, accept best we found
    tiers, cuts = build_tiers(best_n, min_group=3)

    tiers, cuts = build_tiers(best_n)
    n_tiers = len(tiers)
    labels = [f"Tier {i+1}" for i in range(n_tiers)]
    named = {
        2: ["Upper", "Lower"],
        3: ["High", "Middle", "Low"],
        4: ["High", "Mid-High", "Mid-Low", "Low"],
        5: ["High", "Mid-High", "Middle", "Mid-Low", "Low"],
        6: ["Highest", "High", "Mid-High", "Mid-Low", "Low", "Lowest"],
    }
    if n_tiers in named:
        labels = named[n_tiers]

    print(f"\n  GAP ANALYSIS (adjacent cases sorted by separation strength):")
    print(f"  {'Above':<28} {'Below':<28} {'Pt Gap':>7} {'Band Gap':>9} {'Overlap%':>9} {'Score':>7}")
    for g in gaps_ranked:
        marker = " ◄ CUT" if g["position"] in cuts else ""
        print(f"  {g['above']:<28} {g['below']:<28} {g['point_gap']:>7.3f} "
              f"{g['band_gap']:>+9.3f} {g['overlap_pct']:>8.1f}% {g['score']:>7.3f}{marker}")

    print(f"\n{'─' * 100}")
    print(f"  NATURAL TIERS ({best_n + 1} groups, cut at {best_n} widest gaps)")
    print(f"{'─' * 100}")

    groups = []  # for machine-readable output
    for ti, tier in enumerate(tiers):
        lo_pt = min(r["mi_point"] for r in tier)
        hi_pt = max(r["mi_point"] for r in tier)
        lo_band = min(r["mi_band"][0] for r in tier)
        hi_band = max(r["mi_band"][1] for r in tier)
        label = labels[ti]

        print(f"\n  ┌─ {label} (MI {lo_pt:.3f}–{hi_pt:.3f}, band envelope [{lo_band:.3f}–{hi_band:.3f}])")
        for r in tier:
            print(f"  │   {r['case']:<30} {r['mi_point']:.3f}  [{r['mi_band'][0]:.3f}–{r['mi_band'][1]:.3f}]")
        print(f"  └─")

        groups.append({
            "tier": ti + 1,
            "label": label,
            "mi_range": [round(lo_pt, 3), round(hi_pt, 3)],
            "mi_envelope": [round(lo_band, 3), round(hi_band, 3)],
            "cases": [r["case"] for r in tier],
        })

        # Within-tier stability: do any pairwise bands NOT overlap?
        non_overlapping = 0
        total_in_tier = 0
        for a in range(len(tier)):
            for b in range(a + 1, len(tier)):
                total_in_tier += 1
                if tier[a]["mi_band"][0] > tier[b]["mi_band"][1]:
                    non_overlapping += 1
        if total_in_tier > 0 and non_overlapping > 0:
            print(f"        ⚠  {non_overlapping}/{total_in_tier} pairs within this tier "
                  f"don't overlap — consider splitting further")

    # Between-tier robustness
    print(f"\n  BETWEEN-TIER ROBUSTNESS:")
    for ti in range(len(tiers) - 1):
        above = tiers[ti]
        below = tiers[ti + 1]
        worst_above = min(r["mi_band"][0] for r in above)
        best_below = max(r["mi_band"][1] for r in below)
        margin = worst_above - best_below
        if margin > 0:
            print(f"    {labels[ti]:>10} vs {labels[ti+1]:<10}: clean break (margin {margin:.3f})")
        else:
            overlap_cases_above = [r["case"] for r in above if r["mi_band"][0] < best_below]
            overlap_cases_below = [r["case"] for r in below if r["mi_band"][1] > worst_above]
            print(f"    {labels[ti]:>10} vs {labels[ti+1]:<10}: overlap zone "
                  f"[{max(worst_above, min(r['mi_band'][0] for r in below)):.3f}"
                  f"–{min(best_below, max(r['mi_band'][1] for r in above)):.3f}]")
            if overlap_cases_above:
                print(f"      borderline (could drop): {', '.join(overlap_cases_above)}")
            if overlap_cases_below:
                print(f"      borderline (could rise):  {', '.join(overlap_cases_below)}")

    # Machine-readable output
    summary_path = Path(__file__).parent / "sensitivity_report.json"
    summary = {
        "method": "confidence-based uncertainty bands",
        "uncertainty_margins": UNCERTAINTY,
        "peak_ranking": [
            {
                "rank": i + 1,
                "case": r["case"],
                "mi_point": r["mi_point"],
                "mi_band": r["mi_band"],
                "mi_width": r["mi_width"],
                "pillars": {p: {"point": d["point"], "band": d["band"]}
                           for p, d in r["pillars"].items()},
            }
            for i, r in enumerate(peak_results)
        ],
        "tiers": groups,
        "gap_analysis": [
            {
                "above": g["above"], "below": g["below"],
                "point_gap": g["point_gap"], "band_gap": g["band_gap"],
                "overlap_pct": g["overlap_pct"], "is_cut": g["position"] in cuts,
            }
            for g in gaps_ranked
        ],
        "ranking_stability": {
            "total_pairs": total_pairs,
            "stable_pairs": stable_pairs,
            "stable_pct": round(100 * stable_pairs / total_pairs, 1),
        },
    }
    summary_path.write_text(json.dumps(summary, indent=2))
    print(f"\n\nMachine-readable report: {summary_path}")


if __name__ == "__main__":
    main()
