# Lead-time / foresight horizon analysis (MI v3, 51-case baseline)

**Question:** for each case, how far *before* the outcome can the framework still predict
accurately — and where does it lose the signal? **Config:** `mi.constants.LEAD_TIME` (single
source). **Per-case result:** the `lead_time` block written into every record in
`data/case_studies/completed/`.

## Method
Anchor every case on its **2024 outcome**; run the predictor backwards at leads of
**1 / 3 / 5 / 7 / 10** years (and 15 / 20 / 28 to find the breakpoint), i.e. predictor =
pre-event **P1 at (2024 − lead)** → does it call the 2024 outcome? The Mod4 margin + V3
consolidated-pair gates apply, so an **abstention counts as "correctly cautious," not a miss**.
Accuracy = hits / (hits + misses). (Outcome anchored at 2024 to match how the corpus is scored;
WGI is annual back to 1996, so every lead is real data.)

## Headline finding: there are TWO signals with very different shelf lives

### 1. The ordinal / structural signal — reliable to ~10–28 years (no horizon decay)
"Which polity is more durable" and "is this state structurally fragile" are **persistent**:
relative institutional rank barely moves, so old P1 predicts the 2024 outcome about as well as
recent P1.

| lead (yrs) | 1 | 3 | 5 | 7 | 10 | 15 | 20 | 28 |
|---|---|---|---|---|---|---|---|---|
| ordinal accuracy | 91% | 92% | 92% | 92% | 92% | 100% | 92% | 100% |

- Flat across the whole range — **we do not lose the ordinal "sauce" within any testable horizon.**
- The only persistent miss is **Ethiopia/Eritrea**, which mis-ranks at *every* lead → a
  **structural** exception, not a timing effect.
- Single-entity diagnoses are likewise durable: **21 / 26** risk tiers (HIGH/MOD/LOW from P1) are
  identical 10 years back and at 2024. Fragile states were diagnosable a decade early — Venezuela
  was HIGH-risk with a 0.52 spread in 2010; Yemen, Sudan, Iraq the same.

### 2. The acute-timing signal — only ~3–5 years (the framework is directional, not a clock)
*When* a stable-looking state actually turns over only becomes visible close to the event:

| case | P1 / spread trajectory | signal emerges |
|---|---|---|
| **Chile** | spread 0.19 (2014) → 0.38 (2018) before the 2019 unrest | ~5y, **not** 10y |
| **Lebanon** | level crosses MOD→HIGH between 2018 and 2021 (2019 collapse) | ~3–5y |
| Venezuela | already P1 0.28 / spread 0.52 in 2010 (slow-burn) | 10y+ |

The 5 single-entity tiers that **shifted** within the decade (South Africa, Lebanon, Argentina,
Sri Lanka, Myanmar) are exactly the time-sensitive cases. And the corpus's lone falsification —
**Chile/Uruguay** — is precisely a consolidated state whose turn was **not** in the data far back
(which is why V3 abstains on consolidated pairs).

## Where we lose the sauce
Not at a fixed number of years, but at a **type of question**:
- **Durability ranking / structural fragility:** good for **a decade-plus** (empirically ~28y).
- **Collapse / turn-over *date*:** good for **~3–5 years only** — the level/spread shift appears
  late. This quantifies the framework's standing "directional, not timing" disclaimer (Mod8).

## Per-case record
Each case carries a `lead_time` structural fact:
- **comparative** (20 cases): `ordinal_by_lead` (hit/abstain/miss at each lead) + `ordinal_holds_to_years`.
- **single_entity** (26): `risk_tier_by_lead`, `risk_tier_2024`, `risk_tier_stable_10y`.
- **comparative_data_limited / single_entity_data_limited** (5): a proxy/non-WB entity (Taiwan,
  Aceh, Bougainville, Somaliland, Kosovo/East Timor/South Sudan pre-event) lacks the data to
  compute an ordinal/tier lead-time → judgment-only, flagged.

Reproduce: edit `mi.constants.LEAD_TIME`, re-run the per-case computation; nothing about the
verdicts changes (the lead-time fact is additive — corpus stays 213C/77P/0F).
