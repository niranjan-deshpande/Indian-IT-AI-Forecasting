"""Build the working-draft checkpoint page (docs/two-questions.html) for GitHub Pages.

    python3 scripts/final/build_checkpoint.py

The text lives in checkpoint_text.md (conventions in the comment at its top). Every chart is built from repo CSVs:
  levels, rpelevel   output/final/table_A.csv (cumulated growth vs FY16-20 trend; reproduces round4/robustness/baseline)
  sector             data/explore/round3/plfs/employment_levels_long.csv, key_series_grads_21_30.csv
  subcon             output/final/fig2_data.csv (as in the pilot note)
  kept, sbar         data/explore/round4/robustness/m1_scope_subcon/m1_top6.csv, sbar_phi_ai_share.csv
  prices             data/explore/round4/price_statements/m2_aggregate.csv
  infosyshires       data/explore/round4/junior_gap/stockflow_firm_year.csv
  under30            data/explore/workforce/firm_year_junior_metrics.csv
  juniorpay          data/explore/round4/junior_gap/plfs_relative_pay.csv
  yardsticks         data/explore/round4/robustness/baseline/r1_summary.csv
  demand, decomp     data/explore/round4/robustness/demand/d_bounds_r3.csv (+ r1_summary, sbar_phi_ai_share)
  clients            data/explore/round4/demand_shift/proxy_prepost_summary.csv
  inhouse            data/explore/round4/demand_shift/oews_computer_occ_by_bucket.csv, robustness/demand/oews_ces_check.csv
  gcc                data/explore/round4/robustness/demand/gcc_rbi_relative_growth.csv
  listed             data/explore/round3/listed_panel/listed_panel_summary.csv
  share              data/explore/round3/offshore_competitors/india_share_summary.csv
  jevons             computed from the replacement rate (sbar_phi_ai_share.csv) and the elasticity prior
External resources load only from CDNs: Plotly, KaTeX (cdnjs) and Google Fonts.
"""
import html
import json
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_note import FINAL, REPO_URL, ROOT, clean, fig2_data, inline, pipe_table  # noqa: E402

OUT = ROOT / "docs" / "two-questions.html"
TEXT = ROOT / "checkpoint_text.md"
EX = ROOT / "data" / "explore"
R4 = EX / "round4"
R3 = EX / "round3"
FIRMS6 = [("tcs", "TCS"), ("infosys", "Infosys"), ("hcltech", "HCLTech"), ("wipro", "Wipro"),
          ("techm", "Tech Mahindra"), ("ltim", "LTIMindtree")]
EPS_CENTRE = 0.9  # price-elasticity prior for IT services (round4/elasticity_xsec, §6)


def r(v, nd=2):
    return None if v is None or pd.isna(v) else round(float(v), nd)


# ---------------------------------------------------------------- chart data

def trend_gap(values, base_years):
    """Cumulate annual log growth into a level (FY20 = 0) and return the gap to the FY16-20 mean-growth trend."""
    fys = list(range(2015, 2027))
    g = {y: values.get(f"FY{y % 100:02d}") for y in fys[1:]}
    lvl, cur = {2015: 0.0}, 0.0
    for y in fys[1:]:
        cur += 0.0 if g[y] is None or pd.isna(g[y]) else g[y]
        lvl[y] = cur
    g0 = sum(g[y] for y in base_years) / len(base_years)
    first = base_years[0] - 1
    return {"x": [y for y in fys if y >= first],
            "y": [r(lvl[y] - lvl[2020] - g0 * (y - 2020)) for y in fys if y >= first]}


def levels_data():
    t = pd.read_csv(FINAL / "table_A.csv")
    get = lambda grp, m: t[(t.group == grp) & (t.metric == m)].set_index("period").value.to_dict()
    out = {}
    for m in ["headcount", "rev_cc", "rpe_cc"]:
        out[m] = {"top": trend_gap(get("Indian simple average", m), [2016, 2017, 2018, 2019, 2020]),
                  "acn": trend_gap(get("Accenture", m), [2017, 2018, 2019, 2020])}
    # check against round4/robustness/baseline (R1)
    gaps = pd.read_csv(R4 / "robustness/baseline/r1_level_gaps_group.csv").set_index("metric")
    for m in ["headcount", "rev_cc", "rpe_cc"]:
        y = dict(zip(out[m]["top"]["x"], out[m]["top"]["y"]))
        assert abs(y[2023] - gaps.loc[m, "gap_vs_trend_fy23"]) < 0.05, (m, y[2023])
        assert abs(y[2026] - gaps.loc[m, "gap_vs_trend_fy26"]) < 0.05, (m, y[2026])
    return out


def sector_data():
    e = pd.read_csv(R3 / "plfs/employment_levels_long.csv")
    e = e[(e.group == "nic62_63") & (e.cut == "all")]
    k = pd.read_csv(R3 / "plfs/key_series_grads_21_30.csv")
    k = k[k.series == "nic62_63"]
    lab = lambda s: {"cy2024": "CY2024", "cy2025": "CY2025"}.get(s, s)
    pack = lambda d: {"x": [lab(v) for v in d["round"]], "y": [r(v / 1e6, 3) for v in d.estimate],
                      "lo": [r(v / 1e6, 3) for v in d.ci90_lo], "hi": [r(v / 1e6, 3) for v in d.ci90_hi]}
    return {"all": pack(e), "young": pack(k)}


M1_WINDOWS = [("baseline FY16-20 only", "FY16–20"), ("base: FY16-23 vs FY24-26", "FY16–23"),
              ("excl. FY22-23 (boom)", "FY16–23 without the boom"), ("excl. FY21", "FY16–23 without FY21 (COVID)")]


def kept_data():
    m = pd.read_csv(R4 / "robustness/m1_scope_subcon/m1_top6.csv")
    m = m[m.weighting == "equal"]
    rows = []
    for w, label in M1_WINDOWS:
        u = m[(m.variant == "uncorrected") & (m.window == w)].iloc[0]
        c = {v: m[(m.variant.str.startswith(v)) & (m.window == w)].iloc[0] for v in ["k_lo", "k_mid", "k_hi"]}
        rows.append({"label": label,
                     "unc": {"c": r(u.m1_central), "blo": r(u.bound_lo), "bhi": r(u.bound_hi),
                             "slo": r(u.union95_lo), "shi": r(u.union95_hi)},
                     "cor": {"c": r(c["k_mid"].m1_central), "blo": r(c["k_lo"].bound_lo), "bhi": r(c["k_hi"].bound_hi),
                             "slo": r(min(x.union95_lo for x in c.values())), "shi": r(max(x.union95_hi for x in c.values()))}})
    return rows


def sbar_data():
    s = pd.read_csv(R4 / "robustness/m1_scope_subcon/sbar_phi_ai_share.csv")
    s = s[(s.weighting == "equal") & (s.window == "baseline FY16-20 only")]
    m = pd.read_csv(R4 / "robustness/m1_scope_subcon/m1_top6.csv")
    m = m[(m.weighting == "equal") & (m.window == "baseline FY16-20 only")]
    pick = lambda df, v: df[df.variant.str.startswith(v)].iloc[0]
    mid, lo, hi = pick(s, "k_mid"), pick(s, "k_lo"), pick(s, "k_hi")
    mm, ml, mh = pick(m, "k_mid"), pick(m, "k_lo"), pick(m, "k_hi")
    m2 = pd.read_csv(R4 / "price_statements/m2_aggregate.csv")
    m2 = m2[(m2.segment == "IT top-6") & m2.fy.isin(["FY24", "FY25", "FY26"])]
    # M2 enters sbar_phi_ai_share as the equal-weighted FY24-26 mean (0.20; range 0.03-0.59; bias-widened to 1.19)
    m2c = float(mid.m2_central)
    return {"kept": {"c": r(mm.m1_central), "blo": r(ml.bound_lo), "bhi": r(mh.bound_hi),
                     "slo": r(min(ml.union95_lo, mm.union95_lo, mh.union95_lo)), "shi": r(max(ml.union95_hi, mm.union95_hi, mh.union95_hi))},
            "passed": {"c": r(m2c), "blo": 0.03, "bhi": 0.59, "slo": 0.0, "shi": 1.19},
            "total": {"c": r(mid.sbar_central), "blo": r(lo.sbar_bound_lo), "bhi": r(hi.sbar_bound_hi),
                      "slo": r(min(lo.sbar_wide_lo, mid.sbar_wide_lo, hi.sbar_wide_lo)),
                      "shi": r(max(lo.sbar_wide_hi, mid.sbar_wide_hi, hi.sbar_wide_hi))},
            "m2_rev_weighted_mean": r(m2.central.mean())}


def prices_data():
    m = pd.read_csv(R4 / "price_statements/m2_aggregate.csv")
    m = m[m.segment == "IT top-6"]
    return {"fy": list(m.fy), "base": [r(v) for v in m.baseline_central], "ai": [r(v) for v in m.central],
            "lo": [r(v) for v in m.low], "hi": [r(v) for v in m.high]}


def infosys_hires_data():
    s = pd.read_csv(R4 / "junior_gap/stockflow_firm_year.csv")
    s = s[s.firm == "infosys"].sort_values("fy")
    return {"x": [int(v) for v in s.fy], "j": [int(v) for v in s.hires_J], "e": [int(v) for v in s.hires_E]}


def under30_data():
    w = pd.read_csv(EX / "workforce/firm_year_junior_metrics.csv")
    out = []
    alias = {"ltim": ["mindtree", "ltimindtree"]}  # LTIMindtree: Mindtree before the FY23 merger
    for key, name in FIRMS6:
        d = w[w.firm.isin(alias.get(key, [key])) & w.sh_lt30.notna()].sort_values("fy")
        if len(d):
            out.append({"key": key, "name": name, "x": [int(v) for v in d.fy], "y": [r(v, 1) for v in d.sh_lt30]})
    return out


def junior_pay_data():
    p = pd.read_csv(R4 / "junior_gap/plfs_relative_pay.csv")
    lab = {"cy2024": "CY2024", "cy2025": "CY2025"}
    out = {}
    for key, sample in [("it", "cws_regular_nic62_63"), ("all", "cws_regular_all_grads")]:
        d = p[p["sample"] == sample]
        out[key] = {"x": [lab.get(v, v) for v in d["round"]], "y": [r(v, 3) for v in d.ratio_mean],
                    "lo": [r(v * (2.718281828 ** -se), 3) for v, se in zip(d.ratio_mean, d.lnratio_se)],
                    "hi": [r(v * (2.718281828 ** se), 3) for v, se in zip(d.ratio_mean, d.lnratio_se)]}
    return out


def yardsticks_data():
    s = pd.read_csv(R4 / "robustness/baseline/r1_summary.csv").set_index("cf")
    names = [("a0", "Pre-COVID growth rates"), ("c", "Pre-COVID path"), ("e", "Peers (Accenture, Cognizant)")]
    return {"labels": [n for _, n in names], "L": [r(s.loc[k, "dg_L"]) for k, _ in names],
            "R": [r(s.loc[k, "dg_R_cc"]) for k, _ in names]}


def demand_data():
    d = pd.read_csv(R4 / "robustness/demand/d_bounds_r3.csv")
    row = lambda pat: d[d.component.str.startswith(pat)].iloc[0]
    y = yardsticks_data()
    comps = [("Clients' overall spending", row("market, destination-weighted")),
             ("Clients doing the work themselves", row("share, destination-weighted")),
             ("GCCs (change in their pace)", row("GCC, net of pre-2023")),
             ("All measured causes", row("R3 vendor total"))]
    return {"implied": [{"label": f"Implied by {lab[0].lower() + lab[1:]}", "c": v}
                        for lab, v in zip(y["labels"], y["R"])],
            "measured": [{"label": lab, "c": r(x.central), "lo": r(x.low), "hi": r(x.high)} for lab, x in comps]}


def clients_data():
    p = pd.read_csv(R4 / "demand_shift/proxy_prepost_summary.csv").set_index("series")
    rows = [("real_gdp", "US real GDP"), ("bank3_comm_it_expense", "Big-bank technology spending"),
            ("bea_ownacct_real", "US in-house software investment (real)"),
            ("oews_comp_client_inhouse", "US computer jobs at client firms")]
    return [{"label": lab, "pre": r(p.loc[k, "avg_g_2016_22"]), "post": r(p.loc[k, "avg_g_2023_25"])} for k, lab in rows]


def inhouse_data():
    o = pd.read_csv(R4 / "demand_shift/oews_computer_occ_by_bucket.csv")
    c = pd.read_csv(R4 / "robustness/demand/oews_ces_check.csv").set_index("year")
    idx = lambda s: [r(100 * v / s.loc[2022], 1) for v in s]
    return {"share": {"x": [int(v) for v in o.year], "y": [r(100 * v, 2) for v in o.inhouse_share_client_over_client_plus_5415]},
            "emp": {"x": [int(v) for v in c.index], "oews": idx(c.oews_total_5415_k), "ces": idx(c.ces_may_5415_k)}}


def gcc_data():
    g = pd.read_csv(R4 / "robustness/demand/gcc_rbi_relative_growth.csv")
    return {"fy": [f"FY{int(v) % 100:02d}" for v in g.fy], "subs": [r(v, 1) for v in g.within_round_growth_usd_pct_approx],
            "total": [r(v, 1) for v in g.total_sw_exports_growth_usd]}


def listed_data():
    s = pd.read_csv(R3 / "listed_panel/listed_panel_summary.csv")
    s = s[s.metric == "hc"].set_index("set")
    acq = lambda note: float(re.search(r"known acquired heads (\d+)", note).group(1)) if isinstance(note, str) and "acquired" in note else 0.0
    groups = [("mid4", "Mid-tier four"), ("ITservices_ex_mid4_7", "7 other IT services firms"), ("ERD_5", "5 engineering firms"),
              ("ITeS_BPM_5", "5 BPO firms")]
    rows = [{"label": "Top six", "total": -61.466, "acq": 0.0}]  # 1,679,489 -> 1,618,023 (round3/listed_panel FINDINGS)
    for k, lab in groups:
        rows.append({"label": lab, "total": r(s.loc[k, "abs_change_FY23_26"] / 1000, 2), "acq": r(acq(s.loc[k, "note"]) / 1000, 2)})
    return rows


def share_data():
    s = pd.read_csv(R3 / "offshore_competitors/india_share_summary.csv")
    pick = lambda m: s[s.metric == m].sort_values("year")
    w = pick("India share excl. Ireland, balanced panel 2015-2025, %")
    u = pick("India share of US computer-services imports, %")
    u = u[u.year >= 2015]
    return {"world": {"x": [int(v) for v in w.year], "y": [r(v, 1) for v in w.value]},
            "us": {"x": [int(v) for v in u.year], "y": [r(v, 1) for v in u.value]}}


def decomp_data():
    s = pd.read_csv(R4 / "robustness/baseline/r1_summary.csv").set_index("cf")
    sb = sbar_data()
    d = pd.read_csv(R4 / "robustness/demand/d_bounds_r3.csv")
    measured = float(d[d.component.str.startswith("R3 vendor total")].central.iloc[0])
    total = float(s.loc["a0", "dg_L"])
    sbar, m2 = sb["total"]["c"], sb["passed"]["c"]
    insource = 1.1  # round4/robustness/m1_scope_subcon FINDINGS §5: in-sourced subcontracted work, +1.1 pp/yr
    price = round(EPS_CENTRE * m2, 2)
    demand = round(total + sbar - price - insource, 2)
    return {"total": r(total), "parts": [
        {"label": "AI replacement", "v": r(-sbar)},
        {"label": "Clients buying more<br>at lower prices", "v": price},
        {"label": "Subcontracted work<br>brought in-house", "v": insource},
        {"label": "Demand shift:<br>measured", "v": r(measured)},
        {"label": "Demand shift:<br>unexplained", "v": r(demand - measured)}]}


def jevons_data():
    sb = sbar_data()
    return {"s": sb["total"]["c"], "phi_now": r(sb["passed"]["c"] / sb["total"]["c"], 3), "eps": [0.5, 0.9, 1.5]}


# ---------------------------------------------------------------- figures (HTML shells)

def fig(name, title="", legend="", wide=True, extra=""):
    t = f'<div class="fig-title">{title}</div>' if title else ""
    lg = f'<div class="legend" aria-hidden="true">{legend}</div>' if legend else ""
    top = f'<div class="fig-top">{t}{lg}{extra}</div>' if (t or lg or extra) else ""
    return (f'<figure class="{"wide" if wide else ""}" id="fig-{name}"><div class="fig-panel">{top}'
            f'<div id="chart-{name}" class="chart" role="img" aria-label="{html.escape(re.sub("<[^>]+>", "", title or name))}"></div>'
            '</div><figcaption>{caption}</figcaption></figure>')


def sw(color):
    return f'<span><span class="sw" style="background:{color}"></span>'


def ln(color, style="solid", w=3):
    return f'<span><i style="border-color:{color};border-top-style:{style};border-top-width:{w}px"></i>'


CHAIN = """<figure class="wide" id="fig-chain"><div class="fig-panel chain-panel">
<div class="chain">
  <div class="node q1"><span class="tag">Question 1</span><b>AI saves labour</b><span>Fewer workers needed for each piece of work</span></div>
  <div class="arrow" aria-hidden="true"></div>
  <div class="node split"><b>The firm either…</b>
    <div class="pair"><div class="mini">keeps the saving<span>higher revenue per worker</span></div><div class="mini hot">passes it on<span>a lower price for clients</span></div></div></div>
  <div class="arrow" aria-hidden="true"></div>
  <div class="node q2"><span class="tag">Question 2</span><b>Clients buy more?</b><span>If the work is cheaper, more of it may be bought</span></div>
  <div class="arrow" aria-hidden="true"></div>
  <div class="node jobs"><b>Jobs</b><span>amount of work × workers per piece of work</span></div>
</div>
<div class="side"><div class="node d"><b>Demand shift</b><span>Everything else that changes the amount of work: client budgets, clients doing work themselves, work moving to other firms</span></div></div>
</div><figcaption>{caption}</figcaption></figure>"""

FIGURES = {
    "chain": CHAIN,
    "levels": fig("levels", legend=ln("var(--accent)") + "Top six</span>" + ln("var(--acn)", "dashed", 2.5) + "Accenture</span>"
                  + ln("var(--ink-3)", "dotted", 2) + "FY16–20 trend</span>"),
    "sector": fig("sector", legend=sw("var(--accent)") + "Estimate, with 90% interval</span>"),
    "subcon": fig("subcon", title="Subcontracting cost, % of revenue"),
    "kept": fig("kept", legend=sw("var(--ink-3)") + "Before subcontracting correction</span>" + sw("var(--accent)") + "After</span>"),
    "prices": fig("prices", title="Price cuts to clients, % of revenue a year",
                  legend=sw("#cfc4b4") + "Routine pre-AI discount</span>" + sw("var(--accent)") + "Extra cut from AI</span>"),
    "sbar": fig("sbar", title="The replacement rate, percentage points a year"),
    "rpelevel": fig("rpelevel", title="Revenue per employee, gap to FY16–20 trend (log points ×100)",
                    legend=ln("var(--accent)") + "Top six</span>" + ln("var(--acn)", "dashed", 2.5) + "Accenture</span>"),
    "infosyshires": fig("infosyshires", title="Infosys hires a year, thousands",
                        legend=sw("var(--accent)") + "Under 30</span>" + sw("var(--cat-a)") + "30 and over</span>"),
    "under30": fig("under30", title="Share of headcount under 30, %"),
    "juniorpay": fig("juniorpay", title="Pay at 21–25 relative to 31–40",
                     legend=ln("var(--accent)") + "IT (industry 62–63)</span>" + ln("var(--acn)", "dashed", 2.5) + "All graduates</span>"),
    "yardsticks": fig("yardsticks", title="Fall in growth, FY24–26, percentage points a year",
                      legend=sw("var(--accent)") + "Headcount</span>" + sw("var(--cat-a)") + "Revenue (constant currency)</span>"),
    "demand": fig("demand", title="Demand shift, percentage points a year"),
    "clients": fig("clients", title="Growth, % a year",
                   legend=sw("var(--ink-3)") + "2016–22</span>" + sw("var(--accent)") + "2023–25</span>"),
    "inhouse": fig("inhouse", legend=ln("var(--accent)") + "Occupational survey (OEWS)</span>" + ln("var(--cat-a)", "dashed", 2.5)
                   + "Payroll survey (CES)</span>"),
    "gcc": fig("gcc", title="Export growth, % (US dollars)",
               legend=sw("var(--mid)") + "Foreign-owned subsidiaries</span>" + sw("var(--ink-3)") + "All software exports</span>"),
    "listed": fig("listed", title="Change in headcount, FY23 to FY26, thousands",
                  legend=sw("var(--accent)") + "Organic or not stated</span>" + sw("#9fb8d6") + "Acquired (lower bound)</span>"),
    "share": fig("share", title="India's share, %",
                 legend=ln("var(--accent)") + "World computer-services exports (excl. Ireland)</span>" + ln("var(--cat-a)", "dashed", 2.5)
                 + "US computer-services imports</span>"),
    "jevons": fig("jevons", title="AI's net effect on job growth, points a year"),
    "decomp": fig("decomp", title="Fall in headcount growth, FY24–26 against FY16–20, points a year"),
}


# ---------------------------------------------------------------- text rendering

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
            body = inline(self.notes[key], self.tokens)
            return (f'<span class="fn"><a class="fn-ref" href="#note-{key}" aria-label="Note {n}">{n}</a>'
                    f'<span class="fn-pop" role="note"><span class="fn-n">{n}</span> {body}</span></span>')
        return re.sub(r"\x02(\d+)\x02", put, h)

    def block(self, kind, arg, lines, depth):
        if kind == "figure":
            cap = " ".join(l.strip() for l in lines if l.strip())
            return FIGURES[arg].replace("{caption}", self.il(cap))
        if kind == "answer":
            return f'<div class="answer"><span class="answer-tag">Short answer</span>{self.render(lines, depth + 1)}</div>'
        if kind == "details":
            sid = slug(arg)
            self.toc.append((3, arg, sid, True))
            return (f'<details class="more" id="{sid}"><summary><span class="more-title">{self.il(arg)}</span>'
                    f'<span class="more-hint">Optional detail. Click to expand.</span></summary>'
                    f'<div class="more-body">{self.render(lines, depth + 1)}</div></details>')
        # table
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
            if st == "$$":
                flush()
                j = i + 1
                while lines[j].strip() != "$$":
                    j += 1
                tex = " ".join(l.strip() for l in lines[i + 1:j])
                out.append(f'<div class="math" data-tex="{html.escape(tex)}"><span class="math-fallback">{html.escape(tex)}</span></div>')
                i = j + 1; continue
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

TEMPLATE = (Path(__file__).resolve().parent / "checkpoint_template.html").read_text(encoding="utf-8")


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
                  '<p class="footer">Built from <code>checkpoint_text.md</code> and the repository CSVs by '
                  '<code>scripts/final/build_checkpoint.py</code>.</p>')
    byline_parts = [p.strip() for p in front["byline"].split("·")]
    header = (f'<header><p class="crumbs"><a href="index.html">Pilot note</a> · <b>Two questions (working draft)</b></p>'
              f'<h1>{inline(front["title"], {})}</h1>'
              f'<p class="byline">{" · ".join(byline_parts[:-1])} · <span class="tag">{html.escape(byline_parts[-1])}</span></p>'
              f'<p class="thanks">{inline(front["thanks"], doc.tokens)}</p></header>')
    data = {"levels": levels_data(), "sector": sector_data(), "subcon": fig2_data(), "kept": kept_data(),
            "sbar": sbar_data(), "prices": prices_data(), "infosyshires": infosys_hires_data(), "under30": under30_data(),
            "juniorpay": junior_pay_data(), "yardsticks": yardsticks_data(), "demand": demand_data(),
            "clients": clients_data(), "inhouse": inhouse_data(), "gcc": gcc_data(), "listed": listed_data(),
            "share": share_data(), "decomp": decomp_data(), "jevons": jevons_data()}
    used = set(re.findall(r'id="chart-(\w+)"', main_html))
    assert used <= set(data) | {"rpelevel"}, used - set(data)
    page = (TEMPLATE.replace("%%TITLE%%", html.escape(re.sub("<[^>]+>", "", front["title"])))
            .replace("%%TOC%%", toc_html(doc.toc))
            .replace("%%BODY%%", header + '<details class="toc-mobile"><summary>Contents</summary>' + toc_html(doc.toc) + "</details>\n" + main_html)
            .replace("%%DATA%%", json.dumps(data, ensure_ascii=False, separators=(",", ":"))))
    assert "%%" not in page
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(page) / 1024:.0f} KB); {len(doc.order)} notes; charts: {sorted(used)}")


if __name__ == "__main__":
    main()
