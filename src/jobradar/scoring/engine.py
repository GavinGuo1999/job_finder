"""Config-driven additive scoring."""

from __future__ import annotations

# The engine is intentionally pure: no IO, network, database, or crawler work.
from collections.abc import Mapping
from dataclasses import dataclass

from jobradar.config import KeywordRule, ScoringConfig, WeightRule


@dataclass(frozen=True)
class ComponentScore:
    value: int
    reason: str
    key: str = ""


@dataclass(frozen=True)
class KeywordScore:
    value: int
    reasons: tuple[str, ...]
    keys: tuple[str, ...]
    matched_keywords: tuple[str, ...]


@dataclass(frozen=True)
class ScoredJob:
    raw: dict[str, str]
    location: ComponentScore
    company: ComponentScore
    role: ComponentScore
    language: ComponentScore
    skill: KeywordScore
    risk: KeywordScore
    total: int
    level: str
    recommendation: str
    explanation: str


def score_jobs(jobs: list[dict[str, str]], config: ScoringConfig) -> list[ScoredJob]:
    return [score_job(job, config) for job in jobs]


def score_job(job: Mapping[str, str], config: ScoringConfig) -> ScoredJob:
    location = score_location(job.get("location_raw", ""), config.locations)
    company = score_company_type(job.get("company_type", ""), config.company_types)
    searchable_text = _join_text(
        job.get("title", ""),
        job.get("description", ""),
        job.get("requirements", ""),
    )
    role = score_role(searchable_text, config.roles)
    language = score_language(job.get("language_raw", ""), config.languages)
    skill = score_skills(searchable_text, config.skills, config.skill_max_total)
    risk = score_risks(searchable_text, config.risks)

    raw_total = (
        location.value
        + company.value
        + role.value
        + language.value
        + skill.value
        + risk.value
    )
    total = _clamp(round(raw_total), 0, 100)
    level = _score_level(total)
    recommendation = _recommendation(total)
    explanation = "; ".join(
        part
        for part in (
            location.reason,
            company.reason,
            role.reason,
            language.reason,
            _format_keyword_reason("skill", skill),
            _format_keyword_reason("risk", risk),
        )
        if part
    )

    return ScoredJob(
        raw=dict(job),
        location=location,
        company=company,
        role=role,
        language=language,
        skill=skill,
        risk=risk,
        total=total,
        level=level,
        recommendation=recommendation,
        explanation=explanation,
    )


def score_location(location_raw: str, rules: tuple[WeightRule, ...]) -> ComponentScore:
    text = _normalize(location_raw)
    unknown_rule = _find_weight_rule("unknown", rules)
    for rule in rules:
        if any(_normalize(pattern) in text for pattern in rule.patterns):
            return ComponentScore(
                rule.score,
                f"location:{rule.explanation} +{rule.score}",
                rule.key,
            )
    if unknown_rule:
        return ComponentScore(
            unknown_rule.score,
            f"location:{unknown_rule.explanation} +{unknown_rule.score}",
            unknown_rule.key,
        )
    return ComponentScore(0, "location:未命中 +0")


def score_company_type(company_type: str, rules: dict[str, WeightRule]) -> ComponentScore:
    rule = rules.get(company_type) or rules.get("unknown")
    if rule is None:
        return ComponentScore(0, "company:未命中 +0")
    return ComponentScore(rule.score, f"company:{rule.explanation} +{rule.score}", rule.key)


def score_role(text: str, rules: tuple[KeywordRule, ...]) -> ComponentScore:
    best_rule: KeywordRule | None = None
    best_keyword = ""
    for rule in rules:
        keyword = _first_matching_keyword(text, rule.keywords)
        if keyword and (best_rule is None or rule.points > best_rule.points):
            best_rule = rule
            best_keyword = keyword

    if best_rule is None:
        return ComponentScore(0, "role:未命中 +0")
    return ComponentScore(
        best_rule.points,
        f"role:{best_rule.explanation} +{best_rule.points} ({best_keyword})",
        best_rule.key,
    )


def score_language(language_raw: str, rules: tuple[KeywordRule, ...]) -> ComponentScore:
    text = language_raw or "unknown"
    for rule in rules:
        keyword = _first_matching_keyword(text, rule.keywords)
        if keyword:
            return ComponentScore(
                rule.points,
                f"language:{rule.explanation} +{rule.points}",
                rule.key,
            )
    unknown = next((rule for rule in rules if rule.key == "unknown"), None)
    if unknown is None:
        return ComponentScore(0, "language:未命中 +0")
    return ComponentScore(
        unknown.points,
        f"language:{unknown.explanation} +{unknown.points}",
        unknown.key,
    )


def score_skills(
    text: str,
    rules: tuple[KeywordRule, ...],
    max_total: int | None = None,
) -> KeywordScore:
    return _score_keyword_sum(text, rules, max_total=max_total)


def score_risks(text: str, rules: tuple[KeywordRule, ...]) -> KeywordScore:
    return _score_keyword_sum(text, rules, min_total=-40)


def _score_keyword_sum(
    text: str,
    rules: tuple[KeywordRule, ...],
    max_total: int | None = None,
    min_total: int | None = None,
) -> KeywordScore:
    value = 0
    reasons: list[str] = []
    keys: list[str] = []
    matched_keywords: list[str] = []

    for rule in rules:
        keyword = _first_matching_keyword(text, rule.keywords)
        if not keyword:
            continue
        value += rule.points
        keys.append(rule.key)
        matched_keywords.append(keyword)
        sign = "+" if rule.points >= 0 else ""
        reasons.append(f"{rule.explanation} {sign}{rule.points} ({keyword})")

    if max_total is not None and value > max_total:
        value = max_total
    if min_total is not None and value < min_total:
        value = min_total

    return KeywordScore(
        value=value,
        reasons=tuple(reasons),
        keys=tuple(keys),
        matched_keywords=tuple(matched_keywords),
    )


def _find_weight_rule(key: str, rules: tuple[WeightRule, ...]) -> WeightRule | None:
    return next((rule for rule in rules if rule.key == key), None)


def _first_matching_keyword(text: str, keywords: tuple[str, ...]) -> str:
    normalized_text = _normalize(text)
    for keyword in keywords:
        if _normalize(keyword) in normalized_text:
            return keyword
    return ""


def _normalize(value: str) -> str:
    return value.casefold()


def _join_text(*parts: str) -> str:
    return "\n".join(part for part in parts if part)


def _clamp(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, value))


def _score_level(total: int) -> str:
    if total >= 85:
        return "high"
    if total >= 65:
        return "medium"
    if total >= 40:
        return "low"
    return "very_low"


def _recommendation(total: int) -> str:
    if total >= 85:
        return "strong_match"
    if total >= 65:
        return "match"
    if total >= 40:
        return "maybe"
    return "low_priority"


def _format_keyword_reason(prefix: str, score: KeywordScore) -> str:
    if not score.reasons:
        return f"{prefix}:未命中 +0"
    return f"{prefix}:" + ", ".join(score.reasons)
