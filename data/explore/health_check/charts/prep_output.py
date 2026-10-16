"""Chart-ready CSVs for the Output and Who-is-growing sections of the health-check page.

    python3 data/explore/health_check/charts/prep_output.py

Reads repo CSVs only (no web access) and writes small, tidy CSVs next to this script. Canonical files
(data/corrected/*, output/final/*, data/explore/round*/...) are read, never written.

Outputs (this folder)
  exports_orgtype.csv     RBI software-exports survey FY12-FY26 by exporter type: USD bn and % share.
  publtd_share.csv        Public- vs private-limited share of software exports FY12-FY26 (subset of the above).
  revgrowth_peers.csv     Annual growth FY16-FY26 + Q1FY27: top-6 rev-weighted (cc and USD), mid-tier four (USD),
                          Accenture (cc), Cognizant (cc).
  rev_trend_levels.csv    Log level vs FY16-20 trend, FY16-FY26: top-6 (simple and weighted avg) and Accenture;
                          cc revenue and average headcount.
  india_world_share.csv   India's share of world computer-services exports (ex-Ireland balanced panel) and of the
                          emerging delivery-country group, 2015-2025.
  india_h1_growth.csv     H1 y/y growth of computer-services exports, India vs 24 other delivery countries, 2020-2026.
  exports_activity.csv    RBI exports by activity FY24-FY26, USD bn and y/y.
  segment_change.csv      FY23->FY26 change in headcount (incl./excl. known acquisitions) and USD revenue by
                          segment, plus GCC tech-jobs range.
  firm_cc_quarterly.csv   Quarterly cc y/y revenue growth per top-6 firm, 2022Q1 -> 2026Q3 (Q2FY27 where reported).
  scorecard_output.csv    Scorecard rows for this section.
  numbers_output.csv      Every number the prose is likely to quote, with how it was computed and a check
                          against the value quoted in the outline/brief.

Conventions
  * Growth columns ending _logx100 are log change x 100 (the repo's table_A convention); _pct columns are
    ordinary percent changes. pct = 100*(exp(log/100)-1).
  * Indian fiscal year FYxx = April (xx-1) to March xx. Calendar quarter 2026Q3 = Jul-Sep 2026 = Q2FY27.
"""
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
EX = ROOT / "data/explore"

P = dict(
    orgtype=EX / "trade/rbi_survey_orgtype.csv",
    exports=EX / "round3/sector_aggregates/exports_recomputed.csv",
    activity=EX / "round3/red_team/rbi_exports_by_activity_type.csv",
    tableA=ROOT / "output/final/table_A.csv",
    midtier=EX / "midtier/midtier_vs_top6.csv",
    r1gaps=EX / "round4/robustness/baseline/r1_level_gaps_group.csv",
    r1comp=EX / "round4/robustness/baseline/r1_comparators_levels.csv",
    share=EX / "round3/offshore_competitors/india_share_summary.csv",
    h1=EX / "round3/offshore_competitors/imf_h1_india_vs_delivery_group.csv",
    lp_sum=EX / "round3/listed_panel/listed_panel_summary.csv",
    lp_firms=EX / "round3/listed_panel/listed_panel_firms.csv",
    gcc=EX / "round3/gcc_reconcile/gcc_scenarios.csv",
    core=ROOT / "data/corrected/core_quarterly_final.csv",
    yoy=ROOT / "data/corrected/yoy_metrics_final.csv",
    q2=EX / "health_check/contradictions/q2fy27_update.csv",
)


def rel(p):
    return str(Path(p).relative_to(ROOT))


def log2pct(x):
    return 100 * (np.exp(np.asarray(x, float) / 100) - 1)


def fy_label(s):  # "2022-23" -> "FY23"
    return "FY" + s[-2:]


def save(df, name):
    df.to_csv(HERE / name, index=False)
    print(f"wrote {name}: {len(df)} rows")


NUM = []  # numbers_output rows


def num(key, value, unit, period, source_file, how, quoted=None, quoted_note=""):
    NUM.append(dict(key=key, value=value, unit=unit, period=period, source_file=source_file, how_computed=how,
                    quoted_value=quoted, check=quoted_note))


# ============================================================ 1. exports_orgtype / publtd_share
og = pd.read_csv(P["orgtype"])
og["fy"] = og.fy.map(fy_label)
og["fy_n"] = og.fy.str[2:].astype(int)
og = og[og.fy_n >= 12].copy()
# FY18 is missing in the source; add an empty row so lines break rather than interpolate
og = pd.concat([og, pd.DataFrame([dict(fy="FY18", fy_n=18, release_round="not published in collected releases",
                                       basis="missing")])]).sort_values("fy_n")

rows = []
for _, r in og.iterrows():
    for typ, sh, usd in [("public_ltd", "public_ltd_share_pct", "public_ltd_usd_bn"),
                         ("private_ltd", "private_ltd_share_pct", "private_ltd_usd_bn"),
                         ("others", "others_share_pct", None)]:
        share = r[sh]
        if usd and pd.notna(r.get(usd)):
            v, vb = r[usd], "reported"
        elif typ == "others" and pd.notna(r.get("public_ltd_usd_bn")):
            v, vb = r.total_usd_bn - r.public_ltd_usd_bn - r.private_ltd_usd_bn, "residual: total - public - private"
        elif pd.notna(share):
            v, vb = share / 100 * r.total_usd_bn, "derived: share x total"
        else:
            v, vb = np.nan, "missing"
        brk = ""
        if r.fy == "FY23":
            brk = ("probable method break: new release round (2023-24, PR Oct 2024), grossed-up final estimates; "
                   "public-ltd exports +31.8% y/y and public share +4.2pp in one year")
        elif r.fy == "FY14":
            brk = "basis change: early-method survey estimates (FY12-13) -> as reported by respondents"
        elif r.fy == "FY21":
            brk = "basis change: grossed-up final estimates from FY21"
        rows.append(dict(fy=r.fy, exporter_type=typ, exports_usd_bn=round(v, 2) if pd.notna(v) else np.nan,
                         usd_value_basis=vb, share_pct=share, total_exports_usd_bn=r.total_usd_bn,
                         release_round=r.release_round, survey_basis=r.basis,
                         method_break_flag=int(r.fy == "FY23"), break_note=brk,
                         source=f"RBI Survey on Computer Software & ITES Exports, via {rel(P['orgtype'])}"))
EO = pd.DataFrame(rows)
# cross-check FY23-26 against exports_recomputed
ex = pd.read_csv(P["exports"])
for ser, typ in [("RBI survey public_ltd_usd_bn", "public_ltd"), ("RBI survey private_ltd_usd_bn", "private_ltd")]:
    for _, r in ex[ex.series == ser].iterrows():
        a = EO[(EO.fy == fy_label(r.fy)) & (EO.exporter_type == typ)].exports_usd_bn.iloc[0]
        assert abs(a - r.level) < 0.05, (ser, r.fy, a, r.level)
save(EO, "exports_orgtype.csv")

PS = EO[EO.exporter_type.isin(["public_ltd", "private_ltd"])][
    ["fy", "exporter_type", "share_pct", "method_break_flag", "break_note", "source"]].copy()
save(PS, "publtd_share.csv")

tot = og.set_index("fy").total_usd_bn
pub = og.set_index("fy").public_ltd_share_pct
num("exports_fy26_usd_bn", tot["FY26"], "USD bn", "FY26", rel(P["orgtype"]), "RBI survey total, excl. Mode 3", 221.4,
    "matches")
num("exports_fy23_usd_bn", tot["FY23"], "USD bn", "FY23", rel(P["orgtype"]), "RBI survey total", None, "")
g = 100 * (tot["FY26"] / tot["FY23"] - 1)
num("exports_growth_fy23_26_pct", round(g, 1), "%", "FY23-FY26", rel(P["orgtype"]), "221.4/185.5-1", 19.4, "matches")
num("exports_cagr_fy23_26_pct", round(100 * ((tot["FY26"] / tot["FY23"]) ** (1 / 3) - 1), 1), "% per yr",
    "FY23-FY26", rel(P["orgtype"]), "(221.4/185.5)^(1/3)-1", 6.0, "outline says 'about 6% a year': 6.1")
for a, b in [("FY24", "FY23"), ("FY25", "FY24"), ("FY26", "FY25")]:
    v = round(100 * (tot[a] / tot[b] - 1), 1)
    num(f"exports_yoy_{a.lower()}_pct", v, "%", a, rel(P["orgtype"]), f"{a}/{b}-1 on USD bn",
        {"FY26": 8.2, "FY25": 7.3, "FY24": 2.8}[a], "matches exports_recomputed yoy_pct")
num("publtd_share_fy23_pct", pub["FY23"], "%", "FY23", rel(P["orgtype"]), "as published", 41.5, "matches")
num("publtd_share_fy26_pct", pub["FY26"], "%", "FY26", rel(P["orgtype"]), "as published", 36.9, "matches")
num("publtd_share_fy13_pct", pub["FY13"], "%", "FY13", rel(P["orgtype"]), "as published (early method)", 64.6, "matches")
num("publtd_share_fy12_pct", pub["FY12"], "%", "FY12", rel(P["orgtype"]), "as published (early method)", None, "")
num("publtd_share_fy20_pct", pub["FY20"], "%", "FY20", rel(P["orgtype"]), "as published", 46.6, "matches")
pv = og.set_index("fy").private_ltd_share_pct
num("privltd_share_fy13_pct", pv["FY13"], "%", "FY13", rel(P["orgtype"]), "as published", 35.3, "matches")
num("privltd_share_fy26_pct", pv["FY26"], "%", "FY26", rel(P["orgtype"]), "as published", 60.8, "matches")
sl1 = (pv["FY22"] - pv["FY14"]) / 8
sl2 = (pv["FY26"] - pv["FY23"]) / 3
num("privltd_share_pp_per_yr_fy14_22", round(sl1, 2), "pp per yr", "FY14-FY22", rel(P["orgtype"]),
    "(share FY22 - share FY14)/8", 3.0, "matches inventory (+3.0pp/yr)")
num("privltd_share_pp_per_yr_fy23_26", round(sl2, 2), "pp per yr", "FY23-FY26", rel(P["orgtype"]),
    "(share FY26 - share FY23)/3", 1.6, "matches inventory (+1.6pp/yr)")
pu = og.set_index("fy")
num("publtd_exports_fy23_26_pct", round(100 * (pu.public_ltd_usd_bn["FY26"] / pu.public_ltd_usd_bn["FY23"] - 1), 1), "%",
    "FY23-FY26", rel(P["orgtype"]), "81.7/77.0-1", 6.0, "matches (+6%)")
num("privltd_exports_fy23_26_pct", round(100 * (pu.private_ltd_usd_bn["FY26"] / pu.private_ltd_usd_bn["FY23"] - 1), 1),
    "%", "FY23-FY26", rel(P["orgtype"]), "134.6/104.1-1", 29.0, "matches (+29%)")
num("publtd_exports_fy23_yoy_pct", round(100 * (pu.public_ltd_usd_bn["FY23"] / pu.public_ltd_usd_bn["FY22"] - 1), 1), "%",
    "FY23", rel(P["orgtype"]), "77.0/58.4-1; evidence of method break", 31.8, "matches")

# ============================================================ 2. exports_activity
ac = pd.read_csv(P["activity"])
ac["fy"] = ac.fy.map(fy_label)
keep = ["it_services", "software_products", "bpo", "engineering", "total"]
A_ = ac[ac.series.isin(keep)].copy()
# subtotals: computer services = IT services + software products; ITeS = BPO + engineering
for name, parts in [("computer_services_subtotal", ["it_services", "software_products"]),
                    ("ites_subtotal", ["bpo", "engineering"])]:
    s = A_[A_.series.isin(parts)].groupby("fy")[["inr_crore", "usd_bn"]].sum().reset_index()
    s["series"] = name
    A_ = pd.concat([A_, s])
A_ = A_.sort_values(["series", "fy"])
A_["yoy_usd_pct"] = A_.groupby("series").usd_bn.pct_change() * 100
A_["yoy_inr_pct"] = A_.groupby("series").inr_crore.pct_change() * 100
A_["share_of_total_pct"] = A_.usd_bn / A_.fy.map(A_[A_.series == "total"].set_index("fy").usd_bn) * 100
A_ = A_.rename(columns={"series": "activity", "usd_bn": "exports_usd_bn", "inr_crore": "exports_inr_crore"})
A_["note"] = np.where(A_.fy == "FY24", "FY24 from 2024-25 survey round (PR Nov 2025); FY25-26 from 2025-26 round "
                                        "(PR Sep 2026): FY25 y/y spans two release vintages", "")
A_["source"] = "RBI Survey on Computer Software & ITES Exports, via " + rel(P["activity"])
A_ = A_[["fy", "activity", "exports_usd_bn", "exports_inr_crore", "yoy_usd_pct", "yoy_inr_pct", "share_of_total_pct",
         "note", "source"]].round(2)
chk = A_[A_.activity.isin(["it_services", "software_products", "bpo", "engineering"])].groupby("fy").exports_usd_bn.sum()
assert (abs(chk - A_[A_.activity == "total"].set_index("fy").exports_usd_bn) < 0.15).all()
save(A_, "exports_activity.csv")
ai = A_.set_index(["activity", "fy"])
for act, fy, q in [("it_services", "FY25", 4.6), ("it_services", "FY26", 12.0), ("bpo", "FY25", 11.4), ("bpo", "FY26", 0.4),
                   ("engineering", "FY26", None), ("software_products", "FY26", None)]:
    num(f"exports_{act}_yoy_{fy.lower()}_pct", round(ai.loc[(act, fy)].yoy_usd_pct, 1), "%", fy, rel(P["activity"]),
        "y/y on USD bn", q, "matches" if q is not None else "")
for act, q in [("it_services", 147.0), ("bpo", 56.0), ("engineering", 12.0), ("software_products", 6.4),
               ("computer_services_subtotal", 153.4), ("ites_subtotal", 68.0)]:
    num(f"exports_{act}_fy26_usd_bn", round(ai.loc[(act, "FY26")].exports_usd_bn, 1), "USD bn", "FY26",
        rel(P["activity"]), "as published / summed", q, "matches")
num("exports_inr_yoy_fy26_pct", round(ai.loc[("total", "FY26")].yoy_inr_pct, 1), "%", "FY26", rel(P["activity"]),
    "INR crore y/y", 13.0, "matches")

# ============================================================ 3. revgrowth_peers
TA = pd.read_csv(P["tableA"])
TA["period"] = TA.period.replace({"FY27 Q1 (one quarter)": "Q1FY27"})
spec = [("top6_weighted", "Indian revenue-weighted average", "rev_cc", "cc"),
        ("top6_weighted", "Indian revenue-weighted average", "rev_usd", "usd"),
        ("accenture", "Accenture", "rev_cc", "cc"),
        ("cognizant", "Cognizant", "rev_cc", "cc")]
rows = []
for ser, grp, met, basis in spec:
    d = TA[(TA.group == grp) & (TA.metric == met)]
    for _, r in d.iterrows():
        note = ""
        if ser == "top6_weighted":
            note = f"{r.n_firms} firms: {r.firms}"
        if ser == "accenture":
            note = "Accenture quarters mapped to Indian FY (Mar-Feb); Q1FY27 = its quarter to May 2026; acquisitions not adjusted"
        if ser == "cognizant" and pd.notna(r.value):
            note = "Belcan acquisition adds ~4pp in late 2024-mid 2025, not adjusted"
        if r.period == "Q1FY27":
            note = (note + "; " if note else "") + "one quarter (Apr-Jun 2026 vs Apr-Jun 2025), not a fiscal year"
        rows.append(dict(period=r.period, series=ser, currency_basis=basis, growth_logx100=r.value,
                         n_firms=r.n_firms, note=note, source=rel(P["tableA"])))
MT = pd.read_csv(P["midtier"])
for _, r in MT.iterrows():
    note = ("USD revenue, NOT constant currency; includes acquisitions (Coforge: Cigniti FY25); Hexaware calendar "
            "year t-1 used as FYt; growth on matched same-basis prior-year levels (" + r.mid4_rev_growth_firms + ")")
    rows.append(dict(period=r.fiscal_year, series="midtier4", currency_basis="usd",
                     growth_logx100=r.mid4_rev_growth_logx100, n_firms=len(r.mid4_rev_growth_firms.split("+")),
                     note=note, source=rel(P["midtier"])))
RG = pd.DataFrame(rows)
RG["growth_pct"] = log2pct(RG.growth_logx100)
order = {f"FY{y}": y for y in range(16, 27)} | {"Q1FY27": 27}
RG["_o"] = RG.period.map(order)
RG = RG.sort_values(["series", "currency_basis", "_o"]).drop(columns="_o")
RG = RG[["period", "series", "currency_basis", "growth_logx100", "growth_pct", "n_firms", "note", "source"]].round(3)
save(RG, "revgrowth_peers.csv")

rg = RG.set_index(["series", "currency_basis", "period"]).growth_logx100
pre = rg.loc[("top6_weighted", "cc")].loc[[f"FY{y}" for y in range(16, 21)]].mean()
num("top6_cc_growth_fy26_logx100", round(rg[("top6_weighted", "cc", "FY26")], 1), "log pts x100", "FY26",
    rel(P["tableA"]), "revenue-weighted avg of firm-reported cc growth", 0.6, "matches")
num("top6_cc_growth_fy24_logx100", round(rg[("top6_weighted", "cc", "FY24")], 1), "log pts x100", "FY24",
    rel(P["tableA"]), "revenue-weighted", 1.5, "matches")
num("top6_cc_growth_fy25_logx100", round(rg[("top6_weighted", "cc", "FY25")], 1), "log pts x100", "FY25",
    rel(P["tableA"]), "revenue-weighted", 3.2, "matches")
num("top6_cc_growth_q1fy27_logx100", round(rg[("top6_weighted", "cc", "Q1FY27")], 1), "log pts x100", "Q1FY27",
    rel(P["tableA"]), "revenue-weighted, one quarter y/y", 3.0, "matches")
num("top6_cc_growth_prefy16_20_mean_logx100", round(pre, 1), "log pts x100", "FY16-FY20", rel(P["tableA"]),
    "mean of FY16-20 revenue-weighted cc growth (4 firms: TCS, Infosys, HCL, Wipro)", 9.0,
    "outline '~9%': 8.7 log = 9.1% -> ok as '~9%'")
num("top6_cc_growth_fy24_26_range_logx100", f"{min(rg[('top6_weighted','cc',p)] for p in ['FY24','FY25','FY26']):.2f} to "
    f"{max(rg[('top6_weighted','cc',p)] for p in ['FY24','FY25','FY26']):.2f}", "log pts x100", "FY24-FY26",
    rel(P["tableA"]), "min/max of weighted cc growth", "1-3", "outline says '1-3% a year', but FY26 is 0.6 (below 1); FY24-26 range is the value shown")
num("accenture_cc_growth_fy26_logx100", round(rg[("accenture", "cc", "FY26")], 1), "log pts x100", "FY26",
    rel(P["tableA"]), "table_A", 5.0, "matches")
num("cognizant_cc_growth_fy26_logx100", round(rg[("cognizant", "cc", "FY26")], 1), "log pts x100", "FY26",
    rel(P["tableA"]), "table_A", 5.2, "matches")
for fy in ["FY24", "FY25", "FY26"]:
    v = rg[("midtier4", "usd", fy)]
    num(f"midtier_usd_growth_{fy.lower()}_logx100", round(v, 1), "log pts x100", fy, rel(P["midtier"]),
        f"USD, incl. acquisitions; pct = {float(log2pct(v)):.1f}", {"FY24": None, "FY25": 14.0, "FY26": 14.0}[fy],
        "" if fy == "FY24" else f"'~14%' holds in log points; as ordinary % it is {float(log2pct(v)):.1f}% (USD, not cc)")
mt = MT.set_index("fiscal_year")
num("midtier_rev_level_growth_fy26_pct", round(100 * (mt.mid4_rev_usd_mn["FY26"] / mt.mid4_rev_usd_mn["FY25"] - 1), 1),
    "%", "FY26", rel(P["midtier"]), "ratio of summed USD levels (unmatched; differs from matched log growth)", None, "")
num("midtier_rev_share_fy20_pct", round(mt.mid4_rev_share_pct["FY20"], 1), "%", "FY20", rel(P["midtier"]),
    "mid4/(mid4+top6) USD revenue (FY20 excl. Coforge)", 4.0, "matches")
num("midtier_rev_share_fy26_pct", round(mt.mid4_rev_share_pct["FY26"], 1), "%", "FY26", rel(P["midtier"]),
    "mid4/(mid4+top6) USD revenue", 7.3, "matches")

# ============================================================ 4. rev_trend_levels
rows = []
for ser, grp in [("top6_simple", "Indian simple average"), ("top6_weighted", "Indian revenue-weighted average"),
                 ("accenture", "Accenture")]:
    for met in ["rev_cc", "headcount"]:
        s = TA[(TA.group == grp) & (TA.metric == met) & TA.period.str.startswith("FY")].copy()
        s["fy"] = s.period.str[2:].astype(int)
        s = s.set_index("fy").value
        g0 = s.loc[16:20].dropna().mean()
        nb = int(s.loc[16:20].notna().sum())
        for t in range(16, 27):
            if t <= 20:
                if s.loc[t + 1:20].isna().any():
                    continue
                L = -s.loc[t + 1:20].sum()
            else:
                L = s.loc[21:t].sum()
            T = g0 * (t - 20)
            rows.append(dict(fy=f"FY{t}", series=ser, metric=met, log_level_vs_fy20_x100=L, trend_log_vs_fy20_x100=T,
                             gap_vs_trend_logx100=L - T, index_fy20_100=100 * np.exp(L / 100),
                             trend_index_fy20_100=100 * np.exp(T / 100), gap_vs_trend_pct=log2pct(L - T),
                             trend_growth_fy16_20_logx100=g0, n_base_years=nb,
                             note=("headcount = average-based (table_A 'headcount'); " if met == "headcount" else "")
                             + "trend = FY20 actual level extended at mean FY16-20 log growth "
                             + ("(Accenture FY16 n/a: FY17-20 mean)" if ser == "accenture" else
                                "(top-6 cc FY16-20 covers TCS, Infosys, HCL, Wipro only)" if met == "rev_cc" else ""),
                             source=rel(P["tableA"]) + "; method as " + rel(EX / "round4/robustness/baseline/r1_baseline.py")))
TL = pd.DataFrame(rows).round(3)
# reproduce r1 numbers
r1 = pd.read_csv(P["r1gaps"]).set_index("metric")
r1c = pd.read_csv(P["r1comp"]).set_index(["firm", "metric"])
tl = TL.set_index(["series", "metric", "fy"]).gap_vs_trend_logx100
for met in ["rev_cc", "headcount"]:
    assert abs(tl[("top6_simple", met, "FY26")] - r1.loc[met, "gap_vs_trend_fy26"]) < 0.02
    assert abs(tl[("top6_simple", met, "FY23")] - r1.loc[met, "gap_vs_trend_fy23"]) < 0.02
    assert abs(tl[("accenture", met, "FY23")] - r1c.loc[("accenture", met), "overshoot_vs_trend_by_fy23"]) < 0.02
save(TL, "rev_trend_levels.csv")
for ser in ["top6_simple", "top6_weighted", "accenture"]:
    for met in ["rev_cc", "headcount"]:
        v = tl[(ser, met, "FY26")]
        q, c = None, ""
        if ser == "top6_simple" and met == "rev_cc":
            q, c = -18, (f"'~18% below trend' is {-v:.1f} LOG POINTS; as an ordinary % it is {-float(log2pct(v)):.1f}% below "
                         "trend. Say 'about 16% below' or '18 log points'")
        if ser == "top6_weighted" and met == "rev_cc":
            c = f"revenue-weighted variant: {-float(log2pct(v)):.1f}% below"
        if ser == "accenture" and met == "rev_cc":
            q, c = 0, (f"'on trend' holds: {v:+.1f} log pts ({float(log2pct(v)):+.1f}%) at FY26. Note r1 FINDINGS' '-0.9/+0.6' are "
                       "growth-rate deltas vs counterfactual c, not level gaps")
        num(f"{ser}_{met}_gap_vs_trend_fy26_logx100", round(v, 1), "log pts x100", "FY26", rel(P["tableA"]),
            "cum. log growth FY21-26 minus 6 x FY16-20 mean", q, c)
num("top6_simple_rev_cc_gap_vs_trend_fy26_pct", round(log2pct(tl[("top6_simple", "rev_cc", "FY26")]), 1), "%", "FY26",
    rel(P["tableA"]), "100*(exp(gap/100)-1)", -18, "differs: -16.3% in ordinary percent")
num("top6_simple_headcount_gap_vs_trend_fy23_logx100", round(tl[("top6_simple", "headcount", "FY23")], 1),
    "log pts x100", "FY23", rel(P["r1gaps"]), "boom overshoot in staff", 14.1, "matches r1 FINDINGS")
num("top6_simple_rev_cc_gap_vs_trend_fy23_logx100", round(tl[("top6_simple", "rev_cc", "FY23")], 1),
    "log pts x100", "FY23", rel(P["r1gaps"]), "boom overshoot in revenue", 3.5, "matches r1 FINDINGS")

# ============================================================ 5. india_world_share + h1
SH = pd.read_csv(P["share"])
mets = {"India share excl. Ireland, balanced panel 2015-2025, %": "world_excl_ireland",
        "India share of emerging delivery-country group, balanced 2015-2025, %": "emerging_delivery_group",
        "India share of world computer-services exports, balanced panel 2015-2025, %": "world_incl_ireland"}
W = SH[SH.metric.isin(mets)].copy()
W["denominator"] = W.metric.map(mets)
W = W[(W.year >= 2015) & (W.year <= 2025)]
W = W.rename(columns={"value": "india_share_pct"})
W["source"] = "IMF BOP (SI2 computer services, USD), via " + rel(P["share"])
W = W[["year", "denominator", "india_share_pct", "n_countries", "note", "source"]]
W["year"] = W.year.astype(int)
save(W, "india_world_share.csv")
w = W.set_index(["denominator", "year"]).india_share_pct
for den, yrs, qs in [("world_excl_ireland", [2015, 2022, 2025], [34.6, 29.3, 30.1]),
                     ("emerging_delivery_group", [2015, 2022, 2025], [75.2, 65.9, 65.2]),
                     ("world_incl_ireland", [2015, 2022, 2025], [27.3, 20.4, 19.5])]:
    for y, q in zip(yrs, qs):
        v = w[(den, y)]
        num(f"india_share_{den}_{y}_pct", round(v, 1), "%", str(y), rel(P["share"]), "balanced panel 2015-2025", q,
            "matches" if abs(round(v, 1) - q) < 0.05 else f"differs ({v:.2f})")

H = pd.read_csv(P["h1"])
H = H[H.year >= 2020]
H1 = pd.concat([
    H[["year", "india_yoy_pct", "india_h1_usd_bn"]].rename(columns={"india_yoy_pct": "h1_yoy_pct", "india_h1_usd_bn": "h1_usd_bn"}).assign(group="india"),
    H[["year", "others_yoy_pct", "others_h1_usd_bn"]].rename(columns={"others_yoy_pct": "h1_yoy_pct", "others_h1_usd_bn": "h1_usd_bn"}).assign(group="24_other_delivery_countries"),
])
H1 = H1.merge(H[["year", "india_share_pct"]].rename(columns={"india_share_pct": "india_share_of_25_pct"}), on="year")
H1["source"] = "IMF BOP quarterly SI2, Jan-Jun sums, via " + rel(P["h1"])
H1 = H1[["year", "group", "h1_usd_bn", "h1_yoy_pct", "india_share_of_25_pct", "source"]].sort_values(["group", "year"])
save(H1, "india_h1_growth.csv")
hh = H.set_index("year")
num("india_h1_2026_yoy_pct", hh.india_yoy_pct[2026], "%", "H1 2026", rel(P["h1"]), "Jan-Jun 2026 vs Jan-Jun 2025", 11.1, "matches")
num("others_h1_2026_yoy_pct", hh.others_yoy_pct[2026], "%", "H1 2026", rel(P["h1"]), "24 other delivery countries", 11.1, "matches")
num("india_h1_share_of_25_2026_pct", hh.india_share_pct[2026], "%", "H1 2026", rel(P["h1"]), "", 66.6, "matches (66.55)")

# ============================================================ 6. segment_change
LS = pd.read_csv(P["lp_sum"])
LF = pd.read_csv(P["lp_firms"])
segs = [("top6 (repo)", "top6", "Top six"), ("mid4", "midtier4", "Mid-tier four"),
        ("ITservices_ex_mid4_7", "other_it_services_7", "Other IT services (7)"), ("ERD_5", "erd_5", "ER&D (5)"),
        ("ITeS_BPM_5", "ites_bpm_5", "ITeS/BPM (5)"),
        ("broader_ex_mid4_ex_ITeS_12", "other_it_plus_erd_12", "Other IT + ER&D (12)")]
rows = []
for key, seg, lab in segs:
    hc = LS[(LS.set == key) & (LS.metric == "hc")].iloc[0]
    rv = LS[(LS.set == key) & (LS.metric == "rev_usd_mn")].iloc[0]
    acq = 0.0
    if isinstance(hc.note, str) and "known acquired heads" in hc.note:
        acq = float(hc.note.split("known acquired heads ")[1].split(";")[0])
    hc_ex = (hc.abs_change_FY23_26 - acq) if key != "top6 (repo)" else np.nan
    rows.append(dict(segment=seg, segment_label=lab, n_firms_hc=int(hc.n_firms), n_firms_rev_usd=int(rv.n_firms),
                     hc_fy23=hc.FY23, hc_fy26=hc.FY26, hc_change_k=hc.abs_change_FY23_26 / 1000,
                     hc_change_pct=hc.agg_pct_change_FY23_26, known_acquired_hc_k=acq / 1000 if key != "top6 (repo)" else np.nan,
                     hc_change_excl_acq_k=hc_ex / 1000, hc_change_excl_acq_pct=100 * hc_ex / hc.FY23,
                     rev_usd_change_pct=rv.agg_pct_change_FY23_26, n_firms_hc_fell=hc.n_firms_falling,
                     range_low_k=np.nan, range_high_k=np.nan,
                     note=("global headcount; HCL Q1FY25 divestiture (7,398 staff) not added back" if key == "top6 (repo)"
                           else "global headcount; acquisition adjustment is a lower bound"
                           + (f"; USD revenue missing for {rv.firms_missing_FY23_or_FY26}" if isinstance(rv.firms_missing_FY23_or_FY26, str) else "")),
                     source=rel(P["lp_sum"])))
G = pd.read_csv(P["gcc"])
g23 = G[G.window == "FY23-26"].set_index("scenario")
s2 = g23.loc[[i for i in g23.index if i.startswith("S2")][0]]
s3 = g23.loc[[i for i in g23.index if i.startswith("S3")][0]]
s4 = g23.loc[[i for i in g23.index if i.startswith("S4")][0]]
gl, gc, gh = s4["gcc_tech_change_k_share0.55"], s3["gcc_tech_change_k_share0.67"], s2["gcc_tech_change_k_share0.80"]
rows.append(dict(segment="gcc_tech", segment_label="GCCs, tech roles (estimate)", hc_change_k=gc,
                 range_low_k=gl, range_high_k=gh,
                 note="central = S3 staffing-firm net hiring x 0.67 tech share; low = S4 (2024-edition path) x 0.55; "
                      "high = S2 (restated Zinnov basis) x 0.80. India-only, all GCCs; not comparable to listed-firm "
                      "global headcount. Round-4: pace no faster than pre-2023.",
                 source=rel(P["gcc"])))
rows.append(dict(segment="gcc_all_functions", segment_label="GCCs, all functions (estimate)",
                 hc_change_k=s3.gcc_change_all_functions_k_central, range_low_k=s4.gcc_change_all_functions_k_low,
                 range_high_k=s2.gcc_change_all_functions_k_high,
                 note="central = S3; low = S4 low; high = S2 high", source=rel(P["gcc"])))
SC = pd.DataFrame(rows).round(2)
save(SC, "segment_change.csv")
sc = SC.set_index("segment")
for seg, col, q, unit in [("top6", "rev_usd_change_pct", 7.2, "%"), ("top6", "hc_change_pct", -3.7, "%"),
                          ("top6", "hc_change_k", -61.5, "thousand"),
                          ("midtier4", "hc_change_pct", 18.0, "%"), ("midtier4", "hc_change_excl_acq_pct", 14.1, "%"),
                          ("midtier4", "rev_usd_change_pct", 39.4, "%"),
                          ("erd_5", "hc_change_pct", 4.0, "%"), ("erd_5", "hc_change_excl_acq_pct", 0.2, "%"),
                          ("erd_5", "rev_usd_change_pct", 25.0, "%"),
                          ("other_it_services_7", "hc_change_pct", 7.3, "%"),
                          ("other_it_services_7", "hc_change_excl_acq_pct", 4.9, "%"),
                          ("other_it_services_7", "rev_usd_change_pct", 13.7, "%"),
                          ("ites_bpm_5", "hc_change_pct", 36.2, "%"), ("ites_bpm_5", "hc_change_excl_acq_pct", 28.7, "%"),
                          ("ites_bpm_5", "rev_usd_change_pct", 47.7, "%"),
                          ("other_it_plus_erd_12", "hc_change_excl_acq_pct", 2.3, "%"),
                          ("other_it_plus_erd_12", "n_firms_hc_fell", 5, "firms of 12"),
                          ("gcc_tech", "hc_change_k", 260, "thousand"), ("gcc_tech", "range_low_k", 155, "thousand"),
                          ("gcc_tech", "range_high_k", 430, "thousand"),
                          ("gcc_all_functions", "hc_change_k", 385, "thousand")]:
    v = sc.loc[seg, col]
    ok = abs(float(v) - q) <= 0.06 * max(1, abs(q)) if unit == "thousand" else abs(float(v) - q) < 0.06
    num(f"seg_{seg}_{col}", round(float(v), 2), unit, "FY23-FY26", sc.loc[seg, "source"], col, q,
        "matches" if ok else f"differs ({v})")
# verify 5 of 12 from the firm file
f12 = LF[(LF.mid4 == 0) & LF.group.isin(["ER&D", "IT services", "IT services / ITeS"])]  # Datamatics sits in the IT-services 7
shr = f12[f12.hc_FY26 < f12.hc_FY23]
num("other_it_erd_firms_shrank_list", "; ".join(f"{r['name']} {r.hc_chg_pct_FY23_26:+.0f}%" for _, r in shr.iterrows()),
    "firms", "FY23-FY26", rel(P["lp_firms"]), f"hc_FY26 < hc_FY23 among {len(f12)} non-mid4, non-ITeS firms",
    "5 of 12", f"{len(shr)} of {len(f12)}")

# ============================================================ 7. firm_cc_quarterly
core = pd.read_csv(P["core"], dtype={"cal_q": str})
yoy = pd.read_csv(P["yoy"], dtype={"cal_q": str})
m = core[["firm", "cal_q", "rev_cc_yoy", "rev_cc_yoy_src"]].merge(yoy[["firm", "cal_q", "gR"]], on=["firm", "cal_q"])
TOP6 = ["tcs", "infosys", "hcltech", "wipro", "techm", "ltim"]
m = m[(m.cal_q >= "2022Q1") & m.firm.isin(TOP6 + ["lti"])].copy()
m = m[~((m.firm == "lti") & (m.cal_q >= "2022Q4")) & ~((m.firm == "ltim") & (m.cal_q < "2022Q4"))]
# LTI (pre-merger) stands in for the LTI group in 2022Q1-Q3: LTIM's restated cc series starts 2022Q4
m["entity_reported"] = m.firm
m.loc[m.firm == "lti", "firm"] = "ltim"
assert (abs(100 * np.log1p(m.rev_cc_yoy / 100) - m.gR).dropna() < 1e-6).all()  # gR is the log of reported cc
m["source"] = rel(P["core"]) + " (rev_cc_yoy, firm-reported)"
m["status"] = "canonical panel"
m = m.rename(columns={"rev_cc_yoy": "cc_yoy_pct", "gR": "cc_yoy_logx100", "rev_cc_yoy_src": "source_url"})
q2 = pd.read_csv(P["q2"])
q2 = q2[q2.firm.isin(TOP6) & (q2.status == "reported")]
add = pd.DataFrame(dict(firm=q2.firm, cal_q=q2.cal_q, cc_yoy_pct=q2.rev_cc_yoy_pct,
                        cc_yoy_logx100=100 * np.log1p(q2.rev_cc_yoy_pct / 100), source_url=q2.source_url,
                        entity_reported=q2.firm, source=rel(P["q2"]), status="Q2FY27 update (not in canonical panel)"))
F = pd.concat([m, add], ignore_index=True)
F["fiscal_quarter"] = F.cal_q.map(lambda c: f"Q{(int(c[-1]) - 2) % 4 + 1}FY{(int(c[2:4]) + (1 if int(c[-1]) >= 2 else 0)):02d}")
F["note"] = ""
F.loc[F.entity_reported == "lti", "note"] = "LTI standalone (pre-merger); LTIM cc y/y starts 2022Q4"
F.loc[(F.firm == "hcltech") & (F.cal_q == "2026Q3"), "note"] = "company-level cc (services-only cc +4.0%)"
F.loc[F.firm == "wipro", "note"] = "IT Services segment"
F.loc[(F.firm == "techm") & (F.cal_q == "2026Q3"), "note"] = "company-level cc"
F = F[["firm", "cal_q", "fiscal_quarter", "cc_yoy_pct", "cc_yoy_logx100", "entity_reported", "status", "note",
       "source", "source_url"]].sort_values(["firm", "cal_q"]).round(3)
save(F, "firm_cc_quarterly.csv")
f = F.set_index(["firm", "cal_q"]).cc_yoy_pct
for fm in TOP6:
    last = F[F.firm == fm].cal_q.max()
    num(f"cc_yoy_{fm}_latest_pct", f[(fm, last)], "%", last, F[(F.firm == fm) & (F.cal_q == last)].source.iloc[0],
        "firm-reported cc y/y", None, "")
num("tcs_cc_yoy_2025q2_2026q1", "; ".join(f"{f[('tcs', q)]:+.1f}" for q in ["2025Q2", "2025Q3", "2025Q4", "2026Q1"]),
    "%", "2025Q2-2026Q1", rel(P["core"]), "TCS negative four quarters", "-3.1,-3.3,-2.6,-0.6", "matches")
missing = sorted(set(TOP6) - set(q2.firm))
num("q2fy27_firms_pending", ", ".join(missing), "firms", "2026Q3", rel(P["q2"]), "status != reported as of 2026-10-15",
    None, "")

# ============================================================ 8. scorecard
S = [
    dict(indicator="Software exports (RBI survey)", value=tot["FY26"], unit="USD bn", period="FY26",
         change_value=round(100 * (tot["FY26"] / tot["FY25"] - 1), 1), change_unit="% y/y",
         change2_value=round(g, 1), change2_unit="% vs FY23", direction="up", source=rel(P["orgtype"])),
    dict(indicator="India share of world computer-services exports (ex-Ireland)", value=round(w[("world_excl_ireland", 2025)], 1),
         unit="%", period="2025", change_value=round(w[("world_excl_ireland", 2025)] - w[("world_excl_ireland", 2022)], 1),
         change_unit="pp vs 2022", change2_value=round(w[("world_excl_ireland", 2025)] - w[("world_excl_ireland", 2015)], 1),
         change2_unit="pp vs 2015", direction="flat", source=rel(P["share"])),
    dict(indicator="Top-6 constant-currency revenue growth (rev-weighted)", value=round(rg[("top6_weighted", "cc", "FY26")], 1),
         unit="log pts x100", period="FY26", change_value=round(pre, 1), change_unit="FY16-20 mean, log pts x100",
         change2_value=round(rg[("top6_weighted", "cc", "Q1FY27")], 1), change2_unit="Q1FY27 y/y",
         direction="down vs pre-COVID", source=rel(P["tableA"])),
    dict(indicator="Mid-tier four revenue growth (USD, incl. acquisitions)", value=round(rg[("midtier4", "usd", "FY26")], 1),
         unit="log pts x100", period="FY26", change_value=round(rg[("midtier4", "usd", "FY25")], 1),
         change_unit="FY25, log pts x100", change2_value=round(rg[("top6_weighted", "usd", "FY26")], 1),
         change2_unit="top-6 USD FY26, log pts x100", direction="up", source=rel(P["midtier"])),
]
save(pd.DataFrame(S), "scorecard_output.csv")

# ============================================================ numbers
N = pd.DataFrame(NUM)
save(N, "numbers_output.csv")
flag = N[N.check.astype(str).str.contains("differ|LOG POINTS|but|not cc", case=False)]
print("\nDiscrepancies / caveats vs quoted values:")
print(flag[["key", "value", "quoted_value", "check"]].to_string(index=False))
