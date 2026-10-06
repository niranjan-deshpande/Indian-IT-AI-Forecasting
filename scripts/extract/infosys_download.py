"""Download all exhibits of Infosys quarterly-results 6-Ks (those that mention a fact sheet) to data/sources/infosys/edgar/<acc>/"""
import json, time, os, requests
UA = {"User-Agent": "ndeshpande research ndeshpande@college.harvard.edu"}
BASE = "data/sources/infosys"
d = json.load(open(f"{BASE}/edgar_6k_index.json"))
for acc, v in sorted(d.items(), key=lambda x: x[1]["date"]):
    if not v["has_fact"]: continue
    a = acc.replace("-", "")
    od = f"{BASE}/edgar/{acc}"; os.makedirs(od, exist_ok=True)
    for text, href in v["links"]:
        if href.startswith("#") or not href.endswith((".htm", ".html", ".txt")): continue
        fn = os.path.basename(href)
        if os.path.exists(f"{od}/{fn}"): continue
        url = f"https://www.sec.gov/Archives/edgar/data/1067491/{a}/{fn}"
        time.sleep(0.12)
        r = requests.get(url, headers=UA, timeout=120)
        open(f"{od}/{fn}", "wb").write(r.content)
    # primary doc
    fn = os.path.basename(v["url"])
    if not os.path.exists(f"{od}/{fn}"):
        time.sleep(0.12); open(f"{od}/{fn}", "wb").write(requests.get(v["url"], headers=UA).content)
    print(acc, v["date"], len(os.listdir(od)))
