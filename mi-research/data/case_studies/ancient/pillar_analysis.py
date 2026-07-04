#!/usr/bin/env python3
"""Pillar-level sensitivity analysis for Track 3 ancient cases.

Instead of trying to total-order cases by composite MI, this decomposes
the analysis to where the formula earns its keep: per-pillar comparisons.

For each pillar, identifies:
  1. Which cases are clearly high/low even under uncertainty
  2. Which pairwise pillar comparisons survive the confidence bands
  3. Cross-pillar profiles: what makes each case distinctive

Confidence-based uncertainty:
  HIGH:     ±0.10
  MODERATE: ±0.15
  LOW:      ±0.25
"""
import json
from pathlib import Path

WEIGHTS = {"P1": 0.34, "P2": 0.15, "P3": 0.16, "P4": 0.20, "P5": 0.16}

PILLAR_NAMES = {
    "P1": "Institutional Quality",
    "P2": "Innovation & Knowledge",
    "P3": "Human Capital",
    "P4": "Economic Structure",
    "P5": "Stability & Resilience",
}

UNCERTAINTY = {"HIGH": 0.10, "MODERATE": 0.15, "LOW": 0.25}

def clamp(v): return max(0.0, min(1.0, v))


def pillar_band(tp, pillar):
    indicators = tp[pillar]["indicators"]
    point_vals, low_vals, high_vals = [], [], []
    for ind_data in indicators.values():
        val = ind_data["value"]
        unc = UNCERTAINTY[ind_data["confidence"]]
        point_vals.append(val)
        low_vals.append(clamp(val - unc))
        high_vals.append(clamp(val + unc))
    point = sum(point_vals) / len(point_vals)
    lo = sum(low_vals) / len(low_vals)
    hi = sum(high_vals) / len(high_vals)
    return round(point, 3), round(lo, 3), round(hi, 3)


def main():
    data_path = Path(__file__).parent / "ancient_cases.json"
    cases = json.load(open(data_path))

    # Build per-pillar data for peak timepoints
    pillar_data = {p: [] for p in WEIGHTS}
    for case in cases:
        tp = case["peak"]
        for p in WEIGHTS:
            point, lo, hi = pillar_band(tp, p)
            pillar_data[p].append({
                "case": case["name"],
                "point": point, "lo": lo, "hi": hi,
                "width": round(hi - lo, 3),
            })

    # Sort each pillar by point estimate
    for p in pillar_data:
        pillar_data[p].sort(key=lambda x: x["point"], reverse=True)

    print("=" * 110)
    print("PILLAR-LEVEL ANALYSIS — What's defensible per dimension")
    print("=" * 110)

    report = {}

    for p in ["P1", "P2", "P3", "P4", "P5"]:
        pname = PILLAR_NAMES[p]
        ranked = pillar_data[p]

        print(f"\n{'━' * 110}")
        print(f"  {p}: {pname}")
        print(f"{'━' * 110}")
        print(f"  {'Case':<30} {'Point':>6} {'Band':>16} {'Width':>6}")
        for r in ranked:
            print(f"  {r['case']:<30} {r['point']:>6.3f} [{r['lo']:.3f}–{r['hi']:.3f}] {r['width']:>6.3f}")

        # Find clearly-above-peers: cases whose LOW end is above the HIGH end of at least half the corpus
        n = len(ranked)
        clear_top = []
        clear_bottom = []
        for r in ranked:
            above_count = sum(1 for other in ranked if r["lo"] > other["hi"] and other["case"] != r["case"])
            below_count = sum(1 for other in ranked if r["hi"] < other["lo"] and other["case"] != r["case"])
            r["beats_clearly"] = above_count
            r["loses_clearly"] = below_count
            if above_count >= n // 2:
                clear_top.append(r)
            if below_count >= n // 2:
                clear_bottom.append(r)

        print(f"\n  DEFENSIBLE CLAIMS:")
        if clear_top:
            print(f"    Clearly above majority (worst-case > best-case of ≥{n//2} others):")
            for r in clear_top:
                print(f"      {r['case']:<28} (band [{r['lo']:.3f}–{r['hi']:.3f}], "
                      f"clearly beats {r['beats_clearly']}/{n-1})")
        else:
            print(f"    No case is clearly above majority — too much overlap at the top.")

        if clear_bottom:
            print(f"    Clearly below majority (best-case < worst-case of ≥{n//2} others):")
            for r in clear_bottom:
                print(f"      {r['case']:<28} (band [{r['lo']:.3f}–{r['hi']:.3f}], "
                      f"clearly below {r['loses_clearly']}/{n-1})")
        else:
            print(f"    No case is clearly below majority — too much overlap at the bottom.")

        # Count defensible pairwise comparisons
        defensible_pairs = 0
        total_pairs = n * (n - 1) // 2
        for i in range(n):
            for j in range(i + 1, n):
                if ranked[i]["lo"] > ranked[j]["hi"] or ranked[j]["lo"] > ranked[i]["hi"]:
                    defensible_pairs += 1

        print(f"\n    Pairwise: {defensible_pairs}/{total_pairs} comparisons "
              f"({100*defensible_pairs/total_pairs:.0f}%) survive uncertainty bands")

        report[p] = {
            "name": pname,
            "ranking": [{"case": r["case"], "point": r["point"],
                         "band": [r["lo"], r["hi"]], "beats_clearly": r["beats_clearly"]}
                        for r in ranked],
            "clear_top": [r["case"] for r in clear_top],
            "clear_bottom": [r["case"] for r in clear_bottom],
            "defensible_pairs": defensible_pairs,
            "total_pairs": total_pairs,
            "defensible_pct": round(100 * defensible_pairs / total_pairs, 1),
        }

    # ── CROSS-PILLAR PROFILES ──
    print(f"\n{'━' * 110}")
    print(f"  CROSS-PILLAR PROFILES — What makes each case distinctive")
    print(f"{'━' * 110}")
    print(f"  These use point estimates (not bands) to identify the shape of each case's")
    print(f"  modernization profile — where they're strongest vs weakest relative to their own average.\n")

    profiles = []
    for case in cases:
        tp = case["peak"]
        pillars = {}
        for p in WEIGHTS:
            point, lo, hi = pillar_band(tp, p)
            pillars[p] = {"point": point, "lo": lo, "hi": hi}
        avg = sum(pillars[p]["point"] for p in WEIGHTS) / 5
        strongest = max(WEIGHTS, key=lambda p: pillars[p]["point"])
        weakest = min(WEIGHTS, key=lambda p: pillars[p]["point"])
        spread = pillars[strongest]["point"] - pillars[weakest]["point"]

        # Is the strongest-vs-weakest distinction robust?
        strong_lo = pillars[strongest]["lo"]
        weak_hi = pillars[weakest]["hi"]
        profile_robust = strong_lo > weak_hi

        profiles.append({
            "case": case["name"],
            "pillars": pillars,
            "avg": round(avg, 3),
            "strongest": strongest,
            "weakest": weakest,
            "spread": round(spread, 3),
            "profile_robust": profile_robust,
        })

    profiles.sort(key=lambda x: x["avg"], reverse=True)

    for prof in profiles:
        pillars = prof["pillars"]
        bar = ""
        for p in ["P1", "P2", "P3", "P4", "P5"]:
            v = pillars[p]["point"]
            filled = int(v * 10)
            bar += f"  {p} {'█' * filled}{'░' * (10 - filled)} {v:.2f}"

        robust_marker = "✓" if prof["profile_robust"] else "~"
        strongest_name = PILLAR_NAMES[prof["strongest"]].split()[0]
        weakest_name = PILLAR_NAMES[prof["weakest"]].split()[0]

        print(f"  {prof['case']:<28} avg={prof['avg']:.3f}  "
              f"strongest={prof['strongest']}({strongest_name})  "
              f"weakest={prof['weakest']}({weakest_name})  "
              f"spread={prof['spread']:.2f} {robust_marker}")
        print(f"    {bar}")

    # ── DEFENSIBLE CROSS-CASE PILLAR COMPARISONS ──
    print(f"\n{'━' * 110}")
    print(f"  DEFENSIBLE CROSS-CASE CLAIMS (band-separated)")
    print(f"{'━' * 110}")
    print(f"  Statements of the form 'X has higher P_ than Y' that survive full uncertainty.\n")

    claims = []
    for p in WEIGHTS:
        ranked = pillar_data[p]
        for i in range(len(ranked)):
            for j in range(i + 1, len(ranked)):
                if ranked[i]["lo"] > ranked[j]["hi"]:
                    claims.append({
                        "pillar": p,
                        "higher": ranked[i]["case"],
                        "lower": ranked[j]["case"],
                        "margin": round(ranked[i]["lo"] - ranked[j]["hi"], 3),
                        "higher_band": [ranked[i]["lo"], ranked[i]["hi"]],
                        "lower_band": [ranked[j]["lo"], ranked[j]["hi"]],
                    })

    claims.sort(key=lambda c: c["margin"], reverse=True)

    # Show top claims per pillar
    for p in WEIGHTS:
        p_claims = [c for c in claims if c["pillar"] == p]
        print(f"\n  {p} ({PILLAR_NAMES[p]}) — {len(p_claims)} defensible comparisons:")
        for c in p_claims[:8]:
            print(f"    {c['higher']:<28} > {c['lower']:<28} "
                  f"(margin {c['margin']:.3f})")
        if len(p_claims) > 8:
            print(f"    ... and {len(p_claims) - 8} more")

    # ── SUMMARY STATISTICS ──
    total_claims = len(claims)
    total_possible = len(cases) * (len(cases) - 1) // 2 * 5
    print(f"\n{'━' * 110}")
    print(f"  SUMMARY")
    print(f"{'━' * 110}")
    print(f"  Total defensible pillar-level claims: {total_claims} / {total_possible} possible "
          f"({100*total_claims/total_possible:.0f}%)")
    print(f"  By pillar:")
    for p in WEIGHTS:
        p_claims = [c for c in claims if c["pillar"] == p]
        n_possible = len(cases) * (len(cases) - 1) // 2
        print(f"    {p} ({PILLAR_NAMES[p]:<25}): {len(p_claims):>3} / {n_possible} "
              f"({100*len(p_claims)/n_possible:.0f}%)")
    print(f"\n  These are the claims you can make that no reasonable scholarly disagreement")
    print(f"  (within the confidence margins) can overturn.")

    # Machine-readable output
    out = {
        "method": "pillar-level sensitivity with confidence bands",
        "uncertainty": UNCERTAINTY,
        "pillar_rankings": report,
        "profiles": [
            {"case": p["case"], "avg": p["avg"],
             "strongest": p["strongest"], "weakest": p["weakest"],
             "spread": p["spread"], "robust": p["profile_robust"],
             "pillars": {k: {"point": v["point"], "band": [v["lo"], v["hi"]]}
                        for k, v in p["pillars"].items()}}
            for p in profiles
        ],
        "defensible_claims": claims,
        "summary": {
            "total_claims": total_claims,
            "total_possible": total_possible,
            "pct": round(100 * total_claims / total_possible, 1),
        },
    }
    out_path = Path(__file__).parent / "pillar_analysis_report.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(f"\n  Report: {out_path}")


if __name__ == "__main__":
    main()
