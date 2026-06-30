type Props = {
  pillars: Record<string, number | null>;
  names: Record<string, string>;
  size?: number;
};

const ORDER = ["P1", "P2", "P3", "P4", "P5"];
const SHORT: Record<string, string> = {
  P1: "Institutions",
  P2: "Complexity",
  P3: "Human cap.",
  P4: "Economy",
  P5: "Stability",
};

export default function Radar({ pillars, size = 260 }: Props) {
  const cx = size / 2;
  const cy = size / 2;
  const r = size / 2 - 54;
  const n = ORDER.length;
  const angle = (i: number) => -Math.PI / 2 + (i * 2 * Math.PI) / n;
  const pt = (i: number, frac: number) => [cx + r * frac * Math.cos(angle(i)), cy + r * frac * Math.sin(angle(i))];

  const rings = [0.25, 0.5, 0.75, 1].map((f) => ORDER.map((_, i) => pt(i, f).join(",")).join(" "));
  const filled = ORDER.map((p, i) => pt(i, pillars[p] == null ? 0 : (pillars[p] as number)).join(",")).join(" ");

  return (
    <svg viewBox={`0 0 ${size} ${size}`} width={size} height={size}>
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
        const ox = lx + (lx - cx) * 0.1;
        const oy = ly + (ly - cy) * 0.1;
        const v = pillars[p];
        const anchor = Math.abs(ox - cx) < 8 ? "middle" : ox > cx ? "start" : "end";
        return (
          <text key={p} x={ox} y={oy} textAnchor={anchor} dominantBaseline="middle" className="mono" fontSize={9.5}>
            <tspan fontWeight={600} fill={v == null ? "#6b6b82" : "#cfcfe0"}>{p}</tspan>
            <tspan x={ox} dy={11} fontSize={8} fill={v == null ? "#6b6b82" : "#8a8aa0"}>
              {v == null ? "no data" : SHORT[p]}
            </tspan>
          </text>
        );
      })}
    </svg>
  );
}
