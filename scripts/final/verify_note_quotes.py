"""Re-verify the note quotes verbatim against the transcript text (whitespace-normalised; '...' = elision).
    python3 scripts/final/verify_note_quotes.py   -> output/final/note_quotes_check.csv"""
import html, re, subprocess
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[2]
IDS = ["DEM-TCS-093", "DEM-Infosys-111", "TCS-15", "TCS-23", "HCLTech-52", "HCLTech-55"]
s = pd.read_csv(ROOT / "audit/calls_statements.csv").set_index("stmt_id")
t = pd.read_csv(ROOT / "audit/calls_transcripts.csv")
norm = lambda x: re.sub(r"\s+", " ", x.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')).strip()

def text_of(path, page):
    p = ROOT / path if not str(path).startswith("/") else Path(path)
    if p.suffix.lower() == ".pdf":
        args = ["pdftotext", "-layout"] + (["-f", str(page), "-l", str(page)] if page else []) + [str(p), "-"]
        return subprocess.run(args, capture_output=True, text=True).stdout
    raw = p.read_text(errors="ignore")
    return html.unescape(re.sub(r"<[^>]+>", " ", raw))

rows = []
for i in IDS:
    r = s.loc[i]
    tr = t[(t.firm == r.firm) & (t.call == r.call)].iloc[0]
    m = re.search(r"p\.(\d+)", str(r.page))
    page = int(m.group(1)) if m else None
    txt = norm(text_of(tr.local_path, page))
    parts = [norm(x) for x in r.quote.split("...") if norm(x)]
    pos, ok = 0, True
    for part in parts:                       # each fragment must appear, in order
        k = txt.find(part, pos)
        if k < 0:
            ok = False; break
        pos = k + len(part)
    rows.append(dict(stmt_id=i, firm=r.firm, call=r.call, call_date=r.call_date, speaker=r.speaker, page=r.page,
                     verbatim_on_page=ok, local_path=tr.local_path, source_url=tr.source_url))
out = pd.DataFrame(rows); out.to_csv(ROOT / "output/final/note_quotes_check.csv", index=False)
print(out[["stmt_id", "call", "page", "verbatim_on_page"]].to_string())
