#!/usr/bin/env python3
"""EXTERNAL hand-coded country attributes (not in the repo). Legal origin = the La Porta et al.
commercial-law classification (English/French/German/Scandinavian/Socialist); colonizer = last
major colonial ruler. Compiled from published sources for the countries in the V-Dem panel;
best-effort, ISO3-keyed. Flagged as external per the repo's 'don't fake real data — flag it' rule.
Mixed/unclear cases assigned the dominant tradition or left out (None -> dropped)."""

LEGAL_ORIGIN = {
 # English common law (UK + settler + British colonies)
 **{k:"English" for k in ["GBR","USA","IRL","CAN","AUS","NZL","IND","PAK","BGD","LKA","MYS","SGP",
   "MMR","ISR","ZAF","NGA","GHA","KEN","UGA","TZA","ZMB","ZWE","MWI","SLE","GMB","LBR","BWA","LSO",
   "SWZ","NAM","SDN","SSD","JAM","TTO","GUY","BLZ","BHS","BRB","MUS","CYP","MLT","FJI","PNG","YEM"]},
 # French civil law (France/Iberia/Low Countries + their colonies + Latin America + Francophone Africa + much of MENA/SE-Asia)
 **{k:"French" for k in ["FRA","BEL","NLD","LUX","ITA","ESP","PRT","GRC",
   "BRA","ARG","MEX","CHL","COL","PER","VEN","ECU","BOL","PRY","URY","GTM","HND","SLV","NIC","CRI",
   "PAN","DOM","HTI",
   "SEN","CIV","MLI","BFA","NER","TCD","CMR","GAB","COG","COD","CAF","BEN","TGO","GIN","GNB","MDG",
   "DJI","MRT","BDI","RWA","COM","GNQ","MAR","DZA","TUN","EGY","LBN","SYR","JOR","IRQ","LBY",
   "IDN","PHL","KHM","THA","TUR","MOZ","AGO","CPV","STP","SUR"]},
 # German civil law
 **{k:"German" for k in ["DEU","AUT","CHE","JPN","KOR","TWN"]},
 # Scandinavian
 **{k:"Scandinavian" for k in ["SWE","NOR","DNK","FIN","ISL"]},
 # Socialist / post-communist legal heritage
 **{k:"Socialist" for k in ["RUS","UKR","BLR","MDA","POL","CZE","SVK","HUN","ROU","BGR","ALB","SRB",
   "HRV","SVN","BIH","MKD","MNE","EST","LVA","LTU","KAZ","UZB","TKM","KGZ","TJK","GEO","ARM","AZE",
   "MNG","CHN","VNM","CUB","PRK","LAO"]},
}

COLONIZER = {
 **{k:"British" for k in ["USA","CAN","AUS","NZL","IND","PAK","BGD","LKA","MYS","SGP","MMR","ZAF",
   "NGA","GHA","KEN","UGA","TZA","ZMB","ZWE","MWI","SLE","GMB","BWA","LSO","SWZ","SDN","SSD","JAM",
   "TTO","GUY","BLZ","EGY","IRQ","JOR","ISR","YEM","FJI","PNG","MUS","CYP"]},
 **{k:"French" for k in ["SEN","CIV","MLI","BFA","NER","TCD","CMR","GAB","COG","CAF","BEN","TGO",
   "GIN","MDG","DJI","MRT","DZA","TUN","MAR","LBN","SYR","KHM","LAO","VNM"]},
 **{k:"Spanish" for k in ["MEX","ARG","CHL","COL","PER","VEN","ECU","BOL","PRY","URY","GTM","HND",
   "SLV","NIC","CRI","PAN","DOM","CUB","PHL","GNQ"]},
 **{k:"Portuguese" for k in ["BRA","AGO","MOZ","CPV","GNB","STP","GNQ"]},
 **{k:"Belgian" for k in ["COD","RWA","BDI"]},
 **{k:"Dutch" for k in ["IDN","SUR"]},
}

def legal_origin(iso): return LEGAL_ORIGIN.get(iso)
def colonizer(iso): return COLONIZER.get(iso)

if __name__=="__main__":
    from collections import Counter
    print("legal origin coverage:", len(LEGAL_ORIGIN), Counter(LEGAL_ORIGIN.values()))
    print("colonizer coverage:", len(COLONIZER), Counter(COLONIZER.values()))
