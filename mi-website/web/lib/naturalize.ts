function naturalizeString(value: string): string {
  let text = value
    .replace(/[\u2013\u2014\u2015]/g, ",")
    .replace(/max\(pillar\)\s+-\s+min\(pillar\)/g, "max(pillar) minus min(pillar)")
    .replace(/^HYPOTHESIS \(V3\.2\)\s*[-,:]\s*/i, "Exploratory note (v3.2): ")
    .replace(/^DISTRUST THE SLOPE\s*[-,:]\s*/i, "Short-term movement is noisy: ")
    .replace(/^STRUCTURALLY VULNERABLE\s*[-,:]\s*/i, "Structural vulnerability flag: ")
    .replace(/^INDETERMINATE\s*[-,:]\s*/i, "No clear classification: ")
    .replace(/^CRITICAL:\s*/i, "High concern: ")
    .replace(/^WARNING:\s*/i, "Watch: ");

  text = text
    .replace(/\s+-\s+(?=[a-z])/g, ", ")
    .replace(/\s+-\s+/g, ": ")
    .replace(/\s+->\s+/g, ": ")
    .replace(/STRUCTURALLY crisis-vulnerable under shock/g, "structurally vulnerable under stress")
    .replace(/UNIDENTIFIED here/g, "uncertain here")
    .replace(/elevated WATCH, not a verdict/g, "worth closer review, not a firm result")
    .replace(/RE-SUPPRESSION AFTER POROSITY \(WORST PATH\)/g, "renewed suppression after power-sharing")
    .replace(/CAPACITY WITHOUT CONSENT, accountability far below income\/capacity; hypothesized brittle failure mode \(succession\/legitimacy shock\)\. HYPOTHESIS, not a verdict\./g,
      "Accountability is far below income and state capacity. This is an exploratory concern about succession or legitimacy shocks, not a verdict.")
    .replace(/PATRON-SHIELDED/g, "protected by an outside ally")
    .replace(/SHIELDED/g, "protected")
    .replace(/EXPOSED/g, "exposed")
    .replace(/DETERS/g, "reduces")
    .replace(/BLUNTS/g, "softens")
    .replace(/\bUNCLASSIFIED\b/g, "not classified")
    .replace(/\bMATERIAL\b/g, "material")
    .replace(/\bSEVERE\b/g, "severe")
    .replace(/Risk level: CRITICAL/g, "Risk level: high concern");

  text = text
    .replace(
      /^Economic Structure-Institutions gap = (-?\d+\.\d+) <= 0\.2 \(absorber ceiling\): institutions roughly keep pace with income, not structurally flagged \(absorber-class\)\.$/,
      "Income minus institutions is $1. This is at or below the 0.20 lower-risk threshold, so this check is clear.",
    )
    .replace(
      /^Economic Structure-Institutions gap = (-?\d+\.\d+) in the indeterminate band \(0\.2, 0\.28\):.*$/,
      "Income minus institutions is $1. This falls between the 0.20 lower-risk threshold and the 0.28 higher-risk threshold. The 21 comparison cases do not support a firm classification in this range.",
    )
    .replace(
      /^Economic Structure-Institutions gap = (-?\d+\.\d+) >= 0\.28 \(crisis floor\):.*$/,
      "Income minus institutions is $1. This meets or exceeds the 0.28 higher-risk threshold. In the 21 comparison cases, a gap this large was associated with greater risk under stress.",
    )
    .replace(
      /^Institutions or Economic Structure unavailable, gate not evaluable\.$/,
      "This check needs both the Institutions and Economic Structure pillars.",
    );

  text = text.replace(/\s+,/g, ",").replace(/,\s*,/g, ",").replace(/\s{2,}/g, " ");

  const replacements: Record<string, string> = {
    "Spread between the strongest and weakest pillar, the country's structural shape.":
      "The gap between the strongest and weakest pillar shows how balanced the country's structure is.",
    "Institutions roughly match or exceed what income predicts, durable.":
      "Institutions roughly match or exceed the level predicted by income, which suggests greater durability.",
    "Wealth has outrun institutions, historically fragile.":
      "Income has grown faster than institutional strength, a pattern associated with greater fragility.",
    "institutions roughly keep pace with income, not structurally crisis-flagged (absorber-class on this measure).":
      "Institutions roughly keep pace with income, so this measure does not flag elevated structural risk.",
    "This country's prosperity has outrun its institutions. Income the institutions cannot anchor is the classic fragility signal, historically it tends not to last.":
      "This country's income has risen faster than its institutions. In the historical cases, that gap is associated with greater fragility.",
    "A state can survive intact while carrying chronic, managed instability, repeated executive collapses, high anti-system voting, sharp regional divergence. This is a management-load signal, not a collapse indicator.":
      "A state can remain intact while dealing with repeated government collapses, high anti-system voting, or sharp regional divisions. This check measures that ongoing burden, not the likelihood of collapse.",
    "Bosnia's WGI institutional scores under the Dayton OHR sat above Croatia's and Serbia's, the administrator's competence, not indigenous capacity, was being measured. The safeguard discounts raw P1 where an external administrator governs.":
      "Under the Dayton OHR, Bosnia's WGI scores partly reflected the external administrator's capacity. This safeguard discounts P1 when an external administration is doing much of the governing.",
    "Sudan split into just two successor states, a low fragment count that would normally read as manageable, yet produced the worst outcome in the sample, because institutional capacity (P1) was far below the bottom third. Low count is not safety when P1 is that low.":
      "Sudan produced only two successor states, but the outcome was still the worst in the sample because institutional capacity was very low. A small number of fragments is not reassuring when P1 is that weak.",
    "The framework's most genuinely novel prediction: when a great-power patron backstops a state's territorial integrity, an internal secession tends to end in re-suppression and partial reconsolidation, not permanent independence.":
      "This safeguard tests whether support from a major outside power makes renewed suppression and partial reunification more likely than permanent independence.",
    "The framework predicted Tunisia's initial positive trajectory but missed the 2021 presidential self-coup. Democratic transitions with weak economic delivery are flagged as reversal-prone rather than assumed durable.":
      "The framework captured Tunisia's initial improvement but missed the 2021 presidential self-coup. This safeguard marks democratic transitions with weak economic results as vulnerable to reversal.",
    "Suppression and prevention looked identical until this safeguard split them into tiers: military suppression (Tier 1) doesn't resolve the underlying mismatch; institutional/legal suppression (Tier 2) de-escalates; porosity/power-sharing (Tier 3) addresses it by design. Re-suppression after a porosity period is the worst path.":
      "This safeguard separates military suppression, legal or institutional de-escalation, and power-sharing. In the case studies, renewed suppression after a period of power-sharing had the worst outcomes.",
    "Short-term movement is noisy: movement is mean-reverting and low-reliability; the predictive content is the LEVEL and the durability gap, not the delta.":
      "Short-term movement is noisy and often reverses. The current level and the durability gap are more informative than a recent change.",
    "No clear classification: gap sits in the empty band between the validated absorber ceiling and crisis floor; above every confirmed absorber but below the crisis floor. Elevated watch, not a verdict.":
      "The gap falls between the comparison ranges used for lower-risk and crisis cases. It deserves attention, but the available evidence does not support a firm classification.",
    "Structural vulnerability flag: income/economy has outrun institutions (granted/fragile); elevated crisis risk under shock.":
      "Income and economic development have moved ahead of institutional strength. The historical cases associate this gap with higher risk under stress.",
    "Scored on the pillars we have data for. Its score is not directly comparable to a fully-measured country, the missing pillars are unmeasured, not zero.":
      "This score uses only the pillars with available data. It is not directly comparable with a complete five-pillar score, and missing pillars are unmeasured rather than zero.",
    "Resource rents can inflate or hollow out measured institutional quality (Timor-Leste), or buy elite cohesion in a low-capacity state (Nigeria/Gulf). Graded E-1 (material, >15% of GDP) / E-2 (severe, >25%); severe rents make P1 unreliable.":
      "Resource income can distort measures of institutional strength or help governments maintain elite support. This check marks rents above 15 percent of GDP and treats levels above 25 percent as severe.",
    "A structurally sound state can be overrun from outside. The safeguard separates a country's endogenous trajectory from vulnerability to an aggressive neighbour or external shock, so the outcome isn't misread as internally generated.":
      "External threats can overwhelm a country even when its internal structure is sound. This safeguard records those threats separately from conditions inside the country.",
    "No significant predatory neighbor threat identified.":
      "No major threat from a hostile neighboring state was identified.",
    "The base is already high, so large structural jumps from here are historically rare.":
      "The institutional starting level is already high, and large further increases are uncommon in the historical data.",
    "accountability roughly tracks capacity and income.":
      "Accountability is broadly in line with state capacity and income.",
    "accountability trails income/capacity, partial; watch.":
      "Accountability trails income and state capacity. The available evidence is partial, so this remains a watch item.",
    "Institutions match or exceed what the country's income would predict. Prosperity here looks earned, and durable.":
      "Institutions match or exceed the level predicted by income. The historical comparison suggests that this prosperity is more durable.",
    "Starting from a low institutional base, the country is structurally eligible to climb. This is eligibility, not a forecast, the effect only showed up strongly in the 2000s global growth wave.":
      "The country starts from a low institutional level, which was associated with improvement during the 2000s. That period-specific pattern is not a forecast.",
    "A large share of prosperity comes from extracting resources rather than from strong institutions or a complex economy. Historically this masks structural weakness, the money can vanish with a price swing.":
      "A large share of income comes from resource extraction rather than a diverse economy. That dependence can expose the country to price swings and can conceal institutional weakness.",
    "Generated by the deterministic mi-research engine over all available public data. Each country carries the full safeguard board plus diagnostics for strategy, vulnerability, movement, and sensitivity. Countries with partial data show fewer pillars, and safeguards needing curated context read 'not assessed'. Gaps are shown, never filled with invented values.":
      "Generated from the available public data with the same scoring code for every country. Country profiles show the five pillars, additional checks, changes over time, and tests using alternative weights. Missing data remains visible, and checks that need a human review are labeled 'not assessed'.",
    "Independently derived on 21 crisis/absorber cases: the level gap between income (P4) and institutions (P1) separated real crises from shock-absorbers at 83% sensitivity / 100% specificity. When income has outrun institutions, the state is structurally crisis-prone under shock: 'granted/fragile'.":
      "In a 21-case historical comparison, an income-to-institutions gap above 0.28 identified 83 percent of the crisis cases without flagging any lower-risk cases. The sample is small and retrospective, so the threshold should be treated as provisional.",
    "N=21 acute-signature test set": "21-case crisis comparison",
    "N=21 signature set": "21-case comparison",
    "unifies with the durability ratio": "consistent with the income and institutions gap",
    "No significant sub-state turbulence indicators.": "No significant local political instability was identified.",
    "No backstop-porosity configuration detected.": "No combination of outside support and power-sharing was identified.",
    "Ethiopia / Tigray (AU backstop)": "Ethiopia / Tigray (African Union support)",
    "Myanmar (China backstop)": "Myanmar (Chinese support)",
    "No fragmentation mechanism specified.": "No relevant fragmentation case was identified.",
    "Exploratory note (v3.2): informational; orthogonal to the durability gap; no crisis validation yet.":
      "This is an exploratory comparison. It is separate from the income and institutions gap and has not yet been tested against crisis outcomes.",
  };

  text = replacements[text] ?? text;
  const safeguardNames: Record<string, string> = {
    A: "external administrator",
    B: "low institutional capacity",
    C: "post-transition reversal risk",
    D: "external threat",
    E: "resource dependence",
    G: "control compared with prevention",
    I: "outside support and power-sharing",
    J: "income and institutions gap",
  };
  text = text.replace(/^Active safeguards: ([A-Z, ]+)$/, (_match, value: string) => {
    const labels = value
      .split(",")
      .map((code) => safeguardNames[code.trim()] ?? code.trim())
      .filter(Boolean);
    return `Flagged checks: ${labels.join(", ")}`;
  });
  return text
    .replace(/^Highly modernized(?=[,.:]|$)/, "Very high structural capacity")
    .replace(/^Structurally durable(?=[,.:]|$)/, "High structural capacity")
    .replace(/^Mixed structural profile(?=[,.:]|$)/, "Mixed structural capacity")
    .replace(/^Structurally fragile(?=[,.:]|$)/, "Low structural capacity")
    .replace(/^(.+) is the pillar dragging the score down\. A chain breaks at its weakest link, so this is where the structural risk concentrates\.$/,
      "$1 is the lowest pillar and the main source of imbalance in the score.")
    .replace(/Re-suppression after porosity \(WORST\)/gi, "Renewed suppression after power-sharing")
    .replace(/\bporosity\b/gi, "power-sharing")
    .replace(/absorber ceiling/gi, "lower-risk threshold")
    .replace(/confirmed absorber/gi, "confirmed lower-risk case")
    .replace(/crisis floor/gi, "crisis threshold")
    .replace(/granted\/fragile/gi, "institutions lag income")
    .replace(/\babsorber-class\b/gi, "lower-risk case")
    .replace(/\bsafeguard\b/gi, "check")
    .replace(/\bsub-state\b/gi, "local")
    .replace(/\banti-system voting\b/gi, "voting for parties that reject the current system")
    .replace(/\bbackstop\b/gi, "outside support")
    .replace(/^Watch: P1 below median, elevated structural risk$/i, "Watch: Institutions score is below the median")
    .replace(/^High concern: P1 in bottom third, high fragmentation\/violence risk$/i, "High concern: Institutions score is in the bottom third")
    .replace(/^Watch: Pillar spread ([0-9.]+), significant imbalance$/i, "Watch: $1 gap between the highest and lowest pillars")
    .replace(/^High concern: Pillar spread ([0-9.]+), extreme configuration imbalance$/i, "High concern: $1 gap between the highest and lowest pillars")
    .replace(/^Durability Gate \(P4-P1 gap\)$/i, "Income and institutions gap")
    .replace(/^Rentier Capture \(Bidirectional\)$/i, "Resource dependence")
    .replace(/^External Administration$/i, "External administrator")
    .replace(/^Capacity Gate$/i, "Low institutional capacity")
    .replace(/^Predatory Neighbor \/ Exogenous Shock$/i, "External threat")
    .replace(/^Reversal Risk$/i, "Post-transition reversal risk")
    .replace(/^Sub-State Turbulence$/i, "Local political instability")
    .replace(/^(?:Porosity|power-sharing)-with-Backstop$/i, "Outside support and power-sharing")
    .replace(/^Suppression vs Prevention$/i, "Control compared with prevention")
    .replace(/^needs curated input$/i, "not reviewed")
    .replace(/^no such condition$/i, "condition not found")
    .replace(/^condition present$/i, "condition found")
    .replace(/^earned-vs-granted/i, "institutional gap")
    .replace(/^E-1 \(material\)$/i, "Material resource dependence")
    .replace(/^E-2 \(severe\)$/i, "Severe resource dependence");
}

export function naturalizeCopy(value: unknown, key?: string): unknown {
  if (typeof value === "string") return naturalizeString(value);
  if (Array.isArray(value)) return value.map((item) => naturalizeCopy(item));
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value).map(([childKey, childValue]) => [childKey, naturalizeCopy(childValue, childKey)]),
    );
  }
  return value;
}
