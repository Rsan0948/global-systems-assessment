export const metadata = { title: "What this can and cannot tell you | Modernization Index" };

const LIMITS = [
  [
    "It describes structure, not timing",
    "The index compares the conditions that can help a country absorb stress. It does not say when a crisis will begin or which event will trigger it.",
  ],
  [
    "A score is not a forecast",
    "A low score can persist for years without a major break, and a high-scoring country can still be harmed by war, disaster, or another outside shock.",
  ],
  [
    "A repeated result is not proof",
    "Most historical cases were scored after their outcomes were known. They show that the method can be applied consistently, but they do not provide the same evidence as a successful test registered in advance.",
  ],
  [
    "Missing data stays missing",
    "When the required public data is unavailable, the site leaves the gap visible. An empty axis means unmeasured, not zero, and an unscored country has not been assigned a grade.",
  ],
  [
    "The result comes from a fixed calculation",
    "The score is calculated from published data using the same code for every country. You can inspect the inputs, run the code, and reproduce the result.",
  ],
];

export default function Limits() {
  return (
    <div className="prose-mi mx-auto max-w-2xl py-12">
      <h1 className="serif text-3xl font-black">What this can and can&apos;t tell you</h1>
      <p className="mt-4 text-[15px] leading-relaxed text-fg2">
        Use the index to compare structural conditions and see what drives each score. Keep these
        limits in mind when interpreting the results.
      </p>

      {LIMITS.map(([heading, body]) => (
        <div key={heading} className="mt-7">
          <h2 className="serif text-lg">{heading}</h2>
          <p className="mt-1.5 text-[14px] leading-relaxed text-fg2">{body}</p>
        </div>
      ))}
    </div>
  );
}
