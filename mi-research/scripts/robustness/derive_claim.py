#!/usr/bin/env python3
"""
Priority 1 — Reproducibility rebuild (see docs/ROBUSTNESS_PREREGISTRATION.md).

Builds a LIVE, recomputable `derive_claim(case)` that produces each case's claim
values PURELY from the engine's output (mi.scoring / mi.safeguards / mi.diagnostics)
and the WRITTEN spec rules — never from the static `verification{}` codings baked
into the case JSON.

THE CRITICAL DISCIPLINE (spec-driven, not label-driven): this module NEVER reads
`case["verification"][*]["result"]` (or any coded VALUE/verdict). It only uses the
engine output + the frozen written rules. It emits the "generate" artifact; the
"grade" half (comparing to the frozen codings, computing agreement) is run
SEPARATELY, afterward, by the pre-registration owner. This module does NOT grade.

Claim types and their derivation rules (file:section citations):

  ORDINALITY / comparative-trajectory cases (case01-51) — verification keys a-h:
    a_trajectory      P1-ordinality ranking. Rank entities by pre-event P1 desc.
                      mi/diagnostics.py:393-405 generate_predictions §(a). Mod4 gate
                      (mi/safeguards.py:480-530 evaluate_mod4) applied to each
                      adjacent pair: p1_comparison_gap = P1_hi - P1_lo, p1_min_level
                      = min(pair) — derived mechanically from entity P1 as the prereg
                      Plan-3 mechanism paragraph authorizes.
                      For single-entity cases (n=1, no ranking possible) the trajectory
                      is derived from the prereg "Shared mechanical rule set" (bottom
                      of ROBUSTNESS_PREREGISTRATION.md): Safeguard-J gap (P4-P1) +
                      P1 level. [JUDGMENT CALL — see JUDGMENT_CALLS #3]
    b_violence        Violence RISK from P1. HIGH if P1<p1_bottom_third(0.33),
                      MODERATE if P1<p1_median(0.5), else LOW.
                      mi/diagnostics.py:408-415 generate_predictions §(b) + Mod8.
    c_convergence     DIVERGENCE if cross-entity P1 range > 0.15 else CONVERGENCE.
                      mi/diagnostics.py:419-426 generate_predictions §(c).
                      N/A for single-entity cases. [JUDGMENT CALL #4]
    d_failure_dimension  Weakest pillar = configuration[-1] of the reference entity.
                      mi/diagnostics.py:429-435 generate_predictions §(d).
    e_fragment_count  Safeguard B (Capacity Gate): triggered if P1<0.33 AND
                      n_successor_states<=4. mi/safeguards.py:164-193.
    f_reversal_risk   Safeguard C (Reversal Risk): triggered if is_democratic_transition;
                      severity from rents/growth/youth. mi/safeguards.py:196-254.
    g_suppression     Safeguard G (Suppression vs Prevention) tier from
                      fragmentation_mechanism + prior_porosity. mi/safeguards.py:381-440.
    h_turbulence      Safeguard F (Sub-State Turbulence): antisystem_vote / exec_collapses /
                      regional_divergence. mi/safeguards.py:339-378.

  DURABILITY-GATE cases (sig01-19) — verification key j_durability_gate:
    j_durability_gate Safeguard J (durability gate). Score at predictor_year, then
                      status = flagged (gap>=0.28) / clear (gap<=0.20) / borderline.
                      mi/safeguards.py:64-135 evaluate_safeguard_j;
                      mi/diagnostics.py:322-353 structural_vulnerability.

  RULE-VALIDATION cases (rv01-14) — verification key rule_test:
    rule_test         Rule A (Convergence Qualifier) + Rule B (Accountability Gap) + drift.
                      Score at predictor_year AND prior_year; pass prior {P1,P4} as
                      context.prior_pillars so Safeguard J emits its convergence
                      qualifier (widening/closing/static). Accountability status from
                      mi/diagnostics.py:287-319 accountability_gap (V3.2).
                      J: mi/safeguards.py:64-135 (incl. convergence qualifier 114-134).

Spec sources: MASTER_REFERENCE_ARCHITECTURE.md §4 (line 36 headline: "100% directional
accuracy with P1 ordinality across all 51 ordinality cases (213C/77P/0F)"; line 39
directional/relative-ranking framing), RESEARCH.md, mi/safeguards.py, mi/diagnostics.py,
mi/constants.LENS.

Ancient corpus (data/case_studies/ancient/ancient_cases.json, 25 Track-3 cases) is
DEFERRED — see ANCIENT_STATUS below.

    python scripts/robustness/derive_claim.py
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # mi-research/
sys.path.insert(0, str(ROOT))

from mi import datasource                              # noqa: E402
from mi.scoring import score_country                   # noqa: E402
from mi.safeguards import evaluate_all_safeguards, evaluate_mod4  # noqa: E402
from mi.diagnostics import (                           # noqa: E402
    generate_predictions, assess_vulnerability, accountability_gap)
from mi.constants import LENS                          # noqa: E402

PREREG = ROOT / "docs" / "ROBUSTNESS_PREREGISTRATION.md"
COMPLETED = ROOT / "data" / "case_studies" / "completed"
ANCIENT = ROOT / "data" / "case_studies" / "ancient" / "ancient_cases.json"
OUT = ROOT / "data" / "robustness" / "derived_claims.json"

# Frozen "Shared mechanical rule set" thresholds (bottom of ROBUSTNESS_PREREGISTRATION.md),
# reused only for the single-entity trajectory fallback (judgment call #3).
J_FLAG_FLOOR = LENS["structural_vuln_flag_floor"]      # 0.28
J_CLEAR_CEILING = LENS["structural_vuln_clear_ceiling"]  # 0.20
P1_DECLINE = 0.30
P1_IMPROVE = 0.50

JUDGMENT_CALLS = [
    "1. REFERENCE ENTITY = first-listed entity (dict insertion order). b_violence and "
    "d_failure_dimension are computed on it, matching run_retrodiction.run_phase2 which "
    "passes list(phase1_results.values())[0] as the reference score to generate_predictions. "
    "The corpus 'focus' coding sometimes names a different entity (e.g. case01 b_violence "
    "focus=Russia, the 2nd entity); we did NOT copy that — we derive per the engine's own "
    "first-entity rule. A per-entity map is also emitted so the grader can re-key if desired.",
    "2. MOD4 CONTEXT: p1_comparison_gap and p1_min_level are not in the case JSON; derived "
    "mechanically as (P1_hi - P1_lo) and min(pair) for each adjacent ranked pair. Explicitly "
    "authorized by the prereg Plan-3 mechanism paragraph ('derived mechanically from the case "
    "entities' P1 and documented').",
    "3. SINGLE-ENTITY a_trajectory: generate_predictions produces NO ranking for n=1 (needs "
    ">=2 comparison_scores). The corpus still codes an a_trajectory for single-entity cases "
    "(a directional improve/decline call, not a ranking). We derive it from the prereg 'Shared "
    "mechanical rule set': J-gap flagged->'stress/decline-lean', clear->'sustain_or_improve', "
    "else 'monitor'; annotated with the P1-level read. This rule set is labeled in the prereg "
    "for P0/P2 but is the only frozen spec-level mechanical trajectory rule; flag for review.",
    "4. SINGLE-ENTITY c_convergence: generate_predictions §(c) is undefined for one entity "
    "(no cross-entity P1 range). Emitted as 'N/A_single_entity'.",
    "5. e/f/g/h CASE-LEVEL AGGREGATION across entities: the safeguard is per-entity; the "
    "case-level claim is set triggered if ANY resolved entity triggers it (for g_suppression, "
    "the first non-null tier is taken). Per-entity detail is retained under each claim.",
    "6. YEAR PARSING: malformed multi-year pre_year strings (e.g. Yemen '1990/1996') fall back "
    "to the LAST 4-digit token ('1996'). Documented, mechanical.",
    "7. UNRESOLVABLE ENTITIES (sub-national / unrecognized / pre-WGI: Taiwan, Aceh, Quebec, "
    "Bougainville, Somaliland, East-Timor-1998) are DROPPED from the ranking and recorded under "
    "unresolved_entities. A comparative case with <2 resolvable entities degrades to the "
    "single-entity derivation; with 0 it is marked underivable.",
    "8. e_fragment_count is derived ONLY as the Safeguard-B mechanical status. The broader "
    "qualitative 'engineered vs organic fragmentation' judgment in the corpus is NOT "
    "mechanically derivable from the engine and is out of scope for the mechanical claim.",
]

ANCIENT_STATUS = (
    "DEFERRED. The 25 ancient cases (data/case_studies/ancient/ancient_cases.json) are Track-3 "
    "proxy records with a DIFFERENT schema: (a) they carry NO `verification{}` block at all, so "
    "there is no claim coding to recompute; (b) their pillars are hand-coded proxy sub-scores "
    "(e.g. P1.indicators.P1a_admin_depth {value, source, confidence}) with peak/pre_stress "
    "time-points, NOT the WGI/CPI/GII/GDP raw-indicator dict that score_country consumes; there "
    "is no country_ref/year the Data API can resolve. Re-scoring them through the modern engine "
    "would require a separate Track-3 proxy-scoring path (firewalled per mi-research/CLAUDE.md). "
    "Scope is therefore the 84 modern cases."
)


def _year(y):
    """Parse a pre_year/predictor_year field, falling back to the last 4-digit token."""
    if y is None:
        return None
    toks = re.findall(r"\d{4}", str(y))
    return toks[-1] if toks else None


def _score_ref(country_ref, year):
    """Resolve indicators via the Data API and score. Returns (score|None, reason|None)."""
    yr = _year(year)
    if not country_ref or yr is None:
        return None, f"no country_ref/year (ref={country_ref!r}, year={year!r})"
    ind = datasource.get_indicators(country_ref, yr)
    if ind is None:
        return None, f"Data API has no record for ({country_ref}, {yr})"
    sc = score_country(ind)
    if sc["pillar_scores"].get("P1") is None:
        return None, f"P1 unavailable for ({country_ref}, {yr})"
    sc["_va"] = ind.get("voice_accountability")
    return sc, None


def _violence_band(p1):
    return ("HIGH" if p1 < LENS["p1_bottom_third"]
            else "MODERATE" if p1 < LENS["p1_median"] else "LOW")


def _single_trajectory(p1, p4):
    gap = p4 - p1
    if gap >= J_FLAG_FLOOR:
        traj = "stress_decline_lean"
    elif gap <= J_CLEAR_CEILING:
        traj = "sustain_or_improve"
    else:
        traj = "monitor"
    level = ("decline_risk" if p1 < P1_DECLINE
             else "improvement_capacity" if p1 > P1_IMPROVE else "hold")
    return {"trajectory": traj, "level": level, "gap": round(gap, 3),
            "basis": "prereg Shared mechanical rule set (Safeguard-J gap + P1 level)"}


# ----------------------------------------------------------------------------- #
# Schema derivations
# ----------------------------------------------------------------------------- #

def _derive_ordinality(case, case_id):
    ents = case["pre_event"]["entities"]
    scored, unresolved = [], []
    contexts = {}
    for name, ed in ents.items():
        sc, reason = _score_ref(ed.get("country_ref"), ed.get("pre_year"))
        ctx = ed.get("context", {}) or {}
        if sc is None:
            unresolved.append({"entity": name, "country_ref": ed.get("country_ref"),
                               "pre_year": ed.get("pre_year"), "reason": reason})
        else:
            scored.append((name, sc))
            contexts[name] = ctx

    if not scored:
        return {"case_id": case_id, "schema": "comparative", "derivable": False,
                "underivable_reason": "no resolvable entities",
                "unresolved_entities": unresolved, "claims": {}, "summary": None}

    # per-entity safeguards (context-driven)
    safeguards = {name: evaluate_all_safeguards(sc, contexts.get(name, {}))
                  for name, sc in scored}
    ref_name, ref_score = scored[0]
    ref_safe = safeguards[ref_name]
    comparison = {name: sc for name, sc in scored}

    claims = {}

    if len(scored) >= 2:
        gp = generate_predictions(ref_score, ref_safe, comparison)
        # (a) ranking + Mod4 per adjacent pair
        rankings = gp["a_trajectory_ranking"]["rankings"]  # [(name, p1), ...] sorted desc
        pairs = []
        any_abstain = False
        for i in range(len(rankings) - 1):
            (hn, hp1), (ln, lp1) = rankings[i], rankings[i + 1]
            gap = hp1 - lp1
            m = evaluate_mod4({}, {"p1_comparison_gap": gap, "p1_min_level": min(hp1, lp1)})
            any_abstain = any_abstain or m["triggered"]
            pairs.append({"higher": hn, "lower": ln, "gap": round(gap, 3),
                          "abstain": m["triggered"], "reason": m.get("explanation")})
        claims["a_trajectory"] = {
            "type": "p1_ordinality_ranking",
            "ranking": [n for n, _ in rankings],
            "p1_values": {n: round(p, 4) for n, p in rankings},
            "adjacent_pairs": pairs,
            "any_pair_abstains": any_abstain,
        }
        # (c) convergence
        claims["c_convergence"] = {"type": "convergence",
                                   "value": gp["c_convergence"]["prediction"],
                                   "basis": gp["c_convergence"]["basis"]}
    else:
        # degraded to single resolvable entity
        p1 = ref_score["pillar_scores"]["P1"]; p4 = ref_score["pillar_scores"].get("P4")
        claims["a_trajectory"] = {"type": "single_entity_trajectory",
                                  **(_single_trajectory(p1, p4) if p4 is not None
                                     else {"trajectory": "undetermined", "reason": "P4 unavailable"})}
        claims["c_convergence"] = {"type": "convergence", "value": "N/A_single_entity"}

    # (b) violence — reference entity, plus per-entity map
    ref_p1 = ref_score["pillar_scores"]["P1"]
    claims["b_violence"] = {
        "type": "violence_risk",
        "reference_entity": ref_name,
        "risk": _violence_band(ref_p1),
        "reference_p1": round(ref_p1, 4),
        "per_entity": {n: _violence_band(sc["pillar_scores"]["P1"]) for n, sc in scored},
    }
    # (d) failure dimension — reference entity weakest pillar
    ref_cfg = ref_score.get("configuration", [])
    weakest = ref_cfg[-1] if ref_cfg else None
    claims["d_failure_dimension"] = {
        "type": "primary_failure_pillar",
        "reference_entity": ref_name,
        "weakest_pillar": weakest[0] if weakest else None,
        "score": round(weakest[1], 4) if weakest else None,
    }
    # (e) Safeguard B  (f) Safeguard C  (g) Safeguard G  (h) Safeguard F
    def _agg(letter):
        per = {n: safeguards[n].get(letter, {}) for n, _ in scored}
        return per

    perB = _agg("B")
    claims["e_fragment_count"] = {
        "type": "safeguard_B_capacity_gate",
        "any_triggered": any(v.get("triggered") for v in perB.values()),
        "per_entity": {n: {"triggered": v.get("triggered"),
                           "n_successor_states": contexts.get(n, {}).get("n_successor_states")}
                       for n, v in perB.items()},
    }
    perC = _agg("C")
    claims["f_reversal_risk"] = {
        "type": "safeguard_C_reversal_risk",
        "any_triggered": any(v.get("triggered") for v in perC.values()),
        "per_entity": {n: {"triggered": v.get("triggered"), "severity": v.get("severity")}
                       for n, v in perC.items()},
    }
    perG = _agg("G")
    g_tier = next((v.get("tier") for v in perG.values() if v.get("triggered")), None)
    claims["g_suppression"] = {
        "type": "safeguard_G_suppression_tier",
        "tier": g_tier,
        "per_entity": {n: {"triggered": v.get("triggered"), "tier": v.get("tier")}
                       for n, v in perG.items()},
    }
    perF = _agg("F")
    claims["h_turbulence"] = {
        "type": "safeguard_F_substate_turbulence",
        "any_triggered": any(v.get("triggered") for v in perF.values()),
        "per_entity": {n: {"triggered": v.get("triggered"), "triggers": v.get("triggers")}
                       for n, v in perF.items()},
    }

    vuln = assess_vulnerability(ref_score, ref_safe)
    if len(scored) >= 2:
        directional = "ranking: " + " > ".join(claims["a_trajectory"]["ranking"])
        abstention = claims["a_trajectory"]["any_pair_abstains"]
    else:
        directional = claims["a_trajectory"].get("trajectory")
        abstention = False
    summary = {
        "directional_call": directional,
        "tier": (ref_score.get("tier") or {}).get("tier"),
        "abstention": abstention,
        "risk_level": vuln.get("risk_level"),
        "reference_entity": ref_name,
    }
    return {"case_id": case_id, "schema": "comparative" if len(scored) >= 2 else "comparative_degraded_single",
            "derivable": True, "underivable_reason": None,
            "resolved_entities": [n for n, _ in scored],
            "unresolved_entities": unresolved, "claims": claims, "summary": summary}


def _derive_durability_gate(case, case_id):
    sc, reason = _score_ref(case.get("country_ref"), case.get("predictor_year"))
    if sc is None:
        return {"case_id": case_id, "schema": "durability_gate", "derivable": False,
                "underivable_reason": reason, "claims": {}, "summary": None}
    safe = evaluate_all_safeguards(sc, {})
    j = safe["J"]
    status = j.get("status")
    call = {"flagged": "crisis_vulnerable", "clear": "absorber",
            "borderline": "watch"}.get(status, "undetermined")
    claims = {"j_durability_gate": {
        "type": "safeguard_J_durability_gate",
        "status": status, "gap": j.get("gap"),
        "flag_floor": j.get("flag_floor"), "clear_ceiling": j.get("clear_ceiling"),
        "directional_call": call,
        "P1": round(sc["pillar_scores"]["P1"], 4),
        "P4": round(sc["pillar_scores"]["P4"], 4),
    }}
    vuln = assess_vulnerability(sc, safe)
    summary = {"directional_call": call, "tier": (sc.get("tier") or {}).get("tier"),
               "abstention": status == "borderline", "risk_level": vuln.get("risk_level")}
    return {"case_id": case_id, "schema": "durability_gate", "derivable": True,
            "underivable_reason": None, "claims": claims, "summary": summary}


def _derive_rule_validation(case, case_id):
    sc, reason = _score_ref(case.get("country_ref"), case.get("predictor_year"))
    if sc is None:
        return {"case_id": case_id, "schema": "rule_validation", "derivable": False,
                "underivable_reason": reason, "claims": {}, "summary": None}
    ctx = {}
    prior_year = case.get("prior_year")
    prior_note = None
    if prior_year:
        psc, preason = _score_ref(case.get("country_ref"), prior_year)
        if psc is not None:
            ctx["prior_pillars"] = {"P1": psc["pillar_scores"]["P1"],
                                    "P4": psc["pillar_scores"]["P4"]}
        else:
            prior_note = f"prior_year {prior_year} unresolvable ({preason}); convergence qualifier omitted"
    safe = evaluate_all_safeguards(sc, ctx)
    j = safe["J"]
    conv = j.get("convergence", {})
    ag = accountability_gap(sc.get("_va"), sc["pillar_scores"])
    status = j.get("status")
    call = {"flagged": "crisis_vulnerable", "clear": "absorber",
            "borderline": "watch"}.get(status, "undetermined")
    claims = {"rule_test": {
        "type": "rules_A_convergence_B_accountability_drift",
        "J_status": status, "gap": j.get("gap"),
        "convergence_direction": conv.get("direction"),
        "convergence_refined": conv.get("refined"),
        "accountability_status": ag.get("status") if ag else None,
        "va_minus_p4": ag.get("va_minus_p4") if ag else None,
        "directional_call": call,
        "prior_note": prior_note,
    }}
    vuln = assess_vulnerability(sc, safe)
    summary = {"directional_call": call, "tier": (sc.get("tier") or {}).get("tier"),
               "abstention": status == "borderline", "risk_level": vuln.get("risk_level")}
    return {"case_id": case_id, "schema": "rule_validation", "derivable": True,
            "underivable_reason": None, "claims": claims, "summary": summary}


def derive_claim(case: dict) -> dict:
    """Derive claim values for one case purely from engine output + spec rules.

    Dispatches on the case schema. NEVER reads case['verification'][*]['result'].
    """
    case_id = (case.get("metadata", {}).get("case_id")
               or case.get("metadata", {}).get("case_name")
               or case.get("name") or "unknown")
    st = case.get("metadata", {}).get("stress_type")
    if st == "durability_gate_test":
        return _derive_durability_gate(case, case_id)
    if st == "rule_validation":
        return _derive_rule_validation(case, case_id)
    if "pre_event" in case:
        return _derive_ordinality(case, case_id)
    return {"case_id": case_id, "schema": "unknown", "derivable": False,
            "underivable_reason": f"unrecognized schema (stress_type={st})",
            "claims": {}, "summary": None}


def main():
    from collections import Counter
    results = []
    for f in sorted(COMPLETED.glob("*.json")):
        case = json.loads(f.read_text())
        r = derive_claim(case)
        r["source_file"] = f.name
        results.append(r)

    # coverage: how many cases each claim type applies to (derivable cases only)
    claim_cov = Counter()
    schema_cov = Counter()
    derivable = 0
    for r in results:
        schema_cov[r["schema"]] += 1
        if r["derivable"]:
            derivable += 1
            for k in r["claims"]:
                claim_cov[k] += 1
    underivable = [{"file": r["source_file"], "reason": r["underivable_reason"]}
                   for r in results if not r["derivable"]]

    prereg_hash = hashlib.sha256(PREREG.read_bytes()).hexdigest()[:16]
    payload = {
        "workstream": "P1_reproducibility_rebuild__GENERATE_HALF_ONLY",
        "discipline_note": ("Spec-driven derivation. Derived ONLY from engine output + written "
                            "spec rules; case verification{} VALUES were never read. This is the "
                            "generate artifact; grading (agreement vs frozen codings) is run "
                            "separately afterward and is NOT performed here."),
        "prereg_sha256_16": prereg_hash,
        "engine_config": {
            "p1_bottom_third": LENS["p1_bottom_third"], "p1_median": LENS["p1_median"],
            "mod4_margin": LENS["mod4_margin"],
            "v3_consolidation_threshold": LENS["v3_consolidation_threshold"],
            "v3_high_end_margin": LENS["v3_high_end_margin"],
            "j_flag_floor": J_FLAG_FLOOR, "j_clear_ceiling": J_CLEAR_CEILING,
        },
        "scope": "84 modern cases (51 ordinality + 19 durability-gate + 14 rule-validation)",
        "ancient_status": ANCIENT_STATUS,
        "judgment_calls": JUDGMENT_CALLS,
        "n_cases": len(results),
        "n_derivable": derivable,
        "n_underivable": len(underivable),
        "underivable": underivable,
        "schema_coverage": dict(schema_cov),
        "claim_type_coverage": dict(claim_cov),
        "cases": results,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))

    print(f"Derived claims for {derivable}/{len(results)} modern cases "
          f"({len(underivable)} underivable).")
    print(f"Schema coverage: {dict(schema_cov)}")
    print(f"Claim-type coverage: {dict(claim_cov)}")
    if underivable:
        print("Underivable:")
        for u in underivable:
            print(f"  {u['file']}: {u['reason']}")
    print(f"prereg hash: {prereg_hash}")
    print(f"-> {OUT.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
