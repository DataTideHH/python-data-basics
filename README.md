# Python Data Basics

[![Python quality](https://github.com/DataTideHH/python-data-basics/actions/workflows/python-quality.yml/badge.svg)](https://github.com/DataTideHH/python-data-basics/actions/workflows/python-quality.yml)

**Python 3.12 · pandas · data quality · pytest · Ruff · Jupyter · GitHub Actions**

This repository is a compact, tested foundation for reproducible Python Data/BI workflows. It combines environment setup, deterministic pandas transformations, a small auditable data-quality workflow, notebook hygiene and cross-platform CI.

It is part of my DataTideHH portfolio during the IHK retraining program in Data and Process Analysis. The scope remains deliberately bounded: this is a reusable learning baseline, not a production ETL platform, predictive-model showcase or finished business analysis.

---

## Project at a Glance

| Area | Current implementation |
|---|---|
| Python baseline | Python 3.12-compatible environment and deterministic pandas sanity check |
| Dependency model | Runtime, notebook, optional ML and development groups in `pyproject.toml` |
| Data-quality workflow | CSV input, schema checks, type conversion, row-level rejection, cleaning, KPIs and export |
| Testing | pytest coverage for baseline logic, data-quality rules, notebook hygiene and optional ML |
| Code quality | Ruff linting and formatting plus Python bytecode compilation |
| Continuous integration | Ubuntu 24.04 and Windows 2025 matrix with Python 3.12 |
| Credential safety | Synthetic/public-safe inputs; local environments and secrets excluded |

## What This Repository Demonstrates

The repository focuses on small tasks that recur in Data/BI work:

- create an isolated Python environment
- define direct dependencies separately from development tooling
- read raw CSV data as text before controlled conversion
- enforce required columns and explicit value rules
- preserve rejected records with reason codes
- normalise identifiers and text fields
- derive analysis-ready columns
- aggregate deterministic module KPIs
- export cleaned data, rejected rows, KPIs and a JSON quality report
- test positive and negative data-quality cases
- run the same checks on Windows and Linux

More complete analyses remain in separate repositories. This project provides tested building blocks underneath them.

---

## Quick Start

Detailed setup instructions are in [`docs/setup.md`](docs/setup.md).

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
& ".\.venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python main.py
```

### macOS and Linux

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python main.py
```

On the Intel iMac used for local portfolio work, Python 3.12 is available at `/usr/local/bin/python3.12`.

---

## Data-Quality Workflow

The main portfolio increment in this repository is the workflow in [`data_quality/`](data_quality/).

It processes the synthetic raw file:

```text
data/raw/training_results.csv
```

Run it from the repository root:

```powershell
python -m data_quality `
  --input "data/raw/training_results.csv" `
  --output ".ci-output/data-quality"
```

Equivalent macOS/Linux command:

```bash
python -m data_quality \
  --input data/raw/training_results.csv \
  --output .ci-output/data-quality
```

The workflow writes:

```text
.ci-output/data-quality/
├── cleaned_results.csv
├── rejected_results.csv
├── module_kpis.csv
└── quality_report.json
```

### Validation rules

Required fields:

```text
result_id
learner_id
module
assessment_date
score
max_score
pass_score
```

Implemented checks include:

- required-column validation
- missing-value detection
- strict ISO date parsing
- numeric conversion
- positive `max_score`
- non-negative score and pass threshold
- score not above maximum
- pass threshold not above maximum
- exact duplicate removal
- conflicting duplicate rejection
- whitespace and identifier normalisation

Invalid rows are not silently dropped. They are exported with explicit pipe-separated rejection reasons.

### Derived fields

Accepted records receive:

- `source_row` for lineage back to the raw CSV
- `score_percentage`
- Boolean `passed`

### KPI output

The workflow aggregates one row per module with:

- result count
- distinct learner count
- average score percentage
- passed count
- failed count
- pass-rate percentage

The committed fixture contains 15 raw rows. The expected control totals are:

```text
accepted rows: 8
rejected rows: 7
exact duplicate rows removed: 1
```

Detailed rules, expected module values and scope boundaries are documented in [`docs/data-quality-workflow.md`](docs/data-quality-workflow.md).

---

## Baseline Entry Point

[`main.py`](main.py) remains a separate deterministic environment and pandas sanity check. It reports the active interpreter and direct runtime package versions, validates a tiny DataFrame and calculates a stable category summary.

This keeps environment verification separate from the larger row-level data-quality workflow.

---

## Additional Example Modules

- [`examples/01_csv_pandas_basics.py`](examples/01_csv_pandas_basics.py) — CSV and grouped pandas operations
- [`examples/02_json_basics.py`](examples/02_json_basics.py) — nested JSON normalisation
- [`examples/03_api_request_basics.py`](examples/03_api_request_basics.py) — public Open-Meteo request without credentials
- [`examples/04_ollama_local_api_basics.py`](examples/04_ollama_local_api_basics.py) — optional localhost-only JSON request
- [`examples/optional/logistic_regression_basics.py`](examples/optional/logistic_regression_basics.py) — bounded scikit-learn API example without a model-quality claim

---

## Notebook Hygiene

[`dataspell_test.ipynb`](dataspell_test.ipynb) verifies core package imports without committing:

- cell outputs
- execution counts
- IDE execution timestamps
- absolute local paths
- incorrect legacy Python metadata

GitHub Actions executes a temporary copy into `.ci-output/` and leaves the committed notebook unchanged.

---

## Dependency Model

`pyproject.toml` is the source of truth.

| Installation | Included scope |
|---|---|
| `python -m pip install -e .` | Runtime baseline and data-quality package |
| `python -m pip install -e ".[notebook]"` | Runtime plus Jupyter |
| `python -m pip install -e ".[ml]"` | Runtime plus optional scikit-learn example |
| `python -m pip install -e ".[dev]"` | Runtime plus pytest and Ruff |
| `python -m pip install -r requirements-dev.txt` | Complete CI-equivalent environment |

The requirement files remain small wrappers rather than machine-specific freezes of every transitive package.

---

## Local Quality Checks

```bash
python -m compileall -q main.py data_quality examples tests
python -m ruff check main.py data_quality examples tests
python -m ruff format --check main.py data_quality examples tests
python -m pytest
python main.py
python -m data_quality --input data/raw/training_results.csv --output .ci-output/data-quality
python examples/optional/logistic_regression_basics.py
```

---

## Continuous Integration

The workflow in [`.github/workflows/python-quality.yml`](.github/workflows/python-quality.yml) runs on:

- Ubuntu 24.04
- Windows 2025
- Python 3.12

Each matrix job:

1. installs the project and optional quality groups
2. compiles Python sources
3. runs Ruff lint and format checks
4. runs pytest
5. executes `main.py`
6. executes the complete data-quality workflow
7. validates the expected row counts
8. executes the optional ML example
9. executes a clean notebook copy
10. uploads short-lived generated workflow outputs and Ruff diagnostics

The workflow is quality assurance, not deployment or release automation.

---

## Repository Structure

```text
python-data-basics/
├── .github/workflows/python-quality.yml
├── data/raw/training_results.csv
├── data_quality/
│   ├── __init__.py
│   ├── __main__.py
│   └── workflow.py
├── docs/
│   ├── api-json-oauth2-notes.md
│   ├── data-quality-workflow.md
│   ├── ollama-local-api-notes.md
│   └── setup.md
├── examples/
├── tests/
│   ├── test_data_quality_workflow.py
│   ├── test_main.py
│   ├── test_notebook_hygiene.py
│   └── test_optional_ml.py
├── dataspell_test.ipynb
├── main.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

---

## Data and Credential Safety

Only synthetic learning data and public endpoints belong in this repository. The committed training-results file contains no real learners or personal information.

Excluded content includes local environments, `.env` files, API keys, OAuth tokens, credential downloads, personal/customer data, IDE metadata, caches and generated workflow outputs.

---

## Current Boundaries

This repository does not claim:

- a production Python package or ETL platform
- streaming or distributed processing
- production orchestration or observability
- regulatory data validation
- a validated predictive model
- a complete business analysis or dashboard
- deployment or cloud infrastructure

The workflow is intentionally small enough to inspect, run, test and explain in an interview or technical review.
