from inventory import core
from inventory.core import Tool


def test_counts_total_and_available():
    tools = [
        Tool(1, "Soldering station", "electronics"),
        Tool(2, "Multimeter", "electronics", lent_to="ana"),
        Tool(3, "Jigsaw", "woodworking"),
    ]
    assert core.by_category(tools) == {
        "electronics": {"total": 2, "available": 1},
        "woodworking": {"total": 1, "available": 1},
    }


def test_no_tools():
    assert core.by_category([]) == {}
