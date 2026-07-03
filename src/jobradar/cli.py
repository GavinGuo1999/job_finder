"""Command line entry point for Job Radar."""

from __future__ import annotations

import argparse

from jobradar import __version__
from jobradar.config import load_scoring_config
from jobradar.exporter import export_jobs_csv, read_fixture_jobs
from jobradar.scoring import score_jobs

# Phase 2 exposes only local fixture scoring; it does not crawl websites.
DESCRIPTION = "Local CSV-first job opportunity radar."


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jobradar",
        description=DESCRIPTION,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    subparsers = parser.add_subparsers(dest="command")

    score_fixtures = subparsers.add_parser(
        "score-fixtures",
        help="Score local fixture jobs and export jobs.csv.",
    )
    score_fixtures.add_argument("--input", required=True, help="Input fixture jobs CSV.")
    score_fixtures.add_argument("--config", required=True, help="Configuration CSV directory.")
    score_fixtures.add_argument("--output", required=True, help="Output runs directory.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "score-fixtures":
        config = load_scoring_config(args.config)
        jobs = read_fixture_jobs(args.input)
        output_path = export_jobs_csv(score_jobs(jobs, config), args.output)
        print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
