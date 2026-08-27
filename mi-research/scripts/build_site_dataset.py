#!/usr/bin/env python3
"""
Build the published dataset the website consumes - the engine, run in public, over ALL available data.

Coverage levels (every country gets a page; gaps are shown, never faked):
  A. wb_anchored (full indicators)        -> canonical via datasource.get_indicators
  B. mi-pipeline panel (full indicators)  -> assembled by iso3 (P1/P2/P3) + wgi_full_panel (gdp/PV/rents)
  C. wgi_full_panel only (WGI institutions + gdp) -> partial pillars, gaps shown
The validated mi-research engine (score_country) is the single source of truth; this script only
ASSEMBLES inputs and calls it. Deterministic.

Emits to web/public/data: countries.json, country/<slug>.json, meta.json
"""
import json
import math
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mi.scoring import (score_country, get_score_band, get_configuration_profile,
                        calculate_pillar_spread)
from mi.diagnostics import (below_floor_diagnostic, ascent_potential,
                            classify_strategy, assess_vulnerability,
                            movement_quality, accountability_gap)
from mi.safeguards import evaluate_all_safeguards
from mi.panel import DISPLAY_FIX, iter_universe, indicators_for

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT.parent / "mi-website" / "web" / "public" / "data"
YEAR = 2024

PILLAR_NAMES = {"P1": "Institutions", "P2": "Economic Complexity", "P3": "Human Capital",
                "P4": "Economic Structure", "P5": "Stability & Resilience"}
SCORE_BAND_LABEL = {1: "Highly Modernized", 2: "Durable", 3: "Mixed", 4: "Fragile", 5: "Floor"}
INDICATOR_SOURCES = {
    "gov_effectiveness": "World Bank WGI", "rule_of_law": "World Bank WGI",
    "regulatory_quality": "World Bank WGI", "control_of_corruption": "World Bank WGI",
    "voice_accountability": "World Bank WGI", "political_stability": "World Bank WGI",
    "cpi": "Transparency International", "gii": "WIPO Global Innovation Index",
    "rd_pct_gdp": "World Bank WDI", "eci": "Harvard Atlas (ECI)",
    "education_index": "UNDP HDR", "life_expectancy_index": "UNDP HDR",
    "gdp_per_capita_ppp": "World Bank WDI", "resource_rents_pct_gdp": "World Bank WDI",
    "oda_pct_gni": "World Bank WDI", "fsi": "Fund for Peace FSI",
}
def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


PILLARS_L = ["P1", "P2", "P3", "P4", "P5"]
PRIOR_YEAR = 2014  # ~10y prior scored state, for movement quality (real-vs-hollow ascent)
_SRC = ROOT / "data" / "sources"


def _load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return default


_COPY_REPLACEMENTS = {
    "Spread between the strongest and weakest pillar, the country's structural shape.":
        "The gap between the strongest and weakest pillar shows how balanced the country's structure is.",
    "Institutions roughly match or exceed what income predicts, durable.":
        "Institutions roughly match or exceed the level predicted by income, which suggests greater durability.",
    "Wealth has outrun institutions, historically fragile.":
        "Income has grown faster than institutional strength, a pattern associated with greater fragility.",
    "institutions roughly keep pace with income, not structurally crisis-flagged (absorber-class on this measure).":
        "Institutions roughly keep pace with income, so this measure does not flag elevated structural risk.",
    "This country's prosperity has outrun its institutions. Income the institutions cannot anchor is the classic fragility signal, historically it tends not to last.":
        "This country's income has risen faster than its institutions. In the historical cases, that gap is associated with greater fragility.",
    "A state can survive intact while carrying chronic, managed instability, repeated executive collapses, high anti-system voting, sharp regional divergence. This is a management-load signal, not a collapse indicator.":
        "A state can remain intact while dealing with repeated government collapses, high anti-system voting, or sharp regional divisions. This check measures that ongoing burden, not the likelihood of collapse.",
    "Bosnia's WGI institutional scores under the Dayton OHR sat above Croatia's and Serbia's, the administrator's competence, not indigenous capacity, was being measured. The safeguard discounts raw P1 where an external administrator governs.":
        "Under the Dayton OHR, Bosnia's WGI scores partly reflected the external administrator's capacity. This safeguard discounts P1 when an external administration is doing much of the governing.",
    "Sudan split into just two successor states, a low fragment count that would normally read as manageable, yet produced the worst outcome in the sample, because institutional capacity (P1) was far below the bottom third. Low count is not safety when P1 is that low.":
        "Sudan produced only two successor states, but the outcome was still the worst in the sample because institutional capacity was very low. A small number of fragments is not reassuring when P1 is that weak.",
    "The framework's most genuinely novel prediction: when a great-power patron backstops a state's territorial integrity, an internal secession tends to end in re-suppression and partial reconsolidation, not permanent independence.":
        "This safeguard tests whether support from a major outside power makes renewed suppression and partial reunification more likely than permanent independence.",
    "The framework predicted Tunisia's initial positive trajectory but missed the 2021 presidential self-coup. Democratic transitions with weak economic delivery are flagged as reversal-prone rather than assumed durable.":
        "The framework captured Tunisia's initial improvement but missed the 2021 presidential self-coup. This safeguard marks democratic transitions with weak economic results as vulnerable to reversal.",
    "Suppression and prevention looked identical until this safeguard split them into tiers: military suppression (Tier 1) doesn't resolve the underlying mismatch; institutional/legal suppression (Tier 2) de-escalates; porosity/power-sharing (Tier 3) addresses it by design. Re-suppression after a porosity period is the worst path.":
        "This safeguard separates military suppression, legal or institutional de-escalation, and power-sharing. In the case studies, renewed suppression after a period of power-sharing had the worst outcomes.",
    "Short-term movement is noisy: movement is mean-reverting and low-reliability; the predictive content is the LEVEL and the durability gap, not the delta.":
        "Short-term movement is noisy and often reverses. The current level and the durability gap are more informative than a recent change.",
    "No clear classification: gap sits in the empty band between the validated absorber ceiling and crisis floor; above every confirmed absorber but below the crisis floor. Elevated watch, not a verdict.":
        "The gap falls between the comparison ranges used for lower-risk and crisis cases. It deserves attention, but the available evidence does not support a firm classification.",
    "Structural vulnerability flag: income/economy has outrun institutions (granted/fragile); elevated crisis risk under shock.":
        "Income and economic development have moved ahead of institutional strength. The historical cases associate this gap with higher risk under stress.",
    "Scored on the pillars we have data for. Its score is not directly comparable to a fully-measured country, the missing pillars are unmeasured, not zero.":
        "This score uses only the pillars with available data. It is not directly comparable with a complete five-pillar score, and missing pillars are unmeasured rather than zero.",
    "Resource rents can inflate or hollow out measured institutional quality (Timor-Leste), or buy elite cohesion in a low-capacity state (Nigeria/Gulf). Graded E-1 (material, >15% of GDP) / E-2 (severe, >25%); severe rents make P1 unreliable.":
        "Resource income can distort measures of institutional strength or help governments maintain elite support. This check marks rents above 15 percent of GDP and treats levels above 25 percent as severe.",
    "A structurally sound state can be overrun from outside. The safeguard separates a country's endogenous trajectory from vulnerability to an aggressive neighbour or external shock, so the outcome isn't misread as internally generated.":
        "External threats can overwhelm a country even when its internal structure is sound. This safeguard records those threats separately from conditions inside the country.",
    "No significant predatory neighbor threat identified.":
        "No major threat from a hostile neighboring state was identified.",
    "The base is already high, so large structural jumps from here are historically rare.":
        "The institutional starting level is already high, and large further increases are uncommon in the historical data.",
    "accountability roughly tracks capacity and income.":
        "Accountability is broadly in line with state capacity and income.",
    "accountability trails income/capacity, partial; watch.":
        "Accountability trails income and state capacity. The available evidence is partial, so this remains a watch item.",
    "Institutions match or exceed what the country's income would predict. Prosperity here looks earned, and durable.":
        "Institutions match or exceed the level predicted by income. The historical comparison suggests that this prosperity is more durable.",
    "Starting from a low institutional base, the country is structurally eligible to climb. This is eligibility, not a forecast, the effect only showed up strongly in the 2000s global growth wave.":
        "The country starts from a low institutional level, which was associated with improvement during the 2000s. That period-specific pattern is not a forecast.",
    "A large share of prosperity comes from extracting resources rather than from strong institutions or a complex economy. Historically this masks structural weakness, the money can vanish with a price swing.":
        "A large share of income comes from resource extraction rather than a diverse economy. That dependence can expose the country to price swings and can conceal institutional weakness.",
}


def strip_dashes(obj):
    """Reformat engine diagnostics as plain, readable site copy."""
    if isinstance(obj, str):
        text = obj.replace("\u2014", ",").replace("\u2013", ",").replace("\u2015", ",")
        text = re.sub(r"max\(pillar\)\s+-\s+min\(pillar\)",
                      "max(pillar) minus min(pillar)", text)
        text = re.sub(r"^HYPOTHESIS \(V3\.2\)\s*[-,:]\s*",
                      "Exploratory note (v3.2): ", text, flags=re.IGNORECASE)
        text = re.sub(r"^DISTRUST THE SLOPE\s*[-,:]\s*",
                      "Short-term movement is noisy: ", text, flags=re.IGNORECASE)
        text = re.sub(r"^STRUCTURALLY VULNERABLE\s*[-,:]\s*",
                      "Structural vulnerability flag: ", text, flags=re.IGNORECASE)
        text = re.sub(r"^INDETERMINATE\s*[-,:]\s*",
                      "No clear classification: ", text, flags=re.IGNORECASE)
        text = re.sub(r"^CRITICAL:\s*", "High concern: ", text, flags=re.IGNORECASE)
        text = re.sub(r"^WARNING:\s*", "Watch: ", text, flags=re.IGNORECASE)
        text = re.sub(r"\s+-\s+(?=[a-z])", ", ", text)
        text = re.sub(r"\s+-\s+", ": ", text)
        text = re.sub(r"\s+->\s+", ": ", text)
        text = text.replace("STRUCTURALLY crisis-vulnerable under shock", "structurally vulnerable under stress")
        text = text.replace("UNIDENTIFIED here", "uncertain here")
        text = text.replace("elevated WATCH, not a verdict", "worth closer review, not a firm result")
        text = text.replace("RE-SUPPRESSION AFTER POROSITY (WORST PATH)", "renewed suppression after power-sharing")
        text = text.replace(
            "CAPACITY WITHOUT CONSENT, accountability far below income/capacity; hypothesized brittle failure mode (succession/legitimacy shock). HYPOTHESIS, not a verdict.",
            "Accountability is far below income and state capacity. This is an exploratory concern about succession or legitimacy shocks, not a verdict.",
        )
        text = text.replace("PATRON-SHIELDED", "protected by an outside ally")
        text = text.replace("SHIELDED", "protected")
        text = text.replace("EXPOSED", "exposed")
        text = text.replace("DETERS", "reduces")
        text = text.replace("BLUNTS", "softens")
        text = re.sub(r"\bUNCLASSIFIED\b", "not classified", text)
        text = re.sub(r"\bMATERIAL\b", "material", text)
        text = re.sub(r"\bSEVERE\b", "severe", text)
        text = text.replace("Risk level: CRITICAL", "Risk level: high concern")
        text = re.sub(r"\s+,", ",", text)
        text = re.sub(r"\s{2,}", " ", text)
        text = _COPY_REPLACEMENTS.get(text, text)
        return re.sub(
            r"^(.+) is the pillar dragging the score down\. A chain breaks at its weakest link, so this is where the structural risk concentrates\.$",
            r"\1 is the lowest pillar and the main source of imbalance in the score.",
            text,
        )
    if isinstance(obj, list):
        return [strip_dashes(x) for x in obj]
    if isinstance(obj, dict):
        return {k: strip_dashes(v) for k, v in obj.items()}
    return obj


# Curated per-country context (option B) lets the event safeguards run on modern
# states; and the safeguard→case lineage (which case produced each safeguard, and why).
COUNTRY_CONTEXT = _load_json(_SRC / "country_context.json", {})
DERIVATIONS = _load_json(_SRC / "safeguard_derivations.json", {})

# Board order: the two always-evaluable structural gates first (J durability, E rentier),
# then the seven condition/event safeguards. Mod4 is comparison-scoped (lives on /compare);
# Mod8 is a standing framing note, surfaced separately.
SAFEGUARD_ORDER = ["J", "E", "A", "B", "C", "D", "F", "G", "I"]
_J_STATUS = {"flagged": "firing", "borderline": "borderline", "clear": "clear"}


def build_safeguard_board(sg_raw, in_table):
    """Turn the raw safeguard evaluations into display tiles with an honest status:
    firing / borderline / clear / not_assessed. J and E are always evaluable (pillars +
    panel rents); the condition safeguards read 'not_assessed' unless the country is in the
    curated context table, so we never assert a false 'clear'. Each tile carries the case
    that derived it (from safeguard_derivations.json)."""
    board = []
    for key in SAFEGUARD_ORDER:
        r = sg_raw.get(key, {})
        triggered = bool(r.get("triggered", False))
        if key == "J":
            status = _J_STATUS.get(r.get("status"), "clear")
            headline = f"income-institutions gap {r.get('gap', 0):+.2f} · {r.get('status', '')}"
        elif key == "E":
            status = "firing" if triggered else "clear"
            headline = r.get("tier") or "below 15% of GDP · no penalty"
        else:
            status = "firing" if triggered else ("clear" if in_table else "not_assessed")
            headline = {"firing": "condition present", "clear": "no such condition",
                        "not_assessed": "needs curated input"}[status]
        der = DERIVATIONS.get(key, {})
        detail = _pillar_names_in((r.get("explanation") or "").replace("\u2014", ",")).strip()
        board.append({
            "key": key, "name": r.get("name") or der.get("name", key),
            "status": status, "triggered": triggered, "headline": headline,
            "detail": detail, "modification": r.get("modification"),
            "tier": r.get("tier"), "origin_cases": der.get("origin_cases", []),
            "why": der.get("why"), "validated_by": der.get("validated_by", []),
        })
    return board


def build_context(iso, name, ind):
    """Assemble the engine context for one country: curated flags + panel-derived resource
    rents (so E fires from panel data) + a ~10y-prior pillar vector (for movement + the J
    convergence qualifier). Returns (context, in_table, prior_pillars)."""
    ctx = dict(COUNTRY_CONTEXT.get(iso, {}))
    in_table = iso in COUNTRY_CONTEXT
    if ind.get("resource_rents_pct_gdp") is not None:
        ctx.setdefault("resource_rents_pct_gdp", ind.get("resource_rents_pct_gdp"))
    prior_ind = indicators_for(iso, PRIOR_YEAR) or indicators_for(name, PRIOR_YEAR)
    prior_pillars = None
    if prior_ind:
        ps = score_country(prior_ind, event_year=PRIOR_YEAR)
        pp = ps.get("pillar_scores", {})
        if ps.get("mi_score") is not None and all(pp.get(p) is not None for p in PILLARS_L):
            prior_pillars = {p: round(pp[p], 3) for p in PILLARS_L}
            ctx.setdefault("prior_pillars", prior_pillars)
    return ctx, in_table, prior_pillars


def chips_for(ind, band, residual, spread, weakest, present):
    chips = [{"key": "score_band", "label": f"Band {band}: {SCORE_BAND_LABEL.get(band,'')}",
              "valence": "good" if band <= 2 else "warn" if band == 3 else "bad",
              "why": "MI v3.3 score band based on five equally weighted pillars.",
              "rule": "The MI score is grouped into five public score bands."}]
    if present < 5:
        chips.append({"key": "partial", "label": f"Partial data · {present}/5 pillars", "valence": "neutral",
                      "why": ("Scored on the pillars we have data for. Its score is not directly comparable "
                              "to a fully-measured country - the missing pillars are unmeasured, not zero."),
                      "rule": f"{5 - present} of 5 pillars lack public data."})
    if residual is not None:
        granted = residual < -0.03
        chips.append({"key": "durability", "label": "Granted prosperity" if granted else "Earned prosperity",
                      "valence": "bad" if granted else "good",
                      "why": ("Wealth has outrun institutions - historically fragile." if granted
                              else "Institutions roughly match or exceed what income predicts - durable."),
                      "rule": "MI residual vs. the log-GDP regression (the durability gap): below -0.03 → granted, "
                              "otherwise earned (a ±0.03 tolerance treats near-zero gaps as in-line)."})
    if spread is not None:
        shape = "Balanced" if spread < 0.15 else "Some imbalance" if spread < 0.35 else "Lopsided"
        chips.append({"key": "shape", "label": f"{shape} · weakest: {PILLAR_NAMES.get(weakest, weakest)}",
                      "valence": "good" if spread < 0.15 else "warn" if spread < 0.35 else "bad",
                      "why": "Spread between the strongest and weakest pillar - the country's structural shape.",
                      "rule": "max(pillar) - min(pillar)."})
    rents = ind.get("resource_rents_pct_gdp")
    if rents is not None and rents >= 10:
        chips.append({"key": "resource", "label": "Resource-dependent", "valence": "warn",
                      "why": f"Resource rents ≈ {rents:.0f}% of GDP - prosperity leans on extraction.",
                      "rule": "resource rents ≥ 10% of GDP."})
    oda = ind.get("oda_pct_gni")
    if oda is not None and oda >= 5:
        chips.append({"key": "aid", "label": "Aid-dependent", "valence": "warn",
                      "why": f"Official aid ≈ {oda:.0f}% of GNI.", "rule": "ODA ≥ 5% of GNI."})
    return chips


def _pillar_names_in(text):
    """Replace raw pillar codes (P1..P5, P1/P2) with friendly names in engine text."""
    text = text.replace("P1/P2", "Institutions and Economic Complexity")
    for code, name in PILLAR_NAMES.items():
        text = text.replace(code, name)
    return text


def build_checks(pillars, mi, ind, weakest, residual):
    """The deterministic diagnostic checks the engine runs on every country - the
    'rules firing' you see in a case study, computed from the pillars alone."""
    checks = []

    # 1. Durability gate (is prosperity earned or granted? - the residual vs log-GDP, same as the chip)
    if residual is not None:
        if residual < -0.03:
            status, detail = "flag", ("This country's prosperity has outrun its institutions. Income the "
                                      "institutions cannot anchor is the classic fragility signal - historically it "
                                      "tends not to last.")
        elif residual > 0.03:
            status, detail = "clear", ("Institutions match or exceed what the country's income would predict. "
                                       "Prosperity here looks earned, and durable.")
        else:
            status, detail = "clear", "Prosperity sits roughly in line with institutions. No durability warning here."
        checks.append({"key": "durability", "title": "Durability gate", "status": status,
                       "headline": f"earned-vs-granted {residual:+.2f}", "detail": detail})

    # 2. Configuration (the shape of a failure, when there is one)
    bf = below_floor_diagnostic(pillars, mi)
    if bf and bf.get("reading"):
        detail = (bf.get("reading", "") + " " + bf.get("prescription", "")).replace("\u2014", ",").replace("*", "").strip()
        detail = _pillar_names_in(detail)
        checks.append({"key": "config", "title": "Configuration", "status": "flag",
                       "headline": bf.get("configuration", "").replace("_", " "), "detail": detail})

    # 3. Weakest link
    if weakest:
        nm = PILLAR_NAMES.get(weakest, weakest)
        checks.append({"key": "weak", "title": "Weakest link", "status": "info",
                       "headline": f"{nm} is lowest",
                       "detail": f"{nm} is the pillar dragging the score down. A chain breaks at its weakest link, "
                                 "so this is where the structural risk concentrates."})

    # 4. Room to rise (low-base eligibility)
    ap = ascent_potential(pillars)
    if ap:
        if ap.get("low_base"):
            checks.append({"key": "ascent", "title": "Room to rise", "status": "info", "headline": "low base",
                           "detail": "Starting from a low institutional base, the country is structurally eligible "
                                     "to climb. This is eligibility, not a forecast - the effect only showed up "
                                     "strongly in the 2000s global growth wave."})
        else:
            checks.append({"key": "ascent", "title": "Room to rise", "status": "info", "headline": "already high",
                           "detail": "The base is already high, so large structural jumps from here are historically rare."})

    # 5. Rentier check (prosperity leaning on extraction)
    rents = ind.get("resource_rents_pct_gdp")
    if rents is not None and rents >= 10:
        weak_inst = (pillars.get("P1") or 1.0) < 0.55
        detail = ("A large share of prosperity comes from extracting resources rather than from strong "
                  "institutions or a complex economy. Historically this masks structural weakness - the money "
                  "can vanish with a price swing." if weak_inst else
                  "A meaningful share of income comes from resource extraction. The institutions here are solid, "
                  "but resource dependence is still a source of volatility.")
        checks.append({"key": "rentier", "title": "Rentier check", "status": "flag" if weak_inst else "info",
                       "headline": f"resource rents ~{rents:.0f}% of GDP", "detail": detail})
    return checks


def verdict(band, residual, spread, weakest):
    parts = [{1: "Highly modernized", 2: "Structurally durable", 3: "Mixed structural profile",
              4: "Structurally fragile", 5: "At the structural floor"}.get(band, "")]
    if residual is not None:
        parts.append("prosperity outrunning institutions" if residual < -0.03
                     else "prosperity matched by institutions" if residual > 0.03
                     else "prosperity roughly in line with institutions")
    if spread is not None and spread >= 0.35:
        parts.append(f"lopsided ({PILLAR_NAMES.get(weakest, weakest).lower()} the weak point)")
    return " - ".join(p for p in parts if p) + "."


def fit_durability(points):
    """OLS MI ~ a + b*ln(gdp) across all scored countries -> residual per country."""
    xs = [math.log(g) for _, m, g in points if g and g > 0]
    ys = [m for _, m, g in points if g and g > 0]
    n = len(xs)
    if n < 5:
        return {}
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx if sxx else 0
    a = my - b * mx
    out = {}
    for iso, m, g in points:
        if g and g > 0:
            out[iso] = m - (a + b * math.log(g))
    return out


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "country").mkdir(exist_ok=True)
    for stale in (OUT / "country").glob("*.json"):  # avoid orphaned files from renamed slugs
        stale.unlink()
    scored = []  # (iso, name, ind, pillars, mi, score band, source)
    points = []
    for iso, name, _display, ind, source in iter_universe(YEAR):  # canonical panel (sorted, deterministic)
        if not ind:
            continue
        s = score_country(ind, event_year=YEAR)
        mi = s["mi_score"]
        if mi is None:
            continue
        pillars = s["pillar_scores"]
        scored.append((iso, name, ind, pillars, mi, get_score_band(mi)["band"], source, s))
        points.append((iso, mi, ind.get("gdp_per_capita_ppp")))

    residuals = fit_durability(points)

    summaries = []
    records = []                                   # (slug, full), written after the flagged tally
    firing_tally = {k: 0 for k in SAFEGUARD_ORDER}  # how many countries each safeguard fires on
    for iso, name, ind, pillars, mi, band, source, s in scored:
        spread = calculate_pillar_spread(pillars)
        config = get_configuration_profile(pillars)
        weakest = config[-1][0] if config else None
        residual = residuals.get(iso)
        present = [p for p in PILLARS_L if pillars.get(p) is not None]
        missing = [p for p in PILLARS_L if pillars.get(p) is None]
        chips = chips_for(ind, band, residual, spread, weakest, len(present))
        display = DISPLAY_FIX.get(name, name)  # readable name for the site; `name` stays the data key
        slug = slugify(display)
        summary = {
            "slug": slug, "name": display, "iso3": iso, "mi": round(mi, 3),
            "band": band, "tier": band,
            "pillars": {p: (round(pillars[p], 3) if pillars.get(p) is not None else None)
                        for p in PILLARS_L},
            "chips": chips, "coverage": {"present": len(present), "total": 5, "missing": missing},
        }
        summaries.append(summary)
        indicators = [{"key": k, "value": v, "source": INDICATOR_SOURCES.get(k, "-")}
                      for k, v in ind.items()
                      if not (k.endswith("_min") or k.endswith("_max")) and v is not None]

        # The full engine surface: safeguard board + diagnostics (previously computed then dropped).
        ctx, in_table, prior_pillars = build_context(iso, name, ind)
        sg_raw = evaluate_all_safeguards(s, ctx)
        board = build_safeguard_board(sg_raw, in_table)
        for t in board:
            if t["status"] == "firing":
                firing_tally[t["key"]] += 1
        diagnostics = {
            "context_curated": in_table,
            "strategy": classify_strategy(s, ctx),
            "vulnerability": assess_vulnerability(s, sg_raw),
            "movement": movement_quality(pillars, prior_pillars) if prior_pillars else None,
            "accountability_gap": accountability_gap(ind.get("voice_accountability"), pillars),
            "sensitivity": s.get("sensitivity"),
            "prior_year": PRIOR_YEAR if prior_pillars else None,
        }

        full = dict(summary)
        full.update({
            "verdict": verdict(band, residual, spread, weakest),
            "spread": round(spread, 3) if spread is not None else None,
            "residual": round(residual, 3) if residual is not None else None,
            "config": [[p, round(v, 3)] for p, v in config],
            "pillar_names": PILLAR_NAMES, "indicators": indicators, "data_year": YEAR,
            "source_tier": source, "checks": build_checks(pillars, mi, ind, weakest, residual),
            "safeguards": board, "diagnostics": diagnostics,
        })
        records.append((slug, full))

    # inject "how many countries share this" onto each firing tile, then write (deterministic).
    for slug, full in records:
        for t in full["safeguards"]:
            t["share_firing"] = firing_tally.get(t["key"], 0)
        json.dump(strip_dashes(full), open(OUT / "country" / f"{slug}.json", "w"), indent=1)

    # full-coverage countries first (comparable), then partial - each by MI desc.
    # slug is the stable tiebreak so equal-MI countries (e.g. Denmark/Ireland) have
    # a deterministic order run-to-run.
    summaries.sort(key=lambda r: r["slug"])
    summaries.sort(key=lambda r: (r["coverage"]["present"] == 5, r["mi"]), reverse=True)
    json.dump(strip_dashes(summaries), open(OUT / "countries.json", "w"), indent=1)
    json.dump({"built": date.today().isoformat(), "count": len(summaries), "engine": "MI v3.3",
               "weighting": "equal", "score_classification": "five score bands",
               "data_vintage": "WGI 2025-anchored", "world_states": 195,
               "context_countries": len(COUNTRY_CONTEXT),
               "note": "Generated by the deterministic mi-research engine over all available public data. "
                       "Each country carries the full safeguard board plus diagnostics for strategy, "
                       "vulnerability, movement, and sensitivity. Countries with partial data show fewer "
                       "pillars, and safeguards needing curated context read 'not assessed'. Gaps are "
                       "shown, never filled with invented values."},
              open(OUT / "meta.json", "w"), indent=1)
    full5 = sum(1 for s in summaries if s["coverage"]["present"] == 5)
    print(f"Wrote {len(summaries)} countries ({full5} with all 5 pillars) -> {OUT}")


if __name__ == "__main__":
    build()
