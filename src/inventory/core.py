"""Inventory logic: load, search, lend and return tools."""

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Tool:
    id: int
    name: str
    category: str
    lent_to: str | None = None


def load(path: Path) -> list[Tool]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [Tool(**t) for t in data]


def save(path: Path, tools: list[Tool]) -> None:
    text = json.dumps([asdict(t) for t in tools], ensure_ascii=False, indent=2)
    Path(path).write_text(text + "\n", encoding="utf-8")


def add(tools: list[Tool], name: str, category: str) -> Tool:
    new_id = max((t.id for t in tools), default=0) + 1
    tool = Tool(id=new_id, name=name, category=category)
    tools.append(tool)
    return tool


def _normalise(text: str) -> str:
    """Lowercase and hyphens as spaces, to compare the way a person would."""
    return text.replace("-", " ").casefold()


def search(tools: list[Tool], text: str) -> list[Tool]:
    """Tools whose name contains `text`, ignoring case and hyphens."""
    wanted = _normalise(text.strip())  # issue 42: extra spaces when copying and pasting
    return [t for t in tools if wanted in _normalise(t.name)]


def get(tools: list[Tool], id: int) -> Tool:
    for t in tools:
        if t.id == id:
            return t
    raise KeyError(f"there is no tool {id}")


def lend(tools: list[Tool], id: int, member: str) -> Tool:
    tool = get(tools, id)
    if tool.lent_to:
        raise ValueError(f"{tool.name} is already lent to {tool.lent_to}")
    tool.lent_to = member
    return tool


def give_back(tools: list[Tool], id: int) -> Tool:
    tool = get(tools, id)
    tool.lent_to = None
    return tool


def available(tools: list[Tool]) -> list[Tool]:
    return [t for t in tools if t.lent_to is None]


def by_category(tools: list[Tool]) -> dict[str, dict[str, int]]:
    """Per category, how many there are and how many are available, sorted by name."""
    summary: dict[str, dict[str, int]] = {}
    for t in sorted(tools, key=lambda t: t.category):
        count = summary.setdefault(t.category, {"total": 0, "available": 0})
        count["total"] += 1
        count["available"] += t.lent_to is None
    return summary
