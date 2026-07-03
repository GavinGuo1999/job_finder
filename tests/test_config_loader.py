from pathlib import Path

from jobradar.config import load_scoring_config


def test_load_scoring_config() -> None:
    config = load_scoring_config(Path("data/config"))

    assert config.locations
    assert config.company_types["foreign_tech_saas"].score == 19
    assert any(rule.key == "ai_llm_agent_rag" for rule in config.roles)
    assert config.skill_max_total == 20
    assert any(rule.key == "outsourcing" for rule in config.risks)
