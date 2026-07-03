"""CSV configuration loader."""

from __future__ import annotations

# Config files are local UTF-8 CSV files; no network access happens here.
import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class WeightRule:
    key: str
    score: int
    explanation: str
    patterns: tuple[str, ...] = ()


@dataclass(frozen=True)
class KeywordRule:
    key: str
    keywords: tuple[str, ...]
    points: int
    explanation: str
    max_total: int | None = None


@dataclass(frozen=True)
class ScoringConfig:
    locations: tuple[WeightRule, ...]
    company_types: dict[str, WeightRule]
    roles: tuple[KeywordRule, ...]
    languages: tuple[KeywordRule, ...]
    skills: tuple[KeywordRule, ...]
    risks: tuple[KeywordRule, ...]

    @property
    def skill_max_total(self) -> int | None:
        totals = [rule.max_total for rule in self.skills if rule.max_total is not None]
        return max(totals) if totals else None


def load_scoring_config(config_dir: str | Path) -> ScoringConfig:
    root = Path(config_dir)
    company_rules = _load_simple_weights(root / "company_type_weights.csv", "company_type")
    return ScoringConfig(
        locations=tuple(_load_location_weights(root / "location_weights.csv")),
        company_types={rule.key: rule for rule in company_rules},
        roles=tuple(
            _load_keyword_rules(root / "role_category_weights.csv", "role_category", "score")
        ),
        languages=tuple(
            _load_keyword_rules(root / "language_weights.csv", "language_category", "score")
        ),
        skills=tuple(_load_keyword_rules(root / "skill_keywords.csv", "skill_category", "points")),
        risks=tuple(_load_keyword_rules(root / "risk_keywords.csv", "risk_flag", "penalty")),
    )


def _read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing config file: {path}")

    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def _split_terms(value: str | None) -> tuple[str, ...]:
    if not value:
        return ()
    return tuple(term.strip() for term in value.split(";") if term.strip())


def _parse_int(value: str, *, path: Path, field: str) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"Invalid integer in {path.name}.{field}: {value!r}") from exc


def _parse_optional_int(value: str | None, *, path: Path, field: str) -> int | None:
    if value is None or value == "":
        return None
    return _parse_int(value, path=path, field=field)


def _load_location_weights(path: Path) -> list[WeightRule]:
    rules = []
    for row in _read_rows(path):
        rules.append(
            WeightRule(
                key=row["location_category"],
                patterns=_split_terms(row.get("patterns")),
                score=_parse_int(row["score"], path=path, field="score"),
                explanation=row.get("explanation", ""),
            )
        )
    return rules


def _load_simple_weights(path: Path, key_field: str) -> list[WeightRule]:
    rules = []
    for row in _read_rows(path):
        rules.append(
            WeightRule(
                key=row[key_field],
                score=_parse_int(row["score"], path=path, field="score"),
                explanation=row.get("explanation", ""),
            )
        )
    return rules


def _load_keyword_rules(path: Path, key_field: str, points_field: str) -> list[KeywordRule]:
    rules = []
    for row in _read_rows(path):
        rules.append(
            KeywordRule(
                key=row[key_field],
                keywords=_split_terms(row.get("keywords")),
                points=_parse_int(row[points_field], path=path, field=points_field),
                explanation=row.get("explanation", ""),
                max_total=_parse_optional_int(row.get("max_total"), path=path, field="max_total"),
            )
        )
    return rules
