import { getCountries } from "@/lib/data";
import AtlasTable from "@/components/AtlasTable";
import { PageHeader, ScoreBandLegend } from "@/components/ui";

export const metadata = { title: "Atlas | Modernization Index" };

export default function Atlas() {
  const countries = getCountries();
  return (
    <div className="py-10">
      <PageHeader
        title="Country atlas"
        lede="Search all scored countries and sort by the overall score or any of the five pillars. When sorting by the overall score, complete five-pillar profiles appear before partial profiles."
      />
      <div className="mb-5">
        <ScoreBandLegend countries={countries} />
      </div>
      <AtlasTable countries={countries} />
    </div>
  );
}
