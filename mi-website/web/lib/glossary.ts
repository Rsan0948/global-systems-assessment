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
      "A single score from 0 to 1 that combines five structural traits of a country. Higher means it is better built to withstand stress. It is a health check, not a prediction.",
    what: "A 0-to-1 score that averages five equally-weighted pillars of how a country is built.",
    why: "It compresses a country's whole structural profile into one comparable number, so you can scan the world at a glance and then dig into why a country scores the way it does.",
    example: "Switzerland scores ~0.87 (very durable); a fragile state may score below 0.30.",
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
    what: "The quality of the machinery of government: courts that function, agencies that deliver, corruption that is checked, leaders who can be held to account.",
    why: "Institutions are what let a country absorb a shock in an orderly way instead of fracturing. They are the single most load-bearing pillar.",
    example:
      "When a crisis hits, a country with real rule of law resolves it through courts and elections; one without resolves it on the street.",
  },
  p2: {
    id: "pillar-p2",
    term: "Economic Complexity",
    short:
      "How sophisticated and diversified the economy is. Does it make many complex things, or depend on one commodity?",
    what: "A measure of the range and sophistication of what a country produces and exports.",
    why: "A complex economy has more ways to adapt when one sector fails; a one-product economy is hostage to that one product.",
    example:
      "A country that only exports oil rises and falls with the oil price. One that exports machinery, chemicals, and software has shock absorbers.",
  },
  p3: {
    id: "pillar-p3",
    term: "Human Capital",
    short: "The capacity of the population: education and health.",
    what: "How educated and healthy the people are, the raw human material a country works and rebuilds with.",
    why: "A skilled, healthy population is what makes recovery possible. It is the slowest pillar to build and the slowest to lose.",
    example: "Post-war recoveries are far faster where the workforce is already educated.",
  },
  p4: {
    id: "pillar-p4",
    term: "Economic Structure",
    short:
      "The material base: income per person. Wealth buys options and a cushion, but on its own it is the least reliable pillar.",
    what: "How wealthy the country is, in income per person.",
    why: "Money buys reserves and breathing room. But wealth without the institutions to anchor it is fragile, which is the whole point of the durability gap.",
    example: "An oil state can look rich on this pillar while being structurally hollow underneath.",
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
      "Is a country's prosperity earned (institutions match its wealth) or granted (wealth has outrun institutions)? Granted prosperity is historically fragile.",
    what: "The relationship between how wealthy a country is and how strong its institutions are.",
    why: "Wealth without the institutions to anchor it tends not to last. Income that has outrun institutions is the clearest structural warning sign in the index.",
    example:
      "Two countries can have the same income; the one whose institutions match it is durable, the one whose institutions lag is living on borrowed time.",
  },
  shape: {
    id: "shape",
    term: "Structural shape",
    short:
      "We read the shape of the five pillars, not just the average. A balanced country is sturdier than a lopsided one with the same score.",
    what: "How even or uneven a country's five pillars are.",
    why: "A chain breaks at its weakest link. A lopsided country carries a hidden liability that a single average score hides.",
  },
  exposure: {
    id: "relational",
    term: "Exposure",
    short:
      "How much external danger a country faces: a powerful hostile neighbor, a contested border, a bad neighborhood. The internal pillars do not see this.",
    what: "The raw external threat a country sits under, independent of how it is built inside.",
    why: "A perfectly-built country can still be invaded. Exposure is the part of the story the internal pillars are blind to.",
  },
  protection: {
    id: "relational",
    term: "Protection",
    short:
      "Whether a powerful ally would actually defend it. A weak country with a strong protector can survive what would sink it alone.",
    what: "Whether a credible external patron or alliance stands behind the country.",
    why: "Among exposed countries, protection is often the difference between a weak state that survives and an identical one that gets swallowed.",
    example: "Kuwait was conquered in 1990, then restored by a coalition. The protector was the whole story.",
  },
  response: {
    id: "relational",
    term: "Response",
    short: "How well a country could absorb a shock that lands: its cohesion, capacity, and whether help arrives.",
    what: "The ability to blunt a shock once it hits, through internal cohesion or outside help.",
    why: "Exposure says how likely a hit is; response says how well the country takes one.",
  },
};

export const PILLAR_KEYS = ["p1", "p2", "p3", "p4", "p5"] as const;
