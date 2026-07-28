from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from data_quality import DataQualityError, build_module_kpis, run_workflow, validate_and_clean

SAMPLE_INPUT = Path("data/raw/training_results.csv")


def test_sample_workflow_writes_verified_outputs(tmp_path: Path) -> None:
    result = run_workflow(SAMPLE_INPUT, tmp_path)

    assert result.report["quality_status"] == "passed_with_rejections"
    assert result.report["input_rows"] == 15
    assert result.report["accepted_rows"] == 8
    assert result.report["rejected_rows"] == 7
    assert result.report["exact_duplicate_rows_removed"] == 1
    assert result.report["conflicting_duplicate_rows"] == 0
    assert result.report["acceptance_rate_percentage"] == 53.33

    assert set(result.cleaned["result_id"]) == {
        "R001",
        "R002",
        "R003",
        "R007",
        "R008",
        "R011",
        "R012",
        "R014",
    }
    assert result.cleaned["result_id"].is_unique
    assert result.cleaned["score_percentage"].between(0, 100).all()
    assert result.cleaned["passed"].dtype == bool

    expected_files = {
        "cleaned_results.csv",
        "rejected_results.csv",
        "module_kpis.csv",
        "quality_report.json",
    }
    assert {path.name for path in tmp_path.iterdir()} == expected_files

    report_text = (tmp_path / "quality_report.json").read_text(encoding="utf-8")
    assert json.loads(report_text) == result.report


def test_module_kpis_are_deterministic(tmp_path: Path) -> None:
    result = run_workflow(SAMPLE_INPUT, tmp_path)
    kpis = result.module_kpis.set_index("module")

    assert list(result.module_kpis["module"]) == [
        "Data Quality",
        "Process Analysis",
        "Python Basics",
        "SQL Basics",
    ]
    assert kpis.loc["SQL Basics", "result_count"] == 3
    assert kpis.loc["SQL Basics", "average_score_percentage"] == 77.33
    assert kpis.loc["SQL Basics", "pass_rate_percentage"] == 66.67
    assert kpis.loc["Process Analysis", "failed_count"] == 1
    assert kpis.loc["Python Basics", "pass_rate_percentage"] == 100.0


def test_missing_required_column_raises_clear_error() -> None:
    frame = pd.DataFrame(
        {
            "result_id": ["R001"],
            "learner_id": ["L001"],
            "module": ["SQL Basics"],
            "assessment_date": ["2026-07-01"],
            "score": ["80"],
            "max_score": ["100"],
        }
    )

    with pytest.raises(DataQualityError, match="pass_score"):
        validate_and_clean(frame)


def test_conflicting_duplicate_result_ids_reject_every_variant() -> None:
    frame = pd.DataFrame(
        {
            "result_id": ["R001", "R001"],
            "learner_id": ["L001", "L001"],
            "module": ["SQL Basics", "SQL Basics"],
            "assessment_date": ["2026-07-01", "2026-07-01"],
            "score": ["80", "90"],
            "max_score": ["100", "100"],
            "pass_score": ["60", "60"],
        }
    )

    cleaned, rejected, report = validate_and_clean(frame)

    assert cleaned.empty
    assert len(rejected) == 2
    assert rejected["rejection_reasons"].eq("duplicate_result_id_conflict").all()
    assert report["conflicting_duplicate_rows"] == 2


def test_whitespace_and_identifiers_are_normalised() -> None:
    frame = pd.DataFrame(
        {
            "result_id": [" r001 "],
            "learner_id": [" l001 "],
            "module": ["  Data   Quality  "],
            "assessment_date": ["2026-07-01"],
            "score": ["75"],
            "max_score": ["100"],
            "pass_score": ["60"],
        }
    )

    cleaned, rejected, report = validate_and_clean(frame)

    assert rejected.empty
    assert report["quality_status"] == "passed"
    assert cleaned.loc[0, "result_id"] == "R001"
    assert cleaned.loc[0, "learner_id"] == "L001"
    assert cleaned.loc[0, "module"] == "Data Quality"
    assert cleaned.loc[0, "score_percentage"] == 75.0
    assert bool(cleaned.loc[0, "passed"]) is True


def test_empty_cleaned_frame_has_stable_kpi_schema() -> None:
    empty = pd.DataFrame(
        columns=["module", "learner_id", "result_id", "score_percentage", "passed"]
    )

    kpis = build_module_kpis(empty)

    assert kpis.empty
    assert list(kpis.columns) == [
        "module",
        "result_count",
        "learner_count",
        "average_score_percentage",
        "passed_count",
        "failed_count",
        "pass_rate_percentage",
    ]
