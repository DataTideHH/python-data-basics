# Python Data Basics

A small Python data environment and learning repository for my local developer setup.

This repository verifies that a Python 3.12 data workflow works correctly with a project-specific virtual environment, PyCharm, DataSpell, Jupyter Notebook, pandas, NumPy, matplotlib, scikit-learn, Git, and GitHub.

## Purpose

This is not intended to be a large data science project. It is a compact baseline repository for:

- verifying a clean Python data environment
- practicing Python data analysis fundamentals
- using a project-specific virtual environment
- working with pandas, NumPy, matplotlib, and scikit-learn
- testing PyCharm and DataSpell with the same interpreter
- keeping a clean Git/GitHub workflow for Python projects

Python is one of my core technical skills in my current learning path. My main focus is data and process analysis, SQL, Python, BI, and Microsoft-oriented data tooling.

## Tested Environment

- iMac Retina 4K, 21.5-inch, Late 2015
- Intel x86_64
- macOS Sonoma 14.8.7 via OpenCore Legacy Patcher
- PyCharm via JetBrains Toolbox
- DataSpell via JetBrains Toolbox
- Python 3.12.13
- Project-specific `.venv`
- pandas
- NumPy
- matplotlib
- scikit-learn
- Jupyter Notebook
- Git / GitHub

This repository also documents that the Python data stack works on a legacy Intel Mac setup used as a stable learning and development machine.

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
└── .gitignore
```

Local virtual environments, IDE metadata, cache files, and machine-specific files are intentionally excluded from Git.

```text
.venv/
.idea/
__pycache__/
*.pyc
.DS_Store
```

## Setup

Create the virtual environment with Python 3.12:

```zsh
/usr/local/bin/python3.12 -m venv .venv
```

Activate it:

```zsh
source .venv/bin/activate
```

Install the exact tested dependency set:

```zsh
python -m pip install -r requirements.txt
```

Alternatively, install only the core packages:

```zsh
python -m pip install -r requirements-core.txt
```

## Run the Python Example

Run:

```zsh
python main.py
```

The script verifies the interpreter and package versions, creates a small example DataFrame, and trains a minimal logistic regression model on synthetic learning data.

Expected output includes:

```text
Python data environment check
Python: 3.12.13
pandas
NumPy
matplotlib
scikit-learn
Minimal logistic regression example
```

## DataSpell Notebook

The notebook `dataspell_test.ipynb` verifies that DataSpell uses the same project-specific Python 3.12 virtual environment and can import the core data stack.

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

## Next Steps

Possible future additions:

- a small CSV analysis example
- a simple matplotlib visualization
- a notebook with a short exploratory data analysis workflow
- a basic logistic regression example with clearer explanation
- a small SQL-to-pandas workflow using a local database

## Notes

This repository is intentionally small. Its purpose is to document and verify a clean Python data development setup before building larger data analysis and BI-related projects.

No virtual environment, IDE metadata, cache files, or machine-specific files are committed.
