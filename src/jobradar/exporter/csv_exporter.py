"""CSV fixture input and jobs.csv output."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

from jobradar.scoring import ScoredJob

CSV_HEADER = [
    "run__id",
    "run__timestamp",
    "run__date",
    "source__id",
    "source__type",
    "source__name",
    "source__url",
    "source__status",
    "source__fetched_at",
    "company__id",
    "company__name",
    "company__display_name",
    "company__type",
    "company__industry",
    "company__hq_country",
    "company__is_multinational",
    "company__career_url",
    "job__id",
    "job__source_job_id",
    "job__url",
    "job__title",
    "job__department",
    "job__employment_type",
    "job__seniority",
    "job__published_at",
    "job__updated_at",
    "job__is_active",
    "location__raw",
    "location__country",
    "location__region",
    "location__city",
    "location__district",
    "location__remote_type",
    "location__remote_scope",
    "location__preference_band",
    "language__raw",
    "language__category",
    "language__english_required",
    "language__chinese_required",
    "comp__raw",
    "comp__currency",
    "comp__min",
    "comp__max",
    "comp__period",
    "benefit__raw",
    "benefit__highlights",
    "text__summary",
    "text__description",
    "text__requirements",
    "skill__matched_keywords",
    "skill__ai",
    "skill__erp",
    "skill__bi",
    "skill__python_api",
    "skill__integration",
    "risk__flags",
    "risk__outsourcing",
    "risk__staffing",
    "risk__sales_heavy",
    "risk__language_barrier",
    "risk__low_relevance",
    "score__location",
    "score__company",
    "score__role",
    "score__language",
    "score__skill",
    "score__risk",
    "score__total",
    "score__reasons",
    "debug__adapter",
    "debug__raw_hash",
    "debug__missing_fields",
    "debug__notes",
    "job__apply_url",
    "score__recommendation",
    "debug__parse_confidence",
    "score__level",
    "score__explanation",
    "risk__penalty",
    "risk__reason",
]


def read_fixture_jobs(input_path: str | Path) -> list[dict[str, str]]:
    path = Path(input_path)
    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def export_jobs_csv(
    scored_jobs: list[ScoredJob],
    output_root: str | Path,
    *,
    timestamp: datetime | None = None,
) -> Path:
    run_time = timestamp or datetime.now()
    run_id = run_time.strftime("%Y%m%dT%H%M%S")
    run_dir = Path(output_root) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    output_path = run_dir / "jobs.csv"

    rows = [_to_output_row(job, run_id, run_time) for job in scored_jobs]
    rows.sort(key=lambda row: int(row["score__total"] or 0), reverse=True)

    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=CSV_HEADER,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({field: _empty_if_none(row.get(field)) for field in CSV_HEADER})

    return output_path


def _to_output_row(scored: ScoredJob, run_id: str, run_time: datetime) -> dict[str, str | int]:
    raw = scored.raw
    risk_flags = set(scored.risk.keys)
    skill_flags = set(scored.skill.keys)
    score_reasons = scored.explanation

    return {
        "run__id": run_id,
        "run__timestamp": run_time.isoformat(timespec="seconds"),
        "run__date": run_time.date().isoformat(),
        "source__id": raw.get("source_id", ""),
        "source__type": raw.get("source_type", ""),
        "source__name": raw.get("source_name", ""),
        "source__url": raw.get("source_url", ""),
        "source__status": raw.get("source_status", "ok"),
        "source__fetched_at": run_time.isoformat(timespec="seconds"),
        "company__id": raw.get("company_id", ""),
        "company__name": raw.get("company_name", ""),
        "company__display_name": raw.get("company_display_name", raw.get("company_name", "")),
        "company__type": raw.get("company_type", ""),
        "company__industry": raw.get("company_industry", ""),
        "company__hq_country": raw.get("company_hq_country", ""),
        "company__is_multinational": _bool_text(raw.get("company_type", "").startswith("foreign")),
        "company__career_url": raw.get("company_career_url", ""),
        "job__id": raw.get("job_id", ""),
        "job__source_job_id": raw.get("source_job_id", ""),
        "job__url": raw.get("job_url", ""),
        "job__title": raw.get("title", ""),
        "job__department": raw.get("department", ""),
        "job__employment_type": raw.get("employment_type", ""),
        "job__seniority": raw.get("seniority", ""),
        "job__published_at": raw.get("published_at", ""),
        "job__updated_at": raw.get("updated_at", ""),
        "job__is_active": raw.get("is_active", ""),
        "location__raw": raw.get("location_raw", ""),
        "location__preference_band": scored.location.key,
        "language__raw": raw.get("language_raw", ""),
        "language__category": scored.language.key,
        "comp__raw": raw.get("comp_raw", ""),
        "benefit__raw": raw.get("benefit_raw", ""),
        "benefit__highlights": raw.get("benefit_raw", ""),
        "text__summary": raw.get("title", ""),
        "text__description": raw.get("description", ""),
        "text__requirements": raw.get("requirements", ""),
        "skill__matched_keywords": ";".join(scored.skill.matched_keywords),
        "skill__ai": _bool_text("ai" in skill_flags),
        "skill__erp": _bool_text("erp" in skill_flags),
        "skill__bi": _bool_text("bi" in skill_flags),
        "skill__python_api": _bool_text("python_api" in skill_flags),
        "skill__integration": _bool_text("integration" in skill_flags),
        "risk__flags": ";".join(scored.risk.keys),
        "risk__outsourcing": _bool_text("outsourcing" in risk_flags),
        "risk__staffing": _bool_text("staffing" in risk_flags),
        "risk__sales_heavy": _bool_text("sales_heavy" in risk_flags),
        "risk__language_barrier": _bool_text("language_barrier" in risk_flags),
        "risk__low_relevance": _bool_text("low_relevance" in risk_flags),
        "score__location": scored.location.value,
        "score__company": scored.company.value,
        "score__role": scored.role.value,
        "score__language": scored.language.value,
        "score__skill": scored.skill.value,
        "score__risk": scored.risk.value,
        "score__total": scored.total,
        "score__reasons": score_reasons,
        "debug__adapter": "fixture",
        "debug__notes": "scored from local fixture",
        "job__apply_url": raw.get("apply_url", ""),
        "score__recommendation": scored.recommendation,
        "debug__parse_confidence": "1",
        "score__level": scored.level,
        "score__explanation": score_reasons,
        "risk__penalty": scored.risk.value,
        "risk__reason": "; ".join(scored.risk.reasons),
    }


def _empty_if_none(value: object) -> object:
    return "" if value is None else value


def _bool_text(value: bool) -> str:
    return "true" if value else "false"
