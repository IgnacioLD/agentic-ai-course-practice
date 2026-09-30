"""Judge for the session 2 eval: checks the task in evals/task.md.

    uv run pytest evals
"""

import json
import shutil
from pathlib import Path

from inventory import __main__ as cli

DATA = Path(__file__).resolve().parents[1] / "data" / "inventory.json"


def test_available_lists_only_what_is_not_lent_out(tmp_path, monkeypatch, capsys):
    path = tmp_path / "inventory.json"
    shutil.copy(DATA, path)
    monkeypatch.setattr(cli, "PATH", path)

    assert cli.main(["available"]) == 0
    output = capsys.readouterr().out

    tools = json.loads(DATA.read_text(encoding="utf-8"))
    for t in tools:
        if t["lent_to"] is None:
            assert t["name"] in output
        else:
            assert t["name"] not in output
    assert len(output.strip().splitlines()) == sum(t["lent_to"] is None for t in tools)
