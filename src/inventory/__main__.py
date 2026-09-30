"""Usage: uv run inventory <command> ...

Commands:
  list                       every tool
  search <text>              search by name
  lend <id> <member>         lend a tool
  return <id>                return a tool
  add <name> <category>
"""

import argparse
import sys
from pathlib import Path

from . import core

# src/inventory/__main__.py -> repo root
PATH = Path(__file__).resolve().parents[2] / "data" / "inventory.json"


def show(tools):
    for t in tools:
        status = f"lent to {t.lent_to}" if t.lent_to else "available"
        print(f"{t.id:>3}  {t.name:<32} {t.category:<12} {status}")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="inventory", description="Hackerspace Valencia tool inventory")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    p = sub.add_parser("search")
    p.add_argument("text")
    p = sub.add_parser("lend")
    p.add_argument("id", type=int)
    p.add_argument("member")
    p = sub.add_parser("return")
    p.add_argument("id", type=int)
    p = sub.add_parser("add")
    p.add_argument("name")
    p.add_argument("category")
    args = parser.parse_args(argv)

    tools = core.load(PATH)
    try:
        if args.command == "list":
            show(tools)
        elif args.command == "search":
            show(core.search(tools, args.text))
        elif args.command == "lend":
            t = core.lend(tools, args.id, args.member)
            core.save(PATH, tools)
            print(f"{t.name} lent to {t.lent_to}")
        elif args.command == "return":
            t = core.give_back(tools, args.id)
            core.save(PATH, tools)
            print(f"{t.name} returned")
        elif args.command == "add":
            t = core.add(tools, args.name, args.category)
            core.save(PATH, tools)
            print(f"added with id {t.id}")
    except (KeyError, ValueError) as err:
        print(f"error: {err.args[0]}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
