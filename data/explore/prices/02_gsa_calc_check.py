"""Quick access check of GSA CALC+ ceiling labor rates (no key). Saves vendor row counts + price summary for the 8 firms."""
import requests, pandas as pd, statistics as st
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"}
BASE = "https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/"
rows = []
for kw, match in [("accenture", "ACCENTURE"), ("cognizant", "COGNIZANT"), ("tata", "TATA"), ("infosys", "INFOSYS"),
                  ("wipro", "WIPRO"), ("hcl", "HCL"), ("tech mahindra", "MAHINDRA"), ("ltimindtree", "LTIMINDTREE")]:
    hits, page = [], 1
    while True:
        d = requests.get(BASE, params={"keyword": kw, "page": page, "page_size": 500}, headers=UA, timeout=60).json()
        h = d["hits"]["hits"]; hits += h
        if len(h) < 500 or page >= 10: break
        page += 1
    h = [x["_source"] for x in hits if match in x["_source"]["vendor_name"].upper()]
    pr = [x["current_price"] for x in h if x.get("current_price")]
    rows.append(dict(keyword=kw, vendors="; ".join(sorted({x["vendor_name"] for x in h})), n_labor_cats=len(h),
                     median_current_hourly_ceiling=st.median(pr) if pr else None,
                     contract_start_min=min((x["contract_start"] for x in h), default=None),
                     source_url=f"{BASE}?keyword={kw.replace(' ', '%20')}"))
df = pd.DataFrame(rows); print(df.to_string()); df.to_csv("gsa_calc_vendor_check.csv", index=False)
