"""Build the research note as one self-contained HTML page (docs/index.html) for GitHub Pages.

    python3 scripts/final/build_note.py

Chart data and the generated tables are read from the repo CSVs (nothing hand-typed):
  fact              output/final/table_A.csv                (rev_cc, headcount, rpe_cc; FY16-FY26)
  midtier           data/explore/midtier/midtier_vs_top6.csv, midtier_annual.csv
  verticals         data/tidy/panel_long.csv (top six), data/explore/midtier/vertical_mix_midtier.csv
  residual          output/final/table_A_firms.csv, table_B.csv
  subcontracting    output/final/fig2_data.csv
  calls             output/final/fig3_data.csv, fig3_data_coder2.csv
  bls               data/explore/prices/final_bls/ppi_518210_monthly.csv
  residual table    output/final/table_B.csv
  agreement table   output/final/calls_agreement.csv
The text of the note lives in note_text.md (see the comment at its top for the conventions); numbers in the
prose are typed there and checked by scripts/final/note_number_check.py (-> note_number_check.md).
External resources load only from CDNs: Plotly, KaTeX (cdnjs) and Google Fonts.
"""
import csv
import html
import json
import math
import re
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

S2_ILLUSTRATION = 4.0  # labor saving of 4% a year: the pilot's working figure (note_inputs.md §2), shown as an illustration


def series(values, nd=1):
    return {"y": [clean(v) for v in values], "text": [fmt(v, nd) for v in values]}


def midtier_fig_data():
    """Top six vs mid-tier four, and Persistent + Coforge alone (Mphasis and Hexaware count contractors)."""
    m = pd.read_csv(ROOT / "data/explore/midtier/midtier_vs_top6.csv").set_index("fiscal_year")
    a = pd.read_csv(ROOT / "data/explore/midtier/midtier_annual.csv")
    two = a[a.firm.isin(["persistent", "coforge"])]
    rev2 = two.pivot(index="aligned_fy", columns="firm", values="revenue_usd_mn").sum(axis=1, min_count=2)
    hc2 = two.pivot(index="aligned_fy", columns="firm", values="headcount").sum(axis=1, min_count=2)
    g = lambda s_: 100 * (s_ / s_.shift()).apply(lambda r: math.log(r) if pd.notna(r) else float("nan"))
    yrs = ["FY22", "FY23", "FY24", "FY25", "FY26"]
    return {"x": [2000 + int(y[2:]) for y in yrs], "labels": yrs,
            "rev": {"top": series(m.loc[yrs, "top6_rev_growth_logx100"]), "mid4": series(m.loc[yrs, "mid4_rev_growth_logx100"]),
                    "mid2": series(g(rev2).reindex(yrs))},
            "hc": {"top": series(m.loc[yrs, "top6_hc_growth_logx100"]), "mid4": series(m.loc[yrs, "mid4_hc_growth_logx100"]),
                   "mid2": series(g(hc2).reindex(yrs))}}


def residual_fig_data():
    f = pd.read_csv(FINAL / "table_A_firms.csv")
    f = f[~f.period.str.contains("Q1")]
    names = [("infosys", "Infosys"), ("hcltech", "HCLTech"), ("wipro", "Wipro"), ("techm", "Tech Mahindra"),
             ("lti_group", "LTI group")]
    firms = []
    for key, name in names:
        r = f[(f.firm == key) & f.residual.notna()]
        firms.append({"key": key, "name": name, "x": [2000 + int(p[2:]) for p in r.period],
                      "y": [clean(v) for v in r.residual], "text": [f"{p}: {fmt(v)}" for p, v in zip(r.period, r.residual)]})
    b = pd.read_csv(FINAL / "table_B.csv")
    b = b[b.metric == "residual"].set_index("window").mean_firm_years
    pre, post = float(b["FY16-FY23"]), float(b["FY24-FY26"])
    return {"firms": firms, "pre": pre, "post": post, "s2": pre + S2_ILLUSTRATION,
            "avgLabel": f"Average: {fmt(pre)} before FY24,<br>{fmt(post)} from FY24",
            "avgShort": f"Avg {fmt(pre)} / {fmt(post)}",
            "s2Label": f"S2 with a {S2_ILLUSTRATION:.0f}% labor saving<br>(illustration)", "s2Short": "S2 (illustration)"}


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
    return (f"<table><thead><tr><th>Firm set</th><th>FY16–23</th><th>FY16–23<br>excl. FY21</th>"
            f"<th>FY24–26</th></tr></thead><tbody>{body}</tbody></table>")


def agreement_table():
    a = pd.read_csv(FINAL / "calls_agreement.csv").set_index("category")
    names = {"A": "Demand weakness", "B": "Pricing stable", "C": "Pricing pressure without AI",
             "D": "AI savings passed to clients", "E": "Other or unclear"}
    body = ""
    for c in "ABCDE":
        r = a.loc[c]
        body += (f'<tr><th scope="row">{c} · {names[c]}</th><td>{int(r.n_coder1):,}</td><td>{int(r.n_coder2):,}</td>'
                 f"<td>{r.percent_agreement:.1f}%</td><td>{r.cohen_kappa:.2f}</td></tr>")
    o = a.loc["overall"]
    body += (f'<tr class="tot"><th scope="row">All statements</th><td>{int(o.n_coder1):,}</td><td>{int(o.n_coder2):,}</td>'
             f"<td>{o.percent_agreement:.1f}%</td><td>{o.cohen_kappa:.2f}</td></tr>")
    return ("<table><thead><tr><th>Category</th><th>Model 1</th><th>Model 2</th>"
            "<th>Model 1 codes matched</th><th>κ</th></tr></thead>"
            f"<tbody>{body}</tbody></table>")


VERTICAL_GROUP = {  # reported industry label -> chart group; "mixed" = reported only together with another group
    "fin": ["BFSI", "Financial services", "Financial Services", "Banking, Financial Services and Insurance",
            "Banking, Financial services & Insurance", "Banking and Financial Services (BFS)", "Insurance",
            "Banking and Financial Services", "Banking"],
    "tech": ["Communication & Media", "Technology & Services", "Communication", "Hi-Tech", "Technology and Communications",
             "Telecommunications, Media, Publishing & Entertainment", "Communications", "Hi-Tech and Media",
             "Software, Hi-Tech & Emerging Industries", "Technology Media and Telecom", "High Tech and Professional Services"],
    "health": ["Life Sciences & Healthcare", "Life Sciences", "Lifesciences & Healthcare", "Health",
               "Healthcare &  Life Sciences", "Healthcare & Life Sciences"],
    "mixed": ["Healthcare & HiTech", "Healthcare and Insurance"],
}
LABEL_GROUP = {lab: g for g, labs in VERTICAL_GROUP.items() for lab in labs}


def verticals_fig_data():
    """Revenue share by client industry: top six in Jan-Mar 2026 (latest vintage in panel_long), mid-tier FY26/CY25."""
    p = pd.read_csv(ROOT / "data/tidy/panel_long.csv", low_memory=False)
    v = p[(p.dim_type == "vertical") & (p.metric == "revenue_share") & (p.cal_q == "2026Q1") & (p.period_type == "quarter")]
    rows = []
    for key in ["tcs", "infosys", "hcltech", "wipro", "techm", "ltim"]:
        d = v[v.firm == key]
        d = d[d.doc_date == d.doc_date.max()]
        rows += [(key, r.dimension, float(r.value)) for r in d.itertuples()]
    m = pd.read_csv(ROOT / "data/explore/midtier/vertical_mix_midtier.csv")
    rows += [(r.firm, r.vertical_reported, float(r.share_pct)) for r in m.itertuples()]
    names = {"tcs": "TCS", "infosys": "Infosys", "hcltech": "HCLTech", "wipro": "Wipro", "techm": "Tech Mahindra",
             "ltim": "LTIMindtree", "persistent": "Persistent", "coforge": "Coforge", "mphasis": "Mphasis", "hexaware": "Hexaware"}
    out = {"firms": [], "groups": {"fin": [], "tech": [], "health": []}, "note": {"fin": [], "tech": [], "health": []}}
    for key, name in names.items():
        mine = [(lab, val) for f, lab, val in rows if f == key]
        assert abs(sum(v_ for _, v_ in mine) - 100) < 0.6, (key, sum(v_ for _, v_ in mine))
        out["firms"].append({"key": key, "name": name, "mid": key in ("persistent", "coforge", "mphasis", "hexaware")})
        mixed = [lab for lab, _ in mine if LABEL_GROUP.get(lab) == "mixed"]
        for g in ["fin", "tech", "health"]:
            parts = [(lab, val) for lab, val in mine if LABEL_GROUP.get(lab) == g]
            total = sum(val for _, val in parts)
            mixed_here = [lab for lab in mixed if (g == "health" and "ealth" in lab) or (g == "tech" and "Tech" in lab)
                          or (g == "fin" and "Insurance" in lab)]
            out["groups"][g].append(round(total, 2) if parts else None)
            note = " + ".join(f"{lab} {val:.1f}" for lab, val in parts)
            if mixed_here:
                note += ("; " if note else "") + "also in " + ", ".join(f"“{lab}”" for lab in mixed_here)
            out["note"][g].append(note or "not reported separately")
    return out


def bls_fig_data():
    # from the monthly index, not the 2-dp annual file, to avoid double rounding (2025 is 3.245, not 3.25)
    m = pd.read_csv(ROOT / "data/explore/prices/final_bls/ppi_518210_monthly.csv")
    avg = m.groupby("year").value.mean()
    ja = m[m.month <= 8].groupby("year").value.mean()
    vals = [(y, 100 * (avg[y] / avg[y - 1] - 1)) for y in range(2015, 2026)] + [(2026, 100 * (ja[2026] / ja[2025] - 1))]
    return {"x": [y for y, _ in vals], "y": [round(v, 3) for _, v in vals],
            "text": [f"{y}{' (Jan–Aug, year on year)' if y == 2026 else ''}: {fmt(v)}%" for y, v in vals]}


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


FIGURES = {
    "fact": """<figure class="wide" id="fig-fact">
  <div class="fig-panel">
    <div class="fig-top">
      <div class="legend" aria-hidden="true"><span><i style="border-color:var(--accent);border-top-style:solid;border-top-width:3px"></i>Top six (average)</span><span><i style="border-color:var(--acn);border-top-style:dashed;border-top-width:2.5px"></i>Accenture</span><span><i style="border-color:var(--cog);border-top-style:dotted;border-top-width:3px"></i>Cognizant</span></div>
      <div class="toggle-wrap"><span class="toggle-label">Average</span><span class="toggle" role="group" aria-label="Top-six average">
        <button type="button" data-avg="rw" aria-pressed="true">Revenue-weighted</button><button type="button" data-avg="simple" aria-pressed="false">Simple</button>
      </span></div>
    </div>
    <div id="chart-fact" class="chart" role="img" aria-label="Three panels: revenue growth, headcount growth and revenue-per-employee growth for the top-six average, Accenture and Cognizant, FY16 to FY26."></div>
  </div>
  <figcaption>{caption}</figcaption>
</figure>""",
    "midtier": """<figure class="wide" id="fig-midtier">
  <div class="fig-panel">
    <div class="fig-top">
      <div class="legend" aria-hidden="true"><span><i style="border-color:var(--accent);border-top-style:solid;border-top-width:3px"></i>Top six</span><span><i style="border-color:var(--mid);border-top-style:solid;border-top-width:2.5px"></i>Mid-tier four</span><span><i style="border-color:var(--mid);border-top-style:dashed;border-top-width:2px"></i>Persistent and Coforge only</span></div>
    </div>
    <div id="chart-midtier" class="chart" role="img" aria-label="Two panels: revenue growth and year-end headcount growth, FY22 to FY26, for the top six, the four mid-tier firms, and Persistent and Coforge alone."></div>
  </div>
  <figcaption>{caption}</figcaption>
</figure>""",
    "verticals": """<figure class="wide" id="fig-verticals">
  <div class="fig-panel">
    <div class="fig-top">
      <div class="legend" aria-hidden="true"><span><span class="sw" style="background:var(--accent)"></span>Top six</span><span><span class="sw" style="background:var(--mid)"></span>Mid-tier four</span></div>
    </div>
    <div id="chart-verticals" class="chart" role="img" aria-label="Three bar-chart panels: share of revenue from financial services; from technology, media and telecom clients; and from healthcare and life sciences, for each of the ten firms."></div>
  </div>
  <figcaption>{caption}</figcaption>
</figure>""",
    "residual": """<figure class="wide" id="fig-residual">
  <div class="fig-panel">
    <div class="fig-top">
      <div class="legend" aria-hidden="true"><span><span class="sw" style="background:#b8643f"></span>Infosys</span><span><span class="sw" style="background:#5a9370"></span>HCLTech</span><span><span class="sw" style="background:#8f68a6"></span>Wipro</span><span><span class="sw" style="background:#ae8a2c"></span>Tech Mahindra</span><span><span class="sw" style="background:#c0607e"></span>LTI group</span><span><i style="border-color:var(--accent);border-top-style:solid;border-top-width:3px"></i>Average</span></div>
    </div>
    <div id="chart-residual" class="chart" role="img" aria-label="Dot chart of the residual for each firm and year, FY16 to FY26, with the average before and after FY24 and an illustrative line for what S2 would predict."></div>
  </div>
  <figcaption>{caption}</figcaption>
</figure>""",
    "subcontracting": """<figure class="wide" id="fig-subcontracting">
  <div class="fig-panel">
    <div class="fig-top"><div class="fig-title">Subcontracting cost, % of revenue</div></div>
    <div id="chart-subcon" class="chart" role="img" aria-label="Line chart: subcontracting cost as a share of revenue for six firms, FY20 to FY26. All six fall from FY23 to FY24."></div>
  </div>
  <figcaption>{caption}</figcaption>
</figure>""",
    "calls": """<figure class="wide" id="fig-calls">
  <div class="fig-panel">
    <div class="fig-top">
      <div class="fig-title">Statements per transcript</div>
      <div class="toggle-wrap"><span class="toggle-label">Codes from</span><span class="toggle" role="group" aria-label="Which model's codes">
        <button type="button" data-coder="c1" aria-pressed="true">Model 1</button><button type="button" data-coder="c2" aria-pressed="false">Model 2</button>
      </span></div>
    </div>
    <div id="chart-calls" class="chart" role="img" aria-label="Two bar-chart panels by half-year, 2021 to 2026: demand-weakness statements per transcript, and AI pass-through statements per transcript."></div>
  </div>
  <figcaption>{caption}</figcaption>
</figure>""",
    "bls": """<figure class=" narrowfig" id="fig-bls">
  <div class="fig-panel">
    <div class="fig-top"><div class="fig-title">US data processing and hosting prices (BLS PPI 518210), % change on a year earlier</div></div>
    <div id="chart-bls" class="chart" role="img" aria-label="Bar chart: annual change in the BLS producer price index for data processing and hosting, 2015 to 2026. Every year is positive."></div>
  </div>
  <figcaption>{caption}</figcaption>
</figure>""",
}

GENERATED_TABLES = {"residual": residual_table, "agreement": agreement_table}


def smarten(text):
    """Curly quotes in text, leaving HTML tags alone."""
    out = []
    for part in re.split(r"(<[^>]+>)", text):
        if part.startswith("<"):
            out.append(part)
            continue
        part = re.sub(r'(^|[\s(\[—–])"', "\\1“", part)
        part = part.replace('"', "”")
        part = re.sub(r"(^|[\s(\[—–])'", "\\1‘", part)
        out.append(part.replace("'", "’"))
    return "".join(out)


def inline(s, tokens):
    s = s.replace("\\*", "\x00")
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
    s = smarten(s).replace("\x00", "*")
    return re.sub(r"\{\{(\w+)\}\}", lambda m: tokens[m.group(1)], s)


def cell(c, tokens):
    h = inline(c.strip(), tokens)
    h = re.sub(r"([↓↑])", r'<span class="arr">\1</span>', h)
    h = re.sub(r"(\([^)]*\))", r'<span class="dim">\1</span>', h)
    return '<span class="dim">—</span>' if h == "—" else h


def pipe_table(lines, tokens):
    rows = [[c for c in l.strip().strip("|").split("|")] for l in lines if not re.match(r"^\|?\s*:?-{3,}", l)]
    head, body = rows[0], rows[1:]
    arrows = any("↓" in c or "↑" in c for r in body for c in r)
    h = "".join(f"<th>{cell(c, tokens)}</th>" for c in head)
    b = "".join("<tr>" + f'<th scope="row">{cell(r[0], tokens)}</th>' +
                "".join(f"<td>{cell(c, tokens)}</td>" for c in r[1:]) + "</tr>" for r in body)
    return f'<table class="{"pred" if arrows else "items"}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>'


def block(kind, name, lines, tokens):
    if kind == "figure":
        cap = " ".join(l.strip() for l in lines if l.strip())
        return FIGURES[name].replace("{caption}", inline(cap, tokens))
    if "---" in [l.strip() for l in lines]:
        i = [l.strip() for l in lines].index("---")
        top, note_lines = lines[:i], lines[i + 1:]
    else:
        top, note_lines = lines, []
    cap = [l for l in top if l.strip() and not l.strip().startswith("|")]
    tbl = [l for l in top if l.strip().startswith("|")]
    table = GENERATED_TABLES[name]() if name else pipe_table(tbl, tokens)
    note = " ".join(l.strip() for l in note_lines if l.strip())
    return ('<div class="table-wrap">' + f'<p class="table-cap">{inline(" ".join(cap), tokens)}</p>' + table +
            (f'<p class="table-note">{inline(note, tokens)}</p>' if note else "") + "</div>")


def render_md(text, tokens):
    """Small Markdown renderer for note_text.md; returns (front matter dict, body HTML)."""
    front = {}
    if text.startswith("---"):
        fm, text = text[3:].split("\n---", 1)
        for line in fm.strip().splitlines():
            k, v = line.split(":", 1)
            front[k.strip()] = v.strip()
    lines = text.splitlines()
    out, para, i = [], [], 0
    in_appendix = details_open = False

    def flush():
        if para:
            out.append(f"<p>{inline(' '.join(para), tokens)}</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        st = line.strip()
        if not st:
            flush(); i += 1; continue
        if st.startswith("<!--"):
            flush()
            j = i
            while "-->" not in lines[j]:
                j += 1
            if "HOW THIS FILE WORKS" not in "\n".join(lines[i:j + 1]):  # the editing guide stays out of the page
                out.append("\n".join(lines[i:j + 1]))
            i = j + 1; continue
        if st.startswith("## "):
            flush()
            title = st[3:]
            if title.lower().startswith("appendix"):
                in_appendix = True
                out.append(f'<section class="appendix" id="appendix">\n<h2>{inline(title, tokens)}</h2>')
            else:
                m = re.match(r"(\d+)\.\s+(.*)", title)
                num, t = (m.group(1), m.group(2)) if m else ("", title)
                slug = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
                out.append(f'<h2 id="{slug}">' + (f'<span class="num">{num}</span>' if num else "") +
                           f"{inline(t, tokens)}</h2>")
            i += 1; continue
        if st.startswith("### "):
            flush()
            if in_appendix:
                if details_open:
                    out.append("</div>\n</details>")
                out.append(f"<details>\n<summary>{inline(st[4:], tokens)}</summary>\n<div>")
                details_open = True
            else:
                out.append(f"<h3>{inline(st[4:], tokens)}</h3>")
            i += 1; continue
        if st == "$$":
            flush()
            j = i + 1
            while lines[j].strip() != "$$":
                j += 1
            tex = " ".join(l.strip() for l in lines[i + 1:j])
            out.append(f'<div class="math" data-tex="{html.escape(tex)}"><span class="math-fallback">{html.escape(tex)}</span></div>')
            i = j + 1; continue
        if st.startswith(":::"):
            flush()
            parts = st[3:].split()
            j = i + 1
            while lines[j].strip() != ":::":
                j += 1
            out.append(block(parts[0], parts[1] if len(parts) > 1 else None, lines[i + 1:j], tokens))
            i = j + 1; continue
        m = re.fullmatch(r"\{\{quote (\w+)\}\}", st)
        if m:
            flush(); out.append(quote(m.group(1))); i += 1; continue
        if re.match(r"^(- |\d+\. )", st):
            flush()
            ordered = bool(re.match(r"^\d+\. ", st))
            items = []
            while i < len(lines) and (re.match(r"^(- |\d+\. )", lines[i].strip()) or lines[i].strip().startswith("<!--")):
                l = lines[i].strip()
                items.append(l if l.startswith("<!--") else re.sub(r"^(- |\d+\. )", "", l))
                i += 1
            if not ordered and all(re.match(r"^\*\*S\d\*\*", it) for it in items):
                lis = "".join(f"<li><b>{it[2:4]}</b>{inline(it[6:].strip(), tokens)}</li>" for it in items)
                out.append(f'<ul class="scen">{lis}</ul>')
            else:
                lis = "".join(it if it.startswith("<!--") else f"<li>{inline(it, tokens)}</li>" for it in items)
                out.append(f'<ol class="lim">{lis}</ol>' if ordered else f"<ul>{lis}</ul>")
            continue
        para.append(st)
        i += 1
    flush()
    if details_open:
        out.append("</div>\n</details>")
    if in_appendix:
        out.append('<p class="footer">Built from <code>note_text.md</code> and the repository CSVs by '
                   "<code>scripts/final/build_note.py</code>.</p>\n</section>")
    return front, "\n\n".join(out)


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%%TITLE%%</title>
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
figure.narrowfig .fig-panel { padding-bottom: 4px; }
.fig-panel { background: var(--panel); border: 1px solid var(--rule); border-radius: 6px; padding: 16px 16px 8px; }
.fig-top { display: flex; flex-wrap: wrap; gap: 10px 22px; align-items: center; justify-content: space-between; margin-bottom: 4px; }
.fig-title { font-family: var(--sans); font-weight: 600; font-size: 15px; color: var(--ink); }
.legend { display: flex; flex-wrap: wrap; gap: 4px 16px; font-family: var(--sans); font-size: 13.5px; color: var(--ink); }
.legend .sw { display: inline-block; width: 10px; height: 10px; border-radius: 50%; vertical-align: -1px; margin-right: 6px; }
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
%%BODY%%
</main>

<script src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.27.0/plotly.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
<script>
const DATA = %%DATA%%;
const C = { accent: "#235fa6", acn: "#7a7268", cog: "#aaa196", a: "#b0702a", d: "#6b4a92",
  ink: "#2a2318", ink2: "#5e5245", ink3: "#8a7d6d", rule: "#e6ddd0", rule2: "#cfc4b4",
  mid: "#2f8a57" };
const FONT = "'Source Sans 3', -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif";
const CONFIG = { displayModeBar: false, responsive: true, scrollZoom: false };
const YEARS = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026];

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

const FIRM = { tcs: "#4d6f91", infosys: "#b8643f", hcltech: "#5a9370", wipro: "#8f68a6", techm: "#ae8a2c",
  ltim: "#c0607e", lti_group: "#c0607e" };
const FYTICKS = { tickvals: [2016, 2018, 2020, 2022, 2024, 2026], ticktext: ["FY16", "FY18", "FY20", "FY22", "FY24", "FY26"] };
function band(k, x0, x1) {
  return { type: "rect", xref: "x" + k, yref: "y" + k + " domain", x0, x1, y0: 0, y1: 1,
    fillcolor: C.accent, opacity: 0.07, line: { width: 0 }, layer: "below" };
}
function zero(k) {
  return { type: "line", xref: "x" + k + " domain", yref: "y" + k, x0: 0, x1: 1, y0: 0, y1: 0,
    line: { color: C.rule2, width: 1 }, layer: "below" };
}
function panelTitle(k, text) {
  return { text, xref: "x" + k + " domain", yref: "y" + k + " domain", x: 0, y: 1.02, xanchor: "left",
    yanchor: "bottom", showarrow: false, font: { family: FONT, size: 13.5, color: C.ink } };
}
function domains(n, i, narrow, gap) {
  if (narrow) { const h = (1 - (n - 1) * gap) / n; return { x: [0, 1], y: [1 - (i + 1) * h - i * gap, 1 - i * (h + gap)] }; }
  const w = (1 - (n - 1) * gap) / n; return { x: [i * (w + gap), i * (w + gap) + w], y: [0, 0.9] };
}
function lineTrace(x, s, name, line, k) {
  return { x, y: s.y, text: s.text, name, mode: "lines+markers", line, marker: { size: 5, color: line.color },
    connectgaps: false, xaxis: "x" + k, yaxis: "y" + k, hovertemplate: "%{text}<extra>" + name + "</extra>" };
}

/* ---------------- The fact: top six vs Accenture and Cognizant ---------------- */
let avgMode = "rw";
const FACT = [["rev_cc", "Revenue growth (cc)"], ["headcount", "Headcount growth"], ["rpe_cc", "Revenue per employee (cc)"]];
function figFact() {
  const el = document.getElementById("chart-fact");
  const narrow = width(el) < 640, gap = narrow ? 0.12 : 0.07;
  const traces = [], shapes = [], annotations = [], layout = {};
  FACT.forEach(([metric, title], i) => {
    const k = i === 0 ? "" : String(i + 1), d = DATA.fact[metric], avg = d[avgMode];
    const avgName = avgMode === "rw" ? "Top six (revenue-weighted)" : "Top six (simple)";
    const avgText = { y: avg.y, text: avg.text.map((t, j) => avg.n[j] ? `${t}  <span style="color:${C.ink3}">${avg.n[j]} firms</span>` : t) };
    traces.push(lineTrace(YEARS, avgText, avgName, { color: C.accent, width: 2.75 }, k));
    traces.push(lineTrace(YEARS, d.acn, "Accenture", { color: C.acn, width: 2, dash: "dash" }, k));
    traces.push(lineTrace(YEARS, d.cog, "Cognizant", { color: C.cog, width: 2.25, dash: "dot" }, k));
    const dom = domains(3, i, narrow, gap);
    layout["xaxis" + k] = axis(Object.assign({ domain: dom.x, anchor: "y" + k, range: [2015.5, 2026.5] }, FYTICKS));
    layout["yaxis" + k] = axis({ domain: dom.y, anchor: "x" + k, nticks: 6 });
    shapes.push(band(k, 2023.5, 2024.5), zero(k));
    annotations.push(panelTitle(k, title));
  });
  Plotly.react(el, traces, baseLayout(Object.assign(layout, { shapes, annotations, hovermode: "x unified",
    height: narrow ? 720 : 330, margin: { l: 34, r: 8, t: narrow ? 26 : 10, b: 30 } })), CONFIG);
  el.dataset.narrow = narrow;
}

/* ---------------- Mid-tier firms ---------------- */
function figMidtier() {
  const el = document.getElementById("chart-midtier"), d = DATA.midtier;
  const narrow = width(el) < 640, gap = narrow ? 0.16 : 0.09;
  const traces = [], shapes = [], annotations = [], layout = {};
  [["rev", "Revenue growth (US dollars)"], ["hc", "Headcount growth (year-end)"]].forEach(([m, title], i) => {
    const k = i === 0 ? "" : "2";
    traces.push(lineTrace(d.x, d[m].top, "Top six", { color: C.accent, width: 2.75 }, k));
    traces.push(lineTrace(d.x, d[m].mid4, "Mid-tier four", { color: C.mid, width: 2.5 }, k));
    traces.push(lineTrace(d.x, d[m].mid2, "Persistent and Coforge only", { color: C.mid, width: 1.75, dash: "dash" }, k));
    const dom = domains(2, i, narrow, gap);
    layout["xaxis" + k] = axis({ domain: dom.x, anchor: "y" + k, range: [2021.6, 2026.4], tickvals: d.x, ticktext: d.labels });
    layout["yaxis" + k] = axis({ domain: dom.y, anchor: "x" + k, nticks: 6 });
    shapes.push(band(k, 2023.5, 2024.5), zero(k));
    annotations.push(panelTitle(k, title));
  });
  Plotly.react(el, traces, baseLayout(Object.assign(layout, { shapes, annotations, hovermode: "x unified",
    height: narrow ? 560 : 320, margin: { l: 34, r: 8, t: narrow ? 26 : 10, b: 30 } })), CONFIG);
  el.dataset.narrow = narrow;
}

/* ---------------- Client industries ---------------- */
function figVerticals() {
  const el = document.getElementById("chart-verticals"), d = DATA.verticals;
  const narrow = width(el) < 640, gap = narrow ? 0.1 : 0.05;
  const names = d.firms.map(f => f.name).reverse();
  const colors = d.firms.map(f => f.mid ? C.mid : C.accent).reverse();
  const traces = [], annotations = [], layout = {};
  [["fin", "Financial services"], ["tech", "Tech, media and telecom"], ["health", "Healthcare and life sciences"]].forEach(([g, title], i) => {
    const k = i === 0 ? "" : String(i + 1);
    const vals = d.groups[g].slice().reverse(), notes = d.note[g].slice().reverse();
    traces.push({ type: "bar", orientation: "h", x: vals.map(v => v === null ? 0 : v), y: names, xaxis: "x" + k, yaxis: "y" + k,
      marker: { color: colors }, customdata: notes,
      hovertemplate: "<b>%{y}</b>: %{x:.1f}%<br><span style='color:" + C.ink3 + "'>%{customdata}</span><extra></extra>" });
    vals.forEach((v, j) => { if (v === null) annotations.push({ x: 0, y: names[j], xref: "x" + k, yref: "y" + k,
      text: "not separate", xanchor: "left", xshift: 4, showarrow: false, font: { family: FONT, size: 11, color: C.ink3 } }); });
    const dom = domains(3, i, narrow, gap);
    layout["xaxis" + k] = axis({ domain: dom.x, anchor: "y" + k, range: [0, 70], ticksuffix: "%", dtick: 20 });
    layout["yaxis" + k] = axis({ domain: dom.y, anchor: "x" + k, showticklabels: narrow || i === 0, ticks: "",
      automargin: true, showline: false });
    annotations.push(panelTitle(k, title));
  });
  Plotly.react(el, traces, baseLayout(Object.assign(layout, { annotations, bargap: 0.3, hovermode: "closest",
    height: narrow ? 900 : 360, margin: { l: 96, r: 8, t: narrow ? 26 : 10, b: 30 },
    shapes: [0, 1, 2].map(i => ({ type: "line", xref: "paper", yref: "y" + (i ? i + 1 : ""), x0: 0, x1: 1,
      y0: 3.5, y1: 3.5, line: { color: C.rule2, width: 1, dash: "dot" } })) })), CONFIG);
  el.dataset.narrow = narrow;
}

/* ---------------- Residual by firm ---------------- */
function figResidual() {
  const el = document.getElementById("chart-residual"), d = DATA.residual;
  const narrow = width(el) < 640;
  const traces = d.firms.map(f => ({ x: f.x, y: f.y, text: f.text, name: f.name, mode: "markers",
    marker: { size: 9, color: FIRM[f.key], line: { color: "#fffdf9", width: 1.5 } },
    hovertemplate: "%{text}<extra>" + f.name + "</extra>" }));
  const seg = (x0, x1, y, color, w, dash) => ({ type: "line", xref: "x", yref: "y", x0, x1, y0: y, y1: y,
    line: { color, width: w, dash } });
  const side = (y, text, color) => ({ x: 1, y, xref: "paper", yref: "y", text, showarrow: false, xanchor: "left",
    xshift: 8, align: "left", font: { family: FONT, size: narrow ? 11 : 12, color } });
  const lay = baseLayout({ height: narrow ? 380 : 360, hovermode: "closest", margin: { l: 34, r: narrow ? 96 : 200, t: 10, b: 30 },
    xaxis: axis(Object.assign({ range: [2015.5, 2026.5] }, FYTICKS)), yaxis: axis({ nticks: 7 }),
    shapes: [band("", 2023.5, 2026.5), zero(""), seg(2015.6, 2023.4, d.pre, C.accent, 2.5, "solid"),
      seg(2023.6, 2026.4, d.post, C.accent, 2.5, "solid"), seg(2023.6, 2026.4, d.s2, C.ink3, 1.75, "dash")],
    annotations: [side((d.pre + d.post) / 2, narrow ? d.avgShort : d.avgLabel, C.ink),
      side(d.s2, narrow ? d.s2Short : d.s2Label, C.ink2)] });
  Plotly.react(el, traces, lay, CONFIG);
  el.dataset.narrow = narrow;
}

/* ---------------- Subcontracting ---------------- */
function figSubcon() {
  const el = document.getElementById("chart-subcon"), d = DATA.subcon;
  const traces = d.firms.map(f => ({ x: d.x, y: f.y, text: f.text, name: f.name, mode: "lines+markers",
    line: { color: FIRM[f.key], width: 2 }, marker: { size: 6, color: FIRM[f.key] },
    hovertemplate: "%{text}<extra>" + f.name + "</extra>" }));
  const last = d.x[d.x.length - 1];
  const annotations = d.firms.map(f => ({ x: last, y: f.y[f.y.length - 1], xref: "x", yref: "y", text: f.name,
    xanchor: "left", xshift: 9, showarrow: false, font: { family: FONT, size: 12.5, color: C.ink2 } }));
  annotations.push({ x: 2023.5, y: 1, xref: "x", yref: "paper", yanchor: "bottom", text: "FY23 → FY24: fell at all six",
    showarrow: false, font: { family: FONT, size: 12, color: C.ink2 } });
  Plotly.react(el, traces, baseLayout({ height: 360, hovermode: "x unified", margin: { l: 34, r: 104, t: 24, b: 30 },
    xaxis: axis({ range: [2019.7, 2026.3], tickvals: d.x, ticktext: d.labels }),
    yaxis: axis({ range: [3.5, 16.5], ticksuffix: "%", dtick: 2 }),
    shapes: [{ type: "rect", xref: "x", yref: "paper", x0: 2023, x1: 2024, y0: 0, y1: 1, fillcolor: C.accent,
      opacity: 0.06, line: { width: 0 }, layer: "below" }], annotations }), CONFIG);
}

/* ---------------- Earnings calls ---------------- */
let coder = "c1";
function figCalls() {
  const el = document.getElementById("chart-calls"), d = DATA.calls[coder];
  const narrow = width(el) < 640, last = d.half.length - 1;
  const ticks = d.half.map((h, i) => (narrow ? "’" + h.slice(2, 4) + "<br>" + h.slice(4) : h) +
    "<br><span style='font-size:10.5px;color:" + C.ink3 + "'>" + d.n[i] + "</span>");
  const mk = (cat, color, k, name) => ({
    x: d.half, y: d[cat].per, type: "bar", name, xaxis: "x" + k, yaxis: "y" + k,
    marker: { color: d.half.map((_, i) => i === last ? tint(color, 0.3) : color),
              line: { color, width: d.half.map((_, i) => i === last ? 1.5 : 0) } },
    customdata: d.half.map((h, i) => [d[cat].count[i], d.n[i], i === last ? " (partial)" : ""]),
    hovertemplate: "<b>%{x}%{customdata[2]}</b><br>" + name + ": %{y:.2f} per transcript<br>" +
      "<span style='color:" + C.ink3 + "'>%{customdata[0]} statements / %{customdata[1]} transcripts</span><extra></extra>",
  });
  const ttl = (t, y) => ({ text: t, xref: "paper", yref: "paper", x: 0, y, xanchor: "left", yanchor: "bottom",
    showarrow: false, font: { family: FONT, size: 13.5, color: C.ink } });
  Plotly.react(el, [mk("A", C.a, "", "A · demand weakness"), mk("D", C.d, "2", "D · AI pass-through")], baseLayout({
    height: narrow ? 470 : 440, bargap: 0.3, hovermode: "closest", margin: { l: 34, r: 8, t: 24, b: narrow ? 66 : 52 },
    xaxis: axis({ domain: [0, 1], anchor: "y", showticklabels: false, ticks: "", matches: "x2" }),
    yaxis: axis({ domain: [0.56, 1], anchor: "x", nticks: 5, rangemode: "tozero" }),
    xaxis2: axis({ domain: [0, 1], anchor: "y2", tickvals: d.half, ticktext: ticks, tickangle: 0,
      tickfont: { family: FONT, size: narrow ? 10.5 : 11.5, color: C.ink2 } }),
    yaxis2: axis({ domain: [0, 0.42], anchor: "x2", nticks: 5, rangemode: "tozero" }),
    annotations: [ttl("A · demand weakness", 1.01), ttl("D · AI pass-through", 0.45),
      { x: d.half[last], y: d.D.per[last], xref: "x2", yref: "y2", yanchor: "bottom", yshift: 4,
        text: "partial", showarrow: false, font: { family: FONT, size: 11, color: C.ink3 } }] }), CONFIG);
  el.dataset.narrow = narrow;
}

/* ---------------- BLS producer price index ---------------- */
function figBls() {
  const el = document.getElementById("chart-bls"), d = DATA.bls, last = d.x.length - 1;
  Plotly.react(el, [{ x: d.x, y: d.y, text: d.text, textposition: "none", type: "bar", hovertemplate: "%{text}<extra></extra>",
    marker: { color: d.x.map((_, i) => i === last ? tint(C.acn, 0.35) : C.acn), line: { color: C.acn, width: d.x.map((_, i) => i === last ? 1.5 : 0) } } }],
    baseLayout({ height: 220, bargap: 0.35, hovermode: "closest", margin: { l: 30, r: 8, t: 8, b: 28 },
      xaxis: axis({ tickvals: [2015, 2017, 2019, 2021, 2023, 2025], ticktext: ["2015", "2017", "2019", "2021", "2023", "2025"] }),
      yaxis: axis({ rangemode: "tozero", ticksuffix: "%", nticks: 4 }) }), CONFIG);
}

/* ---------------- wiring ---------------- */
const CHARTS = { "chart-fact": figFact, "chart-midtier": figMidtier, "chart-verticals": figVerticals, "chart-residual": figResidual,
  "chart-subcon": figSubcon, "chart-calls": figCalls, "chart-bls": figBls };
function press(group, btn) {
  group.querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", b === btn ? "true" : "false"));
}
document.querySelectorAll("[data-avg]").forEach(b => b.addEventListener("click", () => {
  avgMode = b.dataset.avg; press(b.parentNode, b); figFact();
}));
document.querySelectorAll("[data-coder]").forEach(b => b.addEventListener("click", () => {
  coder = b.dataset.coder; press(b.parentNode, b); figCalls();
}));
function drawAll() { Object.entries(CHARTS).forEach(([id, fn]) => document.getElementById(id) && fn()); }
if (window.Plotly) drawAll();
let rt;
window.addEventListener("resize", () => {
  clearTimeout(rt);
  rt = setTimeout(() => Object.entries(CHARTS).forEach(([id, fn]) => {
    const el = document.getElementById(id);
    if (el && el.dataset.narrow !== undefined && String(width(el) < 640) !== el.dataset.narrow) fn();
  }), 150);
});

/* print: open the appendix and fit charts to the page width */
window.addEventListener("beforeprint", () => {
  document.querySelectorAll("details").forEach(d => { d.dataset.wasOpen = d.open; d.open = true; });
  Object.keys(CHARTS).forEach(id => window.Plotly && document.getElementById(id) && Plotly.relayout(id, { width: 660 }));
});
window.addEventListener("afterprint", () => {
  document.querySelectorAll("details").forEach(d => { d.open = d.dataset.wasOpen === "true"; });
  Object.keys(CHARTS).forEach(id => window.Plotly && document.getElementById(id) &&
    Plotly.relayout(id, { width: null, autosize: true }));
});

if (window.katex) {
  document.querySelectorAll(".math[data-tex]").forEach(el =>
    katex.render(el.dataset.tex, el, { displayMode: true, throwOnError: false }));
}
</script>
</body>
</html>
"""


def main():
    data = {"fact": fig1_data(), "midtier": midtier_fig_data(), "verticals": verticals_fig_data(),
            "residual": residual_fig_data(),
            "subcon": fig2_data(), "calls": fig3_data(), "bls": bls_fig_data()}
    repo = f'<a href="{REPO_URL}">{REPO_URL.replace("https://", "")}</a>' if REPO_URL else "[repository link to be added]"
    tokens = {"repo": repo}
    front, body = render_md((ROOT / "note_text.md").read_text(encoding="utf-8"), tokens)
    header = (f"<header>\n  <h1>{inline(front['title'], tokens)}</h1>\n"
              f"  <p class=\"byline\">{byline(front['byline'])}</p>\n"
              f"  <p class=\"thanks\">{inline(front['thanks'], tokens)}</p>\n</header>")
    page = (TEMPLATE
            .replace("%%TITLE%%", html.escape(front["title"].split("?")[0] + "?" if "?" in front["title"] else front["title"]))
            .replace("%%BODY%%", header + "\n\n" + body)
            .replace("%%DATA%%", json.dumps(data, ensure_ascii=False, separators=(",", ":"))))
    assert "%%" not in page, "unfilled placeholder"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(page) / 1024:.0f} KB)")


def byline(text):
    """Last '·' item of the byline is shown as a tag (e.g. 'Pilot note')."""
    parts = [p.strip() for p in text.split("·")]
    return " · ".join(parts[:-1]) + f' · <span class="tag">{html.escape(parts[-1])}</span>'


if __name__ == "__main__":
    main()
