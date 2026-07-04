"""
Build the 10 expansion case JSONs from hardcoded historical facts + Maddison/V-Dem.

These 10 cases were randomly selected (seed=42) from a 20-case candidate pool
to avoid cherry-picking bias. The candidate pool spans all continents and 3,000+
years of history. Selection was done before any feature vectors were coded.

Feature vector encoding rules (same as original 10 cases):
  - Each feature is a verifiable fact from constitutional documents, treaties,
    or observable institutional structure AT THE DATE specified.
  - features_pre: the governance structure of the pre-fragmentation entity
  - features_post: the governance structure of the post-collectivization entity
  - All 15 features are binary (0/1), no subjective judgment.

Run:  python -m ingest.build_expansion_cases
From: studies/5_collectivization/
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from ingest_maddison import load_gdp_series, avg_annual_growth, gdp_subseries
from ingest_vdem import load_vdem_series, vdem_subseries

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
    # 1. NETHERLANDS: Habsburg provinces -> Dutch Republic (1568-1648)
    # ================================================================
    {
        "name": "Netherlands",
        "is_control": False,
        "pre_frag_year": 1548,       # Pragmatic Sanction unifies 17 provinces
        "frag_peak_year": 1576,      # Sack of Antwerp, Pacification of Ghent
        "first_integration_year": 1579,  # Union of Utrecht
        "post_collect_year": 1648,   # Peace of Westphalia, independence recognized

        # PRE: Habsburg composite monarchy over 17 provinces
        # Single executive (governor-general): 1, hereditary (Habsburg): 1,
        # independent militaries (provincial): 1, indep foreign policy: 0 (Habsburg crown),
        # shared currency (partially): 0, shared legal code: 0 (each province own law),
        # unilateral exit: 0 (Habsburg wouldn't allow), central tax: 1 (Habsburg levies),
        # popular sovereignty: 0, elected leadership: 0,
        # free movement persons: 1, free movement goods: 0 (internal tolls),
        # shared supreme court: 0 (Great Council but limited), central standing army: 1,
        # preexisting polities: 1
        "features_pre": [1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],

        # POST: Dutch Republic (7 United Provinces)
        # Single executive: 0 (Stadtholder not supreme, States-General sovereign),
        # hereditary: 0 (Stadtholder quasi-hereditary but not executive),
        # independent militaries: 1 (provincial forces), indep foreign policy: 0 (States-General),
        # shared currency: 1 (guilder), shared legal code: 0 (provincial law),
        # unilateral exit: 1 (sovereign provinces), central tax: 0 (quota system),
        # popular sovereignty: 1 (sovereignty from the people via abjuration),
        # elected leadership: 1 (States-General delegates), free movement persons: 1,
        # free movement goods: 1 (internal free trade), shared supreme court: 0,
        # central standing army: 0 (provincial forces under Stadtholder), preexisting: 1
        "features_post": [0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1],

        "units_pre": 17,    # 17 provinces under Pragmatic Sanction
        "units_peak": 17,   # All 17 initially rebel
        "units_post": 7,    # 7 United Provinces
        "pop_pre": 3_000_000,   # ~3M in all 17 provinces c.1550
        "pop_post": 1_900_000,  # ~1.9M in the 7 northern provinces c.1650
        "frag_duration_years": 28,   # 1548-1576
        "conflicts_per_decade": 8.0, # Eighty Years War, constant
        "collect_speed_years": 69,   # 1579-1648
        "durability_years": 207,     # Republic to 1795 (Batavian)
        "maddison_codes": ["NLD"],
        "vdem_codes": ["NLD"],
        "sources": "Parker, The Dutch Revolt; Israel, The Dutch Republic",
        "notes": "Unusual case: collectivization produces a smaller entity (7 of 17 provinces). Tests whether the ratchet applies even with territorial shrinkage.",
    },

    # ================================================================
    # 2. SPAIN: Reconquista kingdoms -> unified crown (1469-1516)
    # ================================================================
    {
        "name": "Spain",
        "is_control": False,
        "pre_frag_year": 711,        # Muslim conquest shatters Visigothic kingdom
        "frag_peak_year": 1031,      # Caliphate of Cordoba fragments into taifas
        "first_integration_year": 1230, # Castile-Leon permanent union
        "post_collect_year": 1516,   # Charles I unites all crowns

        # PRE: Visigothic Kingdom (pre-711)
        # Single executive (king): 1, hereditary: 1, independent militaries: 0,
        # indep foreign policy: 0, shared currency: 1, shared legal code: 1 (Liber Iudiciorum),
        # unilateral exit: 0, central tax: 1, popular sovereignty: 0, elected: 0,
        # free movement: 1, free goods: 1, shared court: 1, central army: 1, preexisting: 0
        "features_pre": [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0],

        # POST: United Spain under Ferdinand & Isabella / Charles I
        # Single executive: 1, hereditary: 1, independent militaries: 0,
        # indep foreign policy: 0, shared currency: 1 (maravedi/real),
        # shared legal code: 0 (Castile/Aragon kept separate codes),
        # unilateral exit: 0, central tax: 1, popular sovereignty: 0, elected: 0,
        # free movement: 0 (internal borders persisted between crowns),
        # free goods: 0 (internal customs between Castile/Aragon),
        # shared court: 0 (separate royal councils), central army: 1, preexisting: 1
        "features_post": [1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],

        "units_pre": 1,      # Visigothic Kingdom
        "units_peak": 30,    # ~5 Christian kingdoms + ~25 taifas at peak
        "units_post": 1,     # United Spain (though composite monarchy)
        "pop_pre": 4_000_000,    # Visigothic Hispania c.700
        "pop_post": 6_800_000,   # Spain c.1516
        "frag_duration_years": 320,  # 711-1031
        "conflicts_per_decade": 4.0, # Reconquista was near-constant
        "collect_speed_years": 286,  # 1230-1516 (slow integration)
        "durability_years": 508,     # 1516 to present (still unified)
        "maddison_codes": ["ESP"],
        "vdem_codes": ["ESP"],
        "sources": "O'Callaghan, A History of Medieval Spain; Elliott, Imperial Spain",
        "notes": "Very long fragmentation and very long collectivization. Composite monarchy kept separate legal systems — tests form-shift with incomplete integration.",
    },

    # ================================================================
    # 3. INDIA (MUGHAL): post-Delhi Sultanate -> Mughal Empire (1526-1605)
    # ================================================================
    {
        "name": "India (Mughal)",
        "is_control": False,
        "pre_frag_year": 1398,       # Timur sacks Delhi, Sultanate collapses
        "frag_peak_year": 1451,      # Delhi Sultanate reduced to rump; 5+ successor states
        "first_integration_year": 1526, # Babur defeats Ibrahim Lodi at Panipat
        "post_collect_year": 1605,   # Akbar's death; Mughal dominion covers most of subcontinent

        # PRE: Delhi Sultanate (pre-Timur)
        # Single executive (Sultan): 1, hereditary: 1 (dynastic but contested),
        # independent militaries: 0, indep foreign policy: 0,
        # shared currency: 1 (tanka), shared legal code: 1 (sharia + sultanate law),
        # unilateral exit: 0, central tax: 1 (iqta system),
        # popular sovereignty: 0, elected: 0, free movement: 1, free goods: 1,
        # shared court: 1, central army: 1, preexisting: 1
        "features_pre": [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1],

        # POST: Mughal Empire under Akbar
        # Single executive (Emperor): 1, hereditary: 1,
        # independent militaries: 0, indep foreign policy: 0,
        # shared currency: 1 (rupee), shared legal code: 1 (Akbar's Din-i-Ilahi + codified law),
        # unilateral exit: 0, central tax: 1 (mansabdari),
        # popular sovereignty: 0, elected: 0, free movement: 1, free goods: 1,
        # shared court: 1, central army: 1, preexisting: 1
        "features_post": [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1],

        "units_pre": 1,      # Delhi Sultanate (unified)
        "units_peak": 15,    # Jaunpur, Malwa, Gujarat, Bahmani, Bengal, etc. + Hindu kingdoms
        "units_post": 1,     # Mughal Empire
        "pop_pre": 100_000_000,  # India c.1400
        "pop_post": 150_000_000, # India c.1600
        "frag_duration_years": 53,  # 1398-1451
        "conflicts_per_decade": 5.0,
        "collect_speed_years": 79,  # 1526-1605
        "durability_years": 154,    # 1605 to 1759 (Battle of Plassey / effective end)
        "maddison_codes": ["IND"],
        "vdem_codes": ["IND"],
        "sources": "Richards, The Mughal Empire; Asher & Talbot, India Before Europe",
        "notes": "Unusual case: pre and post feature vectors are nearly identical. Tests whether form-shift is required for successful collectivization, or if restoration is possible.",
    },

    # ================================================================
    # 4. INDIA (MAURYA): Mahajanapadas -> Mauryan Empire (322-185 BCE)
    # ================================================================
    {
        "name": "India (Maurya)",
        "is_control": False,
        "pre_frag_year": -600,
        "frag_peak_year": -500,     # 16 Mahajanapadas competing
        "first_integration_year": -322,  # Chandragupta defeats Nanda dynasty
        "post_collect_year": -260,  # Ashoka's consolidation after Kalinga

        # PRE: Mahajanapada system (fragmented kingdoms/republics)
        # Single executive: 0 (some monarchies, some ganas/republics),
        # hereditary: 0 (mixed), independent militaries: 1, indep foreign policy: 1,
        # shared currency: 0, shared legal code: 0, unilateral exit: 1,
        # central tax: 0, popular sovereignty: 0 (some ganas had assemblies but not dominant),
        # elected: 0, free movement: 0, free goods: 0, shared court: 0,
        # central army: 0, preexisting: 1
        "features_pre": [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],

        # POST: Mauryan Empire under Ashoka
        # Single executive (Samrat): 1, hereditary: 1,
        # independent militaries: 0, indep foreign policy: 0,
        # shared currency: 1 (punch-marked coins standardized),
        # shared legal code: 1 (Arthashastra + Ashoka's edicts),
        # unilateral exit: 0, central tax: 1 (elaborate system per Arthashastra),
        # popular sovereignty: 0, elected: 0,
        # free movement: 1, free goods: 1 (extensive road network, trade),
        # shared court: 1 (dharmamahamatras), central army: 1, preexisting: 1
        "features_post": [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1],

        "units_pre": 16,     # 16 Mahajanapadas
        "units_peak": 16,
        "units_post": 1,     # Mauryan Empire
        "pop_pre": 30_000_000,   # Indian subcontinent c.500 BCE (rough)
        "pop_post": 50_000_000,  # Mauryan Empire c.260 BCE
        "frag_duration_years": 100,  # c.600-500 BCE
        "conflicts_per_decade": 4.0,
        "collect_speed_years": 62,   # 322-260 BCE
        "durability_years": 137,     # 322-185 BCE
        "maddison_codes": ["IND"],
        "vdem_codes": [],   # no V-Dem for ancient period
        "sources": "Thapar, Ashoka and the Decline of the Mauryas; Olivelle, King Governance and Law",
        "notes": "Ancient case. No V-Dem or GDP data available. Feature vectors are the primary data.",
    },

    # ================================================================
    # 5. ZULU: Nguni chiefdoms -> Zulu Kingdom (1816-1828)
    # ================================================================
    {
        "name": "Zulu Kingdom",
        "is_control": False,
        "pre_frag_year": 1750,
        "frag_peak_year": 1810,     # Dozens of competing Nguni chiefdoms
        "first_integration_year": 1816,  # Shaka becomes chief of the Zulu
        "post_collect_year": 1828,  # Shaka's death; kingdom consolidated

        # PRE: Nguni chiefdom system
        # Single executive: 0 (each chief independent), hereditary: 1 (chieftaincy hereditary),
        # independent militaries: 1 (each chiefdom), indep foreign policy: 1,
        # shared currency: 0, shared legal code: 0 (customary, local),
        # unilateral exit: 1, central tax: 0, popular sovereignty: 0, elected: 0,
        # free movement: 1 (no hard borders), free goods: 1 (cattle trade),
        # shared court: 0, central army: 0, preexisting: 1
        "features_pre": [0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1],

        # POST: Zulu Kingdom under Shaka/Dingane
        # Single executive (king): 1, hereditary: 1,
        # independent militaries: 0 (amabutho system, central), indep foreign policy: 0,
        # shared currency: 0 (cattle economy), shared legal code: 1 (king's law),
        # unilateral exit: 0, central tax: 1 (tribute/labor),
        # popular sovereignty: 0, elected: 0, free movement: 1, free goods: 1,
        # shared court: 1 (king's court final arbiter), central army: 1, preexisting: 1
        "features_post": [1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1],

        "units_pre": 2,      # Pre-mfecane, a few major clans
        "units_peak": 30,    # Dozens of competing chiefdoms during mfecane
        "units_post": 1,     # Zulu Kingdom
        "pop_pre": 100_000,      # Nguni peoples in the region c.1750
        "pop_post": 250_000,     # Zulu Kingdom c.1828
        "frag_duration_years": 60,   # 1750-1810
        "conflicts_per_decade": 6.0, # mfecane was extremely violent
        "collect_speed_years": 12,   # 1816-1828 (very fast)
        "durability_years": 51,      # 1828-1879 (Anglo-Zulu War)
        "maddison_codes": ["ZAF"],
        "vdem_codes": ["ZAF"],
        "sources": "Laband, The Rise and Fall of the Zulu Nation; Wylie, Myth of Iron",
        "notes": "Very rapid collectivization. Small scale. ZAF Maddison data starts at 1700 but represents different polities.",
    },

    # ================================================================
    # 6. POLAND-LITHUANIA: fragmented duchies -> Commonwealth (1320-1569)
    # ================================================================
    {
        "name": "Poland-Lithuania",
        "is_control": False,
        "pre_frag_year": 1138,       # Testament of Boleslaw III fragments Poland
        "frag_peak_year": 1295,      # ~10 competing Piast duchies
        "first_integration_year": 1320,  # Wladyslaw I reunifies core Poland
        "post_collect_year": 1569,   # Union of Lublin creates Commonwealth

        # PRE: Piast Kingdom of Poland (pre-1138)
        # Single executive: 1, hereditary: 1, independent militaries: 0,
        # indep foreign policy: 0, shared currency: 1 (denar),
        # shared legal code: 1, unilateral exit: 0, central tax: 1,
        # popular sovereignty: 0, elected: 0, free movement: 1, free goods: 1,
        # shared court: 1, central army: 1, preexisting: 0
        "features_pre": [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0],

        # POST: Polish-Lithuanian Commonwealth
        # Single executive: 1 (king), hereditary: 0 (elected monarchy!),
        # independent militaries: 0, indep foreign policy: 0,
        # shared currency: 1 (zloty), shared legal code: 0 (Poland/Lithuania separate codes),
        # unilateral exit: 0 (after Lublin), central tax: 0 (Sejm controlled, weak),
        # popular sovereignty: 1 (szlachta sovereignty), elected: 1 (royal elections),
        # free movement: 1, free goods: 1,
        # shared court: 0 (separate tribunals), central army: 0 (pospolite ruszenie, weak),
        # preexisting: 1
        "features_post": [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1],

        "units_pre": 1,      # Unified Piast Poland
        "units_peak": 10,    # ~10 Piast duchies + Teutonic Order
        "units_post": 1,     # Commonwealth (dual state)
        "pop_pre": 2_000_000,    # Poland c.1138
        "pop_post": 11_000_000,  # Commonwealth c.1569
        "frag_duration_years": 157,  # 1138-1295
        "conflicts_per_decade": 3.0,
        "collect_speed_years": 249,  # 1320-1569 (very slow)
        "durability_years": 226,     # 1569-1795 (Third Partition)
        "maddison_codes": ["POL"],
        "vdem_codes": ["POL"],
        "sources": "Davies, God's Playground; Frost, The Oxford History of Poland-Lithuania",
        "notes": "Unique elected monarchy. Tests whether democratic legitimacy features appear through collectivization even in pre-modern contexts.",
    },

    # ================================================================
    # 7. PERSIA (SAFAVID): post-Timurid beyliks -> Safavid Empire (1501-1588)
    # ================================================================
    {
        "name": "Persia (Safavid)",
        "is_control": False,
        "pre_frag_year": 1405,       # Timur dies, empire fragments
        "frag_peak_year": 1468,      # Aq Qoyunlu vs Qara Qoyunlu peak competition
        "first_integration_year": 1501,  # Ismail I conquers Tabriz
        "post_collect_year": 1588,   # Abbas I begins reign, full consolidation

        # PRE: Timurid Empire (pre-fragmentation)
        # Single executive: 1, hereditary: 1, independent militaries: 0,
        # indep foreign policy: 0, shared currency: 1, shared legal code: 1 (sharia + yasa),
        # unilateral exit: 0, central tax: 1, popular sovereignty: 0, elected: 0,
        # free movement: 1, free goods: 1, shared court: 1, central army: 1, preexisting: 1
        "features_pre": [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1],

        # POST: Safavid Empire under Abbas I
        # Single executive (Shah): 1, hereditary: 1,
        # independent militaries: 0, indep foreign policy: 0,
        # shared currency: 1 (Safavid tuman), shared legal code: 1 (sharia + urf),
        # unilateral exit: 0, central tax: 1 (crown lands + tuyul),
        # popular sovereignty: 0, elected: 0,
        # free movement: 1, free goods: 1 (active trade policy),
        # shared court: 1, central army: 1 (ghulam slave soldiers), preexisting: 1
        "features_post": [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1],

        "units_pre": 1,      # Timurid Empire
        "units_peak": 12,    # Aq Qoyunlu, Qara Qoyunlu, Timurids, local dynasties
        "units_post": 1,     # Safavid Empire
        "pop_pre": 10_000_000,   # Greater Iran c.1400
        "pop_post": 10_000_000,  # Safavid Iran c.1588 (roughly same, post-Mongol recovery)
        "frag_duration_years": 63,   # 1405-1468
        "conflicts_per_decade": 5.0,
        "collect_speed_years": 87,   # 1501-1588
        "durability_years": 134,     # 1588-1722 (Afghan invasion)
        "maddison_codes": ["IRN"],
        "vdem_codes": ["IRN"],
        "sources": "Savory, Iran Under the Safavids; Newman, Safavid Iran",
        "notes": "Like Mughal India, pre/post vectors are nearly identical — tests restoration vs. form-shift.",
    },

    # ================================================================
    # 8. FRANCE: feudal fragmentation -> Bourbon centralization
    # ================================================================
    {
        "name": "France",
        "is_control": False,
        "pre_frag_year": 843,        # Treaty of Verdun splits Carolingian Empire
        "frag_peak_year": 987,       # Capetian takeover, royal domain tiny
        "first_integration_year": 1214,  # Battle of Bouvines, Philip II dominates
        "post_collect_year": 1661,   # Louis XIV personal rule, full centralization

        # PRE: Carolingian Western Francia
        # Single executive: 1, hereditary: 1, independent militaries: 0,
        # indep foreign policy: 0, shared currency: 1 (denier),
        # shared legal code: 1 (capitularies), unilateral exit: 0,
        # central tax: 1, popular sovereignty: 0, elected: 0,
        # free movement: 1, free goods: 1, shared court: 1, central army: 1,
        # preexisting: 0
        "features_pre": [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0],

        # POST: France under Louis XIV
        # Single executive: 1, hereditary: 1, independent militaries: 0,
        # indep foreign policy: 0, shared currency: 1 (livre),
        # shared legal code: 0 (northern coutume vs southern Roman law, not unified until Napoleon),
        # unilateral exit: 0, central tax: 1 (taille, gabelle),
        # popular sovereignty: 0, elected: 0,
        # free movement: 0 (internal passport/travel restrictions),
        # free goods: 0 (internal customs barriers — the cinq grosses fermes),
        # shared court: 1 (parlements), central army: 1 (standing army from 1445),
        # preexisting: 1 (provinces retained identity)
        "features_post": [1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1],

        "units_pre": 1,      # West Francia
        "units_peak": 30,    # ~30 effectively independent fiefs/duchies c.987
        "units_post": 1,     # Kingdom of France
        "pop_pre": 6_000_000,    # West Francia c.843
        "pop_post": 20_000_000,  # France c.1661
        "frag_duration_years": 144,  # 843-987
        "conflicts_per_decade": 4.0, # Hundred Years War, religious wars, constant feudal warfare
        "collect_speed_years": 447,  # 1214-1661 (extremely slow)
        "durability_years": 128,     # 1661-1789 (Revolution)
        "maddison_codes": ["FRA"],
        "vdem_codes": ["FRA"],
        "sources": "Dunbabin, France in the Making; Treasure, The Making of Modern Europe",
        "notes": "Slowest collectivization in the pool (447 years). Tests whether speed correlates with fragmentation intensity.",
    },

    # ================================================================
    # 9. VIETNAM: Trinh-Nguyen division -> Nguyen unification (1771-1802)
    # ================================================================
    {
        "name": "Vietnam",
        "is_control": False,
        "pre_frag_year": 1527,       # Mac dynasty usurps Le throne
        "frag_peak_year": 1672,      # Trinh-Nguyen civil war stalemate
        "first_integration_year": 1771,  # Tay Son rebellion begins unification
        "post_collect_year": 1802,   # Gia Long (Nguyen Anh) unifies Vietnam

        # PRE: Le dynasty unified Vietnam (pre-1527)
        # Single executive: 1 (Emperor), hereditary: 1,
        # independent militaries: 0, indep foreign policy: 0,
        # shared currency: 1, shared legal code: 1 (Hong Duc code),
        # unilateral exit: 0, central tax: 1,
        # popular sovereignty: 0, elected: 0 (but Confucian mandate of heaven),
        # free movement: 1, free goods: 1, shared court: 1, central army: 1,
        # preexisting: 0
        "features_pre": [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0],

        # POST: Nguyen dynasty unified Vietnam (Gia Long)
        # Single executive: 1, hereditary: 1,
        # independent militaries: 0, indep foreign policy: 0,
        # shared currency: 1, shared legal code: 1 (Gia Long Code/Hoang Viet Luat Le),
        # unilateral exit: 0, central tax: 1 (mandarin system),
        # popular sovereignty: 0, elected: 0,
        # free movement: 1, free goods: 1, shared court: 1, central army: 1,
        # preexisting: 1 (Trinh/Nguyen/Champa territories had separate identities)
        "features_post": [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1],

        "units_pre": 1,       # Le dynasty Vietnam
        "units_peak": 4,      # Trinh domain, Nguyen domain, Mac remnant, Champa
        "units_post": 1,      # Nguyen dynasty
        "pop_pre": 5_000_000,     # Vietnam c.1527
        "pop_post": 8_000_000,    # Vietnam c.1802
        "frag_duration_years": 145,  # 1527-1672
        "conflicts_per_decade": 3.0,
        "collect_speed_years": 31,   # 1771-1802
        "durability_years": 83,      # 1802-1885 (French protectorate)
        "maddison_codes": ["VNM"],
        "vdem_codes": ["VNM"],
        "sources": "Taylor, A History of the Vietnamese; Dutton et al., Sources of Vietnamese Tradition",
        "notes": "Pre/post nearly identical — another restoration case. VNM Maddison data starts 1820, V-Dem starts 1976 (limited).",
    },

    # ================================================================
    # 10. ETHIOPIA: Zemene Mesafint -> Tewodros II reunification (1855-1889)
    # ================================================================
    {
        "name": "Ethiopia",
        "is_control": False,
        "pre_frag_year": 1706,       # Iyasu I assassinated, imperial authority collapses
        "frag_peak_year": 1800,      # Regional lords (Ras) completely dominate
        "first_integration_year": 1855,  # Tewodros II crowned Emperor
        "post_collect_year": 1889,   # Menelik II consolidates, defeats Italy at Adwa (1896)

        # PRE: Solomonic Empire (strong phase, pre-Zemene Mesafint)
        # Single executive: 1, hereditary: 1 (Solomonic dynasty),
        # independent militaries: 0, indep foreign policy: 0,
        # shared currency: 0 (largely barter/salt bars), shared legal code: 1 (Fetha Nagast),
        # unilateral exit: 0, central tax: 1 (tribute from provinces),
        # popular sovereignty: 0, elected: 0,
        # free movement: 1, free goods: 1, shared court: 1, central army: 1,
        # preexisting: 1
        "features_pre": [1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1],

        # POST: Ethiopian Empire under Menelik II
        # Single executive: 1, hereditary: 1,
        # independent militaries: 0 (Menelik controlled), indep foreign policy: 0,
        # shared currency: 1 (Maria Theresa thaler + birr from 1894),
        # shared legal code: 1 (Fetha Nagast + Menelik's proclamations),
        # unilateral exit: 0, central tax: 1,
        # popular sovereignty: 0, elected: 0,
        # free movement: 1, free goods: 1,
        # shared court: 1, central army: 1 (modernized), preexisting: 1
        "features_post": [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1],

        "units_pre": 1,      # Solomonic Empire (unified)
        "units_peak": 8,     # ~8 major Ras (regional lords) + emperor as figurehead
        "units_post": 1,     # Ethiopian Empire
        "pop_pre": 5_000_000,    # Ethiopia c.1706
        "pop_post": 12_000_000,  # Ethiopia c.1889
        "frag_duration_years": 94,   # 1706-1800
        "conflicts_per_decade": 4.0,
        "collect_speed_years": 34,   # 1855-1889
        "durability_years": 85,      # 1889-1974 (Derg revolution)
        "maddison_codes": ["ETH"],
        "vdem_codes": ["ETH"],
        "sources": "Henze, Layers of Time; Marcus, A History of Ethiopia",
        "notes": "Zemene Mesafint (Era of Princes). Emperor existed but was a puppet — de facto fragmentation without formal dissolution.",
    },
]


def build_all():
    os.makedirs(CASES_DIR, exist_ok=True)

    for spec in SPECS:
        name = spec["name"]
        slug = name.lower().replace(" ", "_").replace("(", "").replace(")", "")
        slug = slug.replace("-", "_")
        out_path = os.path.join(CASES_DIR, f"exp_{slug}.json")

        # GDP growth rates
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

        # V-Dem series
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

    print(f"\nbuilt {len(SPECS)} expansion cases")


if __name__ == "__main__":
    build_all()
