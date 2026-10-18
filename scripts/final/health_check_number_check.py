"""Check every number in the health-check page text (health_check_text.md) against its source -> health_check_number_check.md.

    python3 scripts/final/health_check_number_check.py

Modelled on note_number_check.py. Reads the TEXT FILE (prose, Tables 1-2, figure captions, details blocks and
footnotes; the HTML comment block and the YAML front matter are skipped), not the built HTML.

Each entry gives the number as printed, where it appears, the source file and row, and how it is checked:
  - num(): CSV numbers are recomputed from the file. Passes if the source value rounds to the printed value at the
    printed precision ("about 7%" passes for 6.5 <= v <= 7.5). A value exactly on the rounding boundary that
    half-up rounding would send the other way (185.5 printed as 185) passes but is flagged "borderline".
  - rng(): ranges ("12–14%") pass if every source value lies in the printed range at the printed precision and the
    ends round to the printed ends.
  - cond(): word claims ("roughly flat", "kept falling", "about a third") are tested as explicit conditions.
  - txt(): numbers that come only from documents (external reports, press, our FINDINGS write-ups) pass if the
    cited text is found verbatim in the cited repo file. Labelled 'external' when the number is someone else's.
Growth conventions: the page says "Growth rates are log changes unless stated". Where a printed figure is an
ordinary percent (e.g. "about 16% below trend" = 17.8 log points = 16.3%), the entry says which convention it tests.
A final pass lists numeric tokens in the text that no entry covers.
"""
import math
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
TEXT = ROOT / "health_check_text.md"
OUT = ROOT / "health_check_number_check.md"
HC = ROOT / "data/explore/health_check"
CH = HC / "charts"
MINUS = "−"
ENTRIES = []


def rd(path, **kw):
    return pd.read_csv(ROOT / path, comment=kw.pop("comment", None), **kw)


def rounds_to(v, shown, digits):
    return abs(v - shown) <= 0.5 * 10 ** -digits + 1e-9


def borderline(v, shown, digits):
    """True if v sits exactly on the rounding boundary and half-up rounding gives something other than `shown`."""
    unit = 10 ** -digits
    on_edge = abs(abs(v - shown) - 0.5 * unit) < 1e-9
    half_up = math.floor(v / unit + 0.5 + 1e-12) * unit
    return on_edge and abs(half_up - shown) > 1e-9


def add(printed, where, source, key, repo, ok, kind="data", note=""):
    ENTRIES.append(dict(printed=printed, where=where, source=source, key=key, repo=repo, ok=bool(ok), kind=kind, note=note))


def num(printed, where, source, key, value, shown, digits=0, kind="data", note=""):
    v = float(value)
    ok = rounds_to(v, shown, digits)
    if ok and borderline(v, shown, digits):
        note = (note + "; " if note else "") + f"borderline: half-up rounding of {v:g} gives {math.floor(v / 10 ** -digits + 0.5) * 10 ** -digits:g}"
    add(printed, where, source, key, v, ok, kind, note)


def rng(printed, where, source, key, values, lo, hi, digits=0, kind="data", note=""):
    vals = [float(v) for v in values]
    tol = 0.5 * 10 ** -digits + 1e-9
    ok = all(lo - tol <= v <= hi + tol for v in vals) and rounds_to(min(vals), lo, digits) and rounds_to(max(vals), hi, digits)
    if ok and (borderline(min(vals), lo, digits) or borderline(max(vals), hi, digits)):
        note = (note + "; " if note else "") + "borderline end value"
    add(printed, where, source, key, ", ".join(f"{v:.3f}".rstrip("0").rstrip(".") for v in vals), ok, kind, note)


def cond(printed, where, source, key, value, ok, kind="data", note=""):
    add(printed, where, source, key, value, ok, kind, note)


def txt(printed, where, source, needle, kind="external", note=""):
    p = ROOT / source
    ok = p.exists() and needle in p.read_text(encoding="utf-8")
    add(printed, where, source, f'text: "{needle}"', "found verbatim" if ok else "NOT FOUND", ok, kind, note)


def logx(a, b):
    return 100 * math.log(b / a)


def pct(a, b):
    return 100 * (b / a - 1)


# ------------------------------------------------------------------ data
NO, NJ = "data/explore/health_check/charts/numbers_output.csv", "data/explore/health_check/charts/numbers_jobs.csv"
nout = rd(NO).set_index("key").value
njob = rd(NJ).set_index("key").value
nbus = rd("data/explore/health_check/charts/numbers_business.csv", comment="#").set_index("key").value

EO = "data/explore/health_check/charts/exports_orgtype.csv"
eo = rd(EO)
tot = eo.groupby("fy").total_exports_usd_bn.first()
priv = eo[eo.exporter_type == "private_ltd"].set_index("fy").share_pct
EA = "data/explore/health_check/charts/exports_activity.csv"
ea = rd(EA).pivot_table(index="fy", columns="activity", values="exports_usd_bn")
eay = rd(EA).pivot_table(index="fy", columns="activity", values="yoy_usd_pct")
IW = "data/explore/health_check/charts/india_world_share.csv"
iw = rd(IW).pivot_table(index="year", columns="denominator", values="india_share_pct")
iwn = rd(IW).groupby("denominator").n_countries.max()
H1 = "data/explore/health_check/charts/india_h1_growth.csv"
h1 = rd(H1).set_index(["year", "group"])
RG = "data/explore/health_check/charts/revgrowth_peers.csv"
rg = rd(RG)
g = lambda s, b, p, c="growth_logx100": float(rg[(rg.series == s) & (rg.currency_basis == b) & (rg.period == p)][c].iloc[0])
RT = "data/explore/health_check/charts/rev_trend_levels.csv"
rt = rd(RT)
gap = lambda s, m, c: float(rt[(rt.fy == "FY26") & (rt.series == s) & (rt.metric == m)][c].iloc[0])
FC = "data/explore/health_check/charts/firm_cc_quarterly.csv"
fc = rd(FC)
SC = "data/explore/health_check/charts/segment_change.csv"
sc = rd(SC).set_index("segment")
TH = "data/explore/health_check/charts/top6_headcount.csv"
th = rd(TH).pivot_table(index="cal_q", columns="firm", values="headcount_persons", aggfunc="sum")
top = th["top6"]
five = th[["tcs", "infosys", "hcltech", "wipro", "techm"]].sum(axis=1)
RV = "data/explore/health_check/charts/rev_vs_hc.csv"
rv = rd(RV)
rvq = rv[rv.metric == "revenue_per_employee_annualised"].set_index("period").value
rvf = rv[rv.freq == "FY"].pivot_table(index="period", columns="metric", values="value")
Q2 = "data/explore/health_check/contradictions/q2fy27_update.csv"
q2 = rd(Q2).set_index("firm")
SE = "data/explore/health_check/charts/sector_employment.csv"
se = rd(SE)
sev = lambda s, p, vint=None: float(se[(se.series == s) & (se.period == p) & (se.vintage.str.contains(vint) if vint else True)].value_persons.iloc[0])
PC = "data/explore/health_check/contradictions/plfs_change_ci.csv"
pc = rd(PC).set_index(["series", "from_round", "to_round"])
pc1 = pc.loc[("nic62_63", "2022-23", "cy2025")]
FI = "data/explore/health_check/charts/fresher_intake.csv"
fi = rd(FI)
fsum = fi[fi.series == "sum_tcs_infosys_hcltech"].set_index("fy").value_persons
fv = lambda s, fy, kind=None: fi[(fi.series == s) & (fi.fy == fy) & ((fi.kind == kind) if kind else True)].value_persons.iloc[0]
FS = "data/explore/health_check/charts/four_shares.csv"
fs = rd(FS)
fsv = lambda s, p: float(fs[(fs.series == s) & (fs.period == p)].share_pct.iloc[0])
PL, EP = "plfs_it_share_salaried_grads_21_25", "epfo_it_share_net_payroll_18_25_annual"
JP = "data/explore/health_check/charts/junior_pay.csv"
jp = rd(JP)
jpv = lambda r, s, a: float(jp[(jp["round"] == r) & (jp["sample"] == s) & (jp.age_band == a)].mean_real_inr_month.iloc[0])
U30 = "data/explore/health_check/charts/under30.csv"
u30 = rd(U30)
IG = "data/explore/health_check/charts/infosys_grades.csv"
ig = rd(IG)
igv = lambda fy: float(ig[(ig.fy == fy) & (ig.band == "junior")].share_pct.iloc[0])
NI = "data/explore/health_check/charts/nirf.csv"
ni = rd(NI)
niw = ni[(ni.comparison == "within_edition") & (ni.tier == "all")].set_index("grad_year")
GU = "data/explore/health_check/charts/grad_unemp.csv"
gu = rd(GU)
guv = lambda r, c, a="15-25": float(gu[(gu["round"] == r) & (gu.concept == c) & (gu.age == a)].ur_pct.iloc[0])
PE = "data/explore/health_check/charts/postings_experience.csv"
pe = rd(PE).set_index("category")
AT = "data/explore/health_check/charts/business_attrition.csv"
at = rd(AT, comment="#")
UT = "data/explore/health_check/charts/business_utilization.csv"
ut = rd(UT, comment="#")
TV = "data/explore/health_check/charts/business_tcv_ttm.csv"
tv = rd(TV, comment="#").pivot_table(index="cal_q", columns="firm", values="tcv_ttm_usd_bn")
LS = "data/explore/health_check/charts/business_labour_share.csv"
ls = rd(LS, comment="#").pivot_table(index="fy", columns="series", values="labour_share")
FL = "data/explore/health_check/labour_share/firm_labour_share.csv"
fl = rd(FL)
t6 = fl[fl.firm == "top6_sum"].set_index("fy")
GB = "data/explore/health_check/charts/business_price_giveback.csv"
gb = rd(GB, comment="#")
gbv = lambda s, fy, c="central_pct_yr": float(gb[(gb.series.str.startswith(s)) & (gb.fy == fy)][c].iloc[0])
US = "data/explore/health_check/charts/demand_us_inhouse_share.csv"
us = rd(US, comment="#").set_index("year").inhouse_share_pct
CE = "data/explore/health_check/charts/demand_ces5415_monthly.csv"
ce = rd(CE, comment="#").set_index("date").ces_5415_emp_k
CT = "data/explore/health_check/charts/demand_call_themes.csv"
ct = rd(CT, comment="#")
ctv = lambda m, u: ct[(ct.metric == m) & (ct.unit == u)].set_index("half_year").value
DS = "data/explore/round4/demand_shift/rbi_destination_split.csv"
ING = "data/explore/health_check/contradictions/output_side/ing_gdp_shares.csv"
ing = rd(ING).set_index("fy")
BOP = "data/explore/health_check/contradictions/output_side/bop_vs_survey.csv"
bop = rd(BOP).set_index("fy")
TG = "data/explore/health_check/contradictions/output_side/india_trend_gap.csv"
tg = rd(TG)
VS = "output/cross_section_variance_shares.csv"
vs = rd(VS).set_index("dim")
GBS = "data/explore/round4/robustness/demand/gcc_baseline_scenarios.csv"
gbs = rd(GBS)
RBR = "data/explore/round4/robustness/demand/gcc_rbi_relative_growth.csv"
rbr = rd(RBR).set_index("fy")
LP = "data/explore/round3/listed_panel/listed_panel_firms.csv"
lp = rd(LP)
JS = "data/explore/workforce/jobspeak_monthly.csv"
js = rd(JS)
js["y"] = js.month.str[:4]
IN = "data/explore/health_check/postings/indeed_comparators_monthly.csv"
ind = rd(IN)
ind["y"] = ind.month.str[:4]
LI = "data/explore/health_check/postings/linkedin_hiring_rate_monthly.csv"
li = rd(LI)
li = li[li.country == "India"].assign(y=lambda d: d.month.str[:4])
M2S = "data/explore/round4/price_statements/m2_statements.csv"
m2s = rd(M2S)

CAT = "data/explore/health_check/literature/CATALOGUE.csv"
FJ = "data/explore/health_check/contradictions/FINDINGS_jobs.md"
FO = "data/explore/health_check/contradictions/FINDINGS_output.md"
FE = "data/explore/health_check/contradictions/FINDINGS_entry_level.md"
FT = "data/explore/health_check/fresher_thirdparty/FINDINGS.md"
FEP = "data/explore/health_check/epfo/FINDINGS.md"
FLS = "data/explore/health_check/labour_share/FINDINGS.md"
FP = "data/explore/health_check/postings/FINDINGS.md"
R3 = "data/explore/round3/SYNTHESIS.md"
R4 = "data/explore/round4/SYNTHESIS.md"
JG = "data/explore/round4/junior_gap/FINDINGS.md"
PS = "data/explore/round4/price_statements/FINDINGS.md"
INV2 = "data/explore/health_check/inventory/2_sector_trade_gcc.md"

# ================================================================== Summary
S = "Summary"
num("$221 billion", f"{S} 1; §2; Table 1", EO, "FY26 total_exports_usd_bn", tot["FY26"], 221)
num("19% more than in FY23", f"{S} 1; §2; §3", EO, "FY26/FY23 − 1, % (ordinary)", pct(tot["FY23"], tot["FY26"]), 19)
num("about 30% (world share)", f"{S} 1", IW, "2025 world_excl_ireland", iw.loc[2025, "world_excl_ireland"], 30)
sh = iw.loc[2022:2025, "world_excl_ireland"]
cond("stayed at about 30% since 2022 (world share)", f"{S} 1", IW, "world_excl_ireland 2022-2025 each within 29–31", ", ".join(f"{v:.1f}" for v in sh), all(29 <= v <= 31 for v in sh))
rng("between 0.6% and 3.2% a year (six largest, cc, FY24–26)", f"{S} 2", RG, "top6_weighted cc growth_logx100 FY24-FY26",
    [g("top6_weighted", "cc", y) for y in ("FY24", "FY25", "FY26")], 0.6, 3.2, 1, note="log points (page convention)")
pre = sum(g("top6_weighted", "cc", f"FY{y}") for y in range(16, 21)) / 5
num("about 9% a year before COVID", f"{S} 2", RG, "mean top6_weighted cc FY16-FY20 (log)", pre, 9)
num("3.7% fewer people than in March 2023", f"{S} 3", TH, "top6 2023Q1 → 2026Q1, % (ordinary)", -pct(top["2023Q1"], top["2026Q1"]), 3.7, 1,
    note="log change is 3.73 too")
cond("growing by at most about 2% a year (sector)", f"{S} 3", f"{SE}; {PC}",
     "Nasscom FY26 growth and PLFS annualised point estimate both ≤ 2.5",
     f"Nasscom {pct(sev('nasscom_direct_employment', 'FY25', 'SR Feb 2026'), sev('nasscom_direct_employment', 'FY26')):.2f}; PLFS {pc1.annual_pct}%/yr",
     pct(sev("nasscom_direct_employment", "FY25", "SR Feb 2026"), sev("nasscom_direct_employment", "FY26")) < 2.5 and pc1.annual_pct < 2.5)
xs = [fsv(PL, "2022-23"), fsv(PL, "CY2025")], [fsv(EP, "FY22"), fsv(EP, "FY24"), fsv(EP, "FY25")]
xp = fs[fs.series.str.startswith("xpheno")].set_index("period").share_pct
cond("IT's share … is lower than before the boom ended (graduates, formal entrants, entry-level openings)", f"{S} 4", FS,
     "latest value below 2022-23 (PLFS), FY22 (EPFO) and Jun 2025 (Xpheno)",
     f"PLFS {fsv(PL, '2022-23')} → {fsv(PL, 'CY2025')}; EPFO {fsv(EP, 'FY22')} → {fsv(EP, 'FY25')}; Xpheno {xp['2025-06']} → {xp['2026-10']}",
     fsv(PL, "CY2025") < fsv(PL, "2022-23") and fsv(EP, "FY25") < fsv(EP, "FY22") and xp["2026-10"] < xp["2025-06"])
num("about 0.4% (AI price cuts, FY26)", f"{S} 5; Table 1; §6", GB, "M2 AI-specific FY26 central_pct_yr", gbv("M2 AI-specific", "FY26"), 0.4, 1)
num("about 1.5% (expected FY27)", f"{S} 5; Table 1; §6; §9", GB, "M2 AI-specific FY27 central_pct_yr", gbv("M2 AI-specific", "FY27"), 1.5, 1)
txt("summer of 2026 / mid-2026 jump in coding-agent capability", f"{S}; §9", R4, "before coding agents' step change in summer 2026", kind="repo doc")

# ================================================================== Table 1
T = "Table 1"
num("$186bn in FY23", T, EO, "FY23 total_exports_usd_bn", tot["FY23"], 186)
num("30.1% (2025)", f"{T}; §2", IW, "2025 world_excl_ireland", iw.loc[2025, "world_excl_ireland"], 30.1, 1)
num("29.3% in 2022", f"{T}; §2", IW, "2022 world_excl_ireland", iw.loc[2022, "world_excl_ireland"], 29.3, 1)
num("0.6% (FY26, six largest, cc)", f"{T}; §3", RG, "top6_weighted cc FY26 (log)", g("top6_weighted", "cc", "FY26"), 0.6, 1)
num("8.7% a year in FY16–20", f"{T}; §3", RG, "mean top6_weighted cc FY16-FY20 (log)", pre, 8.7, 1)
num("14.9% (FY26, mid-tier USD)", T, RG, "midtier4 usd FY26 growth_pct (ORDINARY %; log is 13.9)", g("midtier4", "usd", "FY26", "growth_pct"), 14.9, 1,
    note="ordinary % while the page convention is log points (13.9)")
MT = "data/explore/midtier/midtier_vs_top6.csv"
mt = rd(MT).set_index("fiscal_year")
num("14.9% (FY26, mid-tier USD) — same file as the 2.2%", T, MT, "FY26 mid4_rev_growth_logx100 → ordinary % (exp − 1)",
    100 * math.expm1(mt.loc["FY26", "mid4_rev_growth_logx100"] / 100), 14.9, 1, note="log is 13.9")
num("2.2% for the six largest (USD, FY26) — ordinary %", T, MT, "FY26 top6_rev_growth_logx100 → ordinary %",
    100 * math.expm1(mt.loc["FY26", "top6_rev_growth_logx100"] / 100), 2.2, 1,
    note=f"log is {mt.loc['FY26', 'top6_rev_growth_logx100']:.2f}; revgrowth_peers.csv (Fig. 4) top6_weighted USD gives {g('top6_weighted', 'usd', 'FY26', 'growth_pct'):.2f}% (2.3)")
num("1.62m (Mar 2026)", f"{T}; §4", TH, "top6 2026Q1 / 1e6", top["2026Q1"] / 1e6, 1.62, 2)
num("1.68m in Mar 2023", T, TH, "top6 2023Q1 / 1e6", top["2023Q1"] / 1e6, 1.68, 2)
num("5.7m (2025, PLFS NIC 62–63)", f"{T}; §4", SE, "plfs_nic62_63 CY2025 / 1e6", sev("plfs_nic62_63", "CY2025") / 1e6, 5.7, 1)
num("5.5m in 2022-23", T, SE, "plfs_nic62_63 2022-23 / 1e6", sev("plfs_nic62_63", "2022-23") / 1e6, 5.5, 1)
num("5.95m (FY26, Nasscom)", f"{T}; §4", SE, "nasscom_direct_employment FY26 / 1e6", sev("nasscom_direct_employment", "FY26") / 1e6, 5.95, 2, kind="external (as published)")
txt("5.95m — Nasscom source text", f"{T}; §4", CAT, "59.5 lakh, up from 58.15 lakh")
num("+2.3% on FY25", f"{T}; §4", SE, "Nasscom FY26/FY25 (SR Feb 2026 vintage) − 1, %",
    pct(sev("nasscom_direct_employment", "FY25", "SR Feb 2026"), sev("nasscom_direct_employment", "FY26")), 2.3, 1, kind="external (as published)")
num("76,000 (FY26 freshers, TCS+Infosys+HCLTech)", f"{T}; §5", FI, "sum_tcs_infosys_hcltech FY26", fsum["FY26"], 76000, -3)
num("218,000 in FY22", f"{T}; §5", FI, "sum_tcs_infosys_hcltech FY22", fsum["FY22"], 218000, -3)
num("16% (2025, IT share of salaried grads 21–25)", T, FS, f"{PL} CY2025", fsv(PL, "CY2025"), 16)
num("20% in 2022-23", T, FS, f"{PL} 2022-23", fsv(PL, "2022-23"), 20)
num("3.9% (FY25, IT share of EPFO net payroll 18–25)", T, FS, f"{EP} FY25", fsv(EP, "FY25"), 3.9, 1)
num("5.8% in FY22", T, FS, f"{EP} FY22", fsv(EP, "FY22"), 5.8, 1)
num("₹30,900 (2025, real pay IT 21–25)", T, JP, "cws_regular_nic62_63 21-25 CY2025 mean", jpv("CY2025", "cws_regular_nic62_63", "21-25"), 30900, -2)
num("₹35,200 in 2024", T, JP, "cws_regular_nic62_63 21-25 CY2024 mean", jpv("CY2024", "cws_regular_nic62_63", "21-25"), 35200, -2)
at26 = at[at.cal_q == "2026Q2"].attrition_ltm_pct
rng("12–14% (Jun 2026 attrition)", f"{T}; §6", AT, "attrition_ltm_pct 2026Q2, six firms", at26, 12, 14)
pk = at[at.cal_q.between("2021Q1", "2023Q4")].groupby("firm").attrition_ltm_pct.max()
rng("22–28% at the 2022 peak", f"{T}; §6", AT, "max attrition 2021Q1-2023Q4 by firm", pk, 22, 28)
pkq = at[at.cal_q.between("2021Q1", "2023Q4")].sort_values("attrition_ltm_pct").groupby("firm").tail(1).cal_q
cond("peaks in 2022", f"{T}; §6", AT, "quarter of each firm's peak is in 2022", ", ".join(sorted(pkq)), all(q.startswith("2022") for q in pkq))
num("0.71 (FY26 labour share)", T, LS, "Top-6 firms FY26", ls.loc["FY26", "Top-6 firms"], 0.71, 2)
num("0.69 in FY22", T, LS, "Top-6 firms FY22", ls.loc["FY22", "Top-6 firms"], 0.69, 2)
cond("change since 2022-23 is not statistically significant (PLFS)", T, PC, "nic62_63 2022-23→cy2025 90% CI spans 0",
     f"{pc1.pct_ci90_lo} to {pc1.pct_ci90_hi}", pc1.pct_ci90_lo < 0 < pc1.pct_ci90_hi)

# ================================================================== §1
num("about six million (sector employment)", "§1", SE, "Nasscom FY26 / 1e6", sev("nasscom_direct_employment", "FY26") / 1e6, 6)
num("about 5½% of GDP (exports)", "§1", ING, "rbi_survey_pct_gdp FY26 (½-point precision: 5.25–5.75)", ing.loc["FY26", "rbi_survey_pct_gdp"], 5.5, 0.30103)
num("5.7% of GDP in FY26 (RBI survey)", "fn gdp", ING, "rbi_survey_pct_gdp FY26", ing.loc["FY26", "rbi_survey_pct_gdp"], 5.7, 1)
num("nearer 8½% (BoP incl. business services)", "fn gdp", ING, "computer_plus_obs_pct_gdp FY26 (½-point precision)", ing.loc["FY26", "computer_plus_obs_pct_gdp"], 8.5, 0.30103)
txt("in February 2026 … share prices fell sharply", "§1", CAT, "Indian IT stocks fell nearly 6% on 4 Feb 2026")
num("21 smaller listed firms", "§1; appendix", LP, "rows in listed_panel_firms.csv", len(lp), 21)

# ================================================================== §2
num("8.2% more than in FY25", "§2", EO, "FY26/FY25 − 1, %", pct(tot["FY25"], tot["FY26"]), 8.2, 1)
num("about 6% a year in dollars", "§2", EO, "(FY26/FY23)^(1/3) − 1, % (log: 5.9)", 100 * ((tot["FY26"] / tot["FY23"]) ** (1 / 3) - 1), 6)
num("IT services rose 12% (FY26)", "§2", EA, "it_services yoy_usd_pct FY26", eay.loc["FY26", "it_services"], 12)
cond("BPO exports were flat (FY26)", "§2", EA, "bpo yoy_usd_pct FY26 within ±1", eay.loc["FY26", "bpo"], abs(eay.loc["FY26", "bpo"]) < 1)
cond("IT services drove FY26", "Fig. 2 caption", EA, "FY26 USD increment: it_services > bpo",
     f"IT services +{ea.loc['FY26', 'it_services'] - ea.loc['FY25', 'it_services']:.1f}bn, BPO +{ea.loc['FY26', 'bpo'] - ea.loc['FY25', 'bpo']:.1f}bn",
     ea.loc["FY26", "it_services"] - ea.loc["FY25", "it_services"] > ea.loc["FY26", "bpo"] - ea.loc["FY25", "bpo"])
inc = {a: ea.loc["FY25", a] - ea.loc["FY24", a] for a in ("it_services", "bpo")}
cond("in FY25, IT services and BPO added similar amounts", "Fig. 2 caption", EA, "FY25 USD increments within 15% of each other",
     f"IT services +{inc['it_services']:.1f}bn, BPO +{inc['bpo']:.1f}bn", abs(inc["it_services"] - inc["bpo"]) <= 0.15 * max(inc.values()))
cond("Fig. 1 covers FY12–FY26", "Fig. 1 caption", EO, "min/max fy", f"{eo.fy.min()}–{eo.fy.max()}", eo.fy.min() == "FY12" and eo.fy.max() == "FY26")
cond("survey method changed around FY23", "Fig. 1 caption", EO, "method_break_flag == 1 rows", ", ".join(eo[eo.method_break_flag == 1].fy.unique()),
     "FY23" in set(eo[eo.method_break_flag == 1].fy))
cond("Fig. 2: FY24–FY26", "Fig. 2 caption", EA, "fy values", ", ".join(ea.index), list(ea.index) == ["FY24", "FY25", "FY26"])
num("grew 11% (India, H1 2026)", "§2", H1, "2026 india h1_yoy_pct", h1.loc[(2026, "india"), "h1_yoy_pct"], 11)
cond("as fast as those of 24 other delivery countries combined", "§2", H1, "2026 india yoy vs 24_other yoy, |diff| < 0.5",
     f"{h1.loc[(2026, 'india'), 'h1_yoy_pct']} vs {h1.loc[(2026, '24_other_delivery_countries'), 'h1_yoy_pct']}",
     abs(h1.loc[(2026, "india"), "h1_yoy_pct"] - h1.loc[(2026, "24_other_delivery_countries"), "h1_yoy_pct"]) < 0.5)
num("30 emerging delivery countries", "Fig. 3 caption", IW, "max n_countries, emerging_delivery_group", iwn["emerging_delivery_group"], 30)
cond("2015–2025; share fell before 2022 and flat since", "Fig. 3 caption", IW, "world_excl_ireland 2015 > 2022 + 3; |2025−2022| < 1.5",
     f"{iw.loc[2015, 'world_excl_ireland']:.1f}, {iw.loc[2022, 'world_excl_ireland']:.1f}, {iw.loc[2025, 'world_excl_ireland']:.1f}",
     iw.loc[2015, "world_excl_ireland"] > iw.loc[2022, "world_excl_ireland"] + 3 and abs(iw.loc[2025, "world_excl_ireland"] - iw.loc[2022, "world_excl_ireland"]) < 1.5)
num("20.4% in 2022 (incl. Ireland)", "fn ireland", IW, "2022 world_incl_ireland", iw.loc[2022, "world_incl_ireland"], 20.4, 1)
num("19.5% in 2025 (incl. Ireland)", "fn ireland", IW, "2025 world_incl_ireland", iw.loc[2025, "world_incl_ireland"], 19.5, 1)
num("39% (BoP growth FY23–26)", "fn bop", BOP, "bop_SI2 FY26/FY23 − 1, %", pct(bop.loc["FY23", "bop_SI2"], bop.loc["FY26", "bop_SI2"]), 39)
num("19% (survey growth FY23–26)", "fn bop", BOP, "survey_total FY26/FY23 − 1, %", pct(bop.loc["FY23", "survey_total"], bop.loc["FY26", "survey_total"]), 19)

# ================================================================== §3
num("$86 billion in FY26 (six firms)", "§3", RV, "FY revenue_usd FY26 / 1000", rvf.loc["FY26", "revenue_usd"] / 1000, 86)
num("7% more than in FY23", "§3", RV, "revenue_usd FY26/FY23 − 1, % (log 6.9)", pct(rvf.loc["FY23", "revenue_usd"], rvf.loc["FY26", "revenue_usd"]), 7)
num("1.5% (FY24)", "§3", RG, "top6_weighted cc FY24 (log)", g("top6_weighted", "cc", "FY24"), 1.5, 1)
num("3.2% (FY25)", "§3", RG, "top6_weighted cc FY25 (log)", g("top6_weighted", "cc", "FY25"), 3.2, 1)
peer = lambda y: (g("accenture", "cc", y) + g("cognizant", "cc", y)) / 2
num("Accenture and Cognizant grew about 5% in FY26 (Fig. 4 peer average)", "§3", RG, "mean of accenture, cognizant cc FY26 (log)", peer("FY26"), 5)
pre_gap = [abs(peer(f"FY{y}") - g("top6_weighted", "cc", f"FY{y}")) for y in range(18, 24)]
cond("Fig. 4: until FY23 the two groups moved together", "Fig. 4 caption", RG, "|peer avg − top6| FY18-FY23 each < 3 pts",
     ", ".join(f"{v:.1f}" for v in pre_gap), all(v < 3 for v in pre_gap))
post_gap = {y: peer(y) - g("top6_weighted", "cc", y) for y in ("FY24", "FY25", "FY26")}
cond("Fig. 4: since then the Indian firms have grown more slowly", "Fig. 4 caption", RG, "sum of (peer avg − top6) over FY24-FY26 > 0",
     ", ".join(f"{k} {v:+.1f}" for k, v in post_gap.items()), sum(post_gap.values()) > 0,
     note="cumulatively true; in FY24 alone the Indian firms grew faster (1.5 vs 0.8)")
cond("Fig. 4: FY16–FY26", "Fig. 4 caption", RG, "period range", f"{rg.period.min()}–FY26", rg.period.min() == "FY16")
cond("Accenture's revenue is back on its pre-COVID trend", "§3", RT, "accenture rev_cc gap FY26 within ±3 log pts", gap("accenture", "rev_cc", "gap_vs_trend_logx100"),
     abs(gap("accenture", "rev_cc", "gap_vs_trend_logx100")) < 3)
num("about 16% below trend (six firms) — ordinary %", "§3", RT, "top6_simple rev_cc gap_vs_trend_pct FY26", -gap("top6_simple", "rev_cc", "gap_vs_trend_pct"), 16,
    note="= 17.8 log points; Fig. 5 is drawn in log points, so the chart reads −17.8")
num("about 16% below trend — revenue-weighted variant, ordinary %", "§3", RT, "top6_weighted rev_cc gap_vs_trend_pct FY26", -gap("top6_weighted", "rev_cc", "gap_vs_trend_pct"), 16)
num("FY16–20 trend (Fig. 5)", "Fig. 5 caption", RT, "n_base_years", rt.n_base_years.max(), 5)
tq = fc[(fc.firm == "tcs") & fc.cal_q.isin(["2025Q2", "2025Q3", "2025Q4", "2026Q1"])].cc_yoy_pct
cond("TCS shrank in cc in each of the four quarters to March 2026", "§3", FC, "tcs cc_yoy_pct 2025Q2-2026Q1 all < 0", ", ".join(map(str, tq)), (tq < 0).all() and len(tq) == 4)
last = fc.sort_values("cal_q").groupby("firm").tail(1).set_index("firm")
rng("6–7% (LTIMindtree, TechM, latest quarter)", "§3", FC, "latest cc_yoy_pct: ltim, techm", [last.loc["ltim", "cc_yoy_pct"], last.loc["techm", "cc_yoy_pct"]], 6, 7)
cond("Fig. 6: 2022 to September 2026", "Fig. 6 caption", FC, "cal_q range", f"{fc.cal_q.min()}–{fc.cal_q.max()}", fc.cal_q.min().startswith("2022") and fc.cal_q.max() == "2026Q3")
fsh = [vs.loc["vertical", "share_firm"] * 100, vs.loc["geography", "share_firm"] * 100]
cond("about 40% (firm differences explain, by industry and by region)", "§3", VS, "share_firm vertical, geography both within 38–42",
     ", ".join(f"{v:.1f}" for v in fsh), all(38 <= v <= 42 for v in fsh))
rng("2–6% (industry or region itself)", "§3", VS, "share_group vertical, geography", [vs.loc["vertical", "share_group"] * 100, vs.loc["geography", "share_group"] * 100], 2, 6)
num("39% (mid-tier four, USD revenue FY23–26)", "§3", SC, "midtier4 rev_usd_change_pct", sc.loc["midtier4", "rev_usd_change_pct"], 39)
num("48% (three listed BPM firms)", "§3", SC, "ites_bpm_5 rev_usd_change_pct", sc.loc["ites_bpm_5", "rev_usd_change_pct"], 48)
num("three listed BPM firms (48% revenue)", "§3", SC, "ites_bpm_5 n_firms_rev_usd", sc.loc["ites_bpm_5", "n_firms_rev_usd"], 3)
num("roughly 260,000 GCC tech jobs", "§3", SC, "gcc_tech hc_change_k ×1000", sc.loc["gcc_tech", "hc_change_k"] * 1000, 260000, -4)
num("about 155,000 (GCC range low)", "fn gcc", NO, "seg_gcc_tech_range_low_k ×1000", float(nout["seg_gcc_tech_range_low_k"]) * 1000, 155000, -3)
num("430,000 (GCC range high)", "fn gcc", NO, "seg_gcc_tech_range_high_k ×1000", float(nout["seg_gcc_tech_range_high_k"]) * 1000, 430000, -4)
num("12 other IT and engineering-services firms", "§3", SC, "other_it_plus_erd_12 n_firms_hc", sc.loc["other_it_plus_erd_12", "n_firms_hc"], 12)
num("five employed fewer people in FY26 than FY23", "§3", SC, "other_it_plus_erd_12 n_firms_hc_fell", sc.loc["other_it_plus_erd_12", "n_firms_hc_fell"], 5)
num("35% in FY13 (private-limited share)", "§3", EO, "private_ltd share_pct FY13", priv["FY13"], 35)
num("61% in FY26", "§3", EO, "private_ltd share_pct FY26", priv["FY26"], 61)
pre_pace, post_pace = (priv["FY22"] - priv["FY14"]) / 8, (priv["FY26"] - priv["FY23"]) / 3
cond("continuation of a long trend, not a break after 2023", "§3", EO, "pp/yr FY23-26 ≤ pp/yr FY14-22", f"{post_pace:.2f} vs {pre_pace:.2f}", post_pace <= pre_pace)
cond("Fig. 7: FY23 to FY26, by segment", "Fig. 7 caption", SC, "segments", len(sc), len(sc) >= 6)
rng("100,000–165,000 a year before 2023 (GCC hiring)", "fn gccpace", GBS, "pre_adds_k_per_yr ×1000 (all pre scenarios)", gbs.pre_adds_k_per_yr.unique() * 1000, 100000, 165000, -4,
    note="low end is 100,600 (scenario P3, flagged NOT CONFIRMED)")
post = gbs[~gbs.post_scenario.str.startswith("E26")].post_adds_k_per_yr.unique() * 1000
rng("94,000–180,000 after", "fn gccpace", GBS, "post_adds_k_per_yr ×1000 (S2, S3, S4; excludes E26 230k)", post, 94000, 180000, -3,
    note="the E26 2026-edition scenario (230k/yr) is outside the printed range")
num("about 5 points a year faster, FY20–23", "fn gccpace", RBR, "mean foreign_subs_minus_total FY22-23 (only years with data)", rbr.loc[[2022, 2023], "foreign_subs_minus_total"].mean(), 5,
    note="file has FY22-23 only; INV2 quotes FY20-23 +5.3")
num("about 4 points faster, FY24–25", "fn gccpace", RBR, "mean foreign_subs_minus_total FY24-25", rbr.loc[[2024, 2025], "foreign_subs_minus_total"].mean(), 4)
txt("+5.3 pp FY20–23 and +4.3 pp FY24–25 (source text)", "fn gccpace", INV2, "+5.3 pp in FY20–23 and +4.3 pp in FY24–25", kind="repo doc")

# ================================================================== §4
num("1.69 million (peak)", "§4", TH, "top6 max", top.max() / 1e6, 1.69, 2)
cond("peak in September 2022", "§4", TH, "quarter of top6 max", top.idxmax(), top.idxmax() == "2022Q3")
num("fell about 4% in FY24", "§4", TH, "top6 2023Q1→2024Q1, % (log −4.5)", -pct(top["2023Q1"], top["2024Q1"]), 4)
cond("roughly flat since (FY25, FY26)", "§4", TH, "|FY25|, |FY26| change < 1.5%",
     f"{pct(top['2024Q1'], top['2025Q1']):.2f}, {pct(top['2025Q1'], top['2026Q1']):.2f}",
     abs(pct(top["2024Q1"], top["2025Q1"])) < 1.5 and abs(pct(top["2025Q1"], top["2026Q1"])) < 1.5)
num("added 9,400 (four firms, quarter to Sep 2026)", "§4", Q2, "sum net_adds_qoq of reported firms", q2[q2.status == "reported"].net_adds_qoq.sum(), 9400, -2)
num("the four firms that have reported", "§4; Fig. 8", Q2, "count status == reported", (q2.status == "reported").sum(), 4)
cond("mostly freshers", "§4", Q2, "freshers_added / net adds > 0.5",
     f"{q2.freshers_added.sum():.0f} / {q2[q2.status == 'reported'].net_adds_qoq.sum():.0f}",
     q2.freshers_added.sum() / q2[q2.status == "reported"].net_adds_qoq.sum() > 0.5,
     note="only HCLTech reports freshers (6,136); TCS fresher count is not in the file")
num("$48,600 (end of 2022)", "§4", RV, "revenue_per_employee_annualised 2022Q4 ($k)", rvq["2022Q4"], 48.6, 1)
num("$53,900 (mid-2026)", "§4", RV, "revenue_per_employee_annualised 2026Q2 ($k)", rvq["2026Q2"], 53.9, 1)
cond("Fig. 9 indexed to FY19 = 100", "Fig. 9 caption", RV, "FY19 revenue_index", rvf.loc["FY19", "revenue_index"], abs(rvf.loc["FY19", "revenue_index"] - 100) < 0.05)
cond("Fig. 8: 2015 to September 2026", "Fig. 8 caption", TH, "cal_q range", f"{top.index.min()}–{top.index.max()}", top.index.min().startswith("2015") and top.index.max() == "2026Q3")
txt("Nasscom revenue estimate rose 6.1%", "§4", CAT, "up 6.1% y/y")
num("4% more than in 2022-23 (PLFS)", "§4; details", PC, "nic62_63 2022-23→cy2025 pct_log", pc1.pct_log, 4)
num("−7% (margin of error, low)", "§4", PC, "pct_ci90_lo", pc1.pct_ci90_lo, -7)
num("+15% (margin of error, high)", "§4", PC, "pct_ci90_hi", pc1.pct_ci90_hi, 15)
cond("cannot tell that apart from no growth or from 2% a year", "§4", PC, "0 and 2%/yr × 2.5 yrs = 5.0 both inside 90% CI",
     f"CI {pc1.pct_ci90_lo} to {pc1.pct_ci90_hi}", pc1.pct_ci90_lo < 0 < pc1.pct_ci90_hi and pc1.pct_ci90_lo < 5.0 < pc1.pct_ci90_hi)
num("±11 points", "details", PC, "half-width of 90% CI", (pc1.pct_ci90_hi - pc1.pct_ci90_lo) / 2, 11)
num("another half a million (ICT workers in other industries)", "§4", SE, "plfs_ict_occupations_outside_nic62_63 CY2025 / 1e6", sev("plfs_ict_occupations_outside_nic62_63", "CY2025") / 1e6, 0.5, 1)
num("about 190,000 more than in 2022-23", "§4", SE, "ICT outside CY2025 − 2022-23",
    sev("plfs_ict_occupations_outside_nic62_63", "CY2025") - sev("plfs_ict_occupations_outside_nic62_63", "2022-23"), 190000, -4)
cond("Fig. 10: 90% confidence intervals", "Fig. 10 caption", SE, "ci90 columns present for PLFS", "ci90_lo/hi_persons", se.ci90_lo_persons.notna().any())
txt("Four estimates circulate", "details", FJ, "Nasscom, ICRIER and Goldman/World Bank vs PLFS", kind="repo doc")
num("+135,000 in FY26 (Nasscom)", "details; Table 2", SE, "Nasscom FY26 − FY25 (SR Feb 2026)",
    sev("nasscom_direct_employment", "FY26") - sev("nasscom_direct_employment", "FY25", "SR Feb 2026"), 135000, -3, kind="external (as published)")
txt("135,000 — Nasscom source text", "details; Table 2", CAT, "+2.3% or net 135,000 added")
num("+2.3% (Nasscom, details)", "details", SE, "Nasscom FY26/FY25 − 1", pct(sev("nasscom_direct_employment", "FY25", "SR Feb 2026"), sev("nasscom_direct_employment", "FY26")), 2.3, 1, kind="external (as published)")
num("shed about 64,000 jobs over three years", "details", TH, "top6 2022Q4 − 2025Q4", top["2022Q4"] - top["2025Q4"], 64000, -3)
num("our data reproduce (63,557)", "details", TH, "top6 2022Q4 − 2025Q4", top["2022Q4"] - top["2025Q4"], 63557)
txt("64,000 — World Bank/Goldman source text", "details", CAT, "cut about 64,000 workers from a combined 1.7 million")
txt("added around 700,000 (Goldman via World Bank)", "details; Table 2", CAT, "added around 700,000 workers over three years")
num("about 240,000 is Nasscom adding GCCs", "details", SE, "Nasscom FY24 restated (SR Feb 2025) − FY24 (SR Feb 2024)",
    sev("nasscom_direct_employment", "FY24", "SR Feb 2025") - sev("nasscom_direct_employment", "FY24", "SR Feb 2024"), 240000, -4)
n25 = float(re.search(r"net addition (\d+)k \(SR2026", se[(se.series == "nasscom_direct_employment") & (se.period == "FY25") & se.vintage.str.contains("2026")].note.iloc[0]).group(1)) * 1000
chained = (sev("nasscom_direct_employment", "FY24", "SR Feb 2024") - sev("nasscom_direct_employment", "FY23")) + n25 + \
          (sev("nasscom_direct_employment", "FY26") - sev("nasscom_direct_employment", "FY25", "SR Feb 2026")) - (top["2026Q1"] - top["2023Q1"])
num("about 390,000 like for like", "details; Table 2", f"{SE}; {TH}", "Nasscom chained within vintages FY23→26 minus top-6 change (recomputed)", chained, 390000, -4)
txt("+0.39m like for like (source text)", "details; Table 2", FJ, "+0.39m (+10.6%, ~3.4% a year)", kind="repo doc")
txt("ICRIER: rests on PLFS 2021-22 to 2023-24", "details; Table 2", FJ, "but for 2021-22 → 2023-24", kind="repo doc")
txt("ICRIER Section 7", "fn icrier", CAT, "Section 7")
txt("ICRIER February 2026, title", "fn icrier", CAT, "AI and Jobs: This Time Is No Different - A Case Study of India's IT Sector. ICRIER, New Delhi (February)")
txt("651 firms", "fn icrier", CAT, "Survey of 651 IT firms")
txt("55% lower, 35% higher (entry level)", "fn icrier", CAT, "55% of firms report a decline in entry-level employment over the last 24 months, 35% an increase")
txt("World Bank IDU October 2026, p. 41; Goldman July 2026", "fn goldman", CAT, "October 2026, p.41, citing Goldman Sachs, 'Gen-AI in India: Jobs Crosswinds, Productivity Tailwinds' (July 2026)")
txt("NIC 62 and 63 definitions", "fn plfs", FJ, "NIC 62 (programming, consultancy) or 63 (data processing, hosting, portals)", kind="repo doc")

# ================================================================== §5
num("65,000 in FY25", "§5", FI, "sum_tcs_infosys_hcltech FY25", fsum["FY25"], 65000, -3)
rng("400,000 to 600,000 (staffing firms' FY22 peak)", "§5", FI, "FY22 actual: han_digital, xpheno",
    [fv("han_digital_it_bpm_fresher_hiring", "FY22"), fv("xpheno_it_fresher_intake", "FY22", "actual")], 400000, 600000, -5, kind="external (as published)")
xph = fi[fi.series == "xpheno_it_fresher_intake"].set_index(["fy", "kind"]).value_persons
cond("hiring bottomed in FY24 / fell to a low in FY24 and has since partly recovered", "§5; Summary 4", FI, "Xpheno FY24 < FY25 < FY22; Infosys FY24 is its FY22-26 low",
     f"Xpheno {xph[('FY22', 'actual')]:.0f} / {xph[('FY24', 'actual')]:.0f} / {xph[('FY25', 'actual')]:.0f}; Infosys FY24 {fv('firm_fresher_hires_infosys', 'FY24'):.0f}",
     xph[("FY24", "actual")] < xph[("FY25", "actual")] < xph[("FY22", "actual")] and
     fv("firm_fresher_hires_infosys", "FY24") == fi[(fi.series == "firm_fresher_hires_infosys") & fi.fy.isin(["FY22", "FY23", "FY24", "FY25", "FY26"])].value_persons.min(),
     note="TCS FY24 is missing and HCLTech's low is FY25 (7,829), so the FY24 trough rests on Xpheno")
num("25,000 offers at TCS (FY27)", "§5", FI, "fy27_target_tcs", fv("fy27_target_tcs", "FY27"), 25000, -3, kind="external (as published)")
txt("25,000 offers — source text", "§5", CAT, "TCS issued about 25,000 fresher offers at the start of FY27")
num("20,000 at Infosys (FY27)", "§5", FI, "fy27_target_infosys", fv("fy27_target_infosys", "FY27"), 20000, -3, kind="external (as published)")
cond("none announced at Wipro or HCLTech", "§5", FI, "fy27_target_wipro, fy27_target_hcltech are blank",
     "NaN, NaN", pd.isna(fv("fy27_target_wipro", "FY27")) and pd.isna(fv("fy27_target_hcltech", "FY27")))
cond("Fig. 11: FY16–FY26", "Fig. 11 caption", FI, "min fy of firm actuals", fi[fi.group == "firm"].fy.min(), fi[fi.group == "firm"].fy.min() == "FY16")
txt("salaried graduates 21–25 in IT held at about one million", "§5", FE, "9.5 → 11.5 → 10.9 → 9.95 lakh (2022-23 to CY2025)", kind="repo doc (PLFS tabulation)")
num("about one million (2025)", "§5", FE, "9.95 lakh = 0.995m (FINDINGS_entry_level)", 0.995, 1, 0)
txt("salaried jobs for that age group grew (46.8 → 62.0 lakh)", "§5", FE, "rose from 46.8 to 62.0 lakh", kind="repo doc (PLFS tabulation)")
cond("grew by about a third", "§5", FE, "62.0/46.8 − 1 within 0.28–0.40", f"{62.0 / 46.8 - 1:.3f}", 0.28 <= 62.0 / 46.8 - 1 <= 0.40)
cond("Fig. 12: four flows, 21–25, 18–25, 0–2 years", "Fig. 12 caption", FS, "panels a-d present", ", ".join(sorted(fs.panel.unique())), len(fs.panel.unique()) == 4)
fell = u30[(u30.slope_point == "end") & (u30.direction == "fell")]
num("8 of 10 large firms (under-30 share fell)", "§5", U30, "firms with direction == fell", len(fell), 8)
num("10 large firms (under-30 panel)", "§5; Fig. 13", U30, "firms with an end point", (u30.slope_point == "end").sum(), 10)
nofy23 = u30[(u30.slope_point == "start") & (u30.fy != "FY23")].firm.tolist()
cond("'after FY23' for every firm in the count", "§5", U30, "firms whose slope starts later than FY23", ", ".join(nofy23) or "none", True,
     note="informational: these firms' change is measured from a later start year")
num("46% in FY23 (Infosys junior grade)", "§5", IG, "junior share_pct FY23", igv("FY23"), 46)
num("30% in FY26", "§5", IG, "junior share_pct FY26", igv("FY26"), 30)
cond("Fig. 14: FY14–FY26", "Fig. 14 caption", IG, "fy range", f"{ig.fy.min()}–{ig.fy.max()}", ig.fy.min() == "FY14" and ig.fy.max() == "FY26")
txt("from about FY30, will pass age 30", "fn cohort", JG, "The fresher bulge reaches 30 in FY30–31", kind="repo doc")
txt("boom cohorts FY22–23", "fn cohort", JG, "Excess under-30 hiring in FY22–23", kind="repo doc")
txt("65% (Infosys 30+ hires) — source text", "fn cohort", JG, "30+ hires: 18.7k vs 11.3k (+65%)", kind="repo doc")
txt("65% higher a year in FY24–26 than in FY16–21 (window)", "fn cohort", JG, "What changed instead: the hiring mix (Infosys, FY24–26 vs FY16–21 average)", kind="repo doc")
txt("hiring of under-30s was about the same", "fn cohort", JG, "Under-30 hires: 42.3k vs 43.1k (flat)", kind="repo doc")
fy2324 = niw.loc["2023-24"]
num("number placed fell about 1.8%", "fn nirf", NI, "within_edition all 2023-24 dlog_placed_x100", -fy2324.dlog_placed_x100, 1.8, 1, note="log points")
num("graduates rose about 3.3%", "fn nirf", NI, "within_edition all 2023-24 dlog_graduates_x100", fy2324.dlog_graduates_x100, 3.3, 1, note="log points")
cond("the first fall in the series", "§5", NI, "within_edition dlog_placed > 0 for every earlier class", ", ".join(f"{v:g}" for v in niw.dlog_placed_x100),
     (niw.drop("2023-24").dlog_placed_x100 > 0).all() and fy2324.dlog_placed_x100 < 0)
cond("NIRF classes 2015-16 to 2023-24", "appendix", NI, "grad_year range (by_grad_year)", f"{ni.grad_year.min()}–{ni.grad_year.max()}",
     ni.grad_year.min() == "2015-16" and ni.grad_year.max() == "2023-24")
num("fell 12% in 2025 (real pay 21–25)", "§5", JP, "21-25 CY2025/CY2024 − 1", -pct(jpv("CY2024", "cws_regular_nic62_63", "21-25"), jpv("CY2025", "cws_regular_nic62_63", "21-25")), 12)
num("fell 2% (31–40)", "§5", JP, "31-40 CY2025/CY2024 − 1", -pct(jpv("CY2024", "cws_regular_nic62_63", "31-40"), jpv("CY2025", "cws_regular_nic62_63", "31-40")), 2)
cond("Fig. 16: also all graduates aged 21–25", "Fig. 16 caption", JP, "cws_regular_all_grads present", "yes", "cws_regular_all_grads" in set(jp["sample"]))
cond("up to five years fell most; ten or more did not fall", "§5", PE, "0-5 most negative; 10-15 CI includes 0 or positive",
     f"0-5 {pe.loc['0-5 yrs', 'value']}, 5-10 {pe.loc['5-10 yrs', 'value']}, 10-15 {pe.loc['10-15 yrs', 'value']} ({pe.loc['10-15 yrs', 'ci95_lo']} to {pe.loc['10-15 yrs', 'ci95_hi']})",
     pe.loc["0-5 yrs", "value"] < pe.loc["5-10 yrs", "value"] < 0 and pe.loc["10-15 yrs", "ci95_lo"] < 0 < pe.loc["10-15 yrs", "ci95_hi"])
num("fell 11.9% per SD (0–5 years)", "fn lightcast", PE, "0-5 yrs value", -pe.loc["0-5 yrs", "value"], 11.9, 1, kind="external (reproduced from WB chart data)")
num("rose 3.1% (10–15 years)", "fn lightcast", PE, "10-15 yrs value", pe.loc["10-15 yrs", "value"], 3.1, 1, kind="external (reproduced from WB chart data)")
txt("Annex Table A2.12", "fn lightcast", FP, "annex table A2.12")
txt("data end in March 2025; WB SADU October 2025", "fn lightcast", FP, "Lightcast via World Bank South Asia Development Update, Oct 2025")
txt("Fig. 17: after November 2022, 95% CIs", "Fig. 17 caption", FP, "Posting index, Nov 2022 → Mar 2025", kind="repo doc")
cond("Fig. 17: 95% confidence intervals", "Fig. 17 caption", PE, "ci95 columns", "ci95_lo/hi", "ci95_lo" in pe.columns)

# ---- details: evidence against a collapse
ratio = xph[("FY25", "actual")] / xph[("FY24", "actual")]
cond("roughly doubled from FY24 to FY25 (Xpheno)", "details", FI, "Xpheno FY25/FY24 within 1.7–2.3", f"{ratio:.2f}", 1.7 <= ratio <= 2.3, kind="external (as published)")
txt("TeamLease: IT hiring intentions rebounding in 2025–26", "details", FT, "rebounded to 75–81% in 2025–26")
txt("TeamLease changed its sample in 2025", "fn teamlease", FT, "There is a series break at the 2025 H2 edition")
txt("Naukri 0–3 postings back to 2022 level", "details", FE, "That is a return to the 2022 level")
jsy = js.groupby("y").idx_it_software.mean()
num("IT postings remain about 30% below (2022)", "details", JS, "idx_it_software mean 2026 (Jan-Aug) / mean 2022 − 1", -pct(jsy["2022"], jsy["2026"]), 30, -1)
num("about 40% of graduates 15–25 unemployed, 2023-24 (principal status)", "details; Table 2", GU, "ups 15-25 2023-24", guv("2023-24", "ups"), 40, -1,
    note=f"weekly {guv('2023-24', 'cws')}, official ps+ss {guv('2023-24', 'upss')}")
txt("State of Working India's figure (nearly 40%)", "details; Table 2", CAT, "nearly 40% among 15-25-year-olds")
num("about 48% in 2017-18", "details", GU, "ups 15-25 2017-18", guv("2017-18", "ups"), 48)
cw = [guv(r, "cws") for r in ("2023-24", "CY2024", "CY2025")]
cond("on the weekly measure it has not moved since (2023-24)", "details", GU, "cws 15-25 2023-24, CY2024, CY2025: range < 2 pts",
     ", ".join(map(str, cw)), max(cw) - min(cw) < 2, note="CY2025 is 1.6 pts above 2023-24; CIs overlap")
cond("Fig. 18: 15–25 and 21–25", "Fig. 18 caption", GU, "age bands", ", ".join(sorted(gu.age.unique())), {"15-25", "21-25"} <= set(gu.age))
liy = li.groupby("y").hiring_rate_idx_2016avg_eq_1.mean()
rng("India's technology postings and hiring fell by about a third from 2022", "details", f"{JS}; {LI}",
    "JobSpeak IT 2026 vs 2022; LinkedIn India 2026 (Jan-May) vs 2022, % decline",
    [-pct(jsy["2022"], jsy["2026"]), -pct(liy["2022"], liy["2026"])], 28, 32, note="'about a third' tested as 28–32 at 0 dp")
sw = ind[ind.series.str.contains("software")].groupby(["country", "y"]).value.mean()
dec = {f"{c} {y}": -pct(sw[(c, "2022")], sw[(c, y)]) for c in ("US", "GB") for y in ("2025", "2026")}
cond("US and UK software postings fell by about two-thirds", "details", IN, "decline vs 2022, 2025 and 2026 means, all within 58–72%",
     ", ".join(f"{k} {v:.1f}" for k, v in dec.items()), all(58 <= v <= 72 for v in dec.values()))

# ================================================================== §6
pkv = at[at.cal_q.between("2021Q1", "2023Q4")].groupby("firm").attrition_ltm_pct.max()
pre_ut = ut[ut.cal_q.between("2016Q1", "2019Q4")].groupby("firm").utilization_pct.agg(["min", "max", "mean"])
last_ut = ut.sort_values("cal_q").groupby("firm").tail(1).set_index("firm").utilization_pct
mean_ut = ut.groupby("firm").mean_2016_19_pct.first()
cond("utilisation at or above its pre-COVID average", "§6", UT, "latest ≥ each firm's 2016-19 mean",
     ", ".join(f"{f} {last_ut[f]:.1f} vs {mean_ut[f]:.1f}" for f in last_ut.index), all(last_ut[f] >= mean_ut[f] for f in last_ut.index))
num("the four firms that report it (utilisation)", "§6", UT, "firms in file", len(last_ut), 4)
d = {f: pct(tv.loc["2025Q2", f], tv.loc["2026Q2", f]) for f in tv.columns}
cond("value of deals signed over the past year is flat or rising", "§6", TV, "TTM TCV 2026Q2 vs 2025Q2 ≥ −3% for every firm",
     ", ".join(f"{k} {v:+.1f}%" for k, v in d.items()), all(v >= -3 for v in d.values()))
cond("Fig. 19: 2016–19 average", "Fig. 19 caption", AT, "mean_2016_19_pct present", "yes", at.mean_2016_19_pct.notna().any())
rng("held at about 0.7 since FY16", "§6", LS, "Top-6 firms FY16-FY26", ls["Top-6 firms"].dropna(), 0.7, 0.7, 1)
avg_hc = lambda a, b: (top[a] + top[b]) / 2
pe23, pe26 = t6.loc["FY23", "employee_cost_inr_cr"] / avg_hc("2022Q1", "2023Q1"), t6.loc["FY26", "employee_cost_inr_cr"] / avg_hc("2025Q1", "2026Q1")
va23, va26 = t6.loc["FY23", "value_added_inr_cr"] / avg_hc("2022Q1", "2023Q1"), t6.loc["FY26", "value_added_inr_cr"] / avg_hc("2025Q1", "2026Q1")
num("pay per average employee rose about 21% (FY23–26)", "§6", f"{FL}; {TH}", "employee cost / avg(opening, closing) headcount, FY26/FY23 − 1", pct(pe23, pe26), 21,
    note="with year-end headcount it is 24.7%")
num("value added per average employee rose about 21%", "§6", f"{FL}; {TH}", "value added / avg(opening, closing) headcount, FY26/FY23 − 1", pct(va23, va26), 21,
    note="with year-end headcount it is 24.3%")
cond("Fig. 20: three mid-tier firms, FY16–FY26", "Fig. 20 caption", LS, "mid-tier series and fy range", f"{ls.index.min()}–{ls.index.max()}",
     any("Persistent, Coforge, Mphasis" in c for c in ls.columns) and ls.index.min() == "FY16" and ls.index.max() == "FY26")
num("0.1% in FY25 (AI price cuts)", "§6", GB, "M2 AI-specific FY25 central", gbv("M2 AI-specific", "FY25"), 0.1, 1)
rng("brokers' 2–3.5% a year", "§6; Table 2", GB, "Broker deflation range FY26 low/high", [gbv("Broker", "FY26", "low_pct_yr"), gbv("Broker", "FY26", "high_pct_yr")], 2, 3.5, 1,
    kind="external (as published)")
num("routine annual discounts of about 1.5%", "§6", GB, "M2 gross − AI-specific, FY24 (pre-AI baseline)", gbv("M2 gross", "FY24") - gbv("M2 AI-specific", "FY24"), 1.5, 1)
cond("Fig. 21: FY24–FY27", "Fig. 21 caption", GB, "M2 fy range", ", ".join(gb[gb.series.str.startswith("M2 AI")].fy), list(gb[gb.series.str.startswith("M2 AI")].fy) == ["FY24", "FY25", "FY26", "FY27"])
m2s["base"] = m2s.firm.str.split(" (", regex=False).str[0]
it_f = set(m2s[m2s.segment == "IT"].base)
bpo_only = set(m2s[m2s.segment == "BPO"].base) - it_f
num("108 statements", "fn m2", M2S, "rows", len(m2s), 108)
num("by eight IT firms", "fn m2", M2S, "distinct firms with IT statements (supplier contract rows mapped to their vendor)", len(it_f), 8)
num("and four BPO firms", "fn m2", M2S, "firms with only BPO statements", len(bpo_only), 4, note=", ".join(sorted(bpo_only)))
txt("broker range: Kotak, ICICI Securities and HCLTech guidance", "fn m2", "data/explore/health_check/contradictions/output_side/broker_deflation_vs_m2.csv",
    "HCLTech (management; cited by Kotak)")
txt("documented in round4/price_statements", "fn m2", PS, "AI-driven price change on same-scope work", kind="repo doc")
txt("six firms' wage bill alone would exceed the whole sector's", "fn labourshare", FLS, "exceeds the PLFS wage bill for the whole sector", kind="repo doc")
txt("no BLS PPI for computer systems design", "fn noindex", "price_data.md", "BLS has never published one", kind="repo doc")

# ================================================================== §7
dsp = rd(DS)
usv = dsp[dsp.iloc[:, 1].astype(str).str.contains("United States")].iloc[:, 2]
num("about 54% (US share of exports)", "§7", DS, "United States share, FY24-FY26 (latest)", float(usv.iloc[-1]), 54)
rng("64–65% in 2015–22 (in-house share)", "§7", US, "inhouse_share_pct 2015-2022", us.loc[2015:2022], 64, 65)
num("67.5% in 2025", "§7", US, "inhouse_share_pct 2025", us.loc[2025], 67.5, 1)
num("fallen 5% since March 2023 (US IT-services employment)", "§7", CE, "latest / 2023-03 − 1", -pct(ce["2023-03"], ce.iloc[-1]), 5,
    note=f"latest month {ce.index[-1]}")
cond("peak was March 2023", "§7", CE, "idxmax", ce.idxmax(), ce.idxmax() == "2023-03")
cond("Fig. 22: 2015–2025; NAICS 5415 monthly", "Fig. 22 caption", US, "year range", f"{us.index.min()}–{us.index.max()}", us.index.min() == 2015 and us.index.max() == 2025)
A = ctv("A: demand weakness", "statements per transcript")
cond("weak demand peaked in 2023 and stayed well above pre-2022", "§7", CT, "argmax in 2023; min since 2024 > 2 × max 2021",
     f"peak {A.idxmax()} {A.max():.2f}; since 2024 min {A.loc['2024H1':].min():.2f}; 2021 max {A.loc[['2021H1', '2021H2']].max():.2f}",
     A.idxmax().startswith("2023") and A.loc["2024H1":].min() > 2 * A.loc[["2021H1", "2021H2"]].max())
AI, D = ctv("AI mentions", "per 10k words"), ctv("D: AI productivity passed to clients", "statements per transcript")
cond("AI mentions and AI pass-through have risen steeply since 2025", "§7", CT, "2026H2 / 2024H2 ≥ 1.5 for both",
     f"AI {AI['2024H2']:.1f} → {AI['2026H2']:.1f}; D {D['2024H2']:.2f} → {D['2026H2']:.2f}", AI["2026H2"] / AI["2024H2"] >= 1.5 and D["2026H2"] / D["2024H2"] >= 1.5,
     note="AI mentions had already risen ~20× in 2023–24")
cond("Fig. 23: per 10,000 words, by half-year", "Fig. 23 caption", CT, "unit 'per 10k words' present", "yes", (ct.unit == "per 10k words").any())

# ================================================================== §8 Table 2
T2 = "Table 2"
txt("Future of India: 20.0% to 15.8%", T2, CAT, "fell from 20.0% to 15.8%")
cond("'Correct' (Future of India shares)", T2, FS, "ours 20.4 → 16.0 within 0.5 of theirs", f"{fsv(PL, '2022-23')} → {fsv(PL, 'CY2025')}",
     abs(fsv(PL, "2022-23") - 20.0) <= 0.5 and abs(fsv(PL, "CY2025") - 15.8) <= 0.5)
cond("labour share has fallen: 'Not on company or RBI data'", T2, LS, "Top-6 and RBI listed FY26 ≥ FY22",
     f"top-6 {ls.loc['FY22', 'Top-6 firms']:.3f} → {ls.loc['FY26', 'Top-6 firms']:.3f}; RBI {ls.loc['FY22', 'RBI listed IT companies']:.3f} → {ls.loc['FY26', 'RBI listed IT companies']:.3f}",
     ls.loc["FY26", "Top-6 firms"] >= ls.loc["FY22", "Top-6 firms"] and ls.loc["FY26", "RBI listed IT companies"] >= ls.loc["FY22", "RBI listed IT companies"])
txt("LinkedIn: entry-level hiring rose 168%; refers to firms of 1–10 staff", T2, CAT, "hiring into firms with 1-10 employees")
txt("LinkedIn 168% (claim)", T2, CAT, "India entry-level hiring up 168% from 2023 to 2025")
txt("Baldwin: 27% above trend", T2, CAT, "now sit 27% above a log-linear 2015-22 trend")
b = tg[(tg.column == "wto_SJ_4q") & (tg.fit_window == "2015Q1-2022Q4")].iloc[0]
num("Baldwin 27% (reproduced)", T2, TG, "wto_SJ_4q 2015Q1-2022Q4 gap_2025Q4_pct", b.gap_2025Q4_pct, 27)
cond("about half the gap predates ChatGPT", T2, TG, "gap 2022Q4 / gap 2025Q4 within 0.4–0.6", f"{b.gap_2022Q4_pct} / {b.gap_2025Q4_pct} = {b.gap_2022Q4_pct / b.gap_2025Q4_pct:.2f}",
     0.4 <= b.gap_2022Q4_pct / b.gap_2025Q4_pct <= 0.6)
txt("Economic Survey 2025-26: 39.5%", T2, CAT, "rose about 39.5% relative to less-exposed services")
txt("Xpheno, via Economic Times: 600,000 to 140,000", f"{T2}; appendix", FT, "\"net hiring in the IT sector fell from around 600,000 in FY22 to 140,000 in FY26\"")
txt("Xpheno FY22: 450,000 first, 600,000 in 2026", "fn fresher3p", FT, "The FY22 figure has drifted up from 450k to 600k")
txt("HAN Digital, TeamLease Digital", "fn fresher3p", FT, "HAN Digital (ET, 14 Oct 2026; IT-BPM including GCCs and BPO)")

# ================================================================== §9 and appendix
txt("Infosys reports on 23 October", "§9", FJ, "Infosys (23 Oct)")
txt("RBI census due late October 2026", "§9", R3, "The FY26 round is due around late October 2026.", kind="repo doc")
txt("EPFO payroll releases stopped after September 2025", "§9", FEP, "The last PIB payroll release is dated 23 Sep 2025", kind="repo doc")
txt("EPFO monthly payroll reports to July 2025", "appendix", FEP, "July 2025 uses the PIB release headline", kind="repo doc")
cond("PLFS 2017-18 to 2025", "appendix", FS, "PLFS period range", f"{fs[fs.series == PL].period.iloc[0]}–{fs[fs.series == PL].period.iloc[-1]}",
     fs[fs.series == PL].period.iloc[0] == "2017-18" and fs[fs.series == PL].period.iloc[-1] == "CY2025")
txt("price statements: eight firms, 2021–2026", "appendix", "calls_codebook.md", "Jan 2021 – Oct 2026, eight firms", kind="repo doc")
num("TCS Sep 2026 4,700 higher than a year earlier", "appendix", TH, "tcs 2026Q3 − 2025Q3", th.loc["2026Q3", "tcs"] - th.loc["2025Q3", "tcs"], 4700, -2)
txt("not 15,000 lower (claim corrected)", "appendix", FJ, "TCS is +4.7k year on year, not \"15k below a year earlier\"", kind="repo doc")
num("15,000 below its level of June 2025", "appendix", TH, "tcs 2025Q2 − 2026Q3", th.loc["2025Q2", "tcs"] - th.loc["2026Q3", "tcs"], 15000, -3)
num("five largest fell by 6,981 in FY26", "appendix", TH, "TCS+Infosys+HCLTech+Wipro+TechM 2025Q1 − 2026Q1", five["2025Q1"] - five["2026Q1"], 6981)
txt("not 7,389 (IANS)", "appendix", CAT, "fell by 7,389 in FY26")
num("about 160 in the nine months to December 2025", "appendix", TH, "five firms 2025Q4 − 2025Q1", five["2025Q4"] - five["2025Q1"], 160, -1)
txt("not 17 (Computerworld)", "appendix", FJ, "+17 in 9M FY26", kind="external")
txt("PLFS 2025 sample about 2.5 times larger", "data notes", FLS, "CY2025 PLFS** is a redesigned survey with a 2.5× larger sample", kind="repo doc")
num("about 0.3 million lower without the high-weight unit (2023-24)", "data notes", SE, "plfs_nic62_63 2023-24 − excl_high_weight_cluster",
    (sev("plfs_nic62_63", "2023-24") - sev("plfs_nic62_63_excl_high_weight_cluster", "2023-24")) / 1e6, 0.3, 1)
txt("EPFO: ten largest industries; IT visible only for ages 18–28", "data notes", FEP, "IT × age for 18-28 only, with no all-ages IT total", kind="repo doc")
txt("EPFO: top 10 industries in each age band", "data notes", FEP, "top 10 industries within each age band", kind="repo doc")

# ================================================================== revision of 18 Oct: new Summary, Introduction, §3-5 text, new footnotes
NH = "data/explore/health_check/charts/nasscom_employment_history.csv"
nh = rd(NH, comment="#").set_index("fy")
num("about 4% a year before COVID (sector employment)", f"{S} 3; fn nasscomhist", NH, "(FY20/FY16)^(1/4) − 1, %", 100 * ((nh.loc["FY20", "level_m"] / nh.loc["FY16", "level_m"]) ** 0.25 - 1), 4, kind="external (as published)")
num("3.7 million in FY16 (Nasscom)", "fn nasscomhist", NH, "FY16 level_m", nh.loc["FY16", "level_m"], 3.7, 1, kind="external (as published)")
num("4.36 million in FY20", "fn nasscomhist", NH, "FY20 level_m", nh.loc["FY20", "level_m"], 4.36, 2, kind="external (as published)")
num("about 4.2% a year", "fn nasscomhist", NH, "(FY20/FY16)^(1/4) − 1, % (log 4.1)", 100 * ((nh.loc["FY20", "level_m"] / nh.loc["FY16", "level_m"]) ** 0.25 - 1), 4.2, 1, kind="external (as published)")
num("net additions averaging about 160,000 a year (FY17–20)", "fn nasscomhist", NH, "mean net_addition_k FY17-FY20 ×1000", nh.loc["FY17":"FY20", "net_addition_k"].mean() * 1000, 160000, -4,
    kind="external (as published)", note=f"FY16-FY20 mean is {nh.loc['FY16':'FY20', 'net_addition_k'].mean():.0f}k")
num("in the FY21–23 boom they averaged about 290,000", "fn nasscomhist", NH, "mean net_addition_k FY21-FY23 ×1000", nh.loc["FY21":"FY23", "net_addition_k"].mean() * 1000, 290000, -4, kind="external (as published)")
rt23 = rt[(rt.fy == "FY23") & (rt.series == "top6_simple")].set_index("metric").gap_vs_trend_pct
num("in FY23 headcount about 15% above its pre-COVID trend", "§5", RT, "top6_simple headcount gap_vs_trend_pct FY23", rt23["headcount"], 15, note="log 14.1")
num("revenue only about 3.5% above", "§5", RT, "top6_simple rev_cc gap_vs_trend_pct FY23", rt23["rev_cc"], 3.5, 1, note="log 3.5")
FB = "data/explore/workforce/fresher_hires_annual_best.csv"
fb = rd(FB).set_index(["firm", "fy"]).fresher
num("TCS and Infosys together hired 64,000 freshers in FY26", "§5", FB, "tcs + infosys fresher, fy 2026", fb[("tcs", 2026)] + fb[("infosys", 2026)], 64000, -3)
num("more than the 50,000 they hired in FY16", "§5", FB, "tcs + infosys fresher, fy 2016", fb[("tcs", 2016)] + fb[("infosys", 2016)], 50000, -3)
txt("staffing firms' estimates remain below pre-COVID levels: pre-COVID ~200k a year", "§5", FT, "| pre-COVID | ~200k a year |", kind="repo doc")
cond("… remain below pre-COVID levels (latest sector estimates vs ~200k)", "§5", FI, "HAN FY26 and Xpheno FY25 < 200,000",
     f"HAN FY26 {fv('han_digital_it_bpm_fresher_hiring', 'FY26'):.0f}; Xpheno FY25 {xph[('FY25', 'actual')]:.0f}",
     fv("han_digital_it_bpm_fresher_hiring", "FY26") < 200000 and xph[("FY25", "actual")] < 200000, kind="external (as published)")
txt("Business Today (21 March 2026): deferred offers at Wipro and Tech Mahindra", "fn deferred", CAT, "Business Today, 21 Mar 2026 (Xpheno data)")
txt("deferred offers (source text)", "fn deferred", CAT, "Offer deferrals: Wipro cut its fresher guidance")
rng("12 other listed IT and engineering-services firms grew headcount by only 2%, net of acquisitions", "§3", SC, "other_it_plus_erd_12 hc_change_excl_acq_pct",
    [sc.loc["other_it_plus_erd_12", "hc_change_excl_acq_pct"]], 2, 2)
num("the 12 other listed firms (count)", "§3", SC, "other_it_plus_erd_12 n_firms_hc", sc.loc["other_it_plus_erd_12", "n_firms_hc"], 12)
num("IT employed about 20% of salaried graduates aged 21–25 in 2022-23", "fn route", FS, f"{PL} 2022-23", fsv(PL, "2022-23"), 20)
KS = "data/explore/round3/plfs/key_series_grads_21_30.csv"
ks = rd(KS)
eng = ks[ks.series == "nic62_63__engdeg_21_30"].set_index("round").share * 100
num("about 30% in 2017-18 (IT share of employed engineering grads 21–30)", "fn route", KS, "nic62_63__engdeg_21_30 share 2017-18", eng["2017-18"], 30)
rng("45–53% from 2021-22", "fn route", KS, "nic62_63__engdeg_21_30 share, 2021-22 onward", eng.loc["2021-22":], 45, 53)
txt("State of Working India 2026 (young graduates' employers)", "fn route", CAT, "State of Working India 2026")
ext = lambda printed, where, url_frag, note="": add(printed, where, "health_check_text.md (inline citation)", f'cited URL contains "{url_frag}"',
                                                   "cited inline; no copy in repo" if url_frag in TEXT.read_text(encoding="utf-8") else "NO CITATION",
                                                   url_frag in TEXT.read_text(encoding="utf-8"), "external (unverified in repo)", note)
ext("Upadhya 2007", "fn mobility", "epw.in/journal/2007/20")
ext("Jensen 2012", "fn mobility", "doi.org/10.1093/qje/qjs002")
ext("Oster and Steinberg 2013: enrolment up about 5%", "fn mobility", "Oster and Steinberg 2013](", note="number not checked: no repo copy of the paper")
ext("Reuters, 4 February 2026: sell-off began on 4 February", "fn selloff", "marketscreener.com/news/indian-tech-stocks-slump")
ext("about $50 billion wiped off by mid-February (Reuters, 24 February 2026)", "fn selloff", "finance.yahoo.com/news/indian-shares-trail-regional-peers",
    note="the $50bn figure is not in any repo file")
txt("Rest of World (6 February 2026)", "fn worry", CAT, "Rest of World, Feb 6")
ext("Jefferies cut price targets (Business Today, 23 February 2026)", "fn worry", "jefferies-cuts-targets-for-indian-it-stocks-by-up-to-33-517481-2026-02-23",
    note="catalogue IND-08d has the Jefferies downgrade via 5paisa, 24 Feb 2026")
ext("IDR summary, 12 May 2026", "fn route", "idronline.org/article/livelihoods/the-changing-nature-of-work-in-india")
at_now = at[at.cal_q == "2026Q2"].set_index("firm")
cond("attrition close to its pre-COVID norm (Summary)", f"{S} 5", AT, "2026Q2 ≤ 2016-19 mean + 2.5 at every firm",
     ", ".join(f"{f} {r.attrition_ltm_pct} vs {r.mean_2016_19_pct}" for f, r in at_now.iterrows()), all(r.attrition_ltm_pct <= r.mean_2016_19_pct + 2.5 for _, r in at_now.iterrows()))
cond("utilisation at or above its pre-COVID average (Summary)", f"{S} 5", UT, "latest >= each firm's 2016-19 mean",
     ", ".join(f"{f} {last_ut[f]:.1f} vs {mean_ut[f]:.1f}" for f in last_ut.index), all(last_ut[f] >= mean_ut[f] for f in last_ut.index))

# ---------------------------------------------------------------- coverage scan
raw = TEXT.read_text(encoding="utf-8")
raw = re.sub(r"\A---\n.*?\n---\n", "", raw, flags=re.S)              # YAML front matter
raw = re.sub(r"<!--.*?-->", " ", raw, flags=re.S)                    # HTML comment block
raw = re.sub(r"^::: ?(figure|table|details)?[^\n]*$", " ", raw, flags=re.M)  # directive lines
raw = re.sub(r"\]\([^)]*\)", "]", raw)                               # link targets
raw = re.sub(r"\[\^[^\]]+\]:?", " ", raw)                        # footnote markers and keys
raw = re.sub(r"^#+ \d+\.", " ", raw, flags=re.M)                     # section numbers
raw = re.sub(r"^\d\. ", " ", raw, flags=re.M)                        # numbered list items
STRIP = [r"\bNAICS 5415\b", r"\bFY\d{2}(?:–\d{2})?\b", r"\b20\d{2}–(?:20)?\d{2}\b", r"\b(?:19|20)\d{2}(?:-\d{2})?\b",
         r"\b(?:Table|Figure|Section)\s+\d+\b", r"\bp\.\s*\d+\b", r"A2\.12", r"\bNIC 62–63\b", r"\bdivisions 62\b", r"\band 63 \(",
         r"\b\d{1,2}–\d{1,2} (?:years|staff)\b", r"\baged \d{2}–\d{2}\b", r"\bages \d{2}–\d{2}\b", r"\b\d{2}–\d{2}\b(?= on| and|,|\))",
         r"\bTable\b", r"\b10,000 words\b", r"\b23 October\b", r"\b6 February\b", r"\b(?:19|20)\d0s\b"]
for pat in STRIP:
    raw = re.sub(pat, " ", raw)
tokens = re.findall(r"[+−-]?\d[\d,]*(?:\.\d+)?%?", raw)
norm = lambda t: t.lstrip("+−-").rstrip("%").rstrip(",")
covered = set()
for e in ENTRIES:
    for t in re.findall(r"[+−-]?\d[\d,]*(?:\.\d+)?%?", e["printed"]):
        covered.add(norm(t))
uncovered = sorted({norm(t) for t in tokens} - covered, key=lambda s: float(s.replace(",", "")))

bad = [e for e in ENTRIES if not e["ok"]]
edge = [e for e in ENTRIES if e["ok"] and "borderline" in e["note"]]
show = lambda r: (f"{r:.3f}".rstrip("0").rstrip(".") if isinstance(r, float) else str(r))
lines = ["# Number check for the health-check page (`health_check_text.md`)", "",
         "*Generated by `scripts/final/health_check_number_check.py` from the text file (HTML comment and front matter skipped). "
         "CSV numbers are recomputed and must round to the printed value at the printed precision; ranges must contain every source value; "
         "word claims are tested as explicit conditions; text-sourced numbers must appear verbatim in the cited file "
         "('external' = someone else's number, checked only for being quoted correctly). Growth rates are log ×100 unless the entry says otherwise.*", "",
         f"**Result:** {len(ENTRIES)} entries checked, {len(ENTRIES) - len(bad)} pass, {len(bad)} fail, {len(edge)} pass only at a rounding boundary. "
         f"Uncovered numeric tokens in the text: {len(uncovered)}.", ""]
if bad:
    lines += ["## Failures", "", "| printed | where | source | row / key | repo value | note |", "|---|---|---|---|---|---|"]
    lines += [f"| {e['printed']} | {e['where']} | `{e['source']}` | {e['key']} | {show(e['repo'])} | {e['note']} |" for e in bad] + [""]
if edge:
    lines += ["## Borderline (pass only at the rounding boundary)", "", "| printed | where | source | repo value | note |", "|---|---|---|---|---|"]
    lines += [f"| {e['printed']} | {e['where']} | `{e['source']}` | {show(e['repo'])} | {e['note']} |" for e in edge] + [""]
notes = [e for e in ENTRIES if e["ok"] and e["note"] and "borderline" not in e["note"]]
if notes:
    lines += ["## Passes with a caveat", "", "| printed | where | note |", "|---|---|---|"]
    lines += [f"| {e['printed']} | {e['where']} | {e['note']} |" for e in notes] + [""]
lines += ["## All entries", "", "| printed | where | kind | source | row / key | repo value | pass |", "|---|---|---|---|---|---|---|"]
lines += [f"| {e['printed']} | {e['where']} | {e['kind']} | `{e['source']}` | {e['key']} | {show(e['repo'])} | {'yes' if e['ok'] else '**NO**'} |" for e in ENTRIES]
lines += ["", "## Coverage scan", "",
          "Numeric tokens in the text (prose, tables, captions, details, footnotes) that no entry's printed label covers, after removing "
          "fiscal and calendar years, year ranges, section/table/figure numbers, list numbers, page numbers, NIC/NAICS codes and age bands:", "",
          ("none" if not uncovered else ", ".join(f"`{t}`" for t in uncovered)), ""]
OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"{len(ENTRIES)} entries, {len(bad)} fail, {len(edge)} borderline")
for e in bad:
    print("FAIL:", e["printed"], "|", e["where"], "|", show(e["repo"]), "|", e["note"])
for e in edge:
    print("EDGE:", e["printed"], "|", show(e["repo"]), "|", e["note"])
print(f"{len(tokens)} numeric tokens scanned ({len({norm(t) for t in tokens})} distinct); uncovered:", uncovered)
import os
if os.environ.get("HCDEBUG"):
    print(sorted({norm(t) for t in tokens}))
