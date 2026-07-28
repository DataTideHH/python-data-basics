# Python Data Basics

[![Python quality](https://github.com/DataTideHH/python-data-basics/actions/workflows/python-quality.yml/badge.svg)](https://github.com/DataTideHH/python-data-basics/actions/workflows/python-quality.yml)

**Python 3.12 · pandas · NumPy · matplotlib · pytest · Ruff · Jupyter · GitHub Actions**

This repository is a compact, tested foundation for reproducible Python Data/BI workflows. It demonstrates a clean project environment, deterministic tabular transformations, explicit dependency groups, public notebook hygiene and cross-platform quality checks.

It is part of my DataTideHH portfolio during the IHK retraining program in Data and Process Analysis. The scope is deliberately bounded: this is a reusable learning baseline, not a production package, a machine-learning showcase or a substitute for the larger analysis projects in the portfolio.

---

## Project at a Glance

| Area | Current implementation |
|---|---|
| Python baseline | Python 3.12-compatible environment and deterministic pandas sanity check |
| Dependency model | Direct runtime, notebook, optional ML and development groups in `pyproject.toml` |
| Data handling | Small CSV, JSON and public API examples with synthetic or public-safe inputs |
| Testing | pytest coverage for the baseline transformation, notebook hygiene and optional ML example |
| Code quality | Ruff linting and formatting checks plus Python bytecode compilation |
| Notebook hygiene | Cleared outputs, neutral metadata and tests against committed local paths |
| Continuous integration | Matrix workflow for Ubuntu 24.04 and Windows 2025 with Python 3.12 |
| Credential safety | Local environments, tokens, secrets and machine-specific files remain excluded |

## What This Repository Demonstrates

The repository focuses on foundational tasks that recur in Data/BI work:

- create an isolated and reproducible Python environment
- define direct dependencies separately from development tooling
- build and validate small pandas transformations
- parse nested JSON into tabular structures
- call a public API without embedding credentials
- keep notebook outputs and local paths out of version control
- run syntax, lint, formatting and unit checks automatically
- use the same entry points on Windows, macOS, Linux and GitHub-hosted runners

More complete business analyses remain in separate repositories. This project provides the tested building blocks underneath them.

---

## Quick Start

The detailed platform-specific procedure is documented in [`docs/setup.md`](docs/setup.md).

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

On the Intel iMac used for local portfolio work, Python 3.12 is currently available at `/usr/local/bin/python3.12`.

Expected baseline output contains:

- Python implementation and version
- pandas, NumPy and matplotlib versions
- a deterministic two-row category summary
- `Baseline check passed.`

---

## Dependency Model

`pyproject.toml` is the source of truth.

| Installation | Included scope |
|---|---|
| `python -m pip install -e .` | pandas, NumPy and matplotlib runtime baseline |
| `python -m pip install -e ".[notebook]"` | runtime baseline plus Jupyter |
| `python -m pip install -e ".[ml]"` | runtime baseline plus scikit-learn example |
| `python -m pip install -e ".[dev]"` | runtime baseline plus pytest and Ruff |
| `python -m pip install -r requirements.txt` | complete local learning environment |
| `python -m pip install -r requirements-dev.txt` | complete development and CI-equivalent environment |

The requirement files are intentionally small wrappers. They no longer contain a machine-specific freeze of every transitive Jupyter dependency.

---

## Baseline Entry Point

[`main.py`](main.py) performs two bounded checks:

1. reports the active interpreter and direct runtime package versions
2. creates a deterministic DataFrame, validates its required columns and values, and calculates one summary row per category

The script exits with an error when:

- Python is older than 3.12
- a required column is missing
- the value column contains missing values
- the deterministic transformation returns an unexpected shape

This keeps the repository focused on an explainable Data/BI baseline rather than presenting a tiny synthetic model as the primary result.

---

## Example Modules

### CSV and pandas

[`examples/01_csv_pandas_basics.py`](examples/01_csv_pandas_basics.py) demonstrates reading in-memory CSV data, filtering and grouped aggregation.

### JSON normalization

[`examples/02_json_basics.py`](examples/02_json_basics.py) demonstrates nested dictionaries and lists and converts selected values into a tabular DataFrame.

### Public API request

[`examples/03_api_request_basics.py`](examples/03_api_request_basics.py) calls Open-Meteo for Hamburg using the Python standard library. It uses no API key or token and handles common network failures.

### Local Ollama request

[`examples/04_ollama_local_api_basics.py`](examples/04_ollama_local_api_basics.py) remains an optional localhost-only JSON request example. It is not part of the automated CI path because it requires a running local Ollama service and an installed model.

### Optional logistic regression

[`examples/optional/logistic_regression_basics.py`](examples/optional/logistic_regression_basics.py) contains the former `main.py` model example. It now has an explicit optional dependency group and a clear limitation: the tiny synthetic dataset demonstrates scikit-learn API usage only and does not support a model-quality claim.

Run it with:

```bash
python examples/optional/logistic_regression_basics.py
```

---

## Notebook Hygiene

[`dataspell_test.ipynb`](dataspell_test.ipynb) verifies the project interpreter and core package imports without storing machine-specific evidence.

The committed notebook contains:

- no cell outputs
- no execution counts
- no IDE execution timestamps
- no absolute local interpreter path
- Python 3.12 kernel and language metadata

The pytest suite checks these properties. GitHub Actions executes a temporary notebook copy into the ignored `.ci-output/` directory, leaving the committed notebook unchanged.

---

## Local Quality Checks

Run the same core checks used in CI:

```bash
python -m compileall -q main.py examples tests
python -m ruff check main.py examples tests
python -m ruff format --check main.py examples tests
python -m pytest
python main.py
python examples/optional/logistic_regression_basics.py
```

Execute the notebook separately:

```bash
python -c "from pathlib import Path; Path('.ci-output').mkdir(exist_ok=True)"
jupyter nbconvert --to notebook --execute dataspell_test.ipynb --output environment-check.executed.ipynb --output-dir .ci-output --ExecutePreprocessor.timeout=120
```

---

## Continuous Integration

The workflow in [`.github/workflows/python-quality.yml`](.github/workflows/python-quality.yml) uses a Python 3.12 matrix on:

- Ubuntu 24.04
- Windows 2025

Each job:

1. checks out the repository with read-only contents permission and without persisted credentials
2. installs the project and all optional quality groups
3. compiles Python sources
4. runs Ruff linting
5. verifies Ruff formatting
6. runs pytest
7. executes the baseline entry point
8. executes the optional ML example
9. executes the clean notebook into a temporary ignored directory

The workflow is an automated quality check, not a deployment or release pipeline.

---

## Repository Structure

```text
python-data-basics/
├── .github/
│   └── workflows/
│       └── python-quality.yml
├── docs/
│   ├── api-json-oauth2-notes.md
│   ├── ollama-local-api-notes.md
│   └── setup.md
├── examples/
│   ├── __init__.py
│   ├── 01_csv_pandas_basics.py
│   ├── 02_json_basics.py
│   ├── 03_api_request_basics.py
│   ├── 04_ollama_local_api_basics.py
│   └── optional/
│       ├── __init__.py
│       └── logistic_regression_basics.py
├── tests/
│   ├── test_main.py
│   ├── test_notebook_hygiene.py
│   └── test_optional_ml.py
├── dataspell_test.ipynb
├── main.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── .editorconfig
├── .gitignore
├── LICENSE
└── README.md
```

---

## Credentials and Data Safety

Only synthetic learning data and public endpoints belong in this repository.

Excluded content includes:

- `.env` files
- API keys and client secrets
- OAuth access and refresh tokens
- credential downloads
- personal or customer data
- local virtual environments
- IDE metadata and caches
- executed CI notebook copies

OAuth2 remains conceptual documentation only. Any future authenticated example must use placeholders and local configuration rather than committed credentials.

---

## Relationship to Other Portfolio Projects

This repository is the tested Python foundation beneath more specific projects:

- [`open-meteo-germany-weather-ranking`](https://github.com/DataTideHH/open-meteo-germany-weather-ranking) — API-to-CSV scoring workflow
- [`hamburg-district-data-basics`](https://github.com/DataTideHH/hamburg-district-data-basics) — public-data analysis and Power BI preparation
- [`sql-server-docker-basics`](https://github.com/DataTideHH/sql-server-docker-basics) — SQL Server, relational integrity, star schema and CI
- [`flask-country-data-api`](https://github.com/DataTideHH/flask-country-data-api) — validated ingestion, persistence and API delivery

## Current Boundaries

This repository does not claim:

- a production Python package
- a production API client
- a validated predictive model
- a large business analysis
- a finished dashboard
- deployment or cloud infrastructure
- support for copying virtual environments between operating systems

The next useful increment is a small, tested data-quality workflow with explicit raw input, validation rules, cleaned output and KPI aggregation.
