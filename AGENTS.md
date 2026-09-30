# AGENTS.md

Hackerspace Valencia tool inventory: what there is and who has it.
Python 3.12+ with [uv](https://docs.astral.sh/uv/). Data in
`data/inventory.json`.

## Commands

- Install: `uv sync`
- Tests: `uv run pytest`. They must pass before anything counts as done.
- Run: `uv run inventory list` (see `uv run inventory --help`).

## How we work

- Logic goes in `src/inventory/core.py`; the command line, in
  `src/inventory/__main__.py`, with no business logic.
- Every behaviour change comes with its test in `tests/`.
- Don't change a test to make it pass: if a test is wrong, say so and explain why.
- New dependencies only with `uv add`, and ask first.
- Small, focused changes: touch only the files the task asks for.

## Style

- Names and messages in English, like the rest of the code.
- A short docstring when it isn't obvious what a function does.

## Don't

- Don't edit `data/inventory.json` by hand in a code task.
- Don't commit or push: the person decides that.
