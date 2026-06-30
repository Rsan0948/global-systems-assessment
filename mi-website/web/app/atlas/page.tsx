import { getCountries } from "@/lib/data";
import AtlasTable from "@/components/AtlasTable";

export const metadata = { title: "Atlas — Modernization Index" };

export default function Atlas() {
  return (
    <div className="py-10">
      <h1 className="serif text-3xl font-black">The Atlas</h1>
      <p className="mt-2 max-w-2xl text-[14px] text-fg2">
        Every scored country, rankable by any pillar. The score is a deterministic formula over public
        data — sort it, don&apos;t trust it blindly.
      </p>
      <div className="mt-6">
        <AtlasTable countries={getCountries()} />
      </div>
    </div>
  );
}
