# Cross-platform setup

This project targets Python 3.12 or newer and keeps all dependencies inside a project-specific virtual environment.

`pyproject.toml` is the dependency source of truth. The requirement files are convenience wrappers:

- `requirements.txt` installs the complete local learning environment
- `requirements-dev.txt` additionally installs pytest and Ruff for development and CI parity

## Dependency groups

| Group | Purpose |
|---|---|
| default | pandas, NumPy and matplotlib runtime baseline |
| `notebook` | Jupyter notebook execution |
| `ml` | optional scikit-learn learning example |
| `dev` | pytest and Ruff quality tooling |

## Windows PowerShell

Verify Python 3.12:

```powershell
py -3.12 --version
```

Create and activate the virtual environment:

```powershell
py -3.12 -m venv .venv
& ".\.venv\Scripts\Activate.ps1"
```

Install the complete development environment:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

PowerShell activation is optional. When local policy prevents script activation, use the virtual-environment interpreter directly instead of changing machine-wide policy:

```powershell
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -r requirements-dev.txt
& ".\.venv\Scripts\python.exe" main.py
```

## Windows Command Prompt

Create and activate the virtual environment:

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
```

Install the complete development environment:

```bat
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

## macOS and Linux

Verify that the intended interpreter is available:

```bash
python3.12 --version
command -v python3.12
```

Create and activate the virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

On the Intel iMac used for local portfolio work, the explicit interpreter path is currently:

```bash
/usr/local/bin/python3.12 -m venv .venv
```

Install the complete development environment:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

Do not copy a `.venv` directory between macOS, Linux, Windows, OneDrive locations or different CPU architectures. Recreate it from `pyproject.toml` or the requirement wrapper on each machine.

## Minimal runtime installation

For the baseline script without notebooks, machine learning or quality tools:

```bash
python -m pip install -e .
```

For the complete local learning environment without developer tools:

```bash
python -m pip install -r requirements.txt
```

## Local verification

Run the same core checks used by GitHub Actions:

```bash
python -m compileall -q main.py examples tests
python -m ruff check main.py examples tests
python -m ruff format --check main.py examples tests
python -m pytest
python main.py
python examples/optional/logistic_regression_basics.py
```

Execute the notebook into an ignored temporary directory without modifying the committed source notebook:

```bash
python -c "from pathlib import Path; Path('.ci-output').mkdir(exist_ok=True)"
jupyter nbconvert --to notebook --execute dataspell_test.ipynb --output environment-check.executed.ipynb --output-dir .ci-output --ExecutePreprocessor.timeout=120
```

## IDE interpreter selection

Configure PyCharm, DataSpell, VS Code or Jupyter to use the interpreter inside this repository:

- Windows: `.venv\Scripts\python.exe`
- macOS/Linux: `.venv/bin/python`

Do not select a global interpreter when the repository-specific environment is available.
