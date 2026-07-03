import csv
from datetime import datetime
from pathlib import Path

from jobradar.config import load_scoring_config
from jobradar.exporter import CSV_HEADER, export_jobs_csv
from jobradar.scoring import score_jobs


def test_csv_exporter_writes_sorted_jobs(tmp_path: Path) -> None:
    config = load_scoring_config(Path("data/config"))
    jobs = [
        {
            "source_id": "fixture",
            "company_id": "vendor",
            "company_name": "Vendor",
            "company_type": "outsourcing_staffing",
            "job_id": "low",
            "title": "Customer Service",
            "location_raw": "US only",
            "language_raw": "Chinese only",
            "description": "outsourcing cold call quota",
            "requirements": "customer service",
        },
        {
            "source_id": "fixture",
            "company_id": "acme",
            "company_name": "Acme",
            "company_type": "foreign_tech_saas",
            "job_id": "high",
            "title": "AI Solution Architect",
            "location_raw": "上海",
            "language_raw": "English and Chinese",
            "description": "LLM RAG Agent",
            "requirements": "Python REST API integration",
        },
    ]

    output = export_jobs_csv(
        score_jobs(jobs, config),
        tmp_path,
        timestamp=datetime(2026, 7, 1, 9, 30, 0),
    )

    with output.open("r", encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    assert rows[0]["job__id"] == "high"
    assert rows[0]["score__total"] == "100"
    assert rows[0]["score__level"] == "high"
    assert rows[0]["score__recommendation"] == "strong_match"
    assert rows[1]["risk__penalty"].startswith("-")


def test_csv_exporter_writes_header_for_empty_input(tmp_path: Path) -> None:
    output = export_jobs_csv([], tmp_path, timestamp=datetime(2026, 7, 1, 9, 30, 0))

    with output.open("r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        rows = list(reader)

    assert rows == [CSV_HEADER]


def test_csv_exporter_escapes_commas_quotes_and_newlines(tmp_path: Path) -> None:
    config = load_scoring_config(Path("data/config"))
    jobs = [
        {
            "source_id": "fixture",
            "company_id": "quoted",
            "company_name": 'Quote "Company"',
            "company_type": "foreign_mnc",
            "job_id": "quoted",
            "title": 'AI, "Platform" Consultant',
            "location_raw": "上海",
            "language_raw": "English and Chinese",
            "description": 'Line one, with comma\nLine two with "quote" and LLM',
            "requirements": "Python API",
        }
    ]

    output = export_jobs_csv(
        score_jobs(jobs, config),
        tmp_path,
        timestamp=datetime(2026, 7, 1, 9, 30, 0),
    )

    with output.open("r", encoding="utf-8", newline="") as file:
        row = next(csv.DictReader(file))

    assert row["job__title"] == 'AI, "Platform" Consultant'
    assert row["text__description"] == 'Line one, with comma\nLine two with "quote" and LLM'
