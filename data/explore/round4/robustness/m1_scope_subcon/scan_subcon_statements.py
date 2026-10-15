"""Scan the calls corpus (audit/calls_transcripts.csv, all years) for management statements about
subcontractors: cost, headcount, in-sourcing, rationalisation. Output: subcon_statement_candidates.csv
(one row per matching sentence; screened by hand afterwards). Read-only w.r.t. project data.
    python3 data/explore/round4/robustness/m1_scope_subcon/scan_subcon_statements.py
"""
import csv, re, subprocess, html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
KEY = re.compile(r"(sub-?contract|subcon|contractor|external consultant|third[- ]party (staff|resources)|"
                 r"in-?sourc|insourc|outsourcing cost|freelanc)", re.I)


def pages(path):
    if path.suffix.lower() == ".pdf":
        t = subprocess.run(["pdftotext", str(path), "-"], capture_output=True, text=True).stdout
        return t.split("\f")
    raw = path.read_text(encoding="utf-8", errors="ignore")
    raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</tr>", "\n", raw)
    return [html.unescape(re.sub(r"<[^>]+>", " ", raw)).replace("\xa0", " ")]


rows = []
for r in csv.DictReader(open(ROOT / "audit/calls_transcripts.csv")):
    p = ROOT / r["local_path"]
    if not p.exists():
        continue
    for i, pg in enumerate(pages(p), 1):
        txt = re.sub(r"\s+", " ", pg)
        for s in re.split(r"(?<=[.?!])\s+", txt):
            if KEY.search(s) and 30 < len(s) < 1200:
                rows.append(dict(firm=r["firm"], call=r["call"], call_date=r["call_date"], page=i,
                                 has_number=bool(re.search(r"\d", s)), sentence=s.strip()))
with open(OUT / "subcon_statement_candidates.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["firm", "call", "call_date", "page", "has_number", "sentence"])
    w.writeheader()
    w.writerows(rows)
print(len(rows), "candidate sentences")
