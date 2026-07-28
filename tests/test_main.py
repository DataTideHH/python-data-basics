from __future__ import annotations

import pandas as pd
import pytest

from main import (
    build_baseline_data,
    collect_environment,
    run_baseline_check,
    summarize_baseline_data,
)


def test_collect_environment_reports_direct_runtime_dependencies() -> None:
    environment = collect_environment()

    assert set(environment) == {
        "python",
        "implementation",
        "pandas",
        "numpy",
        "matplotlib",
    }
    assert all(environment.values())


def test_build_baseline_data_returns_expected_shape() -> None:
    frame = build_baseline_data()

    assert list(frame.columns) == ["city", "category", "value"]
    assert frame.shape == (4, 3)
    assert frame["value"].notna().all()


def test_summarize_baseline_data_returns_deterministic_results() -> None:
    summary = summarize_baseline_data(build_baseline_data())

    assert summary.to_dict(orient="records") == [
        {"category": "processing", "row_count": 2, "average_value": 74.0},
        {"category": "quality", "row_count": 2, "average_value": 90.0},
    ]


def test_summarize_baseline_data_rejects_missing_columns() -> None:
    incomplete = pd.DataFrame({"category": ["quality"], "value": [90.0]})

    with pytest.raises(ValueError, match="Missing required columns: city"):
        summarize_baseline_data(incomplete)


def test_summarize_baseline_data_rejects_missing_values() -> None:
    frame = build_baseline_data()
    frame.loc[0, "value"] = None

    with pytest.raises(ValueError, match="contains missing values"):
        summarize_baseline_data(frame)


def test_run_baseline_check_succeeds() -> None:
    summary = run_baseline_check()

    assert summary["row_count"].sum() == 4
    assert len(summary) == 2
