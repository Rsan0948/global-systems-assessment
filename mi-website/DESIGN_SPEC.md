# Modernization Index Website — Tentative Design Specification

**Version:** 0.1 (tentative)
**Date:** June 27, 2026
**Status:** Pre-development concept specification

---

## 1. PURPOSE AND POSITIONING

The MI website is the institutional home of the Modernization Index — a living research instrument, not a static publication site. It serves four functions simultaneously:

1. **Public diagnostic tool:** Any person can look up any country and see its structural profile, pillar scores, configuration, strategy classification, and safeguard flags.
2. **Research platform:** Researchers can access the complete dataset, methodology, and case study database to evaluate, replicate, and extend the framework.
3. **Educational experience:** Interactive case study walkthroughs teach structural diagnosis through practice.
4. **Growing institution:** A contribution portal enables researchers to submit new case studies and proposed safeguards, building the framework through collective use.

The website should feel like a Bloomberg Terminal for geopolitics — serious, data-dense, precise, beautiful in its clarity rather than its decoration.

---

## 2. INFORMATION ARCHITECTURE

### 2.1 Site Map

```
/                           → Landing page (interactive global map)
/country/:slug              → Country profile (full diagnostic)
/compare                    → Country comparison tool
/explorer                   → Dataset explorer (filter, rank, sort)
/case-studies               → Case study index
/case-studies/:slug         → Individual case study (interactive)
/methodology                → Layered methodology (visual → technical → replication)
/methodology/pillars        → Deep dive on each pillar
/methodology/safeguards     → Complete safeguard system
/methodology/strategies     → Three-strategy framework
/alerts                     → Structural alerts feed
/data                       → Dataset download page
/contribute                 → Research contribution portal
/contribute/case-study      → Case study submission
/contribute/safeguard       → Safeguard proposal submission
/analysis                   → Blog / applied analysis posts
/about                      → Project background, author, methodology summary
/book                       → Book information and links
```

### 2.2 Navigation Structure

**Primary nav (persistent header):**
Map | Explorer | Case Studies | Methodology | Alerts | Data | Contribute

**Secondary nav (contextual):**
- Within country profiles: Overview | Pillars | Trajectory | Safeguards | Similar | Case Studies
- Within methodology: Visual Guide | Technical Spec | Replication Guide | Safeguards | Strategies
- Within case studies: Free (10) | Full Collection (51) | Submit New

---

## 3. CORE FEATURES

### 3.1 Landing Page — Interactive Global Map

**Purpose:** Immediate visual entry point. Every country colored by MI tier. The map IS the first impression.

**Specifications:**
- Full-viewport interactive map (likely Mapbox GL or D3 with GeoJSON)
- Color scale by tier:
  - Tier 1 (≥0.80): deep emerald `#059669`
  - Tier 2 (0.60-0.79): blue `#2563EB`
  - Tier 3 (0.40-0.59): amber `#D97706`
  - Tier 4 (0.20-0.39): orange `#EA580C`
  - Tier 5 (0.00-0.19): red `#DC2626`
  - Below floor (<0.00): dark red `#7F1D1D`
  - No data: dark gray `#1F2937`
- Hover state: tooltip showing country name, MI score, mini radar chart (5 pillars), tier label
- Click: navigates to full country profile
- Below map: one-sentence description, three live metrics (countries scored, case studies validated, P1 ordinality record), download/guide links

**Hero text:** "The Modernization Index: Measuring Earned Prosperity"
**Sub-text:** "A quantitative diagnostic framework for understanding how complex governance systems respond to structural stress. [X] countries scored. [Y] case studies validated. Zero falsifications."

### 3.2 Country Profiles

**Purpose:** Complete structural diagnostic for any scored country. The product's core value.

**URL pattern:** `/country/estonia`, `/country/nigeria`, etc.

**Layout — single scrollable page with anchor sections:**

#### Section A: Header
- Country name, flag, region
- MI Score (large, prominent) with tier badge
- Last updated date and data vintage indicator

#### Section B: Radar Chart
- Five-axis radar chart showing pillar scores (P1-P5)
- Filled area shows the country's "shape"
- Reference overlay option: toggle Switzerland (ceiling), Lebanon (floor), or any other country for comparison
- Below chart: pillar spread score with interpretation
  - Narrow (< 0.15): "Balanced configuration — structurally durable"
  - Moderate (0.15-0.35): "Some imbalance — monitor weakest pillar"
  - Wide (0.35-0.50): "Significant imbalance — structural vulnerability"
  - Extreme (> 0.50): "Critical imbalance — highest vulnerability in dataset"

#### Section C: Pillar Detail
- Five expandable cards, one per pillar
- Each card shows:
  - Pillar score (0-1)
  - Individual indicator values with sources and dates
  - Trend arrow (improving/stable/declining vs prior period)
  - Percentile rank among all scored countries
  - One-line diagnostic interpretation
- Configuration ranking displayed as: P4 (0.93) > P3 (0.87) > P1 (0.85) > P5 (0.62) > P2 (0.59)
- Plain-language configuration interpretation: e.g., "Strong economic structure with innovation as the weakest dimension"

#### Section D: Trajectory Chart
- Time series line chart (1996-present)
- Toggle: overall MI score OR individual pillar scores
- Toggle: v1 (anchor-based, absolute) OR v2 (GPA, relative to peers)
- Annotations for significant events (if country appears in case studies)
- Trend line with direction indicator

#### Section E: Strategy Classification
- Which of the three strategies the country is running
- Visual indicator (icon + color)
- Brief explanation of what the strategy means
- Characteristic failure mode
- If suppression: which tier (1/2/3)
- "How this was determined" expandable with the classification logic

#### Section F: Safeguard Panel
- List of all seven safeguards (A-G) plus I, Mod4, Mod8
- Each shows: triggered (yes/no), explanation, modification to predictions
- Triggered safeguards highlighted with warning styling
- Expandable detail for each: derivation history, validation record, what the safeguard means for this country specifically
- Color coding: red for triggered critical safeguards (B+E combo, re-suppression), amber for triggered standard safeguards, green for clear

#### Section G: Similar Configurations
- Table/cards showing 5-10 countries with the most similar pillar configurations
- Similarity metric: Euclidean distance across normalized pillar scores
- For each similar country: MI score, tier, key events, case study link if applicable
- Emphasis on countries from the case study database: "Countries with similar profiles that experienced structural stress had these outcomes..."

#### Section H: Comparison Tool (inline)
- "Compare with..." dropdown/search
- Side-by-side radar charts, pillar scores, trajectories
- Mod4 assessment: is the P1 gap large enough for an ordinal prediction?
- Explicit statement: "The MI predicts [Country A] would outperform [Country B] under structural stress" OR "The P1 gap is within the margin of error — the MI abstains from ranking these two"

#### Section I: Sensitivity Analysis
- Scores under all three weighting schemes (v1, v2, equal)
- Rank shift under equal weights (captures cases like Israel dropping 10 ranks)
- Brief interpretation of what the sensitivity reveals

#### Section J: Case Study Links
- If country appears in any validated case studies, link to them
- Brief summary of what the case study found for this country

#### Section K: Data Sources and Gaps
- Complete indicator table with source, date, and value for each
- Any missing indicators flagged
- Data vintage clearly stated
- Download this country's data as CSV/JSON

### 3.3 Dataset Explorer

**Purpose:** Filter, rank, and sort the complete dataset across any dimension.

**Features:**
- Sortable table: all countries with MI score, tier, and all five pillar scores
- Filter by: region, tier, strategy, any pillar above/below threshold, any safeguard triggered
- Rank by: any single pillar, overall MI, pillar spread, trajectory slope (improving/declining)
- Search: find any country by name
- Export filtered results as CSV
- Preset views:
  - "Most balanced configurations" (narrowest spread)
  - "Most imbalanced" (widest spread)
  - "Fastest improving" (trajectory slope)
  - "Fastest declining"
  - "Resource penalty" (high GDP + high resource rents + low MI)
  - "Earned prosperity" (high MI + low resource rents)
  - "Reversal risk" (Safeguard C triggered)
  - "Fragmentation pressure" (low P1 + wide spread + safeguards B/D/G triggered)

### 3.4 Interactive Case Studies

**Purpose:** Train structural diagnostic thinking through guided practice.

**Free tier:** 10 case studies (5 modern + 5 ancient from the companion guide)
**Full tier:** All 51 case studies (gated by book purchase or subscription)

**Each case study is a multi-step interactive experience:**

**Step 1 — Context**
Brief historical background. What happened, when, who was involved. No MI analysis yet.

**Step 2 — Pre-Event Data**
Show the entities' indicator values and pillar scores. Radar charts for each entity. Safeguard panel. Strategy classification. All the diagnostic information — but NOT the predictions or outcomes yet.

**Step 3 — Reader Prediction (interactive)**
The page asks: "Based on these profiles, what do you predict?"
- Which entity will fare best? (dropdown/select)
- Violent or peaceful? (select)
- Convergence or divergence? (select)
- Which pillar is the primary vulnerability? (select)
- Optional: free-text reasoning
Reader's predictions are stored (using persistent storage API).

**Step 4 — Framework Prediction**
Reveal the MI's predictions with explicit reasoning for each. The reader can compare their predictions to the framework's before seeing the outcome.

**Step 5 — What Actually Happened**
Post-event data, trajectory charts, key events, outcome summary. The verification scoring: confirmed, partially confirmed, or falsified for each prediction.

**Step 6 — Analysis**
What the case reveals. Which safeguards fired correctly. What failure modes were discovered. How the case contributed to the framework's development (if it generated a safeguard or refinement).

**Step 7 — Reader Scorecard**
How did the reader's predictions compare to the framework's predictions and to the actual outcomes? Track across cases so the reader can see their calibration improving.

**Across all cases:** a cumulative accuracy tracker showing the reader's prediction accuracy versus the MI's, building across all completed case studies. Gamification-light — no badges or social features, just an honest calibration metric.

### 3.5 Structural Alerts Feed

**Purpose:** Automated diagnostic flags based on MI data changes. The feature that makes the site useful for policy professionals.

**URL:** `/alerts`

**Alert types:**

- **Pillar decline alert:** "Country X's P1 has declined for [N] consecutive data releases. Current value: [X]. Threshold watch: [specific threshold and what happens if crossed]."
- **Safeguard trigger alert:** "Country Y now triggers Safeguard C — democratic transition with stagnant per-capita growth and youth unemployment above 25%. Historical database: [N] of [M] countries with this profile experienced democratic reversal."
- **Configuration change alert:** "Country Z's pillar spread has widened to [X], crossing the vulnerability threshold. Configuration now resembles pre-crisis profiles of [list of similar historical cases with links to case studies]."
- **Trajectory inflection alert:** "Country W's P5 trajectory has reversed from improving to declining after [N] years of improvement."
- **Tier boundary alert:** "Country V is approaching the Tier [X]/Tier [Y] boundary. Current score: [Z], threshold: [T]."

**Alert format:**
- Date generated
- Country (linked to profile)
- Alert type and severity (info / watch / warning / critical)
- Specific metric change that triggered the alert
- Historical context: what happened in the case study database for countries with similar alert profiles
- Explicit disclaimer: "The MI does not predict timing or specific events. This alert identifies structural conditions that have historically preceded instability."

**Delivery:**
- On-site feed (chronological, filterable by region/severity/type)
- Email subscription (daily/weekly digest, filterable)
- RSS feed for integration with newsreaders and monitoring tools
- API endpoint for programmatic access

### 3.6 Methodology Section (Layered)

**Purpose:** Three audiences, three depth levels, one section.

#### Layer 1: Visual Guide (`/methodology`)
- Target: general public, journalists, students
- Estimated reading time: 5-7 minutes
- Animated/scrolling explainer:
  - "We measure five things about every country" (pillar icons with one-sentence descriptions)
  - "We weight them based on what the data says matters most" (animated weight bars showing correlation-derived adjustment)
  - "We read the SHAPE, not just the score" (radar chart morphing between balanced and imbalanced configurations)
  - "We check our work against history" (map showing case study locations lighting up)
  - "Here's what we can predict — and what we can't" (honest boundaries stated clearly)

#### Layer 2: Technical Specification (`/methodology/technical`)
- Target: researchers, reviewers, graduate students
- Complete MI specification: all 13 indicators, sources, scales, normalizations
- Weight derivation with full correlation matrix
- Three scoring models with cross-validation results
- Track 1 vs Track 2 formulas
- Sensitivity analysis
- WGI 2025 revision handling

#### Layer 3: Replication Guide (`/methodology/replication`)
- Target: researchers who want to reproduce or extend the work
- Step-by-step instructions
- Links to all data source APIs
- Code samples (Python) from the mi-research codebase
- The case study template
- Contribution guidelines

#### Safeguard System (`/methodology/safeguards`)
- Each safeguard (A through I) on its own page
- Derivation history: which case generated it
- Trigger conditions
- Modification logic
- Validation record: which subsequent cases confirmed it
- Falsification conditions: what would invalidate it

#### Three-Strategy Framework (`/methodology/strategies`)
- Porosity, Suppression (three-tier), Complexity Control
- Each strategy: definition, mechanism, examples, characteristic failure mode, MI signature
- How to identify which strategy a country is running from its profile

### 3.7 Data Download Page

**Purpose:** Maximum accessibility. No registration wall for the data itself.

**Available downloads:**
- Complete country dataset (all countries, all years, all indicators, all pillar scores, all MI scores)
  - Formats: CSV, JSON, Excel
- Individual country data (select and download)
- Case study database (all completed case studies as structured JSON)
- Methodology document (PDF)
- Scoring engine source code (link to GitHub repo)

**Data dictionary:** complete variable definitions, sources, update frequencies, known limitations

**License:** Creative Commons Attribution (CC BY 4.0) — free to use, modify, and distribute with attribution

**Citation format:** pre-formatted citation in APA, Chicago, and BibTeX

### 3.8 Research Contribution Portal

**Purpose:** Enable collective improvement of the framework.

#### Case Study Submission (`/contribute/case-study`)
- Structured form following the case study JSON template
- Guided workflow: metadata → pre-event data → predictions → post-event data → verification → analysis
- Review process: submitted → under review → accepted/revision requested/rejected
- Accepted cases added to the validated baseline with contributor credit
- Contributor profile page showing their contributions

#### Safeguard Proposal (`/contribute/safeguard`)
- Structured form: name → derivation (which case failed) → trigger conditions → modification logic → falsification conditions → validation against existing baseline
- Requirement: proposer must demonstrate no degradation on existing baseline cases
- Review process: submitted → baseline testing → peer review → accepted/rejected
- Accepted safeguards get formal designation (Safeguard J, K, etc.) with contributor credit

#### Discussion / Community
- Lightweight — not a full forum
- Each case study page has a discussion thread
- Each safeguard page has a discussion thread
- Moderated for quality — research discussion, not social media

### 3.9 Analysis Blog

**Purpose:** Applied MI analysis of current events. Demonstrates real-time utility.

**Format:** Blog posts applying the MI framework to current situations
- Rapid structural assessments when crises break
- Periodic "structural state of the world" overviews
- Deep dives on specific countries or regions
- Guest posts from researchers using the framework

**Each post includes:**
- The country's current MI profile (embedded from the live data)
- Which safeguards apply
- What the historical database suggests for similar profiles
- Explicit disclaimer about timing/prediction limitations

---

## 4. DESIGN LANGUAGE

### 4.1 Overall Aesthetic

**Inspiration:** Bloomberg Terminal meets academic research meets elegant data journalism. Dark mode primary. Data-dense but not cluttered. Every pixel serves a purpose.

**Primary background:** Very dark blue-black `#0A0A14`
**Secondary background (cards):** Dark navy `#12121F`
**Borders:** Subtle dark `#1E293B`
**Primary text:** Light gray `#E0E0E0`
**Secondary text:** Medium gray `#808098`
**Muted text:** Dark gray `#606078`

**Accent colors (semantic):**
- Positive/success: Emerald `#4ADE80`
- Primary accent: Blue `#60A5FA`
- Warning: Amber `#FBBF24`
- Caution: Orange `#F97316`
- Critical/danger: Red `#F87171`
- Innovation: Purple `#A78BFA`
- Neutral highlight: Teal `#2DD4BF`

### 4.2 Typography

**Headings:** Playfair Display (serif) — weight 700-900, conveys authority and seriousness
**Body:** DM Sans (sans-serif) — weight 400-700, clean and readable at all sizes
**Data/monospace:** JetBrains Mono — for scores, indicators, code samples, data tables

**Scale:**
- Page title: 36px Playfair Display 900
- Section headers: 18px DM Sans 800
- Card headers: 14px DM Sans 700
- Body text: 13-14px DM Sans 400
- Data values: 12-14px JetBrains Mono 600
- Captions/metadata: 10-11px JetBrains Mono 400

### 4.3 Data Visualization

**Radar charts (pillar profiles):**
- Five-axis, origin at center
- Filled area with 20% opacity fill + solid stroke
- Axis labels at each point (P1-P5 with short name)
- Optional comparison overlay in different color
- Grid lines at 0.25 intervals

**Line charts (trajectories):**
- Clean, minimal grid (dark, subtle)
- Line colors from the accent palette
- Interactive tooltip on hover showing exact values
- Annotation markers for significant events

**Bar charts (rankings/comparisons):**
- Horizontal bars colored by tier
- Reference lines at tier boundaries
- Sort controls

**Tables:**
- Alternating row backgrounds (subtle)
- Sortable column headers
- Fixed first column (country name) on horizontal scroll
- Hover highlighting
- Cell colors for pillar scores (gradient from red through amber to green)

### 4.4 Interactive Elements

- **Hover states:** Subtle brightness increase, tooltip appearance
- **Click targets:** Minimum 44px touch target on mobile
- **Transitions:** Smooth, fast (150-200ms), no decorative animations
- **Loading states:** Skeleton screens matching final layout, not spinners
- **Empty states:** Helpful guidance ("No countries match this filter. Try adjusting...")

### 4.5 Responsive Behavior

- **Desktop (>1200px):** Full layout, side-by-side comparisons, full data tables
- **Tablet (768-1200px):** Stacked layout, scrollable tables, maintained radar charts
- **Mobile (<768px):** Single column, simplified radar charts, collapsible sections, swipeable case study steps

---

## 5. TECHNICAL ARCHITECTURE

### 5.1 Stack

**Frontend:**
- Next.js (React) — SSR for SEO, client-side interactivity
- Tailwind CSS — utility-first styling matching the design language
- Recharts or D3 — data visualization
- Mapbox GL JS — interactive global map
- Framer Motion — subtle animations for the methodology visual guide

**Backend:**
- Supabase (PostgreSQL) — primary database for country data, scores, case studies, user data
- Supabase Auth — for researcher accounts (contribution portal, case study progress tracking)
- Supabase Edge Functions — server-side scoring engine API
- Supabase Realtime — live updates for the alerts feed

**Data Pipeline:**
- Python scheduled jobs (daily cron) pulling from source APIs
- The `mi-research` scoring engine running server-side
- Results written to Supabase
- Change detection triggering structural alerts

**Deployment:**
- Vercel (frontend hosting, edge functions)
- Supabase (database, auth, storage)
- GitHub (source code, the mi-research codebase)

### 5.2 Database Schema (key tables)

```
countries
  id, slug, name, iso3, region, sub_region

country_indicators
  id, country_id, year, indicator_name, value, source, vintage_date

country_scores
  id, country_id, year, p1, p2, p3, p4, p5, mi_score_v1, mi_score_v2,
  mi_score_equal, pillar_spread, configuration_json, tier,
  strategy, strategy_tier, computed_at

safeguard_evaluations
  id, country_id, year, safeguard_code (A-I), triggered (bool),
  severity, explanation, computed_at

case_studies
  id, slug, title, status (draft/review/validated), author_id,
  stress_type, region, time_period, entities_json,
  pre_event_data_json, predictions_json, post_event_data_json,
  verification_json, analysis_json, round, created_at

structural_alerts
  id, country_id, alert_type, severity, metric_name,
  old_value, new_value, threshold, explanation,
  similar_cases_json, created_at

user_predictions (for interactive case studies)
  id, user_id, case_study_id, step, prediction_json, created_at

contributors
  id, user_id, name, institution, contributions_count,
  accepted_case_studies, accepted_safeguards
```

### 5.3 API Endpoints

```
GET  /api/countries                    → list all countries with scores
GET  /api/countries/:slug              → full country profile
GET  /api/countries/:slug/trajectory   → time-series data
GET  /api/countries/:slug/safeguards   → safeguard evaluations
GET  /api/countries/:slug/similar      → similar configurations
GET  /api/compare?a=:slug&b=:slug      → side-by-side comparison with Mod4
GET  /api/explorer?sort=p1&tier=1      → filtered/sorted dataset
GET  /api/alerts                       → structural alerts feed
GET  /api/alerts?region=&severity=     → filtered alerts
GET  /api/case-studies                 → case study index
GET  /api/case-studies/:slug           → full case study data
GET  /api/data/download?format=csv     → complete dataset download
POST /api/contribute/case-study        → submit new case study
POST /api/contribute/safeguard         → submit safeguard proposal
POST /api/user/predictions             → store user prediction (case study walkthrough)
GET  /api/user/scorecard               → user's prediction accuracy across cases
```

### 5.4 Data Pipeline Architecture

```
Daily cron job (runs at 06:00 UTC):
  1. Pull latest from WGI API → check for updates
  2. Pull latest from UNDP HDR → check for updates
  3. Pull latest from World Bank WDI → check for updates
  4. Pull latest from TI CPI → check for updates
  5. Pull latest from WIPO GII → check for updates
  6. Pull latest from Harvard/OEC ECI → check for updates
  7. Pull latest from Fund for Peace FSI → check for updates
  
  If any updates detected:
    8. Run scoring engine on affected countries
    9. Compare new scores to previous scores
    10. Generate structural alerts for significant changes
    11. Write new scores to country_scores table
    12. Write alerts to structural_alerts table
    13. Log the vintage and changes for audit trail
    
  Regardless:
    14. Update "last checked" timestamp on the site
```

---

## 6. BUILD PRIORITIES

### Phase 1 — Minimum Viable Product (8-10 weeks)

**Goal:** Country profiles + dataset explorer + data download. The core product that lets anyone look up any country and see its MI diagnostic.

Build:
- [ ] Database schema and seed with existing 85-country snapshot data
- [ ] Scoring engine API (port mi-research Python to Supabase Edge Functions or keep as Python API)
- [ ] Landing page with static map (upgrade to interactive later)
- [ ] Country profile pages (sections A-F: header, radar, pillars, trajectory, strategy, safeguards)
- [ ] Dataset explorer (sortable/filterable table)
- [ ] Data download page (CSV/JSON export)
- [ ] Basic responsive layout

### Phase 2 — Interactive Features (6-8 weeks)

**Goal:** Interactive map, comparison tool, and case study walkthroughs. The features that make the site engaging beyond data lookup.

Build:
- [ ] Interactive Mapbox global map on landing page
- [ ] Country comparison tool (side-by-side with Mod4)
- [ ] Similar configurations algorithm and display
- [ ] 10 free interactive case study walkthroughs
- [ ] User prediction tracking (persistent storage)
- [ ] Reader scorecard (prediction accuracy across cases)

### Phase 3 — Living Instrument (6-8 weeks)

**Goal:** Daily data pipeline, structural alerts, and analysis blog. The features that make the site a living instrument rather than a static reference.

Build:
- [ ] Data ingestion pipeline (daily cron pulling from source APIs)
- [ ] Structural alert generation system
- [ ] Alert feed page with filtering and subscription
- [ ] Email notification system for alerts
- [ ] Analysis blog with embedded MI data
- [ ] RSS feed

### Phase 4 — Community Platform (4-6 weeks)

**Goal:** Contribution portal and community features. The features that build the field.

Build:
- [ ] Researcher authentication (Supabase Auth)
- [ ] Case study submission workflow
- [ ] Safeguard proposal workflow
- [ ] Review queue and moderation tools
- [ ] Contributor profiles and credit system
- [ ] Discussion threads on case studies and safeguards

### Phase 5 — Full Case Study Library (4 weeks)

**Goal:** All 51 case studies as interactive experiences, gated behind book purchase or subscription.

Build:
- [ ] Remaining 41 case study walkthroughs
- [ ] Payment/access gate integration
- [ ] Cumulative reader scorecard across all 51

---

## 7. CONTENT REQUIREMENTS

### Launch content (Phase 1):
- 85+ country profiles with current MI data
- Methodology text (all three layers)
- Safeguard system documentation (A through I + Mod4, Mod8)
- Three-strategy framework documentation
- Data dictionary
- About page
- Book information page

### Phase 2 content:
- 10 interactive case studies (written and structured)
- Landing page copy
- Comparison tool copy and Mod4 explanations

### Phase 3 content:
- Initial analysis blog posts (3-5 to launch)
- Alert template text
- Email notification templates

### Phase 4 content:
- Contribution guidelines
- Review criteria documentation
- Community standards

### Ongoing content:
- Analysis blog posts (target: 2-4 per month)
- Case study walkthroughs as new cases are validated
- Methodology updates as framework evolves

---

## 8. SUCCESS METRICS

### Engagement:
- Monthly unique visitors
- Country profiles viewed per session
- Case studies completed per user
- Time on site (target: >5 min average)
- Return visit rate

### Adoption:
- Dataset downloads per month
- Academic citations of the MI
- Case studies submitted through contribution portal
- Safeguard proposals submitted
- Researchers with active accounts

### Impact:
- Media mentions citing MI data
- Policy documents referencing MI framework
- University courses using the case study collection
- Countries whose profiles are referenced in policy discussions

### Data quality:
- Data freshness (time between source update and MI update)
- Coverage (percentage of world population in scored countries)
- Alert accuracy (do structural alerts precede actual events?)

---

## 9. CONSTRAINTS AND DECISIONS TO MAKE

### Open questions:
- **Monetization:** Free companion guide vs. freemium (basic profiles free, full case studies paid)? The additive philosophy argues for maximum free access. Revenue could come from books, consulting, or institutional subscriptions rather than paywalling core data.
- **Case study gating:** Free 10 + paid 41? Or all free with the books providing the curated/narrative experience?
- **Alert delivery:** Email only, or also push notifications / Slack integration / API webhook?
- **Community moderation:** Author-only review initially? How soon to establish a peer review board?
- **Mobile app:** A dedicated app would enable push notification alerts. Worth building or is the responsive web app sufficient?
- **Internationalization:** The MI covers 85+ countries. Should the site itself be multilingual? At minimum, country profiles could have auto-translated summaries.

### Technical decisions:
- **Scoring engine location:** Python API server vs. Supabase Edge Functions (TypeScript) vs. hybrid? The existing mi-research codebase is Python. Porting to TypeScript adds maintenance burden but simplifies the stack.
- **Map provider:** Mapbox GL (best quality, usage-based pricing) vs. Leaflet + OpenStreetMap (free, less polished) vs. D3 custom (most flexible, most work)?
- **Real-time vs. daily:** Daily updates are sufficient for annual data sources. But should the alerts feed feel "live" (websocket updates) or is a refresh adequate?

---

*This specification is tentative and will evolve as development begins. The core principle throughout: the website should feel like a serious research instrument that happens to be beautifully designed, not a beautiful website that happens to contain research. Every design choice should reinforce the credibility that the MI's empirical track record has earned.*
