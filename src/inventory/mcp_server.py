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


# EXERCISE: add two more tools, read-only like `list_all`:
#   - search(text): the tools whose name contains `text`.
#   - available(): the ones that aren't lent out.
# The docstring is what the model reads to decide when to use each one:
# write it with the model in mind.


def main() -> None:
    server.run()
