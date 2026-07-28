"""Command-line entry point for the data-quality workflow."""

from __future__ import annotations

import argparse
from pathlib import Path

from data_quality.workflow import DataQualityError, run_workflow


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate, clean, aggregate and export a small assessment-result CSV."
    )
    parser.add_argument("--input", type=Path, required=True, help="Path to the raw CSV input.")
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Directory for cleaned data, rejected rows, KPIs and the quality report.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        result = run_workflow(args.input, args.output)
    except DataQualityError as exc:
        print(f"Data-quality workflow failed: {exc}")
        return 1

    print("Data-quality workflow completed.")
    print(f"Input rows: {result.report['input_rows']}")
    print(f"Accepted rows: {result.report['accepted_rows']}")
    print(f"Rejected rows: {result.report['rejected_rows']}")
    print(f"Output directory: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
