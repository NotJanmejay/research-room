import asyncio
from utils import (
    load_env,
    setup_logging,
    initialize_model,
    initialize_search,
    fetch_company_details,
    fetch_company_financials,
    fetch_market_insights,
    fetch_latest_news,
    generate_report,
    save_report,
    convert_markdown_to_docx,
    add_hyperlink,
    convert_word_to_pdf
)
from ResearchRoomPrompt import template


def main(domain, country):
    # Load environment and set up logging
    load_env()
    setup_logging()

    # Initialize search and model
    search = initialize_search()
    search_news = initialize_search(api_type="news")
    model = initialize_model()

    if not search or not model or not search_news:
        return  # Exit if initialization fails

    # Fetch company details and financials concurrently
    companies = fetch_company_details(domain, country, search, model)
    company_info = fetch_company_financials(companies, search)

    # Fetch market insights and news concurrently
    insights_task = fetch_market_insights(domain, country, search)
    news_task = fetch_latest_news(domain, country, search_news)
    insights, latest_news = (insights_task, news_task)

    # Generate report content
    report_content = generate_report(
        domain, country, model, template, company_info, insights, latest_news
    )

    # Save the report to a file
    file_name = save_report(report_content, domain, country)
    return file_name
    filename = save_report(report_content, domain, country)

    # Save the report in word file 
    word_file = convert_markdown_to_docx(report_content,file_name = filename)

    # Save the report in PDF File
    convert_word_to_pdf(word_file)

if __name__ == "__main__":
    main("Fashion", "India")
