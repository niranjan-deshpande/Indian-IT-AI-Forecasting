"""EU27 imports of computer services (SI2) by selected partner + India shares. Input raw/eurostat_its6_eu27_imports.csv (fetch_eurostat.py)."""
import sys, pandas as pd
d = pd.read_csv(f"{sys.argv[1]}/eurostat_its6_eu27_imports.csv")
s = d[d.bop_item == "SI2"]
keep = ["EXT_EU27_2020", "IN", "US", "UK", "CH", "CN_X_HK", "PH", "EG", "MA", "MX", "BR", "AR", "SG", "CA", "RU", "TR", "JP"]
e = s[s.partner.isin(keep)][["partner", "partner_label", "time", "value_meur", "flag", "url"]]
e.to_csv("eurostat_eu27_computer_imports_by_partner.csv", index=False)
p = s.pivot_table(index="time", columns="partner", values="value_meur")
sh = pd.DataFrame({"india_share_of_extra_eu_pct": 100 * p.IN / p.EXT_EU27_2020,
                   "india_share_extra_eu_ex_US_UK_CH_pct": 100 * p.IN / (p.EXT_EU27_2020 - p.US - p.UK - p.CH),
                   "india_yoy_pct": 100 * p.IN.pct_change(), "extra_eu_yoy_pct": 100 * p.EXT_EU27_2020.pct_change()}).round(2)
sh["url"] = s.url.iloc[0]
sh.to_csv("eurostat_india_share.csv")
print(sh.drop(columns="url").to_string())
