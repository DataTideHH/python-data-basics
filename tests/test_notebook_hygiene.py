from __future__ import annotations

import json
from pathlib import Path

NOTEBOOK_PATH = Path(__file__).resolve().parents[1] / "dataspell_test.ipynb"


def load_notebook() -> dict[str, object]:
    return json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))


def test_notebook_has_no_stored_execution_output() -> None:
    notebook = load_notebook()

    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            assert cell["execution_count"] is None
            assert cell["outputs"] == []
            assert "ExecuteTime" not in cell.get("metadata", {})


def test_notebook_uses_python_3_12_metadata() -> None:
    notebook = load_notebook()
    metadata = notebook["metadata"]

    assert metadata["kernelspec"]["display_name"] == "Python 3.12"
    assert metadata["kernelspec"]["name"] == "python3"
    assert metadata["language_info"]["version"] == "3.12"
    assert metadata["language_info"]["pygments_lexer"] == "ipython3"


def test_notebook_contains_no_local_absolute_paths() -> None:
    serialized = NOTEBOOK_PATH.read_text(encoding="utf-8")

    assert "/Users/" not in serialized
    assert "C:\\Users\\" not in serialized
