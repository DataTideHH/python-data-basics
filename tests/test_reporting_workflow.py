from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from data_quality import run_workflow
from reporting import (
    ReportingError,
    build_rejection_reason_summary,
    load_reporting_inputs,
    reconcile_module_kpis,
    run_reporting,
)

SAMPLE_INPUT = Path("data/raw/training_results.csv")


def prepare_data_quality_outputs(tmp_path: Path) -> Path:
    output_dir = tmp_path / "data-quality"
    run_workflow(SAMPLE_INPUT, output_dir)
    return output_dir


def test_reporting_outputs_match_verified_control_totals(tmp_path: Path) -> None:
    data_quality_dir = prepare_data_quality_outputs(tmp_path)
    result = run_reporting(data_quality_dir, tmp_path / "reporting")

    assert result.summary["kpi_reconciliation"] == "passed"
    assert result.summary["source_quality_status"] == "passed_with_rejections"
    assert result.summary["module_count"] == 4
    assert result.summary["result_count"] == 8
    assert result.summary["rejected_row_count"] == 7
    assert result.summary["overall_average_score_percentage"] == 70.0
    assert result.summary["overall_pass_rate_percentage"] == 62.5
    assert result.summary["rejection_reason_count"] == 7

    expected_files = {
        "average_score_by_module.svg",
        "pass_rate_by_module.svg",
        "rejection_reason_summary.csv",
        "reporting_summary.json",
    }
    assert {path.name for path in result.output_dir.iterdir()} == expected_files

    persisted_summary = json.loads(
        (result.output_dir / "reporting_summary.json").read_text(encoding="utf-8")
    )
    assert persisted_summary == result.summary


def test_rejection_reason_summary_is_complete_and_deterministic(tmp_path: Path) -> None:
    data_quality_dir = prepare_data_quality_outputs(tmp_path)
    inputs = load_reporting_inputs(data_quality_dir)

    summary = build_rejection_reason_summary(inputs.rejected)

    assert list(summary.columns) == ["rejection_reason", "rejected_row_count"]
    assert dict(zip(summary["rejection_reason"], summary["rejected_row_count"], strict=True)) == {
        "pass_score_above_max_score": 2,
        "score_above_max_score": 2,
        "duplicate_exact": 1,
        "invalid_assessment_date": 1,
        "max_score_not_positive": 1,
        "missing_learner_id": 1,
        "missing_score": 1,
    }
    assert list(summary["rejection_reason"]) == [
        "pass_score_above_max_score",
        "score_above_max_score",
        "duplicate_exact",
        "invalid_assessment_date",
        "max_score_not_positive",
        "missing_learner_id",
        "missing_score",
    ]


def test_persisted_kpi_mismatch_is_rejected(tmp_path: Path) -> None:
    data_quality_dir = prepare_data_quality_outputs(tmp_path)
    inputs = load_reporting_inputs(data_quality_dir)
    modified = inputs.module_kpis.copy()
    modified.loc[modified["module"] == "SQL Basics", "pass_rate_percentage"] = 99.0

    with pytest.raises(ReportingError, match="do not match"):
        reconcile_module_kpis(inputs.cleaned, modified)


def test_missing_reporting_input_file_raises_clear_error(tmp_path: Path) -> None:
    data_quality_dir = prepare_data_quality_outputs(tmp_path)
    (data_quality_dir / "module_kpis.csv").unlink()

    with pytest.raises(ReportingError, match="module_kpis.csv"):
        load_reporting_inputs(data_quality_dir)


def test_generated_svg_charts_are_nonempty_and_labeled(tmp_path: Path) -> None:
    data_quality_dir = prepare_data_quality_outputs(tmp_path)
    result = run_reporting(data_quality_dir, tmp_path / "reporting")

    average_svg = (result.output_dir / "average_score_by_module.svg").read_text(encoding="utf-8")
    pass_rate_svg = (result.output_dir / "pass_rate_by_module.svg").read_text(encoding="utf-8")

    assert "<svg" in average_svg
    assert "Average score by module" in average_svg
    assert "77.33%" in average_svg
    assert "<svg" in pass_rate_svg
    assert "Pass rate by module" in pass_rate_svg
    assert "100.00%" in pass_rate_svg


def test_empty_rejection_input_has_stable_schema() -> None:
    rejected = pd.DataFrame(columns=["result_id", "rejection_reasons"])

    summary = build_rejection_reason_summary(rejected)

    assert summary.empty
    assert list(summary.columns) == ["rejection_reason", "rejected_row_count"]
