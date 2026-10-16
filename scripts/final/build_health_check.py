"""Build the health-check page (docs/health-check.html) for GitHub Pages.

    python3 scripts/final/build_health_check.py

The text lives in health_check_text.md (conventions in the comment at its top; same as checkpoint_text.md).
Every chart is built only from the chart-ready CSVs in data/explore/health_check/charts/ (one *_data() per figure):
  exports_orgtype      exports_orgtype.csv
  exports_activity     exports_activity.csv
  india_world_share    india_world_share.csv, india_h1_growth.csv
  revgrowth_peers      revgrowth_peers.csv
  rev_trend_levels     rev_trend_levels.csv
  firm_cc_quarterly    firm_cc_quarterly.csv
  segment_change       segment_change.csv
  top6_headcount       top6_headcount.csv
  rev_vs_hc            rev_vs_hc.csv
  sector_employment    sector_employment.csv
  fresher_intake       fresher_intake.csv
  four_shares          four_shares.csv
  under30              under30.csv
  infosys_grades       infosys_grades.csv
  nirf                 nirf.csv
  junior_pay           junior_pay.csv
  postings_experience  postings_experience.csv
  grad_unemp           grad_unemp.csv
  stress_gauges        business_attrition.csv, business_utilization.csv
  labour_share         business_labour_share.csv
  price_giveback       business_price_giveback.csv
  us_inhouse           demand_us_inhouse_share.csv, demand_ces5415_monthly.csv
  call_themes          demand_call_themes.csv, ai_mentions_halfyear.csv
External resources load only from CDNs: Plotly (cdnjs) and Google Fonts.
"""
import html
import json
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_note import REPO_URL, ROOT, clean, inline, pipe_table  # noqa: E402

OUT = ROOT / "docs" / "health-check.html"
TEXT = ROOT / "health_check_text.md"
CH = ROOT / "data" / "explore" / "health_check" / "charts"
FIRMS6 = [("tcs", "TCS"), ("infosys", "Infosys"), ("hcltech", "HCLTech"), ("wipro", "Wipro"),
          ("techm", "Tech Mahindra"), ("ltim", "LTIMindtree")]
NAME2KEY = {"TCS": "tcs", "Infosys": "infosys", "HCLTech": "hcltech", "Wipro": "wipro", "TechM": "techm",
            "LTIMindtree": "ltim"}


def R(name):
    """Read a chart CSV; some start with a '#' comment line."""
    return pd.read_csv(CH / name, comment="#")


def r(v, nd=2):
    return clean(v, nd)


def L(values, nd=2):
    return [r(v, nd) for v in values]


def qnum(cal_q):
    """'2022Q3' -> 2022.75 (quarter end, as a decimal year)."""
    y, q = cal_q.split("Q")
    return round(int(y) + int(q) / 4, 3)


def fynum(fy):
    return 2000 + int(fy[2:4])


# ---------------------------------------------------------------- chart data (one function per figure)

def exports_orgtype_data():
    d = R("exports_orgtype.csv")
    fys = list(dict.fromkeys(d.fy))
    p = d.pivot(index="fy", columns="exporter_type", values="exports_usd_bn").reindex(fys)
    s = d.pivot(index="fy", columns="exporter_type", values="share_pct").reindex(fys)
    tot = d.groupby("fy").total_exports_usd_bn.first().reindex(fys)
    brk = list(dict.fromkeys(d[d.method_break_flag == 1].fy))
    assert brk == ["FY23"], brk
    return {"fy": fys, "pub": L(p.public_ltd), "priv": L(p.private_ltd), "oth": L(p.others),
            "privshare": L(s.private_ltd, 1), "total": L(tot, 1), "brk": brk[0],
            "missing": [f for f in fys if pd.isna(tot[f])]}


def exports_activity_data():
    d = R("exports_activity.csv")
    fys = ["FY24", "FY25", "FY26"]
    acts = [("it_services", "IT services"), ("bpo", "BPO"), ("engineering", "Engineering services"),
            ("software_products", "Software products")]
    out = []
    for k, lab in acts:
        x = d[d.activity == k].set_index("fy").reindex(fys)
        out.append({"key": k, "label": lab, "v": L(x.exports_usd_bn, 1), "g": L(x.yoy_usd_pct, 1)})
    tot = d[d.activity == "total"].set_index("fy").reindex(fys)
    return {"fy": fys, "acts": out, "total": L(tot.exports_usd_bn, 1)}


def india_world_share_data():
    d = R("india_world_share.csv").pivot(index="year", columns="denominator", values="india_share_pct")
    h = R("india_h1_growth.csv")
    h = h[h.year >= 2021].pivot(index="year", columns="group", values="h1_yoy_pct")
    return {"x": [int(v) for v in d.index], "world": L(d.world_excl_ireland, 1), "group": L(d.emerging_delivery_group, 1),
            "h1": {"x": [int(v) for v in h.index], "india": L(h.india, 1), "others": L(h["24_other_delivery_countries"], 1)}}


def revgrowth_peers_data():
    d = R("revgrowth_peers.csv")
    d = d[d.period.str.match(r"^FY\d\d$") & d.growth_pct.notna()]
    pick = lambda s, b: d[(d.series == s) & (d.currency_basis == b)]
    pack = lambda x: {"x": [fynum(v) for v in x.period], "y": L(x.growth_pct, 1), "n": [int(v) for v in x.n_firms]}
    return {"top6cc": pack(pick("top6_weighted", "cc")), "top6usd": pack(pick("top6_weighted", "usd")),
            "mid": pack(pick("midtier4", "usd")), "acn": pack(pick("accenture", "cc")), "cog": pack(pick("cognizant", "cc"))}


def rev_trend_levels_data():
    d = R("rev_trend_levels.csv")
    out = {}
    for s, key in [("top6_weighted", "top"), ("accenture", "acn")]:
        for m in ["rev_cc", "headcount"]:
            x = d[(d.series == s) & (d.metric == m)]
            out[f"{key}_{m}"] = {"x": [fynum(v) for v in x.fy], "y": L(x.gap_vs_trend_logx100, 1)}
    return out


def firm_cc_quarterly_data():
    d = R("firm_cc_quarterly.csv")
    qs = sorted(d.cal_q.unique())
    fq = d.drop_duplicates("cal_q").set_index("cal_q").fiscal_quarter.reindex(qs)
    firms = []
    for key, name in FIRMS6:
        x = d[d.firm == key].set_index("cal_q").reindex(qs)
        pre = [isinstance(e, str) and e == "lti" for e in x.entity_reported]
        firms.append({"key": key, "name": name, "y": L(x.cc_yoy_pct, 1), "pre": pre})
    return {"x": [qnum(q) for q in qs], "q": qs, "fq": list(fq), "firms": firms}


def segment_change_data():
    d = R("segment_change.csv").set_index("segment")
    rows = [("top6", "Six largest"), ("midtier4", "Mid-tier four"), ("other_it_services_7", "Other IT services (7)"),
            ("erd_5", "Engineering services (5)"), ("ites_bpm_5", "BPM (5)"), ("gcc_tech", "GCCs, tech jobs (estimate)")]
    out = []
    for k, lab in rows:
        x = d.loc[k]
        out.append({"key": k, "label": lab, "hc_pct": r(x.hc_change_pct, 1), "rev_pct": r(x.rev_usd_change_pct, 1),
                    "hc_k": r(x.hc_change_k, 1), "lo": r(x.range_low_k, 0), "hi": r(x.range_high_k, 0),
                    "n": r(x.n_firms_hc, 0), "fell": r(x.n_firms_hc_fell, 0), "acq": r(x.known_acquired_hc_k, 1)})
    return out


def top6_headcount_data():
    d = R("top6_headcount.csv")
    t = d[d.firm == "top6"].sort_values("cal_q")
    t = t[t.cal_q >= "2016Q1"]
    peak = t[t.is_peak].cal_q.tolist()
    assert len(peak) == 1, peak
    return {"x": [qnum(q) for q in t.cal_q], "q": list(t.cal_q), "y": L(t.headcount_persons / 1e6, 4),
            "partial": [bool(v) for v in t.is_partial], "peak": peak[0]}


def rev_vs_hc_data():
    d = R("rev_vs_hc.csv")
    d = d[d.freq == "FY"].pivot(index="period", columns="metric", values="value")
    return {"x": [fynum(v) for v in d.index], "rev": L(d.revenue_index, 1), "hc": L(d.headcount_index, 1),
            "rev_bn": L(d.revenue_usd / 1000, 1), "hc_m": L(d.headcount_fy_end / 1e6, 3)}


def sector_employment_data():
    d = R("sector_employment.csv")
    m = lambda v: r(v / 1e6, 3)
    p = d[d.series == "plfs_nic62_63"]
    plfs = {"x": list(p.plot_date), "lab": list(p.period), "y": L(p.value_m, 3), "lo": [m(v) for v in p.ci90_lo_persons],
            "hi": [m(v) for v in p.ci90_hi_persons]}
    e = d[d.series == "plfs_nic62_63_excl_high_weight_cluster"]
    excl = {"x": list(e.plot_date), "lab": list(e.period), "y": L(e.value_m, 3)}
    o = d[d.series == "plfs_ict_occupations_outside_nic62_63"]
    o = o[o.plot_date >= "2023-01-01"]  # NCO-2004 -> NCO-2015 switch: comparable only from 2022-23
    base = p.set_index("plot_date").value_m
    ict = {"x": list(o.plot_date), "lab": list(o.period), "y": L(o.value_m, 3), "base": [r(base[x], 3) for x in o.plot_date]}
    n = d[d.series == "nasscom_direct_employment"]
    eds = []
    for ed, lab in [("SR Feb 2024", "Feb 2024 edition"), ("SR Feb 2025", "Feb 2025 edition"), ("SR Feb 2026", "Feb 2026 edition")]:
        x = n[n.vintage.str.startswith(ed)]
        eds.append({"label": lab, "x": list(x.plot_date), "lab": list(x.period), "y": L(x.value_m, 3)})
    return {"plfs": plfs, "excl": excl, "ict": ict, "nasscom": eds}


def fresher_intake_data():
    d = R("fresher_intake.csv")
    years = list(range(2016, 2027))
    alias = {"lti": "ltim", "mindtree": "ltim", "ltimindtree": "ltim"}
    f = d[d.group == "firm"].copy()
    f["key"] = f.entity.map(lambda e: alias.get(e, e))
    f["year"] = f.fy.map(fynum)
    g = f.groupby(["key", "year"]).value_persons.sum()
    firms = [{"key": k, "name": nm, "y": [r(g[(k, y)] / 1000, 2) if (k, y) in g.index else None for y in years]}
             for k, nm in FIRMS6]
    cover = [sum(1 for fm in firms if fm["y"][i] is not None) for i in range(len(years))]
    t = d[d.group == "firm_target"]
    targets = [{"key": k, "name": nm, "y": r(t[t.entity == k].value_persons.iloc[0] / 1000, 1)}
               for k, nm in FIRMS6 if k in set(t.entity) and t[t.entity == k].value_persons.notna().any()]
    nontarget = [nm for k, nm in FIRMS6 if k in set(t.entity) and t[t.entity == k].value_persons.isna().all()]
    tp = d[d.group == "thirdparty"]
    src = {"xpheno": "Xpheno", "han_digital": "HAN Digital", "teamlease_digital": "TeamLease Digital"}
    third = [{"src": e, "name": src[e], "x": fynum(x.fy), "fy": x.fy, "y": r(x.value_persons / 1000, 0),
              "lo": r(x.value_low / 1000, 0), "hi": r(x.value_high / 1000, 0), "proj": x.kind == "projection",
              "pub": x.published if isinstance(x.published, str) else ""}
             for e in src for _, x in tp[tp.entity == e].iterrows()]
    s = d[d.series == "sum_tcs_infosys_hcltech"]
    assert abs(s[s.fy == "FY22"].value_persons.iloc[0] - 217782) < 1
    return {"x": years, "firms": firms, "cover": cover, "targets": targets, "nontarget": nontarget, "third": third}


def four_shares_data():
    d = R("four_shares.csv")
    pk = lambda s: d[d.series == s].sort_values("plot_date")
    pack = lambda x: {"x": list(x.plot_date), "lab": list(x.period), "y": L(x.share_pct, 1)}
    a = pk("plfs_it_share_salaried_grads_21_25")
    a_ = dict(pack(a), lo=L(a.ci90_lo_pct, 1), hi=L(a.ci90_hi_pct, 1))
    d_ = pk("foundit_it_industry_share_of_fresher_postings")
    d_ = d_[d_.period.isin(["2025-07", "2026-07"])]
    assert len(d_) == 2
    return {"a": a_, "a_excl": pack(pk("plfs_it_share_salaried_grads_21_25_excl_cluster")),
            "b": pack(pk("epfo_it_share_net_payroll_18_25_annual")),
            "c": pack(pk("xpheno_entry_level_0_2y_share_of_active_tech_openings")), "d": pack(d_)}


def under30_data():
    d = R("under30.csv")
    d = d[d.slope_point.notna()]
    keymap = {"ltimindtree": "ltim"}
    out = []
    for firm, g in d.groupby("firm", sort=False):
        s, e = g[g.slope_point == "start"].iloc[0], g[g.slope_point == "end"].iloc[0]
        out.append({"key": keymap.get(firm, firm), "name": e.firm_label, "fy0": s.fy, "y0": r(s.hc_share_lt30_pct, 1),
                    "fy1": e.fy, "y1": r(e.hc_share_lt30_pct, 1), "fell": e.direction == "fell",
                    "scope": e.scope_note if isinstance(e.scope_note, str) else ""})
    assert len(out) == 10 and sum(o["fell"] for o in out) == 8
    return out


def infosys_grades_data():
    d = R("infosys_grades.csv").pivot(index="fy", columns="band", values="share_pct")
    return {"fy": list(d.index), "junior": L(d.junior, 1), "middle": L(d.middle, 1), "senior": L(d.senior_incl_top, 1)}


def nirf_data():
    d = R("nirf.csv")
    d = d[(d.comparison == "by_grad_year") & (d["sample"] == "balanced")]
    out = {}
    for t in ["elite", "other"]:
        x = d[d.tier == t].sort_values("grad_year")
        out[t] = {"x": list(x.grad_year), "rate": L(x.placement_rate_pct, 1), "sal": L(x.median_inst_median_salary_inr_yr / 1e5, 2),
                  "n": int(x.n_inst.max()), "placed": L(x.placed, 0), "grads": L(x.graduates, 0)}
    out["n_all"] = int(d[d.tier == "all"].n_inst.max())
    return out


def junior_pay_data():
    d = R("junior_pay.csv")
    rounds = list(dict.fromkeys(d["round"]))
    out = {"x": rounds}
    for key, sample, age in [("it21", "cws_regular_nic62_63", "21-25"), ("it26", "cws_regular_nic62_63", "26-30"),
                             ("it31", "cws_regular_nic62_63", "31-40"), ("all21", "cws_regular_all_grads", "21-25")]:
        x = d[(d["sample"] == sample) & (d.age_band == age)].set_index("round").reindex(rounds)
        out[key] = {"y": L(x.mean_real_inr_month / 1000, 2), "lo": L(x.ci90_lo_inr / 1000, 2), "hi": L(x.ci90_hi_inr / 1000, 2)}
    return out


def postings_experience_data():
    d = R("postings_experience.csv")
    a = d[d.panel == "A"]
    b = d[d.panel == "B"]
    pack = lambda s: {"x": [int(v) for v in b[b.series == s].category], "y": L(b[b.series == s].value, 3),
                      "per": list(b[b.series == s].period)}
    return {"a": {"cat": [c.replace("yrs", "years").replace("-", "–") for c in a.category], "v": L(a.value, 1),
                  "lo": L(a.ci95_lo, 1), "hi": L(a.ci95_hi, 1)},
            "b": {"linkedin": pack("linkedin_india_hiring_rate"), "jobspeak": pack("jobspeak_it_software_postings")}}


def grad_unemp_data():
    d = R("grad_unemp.csv")
    rounds = list(dict.fromkeys(d["round"]))
    out = {"x": rounds}
    for age in ["15-25", "21-25"]:
        for c in ["ups", "cws"]:
            x = d[(d.age == age) & (d.concept == c)].set_index("round").reindex(rounds)
            out[f"{c}_{age[:2]}"] = {"y": L(x.ur_pct, 1), "lo": L(x.ci90_lo_pct, 1), "hi": L(x.ci90_hi_pct, 1)}
    return out


def _deviation(df, col):
    qs = sorted(df.cal_q.unique())
    firms = []
    for name, g in df.groupby("firm"):
        g = g.set_index("cal_q").reindex(qs)
        mean = float(g.mean_2016_19_pct.dropna().iloc[0])
        firms.append({"key": NAME2KEY[name], "name": name, "mean": r(mean, 1), "lvl": L(g[col], 1),
                      "dev": [r(v - mean, 1) for v in g[col]]})
    order = [k for k, _ in FIRMS6]
    firms.sort(key=lambda f: order.index(f["key"]))
    return {"x": [qnum(q) for q in qs], "q": qs, "firms": firms}


def stress_gauges_data():
    return {"attr": _deviation(R("business_attrition.csv"), "attrition_ltm_pct"),
            "util": _deviation(R("business_utilization.csv"), "utilization_pct")}


def labour_share_data():
    d = R("business_labour_share.csv")
    labels = {"Top-6 firms": "Six largest firms", "RBI listed IT companies": "RBI listed IT companies",
              "Mid-tier (Persistent, Coforge, Mphasis)": "Mid-tier (Persistent, Coforge, Mphasis)",
              "KLEMS business services": "KLEMS, business services", "NAS group, private corporations (2011-12 base)":
              "National accounts, old base", "NAS group, private corporations (2022-23 base)": "National accounts, new base"}
    out = []
    for s in labels:
        x = d[(d.series == s) & d.labour_share.notna()]
        out.append({"name": labels[s], "role": x.role.iloc[0], "x": [fynum(v) for v in x.fy], "y": L(x.labour_share, 3)})
    return out


def price_giveback_data():
    d = R("business_price_giveback.csv")
    ai = d[d.series == "M2 AI-specific give-back"].set_index("fy")
    gross = d[d.series.str.startswith("M2 gross")].set_index("fy")
    fys = list(ai.index)
    routine = [r(gross.central_pct_yr[f] - ai.central_pct_yr[f], 2) for f in fys]
    assert all(abs(v - 1.55) < 0.01 for v in routine), routine
    brk = d[d.series.str.startswith("Broker")]
    return {"fy": fys, "c": L(ai.central_pct_yr), "lo": L(ai.low_pct_yr), "hi": L(ai.high_pct_yr), "routine": routine,
            "expected": [s != "measured" for s in ai.status],
            "broker": {"fy": list(brk.fy), "lo": r(brk.low_pct_yr.min()), "hi": r(brk.high_pct_yr.max())}}


def us_inhouse_data():
    s = R("demand_us_inhouse_share.csv")
    c = R("demand_ces5415_monthly.csv")
    pk = c.loc[c.ces_5415_emp_k.idxmax()]
    return {"share": {"x": [int(v) for v in s.year], "y": L(s.inhouse_share_pct, 2)},
            "ces": {"x": list(c.date), "y": L(c.ces_5415_emp_k, 1), "peak_x": pk.date, "peak_y": r(pk.ces_5415_emp_k, 1),
                    "last_pct": r(c.pct_from_peak.iloc[-1], 1)}}


def call_themes_data():
    d = R("demand_call_themes.csv")
    a = R("ai_mentions_halfyear.csv").set_index("half_year")
    hy = list(dict.fromkeys(d.half_year))
    get = lambda m, u: d[(d.metric == m) & (d.unit == u)].set_index("half_year").reindex(hy).value
    ai = a.ai_any_per_10k_words.reindex(hy)  # includes the token 'GenAI'
    assert (abs(ai - get("AI mentions", "per 10k words")) < 0.01).all()
    n = d.drop_duplicates("half_year").set_index("half_year").n_calls.reindex(hy)
    return {"x": hy, "demand": L(get("A: demand weakness", "statements per transcript")),
            "pass": L(get("D: AI productivity passed to clients", "statements per transcript")),
            "ai": L(ai, 1), "n": [int(v) for v in n], "partial": [isinstance(v, str) for v in a.low_n_flag.reindex(hy)]}


DATA_FUNCS = {
    "exports_orgtype": exports_orgtype_data, "exports_activity": exports_activity_data, "india_world_share": india_world_share_data,
    "revgrowth_peers": revgrowth_peers_data, "rev_trend_levels": rev_trend_levels_data, "firm_cc_quarterly": firm_cc_quarterly_data,
    "segment_change": segment_change_data, "top6_headcount": top6_headcount_data, "rev_vs_hc": rev_vs_hc_data,
    "sector_employment": sector_employment_data, "fresher_intake": fresher_intake_data, "four_shares": four_shares_data,
    "under30": under30_data, "infosys_grades": infosys_grades_data, "nirf": nirf_data, "junior_pay": junior_pay_data,
    "postings_experience": postings_experience_data, "grad_unemp": grad_unemp_data, "stress_gauges": stress_gauges_data,
    "labour_share": labour_share_data, "price_giveback": price_giveback_data, "us_inhouse": us_inhouse_data,
    "call_themes": call_themes_data,
}


# ---------------------------------------------------------------- figures (HTML shells)

def fig(name, title="", legend="", wide=True, extra=""):
    t = f'<div class="fig-title">{title}</div>' if title else ""
    lg = f'<div class="legend" aria-hidden="true">{legend}</div>' if legend else ""
    top = f'<div class="fig-top">{t}{lg}{extra}</div>' if (t or lg or extra) else ""
    return (f'<figure class="{"wide" if wide else ""}" id="fig-{name}"><div class="fig-panel">{top}'
            f'<div id="chart-{name}" class="chart" role="img" aria-label="{html.escape(re.sub("<[^>]+>", "", title or name))}"></div>'
            '</div><figcaption>{caption}</figcaption></figure>')


def sw(color, hollow=False):
    st = f"border:1.5px solid {color};background:transparent" if hollow else f"background:{color}"
    return f'<span><span class="sw" style="{st}"></span>'


def ln(color, style="solid", w=3):
    return f'<span><i style="border-color:{color};border-top-style:{style};border-top-width:{w}px"></i>'


def mk(glyph, color="var(--ink-2)"):
    return f'<span><b class="mk" style="color:{color}">{glyph}</b>'


FIRM_CSS = {"tcs": "#4d6f91", "infosys": "#b8643f", "hcltech": "#5a9370", "wipro": "#8f68a6", "techm": "#ae8a2c", "ltim": "#c0607e"}
FIRM_LEGEND = "".join(sw(FIRM_CSS[k]) + f"{n}</span>" for k, n in FIRMS6)

FIGURES = {
    "exports_orgtype": fig("exports_orgtype", title="Exports, US$ billion",
                           legend=sw("var(--accent)") + "Public limited</span>" + sw("var(--mid)") + "Private limited</span>"
                           + sw("var(--rule-2)") + "Others</span>"),
    "exports_activity": fig("exports_activity", title="Exports by activity, US$ billion (labels: growth on a year earlier)",
                            legend=sw("#bccde2") + "FY24</span>" + sw("#7b9cc6") + "FY25</span>" + sw("var(--accent)") + "FY26</span>"),
    "india_world_share": fig("india_world_share",
                             legend=sw("var(--accent)") + "India</span>" + sw("var(--rule-2)") + "24 other delivery countries</span>"),
    "revgrowth_peers": fig("revgrowth_peers", title="Revenue growth, % a year",
                           legend=ln("var(--accent)") + "Six largest (constant currency)</span>" + ln("var(--accent)", "dotted", 2)
                           + "Six largest (US$)</span>" + ln("var(--mid)") + "Mid-tier four (US$, incl. acquisitions)</span>"
                           + ln("var(--acn)") + "Accenture (cc)</span>" + ln("#b3a99c", "dashed", 2) + "Cognizant (cc)</span>"),
    "rev_trend_levels": fig("rev_trend_levels", title="Gap to FY16–20 trend, log points",
                            legend=ln("var(--accent)") + "Six largest</span>" + ln("var(--acn)") + "Accenture</span>"
                            + ln("var(--ink-2)", "solid", 2) + "Revenue (cc)</span>" + ln("var(--ink-2)", "dashed", 2) + "Headcount</span>"),
    "firm_cc_quarterly": fig("firm_cc_quarterly", title="Revenue growth on a year earlier, constant currency, %"),
    "segment_change": fig("segment_change", title="FY23 to FY26",
                          legend=sw("var(--accent)") + "Headcount</span>" + sw("var(--cat-a)") + "US$ revenue</span>"
                          + sw("var(--mid)") + "GCC estimate, with range</span>"),
    "top6_headcount": fig("top6_headcount", title="Combined headcount, six largest firms, millions"),
    "rev_vs_hc": fig("rev_vs_hc", title="Six largest firms, index FY19 = 100",
                     legend=ln("var(--accent)") + "Revenue (US$)</span>" + ln("var(--cat-a)") + "Headcount (end-March)</span>"),
    "sector_employment": fig("sector_employment", title="Employment, millions",
                             legend=sw("var(--accent)") + "PLFS: IT (NIC 62–63), 90% interval</span>" + sw("#c8d7ea")
                             + "PLFS: ICT workers in other industries</span>" + mk("○", "var(--accent)")
                             + "Without one high-weight sampling unit</span>" + ln("var(--cat-a)") + "Nasscom, by edition</span>"),
    "fresher_intake": fig("fresher_intake", title="Fresher hires, thousands",
                          legend=FIRM_LEGEND + mk("●") + "Xpheno</span>" + mk("◆") + "HAN Digital</span>" + mk("■")
                          + "TeamLease Digital</span>" + mk("○") + "hollow: target or projection</span>"),
    "four_shares": fig("four_shares", title="IT's share of young entrants, %"),
    "under30": fig("under30", title="Employees under 30, % of headcount",
                   legend=FIRM_LEGEND.replace("Tech Mahindra", "TechM") + sw("var(--mid)") + "Mid-tier firms</span>"),
    "infosys_grades": fig("infosys_grades", title="Infosys employees by grade, % of headcount",
                          legend=sw("var(--accent)") + "Junior</span>" + sw("#9fb8d6") + "Middle</span>" + sw("var(--rule-2)")
                          + "Senior (incl. top)</span>"),
    "nirf": fig("nirf", title="Four-year engineering graduates, same 147 institutions every year",
                legend=ln("var(--accent)") + "Elite institutions</span>" + ln("var(--cat-a)") + "Other institutions</span>"),
    "junior_pay": fig("junior_pay", title="Real monthly pay, ₹ thousand at 2025 prices",
                      legend=ln("var(--accent)") + "IT, aged 21–25 (90% interval)</span>" + ln("#7fa3cf", "solid", 2) + "IT, 26–30</span>"
                      + ln("#163d6b", "solid", 2) + "IT, 31–40</span>" + ln("var(--acn)", "dashed", 2) + "All graduates, 21–25</span>"),
    "postings_experience": fig("postings_experience",
                               legend=ln("var(--accent)") + "Naukri JobSpeak, IT-software postings</span>" + ln("var(--cat-a)")
                               + "LinkedIn hiring rate, all industries</span>"),
    "grad_unemp": fig("grad_unemp", title="Unemployment rate of graduates, %",
                      legend=ln("var(--accent)") + "Principal status</span>" + ln("var(--cat-a)") + "Weekly status</span>"
                      + ln("var(--ink-2)", "solid", 2) + "Aged 15–25</span>" + ln("var(--ink-2)", "dashed", 2) + "Aged 21–25</span>"),
    "stress_gauges": fig("stress_gauges", title="Percentage points above or below each firm's own 2016–19 average",
                         legend=FIRM_LEGEND),
    "labour_share": fig("labour_share", title="Labour share of value added",
                        legend=ln("var(--accent)") + "Six largest firms</span>" + ln("var(--cat-a)") + "RBI listed IT companies</span>"
                        + ln("var(--mid)") + "Mid-tier (Persistent, Coforge, Mphasis)</span>" + ln("var(--ink-3)", "dashed", 2)
                        + "National-accounts measures (different scope)</span>"),
    "price_giveback": fig("price_giveback", title="Price cuts to clients, % of revenue a year",
                          legend=sw("var(--rule-2)") + "Routine pre-AI discount</span>" + sw("var(--accent)") + "AI-related cut, with range</span>"
                          + sw("rgba(176,112,42,0.25)") + "Brokers' forecasts</span>"),
    "us_inhouse": fig("us_inhouse"),
    "call_themes": fig("call_themes", legend=ln("var(--cat-a)") + "Weak demand</span>" + ln("var(--accent)")
                       + "Passing AI savings to clients</span>" + sw("var(--mid)") + "AI mentions</span>" + mk("○")
                       + "hollow / pale: partial half-year</span>"),
}


# ---------------------------------------------------------------- text rendering (as in build_checkpoint.py)

def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", re.sub("<[^>]+>", "", t).lower()).strip("-")


class Doc:
    def __init__(self, tokens, notes):
        self.tokens, self.notes, self.order, self.toc = tokens, notes, [], []

    def il(self, s):
        """inline() plus footnote references, which become hover pop-ups."""
        refs = []

        def take(m):
            refs.append(m.group(1))
            return f"\x02{len(refs) - 1}\x02"
        s = re.sub(r"\[\^([\w-]+)\]", take, s)
        h = inline(s, self.tokens)

        def put(m):
            key = refs[int(m.group(1))]
            if key not in self.order:
                self.order.append(key)
            n = self.order.index(key) + 1
            body = inline(self.notes.get(key, f"MISSING NOTE {key}"), self.tokens)
            return (f'<span class="fn"><a class="fn-ref" href="#note-{key}" aria-label="Note {n}">{n}</a>'
                    f'<span class="fn-pop" role="note"><span class="fn-n">{n}</span> {body}</span></span>')
        return re.sub(r"\x02(\d+)\x02", put, h)

    def block(self, kind, arg, lines, depth):
        if kind == "figure":
            cap = " ".join(l.strip() for l in lines if l.strip())
            assert arg in FIGURES, f"no figure shell for {arg}"
            return FIGURES[arg].replace("{caption}", self.il(cap))
        if kind == "details":
            sid = slug(arg)
            self.toc.append((3, arg, sid, True))
            return (f'<details class="more" id="{sid}"><summary><span class="more-title">{self.il(arg)}</span>'
                    f'<span class="more-hint">Optional detail. Click to expand.</span></summary>'
                    f'<div class="more-body">{self.render(lines, depth + 1)}</div></details>')
        assert kind == "table", f"unknown block kind {kind}"
        st = [l.strip() for l in lines]
        top, note_lines = (lines[:st.index("---")], lines[st.index("---") + 1:]) if "---" in st else (lines, [])
        cap = [l for l in top if l.strip() and not l.strip().startswith("|")]
        tbl = [l for l in top if l.strip().startswith("|")]
        note = " ".join(l.strip() for l in note_lines if l.strip())
        return ('<div class="table-wrap">' + f'<p class="table-cap">{self.il(" ".join(cap))}</p>' + pipe_table(tbl, self.tokens) +
                (f'<p class="table-note">{self.il(note)}</p>' if note else "") + "</div>")

    def render(self, lines, depth=0):
        out, para, i = [], [], 0
        appendix = False

        def flush():
            if para:
                out.append(f"<p>{self.il(' '.join(para))}</p>")
                para.clear()
        while i < len(lines):
            st = lines[i].strip()
            if not st:
                flush(); i += 1; continue
            if st.startswith("<!--"):
                flush()
                while "-->" not in lines[i]:
                    i += 1
                i += 1; continue
            if st.startswith("## "):
                flush()
                title = st[3:]
                m = re.match(r"(\d+)\.\s+(.*)", title)
                num, t = (m.group(1), m.group(2)) if m else ("", title)
                sid = slug(t)
                self.toc.append((2, (f"{num}. " if num else "") + t, sid, False))
                appendix = t.lower().startswith("appendix")
                out.append(f'<h2 id="{sid}">' + (f'<span class="num">{num}</span>' if num else "") + f"{self.il(t)}</h2>")
                i += 1; continue
            if st.startswith("### "):
                flush()
                t = st[4:]
                sid = slug(t)
                if appendix:
                    out.append(f'<details class="app" id="{sid}"><summary>{self.il(t)}</summary><div>')
                    j = i + 1
                    while j < len(lines) and not lines[j].strip().startswith(("### ", "## ")) and not re.match(r"^\[\^[\w-]+\]:", lines[j].strip()):
                        j += 1
                    out.append(self.render(lines[i + 1:j], depth + 1))
                    out.append("</div></details>")
                    i = j; continue
                self.toc.append((3, t, sid, False))
                out.append(f'<h3 id="{sid}">{self.il(t)}</h3>')
                i += 1; continue
            if st.startswith(":::") and st != ":::":
                flush()
                parts = st[3:].strip().split(None, 1)
                kind, arg = parts[0], (parts[1] if len(parts) > 1 else None)
                j, d = i + 1, 1
                while True:
                    s2 = lines[j].strip()
                    if s2 == ":::":
                        d -= 1
                        if d == 0:
                            break
                    elif s2.startswith(":::"):
                        d += 1
                    j += 1
                out.append(self.block(kind, arg, lines[i + 1:j], depth))
                i = j + 1; continue
            if re.match(r"^\[\^[\w-]+\]:", st):
                flush(); i += 1; continue
            if re.match(r"^(- |\d+\. )", st):
                flush()
                ordered = bool(re.match(r"^\d+\. ", st))
                items = []
                while i < len(lines) and re.match(r"^(- |\d+\. )", lines[i].strip()):
                    items.append(re.sub(r"^(- |\d+\. )", "", lines[i].strip()))
                    i += 1
                lis = "".join(f"<li>{self.il(it)}</li>" for it in items)
                out.append(f"<ol>{lis}</ol>" if ordered else f"<ul>{lis}</ul>")
                continue
            para.append(st)
            i += 1
        flush()
        return "\n".join(o for o in out if o)


def toc_html(toc):
    items, open_sub = [], False
    for level, title, sid, collapsible in toc:
        label = inline(title, {})
        if level == 2:
            if open_sub:
                items.append("</ul></li>"); open_sub = False
            items.append(f'<li><a href="#{sid}" data-target="{sid}">{label}</a><ul>')
            open_sub = True
        else:
            cls = ' class="opt"' if collapsible else ""
            items.append(f'<li{cls}><a href="#{sid}" data-target="{sid}">{label}</a></li>')
    if open_sub:
        items.append("</ul></li>")
    html_ = "".join(items).replace("<ul></ul>", "")
    return f'<nav class="toc" aria-label="Contents"><div class="toc-head">Contents</div><ul>{html_}</ul></nav>'


# ---------------------------------------------------------------- page

TEMPLATE = (Path(__file__).resolve().parent / "health_check_template.html").read_text(encoding="utf-8")


def main():
    raw = TEXT.read_text(encoding="utf-8")
    fm, body = raw[3:].split("\n---", 1)
    front = dict((k.strip(), v.strip()) for k, v in (l.split(":", 1) for l in fm.strip().splitlines()))
    notes = dict(re.findall(r"^\[\^([\w-]+)\]:\s*(.+)$", body, flags=re.M))
    repo = f'<a href="{REPO_URL}">{REPO_URL.replace("https://", "")}</a>'
    doc = Doc({"repo": repo}, notes)
    main_html = doc.render(body.splitlines())
    missing = [k for k in doc.order if k not in notes]
    assert not missing, f"undefined footnotes: {missing}"
    unused = [k for k in notes if k not in doc.order]
    assert not unused, f"unused footnotes: {unused}"
    notes_html = "".join(f'<li id="note-{k}">{inline(notes[k], doc.tokens)}</li>' for k in doc.order)
    main_html += (f'<details class="app" id="notes"><summary>All notes</summary><div><ol class="notes">{notes_html}</ol></div></details>'
                  '<p class="footer">Built from <code>health_check_text.md</code> and the CSVs in '
                  '<code>data/explore/health_check/charts/</code> by <code>scripts/final/build_health_check.py</code>.</p>')
    byline = " · ".join(html.escape(p.strip()) for p in front["byline"].split("·"))
    header = (f'<header><p class="crumbs"><a href="index.html">Pilot note</a> · <a href="two-questions.html">Two questions '
              f'(working draft)</a> · <b>Health check</b></p>'
              f'<h1>{inline(front["title"], {})}</h1>'
              f'<p class="byline">{byline}</p>'
              f'<p class="thanks">{inline(front["thanks"], doc.tokens)}</p></header>')
    used = re.findall(r'id="chart-(\w+)"', main_html)
    assert len(used) == len(set(used)), "a chart appears twice"
    data = {k: DATA_FUNCS[k]() for k in used if k in DATA_FUNCS}
    assert set(used) == set(data), f"charts without data: {set(used) - set(data)}"
    assert set(DATA_FUNCS) == set(used), f"data built for charts not in the text: {set(DATA_FUNCS) - set(used)}"
    registry = set(re.findall(r'"chart-(\w+)":\s*fig', TEMPLATE))
    assert registry == set(used), f"CHARTS registry mismatch: missing {set(used) - registry}, extra {registry - set(used)}"
    data_json = json.dumps(data, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    page = (TEMPLATE.replace("%%TITLE%%", html.escape(re.sub("<[^>]+>", "", front["title"])))
            .replace("%%TOC%%", toc_html(doc.toc))
            .replace("%%BODY%%", header + '<details class="toc-mobile"><summary>Contents</summary>' + toc_html(doc.toc) + "</details>\n" + main_html)
            .replace("%%DATA%%", data_json))
    assert "%%" not in page, "leftover template placeholder"
    assert "MISSING NOTE" not in page
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(page) / 1024:.0f} KB); {len(doc.order)} notes; {len(used)} charts: {used}")


if __name__ == "__main__":
    main()
