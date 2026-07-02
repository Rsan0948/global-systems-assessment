export const metadata = { title: "What this can & can't tell you - Modernization Index" };

export default function Limits() {
  return (
    <div className="prose-mi mx-auto max-w-2xl py-12">
      <h1 className="serif text-3xl font-black">What this can &amp; can&apos;t tell you</h1>
      <p className="mt-4 text-[15px] leading-relaxed text-fg2">
        This is a serious instrument, and serious instruments are honest about their range. None of
        what follows is a hedge - it&apos;s the difference between a diagnostic you can trust and a
        crystal ball you can&apos;t.
      </p>

      {[
        [
          "It reads structure, not timing",
          "The index tells you how a country is built to withstand stress - who is durable and who is fragile, and why. It does not tell you when something will happen. Trust the level; distrust the slope. The moment a specific crisis breaks is driven by contingency the structure can't see.",
        ],
        [
          "It's a diagnosis, not a forecast",
          "Like a doctor reading a chart: it identifies the structural conditions that have historically preceded instability. It does not predict events. A fragile country can stand for decades; a sturdy one can be struck from outside.",
        ],
        [
          "Consistency is not the same as proof",
          "The framework reproduces well across history, and it points the right way on cases it was selected for blind. But most of its track record was scored knowing the outcomes - that's reproducibility, not validated prediction. We say so plainly, and the one genuine forward test still pending is the honest measure.",
        ],
        [
          "Missing data is shown, never faked",
          "Where a country lacks the public data the engine needs, we leave the gap visible rather than guess. An empty axis means 'unmeasured,' not 'zero.' Roughly half the world's states aren't scored yet - they're dark, not graded.",
        ],
        [
          "It's a formula, not an opinion",
          "No model is interpreting anything here. The score is a fixed, deterministic calculation over citable public numbers. Same inputs, same answer, every time - and the engine is open source, so you can run it yourself.",
        ],
      ].map(([h, b]) => (
        <div key={h} className="mt-7">
          <h2 className="serif text-lg">{h}</h2>
          <p className="mt-1.5 text-[14px] leading-relaxed text-fg2">{b}</p>
        </div>
      ))}
    </div>
  );
}
