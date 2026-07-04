"""
Build the 10 case profiles (6 core + 4 controls) from hardcoded historical
facts + computed GDP/V-Dem time series from existing repo datasets.

DATA TIER -- CURATED (same as census/governance/state_dissolutions.py).
Feature vectors, unit counts, dates, and population figures are coded from
standard historical references. GDP growth rates and V-Dem series are computed
from the committed Maddison and V-Dem datasets.

Run:  python -m ingest.build_cases   (from studies/5_collectivization/)

Writes one JSON per case to cases/.
"""

from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)

from ingest_maddison import (
    load_gdp_series, avg_annual_growth, gdp_subseries, multi_country_growth,
)
from ingest_vdem import vdem_subseries, multi_country_vdem

CASES_DIR = os.path.join(HERE, "..", "cases")

# ── hardcoded case specifications ──────────────────────────────────────
# Each tuple: (name, is_control, pre_frag_year, frag_peak_year,
#              first_integration_year, post_collect_year,
#              features_pre, features_post,
#              units_pre, units_peak, units_post,
#              pop_pre, pop_post,
#              conflicts_per_decade,
#              iso3_for_gdp, iso3_for_vdem,
#              sources, notes)

SPECS = [
    # ── CORE CASES ──
    {
        "name": "Germany",
        "is_control": False,
        "pre_frag_year": 1806,
        "frag_peak_year": 1815,
        "first_integration_year": 1834,
        "post_collect_year": 1871,
        "features_pre":  [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
        "features_post": [1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        "units_pre": 300,
        "units_peak": 39,
        "units_post": 25,
        "pop_pre": 24_000_000,
        "pop_post": 41_000_000,
        "conflicts_per_decade": 1.5,
        "iso3_gdp": "DEU",
        "iso3_vdem": "DEU",
        "sources": "HRE dissolution 1806; German Confederation (39 states) 1815; "
                   "Zollverein 1834; German Empire 1871 (25 constituent states). "
                   "Pop: Maddison/historical demography. Conflicts: Napoleonic Wars, "
                   "1848 revolutions, Austro-Prussian War, Franco-Prussian War.",
        "notes": "Features_pre coded for HRE ~1800 (feudal order with weak center). "
                 "Feature 12 (shared court) = 1 because Reichskammergericht existed. "
                 "Features_post coded for German Empire 1871 (federal empire with "
                 "strong central institutions but constituent monarchies retained).",
    },
    {
        "name": "Italy",
        "is_control": False,
        "pre_frag_year": 1494,
        "frag_peak_year": 1559,
        "first_integration_year": 1848,
        "post_collect_year": 1861,
        "features_pre":  [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        "features_post": [1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
        "units_pre": 12,
        "units_peak": 12,
        "units_post": 1,
        "pop_pre": 10_500_000,
        "pop_post": 26_800_000,
        "conflicts_per_decade": 2.0,
        "iso3_gdp": "ITA",
        "iso3_vdem": "ITA",
        "sources": "Italian city-state system pre-1494 (~12 significant polities: "
                   "Venice, Milan, Florence, Naples, Papal States, Genoa, Savoy, etc.). "
                   "Italian Wars 1494-1559. Congress of Vienna 1815 (~8 states). "
                   "First War of Independence 1848. Kingdom of Italy 1861. "
                   "Pop: Maddison/historical demography (Italian peninsula).",
        "notes": "Pre-frag entity is the city-state system itself (no unified "
                 "predecessor). Features_pre = city-state system archetype. "
                 "Frag_peak = 1559 (Treaty of Cateau-Cambresis, foreign domination "
                 "consolidated). Features_post = unitary nation-state (constitutional "
                 "monarchy under House of Savoy).",
    },
    {
        "name": "United States",
        "is_control": False,
        "pre_frag_year": 1860,
        "frag_peak_year": 1861,
        "first_integration_year": 1865,
        "post_collect_year": 1868,
        "features_pre":  [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        "features_post": [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        "units_pre": 33,
        "units_peak": 2,
        "units_post": 37,
        "pop_pre": 31_443_000,
        "pop_post": 38_558_000,
        "conflicts_per_decade": 10.0,
        "iso3_gdp": "USA",
        "iso3_vdem": "USA",
        "sources": "Pre-Civil War US (33 states, 1860 census). Secession 1860-61 "
                   "(11 Confederate states -> 2 entities). Appomattox 1865. "
                   "14th Amendment ratified 1868. Pop: US Census.",
        "notes": "Subtlest form shift in the corpus. Pre features code the de-facto "
                 "confederation (states as primary military force via militias, "
                 "unilateral exit contested but live doctrine, no federal income tax). "
                 "Post features reflect Reconstruction amendments (14th/15th) and "
                 "expanded federal power. Feature 2 (indep militaries) flipped: "
                 "state militias subordinated to federal authority.",
    },
    {
        "name": "European Union",
        "is_control": False,
        "pre_frag_year": 1914,
        "frag_peak_year": 1945,
        "first_integration_year": 1951,
        "post_collect_year": 1993,
        "features_pre":  [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
        "features_post": [0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        "units_pre": 20,
        "units_peak": 28,
        "units_post": 12,
        "pop_pre": 295_000_000,
        "pop_post": 349_000_000,
        "conflicts_per_decade": 5.0,
        "iso3_gdp": ["FRA", "DEU", "ITA", "GBR", "NLD", "BEL"],
        "iso3_vdem": ["FRA", "DEU", "ITA", "GBR", "NLD", "BEL"],
        "sources": "European state system pre-1914 (~20 major states). WWI/WWII "
                   "devastation. ECSC 1951 (Treaty of Paris). EEC 1957 (Treaty of "
                   "Rome). EU 1993 (Maastricht Treaty, 12 founding members). "
                   "Pop: pre = major European states ~1914; post = EU-12 1993.",
        "notes": "Pre-frag entity is the European Concert/state system (no single "
                 "governance structure). Features_pre code the system-level properties "
                 "(each nation sovereign, free movement pre-1914 but no shared currency "
                 "or legal code). Features_post = supranational union with single market, "
                 "shared court (ECJ), but members retain militaries and partial foreign "
                 "policy independence. EU is the most novel form in the corpus.",
    },
    {
        "name": "China",
        "is_control": False,
        "pre_frag_year": -771,
        "frag_peak_year": -403,
        "first_integration_year": -230,
        "post_collect_year": -221,
        "features_pre":  [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        "features_post": [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0],
        "units_pre": 148,
        "units_peak": 7,
        "units_post": 1,
        "pop_pre": 12_000_000,
        "pop_post": 20_000_000,
        "conflicts_per_decade": 4.0,
        "iso3_gdp": "CHN",
        "iso3_vdem": "CHN",
        "sources": "Western Zhou fall -771. Spring and Autumn (~148 states initially). "
                   "Warring States conventionally from -403 (Jin partition). "
                   "Seven major states by -350. Qin conquest begins -230 (Han). "
                   "Qin unification -221 (36 commanderies). "
                   "Pop: historical demography estimates (Zhao Gang, Ge Jianxiong).",
        "notes": "Pre-frag = Western Zhou feudal order. Features code the feudal "
                 "system (lords with independent forces, nominal Son of Heaven). "
                 "Post = Qin centralized bureaucratic empire (commanderies, "
                 "standardized currency/weights/script, Legalist legal code). "
                 "Most radical form shift in the corpus (11 feature flips). "
                 "GDP data unavailable for this period; uses NaN.",
    },
    {
        "name": "Japan",
        "is_control": False,
        "pre_frag_year": 1467,
        "frag_peak_year": 1550,
        "first_integration_year": 1568,
        "post_collect_year": 1889,
        "features_pre":  [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        "features_post": [1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0],
        "units_pre": 66,
        "units_peak": 250,
        "units_post": 1,
        "pop_pre": 10_000_000,
        "pop_post": 40_000_000,
        "conflicts_per_decade": 8.0,
        "iso3_gdp": "JPN",
        "iso3_vdem": "JPN",
        "sources": "Ashikaga shogunate effective collapse 1467 (Onin War). "
                   "Sengoku peak ~1550 (~250 daimyo domains). Nobunaga enters "
                   "Kyoto 1568. Tokugawa 1603 (intermediate centralization). "
                   "Meiji Constitution 1889 (nation-state). Pop: Farris/Totman "
                   "historical demography.",
        "notes": "Two-stage collectivization: Sengoku->Tokugawa (partial, feudal "
                 "centralization) then Tokugawa->Meiji (full nation-state). We code "
                 "the full arc (1467->1889). Feature 8 (popular sovereignty) = 0: "
                 "Meiji Constitution vested sovereignty in the Emperor. Feature 9 "
                 "(elections) = 1: Diet elected (limited franchise). Feature 14 "
                 "(preexisting polities) = 0: han system abolished, prefectures "
                 "replaced daimyo domains.",
    },
    # ── CONTROL CASES (collectivization failed or stalled) ──
    {
        "name": "Middle East (post-Ottoman)",
        "is_control": True,
        "pre_frag_year": 1918,
        "frag_peak_year": 1946,
        "first_integration_year": 1945,
        "post_collect_year": 1945,
        "features_pre":  [1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1],
        "features_post": [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        "units_pre": 1,
        "units_peak": 22,
        "units_post": 22,
        "pop_pre": 20_000_000,
        "pop_post": 70_000_000,
        "conflicts_per_decade": 3.0,
        "iso3_gdp": ["EGY", "TUR", "IRQ", "SAU"],
        "iso3_vdem": ["EGY", "TUR", "IRQ", "SAU"],
        "sources": "Ottoman Empire dissolution 1918. Mandate system 1920s. "
                   "Independence of most states by 1946. Arab League 1945 (22 members, "
                   "nominal confederation with no binding authority). "
                   "Pop: Ottoman ~1910; Arab League members ~1950.",
        "notes": "CONTROL: fragmentation without successful collectivization. "
                 "Arab League is the weakest form of association -- members retain "
                 "full sovereignty on all dimensions. Feature vector post reflects "
                 "the Arab League's lack of integration (no shared currency, legal "
                 "code, court, army, or free movement). The flip pattern shows "
                 "DISINTEGRATION (features moving from integrated to fragmented), "
                 "opposite of the core cases.",
    },
    {
        "name": "Sub-Saharan Africa",
        "is_control": True,
        "pre_frag_year": 1960,
        "frag_peak_year": 1970,
        "first_integration_year": 1963,
        "post_collect_year": 2002,
        "features_pre":  [1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
        "features_post": [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        "units_pre": 6,
        "units_peak": 48,
        "units_post": 55,
        "pop_pre": 230_000_000,
        "pop_post": 800_000_000,
        "conflicts_per_decade": 6.0,
        "iso3_gdp": ["NGA", "ZAF", "KEN", "GHA", "ETH"],
        "iso3_vdem": ["NGA", "ZAF", "KEN", "GHA", "ETH"],
        "sources": "Colonial empires (British, French, Portuguese, Belgian, Spanish ~6 "
                   "metropolitan powers over sub-Saharan Africa). Year of Africa 1960. "
                   "OAU 1963. AU 2002 (55 members). Pop: colonial Africa ~1960; "
                   "AU members ~2002.",
        "notes": "CONTROL: colonial fragmentation without strong re-collectivization. "
                 "The AU has more institutional ambition than the Arab League (Peace and "
                 "Security Council, NEPAD) but remains very weak on integration. "
                 "Features_pre code the colonial system (metropole-centered). "
                 "Features_post code the AU (sovereignty retained by all members).",
    },
    {
        "name": "Post-Soviet",
        "is_control": True,
        "pre_frag_year": 1991,
        "frag_peak_year": 1991,
        "first_integration_year": 1991,
        "post_collect_year": 2015,
        "features_pre":  [1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1],
        "features_post": [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
        "units_pre": 1,
        "units_peak": 15,
        "units_post": 5,
        "pop_pre": 293_000_000,
        "pop_post": 183_000_000,
        "conflicts_per_decade": 4.0,
        "iso3_gdp": ["RUS", "UKR", "KAZ", "BLR"],
        "iso3_vdem": ["RUS", "UKR", "KAZ", "BLR"],
        "sources": "USSR dissolution 1991 (15 successor states). CIS 1991 (nominal). "
                   "EAEU 2015 (5 members: Russia, Belarus, Kazakhstan, Armenia, "
                   "Kyrgyzstan). Pop: USSR 1991; EAEU 2015.",
        "notes": "CONTROL: partial re-collectivization. EAEU has customs union and "
                 "some economic integration but is dominated by Russia and lacks "
                 "political integration, shared legal code, or shared court with "
                 "binding authority. CIS is even weaker. The post-Soviet space "
                 "demonstrates stalled collectivization with significant resistance "
                 "from members seeking Western integration (Ukraine, Georgia, Moldova).",
    },
    {
        "name": "Greek poleis",
        "is_control": True,
        "pre_frag_year": -1200,
        "frag_peak_year": -500,
        "first_integration_year": -338,
        "post_collect_year": -337,
        "features_pre":  [1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
        "features_post": [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        "units_pre": 1,
        "units_peak": 750,
        "units_post": 750,
        "pop_pre": 2_000_000,
        "pop_post": 8_000_000,
        "conflicts_per_decade": 5.0,
        "iso3_gdp": "GRC",
        "iso3_vdem": "GRC",
        "sources": "Mycenaean palace system collapse ~-1200. Greek Dark Age. "
                   "Polis system ~-800 to -338 (~750 known poleis per Hansen/Nielsen "
                   "inventory). Battle of Chaeronea -338 (Macedon conquers). "
                   "League of Corinth -337 (externally imposed). Pop: Mogens Hansen "
                   "estimates for Archaic-Classical Greece.",
        "notes": "CONTROL: fragmentation without ENDOGENOUS collectivization. "
                 "The League of Corinth was imposed by Macedon (external force), "
                 "not generated by the polis system itself. The poleis never "
                 "developed internal mechanisms for political unification -- "
                 "attempts (Delian League, Boeotian League) were unstable hegemonies. "
                 "Features_post code the polis system itself (what persisted without "
                 "external imposition), not the Macedonian imposed order. "
                 "No Maddison or V-Dem data for this period.",
    },
]


def _growth(iso3, pre_frag_year, post_collect_year, window=30):
    """Compute pre/post GDP growth rates. Handles single ISO3 or list."""
    if isinstance(iso3, list):
        series_all = {}
        for iso in iso3:
            s = load_gdp_series(iso)
            for y, v in s.items():
                series_all.setdefault(y, []).append(v)
        series = {y: sum(vs) / len(vs) for y, vs in series_all.items()}
    else:
        series = load_gdp_series(iso3)

    growth_pre = avg_annual_growth(series, pre_frag_year - window, pre_frag_year)
    growth_post = avg_annual_growth(series, post_collect_year, post_collect_year + window)
    return growth_pre, growth_post, series


def _vdem(iso3, post_collect_year):
    """Load V-Dem subseries. Handles single ISO3 or list."""
    start = post_collect_year
    end = min(post_collect_year + 200, 2025)
    if isinstance(iso3, list):
        return multi_country_vdem(iso3, start, end)
    return vdem_subseries(iso3, start, end)


def build_all():
    """Build all case JSONs from specs + computed data."""
    os.makedirs(CASES_DIR, exist_ok=True)

    for spec in SPECS:
        growth_pre, growth_post, gdp_full = _growth(
            spec["iso3_gdp"], spec["pre_frag_year"], spec["post_collect_year"])

        gdp_series = {}
        start = min(spec["pre_frag_year"] - 50, spec["post_collect_year"])
        end = min(spec["post_collect_year"] + 200, 2025)
        for y, v in gdp_full.items():
            if start <= y <= end:
                gdp_series[y] = round(v, 1)

        vdem_series = _vdem(spec["iso3_vdem"], spec["post_collect_year"])
        vdem_out = {str(y): round(v, 4) for y, v in vdem_series.items()} if vdem_series else {}

        frag_dur = spec["frag_peak_year"] - spec["pre_frag_year"]
        if frag_dur <= 0:
            frag_dur = abs(frag_dur) if frag_dur < 0 else 1
        collect_speed = spec["post_collect_year"] - spec["first_integration_year"]
        durability = 2026 - spec["post_collect_year"]
        if spec["name"] == "Germany":
            durability = 1918 - 1871  # Empire ended at WWI
        elif spec["name"] == "China":
            durability = -206 - (-221)  # Qin lasted ~15 years; Han continued the form

        case = {
            "name": spec["name"],
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
            "gdp_growth_pre": round(growth_pre, 5) if growth_pre == growth_pre else None,
            "gdp_growth_post": round(growth_post, 5) if growth_post == growth_post else None,
            "frag_duration_years": frag_dur,
            "conflicts_per_decade": spec["conflicts_per_decade"],
            "collect_speed_years": collect_speed,
            "durability_years": durability,
            "gdp_series": {str(y): v for y, v in sorted(gdp_series.items())},
            "vdem_series": vdem_out,
            "sources": spec["sources"],
            "notes": spec["notes"],
        }

        slug = spec["name"].lower().replace(" ", "_").replace("(", "").replace(")", "")
        slug = slug.replace("-", "_")
        if spec["is_control"]:
            slug = "ctrl_" + slug
        path = os.path.join(CASES_DIR, f"{slug}.json")
        with open(path, "w") as f:
            json.dump(case, f, indent=2)
        print(f"wrote {path}")


if __name__ == "__main__":
    build_all()
