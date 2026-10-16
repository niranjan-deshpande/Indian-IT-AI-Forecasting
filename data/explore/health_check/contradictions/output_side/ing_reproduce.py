"""Reproduce ING (Bhargava, 16 Sep 2026) as reported by Business Today (18 Sep 2026):
  (a) software services exports ~5.2% of GDP vs 3.3% pre-pandemic; business services 3.3% of GDP; ~$205bn
  (b) India's digitally delivered services exports +45% since 2022 vs +32% world.
Inputs: ../raw_output/imf/imf_bop_ind_q.csv (RBI BoP via IMF), ../raw_output/imf/weo_ngdpd.json (IMF WEO, India FY basis),
        ../raw_output/imf/imf_bop_all_annual_dds.csv (IMF BOP annual credits, all reporters),
        RBI software-exports survey totals (from data/explore/round3/sector_aggregates/exports_recomputed.csv).
Proxy for 'digitally delivered': UNCTAD/WTO 'digitally deliverable' BPM6 items SF+SG+SH+SI+SJ+SK1. WTO's own
'digitally delivered' estimate applies mode-1 shares to these items; the free API does not carry it.
Outputs: ing_gdp_shares.csv, ing_dds_growth.csv.  Run: python3 -I ing_reproduce.py
"""
import os, json, pandas as pd
OUT = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(OUT, "..", "raw_output", "imf")
REPO_EXPLORE = os.path.abspath(os.path.join(OUT, "..", "..", ".."))

# ---- (a) shares of GDP, Indian fiscal years ------------------------------------------------
q = pd.read_csv(os.path.join(RAW, "imf_bop_ind_q.csv"), low_memory=False)
q = q[(q.COUNTRY == "IND") & (q.BOP_ACCOUNTING_ENTRY == "CD_T")]
q = q.pivot_table(index="TIME_PERIOD", columns="INDICATOR", values="OBS_VALUE") / 1e9
q.index = pd.PeriodIndex([x.replace("-", "") for x in q.index], freq="Q")
# Indian FY t/t+1 = Apr t .. Mar t+1 = calendar Q2..Q4 of t + Q1 of t+1; label by starting year t
lab = [p.year if p.quarter >= 2 else p.year - 1 for p in q.index]
cnt = q.groupby(lab).size(); fy = q.groupby(lab).sum()[cnt == 4]
w = json.load(open(os.path.join(RAW, "weo_ngdpd.json")))["values"]["NGDPD"]["IND"]
gdp = pd.Series({int(k): v for k, v in w.items()})  # WEO India is FY-basis: 2025 = FY2025/26
surv = pd.read_csv(os.path.join(REPO_EXPLORE, "round3", "sector_aggregates", "exports_recomputed.csv"))
surv = surv[surv.series == "RBI survey total_usd_bn"].assign(y=lambda d: d.fy.str[:4].astype(int)).set_index("y").level
rows = []
for y in range(2015, 2026):
    if y not in fy.index: continue
    rows.append(dict(fy=f"FY{str(y+1)[2:]}", gdp_usd_bn_weo=gdp[y], bop_computer_SI2_usd_bn=round(fy.loc[y, "SI2"], 1),
                     bop_obs_SJ_usd_bn=round(fy.loc[y, "SJ"], 1),
                     computer_pct_gdp=round(fy.loc[y, "SI2"] / gdp[y] * 100, 2), obs_pct_gdp=round(fy.loc[y, "SJ"] / gdp[y] * 100, 2),
                     computer_plus_obs_pct_gdp=round((fy.loc[y, "SI2"] + fy.loc[y, "SJ"]) / gdp[y] * 100, 2),
                     rbi_survey_total_usd_bn=surv.get(y, None),
                     rbi_survey_pct_gdp=round(surv[y] / gdp[y] * 100, 2) if y in surv.index else None))
g = pd.DataFrame(rows); g.to_csv(os.path.join(OUT, "ing_gdp_shares.csv"), index=False)
print(g.to_string(index=False))
t4 = q.loc["2025Q3":"2026Q2"].sum()
print(f"\nTrailing 4q to 2026Q2: SI2 {t4.SI2:.1f}bn, SJ {t4.SJ:.1f}bn; over FY26 WEO GDP: {t4.SI2/gdp[2025]*100:.2f}% / {t4.SJ/gdp[2025]*100:.2f}%")

# ---- (b) digitally deliverable services growth, calendar 2022 -> 2025 ----------------------
a = pd.read_csv(os.path.join(RAW, "imf_bop_all_annual_dds.csv"), low_memory=False)
a = a[a.COUNTRY.notna() & (a.COUNTRY.str.len() == 3) & (a.BOP_ACCOUNTING_ENTRY == "CD_T")]
a = a.pivot_table(index=["COUNTRY", "TIME_PERIOD"], columns="INDICATOR", values="OBS_VALUE") / 1e9
items = ["SF", "SG", "SH", "SI", "SJ", "SK1"]
a["dds"] = a[items].sum(axis=1, min_count=4)  # require most items
a["dds_strict"] = a[items].sum(axis=1, min_count=6)
def growth(col, ctys=None, excl=()):
    x = a[col].unstack("TIME_PERIOD")[[2022, 2025]].dropna()
    if ctys is not None: x = x[x.index.isin(ctys)]
    x = x[~x.index.isin(excl)]
    return len(x), x[2022].sum(), x[2025].sum(), (x[2025].sum() / x[2022].sum() - 1) * 100
out = []
for col in ["dds", "dds_strict", "SI", "SJ", "S"]:
    for lab_, kw in [("India", dict(ctys=["IND"])), ("World balanced panel (reporters with 2022 and 2025)", {}),
                     ("World balanced ex India", dict(excl=("IND",))),
                     ("World balanced ex India, Ireland, Netherlands, Luxembourg", dict(excl=("IND", "IRL", "NLD", "LUX")))]:
        n, v22, v25, gr = growth(col, **kw)
        out.append(dict(measure=col, group=lab_, n_reporters=n, usd_bn_2022=round(v22, 1), usd_bn_2025=round(v25, 1), growth_2022_25_pct=round(gr, 1)))
o = pd.DataFrame(out); o.to_csv(os.path.join(OUT, "ing_dds_growth.csv"), index=False)
print(o.to_string(index=False))
