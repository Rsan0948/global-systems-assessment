"""Shared country-code / country-name → ISO3 resolution for the robustness program.

Consolidates maps that were previously duplicated across scripts:
  * ``GW_ISO_BASE`` — Gleditsch-Ward country number → ISO3 (was verbatim in both
    ``data/robustness/outcomes/grade.py`` and ``scripts/historical/build_conflict_onsets.py``).
  * ``GW_ISO_EXTENDED`` — the base + 8 onset-bearing GW codes absent from grade.py's
    map. ``build_conflict_onsets`` uses this; ``grade.py`` uses BASE (so its
    ``ucdp_unmapped_gw_codes`` output stays exactly those 8 codes).
  * ``CRAG_NAME_MANUAL`` — CRAG country-name → ISO3 overrides (was inline in grade.py).
  * ``COW_NAME_MANUAL`` — Correlates-of-War StateNme → ISO3 overrides (was inline in
    build_conflict_onsets).

``name_to_iso(name, manual)`` reproduces the original manual-then-pycountry lookup.
"""

# ---------- Gleditsch-Ward country number -> ISO3 ----------
GW_ISO_BASE = {
 2: 'USA', 20: 'CAN', 40: 'CUB', 41: 'HTI', 42: 'DOM', 70: 'MEX', 90: 'GTM', 91: 'HND', 92: 'SLV',
 93: 'NIC', 95: 'PAN', 100: 'COL', 101: 'VEN', 110: 'GUY', 130: 'ECU', 135: 'PER', 140: 'BRA',
 145: 'BOL', 150: 'PRY', 155: 'CHL', 160: 'ARG', 165: 'URY', 200: 'GBR', 205: 'IRL', 210: 'NLD',
 211: 'BEL', 212: 'LUX', 220: 'FRA', 225: 'CHE', 230: 'ESP', 235: 'PRT', 255: 'DEU', 290: 'POL',
 305: 'AUT', 310: 'HUN', 316: 'CZE', 317: 'SVK', 325: 'ITA', 338: 'MLT', 339: 'ALB', 341: 'MNE',
 343: 'MKD', 344: 'HRV', 345: 'SRB', 346: 'BIH', 349: 'SVN', 350: 'GRC', 352: 'CYP', 355: 'BGR',
 359: 'MDA', 360: 'ROU', 365: 'RUS', 366: 'EST', 367: 'LVA', 368: 'LTU', 369: 'UKR', 370: 'BLR',
 371: 'ARM', 372: 'GEO', 373: 'AZE', 375: 'FIN', 380: 'SWE', 385: 'NOR', 390: 'DNK', 395: 'ISL',
 402: 'CPV', 404: 'GNB', 411: 'GNQ', 420: 'GMB', 432: 'MLI', 433: 'SEN', 434: 'BEN', 435: 'MRT',
 436: 'NER', 437: 'CIV', 438: 'GIN', 439: 'BFA', 450: 'LBR', 451: 'SLE', 452: 'GHA', 461: 'TGO',
 471: 'CMR', 475: 'NGA', 481: 'GAB', 482: 'CAF', 483: 'TCD', 484: 'COG', 490: 'COD', 500: 'UGA',
 501: 'KEN', 510: 'TZA', 516: 'BDI', 517: 'RWA', 520: 'SOM', 522: 'DJI', 530: 'ETH', 531: 'ERI',
 540: 'AGO', 541: 'MOZ', 551: 'ZMB', 552: 'ZWE', 553: 'MWI', 560: 'ZAF', 565: 'NAM', 570: 'LSO',
 571: 'BWA', 572: 'SWZ', 580: 'MDG', 590: 'MUS', 600: 'MAR', 615: 'DZA', 616: 'TUN', 620: 'LBY',
 625: 'SDN', 626: 'SSD', 630: 'IRN', 640: 'TUR', 645: 'IRQ', 651: 'EGY', 652: 'SYR', 660: 'LBN',
 663: 'JOR', 666: 'ISR', 670: 'SAU', 678: 'YEM', 680: 'YEM', 690: 'KWT', 692: 'BHR', 694: 'QAT',
 696: 'ARE', 698: 'OMN', 700: 'AFG', 701: 'TKM', 702: 'KGZ', 703: 'TJK', 704: 'UZB', 705: 'KAZ',
 710: 'CHN', 712: 'MNG', 713: 'TWN', 731: 'PRK', 732: 'KOR', 740: 'JPN', 750: 'IND', 760: 'BTN',
 770: 'PAK', 771: 'BGD', 775: 'MMR', 780: 'LKA', 781: 'MDV', 790: 'NPL', 800: 'THA', 811: 'KHM',
 812: 'LAO', 816: 'VNM', 820: 'MYS', 830: 'SGP', 840: 'PHL', 850: 'IDN', 860: 'TLS', 900: 'AUS',
 910: 'PNG', 920: 'NZL', 990: 'WSM',
}

# Onset-bearing GW codes absent from grade.py's base map (build_conflict_onsets only).
_GW_ISO_EXTENSIONS = {
 52: 'TTO', 55: 'GRD', 94: 'CRI', 115: 'SUR', 581: 'COM', 751: 'IND', 817: 'VNM', 835: 'BRN',
}
GW_ISO_EXTENDED = {**GW_ISO_BASE, **_GW_ISO_EXTENSIONS}

# ---------- CRAG country-name -> ISO3 overrides (grade.py) ----------
CRAG_NAME_MANUAL = {
 'Korea, Republic of': 'KOR', 'Korea': 'KOR', 'Russia': 'RUS', 'Russian Federation': 'RUS',
 'Congo, Dem. Rep.': 'COD', 'Congo, Democratic Republic of the': 'COD', 'Congo': 'COG',
 'Congo, Republic of': 'COG', 'Democratic Republic of the Congo': 'COD',
 'Egypt': 'EGY', 'Iran': 'IRN', 'Syria': 'SYR', 'Venezuela': 'VEN', 'Bolivia': 'BOL',
 'Tanzania': 'TZA', 'Vietnam': 'VNM', 'Laos': 'LAO', 'Moldova': 'MDA', 'Macedonia': 'MKD',
 'Slovak Republic': 'SVK', 'Kyrgyz Republic': 'KGZ', 'Yemen': 'YEM', 'Cape Verde': 'CPV',
 "Cote d'Ivoire": 'CIV', "Côte d'Ivoire": 'CIV', 'Ivory Coast': 'CIV', 'Gambia, The': 'GMB',
 'Gambia': 'GMB', 'Turkiye': 'TUR', 'Turkey': 'TUR', 'Brunei': 'BRN', 'Taiwan': 'TWN',
 'Bosnia & Herzegovina': 'BIH', 'USSR/Russia': 'RUS',
 'Dem. Rep. of Congo (Kinshasa)': 'COD', 'Rep. Of Congo (Brazzaville)': 'COG',
 "Côte d’Ivoire": 'CIV', 'Swaziland': 'SWZ', 'Korea (North)': 'PRK',
 'Trinidad & Tobago': 'TTO', 'São Tomé and Príncipe': 'STP',
}

# ---------- COW StateNme -> ISO3 overrides (historical / renamed / merged states) ----------
COW_NAME_MANUAL = {
 'German Federal Republic': 'DEU', 'German Democratic Republic': 'DEU', 'Prussia': 'DEU',
 'Germany (Prussia)': 'DEU', 'Baden': 'DEU', 'Bavaria': 'DEU', 'Saxony': 'DEU', 'Wuerttemburg': 'DEU',
 'Hesse Electoral': 'DEU', 'Hesse Grand Ducal': 'DEU', 'Hesse-Kassel (Electoral)': 'DEU',
 'Hesse-Darmstadt (Ducal)': 'DEU', 'Mecklenburg Schwerin': 'DEU', 'Hanover': 'DEU',
 'Austria-Hungary': 'AUT', 'Yugoslavia': 'SRB', 'Serbia': 'SRB', 'Rumania': 'ROU',
 'Russia (Soviet Union)': 'RUS', 'Russia': 'RUS', 'Korea': 'KOR',
 "Korea, People's Republic of": 'PRK', 'Korea, Republic of': 'KOR',
 'Democratic Republic of the Congo': 'COD', 'Congo': 'COG', 'Zaire': 'COD',
 'Vietnam, Democratic Republic of': 'VNM', 'Republic of Vietnam': 'VNM',
 'Democratic Republic of Vietnam': 'VNM', 'Vietnam': 'VNM',
 'Iran (Persia)': 'IRN', 'Turkey (Ottoman Empire)': 'TUR', 'Turkey': 'TUR', 'Kyrgyzstan': 'KGZ',
 'Cote D’Ivoire': 'CIV', 'Ivory Coast': 'CIV', 'Cote d’Ivoire': 'CIV',
 'Tanzania': 'TZA', 'Tanzania/Tanganyika': 'TZA', 'Myanmar (Burma)': 'MMR', 'Burma': 'MMR',
 'Cambodia (Kampuchea)': 'KHM', 'Cambodia': 'KHM', 'Sri Lanka (Ceylon)': 'LKA',
 'Zimbabwe (Rhodesia)': 'ZWE', 'Yemen Arab Republic': 'YEM', 'Yemen': 'YEM',
 "Yemen People's Republic": 'YEM', 'Yemen People’s Republic': 'YEM',
 'Macedonia': 'MKD', 'Macedonia (FYROM)': 'MKD', 'Bosnia and Herzegovina': 'BIH',
 'Laos': 'LAO', 'Moldova': 'MDA', 'Belarus (Byelorussia)': 'BLR', 'Cape Verde': 'CPV',
 'Sao Tome and Principe': 'STP', 'Surinam': 'SUR', 'Trinidad and Tobago': 'TTO',
 'Papal States': 'ITA', 'Two Sicilies': 'ITA', 'Sardinia': 'ITA', 'Modena': 'ITA',
 'Parma': 'ITA', 'Tuscany': 'ITA', 'Ethiopia': 'ETH', 'Abyssinia': 'ETH', 'East Timor': 'TLS',
 'Swaziland': 'SWZ', 'Gambia': 'GMB', 'United States of America': 'USA', 'United Kingdom': 'GBR',
 'Czechoslovakia': 'CZE', 'Kosovo': 'SRB', 'Zanzibar': 'TZA', 'Brunei': 'BRN',
 'St. Lucia': 'LCA', 'St. Vincent and the Grenadines': 'VCT', 'Antigua & Barbuda': 'ATG',
 'St. Kitts and Nevis': 'KNA',
}


def name_to_iso(name, manual):
    """Resolve a country name to ISO3: manual override first, then pycountry.

    Matches the original inline resolvers in grade.py / build_conflict_onsets.
    Returns None if unresolved.
    """
    if name in manual:
        return manual[name]
    try:
        import pycountry
        return pycountry.countries.lookup(name).alpha_3
    except Exception:
        return None
