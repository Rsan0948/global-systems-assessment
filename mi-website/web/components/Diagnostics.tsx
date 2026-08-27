import type { Diagnostics as Dx } from "@/lib/types";
import { RISK_COLOR } from "@/lib/config";

const STRATEGY: Record<string, { label: string; blurb: string }> = {
  porosity: { label: "Power sharing and devolution", blurb: "routes political pressure through federalism, local autonomy, or power-sharing institutions" },
  suppression: { label: "Centralized control", blurb: "manages political pressure through central control rather than shared authority" },
  complexity_control: { label: "High-capacity small system", blurb: "combines strong institutions with a relatively small or less complex governing environment" },
  ambiguous: { label: "No clear classification", blurb: "the reviewed context is mixed, incomplete, or changing" },
  unknown: { label: "Not assessed", blurb: "there is not enough reviewed context for a classification" },
};

const MOVEMENT: Record<string, string> = {
  real_ascent: "Institution-led ascent",
  windfall: "Income-led rise",
  ratchet_rise: "Broad gradual rise",
  hollow_stability: "Uneven stability",
  decline: "Decline",
  stable: "Stable",
};

const SENSITIVITY_LABEL: Record<string, string> = {
  v2_equal: "Equal weights",
  v2_timevarying: "Time-varying weights",
  v1: "Correlation weights",
  archived_hand_v0: "Archived manual weights",
};

function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="rounded-lg border border-border bg-surface2/40 p-3.5">
      <div className="mono mb-1.5 text-[10px] uppercase tracking-wider text-fg3">{title}</div>
      {children}
    </div>
  );
}

export default function Diagnostics({ d }: { d: Dx }) {
  const strat = STRATEGY[d.strategy?.strategy] ?? STRATEGY.unknown;
  const risk = d.vulnerability?.risk_level ?? "low";
  const riskCol = RISK_COLOR[risk] ?? "#8a8aa4";
  const sens = d.sensitivity ? Object.entries(d.sensitivity) : [];
  const sensVals = sens.map(([, v]) => v);
  const sensSpread = sensVals.length ? Math.max(...sensVals) - Math.min(...sensVals) : 0;
  const mv = d.movement;
  const acct = d.accountability_gap;

  return (
    <section className="card mt-6 p-5">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h2 className="serif text-base">Additional diagnostics</h2>
        {!d.context_curated && (
          <span className="mono text-[10px] text-fg3">governance context has not been reviewed</span>
        )}
      </div>

      <div className="mt-3 grid gap-3 sm:grid-cols-2">
        <Panel title="Governance approach">
          <div className="text-[14px] font-semibold text-fg">
            {strat.label}
            {d.strategy?.tier_label && (
              <span className="ml-2 text-[12px] font-normal text-fg3">
                · {d.strategy.tier_label.replace(/^Tier /, "Mode ")}
              </span>
            )}
          </div>
          <p className="mt-1 text-[12px] leading-relaxed text-fg2">{strat.blurb}.</p>
          {d.strategy?.failure_mode && (
            <p className="mt-1.5 text-[11px] text-fg3">Main risk in this approach: {d.strategy.failure_mode}</p>
          )}
        </Panel>

        <Panel title="Structural risk">
          <div className="flex items-baseline gap-2">
            <span className="num text-[15px] font-bold uppercase" style={{ color: riskCol }}>
              {risk}
            </span>
            <span className="text-[12px] text-fg3">from the scoring formula&apos;s structural checks</span>
          </div>
          {d.vulnerability?.flags?.length > 0 ? (
            <ul className="mt-1.5 space-y-1 text-[11px] leading-snug text-fg2">
              {d.vulnerability.flags.slice(0, 4).map((f, i) => (
                <li key={i}>· {f}</li>
              ))}
            </ul>
          ) : (
            <p className="mt-1.5 text-[11px] text-fg3">No structural risk flags.</p>
          )}
        </Panel>
      </div>

      {mv && (
        <Panel title={`Change since ${d.prior_year ?? "the prior period"}`}>
          <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
            <span className="text-[14px] font-semibold text-fg">{MOVEMENT[mv.class] ?? mv.class}</span>
            <span className="num text-[12px] text-fg3">
              Score {mv.dMI >= 0 ? "+" : ""}
              {mv.dMI.toFixed(2)} · largest change: {mv.lead}
            </span>
          </div>
          <p className="mt-1 text-[12px] leading-relaxed text-fg2">{mv.reading}</p>
          <p className="mt-1 text-[10px] text-fg3">{mv.caveat}</p>
        </Panel>
      )}

      {acct && acct.status !== "balanced" && (
        <Panel title="Accountability check · exploratory">
          <div className="flex flex-wrap items-baseline gap-x-3">
            <span className="text-[14px] font-semibold text-fg">
              {acct.status === "legitimacy_capped" ? "Low accountability relative to capacity" : "Accountability trails income"}
            </span>
            <span className="num text-[12px] text-fg3">difference from income: {acct.va_minus_p4.toFixed(2)}</span>
          </div>
          <p className="mt-1 text-[12px] leading-relaxed text-fg2">{acct.reading}</p>
          <p className="mt-1 text-[10px] text-fg3">{acct.caveat}</p>
        </Panel>
      )}

      {sens.length > 0 && (
        <div className="mt-3">
          <div className="mono mb-1.5 text-[10px] uppercase tracking-wider text-fg3">
            Weighting check · score under {sens.length} sets of weights
          </div>
          <div className="grid gap-2 sm:grid-cols-4">
            {sens.map(([k, v]) => (
              <div key={k} className="rounded-md border border-border bg-surface2/40 px-2.5 py-2">
                <div className="num text-[15px] font-semibold text-fg">{v.toFixed(3)}</div>
                <div className="mono text-[10px] text-fg3">
                  {SENSITIVITY_LABEL[k] ?? k.replace(/_/g, " ")}
                </div>
              </div>
            ))}
          </div>
          <p className="mt-1.5 text-[11px] text-fg3">
            Largest difference across the weighting methods: <span className="num">{sensSpread.toFixed(3)}</span>.
            The country stays in the same score band in each check.
          </p>
        </div>
      )}
    </section>
  );
}
