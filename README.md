# Python Data Basics

**Python 3.12 data environment · pandas · NumPy · matplotlib · scikit-learn · Jupyter · JSON · API basics · OAuth2 notes · optional Ollama local API**

This repository documents a working Python 3.12 data environment and selected Python fundamentals for Data/BI work.

It is part of my broader **DataTideHH portfolio** and supports my learning path toward **Data/BI Analyst** roles with a focus on Python, pandas, SQL, Power BI, Microsoft Fabric/Azure fundamentals, API data workflows and reproducible analysis.

The purpose is not to collect random scripts. This repository is intended as a small, understandable foundation for learning and documenting practical Python data workflows before building larger analysis and BI-related projects.

---

## Why This Repository Matters for Data/BI

Many Data/BI workflows start with basic Python tasks:

- read structured data
- inspect and clean tabular data
- work with CSV files
- understand JSON responses
- request data from APIs
- transform nested data into tables
- document assumptions and limitations
- keep credentials and tokens out of Git
- prepare clean outputs for reporting or further analysis

This repository is the technical foundation for those skills. More complete project work is documented in separate repositories such as API-based analysis projects, public-data analysis projects and SQL/database projects.

---

## Current Scope

This repository currently focuses on:

- Python 3.12 environment setup
- project-specific virtual environment usage
- PyCharm and DataSpell workflow
- pandas, NumPy, matplotlib and scikit-learn basics
- Jupyter Notebook / DataSpell validation
- a minimal logistic regression example in `main.py`
- CSV and DataFrame basics
- JSON parsing basics
- basic public API request workflow
- OAuth2 concept notes
- optional local Ollama API example
- reproducible and safe learning examples

It is deliberately small. The goal is to keep the basics understandable and reusable.

---

## Tested Environment

This repository has been tested on the following local setup:

| Area | Tested setup |
|---|---|
| Device | iMac Retina 4K, 21.5-inch, Late 2015 |
| Architecture | Intel x86_64 |
| Operating system | macOS Sonoma 14.8.7 via OpenCore Legacy Patcher |
| Python IDE | PyCharm via JetBrains Toolbox |
| Notebook IDE | DataSpell via JetBrains Toolbox |
| Python version | Python 3.12.13 |
| Environment | Project-specific `.venv` |
| Core packages | pandas, NumPy, matplotlib, scikit-learn |
| Notebook stack | Jupyter Notebook |
| Version control | Git / GitHub |

This repository also documents that the Python data stack works on a legacy Intel Mac setup used as a stable learning and development machine.

---

## Setup

Create the virtual environment with Python 3.12:

```bash
/usr/local/bin/python3.12 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install the exact tested dependency set:

```bash
python -m pip install -r requirements.txt
```

Alternatively, install only the core packages:

```bash
python -m pip install -r requirements-core.txt
```

---

## Run the Python Baseline Example

Run:

```bash
python main.py
```

The script verifies the interpreter and package versions, creates a small example DataFrame and trains a minimal logistic regression model on synthetic learning data.

Expected output includes:

- Python data environment check
- Python version
- pandas version
- NumPy version
- matplotlib availability
- scikit-learn version
- minimal logistic regression example

The exact package versions may differ on other machines if the environment is recreated with a different dependency set.

---

## DataSpell Notebook

The notebook

```text
dataspell_test.ipynb
```

verifies that DataSpell uses the same project-specific Python 3.12 virtual environment and can import the core data stack.

This is useful because notebook environments can easily point to a different interpreter than the main project. The notebook documents that the local DataSpell setup is aligned with the repository environment.

---

## Planned Learning Modules

| Module | Status | Purpose |
|---|---|---|
| CSV / pandas basics | Added as example | Read small structured data and work with DataFrames |
| JSON basics | Added as example | Understand nested API-like data structures |
| API request basics | Added as example | Fetch public API data without credentials |
| OAuth2 concept notes | Added as documentation | Understand tokens, scopes and safe credential handling |
| Local Ollama API example | Added as optional example | Practice JSON request/response patterns against a local API |
| Data cleaning basics | Planned | Handle missing values, types and simple validation |
| Basic visualizations | Planned | Create simple charts for analysis and reporting |
| SQL-to-pandas workflow | Planned | Read database query results into pandas |
| Notebook workflow | Planned | Use notebooks for documented analysis steps |

---

## Repository Structure

```text
python-data-basics/
├── main.py
├── dataspell_test.ipynb
├── README.md
├── requirements.txt
├── requirements-core.txt
├── LICENSE
├── .editorconfig
├── .gitignore
├── examples/
│   ├── 01_csv_pandas_basics.py
│   ├── 02_json_basics.py
│   ├── 03_api_request_basics.py
│   └── 04_ollama_local_api_basics.py
└── docs/
    ├── api-json-oauth2-notes.md
    └── ollama-local-api-notes.md
```

Local virtual environments, IDE metadata, cache files, token files and machine-specific files are intentionally excluded from Git.

Examples:

```text
.venv/
.idea/
__pycache__/
*.pyc
.DS_Store
.env
*.env
credentials.json
token.json
access_token
refresh_token
```

---

## Example Modules

### CSV / pandas basics

```text
examples/01_csv_pandas_basics.py
```

Demonstrates a small CSV-like dataset, loads it into pandas and calculates simple grouped results.

### JSON basics

```text
examples/02_json_basics.py
```

Demonstrates JSON parsing, nested dictionaries/lists and basic normalization into tabular data.

### API request basics

```text
examples/03_api_request_basics.py
```

Demonstrates a public API request using Python standard-library tools. It uses a public endpoint and does not require credentials.

### OAuth2 concept notes

```text
docs/api-json-oauth2-notes.md
```

Explains API basics, JSON basics and OAuth2 concepts such as access tokens, refresh tokens, scopes, client IDs and client secrets.

### Optional Ollama local API example

```text
examples/04_ollama_local_api_basics.py
```

Demonstrates a local JSON request/response workflow against an Ollama server on `localhost`.

This example is optional. It only works if Ollama is installed, running locally and a model is available.

---

## Credentials, Tokens and Secrets

This repository must not contain real credentials, tokens or secrets.

Do not commit:

- API keys
- OAuth2 access tokens
- OAuth2 refresh tokens
- client secrets
- private `.env` files
- downloaded credential files
- personal data
- customer data

If an example ever needs configuration, use documented placeholders or an `.env.example` file, not real secrets.

OAuth2 is currently documented conceptually only. This is intentional.

---

## What This Demonstrates

This repository demonstrates a working Python data baseline setup using:

- Python 3.12
- a project-specific virtual environment
- pandas for tabular data handling
- NumPy for numerical work
- matplotlib availability for visualization
- scikit-learn for a minimal machine learning example
- Jupyter Notebook / DataSpell for notebook-based work
- PyCharm as the primary Python IDE
- Git and GitHub for version control
- JSON parsing basics
- public API request basics
- safe handling of OAuth2 concepts without committing secrets
- optional local API interaction through Ollama

---

## Relationship to Other Portfolio Projects

This repository is a foundation repository.

More complete project examples are documented separately:

- `open-meteo-germany-weather-ranking` for an API-to-CSV scoring workflow
- `hamburg-district-data-basics` for public-data analysis and Power BI preparation
- `sql-server-docker-basics` for SQL Server and Data/BI database practice

---

## Notes and Limitations

This repository is intentionally small.

It is not intended to be a production application, a package or a complete API client library. The examples are intentionally small, readable and safe to run locally.

The focus is on understanding basic building blocks that can later be used in practical Data/BI projects.

No virtual environment, IDE metadata, cache files, token files, credentials or machine-specific files are committed.
