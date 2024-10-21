import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import GoogleSerperAPIWrapper
import re
from docx import Document
from datetime import datetime
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx2pdf import convert


# Load environment variables
def load_env():
    os.environ["REQUESTS_CA_BUNDLE"] = "./certificate.cer"
    load_dotenv()


# Set up logging
def setup_logging(log_filename="logs/report_generation.log"):
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


# Initialize ChatOpenAI model
def initialize_model(model_id="gpt-4o-mini"):
    try:
        model = ChatOpenAI(model=model_id)
        logging.info("Initialized ChatOpenAI model.")
        return model
    except Exception as e:
        logging.error("Failed to initialize ChatOpenAI model: %s", e)
        print("Please add OPENAI_API_KEY to .env and try again")
        return None


# Initialize GoogleSerperAPIWrapper
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


# Fetch company details
def fetch_company_details(domain, country, search, model):
    logging.info("Searching for top companies in the %s sector in %s.", domain, country)
    search_for_companies = search.results(
        f"Top Company in {domain} sector in {country}"
    )

    companies = model.invoke(
        f"Using the scrapped json value from google, give me the name of the top 5 companies working in the domain in comma separated value strictly only. Give me only the name of the companies and nothing else strictly, Scrapped Value: {search_for_companies}"
    )

    return companies.content.split(", ")


# Fetch company financials
def fetch_company_financials(companies, search):
    companies_query = []

    for company in companies:
        logging.info("Fetching financial information for %s.", company)
        query_result = search.results(
            f"{company} market cap, revenue, debts, assets, financials"
        )
        companies_query.append({"company": company, "result": query_result})

    return companies_query


# Fetch market insights
def fetch_market_insights(domain, country, search):
    prompts = {
        "market_size": f"Provide information about the current market size, historical trends, and future growth prospects of {domain} domain in {country}",
        "market_trends": f"Provide me detail key market trends in the field of {domain} in the country of {country}",
        "technological_advancement": f"Provide information about the latest technological advancements in the field of {domain} in {country}",
        "consumer_preferences": f"Provide information about the consumer preferences in the field of {domain} in the country of {country}",
        "regulatory_changes": f"Provide information about recent regulatory changes that took place in the field of {domain} in {country}",
        "barrier_to_entries": f"Provide information about high potential challenges or barriers to entries in the field of {domain} in {country}",
    }

    insights = {
        "market_size": search.results(prompts["market_size"]),
        "market_trends": search.results(prompts["market_trends"]),
        "technological_advancement": search.results(
            prompts["technological_advancement"]
        ),
        "consumer_preferences": search.results(prompts["consumer_preferences"]),
        "regulatory_changes": search.results(prompts["regulatory_changes"]),
        "barrier_to_entry": search.results(prompts["barrier_to_entries"]),
    }

    return insights


# Fetch latest news
def fetch_latest_news(domain, country, search_news):
    latest_news = search_news.results(f"{domain} sector in {country}")
    return latest_news


# Generate report
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


# Save report to file
def save_report(content, domain, country):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"reports/output_{domain}_{country}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

    if not os.path.exists("reports"):
        os.makedirs("reports")

    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

    logging.info("Report generated successfully: %s", filename)
    return filename



def convert_markdown_to_docx(markdown_content, file_name):
    """Convert markdown content to a DOCX file with proper formatting."""
    # Create a 'report' folder if it doesn't exist
    report_folder = 'report'
    os.makedirs(report_folder, exist_ok=True)

    # Remove 'reports/' from file_name and .md from file_name
    base_file_name = file_name.replace('reports/', '').replace('.md', '')  
    base_output_docx = os.path.join(report_folder, base_file_name)

    # Append timestamp to filename if it already exists
    output_docx = f"{base_output_docx}.docx"
    if os.path.exists(output_docx):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_docx = f"{base_output_docx}_{timestamp}.docx"

    doc = Document()

    # Split the markdown content into lines
    lines = markdown_content.splitlines()

    for line in lines:
        line = line.strip()

        # Handle headers and remove asterisks from them
        if line.startswith('# '):
            doc.add_heading(line[2:].replace('*', '').strip(), level=1)
        elif line.startswith('## '):
            doc.add_heading(line[3:].replace('*', '').strip(), level=2)
        elif line.startswith('### '):
            doc.add_heading(line[4:].replace('*', '').strip(), level=3)
        elif line.startswith('- '):
            bullet_text = line[2:]

            # Make text bold if it contains asterisks
            if '*' in bullet_text:
                paragraph = doc.add_paragraph(style='List Bullet')
                parts = bullet_text.split('**')
                for i, part in enumerate(parts):
                    run = paragraph.add_run(part.strip())
                    run.bold = (i % 2 == 1)
            else:
                # Check if the bullet point contains a hyperlink
                hyperlink_match = re.match(r'\[(.*?)\]\((https?://[^\s]+)\)', bullet_text)
                if hyperlink_match:
                    paragraph = doc.add_paragraph(style='List Bullet')
                    link_text, url = hyperlink_match.groups()
                    add_hyperlink(paragraph, f"{link_text} ({url})", url)
                else:
                    doc.add_paragraph(bullet_text, style='List Bullet')
        elif '**' in line:  # Handle bold text
            paragraph = doc.add_paragraph()
            parts = line.split('**')
            for i, part in enumerate(parts):
                run = paragraph.add_run(part.strip())
                run.bold = (i % 2 == 1)
        elif line:  # Regular paragraph
            # Convert URLs to hyperlinks
            paragraph = doc.add_paragraph()
            url_match = re.search(r'(https?://[^\s]+)', line)
            if url_match:
                url = url_match.group(0)
                add_hyperlink(paragraph, url, url)
            else:
                paragraph.add_run(line)

    # Save the document
    doc.save(output_docx)
    return output_docx

def add_hyperlink(paragraph, text, url):
    """Add a hyperlink to a paragraph with blue color and underlined text."""
    part = paragraph.part
    r_id = part.relate_to(
        url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True
    )

    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)

    run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')

    # Set hyperlink style: blue color and underlined
    color = OxmlElement('w:color')
    color.set(qn('w:val'), '0000FF')  # Blue color

    underline = OxmlElement('w:u')
    underline.set(qn('w:val'), 'single')  # Underlined text

    rPr.extend([color, underline])
    run.append(rPr)

    text_element = OxmlElement('w:t')
    text_element.text = text
    run.append(text_element)
    hyperlink.append(run)
    paragraph._element.append(hyperlink)



# WordFile to PDF

def convert_word_to_pdf(word_file_path):
    """Convert a Word document to PDF and store it in a 'report_pdfs' folder."""
    # Create the 'report_pdfs' folder if it doesn't exist
    pdf_folder = 'report_pdfs'
    os.makedirs(pdf_folder, exist_ok=True)

    # Define the PDF file path
    pdf_path = os.path.join(pdf_folder, os.path.basename(word_file_path).replace('.docx', '.pdf'))

    # Convert the Word document to PDF
    convert(word_file_path, pdf_path)

    return pdf_path

