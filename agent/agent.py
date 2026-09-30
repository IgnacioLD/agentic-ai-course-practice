"""A minimal agent: a loop, two tools and limits.

Usage:
    export OPENROUTER_API_KEY=sk-or-...   # your course key
    uv run agent/agent.py "explain what this project does"

It talks to OpenRouter through the OpenAI SDK: the OpenAI chat API is the de
facto standard and almost every provider accepts it. Change the model with
the MODEL environment variable.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

from openai import OpenAI

MODEL = os.environ.get("MODEL", "~deepseek/deepseek-flash-latest")
MAX_TURNS = 15
MAX_OUTPUT = 20_000  # characters: what a tool returns also takes up context
ROOT = Path.cwd().resolve()

SYSTEM = """You are a coding agent working in the current repository.
Before answering, look at the files you need with your tools.
When you change code, run the tests to check it.
When you are done, reply with a short summary of what you did."""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads a text file from the project and returns its content.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string", "description": "Path relative to the project"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run",
            "description": (
                "Runs a shell command in the project and returns its output. "
                "Use it to list files, run tests or modify files."
            ),
            "parameters": {
                "type": "object",
                "properties": {"command": {"type": "string", "description": "Shell command"}},
                "required": ["command"],
            },
        },
    },
]


# --- Tools: YOUR program runs them, not the model -------------------------------


def read_file(path: str) -> str:
    file = (ROOT / path).resolve()
    if not file.is_relative_to(ROOT):
        return "Error: you can only read files inside the project."
    return file.read_text(encoding="utf-8")[:MAX_OUTPUT]


def run(command: str) -> str:
    # The model proposes; you decide. Without this, any text the agent reads
    # (an issue, a web page) could end up running on your machine.
    if input(f"\nRun `{command}`? [y/N] ").strip().lower() != "y":
        return "The user did not allow running that command."
    r = subprocess.run(command, shell=True, cwd=ROOT, capture_output=True, text=True, timeout=120)
    output = (r.stdout + r.stderr)[-MAX_OUTPUT:]
    return output or f"(no output, exit code {r.returncode})"


FUNCTIONS = {"read_file": read_file, "run": run}


def run_tool(call) -> str:
    """Runs one of the model's tool calls. Errors are returned to it as text
    too: they are information it can use to correct itself."""
    try:
        arguments = json.loads(call.function.arguments or "{}")
        print(f"  -> {call.function.name}({arguments})", file=sys.stderr)
        return FUNCTIONS[call.function.name](**arguments)
    except Exception as error:
        return f"Error: {error}"


# --- The model ------------------------------------------------------------------


def call_model(client: OpenAI, messages: list, model: str, turn: int):
    """One model call with the whole conversation. Shows tokens and cost."""
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=TOOLS,
        extra_body={"usage": {"include": True}},  # OpenRouter returns the cost
    )
    usage = response.usage
    if usage:
        cost = getattr(usage, "cost", None)
        print(
            f"[turn {turn}] input {usage.prompt_tokens} tokens, output {usage.completion_tokens}"
            + (f", ${cost:.5f}" if cost is not None else ""),
            file=sys.stderr,
        )
    return response


# --- The loop ---------------------------------------------------------------------


def agent(task: str, client: OpenAI, model: str = MODEL) -> str:
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": task}]

    # EXERCISE: write the agent loop (about 10 lines).
    # On each turn, at most MAX_TURNS:
    #   1. Call the model: call_model(client, messages, model, turn).
    #      Its message is in response.choices[0].message.
    #   2. Append it to `messages` with message.model_dump(exclude_none=True):
    #      the conversation grows every turn.
    #   3. If it doesn't ask for tools (message.tool_calls is empty), it's
    #      done: return message.content.
    #   4. If it does, run each call with run_tool(call) and append the result
    #      to `messages`:
    #      {"role": "tool", "tool_call_id": call.id, "content": result}
    # If it runs out of turns, return a warning that it didn't finish.
    raise NotImplementedError("write the agent loop")


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit('Usage: uv run agent/agent.py "your task"')
    if not os.environ.get("OPENROUTER_API_KEY"):
        sys.exit("Missing OPENROUTER_API_KEY: export OPENROUTER_API_KEY=sk-or-...")
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"])
    print(agent(" ".join(sys.argv[1:]), client))


if __name__ == "__main__":
    main()
