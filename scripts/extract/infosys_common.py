"""Shared helpers for Infosys extraction."""
import json, re, datetime, os

BASE = "data/sources/infosys"
MONTHS = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
DATE_RE = re.compile(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2})\s*,\s*(\d{4})")
QEND = {3: 31, 6: 30, 9: 30, 12: 31}


def qend_from_date(mon, year):
    return datetime.date(year, mon, QEND[mon])


def period_info(pe):
    """period_end date -> (fiscal_q, period_end str, cal_q)"""
    m, y = pe.month, pe.year
    q = {6: 1, 9: 2, 12: 3, 3: 4}[m]
    fy = y + 1 if m >= 4 else y
    return f"Q{q}FY{fy % 100:02d}", pe.isoformat(), f"{y}Q{(m - 1) // 3 + 1}"


def fq_to_pe(fq):
    q, fy = int(fq[1]), 2000 + int(fq[4:])
    mon = {1: 6, 2: 9, 3: 12, 4: 3}[q]
    y = fy - 1 if q in (1, 2, 3) else fy
    return qend_from_date(mon, y)


def filings():
    """Quarterly results 6-Ks: dict fiscal_q -> {acc, filing_date, announce_date, base_url}"""
    d = json.load(open(f"{BASE}/edgar_6k_index.json"))
    out = {}
    for acc, v in d.items():
        if not v["has_fact"]:
            continue
        fd = datetime.date.fromisoformat(v["date"])
        # quarter end preceding filing date
        cands = [qend_from_date(m, y) for y in (fd.year - 1, fd.year) for m in (3, 6, 9, 12)]
        pe = max(c for c in cands if c < fd)
        fq = period_info(pe)[0]
        a = re.search(r"On ([A-Z][a-z]+ \d+, ?\d{4}),? (?:we|We) announced", re.sub(r"\s+", " ", v["idx"]))
        ad = None
        if a:
            ad = datetime.datetime.strptime(a.group(1).replace(", ", ",").replace(",", ", "), "%B %d, %Y").date()
            if not (pe < ad <= fd):
                ad = None
        out[fq] = dict(acc=acc, filing_date=v["date"], announce_date=(ad or fd).isoformat(),
                       base=f"https://www.sec.gov/Archives/edgar/data/1067491/{acc.replace('-', '')}/")
    return out


NUM_TOKEN = r"(?:\(?-?\d[\d,]*(?:\.\d+)?\)?%?|[–—-])"


def to_num(tok):
    tok = tok.strip()
    if tok in ("–", "—", "-", ""):
        return None
    neg = tok.startswith("(") and tok.endswith(")") or tok.startswith("-")
    t = tok.strip("()%").lstrip("-").replace(",", "")
    try:
        v = float(t)
    except ValueError:
        return None
    return -v if neg else v


COLS = ["firm", "fiscal_q", "period_end", "cal_q", "metric", "dimension", "dim_type", "value", "unit", "basis",
        "period_type", "source_url", "source_doc", "source_loc", "doc_date", "notes"]
