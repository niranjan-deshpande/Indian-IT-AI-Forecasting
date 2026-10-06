"""Shared helpers for the earnings-call statement audit (price pass + demand pass).

- build_docs(): reconstructs the 183-transcript set used by the price pass
  (logic ported from the price pass's corpus builder): 8 firms, call dates 2021-01-01..2026-10-31.
- page_texts(): page-split text (pdftotext default mode, split on form feed; Infosys 6-K HTML = one "page").
- locate(): whitespace-normalised verbatim substring check with '...' elisions; returns PDF page index.
Read-only with respect to project data.
"""
import os, re, glob, subprocess, html, csv, datetime as dt, urllib.parse
from functools import lru_cache

ROOT = "/Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/0. Exploratory Analysis"
SRC = f"{ROOT}/data/sources"
FIRMS = ['TCS', 'Infosys', 'HCLTech', 'Wipro', 'TechM', 'LTIMindtree', 'Cognizant', 'Accenture']
WINDOW = ("2021-01-01", "2026-10-31")


def _rd(p):
    return [l.rstrip("\n").split("\t") for l in open(p) if "\t" in l]


def _candidates():
    docs = []  # firm, call, path, url, kind
    tu = dict(_rd(f"{SRC}/tcs/_transcript_urls.tsv"))
    for p in sorted(glob.glob(f"{SRC}/tcs/20*_q?_transcript.pdf")):
        b = os.path.basename(p); y = int(b[:4])
        if y >= 2020:
            fy = (y + 1) % 100; q = b.split("_")[1].upper()
            docs.append(("TCS", f"{q}FY{fy}", p, tu.get(b, ""), "pdf"))
    for l in open(f"{SRC}/infosys/exhibit_desc.txt"):
        pth, d = l.rstrip("\n").split("|", 1)
        if "TRANSCRIPT OF EARNINGS CALL" in d.upper() or "APRIL 20, 2020 EARNINGS CALL" in d.upper():
            acc = pth.split("/")[0]
            if int(acc.split("-")[1]) >= 20:
                url = f"https://www.sec.gov/Archives/edgar/data/1067491/{acc.replace('-', '')}/{pth.split('/')[1]}"
                docs.append(("Infosys", "?", f"{SRC}/infosys/edgar/{pth}", url, "html"))
    wl = {os.path.basename(x.strip()): "https://www.wipro.com" + x.strip() for x in open(f"{SRC}/wipro/wipro_links_fy15_fy27.txt")}
    for p in sorted(glob.glob(f"{SRC}/wipro/20*.pdf")):
        b = os.path.basename(p)
        if re.search(r"transcript", b, re.I) and int(b[:4]) >= 2020:
            key = b.split("_", 2)[-1]; m = re.search(r"q(\d)-?fy-?(\d\d)", key, re.I)
            docs.append(("Wipro", f"Q{m.group(1)}FY{m.group(2)}", p, wl.get(key, ""), "pdf"))
    for q, u in _rd(f"{SRC}/wipro/transcripts_task3/urls.tsv"):
        docs.append(("Wipro", q, f"{SRC}/wipro/transcripts_task3/Wipro_{q}_transcript.pdf", u, "pdf"))
    au = dict(l.split() for l in open(f"{SRC}/accenture/transcripts/urls.txt"))
    for p in sorted(glob.glob(f"{SRC}/accenture/transcripts/*.pdf")):
        q = os.path.basename(p)[:-4]
        if int(q[-2:]) >= 21:
            docs.append(("Accenture", q, p, au.get(q, ""), "pdf"))
    for q, u in _rd(f"{SRC}/accenture/transcripts_task3/urls.tsv"):
        if int(q[-2:]) >= 21:
            docs.append(("Accenture", q, f"{SRC}/accenture/transcripts_task3/ACN_{q}.pdf", u, "pdf"))
    for firm, d, pre in [("HCLTech", "hcltech", "HCL"), ("TechM", "techm", "TechM"),
                         ("LTIMindtree", "ltim", "LTIM"), ("Cognizant", "cognizant", "CTSH")]:
        for q, u in _rd(f"{SRC}/{d}/transcripts_task3/urls.tsv"):
            p = f"{SRC}/{d}/transcripts_task3/{pre}_{q}.pdf"
            if os.path.exists(p):
                docs.append((firm, q, p, u, "pdf"))
    return docs


MONS = "january|february|march|april|may|june|july|august|september|october|november|december"
MON = MONS + "|jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec"
MI = {}
for _i, _m in enumerate(MONS.split("|")):
    MI[_m] = _i + 1; MI[_m[:3]] = _i + 1
MI["sept"] = 9
PATS = [re.compile(rf"\b({MON})\.?\s+(\d{{1,2}})(?:st|nd|rd|th)?,?\s+(20\d\d)", re.I),
        re.compile(rf"\b(\d{{1,2}})(?:st|nd|rd|th)?[\s\-]+({MON})[,\s\-]+(20\d\d)", re.I)]


def _cdate(t):
    head = t[:3000]; best = None
    for i, pat in enumerate(PATS):
        for m in pat.finditer(head):
            g = m.groups()
            try:
                mo, d, y = (MI[g[0].lower()], int(g[1]), int(g[2])) if i == 0 else (MI[g[1].lower()], int(g[0]), int(g[2]))
                dd = dt.date(y, mo, d)
            except Exception:
                continue
            if best is None or m.start() < best[0]:
                best = (m.start(), dd)
    return best[1] if best else None


@lru_cache(maxsize=None)
def page_texts(path, kind):
    if kind == "pdf":
        t = subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True).stdout
        return tuple(t.split("\f"))
    raw = open(path, encoding="utf-8", errors="ignore").read()
    raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</tr>", "\n", raw)
    t = html.unescape(re.sub(r"<[^>]+>", " ", raw)).replace("\xa0", " ")
    t = re.sub(r"[ \t]+", " ", t); t = re.sub(r"\n\s*\n+", "\n\n", t)
    return (t,)


def _date_and_call(firm, q, p, u, kind):
    full = "\n".join(page_texts(p, kind))
    d = _cdate(full)
    if firm == "Infosys":
        if d is None:
            d = dt.date(2022, 10, 13)  # Q2FY23 exhibit has no parsable date; 6-K filing date
        ref = d - dt.timedelta(days=45); fy = (ref.year + 1 if ref.month >= 4 else ref.year) % 100
        qn = ((ref.month - 4) % 12) // 3 + 1; q = f"Q{qn}FY{fy}"
    if firm == "TCS":
        uu = urllib.parse.unquote(u); m = re.search(r"on ([A-Za-z]+)\s+(\d{1,2}),?\s+(20\d\d)", uu)
        if m:
            d = dt.date(int(m.group(3)), MI[m.group(1).lower()[:3]], int(m.group(2)))
            if q == "Q3FY24":
                d = dt.date(2024, 1, 11)
    if firm == "TechM" and q == "Q2FY22":
        d = dt.date(2021, 10, 25)
    if firm == "TechM" and q == "Q4FY26":
        d = dt.date(2026, 4, 22)  # Analyst Day transcript; date per IR
    return q, d


def half_year(date_iso):
    y, m = int(date_iso[:4]), int(date_iso[5:7])
    return f"{y}H{1 if m <= 6 else 2}"


@lru_cache(maxsize=1)
def build_docs():
    out = []
    for firm, q, p, u, kind in _candidates():
        q, d = _date_and_call(firm, q, p, u, kind)
        if d is None:
            raise RuntimeError(f"no date {firm} {p}")
        di = d.isoformat()
        if WINDOW[0] <= di <= WINDOW[1]:
            out.append(dict(firm=firm, call=q, call_date=di, half_year=half_year(di),
                            local_path=os.path.relpath(p, ROOT), source_url=u, kind=kind, abspath=p))
    out.sort(key=lambda r: (FIRMS.index(r['firm']), r['call_date']))
    return tuple(out)


def doc_index():
    return {(r['firm'], r['call']): r for r in build_docs()}


def pages_of(firm, call):
    r = doc_index()[(firm, call)]
    P = page_texts(r['abspath'], r['kind'])
    if r['kind'] == 'html':
        return [("n/a", P[0])]
    return [(str(i + 1), x) for i, x in enumerate(P) if x.strip()]


def norm(s, loose=False):
    s = s.replace("­", "")
    s = re.sub(r"\s+", " ", s).strip()
    if loose:
        s = s.translate(str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-", "…": "..."}))
        s = s.lower()
    return s


def locate(firm, call, quote, allow_loose=False):
    """Return (start_page, end_page, status). status 'exact' = whitespace-normalised verbatim
    (fragments split on '...' must appear in order within one page or across one page break)."""
    P = pages_of(firm, call)
    frags = [f.strip() for f in re.split(r"\.\.\.|…|\[\.\.\.\]", quote) if f.strip()]
    for loose in ((False, True) if allow_loose else (False,)):
        for i, (pn, txt) in enumerate(P):
            nxt = P[i + 1][1] if i + 1 < len(P) else ""
            win = norm(txt + " " + nxt, loose)
            pos = 0; ok = True; first = None
            for f in frags:
                fn = norm(f, loose).strip(' "\'')
                j = win.find(fn, pos)
                if j < 0:
                    ok = False; break
                if first is None:
                    first = j
                pos = j + len(fn)
            if ok:
                own = norm(txt, loose)
                pg = pn if first < len(own) else P[i + 1][0]
                endpg = pg if pos <= len(own) else (P[i + 1][0] if i + 1 < len(P) else pn)
                return pg, endpg, ("exact" if not loose else "loose")
    return None, None, "NOT FOUND"


def page_label(pg, endpg):
    if pg is None:
        return ""
    if pg == "n/a":
        return "n/a (HTML exhibit, no pagination)"
    return f"PDF p.{pg}" if pg == endpg else f"PDF p.{pg}-{endpg}"
