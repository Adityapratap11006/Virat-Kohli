"""One-off generator for data/reference/venue_aliases.csv (tracked artifact).

Reads raw venue rows (id, name, city, match_count TSV) and emits one registry
row per raw venue using explicit curated family tables. No fuzzy merging:
families are declared by normalized base name; historical renames and
cross-base merges are explicit. Re-run: python db/reference/build_venue_aliases.py
<venue_counts.tsv> <out.csv>  (then review the diff before committing).
"""
import csv
import re
import sys
import unicodedata


def base_key(name: str) -> str:
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    s = s.lower().replace("'", "")
    s = re.sub(r"\s+", " ", s).strip().split(",")[0]
    s = re.sub(r"[^a-z0-9 ]", "", s).strip()
    return re.sub(r"\s+", " ", s)


# base -> primary base (cross-base merges, all evidence-noted)
MERGE_BASES = {
    "rpremadasa stadium": "r premadasa stadium",
    "mchinnaswamy stadium": "m chinnaswamy stadium",
    "feroz shah kotla": "arun jaitley stadium",
    "goodyear park": "mangaung oval",
    "chittagong divisional stadium": "ma aziz stadium",
    "the wanderers stadium": "new wanderers stadium",
    "wanderers": "wanderers cricket ground",
    "sardar patel gujarat stadium": "narendra modi stadium",
    "sardar patel stadium": "narendra modi stadium",
    "gahanga international cricket stadium rwanda": "gahanga international cricket stadium",
}

# base -> family config. curated=True when the merge needs judgment
# (multi-city members, city renames/spelling fixes, metro consolidation).
# rename=True only for documented historical ground renames.
# medium=True where the evidence is thinner (recorded in source note).
FAMILIES = {
    "arnos vale ground": {"name": "Arnos Vale Ground", "city": "Kingstown",
                          "curated": True, "source": "Kingstown is the capital of St Vincent"},
    "bready cricket club": {"name": "Bready Cricket Club, Magheramason", "city": "Bready",
                            "curated": True, "medium": True,
                            "source": "Bready CC ground at Magheramason; Londonderry is a metro tag"},
    "daren sammy national cricket stadium": {"name": "Daren Sammy National Cricket Stadium",
                                             "city": "Gros Islet", "curated": True,
                                             "source": "Gros Islet, St Lucia"},
    "dr dy patil sports academy": {"name": "Dr DY Patil Sports Academy", "city": "Navi Mumbai",
                                   "curated": True, "source": "ground is at Nerul, Navi Mumbai"},
    "kensington oval": {"name": "Kensington Oval", "city": "Bridgetown", "curated": True,
                        "source": "Bridgetown, Barbados (city/country tags swapped in raw rows)"},
    "m chinnaswamy stadium": {"name": "M Chinnaswamy Stadium", "city": "Bengaluru",
                              "curated": True,
                              "source": "city renamed Bangalore->Bengaluru (2014); M. dot spelling merged"},
    "ma aziz stadium": {"name": "MA Aziz Stadium", "city": "Chattogram",
                        "curated": True, "medium": True, "rename": True,
                        "rename_bases": ["chittagong divisional stadium"],
                        "source": "MA Aziz Stadium was formerly Chittagong Divisional Stadium; city renamed Chittagong->Chattogram"},
    "dubai sports city cricket stadium": {"name": "Dubai Sports City Cricket Stadium",
                                          "city": "Dubai", "curated": True,
                                          "source": "city unambiguous from venue name"},
    "galle international stadium": {"name": "Galle International Stadium",
                                    "city": "Galle", "curated": True,
                                    "source": "city unambiguous from venue name"},
    "mombasa sports club ground": {"name": "Mombasa Sports Club Ground",
                                   "city": "Mombasa", "curated": True,
                                   "source": "city unambiguous from venue name"},
    "sheikhupura stadium": {"name": "Sheikhupura Stadium", "city": "Sheikhupura",
                            "curated": True,
                            "source": "city unambiguous from venue name"},
    "sylhet stadium": {"name": "Sylhet Stadium", "city": "Sylhet", "curated": True,
                       "source": "city unambiguous from venue name"},
    "queenstown events centre": {"name": "Queenstown Events Centre",
                                 "city": "Queenstown", "curated": True,
                                 "source": "city unambiguous from venue name"},
    "gahanga international cricket stadium": {"name": "Gahanga International Cricket Stadium",
                                                "city": "Kigali City", "curated": True,
                                                "source": "comma/period spelling variants of the Kigali ground"},
    "jimmy powell oval": {"name": "Jimmy Powell Oval, Cayman Islands",
                          "city": "George Town", "curated": True,
                          "source": "Jimmy Powell Oval is at George Town, Grand Cayman"},
    "guernsey rovers athletic club ground": {"name": "Guernsey Rovers Athletic Club Ground, Port Soif",
                                             "city": "Port Soif", "curated": True,
                                             "source": "Port Soif, Guernsey (fixes double-space raw tag)"},
    "city oval": {"name": "City Oval, Pietermaritzburg", "city": "Pietermaritzburg",
                  "curated": True, "source": "City Oval is at Pietermaritzburg"},
    "st georges quilmes": {"name": "St Georges Quilmes", "city": "Quilmes",
                           "curated": True,
                           "source": "St George's College ground at Quilmes, Argentina"},
    "royal brussels cricket club ground": {"name": "Royal Brussels Cricket Club Ground, Waterloo",
                                           "city": "Waterloo", "curated": True,
                                           "source": "Royal Brussels CC is at Waterloo, Belgium"},
    "maharaja yadavindra singh international cricket stadium": {
        "name": "Maharaja Yadavindra Singh International Cricket Stadium, Mullanpur",
        "city": "New Chandigarh", "curated": True,
        "source": "Mullanpur ground; Mohali/New Chandigarh metro tags"},
    "maple leaf northwest ground": {"name": "Maple Leaf North-West Ground", "city": "King City",
                                    "curated": True, "medium": True,
                                    "source": "ground is at King City (Greater Toronto tag)"},
    "mission road ground": {"name": "Mission Road Ground, Mong Kok", "city": "Mong Kok",
                            "curated": True, "source": "Mong Kok, Hong Kong"},
    "national cricket stadium": {"name": "National Cricket Stadium", "city": "St George's",
                                 "curated": True, "source": "St George's, Grenada"},
    "providence stadium": {"name": "Providence Stadium", "city": "Providence",
                           "curated": True, "source": "Providence, Guyana"},
    "queens park oval": {"name": "Queen's Park Oval", "city": "Port of Spain",
                         "curated": True, "source": "Port of Spain, Trinidad"},
    "r premadasa stadium": {"name": "R Premadasa Stadium", "city": "Colombo",
                            "curated": True,
                            "source": "R. dot spelling merged; Khettarama is a Colombo suburb"},
    "sabina park": {"name": "Sabina Park", "city": "Kingston", "curated": True,
                    "source": "Kingston, Jamaica"},
    "shere bangla national stadium": {"name": "Shere Bangla National Stadium", "city": "Mirpur",
                                      "curated": True, "source": "Mirpur suburb of Dhaka"},
    "sir vivian richards stadium": {"name": "Sir Vivian Richards Stadium", "city": "North Sound",
                                    "curated": True, "source": "North Sound, Antigua"},
    "st georges park": {"name": "St George's Park", "city": "Gqeberha", "curated": True,
                        "source": "city renamed Port Elizabeth->Gqeberha (2021)"},
    "warner park": {"name": "Warner Park", "city": "Basseterre", "curated": True,
                    "source": "Basseterre, St Kitts"},
    "windsor park": {"name": "Windsor Park", "city": "Roseau", "curated": True,
                     "source": "Roseau, Dominica"},
    "zahur ahmed chowdhury stadium": {"name": "Zahur Ahmed Chowdhury Stadium", "city": "Chattogram",
                                      "curated": True,
                                      "source": "city renamed Chittagong->Chattogram"},
    "himachal pradesh cricket association stadium": {
        "name": "Himachal Pradesh Cricket Association Stadium", "city": "Dharamsala",
        "curated": True, "source": "Dharmasala is a spelling variant of Dharamsala"},
    "de beers diamond oval": {"name": "De Beers Diamond Oval", "city": "Kimberley",
                              "curated": True, "medium": True,
                              "source": "Diamond Oval is the abbreviated name of the Kimberley ground"},
    "mangaung oval": {"name": "Mangaung Oval", "city": "Bloemfontein",
                      "curated": True, "rename": True,
                      "rename_bases": ["goodyear park"],
                      "source": "Bloemfontein ground renamed Goodyear Park->Mangaung Oval"},
    "arun jaitley stadium": {"name": "Arun Jaitley Stadium", "city": "Delhi",
                             "curated": True, "rename": True,
                             "rename_bases": ["feroz shah kotla"],
                             "source": "Delhi ground renamed Feroz Shah Kotla->Arun Jaitley Stadium (2019)"},
    "narendra modi stadium": {"name": "Narendra Modi Stadium", "city": "Ahmedabad",
                              "curated": True, "rename": True,
                              "rename_bases": ["sardar patel gujarat stadium",
                                               "sardar patel stadium"],
                              "source": "Motera ground renamed Sardar Patel Stadium->Narendra Modi Stadium (2021)"},
    "new wanderers stadium": {"name": "New Wanderers Stadium", "city": "Johannesburg",
                              "curated": True, "medium": True,
                              "source": "The Wanderers is the concurrent Cricsheet spelling of the Johannesburg ground"},
    "wanderers cricket ground": {"name": "Wanderers Cricket Ground", "city": "Windhoek",
                                 "curated": True, "source": "Windhoek bare-name variant merged"},
}

# base -> split into one canonical per raw city (genuinely different grounds)
SPLIT_FAMILIES = {"county ground", "national stadium", "nehru stadium",
                  "gymkhana club ground"}

# City renames/spelling fixes safe to apply globally (same place, new name).
GLOBAL_CITY_FIXUPS = {"Bangalore": "Bengaluru", "Chittagong": "Chattogram",
                      "Port Elizabeth": "Gqeberha", "Poona": "Pune",
                      "Dharmasala": "Dharamsala"}

CITY_COUNTRY = {
    "Mirpur": "Bangladesh", "Dhaka": "Bangladesh", "Fatullah": "Bangladesh",
    "Bogra": "Bangladesh", "Khulna": "Bangladesh", "Sylhet": "Bangladesh",
    "Chattogram": "Bangladesh", "Chittagong": "Bangladesh",
    "Bengaluru": "India", "Bangalore": "India", "Mumbai": "India",
    "Navi Mumbai": "India", "Kolkata": "India", "Delhi": "India",
    "Chennai": "India", "Hyderabad": "India", "Pune": "India",
    "Jaipur": "India", "Kochi": "India", "Guwahati": "India",
    "Margao": "India", "Ranchi": "India", "Raipur": "India",
    "Rajkot": "India", "Indore": "India", "Kanpur": "India",
    "Nagpur": "India", "Gwalior": "India", "Jamshedpur": "India",
    "Lucknow": "India", "Faridabad": "India", "Chandigarh": "India",
    "Mohali": "India", "New Chandigarh": "India", "Dharamsala": "India",
    "Dharmasala": "India", "Visakhapatnam": "India", "Thiruvananthapuram": "India",
    "Cuttack": "India", "Ahmedabad": "India", "Vadodara": "India",
    "Sydney": "Australia", "Melbourne": "Australia", "Adelaide": "Australia",
    "Brisbane": "Australia", "Perth": "Australia", "Hobart": "Australia",
    "Canberra": "Australia", "Darwin": "Australia", "Geelong": "Australia",
    "Cairns": "Australia", "Mackay": "Australia", "Townsville": "Australia",
    "Carrara": "Australia", "King City": "Canada", "Toronto": "Canada",
    "London": "England", "Birmingham": "England", "Leeds": "England",
    "Manchester": "England", "Nottingham": "England", "Southampton": "England",
    "Bristol": "England", "Taunton": "England", "Chelmsford": "England",
    "Chester-le-Street": "England", "Canterbury": "England",
    "Colombo": "Sri Lanka", "Kandy": "Sri Lanka", "Dambulla": "Sri Lanka",
    "Hambantota": "Sri Lanka", "Auckland": "New Zealand",
    "Wellington": "New Zealand", "Christchurch": "New Zealand",
    "Hamilton": "New Zealand", "Napier": "New Zealand", "Nelson": "New Zealand",
    "Dunedin": "New Zealand", "Queenstown": "New Zealand",
    "Mount Maunganui": "New Zealand", "Whangarei": "New Zealand",
    "Lincoln": "New Zealand", "Cape Town": "South Africa",
    "Johannesburg": "South Africa", "Durban": "South Africa",
    "Centurion": "South Africa", "Gqeberha": "South Africa",
    "Port Elizabeth": "South Africa", "Kimberley": "South Africa",
    "Bloemfontein": "South Africa", "Paarl": "South Africa",
    "Benoni": "South Africa", "Potchefstroom": "South Africa", "East London": "South Africa",
    "Karachi": "Pakistan", "Lahore": "Pakistan", "Faisalabad": "Pakistan",
    "Multan": "Pakistan", "Rawalpindi": "Pakistan", "Peshawar": "Pakistan",
    "Sind": "Pakistan", "Harare": "Zimbabwe", "Bulawayo": "Zimbabwe",
    "Kingston": "Jamaica", "Jamaica": "Jamaica", "Bridgetown": "Barbados",
    "Barbados": "Barbados", "Port of Spain": "Trinidad and Tobago",
    "Trinidad": "Trinidad and Tobago", "Tarouba": "Trinidad and Tobago",
    "Gros Islet": "Saint Lucia", "St Lucia": "Saint Lucia",
    "Kingstown": "Saint Vincent and the Grenadines",
    "St Vincent": "Saint Vincent and the Grenadines",
    "North Sound": "Antigua and Barbuda", "Antigua": "Antigua and Barbuda",
    "Coolidge": "Antigua and Barbuda", "Basseterre": "Saint Kitts and Nevis",
    "St Kitts": "Saint Kitts and Nevis", "Roseau": "Dominica",
    "Dominica": "Dominica", "St George's": "Grenada", "Grenada": "Grenada",
    "Providence": "Guyana", "Guyana": "Guyana",
    "Mong Kok": "Hong Kong", "Hong Kong": "Hong Kong",
    "Singapore": "Singapore", "Kuala Lumpur": "Malaysia", "Bangi": "Malaysia",
    "Bangkok": "Thailand", "Kirtipur": "Nepal", "Kathmandu": "Nepal",
    "Gelephu": "Bhutan", "Port Moresby": "Papua New Guinea",
    "Apia": "Samoa", "Port Vila": "Vanuatu", "Seychelles": "Seychelles",
    "Victoria": "Seychelles", "Port Soif": "Seychelles",
    "Dubai": "United Arab Emirates", "Sharjah": "United Arab Emirates",
    "Abu Dhabi": "United Arab Emirates", "Doha": "Qatar", "Al Amarat": "Oman",
    "Dublin": "Ireland", "Belfast": "Northern Ireland", "Derry": "Northern Ireland",
    "Londonderry": "Northern Ireland", "Bready": "Northern Ireland",
    "Edinburgh": "Scotland", "Glasgow": "Scotland", "Aberdeen": "Scotland",
    "Ayr": "Scotland", "Dundee": "Scotland", "Cardiff": "Wales",
    "St Peter Port": "Guernsey", "St Saviour": "Guernsey", "Castel": "Guernsey",
    "Gibraltar": "Gibraltar", "Episkopi": "Cyprus",
    "Amstelveen": "Netherlands", "Rotterdam": "Netherlands",
    "Deventer": "Netherlands", "Utrecht": "Netherlands", "The Hague": "Netherlands",
    "Copenhagen": "Denmark", "Brondby": "Denmark", "Ishoj": "Denmark",
    "Koge": "Denmark", "Vantaa": "Finland", "Kerava": "Finland",
    "Stockholm": "Sweden", "Oslo": "Norway", "Prague": "Czechia",
    "Tallinn": "Estonia", "Sofia": "Bulgaria", "Szodliget": "Hungary",
    "Zagreb": "Croatia", "Belgrade": "Serbia", "Zemst": "Belgium",
    "Ghent": "Belgium", "Rome": "Italy", "Spinaceto": "Italy",
    "Graz": "Austria", "Latschach": "Austria", "Krefeld": "Germany",
    "Almeria": "Spain", "Murcia": "Spain", "Dreux": "France",
    "Albergaria": "Portugal", "Walferdange": "Luxembourg",
    "Marsa": "Malta", "Nairobi": "Kenya", "Dar-es-Salaam": "Tanzania",
    "Kampala": "Uganda", "Jinja": "Uganda", "Entebbe": "Uganda",
    "Kigali City": "Rwanda", "Kigali": "Rwanda",
    "Gaborone": "Botswana", "Windhoek": "Namibia",
    "Blantyre": "Malawi", "Malkerns": "Eswatini", "Lagos": "Nigeria",
    "Abuja": "Nigeria", "Accra": "Ghana", "Ilfov County": "Romania",
    "Lauderhill": "United States", "Dallas": "United States",
    "Houston": "United States", "Pearland": "United States",
    "New York": "United States", "Bogota": "Colombia",
    "Buenos Aires": "Argentina", "Seropedica": "Brazil",
    "Naucalpan": "Mexico", "Panama City": "Panama", "Guacima": "Costa Rica",
    "Hangzhou": "China", "Incheon": "South Korea", "Sano": "Japan",
    "Nisshin": "Japan", "Bali": "Indonesia", "George Town": "Cayman Islands",
    "Port Soif": "Seychelles", "Pietermaritzburg": "South Africa",
    "Quilmes": "Argentina", "Waterloo": "Belgium", "Mombasa": "Kenya",
    "Galle": "Sri Lanka", "Sheikhupura": "Pakistan", "Queenstown": "New Zealand",
}

HEADER = ["raw_venue_name", "raw_city", "canonical_venue_name", "canonical_city",
          "canonical_country", "mapping_type", "confidence", "source"]


def build(rows):
    """rows: [(id, name, city_or_None, matches)]. Returns list of dicts."""
    by_base = {}
    for vid, name, city, n in rows:
        b = base_key(name)
        b = MERGE_BASES.get(b, b)
        by_base.setdefault(b, []).append((vid, name, city, n))

    out = []
    for base in sorted(by_base):
        members = by_base[base]
        fam = FAMILIES.get(base, {})
        if base in SPLIT_FAMILIES:
            groups = {}
            for m in members:
                groups.setdefault(m[2], []).append(m)
            for city in sorted(groups, key=lambda c: (c is None, c or "")):
                out.extend(_emit_split(base, city, groups[city]))
            continue
        cname = fam.get("name") or _top(members, lambda m: m[1])
        ccity = fam.get("city")
        if ccity is None:
            ccity = GLOBAL_CITY_FIXUPS.get(
                _top_city(members) or "", _top_city(members))
        country = CITY_COUNTRY.get(ccity or "", "")
        rename_bases = fam.get("rename_bases", [])
        curated = fam.get("curated", False)
        medium = fam.get("medium", False)
        src = fam.get("source", "same-ground naming variants in Cricsheet data")
        for vid, name, city, n in sorted(members):
            mb = base_key(name)
            if name == cname and (city or "") == (ccity or ""):
                mtype = "EXACT"
            elif mb in rename_bases:
                mtype = "HISTORICAL_RENAME"
            elif curated:
                mtype = "CURATED_ALIAS"
            else:
                mtype = "NORMALIZED_ALIAS"
            out.append({
                "raw_venue_name": name, "raw_city": city or "",
                "canonical_venue_name": cname, "canonical_city": ccity or "",
                "canonical_country": country,
                "mapping_type": mtype,
                "confidence": "medium" if medium else "high",
                "source": "identity mapping" if mtype == "EXACT" else src,
            })
    return out


def _top(members, key):
    best = sorted(members, key=lambda m: (-m[3], key(m)))
    return key(best[0])


def _top_city(members):
    agg = {}
    for m in members:
        c = m[2]
        agg[c] = agg.get(c, 0) + m[3]
    ranked = sorted(agg.items(), key=lambda kv: (-kv[1], str(kv[0])))
    non_null = [c for c, _ in ranked if c]
    return non_null[0] if non_null else None


def _emit_split(base, city, members):
    cname = _top(members, lambda m: m[1])
    country = CITY_COUNTRY.get(city or "", "")
    rows = []
    for vid, name, c, n in sorted(members):
        identity = name == cname and c == city
        rows.append({
            "raw_venue_name": name, "raw_city": c or "",
            "canonical_venue_name": cname, "canonical_city": city or "",
            "canonical_country": country,
            "mapping_type": "EXACT" if identity else "NORMALIZED_ALIAS",
            "confidence": "high",
            "source": ("identity mapping" if identity
                       else "same-city spelling variant; grounds differ by city"),
        })
    return rows


def main():
    src, dst = sys.argv[1], sys.argv[2]
    rows = []
    for line in open(src, encoding="utf-8"):
        parts = line.rstrip("\n").split("\t")
        rows.append((int(parts[0]), parts[1], parts[2] or None, int(parts[3])))
    out = build(rows)
    with open(dst, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        w.writeheader()
        w.writerows(out)
    print(f"rows={len(out)} canonical={len({(r['canonical_venue_name'], r['canonical_city']) for r in out})}")


if __name__ == "__main__":
    main()
