# Reporting and Notebook Verification

## Purpose

This increment adds a compact reporting layer on top of the tested data-quality workflow. It does not recalculate business results from the raw CSV independently. Instead, it consumes the four generated data-quality outputs, verifies that the persisted module KPIs still match a fresh calculation from the cleaned records, and then produces presentation-ready reporting artefacts.

The reporting sequence is:

```text
raw CSV
→ tested data-quality workflow
→ cleaned and rejected records
→ persisted module KPIs
→ independent KPI reconciliation
→ rejection-reason summary
→ charts and notebook verification
```

## Required inputs

Run the data-quality workflow first:

```bash
python -m data_quality \
  --input data/raw/training_results.csv \
  --output .ci-output/data-quality
```

The reporting workflow expects:

```text
.ci-output/data-quality/
├── cleaned_results.csv
├── rejected_results.csv
├── module_kpis.csv
└── quality_report.json
```

A missing file, missing required column or KPI mismatch stops reporting with a non-zero exit code.

## Reporting command

### Windows PowerShell

```powershell
python -m reporting `
  --input ".ci-output/data-quality" `
  --output ".ci-output/reporting"
```

### macOS and Linux

```bash
python -m reporting \
  --input .ci-output/data-quality \
  --output .ci-output/reporting
```

The command writes:

```text
.ci-output/reporting/
├── average_score_by_module.svg
├── pass_rate_by_module.svg
├── rejection_reason_summary.csv
└── reporting_summary.json
```

## Verified control totals

The committed synthetic fixture produces these reporting controls:

| Control | Expected value |
|---|---:|
| Reconciled modules | 4 |
| Accepted results | 8 |
| Rejected rows | 7 |
| Overall average score | 70.00% |
| Overall pass rate | 62.50% |
| Distinct rejection reasons | 7 |
| Rejection-reason occurrences | 9 |
| KPI reconciliation | passed |

The reporting workflow recalculates module KPIs from `cleaned_results.csv` and compares them with `module_kpis.csv`. The comparison permits harmless dtype differences introduced by CSV persistence but not value differences.

## Rejection-reason reporting

`rejected_results.csv` retains pipe-separated reason codes per rejected source row. Reporting explodes those codes and creates one deterministic count per reason.

A rejected row can violate more than one rule. The fixture has seven rejected rows but nine reason occurrences:

| Rejection reason | Occurrences |
|---|---:|
| `pass_score_above_max_score` | 2 |
| `score_above_max_score` | 2 |
| `duplicate_exact` | 1 |
| `invalid_assessment_date` | 1 |
| `max_score_not_positive` | 1 |
| `missing_learner_id` | 1 |
| `missing_score` | 1 |

This distinction is intentional. A non-positive maximum score can also cause the score and pass threshold to exceed that maximum, so suppressing secondary violations would hide useful quality information.

## Notebook

[`notebooks/reporting_verification.ipynb`](../notebooks/reporting_verification.ipynb) reads the generated data-quality files and performs the same reconciliation through the reusable `reporting` package.

The notebook contains:

1. verified module KPI table
2. rejection-reason summary
3. average-score chart
4. pass-rate chart
5. explicit control-total assertions
6. final `Reporting notebook verification passed.` marker

The notebook resolves the repository root from its current working directory, so it behaves consistently when launched from the repository root, an IDE or `nbconvert` from the `notebooks/` directory.

The committed notebook contains no outputs, execution counts, local paths or IDE timestamps. CI executes a temporary copy after the data-quality and reporting command-line workflows have succeeded.

## Reference charts

The README embeds two small SVG reference charts for the committed synthetic fixture. Fresh Matplotlib SVG files are generated on every CI run and uploaded as short-lived workflow artefacts.

The committed reference files are:

- [`docs/assets/average-score-by-module.svg`](assets/average-score-by-module.svg)
- [`docs/assets/pass-rate-by-module.svg`](assets/pass-rate-by-module.svg)

## Automated verification

The pytest suite covers:

- expected reporting control totals
- exact generated file set
- complete and deterministic rejection-reason counts
- rejection of a deliberately modified KPI value
- clear failure for a missing reporting input
- non-empty, labelled SVG output
- stable empty-summary schemas
- hygiene checks for both committed notebooks

GitHub Actions runs the complete chain on Ubuntu 24.04 and Windows 2025 with Python 3.12.

## Scope boundary

This is a learning-grade reporting and verification layer. It does not claim:

- a production semantic model
- a Power BI report
- scheduled orchestration
- interactive dashboard filtering
- production publication or access control
- statistical inference from the small synthetic fixture

Its purpose is to demonstrate a controlled transition from validated tabular data to reproducible reporting evidence.
