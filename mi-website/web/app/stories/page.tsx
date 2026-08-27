export const metadata = { title: "Stories - Modernization Index" };

const STORIES = [
  ["The fall of Rome", "ancient", "Everyone blames decadence. The structure tells a different story.", true],
  ["The conquest of the Aztecs", "ancient", "How a few hundred men toppled an empire - the exposure layer explains it.", true],
  ["The post-Soviet split", "modern", "Estonia, Russia, Ukraine: same starting gun, three destinies.", false],
  ["The fall of Kabul", "modern", "It wasn't really about the Taliban. It was a propped-up state, and the prop left.", false],
  ["The Gulf War", "modern", "Kuwait was conquered - then handed back. The clearest 'who has your back' story.", false],
  ["Venezuela's collapse", "modern", "Richest in Latin America to people fleeing - the durability gap as a human story.", false],
  ["The Arab Spring", "modern", "One wave, wildly different fates. The natural experiment everyone remembers.", false],
  ["The two Koreas", "modern", "The most extreme experiment on Earth - and the framework reads the split.", false],
  ["The Velvet Divorce", "modern", "The breakup that didn't become Yugoslavia. Why do some splits stay peaceful?", false],
];

export default function Stories() {
  return (
    <div className="py-12">
      <div className="mx-auto max-w-2xl text-center">
        <h1 className="serif text-3xl font-black">Stories</h1>
        <p className="mt-3 text-[15px] leading-relaxed text-fg2">
          Familiar history, read through the structure - and sometimes the structure disagrees with the
          textbook. A curated set; the full library lives in the book.
        </p>
      </div>
      <div className="mx-auto mt-8 grid max-w-4xl gap-3 sm:grid-cols-2">
        {STORIES.map(([title, kind, hook, firewalled]) => (
          <div key={title as string} className="card flex flex-col gap-2 p-5">
            <div className="flex items-center gap-2">
              <span className="mono text-[10px] uppercase tracking-wider text-fg3">{kind}</span>
              {firewalled && (
                <span className="mono rounded bg-warn/10 px-1.5 py-0.5 text-[9px] text-warn">
                  lowest-confidence evidence level
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
        Each story follows one shape: the event you know → what everyone thinks happened → what the
        structure shows → the reframe. The ancient cases carry our lowest-confidence lens - we say so,
        because applying a careful instrument to history&apos;s most famous collapses is the interesting
        part.
      </p>
    </div>
  );
}
