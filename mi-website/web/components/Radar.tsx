type Props = {
  pillars: Record<string, number | null>;
  names: Record<string, string>;
  size?: number;
};

const ORDER = ["P1", "P2", "P3", "P4", "P5"];

export default function Radar({ pillars, names, size = 280 }: Props) {
  const cx = size / 2;
  const cy = size / 2;
  const r = size / 2 - 46;
  const n = ORDER.length;
  const angle = (i: number) => -Math.PI / 2 + (i * 2 * Math.PI) / n;
  const pt = (i: number, frac: number) => [cx + r * frac * Math.cos(angle(i)), cy + r * frac * Math.sin(angle(i))];

  const rings = [0.25, 0.5, 0.75, 1].map((f) =>
    ORDER.map((_, i) => pt(i, f).join(",")).join(" ")
  );

  const filled = ORDER.map((p, i) => {
    const v = pillars[p];
    return pt(i, v == null ? 0 : v).join(",");
  }).join(" ");

  return (
    <svg viewBox={`0 0 ${size} ${size}`} width={size} height={size} className="overflow-visible">
      {rings.map((pts, i) => (
        <polygon key={i} points={pts} fill="none" stroke="#232338" strokeWidth={1} />
      ))}
      {ORDER.map((_, i) => {
        const [x, y] = pt(i, 1);
        return <line key={i} x1={cx} y1={cy} x2={x} y2={y} stroke="#232338" strokeWidth={1} />;
      })}
      <polygon points={filled} fill="#3b82f633" stroke="#60a5fa" strokeWidth={2} strokeLinejoin="round" />
      {ORDER.map((p, i) => {
        const v = pillars[p];
        const [x, y] = pt(i, v == null ? 0 : v);
        return <circle key={p} cx={x} cy={y} r={v == null ? 0 : 3} fill="#60a5fa" />;
      })}
      {ORDER.map((p, i) => {
        const [lx, ly] = pt(i, 1.0);
        const ox = lx + (lx - cx) * 0.18;
        const oy = ly + (ly - cy) * 0.18;
        const v = pillars[p];
        return (
          <text
            key={p}
            x={ox}
            y={oy}
            textAnchor={Math.abs(ox - cx) < 6 ? "middle" : ox > cx ? "start" : "end"}
            dominantBaseline="middle"
            className="mono"
            fontSize={10}
            fill={v == null ? "#6b6b82" : "#9a9ab0"}
          >
            <tspan fontWeight={600} fill={v == null ? "#6b6b82" : "#cfcfe0"}>{p}</tspan>
            <tspan x={ox} dy={12} fontSize={8.5}>{v == null ? "no data" : (names[p] ?? "")}</tspan>
          </text>
        );
      })}
    </svg>
  );
}
