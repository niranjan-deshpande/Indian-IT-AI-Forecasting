"""Check every number in the note (docs/index.html) against its source -> note_number_check.md.

    python3 scripts/final/note_number_check.py

Each entry gives the number as printed, where it appears, the source file and row, and a lookup.
CSV-backed numbers are recomputed from the file and compared after rounding to the printed precision.
Numbers that come from text sources (external series, audit reports) are checked by finding the
cited figure verbatim in the cited file. A final pass scans the page's visible text for numeric tokens
that no entry covers, so nothing printed goes unchecked.
"""
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
ppi = pd.read_csv(ROOT / "data/explore/prices/final_bls/ppi_518210_annual.csv").set_index("year")


def fig3(path):
    import csv
    rows = list(csv.reader(open(path)))
    cols = ["half"] + [f"{a}_{b}" if b else a for a, b in zip(rows[0][1:], rows[1][1:])]
    d = pd.DataFrame([r for r in rows[3:] if r and r[0]], columns=cols).set_index("half")
    return d.apply(pd.to_numeric)


f3 = fig3(F / "fig3_data.csv")


def note(item):
    return float(nn.loc[item, "value"])


def firm(period, firm_, col):
    return float(tAf[(tAf.period == period) & (tAf.firm == firm_)][col].iloc[0])


def resid(window, col="mean_firm_years"):
    return float(tB[(tB.window == window) & (tB.metric == "residual")][col].iloc[0])


def text_has(path, needle):
    return needle in (ROOT / path).read_text(encoding="utf-8")


ENTRIES = []  # (printed, where, source, row/key, value_or_None, digits, kind)


def num(printed, where, source, key, value, digits=1, absval=False):
    ENTRIES.append(dict(printed=printed, where=where, source=source, key=key, value=value,
                        digits=digits, absval=absval, kind="csv"))


def txt(printed, where, source, needle):
    ENTRIES.append(dict(printed=printed, where=where, source=source, key=f'text "{needle}"',
                        value=None, needle=needle, kind="text"))


NN = "output/final/note_numbers.csv"
S = "Indian simple average"

# ---- §1 Summary
num("+14%", "§1", NN, f"{S} | headcount | FY23", note(f"{S} | headcount | FY23"), 0)
num("−4%", "§1", NN, f"{S} | headcount | FY24", note(f"{S} | headcount | FY24"), 0)
num("four firms", "§1", "output/final/table_B.csv", "FY24-FY26 residual n_firms", resid("FY24-FY26", "n_firms"), 0)
txt("mid-2024", "§1, §5c", "output/final/fig3_data.csv", "2024H2,75,2,8,10")

# ---- §2 The fact
for lab, item, where in [
    ("7.4%", "headcount | mean FY16-FY20", "§2"), ("18.5%", "headcount | FY22", "§2"),
    ("14.3%", "headcount | FY23", "§2"), ("3.6%", "headcount | FY24", "§2 (fell 3.6%)"),
    ("−0.5%", "headcount | FY25", "§2"), ("+1.2%", "headcount | FY26", "§2"),
    ("8.7%", "rev_cc | mean FY16-FY20", "§2"), ("0.7%", "rev_cc | FY24", "§2"),
    ("2.6%", "rev_cc | FY25", "§2"), ("1.4%", "rev_cc | FY26", "§2")]:
    v = note(f"{S} | {item}")
    num(lab, where, NN, f"{S} | {item}", v, 1, absval=lab[0].isdigit())
txt("11 of 12 months", "Fig. 1 caption; appendix", "output/final/table_A.md", "11 of 12 months overlap")
n_cc = tA[(tA.group == S) & (tA.metric == "rev_cc")].set_index("period").n_firms
num("four (FY16–20)", "Fig. 1 caption: 'four or five firms'", "output/final/table_A.csv", "rev_cc n_firms FY16-FY20 (max)",
    n_cc[[f"FY{y}" for y in range(16, 21)]].max(), 0)
num("five (FY21–23)", "Fig. 1 caption: 'four or five firms'", "output/final/table_A.csv", "rev_cc n_firms FY21-FY23 (max)",
    n_cc[["FY21", "FY22", "FY23"]].max(), 0)
num("five of the six", "§2", NN, "Indian entities with negative headcount growth in FY24",
    note("Indian entities with negative headcount growth in FY24 (count of 6)"), 0)
num("+2.1%", "§2", NN, "hcltech | headcount | FY24", note("hcltech | headcount | FY24"))
num("1.5%", "§2", NN, "Accenture | headcount | FY24", note("Accenture | headcount | FY24"))
num("0.9%", "§2 (Cognizant fell)", NN, "Cognizant | headcount | FY24", note("Cognizant | headcount | FY24"), absval=True)
num("2.5%", "§2 (Cognizant fell)", NN, "Cognizant | headcount | FY25", note("Cognizant | headcount | FY25"), absval=True)
MT = "data/explore/midtier/midtier_vs_top6.csv"
for lab, col in [("Top-six revenue growth (USD)", "top6_rev_growth_logx100"),
                 ("Mid-tier revenue growth (USD)", "mid4_rev_growth_logx100"),
                 ("Top-six headcount growth (year-end)", "top6_hc_growth_logx100"),
                 ("Mid-tier headcount growth (year-end)", "mid4_hc_growth_logx100")]:
    for y in ["FY24", "FY25", "FY26"]:
        v = mid.loc[y, col]
        num(f"{v:+.1f}".replace("-", MINUS), f"Table 1, {lab}, {y}", MT, f"{y} {col}", v)
lv = mida.set_index(["firm", "aligned_fy"]).revenue_usd_mn
ex = [("persistent", "mphasis", "hexaware")]
ex_cof = 100 * math.log(sum(lv[(f, "FY25")] for f in ex[0]) / sum(lv[(f, "FY24")] for f in ex[0]))
num("10.9%", "§2 (ex-Coforge FY25 revenue growth)", "data/explore/midtier/midtier_annual.csv",
    "log change of summed revenue_usd_mn, Persistent+Mphasis+Hexaware, FY24→FY25 (recomputed here)", ex_cof)
num("5.1%", "§2", MT, "FY21 mid4_rev_share_pct", mid.loc["FY21", "mid4_rev_share_pct"])
num("7.3%", "§2", MT, "FY26 mid4_rev_share_pct", mid.loc["FY26", "mid4_rev_share_pct"])
txt("three months later", "Table 1 note", "FINAL_PASS_SUMMARY.md", "Indian fiscal year ending three months later")

# ---- §4 Identity and Table 3
TB = "output/final/table_B.csv"
for w, lab in [("FY16-FY23", "all, FY16–23"), ("FY16-FY23 excl. FY21 (COVID)", "all, excl. FY21"),
               ("FY24-FY26", "all, FY24–26"), ("FY16-FY23, same firms", "same, FY16–23"),
               ("FY16-FY23 excl. FY21, same firms", "same, excl. FY21"), ("FY24-FY26, same firms", "same, FY24–26")]:
    v = resid(w)
    num(f"{v:+.1f}".replace("-", MINUS), f"Table 3, {lab}", TB, f"{w} residual mean_firm_years", v)
    n = resid(w, "n_firm_years")
    num(f"{int(n)}", f"Table 3, {lab} (firm-years)", TB, f"{w} residual n_firm_years", n, 0)
num("+4.2%", "§4", "output/final/table_A_firms.csv", "FY24 tcs rpe_cc", firm("FY24", "tcs", "rpe_cc"))
num("+3.9%", "§4", "output/final/table_A_firms.csv", "FY25 tcs rpe_cc", firm("FY25", "tcs", "rpe_cc"))
tcs_pre = tAf[(tAf.firm == "tcs") & tAf.period.isin([f"FY{y}" for y in range(16, 21)])].rpe_cc.mean()
num("+1.7%", "§4", "output/final/table_A_firms.csv", "mean of tcs rpe_cc FY16-FY20 (recomputed here)", tcs_pre)
num("+6.6", "§4", "output/final/table_A_firms.csv", "FY24 infosys residual", firm("FY24", "infosys", "residual"))

# ---- §5a Subcontracting
FG = "output/final/fig2_data.csv"
num("9.5%", "§5a (TCS FY23)", FG, "FY23 tcs", f2.loc["FY23", "tcs"])
num("6.6%", "§5a (TCS FY24)", FG, "FY24 tcs", f2.loc["FY24", "tcs"])
num("15.0%", "§5a (Tech Mahindra FY23)", FG, "FY23 techm", f2.loc["FY23", "techm"])
num("12.9%", "§5a (Tech Mahindra FY24)", FG, "FY24 techm", f2.loc["FY24", "techm"])
num("all six fell", "§5a; Fig. 2 annotation", NN, "subcontracting: firms whose share fell FY23->FY24",
    note("subcontracting: firms whose share fell FY23->FY24"), 0)
rose = int((f2.loc["FY26"] > f2.loc["FY25"]).sum())
num("five of six rose in FY26", "§5a", FG, "count of firms with FY26 > FY25 (recomputed here)", rose, 0)
num("below FY23 everywhere", "§5a", NN, "subcontracting: firms with FY26 share below FY23",
    note("subcontracting: firms with FY26 share below FY23"), 0)

# ---- §5b
txt("₹6.54 lakh crore", "§5b", "note_inputs.md", "₹6,53,856 cr (2021-22)")
txt("₹8.45 lakh crore", "§5b", "note_inputs.md", "₹8,45,021 cr (2022-23)")
txt("893,000", "§5b", "note_inputs.md", "893.2 (2023, preliminary)")
txt("598,000", "§5b", "note_inputs.md", "598.4 (2019)")
txt("+4% / −4%", "§5b", "note_inputs.md", "IT/Software Services −4%, GCC +4%")
txt("2021–22 boom and bust", "§5b", "audit_report.md", "driven by the single 2021–22 boom-and-bust")

# ---- §5c
num("2,087", "§5c; appendix", "output/final/calls_agreement.csv", "overall n_coder1", agree.loc["overall", "n_coder1"], 0)
txt("183", "§5c", "calls_codebook.md", "2,087 verbatim management statements from 183 transcripts")
num("92%", "§5c", "output/final/calls_agreement.csv", "overall percent_agreement", agree.loc["overall", "percent_agreement"], 0)
num("0.87", "§5c", "output/final/calls_agreement.csv", "overall cohen_kappa", agree.loc["overall", "cohen_kappa"], 2)
FT = "output/final/fig3_data.csv"
num("7.5", "§5c (A 2023 low)", FT, "per_transcript_A min(2023H1, 2023H2)", f3.loc[["2023H1", "2023H2"], "per_transcript_A"].min())
num("7.9", "§5c (A 2023 high)", FT, "per_transcript_A max(2023H1, 2023H2)", f3.loc[["2023H1", "2023H2"], "per_transcript_A"].max())
w = ["2024H2", "2025H1", "2025H2", "2026H1"]
num("4.7", "§5c (A 2024H2–2026H1 low)", FT, "per_transcript_A min 2024H2-2026H1", f3.loc[w, "per_transcript_A"].min())
num("5.7", "§5c (A 2024H2–2026H1 high)", FT, "per_transcript_A max 2024H2-2026H1", f3.loc[w, "per_transcript_A"].max())
pre = ["2021H1", "2021H2", "2022H1", "2022H2", "2023H1", "2023H2", "2024H1"]
num("0", "§5c (D before mid-2024 low)", FT, "per_transcript_D min 2021H1-2024H1", f3.loc[pre, "per_transcript_D"].min())
num("0.3", "§5c (D before mid-2024 high)", FT, "per_transcript_D max 2021H1-2024H1", f3.loc[pre, "per_transcript_D"].max())
num("0.6", "§5c (D 2024H2–2026H1 low)", FT, "per_transcript_D min 2024H2-2026H1", f3.loc[w, "per_transcript_D"].min())
num("1.6", "§5c (D 2024H2–2026H1 high)", FT, "per_transcript_D max 2024H2-2026H1", f3.loc[w, "per_transcript_D"].max())
num("8 transcripts", "Fig. 3 caption", FT, "2026H2 n_transcripts", f3.loc["2026H2", "n_transcripts"], 0)
txt("eight firms (six + Accenture + Cognizant)", "§5c", "calls_codebook.md", "Jan 2021 – Oct 2026, eight firms")
for k, needle in [("$100 … $95 or $90", "And particularly, if there is AI for IT, because of AI if there is a productivity gain, we will try to share those gains with our customers. So, in that sense, that will be what we did with $100 if we are able to do with $95 or $90."),
                  ("$100 million … 80 million; 25%, 30%", "$100 million deal would be much lesser today - maybe 80 million, just on a rough ballpark. So, deal TCV is flat. But technically, it does require at least 25%, 30% more effort to convert and get to the same number."),
                  ("Infosys quote", "We continue to see the overall environment where digital transformation program and discretionary spends are low and decision-making is slow. This is impacting our volumes."),
                  ("Seksaria quote", "Gaurav, I will distinguish realization from pricing. Pricing environment is stable. Realization is an outcome. You can measure it as revenue per FTE and you will notice that it has been improving")]:
    txt(k, "§5c quotes (verbatim)", "note_quotes.md", needle)

# ---- §6
txt("NAICS 5415 not covered", "§6", "price_data.md", "541512 \"Computer Systems Design Services\"")
mo = pd.read_csv(ROOT / "data/explore/prices/final_bls/ppi_518210_monthly.csv")
avg = mo.groupby("year").value.mean()
ja = mo[mo.month <= 8].groupby("year").value.mean()
spark = {y: 100 * (avg[y] / avg[y - 1] - 1) for y in range(2015, 2026)}
spark[2026] = 100 * (ja[2026] / ja[2025] - 1)
PP = "data/explore/prices/final_bls/ppi_518210_monthly.csv"
num("+0.3%", "§6 (PPI 518210 low, 2015–2026)", PP, "min of annual-average % change 2015-2025 and 2026 Jan-Aug YoY", min(spark.values()))
num("+3.2%", "§6 (PPI 518210 high)", PP, "max of the same (2025: 3.245; the 2-dp annual file shows 3.25)", max(spark.values()))
for y, v in spark.items():
    num(f"{v:+.1f}%", f"§6 sparkline tooltip, {y}", PP, f"{y} {'Jan-Aug YoY' if y == 2026 else 'annual-average % change'}", v)
txt("ISG declines accelerated", "§6", "price_data.md", "\"doubled or even tripling in some cases\"")
txt("billed person-months through FY20", "§6; Table 4", "price_data.md", "every year FY2003–FY2020 (20-F)")
txt("−1% to −2% (FY15–17), ~0% (FY18–20)", "§6", "note_inputs.md",
    "about −1% to −2% a year in FY15–FY17 and about 0% in FY18–FY20")
txt("LTI until 2022", "Table 4", "price_data.md", "LTI published billed person-months to Sep 2022")

# ---- §8 and appendix
txt("30-point audit / 30 of 30", "§8; appendix", "audit_report.md", "Spot-check: 30 of 30 values match the primary documents")
for c in "ABCDE":
    r = agree.loc[c]
    num(f"{int(r.n_coder1):,}", f"Appendix table, {c}, coder 1", "output/final/calls_agreement.csv", f"{c} n_coder1", r.n_coder1, 0)
    num(f"{int(r.n_coder2):,}", f"Appendix table, {c}, coder 2", "output/final/calls_agreement.csv", f"{c} n_coder2", r.n_coder2, 0)
    num(f"{r.percent_agreement:.1f}%", f"Appendix table, {c}, matched", "output/final/calls_agreement.csv", f"{c} percent_agreement", r.percent_agreement)
    num(f"{r.cohen_kappa:.2f}", f"Appendix table, {c}, κ", "output/final/calls_agreement.csv", f"{c} cohen_kappa", r.cohen_kappa, 2)
num("92.1%", "Appendix table, all", "output/final/calls_agreement.csv", "overall percent_agreement", agree.loc["overall", "percent_agreement"])
num("2,087 (coder 2)", "Appendix table, all", "output/final/calls_agreement.csv", "overall n_coder2", agree.loc["overall", "n_coder2"], 0)
txt("389", "Appendix", "calls_codebook.md", "Pricing pass (previous round): 389 statements")
txt("1,711", "Appendix", "calls_codebook.md", "Demand pass (this round): 1,711 statements")
txt("13 duplicates", "Appendix", "calls_codebook.md", "389 + 1,711 − 13 cross-pass duplicates = 2,087")
txt("about 2 per call", "Appendix", "calls_codebook.md", "about 2.1 statements per call")
txt("about 9 per call", "Appendix", "calls_codebook.md", "about 9.3 statements per call")
txt("12-family dictionary", "Appendix", "calls_codebook.md", "12 term families")


# ---------------------------------------------------------------- evaluate

def printed_value(s):
    m = re.search(r"[+−-]?\d[\d,]*\.?\d*", s)
    return float(m.group().replace("−", "-").replace(",", "")) if m else None


rows = []
for e in ENTRIES:
    if e["kind"] == "text":
        ok = text_has(e["source"], e["needle"])
        repo = "found verbatim" if ok else "NOT FOUND"
    else:
        v = float(e["value"])
        rv = round(abs(v) if e["absval"] else v, e["digits"])
        p = printed_value(e["printed"])
        if e["printed"].startswith(("all six", "below FY23", "four", "five", "eight")):
            p = {"all six": 6, "below FY23": 6, "four": 4, "five": 5}.get(next(k for k in
                 ["all six", "below FY23", "four", "five"] if e["printed"].startswith(k)), p)
        ok = p is not None and math.isclose(p, rv, abs_tol=1e-9)
        repo = f"{v:.3f}".rstrip("0").rstrip(".") if not float(v).is_integer() else f"{int(v)}"
    rows.append((e["printed"], e["where"], e["source"], e["key"], repo, "yes" if ok else "**NO**"))

# coverage scan of the visible page text
page = PAGE.read_text(encoding="utf-8")
body = page.split("<main>")[1].split("</main>")[0]
body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
body = re.sub(r"<(script|style)\b.*?</\1>", " ", body, flags=re.S)
body = re.sub(r'<a [^>]*href="[^"]*"', "<a", body)
text = unescape(re.sub(r"<[^>]+>", " ", body))
text = re.sub(r"\bFY\d{2}(?:–\d{2})?\b|\b(?:19|20)\d{2}(?:H[12])?\b|’\d{2}\b|\bS[1-4]\b|§\d|\b[Q]\d\b", " ", text)
text = re.sub(r"\b(?:Table|Figure)\s+\d\b|\bNAICS\s+\d+\b|\bPPI\s+\d+\b|\b518210\b|\b5415\b|\b99\.5\b", " ", text)
text = re.sub(r"\bp\.\s*\d+\b|\b20-F\b|\b6-K\b|\bASC 606\b|\b12 Oct\b|\b11 Jan\b|\b10 Apr\b|\b21 Apr\b|×100|x\.x", " ", text)
tokens = re.findall(r"[+−]?\d[\d,]*(?:\.\d+)?%?", text)
covered = set()
for e in ENTRIES:
    for t in re.findall(r"[+−]?\d[\d,]*(?:\.\d+)?%?", e["printed"] + " " + e.get("needle", "") + " " + e["key"]):
        covered.add(t.lstrip("+−").rstrip("%"))
# structural integers that are not data: section numbers, list items, months, scenario counts in words
STRUCT = {"1", "2", "3", "4", "5", "6", "7", "8", "0"}
uncovered = sorted({t for t in tokens if t.lstrip("+−").rstrip("%") not in covered | STRUCT})

bad = [r for r in rows if r[-1] != "yes"]
lines = ["# Number check for the note (`docs/index.html`)", "",
         "*Generated by `scripts/final/note_number_check.py`. CSV numbers are recomputed from the file and compared after "
         "rounding to the printed precision; text-sourced numbers are checked by finding the cited figure verbatim in the cited file. "
         "Growth rates are log change ×100 unless the source says otherwise.*", "",
         f"**Result:** {len(rows)} entries checked, {len(rows) - len(bad)} match, {len(bad)} mismatch. "
         f"Uncovered numeric tokens on the page: {len(uncovered)}.", ""]
if bad:
    lines += ["## Mismatches", "", "| printed | where | source | row | repo value |", "|---|---|---|---|---|"]
    lines += [f"| {r[0]} | {r[1]} | `{r[2]}` | {r[3]} | {r[4]} |" for r in bad] + [""]
lines += ["## Differences from the outline", "",
          "- **Cognizant FY25 headcount growth.** The outline (and `FINAL_PASS_SUMMARY.md`, `note_inputs.md`) say −2.6. "
          "`note_numbers.csv` gives −2.547, which rounds to −2.5. The note prints 2.5.",
          "- **BLS PPI 518210 range.** The outline (and `price_data.md`, `FINAL_PASS_SUMMARY.md`, `note_inputs.md`) say +0.3 to +3.3. "
          "From the monthly index, 2025 growth is 3.245%, so +3.2 at one decimal; +3.3 came from rounding the 2-dp value 3.25 again. "
          "The note prints +3.2. (2024 has the same issue: 1.247, shown as +1.3 in the docs; it is not printed in the prose.)",
          "- **Ex-Coforge FY25 mid-tier revenue growth (+10.9)** is stated in `FINAL_PASS_SUMMARY.md` but is not a row in any CSV; "
          "it is recomputed here from `midtier_annual.csv` levels and matches.",
          "- **TCS FY16–20 revenue-per-employee mean (+1.7)** and **5 of 6 subcontracting rises in FY26** are likewise "
          "recomputed here from `table_A_firms.csv` and `fig2_data.csv`; both match.", ""]
lines += ["## All entries", "", "| printed | where | source | row / key | repo value | match |", "|---|---|---|---|---|---|"]
lines += [f"| {r[0]} | {r[1]} | `{r[2]}` | {r[3]} | {r[4]} | {r[5]} |" for r in rows]
lines += ["", "## Coverage scan", "",
          "Numeric tokens in the page's visible text that no entry above covers (after removing fiscal years, calendar years, "
          "half-years, scenario labels, section/table/figure numbers, industry codes, page numbers and call dates):", "",
          ("none" if not uncovered else ", ".join(f"`{t}`" for t in uncovered)), ""]
OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"{len(rows)} entries, {len(bad)} mismatches, uncovered: {uncovered}")
