"""Shared helpers for Tech Mahindra extraction (firm id `techm`)."""
import csv, os, re, datetime as dt

ROOT = "/Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/0. Exploratory Analysis"
SRC = os.path.join(ROOT, "data/sources/techm")
TXT = os.path.join(SRC, "txt")          # pdftotext -layout outputs (created by techm_extract.py)
FIRM = "techm"
BASE_URL = "https://insights.techmahindra.com/investors/"

COLS = ["firm", "fiscal_q", "period_end", "cal_q", "metric", "dimension", "dim_type", "value", "unit",
        "basis", "period_type", "source_url", "source_doc", "source_loc", "doc_date", "notes"]


def link_map():
    """filename -> (IR quarter label, doc type, URL) from the IR quarterly-earnings page scrape."""
    m = {}
    with open(os.path.join(SRC, "_ir_links_quarterly_earnings.csv")) as f:
        for q, t, u in csv.reader(f):
            fn = os.path.basename(u).replace("%20", "_")
            m[fn] = (q, t, u)
    return m


def fq(q, fy):
    """(1, 2017) -> 'Q1FY17'"""
    return f"Q{q}FY{fy % 100:02d}"


def parse_fq(s):
    m = re.match(r"Q([1-4])FY(\d{2})$", s)
    return int(m.group(1)), 2000 + int(m.group(2))


def period_end(fiscal_q):
    q, fy = parse_fq(fiscal_q)
    return {1: f"{fy-1}-06-30", 2: f"{fy-1}-09-30", 3: f"{fy-1}-12-31", 4: f"{fy}-03-31"}[q]


def cal_q(fiscal_q):
    q, fy = parse_fq(fiscal_q)
    return {1: f"{fy-1}Q2", 2: f"{fy-1}Q3", 3: f"{fy-1}Q4", 4: f"{fy}Q1"}[q]


def prev_q(fiscal_q, n=1):
    q, fy = parse_fq(fiscal_q)
    for _ in range(n):
        q -= 1
        if q == 0:
            q, fy = 4, fy - 1
    return fq(q, fy)


NUM_RE = re.compile(r"\(?-?[\d,]*\.?\d+\)?%?|(?<!\w)-(?!\w)")


def to_num(tok):
    tok = tok.strip()
    if tok in ("-", ""):
        return None
    neg = tok.startswith("(") and tok.endswith(")")
    t = tok.strip("()").replace(",", "").replace("%", "")
    try:
        v = float(t)
    except ValueError:
        return None
    return -v if neg else v


def row(fiscal_q, metric, dimension, dim_type, value, unit, basis, period_type, url, doc, loc, doc_date, notes=""):
    return dict(firm=FIRM, fiscal_q=fiscal_q, period_end=period_end(fiscal_q), cal_q=cal_q(fiscal_q),
                metric=metric, dimension=dimension, dim_type=dim_type,
                value="" if value is None else (int(value) if isinstance(value, float) and value.is_integer() and unit == "count" else value),
                unit=unit, basis=basis, period_type=period_type, source_url=url, source_doc=doc,
                source_loc=loc, doc_date=doc_date, notes=notes)


# Approximate announcement dates (from press-release datelines where available; otherwise approx.)
MONTHS = {m: i for i, m in enumerate(["january", "february", "march", "april", "may", "june", "july", "august",
                                        "september", "october", "november", "december"], 1)}


def dateline(text, after=None):
    """First 'Month dd, yyyy' date in the document header that falls after `after` (the period end)."""
    for m in re.finditer(r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})\s*(?:st|nd|rd|th)?\s*,?\s+(20\d\d)", text[:3000]):
        d = f"{m.group(3)}-{MONTHS[m.group(1).lower()]:02d}-{int(m.group(2)):02d}"
        if after is None or d > after:
            return d
    return None


def _old_dateline(text):
    m = re.search(r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(20\d\d)", text[:3000])
    if not m:
        return None
    return f"{m.group(3)}-{MONTHS[m.group(1).lower()]:02d}-{int(m.group(2)):02d}"
