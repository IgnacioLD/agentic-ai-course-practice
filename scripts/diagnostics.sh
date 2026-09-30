#!/bin/sh
# Standard diagnostics for issues: project versions and configuration.
echo "## Diagnostics $(date +%F)"
echo "- uv: $(uv --version)"
echo "- python: $(uv run python --version)"
echo "- tests: $(uv run pytest -q 2>&1 | tail -1)"
echo "## Configuration"
for f in pyproject.toml .python-version .env; do
  [ -f "$f" ] && { echo "### $f"; cat "$f"; }
done
