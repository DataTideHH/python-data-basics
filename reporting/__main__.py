"""Command-line entry point for verified reporting outputs."""

from __future__ import annotations

import argparse
from pathlib import Path

from reporting.workflow import ReportingError, run_reporting


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Reconcile data-quality outputs and generate reporting tables and charts."
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Directory containing cleaned_results.csv and the other data-quality outputs.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Directory for verified reporting outputs.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        result = run_reporting(args.input, args.output)
    except ReportingError as exc:
        print(f"Reporting workflow failed: {exc}")
        return 1

    print("Reporting workflow passed.")
    print(f"Modules: {result.summary['module_count']}")
    print(f"Results: {result.summary['result_count']}")
    print(f"Rejected rows: {result.summary['rejected_row_count']}")
    print(
        "Overall average score: "
        f"{result.summary['overall_average_score_percentage']:.2f}%"
    )
    print(
        "Overall pass rate: "
        f"{result.summary['overall_pass_rate_percentage']:.2f}%"
    )
    print(f"Output directory: {result.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
