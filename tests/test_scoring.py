from pathlib import Path

from jobradar.config import load_scoring_config
from jobradar.scoring.engine import (
    score_company_type,
    score_job,
    score_language,
    score_location,
    score_risks,
    score_role,
    score_skills,
)


def _config():
    return load_scoring_config(Path("data/config"))


def test_location_scoring() -> None:
    config = _config()

    score = score_location("上海 Hybrid", config.locations)

    assert score.value == 25
    assert score.key == "shanghai"


def test_company_type_scoring() -> None:
    config = _config()

    score = score_company_type("foreign_mnc", config.company_types)

    assert score.value == 20
    assert score.key == "foreign_mnc"


def test_role_scoring_uses_best_match() -> None:
    config = _config()

    score = score_role("AI Solution Architect working on LLM and RAG", config.roles)

    assert score.value == 30
    assert score.key == "ai_llm_agent_rag"


def test_language_scoring() -> None:
    config = _config()

    score = score_language("English preferred", config.languages)

    assert score.value == 12
    assert score.key == "english_preferred"


def test_skill_keyword_scoring() -> None:
    config = _config()

    score = score_skills("Python REST API integration for LLM RAG workflow", config.skills, 20)

    assert score.value == 18
    assert set(score.keys) >= {"ai", "python_api", "integration"}


def test_risk_penalty_scoring() -> None:
    config = _config()

    score = score_risks("outsourcing with cold call quota", config.risks)

    assert score.value == -22
    assert set(score.keys) >= {"outsourcing", "sales_heavy"}


def test_risk_penalty_is_capped() -> None:
    config = _config()

    score = score_risks(
        "outsourcing contractor dispatch cold call quota "
        "customer service Japanese required US only",
        config.risks,
    )

    assert score.value == -40


def test_score_job_adds_components_and_clamps() -> None:
    config = _config()
    job = {
        "location_raw": "上海",
        "company_type": "foreign_tech_saas",
        "language_raw": "English and Chinese",
        "title": "AI Solution Architect",
        "description": "LLM RAG Agent platform",
        "requirements": "Python REST API integration",
    }

    scored = score_job(job, config)

    assert scored.total == 100
    assert scored.recommendation == "strong_match"
    assert "location:" in scored.explanation
