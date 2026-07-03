"""Configuration loading for Job Radar."""

# Public imports kept explicit for tests and CLI wiring.
from jobradar.config.loader import (
    KeywordRule,
    ScoringConfig,
    WeightRule,
    load_scoring_config,
)

__all__ = ["KeywordRule", "ScoringConfig", "WeightRule", "load_scoring_config"]
