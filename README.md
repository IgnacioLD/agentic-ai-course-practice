# Hackerspace inventory

Practice repo for the agentic AI course for Hackerspace Valencia members, in
English. It's a minimal tool inventory manager: what there is and who has it.

The course is taught in Spanish with
[taller-ia-agentica-practicas](https://github.com/IgnacioLD/taller-ia-agentica-practicas);
this repo has the same exercises with English code, so you can follow the
English slides on your own laptop.

## Getting started

You need [uv](https://docs.astral.sh/uv/getting-started/installation/), which
installs whatever Python is needed.

```sh
uv sync                          # installs Python and the dependencies
uv run inventory list
uv run inventory search soldering
uv run pytest                    # inventory tests
cp .env.example .env             # local configuration
```

## What's here

| Folder | What it is | Session |
| --- | --- | --- |
| `src/inventory/` | The inventory: logic (`core.py`) and command line | 1 |
| `tests/` | Tests with pytest. On `main`, 2 fail on purpose | 1 |
| `agent/` | Your own agent: you write the loop | 2 |
| `src/inventory/mcp_server.py` | Inventory MCP server | 2 |
| `issues/` | The project's open issues | 2 |
| `scripts/` | Project utilities | 2 |
| `templates/` | `AGENTS.md`, agent diary and your final project sheet | 2 |
| `.devcontainer/` | Sandbox: the agent inside a container that only sees this repo | 2 |

## Your agent (session 2)

`agent/agent.py` talks to OpenRouter with the OpenAI SDK. The tools and the
model call are already there; the loop isn't. Its tests use a fake client and
spend no credit: when they pass, your loop works.

```sh
uv run pytest agent
export OPENROUTER_API_KEY=sk-or-...   # your course key
uv run agent/agent.py "explain what this project does"
```

## Solutions

Every exercise has its solution on a `solution/sN-M` branch (session N,
exercise M). They're cumulative: each one includes the previous ones. If you
fall behind:

```sh
git switch solution/s1-2
```
