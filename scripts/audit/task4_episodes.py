"""Audit Task 1b, item 4: is 2023 / FY23 missing from the REPORT §3 episode table?

Outputs (ROOT/audit/):
  episode_row_quarter_map.csv  every calendar quarter 2015Q2-2026Q2 with its Indian / Accenture fiscal label and
                               the REPORT §3 rows that contain it
  episode_row_fy_counts.csv    number of quarters of each Indian FY inside each REPORT row
  latest_quarter_by_firm.csv   last quarter with data per firm (cal_q and own fiscal label)
  episodes_relabelled.csv      REPORT §3 table recomputed, with calendar + Indian-FY + Accenture-FY labels,
                               under the pilot entity set (reproduces REPORT) and a clean 6-entity set
  episodes_fiscal.csv          same metrics on Indian fiscal-year windows (FY16-FY22 ex-COVID, FY23, FY24, FY25,
                               FY26, Q1FY27)
Statistic (as in the pilot): for each firm, mean of quarterly YoY values in the window; group value = mean across
firms with data. n_firms_<m> and n_firmq_<m> give the number of firms and firm-quarters behind each cell.
"""
import argparse
import numpy as np
import pandas as pd
from audit_common import (AUD, EXCL, INDIAN_ALL, qrange, indian_fiscal, indian_fy, accenture_fiscal,
                          load_yoy, load_core, ltim_chain)

ap = argparse.ArgumentParser()
ap.add_argument("--yoy", default=None)
ap.add_argument("--core", default=None)
ap.add_argument("--tag", default="")
args = ap.parse_args()
yoy, core = load_yoy(args.yoy), load_core(args.core)
M = ["gR", "gL", "gRPE", "du", "resid"]

# REPORT §3 rows, as computed (2015-22 and pre-COVID rows are not produced by any saved script; the definitions
# below reproduce the published numbers exactly: see findings_1b.md §4)
REPORT_ROWS = {
    "2015–22 (ex-COVID)": ("2015Q2", "2022Q4", EXCL),
    "pre-COVID 2015–19": ("2015Q2", "2020Q1", []),
    "COVID (2020Q2–Q4)": ("2020Q2", "2020Q4", []),
    "FY24 slowdown (2023Q1–2024Q1)": ("2023Q1", "2024Q1", []),
    "FY25–27 (2024Q2–2026Q2)": ("2024Q2", "2026Q2", []),
}

# ------------------------------------------------------------------ quarter map
qs = qrange("2015Q2", "2026Q2")
rows = []
for q in qs:
    r = dict(cal_q=q, indian_fq=indian_fiscal(q), indian_FY=f"FY{indian_fy(q) % 100:02d}",
             accenture_fq_assigned=accenture_fiscal(q), cognizant_q=q, covid_excluded=q in EXCL)
    inrows = [k for k, (a, b, ex) in REPORT_ROWS.items() if a <= q <= b and q not in ex]
    r["report_rows"] = "; ".join(inrows) if inrows else "(none)"
    r["n_report_rows"] = len(inrows)
    rows.append(r)
qmap = pd.DataFrame(rows)
qmap.to_csv(AUD / f"episode_row_quarter_map{args.tag}.csv", index=False)

fyc = []
for k, (a, b, ex) in REPORT_ROWS.items():
    sub = qmap[(qmap.cal_q >= a) & (qmap.cal_q <= b) & (~qmap.cal_q.isin(ex))]
    for fy, g in sub.groupby("indian_FY"):
        fyc.append(dict(report_row=k, indian_FY=fy, n_quarters=len(g), fiscal_quarters=",".join(g.indian_fq),
                        accenture_quarters=",".join(g.accenture_fq_assigned)))
pd.DataFrame(fyc).to_csv(AUD / f"episode_row_fy_counts{args.tag}.csv", index=False)

# ------------------------------------------------------------------ latest quarter per firm
lat = []
for f, g in yoy.groupby("firm"):
    for m in ["gR", "gL"]:
        s = g[g[m].notna()]
        q = s.cal_q.max() if len(s) else None
        lab = (accenture_fiscal(q) if f == "accenture" else q if f == "cognizant" else indian_fiscal(q)) if q else None
        lat.append(dict(firm=f, metric=m, first_cal_q=s.cal_q.min() if len(s) else None, last_cal_q=q, last_own_fiscal_label=lab))
pd.DataFrame(lat).to_csv(AUD / f"latest_quarter_by_firm{args.tag}.csv", index=False)


# ------------------------------------------------------------------ episode statistics
def entity_panel(scheme):
    if scheme == "pilot":            # every Indian entity in yoy_metrics, as in 03_part2.episode_table
        return yoy[yoy.firm.isin(INDIAN_ALL)]
    if scheme == "clean6":           # 5 firms + one LTI-group chain (no triple counting of the LTI business)
        return pd.concat([yoy[yoy.firm.isin(["tcs", "infosys", "hcltech", "wipro", "techm"])], ltim_chain(yoy, core)])
    raise ValueError(scheme)


def window_stats(panel, a, b, ex):
    d = panel[(panel.cal_q >= a) & (panel.cal_q <= b) & (~panel.cal_q.isin(ex))]
    fm = d.groupby("firm")[M].mean()
    out = {m: fm[m].mean() for m in M}
    out.update({f"n_firms_{m}": int(fm[m].notna().sum()) for m in ["gR", "gL", "du"]})
    out.update({f"n_firmq_{m}": int(d[m].notna().sum()) for m in ["gR", "gL", "du"]})
    out["gR_minus_gL"] = out["gR"] - out["gL"]
    out["firms_gL"] = ",".join(fm.index[fm.gL.notna()])
    return out


def labels(a, b, ex):
    q = [x for x in qrange(a, b) if x not in ex]
    fys = pd.Series([f"FY{indian_fy(x) % 100:02d}" for x in q]).value_counts().sort_index()
    return dict(cal_window=f"{a}–{b}" + (" ex 2020Q2–2021Q2" if ex else ""), n_cal_quarters=len(q),
                indian_fiscal_window=f"{indian_fiscal(a)}–{indian_fiscal(b)}",
                indian_FY_quarter_counts=", ".join(f"{k}:{v}" for k, v in fys.items()),
                accenture_fiscal_window=f"{accenture_fiscal(a)}–{accenture_fiscal(b)} (Accenture FY ends Aug)",
                cognizant_window=f"{a}–{b} (calendar FY)")


def table(windows):
    out = []
    for name, (a, b, ex) in windows.items():
        lab = labels(a, b, ex)
        for scheme in ["pilot", "clean6"]:
            out.append(dict(row=name, group="Indian", entity_set=scheme, **lab, **window_stats(entity_panel(scheme), a, b, ex)))
        for comp in ["accenture", "cognizant"]:
            out.append(dict(row=name, group=comp, entity_set="single firm", **lab, **window_stats(yoy[yoy.firm == comp], a, b, ex)))
    return pd.DataFrame(out)


rel = table(REPORT_ROWS)
rel.to_csv(AUD / f"episodes_relabelled{args.tag}.csv", index=False)

FISCAL = {
    "FY16–FY22 ex-COVID (Q1FY16–Q4FY22)": ("2015Q2", "2022Q1", EXCL),
    "FY23 (Q1–Q4FY23)": ("2022Q2", "2023Q1", []),
    "FY24 (Q1–Q4FY24)": ("2023Q2", "2024Q1", []),
    "FY25 (Q1–Q4FY25)": ("2024Q2", "2025Q1", []),
    "FY26 (Q1–Q4FY26)": ("2025Q2", "2026Q1", []),
    "Q1FY27": ("2026Q2", "2026Q2", []),
    "FY25–Q1FY27 (= REPORT 'FY25–27' row)": ("2024Q2", "2026Q2", []),
}
fis = table(FISCAL)
fis.to_csv(AUD / f"episodes_fiscal{args.tag}.csv", index=False)

pd.set_option("display.width", 250)
cols = ["row", "group", "entity_set", "gR", "gL", "gRPE", "du", "resid", "gR_minus_gL", "n_firms_gR", "n_firms_gL", "n_firms_du"]
print(rel[cols].round(1).to_string())
print(fis[cols].round(1).to_string())
print(pd.DataFrame(fyc).to_string())
print(qmap[qmap.n_report_rows != 1][["cal_q", "indian_fq", "report_rows"]].to_string())
