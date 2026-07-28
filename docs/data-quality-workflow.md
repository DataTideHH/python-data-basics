# Data-Quality Workflow

## Purpose

This increment demonstrates a small, reproducible Data/BI preparation workflow rather than a production ETL platform. It turns a deliberately imperfect synthetic CSV into four auditable outputs:

1. cleaned assessment results
2. rejected rows with explicit reason codes
3. module-level KPIs
4. a machine-readable quality report

The implementation is intentionally separated into reusable functions so validation and transformation logic can be tested independently from file-system export.

## Input contract

The raw CSV must contain these columns:

| Column | Rule |
|---|---|
| `result_id` | Required, unique after exact-duplicate handling |
| `learner_id` | Required |
| `module` | Required; surrounding and repeated whitespace is normalised |
| `assessment_date` | Required ISO date in `YYYY-MM-DD` format |
| `score` | Numeric, at least zero and not above `max_score` |
| `max_score` | Numeric and greater than zero |
| `pass_score` | Numeric, at least zero and not above `max_score` |

Unexpected columns are ignored but listed in `quality_report.json`.

## Validation and cleaning sequence

The workflow performs the following steps in a fixed order:

1. read all CSV fields as text
2. verify required columns
3. preserve the original CSV row number as `source_row`
4. trim text, uppercase identifiers and collapse repeated module whitespace
5. convert date and numeric fields with invalid values becoming rejection reasons
6. enforce score and threshold ranges
7. remove later copies of exact duplicate `result_id` rows
8. reject every variant of a conflicting duplicate `result_id`
9. derive `score_percentage` and Boolean `passed`
10. aggregate deterministic module KPIs
11. export CSV and JSON outputs

Invalid rows are not silently discarded. They remain visible in `rejected_results.csv` with pipe-separated reason codes.

## Included synthetic issues

`data/raw/training_results.csv` intentionally contains:

- one exact duplicate
- a missing score
- a score above the maximum
- an invalid date
- a missing learner identifier
- a non-positive maximum score
- a pass threshold above the maximum
- whitespace requiring normalisation

The committed raw data is synthetic and contains no personal information.

## Run locally

From the repository root:

```bash
python -m data_quality \
  --input data/raw/training_results.csv \
  --output .ci-output/data-quality
```

PowerShell uses the same arguments:

```powershell
python -m data_quality `
  --input "data/raw/training_results.csv" `
  --output ".ci-output/data-quality"
```

The `.ci-output/` directory is already ignored by Git.

## Expected sample result

The committed fixture contains 15 input rows. The expected workflow result is 8 analysis-ready rows and 7 rejected rows, including the later copy of the exact duplicate.

Expected module KPI control values include:

| Module | Results | Average score | Pass rate |
|---|---:|---:|---:|
| Data Quality | 2 | 71.50% | 50.00% |
| Process Analysis | 2 | 55.00% | 50.00% |
| Python Basics | 1 | 75.00% | 100.00% |
| SQL Basics | 3 | 77.33% | 66.67% |

## Output files

| File | Purpose |
|---|---|
| `cleaned_results.csv` | Normalised and validated analysis-ready records |
| `rejected_results.csv` | Original row values plus explicit rejection reasons |
| `module_kpis.csv` | Result count, learner count, average score, pass/fail counts and pass rate |
| `quality_report.json` | Row counts, acceptance rate, duplicate metrics and rejection-reason counts |

## Failure behaviour

A missing input file or missing required column stops the workflow with a non-zero exit code. Row-level quality problems do not crash the workflow; they are isolated in the rejection output and summarised in the report.

## Scope boundary

This is a learning-grade quality workflow for small CSV files. It does not claim streaming ingestion, distributed processing, schema evolution, database transactions, orchestration, production observability or regulatory validation.
