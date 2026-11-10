"""Fetch BEA series for India (no API key; iTable backend). Writes tidy CSVs.
Sources:
  Quarterly: ITA Table 1.3 (Expanded Detail by Area and Country), India, QNSA
    https://apps.bea.gov/iTable/?reqid=62&step=7&isuri=1&product=1&tablelist=30003  (area=India)
  Annual:   Intl Services Table 2.3 (by Country or Affiliation and by Type of Service), India
    https://apps.bea.gov/iTable/?reqid=62&step=7&isuri=1&product=4&tablelist=30583  (area=India)
  Annual:   Intl Services Table 2.3, 'All countries, affiliated/unaffiliated' (world-level affiliation split)
"""
import re, pandas as pd
from bea_itable import get_step, table_grid

def num(x):
    x = x.replace(",", "").replace("\xa0", "").strip()
    try: return float(x)
    except: return None

def clean(s): return re.sub("<[^>]+>", "", s).replace("\xa0", " ").strip()

out = []
# ---- quarterly ITA 1.3 India
r = get_step(7, {"TableList": 30003, "Product": 1, "TableListSecondary": 30031, "Filter_#1": 0, "Filter_#2": 1,
                 "Filter_#3": 27, "Filter_#4": 0, "Filter_#5": 0, "TheTableFlexibleAreas": 1, "isuri": 1})
t, f = table_grid(r)
g = t["grid"]; nh = t["nhdr"]
print(t["title"], t["desc"], nh, [row[:4] for row in g[:nh]])
yrs = [clean(c) for c in g[nh - 2]] if nh >= 3 else None
qs = [clean(c) for c in g[nh - 1]]
q = []
for row in g[nh:]:
    lab = clean(row[1])
    for j in range(2, len(row)):
        v = num(row[j])
        q.append(dict(line=clean(row[0]), label=lab, period=f"{yrs[j]}{qs[j]}", value=v, raw=row[j].strip()))
q = pd.DataFrame(q)
keep = q[q.label.isin(["Services", "Telecommunications, computer, and information services", "Other business services"])].copy()
keep["direction"] = keep.line.astype(int).map(lambda l: "exports" if l < 34 else "imports")
keep["source"] = "BEA ITA Table 1.3 India QNSA, release " + t["desc"]
keep["url"] = "https://apps.bea.gov/iTable/?reqid=62&step=7&isuri=1&product=1&tablelist=30003"
keep.to_csv("bea_ita13_india_quarterly.csv", index=False)
print(keep.groupby(["line", "label"]).size())

# ---- annual Intl Services Table 2.3 for India and for affiliation aggregates
def t23(areakey, name):
    r = get_step(7, {"TableList": 30583, "Product": 4, "TableListSecondary": 290, "Filter_#1": 0, "Filter_#2": areakey,
                     "Filter_#3": 0, "Filter_#4": "", "Filter_#5": "", "TheTableFlexibleAreas": 1, "isuri": 1})
    t, f = table_grid(r)
    g = t["grid"]; nh = t["nhdr"]
    yrs = [clean(c) for c in g[nh - 1]]
    rows = []
    for row in g[nh:]:
        for j in range(2, len(row)):
            rows.append(dict(area=name, line=clean(row[0]), label=clean(row[1]), year=yrs[j], value=num(row[j]), raw=row[j].strip()))
    d = pd.DataFrame(rows); d["release"] = t["desc"]
    d["url"] = "https://apps.bea.gov/iTable/?reqid=62&step=7&isuri=1&product=4&tablelist=30583"
    return d
a = pd.concat([t23(75, "India"), t23(1, "All countries"), t23(91, "All countries, unaffiliated"), t23(92, "All countries, affiliated"),
               t23(93, "All countries, US parents' trade with foreign affiliates")])
lines = ["Exports of services", "Imports of services", "Telecommunications, computer, and information services", "Computer services",
         "Computer software, including end-user licenses and customization", "Cloud computing and data storage services",
         "Other computer services", "Other business services", "Professional and management consulting services",
         "Research and development services", "Technical, trade-related, and other business services",
         "Business and management consulting and public relations services", "Other business services n.i.e. 4",
         "Accounting, auditing, bookkeeping, and tax consulting services", "Unaffiliated", "Affiliated",
         "U.S. parents' imports from their foreign affiliates", "U.S. parents' exports to their foreign affiliates"]
a = a[a.label.isin(lines)]
a["direction"] = a.line.map(lambda l: "exports" if l and l.isdigit() and int(l) < 104 else "imports")
a = a[a.direction == "imports"].copy()  # keep imports only (small extract)
a["note"] = ""
ipaff = a.label.isin(["Unaffiliated", "Affiliated", "U.S. parents' imports from their foreign affiliates", "U.S. parents' exports to their foreign affiliates"])
a.loc[ipaff, "note"] = "Affiliation lines refer ONLY to charges for use of IP (BEA publishes country x affiliation only for IP); for computer services use area='All countries, affiliated/unaffiliated'"
a.to_csv("bea_is23_annual.csv", index=False)
print(a[(a.area == "India") & (a.direction == "imports")].pivot_table(index="year", columns="label", values="value").tail(12).T)
