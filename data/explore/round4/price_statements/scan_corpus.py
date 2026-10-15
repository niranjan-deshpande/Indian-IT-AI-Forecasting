"""M2 corpus scan: find quantitative sentences about price / deal-value / productivity give-backs
in the 2023-01..2026-10 transcripts of the calls corpus (audit/calls_transcripts.csv).

Output: scan_candidates.csv (one row per candidate sentence, with page and a flag for whether the
sentence overlaps a statement already in audit/price_calls_quotes.csv). Candidates are screened by
hand afterwards; the screened, classified statements live in m2_statements.csv.
Read-only with respect to project data.
"""
import csv, os, re, subprocess, html, sys

ROOT = "/Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/0. Exploratory Analysis"
OUT = f"{ROOT}/data/explore/round4/price_statements"

NUM = re.compile(r"(\d+(\.\d+)?\s*(%|percent|per cent|basis points|bps)|\$\s?\d|\d+\s*(million|billion)|one[- ]third|half|two[- ]thirds|double)", re.I)
KEY = re.compile(r"(productivity|deflation|deflationary|pass(ed|ing)? (on|back|through)|give[sn]? back|giving back|"
                 r"renewal|renew|like[- ]for[- ]like|same scope|same work|TCV|ACV|pric(e|ing)|discount|"
                 r"commitment|cheaper|cannibali[sz]|compress|savings? (to|for) (the )?client|lower cost|less effort|effort reduction)", re.I)
AI = re.compile(r"(\bAI\b|GenAI|gen AI|generative|agentic|automation|copilot|AI-led|AI led|technology)", re.I)


def pages(path, kind):
    if kind == "pdf":
        t = subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True).stdout
        return t.split("\f")
    raw = open(path, encoding="utf-8", errors="ignore").read()
    raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</tr>", "\n", raw)
    return [html.unescape(re.sub(r"<[^>]+>", " ", raw)).replace("\xa0", " ")]


def norm(s):
    return re.sub(r"\s+", " ", s.replace("’", "'").replace("ﬁ", "fi").replace("ﬂ", "fl")).strip().lower()


def main():
    known = [norm(r["quote"]) for r in csv.DictReader(open(f"{ROOT}/audit/price_calls_quotes.csv"))]
    known_frag = set()
    for k in known:
        for part in k.split("..."):
            part = part.strip()
            if len(part) > 40:
                known_frag.add(part[:60])
    rows = []
    for r in csv.DictReader(open(f"{ROOT}/audit/calls_transcripts.csv")):
        if r["call_date"] < "2023-01-01":
            continue
        p = f"{ROOT}/{r['local_path']}"
        kind = "html" if p.endswith(".htm") else "pdf"
        for i, pg in enumerate(pages(p, kind), 1):
            text = re.sub(r"\s+", " ", pg)
            for s in re.split(r"(?<=[.?!])\s+(?=[A-Z])", text):
                if len(s) < 30 or len(s) > 900:
                    continue
                if NUM.search(s) and KEY.search(s):
                    ns = norm(s)
                    in_known = any(f in ns or ns[:60] in f for f in known_frag)
                    rows.append(dict(firm=r["firm"], call=r["call"], call_date=r["call_date"],
                                     page=("HTML" if kind == "html" else f"PDF p.{i}"),
                                     ai_term=int(bool(AI.search(s))), in_price_pass=int(in_known),
                                     sentence=s.strip(), source_url=r["source_url"], local_path=r["local_path"]))
    with open(f"{OUT}/scan_candidates.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    print(len(rows), "candidates;", sum(r["in_price_pass"] for r in rows), "overlap price pass")


if __name__ == "__main__":
    main()
