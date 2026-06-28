"""
Modernization Index — Diagnostic Engine

Higher-level analysis: strategy classification, vulnerability assessment,
comparable case identification.
"""

from typing import Optional
from mi.scoring import score_country, calculate_pillar_spread, get_configuration_profile
from mi.safeguards import evaluate_all_safeguards
from mi.constants import LENS


def full_diagnostic(indicators: dict, context: dict = None) -> dict:
    """
    Run the complete MI diagnostic pipeline on a country.

    Returns scoring, configuration analysis, strategy classification,
    all safeguard evaluations, and vulnerability assessment.
    """
    score = score_country(indicators)
    safeguards = evaluate_all_safeguards(score, context or {})
    strategy = classify_strategy(score, context or {})
    vulnerability = assess_vulnerability(score, safeguards)

    return {
        "scoring": score,
        "strategy": strategy,
        "safeguards": safeguards,
        "vulnerability": vulnerability,
        "accountability_gap": accountability_gap(
            indicators.get("voice_accountability"), score.get("pillar_scores", {})),
    }


def classify_strategy(score: dict, context: dict) -> dict:
    """
    Classify which of the three governance strategies a country is running,
    based on its MI configuration.

    Strategy 1 (Porosity): High P1, institutional diffusion of pressure
    Strategy 2 (Suppression): Control through force/authority
    Strategy 3 (Complexity Control): Low internal complexity by design
    """
    pillars = score.get("pillar_scores", {})
    p1 = pillars.get("P1")
    spread = score.get("pillar_spread")

    if p1 is None:
        return {"strategy": "unknown", "confidence": "insufficient data"}

    # Heuristic classification based on P1 level and context
    indicators = []

    # Check for complexity control signals
    small_population = (context.get("population") or float("inf")) < LENS["small_population"]
    island = context.get("is_island", False)
    immigration_restrictive = context.get("immigration_policy", "") in (
        "restrictive", "very_restrictive"
    )

    # V2 Strategy 3 (refined): high institutional quality applied to a LOW-COMPLEXITY
    # environment. Geographic/demographic constraint (small pop, island, restrictive
    # immigration) can FACILITATE this but does NOT by itself confer advantage — the
    # expanded 143-country data shows small states do not systematically outperform.
    # The driver is P1, not geography. So: require high P1 + some low-complexity signal
    # (any one, as a facilitator), not the V1 conjunction.
    low_complexity = small_population or island or immigration_restrictive
    if p1 > LENS["p1_complexity_control_min"] and low_complexity:
        facilitators = [n for n, c in [("small population", small_population),
                        ("island geography", island), ("restrictive immigration", immigration_restrictive)] if c]
        return {
            "strategy": "complexity_control",
            "confidence": "high" if (p1 > 0.80 and len(facilitators) >= 2) else "moderate",
            "explanation": (
                f"High institutional quality (P1={p1:.3f}) applied to a low-complexity "
                f"environment (facilitated by: {', '.join(facilitators)}). The advantage is the "
                "institutional quality, NOT the geographic constraint per se — small/island states "
                "do not systematically outperform in the expanded data; constraint only facilitates."
            ),
            "failure_mode": "Demographic/economic stagnation",
            "examples": "Singapore, Japan (institutional quality in low-complexity settings)",
        }

    # Check for porosity signals
    has_devolution = context.get("has_devolution", False)
    has_power_sharing = context.get("has_power_sharing", False)
    has_federalism = context.get("has_federalism", False)
    democratic = context.get("is_democratic", False)

    porosity_signals = sum([
        has_devolution, has_power_sharing, has_federalism, democratic
    ])

    if p1 > LENS["p1_porosity_min"] and porosity_signals >= 2:
        return {
            "strategy": "porosity",
            "confidence": "high" if porosity_signals >= 3 else "moderate",
            "explanation": (
                f"High P1 ({p1:.3f}) with {porosity_signals} porosity mechanisms. "
                "System diffuses complexity pressure through institutional channels."
            ),
            "failure_mode": "Institutional exhaustion if complexity outgrows adaptation",
            "examples": "Switzerland, Belgium, UK, Canada",
        }

    # Check for suppression signals
    authoritarian = context.get("is_authoritarian", False)
    military_dominant = context.get("military_dominant", False)

    if authoritarian or military_dominant or (p1 < LENS["p1_strategy_authoritarian"] and not democratic):
        # Determine suppression tier
        if context.get("prior_porosity_period", False):
            tier = 3
            tier_label = "Re-suppression after porosity (WORST)"
        elif p1 > LENS["p1_porosity_min"]:
            tier = 2
            tier_label = "Institutional/legal suppression"
        else:
            tier = 1
            tier_label = "Military/authoritarian suppression"

        return {
            "strategy": "suppression",
            "tier": tier,
            "tier_label": tier_label,
            "confidence": "moderate",
            "explanation": (
                f"P1 = {p1:.3f}. System manages complexity through control "
                f"rather than diffusion. Suppression tier: {tier_label}."
            ),
            "failure_mode": (
                "Catastrophic fragmentation (re-suppression after porosity)"
                if tier == 3 else
                "Violent fragmentation when control mechanisms weaken"
                if tier == 1 else
                "De-escalation possible but pressure may recur"
            ),
        }

    # Default / ambiguous
    return {
        "strategy": "ambiguous",
        "confidence": "low",
        "explanation": (
            f"P1 = {p1:.3f}. Insufficient context signals to classify strategy. "
            "Could be transitioning between strategies or running a hybrid."
        ),
        "indicators_needed": [
            "is_democratic", "is_authoritarian", "has_federalism",
            "has_devolution", "population", "is_island"
        ],
    }


def assess_vulnerability(score: dict, safeguards: dict) -> dict:
    """
    Produce an overall vulnerability assessment based on scoring and safeguards.
    """
    pillars = score.get("pillar_scores", {})
    p1 = pillars.get("P1")
    spread = score.get("pillar_spread")
    mi = score.get("mi_score")

    flags = []
    risk_level = "low"

    # P1 assessment
    if p1 is not None:
        if p1 < LENS["p1_bottom_third"]:
            flags.append("CRITICAL: P1 in bottom third — high fragmentation/violence risk")
            risk_level = "critical"
        elif p1 < LENS["p1_median"]:
            flags.append("WARNING: P1 below median — elevated structural risk")
            risk_level = max(risk_level, "high", key=["low", "moderate", "high", "critical"].index)

    # Spread assessment
    if spread is not None:
        if spread > LENS["spread_critical"]:
            flags.append(f"CRITICAL: Pillar spread {spread:.3f} — extreme configuration imbalance")
            risk_level = max(risk_level, "high", key=["low", "moderate", "high", "critical"].index)
        elif spread > LENS["spread_warning"]:
            flags.append(f"WARNING: Pillar spread {spread:.3f} — significant imbalance")

    # Safeguard flags
    triggered_safeguards = [
        name for name, result in safeguards.items()
        if result.get("triggered", False) and name not in ("Mod4", "Mod8")
    ]
    if triggered_safeguards:
        flags.append(f"Active safeguards: {', '.join(triggered_safeguards)}")

    # Specific high-risk combinations
    if (safeguards.get("B", {}).get("triggered") and
            safeguards.get("E", {}).get("triggered")):
        flags.append("CRITICAL COMBINATION: Low P1 + resource dependence — "
                      "catastrophic outcome pattern (Libya/South Sudan profile)")
        risk_level = "critical"

    if safeguards.get("G", {}).get("tier") == "RE-SUPPRESSION AFTER POROSITY (WORST PATH)":
        flags.append("CRITICAL: Re-suppression after porosity — worst documented path")
        risk_level = "critical"

    return {
        "risk_level": risk_level,
        "flags": flags,
        "structural_vulnerability": structural_vulnerability(pillars),
        "below_floor": below_floor_diagnostic(pillars, mi),
        "summary": (
            f"Risk level: {risk_level.upper()}. "
            f"P1 = {f'{p1:.3f}' if p1 is not None else 'N/A'}, "
            f"spread = {f'{spread:.3f}' if spread is not None else 'N/A'}, "
            f"{len(triggered_safeguards)} safeguards active."
        ),
    }


def accountability_gap(voice_accountability, pillars: dict) -> Optional[dict]:
    """
    V3.2 Accountability Gap (HYPOTHESIS — informational, NOT a verdict).

    P1 deliberately excludes Voice & Accountability (VA); among high-capacity states VA is the only
    axis separating democracies from rich authoritarians. When VA sits far below income (P4) — and
    capacity (P1) — the state delivers economically with no accountability channel ("capacity without
    consent"), a hypothesized BRITTLE/sudden failure mode (succession/legitimacy shock), orthogonal to
    the durability gap. NO crisis validation yet (Saudi/China have not broken) — surfaced as a signal
    to watch, never a verdict. `voice_accountability` accepted as 0-100 (WGI .SC) or 0-1; pillars 0-1.
    """
    va = voice_accountability
    p1 = pillars.get("P1"); p4 = pillars.get("P4")
    if va is None or p1 is None or p4 is None:
        return None
    if va > 1.5:           # accept 0-100 input
        va = va / 100.0
    va_p4 = va - p4; va_p1 = va - p1
    cap = LENS["va_legitimacy_cap_p4"]; lag = LENS["va_accountability_lag_p4"]
    if va_p4 <= cap:
        status = "legitimacy_capped"
        reading = ("CAPACITY WITHOUT CONSENT — accountability far below income/capacity; hypothesized "
                   "brittle failure mode (succession/legitimacy shock). HYPOTHESIS, not a verdict.")
    elif va_p4 <= lag:
        status = "accountability_lag"
        reading = "accountability trails income/capacity — partial; watch."
    else:
        status = "balanced"
        reading = "accountability roughly tracks capacity and income."
    return {"voice_accountability": round(va, 3),
            "va_minus_p4": round(va_p4, 3), "va_minus_p1": round(va_p1, 3),
            "status": status, "reading": reading,
            "caveat": "HYPOTHESIS (V3.2) — informational; orthogonal to the durability gap; no crisis validation yet."}


def structural_vulnerability(pillars: dict) -> Optional[dict]:
    """
    V3.1 structural crisis-vulnerability gate (the "durability gap"): P4 - P1 > threshold means
    economy/income has outrun institutions ("granted/fragile") -> structurally crisis-prone. This
    LEVEL discriminator separated real crises from absorbers on the N=21 signature set at 83% sens /
    100% spec / 100% PPV — far better than the (failed) acute pre-turn DECLINE signature, because a
    level is forward-available while a decline emerges only at/after the event. Returns None if P1/P4
    unavailable. NOT a dated forecast (Mod8) — a structural risk flag; idiosyncratic acute events
    (Chile, S.Korea) have no structural warning and are out of scope.
    """
    p1 = pillars.get("P1"); p4 = pillars.get("P4")
    if p1 is None or p4 is None:
        return None
    gap = p4 - p1
    flag_floor = LENS["structural_vuln_flag_floor"]
    clear_ceiling = LENS["structural_vuln_clear_ceiling"]
    if gap >= flag_floor:
        status, reading = "flagged", ("STRUCTURALLY VULNERABLE — income/economy has outrun institutions "
                                      "(granted/fragile); elevated crisis risk under shock.")
    elif gap <= clear_ceiling:
        status, reading = "clear", ("institutions roughly keep pace with income — not structurally "
                                    "crisis-flagged (absorber-class on this measure).")
    else:
        status, reading = "borderline", ("INDETERMINATE — gap sits in the empty band between the validated "
                                         "absorber ceiling and crisis floor; above every confirmed absorber "
                                         "but below the crisis floor. Elevated watch, not a verdict.")
    return {
        "p4_minus_p1_gap": round(gap, 3),
        "status": status,
        "flagged": gap > LENS["structural_vulnerability_gap"],  # back-compat boolean
        "reading": reading,
    }


def below_floor_diagnostic(pillars: dict, mi) -> Optional[dict]:
    """
    V2 below-floor configuration finding: most below-floor countries are PARTIAL failures
    (resource/income strong, institutions+economy catastrophic) — not uniformly poor. This
    changes the prescription from "very bad shape" to "money but no institutions: target P1/P2,
    not P4." Returns None for countries above the below-floor MI cutoff.
    """
    if mi is None or mi > LENS["below_floor_mi"]:
        return None
    p1 = pillars.get("P1"); p2 = pillars.get("P2"); p4 = pillars.get("P4")
    strong_p4 = p4 is not None and p4 >= LENS["partial_failure_p4_min"]
    weak_inst = (p1 is not None and p1 <= LENS["partial_failure_p1p2_max"]) and \
                (p2 is None or p2 <= LENS["partial_failure_p1p2_max"])
    if strong_p4 and weak_inst:
        return {
            "configuration": "partial_failure",
            "reading": "Has money, not institutions: strong P4 (resource/income) atop catastrophic P1/P2.",
            "prescription": "Target P1/P2 (institutions, knowledge economy) — NOT P4. Money is not the binding constraint.",
        }
    return {
        "configuration": "uniformly_poor",
        "reading": "Weak across pillars including P4 — no resource/income cushion.",
        "prescription": "Broad-based capacity building; no single binding constraint to target.",
    }


def generate_predictions(score: dict, safeguards: dict, comparison_scores: dict = None) -> dict:
    """
    Generate the standard prediction set (a-h) from a scored country profile.

    For cases involving comparison between entities, provide comparison_scores
    as a dict of {entity_name: score_dict}.
    """
    pillars = score.get("pillar_scores", {})
    predictions = {}

    # (a) Best trajectory prediction
    if comparison_scores:
        rankings = []
        for name, comp_score in comparison_scores.items():
            comp_p1 = comp_score.get("pillar_scores", {}).get("P1")
            if comp_p1 is not None:
                rankings.append((name, comp_p1))
        rankings.sort(key=lambda x: x[1], reverse=True)
        predictions["a_trajectory_ranking"] = {
            "prediction": f"Predicted ranking: {' > '.join(n for n, _ in rankings)}",
            "basis": "P1 ordinality (highest P1 = best trajectory)",
            "rankings": rankings,
            "mod4_check": "Apply Mod4 to adjacent pairs — abstain if gap < margin",
        }

    # (b) Violence prediction
    p1 = pillars.get("P1")
    if p1 is not None:
        violence_risk = "HIGH" if p1 < LENS["p1_bottom_third"] else "MODERATE" if p1 < LENS["p1_median"] else "LOW"
        predictions["b_violence"] = {
            "prediction": f"Violence RISK: {violence_risk} (P1 = {p1:.3f})",
            "note": "Mod8 applies: this predicts RISK, not AGENCY",
            "basis": "Low P1 → violent outcomes confirmed across all tested cases",
        }

    # (c) Convergence/divergence
    spread = score.get("pillar_spread")
    if comparison_scores and len(comparison_scores) >= 2:
        p1_values = [p1 for s in comparison_scores.values()
                     if (p1 := s.get("pillar_scores", {}).get("P1")) is not None]
        p1_range = max(p1_values) - min(p1_values) if len(p1_values) >= 2 else 0
        predictions["c_convergence"] = {
            "prediction": "DIVERGENCE" if p1_range > 0.15 else "CONVERGENCE",
            "basis": f"P1 range across entities: {p1_range:.3f}",
        }

    # (d) Primary failure dimension
    config = score.get("configuration", [])
    if config:
        weakest = config[-1] if config else None
        predictions["d_failure_dimension"] = {
            "prediction": f"Primary vulnerability: {weakest[0]} ({weakest[1]:.3f})" if weakest else "unknown",
            "note": "Post-hoc coding risk — this prediction is the most exposed to confirmation bias",
        }

    return predictions
