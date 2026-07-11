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
      "Reading the whole world system from the same data - the three improvement engines, the institutional container, and where the current lull sits.",
    status: "exploratory · proxy-based",
  },
  {
    slug: "golden-ages",
    kind: "prediction",
    title: "Are golden ages predictable?",
    lede:
      "A pre-registered prediction that failed its holdout - and the honest signal that survived. Trust the level; distrust the slope.",
    status: "pre-registered · one clean fail",
  },
  {
    slug: "collectivization",
    kind: "sibling study",
    title: "How orders rebuild after they fragment",
    lede:
      "A 30-polity study of how political systems re-integrate after collapse - four pathways, and which ones last.",
    status: "sibling program · not MI scoring",
  },
  {
    slug: "substrate",
    kind: "synthesis",
    title: "What the whole thing means",
    lede:
      "The capstone argument: this is not an index or a forecast - it is a substrate a genuine predictive science could one day be built on.",
    status: "synthesis",
  },
];

export const researchTopic = (slug: string): ResearchTopic | undefined =>
  RESEARCH_TOPICS.find((t) => t.slug === slug);
