"""Reporting, reconciliation and chart generation for verified data-quality outputs."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib
import pandas as pd
from matplotlib import pyplot as plt
from pandas.testing import assert_frame_equal

from data_quality import build_module_kpis

plt.switch_backend("Agg")
matplotlib.rcParams["svg.fonttype"] = "none"
matplotlib.rcParams["svg.hashsalt"] = "python-data-basics-reporting"

CLEANED_COLUMNS = {
    "result_id",
    "learner_id",
    "module",
    "assessment_date",
    "score",
    "max_score",
    "pass_score",
    "score_percentage",
    "passed",
}
REJECTED_COLUMNS = {"result_id", "rejection_reasons"}
KPI_COLUMNS = [
    "module",
    "result_count",
    "learner_count",
    "average_score_percentage",
    "passed_count",
    "failed_count",
    "pass_rate_percentage",
]


class ReportingError(ValueError):
    """Raised when reporting inputs are missing or fail reconciliation."""


@dataclass(frozen=True)
class ReportingInputs:
    """Verified files loaded from one data-quality workflow output directory."""

    cleaned: pd.DataFrame
    rejected: pd.DataFrame
    module_kpis: pd.DataFrame
    quality_report: dict[str, Any]


@dataclass(frozen=True)
class ReportingResult:
    """In-memory and persisted outputs from one reporting run."""

    module_kpis: pd.DataFrame
    rejection_reason_summary: pd.DataFrame
    summary: dict[str, Any]
    output_dir: Path


def _require_columns(frame: pd.DataFrame, required: set[str], label: str) -> None:
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ReportingError(f"{label} is missing required columns: {', '.join(missing)}")


def load_reporting_inputs(data_quality_dir: str | Path) -> ReportingInputs:
    """Load and validate the four files produced by the data-quality workflow."""

    input_dir = Path(data_quality_dir)
    paths = {
        "cleaned": input_dir / "cleaned_results.csv",
        "rejected": input_dir / "rejected_results.csv",
        "module_kpis": input_dir / "module_kpis.csv",
        "quality_report": input_dir / "quality_report.json",
    }
    missing_files = sorted(path.name for path in paths.values() if not path.is_file())
    if missing_files:
        raise ReportingError(f"Missing reporting input files: {', '.join(missing_files)}")

    cleaned = pd.read_csv(paths["cleaned"])
    rejected = pd.read_csv(paths["rejected"])
    module_kpis = pd.read_csv(paths["module_kpis"])
    quality_report = json.loads(paths["quality_report"].read_text(encoding="utf-8"))

    _require_columns(cleaned, CLEANED_COLUMNS, "cleaned_results.csv")
    _require_columns(rejected, REJECTED_COLUMNS, "rejected_results.csv")
    _require_columns(module_kpis, set(KPI_COLUMNS), "module_kpis.csv")

    return ReportingInputs(
        cleaned=cleaned,
        rejected=rejected,
        module_kpis=module_kpis.loc[:, KPI_COLUMNS].copy(),
        quality_report=quality_report,
    )


def reconcile_module_kpis(cleaned: pd.DataFrame, persisted_kpis: pd.DataFrame) -> pd.DataFrame:
    """Recalculate module KPIs and fail when they differ from the persisted CSV."""

    recalculated = build_module_kpis(cleaned).loc[:, KPI_COLUMNS]
    recalculated = recalculated.sort_values("module", kind="stable").reset_index(drop=True)
    persisted = (
        persisted_kpis.loc[:, KPI_COLUMNS]
        .sort_values("module", kind="stable")
        .reset_index(drop=True)
    )

    try:
        assert_frame_equal(
            recalculated,
            persisted,
            check_dtype=False,
            check_exact=False,
            rtol=1e-9,
            atol=1e-9,
        )
    except AssertionError as exc:
        raise ReportingError("Persisted module KPIs do not match recalculated values.") from exc

    return recalculated


def build_rejection_reason_summary(rejected: pd.DataFrame) -> pd.DataFrame:
    """Count pipe-separated rejection reason codes in deterministic order."""

    _require_columns(rejected, REJECTED_COLUMNS, "rejected results")
    if rejected.empty:
        return pd.DataFrame(columns=["rejection_reason", "rejected_row_count"])

    reasons = rejected["rejection_reasons"].astype("string").str.split("|").explode().str.strip()
    reasons = reasons[reasons.ne("") & reasons.notna()]
    summary = (
        reasons.value_counts()
        .rename_axis("rejection_reason")
        .reset_index(name="rejected_row_count")
    )
    summary = summary.sort_values(
        ["rejected_row_count", "rejection_reason"],
        ascending=[False, True],
        kind="stable",
    ).reset_index(drop=True)
    summary["rejected_row_count"] = summary["rejected_row_count"].astype("int64")
    return summary


def build_reporting_summary(
    inputs: ReportingInputs,
    reconciled_kpis: pd.DataFrame,
    rejection_summary: pd.DataFrame,
) -> dict[str, Any]:
    """Build compact machine-readable reporting control totals."""

    passed = inputs.cleaned["passed"].astype("boolean")
    top_reason = None
    if not rejection_summary.empty:
        top_reason = str(rejection_summary.loc[0, "rejection_reason"])

    return {
        "kpi_reconciliation": "passed",
        "source_quality_status": inputs.quality_report.get("quality_status"),
        "module_count": int(len(reconciled_kpis)),
        "result_count": int(len(inputs.cleaned)),
        "rejected_row_count": int(len(inputs.rejected)),
        "overall_average_score_percentage": round(
            float(inputs.cleaned["score_percentage"].mean()), 2
        ),
        "overall_pass_rate_percentage": round(float(passed.mean() * 100), 2),
        "rejection_reason_count": int(len(rejection_summary)),
        "top_rejection_reason": top_reason,
        "generated_files": [
            "average_score_by_module.svg",
            "pass_rate_by_module.svg",
            "rejection_reason_summary.csv",
            "reporting_summary.json",
        ],
    }


def create_metric_figure(
    module_kpis: pd.DataFrame,
    metric: str,
    title: str,
    y_label: str,
) -> plt.Figure:
    """Create a bounded percentage bar chart for one verified module KPI."""

    if metric not in module_kpis.columns:
        raise ReportingError(f"Unknown KPI metric: {metric}")

    figure, axis = plt.subplots(figsize=(8, 4.5))
    bars = axis.bar(module_kpis["module"], module_kpis[metric])
    axis.set_ylim(0, 100)
    axis.set_ylabel(y_label)
    axis.set_title(title)
    axis.tick_params(axis="x", rotation=20)

    for bar, value in zip(bars, module_kpis[metric], strict=True):
        axis.text(
            bar.get_x() + bar.get_width() / 2,
            float(value) + 2,
            f"{float(value):.2f}%",
            ha="center",
            va="bottom",
        )

    figure.tight_layout()
    return figure


def _save_svg(figure: plt.Figure, output_path: Path) -> None:
    figure.savefig(output_path, format="svg", metadata={"Date": None})
    plt.close(figure)


def run_reporting(data_quality_dir: str | Path, output_dir: str | Path) -> ReportingResult:
    """Reconcile source KPIs and export reporting tables, charts and control totals."""

    inputs = load_reporting_inputs(data_quality_dir)
    reconciled_kpis = reconcile_module_kpis(inputs.cleaned, inputs.module_kpis)
    rejection_summary = build_rejection_reason_summary(inputs.rejected)
    summary = build_reporting_summary(inputs, reconciled_kpis, rejection_summary)

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    rejection_summary.to_csv(
        destination / "rejection_reason_summary.csv",
        index=False,
        lineterminator="\n",
    )
    (destination / "reporting_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    average_figure = create_metric_figure(
        reconciled_kpis,
        "average_score_percentage",
        "Average score by module",
        "Average score (%)",
    )
    _save_svg(average_figure, destination / "average_score_by_module.svg")

    pass_rate_figure = create_metric_figure(
        reconciled_kpis,
        "pass_rate_percentage",
        "Pass rate by module",
        "Pass rate (%)",
    )
    _save_svg(pass_rate_figure, destination / "pass_rate_by_module.svg")

    return ReportingResult(
        module_kpis=reconciled_kpis,
        rejection_reason_summary=rejection_summary,
        summary=summary,
        output_dir=destination,
    )
