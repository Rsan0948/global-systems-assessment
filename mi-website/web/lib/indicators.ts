// The raw indicators that feed the five pillars: display label, a plain-language
// "what it measures", and which pillar it contributes to. Sources travel with the
// data (each indicator carries its own source string). Client-safe (no fs).

export const INDICATOR_LABELS: Record<string, string> = {
  gov_effectiveness: "Government effectiveness",
  rule_of_law: "Rule of law",
  regulatory_quality: "Regulatory quality",
  control_of_corruption: "Control of corruption",
  voice_accountability: "Voice & accountability",
  political_stability: "Political stability",
  cpi: "Corruption Perceptions Index",
  gii: "Global Innovation Index",
  rd_pct_gdp: "R&D spending (% of GDP)",
  eci: "Economic Complexity Index",
  education_index: "Education index",
  life_expectancy_index: "Life expectancy index",
  gdp_per_capita_ppp: "GDP per capita (PPP)",
  resource_rents_pct_gdp: "Resource rents (% of GDP)",
  oda_pct_gni: "Aid received (% of GNI)",
  fsi: "Fragile States Index",
};

export const INDICATOR_META: Record<string, { what: string; pillar: string }> = {
  gov_effectiveness: {
    what: "The quality of public services and how well government policy actually gets carried out.",
    pillar: "P1",
  },
  rule_of_law: {
    what: "Confidence in and adherence to the rules of society: courts, contracts, and property rights.",
    pillar: "P1",
  },
  regulatory_quality: {
    what: "The government's ability to write sound rules that let the private sector work.",
    pillar: "P1",
  },
  control_of_corruption: {
    what: "How far public power is kept from being used for private gain.",
    pillar: "P1",
  },
  voice_accountability: {
    what: "How much citizens can take part, speak freely, and hold their government to account.",
    pillar: "P1",
  },
  political_stability: {
    what: "The likelihood of political instability or politically-motivated violence.",
    pillar: "P5",
  },
  cpi: { what: "An expert-and-survey score of how corrupt a country's public sector is perceived to be.", pillar: "P1" },
  gii: { what: "A composite ranking of a country's capacity for, and output of, innovation.", pillar: "P2" },
  rd_pct_gdp: { what: "How much a country spends on research and development, as a share of its economy.", pillar: "P2" },
  eci: {
    what: "How diverse and sophisticated a country's export mix is - the range of complex things it can make.",
    pillar: "P2",
  },
  education_index: { what: "The UN's schooling measure: expected and average years of education.", pillar: "P3" },
  life_expectancy_index: { what: "The UN's population-health measure, from life expectancy at birth.", pillar: "P3" },
  gdp_per_capita_ppp: { what: "Average income per person, adjusted for what money actually buys locally.", pillar: "P4" },
  resource_rents_pct_gdp: { what: "Income from extracting natural resources, as a share of the economy.", pillar: "P4" },
  oda_pct_gni: { what: "Foreign aid received, as a share of national income.", pillar: "P4" },
  fsi: { what: "A composite index of the pressures that push states toward fragility and collapse.", pillar: "P5" },
};

export const labelFor = (k: string) => INDICATOR_LABELS[k] ?? k.replace(/_/g, " ");
export const fmtVal = (v: number) =>
  v >= 1000 ? Math.round(v).toLocaleString() : Number.isInteger(v) ? String(v) : v.toFixed(1);
