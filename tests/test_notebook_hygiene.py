from __future__ import annotations

import json
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATHS = [
    REPOSITORY_ROOT / "dataspell_test.ipynb",
    REPOSITORY_ROOT / "notebooks" / "reporting_verification.ipynb",
]


def load_notebook(notebook_path: Path) -> dict[str, object]:
    return json.loads(notebook_path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("notebook_path", NOTEBOOK_PATHS)
def test_notebook_has_no_stored_execution_output(notebook_path: Path) -> None:
    notebook = load_notebook(notebook_path)

    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            assert cell["execution_count"] is None
            assert cell["outputs"] == []
            assert "ExecuteTime" not in cell.get("metadata", {})


@pytest.mark.parametrize("notebook_path", NOTEBOOK_PATHS)
def test_notebook_uses_python_3_12_metadata(notebook_path: Path) -> None:
    notebook = load_notebook(notebook_path)
    metadata = notebook["metadata"]

    assert metadata["kernelspec"]["display_name"] == "Python 3.12"
    assert metadata["kernelspec"]["name"] == "python3"
    assert metadata["language_info"]["version"] == "3.12"
    assert metadata["language_info"]["pygments_lexer"] == "ipython3"


@pytest.mark.parametrize("notebook_path", NOTEBOOK_PATHS)
def test_notebook_contains_no_local_absolute_paths(notebook_path: Path) -> None:
    serialized = notebook_path.read_text(encoding="utf-8")

    assert "/Users/" not in serialized
    assert "C:\\Users\\" not in serialized


def test_reporting_notebook_contains_explicit_verification_marker() -> None:
    reporting_notebook = NOTEBOOK_PATHS[1].read_text(encoding="utf-8")

    assert "Reporting notebook verification passed." in reporting_notebook
    assert "reconcile_module_kpis" in reporting_notebook
    assert ".ci-output/data-quality" in reporting_notebook
