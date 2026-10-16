"""Chart-ready CSVs for section 6 (health of the business) and section 7 (demand signals) of the
health-check page, plus the business rows of the scorecard and a number-check table.

Run from anywhere:  python3 data/explore/health_check/charts/prep_business.py
Reads only existing repo files (never edits them). Requires ai_mentions_halfyear.csv from
count_ai_mentions.py (run that first; it needs the git-ignored transcripts under data/sources/).

Writes (all in data/explore/health_check/charts/):
  business_attrition.csv      firm x quarter LTM attrition 2016Q1-2026Q3, + 2016-19 mean
  business_utilization.csv    firm x quarter utilization (Infosys, Wipro, LTIM excl trainees; TechM incl)
  business_tcv_ttm.csv        firm x quarter trailing-12m deal TCV, USD bn and index (TTM to 2024Q1 = 100)
  business_labour_share.csv   FY16-FY26 labour share of value added, main + context series
  business_price_giveback.csv M2 AI-specific and gross give-back FY24-FY27 + broker / HCLTech reference bands
  demand_us_inhouse_share.csv US in-house share of computer occupations, OEWS May 2015-2025
  demand_ces5415_monthly.csv  CES NAICS 5415 employment, monthly Jan 2015 - latest
  demand_call_themes.csv      half-year x metric: A and D per transcript (coder 1) + AI mentions per 10k words
  scorecard_business.csv      business rows of the page scorecard
  numbers_business.csv        every number the prose may quote, with how it was computed
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
D = ROOT / "data"
EX = D / "explore"

CORE = "data/corrected/core_quarterly_final.csv"
UPD = "data/explore/health_check/contradictions/q2fy27_update.csv"
TOP6 = ["tcs", "infosys", "hcltech", "wipro", "techm", "ltim"]
NAMES = dict(tcs="TCS", infosys="Infosys", hcltech="HCLTech", wipro="Wipro", techm="TechM", ltim="LTIMindtree")

NUMBERS = []  # rows for numbers_business.csv


def num(key, value, unit, period, source_file, how):
    NUMBERS.append(dict(key=key, value=value, unit=unit, period=period, source_file=source_file, how_computed=how))


def write(df, name, header):
    with open(OUT / name, "w") as f:
        f.write(f"# {header}\n")
        df.to_csv(f, index=False)


core = pd.read_csv(ROOT / CORE)
upd = pd.read_csv(ROOT / UPD)
upd = upd[upd.status == "reported"]


def in_window(q, a, b):
    return (q >= a) & (q <= b)


# ---------------------------------------------------------------- 1a attrition
def ltim_predecessor(col):
    """Headcount-weighted LTI + Mindtree, quarters where both report `col` (pre-merger, 2016Q1-2021Q1)."""
    p = core[core.firm.isin(["lti", "mindtree"])].pivot(index="cal_q", columns="firm", values=[col, "headcount"])
    p = p[in_window(p.index, "2016Q1", "2021Q1")].dropna()
    w = p["headcount"]
    return ((p[col] * w).sum(axis=1) / w.sum(axis=1)).round(2)


rows = []
for f in TOP6:
    s = core[(core.firm == f) & (core.cal_q >= "2016Q1")].dropna(subset=["attrition"])
    for _, r in s.iterrows():
        rows.append(dict(firm=NAMES[f], cal_q=r.cal_q, attrition_ltm_pct=r.attrition, basis="panel"))
    u = upd[(upd.firm == f) & upd.attrition_ltm_pct.notna()]
    for _, r in u.iterrows():
        rows.append(dict(firm=NAMES[f], cal_q=r.cal_q, attrition_ltm_pct=r.attrition_ltm_pct,
                         basis="Q2FY27 update (q2fy27_update.csv)"))
for q, v in ltim_predecessor("attrition").items():
    rows.append(dict(firm="LTIMindtree", cal_q=q, attrition_ltm_pct=v,
                     basis="pre-merger: LTI+Mindtree headcount-weighted"))
att = pd.DataFrame(rows).sort_values(["firm", "cal_q"])
base = att[in_window(att.cal_q, "2016Q1", "2019Q4")].groupby("firm").attrition_ltm_pct.mean().round(1)
att["mean_2016_19_pct"] = att.firm.map(base)
att["mean_basis"] = np.where(att.firm == "LTIMindtree", "LTI+Mindtree headcount-weighted (pre-merger)", "own series")
att["source"] = np.where(att.basis.str.startswith("Q2FY27"), UPD, CORE)
write(att, "business_attrition.csv",
      "LTM attrition %, top-6, 2016Q1-2026Q3 (2026Q3 = Q2FY27 for TCS, HCLTech, Wipro, TechM only; Infosys/LTIM "
      "report 23 Oct / 16 Oct). Definitions differ by firm (TCS IT services; HCL excl involuntary; Wipro voluntary "
      "IT services; TechM IT); compare within firm only.")

latest = att[att.cal_q == "2026Q2"].set_index("firm").attrition_ltm_pct
peak = att[in_window(att.cal_q, "2021Q1", "2023Q4")].groupby("firm").attrition_ltm_pct.max()
peakq = att[in_window(att.cal_q, "2021Q1", "2023Q4")].sort_values("attrition_ltm_pct").groupby("firm").tail(1).set_index("firm").cal_q
num("attrition_2026Q2_min", latest.min(), "% LTM", "2026Q2", CORE, f"min across top-6 ({latest.idxmin()})")
num("attrition_2026Q2_max", latest.max(), "% LTM", "2026Q2", CORE, f"max across top-6 ({latest.idxmax()})")
for f in latest.index:
    num(f"attrition_2026Q2_{f}", latest[f], "% LTM", "2026Q2", CORE, "as reported")
    num(f"attrition_peak_2021_23_{f}", peak[f], "% LTM", peakq[f], CORE, "max of quarterly LTM attrition 2021Q1-2023Q4")
    num(f"attrition_mean_2016_19_{f}", base[f], "% LTM", "2016Q1-2019Q4", CORE,
        "mean of quarterly values" + (" (LTI+Mindtree headcount-weighted)" if f == "LTIMindtree" else ""))
num("attrition_peak_2022_min", peak.min(), "% LTM", "2022", CORE, f"lowest firm peak ({peak.idxmin()}, {peakq[peak.idxmin()]})")
num("attrition_peak_2022_max", peak.max(), "% LTM", "2022", CORE, f"highest firm peak ({peak.idxmax()}, {peakq[peak.idxmax()]})")
l3 = att[att.cal_q == "2026Q3"].set_index("firm").attrition_ltm_pct
num("attrition_2026Q3_range_4firms", f"{l3.min()}-{l3.max()}", "% LTM", "2026Q3 (Q2FY27)", UPD,
    "TCS, HCLTech, Wipro, TechM only: " + ", ".join(f"{k} {v}" for k, v in l3.items()))

# ---------------------------------------------------------------- 1b utilization
UTIL = dict(infosys=("util_excl", "excl. trainees"), wipro=("util_excl", "excl. trainees (IT services)"),
            techm=("util_incl", "incl. trainees"), ltim=("util_excl", "excl. trainees"))
rows = []
for f, (col, defn) in UTIL.items():
    s = core[(core.firm == f) & (core.cal_q >= "2016Q1")].dropna(subset=[col])
    for _, r in s.iterrows():
        rows.append(dict(firm=NAMES[f], cal_q=r.cal_q, utilization_pct=r[col], definition=defn, basis="panel"))
    u = upd[(upd.firm == f) & upd.utilization_pct.notna()]
    for _, r in u.iterrows():
        rows.append(dict(firm=NAMES[f], cal_q=r.cal_q, utilization_pct=r.utilization_pct, definition=defn,
                         basis="Q2FY27 update (q2fy27_update.csv)"))
ut = pd.DataFrame(rows).sort_values(["firm", "cal_q"])
ub = ut[in_window(ut.cal_q, "2016Q1", "2019Q4")].groupby("firm").utilization_pct.mean().round(1)
lti = core[(core.firm == "lti") & in_window(core.cal_q, "2016Q1", "2019Q4")].util_excl.mean().round(1)
ub["LTIMindtree"] = lti
ut["mean_2016_19_pct"] = ut.firm.map(ub)
ut["mean_basis"] = np.where(ut.firm == "LTIMindtree", "LTI only, excl. trainees (pre-merger; Mindtree def. differs)",
                            "own series")
ut["source"] = np.where(ut.basis.str.startswith("Q2FY27"), UPD, CORE)
write(ut, "business_utilization.csv",
      "Utilization %, by firm, 2016Q1-2026Q3. Within-firm comparison only. TCS (ends 2015Q4) and HCLTech (ends "
      "2019Q1) no longer report. TechM excl-trainee series ended 2025Q1, so TechM is incl. trainees throughout. "
      "2026Q3 from q2fy27_update.csv (Wipro, TechM).")
for f in ut.firm.unique():
    x = ut[ut.firm == f].set_index("cal_q").utilization_pct
    num(f"util_2026Q2_{f}", x.get("2026Q2"), "%", "2026Q2", CORE, UTIL[[k for k in NAMES if NAMES[k] == f][0]][1])
    num(f"util_mean_2016_19_{f}", ub[f], "%", "2016-19", CORE,
        "mean of quarterly values" + (" (LTI only, pre-merger)" if f == "LTIMindtree" else ""))
    if "2026Q3" in x.index:
        num(f"util_2026Q3_{f}", x["2026Q3"], "%", "2026Q3 (Q2FY27)", UPD, "as reported")
    pk = x[x.index >= "2020Q1"]
    num(f"util_peak_since2020_{f}", pk.max(), "%", pk.idxmax(), UPD if pk.idxmax() == "2026Q3" else CORE, "max since 2020Q1")

# ---------------------------------------------------------------- 1c TCV TTM
TCVDEF = dict(tcs="total TCV", infosys="large-deal TCV", hcltech="new deal wins TCV", wipro="large-deal TCV (>=$30m)",
              techm="net new deal wins", ltim="order inflow")
rows = []
for f in TOP6:
    s = core[core.firm == f].set_index("cal_q").tcv_q.sort_index()
    s = s[s.index >= "2019Q1"]
    full = pd.Series(index=pd.PeriodIndex(s.index, freq="Q"), data=s.values)
    full = full.reindex(pd.period_range(full.index.min(), full.index.max(), freq="Q"))
    ttm = full.rolling(4, min_periods=4).sum()
    for q, v in ttm.items():
        q = str(q)
        if q >= "2021Q1" and pd.notna(v):
            rows.append(dict(firm=NAMES[f], cal_q=q, tcv_ttm_usd_bn=round(v / 1000, 3), tcv_definition=TCVDEF[f]))
tcv = pd.DataFrame(rows)
b24 = tcv[tcv.cal_q == "2024Q1"].set_index("firm").tcv_ttm_usd_bn
tcv["index_ttm_2024Q1_eq_100"] = (tcv.tcv_ttm_usd_bn / tcv.firm.map(b24) * 100).round(1)
tcv["source"] = CORE + " tcv_q, 4-quarter rolling sum (consecutive quarters only)"
write(tcv, "business_tcv_ttm.csv",
      "Trailing-12-month deal value (TCV), USD bn, top-6, 2021Q1-2026Q2. Definitions differ by firm (see "
      "tcv_definition): levels are NOT comparable across firms; use the index (TTM to 2024Q1 = 100) for shape. "
      "Wipro did not report 2021Q4-2022Q1, so its TTM has one 2021Q3 point then resumes 2023Q1; HCLTech starts 2021Q4; LTIM 2023Q3. "
      "No 2026Q3 TCV in q2fy27_update.csv.")
for f in tcv.firm.unique():
    x = tcv[tcv.firm == f].set_index("cal_q").tcv_ttm_usd_bn
    num(f"tcv_ttm_2026Q2_{f}", x.get("2026Q2"), "USD bn", "2026Q2", CORE, f"sum of tcv_q 2025Q3-2026Q2 ({TCVDEF[[k for k in NAMES if NAMES[k]==f][0]]})")
    if "2025Q2" in x.index:
        num(f"tcv_ttm_2025Q2_{f}", x["2025Q2"], "USD bn", "2025Q2", CORE, "sum of tcv_q 2024Q3-2025Q2")

# ---------------------------------------------------------------- 2 labour share
ls = pd.read_csv(EX / "health_check/labour_share/chart1_labour_share_measures.csv")
LS = [("firm_top6_sum", "Top-6 firms", "main", "employee benefit expense / (employee cost + EBITDA), consolidated"),
      ("rbi_listed_it_op", "RBI listed IT companies", "main", "staff cost / (staff cost + operating profit), standalone, 192-274 firms (not a fixed panel)"),
      ("firm_mid3_sum", "Mid-tier (Persistent, Coforge, Mphasis)", "main", "as top-6"),
      ("klems_business_services", "KLEMS business services", "context", "labour income incl. imputed self-employed / GVA; IT + legal, consulting, R&D; ends FY23"),
      ("nas_group_privcorp_2011", "NAS group, private corporations (2011-12 base)", "context", "CE / GVA, broad NAS group (IT ~55-60%); ends FY24"),
      ("nas_group_privcorp_2022", "NAS group, private corporations (2022-23 base)", "context", "CE / GVA, new base, ~9 pts higher than old base; do not splice")]
ls = ls[ls.fy.str.match(r"20\d\d-\d\d") & (ls.fy >= "2015-16")]
rows = []
for col, name, role, defn in LS:
    for _, r in ls.dropna(subset=[col]).iterrows():
        fy = "FY" + r.fy[-2:]
        rows.append(dict(fy=fy, fiscal_year=r.fy, series=name, role=role, labour_share=round(r[col], 4), definition=defn))
lsl = pd.DataFrame(rows)
lsl["source"] = "data/explore/health_check/labour_share/chart1_labour_share_measures.csv"
write(lsl, "business_labour_share.csv",
      "Labour share of value added, FY16-FY26. role=main: firm/RBI accounts (plot solid); role=context: national-"
      "accounts measures with different scope (plot dashed, flagged). Ind AS 116 (FY20) lowers firm shares ~1-2 pts.")
L = lsl.set_index(["series", "fy"]).labour_share
for fy in ["FY16", "FY22", "FY23", "FY24", "FY25", "FY26"]:
    num(f"labour_share_top6_{fy}", round(L[("Top-6 firms", fy)], 3), "share", fy, "chart1_labour_share_measures.csv", "firm_top6_sum")
num("labour_share_rbi_listed_FY26", round(L[("RBI listed IT companies", "FY26")], 3), "share", "FY26", "chart1_labour_share_measures.csv", "rbi_listed_it_op")
num("labour_share_rbi_listed_FY24", round(L[("RBI listed IT companies", "FY24")], 3), "share", "FY24", "chart1_labour_share_measures.csv", "rbi_listed_it_op")
num("labour_share_mid3_FY26", round(L[("Mid-tier (Persistent, Coforge, Mphasis)", "FY26")], 3), "share", "FY26", "chart1_labour_share_measures.csv", "firm_mid3_sum")

# ---------------------------------------------------------------- 3 price give-back
m2 = pd.read_csv(EX / "round4/price_statements/m2_aggregate.csv")
m2 = m2[m2.segment == "IT top-6"]
rows = []
for _, r in m2.iterrows():
    status = "expected (FY27e)" if r.fy == "FY27" else "measured"
    rows.append(dict(series="M2 AI-specific give-back", fy=r.fy, low_pct_yr=r.low, central_pct_yr=r.central,
                     high_pct_yr=r.high, kind="estimate", status=status,
                     note="same-scope price give-back attributable to AI, top-6 revenue-weighted",
                     source="data/explore/round4/price_statements/m2_aggregate.csv"))
    rows.append(dict(series="M2 gross give-back (AI + pre-AI baseline 1.55)", fy=r.fy, low_pct_yr=r.gross_low,
                     central_pct_yr=r.gross_central, high_pct_yr=r.gross_high, kind="estimate", status=status,
                     note="AI increment + assumed pre-AI productivity give-back ~1.55%/yr",
                     source="data/explore/round4/price_statements/m2_aggregate.csv"))
BRK = "data/explore/health_check/contradictions/output_side/broker_deflation_vs_m2.csv"
for fy in ["FY26", "FY27"]:
    rows.append(dict(series="Broker deflation range (ICICI 2-3%, Kotak 3.5%)", fy=fy, low_pct_yr=2.0, central_pct_yr=np.nan,
                     high_pct_yr=3.5, kind="reference band", status="forecast",
                     note="gross forecasts; ICICI applies to ~30% 'traditional' segment (=0.6-0.9 pp of portfolio); "
                          "Kotak unit/horizon unstated; ICICI peak FY26-28", source=BRK))
rows.append(dict(series="HCLTech management: portfolio give-back", fy="FY27", low_pct_yr=2.0, central_pct_yr=np.nan,
                 high_pct_yr=3.0, kind="reference band", status="company expectation",
                 note="3-5%/yr in AI-disrupted services = 2-3%/yr of HCL portfolio, from FY27 (Apr 2026)", source=BRK))
for fy in ["FY26", "FY27"]:
    rows.append(dict(series="ICICI on whole portfolio (2-3% x ~30%)", fy=fy, low_pct_yr=0.6, central_pct_yr=np.nan,
                     high_pct_yr=0.9, kind="reference band", status="forecast, rescaled",
                     note="ICICI 2-3% applied to ~30% of revenue", source=BRK))
pg = pd.DataFrame(rows)
write(pg, "business_price_giveback.csv",
      "Price give-back, % per year. M2 = coded management statements (top-6 IT). FY24-26 measured, FY27 expected. "
      "Reference bands are forecasts on different bases (gross, partial portfolio): not like-for-like with M2 AI-specific.")
M = m2.set_index("fy")
for fy in ["FY25", "FY26", "FY27"]:
    num(f"giveback_ai_central_{fy}", round(M.central[fy], 2), "% per yr", fy, "m2_aggregate.csv", "IT top-6 central")
    num(f"giveback_ai_range_{fy}", f"{M.low[fy]:.2f}-{M.high[fy]:.2f}", "% per yr", fy, "m2_aggregate.csv", "IT top-6 low-high")
    num(f"giveback_gross_central_{fy}", round(M.gross_central[fy], 2), "% per yr", fy, "m2_aggregate.csv", "IT top-6 gross_central")
num("broker_deflation_range", "2-3.5", "% per yr", "FY26-FY28 forecasts", BRK, "ICICI 2-3% (traditional services) to Kotak 3.5% (pricing erosion)")
num("hcltech_portfolio_giveback", "2-3", "% per yr", "from FY27", BRK, "HCLTech management, Apr 2026")

# ---------------------------------------------------------------- 4 US in-house share and CES
oews = pd.read_csv(EX / "round4/demand_shift/oews_computer_occ_by_bucket.csv")
us = pd.DataFrame(dict(year=oews.year, survey_month="May",
                       inhouse_share_pct=(oews.inhouse_share_client_over_client_plus_5415 * 100).round(2),
                       comp_occ_client_inhouse_k=(oews.comp_client_all / 1000).round(1),
                       comp_occ_vendor_5415_k=(oews.comp_vendor_5415 / 1000).round(1),
                       soc_vintage=oews.soc_code))
us["source"] = "data/explore/round4/demand_shift/oews_computer_occ_by_bucket.csv"
write(us, "demand_us_inhouse_share.csv",
      "US computer occupations (SOC 15-1100/15-1200): in-house share = client industries / (client + NAICS 5415 "
      "vendors), BLS OEWS May. SOC break 2019 (15-1100 -> 15-1200). Client = finance/insurance + government + other "
      "private (excludes tech producers, 5416, 5613).")
for y in [2015, 2019, 2022, 2023, 2024, 2025]:
    num(f"us_inhouse_share_{y}", us.set_index("year").inhouse_share_pct[y], "%", f"May {y}", "oews_computer_occ_by_bucket.csv", "client/(client+5415)")
s1522 = us[us.year <= 2022].inhouse_share_pct
num("us_inhouse_share_2015_22_range", f"{s1522.min()}-{s1522.max()}", "%", "2015-2022", "oews_computer_occ_by_bucket.csv", "min-max")

ces = pd.read_csv(EX / "round3/offshore_competitors/bls_ces_monthly.csv")
ces["date"] = ces.year.astype(str) + "-" + ces.month.astype(str).str.zfill(2)
cm = pd.DataFrame(dict(date=ces.date, ces_5415_emp_k=ces.CES6054150001))
cm["yoy_pct"] = (cm.ces_5415_emp_k.pct_change(12) * 100).round(2)
pk = cm.loc[cm.ces_5415_emp_k.idxmax()]
cm["pct_from_peak"] = ((cm.ces_5415_emp_k / pk.ces_5415_emp_k - 1) * 100).round(2)
cm["source"] = "data/explore/round3/offshore_competitors/bls_ces_monthly.csv (BLS CES6054150001, SA, thousands)"
write(cm, "demand_ces5415_monthly.csv",
      f"US employment, NAICS 5415 computer systems design & related services (CES, SA, thousands), monthly "
      f"{cm.date.iloc[0]} to {cm.date.iloc[-1]}. Peak {pk.date}.")
lt = cm.iloc[-1]
num("ces5415_peak", pk.ces_5415_emp_k, "thousand", pk.date, "bls_ces_monthly.csv", "max of monthly SA series")
num("ces5415_latest", lt.ces_5415_emp_k, "thousand", lt.date, "bls_ces_monthly.csv", "last observation")
num("ces5415_latest_vs_peak_pct", lt.pct_from_peak, "%", f"{pk.date} to {lt.date}", "bls_ces_monthly.csv", "latest/peak-1")
num("ces5415_latest_vs_peak_k", round(lt.ces_5415_emp_k - pk.ces_5415_emp_k, 1), "thousand", f"{pk.date} to {lt.date}", "bls_ces_monthly.csv", "latest-peak")
num("ces5415_latest_yoy_pct", lt.yoy_pct, "%", lt.date, "bls_ces_monthly.csv", "vs same month a year earlier")
chk = pd.read_csv(EX / "round4/robustness/demand/oews_ces_check.csv")
may = cm[cm.date.str.endswith("-05")].assign(year=lambda x: x.date.str[:4].astype(int)).set_index("year").ces_5415_emp_k
diff = (chk.set_index("year").ces_may_5415_k - may).abs().max()
num("check_ces_may_vs_oews_ces_check_maxabsdiff", round(diff, 3), "thousand", "2015-2026", "oews_ces_check.csv", "max |May value difference| between the two files (0 = consistent)")
num("ces5415_may2026_yoy_pct", round((may[2026] / may[2025] - 1) * 100, 2), "%", "May 2026", "bls_ces_monthly.csv", "May 2026 vs May 2025")

# ---------------------------------------------------------------- 5 call themes
f3 = pd.read_csv(ROOT / "output/final/fig3_data.csv", header=[0, 1], skiprows=[2], index_col=0)
f3.index.name = "half_year"
ai = pd.read_csv(OUT / "ai_mentions_halfyear.csv", comment="#").set_index("half_year")
rows = []
for hy, r in f3.iterrows():
    n = int(r[("n_transcripts", "Unnamed: 16_level_1")]) if ("n_transcripts", "Unnamed: 16_level_1") in r.index else int(r.iloc[-1])
    for cat, lab in [("A", "A: demand weakness"), ("D", "D: AI productivity passed to clients")]:
        rows.append(dict(half_year=hy, metric=lab, value=r[("per_transcript", cat)], unit="statements per transcript",
                         n_calls=n, source="output/final/fig3_data.csv (coder 1, per_transcript)"))
        rows.append(dict(half_year=hy, metric=lab, value=r[("share_of_transcripts_with_any", cat)],
                         unit="share of transcripts with any", n_calls=n,
                         source="output/final/fig3_data.csv (coder 1, share_of_transcripts_with_any)"))
for hy, r in ai.iterrows():
    for k, lab in [("ai_any", "AI mentions"), ("genai", "GenAI / generative AI mentions"), ("agentic", "agentic / AI agent mentions")]:
        rows.append(dict(half_year=hy, metric=lab, value=r[f"{k}_per_10k_words"], unit="per 10k words",
                         n_calls=r.n_calls, source="charts/ai_mentions_halfyear.csv (count_ai_mentions.py)"))
        rows.append(dict(half_year=hy, metric=lab, value=r[f"{k}_per_call"], unit="per call",
                         n_calls=r.n_calls, source="charts/ai_mentions_halfyear.csv (count_ai_mentions.py)"))
ct = pd.DataFrame(rows)
write(ct, "demand_call_themes.csv",
      "Earnings-call themes by half-year, 8 firms (top-6 + Accenture + Cognizant), 2021H1-2026H2. 2026H2 = 8 calls "
      "(Jul-Oct 2026), so treat as partial. A/D are coded statements (coder 1; kappa 0.87); AI counts are keyword "
      "counts over full transcripts. Compare each metric over time, not levels across metrics.")
A = f3[("per_transcript", "A")]
Dd = f3[("per_transcript", "D")]
num("calls_A_per_transcript_peak", round(A.max(), 2), "per transcript", A.idxmax(), "fig3_data.csv", "max over half-years")
num("calls_A_per_transcript_2024H2_2026H1_range", f"{A['2024H2':'2026H1'].min():.2f}-{A['2024H2':'2026H1'].max():.2f}", "per transcript", "2024H2-2026H1", "fig3_data.csv", "min-max")
num("calls_A_per_transcript_2026H2", round(A["2026H2"], 2), "per transcript", "2026H2 (8 calls)", "fig3_data.csv", "")
num("calls_D_per_transcript_2022", f"{Dd['2022H1']:.2f}, {Dd['2022H2']:.2f}", "per transcript", "2022H1, 2022H2", "fig3_data.csv", "")
for hy in ["2025H1", "2026H1", "2026H2"]:
    num(f"calls_D_per_transcript_{hy}", round(Dd[hy], 2), "per transcript", hy, "fig3_data.csv", "")
num("calls_D_share_with_any_2026H2", f3[("share_of_transcripts_with_any", "D")]["2026H2"], "share", "2026H2 (8 calls)", "fig3_data.csv", "")
for hy in ["2022H2", "2023H1", "2023H2", "2024H2", "2025H2", "2026H1", "2026H2"]:
    num(f"ai_mentions_per_10k_{hy}", ai.ai_any_per_10k_words[hy], "per 10k words", f"{hy} ({ai.n_calls[hy]} calls)", "ai_mentions_halfyear.csv", "ai_any pooled")
    num(f"ai_mentions_per_call_{hy}", ai.ai_any_per_call[hy], "per call", hy, "ai_mentions_halfyear.csv", "ai_any / n_calls")
num("ai_mentions_per_10k_2021_22_range", f"{ai.ai_any_per_10k_words[:'2022H2'].min()}-{ai.ai_any_per_10k_words[:'2022H2'].max()}", "per 10k words", "2021H1-2022H2", "ai_mentions_halfyear.csv", "min-max")
num("genai_per_10k_peak", ai.genai_per_10k_words.max(), "per 10k words", ai.genai_per_10k_words.idxmax(), "ai_mentions_halfyear.csv", "max")
num("agentic_per_10k_2026H1", ai.agentic_per_10k_words["2026H1"], "per 10k words", "2026H1", "ai_mentions_halfyear.csv", "")

# ---------------------------------------------------------------- scorecard
sc = pd.DataFrame([
    dict(indicator="Attrition (LTM), top-6", latest=f"{latest.min()}-{latest.max()}%", period="2026Q2 (Q1FY27)",
         comparison=f"2022 peaks {peak.min()}-{peak.max()}%; below 2016-19 mean at 5 of 6 (TCS above)",
         direction="normal", source=CORE),
    dict(indicator="Labour share of value added, top-6", latest=f"{L[('Top-6 firms','FY26')]:.3f}", period="FY26",
         comparison=f"FY22 {L[('Top-6 firms','FY22')]:.3f}, FY24 {L[('Top-6 firms','FY24')]:.3f}; RBI listed IT {L[('RBI listed IT companies','FY26')]:.3f}",
         direction="flat", source="data/explore/health_check/labour_share/chart1_labour_share_measures.csv"),
    dict(indicator="AI price give-back (M2, top-6)", latest=f"{M.central['FY26']:.2f}% FY26; {M.central['FY27']:.2f}% FY27e",
         period="FY26 / FY27e", comparison=f"FY26 range {M.low['FY26']:.2f}-{M.high['FY26']:.2f}; FY27e {M.low['FY27']:.2f}-{M.high['FY27']:.2f}; gross FY27e {M.gross_central['FY27']:.2f}",
         direction="rising from low base", source="data/explore/round4/price_statements/m2_aggregate.csv"),
])
write(sc, "scorecard_business.csv", "Business rows for the page scorecard (built by prep_business.py)")

nb = pd.DataFrame(NUMBERS)
write(nb, "numbers_business.csv", "Numbers the business/demand prose may quote, recomputed from repo files by prep_business.py")
print(nb.to_string(index=False))
