"""Scrape Revelio Labs' free company profile pages for Indian IT firms.

Each page (https://www.reveliolabs.com/companies/<slug>/employees) shows, for free:
  - quarterly global headcount (2023 Q2 onward)
  - headcount share by world region (South Asia ~= India for these firms)
  - annual "active job postings" (2023-2026) and "new roles/month" (2023-2026)
Postings are GLOBAL for the firm (not India-only) and 2026 is a partial year
(page data "as of" Q1 2026). Revelio sources postings from company sites + boards.

Usage: python3 -I scrape_revelio_company_pages.py   (saves raw HTML under raw/revelio/)
Outputs: revelio_firm_postings.csv, revelio_firm_headcount_q.csv, revelio_firm_region_share.csv
"""
import html
import io
import os
import re
import subprocess
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw", "revelio")
os.makedirs(RAW, exist_ok=True)

FIRMS = {
    "TCS": "tata-consultancy-services-ltd",
    "Infosys": "infosys",
    "Wipro": "wipro-technologies-ltd",
    "HCLTech": "hcl",
    "Tech Mahindra": "tech-mahindra",
    "LTIMindtree (LTM)": "ltm",
    "Cognizant": "cognizant-technology-sol",
    "Persistent": "persistent-systems",
    "Mphasis": "mphasis",
    "Hexaware": "hexaware",
    "Coforge": "coforge",
    "Accenture": "accenture",
    "Capgemini": "capgemini",
}


def fetch(slug):
    path = os.path.join(RAW, f"{slug}.html")
    if not os.path.exists(path) or os.path.getsize(path) < 10000:
        url = f"https://www.reveliolabs.com/companies/{slug}/employees"
        subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0", "-o", path, url], check=True)
    return open(path, encoding="utf-8").read()


def text_of(s):
    t = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(re.sub(r"\s+", " ", t))


post_rows, hc_rows, reg_rows = [], [], []
for firm, slug in FIRMS.items():
    s = fetch(slug)
    url = f"https://www.reveliolabs.com/companies/{slug}/employees"
    title = re.search(r"<title>([^<|]*)", s)
    title = title.group(1).strip() if title else ""
    i = s.find('id="postings"')
    seg = text_of(s[i:i + 15000]) if i >= 0 else ""
    for m in re.finditer(r"had ([\d,]+) active job postings in (\d{4})", seg):
        post_rows.append(dict(firm=firm, slug=slug, page_title=title, year=int(m.group(2)),
                              metric="active_postings", value=int(m.group(1).replace(",", "")), source_url=url))
    m = re.search(r"Hiring velocity in (\d{4}) : ([\d,]+) new roles/month , up from ([\d,]+) in (\d{4}) and ([\d,]+) in (\d{4})", seg)
    m2 = re.search(r"new postings per month (?:cooling|rising|growing|climbing|falling|declining) from ([\d,]+) in (\d{4}) to ([\d,]+) in (\d{4})", seg)
    vel = {}
    m3 = re.search(r"Hiring velocity in (\d{4}) : ([\d,]+) new roles/month , (?:up|down) from ([\d,]+) in (\d{4}) and ([\d,]+) in (\d{4})", seg)
    if m3:
        vel[int(m3.group(1))] = m3.group(2); vel[int(m3.group(4))] = m3.group(3); vel[int(m3.group(6))] = m3.group(5)
    if m2:
        vel.setdefault(int(m2.group(2)), m2.group(1)); vel.setdefault(int(m2.group(4)), m2.group(3))
    for y, v in vel.items():
        post_rows.append(dict(firm=firm, slug=slug, page_title=title, year=y, metric="new_postings_per_month",
                              value=int(v.replace(",", "")), source_url=url))
    full = text_of(s)
    m4 = re.search(r"In (\d{4}) , [^.]*? opened ([\d,]+) new job postings", full)
    if m4:
        post_rows.append(dict(firm=firm, slug=slug, page_title=title, year=int(m4.group(1)),
                              metric="new_postings_total_year", value=int(m4.group(2).replace(",", "")), source_url=url))
    m5 = re.search(r"In Q1 (\d{4}) , [^.]*? opened ([\d,]+) new job postings", full)
    if m5:
        post_rows.append(dict(firm=firm, slug=slug, page_title=title, year=int(m5.group(1)),
                              metric="new_postings_Q1", value=int(m5.group(2).replace(",", "")), source_url=url))
    try:
        tabs = pd.read_html(io.StringIO(s))
    except ValueError:
        tabs = []
    for t in tabs:
        cols = [str(c) for c in t.columns]
        if "Qtr" in cols:
            for _, r in t.iterrows():
                hc_rows.append(dict(firm=firm, slug=slug, year=r["Year"], quarter=r["Qtr"], headcount=r["Employees"], source_url=url))
        elif "Region" in cols and "% of Total" in cols:
            for _, r in t.iterrows():
                reg_rows.append(dict(firm=firm, slug=slug, region=r["Region"], employees=r["Employees"],
                                     share_pct=float(str(r["% of Total"]).rstrip("%")), source_url=url))
    print(firm, title, len([p for p in post_rows if p["firm"] == firm]), "posting rows", file=sys.stderr)

pd.DataFrame(post_rows).sort_values(["firm", "metric", "year"]).to_csv(os.path.join(HERE, "revelio_firm_postings.csv"), index=False)
pd.DataFrame(hc_rows).to_csv(os.path.join(HERE, "revelio_firm_headcount_q.csv"), index=False)
pd.DataFrame(reg_rows).to_csv(os.path.join(HERE, "revelio_firm_region_share.csv"), index=False)
