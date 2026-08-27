export const metadata = { title: "Stories | Modernization Index" };

const STORIES = [
  ["The fall of Rome", "ancient", "A look at institutional strain, external pressure, and the limits of the surviving evidence.", true],
  ["The conquest of the Aztecs", "ancient", "How internal divisions, disease, and outside alliances changed the balance of power.", true],
  ["The post-Soviet split", "modern", "Why Estonia, Russia, and Ukraine followed different paths after a shared political break.", false],
  ["The fall of Kabul", "modern", "What happened when a state that relied heavily on outside support lost that support.", false],
  ["The Gulf War", "modern", "How Kuwait's external alliances shaped the outcome after the invasion.", false],
  ["Venezuela's collapse", "modern", "How resource wealth and weakening institutions moved in opposite directions.", false],
  ["The Arab Spring", "modern", "Why a regional protest wave produced very different outcomes across countries.", false],
  ["The two Koreas", "modern", "A comparison of two states that began with similar conditions and developed very differently.", false],
  ["The Velvet Divorce", "modern", "Why one national separation remained peaceful while other breakups became violent.", false],
];

export default function Stories() {
  return (
    <div className="py-12">
      <div className="mx-auto max-w-2xl text-center">
        <h1 className="serif text-3xl font-black">Stories</h1>
        <p className="mt-3 text-[15px] leading-relaxed text-fg2">
          These short case studies use familiar events to show how the framework works. They also note
          when the available evidence is thin or open to more than one reading.
        </p>
      </div>
      <div className="mx-auto mt-8 grid max-w-4xl gap-3 sm:grid-cols-2">
        {STORIES.map(([title, kind, hook, limited]) => (
          <div key={title as string} className="card flex flex-col gap-2 p-5">
            <div className="flex items-center gap-2">
              <span className="mono text-[10px] uppercase tracking-wider text-fg3">{kind}</span>
              {limited && (
                <span className="mono rounded bg-warn/10 px-1.5 py-0.5 text-[9px] text-warn">
                  limited evidence
                </span>
              )}
            </div>
            <h2 className="serif text-lg leading-tight">{title}</h2>
            <p className="text-[13px] text-fg2">{hook}</p>
            <span className="mono mt-auto pt-1 text-[10px] text-fg3">writing in progress</span>
          </div>
        ))}
      </div>
      <p className="mx-auto mt-8 max-w-2xl text-center text-[12px] text-fg3">
        Each story separates the known facts, the framework&apos;s reading, and the remaining uncertainty.
        Ancient cases are labeled as limited evidence because their records are less complete.
      </p>
    </div>
  );
}
