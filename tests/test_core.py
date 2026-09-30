import pytest

from inventory import core
from inventory.core import Tool


@pytest.fixture
def tools():
    return [
        Tool(1, "Soldering station Hakko FX-888D", "electronics"),
        Tool(2, "Hot-air rework station", "electronics"),
        Tool(3, "Jigsaw", "woodworking", lent_to="jorge"),
    ]


def ids(items):
    return [t.id for t in items]


def test_searches_by_part_of_the_name(tools):
    assert ids(core.search(tools, "Hakko")) == [1]


def test_ignores_case(tools):
    # Nobody types "Soldering" with a capital when searching.
    assert ids(core.search(tools, "soldering")) == [1]


def test_ignores_hyphens(tools):
    # Nor remembers whether "hot air" has a hyphen.
    assert ids(core.search(tools, "hot air")) == [2]


def test_lend_and_return(tools):
    core.lend(tools, 1, "ana")
    assert core.get(tools, 1).lent_to == "ana"
    core.give_back(tools, 1)
    assert core.get(tools, 1).lent_to is None


def test_cannot_lend_twice(tools):
    with pytest.raises(ValueError):
        core.lend(tools, 3, "ana")


def test_available(tools):
    assert ids(core.available(tools)) == [1, 2]


def test_add_uses_the_next_id(tools):
    assert core.add(tools, "Sander", "woodworking").id == 4
