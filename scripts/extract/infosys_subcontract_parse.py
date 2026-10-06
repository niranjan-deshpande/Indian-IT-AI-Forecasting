"""Extract quarterly 'Cost of technical sub-contractors' (cost of sales break-up note) from Infosys IFRS condensed
financial statements / IFRS earnings releases attached to quarterly-results 6-Ks on EDGAR.
Both USD (Dollars in millions) and INR (crore) IFRS versions. Three-months columns only (current, prior-year).
Output: data/sources/infosys/parsed_subcontract.csv
"""
import re, os, sys, glob, csv, datetime
from bs4 import BeautifulSoup
sys.path.insert(0, os.path.dirname(__file__))
from infosys_common import *

FIL = filings()
rows = []
for fq, f in sorted(FIL.items(), key=lambda x: fq_to_pe(x[0])):
    pe = fq_to_pe(fq)
    d = f"{BASE}/edgar/{f['acc']}"
    got = {}
    for ex in sorted(glob.glob(f"{d}/exv99*.htm")):
        raw = open(ex, encoding="latin-1").read()
        desc = (re.search(r"<DESCRIPTION>(.*)", raw) or [None, ""])[1].strip()
        if re.search(r"IND ?AS|INDIAN GAAP|STANDALONE|STOCK EXCHANGE|TRANSCRIPT", desc, re.I):
            continue
        t = re.sub(r"\s+", " ", BeautifulSoup(raw, "html.parser").get_text(" | ", strip=True))
        for m in re.finditer(r"(?:Cost of )?technical sub-?\s?contractors \| \$? ?\|? ?([\d,]+) \| \$? ?\|? ?([\d,]+)", t, re.I):
            before = t[max(0, m.start() - 1500):m.start()]
            k = before.rfind("Cost of sales")
            hdr = before[k:] if k >= 0 else before[-600:]
            if "Dollars in millions" in hdr or "US$" in hdr:
                ccy = "USD_mn"
            elif re.search(r"crore|₹|Rupees|`", hdr):
                ccy = "INR_cr"
            else:
                continue
            if not re.search(r"Cost of sales \| \(", hdr):
                continue
            if re.search(r"Three months\W+ended|Quarter\W+ended", hdr, re.I):
                ptype = "quarter"
            elif re.search(r"Year ended", hdr, re.I):
                ptype = "annual"
            else:
                continue
            if ccy in got and (got[ccy] == "quarter" or ptype == "annual"):
                continue
            if ccy in got:  # replace earlier annual candidate by quarterly one
                rows[:] = [r for r in rows if not (r["_fq"] == fq and r["unit"] == ccy)]
            got[ccy] = ptype
            v0 = to_num(m.group(1)); v1 = to_num(m.group(2))
            url = f["base"] + os.path.basename(ex)
            for p, v, note in [(pe, v0, ""), (pe.replace(year=pe.year - 1), v1, "prior-year comparative column")]:
                if ptype == "annual":
                    note = ("fiscal-year total (Q4 USD statements for this year report only year-ended figures)" + ("; " + note if note else ""))
                fqq, pes, calq = period_info(p)
                rows.append(dict(_fq=fq, firm="infosys", fiscal_q=fqq, period_end=pes, cal_q=calq, metric="subcontracting_cost",
                                 dimension="total", dim_type="total", value=v, unit=ccy, basis="reported", period_type=ptype,
                                 source_url=url, source_doc=f"Infosys {fq} IFRS financial statements ({'USD' if ccy == 'USD_mn' else 'INR'}), 6-K exhibit: {desc.title()}",
                                 source_loc="Break-up of expenses: Cost of sales - Cost of technical sub-contractors (" + ("three months" if ptype == "quarter" else "year ended") + ")",
                                 doc_date=f["announce_date"],
                                 notes=("Cost of technical sub-contractors within cost of sales, consolidated IFRS" + ("; " + note if note else ""))))
    print(fq, got, file=sys.stderr)
with open(f"{BASE}/parsed_subcontract.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=COLS, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
print(len(rows), file=sys.stderr)
