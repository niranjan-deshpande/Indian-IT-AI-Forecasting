"""Recompute India software/computer-services export growth by Indian fiscal year (Apr-Mar)
from repo CSVs: (a) RBI annual software-exports survey (trade/rbi_survey_orgtype.csv),
(b) RBI BoP via IMF quarterly (trade/imf_bop_india_services_quarterly.csv). Run with python3 -I."""
import sys, pathlib, pandas as pd
here = pathlib.Path(__file__).resolve().parent
trade = here.parent.parent / "trade"
out = []
s = pd.read_csv(trade / "rbi_survey_orgtype.csv")
s = s.set_index("fy")
for c in ["total_usd_bn", "private_ltd_usd_bn", "public_ltd_usd_bn"]:
    g = (s[c] / s[c].shift(1) - 1) * 100
    for fy in ["2022-23", "2023-24", "2024-25", "2025-26"]:
        out.append(dict(series=f"RBI survey {c}", fy=fy, level=s.loc[fy, c], yoy_pct=round(g.loc[fy], 1),
                        source_url=s.loc[fy, "source_url"]))
m = pd.read_csv(trade / "imf_bop_india_services_quarterly.csv")
m = m[m.BOP_ACCOUNTING_ENTRY == "CD_T"].copy()
y = m.TIME_PERIOD.str[:4].astype(int); q = m.TIME_PERIOD.str[-1].astype(int)
m["fy_end"] = y + (q >= 2).astype(int)   # Q2(Apr-Jun) starts FY ending next March
lab = {"SI2": "BoP computer services exports", "S": "BoP total services exports", "SJ": "BoP other business services exports"}
for ind, name in lab.items():
    d = m[m.INDICATOR == ind].groupby("fy_end").agg(v=("OBS_VALUE", "sum"), n=("OBS_VALUE", "size"))
    d = d[d.n == 4]; d["bn"] = d.v / 1e9; d["g"] = (d.bn / d.bn.shift(1) - 1) * 100
    for fe in range(2019, 2027):
        if fe in d.index:
            out.append(dict(series=name + " (USD bn, sum of 4 qtrs)", fy=f"{fe-1}-{str(fe)[2:]}", level=round(d.loc[fe, "bn"], 1),
                            yoy_pct=round(d.loc[fe, "g"], 1), source_url=m.url.iloc[0]))
o = pd.DataFrame(out); o.to_csv(here / "exports_recomputed.csv", index=False); print(o.to_string())
