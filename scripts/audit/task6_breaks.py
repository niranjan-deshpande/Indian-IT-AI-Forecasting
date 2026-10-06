"""Audit Task 1b, item 6: structural breaks (mergers, divestitures, definition changes, acquisitions).

Outputs (ROOT/audit/):
  structural_breaks_jumps.csv  firm-quarters 2015Q2+ outside 2021-22 with |gR|, |gR_usd| or |gL| > 15, plus QoQ level
                               jumps in headcount / USD revenue > 6% (any year), each with the explanation found
                               in the firm's own documents (or 'not explained in collected documents')
  ltim_switch_check.csv        LTI / Mindtree / LTIM around the merger and the Indian aggregate at the switch
  hcl_divestiture_check.csv    HCLTech gL with and without the D10 base adjustment
"""
import argparse
import numpy as np
import pandas as pd
from audit_common import AUD, qadd, qrange, load_yoy, load_core, indian_panel, aggregate

ap = argparse.ArgumentParser()
ap.add_argument("--yoy", default=None)
ap.add_argument("--core", default=None)
ap.add_argument("--tag", default="")
args = ap.parse_args()
yoy, core = load_yoy(args.yoy), load_core(args.core)

# Explanations, each with the primary document it comes from (local copy under data/sources/<firm>/).
# Keys: (firm, first cal_q, last cal_q, which series). Only statements read in the documents are recorded.
EXPLAIN = [
    ("accenture", "2015Q3", "2016Q1", "headcount",
     "organic hiring per filing: 'Based on current and projected future demand, we have increased our headcount ... to approximately 373,000 as of November 30, 2015 ... approximately 319,000 as of November 30, 2014'",
     "Accenture 10-Q for quarter ended 2015-11-30 (sec.gov/Archives/edgar/data/1467373, local data/sources/accenture/10q/2015-12-17_10-Q_acn-20151130x10q.htm), MD&A 'Overview'; same wording in 10-K FY15 for 336k->358k"),
    ("accenture", "2017Q4", "2018Q3", "rev_usd",
     "ASC 606 basis mix: FY18 levels in the tidy panel are the restated post-ASC 606 vintage (incl. reimbursements, from FY19 releases) while FY17 levels are net revenues; gR_usd overstated by ~4pp; gR (cc, as reported) unaffected",
     "data/raw/accenture.csv revenue rows for Q1FY17-Q4FY18 (notes column: 'Net revenues' vs 'Revenues (post ASC 606)'); Accenture 8-K Ex.99 for Q1FY19-Q4FY19 (prior-year columns)"),
    ("accenture", "2016Q1", "2026Q2", "rev_usd_qoq",
     "Accenture fiscal-quarter seasonality in USD levels (Dec-Feb quarter seasonally low, Mar-May / Sep-Nov high) plus FX; YoY series show no break",
     "data/tidy/core_quarterly.csv (pattern recurs every year); YoY cc growth in Accenture 8-K releases continuous"),
    ("accenture", "2021Q3", "2021Q4", "headcount", "inside 2021-22 boom (Accenture reported hiring to demand); not a definitional break", "Accenture 10-Q MD&A (not re-read for this quarter)"),
    ("cognizant", "2015Q1", "2015Q4", "rev_usd",
     "TriZetto acquisition (Nov 2014): 'TriZetto, which contributed revenue of approximately $169.0 million and was the primary driver of the 42.7% revenue growth in our Healthcare segment' (Q1 2015); gR (cc) not available before 2017 so the correlation is unaffected",
     "Cognizant 10-Q Q1 2015 (filed 2015-05-04), MD&A 'Overview' (local data/sources/cognizant/txt/2015-05-04_10-Q_ctsh2015331-10q.htm.txt)"),
    ("cognizant", "2015Q2", "2015Q2", "headcount", "same TriZetto acquisition (headcount acquired not quantified in the collected text)", "as above"),
    ("cognizant", "2016Q3", "2016Q4", "headcount",
     "organic: filing attributes margin pressure to 'headcount growth outpacing revenue growth'; no acquisition of that size in 2016",
     "Cognizant 10-Q Q3 2016 (filed 2016-11-07), MD&A segment discussion"),
    ("cognizant", "2024Q3", "2025Q2", "rev_usd",
     "Belcan acquisition (Aug 2024): 'revenue from our recently completed acquisition of Belcan contributed approximately 4 percentage points to year-over-year revenue growth' (Q2 2025); gR not adjusted (D12)",
     "Cognizant 8-K Ex.99.2 Q2 2025 (2025-07-30), footnote 1; Q1 2025 Ex.99.2 says Belcan and Thirdera ~4pp"),
    ("hcltech", "2019Q2", "2020Q1", "rev_usd",
     "IBM select-products acquisition ($1.8bn) closed 30 Jun 2019, revenue from Q2FY20 (2019Q3); 2019Q2 growth includes earlier IBM IP-partnership deals and FY19 acquisitions (not quantified in the release)",
     "HCLTech Q1FY20 investor release p3, p7; Q2FY20 release p6 ('Current quarter financials include revenue from the previously announced $1.8 bn acquisition')"),
    ("hcltech", "2019Q2", "2019Q4", "headcount", "same period as IBM products / FY19 acquisitions; acquired headcount not quantified in the releases", "HCLTech Q1FY20, Q2FY20 releases"),
    ("hcltech", "2024Q2", "2025Q1", "headcount",
     "divestiture removed 7,398 employees in Q1FY25; handled by D10 (base adjustment); revenue effect of 'a divestiture in Q2 FY25' is NOT adjusted in gR",
     "HCLTech Q1FY25 investor release p3 ('Reduction in headcount due to divestiture (7,398)'); Q4FY25 release p15 footnote"),
    ("lti", "2017Q4", "2020Q1", "rev_usd/headcount",
     "sustained high organic growth (LTI fact sheets show no acquisition-adjusted figures); not a level break: no QoQ jump >6% in headcount, revenue QoQ +8% in 2017Q4 and 2019Q4 only",
     "data/raw/ltim.csv (LTI fact sheets); no acquisition quantified in collected LTI documents"),
    ("mindtree", "2015Q3", "2016Q2", "rev_usd/headcount",
     "QoQ revenue +14.9% and headcount +7.7% in 2015Q3 (Q2FY16); consistent with the FY16 acquisitions (Bluefin, Relational, Discoverture) but NOT verified: Mindtree FY16 filings are scanned and were not read for this audit; Mindtree has no cc YoY so gR is unaffected",
     "not verified in a primary document (Mindtree Q2FY16 NSE filing is image-only)"),
    ("mindtree", "2018Q2", "2018Q4", "rev_usd/headcount", "QoQ +6.5% revenue / +6.9% headcount in 2018Q2 (Q1FY19); not explained in collected documents", "-"),
    ("wipro", "2018Q3", "2019Q2", "headcount",
     "~9,000 employees transferred with the Alight deal in Q2FY19 (rebadging, not an acquisition): 'There is no inorganic component ... About 9000 employees come for the large deal which we had won from Alight'; lifts Wipro gL by ~5pp for 4 quarters; not adjusted",
     "Wipro Q2FY19 earnings-call transcript p15 (local data/sources/wipro/2018-2019_q2fy19_transcripts-conference-call-q2-fy19.pdf)"),
    ("wipro", "2021Q2", "2022Q1", "rev_usd", "Capco acquisition closed Q1FY22 (IT Services +12.0% QoQ cc in Q1FY22 per wipro_NOTES); gR includes inorganic revenue (D12)", "wipro_NOTES.md §3; Wipro Q1FY22 datasheet"),
    ("techm", "2021Q3", "2022Q2", "headcount",
     "Q2FY22 headcount +14,930 QoQ (BPO +7,390, software +6,923); acquisitions in the quarter's release (Lodestone etc.) but acquired headcount not quantified",
     "TechM Q2FY22 press release p1-2; Q2FY22 fact sheet p2"),
    ("ltim", "2021Q3", "2022Q1", "headcount/rev_usd", "LTIM restated combined series during the 2021-22 boom; mirrors LTI + Mindtree", "LTIM Q3FY23 fact sheet Addendum p15-16"),
]


def explain(f, q, series):
    out = []
    for ff, a, b, s, txt, src in EXPLAIN:
        if ff == f and a <= q <= b and series in s.split("/"):
            out.append((txt, src))
    return out or [("not explained in collected documents", "-")]


rows = []
z = yoy[(yoy.cal_q >= "2015Q2")]
for r in z.itertuples():
    if r.cal_q[:4] in ("2021", "2022"):
        continue
    for m, series in [("gR", "rev_usd"), ("gR_usd", "rev_usd"), ("gL", "headcount")]:
        v = getattr(r, m)
        if pd.notna(v) and abs(v) > 15:
            for txt, src in explain(r.firm, r.cal_q, series):
                rows.append(dict(rule="|YoY|>15 outside 2021-22", firm=r.firm, cal_q=r.cal_q, series=m, value=round(v, 2), explanation=txt, source=src))
for f, g in core.groupby("firm"):
    g = g.set_index("cal_q")
    for q in g.index:
        p = qadd(q, -1)
        if q < "2015Q2" or p not in g.index:
            continue
        for col in ["headcount", "rev_usd"]:
            a, b = g[col].get(p), g[col].get(q)
            if pd.notna(a) and pd.notna(b) and abs(100 * np.log(b / a)) > 6:
                if q in ("2020Q2", "2020Q3") and col == "rev_usd":
                    txt = [("COVID quarter (revenue drop / rebound)", "-")]
                elif q[:4] in ("2021", "2022"):
                    txt = explain(f, q, col) if explain(f, q, col)[0][0] != "not explained in collected documents" else [("2021-22 hiring/revenue boom (no definitional break identified)", "-")]
                else:
                    txt = explain(f, q, col)
                    if f == "accenture" and col == "rev_usd" and txt[0][0] == "not explained in collected documents":
                        txt = explain(f, q, "rev_usd_qoq")
                for t, s in txt:
                    rows.append(dict(rule="QoQ level jump >6%", firm=f, cal_q=q, series=col, value=round(100 * np.log(b / a), 2), explanation=t, source=s))
jumps = pd.DataFrame(rows).sort_values(["firm", "cal_q", "rule"])
jumps.to_csv(AUD / f"structural_breaks_jumps{args.tag}.csv", index=False)

# ------------------------------------------------------------------ LTIM switch
c = core[core.firm.isin(["lti", "mindtree", "ltim"])].pivot(index="cal_q", columns="firm", values="headcount")
r = core[core.firm.isin(["lti", "mindtree", "ltim"])].pivot(index="cal_q", columns="firm", values="rev_usd")
qs = qrange("2021Q2", "2023Q2")
sw = pd.DataFrame(index=qs)
for f in ["lti", "mindtree", "ltim"]:
    y = yoy[yoy.firm == f].set_index("cal_q")
    sw[f"gL_{f}"] = y.gL.reindex(qs)
    sw[f"gR_{f}"] = y.gR.reindex(qs)
    sw[f"heads_{f}"] = c[f].reindex(qs)
    sw[f"revusd_{f}"] = r[f].reindex(qs)
hs = c["lti"] + c["mindtree"]
sw["heads_lti_plus_mt"] = hs.reindex(qs)
sw["ltim_restated_vs_sum_pct"] = 100 * (sw.heads_ltim / sw.heads_lti_plus_mt - 1)
sw["gL_lti_plus_mt"] = [100 * np.log(hs[q] / hs[qadd(q, -4)]) if q in hs and qadd(q, -4) in hs and pd.notna(hs.get(q)) and pd.notna(hs.get(qadd(q, -4))) else np.nan for q in qs]
for s in ["pilot", "dedup", "chain"]:
    ind = indian_panel(yoy, core, s)
    agg = aggregate(ind, how="median")
    mean = aggregate(ind, how="mean")
    cnt = ind.groupby("cal_q")[["gR", "gL"]].count()
    sw[f"ind_median_gL_{s}"] = agg.gL.reindex(qs)
    sw[f"ind_mean_gL_{s}"] = mean.gL.reindex(qs)
    sw[f"n_gL_{s}"] = cnt.gL.reindex(qs)
    sw[f"n_gR_{s}"] = cnt.gR.reindex(qs)
sw.index.name = "cal_q"
sw.round(3).to_csv(AUD / f"ltim_switch_check{args.tag}.csv")

# ------------------------------------------------------------------ HCLTech divestiture
h = core[core.firm == "hcltech"].set_index("cal_q").headcount
qs2 = qrange("2023Q4", "2025Q3")
hd = pd.DataFrame(index=qs2)
hd["headcount"] = h.reindex(qs2)
hd["headcount_lag4"] = [h.get(qadd(q, -4)) for q in qs2]
hd["gL_unadjusted"] = 100 * np.log(hd.headcount / hd.headcount_lag4)
hd["gL_pilot_D10"] = yoy[yoy.firm == "hcltech"].set_index("cal_q").gL.reindex(qs2)
hd["base_adjusted"] = [qadd(q, -4) < "2024Q2" <= q for q in qs2]
hd.index.name = "cal_q"
hd.round(3).to_csv(AUD / f"hcl_divestiture_check{args.tag}.csv")

pd.set_option("display.width", 250)
pd.set_option("display.max_colwidth", 70)
print(jumps[["rule", "firm", "cal_q", "series", "value", "explanation"]].to_string())
print(sw[[c for c in sw.columns if c.startswith(("gL_", "ind_median", "ind_mean", "n_gL", "ltim_restated"))]].round(1).to_string())
print(hd.round(2).to_string())
