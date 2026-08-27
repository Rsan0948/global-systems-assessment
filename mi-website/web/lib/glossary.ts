// One place for every plain-language explanation. The Define popovers show `short`;
// the How-it-works page renders the fuller what/why/example. Keep them in sync here.

export type GlossaryEntry = {
  id: string; // anchor on /how-it-works
  term: string;
  short: string; // one or two sentences, for the inline popover
  what: string;
  why: string;
  example?: string;
};

export const GLOSSARY: Record<string, GlossaryEntry> = {
  mi: {
    id: "the-score",
    term: "Modernization Index (MI)",
    short:
      "A score from 0 to 1 that combines five structural features of a country. Higher scores indicate stronger conditions for handling stress. The score is not a prediction.",
    what: "A score from 0 to 1 that averages five pillars. Each pillar contributes 20 percent of the published score.",
    why: "It provides a quick comparison across countries while keeping the five underlying pillar scores available for review.",
    example: "Switzerland scores about 0.87, while countries with much weaker structural conditions may score below 0.30.",
  },
  tier: {
    id: "score-bands",
    term: "Score band",
    short:
      "A readable range for the score. Band 1 starts at 0.80, while Band 5 covers scores below 0.20. A band is only a grouping of the MI score.",
    what: "Five colored ranges of the MI score: Band 1 is 0.80 or higher, Band 2 is 0.60 to 0.79, Band 3 is 0.40 to 0.59, Band 4 is 0.20 to 0.39, and Band 5 is below 0.20.",
    why: "Score bands make the map and lists easy to scan without implying a separate model or evidence level.",
  },
  p1: {
    id: "pillar-p1",
    term: "Institutions",
    short:
      "How well the state actually works: rule of law, government effectiveness, control of corruption, and accountability.",
    what: "How well courts, public agencies, anti-corruption rules, and political accountability work in practice.",
    why: "Strong institutions give a country established ways to respond to a crisis and resolve disputes.",
    example:
      "During a crisis, functioning courts and elections can provide an orderly way to settle disputes.",
  },
  p2: {
    id: "pillar-p2",
    term: "Economic Complexity",
    short:
      "How sophisticated and diversified the economy is. Does it make many complex things, or depend on one commodity?",
    what: "A measure of the range and sophistication of what a country produces and exports.",
    why: "A diverse economy has more ways to adapt when one sector fails. An economy that depends on one product has fewer alternatives.",
    example:
      "A country that depends heavily on oil is more exposed to oil-price changes than one that exports machinery, chemicals, and software.",
  },
  p3: {
    id: "pillar-p3",
    term: "Human Capital",
    short: "The capacity of the population: education and health.",
    what: "How educated and healthy the population is.",
    why: "Education and health affect a country's ability to adapt, provide services, and recover after disruption. They usually change slowly.",
    example: "Post-war recoveries are far faster where the workforce is already educated.",
  },
  p4: {
    id: "pillar-p4",
    term: "Economic Structure",
    short:
      "Income per person. Wealth provides resources and flexibility, but it does not guarantee strong institutions.",
    what: "How wealthy the country is, in income per person.",
    why: "Higher income can provide reserves and policy options. Its effect depends partly on whether institutions are strong enough to manage those resources.",
    example: "An oil-producing country can have high income even when its institutions remain weak.",
  },
  p5: {
    id: "pillar-p5",
    term: "Stability & Resilience",
    short:
      "How prone the system is to violence, fragmentation, or breakdown right now: political stability and the absence of structural fragility.",
    what: "A read on present political stability and the absence of acute fragility.",
    why: "It captures whether the other pillars are currently holding together or already under visible strain.",
  },
  "durability-gap": {
    id: "durability-gap",
    term: "Durability gap",
    short:
      "A comparison between a country's income and the strength of its institutions. A large gap may indicate that prosperity is less durable.",
    what: "The relationship between how wealthy a country is and how strong its institutions are.",
    why: "The historical cases suggest that high income is less durable when institutions remain comparatively weak.",
    example:
      "Two countries can have similar incomes but different institutional strength, which can lead to different readings of durability.",
  },
  shape: {
    id: "shape",
    term: "Structural shape",
    short:
      "The difference between the highest and lowest pillar. It shows whether one weak area is hidden by the overall average.",
    what: "How even or uneven a country's five pillar scores are.",
    why: "A very weak pillar can matter even when the overall average looks healthy. The spread shows information that the combined score can hide.",
  },
  exposure: {
    id: "relational",
    term: "Exposure",
    short:
      "How much external danger a country faces, including hostile neighbors and contested borders. The five internal pillars do not measure this.",
    what: "The raw external threat a country sits under, independent of how it is built inside.",
    why: "Internal strength cannot remove every external threat, so exposure is recorded separately.",
  },
  protection: {
    id: "relational",
    term: "Protection",
    short:
      "Whether a credible ally or alliance is expected to defend the country against an external threat.",
    what: "Whether a credible ally or alliance is expected to help defend the country.",
    why: "In the historical cases, outside protection changed the outcomes of some countries facing similar threats.",
    example: "After Iraq invaded Kuwait in 1990, an international coalition restored the Kuwaiti government.",
  },
  response: {
    id: "relational",
    term: "Response",
    short: "How well a country could respond after an external shock, using its own capacity and any outside help.",
    what: "The ability to respond after an external shock through internal capacity or outside help.",
    why: "Exposure measures the external threat. Response measures the capacity available after the threat becomes real.",
  },
};

export const PILLAR_KEYS = ["p1", "p2", "p3", "p4", "p5"] as const;
