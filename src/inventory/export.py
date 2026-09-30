"""Export the inventory to CSV, to open it in a spreadsheet."""

import csv
import io

from .core import Tool

COLUMNS = ["id", "name", "category", "lent_to"]


def to_csv(tools: list[Tool]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(COLUMNS)
    for t in tools:
        writer.writerow([t.id, t.name, t.category, t.lent_to or ""])
    return output.getvalue()
