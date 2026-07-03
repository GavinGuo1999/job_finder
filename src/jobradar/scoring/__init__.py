"""Scoring utilities for Job Radar."""

# Scoring is additive and config-driven in Phase 2.
from jobradar.scoring.engine import ScoredJob, score_job, score_jobs

__all__ = ["ScoredJob", "score_job", "score_jobs"]
