import csv
import io

from inventory.core import Tool
from inventory.export import to_csv


def rows(text: str) -> list[list[str]]:
    return list(csv.reader(io.StringIO(text)))


def test_header_and_rows():
    text = to_csv([Tool(1, "Soldering station, large", "electronics", lent_to="ana")])
    assert rows(text)[0] == ["id", "name", "category", "lent_to"]
    # The comma in the name doesn't break the CSV.
    assert rows(text)[1] == ["1", "Soldering station, large", "electronics", "ana"]


def test_available_is_empty():
    assert rows(to_csv([Tool(2, "Jigsaw", "woodworking")]))[1][3] == ""


def test_export_command(capsys):
    from inventory import __main__ as cli

    assert cli.main(["export"]) == 0
    assert capsys.readouterr().out.startswith("id,name,category,lent_to")
