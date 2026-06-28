"""
Modernization Index — Safeguard System

All seven safeguards (A-G) plus essential modifications (Mod4, Mod8, Safeguard I).
Each safeguard has: trigger conditions, modification logic, derivation history.
"""

from typing import Optional
from mi.constants import SAFEGUARD_THRESHOLDS, LENS


def evaluate_all_safeguards(
    country_score: dict,
    context: dict = None,
) -> dict:
    """
    Evaluate all safeguards for a scored country.

    Args:
        country_score: output from scoring.score_country()
        context: additional context dict with keys like:
            - under_external_admin (bool)
            - admin_details (str)
            - neighbor_threat_level (str: "none", "moderate", "high")
            - neighbor_details (str)
            - resource_rents_pct_revenue (float)
            - is_democratic_transition (bool)
            - youth_unemployment (float)
            - growth_trajectory (str: "stagnant", "growing", "declining")
            - regional_antisystem_vote (float)
            - executive_collapses (int)
            - regional_gdp_divergence (float)
            - fragmentation_mechanism (str)
            - prior_porosity_period (bool)
            - external_backstop (bool)
            - backstop_details (str)
            - n_successor_states (int)

    Returns:
        Dict of safeguard evaluations, each with triggered (bool),
        explanation (str), and modification (str or None).
    """
    if context is None:
        context = {}

    pillars = country_score.get("pillar_scores", {})
    results = {}

    results["A"] = evaluate_safeguard_a(pillars, context)
    results["B"] = evaluate_safeguard_b(pillars, context)
    results["C"] = evaluate_safeguard_c(pillars, context)
    results["D"] = evaluate_safeguard_d(pillars, context)
    results["E"] = evaluate_safeguard_e(pillars, context)
    results["F"] = evaluate_safeguard_f(pillars, context)
    results["G"] = evaluate_safeguard_g(pillars, context)
    results["I"] = evaluate_safeguard_i(pillars, context)
    results["J"] = evaluate_safeguard_j(pillars, context)
    results["Mod4"] = evaluate_mod4(pillars, context)
    results["Mod8"] = evaluate_mod8(pillars, context)

    return results


def evaluate_safeguard_j(pillars: dict, context: dict) -> dict:
    """
    Safeguard J — Durability Gate (the P4-P1 "durability gap").

    INDEPENDENTLY DERIVED on the N=21 acute-signature test set (2026-06-28): the four-component
    pre-turn DECLINE signature failed blind (14-25% sens, 40% PPV), but a single LEVEL variable —
    the gap between economy/income (P4) and institutions (P1) — separated real crises from absorbers
    at 83% sensitivity / 100% specificity / 100% PPV. When income has outrun institutions
    (P4 - P1 > threshold), the state is "granted/fragile" — structurally crisis-prone under shock.
    Unifies with the durability ratio (mi/durability.py). Directional/structural, NOT a timing or
    idiosyncratic-event forecast (Chile, S.Korea — acute elite gambles — are out of scope by design).

    Derivation: docs/architectural_decisions/v3_1_durability_gate.md.
    """
    p1 = pillars.get("P1"); p4 = pillars.get("P4")
    if p1 is None or p4 is None:
        return {"name": "Durability Gate (P4-P1 gap)", "triggered": False,
                "explanation": "P1 or P4 unavailable — gate not evaluable.", "modification": None,
                "derivation": "N=21 signature set; = durability ratio re-derived as a forward gate."}
    gap = p4 - p1
    threshold = LENS["structural_vulnerability_gap"]
    triggered = gap > threshold
    return {
        "name": "Durability Gate (P4-P1 gap)",
        "triggered": triggered,
        "gap": round(gap, 3),
        "threshold": threshold,
        "explanation": (
            f"P4-P1 gap = {gap:.3f} > {threshold}: income/economy has outrun institutions "
            "(granted/fragile) — STRUCTURALLY crisis-vulnerable under shock."
            if triggered else
            f"P4-P1 gap = {gap:.3f} <= {threshold}: institutions roughly keep pace with income — "
            "not structurally flagged (absorber-class on this measure)."
        ),
        "modification": (
            "Flag elevated structural crisis-vulnerability; pair with stability (P5) and shock "
            "exposure. Risk, not timing (Mod8)."
            if triggered else None
        ),
        "derivation": "N=21 signature set (83% sens/100% spec/100% PPV); = durability ratio re-derived.",
    }


def evaluate_safeguard_a(pillars: dict, context: dict) -> dict:
    """
    Safeguard A — External Administration Flag

    Derived from: Bosnia 1996 (Round 1 falsification)
    Validated by: Kosovo (UNMIK/EULEX), East Timor (UNTAET)
    """
    triggered = context.get("under_external_admin", False)
    return {
        "name": "External Administration",
        "triggered": triggered,
        "explanation": (
            f"State under external administration: {context.get('admin_details', 'unknown')}. "
            "WGI scores may reflect administrator competence, not indigenous capacity. "
            "Assess indigenous capacity qualitatively."
            if triggered else "No external administration detected."
        ),
        "modification": (
            "Discount raw WGI P1 scores. Use qualitative assessment of indigenous "
            "institutional capacity for predictions."
            if triggered else None
        ),
        "derivation": "Bosnia 1996 — Dayton OHR inflated P1 above Croatia/Serbia",
    }


def evaluate_safeguard_b(pillars: dict, context: dict) -> dict:
    """
    Safeguard B — Minimum Capacity Gate on Fragment Count

    Derived from: Sudan/South Sudan (Round 1 falsification)
    Validated by: Ethiopia/Eritrea (Round 2), Nigeria/Biafra (Round 4)
    """
    p1 = pillars.get("P1")
    n_successors = context.get("n_successor_states")
    low_p1 = p1 is not None and p1 < LENS["p1_bottom_third"]  # Bottom third (ordinal)

    triggered = low_p1 and n_successors is not None and n_successors <= 4
    return {
        "name": "Capacity Gate",
        "triggered": triggered,
        "explanation": (
            f"P1 = {p1:.3f} (bottom third) with {n_successors} successor states. "
            "Low fragment count does NOT indicate manageability when P1 is this low. "
            "Code as catastrophic risk despite low count."
            if triggered else
            f"P1 = {f'{p1:.3f}' if p1 else 'N/A'}, "
            f"successors = {n_successors or 'N/A'}. Gate not triggered."
        ),
        "modification": (
            "Override 'natural fragmentation' coding. Predict catastrophic outcome "
            "regardless of fragment count."
            if triggered else None
        ),
        "derivation": "Sudan/South Sudan — 2 states, worst outcome in sample",
    }


def evaluate_safeguard_c(pillars: dict, context: dict) -> dict:
    """
    Safeguard C — Reversal Risk Flag (graded penalty)

    Derived from: Tunisia (Round 1 — missed 2021 reversal)
    Validated by: Bangladesh (2024), Serbia, South Africa, India
    """
    is_transition = context.get("is_democratic_transition", False)
    if not is_transition:
        return {
            "name": "Reversal Risk",
            "triggered": False,
            "explanation": "Not a democratic transition case.",
            "modification": None,
            "derivation": "Tunisia 2021 reversal",
        }

    # Assess severity (treat explicit None context values as absent/0)
    thresholds = SAFEGUARD_THRESHOLDS["C_reversal_risk"]
    resource_rents = context.get("resource_rents_pct_gdp") or 0
    youth_unemp = context.get("youth_unemployment") or 0
    growth = context.get("growth_trajectory", "growing")

    severity_factors = []
    if resource_rents > thresholds["resource_rents_trigger"]:
        severity_factors.append(f"resource rents {resource_rents:.1%} > 30%")
    if growth in ("stagnant", "declining"):
        severity_factors.append(f"growth trajectory: {growth}")
    if context.get("oda_dependent", False):
        severity_factors.append("ODA dependent")

    compounding = []
    if youth_unemp > thresholds["youth_unemployment_compound"]:
        compounding.append(f"youth unemployment {youth_unemp:.1%} > 25%")

    probable = len(severity_factors) > 0
    triggered = is_transition  # Always flag transitions; grade by severity

    severity = "PROBABLE reversal" if probable else "AT RISK"
    if compounding:
        severity += f" (compounded by: {', '.join(compounding)})"

    return {
        "name": "Reversal Risk",
        "triggered": triggered,
        "severity": severity,
        "factors": severity_factors + compounding,
        "explanation": (
            f"Democratic transition with weak economic delivery. "
            f"Severity: {severity}. Factors: {', '.join(severity_factors + compounding) or 'general weakness'}."
        ),
        "modification": (
            "Prediction becomes conditional: initial trajectory positive "
            "BUT reversal probable without economic consolidation."
            if probable else
            "Flag as at-risk. Monitor economic delivery indicators."
        ),
        "derivation": "Tunisia — predicted initial trajectory but missed 2021 coup",
    }


def evaluate_safeguard_d(pillars: dict, context: dict) -> dict:
    """
    Safeguard D — Predatory Neighbor / Exogenous Shock Flag

    Derived from: Ukraine observation
    Validated by: Myanmar (China), Bangladesh (India), Ethiopia/Tigray (Eritrea)
    """
    threat = context.get("neighbor_threat_level", "none")
    triggered = threat in ("moderate", "high")
    p1 = pillars.get("P1")
    low_p1 = p1 is not None and p1 < LENS["p1_median"]

    return {
        "name": "Predatory Neighbor / Exogenous Shock",
        "triggered": triggered,
        "explanation": (
            f"Neighbor threat: {threat}. {context.get('neighbor_details', '')} "
            f"{'Low P1 compounds vulnerability.' if low_p1 else 'P1 provides some resilience.'} "
            "Framework diagnoses vulnerability to shock, not the shock itself."
            if triggered else "No significant predatory neighbor threat identified."
        ),
        "modification": (
            "Note endogenous prediction separately. Flag that outcome may be "
            "externally imposed rather than internally generated."
            if triggered else None
        ),
        "derivation": "Ukraine (Russia invasion); Inca (Spanish conquest)",
    }


def evaluate_safeguard_e(pillars: dict, context: dict) -> dict:
    """
    Safeguard E — Rentier Capture Flag (BIDIRECTIONAL)

    Derived from: Timor-Leste (negative), Nigeria (positive)
    """
    thresholds = SAFEGUARD_THRESHOLDS["E_rentier_capture"]
    rents_gdp = context.get("resource_rents_pct_gdp") or 0           # PERCENT of GDP
    rents_revenue = context.get("resource_rents_pct_revenue") or 0   # PERCENT of revenue
    p1 = pillars.get("P1")

    # V2 graded thresholds (percent of GDP): below 15% no penalty; 15-25% material; >25% severe.
    if rents_gdp > thresholds["e2_severe_gdp"]:
        tier = "E-2 (SEVERE)"
        neg_mod = "Substantial P1 discount — institutional quality likely UNRELIABLE."
    elif rents_gdp > thresholds["e1_material_gdp"]:
        tier = "E-1 (MATERIAL)"
        neg_mod = "Moderate qualitative P1 discount — institutional quality potentially undermined."
    else:
        tier = None
        neg_mod = None

    negative_triggered = tier is not None
    unreliable_p1 = (rents_revenue > thresholds["rents_revenue_unreliable"]) or (tier == "E-2 (SEVERE)")
    # Positive arm (rent-stabilization): low-P1 state using rents to buy cohesion.
    positive_triggered = (negative_triggered and p1 is not None and p1 < thresholds["positive_p1_ceiling"])

    direction = None
    if positive_triggered:
        direction = "bidirectional (capture + rent-stabilization)"
    elif negative_triggered:
        direction = "negative (rentier capture)"

    return {
        "name": "Rentier Capture (Bidirectional)",
        "triggered": negative_triggered,
        "tier": tier,
        "direction": direction,
        "p1_unreliable": unreliable_p1,
        "explanation": (
            f"Resource rents {rents_gdp:.1f}% of GDP -> {tier or 'below 15% (no penalty)'}. "
            f"{'P1 likely unreliable (E-2, or rents >50% of revenue). ' if unreliable_p1 else ''}"
            f"{'Low P1 + rents = rent-stabilization possible (Nigeria/Gulf model). ' if positive_triggered else ''}"
        ),
        "modification": (
            "Treat P1 as unreliable (equivalent to Safeguard A)." if unreliable_p1
            else neg_mod
        ),
        "derivation": "Timor-Leste (negative capture); Nigeria/Gulf (positive stabilization). V2: graded E-1/E-2.",
    }


def evaluate_safeguard_f(pillars: dict, context: dict) -> dict:
    """
    Safeguard F — Sub-State Turbulence Indicator

    Derived from: Round 3 (Northern Ireland Stormont, Germany AfD)
    Validated by: Belgium, Spain/Catalonia
    """
    thresholds = SAFEGUARD_THRESHOLDS["F_substate_turbulence"]

    antisystem_vote = context.get("regional_antisystem_vote") or 0
    exec_collapses = context.get("executive_collapses") or 0
    regional_divergence = context.get("regional_gdp_divergence") or 0

    triggers = []
    if antisystem_vote > thresholds["antisystem_vote_threshold"]:
        triggers.append(f"anti-system vote {antisystem_vote:.1%} > 25%")
    if exec_collapses >= LENS["f_executive_collapses_min"]:
        triggers.append(f"{exec_collapses} executive collapses")
    if regional_divergence > thresholds["regional_divergence_threshold"]:
        triggers.append(f"regional divergence {regional_divergence:.1%} > 30%")

    triggered = len(triggers) > 0

    return {
        "name": "Sub-State Turbulence",
        "triggered": triggered,
        "triggers": triggers,
        "explanation": (
            f"Managed instability detected: {', '.join(triggers)}. "
            "State will survive but experiences significant ongoing dysfunction. "
            "This is a chronic management load, not a collapse indicator."
            if triggered else "No significant sub-state turbulence indicators."
        ),
        "modification": (
            "Flag 'managed instability' — state survives but with significant "
            "chronic dysfunction below the survival threshold."
            if triggered else None
        ),
        "derivation": "NI Stormont collapses; Germany AfD in eastern states",
    }


def evaluate_safeguard_g(pillars: dict, context: dict) -> dict:
    """
    Safeguard G — Suppression vs Prevention Distinction (THREE-TIER)

    Derived from: Round 3 (suppression/prevention indistinguishable)
    Validated by: Spain (Tier 2), Belgium/NI (Tier 3), Nigeria/Ethiopia (Tier 1)
    """
    mechanism = context.get("fragmentation_mechanism")
    prior_porosity = context.get("prior_porosity_period", False)
    p1 = pillars.get("P1")

    if mechanism is None:
        return {
            "name": "Suppression vs Prevention",
            "triggered": False,
            "explanation": "No fragmentation mechanism specified.",
            "modification": None,
            "derivation": "Round 3 — Ethiopia vs NI indistinguishable without this",
        }

    # Re-suppression after porosity is the worst case
    if prior_porosity and mechanism in ("military", "coup", "authoritarian_reversal"):
        tier = "RE-SUPPRESSION AFTER POROSITY (WORST PATH)"
        prediction = (
            "Catastrophic fragmentation predicted. Porosity period created "
            "mobilized actors that re-suppression cannot re-absorb. "
            "Outcome worse than continuous suppression."
        )
    elif mechanism == "military":
        tier = "TIER 1 — Military Suppression"
        prediction = (
            "Mismatch NOT resolved. Predict continued instability "
            "and future fragmentation attempts. High casualty cost."
        )
    elif mechanism in ("legal", "institutional", "article_155"):
        tier = "TIER 2 — Institutional/Legal Suppression"
        prediction = (
            "Mismatch partially addressed. Predict de-escalation but not "
            "permanent resolution. Pressure may recur. Near-zero casualty cost."
        )
    elif mechanism in ("porosity", "power_sharing", "devolution", "gfa"):
        tier = "TIER 3 — Prevention/Porosity"
        prediction = (
            "Mismatch partially or fully addressed through institutional design. "
            "Predict reduced but ongoing pressure with maintenance costs."
        )
    else:
        tier = f"UNCLASSIFIED: {mechanism}"
        prediction = "Unable to classify mechanism."

    return {
        "name": "Suppression vs Prevention",
        "triggered": True,
        "tier": tier,
        "mechanism": mechanism,
        "prior_porosity": prior_porosity,
        "explanation": f"Classification: {tier}.",
        "modification": prediction,
        "derivation": "Round 3-4: Spain Tier 2, NI/Belgium Tier 3, Nigeria/Ethiopia Tier 1, Myanmar re-suppression",
    }


def evaluate_safeguard_i(pillars: dict, context: dict) -> dict:
    """
    Safeguard I — Porosity-with-Backstop

    Derived from: Round 4/5 (Ethiopia/Tigray, Myanmar)
    The framework's most genuinely novel prediction.
    """
    has_backstop = context.get("external_backstop", False)
    has_porosity = context.get("fragmentation_mechanism") in (
        "porosity", "insurgency", "civil_war", "territorial_loss"
    )

    triggered = has_backstop and has_porosity

    return {
        "name": "Porosity-with-Backstop",
        "triggered": triggered,
        "explanation": (
            f"External backstop present ({context.get('backstop_details', 'unknown')}). "
            "Framework predicts re-suppression and territorial reconsolidation "
            "rather than permanent secession. Reabsorption typically partial "
            "and recurrence-prone."
            if triggered else "No backstop-porosity configuration detected."
        ),
        "modification": (
            "Predict re-suppression rather than permanent independence. "
            "The backstop patron enables reconsolidation."
            if triggered else None
        ),
        "derivation": "Ethiopia/Tigray (AU backstop); Myanmar (China backstop)",
        "falsification_condition": (
            "A porosity-with-backstop case resolving into permanent, "
            "internationally-recognized independence."
        ),
    }


def evaluate_mod4(pillars: dict, context: dict) -> dict:
    """
    Mod4 — Margin-of-Error Gate

    Essential modification: P1 ordinality claim applies ONLY when
    the gap between compared entities exceeds margin of error.
    """
    comparison_gap = context.get("p1_comparison_gap")
    margin = LENS["mod4_margin"]  # ordinal abstention threshold (single source: constants.LENS)
    p1_min_level = context.get("p1_min_level")  # min P1 of the compared pair (for the V3 rule)

    if comparison_gap is None:
        return {
            "name": "Margin-of-Error Gate (Mod4)",
            "triggered": False,
            "explanation": "No comparison gap provided.",
            "modification": None,
        }

    within_margin = abs(comparison_gap) < margin
    # V3 consolidated-pair high-end caution: between two already-consolidated polities, a
    # sub-high-end-margin P1 gap does not predict trajectory (Chile/Uruguay) -> abstain.
    consolidated_pair = (
        p1_min_level is not None
        and p1_min_level > LENS["v3_consolidation_threshold"]
        and abs(comparison_gap) < LENS["v3_high_end_margin"]
    )
    abstain = within_margin or consolidated_pair
    reason = ("within margin of error" if within_margin
              else "consolidated-pair high-end caution (both above the capacity threshold; "
                   "sub-high-end-margin gaps don't predict trajectory)" if consolidated_pair
              else None)

    return {
        "name": "Margin-of-Error Gate (Mod4)",
        "triggered": abstain,
        "gap": comparison_gap,
        "margin": margin,
        "consolidated_pair": consolidated_pair,
        "explanation": (
            f"P1 gap ({comparison_gap:.3f}) -> ABSTAIN ({reason})."
            if abstain else
            f"P1 gap ({comparison_gap:.3f}) exceeds margin ({margin}) and not a consolidated-pair "
            "case. Ordinal prediction is warranted."
        ),
        "modification": (
            "ABSTAIN from P1 ordinality claim. Do not predict which entity "
            "will outperform — too close to call / consolidated pair."
            if abstain else None
        ),
    }


def evaluate_mod8(pillars: dict, context: dict) -> dict:
    """
    Mod8 — Violence Risk/Agency Split

    Essential modification: Framework predicts violence RISK, not AGENCY.
    """
    return {
        "name": "Violence Risk/Agency Split (Mod8)",
        "triggered": True,  # Always active as a framing constraint
        "explanation": (
            "STANDING INSTRUCTION: All violence predictions must specify RISK "
            "(the structural vulnerability) separately from AGENCY (who initiates). "
            "The MI predicts elevated risk from low P1 and complexity-capacity mismatch. "
            "It does NOT predict who strikes first or whether violence originates "
            "endogenously or exogenously."
        ),
        "modification": (
            "Frame all violence predictions as: 'elevated risk of violent outcome' "
            "rather than 'this entity will initiate violence.'"
        ),
        "derivation": "East Timor — violence came from departing Indonesia, not from low Timorese P1",
    }
