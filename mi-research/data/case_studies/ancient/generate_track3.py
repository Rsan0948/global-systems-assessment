#!/usr/bin/env python3
"""Generate Track 3 ancient_cases.json with deterministic proxy-indicator scoring.

Each case gets 14 indicators across 2 timepoints (peak, pre_stress).
Pillar scores = mean of constituent indicators.
MI = 0.34*P1 + 0.15*P2 + 0.16*P3 + 0.20*P4 + 0.16*P5

Period normalization:
  P3a life expectancy: (LE - 20) / (40 - 20)  ceiling=40
  P4a GDP/cap:         (ln(GDP) - ln(400)) / (ln(2000) - ln(400))  GK$
  P3c urbanization:    min(urban_rate / 0.25, 1.0)
"""
import json, math, sys
from pathlib import Path

WEIGHTS = {"P1": 0.34, "P2": 0.15, "P3": 0.16, "P4": 0.20, "P5": 0.16}

def mean(vals):
    return round(sum(vals) / len(vals), 2)

def mi(pillars):
    total_w = sum(WEIGHTS[p] for p in WEIGHTS if p in pillars)
    return round(sum(pillars[p] * WEIGHTS[p] for p in WEIGHTS if p in pillars) / total_w, 3)

def build_timepoint(indicators_by_pillar):
    """indicators_by_pillar: dict of P1..P5 -> dict of indicator_key -> {value, source, justification, confidence}"""
    result = {}
    for p in ["P1", "P2", "P3", "P4", "P5"]:
        inds = indicators_by_pillar[p]
        vals = [v["value"] for v in inds.values()]
        result[p] = {"score": mean(vals), "indicators": inds}
    pillar_scores = {p: result[p]["score"] for p in ["P1", "P2", "P3", "P4", "P5"]}
    result["MI"] = mi(pillar_scores)
    return result

def ind(value, source, justification, confidence="MODERATE"):
    return {"value": round(value, 2), "source": source, "justification": justification, "confidence": confidence}

# ── GDP helper (period-normalized) ──
def gdp_norm(gdp_gk):
    if gdp_gk <= 400: return 0.0
    if gdp_gk >= 2000: return 1.0
    return round((math.log(gdp_gk) - math.log(400)) / (math.log(2000) - math.log(400)), 2)

# ── Life expectancy helper (period-normalized) ──
def le_norm(le):
    return round(max(0, min(1, (le - 20) / (40 - 20))), 2)

# ── Urbanization helper ──
def urb_norm(rate):
    return round(min(rate / 0.25, 1.0), 2)

# ═══════════════════════════════════════════════════════════════
# CASE DATA — 25 cases, each with peak and pre_stress indicators
# ═══════════════════════════════════════════════════════════════

CASES = []

# ─── 1. Old Kingdom Egypt ───
CASES.append({
    "name": "Old Kingdom Egypt",
    "metadata": {"stress_type": "ancient_proxy", "region": "Egypt", "data_quality": "RICH",
                 "shock": "mixed", "outcome": "rupture", "fragment_count": 2},
    "tags": ["container_erosion", "frag2-4"],
    "peak_period": "c. 2686–2181 BCE (Dynasties III–VI)",
    "pre_stress_period": "c. 2200–2181 BCE (late Dynasty VI)",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(0.50, "Kemp 2006, Ancient Egypt: Anatomy of a Civilization", "Vizier-nome system: 3+ tiers (king-vizier-nomarch-local), but delegation informal", "HIGH"),
            "P1b_legal_formal": ind(0.50, "Jasnow 2003, 'Egypt: Old Kingdom' in History of Ancient Near Eastern Law", "Royal decrees (Koptos decrees) show formal exemptions; no surviving code but systematic dispute resolution", "MODERATE"),
            "P1c_bureaucratic": ind(0.25, "Strudwick 1985, The Administration of Egypt in the Old Kingdom", "Hereditary offices common; scribal class exists but no exam/merit entry", "HIGH"),
            "P1d_fiscal_std": ind(0.50, "Lehner 2015, 'Labor and the Pyramids' in Ancient Egyptian Administration", "Biennial cattle-count tax; corvée labor system organized by phyles; standardized grain accounting", "HIGH"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.40, "Nicholson & Shaw (eds.) 2000, Ancient Egyptian Materials and Technology", "Pyramid construction, copper metallurgy, papyrus — diffusion mainly court-centered", "HIGH"),
            "P2b_knowledge_inst": ind(0.50, "Baines & Eyre 1983, 'Four Notes on Literacy' in Göttinger Miszellen", "House of Life scribal schools; literacy ~1% but concentrated functional class", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(30), "Scheidel 2001, Death on the Nile", "LE at birth ~28-32 yrs from skeletal/mortuary data", "MODERATE"),
            "P3b_elite_literacy": ind(0.15, "Baines & Eyre 1983", "~1% overall literacy; elite scribal caste only", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.05), "Bard 2015, Introduction to the Archaeology of Ancient Egypt", "Memphis ~30k; total urban fraction ~5%", "LOW"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(550), "Maddison 2007 (extrapolated); Scheidel & Friesen 2009", "Estimated ~$500-600 GK$ for Nile agrarian economy with monumental surplus", "LOW"),
            "P4b_trade_auton": ind(0.50, "Sowada 2009, Egypt in the Eastern Mediterranean during the Old Kingdom", "Significant Levantine/Nubian trade but not dependent; state-managed", "MODERATE"),
            "P4c_tribute_dep": ind(0.25, "Moreno García 2013, 'The Territorial Administration of the Kingdom' in AEA", "Nubian gold/resources significant; not fully autonomous of peripheral extraction", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.85, "Shaw (ed.) 2003, Oxford History of Ancient Egypt", "~500 years of continuous dynastic rule (III–VI); longest unified stretch in antiquity", "HIGH"),
            "P5b_succession": ind(0.75, "Dodson & Hilton 2004, The Complete Royal Families of Ancient Egypt", "Generally orderly father-son succession with occasional branching; no systemic civil wars until end", "MODERATE"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(0.25, "Moreno García 2013", "Nomarchs increasingly autonomous; central authority nominal in Upper Egypt", "MODERATE"),
            "P1b_legal_formal": ind(0.25, "Jasnow 2003", "Royal writ ineffective beyond Memphis region; local customs supersede", "MODERATE"),
            "P1c_bureaucratic": ind(0.25, "Strudwick 1985", "Offices deeply hereditary; Pepi II's 94-yr reign ossified appointments", "MODERATE"),
            "P1d_fiscal_std": ind(0.25, "Kanawati 1980, Governmental Reforms in Old Kingdom Egypt", "Tax collection fragmented; nome-level retention rising", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.40, "Nicholson & Shaw 2000", "No significant technological regression yet", "MODERATE"),
            "P2b_knowledge_inst": ind(0.50, "Baines & Eyre 1983", "Provincial scribal traditions continuing", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(28), "Scheidel 2001", "Possible slight decline from 4.2ka drought stress", "LOW"),
            "P3b_elite_literacy": ind(0.15, "Baines & Eyre 1983", "No major change in literacy rates", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.04), "Bard 2015", "Slight decline in Memphis centrality", "LOW"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(500), "Maddison 2007 (extrapolated)", "Agricultural output declining with Nile low-floods", "LOW"),
            "P4b_trade_auton": ind(0.50, "Sowada 2009", "Trade continuing but state share declining", "MODERATE"),
            "P4c_tribute_dep": ind(0.25, "Moreno García 2013", "Nubian extraction disrupted", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.85, "Shaw 2003", "Dynasty still nominally intact", "HIGH"),
            "P5b_succession": ind(0.25, "Dodson & Hilton 2004", "Pepi II's extreme reign created contested succession; ephemeral Dynasty VII/VIII", "MODERATE"),
        },
    },
})

# ─── 2. Achaemenid Persia ───
CASES.append({
    "name": "Achaemenid Persia",
    "metadata": {"stress_type": "ancient_proxy", "region": "NearEast", "data_quality": "RICH",
                 "shock": "exo", "outcome": "rupture", "fragment_count": "many"},
    "tags": ["P1ord_exo_conquest", "porosity"],
    "peak_period": "c. 522–465 BCE (Darius I – Xerxes I)",
    "pre_stress_period": "c. 340–330 BCE (Darius III)",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(0.75, "Briant 2002, From Cyrus to Alexander", "King-satrap-sub-governor-local: 4+ tiers; 20+ satrapies with sub-provinces", "HIGH"),
            "P1b_legal_formal": ind(0.50, "Briant 2002; Dandamayev 1996 in AchHist IX", "Royal law (data) coexisted with local legal traditions; Bisitun inscription codifies legitimacy norms", "MODERATE"),
            "P1c_bureaucratic": ind(0.50, "Briant 2002; Hallock 1969, Persepolis Fortification Tablets", "Persepolis tablets show systematic accounting; satrapal appointments by king but heritability crept in", "HIGH"),
            "P1d_fiscal_std": ind(0.75, "Briant 2002; Herodotus III.89–97", "Darius's fixed tribute assessments by satrapy; standardized daric coinage", "HIGH"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.60, "Briant 2002; Potts 2014, Nomadism in Iran", "Royal Road postal system (angareion); qanat irrigation diffusion; adopted technologies across empire", "HIGH"),
            "P2b_knowledge_inst": ind(0.50, "Kuhrt 2007, The Persian Empire", "Multilingual administration (Elamite, Aramaic, OP); absorbed Babylonian astronomical traditions", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(30), "Scheidel 2007, 'Demography' in Scheidel et al. Cambridge Economic History", "Estimated ~28-32 yrs; comparable to Mediterranean norms", "LOW"),
            "P3b_elite_literacy": ind(0.30, "Briant 2002", "Multilingual scribal classes in Babylon, Susa, Persepolis; broader than Egypt but still elite", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.10), "Aperghis 2004, The Seleukid Royal Economy", "Babylon ~150k, Susa ~50k, Persepolis complex; ~8-12% urban", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(600), "Scheidel 2009 (adapted); Aperghis 2004", "Diverse economy: irrigated agriculture + pastoralism + trade; ~$550-650 GK$", "LOW"),
            "P4b_trade_auton": ind(0.75, "Briant 2002", "Empire spanned trade routes; largely self-sufficient in basic goods; Royal Road facilitated internal trade", "MODERATE"),
            "P4c_tribute_dep": ind(0.75, "Briant 2002; Herodotus III.89–97", "Tribute important but spread across 20+ satrapies; no single-source dependency", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.90, "Briant 2002", "~200 years of continuous Achaemenid rule; longest Near Eastern imperial dynasty of its era", "HIGH"),
            "P5b_succession": ind(0.50, "Briant 2002", "Several succession crises (Bardiya, Xerxes assassination) but dynasty survived each", "HIGH"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(0.75, "Briant 2002", "Formal structure intact but effective control weakened in western satrapies", "MODERATE"),
            "P1b_legal_formal": ind(0.50, "Briant 2002", "Legal norms unchanged in principle", "MODERATE"),
            "P1c_bureaucratic": ind(0.25, "Briant 2002", "Satrapal revolts (360s); appointments increasingly hereditary/autonomous", "MODERATE"),
            "P1d_fiscal_std": ind(0.50, "Briant 2002", "Tribute system still nominal but collection irregular from rebellious satrapies", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Briant 2002", "Infrastructure maintained but no new major innovations", "MODERATE"),
            "P2b_knowledge_inst": ind(0.50, "Kuhrt 2007", "Scribal traditions continuing", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(30), "Scheidel 2007", "No evidence of demographic decline", "LOW"),
            "P3b_elite_literacy": ind(0.30, "Briant 2002", "Unchanged", "LOW"),
            "P3c_urbanization": ind(urb_norm(0.10), "Aperghis 2004", "Babylon still major center", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(600), "Scheidel 2009 (adapted)", "Economy stable at aggregate level", "LOW"),
            "P4b_trade_auton": ind(0.75, "Briant 2002", "Trade routes still functioning", "MODERATE"),
            "P4c_tribute_dep": ind(0.50, "Briant 2002", "Western satrapies defaulting more frequently", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.90, "Briant 2002", "Dynasty continuous, still >200yr track record", "HIGH"),
            "P5b_succession": ind(0.50, "Briant 2002", "Artaxerxes III seized throne by force; Darius III a late compromise candidate", "HIGH"),
        },
    },
})

# ─── 3. Sasanian Persia ───
CASES.append({
    "name": "Sasanian Persia",
    "metadata": {"stress_type": "ancient_proxy", "region": "NearEast", "data_quality": "RICH",
                 "shock": "exo+confed", "outcome": "rupture", "fragment_count": "many"},
    "tags": ["P1ord_challenge", "confederacy", "container_erosion", "suppression"],
    "peak_period": "c. 498–579 CE (Kavad I – Khosrow I)",
    "pre_stress_period": "c. 628–651 CE (post-Khosrow II)",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(0.75, "Daryaee 2009, Sasanian Persia", "King-of-kings → marzbāns → provincial governors; systematic 4-tier hierarchy", "HIGH"),
            "P1b_legal_formal": ind(0.75, "Perikhanian 1997, The Book of a Thousand Judgements", "Mādayān ī Hazār Dādestān: elaborate codified civil law; Zoroastrian legal tribunals", "HIGH"),
            "P1c_bureaucratic": ind(0.75, "Wiesehöfer 2001, Ancient Persia", "Khosrow I's tax reforms created salaried dehqān officials; merit-adjacent recruitment", "MODERATE"),
            "P1d_fiscal_std": ind(0.75, "Rubin 1995 in Cambridge History of Iran III", "Khosrow I's fixed land-tax assessment (kharāg); standardized coinage", "HIGH"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Daryaee 2009", "Irrigation (qanats), silk weaving adopted from China, Jundishapur academy", "MODERATE"),
            "P2b_knowledge_inst": ind(0.75, "Daryaee 2009; Gutas 1998, Greek Thought, Arabic Culture", "Academy of Gondēshāpur: medicine, philosophy, astronomy; translation movement", "HIGH"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(30), "Scheidel 2007", "Comparable to late-antique Mediterranean norms", "LOW"),
            "P3b_elite_literacy": ind(0.30, "Daryaee 2009", "Zoroastrian priestly + scribal literacy; Pahlavi script; broader than Achaemenid period", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.12), "Daryaee 2009; Whitcomb 1985", "Ctesiphon ~500k (one of world's largest); several cities >50k", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(700), "Scheidel 2009 (adapted)", "Silk Road revenues + irrigated agriculture; wealthier than most contemporaries", "LOW"),
            "P4b_trade_auton": ind(0.75, "Daryaee 2009", "Controlled key Silk Road segments; Persian Gulf trade; diversified", "MODERATE"),
            "P4c_tribute_dep": ind(0.75, "Rubin 1995", "Land tax base diversified across provinces; not dependent on single source", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.85, "Daryaee 2009", "~400 years of Sasanian dynasty by Khosrow I's era", "HIGH"),
            "P5b_succession": ind(0.50, "Daryaee 2009", "Frequent contested successions but dynasty always survived; Mazdakite crisis overcome", "MODERATE"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(0.50, "Daryaee 2009; Howard-Johnston 2010, Witnesses to a World Crisis", "Formal structure intact but Byzantine wars exhausted administrative capacity", "MODERATE"),
            "P1b_legal_formal": ind(0.50, "Perikhanian 1997", "Legal system still operative but state enforcement weakened", "MODERATE"),
            "P1c_bureaucratic": ind(0.25, "Howard-Johnston 2010", "Military commanders (spāhbed) became regional warlords; central appointments failed", "MODERATE"),
            "P1d_fiscal_std": ind(0.25, "Howard-Johnston 2010", "Tax base devastated by Byzantine war + plague; provinces retaining revenues", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Daryaee 2009", "Knowledge institutions still functioning", "MODERATE"),
            "P2b_knowledge_inst": ind(0.50, "Gutas 1998", "Gondēshāpur survived; later transmitted to Abbasids", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(25), "Scheidel 2007; Little (ed.) 2007, Plague and the End of Antiquity", "Justinianic Plague + prolonged warfare likely reduced LE", "LOW"),
            "P3b_elite_literacy": ind(0.25, "Daryaee 2009", "Disruption of scribal training in civil wars", "LOW"),
            "P3c_urbanization": ind(urb_norm(0.08), "Whitcomb 1985", "Ctesiphon sacked repeatedly; urban decline", "LOW"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(500), "Scheidel 2009 (adapted)", "Economy devastated by 26-year Byzantine war; plague; infrastructure damage", "LOW"),
            "P4b_trade_auton": ind(0.50, "Daryaee 2009", "Silk Road trade disrupted but not eliminated", "LOW"),
            "P4c_tribute_dep": ind(0.25, "Howard-Johnston 2010", "Provinces effectively autonomous; tribute collection collapsed", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.25, "Howard-Johnston 2010", "12 kings in 4 years (628–632); dynasty effectively ended", "HIGH"),
            "P5b_succession": ind(0.00, "Daryaee 2009", "Complete succession collapse; regicide became norm; Yazdegerd III a child puppet", "HIGH"),
        },
    },
})

# ─── 4. Mauryan Empire ───
CASES.append({
    "name": "Mauryan Empire",
    "metadata": {"stress_type": "ancient_proxy", "region": "SouthAsia", "data_quality": "RICH",
                 "shock": "endo", "outcome": "rupture", "fragment_count": "many"},
    "tags": ["P4P1gap", "ruler_dependence", "container_erosion"],
    "peak_period": "c. 268–232 BCE (Ashoka)",
    "pre_stress_period": "c. 200–185 BCE (late Maurya)",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(0.75, "Thapar 2003, Early India; Olivelle 2013, King, Governance, and Law in Ancient India", "Arthashastra model: king-mahamatras-pradeshikas-village heads; ~4 tiers", "HIGH"),
            "P1b_legal_formal": ind(0.50, "Olivelle 2013", "Ashoka's dhamma edicts as quasi-legal norms; Arthashastra describes courts but actual implementation debated", "MODERATE"),
            "P1c_bureaucratic": ind(0.50, "Thapar 2003", "Mahamatras (superintendents) appointed, not hereditary under Ashoka; but no formal exam system", "MODERATE"),
            "P1d_fiscal_std": ind(0.50, "Thapar 2003; Arthashastra II.6", "Land revenue ~1/6 of produce; standardized punch-marked coinage; but collection varied by region", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.40, "Thapar 2003; Allchin & Allchin 1982", "Iron technology, NBPW pottery spread; Ashokan pillar engineering; but limited beyond court", "MODERATE"),
            "P2b_knowledge_inst": ind(0.50, "Thapar 2003", "Buddhist monasteries as proto-universities (Taxila); Brahmanical learning centers", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(28), "Scheidel 2007", "South Asian pre-modern norms ~25-30 yrs", "LOW"),
            "P3b_elite_literacy": ind(0.20, "Falk 1993, Schrift im alten Indien; Salomon 1998", "Brahmi/Kharosthi scripts established; literacy concentrated among monks, scribes, merchants", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.08), "Allchin & Allchin 1982; Erdosy 1988", "Pataliputra ~150-300k; several cities >20k; ~6-10% urban", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(550), "Maddison 2007 (India extrapolation)", "Rich Gangetic agriculture + expanding trade; ~$500-600 GK$", "LOW"),
            "P4b_trade_auton": ind(0.50, "Thapar 2003", "Significant internal + external trade but state economy agriculture-dominant", "MODERATE"),
            "P4c_tribute_dep": ind(0.50, "Thapar 2003", "Peripheral regions (Kalinga, Deccan) contributed tribute; some single-source risk", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.50, "Thapar 2003", "Dynasty ~50 years old at Ashoka's peak; relatively new", "HIGH"),
            "P5b_succession": ind(0.50, "Thapar 2003; Lahiri 2015", "Ashoka's own accession reportedly contested; Buddhist legends of fratricidal succession", "MODERATE"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(0.25, "Thapar 2003", "Post-Ashoka rulers controlled only Magadha core; periphery independent", "MODERATE"),
            "P1b_legal_formal": ind(0.25, "Olivelle 2013", "Dhamma edicts abandoned; local law reasserted", "MODERATE"),
            "P1c_bureaucratic": ind(0.25, "Thapar 2003", "Offices became hereditary; central appointments failed in provinces", "MODERATE"),
            "P1d_fiscal_std": ind(0.25, "Thapar 2003", "Revenue from shrunken territory only", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.40, "Allchin & Allchin 1982", "Technologies persisted regionally", "MODERATE"),
            "P2b_knowledge_inst": ind(0.50, "Thapar 2003", "Buddhist institutions continued independently of state", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(28), "Scheidel 2007", "No evidence of demographic change", "LOW"),
            "P3b_elite_literacy": ind(0.20, "Salomon 1998", "Unchanged", "LOW"),
            "P3c_urbanization": ind(urb_norm(0.07), "Erdosy 1988", "Pataliputra declining; successor cities emerging", "LOW"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(550), "Maddison 2007", "Regional economy stable; trade routes shifting", "LOW"),
            "P4b_trade_auton": ind(0.75, "Thapar 2003", "Indo-Greek/Central Asian trade expanding independently of Mauryan state", "MODERATE"),
            "P4c_tribute_dep": ind(0.25, "Thapar 2003", "Peripheral tribute lost; dependent on Gangetic core only", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.50, "Thapar 2003", "~140-year dynasty but weakening legitimacy", "MODERATE"),
            "P5b_succession": ind(0.25, "Thapar 2003", "Rapid turnover of late Mauryan kings; Brihadratha assassinated by general", "MODERATE"),
        },
    },
})

# ─── 5. Gupta Empire ───
CASES.append({
    "name": "Gupta Empire",
    "metadata": {"stress_type": "ancient_proxy", "region": "SouthAsia", "data_quality": "RICH",
                 "shock": "mixed", "outcome": "rupture", "fragment_count": "many"},
    "tags": ["golden_age", "P4P1gap", "container_erosion"],
    "peak_period": "c. 380–467 CE (Chandragupta II – Kumaragupta I)",
    "pre_stress_period": "c. 500–550 CE (post-Skandagupta)",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(0.50, "Majumdar & Altekar 1967, The Vakataka-Gupta Age", "King-governors (uparikas)-district heads (vishayapatis); ~3 tiers but feudal devolution", "MODERATE"),
            "P1b_legal_formal": ind(0.50, "Olivelle 2005, Manu's Code of Law; Lariviere 1989", "Dharmashastra tradition (Narada, Yajnavalkya) provided legal framework; royal courts adjudicated", "MODERATE"),
            "P1c_bureaucratic": ind(0.25, "Majumdar & Altekar 1967", "Officers (kumaramatyas) appointed but feudal subordinates held hereditary authority", "MODERATE"),
            "P1d_fiscal_std": ind(0.50, "Sharma 2001, Early Medieval Indian Society", "Land grants (copper-plate charters) show standardized revenue; but increasing feudal immunities", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.60, "Chattopadhyaya 1986, Astronomy, Science and Society in the Gupta Age", "Decimal numerals, Aryabhata's astronomy, Delhi iron pillar; significant court-patronized innovation", "HIGH"),
            "P2b_knowledge_inst": ind(0.75, "Mookerji 1951, Ancient Indian Education; Li 1996", "Nalanda established/expanded; Valabhi; systematic monastic education", "HIGH"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(28), "Scheidel 2007", "South Asian pre-modern norms ~25-30 yrs", "LOW"),
            "P3b_elite_literacy": ind(0.25, "Salomon 1998", "Sanskrit literary florescence; broader Brahmi literacy among merchants + monks", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.08), "Sharma 2001", "Multiple cities >20k; Pataliputra, Ujjain, Varanasi", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(600), "Maddison 2007 (India extrapolation)", "Agricultural prosperity + Indian Ocean trade; ~$550-650 GK$", "LOW"),
            "P4b_trade_auton": ind(0.75, "Ray 2003, Archaeology of Seafaring in Ancient South Asia", "Indian Ocean maritime trade; Roman gold imports; diversified", "MODERATE"),
            "P4c_tribute_dep": ind(0.50, "Majumdar & Altekar 1967", "Revenue from feudatories but increasingly granted away as land immunities", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.60, "Majumdar & Altekar 1967", "~150 years of effective Gupta rule at peak", "HIGH"),
            "P5b_succession": ind(0.75, "Majumdar & Altekar 1967", "Orderly succession through peak period (Chandragupta II → Kumaragupta I)", "MODERATE"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(0.25, "Sharma 2001", "Feudal devolution accelerated; provincial governors effectively independent", "MODERATE"),
            "P1b_legal_formal": ind(0.50, "Olivelle 2005", "Dharmashastra tradition continued independently of state", "MODERATE"),
            "P1c_bureaucratic": ind(0.25, "Sharma 2001", "Offices hereditary; land grants created autonomous power centers", "MODERATE"),
            "P1d_fiscal_std": ind(0.25, "Sharma 2001", "Revenue base shrinking as land grants proliferated", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.60, "Chattopadhyaya 1986", "Intellectual traditions continued at Nalanda independently", "MODERATE"),
            "P2b_knowledge_inst": ind(0.75, "Mookerji 1951", "Nalanda expanding; survived political fragmentation", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(28), "Scheidel 2007", "No major demographic disruption evidenced", "LOW"),
            "P3b_elite_literacy": ind(0.25, "Salomon 1998", "Sanskrit literary culture continuing", "LOW"),
            "P3c_urbanization": ind(urb_norm(0.06), "Sharma 2001", "Some urban decline as political centers shifted", "LOW"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(550), "Maddison 2007", "Economy still productive but trade disrupted by Hunas", "LOW"),
            "P4b_trade_auton": ind(0.75, "Ray 2003", "Indian Ocean trade continued; less state-directed", "MODERATE"),
            "P4c_tribute_dep": ind(0.25, "Sharma 2001", "Most feudatories no longer remitting tribute", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.50, "Majumdar & Altekar 1967", "Dynasty still nominally existing but >200 yrs diluted actual control", "MODERATE"),
            "P5b_succession": ind(0.25, "Majumdar & Altekar 1967", "Multiple competing Gupta claimants; succession no longer orderly", "MODERATE"),
        },
    },
})

# ─── 6. Vijayanagara ───
CASES.append({
    "name": "Vijayanagara",
    "metadata": {"stress_type": "ancient_proxy", "region": "SouthAsia", "data_quality": "RICH",
                 "shock": "exo", "outcome": "rupture", "fragment_count": "many"},
    "tags": ["suppression", "frag_engineered"],
    "peak_period": "c. 1509–1529 CE (Krishnadevaraya)",
    "pre_stress_period": "c. 1560–1565 CE (pre-Talikota)",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(0.50, "Stein 1989, Vijayanagara (New Cambridge History of India)", "King-governors (nayakas)-district; ~3 tiers but nayaka autonomy significant", "MODERATE"),
            "P1b_legal_formal": ind(0.50, "Stein 1989; Nilakanta Sastri 1966", "Dharmashastra courts + royal edicts; Portuguese observers noted functioning legal system", "MODERATE"),
            "P1c_bureaucratic": ind(0.25, "Stein 1989", "Nayaka system semi-feudal; military commanders held hereditary territories", "MODERATE"),
            "P1d_fiscal_std": ind(0.50, "Stein 1989; Karashima 2014", "Land revenue system well-documented in inscriptions; standardized under Krishnadevaraya", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Stein 1989; Verghese 2000", "Irrigation tanks, temple-based knowledge; imported firearms from Portuguese", "MODERATE"),
            "P2b_knowledge_inst": ind(0.50, "Stein 1989", "Temple complexes as educational centers; Telugu/Kannada literary patronage", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(28), "Scheidel 2007", "South Asian pre-modern norms", "LOW"),
            "P3b_elite_literacy": ind(0.25, "Stein 1989", "Telugu/Kannada/Sanskrit literary culture; merchant literacy in trade", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.08), "Fritz & Michell 2001, City of Victory: Vijayanagara", "Vijayanagara city ~250-500k; one of world's largest; regional towns significant", "HIGH"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(650), "Maddison 2007; Subrahmanyam 2012", "Prosperous mixed economy; Indian Ocean trade; diamond trade", "LOW"),
            "P4b_trade_auton": ind(0.75, "Subrahmanyam 2012, The Portuguese Empire in Asia", "Diverse trade: spices, textiles, diamonds; Portuguese partnership; not dependent on single route", "MODERATE"),
            "P4c_tribute_dep": ind(0.50, "Stein 1989", "Nayaka tribute system but retention rates increasing", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.60, "Stein 1989", "~200 years by Krishnadevaraya; but dynasty changes (Sangama→Saluva→Tuluva)", "MODERATE"),
            "P5b_succession": ind(0.50, "Stein 1989", "Dynasty changes managed without collapse; Krishnadevaraya's own succession orderly", "MODERATE"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(0.50, "Stein 1989", "Structure unchanged but nayaka autonomy growing", "MODERATE"),
            "P1b_legal_formal": ind(0.50, "Stein 1989", "Legal system continuing", "MODERATE"),
            "P1c_bureaucratic": ind(0.25, "Stein 1989", "Nayakas increasingly independent; Aliya Rama Raya a regent, not a king", "MODERATE"),
            "P1d_fiscal_std": ind(0.25, "Stein 1989", "Revenue retention by nayakas rising", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Stein 1989", "Technology stable", "MODERATE"),
            "P2b_knowledge_inst": ind(0.50, "Stein 1989", "Temple institutions continuing", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(28), "Scheidel 2007", "No evidence of change", "LOW"),
            "P3b_elite_literacy": ind(0.25, "Stein 1989", "Unchanged", "LOW"),
            "P3c_urbanization": ind(urb_norm(0.08), "Fritz & Michell 2001", "Capital still massive", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(650), "Maddison 2007", "Economy still prosperous", "LOW"),
            "P4b_trade_auton": ind(0.75, "Subrahmanyam 2012", "Trade continuing; Portuguese Goa active", "MODERATE"),
            "P4c_tribute_dep": ind(0.25, "Stein 1989", "Effective tribute declining as nayakas retained more", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.50, "Stein 1989", "Aliya Rama Raya ruled as regent; dynastic legitimacy contested", "MODERATE"),
            "P5b_succession": ind(0.25, "Stein 1989", "Rama Raya a usurper-regent; puppet kings; succession fragile", "MODERATE"),
        },
    },
})

# ─── 7. Tang Dynasty ───
CASES.append({
    "name": "Tang Dynasty",
    "metadata": {"stress_type": "ancient_proxy", "region": "EastAsia", "data_quality": "RICH",
                 "shock": "endo", "outcome": "rupture", "fragment_count": "many"},
    "tags": ["suppression", "container_erosion"],
    "peak_period": "c. 627–755 CE (Taizong → Xuanzong early)",
    "pre_stress_period": "c. 875–907 CE (Huang Chao → end)",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(1.00, "Lewis 2009, China's Cosmopolitan Empire: The Tang Dynasty", "Emperor-Three Departments-Six Ministries-prefectures-counties: 5+ tiers", "HIGH"),
            "P1b_legal_formal": ind(0.75, "Johnson 1979, The T'ang Code", "Tang Code (Tanglü shuyi): comprehensive criminal/civil law; one of history's most elaborate legal codes", "HIGH"),
            "P1c_bureaucratic": ind(1.00, "Elman 2000, A Cultural History of Civil Examinations in Late Imperial China", "Imperial examination system (keju) fully operational; merit-based selection for officials", "HIGH"),
            "P1d_fiscal_std": ind(0.75, "Twitchett 1963, Financial Administration Under the T'ang Dynasty", "Zu-yong-diao tax system; equal-field (juntian) land allocation; standardized grain levies", "HIGH"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.75, "Needham 1954–, Science and Civilisation in China", "Block printing, gunpowder precursors, porcelain, canal locks; diffusion via Silk Road", "HIGH"),
            "P2b_knowledge_inst": ind(0.75, "Lewis 2009", "Imperial academy (Guozijian); Buddhist monasteries as knowledge centers; extensive libraries", "HIGH"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(30), "Scheidel 2007", "Estimated ~28-32 yrs for Tang-era China", "LOW"),
            "P3b_elite_literacy": ind(0.40, "Lewis 2009", "Examination system drove literacy among gentry class; Buddhist spread broadened further", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.10), "Chandler 1987, Four Thousand Years of Urban Growth", "Chang'an ~1M; Luoyang ~500k; many cities >50k; ~8-12% urban", "HIGH"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(800), "Maddison 2007", "Estimated ~$700-900 GK$ for early Tang; prosperous agrarian-commercial economy", "LOW"),
            "P4b_trade_auton": ind(0.75, "Lewis 2009; de la Vaissière 2005", "Silk Road apex; maritime trade growing; diversified exports", "MODERATE"),
            "P4c_tribute_dep": ind(0.75, "Twitchett 1963", "Land tax system broadly based; not dependent on single revenue source", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.60, "Lewis 2009", "~130 years of stable rule by mid-Tang; dynasty ~150 yrs old by An Lushan", "HIGH"),
            "P5b_succession": ind(0.75, "Lewis 2009", "Generally orderly imperial succession to mid-8th century; Wu Zetian era unusual but non-fatal", "MODERATE"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(0.50, "Lewis 2009", "Jiedushi (military governors) controlled provinces; central authority nominal beyond capital", "HIGH"),
            "P1b_legal_formal": ind(0.50, "Johnson 1979", "Tang Code technically in force but local strongmen administered justice", "MODERATE"),
            "P1c_bureaucratic": ind(0.50, "Elman 2000", "Examination system continued but appointments overridden by military patrons", "MODERATE"),
            "P1d_fiscal_std": ind(0.25, "Twitchett 1963", "Two-tax system (liangshui) nominally standardized but jiedushi retained revenues", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.75, "Needham 1954–", "Technologies continued to spread; woodblock printing expanding", "MODERATE"),
            "P2b_knowledge_inst": ind(0.50, "Lewis 2009", "Institutions weakened by Huang Chao destruction but Buddhist networks survived", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(25), "Scheidel 2007", "Huang Chao rebellion caused massive mortality; An Lushan earlier killed millions", "LOW"),
            "P3b_elite_literacy": ind(0.35, "Lewis 2009", "Some decline from peak but literate class persisted", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.07), "Chandler 1987", "Chang'an sacked; urban population declined", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(600), "Maddison 2007", "Economic decline from rebellions and disruption", "LOW"),
            "P4b_trade_auton": ind(0.50, "Lewis 2009", "Silk Road disrupted; maritime trade shifting south", "MODERATE"),
            "P4c_tribute_dep": ind(0.25, "Twitchett 1963", "Most provinces retained all revenues; center dependent on Jiangnan remittances", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.50, "Lewis 2009", "Dynasty still nominally intact but >250 years old; legitimacy exhausted", "MODERATE"),
            "P5b_succession": ind(0.25, "Lewis 2009", "Eunuch kingmakers; emperors puppets of factions", "HIGH"),
        },
    },
})

# ─── 8. Song Dynasty ───
CASES.append({
    "name": "Song Dynasty",
    "metadata": {"stress_type": "ancient_proxy", "region": "EastAsia", "data_quality": "RICH",
                 "shock": "exo", "outcome": "rupture", "fragment_count": "none-internal"},
    "tags": ["golden_age", "porosity", "P1ord_exo_conquest"],
    "peak_period": "c. 960–1127 CE (Northern Song)",
    "pre_stress_period": "c. 1250–1279 CE (late Southern Song)",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(1.00, "Kuhn 2009, The Age of Confucian Rule (Belknap/Harvard)", "Emperor-Council of State-circuits-prefectures-counties: 5+ tiers; most elaborate bureaucracy in world", "HIGH"),
            "P1b_legal_formal": ind(0.75, "McKnight 1992, Law and Order in Sung China", "Song criminal code + extensive case-law compilations; formal judicial hierarchy", "HIGH"),
            "P1c_bureaucratic": ind(1.00, "Chaffee 1985, The Thorny Gates of Learning in Sung China", "Imperial examination system matured; ~30,000 candidates per cycle; most meritocratic pre-modern system", "HIGH"),
            "P1d_fiscal_std": ind(0.75, "Golas 2015 in Cambridge History of China V.2", "Sophisticated tax system; paper money (jiaozi); state monopolies on salt/tea/liquor", "HIGH"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(1.00, "Needham 1954–; Mokyr 1990, The Lever of Riches", "Moveable type, compass, gunpowder weapons, blast furnace steel, mechanical clock — highest innovation rate in pre-modern world", "HIGH"),
            "P2b_knowledge_inst": ind(0.75, "Chaffee 1985; Bol 2008, Neo-Confucianism in History", "State academies, private academies (shuyuan), printing revolution democratized learning", "HIGH"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(32), "Scheidel 2007; Deng 1999", "Slightly above Asian average due to agricultural surplus and stability", "LOW"),
            "P3b_elite_literacy": ind(0.50, "Chaffee 1985; Bol 2008", "Printing revolution + exam system drove highest pre-modern literacy rate (~15-20% male); commercial literacy widespread", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.15), "Chandler 1987; Skinner 1977", "Kaifeng ~1M+; Hangzhou later ~1M+; dozens of cities >100k; ~10-15% urban", "HIGH"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(1000), "Maddison 2007; Broadberry et al. 2018", "Estimated ~$900-1100 GK$; wealthiest economy in world; iron production exceeded 18th-century Europe", "MODERATE"),
            "P4b_trade_auton": ind(0.75, "Shiba 1970, Commerce and Society in Sung China", "Maritime trade boom; diversified commercial economy; not dependent on single sector", "HIGH"),
            "P4c_tribute_dep": ind(0.50, "Golas 2015", "Significant tribute payments to Liao/Jin (Chanyuan Treaty); but manageable vs. state revenues", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.60, "Kuhn 2009", "Northern Song ~167 years; well-established", "HIGH"),
            "P5b_succession": ind(0.75, "Kuhn 2009", "Orderly imperial succession; no civil wars between legitimate claimants", "HIGH"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(1.00, "Kuhn 2009", "Bureaucratic structure fully intact in Southern Song territory", "HIGH"),
            "P1b_legal_formal": ind(0.75, "McKnight 1992", "Legal system functioning", "MODERATE"),
            "P1c_bureaucratic": ind(1.00, "Chaffee 1985", "Examination system continued unbroken", "HIGH"),
            "P1d_fiscal_std": ind(0.75, "Golas 2015", "Paper money still circulating; but inflation increasing", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.75, "Needham 1954–", "Innovation continued; gunpowder weapons deployed vs Mongols", "MODERATE"),
            "P2b_knowledge_inst": ind(0.75, "Bol 2008", "Academies and printing thriving", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(30), "Scheidel 2007", "Some decline from military pressure and displacement", "LOW"),
            "P3b_elite_literacy": ind(0.50, "Chaffee 1985", "Literacy gains preserved", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.15), "Chandler 1987", "Hangzhou among world's largest cities", "HIGH"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(900), "Maddison 2007", "Slightly reduced from loss of northern territory but south commercially vibrant", "LOW"),
            "P4b_trade_auton": ind(0.75, "Shiba 1970", "Maritime trade at peak; Quanzhou a global port", "HIGH"),
            "P4c_tribute_dep": ind(0.50, "Golas 2015", "Military expenditure consuming large share of revenue", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.75, "Kuhn 2009", "Combined Song dynasty >300 years; Southern Song ~150 yrs", "HIGH"),
            "P5b_succession": ind(0.50, "Kuhn 2009", "Emperor nominal; Jia Sidao dominated as chancellor; succession technically orderly but power hollow", "MODERATE"),
        },
    },
})

# ─── 9. Tokugawa Japan ───
CASES.append({
    "name": "Tokugawa Japan",
    "metadata": {"stress_type": "ancient_proxy", "region": "EastAsia", "data_quality": "RICH",
                 "shock": "mixed", "outcome": "transition", "fragment_count": "none"},
    "tags": ["config", "managed_transition", "container_absorb"],
    "peak_period": "c. 1700–1750 CE (Genroku–Kyōhō)",
    "pre_stress_period": "c. 1840–1868 CE (Bakumatsu)",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(0.75, "Totman 1993, Early Modern Japan", "Shogun-daimyō-domain bureaucracies-village heads: 4+ tiers; baku-han dual system", "HIGH"),
            "P1b_legal_formal": ind(0.75, "Henderson 1965, Conciliation and Japanese Law", "Laws of Military Houses (Buke Shohatto); domain codes; formal adjudication system", "HIGH"),
            "P1c_bureaucratic": ind(0.50, "Totman 1993", "Samurai administrators; hereditary but professionalized by 18th century", "MODERATE"),
            "P1d_fiscal_std": ind(0.75, "Totman 1993; Jansen 2000, The Making of Modern Japan", "Rice-based kokudaka assessment; standardized land surveys (kenchi); domain-level taxation", "HIGH"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Jansen 2000", "Rangaku (Dutch learning); agricultural innovations; but sakoku limited tech imports", "MODERATE"),
            "P2b_knowledge_inst": ind(0.75, "Dore 1965, Education in Tokugawa Japan", "Terakoya (temple schools); ~40% male literacy by late Tokugawa; domain academies (hanko)", "HIGH"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(35), "Jannetta 1987, Epidemics and Mortality in Early Modern Japan", "~33-37 yrs; notably high for pre-modern society due to peace and sanitation", "MODERATE"),
            "P3b_elite_literacy": ind(0.50, "Dore 1965", "~40% male, ~15% female literacy; highest pre-modern rate outside Song China", "HIGH"),
            "P3c_urbanization": ind(urb_norm(0.15), "Chandler 1987; Hanley & Yamamura 1977", "Edo ~1M (world's largest); Osaka/Kyoto ~300k each; ~12-15% urban", "HIGH"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(700), "Maddison 2007", "Estimated ~$600-750 GK$ for 1700 Japan; rice economy + proto-industry", "MODERATE"),
            "P4b_trade_auton": ind(0.75, "Totman 1993", "Sakoku limited foreign trade; domestic economy self-sufficient; Osaka rice market sophisticated", "HIGH"),
            "P4c_tribute_dep": ind(0.75, "Jansen 2000", "Domain system distributed fiscal risk; no single-source dependency", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.90, "Totman 1993", "~100+ years of unbroken peace by 1700; 250+ years total by end", "HIGH"),
            "P5b_succession": ind(0.75, "Totman 1993", "Shogunal succession orderly; advisory councils (rōjū) stabilized transitions", "HIGH"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(0.75, "Jansen 2000", "Administrative structure fully intact; domains still governed", "HIGH"),
            "P1b_legal_formal": ind(0.75, "Henderson 1965", "Legal system functioning", "MODERATE"),
            "P1c_bureaucratic": ind(0.50, "Jansen 2000", "Samurai bureaucracy ossified but functional", "MODERATE"),
            "P1d_fiscal_std": ind(0.50, "Jansen 2000", "Rice-based system struggling with monetized economy; domain debts", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Jansen 2000", "Rangaku expanding; awareness of Western technology growing", "MODERATE"),
            "P2b_knowledge_inst": ind(0.75, "Dore 1965", "Literacy rates continued rising; domain academies reforming", "HIGH"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(35), "Jannetta 1987", "Stable; no major demographic crisis", "MODERATE"),
            "P3b_elite_literacy": ind(0.50, "Dore 1965", "Maintained high levels", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.15), "Chandler 1987", "Edo still among world's largest", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(750), "Maddison 2007", "Slight growth from proto-industrialization", "MODERATE"),
            "P4b_trade_auton": ind(0.50, "Jansen 2000", "Unequal treaties opening; but not yet dependent on foreign trade", "MODERATE"),
            "P4c_tribute_dep": ind(0.50, "Jansen 2000", "Domain system intact but creaking financially", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.90, "Totman 1993", ">250 years of Tokugawa rule; immense institutional inertia", "HIGH"),
            "P5b_succession": ind(0.50, "Jansen 2000", "Last shoguns were weak; tozama domains challenging authority; succession technically orderly but authority hollow", "MODERATE"),
        },
    },
})

# ─── 10. Joseon Korea ───
CASES.append({
    "name": "Joseon Korea",
    "metadata": {"stress_type": "ancient_proxy", "region": "EastAsia", "data_quality": "RICH",
                 "shock": "exo+endo", "outcome": "absorb", "fragment_count": "none"},
    "tags": ["P1ord_longevity", "config", "reconstruction", "moderate_P1_longevity"],
    "peak_period": "c. 1420–1500 CE (Sejong → Seongjong)",
    "pre_stress_period": "c. 1580–1600 CE (pre-Imjin War)",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(0.75, "Palais 1996, Confucian Statecraft and Korean Institutions", "King-State Council-Six Boards-8 provinces-counties: 5 tiers", "HIGH"),
            "P1b_legal_formal": ind(0.75, "Palais 1996", "Gyeongguk daejeon (Grand Code): comprehensive administrative/criminal law", "HIGH"),
            "P1c_bureaucratic": ind(0.75, "Deuchler 1992, The Confucian Transformation of Korea", "Gwageo (civil service exam) system; yangban class but merit-selected within it", "HIGH"),
            "P1d_fiscal_std": ind(0.50, "Palais 1996", "Land tax system standardized; grain levies; but yangban tax exemptions growing", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.75, "Needham 1954–; Kim 2005", "Moveable metal type (pre-Gutenberg), rain gauge (cheugugi), Hangul script, astronomical instruments", "HIGH"),
            "P2b_knowledge_inst": ind(0.75, "Deuchler 1992", "Seonggyungwan academy; private seowon academies; systematic Confucian education", "HIGH"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(30), "Scheidel 2007 (East Asian averages)", "Comparable to Chinese norms; ~28-32 yrs", "LOW"),
            "P3b_elite_literacy": ind(0.40, "Deuchler 1992", "Hangul (1443) democratized literacy; exam system drove classical literacy among yangban", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.06), "Chandler 1987", "Hanyang (Seoul) ~100-200k; relatively less urbanized than China/Japan", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(600), "Maddison 2007 (Korea estimate)", "Rice-based agrarian economy; ~$550-650 GK$", "LOW"),
            "P4b_trade_auton": ind(0.50, "Palais 1996", "Limited foreign trade; self-sufficient but not commercially dynamic", "MODERATE"),
            "P4c_tribute_dep": ind(0.50, "Palais 1996", "Ming tributary relationship: symbolic tribute but not economically dependent", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.50, "Palais 1996", "~100 years by Seongjong; dynasty still establishing itself", "HIGH"),
            "P5b_succession": ind(0.75, "Palais 1996", "Generally orderly succession through early Joseon; council-managed transitions", "MODERATE"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(0.75, "Palais 1996", "Administrative structure fully intact", "MODERATE"),
            "P1b_legal_formal": ind(0.75, "Palais 1996", "Grand Code still operative", "MODERATE"),
            "P1c_bureaucratic": ind(0.50, "Deuchler 1992", "Exam system continuing but yangban factionalism intensifying", "MODERATE"),
            "P1d_fiscal_std": ind(0.25, "Palais 1996", "Yangban tax exemptions eroding fiscal base; land concentration", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Kim 2005", "Innovation slowed; Confucian orthodoxy less receptive to novelty", "MODERATE"),
            "P2b_knowledge_inst": ind(0.75, "Deuchler 1992", "Seowon academies proliferating", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(30), "Scheidel 2007", "Stable", "LOW"),
            "P3b_elite_literacy": ind(0.40, "Deuchler 1992", "Maintained", "LOW"),
            "P3c_urbanization": ind(urb_norm(0.06), "Chandler 1987", "Seoul stable", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(600), "Maddison 2007", "Economy stable", "LOW"),
            "P4b_trade_auton": ind(0.50, "Palais 1996", "Limited trade continuing", "MODERATE"),
            "P4c_tribute_dep": ind(0.50, "Palais 1996", "Ming relationship stable", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.60, "Palais 1996", "~200 years of dynasty; well-established", "HIGH"),
            "P5b_succession": ind(0.50, "Palais 1996", "Factional politics (sarim vs. hungu) made succession contested but managed", "MODERATE"),
        },
    },
})

# ─── 11. Khmer / Angkor ───
CASES.append({
    "name": "Khmer / Angkor",
    "metadata": {"stress_type": "ancient_proxy", "region": "SEAsia", "data_quality": "RICH",
                 "shock": "exo", "outcome": "migrate", "fragment_count": "none"},
    "tags": ["container_erosion", "environmental", "migrate_transform"],
    "peak_period": "c. 1113–1218 CE (Suryavarman II – Jayavarman VII)",
    "pre_stress_period": "c. 1350–1431 CE (decline period)",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(0.50, "Coe 2003, Angkor and the Khmer Civilization", "King-regional governors-local chiefs; ~3 tiers; temple-state integration", "MODERATE"),
            "P1b_legal_formal": ind(0.50, "Coe 2003; Mabbett & Chandler 1995", "Inscriptional evidence of royal edicts, judicial appointments, land regulations", "MODERATE"),
            "P1c_bureaucratic": ind(0.25, "Coe 2003", "Officials appointed by king but positions semi-hereditary; temple hierarchy parallel", "MODERATE"),
            "P1d_fiscal_std": ind(0.50, "Coe 2003", "Rice-based corvée and tax system supported massive construction; water management centralized", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Coe 2003; Fletcher et al. 2008 in Antiquity", "Massive hydraulic engineering (barays); temple construction technology; but limited export", "HIGH"),
            "P2b_knowledge_inst": ind(0.50, "Coe 2003", "Buddhist/Hindu monastic education; Sanskrit literary tradition", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(28), "Scheidel 2007 (SE Asian estimates)", "Tropical disease environment; ~25-30 yrs", "LOW"),
            "P3b_elite_literacy": ind(0.20, "Coe 2003", "Sanskrit + Khmer inscriptions; priestly/scribal literacy only", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.08), "Fletcher et al. 2008; Evans et al. 2007", "Angkor ~750k–1M (LIDAR); one of world's largest pre-modern urban complexes", "HIGH"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(550), "Maddison 2007 (SE Asia extrapolation)", "Rice surplus economy; ~$500-600 GK$", "LOW"),
            "P4b_trade_auton": ind(0.50, "Coe 2003", "Regional trade (Chinese ceramics, Indian goods); not a major maritime power", "MODERATE"),
            "P4c_tribute_dep": ind(0.50, "Coe 2003", "Provincial tribute + corvée labor; some dependency on peripheral rice production", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.75, "Coe 2003", "Angkorian period ~400+ years by Jayavarman VII; long-established", "HIGH"),
            "P5b_succession": ind(0.25, "Coe 2003", "Frequent usurpations; succession often by conquest/assassination between lineages", "MODERATE"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(0.25, "Coe 2003; Groslier 1979", "Administrative reach contracting; provincial control lost", "MODERATE"),
            "P1b_legal_formal": ind(0.25, "Coe 2003", "Inscriptions cease; royal authority unclear", "LOW"),
            "P1c_bureaucratic": ind(0.25, "Coe 2003", "Theravada Buddhist shift undermined temple-state bureaucracy", "MODERATE"),
            "P1d_fiscal_std": ind(0.25, "Coe 2003; Buckley et al. 2010 in PNAS", "Hydraulic system failing (dendro evidence); agricultural base declining", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.25, "Coe 2003", "No new monumental construction; hydraulic maintenance declining", "MODERATE"),
            "P2b_knowledge_inst": ind(0.25, "Coe 2003", "Shift to Theravada disrupted Sanskrit scholastic tradition", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(25), "Scheidel 2007; Buckley et al. 2010", "Droughts + floods likely increased mortality", "LOW"),
            "P3b_elite_literacy": ind(0.15, "Coe 2003", "Inscriptional record virtually ceases", "LOW"),
            "P3c_urbanization": ind(urb_norm(0.04), "Fletcher et al. 2008", "Angkor depopulating; population dispersing", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(450), "Maddison 2007 (extrapolated)", "Agricultural decline from hydraulic failure; near subsistence", "LOW"),
            "P4b_trade_auton": ind(0.50, "Coe 2003", "Shift toward maritime trade (Phnom Penh); adaptation, not collapse", "MODERATE"),
            "P4c_tribute_dep": ind(0.25, "Coe 2003", "Siamese raids extracting tribute; provinces defecting", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.50, "Coe 2003", "Angkorian tradition still nominally alive; >500 years", "MODERATE"),
            "P5b_succession": ind(0.25, "Coe 2003", "Siamese interventions in succession; puppet kings", "MODERATE"),
        },
    },
})

# ─── 12. Srivijaya ───
CASES.append({
    "name": "Srivijaya",
    "metadata": {"stress_type": "ancient_proxy", "region": "SEAsia", "data_quality": "MOD",
                 "shock": "exo", "outcome": "rupture", "fragment_count": "many"},
    "tags": ["P4P1gap_extreme", "thalassocracy"],
    "peak_period": "c. 680–800 CE",
    "pre_stress_period": "c. 1025–1100 CE (post-Chola raids)",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(0.25, "Manguin 2004 in SE Asia from Prehistory to History (Glover & Bellwood)", "Maharaja + port chiefs; minimal territorial administration; mandala network", "MODERATE"),
            "P1b_legal_formal": ind(0.25, "Manguin 2004; Wolters 1967, Early Indonesian Commerce", "Oaths of loyalty (Telaga Batu inscription); no codified law beyond royal commands", "MODERATE"),
            "P1c_bureaucratic": ind(0.25, "Manguin 2004", "Court-based; no evidence of standardized bureaucratic appointments", "LOW"),
            "P1d_fiscal_std": ind(0.25, "Manguin 2004", "Port duties and trade levies; no evidence of standardized land taxation", "LOW"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Manguin 2004; Miksic 2013", "Maritime technology (jong ships); adoption of Indian/Chinese technologies via trade", "MODERATE"),
            "P2b_knowledge_inst": ind(0.50, "Manguin 2004; I-Tsing's 7th-c. account", "Buddhist monastery complex at Palembang; I-Tsing reports 1000+ monks studying there", "HIGH"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(28), "Scheidel 2007", "Tropical maritime; ~25-30 yrs", "LOW"),
            "P3b_elite_literacy": ind(0.20, "Manguin 2004", "Old Malay + Sanskrit inscriptions; monastic literacy", "LOW"),
            "P3c_urbanization": ind(urb_norm(0.06), "Miksic 2013, Singapore and the Silk Road of the Sea", "Palembang a significant port city; limited inland urbanization", "LOW"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(650), "Maddison 2007 (adapted for entrepôt)", "Maritime trade wealth above agrarian baseline; entrepôt economy", "LOW"),
            "P4b_trade_auton": ind(0.75, "Wolters 1967; Manguin 2004", "Controlled Malacca Strait; trade with China, India, Arabia; diversified partners", "MODERATE"),
            "P4c_tribute_dep": ind(0.50, "Manguin 2004", "Chinese tribute system + entrepôt revenues; but vulnerable to trade route shifts", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.50, "Manguin 2004", "~200+ years of Srivijaya as identifiable polity", "MODERATE"),
            "P5b_succession": ind(0.25, "Manguin 2004", "Very little evidence on succession mechanisms; mandala politics inherently fluid", "LOW"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(0.25, "Manguin 2004", "Mandala network fragmenting; vassal ports asserting independence", "MODERATE"),
            "P1b_legal_formal": ind(0.25, "Manguin 2004", "No change from weak baseline", "LOW"),
            "P1c_bureaucratic": ind(0.25, "Manguin 2004", "Unchanged", "LOW"),
            "P1d_fiscal_std": ind(0.25, "Manguin 2004", "Trade revenues declining as ships bypass Palembang", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Manguin 2004", "Maritime technology continued", "MODERATE"),
            "P2b_knowledge_inst": ind(0.25, "Manguin 2004", "Buddhist center declining; scholars relocated to Java/India", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(28), "Scheidel 2007", "No major change", "LOW"),
            "P3b_elite_literacy": ind(0.15, "Manguin 2004", "Inscriptional activity declining", "LOW"),
            "P3c_urbanization": ind(urb_norm(0.04), "Miksic 2013", "Palembang diminishing as port cities multiply", "LOW"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(500), "Maddison 2007 (adapted)", "Trade revenues declining; Chola raids damaged port infrastructure", "LOW"),
            "P4b_trade_auton": ind(0.50, "Manguin 2004; Hall 1985", "Malacca Strait control weakened; competitors (Jambi, Java) capturing trade", "MODERATE"),
            "P4c_tribute_dep": ind(0.25, "Manguin 2004", "Chinese trade shifting to other ports; dependency exposed", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.50, "Manguin 2004", "Still identifiable but increasingly nominal", "MODERATE"),
            "P5b_succession": ind(0.25, "Manguin 2004", "Unknown/fluid; Chola raids may have disrupted royal lineage", "LOW"),
        },
    },
})

# ─── 13. Majapahit ───
CASES.append({
    "name": "Majapahit",
    "metadata": {"stress_type": "ancient_proxy", "region": "SEAsia", "data_quality": "MOD",
                 "shock": "endo", "outcome": "rupture", "fragment_count": "many"},
    "tags": ["config", "ruler_dependence", "suppression"],
    "peak_period": "c. 1350–1389 CE (Hayam Wuruk / Gajah Mada)",
    "pre_stress_period": "c. 1450–1527 CE (late Majapahit)",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(0.50, "Pigeaud 1960–63, Java in the 14th Century (Nāgarakĕrtāgama)", "King-court officials-regional lords; mandala structure with graded tribute relationships", "MODERATE"),
            "P1b_legal_formal": ind(0.50, "Pigeaud 1960–63", "Kutara-manawa dharmasastra (Javanese legal text); formal but limited enforcement", "MODERATE"),
            "P1c_bureaucratic": ind(0.25, "Pigeaud 1960–63", "Court positions semi-hereditary; Gajah Mada exceptional as non-royal chief minister", "MODERATE"),
            "P1d_fiscal_std": ind(0.50, "Pigeaud 1960–63", "Rice tax + trade levies; standardized within Java core", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Pigeaud 1960–63; Reid 1988, Southeast Asia in the Age of Commerce", "Maritime technology; Javanese shipbuilding; bronze-casting; irrigation engineering", "MODERATE"),
            "P2b_knowledge_inst": ind(0.50, "Pigeaud 1960–63", "Court literary culture (kakawin); Buddhist/Hindu monastic education", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(28), "Scheidel 2007", "Tropical SE Asian norms", "LOW"),
            "P3b_elite_literacy": ind(0.25, "Pigeaud 1960–63", "Kawi/Old Javanese literary tradition; court + monastic literacy", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.06), "Reid 1988", "Trowulan capital ~100k+; significant port cities", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(600), "Maddison 2007 (SE Asia); Reid 1988", "Rice + spice trade revenues; Java's agricultural surplus", "LOW"),
            "P4b_trade_auton": ind(0.75, "Reid 1988", "Spice trade gateway; diverse trade partners (China, India, Middle East)", "MODERATE"),
            "P4c_tribute_dep": ind(0.50, "Pigeaud 1960–63", "Tribute from vassal polities + Javanese rice; some dependency on spice trade", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.50, "Pigeaud 1960–63", "~100 years at peak period; relatively established", "MODERATE"),
            "P5b_succession": ind(0.50, "Pigeaud 1960–63", "Hayam Wuruk's succession orderly; Gajah Mada stabilized; but mandala inherently fragile", "MODERATE"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(0.25, "Reid 1988; Ricklefs 2008, A History of Modern Indonesia", "Central control lost; regional lords independent; Islamic coastal polities autonomous", "MODERATE"),
            "P1b_legal_formal": ind(0.25, "Ricklefs 2008", "Royal legal authority nominal", "LOW"),
            "P1c_bureaucratic": ind(0.25, "Ricklefs 2008", "Court positions ceremonial only", "MODERATE"),
            "P1d_fiscal_std": ind(0.25, "Ricklefs 2008", "Tax collection limited to Javanese heartland", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Reid 1988", "Maritime technologies continued in successor states", "MODERATE"),
            "P2b_knowledge_inst": ind(0.25, "Ricklefs 2008", "Hindu-Buddhist institutional base declining; Islamic schools emerging", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(28), "Scheidel 2007", "No major change", "LOW"),
            "P3b_elite_literacy": ind(0.20, "Ricklefs 2008", "Transitional; Kawi declining, Arabic/Malay rising", "LOW"),
            "P3c_urbanization": ind(urb_norm(0.05), "Reid 1988", "Trowulan abandoned; coastal cities (Demak, Gresik) growing instead", "LOW"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(550), "Maddison 2007", "Javanese core economy stable; trade shifting to Muslim ports", "LOW"),
            "P4b_trade_auton": ind(0.50, "Reid 1988", "Spice trade captured by Muslim sultanates (Malacca, Demak)", "MODERATE"),
            "P4c_tribute_dep": ind(0.25, "Ricklefs 2008", "Tributary network collapsed; no peripheral revenue", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.50, "Ricklefs 2008", "Dynasty nominally ~250 years but effectively moribund", "MODERATE"),
            "P5b_succession": ind(0.25, "Ricklefs 2008", "Succession disputes between Hindu-Buddhist and Islamic factions", "MODERATE"),
        },
    },
})

# ─── 14. Mali Empire ───
CASES.append({
    "name": "Mali Empire",
    "metadata": {"stress_type": "ancient_proxy", "region": "SSAfrica", "data_quality": "MOD",
                 "shock": "endo+exo", "outcome": "rupture", "fragment_count": "many"},
    "tags": ["P4P1gap", "ruler_dependence", "container_erosion"],
    "peak_period": "c. 1312–1337 CE (Mansa Musa)",
    "pre_stress_period": "c. 1400–1450 CE (post-Musa)",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(0.50, "Levtzion 1973, Ancient Ghana and Mali", "Mansa-provincial governors (farin)-local chiefs; ~3 tiers", "MODERATE"),
            "P1b_legal_formal": ind(0.50, "Levtzion 1973; Hunwick 1999, Timbuktu and the Songhay Empire", "Islamic law (maliki) in cities; customary law in rural areas; dual system", "MODERATE"),
            "P1c_bureaucratic": ind(0.25, "Levtzion 1973", "Appointments by mansa; personal loyalty basis; no formal civil service", "MODERATE"),
            "P1d_fiscal_std": ind(0.50, "Levtzion 1973; al-Umari's 14th-c. account", "Gold dust taxation + trade levies; Musa's pilgrimage demonstrated enormous fiscal capacity", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.25, "Levtzion 1973", "Iron working; limited technological innovation beyond trade adoption", "MODERATE"),
            "P2b_knowledge_inst": ind(0.50, "Hunwick 1999", "Timbuktu/Djenné mosques as centers of Islamic learning; manuscript tradition emerging", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(28), "Scheidel 2007; Manning 2010", "Sub-Saharan African norms ~25-30 yrs", "LOW"),
            "P3b_elite_literacy": ind(0.15, "Hunwick 1999", "Arabic literacy among ulama and merchants; oral tradition dominant", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.05), "Chandler 1987; McIntosh 2005", "Timbuktu ~50-100k; Djenné, Niani; ~3-5% urban", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(600), "Maddison 2007 (Africa adapted); Austen 2010", "Gold trade made Mali one of wealthiest West African states; ~$500-700 GK$", "LOW"),
            "P4b_trade_auton": ind(0.75, "Levtzion 1973; Austen 2010, Trans-Saharan Africa in World History", "Trans-Saharan gold trade; salt trade; diversified partners (Maghreb, Egypt)", "MODERATE"),
            "P4c_tribute_dep": ind(0.50, "Levtzion 1973", "Gold from Bambuk/Bure crucial; some single-source vulnerability", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.50, "Levtzion 1973", "~100+ years by Musa's reign; Keita dynasty established", "MODERATE"),
            "P5b_succession": ind(0.50, "Levtzion 1973", "Mansa succession sometimes contested between branches; Musa's own accession unusual", "MODERATE"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(0.25, "Levtzion 1973", "Provincial governors (Timbuktu, Gao) increasingly autonomous", "MODERATE"),
            "P1b_legal_formal": ind(0.50, "Hunwick 1999", "Islamic legal system continued in cities independently", "MODERATE"),
            "P1c_bureaucratic": ind(0.25, "Levtzion 1973", "Appointments failed outside heartland; personal networks broken", "MODERATE"),
            "P1d_fiscal_std": ind(0.25, "Levtzion 1973", "Gold revenues declining; Songhai capturing trade", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.25, "Levtzion 1973", "No change", "LOW"),
            "P2b_knowledge_inst": ind(0.50, "Hunwick 1999", "Timbuktu scholarship continuing independently", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(28), "Manning 2010", "No major change", "LOW"),
            "P3b_elite_literacy": ind(0.15, "Hunwick 1999", "Unchanged", "LOW"),
            "P3c_urbanization": ind(urb_norm(0.04), "Chandler 1987", "Niani declining; Timbuktu shifting to Songhai orbit", "LOW"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(500), "Maddison 2007 (adapted)", "Gold revenues declining; economic contraction", "LOW"),
            "P4b_trade_auton": ind(0.50, "Austen 2010", "Songhai capturing key trade nodes", "MODERATE"),
            "P4c_tribute_dep": ind(0.25, "Levtzion 1973", "Peripheral tribute lost; gold sources contested", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.50, "Levtzion 1973", "Keita dynasty still nominal; >200 years", "MODERATE"),
            "P5b_succession": ind(0.25, "Levtzion 1973", "Rapid turnover of mansas; factions contesting", "MODERATE"),
        },
    },
})

# ─── 15. Great Zimbabwe ───
CASES.append({
    "name": "Great Zimbabwe",
    "metadata": {"stress_type": "ancient_proxy", "region": "SSAfrica", "data_quality": "MOD",
                 "shock": "exo+env", "outcome": "migrate", "fragment_count": "2"},
    "tags": ["container_erosion", "environmental", "frag2-4"],
    "peak_period": "c. 1250–1350 CE",
    "pre_stress_period": "c. 1400–1450 CE",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(0.25, "Pikirayi 2001, The Zimbabwe Culture; Huffman 2007", "King-regional chiefs; ~2 tiers; limited administrative depth", "MODERATE"),
            "P1b_legal_formal": ind(0.25, "Pikirayi 2001", "Customary law; no written legal tradition; oral adjudication", "LOW"),
            "P1c_bureaucratic": ind(0.25, "Pikirayi 2001", "Court-based; kinship appointments; no formal civil service", "LOW"),
            "P1d_fiscal_std": ind(0.25, "Pikirayi 2001; Pwiti 1996", "Cattle tribute + trade levies; not standardized", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.25, "Pikirayi 2001", "Iron smelting; stone architecture (unique dry-stone); limited broader innovation", "MODERATE"),
            "P2b_knowledge_inst": ind(0.25, "Pikirayi 2001", "Oral tradition only; no evidence of formal educational institutions", "LOW"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(28), "Manning 2010", "Sub-Saharan norms", "LOW"),
            "P3b_elite_literacy": ind(0.00, "Pikirayi 2001", "No writing system; entirely oral", "HIGH"),
            "P3c_urbanization": ind(urb_norm(0.04), "Pikirayi 2001; Huffman 2007", "Great Zimbabwe ~10-18k; the only major settlement", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(500), "Maddison 2007 (Africa estimates)", "Cattle-based economy + Indian Ocean gold/ivory trade", "LOW"),
            "P4b_trade_auton": ind(0.75, "Pikirayi 2001; Pwiti 1996", "Gold + ivory exports via Sofala to Indian Ocean; diversified trade goods", "MODERATE"),
            "P4c_tribute_dep": ind(0.50, "Pikirayi 2001", "Gold mining areas separate from capital; some single-source risk", "LOW"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.50, "Pikirayi 2001", "~200+ years of Zimbabwe tradition", "MODERATE"),
            "P5b_succession": ind(0.25, "Pikirayi 2001", "Very limited evidence; likely contested between lineages", "LOW"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(0.25, "Pikirayi 2001", "Unchanged weak structure", "LOW"),
            "P1b_legal_formal": ind(0.25, "Pikirayi 2001", "No change", "LOW"),
            "P1c_bureaucratic": ind(0.25, "Pikirayi 2001", "Unchanged", "LOW"),
            "P1d_fiscal_std": ind(0.25, "Pikirayi 2001", "Trade revenues declining", "LOW"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.25, "Pikirayi 2001", "No change", "LOW"),
            "P2b_knowledge_inst": ind(0.25, "Pikirayi 2001", "Unchanged", "LOW"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(25), "Manning 2010", "Environmental stress + possible resource depletion", "LOW"),
            "P3b_elite_literacy": ind(0.00, "Pikirayi 2001", "No writing system", "HIGH"),
            "P3c_urbanization": ind(urb_norm(0.02), "Pikirayi 2001", "Great Zimbabwe depopulating", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(450), "Maddison 2007 (adapted)", "Gold trade shifting; environmental degradation of hinterland", "LOW"),
            "P4b_trade_auton": ind(0.50, "Pikirayi 2001", "Trade continuing via Sofala but competition from Khami/Mutapa", "LOW"),
            "P4c_tribute_dep": ind(0.25, "Pikirayi 2001", "Peripheral areas breaking away", "LOW"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.50, "Pikirayi 2001", "Tradition long but authority waning", "MODERATE"),
            "P5b_succession": ind(0.25, "Pikirayi 2001", "Likely contested; population dispersing to successor polities", "LOW"),
        },
    },
})

# ─── 16. Aksum ───
CASES.append({
    "name": "Aksum",
    "metadata": {"stress_type": "ancient_proxy", "region": "SSAfrica", "data_quality": "MOD",
                 "shock": "exo", "outcome": "migrate", "fragment_count": "none"},
    "tags": ["container_erosion", "P4P1gap", "migrate", "environmental"],
    "peak_period": "c. 325–400 CE (Ezana and successors)",
    "pre_stress_period": "c. 600–700 CE",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(0.50, "Munro-Hay 1991, Aksum: An African Civilisation", "King-regional governors (negus negesti title); ~3 tiers; but limited archaeological evidence", "MODERATE"),
            "P1b_legal_formal": ind(0.25, "Munro-Hay 1991", "Royal inscriptions show military-judicial authority; no surviving legal code", "LOW"),
            "P1c_bureaucratic": ind(0.25, "Munro-Hay 1991", "Court-based appointments; limited evidence of formal bureaucracy", "LOW"),
            "P1d_fiscal_std": ind(0.50, "Munro-Hay 1991", "Aksumite coinage (gold, silver, bronze) implies monetized taxation; unique in sub-Saharan Africa", "HIGH"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Munro-Hay 1991; Phillipson 2012", "Monumental stelae architecture; coinage minting; adoption of Christianity as state religion", "MODERATE"),
            "P2b_knowledge_inst": ind(0.50, "Munro-Hay 1991", "Christian monastic tradition (post-Ezana); Ge'ez literary tradition", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(28), "Manning 2010; Scheidel 2007", "Horn of Africa norms; ~25-30 yrs", "LOW"),
            "P3b_elite_literacy": ind(0.25, "Munro-Hay 1991; Phillipson 2012", "Ge'ez script; trilingual inscriptions (Ge'ez, Greek, Sabaean); monastic + royal literacy", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.05), "Munro-Hay 1991", "Aksum city ~20-30k; Adulis port ~10-20k; limited urban network", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(600), "Maddison 2007 (adapted); Munro-Hay 1991", "Red Sea/Indian Ocean trade in ivory, gold, aromatics; well above subsistence", "LOW"),
            "P4b_trade_auton": ind(0.75, "Munro-Hay 1991", "Adulis as major Red Sea port; trade with Rome, India, Arabia; diversified", "MODERATE"),
            "P4c_tribute_dep": ind(0.50, "Munro-Hay 1991", "Some dependency on Red Sea trade tolls; not fully diversified", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.50, "Munro-Hay 1991", "~200+ years by Ezana; Aksumite state established ~100 CE", "MODERATE"),
            "P5b_succession": ind(0.50, "Munro-Hay 1991", "Succession evidence limited; Ezana's accession suggests some orderly process", "LOW"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(0.25, "Munro-Hay 1991", "Territorial contraction; administration nominal beyond highland core", "MODERATE"),
            "P1b_legal_formal": ind(0.25, "Munro-Hay 1991", "No evidence of change from limited baseline", "LOW"),
            "P1c_bureaucratic": ind(0.25, "Munro-Hay 1991", "Unchanged", "LOW"),
            "P1d_fiscal_std": ind(0.25, "Munro-Hay 1991; Phillipson 2012", "Coinage debased and production declining; monetary economy contracting", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.25, "Phillipson 2012", "No new monumental construction; technological stagnation", "MODERATE"),
            "P2b_knowledge_inst": ind(0.50, "Munro-Hay 1991", "Christian monastic tradition survived and eventually sustained Ethiopian civilization", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(25), "Manning 2010", "Possible decline from environmental/political stress", "LOW"),
            "P3b_elite_literacy": ind(0.20, "Phillipson 2012", "Ge'ez tradition continuing in monasteries", "LOW"),
            "P3c_urbanization": ind(urb_norm(0.03), "Munro-Hay 1991", "Aksum declining; Adulis lost to Islamic expansion", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(450), "Maddison 2007 (adapted)", "Red Sea trade lost to Islamic control; economy contracting to highland agriculture", "LOW"),
            "P4b_trade_auton": ind(0.25, "Munro-Hay 1991", "Adulis captured by Arabs; trade access severely curtailed", "MODERATE"),
            "P4c_tribute_dep": ind(0.25, "Munro-Hay 1991", "Revenue base collapsed with trade loss", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.50, "Munro-Hay 1991", "Aksumite royal tradition continuing; ~500+ years", "MODERATE"),
            "P5b_succession": ind(0.25, "Munro-Hay 1991", "Dynasty weakened; eventual shift to Zagwe dynasty", "LOW"),
        },
    },
})

# ─── 17. Aztec Triple Alliance ───
CASES.append({
    "name": "Aztec Triple Alliance",
    "metadata": {"stress_type": "ancient_proxy", "region": "Meso", "data_quality": "RICH",
                 "shock": "exo", "outcome": "rupture", "fragment_count": "many"},
    "tags": ["suppression_strong", "P4P1gap", "confederacy"],
    "peak_period": "c. 1440–1502 CE (Motecuhzoma I – Ahuitzotl)",
    "pre_stress_period": "c. 1502–1519 CE (Motecuhzoma II)",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(0.50, "Smith 2012, The Aztecs (3rd ed.)", "Huey tlatoani-tributary provinces-calpixque (tax collectors)-altepetl; ~3-4 tiers but hegemonic not territorial", "HIGH"),
            "P1b_legal_formal": ind(0.50, "Smith 2012; Offner 1983, Law and Politics in Aztec Texcoco", "Elaborate court system; codified laws (80 laws of Nezahualcoyotl); formal judicial hierarchy", "HIGH"),
            "P1c_bureaucratic": ind(0.25, "Smith 2012", "Calpixque (tribute collectors) appointed; but warrior/priestly elites largely hereditary pipiltin", "MODERATE"),
            "P1d_fiscal_std": ind(0.75, "Smith 2012; Berdan & Anawalt 1997, Codex Mendoza", "Highly detailed tribute lists (Matricula de Tributos); standardized levies by province", "HIGH"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Smith 2012", "Chinampas agriculture; aqueducts; but no metallurgy for tools; obsidian technology sophisticated", "MODERATE"),
            "P2b_knowledge_inst": ind(0.50, "Smith 2012; León-Portilla 1963", "Calmecac (elite schools) + telpochcalli (commoner schools); systematic education", "HIGH"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(30), "McCaa 2000 in Cambridge World History of Disease", "Estimated ~28-32 yrs; relatively healthy urban population pre-contact", "MODERATE"),
            "P3b_elite_literacy": ind(0.25, "Smith 2012", "Pictographic writing system; scribal class (tlacuilo); functional but not alphabetic", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.12), "Smith 2012; Calnek 1976", "Tenochtitlan ~200-250k; Basin of Mexico ~1M total; ~10-15% urban", "HIGH"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(600), "Smith 2012; Maddison 2007 (adapted)", "Chinampas agriculture + tribute economy; ~$500-650 GK$", "LOW"),
            "P4b_trade_auton": ind(0.50, "Smith 2012; Berdan 2014", "Pochteca long-distance trade; markets; but empire primarily tribute-based", "MODERATE"),
            "P4c_tribute_dep": ind(0.50, "Smith 2012; Berdan & Anawalt 1997", "Highly dependent on tributary provinces; vulnerability if provinces rebel", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.50, "Smith 2012", "Triple Alliance ~70-100 years old; moderate establishment", "HIGH"),
            "P5b_succession": ind(0.50, "Smith 2012", "Tlatoani selected by council from ruling lineage; not always smooth but functional", "MODERATE"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(0.50, "Smith 2012", "Structure unchanged; Motecuhzoma II centralizing further", "MODERATE"),
            "P1b_legal_formal": ind(0.50, "Offner 1983", "Legal system functioning", "MODERATE"),
            "P1c_bureaucratic": ind(0.25, "Smith 2012", "Motecuhzoma II replaced commoner officials with nobles; reversed meritocratic trend", "MODERATE"),
            "P1d_fiscal_std": ind(0.75, "Smith 2012", "Tribute system fully operational", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Smith 2012", "Unchanged", "MODERATE"),
            "P2b_knowledge_inst": ind(0.50, "León-Portilla 1963", "Education system intact", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(30), "McCaa 2000", "No pre-contact demographic change", "MODERATE"),
            "P3b_elite_literacy": ind(0.25, "Smith 2012", "Unchanged", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.12), "Smith 2012", "Tenochtitlan at or near peak", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(600), "Maddison 2007 (adapted)", "Economy at peak level", "LOW"),
            "P4b_trade_auton": ind(0.50, "Berdan 2014", "Trade continuing", "MODERATE"),
            "P4c_tribute_dep": ind(0.50, "Smith 2012", "Tributary provinces restive but still paying", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.50, "Smith 2012", "~90 years of Triple Alliance", "MODERATE"),
            "P5b_succession": ind(0.50, "Smith 2012", "Motecuhzoma II's accession orderly; internal stability maintained", "MODERATE"),
        },
    },
})

# ─── 18. Classic Maya ───
CASES.append({
    "name": "Classic Maya",
    "metadata": {"stress_type": "ancient_proxy", "region": "Meso", "data_quality": "RICH",
                 "shock": "exo+endo", "outcome": "rupture", "fragment_count": "many"},
    "tags": ["config", "environmental", "container_erosion"],
    "peak_period": "c. 600–800 CE (Late Classic)",
    "pre_stress_period": "c. 800–900 CE (Terminal Classic)",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(0.50, "Martin & Grube 2000, Chronicle of the Maya Kings and Queens", "K'uhul ajaw-sajal-aj k'uhuun: ~3 tiers per polity; but no pan-Maya state; peer-polity system", "HIGH"),
            "P1b_legal_formal": ind(0.25, "Martin & Grube 2000", "Royal edicts via inscriptions; no evidence of codified inter-polity law", "MODERATE"),
            "P1c_bureaucratic": ind(0.25, "Martin & Grube 2000; Houston & Stuart 2001", "Court-based noble positions; kin-based appointments", "MODERATE"),
            "P1d_fiscal_std": ind(0.25, "Martin & Grube 2000", "Tribute between polities; labor corvée for construction; not standardized across system", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Sharer & Traxler 2006, The Ancient Maya (6th ed.)", "Sophisticated astronomy, calendar, hydraulic engineering, stucco architecture; but independent invention norm", "HIGH"),
            "P2b_knowledge_inst": ind(0.50, "Sharer & Traxler 2006", "Scribal schools (evidence from Copan, Calakmul); astronomical knowledge systematized", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(28), "McCaa 2000; Storey 1992", "~25-30 yrs from skeletal evidence; disease load in tropical lowlands", "MODERATE"),
            "P3b_elite_literacy": ind(0.20, "Houston 1994; Martin & Grube 2000", "Hieroglyphic literacy confined to scribal-priestly elite; ~1-2% of population", "HIGH"),
            "P3c_urbanization": ind(urb_norm(0.08), "Sharer & Traxler 2006", "Tikal ~60-80k; Calakmul ~50k; dispersed 'garden city' pattern; ~5-10% urban", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(500), "Maddison 2007 (adapted)", "Maize-based agriculture + jade/obsidian/cacao trade; ~$450-550 GK$", "LOW"),
            "P4b_trade_auton": ind(0.50, "Sharer & Traxler 2006", "Long-distance trade in obsidian, jade, cacao; but no single polity controlled it all", "MODERATE"),
            "P4c_tribute_dep": ind(0.50, "Martin & Grube 2000", "Inter-polity tribute; hegemonic polities extracted but not monopolized", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.60, "Martin & Grube 2000", "Major dynasties (Tikal, Calakmul) ~300-500 years old; well-established", "HIGH"),
            "P5b_succession": ind(0.25, "Martin & Grube 2000", "Frequent wars between polities; inter-dynasty conflicts; captive kings", "HIGH"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(0.25, "Demarest 2004, Ancient Maya: Rise and Fall of a Rainforest Civilization", "Polity hierarchies collapsing; subordinate sites asserting independence", "MODERATE"),
            "P1b_legal_formal": ind(0.25, "Martin & Grube 2000", "Royal authority fragmenting", "MODERATE"),
            "P1c_bureaucratic": ind(0.25, "Demarest 2004", "Court systems dissolving as dynasties end", "MODERATE"),
            "P1d_fiscal_std": ind(0.25, "Demarest 2004", "Tribute networks collapsing; agricultural surplus declining", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Sharer & Traxler 2006", "Technologies persisted; some sites still innovating", "MODERATE"),
            "P2b_knowledge_inst": ind(0.25, "Sharer & Traxler 2006", "Scribal traditions dying with royal courts; inscriptions ceasing", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(25), "Storey 1992; Demarest 2004", "Drought stress + warfare likely reduced LE", "MODERATE"),
            "P3b_elite_literacy": ind(0.10, "Martin & Grube 2000", "Inscriptions cease at site after site; literate class dispersing", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.03), "Demarest 2004", "Major centers depopulating; Tikal abandoned by ~900", "HIGH"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(450), "Maddison 2007 (adapted)", "Agricultural crisis from drought; trade disrupted", "LOW"),
            "P4b_trade_auton": ind(0.50, "Demarest 2004", "Coastal trade continuing; inland networks broken", "MODERATE"),
            "P4c_tribute_dep": ind(0.25, "Demarest 2004", "Tributary system collapsed", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.25, "Demarest 2004", "Dynasties ending; some sites last monument decades before abandonment", "MODERATE"),
            "P5b_succession": ind(0.00, "Martin & Grube 2000", "Dynastic sequences ending at major centers; no legitimate succession", "HIGH"),
        },
    },
})

# ─── 19. Tiwanaku ───
CASES.append({
    "name": "Tiwanaku",
    "metadata": {"stress_type": "ancient_proxy", "region": "Andes", "data_quality": "MOD",
                 "shock": "endo", "outcome": "rupture", "fragment_count": "many"},
    "tags": ["container_erosion", "ritual_legitimacy", "NOT_environmental"],
    "peak_period": "c. 600–800 CE (Tiwanaku IV–V)",
    "pre_stress_period": "c. 1000–1100 CE",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(0.50, "Janusek 2008, Ancient Tiwanaku; Kolata 1993", "Urban center → colonial enclaves → local ayllus; ~3 tiers; but colonial vs. hegemonic debate", "MODERATE"),
            "P1b_legal_formal": ind(0.25, "Janusek 2008", "No writing system; ritual/ceremonial authority inferred from monumental architecture", "LOW"),
            "P1c_bureaucratic": ind(0.25, "Janusek 2008", "Elite lineage-based leadership; no evidence of formalized offices", "LOW"),
            "P1d_fiscal_std": ind(0.50, "Kolata 1993, The Tiwanaku", "Raised-field (suka kollu) agriculture managed communally; surplus redistribution via ceremonial center", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Kolata 1993; Janusek 2008", "Raised-field agriculture; monumental stone architecture; bronze metallurgy", "MODERATE"),
            "P2b_knowledge_inst": ind(0.25, "Janusek 2008", "Ritual knowledge centers (Kalasasaya, Pumapunku); no formal schools", "LOW"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(28), "Blom et al. 2003 (bioarchaeology)", "Andean highlands; altitude stress offset by relatively stable food supply", "MODERATE"),
            "P3b_elite_literacy": ind(0.00, "Janusek 2008", "No writing system; khipu possibly used but debated", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.04), "Janusek 2008", "Tiwanaku city ~10-20k (up to 40k debated); only significant urban center", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(500), "Maddison 2007 (Andes estimate)", "Raised-field agriculture + llama caravan trade; near subsistence but with surplus", "LOW"),
            "P4b_trade_auton": ind(0.50, "Janusek 2008; Goldstein 2005", "Vertical archipelago economy; colonies in multiple ecological zones; diversified", "MODERATE"),
            "P4c_tribute_dep": ind(0.50, "Kolata 1993", "Dependency on raised-field system around Lake Titicaca", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.60, "Janusek 2008", "Tiwanaku as dominant center ~400+ years", "MODERATE"),
            "P5b_succession": ind(0.25, "Janusek 2008", "No evidence of succession mechanisms; probably lineage-based", "LOW"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(0.25, "Janusek 2008", "Colonial sites (Moquegua) abandoned; center losing peripheral control", "MODERATE"),
            "P1b_legal_formal": ind(0.25, "Janusek 2008", "No change from weak baseline", "LOW"),
            "P1c_bureaucratic": ind(0.25, "Janusek 2008", "Unchanged", "LOW"),
            "P1d_fiscal_std": ind(0.25, "Kolata 1993", "Raised-field system declining; surplus reduced", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.25, "Janusek 2008", "Raised-field technology abandoned in many areas", "MODERATE"),
            "P2b_knowledge_inst": ind(0.25, "Janusek 2008", "Ritual center losing influence", "LOW"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(25), "Blom et al. 2003", "Possible nutritional stress from agricultural decline", "LOW"),
            "P3b_elite_literacy": ind(0.00, "Janusek 2008", "No writing system", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.02), "Janusek 2008", "Tiwanaku city depopulating", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(450), "Maddison 2007 (adapted)", "Agricultural decline; colonial network broken", "LOW"),
            "P4b_trade_auton": ind(0.25, "Goldstein 2005", "Vertical archipelago colonies abandoned; trade network collapsed", "MODERATE"),
            "P4c_tribute_dep": ind(0.25, "Kolata 1993", "Peripheral inputs lost", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.50, "Janusek 2008", "Tiwanaku tradition ~600+ years but legitimacy waning", "MODERATE"),
            "P5b_succession": ind(0.25, "Janusek 2008", "No evidence; likely contested", "LOW"),
        },
    },
})

# ─── 20. Wari ───
CASES.append({
    "name": "Wari",
    "metadata": {"stress_type": "ancient_proxy", "region": "Andes", "data_quality": "MOD",
                 "shock": "endo", "outcome": "rupture", "fragment_count": "many"},
    "tags": ["centralization_trigger", "config"],
    "peak_period": "c. 600–800 CE",
    "pre_stress_period": "c. 900–1000 CE",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(0.50, "Schreiber 1992, Wari Imperialism in Middle Horizon Peru", "Provincial administrative centers (Pikillaqta, Viracochapampa); ~3 tiers; more territorial than Tiwanaku", "MODERATE"),
            "P1b_legal_formal": ind(0.25, "Schreiber 1992", "No writing; administrative authority expressed through architecture and material culture", "LOW"),
            "P1c_bureaucratic": ind(0.25, "Schreiber 1992; Isbell & McEwan 1991", "Standardized provincial centers suggest planned administration; but no evidence of formal offices", "MODERATE"),
            "P1d_fiscal_std": ind(0.50, "Schreiber 1992", "Corvée labor system; standardized storage facilities (qollqas) at provincial centers", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.25, "Schreiber 1992", "Terrace agriculture; some metallurgy; but less innovative than Tiwanaku", "MODERATE"),
            "P2b_knowledge_inst": ind(0.25, "Isbell & McEwan 1991", "D-shaped temples suggest ritualized knowledge; no formal institutions", "LOW"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(28), "Scheidel 2007 (Andean estimates)", "Similar to Tiwanaku norms", "LOW"),
            "P3b_elite_literacy": ind(0.00, "Schreiber 1992", "No writing system", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.04), "Isbell & McEwan 1991", "Huari capital ~10-20k; provincial centers smaller", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(500), "Maddison 2007 (Andes)", "Terrace agriculture + llama trade; comparable to Tiwanaku", "LOW"),
            "P4b_trade_auton": ind(0.50, "Schreiber 1992", "Vertical archipelago strategy; multi-zone resource access", "MODERATE"),
            "P4c_tribute_dep": ind(0.50, "Schreiber 1992", "Provincial labor tribute; distributed across multiple zones", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.50, "Schreiber 1992", "Wari expansion ~200+ years at peak", "MODERATE"),
            "P5b_succession": ind(0.25, "Isbell & McEwan 1991", "Unknown; no inscriptional or textual evidence", "LOW"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(0.25, "Schreiber 1992", "Provincial centers abandoned (Pikillaqta ritually closed); administration collapsed", "MODERATE"),
            "P1b_legal_formal": ind(0.25, "Schreiber 1992", "No change from weak baseline", "LOW"),
            "P1c_bureaucratic": ind(0.25, "Schreiber 1992", "Provincial administrative staff dispersed", "MODERATE"),
            "P1d_fiscal_std": ind(0.25, "Schreiber 1992", "Storage systems abandoned; corvée extraction ceased", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.25, "Schreiber 1992", "Technologies persisted locally but not centrally directed", "MODERATE"),
            "P2b_knowledge_inst": ind(0.25, "Isbell & McEwan 1991", "D-shaped temples destroyed or abandoned", "LOW"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(25), "Scheidel 2007", "Possible decline from political instability", "LOW"),
            "P3b_elite_literacy": ind(0.00, "Schreiber 1992", "No writing system", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.02), "Isbell & McEwan 1991", "Huari depopulating; regional centers fragmenting", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(450), "Maddison 2007 (adapted)", "Agricultural decline without centralized irrigation management", "LOW"),
            "P4b_trade_auton": ind(0.25, "Schreiber 1992", "Trade networks fragmented with provincial collapse", "MODERATE"),
            "P4c_tribute_dep": ind(0.25, "Schreiber 1992", "No tribute flow; provinces fully autonomous", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.25, "Schreiber 1992", "Wari authority effectively ended; post-Wari local polities", "MODERATE"),
            "P5b_succession": ind(0.25, "Isbell & McEwan 1991", "Regime ended; no succession", "LOW"),
        },
    },
})

# ─── 21. Carolingian ───
CASES.append({
    "name": "Carolingian",
    "metadata": {"stress_type": "ancient_proxy", "region": "Europe", "data_quality": "RICH",
                 "shock": "endo", "outcome": "rupture", "fragment_count": 3},
    "tags": ["frag_engineered", "ruler_dependence", "thin_container"],
    "peak_period": "c. 768–814 CE (Charlemagne)",
    "pre_stress_period": "c. 840–888 CE (post-Louis the Pious)",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(0.50, "McKitterick 2008, Charlemagne: Formation of a European Identity", "Emperor-missi dominici-counts-vicars: ~4 tiers; but counts held hereditary tendencies", "HIGH"),
            "P1b_legal_formal": ind(0.50, "McKitterick 2008; Ganshof 1971, Frankish Institutions Under Charlemagne", "Capitularies (royal legislation); but coexisted with tribal law codes (Lex Salica, etc.)", "HIGH"),
            "P1c_bureaucratic": ind(0.25, "McKitterick 2008", "Missi dominici as inspectors; but no permanent civil service; personal loyalty basis", "HIGH"),
            "P1d_fiscal_std": ind(0.25, "Ganshof 1971", "Royal estates (fiscs) provided revenue; limited standardized taxation; land grants weakened base", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.25, "McKitterick 2008", "Heavy plough spreading; three-field rotation; but limited technological innovation", "MODERATE"),
            "P2b_knowledge_inst": ind(0.50, "McKitterick 2008; Contreni 1995", "Carolingian Renaissance: palace school; monastic scriptoria (Tours, Corbie); curriculum standardization", "HIGH"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(30), "Scheidel 2007; Russell 1958", "Early medieval European norms ~28-32 yrs", "LOW"),
            "P3b_elite_literacy": ind(0.15, "McKitterick 1989, The Carolingians and the Written Word", "Carolingian minuscule; monastic literacy; clerical/noble ~5-10%; commoner near zero", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.03), "Chandler 1987; Verhulst 2002", "Aachen ~10k; Paris ~20k; very low urbanization; overwhelmingly rural", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(500), "Maddison 2007 (Western Europe)", "Agrarian economy; ~$450-550 GK$ for early medieval W. Europe", "MODERATE"),
            "P4b_trade_auton": ind(0.25, "McCormick 2001, Origins of the European Economy", "Limited long-distance trade; some Mediterranean and North Sea commerce; primarily local exchange", "MODERATE"),
            "P4c_tribute_dep": ind(0.50, "Ganshof 1971", "Royal fisc estates + plunder from conquests; plunder income not sustainable long-term", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.50, "McKitterick 2008", "Carolingian dynasty ~50+ years by Charlemagne; building on Merovingian institutions", "HIGH"),
            "P5b_succession": ind(0.50, "McKitterick 2008", "Charlemagne's succession to sole rule after Carloman's death; precedent of kingdom division", "MODERATE"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(0.25, "Nelson 1992, Charles the Bald", "Counts became hereditary local rulers; missi system collapsed; royal authority nominal", "HIGH"),
            "P1b_legal_formal": ind(0.25, "Nelson 1992", "Capitulary system defunct; local custom dominant", "MODERATE"),
            "P1c_bureaucratic": ind(0.25, "Nelson 1992", "No functioning central administration", "MODERATE"),
            "P1d_fiscal_std": ind(0.25, "Nelson 1992", "Royal fisc estates granted away; Danegeld as emergency levy only", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.25, "McKitterick 2008", "Innovation stalled; Viking raids disrupted some centers", "MODERATE"),
            "P2b_knowledge_inst": ind(0.50, "Contreni 1995", "Monastic scriptoria survived and continued; intellectual life persisted", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(28), "Scheidel 2007", "Viking raids + internal warfare may have slightly reduced LE", "LOW"),
            "P3b_elite_literacy": ind(0.10, "McKitterick 1989", "Monastic literacy persisted; lay literacy declined", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.02), "Chandler 1987", "Urban life minimal; Viking destruction of some centers", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(450), "Maddison 2007", "Economic contraction from Viking raids + internal warfare", "LOW"),
            "P4b_trade_auton": ind(0.25, "McCormick 2001", "Trade disrupted by Viking/Saracen raids", "MODERATE"),
            "P4c_tribute_dep": ind(0.25, "Nelson 1992", "Royal lands mostly alienated; Danegeld extraction from peasants", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.50, "Nelson 1992", "Carolingian dynasty ~130 years; but partition tradition weakened it", "MODERATE"),
            "P5b_succession": ind(0.25, "Nelson 1992", "Treaty of Verdun (843) → three-way partition; further subdivision; civil wars among grandsons", "HIGH"),
        },
    },
})

# ─── 22. Byzantine (Macedonian) ───
CASES.append({
    "name": "Byzantine (Macedonian)",
    "metadata": {"stress_type": "ancient_proxy", "region": "Europe", "data_quality": "RICH",
                 "shock": "none", "outcome": "absorb", "fragment_count": "none"},
    "tags": ["golden_age", "P1ord", "porosity", "low_base_recovery"],
    "peak_period": "c. 963–1025 CE (Nikephoros II → Basil II)",
    "pre_stress_period": "c. 1025–1081 CE (post-Basil II)",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(0.75, "Treadgold 1997, A History of the Byzantine State and Society", "Emperor-logothetes-themes/tagmata-local; ~4+ tiers; professional bureaucracy", "HIGH"),
            "P1b_legal_formal": ind(0.75, "Treadgold 1997; Laiou & Morrisson 2007", "Basilika legal code; functioning courts; Roman legal tradition continuous", "HIGH"),
            "P1c_bureaucratic": ind(0.75, "Treadgold 1997", "Professional civil service; advancement by merit/imperial favor; literate administration", "HIGH"),
            "P1d_fiscal_std": ind(0.75, "Laiou & Morrisson 2007, The Byzantine Economy", "Standardized land tax; nomisma coinage stable for ~700 years; sophisticated fiscal administration", "HIGH"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Treadgold 1997; Laiou & Morrisson 2007", "Greek fire; architectural innovation; but limited diffusion beyond court/military", "MODERATE"),
            "P2b_knowledge_inst": ind(0.75, "Treadgold 1997", "University of Constantinople; encyclopedic compilations (Suda); systematic scholarship", "HIGH"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(32), "Scheidel 2007", "Mediterranean urban norms; possibly slightly above due to infrastructure", "LOW"),
            "P3b_elite_literacy": ind(0.35, "Treadgold 1997; Harris 1989", "Relatively high elite literacy; Greek literary culture; bureaucratic class literate", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.12), "Chandler 1987; Laiou & Morrisson 2007", "Constantinople ~400-500k; several cities >20k; ~10-12% urban", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(700), "Maddison 2007; Laiou & Morrisson 2007", "~$600-800 GK$; one of wealthiest states in medieval world", "MODERATE"),
            "P4b_trade_auton": ind(0.75, "Laiou & Morrisson 2007", "Constantinople as trade hub; silk production; diverse Mediterranean trade", "HIGH"),
            "P4c_tribute_dep": ind(0.75, "Laiou & Morrisson 2007", "Diversified tax base; land tax + trade levies + monopolies; not single-source", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.85, "Treadgold 1997", "Roman/Byzantine state ~600+ years continuous; Macedonian dynasty ~100 years at peak", "HIGH"),
            "P5b_succession": ind(0.50, "Treadgold 1997", "Macedonian dynasty survived usurpations (Nikephoros, Tzimiskes); palace coups norm but state survived", "HIGH"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(0.75, "Treadgold 1997", "Administrative structure intact", "HIGH"),
            "P1b_legal_formal": ind(0.75, "Laiou & Morrisson 2007", "Legal system functioning", "MODERATE"),
            "P1c_bureaucratic": ind(0.50, "Treadgold 1997", "Civilian faction (Psellos circle) undermined military; factionalism in bureaucracy", "MODERATE"),
            "P1d_fiscal_std": ind(0.50, "Laiou & Morrisson 2007", "Pronoia grants beginning to alienate tax base; but system still functioning", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Treadgold 1997", "Unchanged", "MODERATE"),
            "P2b_knowledge_inst": ind(0.75, "Treadgold 1997", "Intellectual life continued (Psellos, Mauropous)", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(30), "Scheidel 2007", "Stable", "LOW"),
            "P3b_elite_literacy": ind(0.35, "Treadgold 1997", "Maintained", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.10), "Chandler 1987", "Constantinople stable; provincial towns possibly declining", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(650), "Laiou & Morrisson 2007", "Slight economic contraction; Italian merchants gaining trade share", "MODERATE"),
            "P4b_trade_auton": ind(0.50, "Laiou & Morrisson 2007", "Venetian/Genoese traders gaining privileged access; autonomy declining", "MODERATE"),
            "P4c_tribute_dep": ind(0.50, "Laiou & Morrisson 2007", "Pronoia system beginning; but tax base still broad", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.85, "Treadgold 1997", "Byzantine state >700 years continuous", "HIGH"),
            "P5b_succession": ind(0.25, "Treadgold 1997", "Rapid succession of emperors post-Basil II; 13 emperors in 56 years; instability", "HIGH"),
        },
    },
})

# ─── 23. Venetian Republic ───
CASES.append({
    "name": "Venetian Republic",
    "metadata": {"stress_type": "ancient_proxy", "region": "Europe", "data_quality": "RICH",
                 "shock": "none", "outcome": "durable", "fragment_count": "none"},
    "tags": ["P1ord_strong", "config", "convergence_closure", "durability"],
    "peak_period": "c. 1380–1500 CE (post-Chioggia → height of terraferma)",
    "pre_stress_period": "c. 1570–1600 CE (post-Lepanto, shifting trade)",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(1.00, "Lane 1973, Venice: A Maritime Republic", "Doge-Great Council-Senate-Council of Ten-Podestà (terraferma): 5+ tiers; deeply layered", "HIGH"),
            "P1b_legal_formal": ind(0.75, "Lane 1973; Finlay 1980, Politics in Renaissance Venice", "Elaborate statutory law; formal judicial system; contract law for commerce", "HIGH"),
            "P1c_bureaucratic": ind(0.75, "Lane 1973", "Elected/appointed officials with term limits; rotation system; not hereditary (within patriciate)", "HIGH"),
            "P1d_fiscal_std": ind(0.75, "Lane 1973; Mueller 1997", "Standardized customs duties; forced loans (prestanze); Monte Vecchio public debt system", "HIGH"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.75, "Lane 1973", "Arsenal shipbuilding (proto-assembly line); glassmaking (Murano); printing (Aldus Manutius)", "HIGH"),
            "P2b_knowledge_inst": ind(0.75, "Lane 1973", "University of Padua (part of Venetian state); printing industry; commercial education", "HIGH"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(33), "Scheidel 2007; Cipolla 1993", "Italian city-state norms ~30-35 yrs; relatively prosperous", "MODERATE"),
            "P3b_elite_literacy": ind(0.50, "Lane 1973", "Commercial literacy widespread among patriciate and cittadini; printing hub of Europe", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.20), "Chandler 1987; Lane 1973", "Venice ~100-180k; highly urbanized for territory; terraferma cities significant", "HIGH"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(1500), "Maddison 2007; Lane 1973", "~$1200-1800 GK$; among wealthiest per-capita in world; mercantile economy", "MODERATE"),
            "P4b_trade_auton": ind(0.75, "Lane 1973", "Diversified trade: spices, textiles, glass, salt; multiple trade routes", "HIGH"),
            "P4c_tribute_dep": ind(0.75, "Lane 1973; Mueller 1997", "Revenue from customs, taxes, terraferma; well-diversified; not dependent on single source", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(1.00, "Lane 1973", "Republic ~800 years old by 1400; most durable state in European history to that point", "HIGH"),
            "P5b_succession": ind(1.00, "Lane 1973; Finlay 1980", "Elaborate doge election system; no civil wars; peaceful transitions for centuries", "HIGH"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(1.00, "Lane 1973", "Administrative structure unchanged and fully functional", "HIGH"),
            "P1b_legal_formal": ind(0.75, "Lane 1973", "Legal system intact", "MODERATE"),
            "P1c_bureaucratic": ind(0.75, "Lane 1973", "Bureaucracy functioning; Council of Ten still effective", "MODERATE"),
            "P1d_fiscal_std": ind(0.75, "Lane 1973", "Fiscal system maintained; public debt managed", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Lane 1973", "Innovation slowing; Arsenal less cutting-edge; but printing still strong", "MODERATE"),
            "P2b_knowledge_inst": ind(0.75, "Lane 1973", "Padua university flourishing (Galileo); printing industry peak", "HIGH"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(32), "Cipolla 1993", "Stable; occasional plague outbreaks", "MODERATE"),
            "P3b_elite_literacy": ind(0.50, "Lane 1973", "Maintained high levels", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.18), "Chandler 1987", "Venice ~150-175k; slight decline from peak", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(1200), "Maddison 2007", "Declining from peak as Atlantic trade shifted advantage; ~$1000-1400 GK$", "MODERATE"),
            "P4b_trade_auton": ind(0.50, "Lane 1973", "Portuguese Cape route undermining spice monopoly; but diversifying into manufacturing", "HIGH"),
            "P4c_tribute_dep": ind(0.75, "Lane 1973", "Revenue base still diversified; terraferma taxes reliable", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(1.00, "Lane 1973", "Republic ~1000+ years old; extraordinary longevity", "HIGH"),
            "P5b_succession": ind(1.00, "Lane 1973", "Doge election system still functioning perfectly", "HIGH"),
        },
    },
})

# ─── 24. Ottoman (classical) ───
CASES.append({
    "name": "Ottoman (classical)",
    "metadata": {"stress_type": "ancient_proxy", "region": "NearEast", "data_quality": "RICH",
                 "shock": "none", "outcome": "absorb", "fragment_count": "none"},
    "tags": ["convergence_developmental", "innovation_with_inst", "porosity"],
    "peak_period": "c. 1453–1566 CE (Mehmed II → Süleyman I)",
    "pre_stress_period": "c. 1566–1600 CE (post-Süleyman)",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(1.00, "İnalcık 1973, The Ottoman Empire: The Classical Age", "Sultan-Grand Vizier-beylerbeyi-sancakbeyi-kadi: 5+ tiers; deeply layered provincial system", "HIGH"),
            "P1b_legal_formal": ind(0.75, "İnalcık 1973; Imber 2002, The Ottoman Empire", "Kanunname (sultanic law) + Sharia: dual legal system; kadi courts with formal jurisdiction", "HIGH"),
            "P1c_bureaucratic": ind(1.00, "İnalcık 1973", "Devshirme system: meritocratic recruitment of slave-soldiers/administrators; no hereditary offices at peak", "HIGH"),
            "P1d_fiscal_std": ind(0.75, "İnalcık 1973; Pamuk 2000, A Monetary History of the Ottoman Empire", "Timar land-grant system; tahrir surveys (detailed land/population registers); standardized taxation", "HIGH"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "İnalcık 1973; Ágoston 2005, Guns for the Sultan", "Gunpowder weapons adoption; siege technology; but limited non-military innovation", "MODERATE"),
            "P2b_knowledge_inst": ind(0.75, "İnalcık 1973", "Medrese system: extensive network of Islamic colleges; endowed (vakıf) institutions", "HIGH"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(30), "Scheidel 2007", "Mediterranean/Near Eastern norms ~28-32 yrs", "LOW"),
            "P3b_elite_literacy": ind(0.30, "İnalcık 1973", "Medrese-trained ulema; scribal bureaucracy (kalemiye); but literacy limited to educated class", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.12), "Chandler 1987; İnalcık 1973", "Istanbul ~400-700k (largest European city); several cities >50k; ~10-15% urban", "HIGH"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(700), "Maddison 2007; Pamuk 2000", "~$600-800 GK$; diversified economy: agriculture + trade + manufacturing", "MODERATE"),
            "P4b_trade_auton": ind(0.75, "İnalcık 1973; Pamuk 2000", "Controlled key trade routes; silk, spice trade; diverse economic base", "MODERATE"),
            "P4c_tribute_dep": ind(0.75, "İnalcık 1973", "Timar system + trade taxes + tributes from vassals; well-diversified revenue", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.60, "İnalcık 1973", "~150+ years of Ottoman rule by Süleyman; dynasty well-established", "HIGH"),
            "P5b_succession": ind(0.50, "İnalcık 1973; Imber 2002", "Fratricide norm (solved succession wars); brutal but effective at preventing civil war", "HIGH"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(1.00, "İnalcık 1973", "Administrative structure fully intact", "HIGH"),
            "P1b_legal_formal": ind(0.75, "Imber 2002", "Legal system functioning", "MODERATE"),
            "P1c_bureaucratic": ind(0.75, "İnalcık 1973", "Devshirme system continuing but free Muslims increasingly entering; slight hereditary creep", "MODERATE"),
            "P1d_fiscal_std": ind(0.75, "Pamuk 2000", "Timar system intact; iltizam (tax-farming) beginning to appear", "MODERATE"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Ágoston 2005", "Military technology still competitive; printing rejected by ulema", "MODERATE"),
            "P2b_knowledge_inst": ind(0.75, "İnalcık 1973", "Medrese system continuing strongly", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(30), "Scheidel 2007", "Stable", "LOW"),
            "P3b_elite_literacy": ind(0.30, "İnalcık 1973", "Unchanged", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.12), "Chandler 1987", "Istanbul still massive; urban network stable", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(700), "Pamuk 2000", "Economy stable; but price revolution beginning to stress akçe", "MODERATE"),
            "P4b_trade_auton": ind(0.75, "Pamuk 2000", "Trade continuing; but Portuguese Cape route creating competition", "MODERATE"),
            "P4c_tribute_dep": ind(0.75, "İnalcık 1973", "Revenue still diversified", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.75, "İnalcık 1973", "~300 years of Ottoman dynasty; deeply established", "HIGH"),
            "P5b_succession": ind(0.50, "Imber 2002", "Selim II's smooth accession; kafes (cage) system emerging; reducing fratricide violence", "MODERATE"),
        },
    },
})

# ─── 25. New Kingdom Egypt ───
CASES.append({
    "name": "New Kingdom Egypt",
    "metadata": {"stress_type": "ancient_proxy", "region": "Egypt", "data_quality": "RICH",
                 "shock": "mixed", "outcome": "rupture", "fragment_count": 2},
    "tags": ["container_erosion", "environmental_systemic", "suppression", "frag2-4"],
    "peak_period": "c. 1479–1213 BCE (Thutmose III → Ramesses II)",
    "pre_stress_period": "c. 1150–1070 BCE (late Dynasty XX)",
    "peak": {
        "P1": {
            "P1a_admin_depth": ind(0.75, "Kemp 2006; Van Dijk 2000 in Oxford History of Ancient Egypt", "King-vizier(s: Upper+Lower)-nome governors-local: 4+ tiers; two vizierates a sophistication", "HIGH"),
            "P1b_legal_formal": ind(0.50, "Allam 2007 in Westbrook (ed.), History of Ancient Near Eastern Law", "Royal decrees; Great Kenbet courts; Deir el-Medina worker disputes show functioning judicial system", "HIGH"),
            "P1c_bureaucratic": ind(0.50, "Bryan 2000 in Oxford History of Ancient Egypt", "Scribal bureaucracy professionalized; some positions still hereditary but functional appointment system", "MODERATE"),
            "P1d_fiscal_std": ind(0.75, "Warburton 2007, State and Economy in Ancient Egypt", "Systematic grain taxation; temple/state accounting on papyri; standardized weight (deben) system", "HIGH"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Nicholson & Shaw 2000", "Bronze metallurgy, chariot technology, glass-making; mostly adopted from Near Eastern contact", "HIGH"),
            "P2b_knowledge_inst": ind(0.50, "Baines & Eyre 1983; Lesko 2001", "House of Life continued; Deir el-Medina shows broader-than-elite literacy among artisans", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(30), "Scheidel 2001", "~28-32 yrs; stable Nile ecology", "MODERATE"),
            "P3b_elite_literacy": ind(0.20, "Baines & Eyre 1983; Lesko 2001", "~3-5% overall; artisan literacy at Deir el-Medina notable; scribal class expanded", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.07), "Bard 2015; Kemp 2006", "Thebes/Pi-Ramesse ~100k+; Memphis continues; ~5-8% urban", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(650), "Maddison 2007 (extrapolated); Warburton 2007", "Imperial economy with Nubian gold, Levantine trade, Nile agriculture; ~$600-700 GK$", "LOW"),
            "P4b_trade_auton": ind(0.75, "Cline 2014, 1177 B.C.: The Year Civilization Collapsed", "Late Bronze Age trade network: Egypt-Hatti-Ugarit-Mycenae; diversified partners", "MODERATE"),
            "P4c_tribute_dep": ind(0.50, "Murnane 1990; Van Dijk 2000", "Nubian gold + Levantine tribute significant; some dependency on imperial periphery", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.75, "Shaw 2003", "New Kingdom ~300+ years by Ramesses II; multiple long-reigning pharaohs", "HIGH"),
            "P5b_succession": ind(0.75, "Dodson & Hilton 2004", "Generally orderly succession; Amarna period exception but dynasty survived", "MODERATE"),
        },
    },
    "pre_stress": {
        "P1": {
            "P1a_admin_depth": ind(0.50, "Van Dijk 2000", "Theban high priests functioning as de facto rulers of Upper Egypt; dual authority", "HIGH"),
            "P1b_legal_formal": ind(0.50, "Allam 2007", "Turin judicial papyrus shows courts still functioning but tomb-robbery trials indicate social stress", "MODERATE"),
            "P1c_bureaucratic": ind(0.25, "Van Dijk 2000", "Offices concentrated in fewer hands; high priest Herihor held military/civil/priestly titles simultaneously", "MODERATE"),
            "P1d_fiscal_std": ind(0.25, "Warburton 2007; Janssen 1975", "Grain rations to Deir el-Medina workers regularly defaulted; fiscal system strained", "HIGH"),
        },
        "P2": {
            "P2a_tech_diffusion": ind(0.50, "Nicholson & Shaw 2000", "Iron adoption beginning; bronze still dominant; technology stable", "MODERATE"),
            "P2b_knowledge_inst": ind(0.50, "Lesko 2001", "Scribal traditions continuing", "MODERATE"),
        },
        "P3": {
            "P3a_life_expect": ind(le_norm(28), "Scheidel 2001", "Possible decline from economic stress; Sea Peoples disruption", "LOW"),
            "P3b_elite_literacy": ind(0.15, "Baines & Eyre 1983", "Slight decline as institutional support weakened", "MODERATE"),
            "P3c_urbanization": ind(urb_norm(0.05), "Bard 2015", "Pi-Ramesse abandoned; Thebes declining; Tanis emerging", "MODERATE"),
        },
        "P4": {
            "P4a_gdp_proxy": ind(gdp_norm(500), "Maddison 2007 (adapted); Cline 2014", "Bronze Age trade collapse; loss of Nubian gold revenues; economic contraction", "MODERATE"),
            "P4b_trade_auton": ind(0.25, "Cline 2014", "International trade network collapsed; Wenamun papyrus shows Egypt's diminished standing", "HIGH"),
            "P4c_tribute_dep": ind(0.25, "Van Dijk 2000", "Empire lost; no imperial revenue; Nubian mines gone", "MODERATE"),
        },
        "P5": {
            "P5a_regime_dur": ind(0.50, "Shaw 2003", "Dynasty XX ~80 years; but New Kingdom tradition ~450 years", "MODERATE"),
            "P5b_succession": ind(0.25, "Dodson & Hilton 2004", "Ramessid succession increasingly contested; worker strikes; tomb robberies signal breakdown", "MODERATE"),
        },
    },
})


# ═══════════════════════════════════════════════════════════════
# BUILD JSON
# ═══════════════════════════════════════════════════════════════

def build_case(c):
    peak_tp = build_timepoint(c["peak"])
    pre_tp = build_timepoint(c["pre_stress"])
    peak_tp["period"] = c["peak_period"]
    pre_tp["period"] = c["pre_stress_period"]

    bib = set()
    for tp_data in [c["peak"], c["pre_stress"]]:
        for pillar in tp_data.values():
            for ind_data in pillar.values():
                bib.add(ind_data["source"])
    bibliography = sorted(bib)

    return {
        "name": c["name"],
        "metadata": c["metadata"],
        "track": 3,
        "peak": peak_tp,
        "pre_stress": pre_tp,
        "bibliography": bibliography,
        "tags": c["tags"],
        "note": "TRACK 3: period-normalized proxy indicators (LE ceiling=40, GDP ceiling=$2000 GK$). "
                "Scores measure standing among pre-industrial peers, NOT comparable to modern MI. "
                "All indicators weighted equally; confidence flags are metadata only."
    }

output = [build_case(c) for c in CASES]
out_path = Path(__file__).parent / "ancient_cases.json"
out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
print(f"Wrote {len(output)} cases to {out_path} ({out_path.stat().st_size:,} bytes)")

# Quick validation
for case in output:
    for tp in ["peak", "pre_stress"]:
        mi_val = case[tp]["MI"]
        for p in ["P1", "P2", "P3", "P4", "P5"]:
            s = case[tp][p]["score"]
            assert 0 <= s <= 1, f"{case['name']} {tp} {p}={s} out of range"
        assert 0 <= mi_val <= 1, f"{case['name']} {tp} MI={mi_val} out of range"
print("All validation checks passed.")
