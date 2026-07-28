# Python Data Basics

[![Python quality](https://github.com/DataTideHH/python-data-basics/actions/workflows/python-quality.yml/badge.svg)](https://github.com/DataTideHH/python-data-basics/actions/workflows/python-quality.yml)

**Python 3.12 · pandas · data quality · KPI reconciliation · reporting · Jupyter · pytest · Ruff · GitHub Actions**

A compact, tested Data/BI workflow that turns an intentionally imperfect CSV into validated records, auditable rejections, reconciled KPIs, reporting summaries, charts and a clean verification notebook.

This repository is part of the DataTideHH portfolio for my IHK retraining in Data and Process Analysis. Its purpose is not to imitate an enterprise platform. It demonstrates a small workflow that can be inspected, executed, tested and explained end to end.

> **Portfolio status:** Core scope complete. Future changes are limited mainly to dependency compatibility, defect correction and documentation clarity. See [`docs/project-status.md`](docs/project-status.md).

---

## What This Demonstrates

| Capability | Evidence in this repository |
|---|---|
| Reproducible Python setup | Python 3.12 project metadata, explicit dependency groups and platform-specific setup documentation |
| Data-quality controls | Required columns, controlled type conversion, missing values, ranges, duplicate handling and row-level rejection reasons |
| Data lineage | Original CSV row retained as `source_row` in validated and rejected outputs |
| KPI logic | Module-level result counts, learner counts, average scores, pass/fail counts and pass rates |
| Reconciliation | Persisted KPI output is recalculated from cleaned records and rejected when values differ |
| Reporting | Deterministic summaries plus Matplotlib SVG charts |
| Notebook discipline | Clean notebooks without committed outputs, execution counts, local paths or IDE timestamps |
| Automated verification | pytest, Ruff, bytecode compilation and end-to-end execution on Ubuntu and Windows |
| Scope discipline | Synthetic data, explicit limitations and no production-scale claims |

---

## End-to-End Workflow

```text
data/raw/training_results.csv
        │
        ▼
validation and controlled cleaning
        │
        ├── cleaned_results.csv
        ├── rejected_results.csv
        ├── module_kpis.csv
        └── quality_report.json
        │
        ▼
KPI recalculation and reconciliation
        │
        ├── rejection_reason_summary.csv
        ├── reporting_summary.json
        ├── average_score_by_module.svg
        └── pass_rate_by_module.svg
        │
        ▼
clean reporting notebook with repeated assertions
```

The reporting layer does not trust `module_kpis.csv` blindly. It derives the expected KPIs again from `cleaned_results.csv` and stops if the persisted and recalculated values differ.

---

## Five-Minute Portfolio Review

A technical reviewer can verify the main workflow without reading every example module.

### 1. Install the development environment

#### Windows PowerShell

```powershell
py -3.12 -m venv .venv
& ".\.venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

#### macOS or Linux

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

Detailed setup and troubleshooting are documented in [`docs/setup.md`](docs/setup.md).

### 2. Run the quality workflow

#### Windows PowerShell

```powershell
python -m data_quality `
  --input "data/raw/training_results.csv" `
  --output ".ci-output/data-quality"
```

#### macOS or Linux

```bash
python -m data_quality \
  --input data/raw/training_results.csv \
  --output .ci-output/data-quality
```

### 3. Run reconciled reporting

#### Windows PowerShell

```powershell
python -m reporting `
  --input ".ci-output/data-quality" `
  --output ".ci-output/reporting"
```

#### macOS or Linux

```bash
python -m reporting \
  --input .ci-output/data-quality \
  --output .ci-output/reporting
```

### 4. Run the complete automated checks

```bash
python -m pytest
python -m ruff check main.py data_quality reporting examples tests
python -m ruff format --check main.py data_quality reporting examples tests
```

---

## Verified Control Totals

The committed synthetic fixture contains 15 source rows with deliberately introduced quality problems.

| Control | Verified value |
|---|---:|
| Input rows | 15 |
| Accepted rows | 8 |
| Rejected rows | 7 |
| Exact duplicate rows removed | 1 |
| Modules | 4 |
| Overall average score | 70.00% |
| Overall pass rate | 62.50% |
| Distinct rejection reasons | 7 |
| KPI reconciliation | passed |

These numbers are automated control values for the fixture, not claims about real learners or business operations.

---

## Data-Quality Rules

The package in [`data_quality/`](data_quality/) implements:

- required-column validation
- missing-value detection
- strict ISO date parsing
- controlled numeric conversion
- positive `max_score`
- non-negative scores and pass thresholds
- scores not exceeding their maximum
- pass thresholds not exceeding their maximum
- exact duplicate removal
- rejection of conflicting records sharing one result ID
- identifier and whitespace normalisation

Invalid rows are not silently dropped. They remain visible in `rejected_results.csv` with explicit pipe-separated reason codes.

Accepted records include:

- `source_row` for lineage to the raw CSV
- normalised identifiers and module names
- `score_percentage`
- a non-null Boolean `passed`

The complete contract is documented in [`docs/data-quality-workflow.md`](docs/data-quality-workflow.md).

---

## Reporting and Visual Evidence

The package in [`reporting/`](reporting/) validates the generated files, recalculates KPIs, summarises rejection reasons and writes deterministic reporting outputs.

### Average score by module

![Average score by module](docs/assets/average-score-by-module.svg)

### Pass rate by module

![Pass rate by module](docs/assets/pass-rate-by-module.svg)

Fresh SVG files are generated by the workflow during every CI run. The committed reference charts show the expected result for the synthetic fixture.

Detailed reporting behaviour is documented in [`docs/reporting-notebook.md`](docs/reporting-notebook.md).

---

## Notebook Verification

[`notebooks/reporting_verification.ipynb`](notebooks/reporting_verification.ipynb) reads generated workflow outputs rather than embedding a second copy of the source data.

It displays and verifies:

1. reconciled module KPIs
2. rejection-reason counts
3. average-score chart
4. pass-rate chart
5. expected reporting control totals
6. a final verification marker

[`dataspell_test.ipynb`](dataspell_test.ipynb) remains a smaller interpreter and package-import check.

Both committed notebooks are kept free of outputs, execution counts, absolute local paths and IDE-specific timestamps. CI executes temporary copies only.

---

## Continuous Integration

The workflow in [`.github/workflows/python-quality.yml`](.github/workflows/python-quality.yml) runs with Python 3.12 on:

- Ubuntu 24.04
- Windows 2025

Each matrix job performs:

1. dependency installation
2. bytecode compilation
3. Ruff lint and format checks
4. the complete pytest suite
5. the deterministic baseline entry point
6. the full data-quality workflow
7. source control-total verification
8. reporting and KPI reconciliation
9. reporting control-total and SVG verification
10. the bounded optional ML example
11. both notebook executions
12. short-lived artifact upload
13. a final quality gate

This is a quality-assurance workflow, not a deployment or release pipeline.

---

## Repository Structure

```text
python-data-basics/
├── .github/workflows/python-quality.yml
├── data/raw/training_results.csv
├── data_quality/
├── reporting/
├── notebooks/reporting_verification.ipynb
├── docs/
│   ├── assets/
│   ├── data-quality-workflow.md
│   ├── project-status.md
│   ├── reporting-notebook.md
│   └── setup.md
├── examples/
├── tests/
├── dataspell_test.ipynb
├── main.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

---

## Supporting Examples

The repository retains a few bounded learning examples without presenting them as the main portfolio result:

- [`examples/01_csv_pandas_basics.py`](examples/01_csv_pandas_basics.py) — CSV and grouped pandas operations
- [`examples/02_json_basics.py`](examples/02_json_basics.py) — nested JSON normalisation
- [`examples/03_api_request_basics.py`](examples/03_api_request_basics.py) — public API request without credentials
- [`examples/04_ollama_local_api_basics.py`](examples/04_ollama_local_api_basics.py) — optional localhost-only request
- [`examples/optional/logistic_regression_basics.py`](examples/optional/logistic_regression_basics.py) — scikit-learn API demonstration without a model-quality claim

[`main.py`](main.py) is a deterministic environment and pandas sanity check, separate from the substantive data-quality and reporting workflow.

---

## Data and Credential Safety

Only synthetic learning data and public endpoints belong in this repository. The committed fixture contains no real learner, customer or company data.

Excluded content includes:

- virtual environments and caches
- `.env` files and credentials
- API keys and OAuth tokens
- personal or customer data
- IDE metadata
- executed notebook copies
- generated local workflow outputs

---

## Scope Boundaries

This repository does not claim:

- a production package, ETL platform or semantic model
- streaming or distributed processing
- production orchestration, observability or deployment
- regulatory validation
- an interactive dashboard or Power BI report
- a validated predictive model
- statistical inference from the synthetic fixture

The value is the complete, testable chain from imperfect input through validation, auditable rejection, KPI reconciliation and documented reporting.

---

## Related DataTideHH Projects

- [`sql-server-docker-basics`](https://github.com/DataTideHH/sql-server-docker-basics) — reproducible SQL Server analytics lab, relational integrity and star schema
- [`hamburg-district-data-basics`](https://github.com/DataTideHH/hamburg-district-data-basics) — public Hamburg data and Power BI preparation
- [`open-meteo-germany-weather-ranking`](https://github.com/DataTideHH/open-meteo-germany-weather-ranking) — public API-to-CSV scoring workflow
- [`flask-country-data-api`](https://github.com/DataTideHH/flask-country-data-api) — validated ingestion, persistence and API delivery

Portfolio overview: [datatidehh.github.io/DataTideHH](https://datatidehh.github.io/DataTideHH/) · Website: [datatidehh.de](https://datatidehh.de/) · LinkedIn: [linkedin.com/in/datatidehh](https://www.linkedin.com/in/datatidehh/)
