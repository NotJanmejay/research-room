import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import GoogleSerperAPIWrapper


def load_env():
    os.environ["REQUESTS_CA_BUNDLE"] = "./certificate.cer"
    load_dotenv()


def setup_logging(log_filename="logs/report_generation.log"):
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def initialize_model(model_id="gpt-4o-mini"):
    try:
        model = ChatOpenAI(model=model_id)
        logging.info("Initialized ChatOpenAI model.")
        return model
    except Exception as e:
        logging.error("Failed to initialize ChatOpenAI model: %s", e)
        print("Please add OPENAI_API_KEY to .env and try again")
        return None


def initialize_search(api_type="search"):
    try:
        if api_type == "news":
            search = GoogleSerperAPIWrapper(type="news")
        else:
            search = GoogleSerperAPIWrapper()
        logging.info(f"Initialized GoogleSerperAPIWrapper for {api_type}.")
        return search
    except Exception as e:
        logging.error("Failed to initialize GoogleSerperAPIWrapper: %s", e)
        print("Please add SERPER_API_KEY to .env and try again")
        return None


def fetch_company_details(domain, country, search, model):
    logging.info("Searching for top companies in the %s sector in %s.", domain, country)
    search_for_companies = search.results(
        f"Top Company in {domain} sector in {country}"
    )

    companies = model.invoke(
        f"Using the scrapped json value from google, give me the name of the top 5 companies working in the domain in comma separated value strictly only. Give me only the name of the companies and nothing else strictly, Scrapped Value: {search_for_companies}"
    )

    return companies.content.split(", ")


def fetch_company_financials(companies, search):
    companies_query = []

    for company in companies:
        logging.info("Fetching financial information for %s.", company)
        query_result = search.results(
            f"{company} market cap, revenue, debts, assets, financials"
        )
        companies_query.append({"company": company, "result": query_result})

    return companies_query


def fetch_market_insights(domain, country, search):
    prompts = {
        "market_size": f"Provide information about the current market size, historical trends, and future growth prospects of {domain} domain in {country}",
        "market_trends": f"Provide me detail key market trends in the field of {domain} in the country of {country}",
        "technological_advancement": f"Provide information about the latest technological advancements in the field of {domain} in {country}",
        "consumer_preferences": f"Provide information about the consumer preferences in the field of {domain} in the country of {country}",
        "regulatory_changes": f"Provide information about recent regulatory changes that took place in the field of {domain} in {country}",
        "barrier_to_entries": f"Provide information about high potential challenges or barriers to entries in the field of {domain} in {country}",
    }
    results = [
        search.results(prompts["market_size"]),
        search.results(prompts["market_trends"]),
        search.results(prompts["technological_advancement"]),
        search.results(prompts["consumer_preferences"]),
        search.results(prompts["regulatory_changes"]),
        search.results(prompts["barrier_to_entries"]),
    ]

    insights = {
        "market_size": results[0],
        "market_trends": results[1],
        "technological_advancement": results[2],
        "consumer_preferences": results[3],
        "regulatory_changes": results[4],
        "barrier_to_entry": results[5],
    }

    return insights


def fetch_latest_news(domain, country, search_news):
    latest_news = search_news.results(f"{domain} sector in {country}")
    return latest_news


def generate_report(
    domain, country, model, template, company_info, insights, latest_news
):
    relevant_information = (
        str(insights["market_size"])
        + str(insights["market_trends"])
        + str(insights["technological_advancement"])
        + str(insights["consumer_preferences"])
        + str(insights["regulatory_changes"])
        + str(insights["barrier_to_entry"])
    )

    latest_news_str = str(latest_news)
    prompt = template.format(
        domain=domain,
        country=country,
        current_year="2024",
        relevant_information=relevant_information,
        company_info=str(company_info),
        latest_news=latest_news_str,
    )

    logging.info("Generating report with the model.")
    report = model.invoke(prompt)
    return report.content


def save_report(content, domain, country):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"reports/output_{domain}_{country}.md"

    if not os.path.exists("reports"):
        os.makedirs("reports")

    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

    logging.info("Report generated successfully: %s", filename)
    return filename
