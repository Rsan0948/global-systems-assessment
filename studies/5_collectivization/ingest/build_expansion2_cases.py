"""
Build the second batch of 10 expansion case JSONs.

These 10 cases were randomly selected (seed=43) from a NEW 20-case
candidate pool (no overlap with the first 20). Selection was performed
before any feature vectors were coded.

Run:  python -m ingest.build_expansion2_cases
From: studies/5_collectivization/
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from ingest_maddison import load_gdp_series, avg_annual_growth
from ingest_vdem import load_vdem_series

CASES_DIR = os.path.join(HERE, "..", "cases")

# Feature indices for reference:
# 0  single_executive
# 1  hereditary_succession
# 2  independent_militaries
# 3  independent_foreign_policy
# 4  shared_currency
# 5  shared_legal_code
# 6  unilateral_exit
# 7  central_tax
# 8  popular_sovereignty
# 9  elected_leadership
# 10 free_movement_persons
# 11 free_movement_goods
# 12 shared_supreme_court
# 13 central_standing_army
# 14 preexisting_polities

SPECS = [
    # ================================================================
    # 1. SWITZERLAND: independent cantons -> federal state (1291-1848)
    # ================================================================
    {
        "name": "Switzerland",
        "is_control": False,
        "pre_frag_year": 1291,       # Original three cantons form Eidgenossenschaft
        "frag_peak_year": 1499,      # Independence from HRE (Treaty of Basel)
        "first_integration_year": 1798,  # Helvetic Republic (Napoleon)
        "post_collect_year": 1848,   # Federal constitution adopted

        # PRE: Independent cantons (loose confederation phase, pre-1798)
        # Single executive: 0 (no central executive), hereditary: 0 (cantonal councils),
        # independent militaries: 1, indep foreign policy: 1,
        # shared currency: 0 (cantonal currencies), shared legal code: 0,
        # unilateral exit: 1 (sovereign cantons), central tax: 0,
        # popular sovereignty: 1 (Landsgemeinde tradition), elected: 1,
        # free movement: 1 (relatively open), free goods: 0 (internal tolls),
        # shared court: 0, central army: 0 (cantonal militia), preexisting: 1
        "features_pre": [0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1],

        # POST: Swiss Federal State (1848 constitution)
        # Single executive: 0 (Federal Council is collegial, no single head),
        # hereditary: 0, independent militaries: 0 (federal army),
        # indep foreign policy: 0 (federal), shared currency: 1 (Swiss franc),
        # shared legal code: 1 (federal law), unilateral exit: 0,
        # central tax: 1 (federal customs/taxes), popular sovereignty: 1,
        # elected: 1 (elected parliament + Federal Council),
        # free movement: 1, free goods: 1 (internal free trade),
        # shared court: 1 (Federal Tribunal), central army: 1 (militia but federal),
        # preexisting: 1
        "features_post": [0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],

        "units_pre": 13,     # 13 cantons by 1513 (the "Thirteen Places")
        "units_peak": 22,    # 22 cantons by Napoleonic period
        "units_post": 22,    # 22 cantons in 1848 (25 today)
        "pop_pre": 800_000,      # Swiss Confederation c.1500
        "pop_post": 2_400_000,   # Switzerland c.1850
        "frag_duration_years": 208,  # 1291-1499
        "conflicts_per_decade": 2.0, # Burgundian Wars, Swabian War, Kappel Wars
        "collect_speed_years": 50,   # 1798-1848
        "durability_years": 176,     # 1848 to present (still unified)
        "maddison_codes": ["CHE"],
        "vdem_codes": ["CHE"],
        "sources": "Steinberg, Why Switzerland?; Church & Head, A Concise History of Switzerland",
        "notes": "Unique: collegial executive (Federal Council), no single head of state. Direct democracy tradition predates collectivization.",
    },

    # ================================================================
    # 2. BRAZIL: regional revolts -> centralized empire (1822-1889)
    # ================================================================
    {
        "name": "Brazil",
        "is_control": False,
        "pre_frag_year": 1808,       # Portuguese court arrives; colony gains autonomy
        "frag_peak_year": 1817,      # Pernambucan revolt (peak separatist threat)
        "first_integration_year": 1822,  # Pedro I declares independence
        "post_collect_year": 1845,   # Farroupilha (last major separatist revolt) ends

        # PRE: Portuguese colonial Brazil (pre-independence)
        # Single executive: 1 (Viceroy/Governor-General), hereditary: 1 (Portuguese crown),
        # independent militaries: 0, indep foreign policy: 0,
        # shared currency: 1 (real), shared legal code: 1 (Portuguese law),
        # unilateral exit: 0, central tax: 1,
        # popular sovereignty: 0, elected: 0,
        # free movement: 1, free goods: 0 (captaincy-level restrictions),
        # shared court: 1, central army: 1, preexisting: 1
        "features_pre": [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1],

        # POST: Empire of Brazil (consolidated under Pedro II)
        # Single executive: 1 (Emperor), hereditary: 1,
        # independent militaries: 0, indep foreign policy: 0,
        # shared currency: 1 (mil-reis), shared legal code: 1 (1824 Constitution),
        # unilateral exit: 0, central tax: 1,
        # popular sovereignty: 1 (constitutional monarchy, elected assembly),
        # elected: 1 (Chamber of Deputies),
        # free movement: 1, free goods: 1 (internal trade),
        # shared court: 1 (Supreme Court), central army: 1, preexisting: 1
        "features_post": [1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],

        "units_pre": 1,      # Colonial Brazil (unified colony)
        "units_peak": 6,     # ~6 major separatist movements (Pernambuco, Bahia, Para, Rio Grande do Sul, etc.)
        "units_post": 1,     # Empire of Brazil
        "pop_pre": 4_000_000,    # Brazil c.1808
        "pop_post": 8_000_000,   # Brazil c.1845
        "frag_duration_years": 9,    # 1808-1817
        "conflicts_per_decade": 8.0, # Multiple simultaneous revolts
        "collect_speed_years": 23,   # 1822-1845
        "durability_years": 144,     # 1845 to 1889 (republic) -> continuity to present = 179y
        "maddison_codes": ["BRA"],
        "vdem_codes": ["BRA"],
        "sources": "Bethell, The Cambridge History of Latin America; Barman, Citizen Emperor",
        "notes": "Colonial predecessor with high integration. Tests whether decolonization that preserves institutional form counts as restoration.",
    },

    # ================================================================
    # 3. GRAN COLOMBIA: Bolivar's republic (CONTROL - failed) (1819-1831)
    # ================================================================
    {
        "name": "Gran Colombia",
        "is_control": True,
        "pre_frag_year": 1808,       # Spanish colonial administration collapses
        "frag_peak_year": 1813,      # Multiple independent juntas across region
        "first_integration_year": 1819,  # Congress of Angostura
        "post_collect_year": 1821,   # Congress of Cucuta, constitution

        # PRE: Spanish Viceroyalty of New Granada
        # Single executive: 1 (Viceroy), hereditary: 1 (Spanish crown),
        # independent militaries: 0, indep foreign policy: 0,
        # shared currency: 1 (peso), shared legal code: 1 (Laws of the Indies),
        # unilateral exit: 0, central tax: 1,
        # popular sovereignty: 0, elected: 0,
        # free movement: 1, free goods: 0 (internal restrictions),
        # shared court: 1 (Audiencia), central army: 1, preexisting: 1
        "features_pre": [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1],

        # POST: Gran Colombia (short-lived republic)
        # Single executive: 1 (President/Liberator), hereditary: 0,
        # independent militaries: 1 (regional caudillos kept forces),
        # indep foreign policy: 0, shared currency: 1,
        # shared legal code: 1 (Cucuta constitution),
        # unilateral exit: 1 (and they did — Venezuela, Ecuador seceded),
        # central tax: 0 (couldn't collect effectively),
        # popular sovereignty: 1 (republican), elected: 1 (Congress),
        # free movement: 1, free goods: 0 (regional economies),
        # shared court: 1, central army: 0 (regional loyalties),
        # preexisting: 1
        "features_post": [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],

        "units_pre": 1,      # Viceroyalty of New Granada
        "units_peak": 8,     # ~8 independent juntas/provinces
        "units_post": 3,     # Venezuela, New Granada, Ecuador (nominally united)
        "pop_pre": 3_500_000,    # New Granada c.1808
        "pop_post": 2_500_000,   # Gran Colombia c.1821 (war losses)
        "frag_duration_years": 5,    # 1808-1813
        "conflicts_per_decade": 10.0, # Constant warfare
        "collect_speed_years": 2,    # 1819-1821 (very fast, too fast)
        "durability_years": 10,      # 1821-1831 (dissolved)
        "maddison_codes": ["COL", "VEN", "ECU"],
        "vdem_codes": ["COL", "VEN", "ECU"],
        "sources": "Lynch, Simon Bolivar; Bushnell, The Making of Modern Colombia",
        "notes": "CONTROL: Failed collectivization. Dissolved into Venezuela, Ecuador, and Colombia by 1831. Tests what happens when integration is too fast and too shallow.",
    },

    # ================================================================
    # 4. KOREA: Three Kingdoms -> Unified Silla (660-668 CE)
    # ================================================================
    {
        "name": "Korea (Silla)",
        "is_control": False,
        "pre_frag_year": -57,        # Traditional founding of Silla
        "frag_peak_year": 400,       # Three Kingdoms at height of competition
        "first_integration_year": 660,  # Silla-Tang alliance defeats Baekje
        "post_collect_year": 676,    # Silla expels Tang forces, full unification

        # PRE: Three Kingdoms system (Goguryeo, Baekje, Silla)
        # Single executive: 0 (three separate kings), hereditary: 1,
        # independent militaries: 1, indep foreign policy: 1,
        # shared currency: 0, shared legal code: 0,
        # unilateral exit: 1 (sovereign kingdoms), central tax: 0,
        # popular sovereignty: 0, elected: 0,
        # free movement: 0 (hostile borders), free goods: 0,
        # shared court: 0, central army: 0, preexisting: 1
        "features_pre": [0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],

        # POST: Unified Silla
        # Single executive: 1 (King), hereditary: 1 (bone rank system),
        # independent militaries: 0, indep foreign policy: 0,
        # shared currency: 0 (grain/cloth economy, limited coinage),
        # shared legal code: 1 (Chinese-influenced codes),
        # unilateral exit: 0, central tax: 1 (tribute/tax system),
        # popular sovereignty: 0, elected: 0,
        # free movement: 1, free goods: 1,
        # shared court: 1, central army: 1, preexisting: 1
        "features_post": [1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1],

        "units_pre": 3,      # Three Kingdoms
        "units_peak": 3,
        "units_post": 1,     # Unified Silla
        "pop_pre": 3_000_000,    # Korean peninsula c.400 CE
        "pop_post": 4_000_000,   # Unified Silla c.700 CE
        "frag_duration_years": 457,  # 57 BCE - 400 CE
        "conflicts_per_decade": 3.0,
        "collect_speed_years": 16,   # 660-676
        "durability_years": 259,     # 676-935 (Goryeo replaces)
        "maddison_codes": ["KOR"],
        "vdem_codes": ["KOR"],
        "sources": "Seth, A History of Korea; Lee, A New History of Korea",
        "notes": "Ancient case. Silla used Tang Chinese alliance for conquest then expelled Tang. KOR Maddison data may not cover pre-modern period.",
    },

    # ================================================================
    # 5. EGYPT: First Intermediate Period -> Middle Kingdom (2055-1985 BCE)
    # ================================================================
    {
        "name": "Egypt (Middle Kingdom)",
        "is_control": False,
        "pre_frag_year": -2181,      # Old Kingdom collapses
        "frag_peak_year": -2100,     # Multiple competing nomarchs
        "first_integration_year": -2055,  # Mentuhotep II conquers north
        "post_collect_year": -1985,  # Amenemhat I founds 12th Dynasty, full consolidation

        # PRE: Old Kingdom Egypt (before fragmentation)
        # Single executive: 1 (Pharaoh), hereditary: 1,
        # independent militaries: 0, indep foreign policy: 0,
        # shared currency: 0 (grain/barter economy), shared legal code: 1 (Ma'at + royal decree),
        # unilateral exit: 0, central tax: 1 (corvee + grain tax),
        # popular sovereignty: 0, elected: 0,
        # free movement: 1, free goods: 1 (Nile trade),
        # shared court: 1 (vizier's court), central army: 1, preexisting: 0
        "features_pre": [1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0],

        # POST: Middle Kingdom Egypt (12th Dynasty)
        # Single executive: 1 (Pharaoh), hereditary: 1,
        # independent militaries: 0, indep foreign policy: 0,
        # shared currency: 0 (still grain economy), shared legal code: 1,
        # unilateral exit: 0, central tax: 1,
        # popular sovereignty: 0, elected: 0,
        # free movement: 1, free goods: 1,
        # shared court: 1, central army: 1,
        # preexisting: 1 (nomarchs retained identity initially)
        "features_post": [1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1],

        "units_pre": 1,      # Old Kingdom (unified)
        "units_peak": 20,    # ~20 nomarchs ruling independently
        "units_post": 1,     # Middle Kingdom
        "pop_pre": 1_500_000,    # Egypt c.2200 BCE
        "pop_post": 2_000_000,   # Egypt c.2000 BCE
        "frag_duration_years": 81,   # 2181-2100 BCE
        "conflicts_per_decade": 3.0,
        "collect_speed_years": 70,   # 2055-1985 BCE
        "durability_years": 200,     # 1985-~1785 BCE (Second Intermediate)
        "maddison_codes": ["EGY"],
        "vdem_codes": [],   # no V-Dem for ancient period
        "sources": "Kemp, Ancient Egypt: Anatomy of a Civilization; Shaw, Oxford History of Ancient Egypt",
        "notes": "Ancient case. No GDP or V-Dem data. Restoration of pharaonic model after nomarch independence.",
    },

    # ================================================================
    # 6. ARGENTINA: fragmented provinces -> unified republic (1852-1880)
    # ================================================================
    {
        "name": "Argentina",
        "is_control": False,
        "pre_frag_year": 1810,       # May Revolution, Viceroyalty collapses
        "frag_peak_year": 1835,      # Rosas dominates but provinces remain autonomous
        "first_integration_year": 1852,  # Battle of Caseros, Urquiza defeats Rosas
        "post_collect_year": 1880,   # Buenos Aires federalized, Roca consolidates

        # PRE: Viceroyalty of the Rio de la Plata
        # Single executive: 1 (Viceroy), hereditary: 1 (Spanish crown),
        # independent militaries: 0, indep foreign policy: 0,
        # shared currency: 1 (peso), shared legal code: 1 (Laws of the Indies),
        # unilateral exit: 0, central tax: 1,
        # popular sovereignty: 0, elected: 0,
        # free movement: 1, free goods: 0 (internal restrictions),
        # shared court: 1 (Audiencia), central army: 1, preexisting: 1
        "features_pre": [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1],

        # POST: Argentine Republic (post-1880 consolidation)
        # Single executive: 1 (President), hereditary: 0,
        # independent militaries: 0, indep foreign policy: 0,
        # shared currency: 1 (peso), shared legal code: 1 (1853 Constitution + civil code),
        # unilateral exit: 0, central tax: 1,
        # popular sovereignty: 1 (republican), elected: 1 (elections),
        # free movement: 1, free goods: 1 (customs nationalized 1853),
        # shared court: 1, central army: 1, preexisting: 1
        "features_post": [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],

        "units_pre": 1,      # Viceroyalty
        "units_peak": 14,    # 14 provinces with caudillos
        "units_post": 1,     # Argentine Republic
        "pop_pre": 500_000,      # Rio de la Plata c.1810
        "pop_post": 2_500_000,   # Argentina c.1880
        "frag_duration_years": 25,   # 1810-1835
        "conflicts_per_decade": 7.0, # Civil wars nearly continuous
        "collect_speed_years": 28,   # 1852-1880
        "durability_years": 144,     # 1880 to present (with interruptions)
        "maddison_codes": ["ARG"],
        "vdem_codes": ["ARG"],
        "sources": "Rock, Argentina 1516-1987; Shumway, The Invention of Argentina",
        "notes": "Colonial predecessor. Buenos Aires vs interior provinces was the key axis of fragmentation.",
    },

    # ================================================================
    # 7. AUSTRALIA: separate colonies -> federation (1901)
    # ================================================================
    {
        "name": "Australia",
        "is_control": False,
        "pre_frag_year": 1788,       # First Fleet; single colony
        "frag_peak_year": 1859,      # Queensland separates; 6 colonies now independent
        "first_integration_year": 1891,  # First Federal Convention
        "post_collect_year": 1901,   # Commonwealth of Australia proclaimed

        # PRE: Separate British colonies
        # Single executive: 0 (6 separate governors), hereditary: 0 (governors appointed),
        # independent militaries: 1 (colonial defense forces),
        # indep foreign policy: 0 (all under British crown),
        # shared currency: 1 (pound sterling), shared legal code: 0 (separate colonial law),
        # unilateral exit: 1 (sovereign colonies), central tax: 0,
        # popular sovereignty: 1 (responsible government from 1850s),
        # elected: 1 (colonial parliaments),
        # free movement: 1, free goods: 0 (inter-colonial tariffs!),
        # shared court: 0 (separate supreme courts), central army: 0,
        # preexisting: 1
        "features_pre": [0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1],

        # POST: Commonwealth of Australia (1901)
        # Single executive: 1 (Governor-General/PM), hereditary: 0,
        # independent militaries: 0 (federal defense), indep foreign policy: 0,
        # shared currency: 1 (Australian pound), shared legal code: 0 (state law persists),
        # unilateral exit: 0 (no secession right), central tax: 1 (customs transferred to Commonwealth),
        # popular sovereignty: 1, elected: 1,
        # free movement: 1, free goods: 1 (Section 92: free interstate trade),
        # shared court: 1 (High Court of Australia), central army: 1,
        # preexisting: 1
        "features_post": [1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],

        "units_pre": 6,      # 6 colonies (NSW, VIC, QLD, SA, WA, TAS)
        "units_peak": 6,
        "units_post": 6,     # 6 states (federated, not merged)
        "pop_pre": 400_000,      # British colonies c.1850
        "pop_post": 3_800_000,   # Australia c.1901
        "frag_duration_years": 71,   # 1788-1859
        "conflicts_per_decade": 0.5, # Very low — federation was peaceful negotiation
        "collect_speed_years": 10,   # 1891-1901
        "durability_years": 123,     # 1901 to present
        "maddison_codes": ["AUS"],
        "vdem_codes": ["AUS"],
        "sources": "Hirst, The Sentimental Nation; Irving, To Constitute a Nation",
        "notes": "Peaceful federation through referenda. Very low conflict intensity. Tests whether violent fragmentation is necessary for collectivization.",
    },

    # ================================================================
    # 8. RUSSIA: Kievan Rus -> Muscovite centralization (1380-1547)
    # ================================================================
    {
        "name": "Russia (Muscovy)",
        "is_control": False,
        "pre_frag_year": 1054,       # Death of Yaroslav the Wise, Rus begins fragmenting
        "frag_peak_year": 1240,      # Mongol invasion; 15+ principalities under Mongol suzerainty
        "first_integration_year": 1380,  # Battle of Kulikovo, Moscow asserts dominance
        "post_collect_year": 1547,   # Ivan IV crowned Tsar

        # PRE: Kievan Rus (unified phase under Yaroslav)
        # Single executive: 1 (Grand Prince of Kiev), hereditary: 1,
        # independent militaries: 0, indep foreign policy: 0,
        # shared currency: 0 (limited coinage), shared legal code: 1 (Russkaya Pravda),
        # unilateral exit: 0, central tax: 1 (tribute system),
        # popular sovereignty: 0, elected: 0,
        # free movement: 1, free goods: 1 (Dnieper trade route),
        # shared court: 1, central army: 1, preexisting: 0
        "features_pre": [1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0],

        # POST: Tsardom of Russia (Ivan IV)
        # Single executive: 1 (Tsar), hereditary: 1,
        # independent militaries: 0, indep foreign policy: 0,
        # shared currency: 1 (Moscow ruble standardized), shared legal code: 1 (Sudebnik),
        # unilateral exit: 0, central tax: 1,
        # popular sovereignty: 0, elected: 0,
        # free movement: 0 (serfdom beginning to restrict), free goods: 1,
        # shared court: 1, central army: 1 (streltsy), preexisting: 1
        "features_post": [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1],

        "units_pre": 1,      # Kievan Rus (unified)
        "units_peak": 15,    # ~15 principalities
        "units_post": 1,     # Tsardom of Russia
        "pop_pre": 5_000_000,    # Kievan Rus c.1050
        "pop_post": 10_000_000,  # Muscovy c.1550
        "frag_duration_years": 186,  # 1054-1240
        "conflicts_per_decade": 4.0, # Inter-princely wars + Mongol rule
        "collect_speed_years": 167,  # 1380-1547
        "durability_years": 370,     # 1547-1917 (Revolution)
        "maddison_codes": ["RUS"],
        "vdem_codes": ["RUS"],
        "sources": "Fennell, The Crisis of Medieval Russia; Hosking, Russia and the Russians",
        "notes": "Under Mongol suzerainty during much of fragmentation. Moscow rose by serving as Mongol tax collector.",
    },

    # ================================================================
    # 9. INCA: rival polities -> Tawantinsuyu (1438-1533)
    # ================================================================
    {
        "name": "Inca (Tawantinsuyu)",
        "is_control": False,
        "pre_frag_year": 1200,       # Collapse of Wari/Tiwanaku empires
        "frag_peak_year": 1400,      # Dozens of competing polities in central Andes
        "first_integration_year": 1438,  # Pachacuti defeats Chanka, begins expansion
        "post_collect_year": 1493,   # Huayna Capac; Tawantinsuyu at maximum extent

        # PRE: Post-Wari/Tiwanaku fragmented polities
        # Single executive: 0 (many local kurakas/chiefs), hereditary: 1 (hereditary lords),
        # independent militaries: 1, indep foreign policy: 1,
        # shared currency: 0 (no currency), shared legal code: 0,
        # unilateral exit: 1, central tax: 0,
        # popular sovereignty: 0, elected: 0,
        # free movement: 0, free goods: 0 (hostile borders),
        # shared court: 0, central army: 0, preexisting: 1
        "features_pre": [0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],

        # POST: Inca Tawantinsuyu (Four Quarters)
        # Single executive: 1 (Sapa Inca), hereditary: 1,
        # independent militaries: 0, indep foreign policy: 0,
        # shared currency: 0 (no money — mit'a labor economy),
        # shared legal code: 1 (Inca law through quipu administration),
        # unilateral exit: 0, central tax: 1 (mit'a labor tax),
        # popular sovereignty: 0, elected: 0,
        # free movement: 1 (Qhapaq Nan road network), free goods: 1 (state redistribution),
        # shared court: 1 (Inca justice administered through tucuyricuc),
        # central army: 1, preexisting: 1
        "features_post": [1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1],

        "units_pre": 5,      # ~5 major polities (Chimu, Chanka, Lupaka, Colla, early Inca)
        "units_peak": 20,    # ~20 competing polities at peak fragmentation
        "units_post": 1,     # Tawantinsuyu
        "pop_pre": 6_000_000,    # Central Andes c.1200
        "pop_post": 12_000_000,  # Tawantinsuyu c.1500
        "frag_duration_years": 200,  # 1200-1400
        "conflicts_per_decade": 4.0,
        "collect_speed_years": 55,   # 1438-1493
        "durability_years": 40,      # 1493-1533 (Spanish conquest)
        "maddison_codes": ["PER"],
        "vdem_codes": [],   # no V-Dem for pre-Columbian
        "sources": "D'Altroy, The Incas; McEwan, The Incas: New Perspectives",
        "notes": "No monetary economy (mit'a labor system). Extremely rapid expansion but short durability (Spanish conquest as exogenous shock).",
    },

    # ================================================================
    # 10. CANADA: separate colonies -> Confederation (1867)
    # ================================================================
    {
        "name": "Canada",
        "is_control": False,
        "pre_frag_year": 1791,       # Constitutional Act splits Upper/Lower Canada
        "frag_peak_year": 1841,      # Act of Union reunites the Canadas; other colonies separate
        "first_integration_year": 1864,  # Charlottetown Conference
        "post_collect_year": 1871,   # British Columbia joins; PEI 1873

        # PRE: Separate British North American colonies
        # Single executive: 0 (separate governors), hereditary: 0 (appointed),
        # independent militaries: 1 (colonial militia),
        # indep foreign policy: 0 (British crown),
        # shared currency: 1 (pound sterling / Canadian dollar from 1858),
        # shared legal code: 0 (Upper Canada common law, Lower Canada civil law),
        # unilateral exit: 1 (separate colonies), central tax: 0,
        # popular sovereignty: 1 (responsible government from 1848),
        # elected: 1 (colonial assemblies),
        # free movement: 1, free goods: 0 (inter-colonial tariffs),
        # shared court: 0, central army: 0, preexisting: 1
        "features_pre": [0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1],

        # POST: Dominion of Canada (1871, with BC)
        # Single executive: 1 (Governor General/PM), hereditary: 0,
        # independent militaries: 0 (federal militia), indep foreign policy: 0 (British until 1931),
        # shared currency: 1 (Canadian dollar), shared legal code: 0 (Quebec civil law persists),
        # unilateral exit: 0, central tax: 1 (customs + excise transferred),
        # popular sovereignty: 1, elected: 1 (House of Commons + Senate),
        # free movement: 1, free goods: 1 (Section 121: free interprovincial trade),
        # shared court: 1 (Supreme Court from 1875), central army: 1,
        # preexisting: 1
        "features_post": [1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],

        "units_pre": 5,      # Canada (United), Nova Scotia, New Brunswick, PEI, BC + Rupert's Land
        "units_peak": 6,
        "units_post": 5,     # 4 provinces in 1867, BC 1871 (grew to 10)
        "pop_pre": 2_500_000,    # British North America c.1860
        "pop_post": 3_700_000,   # Canada c.1871
        "frag_duration_years": 50,   # 1791-1841
        "conflicts_per_decade": 1.0, # Very low — Rebellions of 1837-38 only major violence
        "collect_speed_years": 7,    # 1864-1871
        "durability_years": 153,     # 1871 to present
        "maddison_codes": ["CAN"],
        "vdem_codes": ["CAN"],
        "sources": "Martin, Britain and the Origins of Canadian Confederation; Creighton, The Road to Confederation",
        "notes": "Like Australia, peaceful federation. Dual legal system (common law + Quebec civil law) preserved. Very fast collectivization.",
    },
]


def build_all():
    os.makedirs(CASES_DIR, exist_ok=True)

    for spec in SPECS:
        name = spec["name"]
        slug = name.lower().replace(" ", "_").replace("(", "").replace(")", "")
        slug = slug.replace("-", "_")
        out_path = os.path.join(CASES_DIR, f"exp2_{slug}.json")

        mcodes = spec.get("maddison_codes", [])
        gdp_growth_pre = None
        gdp_growth_post = None
        combined_gdp = {}

        for code in mcodes:
            series = load_gdp_series(code)
            combined_gdp.update(series)

        if combined_gdp:
            pre_start = spec["pre_frag_year"] - 30
            pre_end = spec["pre_frag_year"]
            post_start = spec["post_collect_year"]
            post_end = spec["post_collect_year"] + 30
            gdp_growth_pre = avg_annual_growth(combined_gdp, pre_start, pre_end)
            gdp_growth_post = avg_annual_growth(combined_gdp, post_start, post_end)

        vcodes = spec.get("vdem_codes", [])
        combined_vdem = {}
        for code in vcodes:
            series = load_vdem_series(code)
            combined_vdem.update(series)

        case = {
            "name": name,
            "is_control": spec["is_control"],
            "pre_frag_year": spec["pre_frag_year"],
            "frag_peak_year": spec["frag_peak_year"],
            "first_integration_year": spec["first_integration_year"],
            "post_collect_year": spec["post_collect_year"],
            "features_pre": spec["features_pre"],
            "features_post": spec["features_post"],
            "units_pre": spec["units_pre"],
            "units_peak": spec["units_peak"],
            "units_post": spec["units_post"],
            "pop_pre": spec["pop_pre"],
            "pop_post": spec["pop_post"],
            "gdp_growth_pre": gdp_growth_pre,
            "gdp_growth_post": gdp_growth_post,
            "frag_duration_years": spec["frag_duration_years"],
            "conflicts_per_decade": spec["conflicts_per_decade"],
            "collect_speed_years": spec["collect_speed_years"],
            "durability_years": spec["durability_years"],
            "gdp_series": {str(y): v for y, v in combined_gdp.items()},
            "vdem_series": {str(y): v for y, v in combined_vdem.items()},
            "sources": spec.get("sources", ""),
            "notes": spec.get("notes", ""),
        }

        with open(out_path, "w") as f:
            json.dump(case, f, indent=2)
        print(f"  wrote {out_path}")

    print(f"\nbuilt {len(SPECS)} expansion-2 cases")


if __name__ == "__main__":
    build_all()
