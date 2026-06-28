"""
Modernization Index — Constants and Configuration

All weights, thresholds, and indicator specifications.
This is the single source of truth for framework parameters.
"""

# === PILLAR WEIGHTS ===
# MI v1 is the canonical, only-supported methodology from 2026-06-27 onward.
# "MI v1" == the former "LIVE"/v2 version (correlation-derived weights; data
# independently pushed P1 from 25% to 34%, plus Mods 4/8 and Safeguards A-I).
# ALWAYS use WEIGHTS for scoring.
WEIGHTS = {
    "P1": 0.34,  # Institutional Quality (most central: avg |r| = 0.79-0.80)
    "P2": 0.15,  # Innovation & Knowledge Economy
    "P3": 0.16,  # Human Capital
    "P4": 0.20,  # Economic Structure & Independence
    "P5": 0.16,  # Stability & Resilience
}

# === ARCHIVED — DO NOT USE FOR SCORING ===
# Original hand-assigned draft weights (the pre-release "v0" weighting, previously
# labelled "v1"). ARCHIVED 2026-06-27: superseded by MI v1 (WEIGHTS above). Retained
# ONLY for the documented 25%->34% provenance and historical sensitivity, never for
# canonical scoring. See docs/architectural_decisions/mi_v1_naming_and_archive.md.
WEIGHTS_ARCHIVED_HAND_V0 = {
    "P1": 0.25,
    "P2": 0.25,
    "P3": 0.20,
    "P4": 0.20,
    "P5": 0.10,
}

# Equal weights for sensitivity analysis (a robustness control, not a version)
WEIGHTS_EQUAL = {
    "P1": 0.20,
    "P2": 0.20,
    "P3": 0.20,
    "P4": 0.20,
    "P5": 0.20,
}

# === V2 WEIGHTING ARCHITECTURE (retrodiction decides; equal wins ties) ===
# V1's P1=0.34 was an artifact of the 85-country/2018 sample. At 143 countries across
# three time points the most-central pillar ROTATES and all five sit in a tight
# 0.71-0.80 correlation band — so V2 chooses between:
#   Option A — equal weights (WEIGHTS_EQUAL above). Simple, defensible, empirically supported.
#   Option B — time-varying: the most-central pillar at the stress-event era is elevated.
WEIGHTS_V2_EQUAL = dict(WEIGHTS_EQUAL)
# Measured rotation (the era's binding constraint / most-central pillar):
V2_ERA_LEADER = {"2012": "P2", "2018": "P1", "2024": "P3"}
V2_ELEVATED_WEIGHT = 0.30  # leader pillar; remaining 0.70 split equally (0.175 each)
# Active V2 weighting — set by the A-vs-B retrodiction (see docs/architectural_decisions/).
# "equal" | "timevarying" | "v1" (v1 retained only for V1 reproduction).
MI_ACTIVE_WEIGHTING = "equal"

# === MI v1 LENS — the single scoring config ===
# Every scoring/normalization/safeguard threshold the engine uses lives HERE.
# Edit a value once and it propagates to all cases on the next re-score. This is
# the "universal config": the lens through which the (fixed) structural inputs are
# scored. Per-case data and predictions live in the case records, not here.
LENS = {
    # composite
    "min_pillars_for_mi": 3,
    # P4 / P5 normalization denominators (inversion points)
    "resource_rents_full_dependence_pct": 50.0,   # rents/50 -> fully dependent
    "oda_full_dependence_pct": 20.0,              # oda/20  -> fully dependent
    "fsi_max": 120.0,                             # FSI 0-120 scale
    # P2 ECI min-max (dataset-relative; override per-record via eci_dataset_min/max)
    "eci_default_min": -2.5,
    "eci_default_max": 2.5,
    # P4 GDP log min-max reference range (fixed absolute scale, by design)
    "gdp_ppp_floor": 500.0,
    "gdp_ppp_ceiling": 150000.0,
    # Mod4 — margin-of-error gate (ordinal abstention threshold on the 0-1 P1 scale)
    "mod4_margin": 0.10,
    # capacity / risk cutoffs
    "p1_bottom_third": 0.33,        # Safeguard B/E gate; CRITICAL risk
    "p1_median": 0.50,             # Safeguard D; WARNING risk
    "p1_strategy_authoritarian": 0.40,
    "p1_porosity_min": 0.60,
    "p1_complexity_control_min": 0.70,
    # pillar-spread risk cutoffs
    "spread_critical": 0.50,
    "spread_warning": 0.35,
    # Safeguard F
    "f_executive_collapses_min": 2,
    # strategy classification
    "small_population": 10_000_000,
    # V2 below-floor configuration diagnostic
    "below_floor_mi": 0.40,            # apply the partial-failure diagnostic at/below this MI
    "partial_failure_p4_min": 0.50,   # "has money": resource/income pillar strong
    "partial_failure_p1p2_max": 0.40, # "no institutions/economy": P1 and P2 catastrophic
    # === V3 — consolidated-pair high-end caution (Mod4 extension) ===
    # Derived from the lone V2 falsification (Chile/Uruguay): a 3.5-sigma pre-event P1 gap did
    # NOT predict trajectory because BOTH polities were already consolidated. Complexity-capacity
    # matching: above the capacity threshold, more capacity no longer predicts a better outcome.
    # So between two consolidated polities (both P1 > threshold), abstain on a P1-ordinal call
    # unless the gap is wide (>= high-end margin). Calibrated on the 2 available high-vs-high pairs
    # (Chile/Uruguay reversed at 0.107; Singapore/Malaysia held at 0.247) -> PRELIMINARY (n=2).
    "v3_consolidation_threshold": 0.60,
    "v3_high_end_margin": 0.15,
    # === V3.1 — structural vulnerability gate (P4-P1 gap; the "durability gap") ===
    # DISCOVERED on the N=21 signature set: the acute pre-turn DECLINE signature fails blind
    # (14-25% sens, 40% PPV), but a single LEVEL variable — the gap between economy/income (P4) and
    # institutions (P1) — separates real crises from absorbers cleanly (crisis mean 0.29 vs no-crisis
    # 0.10). Rule: P4 - P1 > threshold -> structurally crisis-vulnerable ("granted/fragile": income
    # has outrun institutions). N=21: 83% sens / 100% spec / 100% PPV (only misses = the idiosyncratic
    # acute cases Chile & S.Korea, which have no structural warning by design). This is the durability
    # ratio re-derived as a forward gate; it works where the decline signature failed because a LEVEL
    # is persistent/forward-available while a trajectory emerges late.
    "structural_vulnerability_gap": 0.22,   # nominal cut (back-compat boolean); see band below
    # The single 0.22 line is FALSE PRECISION: on N=21 the data is UNIDENTIFIED inside (0.203, 0.283).
    # Every structural crisis sits at gap >= 0.283 (crisis floor = Tunisia); every confirmed absorber
    # sits at gap <= 0.203 (absorber ceiling = Hungary); the zone between is EMPTY in the test set, so
    # no cutoff there is distinguishable. Report three states, not a hard pass/fail:
    "structural_vuln_flag_floor": 0.28,     # gap >= this -> FLAGGED (matches all 10 crises, 0 absorbers)
    "structural_vuln_clear_ceiling": 0.20,  # gap <= this -> CLEAR (absorber-class)
    # V3.2 Convergence Qualifier: a flagged durability gap means OPPOSITE things by trajectory.
    # CLOSING gap (institutions catching up to income) = developmental catch-up (downgrade);
    # WIDENING/static gap (the grant eroding) = genuine fragility. Validated on flagged states:
    # 92% sens / 80% spec (errors: Saudi rentier-overshoot FP, Peru institutional-churn FN).
    "structural_vuln_converge_deadband": 0.01,  # |dgap| <= this over the window -> "static"
    # V3.2 Accountability Gap (HYPOTHESIS — informational diagnostic, NOT a verdict; no crisis
    # evidence yet). P1 excludes Voice & Accountability (VA) by design; among high-capacity states VA
    # is the only axis separating democracies from rich authoritarians. VA - P4 (income) below the
    # cap = "capacity without consent" (legitimacy-capped: Saudi/China/Russia/Turkey) — hypothesized
    # brittle/sudden failure mode, orthogonal to the durability gap. All in 0-1 units.
    "va_legitimacy_cap_p4": -0.50,     # VA - P4 <= this -> legitimacy-capped
    "va_accountability_lag_p4": -0.20,  # VA - P4 in (cap, this] -> accountability lag
    # (0.20, 0.28) = BORDERLINE / indeterminate — no validated evidence either way. The US (gap 0.211,
    # 2024) lands here, ABOVE every confirmed absorber, ~one 0.07 institutional backslide from the floor.
}

# Active MI model version. V3 = V2 + consolidated-pair Mod4 extension.
# V3.1 = V3 + Safeguard J (the durability gate, P4-P1 gap) — independently derived on the N=21
# signature set (83% sens / 100% spec / 100% PPV), unifying with the durability ratio.
# V3.2 = V3.1 + the Convergence Qualifier on Safeguard J (gap TRAJECTORY: closing=developmental
# catch-up vs widening=fragility; 92% sens / 80% spec on flagged states) + the Accountability-Gap
# diagnostic (VA vs income; "capacity without consent", a hypothesis — informational, not a verdict).
# V3.3 = V3.2 + the LEVEL-OVER-SLOPE epistemic, made operational: movement_quality (the typology +
# an explicit distrust-the-slope caveat) + ascent_potential (low institutional base -> elevated
# durable-climb tendency; the one HOLDOUT-VALIDATED golden-age signal, z+2.4). NB: the golden-age
# *signature* (CC/component jumps) was REFUTED on a pre-registered geographic holdout (z=-0.0) and is
# deliberately NOT added — golden ages are exogenous (level + era + commodity), not internal slope.
MI_MODEL_VERSION = "v3.3"

# Ascent potential: low institutional base predicts a durable climb (room-to-rise / mean-reversion),
# holdout-validated (z+2.4). Not agency — needs an exogenous trigger (transition/commodity window).
ASCENT_LOW_BASE = 0.40

# === GLOBAL SYSTEMS MEASUREMENT (system-level category, distinct from country-level MI) ===
# Aggregates the validated world-system findings: the three improvement "engines" (institutions/
# income/human-capital climb rates), the institutional "container" trajectory (the supercycle
# discriminator), and the global movement-type distribution. EXPLORATORY/descriptive — proxies, not
# the country scoring engine. See docs/global_systems_measurement.md.
# Historical median 10y climb rate per engine (1850-2012, from longrun analysis) — the "firing" bar:
GLOBAL_ENGINE_MEDIAN = {"institutions": 0.049, "income": 0.052, "human_capital": 0.068}
GLOBAL_ENGINE_THRESH = {"institutions": 0.15, "income": 0.50, "human_capital": 7.0}  # 10y climb to count
# Container trajectory bands (institutional net climb-minus-decline rate over the window):
GLOBAL_CONTAINER_STRENGTHENING = 0.05   # net >= this -> robust/strengthening (absorbs deceleration)
GLOBAL_CONTAINER_ERODING = -0.02        # net <= this -> brittle/eroding

# === LEAD-TIME / FORESIGHT CONFIG (single source; the per-case structural fact reads this) ===
# How far before the outcome the framework still predicts accurately. Empirical finding:
# the ORDINAL/STRUCTURAL signal (who is more durable; is a state structurally fragile) is stable
# ~10-28 years out (institutional rank is persistent); the ACUTE-TIMING signal (when a stable-
# looking state actually turns over) is only ~3-5 years out (the framework is directional, not a
# timing oracle - Mod8). Predictor = pre-event P1 at (outcome_anchor - lead); Mod4 + consolidated-
# pair gates apply (an abstention is "correctly cautious", not a miss).
LEAD_TIME = {
    "outcome_anchor": 2024,
    "leads_years": [1, 3, 5, 7, 10, 15, 20, 28],
    "structural_horizon_years": 10,        # ordinal/fragility signal reliable to >= this (empirically ~28)
    "acute_timing_horizon_years": "3-5",   # collapse/turn-over date only foreseeable this far out
    "gates": "Mod4 margin + V3 consolidated-pair caution",
    "finding": ("ordinal accuracy flat ~92% from 1y to 28y (no horizon decay; rank is persistent); "
                "21/26 single-entity risk tiers stable across a decade; acute timing ~3-5y only."),
}

# === INDICATOR SPECIFICATIONS ===
INDICATORS = {
    "P1": {
        "name": "Institutional Quality",
        "indicators": {
            "gov_effectiveness": {
                "source": "World Bank WGI",
                "scale": "0-100 percentile (legacy) or anchored 0-100 (2025+)",
                "normalization": "score / 100",
                "track2_substitute": None,
            },
            "rule_of_law": {
                "source": "World Bank WGI",
                "scale": "0-100 percentile or anchored 0-100",
                "normalization": "score / 100",
                "track2_substitute": None,
            },
            "regulatory_quality": {
                "source": "World Bank WGI",
                "scale": "0-100 percentile or anchored 0-100",
                "normalization": "score / 100",
                "track2_substitute": None,
            },
            "corruption_control": {
                "source": "Transparency International CPI",
                "scale": "0-100",
                "normalization": "score / 100",
                "track2_substitute": "WGI Control of Corruption (for pre-2012)",
            },
        },
        "pillar_score": "arithmetic mean of normalized indicators",
    },
    "P2": {
        "name": "Innovation & Knowledge Economy",
        "indicators": {
            "innovation_index": {
                "source": "WIPO GII",
                "scale": "0-100",
                "normalization": "score / 100",
                "track2_substitute": "R&D Expenditure % GDP (min-max, for pre-2007)",
            },
            "economic_complexity": {
                "source": "Harvard/OEC ECI",
                "scale": "~-2.5 to +2.5",
                "normalization": "min-max within dataset",
                "track2_substitute": None,
            },
        },
        "pillar_score": "arithmetic mean of normalized indicators",
    },
    "P3": {
        "name": "Human Capital",
        "indicators": {
            "education_index": {
                "source": "UNDP HDR",
                "scale": "0-1",
                "normalization": "already normalized",
                "track2_substitute": None,
            },
            "life_expectancy_index": {
                "source": "UNDP HDR",
                "scale": "0-1",
                "normalization": "already normalized",
                "track2_substitute": None,
            },
        },
        "pillar_score": "arithmetic mean",
    },
    "P4": {
        "name": "Economic Structure & Independence",
        "indicators": {
            "gdp_per_capita_ppp": {
                "source": "World Bank WDI",
                "scale": "continuous",
                "normalization": "log-transform, then min-max",
                "track2_substitute": None,
            },
            "resource_rents_pct_gdp": {
                "source": "World Bank WDI",
                "scale": "0-60%+",
                "normalization": "inverted: 1 - min(rents/50, 1)",
                "track2_substitute": None,
            },
            "oda_pct_gni": {
                "source": "World Bank WDI",
                "scale": "0-20%+",
                "normalization": "inverted: 1 - min(oda/20, 1)",
                "track2_substitute": None,
            },
        },
        "pillar_score": "arithmetic mean of normalized indicators",
    },
    "P5": {
        "name": "Stability & Resilience",
        "indicators": {
            "political_stability": {
                "source": "World Bank WGI",
                "scale": "0-100 percentile or anchored 0-100",
                "normalization": "score / 100",
                "track2_substitute": None,
            },
            "fragile_states_index": {
                "source": "Fund for Peace FSI",
                "scale": "0-120 (higher = worse)",
                "normalization": "inverted: 1 - (fsi/120)",
                "available_from": 2006,
                "track2_substitute": "P5 = political_stability alone (pre-2006)",
            },
        },
        "pillar_score": "arithmetic mean (or sole indicator for Track 2 pre-2006)",
    },
}

# === SAFEGUARD THRESHOLDS ===
SAFEGUARD_THRESHOLDS = {
    "B_capacity_gate": {
        "description": "Minimum P1 for fragment count to indicate manageability",
        "threshold": "bottom third of Rule of Law (ordinal, not fixed number)",
        "note": "Apply ordinally due to 2025 WGI revision changing scales",
    },
    "C_reversal_risk": {
        "resource_rents_trigger": 0.30,  # 30% of GDP
        "youth_unemployment_compound": 0.25,  # 25%
        "description": "Democratic transition + weak P4 = reversal risk",
    },
    "E_rentier_capture": {
        # V2 empirically-derived graded thresholds (143-country data), in PERCENT of GDP to
        # match the WB resource-rents unit (e.g. 38.83 = 38.83%). Below 15% ~= zero effect.
        # (V1 expressed these as fractions (0.25) while the data is percent -> trivially-true
        #  comparison; V2 fixes the unit.)
        "e1_material_gdp": 15.0,   # 15-25% of GDP -> MATERIAL penalty: P1 potentially undermined (moderate discount)
        "e2_severe_gdp": 25.0,     # >25% of GDP -> SEVERE penalty: P1 likely unreliable (substantial discount)
        "rents_revenue_unreliable": 50.0,  # >50% of revenue = treat P1 as unreliable
        "bidirectional": True,
        "positive_p1_ceiling": 0.33,  # rent-stabilization (positive arm): low-P1 state using rents for cohesion
        "note": "V2: graded E-1/E-2 (percent-of-GDP); below 15% no penalty. Bidirectional retained.",
    },
    "F_substate_turbulence": {
        "antisystem_vote_threshold": 0.25,  # 25% in any region
        "regional_divergence_threshold": 0.30,  # 30% GDP per capita gap
        "description": "Chronic management load indicator, not collapse predictor",
    },
}

# === TIER BOUNDARIES ===
TIERS = {
    1: {"name": "Fully Modernized", "m_score_min": 0.80},
    2: {"name": "Highly Modernized", "m_score_min": 0.60},
    3: {"name": "Moderately Modernized", "m_score_min": 0.40},
    4: {"name": "Emerging Modern", "m_score_min": 0.20},
    5: {"name": "Fragile Modern", "m_score_min": 0.00},
    6: {"name": "Below Floor", "m_score_min": float("-inf")},
}

# === STRATEGY CLASSIFICATION ===
STRATEGIES = {
    "porosity": {
        "description": "High complexity managed through institutional diffusion",
        "p1_requirement": "high",
        "failure_mode": "institutional exhaustion, chronic dysfunction",
        "examples": ["Switzerland", "Belgium", "UK/GFA", "Canada"],
    },
    "suppression": {
        "description": "Complexity managed through authoritarian control",
        "p1_requirement": "any (determines suppression tier)",
        "failure_mode": "violent fragmentation when control weakens",
        "tiers": {
            1: "Military suppression (armed force)",
            2: "Institutional/legal suppression (high-P1, legal mechanisms)",
            3: "Re-suppression after porosity (WORST outcome)",
        },
        "examples": {
            1: ["Nigeria/Biafra", "Ethiopia/Tigray"],
            2: ["Spain/Catalonia"],
            3: ["Myanmar post-2021"],
        },
    },
    "complexity_control": {
        "description": "Complexity kept below fragmentation threshold",
        "p1_requirement": "high (reflects management efficiency)",
        "failure_mode": "demographic/economic stagnation",
        "examples": ["Singapore", "Japan", "island nations"],
    },
}

# === ANCHORS ===
# For v1 anchor-based scoring
ANCHOR_CEILING = "Switzerland"  # M-Score = 1.000
ANCHOR_FLOOR = "Lebanon"  # M-Score = 0.000

# === VALIDATED BASELINE ===
BASELINE = {
    "version": "MI v1 (canonical; formerly 'LIVE')",
    "n_modern_cases": 20,
    "n_ancient_cases": 5,
    "clean_confirmation_rate": 0.78,  # best estimate
    "clean_confirmation_range": (0.62, 0.85),  # strict to generous
    "directional_accuracy": 1.00,  # zero falsifications
    "p1_ordinality": "20/20",
    "total_predictions": "~130",
    "falsifications": 0,
}
