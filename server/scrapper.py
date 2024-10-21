import requests
from bs4 import BeautifulSoup


def get_top_companies(sector: str):
    country_symbol_map = {
        "uae": "🇦🇪 UAE",
        "saudi": "🇸🇦 S. Arabia",
        "usa": "🇺🇸 USA",
        "india": "🇮🇳 India",
        "germany": "🇩🇪 Germany",
        "malaysia": "🇲🇾 Malaysia",
        "china": "🇨🇳 China",
    }

    base_url = "https://companiesmarketcap.com"
    sector_url = f"{base_url}/{sector.lower()}/largest-{sector.lower()}-companies-by-market-cap"
    stock_page_response = requests.get(sector_url)

    if not stock_page_response.ok:
        print(f'Status code for {sector_url}: {stock_page_response.status_code}')
        return []

    stock_page_doc = BeautifulSoup(stock_page_response.text, "html5lib")
    rows = stock_page_doc.find_all("tr")[1:]

    uae_company_links = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 2:
            continue
        country = cols[7].text.strip()
    
        if country == "🇦🇪 UAE":
            name_div = cols[2].find("div", class_="name-div")
            company_name = name_div.find("div", class_="company-name").text.strip()
            company_link = name_div.find("a")["href"]
            uae_company_links.append({
                "name": company_name,
                "link": f"{base_url}{company_link}".replace("/marketcap", "")
            })

    all_company_data = []
    pages = [
        "marketcap", "revenue", "earnings", "stock-price-history", "pe-ratio",
        "ps-ratio", "pb-ratio", "operating-margin", "total-debt",
        "cash-on-hand", "dividend-yield", "total-assets", "dividends", "eps"
    ]
    
    for company in uae_company_links:
        company_data = {
            "name": company["name"],
            "market_cap": None,
            "market_cap_change": [],
            "revenue": None,
            "revenue_change": [],
            "earnings": None,
            "earnings_change": [],
            "operating_margin": None,
            "operating_margin_change": [],
            "pe_ratio": None,
            "pe_ratio_change": [],
            "ps_ratio": None,
            "ps_ratio_change": [],
            "pb_ratio": None,
            "pb_ratio_change": [],
            "total_debt": None,
            "total_debt_change": [],
            "cash_on_hand": None,
            "cash_on_hand_change": [],
            "total_assets": None,
            "total_assets_change": [],
            "dividends": None,
            "dividends_change": [],
            "eps": None,
            "eps_change": []
        }

        for page in pages:
            req = requests.get(company["link"] + page)
            if req.ok:
                soup = BeautifulSoup(req.text, "html5lib")
                
                # Get the main data
                profile_container = soup.find("div", class_="profile-container")
                if profile_container:
                    span = profile_container.find("span", class_="background-ya")
                    if span:
                        value = span.text.strip()
                        if page == "marketcap":
                            company_data["market_cap"] = value + f" Source:({company["link"]+page})"
                        elif page == "revenue":
                            company_data["revenue"] = value + f" Source:({company["link"]+page})"
                        elif page == "earnings":
                            company_data["earnings"] = value + f" Source:({company["link"]+page})"
                        elif page == "operating-margin":
                            company_data["operating_margin"] = value + f" Source:({company["link"]+page})"
                        elif page == "pe-ratio":
                            company_data["pe_ratio"] = value + f" Source:({company["link"]+page})"
                        elif page == "ps-ratio":
                            company_data["ps_ratio"] = value + f" Source:({company["link"]+page})"
                        elif page == "pb-ratio":
                            company_data["pb_ratio"] = value + f" Source:({company["link"]+page})"
                        elif page == "total-debt":
                            company_data["total_debt"] = value + f" Source:({company["link"]+page})"
                        elif page == "cash-on-hand":
                            company_data["cash_on_hand"] = value + f" Source:({company["link"]+page})"
                        elif page == "total-assets":
                            company_data["total_assets"] = value + f" Source:({company["link"]+page})"
                        elif page == "dividends":
                            company_data["dividends"] = value + f" Source:({company["link"]+page})"
                        elif page == "eps":
                            company_data["eps"] = value + f" Source:({company["link"]+page})"
                
                # Get changes from the table
                table = soup.find("table", class_="table")
                if table:
                    rows = table.find("tbody").find_all("tr")
                    for row in rows:
                        cells = row.find_all("td")
                        if len(cells) >= 3:
                            year = cells[0].text.strip()
                            market_cap_change = cells[1].text.strip() if cells[1].text.strip() else "N/A"
                            change = cells[2].text.strip() if cells[2].text.strip() else "N/A"
                            if page == "marketcap":
                                company_data["market_cap_change"].append({"year": year, "value": market_cap_change, "change": change})
                            elif page == "revenue":
                                company_data["revenue_change"].append({"year": year, "value": market_cap_change, "change": change})
                            elif page == "earnings":
                                company_data["earnings_change"].append({"year": year, "value": market_cap_change, "change": change})
                            elif page == "operating-margin":
                                company_data["operating_margin_change"].append({"year": year, "value": market_cap_change, "change": change})
                            elif page == "pe-ratio":
                                company_data["pe_ratio_change"].append({"year": year, "value": market_cap_change, "change": change})
                            elif page == "ps-ratio":
                                company_data["ps_ratio_change"].append({"year": year, "value": market_cap_change, "change": change})
                            elif page == "pb-ratio":
                                company_data["pb_ratio_change"].append({"year": year, "value": market_cap_change, "change": change})
                            elif page == "total-debt":
                                company_data["total_debt_change"].append({"year": year, "value": market_cap_change, "change": change})
                            elif page == "cash-on-hand":
                                company_data["cash_on_hand_change"].append({"year": year, "value": market_cap_change, "change": change})
                            elif page == "total-assets":
                                company_data["total_assets_change"].append({"year": year, "value": market_cap_change, "change": change})
                            elif page == "dividends":
                                company_data["dividends_change"].append({"year": year, "value": market_cap_change, "change": change})
                            elif page == "eps":
                                company_data["eps_change"].append({"year": year, "value": market_cap_change, "change": change})

        all_company_data.append(company_data)

    return all_company_data

if __name__ == "__main__":
    import json
    print("Scrapping companies in healthcare sector in the country of UAE")
    top_companies = get_top_companies("healthcare")
    with open("company_data.json","w") as file:
        print("Saving to company_data.json")
        json.dump(top_companies, file)
