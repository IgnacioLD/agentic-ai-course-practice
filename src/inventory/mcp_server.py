"""Inventory MCP server: any compatible agent (opencode, Claude Code, Codex,
Cursor...) can query the inventory with these tools.

It runs over stdio: the agent launches it and talks to it through standard
input and output. To try it by hand, with the official inspector:
    npx @modelcontextprotocol/inspector uv run inventory-mcp
"""

from dataclasses import asdict

from mcp.server import MCPServer
from mcp.types import ToolAnnotations

from . import core
from .__main__ import PATH

server = MCPServer(
    "inventory",
    instructions="Hackerspace Valencia tool inventory: what there is and who has it.",
)

READ_ONLY = ToolAnnotations(readOnlyHint=True)


@server.tool(annotations=READ_ONLY)
def list_all() -> list[dict]:
    """Every tool in the inventory, with who has each one."""
    return [asdict(t) for t in core.load(PATH)]


@server.tool(annotations=READ_ONLY)
def search(text: str) -> list[dict]:
    """Tools whose name contains `text`, ignoring case and hyphens. Use it
    before `list_all` when you're looking for something specific."""
    return [asdict(t) for t in core.search(core.load(PATH), text)]


@server.tool(annotations=READ_ONLY)
def available() -> list[dict]:
    """Tools that aren't lent out right now."""
    return [asdict(t) for t in core.available(core.load(PATH))]


def main() -> None:
    server.run()
