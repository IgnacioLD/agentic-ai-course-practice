from inventory import core
from inventory.core import Tool


def test_search_ignores_extra_spaces():
    tools = [Tool(1, "Soldering station Hakko FX-888D", "electronics")]
    assert [t.id for t in core.search(tools, " soldering ")] == [1]
