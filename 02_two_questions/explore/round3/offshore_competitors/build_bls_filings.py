"""BLS CES annual averages (computer systems design 5415; professional & technical services 54) and Cognizant 10-K headcount by location."""
import json, sys, pandas as pd
raw = sys.argv[1]
URL = "https://api.bls.gov/publicAPI/v1/timeseries/data/ (series CES6054150001, CES6054000001; SA, thousands)"
rows = []
for f in ["bls_ces_2015_2024.json", "bls_ces_2025_2026.json"]:
    for s in json.load(open(f"{raw}/{f}"))["Results"]["series"]:
        for o in s["data"]:
            rows.append(dict(series=s["seriesID"], year=int(o["year"]), month=int(o["period"][1:]), value_k=float(o["value"])))
b = pd.DataFrame(rows)
m = b.pivot_table(index=["year", "month"], columns="series", values="value_k").reset_index()
m["url"] = URL
m.to_csv("bls_ces_monthly.csv", index=False)
jan_sep = b[b.month <= 9].groupby(["series", "year"]).value_k.mean().unstack(0).round(1)
print("Jan-Sep averages\n", jan_sep, "\nYoY %\n", (100 * jan_sep.pct_change()).round(1))
c = pd.DataFrame([
    (2021, 330600, 240000, 40900, 15700, 8100, None, "ctsh-20211231.htm", "https://www.sec.gov/Archives/edgar/data/1058290/000105829022000023/ctsh-20211231.htm"),
    (2022, 355300, 258500, 41100, 18200, 9200, 28300, "ctsh-20221231.htm", "https://www.sec.gov/Archives/edgar/data/1058290/000105829023000027/ctsh-20221231.htm"),
    (2023, 347700, 254000, 40500, 16300, 8500, 28400, "ctsh-20231231.htm", "https://www.sec.gov/Archives/edgar/data/1058290/000105829024000017/ctsh-20231231.htm"),
    (2024, 336800, 241500, 42800, 15700, 8200, 28600, "ctsh-20241231.htm", "https://www.sec.gov/Archives/edgar/data/1058290/000105829025000017/ctsh-20241231.htm"),
    (2025, 351600, 256900, 41600, 14600, 7800, 30700, "ctsh-20251231.htm", "https://www.sec.gov/Archives/edgar/data/1058290/000105829026000008/ctsh-20251231.htm")],
    columns=["year_end", "total", "india", "north_america", "continental_europe", "uk", "rest_of_world_ex_india", "doc", "url"])
c["india_share_pct"] = (100 * c.india / c.total).round(1)
c["note"] = "10-K Item 1 Human Capital/Workforce sentence; 2021 10-K gives 'rest of world 265,900 including 240,000 in India'"
c.to_csv("cognizant_headcount_by_location.csv", index=False)
print(c[["year_end", "total", "india", "india_share_pct", "rest_of_world_ex_india"]])
