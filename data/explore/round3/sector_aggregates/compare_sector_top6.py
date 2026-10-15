"""FY23->FY26 cumulative growth: sector-wide series vs top six. Values typed from sector_series_pulled.csv /
exports_recomputed.csv / midtier_vs_top6.csv (repo). Run: python3 -I compare_sector_top6.py"""
import pathlib, pandas as pd
here = pathlib.Path(__file__).resolve().parent
top = pd.read_csv(here.parent.parent / "midtier" / "midtier_vs_top6.csv").set_index("fiscal_year")
R = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63625 ; prid=61562 ; prid=58937"
B = "https://api.imf.org/external/sdmx/2.1/data/IMF.STA,BOP/IND.CD_T+DB_T.SI+SI2+SJ+S.USD.Q?startPeriod=2004"
N = "https://www.etvbharat.com/en/business/india-fy26-tech-revenues-hit-usd-315-billion-enn26022404879 ; https://www.outlookbusiness.com/news/tech-industry-revenue-to-touch-usd-254-bn-this-fiscal-nasscom"
rows = [  # name, start(FY23 or as noted), end(FY26), unit, kind, url, note
 ("Top-6 revenue (global, USD)", top.loc["FY23","top6_rev_usd_mn"], top.loc["FY26","top6_rev_usd_mn"], "USD mn", "firm filings", "repo data/explore/midtier/midtier_vs_top6.csv", ""),
 ("Top-6 headcount (global, FY-end)", top.loc["FY23","top6_headcount"], top.loc["FY26","top6_headcount"], "persons", "firm filings", "repo data/explore/midtier/midtier_vs_top6.csv", ""),
 ("Mid-4 revenue (USD)", top.loc["FY23","mid4_rev_usd_mn"], top.loc["FY26","mid4_rev_usd_mn"], "USD mn", "firm filings", "repo data/explore/midtier/midtier_vs_top6.csv", "includes acquisitions"),
 ("Mid-4 headcount", top.loc["FY23","mid4_headcount"], top.loc["FY26","mid4_headcount"], "persons", "firm filings", "repo data/explore/midtier/midtier_vs_top6.csv", ""),
 ("RBI survey software exports, all exporters", 185.5, 221.4, "USD bn", "official survey", R, "FY23 from a different release vintage"),
 ("RBI survey exports, public-limited cos", 77.0, 81.7, "USD bn", "official survey", R, "~large listed vendors"),
 ("RBI survey exports, private-limited cos", 104.1, 134.6, "USD bn", "official survey", R, "~GCCs + MNC vendors + unlisted Indian firms"),
 ("BoP computer services exports (RBI via IMF)", 146.8, 203.7, "USD bn", "official BoP", B, "sum of 4 quarters; excludes ITeS/BPO (in other business services)"),
 ("Nasscom industry revenue, chained within-vintage", 100.0, 100*1.038*1.059*1.061, "index", "industry body", N, "growth FY24 3.8 (SR2024), FY25 5.9 (SR2026 revised), FY26 6.1 (SR2026); incl. domestic + hardware"),
 ("Nasscom direct employment, chained net adds", 5.37, 5.37+0.060+0.133+0.135, "million", "industry body", N, "FY23 base = 5.43m - 60k (SR2024); FY25/26 net adds from SR2026"),
 ("Nasscom employment minus top-6 headcount (rough)", 5.37e6-top.loc["FY23","top6_headcount"], 5.698e6-top.loc["FY26","top6_headcount"], "persons", "derived", N, "top-6 headcount is global, Nasscom is India -> residual understated in level; growth indicative only"),
]
out = []
for n, a, b, u, k, url, note in rows:
    out.append(dict(series=n, kind=k, unit=u, fy23=round(a, 3), fy26=round(b, 3), cum_growth_pct=round((b/a-1)*100, 1),
                    annualised_pct=round(((b/a)**(1/3)-1)*100, 1), source_url=url, note=note))
o = pd.DataFrame(out); o.to_csv(here / "sector_vs_top6_fy23_fy26.csv", index=False); print(o.drop(columns=["source_url"]).to_string())
