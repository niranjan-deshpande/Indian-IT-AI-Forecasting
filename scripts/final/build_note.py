"""Build the research note as one self-contained HTML page (docs/index.html) for GitHub Pages.

    python3 scripts/final/build_note.py

Chart data and the generated tables are read from the repo CSVs (nothing hand-typed):
  Figure 1          output/final/table_A.csv                (rev_cc, headcount, rpe_cc; FY16-FY26)
  Figure 2          output/final/fig2_data.csv
  Figure 3          output/final/fig3_data.csv, fig3_data_coder2.csv
  Table 1 (mid-tier) data/explore/midtier/midtier_vs_top6.csv
  Table 3 (residual) output/final/table_B.csv
  Appendix table    output/final/calls_agreement.csv
  BLS sparkline     data/explore/prices/final_bls/ppi_518210_monthly.csv
Numbers in the prose are typed; they are checked by scripts/final/note_number_check.py (-> note_number_check.md).
External resources load only from CDNs: Plotly, KaTeX (cdnjs) and Google Fonts.
"""
import csv
import html
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
FINAL = ROOT / "output" / "final"
OUT = ROOT / "docs" / "index.html"
REPO_URL = "https://github.com/niranjan-deshpande/Indian-IT-AI-Forecasting"

YEARS = list(range(2016, 2027))  # FY16..FY26
FY = [f"FY{y % 100:02d}" for y in YEARS]
MINUS = "−"


def fmt(v, nd=1, sign=True):
    """+1.1 / −3.6 with a typographic minus; '–' for missing."""
    if v is None or pd.isna(v):
        return "–"
    s = f"{v:+.{nd}f}" if sign else f"{v:.{nd}f}"
    return s.replace("-", MINUS)


def clean(v, nd=3):
    return None if pd.isna(v) else round(float(v), nd)


# ---------------------------------------------------------------- figure data

def fig1_data():
    t = pd.read_csv(FINAL / "table_A.csv")
    groups = {"rw": "Indian revenue-weighted average", "simple": "Indian simple average",
              "acn": "Accenture", "cog": "Cognizant"}
    out = {}
    for metric in ["rev_cc", "headcount", "rpe_cc"]:
        out[metric] = {}
        for key, g in groups.items():
            s = t[(t.metric == metric) & (t.group == g)].set_index("period").reindex(FY)
            out[metric][key] = {"y": [clean(v) for v in s.value],
                                "text": [fmt(v) for v in s.value],
                                "n": [None if pd.isna(v) else int(v) for v in s.n_firms]}
    return out


def fig2_data():
    d = pd.read_csv(FINAL / "fig2_data.csv")
    firms = [("tcs", "TCS"), ("infosys", "Infosys"), ("hcltech", "HCLTech"), ("wipro", "Wipro"),
             ("techm", "Tech Mahindra"), ("ltim", "LTIMindtree")]
    x = [2000 + int(s[2:]) for s in d.fiscal_year]
    return {"x": x, "labels": list(d.fiscal_year),
            "firms": [{"key": k, "name": n, "y": [clean(v, 2) for v in d[k]],
                       "text": [("–" if pd.isna(v) else f"{v:.2f}%") for v in d[k]]} for k, n in firms]}


def read_fig3(path):
    rows = list(csv.reader(open(path)))
    top, cat = rows[0], rows[1]
    cols = ["half_year"] + [f"{a}_{b}" if b else a for a, b in zip(top[1:], cat[1:])]
    body = [r for r in rows[3:] if r and r[0]]
    df = pd.DataFrame(body, columns=cols)
    out = {"half": list(df.half_year), "n": [int(v) for v in df.n_transcripts]}
    for c in "AD":
        out[c] = {"per": [round(float(v), 3) for v in df[f"per_transcript_{c}"]],
                  "count": [int(v) for v in df[f"statements_{c}"]]}
    return out


def fig3_data():
    return {"c1": read_fig3(FINAL / "fig3_data.csv"), "c2": read_fig3(FINAL / "fig3_data_coder2.csv")}


# ---------------------------------------------------------------- generated tables

def midtier_table():
    m = pd.read_csv(ROOT / "data/explore/midtier/midtier_vs_top6.csv").set_index("fiscal_year")
    yrs = ["FY24", "FY25", "FY26"]
    rows = [("top", "Top-six revenue growth (USD)", "top6_rev_growth_logx100"),
            ("mid", "Mid-tier revenue growth (USD)", "mid4_rev_growth_logx100"),
            ("top", "Top-six headcount growth (year-end)", "top6_hc_growth_logx100"),
            ("mid", "Mid-tier headcount growth (year-end)", "mid4_hc_growth_logx100")]
    head = "".join(f"<th>{y}</th>" for y in yrs)
    body = ""
    for cls, label, col in rows:
        cells = "".join(f"<td>{fmt(m.loc[y, col])}</td>" for y in yrs)
        sep = ' class="grp"' if label.startswith("Top-six headcount") else ""
        body += f'<tr{sep}><th scope="row"><span class="dot {cls}"></span>{label}</th>{cells}</tr>'
    return f"<table><thead><tr><th></th>{head}</tr></thead><tbody>{body}</tbody></table>"


def residual_table():
    b = pd.read_csv(FINAL / "table_B.csv")
    b = b[b.metric == "residual"].set_index("window")
    sets = [("All firms with data", ["FY16-FY23", "FY16-FY23 excl. FY21 (COVID)", "FY24-FY26"]),
            ("Same firms in both windows", ["FY16-FY23, same firms", "FY16-FY23 excl. FY21, same firms",
                                            "FY24-FY26, same firms"])]
    body = ""
    for label, wins in sets:
        cells = "".join(f'<td>{fmt(b.loc[w, "mean_firm_years"])}<span class="fy">'
                        f'{int(b.loc[w, "n_firm_years"])}</span></td>' for w in wins)
        body += f'<tr><th scope="row">{label}</th>{cells}</tr>'
    same = b.loc["FY24-FY26, same firms", "firms"].replace(";", ", ")
    after = b.loc["FY24-FY26", "firms"].replace(";", ", ")
    before = b.loc["FY16-FY23", "firms"].replace(";", ", ")
    return (f"<table><thead><tr><th>Firm set</th><th>FY16–23</th><th>FY16–23<br>excl. FY21</th>"
            f"<th>FY24–26</th></tr></thead><tbody>{body}</tbody></table>",
            before, after, same)


def agreement_table():
    a = pd.read_csv(FINAL / "calls_agreement.csv").set_index("category")
    names = {"A": "Demand weakness", "B": "Pricing stable", "C": "Pricing pressure, no AI link",
             "D": "AI savings passed to clients", "E": "Other or unclear"}
    body = ""
    for c in "ABCDE":
        r = a.loc[c]
        body += (f'<tr><th scope="row">{c} · {names[c]}</th><td>{int(r.n_coder1):,}</td><td>{int(r.n_coder2):,}</td>'
                 f"<td>{r.percent_agreement:.1f}%</td><td>{r.cohen_kappa:.2f}</td></tr>")
    o = a.loc["overall"]
    body += (f'<tr class="tot"><th scope="row">All statements</th><td>{int(o.n_coder1):,}</td><td>{int(o.n_coder2):,}</td>'
             f"<td>{o.percent_agreement:.1f}%</td><td>{o.cohen_kappa:.2f}</td></tr>")
    return ("<table><thead><tr><th>Category</th><th>Coder 1</th><th>Coder 2</th>"
            "<th>Coder 1 codes matched</th><th>κ</th></tr></thead>"
            f"<tbody>{body}</tbody></table>")


def bls_sparkline():
    # from the monthly index, not the 2-dp annual file, to avoid double rounding (2025 is 3.245, not 3.25)
    m = pd.read_csv(ROOT / "data/explore/prices/final_bls/ppi_518210_monthly.csv")
    avg = m.groupby("year").value.mean()
    ja = m[m.month <= 8].groupby("year").value.mean()
    vals = [(y, 100 * (avg[y] / avg[y - 1] - 1)) for y in range(2015, 2026)] + [(2026, 100 * (ja[2026] / ja[2025] - 1))]
    w, h, gap = 9, 30, 3
    top = max(v for _, v in vals)
    bars = ""
    for i, (yr, v) in enumerate(vals):
        bh = max(1.5, v / top * h)
        partial = yr == 2026
        label = f"{yr}{' (Jan–Aug, year on year)' if partial else ''}: {fmt(v)}%"
        bars += (f'<rect x="{i * (w + gap)}" y="{h - bh:.1f}" width="{w}" height="{bh:.1f}" rx="1.5"'
                 f'{" class=\"partial\"" if partial else ""}><title>{label}</title></rect>')
    width = len(vals) * (w + gap) - gap
    return (f'<span class="spark" role="img" aria-label="BLS PPI 518210, annual growth 2015–2026">'
            f'<span class="sp-l">{vals[0][0]}</span><svg viewBox="0 0 {width} {h}" width="{width}" height="{h}">'
            f"{bars}</svg><span class=\"sp-l\">{vals[-1][0]}</span></span>")


# ---------------------------------------------------------------- page

QUOTES = {
    "infosys": dict(
        text="We continue to see the overall environment where digital transformation program and discretionary "
             "spends are low and decision-making is slow. This is impacting our volumes.",
        firm="Infosys", call="Q2 FY24 call", date="12 Oct 2023", who="Salil Parekh, CEO &amp; MD",
        url="https://www.sec.gov/Archives/edgar/data/1067491/000106749123000057/exv99w05.htm",
        src="SEC 6-K, Ex. 99.5"),
    "seksaria": dict(
        text="Gaurav, I will distinguish realization from pricing. Pricing environment is stable. Realization is "
             "an outcome. You can measure it as revenue per FTE and you will notice that it has been improving",
        firm="TCS", call="Q3 FY24 call", date="11 Jan 2024", who="Samir Seksaria, CFO",
        url="https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2023-24/q3/Management%20Commentary/Transcript%20of%20the%20Q3%202023-24%20Earnings%20Conference%20Call%20held%20on%20January%2011,%202023.pdf#page=17",
        src="transcript, p. 17"),
    "krithivasan": dict(
        text="AI for IT, I won’t try to call it deflation. … And particularly, if there is AI for IT, because of AI "
             "if there is a productivity gain, we will try to share those gains with our customers. So, in that "
             "sense, that will be what we did with $100 if we are able to do with $95 or $90.",
        firm="TCS", call="Q4 FY25 call", date="10 Apr 2025", who="K Krithivasan, CEO &amp; MD",
        url="https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2024-25/q4/Management%20Commentary/Transcript%20of%20the%20Q4%202024-25%20Earnings%20Conference%20Call%20held%20at%201900%20hrs%20IST%20on%20Apr%2010,%202025.pdf#page=17",
        src="transcript, p. 17"),
    "vijayakumar": dict(
        text="$100 million deal would be much lesser today - maybe 80 million, just on a rough ballpark. So, deal "
             "TCV is flat. But technically, it does require at least 25%, 30% more effort to convert and get to "
             "the same number.",
        firm="HCLTech", call="Q4 FY26 call", date="21 Apr 2026", who="C. Vijayakumar, CEO &amp; MD",
        url="https://www.hcltech.com/sites/default/files/documents/investor-reports/hcltech-earnings-q4-fy26-transcript.pdf#page=21",
        src="transcript, p. 21"),
}


def quote(key):
    q = QUOTES[key]
    return (f"<blockquote><p>“{html.escape(q['text'], quote=False)}”</p>"
            f"<footer>{q['firm']} · {q['call']} · {q['date']} · {q['who']} · "
            f"<a href=\"{q['url']}\">{q['src']}</a></footer></blockquote>")


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Is AI hitting Indian IT services?</title>
<meta name="description" content="Pilot note: what public data can and can't tell us about AI and the headcount slowdown at India's largest IT services firms.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css">
<style>
:root {
  color-scheme: light;
  --bg: #fbf8f3; --panel: #fffdf9; --ink: #2a2318; --ink-2: #5e5245; --ink-3: #8a7d6d;
  --rule: #e6ddd0; --rule-2: #cfc4b4;
  --accent: #235fa6; --mid: #2f8a57; --acn: #7a7268; --cog: #aaa196;
  --cat-a: #b0702a; --cat-d: #6b4a92;
  --serif: "Source Serif 4", Georgia, "Times New Roman", serif;
  --sans: "Source Sans 3", -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
}
*, *::before, *::after { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; background: var(--bg); color: var(--ink); font-family: var(--serif);
  font-size: 17.5px; line-height: 1.6; font-optical-sizing: auto; }
main { display: grid; grid-template-columns: 1fr min(700px, calc(100% - 32px)) 1fr; padding: 56px 0 72px; }
main > * { grid-column: 2; min-width: 0; }
main > .wide { grid-column: 1 / -1; width: min(960px, calc(100% - 32px)); justify-self: center; }
p { margin: 0 0 1.05em; }
a { color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 2px; }
h1 { font-size: 2.05rem; line-height: 1.2; font-weight: 600; letter-spacing: -0.015em; margin: 0 0 14px; }
h2 { font-size: 1.32rem; line-height: 1.3; font-weight: 600; margin: 2.6em 0 0.7em; letter-spacing: -0.01em; }
h2 .num { color: var(--ink-3); font-weight: 400; margin-right: 0.35em; }
h3 { font-size: 1.05rem; font-weight: 600; margin: 1.9em 0 0.5em; }
.byline { font-family: var(--sans); font-size: 15px; color: var(--ink-2); margin: 0 0 6px; }
.byline .tag { display: inline-block; border: 1px solid var(--rule-2); border-radius: 3px; padding: 0 6px;
  font-size: 12.5px; letter-spacing: 0.04em; text-transform: uppercase; margin-left: 4px; }
.thanks { font-family: var(--sans); font-size: 14px; color: var(--ink-2); margin: 0; }
header { padding-bottom: 22px; border-bottom: 1px solid var(--rule); margin-bottom: 8px; }
ul.scen { list-style: none; padding: 0; margin: 0 0 1.05em; }
ul.scen li { padding-left: 2.6em; text-indent: -2.6em; margin-bottom: 0.3em; }
ul.scen b { display: inline-block; width: 2.6em; text-indent: 0; font-family: var(--sans); font-weight: 600; }
ol.lim { padding-left: 1.4em; } ol.lim li { margin-bottom: 0.35em; padding-left: 0.2em; }

/* figures */
figure { margin: 2em 0 2.2em; }
.fig-panel { background: var(--panel); border: 1px solid var(--rule); border-radius: 6px; padding: 16px 16px 8px; }
.fig-top { display: flex; flex-wrap: wrap; gap: 10px 22px; align-items: center; justify-content: space-between; margin-bottom: 4px; }
.fig-title { font-family: var(--sans); font-weight: 600; font-size: 15px; color: var(--ink); }
.legend { display: flex; flex-wrap: wrap; gap: 4px 16px; font-family: var(--sans); font-size: 13.5px; color: var(--ink); }
.legend i { display: inline-block; width: 20px; height: 0; border-top: 2.5px solid; vertical-align: middle; margin-right: 6px; }
.toggle { display: inline-flex; border: 1px solid var(--rule-2); border-radius: 5px; overflow: hidden; }
.toggle button { font-family: var(--sans); font-size: 13.5px; border: 0; background: transparent; color: var(--ink-2);
  padding: 4px 11px; cursor: pointer; }
.toggle button + button { border-left: 1px solid var(--rule-2); }
.toggle button[aria-pressed="true"] { background: var(--accent); color: #fff; }
.toggle button:focus-visible { outline: 2px solid var(--accent); outline-offset: -2px; }
.toggle-label { font-family: var(--sans); font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em;
  color: var(--ink-2); margin-right: 8px; }
.chart { width: 100%; }
figcaption { font-family: var(--sans); font-size: 14px; line-height: 1.5; color: var(--ink-2); margin: 10px 2px 0; max-width: 720px; }
figcaption b { color: var(--ink); font-weight: 600; }

/* tables */
.table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 1.6em 0 1.9em; }
.table-cap { font-family: var(--sans); font-size: 14px; color: var(--ink-2); margin: 0 0 8px; }
.table-cap b { color: var(--ink); font-weight: 600; }
table { border-collapse: collapse; font-family: var(--sans); font-size: 15px; line-height: 1.4;
  font-variant-numeric: tabular-nums lining-nums; width: 100%; }
th, td { padding: 7px 12px; border-bottom: 1px solid var(--rule); text-align: right; vertical-align: top; }
th:first-child, td:first-child { padding-left: 0; text-align: left; }
th:last-child, td:last-child { padding-right: 0; }
thead th { font-weight: 600; color: var(--ink-2); border-bottom: 1px solid var(--ink-3); vertical-align: bottom; }
tbody th { font-weight: 400; }
tr.grp > * { border-top: 1px solid var(--rule-2); }
tr.tot > * { font-weight: 600; }
.table-note { font-family: var(--sans); font-size: 13px; color: var(--ink-2); margin: 8px 0 0; }
.dot { display: inline-block; width: 9px; height: 9px; border-radius: 50%; margin-right: 8px; vertical-align: 1px; }
.dot.top { background: var(--accent); } .dot.mid { background: var(--mid); }
.fy { display: inline-block; min-width: 2.2em; margin-left: 6px; font-size: 12px; color: var(--ink-3); text-align: right; }
table.pred td, table.pred th { text-align: center; }
table.pred th:first-child, table.pred td:first-child { text-align: left; }
.arr { font-size: 1.15em; font-weight: 600; line-height: 1; }
.arr.dn { color: var(--ink); } .arr.up { color: var(--ink); }
.dim { color: var(--ink-3); }
.nw { white-space: nowrap; }
table.pred tbody th { white-space: nowrap; }
table.items td, table.items th { text-align: left; }

/* math, quotes, sparkline */
.math { margin: 1.4em 0; text-align: center; font-size: 1.12em; overflow-x: auto; }
.math-fallback i { font-family: var(--serif); }
blockquote { margin: 1.5em 0; padding: 2px 0 2px 20px; border-left: 2px solid var(--accent); }
blockquote p { margin: 0 0 6px; font-size: 1.0rem; }
blockquote footer { font-family: var(--sans); font-size: 13.5px; color: var(--ink-2); line-height: 1.45; }
.spark { display: inline-flex; align-items: flex-end; gap: 5px; vertical-align: -4px; margin: 0 2px; }
.spark svg { display: block; } .spark rect { fill: var(--ink-3); } .spark rect.partial { fill: var(--rule-2); }
.sp-l { font-family: var(--sans); font-size: 11.5px; color: var(--ink-3); line-height: 1; }

/* appendix */
.appendix { margin-top: 3.2em; padding-top: 0.4em; border-top: 1px solid var(--rule); font-size: 15.5px; color: #3d3427; }
.appendix h2 { margin-top: 1.2em; font-size: 1.15rem; }
.appendix table { font-size: 14px; }
details { border-bottom: 1px solid var(--rule); padding: 10px 0; }
details > summary { cursor: pointer; font-family: var(--sans); font-weight: 600; font-size: 15px; color: var(--ink); list-style: none; }
details > summary::-webkit-details-marker { display: none; }
details > summary::before { content: "+"; display: inline-block; width: 1.2em; color: var(--ink-3); }
details[open] > summary::before { content: "−"; }
details > div { padding: 8px 0 4px 1.2em; }
details ul { padding-left: 1.1em; margin: 0 0 0.8em; } details li { margin-bottom: 0.3em; }
.footer { font-family: var(--sans); font-size: 13px; color: var(--ink-3); margin-top: 2.5em; }

@media (max-width: 600px) {
  body { font-size: 17px; }
  main { padding-top: 32px; }
  h1 { font-size: 1.65rem; }
  .fig-panel { padding: 12px 10px 6px; }
  table { font-size: 14px; }
  th, td { padding: 6px 8px; }
}
@media print {
  @page { margin: 16mm 14mm; }
  body { background: #fff; font-size: 10.5pt; line-height: 1.45; }
  main { display: block; padding: 0; }
  main > .wide { width: 100%; }
  .toggle-wrap { display: none !important; }
  .fig-panel { border: 0; padding: 0; background: #fff; }
  figure, .table-wrap, blockquote { break-inside: avoid; }
  h2, h3 { break-after: avoid; }
  a { color: inherit; text-decoration: none; }
  .table-wrap { overflow: visible; }
  details > summary::before { content: ""; width: 0; }
}
</style>
</head>
<body>
<main>

<header>
  <h1>Is AI hitting Indian IT services? What public data can and can’t tell us</h1>
  <p class="byline">Niranjan Deshpande · October 2026 · <span class="tag">Pilot note</span></p>
  <p class="thanks">Written as part of SPAR (Fall 2026). Thanks to Andrei Potlogea for supervision. Data and code: %%REPO%%.</p>
</header>

<h2 id="summary"><span class="num">1</span>Summary</h2>

<p>Headcount at the six largest Indian IT services firms went from +14% growth in FY23 to −4% in FY24, and has been roughly flat since. Smaller Indian rivals kept growing. Is AI the cause, or weaker client demand, or work moving elsewhere? Public data cannot separate weaker demand from AI savings passed on to clients as lower prices, because no one measures output prices for these firms. The data do show three things. At the four firms where it can be tested, there is no sign that firms kept AI savings for themselves. There is no evidence of a shift to contractors. And from mid-2024, management began to say it was passing AI savings to clients, while it kept citing weak demand. An output price index for IT services, plus two firm disclosures, would settle the question.</p>

<h2 id="fact"><span class="num">2</span>The fact</h2>

<p>The six firms are TCS, Infosys, HCLTech, Wipro, Tech Mahindra and the LTI group (LTI and Mindtree, merged as LTIMindtree). Growth rates are log changes ×100, which are close to percent changes, over Indian fiscal years (April–March).</p>

<p>On a simple average across the six, headcount grew 7.4% a year in FY16–20. It grew 18.5% in FY22 and 14.3% in FY23, then fell 3.6% in FY24. It changed by −0.5% in FY25 and +1.2% in FY26. Revenue in constant currency grew 8.7% a year in FY16–20, and only 0.7%, 2.6% and 1.4% in FY24, FY25 and FY26.</p>

<figure class="wide" id="fig1">
  <div class="fig-panel">
    <div class="fig-top">
      <div class="legend" aria-hidden="true">
        <span><i style="border-color:var(--accent);border-top-width:3px"></i>Top six (average)</span>
        <span><i style="border-color:var(--acn);border-top-style:dashed"></i>Accenture</span>
        <span><i style="border-color:var(--cog);border-top-style:dotted;border-top-width:3px"></i>Cognizant</span>
      </div>
      <div class="toggle-wrap"><span class="toggle-label">Average</span><span class="toggle" role="group" aria-label="Top-six average">
        <button type="button" data-avg="rw" aria-pressed="true">Revenue-weighted</button><button type="button" data-avg="simple" aria-pressed="false">Simple</button>
      </span></div>
    </div>
    <div id="chart1" class="chart" role="img" aria-label="Three panels: revenue growth, headcount growth and revenue-per-employee growth for the top-six average, Accenture and Cognizant, FY16 to FY26."></div>
  </div>
  <figcaption><b>Figure 1.</b> Top-six average against Accenture and Cognizant, FY16–FY26. Annual growth, log change ×100; revenue and revenue per employee in constant currency. The shaded band is FY24. Accenture and Cognizant are aggregated to Indian fiscal years (April–March); Accenture’s quarters end a month earlier, so 11 of 12 months overlap. Before FY24 some firms lack constant-currency revenue, so the average covers four or five firms (hover for counts).</figcaption>
</figure>

<p>Three qualifiers apply. First, FY22–23 was a hiring boom, so part of the FY24 drop is a correction. Second, the drop was broad: headcount fell at five of the six firms in FY24. HCLTech, at +2.1%, was the exception. Third, the comparators slowed too. Accenture’s headcount grew 1.5% in FY24. Cognizant’s fell 0.9% in FY24 and 2.5% in FY25.</p>

<p>Smaller Indian firms did not follow. Table 1 compares four mid-tier firms (Persistent, Coforge, Mphasis and Hexaware) with the top six.</p>

<div class="table-wrap">
  <p class="table-cap"><b>Table 1.</b> Top six against the mid-tier four, growth in % (log ×100)</p>
  %%MIDTIER_TABLE%%
  <p class="table-note">Growth of summed USD revenue and of summed year-end headcount. Acquisitions included. Hexaware reports calendar years, each aligned to the Indian fiscal year ending three months later.</p>
</div>

<p>So this is not a uniform hit to Indian IT. Any explanation has to account for the largest vendors specifically. Four caveats apply. The mid-tier figures include acquisitions, though without Coforge the other three still grew revenue 10.9% in FY25. Mphasis and Hexaware count contractors in headcount. The mid-tier firms specialize in different segments from the top six. And they are small: their share of combined revenue rose only from 5.1% in FY21 to 7.3% in FY26, so they absorb a small part of the top six’s shortfall.</p>

<h2 id="explanations"><span class="num">3</span>Four explanations</h2>

<p>Four explanations could produce these facts. Each is defined by its mechanism.</p>

<ul class="scen">
  <li><b>S1</b>Client demand fell.</li>
  <li><b>S2</b>Labor per unit of work fell, and prices held. The firms kept the savings.</li>
  <li><b>S3</b>Labor per unit of work fell, and the savings went to clients as lower prices.</li>
  <li><b>S4</b>Work moved to other providers: clients’ own India offices (global capability centres, or GCCs), smaller vendors, or contractors.</li>
</ul>

<p>AI can drive S1 as well as S2 and S3, for example when clients use AI to do work in-house. It can also drive S4. So the question “is it AI?” does not map onto any one scenario. The useful question is which mechanism is at work. Table 2 lists what each predicts.</p>

<div class="table-wrap">
  <p class="table-cap"><b>Table 2.</b> What each explanation predicts</p>
  <table class="pred">
    <thead><tr><th></th><th>Revenue</th><th>Headcount</th><th>Residual*</th><th>Subcontracting share</th><th>Other providers</th></tr></thead>
    <tbody>
      <tr><th scope="row">S1 · demand fell</th><td><span class="arr dn" aria-label="down">↓</span></td><td><span class="arr dn" aria-label="down">↓</span></td><td>flat</td><td><span class="arr dn" aria-label="down">↓</span> or flat</td><td>slow too</td></tr>
      <tr><th scope="row">S2 · savings kept</th><td>flat</td><td><span class="arr dn" aria-label="down">↓</span></td><td><span class="arr up" aria-label="up">↑</span></td><td class="dim">—</td><td class="dim">—</td></tr>
      <tr><th scope="row">S3 · savings passed on</th><td><span class="arr dn" aria-label="down">↓</span></td><td><span class="arr dn" aria-label="down">↓</span></td><td>flat <span class="dim">(full pass-through)</span></td><td class="dim">—</td><td class="dim">—</td></tr>
      <tr><th scope="row">S4 · work moved</th><td><span class="arr dn" aria-label="down">↓</span></td><td><span class="arr dn" aria-label="down">↓</span></td><td>flat</td><td><span class="arr up" aria-label="up">↑</span> <span class="dim">(contractor variant)</span></td><td>grow</td></tr>
    </tbody>
  </table>
  <p class="table-note">* Revenue per employee, net of utilization (§4). A dash means no specific prediction.</p>
</div>

<h2 id="identity"><span class="num">4</span>What the identity can and can’t show</h2>

<p>Growth in revenue per employee splits into two parts:</p>

<div class="math" id="identity-eq"><span class="math-fallback"><i>g</i><sub>R/L</sub> = <i>g</i><sub>u</sub> + (<i>g</i><sub>p</sub> − <i>g</i><sub>a</sub>)</span></div>

<p>Here <i>g</i> is a growth rate, <i>R</i> is revenue, <i>L</i> is headcount, <i>u</i> is utilization (the share of staff billed to clients), <i>p</i> is the price per unit of work, and <i>a</i> is labor per unit of work. The term in brackets is the residual: revenue-per-employee growth net of utilization.</p>

<p>We observe <i>R</i> and <i>L</i> for all firms, and <i>u</i> for some. We do not observe <i>p</i>, <i>a</i> or the volume of work. Even so, the identity has content. Suppose AI cuts labor per unit by <i>e·d</i> and firms pass a share <i>φ</i> of the savings to clients. Then the AI part of the residual equals <span class="nw">(1 − <i>φ</i>)·<i>e·d</i></span>. If firms keep the savings (S2, <span class="nw"><i>φ</i> = 0</span>), the residual should rise by several points. If they pass all of it on (S3 with <span class="nw"><i>φ</i> = 1</span>), the residual does not move, and the observables match S1 exactly.</p>

<p>Table 3 shows the mean residual before and after FY24. There is no rise.</p>

<div class="table-wrap">
  <p class="table-cap"><b>Table 3.</b> Mean residual, % a year</p>
  %%RESID_TABLE%%
  <p class="table-note">Mean over firm-years; small grey numbers are firm-years. All firms with data: %%RESID_BEFORE%% before FY24; %%RESID_AFTER%% from FY24. Same firms: %%RESID_SAME%%.</p>
</div>

<p>Three limits apply. The test covers only Infosys, Wipro, Tech Mahindra and the LTI group; TCS and HCLTech do not report utilization. TCS’s revenue per employee accelerated, to +4.2% and +3.9% in FY24 and FY25 against +1.7% a year in FY16–20, but without utilization this cannot be decomposed. And Infosys’s FY24 residual of +6.6 may be a counting artifact: its utilization excludes trainees, its headcount includes them, and fresher intake collapsed.</p>

<p>The conclusion is therefore weak: there is no sign of retained savings on average at the four firms that can be tested. Separating S1 from S3 requires price data (§6).</p>

<h2 id="other"><span class="num">5</span>Other evidence</h2>

<h3>5a. Contractors</h3>

<p>If work moved to contractors, subcontracting costs should rise as a share of revenue. They fell. The share dropped at all six firms in FY24: at TCS from 9.5% to 6.6%, and at Tech Mahindra from 15.0% to 12.9%. It rose again at five of six in FY26, but it remains below its FY23 level everywhere.</p>

<figure class="wide" id="fig2">
  <div class="fig-panel">
    <div class="fig-top"><div class="fig-title">Subcontracting cost, % of revenue</div></div>
    <div id="chart2" class="chart" role="img" aria-label="Line chart: subcontracting cost as a share of revenue for six firms, FY20 to FY26. All six fall from FY23 to FY24."></div>
  </div>
  <figcaption><b>Figure 2.</b> Subcontracting cost as a share of revenue, FY20–FY26, as reported by each firm. LTIMindtree starts in FY22. The shaded band marks the FY23 → FY24 step. TCS’s line is fees to external consultants.</figcaption>
</figure>

<p>There is no evidence of a shift to contractors. This is a cost ratio, not contractor headcount, so it mixes contractor rates with volume.</p>

<h3>5b. Where the work went</h3>

<p>Beyond the mid-tier firms in §2, three sources bear on S4. RBI’s census of foreign-owned companies shows their information and communication exports rising from ₹6.54 to ₹8.45 lakh crore between FY22 and FY23. The US Bureau of Economic Analysis counts 893,000 people employed in professional services at US-owned affiliates in India in 2023 (preliminary), up from 598,000 in 2019. Naukri’s September 2026 job-postings index shows GCC postings up 4% and IT services postings down 4% on a year earlier. All three are suggestive at best. The first two include foreign-owned vendors as well as clients’ own centres, and postings are not hires. They are consistent with partial S4.</p>

<p>The pilot also compared how closely Indian firms tracked Accenture before and after 2023. That comparison turned out to be driven by the 2021–22 boom and bust, and is dropped.</p>

<h3>5c. What management said</h3>

<p>We extracted 2,087 management statements from 183 earnings-call transcripts of the six firms, Accenture and Cognizant. Two independent LLM coders classified each one; they agreed on 92% (κ = 0.87), and the pattern below holds under either coder.</p>

<figure class="wide" id="fig3">
  <div class="fig-panel">
    <div class="fig-top">
      <div class="fig-title">Statements per transcript</div>
      <div class="toggle-wrap"><span class="toggle-label">Codes</span><span class="toggle" role="group" aria-label="Coder">
        <button type="button" data-coder="c1" aria-pressed="true">Coder 1</button><button type="button" data-coder="c2" aria-pressed="false">Coder 2</button>
      </span></div>
    </div>
    <div id="chart3" class="chart" role="img" aria-label="Two bar-chart panels by half-year, 2021H1 to 2026H2: demand-weakness statements per transcript, and AI pass-through statements per transcript."></div>
  </div>
  <figcaption><b>Figure 3.</b> Management statements per transcript by calendar half-year, 2021H1–2026H2. Small numbers under the axis are transcript counts. 2026H2 is partial (8 transcripts) and drawn lighter. A and D came from different extraction passes, so compare trends within a panel, not levels across panels.</figcaption>
</figure>

<p>Demand-weakness statements (category A) peaked at 7.5–7.9 per transcript in 2023 and eased to 4.7–5.7 between 2024H2 and 2026H1. Statements that AI savings were going to clients (category D) were rare before mid-2024, at 0–0.3 per transcript, and rose to 0.6–1.6 after. Pass-through talk was added to demand talk; it did not replace it.</p>

%%Q_INFOSYS%%
%%Q_SEKSARIA%%
%%Q_KRITHIVASAN%%
%%Q_VIJAYAKUMAR%%

<p>Management chooses which explanations to give investors. These statements show what firms said, not what happened.</p>

<h2 id="prices"><span class="num">6</span>The price gap</h2>

<p>No price index covers Indian vendors. India has no IT services price index. The US Bureau of Labor Statistics lists computer systems design (NAICS 5415) among the industries its producer price index does not cover (<a href="https://www.bls.gov/ppi/fd-id/areas-of-noncoverage-in-the-ppi-system.htm">Areas of Noncoverage</a>).</p>

<p>The nearest proxies are weak. The BLS index for US data processing and hosting (PPI 518210) reprices actual contracts with fixed terms. It has grown between +0.3% and +3.2% a year since 2015 %%SPARK%%. It is a US domestic price and serves only as a proxy. ISG, a sourcing adviser, measures unit-price declines for a narrow slice of managed-services contracts, and says these declines have recently accelerated.</p>

<p>Infosys offers a bound for an earlier period. It reported billed person-months through FY20, and revenue per person-month equals <i>p</i>/<i>a</i>. <em>If labor per unit did not rise</em>, price growth was at most about −1% to −2% a year in FY15–17 and about 0% in FY18–20. That is an assumption, not an observation, and the series ends before the period in question.</p>

<p>Analyst estimates of AI deflation, such as those from Kotak and Jefferies, start from an assumed pass-through rate. They cannot test it.</p>

<h2 id="settle"><span class="num">7</span>What would settle it</h2>

<p>Four data items would separate the explanations (Table 4). None is public today in usable form.</p>

<div class="table-wrap">
  <p class="table-cap"><b>Table 4.</b> Data that would separate the explanations</p>
  <table class="items">
    <thead><tr><th>Data item</th><th>Who could collect it</th><th>Separates</th><th>Exists?</th></tr></thead>
    <tbody>
      <tr><th scope="row">Output price index for IT services</th><td>National statistics agency or RBI</td><td>S1 vs S3</td><td>No</td></tr>
      <tr><th scope="row">Billed effort (person-months)</th><td>Firms; SEBI could require it</td><td>S2 vs S1/S3, with revenue<sup>†</sup></td><td>Infosys until FY20, LTI until 2022</td></tr>
      <tr><th scope="row">GCC headcount by parent company</th><td>RBI census extension</td><td>S1 vs S4</td><td>No</td></tr>
      <tr><th scope="row">Role-level headcount by firm</th><td>Firms</td><td>S2/S3 vs S1</td><td>No</td></tr>
    </tbody>
  </table>
  <p class="table-note">† Revenue per billed person-month is <i>p</i>/<i>a</i>, the residual. It would extend the §4 test to TCS and HCLTech, but like the residual it cannot separate S1 from S3 under full pass-through.</p>
</div>

<p>The cheapest high-value step is the price index, since every other inference here is limited by its absence.</p>

<h2 id="limits"><span class="num">8</span>Limitations</h2>

<ol class="lim">
  <li>The sample is six large firms, plus four mid-tier firms in one comparison.</li>
  <li>TCS and HCLTech do not report utilization, so their revenue per employee cannot be decomposed.</li>
  <li>The data were collected with LLMs; a 30-point audit against source documents matched every value.</li>
  <li>Call statements were coded by two independent LLM coders and have not been validated by hand.</li>
  <!-- UPDATE after manual spot check of calls_spotcheck.csv -->
  <li>Management statements reflect management’s incentives.</li>
  <li>Acquisitions are not adjusted for.</li>
</ol>

<section class="appendix" id="appendix">
<h2>Appendix: data and methods</h2>

<details>
<summary>Sources</summary>
<div>
<p>Quarterly fact sheets, investor releases, annual reports, SEC 20-F and 6-K filings, and earnings-call transcripts from company investor-relations sites and SEC EDGAR. Mid-tier figures come from annual reports. External series: RBI Census on Foreign Liabilities and Assets; BEA data on US multinationals’ foreign affiliates; Naukri JobSpeak; BLS PPI. Every number traces to a file in the repository: %%REPO%%.</p>
</div>
</details>

<details>
<summary>Definitions</summary>
<div>
<ul>
  <li><b>Growth</b> is the log change ×100.</li>
  <li><b>Fiscal years</b> are Indian fiscal years (April–March). Quarterly year-on-year growth is aggregated to fiscal years with prior-year revenue weights; a fiscal-year value needs all four quarters.</li>
  <li><b>Headcount growth</b> is the mean of the four quarterly year-on-year changes, which approximates growth of average headcount.</li>
  <li><b>Comparators</b> are mapped to Indian fiscal years. Cognizant aligns exactly. Accenture’s quarters end in May, August, November and February, so 11 of 12 months overlap.</li>
  <li><b>Residual</b> is revenue-per-employee growth in constant currency minus the change in utilization, within each firm’s own utilization series.</li>
</ul>
</div>
</details>

<details>
<summary>Audit</summary>
<div>
<ul>
  <li><b>Spot-check:</b> 30 randomly drawn values were checked against the primary documents; 30 of 30 matched.</li>
  <li><b>Corrections:</b> LTI and Mindtree negative growth rates printed as “(x.x)%” had lost their sign (the parser is now fixed); Cognizant attrition used an annualized quarterly definition in two quarters instead of the trailing-twelve-month one; Accenture’s FY18 USD revenue growth mixed bases across the ASC 606 restatement and was corrected with like-for-like growth from the FY18 releases.</li>
  <li><b>Decisions:</b> the LTI business is counted once (LTI plus Mindtree through FY22, LTIMindtree from FY23); HCLTech’s divestiture is not adjusted, because no divested revenue figure was disclosed; Wipro growth observations that span level breaks are excluded.</li>
</ul>
</div>
</details>

<details>
<summary>Call coding</summary>
<div>
<p>Each statement gets one primary category:</p>
<ul>
  <li><b>A, demand weakness:</b> clients spending less, deferring or cutting discretionary work, for any reason.</li>
  <li><b>B, pricing stable:</b> management says prices or rates are holding, or denies AI deflation.</li>
  <li><b>C, pricing pressure, no AI link:</b> renewal discounts, competitive pricing or rate cuts with no AI named.</li>
  <li><b>D, AI savings passed to clients:</b> AI or automation savings explicitly given to clients through lower prices, smaller deals or productivity commitments.</li>
  <li><b>E, other or unclear:</b> anything else, including statements of demand strength.</li>
</ul>
<div class="table-wrap">
  <p class="table-cap"><b>Agreement between coders</b>, primary category</p>
  %%AGREE_TABLE%%
  <p class="table-note">“Coder 1 codes matched” is the share of coder 1’s codes in that category that coder 2 also assigned. κ is Cohen’s kappa for that category against the rest.</p>
</div>
<p><b>Extraction passes.</b> A pricing pass used a keyword screen and kept 389 statements about prices, renewals, deflation or passing productivity to clients (about 2 per call). A demand pass used a 12-family dictionary, read effectively every transcript in full, and kept 1,711 statements explaining revenue, deals or headcount through demand (about 9 per call). Merging and removing 13 cross-pass duplicates gives 2,087. Every quote is machine-checked as verbatim, from management only, with the speaker confirmed. A comes mostly from the demand pass and D from the pricing pass, which is why levels should not be compared across categories.</p>
</div>
</details>

<p class="footer">Built from the repository CSVs by <code>scripts/final/build_note.py</code>.</p>
</section>

</main>

<script src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.27.0/plotly.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
<script>
const DATA = %%DATA%%;
const C = { accent: "#235fa6", acn: "#7a7268", cog: "#aaa196", a: "#b0702a", d: "#6b4a92",
  ink: "#2a2318", ink2: "#5e5245", ink3: "#8a7d6d", rule: "#e6ddd0", rule2: "#cfc4b4",
  firms: ["#4d6f91", "#b8643f", "#5a9370", "#8f68a6", "#ae8a2c", "#c0607e"] };
const FONT = "'Source Sans 3', -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif";
const CONFIG = { displayModeBar: false, responsive: true, scrollZoom: false };
const YEARS = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026];
const FYL = YEARS.map(y => "FY" + String(y % 100).padStart(2, "0"));

function baseLayout(extra) {
  return Object.assign({
    font: { family: FONT, size: 12.5, color: C.ink2 },
    paper_bgcolor: "rgba(0,0,0,0)", plot_bgcolor: "rgba(0,0,0,0)",
    showlegend: false, dragmode: false,
    hoverlabel: { bgcolor: "#fffdf9", bordercolor: C.rule2, font: { family: FONT, size: 13, color: C.ink } },
  }, extra);
}
function axis(extra) {
  return Object.assign({ showgrid: false, zeroline: false, fixedrange: true, showline: true,
    linecolor: C.rule2, linewidth: 1, ticks: "outside", ticklen: 4, tickcolor: C.rule2,
    tickfont: { family: FONT, size: 12, color: C.ink2 } }, extra);
}
function tint(hex, a) {
  const n = parseInt(hex.slice(1), 16);
  return `rgba(${n >> 16},${(n >> 8) & 255},${n & 255},${a})`;
}
function width(el) { return el.getBoundingClientRect().width; }

/* ---------------- Figure 1 ---------------- */
let avgMode = "rw";
const F1 = [["rev_cc", "Revenue growth (cc)"], ["headcount", "Headcount growth"], ["rpe_cc", "Revenue per employee (cc)"]];
function fig1() {
  const el = document.getElementById("chart1");
  const narrow = width(el) < 640;
  const traces = [], shapes = [], annotations = [], layout = {};
  const gap = narrow ? 0.12 : 0.07;
  F1.forEach(([metric, title], i) => {
    const k = i === 0 ? "" : String(i + 1);
    const d = DATA.fig1[metric];
    const avgName = avgMode === "rw" ? "Top six (revenue-weighted)" : "Top six (simple)";
    const avg = d[avgMode];
    const series = [
      { y: avg.y, text: avg.text.map((t, j) => avg.n[j] ? `${t}  <span style="color:${C.ink3}">${avg.n[j]} firms</span>` : t),
        name: avgName, line: { color: C.accent, width: 2.75 } },
      { y: d.acn.y, text: d.acn.text, name: "Accenture", line: { color: C.acn, width: 2, dash: "dash" } },
      { y: d.cog.y, text: d.cog.text, name: "Cognizant", line: { color: C.cog, width: 2.25, dash: "dot" } },
    ];
    series.forEach(s => traces.push({ x: YEARS, y: s.y, text: s.text, name: s.name, mode: "lines+markers",
      line: s.line, marker: { size: 5, color: s.line.color }, connectgaps: false,
      xaxis: "x" + k, yaxis: "y" + k, hovertemplate: "%{text}<extra>" + s.name + "</extra>" }));
    let dom;
    if (narrow) { const h = (1 - 2 * gap) / 3; dom = { x: [0, 1], y: [1 - (i + 1) * h - i * gap, 1 - i * (h + gap)] }; }
    else { const w = (1 - 2 * gap) / 3; dom = { x: [i * (w + gap), i * (w + gap) + w], y: [0, 0.9] }; }
    layout["xaxis" + k] = axis({ domain: dom.x, anchor: "y" + k, range: [2015.5, 2026.5],
      tickvals: [2016, 2018, 2020, 2022, 2024, 2026], ticktext: ["FY16", "FY18", "FY20", "FY22", "FY24", "FY26"] });
    layout["yaxis" + k] = axis({ domain: dom.y, anchor: "x" + k, ticksuffix: "", nticks: 6 });
    shapes.push({ type: "rect", xref: "x" + k, yref: "y" + k + " domain", x0: 2023.5, x1: 2024.5, y0: 0, y1: 1,
      fillcolor: C.accent, opacity: 0.07, line: { width: 0 }, layer: "below" });
    shapes.push({ type: "line", xref: "x" + k + " domain", yref: "y" + k, x0: 0, x1: 1, y0: 0, y1: 0,
      line: { color: C.rule2, width: 1 }, layer: "below" });
    annotations.push({ text: title, xref: "x" + k + " domain", yref: "y" + k + " domain", x: 0, y: 1.02,
      xanchor: "left", yanchor: "bottom", showarrow: false, font: { family: FONT, size: 13.5, color: C.ink } });
  });
  const lay = baseLayout(Object.assign(layout, { shapes, annotations, hovermode: "x unified",
    height: narrow ? 720 : 330, margin: { l: 34, r: 8, t: narrow ? 26 : 10, b: 30 } }));
  Plotly.react(el, traces, lay, CONFIG);
  el.dataset.narrow = narrow;
}

/* ---------------- Figure 2 ---------------- */
function fig2() {
  const el = document.getElementById("chart2");
  const d = DATA.fig2;
  const traces = d.firms.map((f, i) => ({ x: d.x, y: f.y, text: f.text, name: f.name, mode: "lines+markers",
    line: { color: C.firms[i], width: 2 }, marker: { size: 6, color: C.firms[i] },
    hovertemplate: "%{text}<extra>" + f.name + "</extra>" }));
  const last = d.x[d.x.length - 1];
  const annotations = d.firms.map(f => ({ x: last, y: f.y[f.y.length - 1], xref: "x", yref: "y", text: f.name,
    xanchor: "left", xshift: 9, showarrow: false, font: { family: FONT, size: 12.5, color: C.ink2 } }));
  annotations.push({ x: 2023.5, y: 1, xref: "x", yref: "paper", yanchor: "bottom", text: "FY23 → FY24: fell at all six",
    showarrow: false, font: { family: FONT, size: 12, color: C.ink2 } });
  const lay = baseLayout({ height: 360, hovermode: "x unified", margin: { l: 34, r: 104, t: 24, b: 30 },
    xaxis: axis({ range: [2019.7, 2026.3], tickvals: d.x, ticktext: d.labels }),
    yaxis: axis({ range: [3.5, 16.5], ticksuffix: "%", dtick: 2 }),
    shapes: [{ type: "rect", xref: "x", yref: "paper", x0: 2023, x1: 2024, y0: 0, y1: 1, fillcolor: C.accent,
      opacity: 0.06, line: { width: 0 }, layer: "below" }],
    annotations });
  Plotly.react(el, traces, lay, CONFIG);
}

/* ---------------- Figure 3 ---------------- */
let coder = "c1";
function fig3() {
  const el = document.getElementById("chart3");
  const d = DATA.fig3[coder];
  const narrow = width(el) < 640;
  const last = d.half.length - 1;
  const ticks = d.half.map((h, i) => {
    const lab = narrow ? "’" + h.slice(2, 4) + "<br>" + h.slice(4) : h;
    return lab + "<br><span style='font-size:10.5px;color:" + C.ink3 + "'>" + d.n[i] + "</span>";
  });
  const mk = (cat, color, k, name) => ({
    x: d.half, y: d[cat].per, type: "bar", name, xaxis: "x" + k, yaxis: "y" + k,
    marker: { color: d.half.map((_, i) => i === last ? tint(color, 0.3) : color),
              line: { color, width: d.half.map((_, i) => i === last ? 1.5 : 0) } },
    customdata: d.half.map((h, i) => [d[cat].count[i], d.n[i], i === last ? " (partial)" : ""]),
    hovertemplate: "<b>%{x}%{customdata[2]}</b><br>" + name + ": %{y:.2f} per transcript<br>" +
      "<span style='color:" + C.ink3 + "'>%{customdata[0]} statements / %{customdata[1]} transcripts</span><extra></extra>",
  });
  const traces = [mk("A", C.a, "", "A · demand weakness"), mk("D", C.d, "2", "D · AI pass-through")];
  const ttl = (t, y) => ({ text: t, xref: "paper", yref: "paper", x: 0, y, xanchor: "left", yanchor: "bottom",
    showarrow: false, font: { family: FONT, size: 13.5, color: C.ink } });
  const lay = baseLayout({ height: narrow ? 470 : 440, bargap: 0.3, hovermode: "closest",
    margin: { l: 34, r: 8, t: 24, b: narrow ? 66 : 52 },
    xaxis: axis({ domain: [0, 1], anchor: "y", showticklabels: false, ticks: "", matches: "x2" }),
    yaxis: axis({ domain: [0.56, 1], anchor: "x", nticks: 5, rangemode: "tozero" }),
    xaxis2: axis({ domain: [0, 1], anchor: "y2", tickvals: d.half, ticktext: ticks, tickangle: 0,
      tickfont: { family: FONT, size: narrow ? 10.5 : 11.5, color: C.ink2 } }),
    yaxis2: axis({ domain: [0, 0.42], anchor: "x2", nticks: 5, rangemode: "tozero" }),
    annotations: [ttl("A · demand weakness", 1.01), ttl("D · AI pass-through", 0.45),
      { x: d.half[last], y: d.D.per[last], xref: "x2", yref: "y2", yanchor: "bottom", yshift: 4,
        text: "partial", showarrow: false, font: { family: FONT, size: 11, color: C.ink3 } }] });
  Plotly.react(el, traces, lay, CONFIG);
  el.dataset.narrow = narrow;
}

/* ---------------- wiring ---------------- */
function press(group, btn) {
  group.querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", b === btn ? "true" : "false"));
}
document.querySelectorAll("[data-avg]").forEach(b => b.addEventListener("click", () => {
  avgMode = b.dataset.avg; press(b.parentNode, b); fig1();
}));
document.querySelectorAll("[data-coder]").forEach(b => b.addEventListener("click", () => {
  coder = b.dataset.coder; press(b.parentNode, b); fig3();
}));

function drawAll() { fig1(); fig2(); fig3(); }
if (window.Plotly) drawAll();
let rt;
window.addEventListener("resize", () => {
  clearTimeout(rt);
  rt = setTimeout(() => {
    const n1 = String(width(document.getElementById("chart1")) < 640);
    if (n1 !== document.getElementById("chart1").dataset.narrow) fig1();
    const n3 = String(width(document.getElementById("chart3")) < 640);
    if (n3 !== document.getElementById("chart3").dataset.narrow) fig3();
  }, 150);
});

/* print: open the appendix and fit charts to the page width */
window.addEventListener("beforeprint", () => {
  document.querySelectorAll("details").forEach(d => { d.dataset.wasOpen = d.open; d.open = true; });
  ["chart1", "chart2", "chart3"].forEach(id => window.Plotly && Plotly.relayout(id, { width: 660 }));
});
window.addEventListener("afterprint", () => {
  document.querySelectorAll("details").forEach(d => { d.open = d.dataset.wasOpen === "true"; });
  ["chart1", "chart2", "chart3"].forEach(id => window.Plotly && Plotly.relayout(id, { width: null, autosize: true }));
});

if (window.katex) {
  katex.render("g_{R/L} = g_u + (g_p - g_a)", document.getElementById("identity-eq"),
    { displayMode: true, throwOnError: false });
}
</script>
</body>
</html>
"""


def main():
    data = {"fig1": fig1_data(), "fig2": fig2_data(), "fig3": fig3_data()}
    resid, before, after, same = residual_table()
    repo = f'<a href="{REPO_URL}">{REPO_URL.replace("https://", "")}</a>' if REPO_URL else "[repository link to be added]"
    page = (TEMPLATE
            .replace("%%DATA%%", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
            .replace("%%MIDTIER_TABLE%%", midtier_table())
            .replace("%%RESID_TABLE%%", resid)
            .replace("%%RESID_BEFORE%%", before)
            .replace("%%RESID_AFTER%%", after)
            .replace("%%RESID_SAME%%", same)
            .replace("%%AGREE_TABLE%%", agreement_table())
            .replace("%%SPARK%%", bls_sparkline())
            .replace("%%Q_INFOSYS%%", quote("infosys"))
            .replace("%%Q_SEKSARIA%%", quote("seksaria"))
            .replace("%%Q_KRITHIVASAN%%", quote("krithivasan"))
            .replace("%%Q_VIJAYAKUMAR%%", quote("vijayakumar"))
            .replace("%%REPO%%", repo))
    assert "%%" not in page, "unfilled placeholder"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(page) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
