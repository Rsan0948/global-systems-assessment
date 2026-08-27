import { getCountries } from "@/lib/data";
import AtlasTable from "@/components/AtlasTable";
import { PageHeader, ScoreBandLegend } from "@/components/ui";

export const metadata = { title: "Atlas - Modernization Index" };

export default function Atlas() {
  const countries = getCountries();
  return (
    <div className="py-10">
      <PageHeader
        title="The Atlas"
        lede="Every scored country, rankable by any pillar. Partial-data countries sort below the fully-measured ones."
      />
      <div className="mb-5">
        <ScoreBandLegend countries={countries} />
      </div>
      <AtlasTable countries={countries} />
    </div>
  );
}
