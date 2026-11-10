"""Find latest earnings 8-K (item 2.02) / 6-K for a ticker on EDGAR and list exhibit docs.
Usage: python edgar_latest.py TICKER [form]"""
import sys, json, urllib.request, re, time
UA = {"User-Agent": "ndeshpande research ndeshpande@college.harvard.edu"}
def get(u):
    time.sleep(0.2)
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA)).read()
tk = sys.argv[1].upper(); form = sys.argv[2] if len(sys.argv) > 2 else "8-K"
m = json.loads(get("https://www.sec.gov/files/company_tickers.json"))
cik = [v["cik_str"] for v in m.values() if v["ticker"] == tk][0]
s = json.loads(get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json"))["filings"]["recent"]
n = 0
for i, f in enumerate(s["form"]):
    if f != form: continue
    if form == "8-K" and "2.02" not in s["items"][i]: continue
    acc = s["accessionNumber"][i].replace("-", "")
    idx = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/"
    print(s["filingDate"][i], f, s["items"][i] if form=="8-K" else "", idx)
    try:
        j = json.loads(get(idx + "index.json"))
        for it in j["directory"]["item"]:
            if re.search(r"\.(htm|pdf)$", it["name"]) and not it["name"].startswith("R"):
                print("   ", idx + it["name"], it.get("size"))
    except Exception as e: print("  err", e)
    n += 1
    if n >= int(sys.argv[3] if len(sys.argv) > 3 else 1): break
