"""MCP server tests, connecting a real MCP client in memory."""

import pytest
from mcp import Client

from inventory.mcp_server import server


@pytest.fixture
def anyio_backend():
    return "asyncio"


async def call(name: str, arguments: dict | None = None) -> list[dict]:
    async with Client(server) as client:
        result = await client.call_tool(name, arguments or {})
    assert not result.is_error
    return result.structured_content["result"]


@pytest.mark.anyio
async def test_read_only_tools():
    async with Client(server) as client:
        tools = (await client.list_tools()).tools
    assert {t.name for t in tools} == {"list_all", "search", "available"}
    assert all(t.annotations.read_only_hint for t in tools)


@pytest.mark.anyio
async def test_search():
    assert [t["id"] for t in await call("search", {"text": "soldering"})] == [1]


@pytest.mark.anyio
async def test_available_excludes_lent_tools():
    available = await call("available")
    assert available
    assert all(t["lent_to"] is None for t in available)
