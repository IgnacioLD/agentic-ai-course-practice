"""Command-line tests, against a copy of the data."""

import shutil
from pathlib import Path

import pytest

from inventory import __main__ as cli

DATA = Path(__file__).resolve().parents[1] / "data" / "inventory.json"


@pytest.fixture
def inventory(tmp_path, monkeypatch, capsys):
    path = tmp_path / "inventory.json"
    shutil.copy(DATA, path)
    monkeypatch.setattr(cli, "PATH", path)

    def run(*args):
        code = cli.main(list(args))
        output = capsys.readouterr()
        return code, output.out, output.err

    return run


def test_list(inventory):
    code, output, _ = inventory("list")
    assert code == 0
    assert "Soldering" in output


def test_lend_and_return_are_saved(inventory):
    inventory("lend", "4", "ana")
    assert "lent to ana" in inventory("list")[1]
    inventory("return", "4")
    assert "lent to ana" not in inventory("list")[1]


def test_lending_twice_is_an_error(inventory):
    code, _, errors = inventory("lend", "3", "ana")  # marta already has number 3
    assert code == 1
    assert "already lent" in errors
