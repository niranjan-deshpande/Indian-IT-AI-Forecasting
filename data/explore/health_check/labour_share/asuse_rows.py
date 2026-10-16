"""Print rows for one activity code from ASUSE report text (pdftotext -layout output),
tagged with the most recent 'Table N:' heading and 'Sec:'/'Est.:' markers seen above them.

Usage: python3 -I asuse_rows.py TEXTFILE CODE TABLE_REGEX
  e.g. python3 -I asuse_rows.py ASUSE_2023_24.txt S7 '^Table (31|33|35|37):'
Reads untrusted text only; nothing is executed from it.
"""
import re
import sys

path, code, table_re = sys.argv[1], sys.argv[2], re.compile(sys.argv[3])
row_re = re.compile(r"^\s*" + re.escape(code) + r"\s")
table = sec = est = None
with open(path, encoding="utf-8", errors="ignore") as fh:
    for i, line in enumerate(fh, start=1):
        s = line.strip()
        m = re.match(r"^(Table\s+\d+[A-Za-z]?)\s*:", s)
        if m:
            table = s[:110] if table_re.search(s) else None
            continue
        if table is None:
            continue
        ms = re.search(r"Sec\.?\s*:\s*(\w+)", line)
        if ms:
            sec = ms.group(1)
        me = re.search(r"Est\.?\s*:\s*(\w+)", line)
        if me:
            est = me.group(1)
        if row_re.match(line):
            print(f"{i}\t{table}\tSec={sec}\tEst={est}\t{' '.join(s.split())}")
