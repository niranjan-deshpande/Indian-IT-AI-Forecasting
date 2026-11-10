"""BEA Activities of U.S. MNEs (USDIA, majority-owned foreign affiliates, MOFAs) for India, 2009-2023 (no API key).
Backend of https://apps.bea.gov/iTable/?ReqID=2&step=1  (Direct Investment and MNE -> USDIA -> Activities of MNEs)
 (a) Services Supplied by MOFAs, by country of affiliate and destination: India -> 'To U.S. parents' = AFFILIATED US imports
     from India (fiscal-year basis, all industries, all service types; BEA survey BE-10/BE-11).
 (b) Employment of MOFAs by industry of affiliate and country: India.
"""
import json, re, requests, pandas as pd
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
URL = "https://apps.bea.gov/iTable/core/data/app/GetStep"
YRS = "40,41,42,43,48,49,52,55,56,58,60,61,65,66,68"   # 2009..2023

def get(series, rowtype, rows):
    data = [["Step1Prompt1", "1"], ["Step1Prompt2", "2"], ["Step2Prompt3", "13"], ["Step3Prompt4", str(series)],
            ["Step4Prompt5", str(rowtype)], ["Step5Prompt6", "1"], ["Step7Prompt8", YRS], ["Step8Prompt9A", "1"], ["Step8Prompt10A", rows]]
    s = json.loads(requests.post(URL, json={"appid": 2, "stepnum": 7, "data": data}, headers={"User-Agent": UA}, timeout=120).text)
    p = [p for p in s["Prompts"] if p["UIControl"] == "Table"][0]
    t = json.loads(json.loads(p["PromtData"])["Table"])
    t = {k.lower(): v for k, v in t.items()}
    nr, nc, nh = int(t["number_of_rows"]), int(t["number_of_columns"]), int(t["number_of_header_rows"])
    g = [[""] * nc for _ in range(nr)]; yr = [""] * nc
    for c in t["td"]:
        g[int(c["Row_ID"]) - 1][int(c["Column_ID"]) - 1] = re.sub("<[^>]+>", "", c["Cell_Value"]).replace("\xa0", " ").strip()
        if "yearValue" in c: yr[int(c["Column_ID"]) - 1] = c["yearValue"]
    out = []
    for r in g[nh:]:
        for j in range(1, nc):
            col = " | ".join(dict.fromkeys(g[i][j] for i in range(nh - 1)))
            v = r[j].replace(",", "")
            out.append(dict(row=r[0], column=col, year=yr[j], raw=r[j], value=float(v) if re.fullmatch(r"-?[\d.]+", v) else None))
    d = pd.DataFrame(out); d["subtitle"] = t["sub_title"]; d["desc"] = t["description"]
    d["url"] = "https://apps.bea.gov/iTable/?ReqID=2&step=1 (USDIA > Activities of MNEs > MOFAs 2009+)"
    return d

if __name__ == "__main__":
    a = get(60, 16, "2,86")   # services supplied, by country & destination: All countries, India
    a.to_csv("bea_mne_mofa_services_by_destination.csv", index=False)
    print(a[a.row == "India"].pivot_table(index="year", columns="column", values="value").iloc[:, :9])
    print(a[(a.row == "India")].groupby("column").raw.apply(lambda s: list(s)[-3:]).head(20))
    # Employment by industry and country (rowtype 2)
    e = get(8, 10, "2,86")   # employment by country (all countries list); industry x India not published in iTable
    e.to_csv("bea_mne_mofa_employment_india.csv", index=False)
    print(e.pivot_table(index="year", columns="row", values="value"))
    print(e[e.value.isna()].groupby("column").raw.apply(list).head(30))
