"""India vs emerging delivery countries, quarterly computer-services exports (IMF BOP SI2), H1 comparisons through 2026Q2."""
import sys, pandas as pd
d = pd.read_csv(f"{sys.argv[1]}/imf_bop_si2_sj_all.csv")
URL = d.url.iloc[0]
q = d[(d.FREQUENCY == "Q") & (d.INDICATOR == "SI2")].copy()
q["y"] = q.TIME_PERIOD.str[:4].astype(int); q["qq"] = q.TIME_PERIOD.str[-1].astype(int)
DELIV = ["IND", "PHL", "POL", "ROU", "UKR", "BRA", "CZE", "HUN", "SRB", "BGR", "PAK", "COL", "ARG", "CRI", "MYS", "LKA", "URY", "MAR",
         "IDN", "ARM", "GEO", "MDA", "BGD", "SLV", "TUN", "SVK", "LVA", "EST", "EGY", "MEX", "KAZ", "UZB"]
h1 = q[(q.qq <= 2) & q.COUNTRY.isin(DELIV)]
cnt = h1.groupby(["COUNTRY", "y"]).OBS_VALUE.agg(["sum", "count"])
cnt = cnt[cnt["count"] == 2]["sum"].unstack() / 1e9
yrs = list(range(2019, 2027))
bal = cnt[yrs].dropna()
out = pd.DataFrame({"year": yrs, "india_h1_usd_bn": bal.loc["IND", yrs].round(2).values, "group_h1_usd_bn": bal[yrs].sum().round(2).values,
                    "india_share_pct": (100 * bal.loc["IND", yrs] / bal[yrs].sum()).round(2).values})
out["others_h1_usd_bn"] = (out.group_h1_usd_bn - out.india_h1_usd_bn).round(2)
out["india_yoy_pct"] = (100 * out.india_h1_usd_bn.pct_change()).round(1); out["others_yoy_pct"] = (100 * out.others_h1_usd_bn.pct_change()).round(1)
out["countries"] = " ".join(bal.index); out["url"] = URL
out.to_csv("imf_h1_india_vs_delivery_group.csv", index=False)
print(out.drop(columns=["url"]).to_string())
