"""US imports of computer services (and comparators) by partner country, BEA International Services Table 2.3.
No API key: uses the public iTable backend (same method as data/explore/trade/bea_itable.py).
Page: https://apps.bea.gov/iTable/?reqid=62&step=7&isuri=1&product=4&tablelist=30583
Line keys (Filter_#3): 162 = imports, computer services; 169 = imports, other business services; 106 = imports of services.
Area Filter_#2 = 0 -> all areas/countries in one table.
"""
import json, re, sys, requests, pandas as pd
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
API = "https://apps.bea.gov/iTable/core/data/app/GetSteps"
PAGE = "https://apps.bea.gov/iTable/?reqid=62&step=7&isuri=1&product=4&tablelist=30583"

def get_step(step, data):
    body = {"appid": 62, "steps": [step], "data": [[k, str(v)] for k, v in data.items()]}
    r = requests.post(API, json=body, headers={"User-Agent": UA}, timeout=180); r.raise_for_status()
    return json.loads(r.text)

def grid(resp):
    st = [s for s in resp["Steps"] if s["IsTable"] == 1][0]
    tp = [p for p in st["Prompts"] if p["UIControl"] == "Table"][0]
    t = json.loads(json.loads(tp["PromtData"])["Table"])
    nr, nc = int(t["Number_Of_Rows"]), int(t["Number_Of_Columns"])
    g = [[""] * nc for _ in range(nr)]
    for c in t["TD"]:
        g[int(c["Row_ID"]) - 1][int(c["Column_ID"]) - 1] = c["Cell_Value"]
    return t, g, int(t["Number_Of_Header_Rows"])

clean = lambda s: re.sub("<[^>]+>", "", s).replace("\xa0", " ").strip()
def num(x):
    x = clean(x).replace(",", "")
    try: return float(x)
    except: return None

out = []
seen = set()
for key in [162, 169, 106]:
    t, g, nh = grid(get_step(7, {"TableList": 30583, "Product": 4, "TableListSecondary": 290, "Filter_#1": 0, "Filter_#2": 0,
                                  "Filter_#3": key, "Filter_#4": "", "Filter_#5": "", "TheTableFlexibleAreas": 1, "isuri": 1}))
    areas = [clean(c) for c in g[0]]; yrs = [clean(c) for c in g[nh - 1]]
    for row in g[nh:]:
        line, label = clean(row[0]), clean(row[1])
        if (line, label) in seen: continue
        seen.add((line, label))
        for j in range(2, len(row)):
            if re.fullmatch(r"\d{4}", yrs[j]):
                out.append(dict(line=line, label="Imports: " + label if line != "104" else label, area=areas[j], year=int(yrs[j]),
                                value_musd=num(row[j]), raw=clean(row[j]), release=t.get("Description"), url=PAGE))
d = pd.DataFrame(out)
d.to_csv(sys.argv[1], index=False)
print(d.groupby("label").size())
