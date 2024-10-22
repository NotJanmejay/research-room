from fastapi import FastAPI, BackgroundTasks
import uvicorn
from pydantic import BaseModel, Field
from main import main
import json
import os
import asyncio
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATUS_FILE = "report_status.json"
REPORTS_MD_DIR = "reports_md"
REPORTS_PDF_DIR = "reports_pdf"
REPORTS_DOCX_DIR = "reports_docx"

# Load or initialize the status file
if not os.path.exists(STATUS_FILE):
    with open(STATUS_FILE, "w") as f:
        json.dump({}, f)


def load_status():
    with open(STATUS_FILE, "r") as f:
        return json.load(f)


def save_status(status):
    with open(STATUS_FILE, "w") as f:
        json.dump(status, f)


class GenerateRequest(BaseModel):
    country: str = Field(
        default=None, title="Country for which report must be generated"
    )
    industry: str = Field(
        default=None, title="Industry on which report needs to be generated"
    )


@app.get("/")
def _():
    return "Server running on port 8000, endpoints as /api"


@app.post("/api/generate")
async def generate_report(req: GenerateRequest, background_tasks: BackgroundTasks):
    country = req.country.lower()
    industry = req.industry.lower()
    report_id = f"{industry}_{country}_{datetime.now().year}"

    # Load the current status
    status = load_status()

    # If a report is already in progress for the same request, return that status
    if report_id in status and status[report_id] == "in_progress":
        return {
            "status": "in_progress",
            "message": "Report generation already in progress.",
        }

    # Mark the report as in_progress
    status[report_id] = "in_progress"
    save_status(status)

    # Generate the report in the background
    background_tasks.add_task(generate_report_task, industry, country, report_id)

    return {
        "status": "in_progress",
        "message": "Report generation started.",
        "report_id": report_id,
    }


async def generate_report_task(industry, country, report_id):
    await asyncio.to_thread(main, domain=industry, country=country)

    status = load_status()
    status[report_id] = "completed"
    save_status(status)


@app.get("/api/status/{report_id}")
async def get_report_status(report_id: str):
    status = load_status()

    if report_id not in status:
        return {"status": "not_found", "message": "Report not found."}

    return {"status": status[report_id]}


@app.get("/api/report/markdown/{report_id}")
async def get_markdown_report(report_id: str):
    status = load_status()

    if report_id not in status:
        return {"status": "not_found", "message": "Report not found."}

    if status[report_id] == "completed":
        report_path = os.path.join(REPORTS_MD_DIR, f"{report_id}.md")
        if os.path.exists(report_path):
            return FileResponse(
                report_path,
                media_type="text/markdown",
                filename=os.path.basename(report_path),
            )
        else:
            return {
                "status": "error",
                "message": "Markdown report file does not exist.",
            }

    return {"status": "error", "message": "Report is not yet completed."}


@app.get("/api/report/pdf/{report_id}")
async def get_pdf_report(report_id: str):
    status = load_status()

    if report_id not in status:
        return {"status": "not_found", "message": "Report not found."}

    if status[report_id] == "completed":
        report_path = os.path.join(
            REPORTS_PDF_DIR, f"{report_id}.pdf"
        )  # Assuming you save PDF with this naming
        if os.path.exists(report_path):
            return FileResponse(
                report_path,
                media_type="application/pdf",
                filename=os.path.basename(report_path),
            )
        else:
            return {"status": "error", "message": "PDF report file does not exist."}

    return {"status": "error", "message": "Report is not yet completed."}


@app.get("/api/report/docx/{report_id}")
async def get_docx_report(report_id: str):
    status = load_status()

    if report_id not in status:
        return {"status": "not_found", "message": "Report not found."}

    if status[report_id] == "completed":
        report_path = os.path.join(
            REPORTS_DOCX_DIR, f"{report_id}.docx"
        )  # Assuming you save PDF with this naming
        if os.path.exists(report_path):
            return FileResponse(
                report_path,
                media_type="application/docx",
                filename=os.path.basename(report_path),
            )
        else:
            return {"status": "error", "message": "PDF report file does not exist."}

    return {"status": "error", "message": "Report is not yet completed."}


if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, log_level="info")
