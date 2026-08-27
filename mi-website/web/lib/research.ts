// Distilled research index - plain data only (no fs, no JSX). Safe to import
// from server or client components. The prose for each topic lives inline in its
// page under app/research/<slug>/page.tsx; this file is the shared table of
// contents (used by the /research hub and any cross-links).

export type ResearchTopic = {
  slug: string;
  kind: string; // short label chip
  title: string;
  lede: string; // one-line description for the hub
  status: string; // honest framing tag
};

export const RESEARCH_TOPICS: ResearchTopic[] = [
  {
    slug: "global-systems",
    kind: "system-level",
    title: "State of the world",
    lede:
      "A global view of three improvement measures, the institutional setting around them, and recent changes in each.",
    status: "exploratory · proxy-based",
  },
  {
    slug: "golden-ages",
    kind: "prediction",
    title: "Are golden ages predictable?",
    lede:
      "A registered prediction that failed its holdout test, followed by a review of the weaker pattern that remained.",
    status: "registered test · failed holdout",
  },
  {
    slug: "collectivization",
    kind: "sibling study",
    title: "How orders rebuild after they fragment",
    lede:
      "A 30-polity study comparing four ways political systems have reunited after fragmentation.",
    status: "sibling program · not MI scoring",
  },
  {
    slug: "substrate",
    kind: "synthesis",
    title: "How the pieces fit together",
    lede:
      "How the score, safeguards, historical tests, and open questions form one research program.",
    status: "synthesis",
  },
];

export const researchTopic = (slug: string): ResearchTopic | undefined =>
  RESEARCH_TOPICS.find((t) => t.slug === slug);
