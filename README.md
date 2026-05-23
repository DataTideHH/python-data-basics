# Python Data Basics

Small Python data environment test project for my Fachinformatiker Daten- und Prozessanalyse setup.

## Environment

- macOS Sonoma on Intel iMac
- Python 3.12 virtual environment
- PyCharm
- DataSpell
- Jupyter Notebook
- pandas
- numpy
- matplotlib
- scikit-learn

## Purpose

This repository verifies that my local Python data stack works correctly with a project-specific virtual environment and can be used from PyCharm, DataSpell, Git, and GitHub.

## Setup

Create and activate the virtual environment:

    /usr/local/bin/python3.12 -m venv .venv
    source .venv/bin/activate

Install dependencies:

    python -m pip install -r requirements.txt

Run the Python test:

    python main.py

Open the notebook:

    dataspell_test.ipynb

## Notes

The .venv directory is intentionally excluded from Git. Dependencies are documented in requirements.txt.
