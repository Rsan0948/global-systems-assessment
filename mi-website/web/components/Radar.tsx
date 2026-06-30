import { PILLAR_ORDER, PILLARS, VALENCE, clamp01 } from "@/lib/config";

type Props = {
  pillars: Record<string, number | null>;
  size?: number;
};

const ORDER = PILLAR_ORDER;

export default function Radar({ pillars, size = 260 }: Props) {
  const cx = size / 2;
  const cy = size / 2;
  const r = size / 2 - 54;
  const n = ORDER.length;
  const angle = (i: number) => -Math.PI / 2 + (i * 2 * Math.PI) / n;
  const pt = (i: number, frac: number) => [cx + r * frac * Math.cos(angle(i)), cy + r * frac * Math.sin(angle(i))];

  const rings = [0.25, 0.5, 0.75, 1].map((f) => ORDER.map((_, i) => pt(i, f).join(",")).join(" "));
  // shape connects ONLY measured pillars (in angular order) - missing axes break the polygon
  // rather than pinching it through the center, so a 3/5 country reads as a triangle, not a 0.
  const filled = ORDER.map((p, i) => (pillars[p] == null ? null : pt(i, clamp01(pillars[p] as number)).join(",")))
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
      <polygon points={filled} fill={VALENCE.primary + "33"} stroke={VALENCE.primary} strokeWidth={2} strokeLinejoin="round" />
      {ORDER.map((p, i) => {
        const v = pillars[p];
        if (v == null) return null;
        const [x, y] = pt(i, clamp01(v));
        return <circle key={p} cx={x} cy={y} r={3} fill={VALENCE.primary} />;
      })}
      {ORDER.map((p, i) => {
        const [lx, ly] = pt(i, 1.0);
        const ox = lx + (lx - cx) * 0.1;
        const oy = ly + (ly - cy) * 0.1;
        const v = pillars[p];
        const anchor = Math.abs(ox - cx) < 8 ? "middle" : ox > cx ? "start" : "end";
        return (
          <text key={p} x={ox} y={oy} textAnchor={anchor} dominantBaseline="middle" className="mono" fontSize={9.5}>
            <tspan fontWeight={600} fill={v == null ? "#8a8aa4" : "#cfcfe0"}>{p}</tspan>
            <tspan x={ox} dy={11} fontSize={8} fill={v == null ? "#8a8aa4" : "#a6a6bd"}>
              {v == null ? "no data" : PILLARS[p].short}
            </tspan>
          </text>
        );
      })}
    </svg>
  );
}
