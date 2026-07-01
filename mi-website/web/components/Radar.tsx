import { PILLAR_ORDER, PILLARS, VALENCE, clamp01 } from "@/lib/config";

type Pillars = Record<string, number | null>;
type Props = {
  pillars: Pillars;
  overlay?: Pillars;
  colors?: [string, string];
  size?: number;
};

const ORDER = PILLAR_ORDER;

export default function Radar({ pillars, overlay, colors, size = 260 }: Props) {
  const cx = size / 2;
  const cy = size / 2;
  const r = size / 2 - 54;
  const n = ORDER.length;
  const cA = colors?.[0] ?? VALENCE.primary;
  const cB = colors?.[1] ?? "#f472b6";
  const angle = (i: number) => -Math.PI / 2 + (i * 2 * Math.PI) / n;
  const pt = (i: number, frac: number) => [cx + r * frac * Math.cos(angle(i)), cy + r * frac * Math.sin(angle(i))];

  const rings = [0.25, 0.5, 0.75, 1].map((f) => ORDER.map((_, i) => pt(i, f).join(",")).join(" "));
  const shape = (ps: Pillars) =>
    ORDER.map((p, i) => (ps[p] == null ? null : pt(i, clamp01(ps[p] as number)).join(",")))
      .filter(Boolean)
      .join(" ");
  const label =
    "Pillar profile: " +
    ORDER.map((p) => `${PILLARS[p].full} ${pillars[p] == null ? "no data" : pillars[p]!.toFixed(2)}`).join(", ");

  return (
    <svg viewBox={`0 0 ${size} ${size}`} width={size} height={size} role="img" aria-label={label}>
      {rings.map((pts, i) => (
        <polygon key={i} points={pts} fill="none" stroke="#232338" strokeWidth={1} />
      ))}
      {ORDER.map((_, i) => {
        const [x, y] = pt(i, 1);
        return <line key={i} x1={cx} y1={cy} x2={x} y2={y} stroke="#232338" strokeWidth={1} />;
      })}
      {overlay && (
        <polygon points={shape(overlay)} fill={cB + "22"} stroke={cB} strokeWidth={2} strokeLinejoin="round" />
      )}
      <polygon points={shape(pillars)} fill={cA + "33"} stroke={cA} strokeWidth={2} strokeLinejoin="round" />
      {ORDER.map((p, i) => {
        const v = pillars[p];
        if (v == null) return null;
        const [x, y] = pt(i, clamp01(v));
        return <circle key={p} cx={x} cy={y} r={3} fill={cA} />;
      })}
      {overlay &&
        ORDER.map((p, i) => {
          const v = overlay[p];
          if (v == null) return null;
          const [x, y] = pt(i, clamp01(v));
          return <circle key={`o${p}`} cx={x} cy={y} r={3} fill={cB} />;
        })}
      {ORDER.map((p, i) => {
        const [lx, ly] = pt(i, 1.0);
        const ox = lx + (lx - cx) * 0.1;
        const oy = ly + (ly - cy) * 0.1;
        const v = pillars[p];
        const anchor = Math.abs(ox - cx) < 8 ? "middle" : ox > cx ? "start" : "end";
        return (
          <text key={p} x={ox} y={oy} textAnchor={anchor} dominantBaseline="middle" className="mono" fontSize={9.5}>
            <tspan fontWeight={600} fill={v == null && !overlay ? "#8a8aa4" : "#cfcfe0"}>{p}</tspan>
            <tspan x={ox} dy={11} fontSize={8} fill={v == null && !overlay ? "#8a8aa4" : "#a6a6bd"}>
              {v == null && !overlay ? "no data" : PILLARS[p].short}
            </tspan>
          </text>
        );
      })}
    </svg>
  );
}
