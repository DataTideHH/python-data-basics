"""Reusable validation, cleaning, KPI and export functions for tabular learning data."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

REQUIRED_COLUMNS = (
    "result_id",
    "learner_id",
    "module",
    "assessment_date",
    "score",
    "max_score",
    "pass_score",
)
TEXT_COLUMNS = ("result_id", "learner_id", "module", "assessment_date")
NUMERIC_COLUMNS = ("score", "max_score", "pass_score")


class DataQualityError(ValueError):
    """Raised when the input schema prevents a meaningful workflow run."""


@dataclass(frozen=True)
class WorkflowResult:
    """In-memory outputs produced by one workflow execution."""

    cleaned: pd.DataFrame
    rejected: pd.DataFrame
    module_kpis: pd.DataFrame
    report: dict[str, Any]


def load_csv(path: str | Path) -> pd.DataFrame:
    """Read a CSV as text so validation controls all later type conversion."""

    input_path = Path(path)
    if not input_path.is_file():
        raise DataQualityError(f"Input file does not exist: {input_path}")

    frame = pd.read_csv(input_path, dtype="string", keep_default_na=False)
    frame.columns = [str(column).strip() for column in frame.columns]
    return frame


def _normalise_text(series: pd.Series) -> pd.Series:
    return series.astype("string").str.strip()


def _append_reason(reasons: dict[int, list[str]], mask: pd.Series, code: str) -> None:
    for index in mask[mask].index:
        reasons[int(index)].append(code)


def validate_and_clean(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    """Validate rows, reject invalid records and derive analysis-ready columns."""

    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(frame.columns))
    if missing_columns:
        joined = ", ".join(missing_columns)
        raise DataQualityError(f"Missing required columns: {joined}")

    unexpected_columns = sorted(set(frame.columns) - set(REQUIRED_COLUMNS))
    raw = frame.loc[:, REQUIRED_COLUMNS].copy().reset_index(drop=True)
    raw.insert(0, "source_row", raw.index + 2)

    working = raw.copy()
    for column in TEXT_COLUMNS:
        working[column] = _normalise_text(working[column])

    working["result_id"] = working["result_id"].str.upper()
    working["learner_id"] = working["learner_id"].str.upper()
    working["module"] = working["module"].str.replace(r"\s+", " ", regex=True)

    reasons: dict[int, list[str]] = {index: [] for index in working.index}

    for column in REQUIRED_COLUMNS:
        missing_mask = working[column].astype("string").str.strip().eq("")
        _append_reason(reasons, missing_mask, f"missing_{column}")

    for column in NUMERIC_COLUMNS:
        working[column] = pd.to_numeric(working[column], errors="coerce")
        invalid_numeric = working[column].isna() & raw[column].astype("string").str.strip().ne("")
        _append_reason(reasons, invalid_numeric, f"invalid_{column}")

    parsed_dates = pd.to_datetime(working["assessment_date"], errors="coerce", format="%Y-%m-%d")
    invalid_dates = parsed_dates.isna() & raw["assessment_date"].astype("string").str.strip().ne("")
    _append_reason(reasons, invalid_dates, "invalid_assessment_date")
    working["assessment_date"] = parsed_dates

    _append_reason(reasons, working["max_score"].le(0), "max_score_not_positive")
    _append_reason(reasons, working["score"].lt(0), "score_below_zero")
    _append_reason(reasons, working["pass_score"].lt(0), "pass_score_below_zero")
    _append_reason(
        reasons,
        working["score"].gt(working["max_score"]),
        "score_above_max_score",
    )
    _append_reason(
        reasons,
        working["pass_score"].gt(working["max_score"]),
        "pass_score_above_max_score",
    )

    duplicate_mask = working["result_id"].ne("") & working["result_id"].duplicated(keep=False)
    for _, group in working[duplicate_mask].groupby("result_id", sort=False):
        comparison_columns = list(REQUIRED_COLUMNS[1:])
        unique_variants = group[comparison_columns].astype("string").drop_duplicates()
        if len(unique_variants) == 1:
            duplicate_indexes = list(group.index[1:])
            for index in duplicate_indexes:
                reasons[int(index)].append("duplicate_exact")
        else:
            for index in group.index:
                reasons[int(index)].append("duplicate_result_id_conflict")

    rejected_indexes = [index for index, row_reasons in reasons.items() if row_reasons]
    accepted_indexes = [index for index in working.index if index not in rejected_indexes]

    cleaned = working.loc[accepted_indexes, ["source_row", *REQUIRED_COLUMNS]].copy()
    cleaned["assessment_date"] = cleaned["assessment_date"].dt.strftime("%Y-%m-%d")
    cleaned["score_percentage"] = cleaned["score"].div(cleaned["max_score"]).mul(100).round(2)
    cleaned["passed"] = cleaned["score"].ge(cleaned["pass_score"]).astype(bool)
    cleaned = cleaned.sort_values(["assessment_date", "result_id"], kind="stable").reset_index(
        drop=True
    )

    rejected = raw.loc[rejected_indexes].copy()
    if rejected.empty:
        rejected["rejection_reasons"] = pd.Series(dtype="string")
    else:
        rejected["rejection_reasons"] = [
            "|".join(sorted(set(reasons[int(index)]))) for index in rejected_indexes
        ]
        rejected = rejected.reset_index(drop=True)

    reason_counts = Counter(
        reason for row_reasons in reasons.values() for reason in set(row_reasons)
    )
    report: dict[str, Any] = {
        "quality_status": "passed_with_rejections" if rejected_indexes else "passed",
        "input_rows": int(len(raw)),
        "accepted_rows": int(len(cleaned)),
        "rejected_rows": int(len(rejected)),
        "acceptance_rate_percentage": round(len(cleaned) / len(raw) * 100, 2) if len(raw) else 0.0,
        "exact_duplicate_rows_removed": int(reason_counts.get("duplicate_exact", 0)),
        "conflicting_duplicate_rows": int(reason_counts.get("duplicate_result_id_conflict", 0)),
        "unexpected_columns_ignored": unexpected_columns,
        "rejection_reason_counts": dict(sorted(reason_counts.items())),
    }
    return cleaned, rejected, report


def build_module_kpis(cleaned: pd.DataFrame) -> pd.DataFrame:
    """Aggregate analysis-ready rows into one deterministic record per module."""

    expected = {"module", "learner_id", "score_percentage", "passed"}
    missing = sorted(expected - set(cleaned.columns))
    if missing:
        raise DataQualityError(f"Cannot build KPIs; missing cleaned columns: {', '.join(missing)}")

    if cleaned.empty:
        return pd.DataFrame(
            columns=[
                "module",
                "result_count",
                "learner_count",
                "average_score_percentage",
                "passed_count",
                "failed_count",
                "pass_rate_percentage",
            ]
        )

    grouped = cleaned.groupby("module", as_index=False, sort=True).agg(
        result_count=("result_id", "size"),
        learner_count=("learner_id", "nunique"),
        average_score_percentage=("score_percentage", "mean"),
        passed_count=("passed", "sum"),
    )
    grouped["failed_count"] = grouped["result_count"] - grouped["passed_count"]
    grouped["pass_rate_percentage"] = (
        grouped["passed_count"].div(grouped["result_count"]).mul(100).round(2)
    )
    grouped["average_score_percentage"] = grouped["average_score_percentage"].round(2)
    for column in ("result_count", "learner_count", "passed_count", "failed_count"):
        grouped[column] = grouped[column].astype("int64")
    return grouped


def run_workflow(input_path: str | Path, output_dir: str | Path) -> WorkflowResult:
    """Run the complete workflow and write deterministic CSV and JSON outputs."""

    frame = load_csv(input_path)
    cleaned, rejected, report = validate_and_clean(frame)
    module_kpis = build_module_kpis(cleaned)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    cleaned.to_csv(output_path / "cleaned_results.csv", index=False, lineterminator="\n")
    rejected.to_csv(output_path / "rejected_results.csv", index=False, lineterminator="\n")
    module_kpis.to_csv(output_path / "module_kpis.csv", index=False, lineterminator="\n")
    (output_path / "quality_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    return WorkflowResult(
        cleaned=cleaned,
        rejected=rejected,
        module_kpis=module_kpis,
        report=report,
    )
