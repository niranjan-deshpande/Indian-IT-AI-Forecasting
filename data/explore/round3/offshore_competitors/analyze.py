"""Shares and growth: India vs other delivery locations.
Inputs (raw/): bea_t23_by_country_raw.csv (fetch_bea_by_country.py), imf_bop_si2_sj_all.csv (fetch_imf_world.py).
Outputs: bea_us_computer_imports_by_country.csv, imf_computer_exports_by_country.csv, india_share_summary.csv"""
import sys, pandas as pd, numpy as np
raw = sys.argv[1]
BEA_URL = "https://apps.bea.gov/iTable/?reqid=62&step=7&isuri=1&product=4&tablelist=30583"
IMF_URL = "https://api.imf.org/external/sdmx/2.1/data/IMF.STA,BOP/.CD_T.SI2+SJ+S.USD.A+Q?startPeriod=2012"
out = []
# ---------- BEA: US imports of computer services by partner
b = pd.read_csv(f"{raw}/bea_t23_by_country_raw.csv")
keep = ["All countries", "All countries, affiliated", "All countries, unaffiliated", "India", "Philippines", "Poland", "Romania", "Czech Republic",
        "Hungary", "Bulgaria", "Mexico", "Colombia", "Brazil", "Argentina", "Costa Rica", "Chile", "Vietnam", "Malaysia", "China", "Canada",
        "Ireland", "United Kingdom", "Israel", "Singapore", "Africa, other"]
b = b[b.area.isin(keep) & b.label.isin(["Imports: Computer services", "Imports: Other business services"]) & (b.year >= 2010)]
b[["label", "area", "year", "value_musd", "raw", "release", "url"]].to_csv("bea_us_computer_imports_by_country.csv", index=False)
cs = b[b.label == "Imports: Computer services"].pivot_table(index="year", columns="area", values="value_musd")
ob = b[b.label == "Imports: Other business services"].pivot_table(index="year", columns="area", values="value_musd")
LOWCOST = ["Philippines", "Poland", "Romania", "Czech Republic", "Hungary", "Bulgaria", "Mexico", "Colombia", "Brazil", "Argentina", "Costa Rica", "Chile", "Vietnam", "Malaysia", "Africa, other"]
for y in range(2014, 2026):
    tot = cs.loc[y, "All countries"]
    out.append(dict(source="BEA T2.3", metric="India share of US computer-services imports, %", year=y, value=round(100 * cs.loc[y, "India"] / tot, 2), url=BEA_URL))
    out.append(dict(source="BEA T2.3", metric="India share of US computer-services imports excl. Ireland+Canada, %", year=y,
                    value=round(100 * cs.loc[y, "India"] / (tot - cs.loc[y, "Ireland"] - cs.loc[y, "Canada"]), 2) if not np.isnan(cs.loc[y, "Ireland"]) else None, url=BEA_URL))
    lc = cs.loc[y, LOWCOST]
    out.append(dict(source="BEA T2.3", metric="US computer-services imports from 15 named low-cost locations (sum of non-suppressed), $m", year=y,
                    value=round(lc.sum(), 0), n_countries=int(lc.notna().sum()), url=BEA_URL))
    out.append(dict(source="BEA T2.3", metric="India share of US computer+other-business-services imports, %", year=y,
                    value=round(100 * (cs.loc[y, "India"] + ob.loc[y, "India"]) / (tot + ob.loc[y, "All countries"]), 2), url=BEA_URL))
    out.append(dict(source="BEA T2.3", metric="US computer-services imports, all countries, unaffiliated share %", year=y,
                    value=round(100 * cs.loc[y, "All countries, unaffiliated"] / tot, 2), url=BEA_URL))
# ---------- IMF: computer-services exports (SI2), all reporters
d = pd.read_csv(f"{raw}/imf_bop_si2_sj_all.csv")
a = d[(d.FREQUENCY == "A") & (d.INDICATOR == "SI2")].copy()
a["year"] = a.TIME_PERIOD.astype(str).str[:4].astype(int); a["usd_bn"] = a.OBS_VALUE / 1e9
p = a.pivot_table(index="COUNTRY", columns="year", values="usd_bn")
DELIV = ["IND", "PHL", "POL", "ROU", "UKR", "BRA", "CZE", "HUN", "SRB", "BGR", "PAK", "COL", "ARG", "CRI", "MYS", "LKA", "URY", "MAR",
         "IDN", "ARM", "GEO", "MDA", "BGD", "SLV", "TUN", "SVK", "LVA", "EST", "EGY", "MEX", "KAZ", "UZB"]
pe = p.reindex(DELIV)
pe.round(3).assign(url=IMF_URL).to_csv("imf_computer_exports_by_country.csv")
for span in [(2015, 2024), (2015, 2025), (2018, 2025)]:
    yrs = list(range(span[0], span[1] + 1))
    bal = p[yrs].dropna()
    bal = bal[(bal > 0).all(axis=1)]
    deliv = pe[yrs].dropna()
    for y in yrs:
        out.append(dict(source="IMF BOP SI2", metric=f"India share of world computer-services exports, balanced panel {span[0]}-{span[1]}, %", year=y,
                        value=round(100 * bal.loc["IND", y] / bal[y].sum(), 2), n_countries=len(bal), url=IMF_URL))
        out.append(dict(source="IMF BOP SI2", metric=f"India share excl. Ireland, balanced panel {span[0]}-{span[1]}, %", year=y,
                        value=round(100 * bal.loc["IND", y] / bal[y].drop("IRL").sum(), 2), n_countries=len(bal) - 1, url=IMF_URL))
        out.append(dict(source="IMF BOP SI2", metric=f"India share of emerging delivery-country group, balanced {span[0]}-{span[1]}, %", year=y,
                        value=round(100 * deliv.loc["IND", y] / deliv[y].sum(), 2), n_countries=len(deliv), url=IMF_URL,
                        note="group: " + " ".join(deliv.index)))
o = pd.DataFrame(out)
o.to_csv("india_share_summary.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 90)
print(o.pivot_table(index="metric", columns="year", values="value").round(1).to_string())
g = pe[[2019, 2022, 2023, 2024, 2025]].dropna()
g["cagr_19_22"] = 100 * ((g[2022] / g[2019]) ** (1 / 3) - 1); g["cagr_22_25"] = 100 * ((g[2025] / g[2022]) ** (1 / 3) - 1)
print(g.sort_values(2025, ascending=False).round(1).to_string())
