"""Print the non-empty cells of an xlsx (all sheets) as tab-separated rows.

Usage: python3 -I dump_xlsx.py FILE [max_rows] [grep_regex]
Reads untrusted downloads with openpyxl (data_only, no macros executed).
"""
import re
import sys

import openpyxl

path = sys.argv[1]
max_rows = int(sys.argv[2]) if len(sys.argv) > 2 else 400
pat = re.compile(sys.argv[3], re.I) if len(sys.argv) > 3 else None

wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
for ws in wb.worksheets:
    print(f"=== sheet: {ws.title}")
    n = 0
    for i, row in enumerate(ws.iter_rows(values_only=True), start=1):
        cells = ["" if v is None else (f"{v:.2f}" if isinstance(v, float) else str(v)) for v in row]
        while cells and cells[-1] == "":
            cells.pop()
        if not any(cells):
            continue
        line = f"{i}\t" + "\t".join(c.replace("\n", " ") for c in cells)
        if pat and not pat.search(line):
            continue
        print(line)
        n += 1
        if n >= max_rows:
            break
