"""Scan LTI / Mindtree / LTIM growth rows for the '(x.x)%' sign bug in scripts/extract/ltim_parse_tables.parse_num
(neg is detected only for '(x)' or '(x%)', not for '(x)%', so printed negatives became positive).

For every row of data/raw/ltim.csv (firms lti, mindtree, ltim) whose metric contains 'growth' and whose value is >= 0,
open the local copy of the source document (data/sources/ltim/: ltm.com PDFs via download_index.tsv, NSE zips/PDFs in
mindtree/nse/ and lti_nse/), go to the page in source_loc, find the line that starts with the row label and look for
the printed token of the same magnitude. Output: audit/ltim_sign_scan.csv with the printed token and a verdict
(negative_printed / positive_printed / ambiguous / not_found). Only 'negative_printed' rows are sign errors.
"""
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path
import pandas as pd
from audit_common import ROOT, AUD

BASE = ROOT / "data" / "sources" / "ltim"
SRC = BASE / "mindtree" / "nse"
idx = pd.read_csv(SRC / "index.tsv", sep="\t", header=None, usecols=[0, 1], names=["local", "url"])
url2local = {u: SRC / l for u, l in zip(idx.url, idx.local)}
di = pd.read_csv(BASE / "download_index.tsv", sep="\t", header=None, usecols=[0, 1], names=["local", "url"])
url2local.update({u: BASE / l for u, l in zip(di.url, di.local)})
raw = pd.read_csv(ROOT / "data" / "raw" / "ltim.csv", low_memory=False, dtype={"cal_q": str})
rows = raw[raw.firm.isin(["lti", "mindtree", "ltim"]) & raw.metric.str.contains("growth") & (raw.value > 0)].copy()
tmp = Path(tempfile.mkdtemp())
cache = {}


def pages(url):
    if url in cache:
        return cache[url]
    p = url2local.get(url)
    if p is None:
        base = url.split("/")[-1]
        for d in (SRC, BASE / "lti_nse", BASE):
            hit = [q for q in d.iterdir() if q.name.endswith(base)]
            if hit:
                p = hit[0]
                break
    out = None
    if p is not None and p.exists():
        pdfs = []
        if p.suffix == ".zip":
            with zipfile.ZipFile(p) as z:
                for n in z.namelist():
                    if n.lower().endswith(".pdf"):
                        z.extract(n, tmp / p.stem)
                        pdfs.append(tmp / p.stem / n)
        elif p.suffix == ".pdf":
            pdfs = [p]
        out = []
        for f in pdfs:
            t = subprocess.run(["pdftotext", "-layout", str(f), "-"], capture_output=True, text=True).stdout
            out.append(t.split("\f"))
    cache[url] = out
    return out


res = []
for r in rows.itertuples():
    loc = str(r.source_loc)
    pg = re.search(r"\bp(\d+)\b", loc)
    lab = re.search(r"row '([^']+)'", loc)
    verdict, token = "not_found", ""
    docs = pages(r.source_url)
    if docs and lab:
        label = lab.group(1).strip().lower()
        target = f"{abs(r.value):.1f}"
        for doc in docs:
            cand_pages = [int(pg.group(1)) - 1] if pg and int(pg.group(1)) - 1 < len(doc) else range(len(doc))
            for i in cand_pages:
                for line in doc[i].splitlines():
                    if re.sub(r"\s+", " ", line.strip().lower()).startswith(re.sub(r"\s+", " ", label)[:25]):
                        toks = re.findall(r"\(?-?[\d,]*\.?\d+\)?%?\)?", line)
                        hit = [t for t in toks if t.strip("()%-").replace(",", "") and
                               abs(float(t.strip("()%-").replace(",", "")) - abs(r.value)) < 0.051]
                        if hit:
                            token = hit[-1] if "yoy" in loc.lower() else hit[0] if len(hit) == 1 else "|".join(hit)
                            neg = [t for t in hit if t.startswith("(") or t.startswith("-")]
                            verdict = "negative_printed" if neg and len(neg) == len(hit) else ("ambiguous" if neg else "positive_printed")
                            break
                if verdict != "not_found":
                    break
            if verdict != "not_found":
                break
    res.append(dict(firm=r.firm, fiscal_q=r.fiscal_q, cal_q=r.cal_q, metric=r.metric, dimension=r.dimension, basis=r.basis,
                    value=r.value, doc_date=r.doc_date, source_loc=loc, source_url=r.source_url, printed=token, verdict=verdict))
out = pd.DataFrame(res)
out.to_csv(AUD / "ltim_sign_scan.csv", index=False)
print(out.groupby("firm").verdict.value_counts())
print(out[out.verdict.isin(["negative_printed", "ambiguous"])][["firm", "fiscal_q", "cal_q", "metric", "dimension", "value", "printed", "doc_date"]].to_string())
