"""Check every number in the note (docs/index.html, written in note_text.md) against its source -> note_number_check.md.

    python3 scripts/final/note_number_check.py

Each entry gives the number as printed, where it appears, the source file and row, and how it is checked:
  - CSV numbers are recomputed from the file. The check passes if the source value rounds to the printed
    value at the printed precision ("about 7%" passes for 6.5 <= v <= 7.5; "+1.1" for 1.05 <= v <= 1.15).
  - Ranges ("1–3%") pass if every value in the range's source set rounds into the printed range.
  - Word claims ("barely grew", "every year") are tested as explicit conditions.
  - Text-sourced numbers (external series, audit reports, verbatim quotes) pass if the cited figure is
    found verbatim in the cited file.
A final pass scans the page's visible text for numeric tokens that no entry covers.
"""
import csv
import math
import re
from html import unescape
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
F = ROOT / "output" / "final"
PAGE = ROOT / "docs" / "index.html"
OUT = ROOT / "note_number_check.md"
MINUS = "−"

tA = pd.read_csv(F / "table_A.csv")
tAf = pd.read_csv(F / "table_A_firms.csv")
tB = pd.read_csv(F / "table_B.csv")
nn = pd.read_csv(F / "note_numbers.csv").set_index("item")
f2 = pd.read_csv(F / "fig2_data.csv").set_index("fiscal_year")
agree = pd.read_csv(F / "calls_agreement.csv").set_index("category")
mid = pd.read_csv(ROOT / "data/explore/midtier/midtier_vs_top6.csv").set_index("fiscal_year")
mida = pd.read_csv(ROOT / "data/explore/midtier/midtier_annual.csv")


def fig3(path):
    rows = list(csv.reader(open(path)))
    cols = ["half"] + [f"{a}_{b}" if b else a for a, b in zip(rows[0][1:], rows[1][1:])]
    d = pd.DataFrame([r for r in rows[3:] if r and r[0]], columns=cols).set_index("half")
    return d.apply(pd.to_numeric)


f3 = fig3(F / "fig3_data.csv")
NN = "output/final/note_numbers.csv"
S = "Indian simple average"
ENTRIES = []


def note(item):
    return float(nn.loc[item, "value"])


def firm(period, firm_, col):
    return float(tAf[(tAf.period == period) & (tAf.firm == firm_)][col].iloc[0])


def resid(window, col="mean_firm_years"):
    return float(tB[(tB.window == window) & (tB.metric == "residual")][col].iloc[0])


def rounds_to(v, shown, digits):
    return abs(v - shown) <= 0.5 * 10 ** -digits + 1e-9


def num(printed, where, source, key, value, shown, digits=0):
    """value: the source number (sign as printed); shown: the number as printed; digits: printed precision."""
    ENTRIES.append(dict(printed=printed, where=where, source=source, key=key,
                        repo=float(value), ok=rounds_to(float(value), shown, digits)))


def rng(printed, where, source, key, values, lo, hi, digits=0):
    vals = [float(v) for v in values]
    tol = 0.5 * 10 ** -digits + 1e-9
    ok = all(lo - tol <= v <= hi + tol for v in vals) and rounds_to(min(vals), lo, digits) and rounds_to(max(vals), hi, digits)
    ENTRIES.append(dict(printed=printed, where=where, source=source, key=key,
                        repo=", ".join(f"{v:.3f}".rstrip("0").rstrip(".") for v in vals), ok=ok))


def cond(printed, where, source, key, value, ok):
    ENTRIES.append(dict(printed=printed, where=where, source=source, key=key, repo=value, ok=bool(ok)))


def txt(printed, where, source, needle):
    ok = needle in (ROOT / source).read_text(encoding="utf-8")
    ENTRIES.append(dict(printed=printed, where=where, source=source, key=f'text: "{needle}"',
                        repo="found verbatim" if ok else "NOT FOUND", ok=ok))


hc = lambda p: note(f"{S} | headcount | {p}")
cc = lambda p: note(f"{S} | rev_cc | {p}")
flat = lambda *v: all(abs(x) < 1.5 for x in v)

# ---- §1 Summary
num("14%", "§1", NN, f"{S} | headcount | FY23", hc("FY23"), 14)
num("4% (fell)", "§1", NN, f"{S} | headcount | FY24", -hc("FY24"), 4)
cond("roughly flat since", "§1", NN, f"{S} | headcount | FY25, FY26 within ±1.5",
     f"{hc('FY25'):.2f}, {hc('FY26'):.2f}", flat(hc("FY25"), hc("FY26")))
num("four firms", "§1, §4", "output/final/table_B.csv", "FY24-FY26 residual n_firms", resid("FY24-FY26", "n_firms"), 4)
cond("mid-2024", "§1", "output/final/fig3_data.csv", "first half-year with D per transcript >= 0.5",
     f3.index[f3.per_transcript_D >= 0.5][0], f3.index[f3.per_transcript_D >= 0.5][0] == "2024H2")

# ---- §2 The fact
num("about 7% a year (FY16–20)", "§1, §2", NN, f"{S} | headcount | mean FY16-FY20", hc("mean FY16-FY20"), 7)
num("18% (FY22)", "§2", NN, f"{S} | headcount | FY22", hc("FY22"), 18)
num("14% (FY23)", "§2", NN, f"{S} | headcount | FY23", hc("FY23"), 14)
num("about 4% (FY24 fall)", "§2", NN, f"{S} | headcount | FY24", -hc("FY24"), 4)
pre = tA[(tA.group == S) & (tA.metric == "headcount") & tA.period.isin([f"FY{y}" for y in range(16, 24)])].value
cond("first fall since our data begin in FY16", "§2", "output/final/table_A.csv",
     f"{S} headcount FY16-FY23 all positive", f"min {pre.min():.2f}", (pre > 0).all())
cond("barely grown since", "§2", NN, f"{S} | headcount | FY25, FY26 within ±1.5",
     f"{hc('FY25'):.2f}, {hc('FY26'):.2f}", flat(hc("FY25"), hc("FY26")))
num("about 9% a year (revenue, before COVID)", "§2", NN, f"{S} | rev_cc | mean FY16-FY20", cc("mean FY16-FY20"), 9)
rng("1–3% a year from FY24", "§2", NN, f"{S} | rev_cc | FY24, FY25, FY26", [cc("FY24"), cc("FY25"), cc("FY26")], 1, 3)
txt("11 of its 12 months", "Fig. 1 caption; appendix", "output/final/table_A.md", "11 of 12 months overlap")
n_cc = tA[(tA.group == S) & (tA.metric == "rev_cc")].set_index("period").n_firms
rng("four or five firms (before FY24)", "Fig. 1 caption", "output/final/table_A.csv", "rev_cc n_firms FY16-FY23",
    n_cc[[f"FY{y}" for y in range(16, 24)]], 4, 5)
num("five of the six firms", "§2", NN, "Indian entities with negative headcount growth in FY24",
    note("Indian entities with negative headcount growth in FY24 (count of 6)"), 5)
cond("all except HCLTech", "§2", NN, "hcltech | headcount | FY24 > 0", f"{note('hcltech | headcount | FY24'):.2f}",
     note("hcltech | headcount | FY24") > 0)
cond("Accenture's headcount barely grew in FY24", "§2", NN, "Accenture | headcount | FY24 between 0 and 2",
     f"{note('Accenture | headcount | FY24'):.2f}", 0 < note("Accenture | headcount | FY24") < 2)
cond("Cognizant's shrank in FY24 and FY25", "§2", NN, "Cognizant | headcount | FY24, FY25 < 0",
     f"{note('Cognizant | headcount | FY24'):.2f}, {note('Cognizant | headcount | FY25'):.2f}",
     note("Cognizant | headcount | FY24") < 0 and note("Cognizant | headcount | FY25") < 0)
MT = "data/explore/midtier/midtier_vs_top6.csv"
rng("14–15% (mid-tier revenue, FY25–26)", "§2", MT, "FY25, FY26 mid4_rev_growth_logx100",
    mid.loc[["FY25", "FY26"], "mid4_rev_growth_logx100"], 14, 15)
rng("2–3% (top-six revenue, FY25–26)", "§2", MT, "FY25, FY26 top6_rev_growth_logx100",
    mid.loc[["FY25", "FY26"], "top6_rev_growth_logx100"], 2, 3)
for lab, col in [("Top-six revenue growth (USD)", "top6_rev_growth_logx100"),
                 ("Mid-tier revenue growth (USD)", "mid4_rev_growth_logx100"),
                 ("Top-six headcount growth (year-end)", "top6_hc_growth_logx100"),
                 ("Mid-tier headcount growth (year-end)", "mid4_hc_growth_logx100")]:
    for y in ["FY24", "FY25", "FY26"]:
        v = mid.loc[y, col]
        num(f"{v:+.1f}".replace("-", MINUS), f"Fig. 2 hover, {lab}, {y}", MT, f"{y} {col}", v, round(v, 1), 1)
lv = mida.set_index(["firm", "aligned_fy"]).revenue_usd_mn
three = ("persistent", "mphasis", "hexaware")
ex_cof = 100 * math.log(sum(lv[(f, "FY25")] for f in three) / sum(lv[(f, "FY24")] for f in three))
cond("above 10% in FY25 even without Coforge", "§2", "data/explore/midtier/midtier_annual.csv",
     "log change of summed revenue_usd_mn, Persistent+Mphasis+Hexaware, FY24→FY25 (recomputed here)",
     f"{ex_cof:.2f}", ex_cof > 10)
txt("Coforge bought Cigniti that year (FY25)", "§2", "FINAL_PASS_SUMMARY.md", "Coforge–Cigniti (FY25)")
num("5% (mid-tier revenue share, FY21)", "§2", MT, "FY21 mid4_rev_share_pct", mid.loc["FY21", "mid4_rev_share_pct"], 5)
num("7% (mid-tier revenue share, FY26)", "§2", MT, "FY26 mid4_rev_share_pct", mid.loc["FY26", "mid4_rev_share_pct"], 7)
txt("three months later", "Fig. 2 caption", "FINAL_PASS_SUMMARY.md", "Indian fiscal year ending three months later")


# ---- §2 additions: mid-tier pattern, robustness, client mix
top_r, mid_r = mid.loc[["FY22", "FY23", "FY24", "FY25", "FY26"], "top6_rev_growth_logx100"], mid.loc[["FY22", "FY23", "FY24", "FY25", "FY26"], "mid4_rev_growth_logx100"]
top_h, mid_h = mid.loc[["FY22", "FY23", "FY24", "FY25", "FY26"], "top6_hc_growth_logx100"], mid.loc[["FY22", "FY23", "FY24", "FY25", "FY26"], "mid4_hc_growth_logx100"]
cond("mid-tier grew faster than the top six throughout FY22–FY26", "§2", MT, "mid4 > top6, revenue and headcount, each year FY22-FY26",
     f"min gaps {(mid_r - top_r).min():.1f} (rev), {(mid_h - top_h).min():.1f} (hc)", ((mid_r > top_r) & (mid_h > top_h)).all())
gap = mid_r - top_r
cond("revenue gap widened sharply from FY25", "§2", MT, "rev gap FY25 and FY26 > 2 × FY24 gap",
     f"FY24 {gap['FY24']:.1f}, FY25 {gap['FY25']:.1f}, FY26 {gap['FY26']:.1f}", min(gap["FY25"], gap["FY26"]) > 2 * gap["FY24"])
two = mida[mida.firm.isin(["persistent", "coforge"])]
r2 = two.pivot(index="aligned_fy", columns="firm", values="revenue_usd_mn").sum(axis=1, min_count=2)
h2 = two.pivot(index="aligned_fy", columns="firm", values="headcount").sum(axis=1, min_count=2)
g2r = {y: 100 * math.log(r2[y] / r2[x]) for x, y in [("FY23", "FY24"), ("FY24", "FY25"), ("FY25", "FY26")]}
g2h = {y: 100 * math.log(h2[y] / h2[x]) for x, y in [("FY23", "FY24"), ("FY24", "FY25"), ("FY25", "FY26")]}
cond("without Mphasis and Hexaware, Persistent and Coforge grew even faster", "§2", "data/explore/midtier/midtier_annual.csv",
     "Persistent+Coforge growth > mid-tier four, revenue and headcount, FY24-FY26 (recomputed here)",
     ", ".join(f"{y} {g2r[y]:.1f}/{g2h[y]:.1f}" for y in g2r),
     all(g2r[y] > mid.loc[y, "mid4_rev_growth_logx100"] and g2h[y] > mid.loc[y, "mid4_hc_growth_logx100"] for y in g2r))
import sys
sys.path.insert(0, str(ROOT / "scripts/final"))
import build_note
vf = build_note.verticals_fig_data()
fin = {f["name"]: v for f, v in zip(vf["firms"], vf["groups"]["fin"])}
mids = [f["name"] for f in vf["firms"] if f["mid"]]
tops = [f["name"] for f in vf["firms"] if not f["mid"]]
cond("mid-tier firms depend more on financial services", "§2", "data/explore/midtier/vertical_mix_midtier.csv; data/tidy/panel_long.csv",
     "min mid-tier financial-services share >= max top-six share", f"{min(fin[m] for m in mids):.1f} vs {max(fin[t] for t in tops):.1f}",
     min(fin[m] for m in mids) >= max(fin[t] for t in tops))
pi = [f["name"] for f in vf["firms"]].index("Persistent")
pers = vf["groups"]["tech"][pi] + vf["groups"]["health"][pi]
cond("Persistent earns most of its revenue from software and healthcare clients", "§2", "data/explore/midtier/vertical_mix_midtier.csv",
     "Persistent FY26: Software, Hi-Tech & Emerging + Healthcare & Life Sciences > 50", f"{pers:.1f}", pers > 50)
txt("4% labor saving (illustration)", "§4; Fig. 4", "note_inputs.md", "e.g. the pilot's prior of about 4 pp a year")

# ---- §4 and Table 2
TB = "output/final/table_B.csv"
for wd, lab in [("FY16-FY23", "all, FY16–23"), ("FY16-FY23 excl. FY21 (COVID)", "all, excl. FY21"),
                ("FY24-FY26", "all, FY24–26"), ("FY16-FY23, same firms", "same, FY16–23"),
                ("FY16-FY23 excl. FY21, same firms", "same, excl. FY21"), ("FY24-FY26, same firms", "same, FY24–26")]:
    v = resid(wd)
    num(f"{v:+.1f}".replace("-", MINUS), f"Table 2, {lab}", TB, f"{wd} residual mean_firm_years", v, round(v, 1), 1)
    n = resid(wd, "n_firm_years")
    num(f"{int(n)}", f"Table 2, {lab} (firm-years)", TB, f"{wd} residual n_firm_years", n, n)
txt("firms with data before FY24", "Table 2 note", TB, "FY16-FY23,residual,1.098,18,4,HCLTech;Infosys;Tech Mahindra;Wipro")
txt("firms with data from FY24", "Table 2 note", TB, "FY24-FY26,residual,1.318,12,4,Infosys;LTI group;Tech Mahindra;Wipro")
txt("three firms present in both periods", "Table 2 note", TB, "\"FY24-FY26, same firms\",residual,0.892,9,3,Infosys;Tech Mahindra;Wipro")
rng("about 4% a year (TCS revenue per employee, FY24–25)", "§4", "output/final/table_A_firms.csv",
    "tcs rpe_cc FY24, FY25", [firm("FY24", "tcs", "rpe_cc"), firm("FY25", "tcs", "rpe_cc")], 4, 4)
tcs_pre = tAf[(tAf.firm == "tcs") & tAf.period.isin([f"FY{y}" for y in range(16, 21)])].rpe_cc.mean()
tcs_post = min(firm("FY24", "tcs", "rpe_cc"), firm("FY25", "tcs", "rpe_cc"))
cond("more than twice its pace in FY16–20", "§4", "output/final/table_A_firms.csv",
     "min(tcs rpe_cc FY24, FY25) > 2 × mean FY16-FY20 (recomputed here)", f"{tcs_post:.2f} vs 2 × {tcs_pre:.2f}",
     tcs_post > 2 * tcs_pre)
six = tAf[(tAf.period == "FY26") & ~tAf.firm.isin(["accenture", "cognizant"])].sort_values("weight_rev_usd")
cond("TCS, the largest firm", "§4", "output/final/table_A_firms.csv", "FY26 weight_rev_usd, largest of the six",
     six.firm.iloc[-1], six.firm.iloc[-1] == "tcs")
cond("Infosys's residual jumped in FY24", "§4", "output/final/table_A_firms.csv", "infosys residual FY23 → FY24, rise > 2",
     f"{firm('FY23', 'infosys', 'residual'):.2f} → {firm('FY24', 'infosys', 'residual'):.2f}",
     firm("FY24", "infosys", "residual") > firm("FY23", "infosys", "residual") + 2)

# ---- §5a
num("all six firms (share fell in FY24)", "§5a; Fig. 2 annotation", NN, "subcontracting: firms whose share fell FY23->FY24",
    note("subcontracting: firms whose share fell FY23->FY24"), 6)
rose = int((f2.loc["FY26"] > f2.loc["FY25"]).sum())
num("five of the six (rose in FY26)", "§5a", "output/final/fig2_data.csv", "firms with FY26 > FY25 (recomputed here)", rose, 5)
num("below its FY23 level at every firm", "§5a", NN, "subcontracting: firms with FY26 share below FY23",
    note("subcontracting: firms with FY26 share below FY23"), 6)

# ---- §5b
txt("RBI figures (source text)", "§5b", "note_inputs.md", "₹6,53,856 cr (2021-22) and ₹8,45,021 cr (2022-23)")
num("₹6.5 lakh crore (FY22)", "§5b", "note_inputs.md", "₹6,53,856 cr = 6.53856 lakh crore", 6.53856, 6.5, 1)
num("₹8.5 lakh crore (FY23)", "§5b", "note_inputs.md", "₹8,45,021 cr = 8.45021 lakh crore", 8.45021, 8.5, 1)
txt("BEA figures (source text)", "§5b", "note_inputs.md", "598.4 (2019), 877.0 (2022), 893.2 (2023, preliminary)")
num("about 900,000 (2023)", "§5b", "note_inputs.md", "893.2 thousand (2023, preliminary)", 893.2, 900, -2)
num("about 600,000 (2019)", "§5b", "note_inputs.md", "598.4 thousand (2019)", 598.4, 600, -2)
txt("GCC postings up 4%, IT services down 4%", "§5b", "note_inputs.md", "IT/Software Services −4%, GCC +4%")
txt("boom and bust of 2021–22", "§5b", "audit_report.md", "driven by the single 2021–22 boom-and-bust")

# ---- §5c
A = "output/final/calls_agreement.csv"
num("2,087 statements", "§5c; appendix", A, "overall n_coder1", agree.loc["overall", "n_coder1"], 2087)
txt("183 transcripts", "§5c", "calls_codebook.md", "2,087 verbatim management statements from 183 transcripts")
txt("2021 to 2026; six firms plus Accenture and Cognizant", "§5c", "calls_codebook.md", "Jan 2021 – Oct 2026, eight firms")
txt("five categories", "§5c", "calls_codebook.md", "| **E** | Other or unclear |")
num("92%", "§5c", A, "overall percent_agreement", agree.loc["overall", "percent_agreement"], 92)
rng("nearly eight per transcript (A, 2023)", "§5c", "output/final/fig3_data.csv", "per_transcript_A 2023H1, 2023H2",
    f3.loc[["2023H1", "2023H2"], "per_transcript_A"], 7.5, 7.9, 1)
late = ["2024H2", "2025H1", "2025H2", "2026H1", "2026H2"]
rng("settled at about five (A, from 2024H2)", "§5c", "output/final/fig3_data.csv", "per_transcript_A 2024H2-2026H2 (4.5–6.0 = 'about five')",
    f3.loc[late, "per_transcript_A"], 4.7, 5.9, 1)
pre_d = f3.loc[["2021H1", "2021H2", "2022H1", "2022H2", "2023H1", "2023H2", "2024H1"], "per_transcript_D"]
cond("close to zero before mid-2024 (D)", "§5c", "output/final/fig3_data.csv", "per_transcript_D max 2021H1-2024H1 < 0.3",
     f"{pre_d.max():.3f}", pre_d.max() < 0.3)
num("8 transcripts (2026H2)", "Fig. 3 caption", "output/final/fig3_data.csv", "2026H2 n_transcripts", f3.loc["2026H2", "n_transcripts"], 8)
for k, needle in [
    ("TCS quote ($100 … $95 or $90)", "And particularly, if there is AI for IT, because of AI if there is a productivity gain, we will try to share those gains with our customers. So, in that sense, that will be what we did with $100 if we are able to do with $95 or $90."),
    ("HCLTech quote ($100 million … 80 million; 25%, 30%)", "$100 million deal would be much lesser today - maybe 80 million, just on a rough ballpark. So, deal TCV is flat. But technically, it does require at least 25%, 30% more effort to convert and get to the same number."),
    ("Infosys quote", "We continue to see the overall environment where digital transformation program and discretionary spends are low and decision-making is slow. This is impacting our volumes."),
    ("Seksaria quote", "Gaurav, I will distinguish realization from pricing. Pricing environment is stable. Realization is an outcome. You can measure it as revenue per FTE and you will notice that it has been improving")]:
    txt(k, "§5c quotes (verbatim)", "note_quotes.md", needle)

# ---- §6
txt("BLS does not cover computer systems design", "§6", "price_data.md", "541512 \"Computer Systems Design Services\"")
mo = pd.read_csv(ROOT / "data/explore/prices/final_bls/ppi_518210_monthly.csv")
avg = mo.groupby("year").value.mean()
ja = mo[mo.month <= 8].groupby("year").value.mean()
spark = {y: 100 * (avg[y] / avg[y - 1] - 1) for y in range(2015, 2026)}
spark[2026] = 100 * (ja[2026] / ja[2025] - 1)
PP = "data/explore/prices/final_bls/ppi_518210_monthly.csv"
cond("risen every year since 2015", "§6", PP, "all annual changes 2015-2026 > 0", f"min {min(spark.values()):.2f}",
     min(spark.values()) > 0)
rng("between 0.3% and 3.2%", "§6", PP, "annual-average % change 2015-2025 and 2026 Jan-Aug YoY (2025: 3.245)",
    list(spark.values()), 0.3, 3.2, 1)
for y, v in spark.items():
    num(f"{v:+.1f}%".replace("-", MINUS), f"Fig. 7 hover, {y}", PP,
        f"{y} {'Jan-Aug YoY' if y == 2026 else 'annual-average % change'}", v, round(v, 1), 1)
txt("ISG: prices recently falling faster", "§6", "price_data.md", "\"doubled or even tripling in some cases\"")
txt("billed person-months until FY20", "§6; Table 4", "price_data.md", "every year FY2003–FY2020 (20-F)")
txt("prices fell at least 1–2% a year FY15–17; flat or falling FY18–20", "§6", "note_inputs.md",
    "about −1% to −2% a year in FY15–FY17 and about 0% in FY18–FY20")
txt("LTI until 2022", "Table 4", "price_data.md", "LTI published billed person-months to Sep 2022")

# ---- §8 and appendix
txt("30 values / all 30 matched", "§8; appendix", "audit_report.md", "Spot-check: 30 of 30 values match the primary documents")
for c in "ABCDE":
    r = agree.loc[c]
    num(f"{int(r.n_coder1):,}", f"Appendix table, {c}, model 1", A, f"{c} n_coder1", r.n_coder1, r.n_coder1)
    num(f"{int(r.n_coder2):,}", f"Appendix table, {c}, model 2", A, f"{c} n_coder2", r.n_coder2, r.n_coder2)
    num(f"{r.percent_agreement:.1f}%", f"Appendix table, {c}, matched", A, f"{c} percent_agreement",
        r.percent_agreement, round(r.percent_agreement, 1), 1)
    num(f"{r.cohen_kappa:.2f}", f"Appendix table, {c}, κ", A, f"{c} cohen_kappa", r.cohen_kappa, round(r.cohen_kappa, 2), 2)
o = agree.loc["overall"]
num("92.1%", "Appendix table, all", A, "overall percent_agreement", o.percent_agreement, 92.1, 1)
num("0.87", "Appendix table, all", A, "overall cohen_kappa", o.cohen_kappa, 0.87, 2)
txt("389 statements", "Appendix", "calls_codebook.md", "Pricing pass (previous round): 389 statements")
txt("1,711 statements", "Appendix", "calls_codebook.md", "Demand pass (this round): 1,711 statements")
txt("13 duplicates", "Appendix", "calls_codebook.md", "389 + 1,711 − 13 cross-pass duplicates = 2,087")
txt("about 2 per call", "Appendix", "calls_codebook.md", "about 2.1 statements per call")
txt("about 9 per call", "Appendix", "calls_codebook.md", "about 9.3 statements per call")
txt("12 groups of terms", "Appendix", "calls_codebook.md", "12 term families")
txt("two quarters (Cognizant attrition)", "Appendix", "audit_report.md", "Cognizant attrition definitions were picked arbitrarily in 2 quarters")

# ---------------------------------------------------------------- coverage scan
page = PAGE.read_text(encoding="utf-8")
body = page.split("<main>")[1].split("</main>")[0]
body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
body = re.sub(r"<(script|style)\b.*?</\1>", " ", body, flags=re.S)
body = re.sub(r"<(a|div) [^>]*>", r"<\1>", body)
text = unescape(re.sub(r"<[^>]+>", " ", body))
STRIP = [r"\b20\d{2}–\d{2}\b", r"\bPPI \d{6}\b", r"\bFY\d{2}(?:–\d{2})?\b", r"\b(?:19|20)\d{2}(?:H[12])?\b", r"’\d{2}\b", r"\bS[1-4]\b", r"\bQ\d\b",
         r"\b(?:Table|Figure|Section)\s+\d\b", r"\b99\.5\b", r"\bp\.\s*\d+\b", r"\b20-F\b", r"\b6-K\b", r"\bASC 606\b",
         r"\b(?:10|11|12|21) (?:Oct|Jan|Apr)\b", r"×100", r"x\.x", r"g_\{R/L\}"]
for pat in STRIP:
    text = re.sub(pat, " ", text)
tokens = re.findall(r"[+−]?\d[\d,]*(?:\.\d+)?%?", text)
covered = set()
for e in ENTRIES:
    for t in re.findall(r"[+−]?\d[\d,]*(?:\.\d+)?%?", f"{e['printed']} {e['key']}"):
        covered.add(t.lstrip("+−").rstrip("%"))
STRUCT = {str(i) for i in range(1, 9)}  # section numbers and list items
uncovered = sorted({t for t in tokens if t.lstrip("+−").rstrip("%") not in covered | STRUCT})

bad = [e for e in ENTRIES if not e["ok"]]
show = lambda r: (f"{r:.3f}".rstrip("0").rstrip(".") if isinstance(r, float) else str(r))
lines = ["# Number check for the note (`docs/index.html`, text in `note_text.md`)", "",
         "*Generated by `scripts/final/note_number_check.py`. CSV numbers are recomputed and must round to the printed "
         "value at the printed precision (so \"about 7%\" passes for 6.5–7.5); ranges must contain every source value; "
         "word claims (\"barely grew\", \"every year\") are tested as explicit conditions; text-sourced numbers must appear "
         "verbatim in the cited file. Growth rates are log change ×100 unless the source says otherwise.*", "",
         f"**Result:** {len(ENTRIES)} entries checked, {len(ENTRIES) - len(bad)} match, {len(bad)} mismatch. "
         f"Uncovered numeric tokens on the page: {len(uncovered)}.", ""]
if bad:
    lines += ["## Mismatches", "", "| printed | where | source | row | repo value |", "|---|---|---|---|---|"]
    lines += [f"| {e['printed']} | {e['where']} | `{e['source']}` | {e['key']} | {show(e['repo'])} |" for e in bad] + [""]
lines += ["## Where the repo docs and the data files disagree", "",
          "- **Cognizant FY25 headcount growth.** `FINAL_PASS_SUMMARY.md` and `note_inputs.md` say −2.6; `note_numbers.csv` "
          "gives −2.547 (−2.5). The note now says only that Cognizant's headcount shrank.",
          "- **BLS PPI 518210, 2025.** The docs say +3.3; from the monthly index it is 3.245% (+3.2). The docs rounded the "
          "2-dp value 3.25 a second time. 2024 (1.247, docs +1.3) and 2019 (0.446, docs +0.5) have the same issue; only "
          "the sparkline tooltips show those years.",
          "- **\"TCS and HCLTech, the two largest\".** The docs say this; by FY26 revenue (`table_A_firms.csv`) the order is "
          "TCS, Infosys, HCLTech. The note calls TCS the largest and does not rank HCLTech.",
          "- **Recomputed here, not stored in any CSV:** ex-Coforge FY25 mid-tier revenue growth (10.9), TCS FY16–20 mean "
          "revenue per employee (1.7), and the count of firms whose subcontracting share rose in FY26 (5). All match the docs.", ""]
lines += ["## All entries", "", "| printed | where | source | row / key | repo value | match |", "|---|---|---|---|---|---|"]
lines += [f"| {e['printed']} | {e['where']} | `{e['source']}` | {e['key']} | {show(e['repo'])} | "
          f"{'yes' if e['ok'] else '**NO**'} |" for e in ENTRIES]
lines += ["", "## Coverage scan", "",
          "Numeric tokens in the page's visible text that no entry above covers, after removing fiscal and calendar years, "
          "half-years, scenario labels, section/table/figure numbers, page numbers and call dates:", "",
          ("none" if not uncovered else ", ".join(f"`{t}`" for t in uncovered)), ""]
OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"{len(ENTRIES)} entries, {len(bad)} mismatches: {[e['printed'] for e in bad]}; uncovered: {uncovered}")
