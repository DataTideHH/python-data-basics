from __future__ import annotations

import platform
import sys

import matplotlib
import numpy as np
import pandas as pd

MINIMUM_PYTHON = (3, 12)
REQUIRED_COLUMNS = {"city", "category", "value"}


def collect_environment() -> dict[str, str]:
    """Return the interpreter and direct runtime dependency versions."""
    return {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "matplotlib": matplotlib.__version__,
    }


def build_baseline_data() -> pd.DataFrame:
    """Create deterministic synthetic data for a small pandas sanity check."""
    return pd.DataFrame(
        {
            "city": ["Hamburg", "Berlin", "Hamburg", "Berlin"],
            "category": ["quality", "quality", "processing", "processing"],
            "value": [92.0, 88.0, 71.0, 77.0],
        }
    )


def summarize_baseline_data(frame: pd.DataFrame) -> pd.DataFrame:
    """Validate the input shape and calculate one summary row per category."""
    missing_columns = REQUIRED_COLUMNS.difference(frame.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    if frame.empty:
        raise ValueError("Baseline data must contain at least one row.")

    if frame["value"].isna().any():
        raise ValueError("Baseline data contains missing values in 'value'.")

    summary = (
        frame.groupby("category", as_index=False)
        .agg(row_count=("value", "size"), average_value=("value", "mean"))
        .sort_values("category", ignore_index=True)
    )
    return summary


def run_baseline_check() -> pd.DataFrame:
    """Run the deterministic DataFrame transformation used by local and CI checks."""
    if sys.version_info < MINIMUM_PYTHON:
        required = ".".join(str(part) for part in MINIMUM_PYTHON)
        raise RuntimeError(f"Python {required} or newer is required.")

    summary = summarize_baseline_data(build_baseline_data())
    if summary["row_count"].sum() != 4 or len(summary) != 2:
        raise RuntimeError("The baseline pandas transformation returned unexpected results.")

    return summary


def main() -> None:
    print("Python data baseline check")
    print("--------------------------")
    for name, version in collect_environment().items():
        print(f"{name}: {version}")

    print("\nDeterministic pandas summary")
    print("----------------------------")
    print(run_baseline_check().to_string(index=False))
    print("\nBaseline check passed.")


if __name__ == "__main__":
    main()
