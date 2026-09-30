Add an `available` command to the inventory command line that lists the tools
that aren't lent out, in the same format as `list`. The logic already exists
in `core.available`. Don't change the existing tests.
Done: `uv run pytest` green.
