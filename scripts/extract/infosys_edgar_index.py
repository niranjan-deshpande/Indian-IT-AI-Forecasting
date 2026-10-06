"""Scan Infosys (CIK 1067491) 6-K filings on EDGAR; find those with a Fact Sheet / press release exhibit
and save the exhibit-index mapping to data/sources/infosys/edgar_6k_index.json"""
import json, time, re, requests, os
from bs4 import BeautifulSoup
UA = {"User-Agent": "ndeshpande research ndeshpande@college.harvard.edu"}
BASE = "data/sources/infosys"
d = json.load(open(f"{BASE}/subs.json"))
r = d["filings"]["recent"]
out = {}
if os.path.exists(f"{BASE}/edgar_6k_index.json"):
    out = json.load(open(f"{BASE}/edgar_6k_index.json"))
for i in range(len(r["form"])):
    if r["form"][i] != "6-K" or r["filingDate"][i] < "2011-01-01":
        continue
    acc = r["accessionNumber"][i]
    if acc in out: continue
    a = acc.replace("-", "")
    url = f"https://www.sec.gov/Archives/edgar/data/1067491/{a}/{r['primaryDocument'][i]}"
    time.sleep(0.15)
    try:
        html = requests.get(url, headers=UA, timeout=60).text
    except Exception as e:
        print("ERR", acc, e); continue
    soup = BeautifulSoup(html, "html.parser")
    txt = soup.get_text(" ", strip=True)
    links = [(x.get_text(" ", strip=True), x.get("href")) for x in soup.find_all("a") if x.get("href")]
    m = re.search(r"INDEX TO EXHIBITS(.*)", txt, re.S)
    idx = m.group(1)[:3000] if m else ""
    out[acc] = dict(date=r["filingDate"][i], url=url, desc=r["primaryDocDescription"][i],
                    has_fact=("fact sheet" in txt.lower()), results=("results of operations" in txt.lower()),
                    idx=idx, links=links, head=txt[:1500])
    print(acc, r["filingDate"][i], out[acc]["has_fact"], out[acc]["results"])
json.dump(out, open(f"{BASE}/edgar_6k_index.json", "w"), indent=1)
