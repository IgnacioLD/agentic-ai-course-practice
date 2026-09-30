"""Agent tests with a fake client: they don't call any model or spend credit.
When they all pass, your loop works: `uv run pytest agent`."""

import copy
import json
from types import SimpleNamespace

from openai.types.chat import ChatCompletion

from agent import agent as ag


def response(message: dict) -> ChatCompletion:
    return ChatCompletion.model_validate({
        "id": "fake",
        "object": "chat.completion",
        "created": 0,
        "model": "fake",
        "choices": [{"index": 0, "finish_reason": "stop", "message": {"role": "assistant", **message}}],
    })


def text(content: str) -> ChatCompletion:
    return response({"content": content})


def asks(name: str, arguments: dict, id: str = "call_1") -> ChatCompletion:
    return response({
        "content": None,
        "tool_calls": [{"id": id, "type": "function", "function": {"name": name, "arguments": json.dumps(arguments)}}],
    })


class FakeClient:
    """Imitates client.chat.completions.create and keeps what it gets sent."""

    def __init__(self, *responses):
        self.responses = list(responses)
        self.requests = []
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self.create))

    def create(self, **request):
        self.requests.append(copy.deepcopy(request["messages"]))
        return self.responses.pop(0) if len(self.responses) > 1 else self.responses[0]


def test_answers_without_tools():
    client = FakeClient(text("It's an inventory."))
    assert ag.agent("what is this?", client) == "It's an inventory."
    assert len(client.requests) == 1


def test_runs_the_tool_and_returns_the_result():
    client = FakeClient(asks("read_file", {"path": "pyproject.toml"}), text("Done."))
    assert ag.agent("read the pyproject", client) == "Done."
    result = client.requests[1][-1]
    assert result["role"] == "tool"
    assert result["tool_call_id"] == "call_1"
    assert 'name = "inventory"' in result["content"]


def test_the_conversation_grows_every_turn():
    client = FakeClient(asks("read_file", {"path": "pyproject.toml"}), text("Done."))
    ag.agent("read the pyproject", client)
    first, second = client.requests
    # The second call carries everything before plus the model's request and the result.
    assert second[: len(first)] == first
    assert len(second) == len(first) + 2


def test_stops_at_the_turn_limit():
    client = FakeClient(asks("read_file", {"path": "pyproject.toml"}))  # never finishes
    final = ag.agent("never stop", client)
    assert len(client.requests) == ag.MAX_TURNS
    assert "limit" in final


def test_a_tool_error_goes_back_to_the_model():
    client = FakeClient(asks("read_file", {"path": "does-not-exist.txt"}), text("It's not there."))
    assert ag.agent("read a file that doesn't exist", client) == "It's not there."
    assert client.requests[1][-1]["content"].startswith("Error:")


def test_does_not_read_outside_the_project():
    assert ag.read_file("../../../../etc/hosts").startswith("Error:")


def test_asks_permission_before_running(monkeypatch, tmp_path):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    marker = tmp_path / "ran"
    assert "did not allow" in ag.run(f"touch {marker}")
    assert not marker.exists()
